#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_short_answers.py —— 由来源总账（manifest）驱动生成各卷 answers_short.tex。

**值取自生成的 answers.tex，正确性由结构化比较担保**：简答版与解析版必须逐字给出
同一个答案，所以答案值直接从 `answers.tex` 的 `\\gksolhead` / `\\gkanswer` 提取；再把
它与唯一事实源 `_答案要点.md`（经 `solution_sources.parse_answer_points()` + 行内
转换）做**逐条结构化比较**——题号、小问号、值三者全等才允许写文件。任何一处对不上
都在写文件之前失败：一份自称"速查"却与解析版不一致的表比没有更糟。

第三路核对：`_答案要点.md` 开头的「答案速查表」是同一份文档里独立转写的一行字母，
与逐题答案行不一致同样硬失败（缺表也失败——少一路核对就该显形，而不是静默降级）。

**版块顺序按题号，绝不按 JSON 键序**：`structure` 是 dict，序列化过一次
`sort_keys=True` 之后键序就成了字典序（单选/填空/多选/解答），照抄即错位。这里一律
按各版块的起始题号排序。

**先校验后原子写**：全批目标先在内存生成并全部通过校验，才以**一个** Task 1 `content`
事务提交。任何一卷失败都不落盘（失败零覆盖），崩溃后由 `RepoLock` 的恢复补完。
事务只读输入 = manifest 整文件 + 每卷 `_答案要点.md` 与 `answers.tex` + 提取器/转换器/
结构表/本工具四份源码。

`structure`（各版块题号区间）不在 manifest 里，唯一的静态表是 `generate_projects.py`
的 `INDEX_METADATA`——直接引它，避免再抄一份出来分叉；该文件因此也是只读输入。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from generate_projects import INDEX_METADATA
from manifest import file_sha256, load_manifest
from solution_sources import SolutionSourceError, parse_answer_points
from transaction import RepoLock, Transaction

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent                       # math-gaokao-latex
sys.path.insert(0, str(PROJECT_ROOT.parent / "math-gaokao-2017-2026" / "tools"))
import md2tex  # noqa: E402  行内 MD→LaTeX 转换，与 answers.tex 走同一套规则

PROJECT_RELATIVE = "math-gaokao-latex"
MANIFEST_TARGET = PROJECT_RELATIVE + "/source-manifest.json"
TOOL_SOURCE_TARGET = PROJECT_RELATIVE + "/tools/make_short_answers.py"
RENDERER_SOURCE_TARGET = PROJECT_RELATIVE + "/tools/solution_sources.py"
STRUCTURE_SOURCE_TARGET = PROJECT_RELATIVE + "/tools/generate_projects.py"
CONVERTER_SOURCE_TARGET = "math-gaokao-2017-2026/tools/md2tex.py"
DEFAULT_MANIFEST = PROJECT_ROOT / "source-manifest.json"

CHOICE_GROUPS = ("选择题", "单选题", "多选题")
SEE_SOLUTION = "见解析版"

_SOLUTION_HEAD = re.compile(r"^\\gksolhead\{(\d+)\}\{")
# 生成答案块转成 LaTeX 后的两种形态：`**答案：X**` 独立段落走 \gkanswer；答案值里含
# `*` 时转换器的 ANSLINE 认不出，退化成 \textbf。两种都是落地的最终答案。
_ANSWER_TEX = re.compile(
    r"^\\(?:gkanswer|textbf)\{答案(?:[（(](\d+)[）)])?[：:](.*)\}$"
)
_CHOICE_LETTERS = re.compile(r"^([A-D]+)")
_QUICK_ROW = "| 答案"
# 行内转换不碰配图，故映射为空；严格模式让未配对 $ 之类的告警直接失败。
_INLINE_CONTEXT = md2tex.ConversionContext(figure_map={}, strict=True)


class ShortAnswerError(ValueError):
    """提取、比较或渲染失败；抛出即代表本次运行一个字节都没落盘。"""


@dataclass(frozen=True)
class AnswerRecord:
    """一条最终答案：题号 + 小问号（整题答案为 None）+ LaTeX 值。"""

    number: int
    subpart: Optional[int]
    value: str


@dataclass(frozen=True)
class ShortAnswerSources:
    """一卷的生成输入：manifest 身份 + 答案规范源 + 生成的 answers.tex + 版块结构。"""

    paper_id: str
    project_dir: str
    title: str
    question_count: int
    answer_key: str          # 仓库相对
    answers_tex: str         # 仓库相对
    structure: Tuple[Tuple[str, int, int], ...]


@dataclass(frozen=True)
class ShortAnswerResult:
    paper_id: str
    project_dir: str
    targets: Mapping[str, bytes]
    inputs: Tuple[str, ...]


# ---------------------------------------------------------------- 提取与比较


def parse_generated_answers_tex(text: str) -> Tuple[AnswerRecord, ...]:
    """从生成的 answers.tex 逐题取出最终答案块，按出现顺序返回。"""
    records: List[AnswerRecord] = []
    current: Optional[int] = None
    for line in text.split("\n"):
        head = _SOLUTION_HEAD.match(line)
        if head is not None:
            current = int(head.group(1))
            continue
        match = _ANSWER_TEX.match(line)
        if match is None:
            continue
        if current is None:
            raise ShortAnswerError(f"answers.tex 里出现了不属于任何题的答案块：{line}")
        subpart = match.group(1)
        records.append(AnswerRecord(
            number=current,
            subpart=int(subpart) if subpart is not None else None,
            value=match.group(2),
        ))
    return tuple(records)


def _converted(value: str) -> str:
    try:
        return md2tex.convert_inline(value, _INLINE_CONTEXT).text
    except md2tex.ConversionError as error:
        raise ShortAnswerError("行内转换告警：%s" % "；".join(error.warnings)) from error


def expected_answer_records(answer_key_text: str) -> Tuple[AnswerRecord, ...]:
    """把 `_答案要点.md` 折算成与 answers.tex 同一口径的答案序列。

    渲染顺序与 `solution_sources._render_answer_paragraphs()` 一致：没有小问集合时
    整题一条，否则按小问号升序逐条，缺最终答案的小问用诚实占位。
    """
    try:
        points = parse_answer_points(answer_key_text)
    except SolutionSourceError as error:
        raise ShortAnswerError(str(error)) from error
    records: List[AnswerRecord] = []
    for point in points:
        if not point.subparts:
            records.append(AnswerRecord(
                number=point.number, subpart=None,
                value=_converted(point.answers[0][1]),
            ))
            continue
        for subpart in point.subparts:
            value = point.answer_for(subpart)
            records.append(AnswerRecord(
                number=point.number, subpart=subpart,
                value=_converted(SEE_SOLUTION if value is None else value),
            ))
    return tuple(records)


def _record_label(record: AnswerRecord) -> str:
    if record.subpart is None:
        return "第 %d 题" % record.number
    return "第 %d 题第 (%d) 问" % (record.number, record.subpart)


def compare_generated_answers(
    answers_tex_text: str, answer_key_text: str
) -> Tuple[str, ...]:
    """结构化比较：answers.tex 的答案序列必须与答案要点折算出的序列逐条全等。"""
    produced = parse_generated_answers_tex(answers_tex_text)
    expected = expected_answer_records(answer_key_text)
    problems: List[str] = []
    produced_map = {(item.number, item.subpart): item.value for item in produced}
    expected_map = {(item.number, item.subpart): item.value for item in expected}
    if len(produced_map) != len(produced):
        problems.append("answers.tex 里有重复的答案块键")
    for key in sorted(set(produced_map) | set(expected_map), key=lambda k: (k[0], k[1] or 0)):
        record = AnswerRecord(number=key[0], subpart=key[1], value="")
        if key not in expected_map:
            problems.append("%s：answers.tex 多出一个答案块 %r"
                            % (_record_label(record), produced_map[key]))
        elif key not in produced_map:
            problems.append("%s：answers.tex 缺答案块，答案要点写的是 %r"
                            % (_record_label(record), expected_map[key]))
        elif produced_map[key] != expected_map[key]:
            problems.append("%s：answers.tex 为 %r，答案要点为 %r"
                            % (_record_label(record), produced_map[key], expected_map[key]))
    return tuple(problems)


def merge_answer_records(records: Sequence[AnswerRecord]) -> Dict[int, str]:
    """把答案序列折成逐题一行的速查文本；分问用「(k) …」以中文分号连接。"""
    grouped: Dict[int, List[AnswerRecord]] = {}
    for record in records:
        grouped.setdefault(record.number, []).append(record)
    merged: Dict[int, str] = {}
    for number, items in grouped.items():
        if len(items) == 1 and items[0].subpart is None:
            merged[number] = items[0].value
            continue
        if any(item.subpart is None for item in items):
            raise ShortAnswerError(f"第 {number} 题混用了整题答案与小问答案")
        # 各分问段末的句号在拼接前剥掉，避免 PDF 里出现「。；」连排。
        merged[number] = "；".join(
            "(%d) %s" % (item.subpart, item.value.rstrip("。"))
            for item in sorted(items, key=lambda item: item.subpart)
        )
    return merged


# ---------------------------------------------------------------- 速查表核对


def parse_quick_table(answer_key_text: str, count: int) -> Optional[Tuple[str, ...]]:
    """取「答案速查表」里的前 count 个字母；行数不足或没有表返回 None。"""
    cells: List[str] = []
    for line in answer_key_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(_QUICK_ROW):
            cells += [cell.strip() for cell in stripped.strip("|").split("|")][1:]
    return tuple(cells[:count]) if len(cells) >= count else None


def choice_letters(
    structure: Sequence[Tuple[str, int, int]], answers: Mapping[int, str]
) -> Tuple[Tuple[int, str], ...]:
    """按题号顺序取出各选择题的答案字母；非字母形是硬错误。"""
    found: List[Tuple[int, str]] = []
    for name, low, high in _ordered(structure):
        if name not in CHOICE_GROUPS:
            continue
        for number in range(low, high + 1):
            if number not in answers:
                raise ShortAnswerError(f"第 {number} 题没有答案，无法渲染{name}")
            match = _CHOICE_LETTERS.match(answers[number])
            if match is None:
                raise ShortAnswerError(
                    "第 %d 题属于%s，答案却不是字母形：%s"
                    % (number, name, answers[number][:40])
                )
            found.append((number, match.group(1)))
    return tuple(found)


def cross_check_quick_table(
    answer_key_text: str,
    structure: Sequence[Tuple[str, int, int]],
    answers: Mapping[int, str],
) -> Tuple[str, ...]:
    """第三路核对：答案要点开头的速查表与逐题答案行必须逐格一致。"""
    letters = choice_letters(structure, answers)
    quick = parse_quick_table(answer_key_text, len(letters))
    if quick is None:
        return ("答案要点缺「答案速查表」或字母数不足 %d，第三路核对无法进行" % len(letters),)
    problems = [
        "第 %d 题速查表=%s、逐题答案行=%s" % (number, table, row)
        for (number, row), table in zip(letters, quick) if table != row
    ]
    return tuple(problems)


# ---------------------------------------------------------------- 渲染


def _ordered(
    structure: Sequence[Tuple[str, int, int]]
) -> Tuple[Tuple[str, int, int], ...]:
    """一律按起始题号排序：dict 的键序在 `sort_keys=True` 之后就是字典序，不可信。"""
    return tuple(sorted(structure, key=lambda item: (item[1], item[2], item[0])))


def normalize_structure(
    structure: Mapping[str, Sequence[int]]
) -> Tuple[Tuple[str, int, int], ...]:
    groups: List[Tuple[str, int, int]] = []
    for name, span in structure.items():
        bounds = list(span)
        if len(bounds) != 2:
            raise ShortAnswerError(f"版块 {name} 的题号区间必须是两个整数：{span}")
        groups.append((name, int(bounds[0]), int(bounds[1])))
    return _ordered(groups)


def _table(numbers: Sequence[int], letters: Sequence[str]) -> str:
    head = " & ".join(str(number) for number in numbers)
    body = " & ".join(letters)
    return ("\\begin{center}\\begin{tabular}{c" + "c" * len(numbers) + "}\n"
            "\\toprule\n题号 & " + head + " \\\\\n\\midrule\n"
            "答案 & " + body + " \\\\\n\\bottomrule\n"
            "\\end{tabular}\\end{center}")


def render_short_answers(
    title: str,
    answer_key_relative: str,
    structure: Mapping[str, Sequence[int]],
    answers: Mapping[int, str],
) -> str:
    """渲染一卷的 answers_short.tex 全文。"""
    groups = normalize_structure(structure)
    covered: set = set()
    for _, low, high in groups:
        covered.update(range(low, high + 1))
    if covered != set(answers):
        raise ShortAnswerError(
            "版块覆盖的题号 %s 与已知答案的题号 %s 不一致"
            % (sorted(covered), sorted(answers))
        )
    letters = dict(choice_letters(groups, answers))

    parts: List[str] = []
    for name, low, high in groups:
        numbers = list(range(low, high + 1))
        if name in CHOICE_GROUPS:
            parts.append(
                "\\gkpart{" + name + "}\n"
                + _table(numbers, [letters[number] for number in numbers])
            )
            continue
        lines = ["\\gkpart{" + name + "}", "\\begin{itemize}[leftmargin=2.6em]"]
        for number in numbers:
            lines.append("  \\item[\\textbf{%d.}] %s" % (number, answers[number]))
        lines.append("\\end{itemize}")
        parts.append("\n".join(lines))

    return (
        "%% answers_short.tex —— %s · 简短答案速查\n"
        "%% 由 tools/make_short_answers.py 自 answers.tex 的 \\gksolhead/\\gkanswer 提取，\n"
        "%% 并与 %s 逐题比对后生成，勿手改（改源 MD 后重跑）。\n\n"
        "\\begin{gknotice}\n"
        "\\textbf{使用说明}：本节只给最终答案便于快速核对，完整推导见解析版。"
        "答案为编写者独立推导，\\textbf{非官方标准答案}。\n"
        "\\end{gknotice}\n\n" % (title, answer_key_relative)
    ) + "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------- 仓库与选择


def _repository_root(path: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(Path(path).resolve()), "rev-parse", "--show-toplevel"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return Path(result.stdout.strip()).resolve()


def _relative_to_repo(root: Path, path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise ShortAnswerError(f"路径不在仓库内：{path}") from error


def _read_text(path: Path) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ShortAnswerError(f"无法读取 {path}：{error}") from error


def _required_sha256(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise ShortAnswerError(f"只读输入缺失：{relative}")
    return file_sha256(path)


def paper_sources(
    paper: Mapping[str, Any], metadata: Mapping[str, Mapping[str, Any]]
) -> ShortAnswerSources:
    directory = paper["project_dir"]
    static = metadata.get(directory)
    if static is None:
        raise ShortAnswerError(f"结构表缺少试卷目录：{directory}")
    return ShortAnswerSources(
        paper_id=paper["paper_id"],
        project_dir=directory,
        title=paper["title"],
        question_count=paper["question_count"],
        answer_key=paper["source_files"]["answer_key"],
        answers_tex="%s/%s/answers.tex" % (PROJECT_RELATIVE, directory),
        structure=normalize_structure(static["structure"]),
    )


def _select(
    manifest: Mapping[str, Any],
    selector: str,
    value: Optional[str],
    metadata: Mapping[str, Mapping[str, Any]],
) -> Tuple[ShortAnswerSources, ...]:
    papers = {paper["paper_id"]: paper for paper in manifest["papers"]}
    if selector == "all":
        return tuple(paper_sources(paper, metadata) for paper in manifest["papers"])
    if selector == "paper":
        if value not in papers:
            raise ShortAnswerError(f"未知 paper_id：{value}")
        return (paper_sources(papers[value], metadata),)
    if selector == "batch":
        batches = [item for item in manifest["batches"] if item["batch_id"] == value]
        if len(batches) != 1:
            raise ShortAnswerError(f"未知批次：{value}")
        selected = []
        for paper_id in batches[0]["paper_ids"]:
            if paper_id not in papers:
                raise ShortAnswerError(f"批次 {value} 引用了不存在的 paper_id：{paper_id}")
            selected.append(paper_sources(papers[paper_id], metadata))
        return tuple(selected)
    raise ShortAnswerError(f"未知选择器：{selector}")


# ---------------------------------------------------------------- 单卷生成


def generate_short_answers(
    repo_root: Path, sources: ShortAnswerSources
) -> Tuple[ShortAnswerResult, Tuple[str, ...]]:
    """在内存里生成本卷 answers_short.tex；返回 (结果, 三路核对发现的问题)。"""
    root = Path(repo_root)
    answers_tex = _read_text(root / sources.answers_tex)
    answer_key = _read_text(root / sources.answer_key)
    empty = ShortAnswerResult(
        paper_id=sources.paper_id, project_dir=sources.project_dir,
        targets={}, inputs=(),
    )

    def labelled(items: Sequence[str]) -> Tuple[str, ...]:
        return tuple("%s: %s" % (sources.paper_id, item) for item in items)

    problems: List[str] = list(compare_generated_answers(answers_tex, answer_key))
    covered: set = set()
    for _, low, high in sources.structure:
        covered.update(range(low, high + 1))
    if covered != set(range(1, sources.question_count + 1)):
        problems.append(
            "版块覆盖的题号 %s 与题量 %d 不一致"
            % (sorted(covered), sources.question_count)
        )
    # 前两道核对没过就别再往下走：答案序列本身就对不上时，字母核对只会刷屏。
    if problems:
        return empty, labelled(problems)

    answers = merge_answer_records(parse_generated_answers_tex(answers_tex))
    problems.extend(cross_check_quick_table(answer_key, sources.structure, answers))
    if problems:
        return empty, labelled(problems)

    text = render_short_answers(
        sources.title,
        sources.answer_key,
        {name: (low, high) for name, low, high in sources.structure},
        answers,
    )
    target = "%s/%s/answers_short.tex" % (PROJECT_RELATIVE, sources.project_dir)
    return (
        ShortAnswerResult(
            paper_id=sources.paper_id,
            project_dir=sources.project_dir,
            targets={target: text.encode("utf-8")},
            inputs=(sources.answer_key, sources.answers_tex),
        ),
        (),
    )


# ---------------------------------------------------------------- 原子提交


def commit_short_answer_results(
    repo_root: Path,
    manifest_path: Path,
    results: Sequence[ShortAnswerResult],
    event_hook: Any = None,
) -> Dict[str, Any]:
    """把全批目标放进**一个** `content` 事务提交；全等则跳过，不做空事务。"""
    root = Path(repo_root)
    manifest_relative = _relative_to_repo(root, Path(manifest_path))
    if manifest_relative != MANIFEST_TARGET:
        raise ShortAnswerError(
            f"manifest 必须是 {MANIFEST_TARGET}，实际 {manifest_relative}"
        )

    inputs: Dict[str, Optional[str]] = {
        manifest_relative: _required_sha256(root, manifest_relative)
    }
    for relative in (
        TOOL_SOURCE_TARGET, RENDERER_SOURCE_TARGET,
        STRUCTURE_SOURCE_TARGET, CONVERTER_SOURCE_TARGET,
    ):
        inputs[relative] = _required_sha256(root, relative)

    targets: Dict[str, bytes] = {}
    for result in results:
        for relative in result.inputs:
            inputs[relative] = _required_sha256(root, relative)
        for relative, value in result.targets.items():
            if relative in targets:
                raise ShortAnswerError(f"批内目标路径重复：{relative}")
            targets[relative] = value

    overlap = sorted(set(inputs) & set(targets))
    if overlap:
        raise ShortAnswerError(f"只读输入与写目标重叠：{overlap}")

    unchanged = all(
        (root / relative).is_file() and (root / relative).read_bytes() == value
        for relative, value in targets.items()
    )
    if unchanged:
        return {"written": False, "targets": sorted(targets)}

    transaction = Transaction(root, event_hook=event_hook)
    transaction.prepare("content", targets, inputs)
    transaction.commit()
    return {"written": True, "targets": sorted(targets)}


# ---------------------------------------------------------------- 驱动


def run(
    manifest_path: Path,
    selector: str,
    value: Optional[str] = None,
    write: bool = False,
    index_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
    event_hook: Any = None,
) -> Dict[str, Any]:
    """生成一批简答；`write=False` 只比对不落盘，`write=True` 先全过再一次性提交。"""
    manifest_path = Path(manifest_path).resolve()
    metadata = INDEX_METADATA if index_metadata is None else index_metadata
    root = _repository_root(manifest_path.parent)
    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        selected = _select(manifest, selector, value, metadata)

        problems: List[str] = []
        results: List[ShortAnswerResult] = []
        for sources in selected:
            try:
                result, found = generate_short_answers(root, sources)
            except ShortAnswerError as error:
                if write:
                    raise
                problems.append("%s: %s" % (sources.paper_id, error))
                continue
            if found:
                problems.extend(found)
                continue
            results.append(result)

        report: Dict[str, Any] = {
            "papers": [result.paper_id for result in results],
            "problems": problems,
            "written": False,
            "targets": [],
        }
        if write:
            if problems:
                raise ShortAnswerError("；".join(problems))
            report.update(
                commit_short_answer_results(root, manifest_path, results, event_hook)
            )
            return report

        for result in results:
            for relative, expected in sorted(result.targets.items()):
                path = root / relative
                if not path.is_file() or path.read_bytes() != expected:
                    problems.append(f"{relative} 与生成结果不一致")
        report["targets"] = sorted(
            key for result in results for key in result.targets
        )
        return report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="由来源总账与生成的 answers.tex 生成各卷简短答案速查"
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--all", action="store_true", help="全部试卷")
    selector.add_argument("--batch", metavar="BATCH_ID", help="按批次")
    selector.add_argument("--paper", metavar="PAPER_ID", help="按 manifest paper_id")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="校验全过后原子写入")
    mode.add_argument("--check", action="store_true", help="只读比对，绝不落盘")
    return parser


def selection(arguments: argparse.Namespace) -> Tuple[str, Optional[str]]:
    if arguments.all:
        return "all", None
    if arguments.batch is not None:
        return "batch", arguments.batch
    return "paper", arguments.paper


def main(
    argv: Optional[Sequence[str]] = None,
    index_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> int:
    """退出码契约：0 全过、1 校验失败或输入无效、2 命令行用法错（argparse）。

    `index_metadata` 不是命令行开关，只是与 `run()` 同一个注入缝——夹具仓库里的虚构
    试卷不在生产结构表里。
    """
    arguments = _parser().parse_args(argv)
    selector, value = selection(arguments)
    try:
        report = run(
            Path(arguments.manifest), selector, value,
            write=arguments.write, index_metadata=index_metadata,
        )
    except ValueError as error:
        print("✗", error)
        return 1
    for problem in report["problems"]:
        print("  ✗", problem)
    if report["problems"]:
        print("\n== 校验失败：%d 项 ==" % len(report["problems"]))
        return 1
    if arguments.write:
        print(
            "✓ %d 套试卷，%s%d 份简答"
            % (
                len(report["papers"]),
                "已写入 " if report["written"] else "无需改动 ",
                len(report["targets"]),
            )
        )
    else:
        print("✓ %d 套试卷的简答与生成结果一致" % len(report["papers"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

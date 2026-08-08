#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_editions.py —— 由来源总账（manifest）与四份模板生成各卷四版本壳文件。

  试题版.tex   只含题目（questions.tex），供测试练习；
  解析版.tex   题目 + 参考答案与详细解析（answers.tex）；
  简答版.tex   题目 + 简短答案速查（answers_short.tex），供快速核对；
  印刷版.tex   题目 + 解析的紧凑排版（五号字、窄边距、紧列表），适合打印。

**版式在模板里，装配在这里**：四份 `templates/<版本>.tex.tpl` 各自持有完整壳文本，
只留五个固定占位符（`PLACEHOLDERS`）。模板里出现名单外的 `@@…@@`、或少写一个必需
占位符，都是硬错误——静默留一个未替换的 `@@TITLE@@` 在壳里，XeLaTeX 照样能编译，
错误会一路印进 PDF。印刷版的紧凑版式属于该版本的版式，整段写在它自己的模板里，
不做成第六个占位符。

**输入矩阵是冻结的**（`EDITION_INPUTS`）：试题版 questions；解析版 questions+answers；
简答版 questions+answers_short；印刷版 questions+answers。`render_body()` 每次都要
自证渲染出的 `\\input` 序列与矩阵逐项相等——简答版一旦 `\\input{answers}` 就悄悄变成
了解析版，而 PDF 看上去仍然「有内容」。

**先校验后原子写**：全批 84 个壳先在内存生成，模板、身份与矩阵输入全部通过后，才以
**一个** Task 1 `content` 事务提交。任何一处失败都不落盘（失败零覆盖），中途崩溃由
`RepoLock` 的恢复把事务补完，绝不留下半套壳。事务只读输入 = manifest 整文件 + 四份
模板 + 本工具源码 + 矩阵引用的三份共享 TeX。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from manifest import file_sha256, load_manifest
from transaction import RepoLock, Transaction

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent                       # math-gaokao-latex

PROJECT_RELATIVE = "math-gaokao-latex"
MANIFEST_TARGET = PROJECT_RELATIVE + "/source-manifest.json"
TOOL_SOURCE_TARGET = PROJECT_RELATIVE + "/tools/make_editions.py"
TEMPLATE_RELATIVE = PROJECT_RELATIVE + "/templates"
DEFAULT_MANIFEST = PROJECT_ROOT / "source-manifest.json"

EDITIONS: Tuple[str, ...] = ("试题版", "解析版", "简答版", "印刷版")
PLACEHOLDERS: Tuple[str, ...] = (
    "@@CLASS_OPTIONS@@", "@@PAPER_ID@@", "@@TITLE@@", "@@EDITION@@", "@@BODY@@",
)
# 大小写都收进来：`@@body@@` 这种写错大小写的占位符必须被判为未知，而不是当普通文本
# 原样留在壳里。
_PLACEHOLDER_RE = re.compile(r"@@[A-Za-z_]+@@")
_INPUT_RE = re.compile(r"\\input\{([^{}]*)\}")

# 印刷版用五号字，其余三版用小四；紧凑版式的其余项写在印刷版模板里。
CLASS_OPTIONS: Mapping[str, str] = {
    "试题版": "zihao=-4, a4paper",
    "解析版": "zihao=-4, a4paper",
    "简答版": "zihao=-4, a4paper",
    "印刷版": "zihao=5, a4paper",
}
# 冻结的输入矩阵：版本 -> 依次 \input 的共享 TeX（不含扩展名）。
EDITION_INPUTS: Mapping[str, Tuple[str, ...]] = {
    "试题版": ("questions",),
    "解析版": ("questions", "answers"),
    "简答版": ("questions", "answers_short"),
    "印刷版": ("questions", "answers"),
}


class EditionError(ValueError):
    """模板、身份或输入矩阵校验失败；抛出即代表本次运行一个字节都没落盘。"""


@dataclass(frozen=True)
class BodySection:
    """正文里的一节：书签 + 可选居中标题 + 一条 `\\input`。"""

    lead: str            # 本节之前的分隔（分页 / 分隔线 / 无）
    bookmark: str
    anchor: str
    heading: str         # 空串表示本节不排居中标题
    heading_size: str
    gap: str             # 居中标题与 \input 之间的留白
    source: str          # \input 的文件名，即输入矩阵成员


_QUESTIONS = BodySection(
    lead="", bookmark="试题", anchor="sec:q",
    heading="", heading_size="", gap="", source="questions",
)
# 解析版/简答版换页起新章；印刷版省纸，解析紧随试题，只用一条分隔线。
_SOLUTIONS = BodySection(
    lead="\\clearpage\n", bookmark="参考答案与详细解析", anchor="sec:s",
    heading="参考答案与详细解析", heading_size="Large", gap="\\medskip",
    source="answers",
)
_SHORT = BodySection(
    lead="\\clearpage\n", bookmark="答案速查", anchor="sec:a",
    heading="答案速查", heading_size="Large", gap="\\medskip",
    source="answers_short",
)
_COMPACT_SOLUTIONS = BodySection(
    lead="\\par\\bigskip\\hrule\\bigskip\n", bookmark="参考答案与详细解析",
    anchor="sec:s", heading="参考答案与详细解析", heading_size="large",
    gap="\\smallskip", source="answers",
)
_BODY_SECTIONS: Mapping[str, Tuple[BodySection, ...]] = {
    "试题版": (_QUESTIONS,),
    "解析版": (_QUESTIONS, _SOLUTIONS),
    "简答版": (_QUESTIONS, _SHORT),
    "印刷版": (_QUESTIONS, _COMPACT_SOLUTIONS),
}


@dataclass(frozen=True)
class PaperShell:
    """一卷的壳身份：manifest 的 paper_id/project_dir/title + 兼容 index 的旧 ID。"""

    paper_id: str
    project_dir: str
    title: str
    legacy_id: str


@dataclass(frozen=True)
class ShellResult:
    """一卷的四个壳与它们引用的矩阵输入（仓库相对路径）。"""

    paper_id: str
    project_dir: str
    targets: Mapping[str, bytes]
    inputs: Tuple[str, ...]


# ---------------------------------------------------------------- 模板与正文


def template_target(edition: str) -> str:
    """模板的仓库相对路径；未知版本立刻报错，不给拼出一个不存在的路径的机会。"""
    if edition not in EDITIONS:
        raise EditionError(f"未知版本：{edition}")
    return "%s/%s.tex.tpl" % (TEMPLATE_RELATIVE, edition)


def load_templates(repo_root: Path) -> Dict[str, str]:
    templates: Dict[str, str] = {}
    for edition in EDITIONS:
        path = Path(repo_root) / template_target(edition)
        try:
            templates[edition] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise EditionError(f"无法读取模板 {template_target(edition)}：{error}") from error
    return templates


def body_inputs(body: str) -> Tuple[str, ...]:
    """正文里 `\\input` 的文件名，按出现顺序。"""
    return tuple(_INPUT_RE.findall(body))


def render_body(edition: str) -> str:
    """按版本装配正文；渲染结果必须自证与冻结的输入矩阵逐项相等。"""
    sections = _BODY_SECTIONS.get(edition)
    if sections is None:
        raise EditionError(f"未知版本：{edition}")
    parts: List[str] = []
    for section in sections:
        parts.append(section.lead)
        parts.append("\\pdfbookmark[1]{%s}{%s}\n" % (section.bookmark, section.anchor))
        if section.heading:
            parts.append(
                "\\begin{center}{\\%s\\bfseries %s}\\end{center}\n"
                % (section.heading_size, section.heading)
            )
            parts.append(section.gap + "\n")
        parts.append("\\input{%s}\n" % section.source)
    body = "".join(parts)
    found = body_inputs(body)
    if found != tuple(EDITION_INPUTS[edition]):
        raise EditionError(
            "%s 的正文 \\input 序列 %s 与冻结的输入矩阵 %s 不一致"
            % (edition, list(found), list(EDITION_INPUTS[edition]))
        )
    return body


def render_edition(template: str, values: Mapping[str, str]) -> str:
    """占位符替换：名单外的一律拒绝，缺一个也拒绝，替换结果绝不二次扫描。"""
    if set(values) != set(PLACEHOLDERS):
        raise EditionError(
            "占位符取值集合必须恰为 %s，实际 %s"
            % (list(PLACEHOLDERS), sorted(values))
        )
    unknown = sorted(set(_PLACEHOLDER_RE.findall(template)) - set(PLACEHOLDERS))
    if unknown:
        raise EditionError(f"模板含未知占位符：{unknown}")
    missing = [name for name in PLACEHOLDERS if name not in template]
    if missing:
        raise EditionError(f"模板缺少必需占位符：{missing}")
    # 一次正则替换，替换进去的文本不再参与匹配：值里若含 `@@…@@` 字样只当普通文本。
    return _PLACEHOLDER_RE.sub(lambda match: values[match.group(0)], template)


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
        raise EditionError(f"路径不在仓库内：{path}") from error


def _required_sha256(root: Path, relative: str) -> str:
    path = root / relative
    if not path.is_file():
        raise EditionError(f"只读输入缺失：{relative}")
    return file_sha256(path)


def paper_shell(paper: Mapping[str, Any]) -> PaperShell:
    """壳的 `\\gkpaperid` 用兼容 index 的旧 ID；旧 ID 不唯一就没法确定填哪一个。"""
    legacy_ids = list(paper["legacy_ids"])
    if len(legacy_ids) != 1:
        raise EditionError(
            "%s 的 legacy_ids 必须恰有一个（壳的 \\gkpaperid 无处可选），实际 %s"
            % (paper["paper_id"], legacy_ids)
        )
    return PaperShell(
        paper_id=paper["paper_id"],
        project_dir=paper["project_dir"],
        title=paper["title"],
        legacy_id=legacy_ids[0],
    )


def _select(
    manifest: Mapping[str, Any], selector: str, value: Optional[str]
) -> Tuple[PaperShell, ...]:
    papers = {paper["paper_id"]: paper for paper in manifest["papers"]}
    if selector == "all":
        return tuple(paper_shell(paper) for paper in manifest["papers"])
    if selector == "paper":
        if value not in papers:
            raise EditionError(f"未知 paper_id：{value}")
        return (paper_shell(papers[value]),)
    if selector == "batch":
        batches = [item for item in manifest["batches"] if item["batch_id"] == value]
        if len(batches) != 1:
            raise EditionError(f"未知批次：{value}")
        selected = []
        for paper_id in batches[0]["paper_ids"]:
            if paper_id not in papers:
                raise EditionError(f"批次 {value} 引用了不存在的 paper_id：{paper_id}")
            selected.append(paper_shell(papers[paper_id]))
        return tuple(selected)
    raise EditionError(f"未知选择器：{selector}")


# ---------------------------------------------------------------- 单卷生成


def build_shells(
    templates: Mapping[str, str], shell: PaperShell
) -> Dict[str, bytes]:
    """在内存里渲染本卷四个壳，键为仓库相对路径。"""
    targets: Dict[str, bytes] = {}
    for edition in EDITIONS:
        if edition not in templates:
            raise EditionError(f"缺少模板：{template_target(edition)}")
        rendered = render_edition(templates[edition], {
            "@@CLASS_OPTIONS@@": CLASS_OPTIONS[edition],
            "@@PAPER_ID@@": shell.legacy_id,
            "@@TITLE@@": shell.title,
            "@@EDITION@@": edition,
            "@@BODY@@": render_body(edition),
        })
        relative = "%s/%s/%s.tex" % (PROJECT_RELATIVE, shell.project_dir, edition)
        targets[relative] = rendered.encode("utf-8")
    return targets


def matrix_inputs(shell: PaperShell) -> Tuple[str, ...]:
    """本卷各版本 `\\input` 到的共享 TeX，去重后按路径排序。"""
    names = sorted({name for inputs in EDITION_INPUTS.values() for name in inputs})
    return tuple(
        "%s/%s/%s.tex" % (PROJECT_RELATIVE, shell.project_dir, name) for name in names
    )


def generate_shells(
    repo_root: Path, templates: Mapping[str, str], shell: PaperShell
) -> ShellResult:
    return ShellResult(
        paper_id=shell.paper_id,
        project_dir=shell.project_dir,
        targets=build_shells(templates, shell),
        inputs=matrix_inputs(shell),
    )


def validate_shell_result(repo_root: Path, result: ShellResult) -> Tuple[str, ...]:
    """矩阵引用的共享 TeX 必须已经存在——壳指向一个不存在的文件是编译期才炸的错。"""
    problems: List[str] = []
    for relative in result.inputs:
        if not (Path(repo_root) / relative).is_file():
            problems.append("%s: 输入矩阵缺 %s" % (result.paper_id, relative))
    return tuple(problems)


# ---------------------------------------------------------------- 原子提交


def commit_shell_results(
    repo_root: Path,
    manifest_path: Path,
    results: Sequence[ShellResult],
    event_hook: Any = None,
) -> Dict[str, Any]:
    """把全批壳放进**一个** `content` 事务提交；全等则跳过，不做空事务。"""
    root = Path(repo_root)
    manifest_relative = _relative_to_repo(root, Path(manifest_path))
    if manifest_relative != MANIFEST_TARGET:
        raise EditionError(f"manifest 必须是 {MANIFEST_TARGET}，实际 {manifest_relative}")

    inputs: Dict[str, Optional[str]] = {
        manifest_relative: _required_sha256(root, manifest_relative),
        TOOL_SOURCE_TARGET: _required_sha256(root, TOOL_SOURCE_TARGET),
    }
    for edition in EDITIONS:
        relative = template_target(edition)
        inputs[relative] = _required_sha256(root, relative)

    targets: Dict[str, bytes] = {}
    for result in results:
        for relative in result.inputs:
            inputs[relative] = _required_sha256(root, relative)
        for relative, value in result.targets.items():
            if relative in targets:
                raise EditionError(f"批内目标路径重复：{relative}")
            targets[relative] = value

    overlap = sorted(set(inputs) & set(targets))
    if overlap:
        raise EditionError(f"只读输入与写目标重叠：{overlap}")

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
    event_hook: Any = None,
) -> Dict[str, Any]:
    """生成一批壳；`write=False` 只比对不落盘，`write=True` 先全过再一次性提交。"""
    manifest_path = Path(manifest_path).resolve()
    root = _repository_root(manifest_path.parent)
    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        templates = load_templates(root)
        selected = _select(manifest, selector, value)

        problems: List[str] = []
        results: List[ShellResult] = []
        for shell in selected:
            result = generate_shells(root, templates, shell)
            found = validate_shell_result(root, result)
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
                raise EditionError("；".join(problems))
            report.update(
                commit_shell_results(root, manifest_path, results, event_hook)
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
        description="由来源总账与四份模板生成各卷试题版/解析版/简答版/印刷版壳文件"
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


def main(argv: Optional[Sequence[str]] = None) -> int:
    """退出码契约：0 全过、1 校验失败或输入无效、2 命令行用法错（argparse）。"""
    arguments = _parser().parse_args(argv)
    selector, value = selection(arguments)
    try:
        report = run(Path(arguments.manifest), selector, value, write=arguments.write)
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
            "✓ %d 套试卷，%s%d 个壳"
            % (
                len(report["papers"]),
                "已写入 " if report["written"] else "无需改动 ",
                len(report["targets"]),
            )
        )
    else:
        print("✓ %d 套试卷的壳与模板渲染结果一致" % len(report["papers"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

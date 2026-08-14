#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_projects.py —— 由来源总账（manifest）驱动生成各卷共享 LaTeX 与 index.json。

**唯一写入口**：`split_project.py` 已降为只读兼容 CLI，转换链上不再有第二处写实现。

每套试卷的三份规范源各司其职，生成物按职责拼装：

- `questions.tex` —— 只由 `_试题.md` 转换而来，**绝不含答案**；
- `answers.tex`   —— 题面来自 `_试题.md`、推导来自 `_解析正文.md`、最终答案来自
  `_答案要点.md`，三者先由 `solution_sources.render_combined()` 确定性合成，再整体
  过一遍转换器。这样「解析里的题面」与「解析里的答案」都不再是独立转写的副本。
- `index.json`    —— manifest 身份在兼容 index 形状上的投影（`project_legacy_index`）。

**项目 `figures/` 只读**：本工具从不写入、也绝不从合并书复制图。图的正确性改由
「引用集合与复用计数必须与 manifest `figure_files` 精确一致」来保证——注意 manifest
里 `figure_files.path` 是**项目相对**、`source_files` 是**仓库相对**，两套基准不可混用。
配对不沿用任何 legacy TeX 的引用顺序，而是由本工具自己的 `FIGMAP` 映射重新数一遍。

**先校验后原子写**：全批目标先在内存生成，题号、答案块、figure 复用计数和 index 投影
全部通过后，才以**一个** Task 1 `content` 事务提交 `questions.tex/answers.tex/index.json`。
任何一卷失败都不落盘（失败零覆盖），崩溃后由 `RepoLock` 的恢复把事务补完。
事务只读输入 = manifest 整文件 + 每卷三份 Markdown + 已登记 figure 树 + 转换器/渲染器/
生成器三份源码；`index.json` 这份**稳定 manifest 投影只是 build/review currency 的读物**，
它作为普通目标随事务落盘，不进 `state` 模式、不参与 manifest revision，故不会把业务
投影塞进通用事务 journal 的状态语义里。
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import cli_common
from manifest import canonical_json, load_manifest
from solution_sources import (
    SolutionSourceError,
    extract_solution_blocks,
    parse_answer_points,
    render_combined,
)
from source_manifest import project_legacy_index
from transaction import RepoLock

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent                       # math-gaokao-latex
sys.path.insert(0, str(PROJECT_ROOT.parent / "math-gaokao-2017-2026" / "tools"))
import md2tex  # noqa: E402  合并书时代的转换器，本工具是它唯一的批量调用方

PROJECT_RELATIVE = "math-gaokao-latex"
MANIFEST_TARGET = PROJECT_RELATIVE + "/source-manifest.json"
INDEX_TARGET = PROJECT_RELATIVE + "/index.json"
GENERATOR_SOURCE_TARGET = PROJECT_RELATIVE + "/tools/generate_projects.py"
RENDERER_SOURCE_TARGET = PROJECT_RELATIVE + "/tools/solution_sources.py"
CONVERTER_SOURCE_TARGET = "math-gaokao-2017-2026/tools/md2tex.py"
DEFAULT_MANIFEST = PROJECT_ROOT / "source-manifest.json"

# 切分边界（经对生成物实测确认，自 split_project.py 逐字保留）：
#   questions：题块起于行首 \gkti{N}，止于下一个 \gkti / \gkpart / \gksubpart / 文件尾
#              （题面里 \gksubpart 只用作"（一）必考题"类节级标题）；
#   answers  ：题块起于行首 \gksolhead{N}{..}，止于下一个 \gksolhead / \gkpart / 文件尾
#              （解析里 \gksubpart 是题内小问标题，作边界会把一道题劈成两半）。
Q_HEAD = re.compile(r"^\\gkti\{(\d+)\}")
S_HEAD = re.compile(r"^\\gksolhead\{(\d+)\}\{")
STRUCT_Q = re.compile(r"^\\(gkpart|gksubpart)\{")
STRUCT_S = re.compile(r"^\\gkpart\{")
_WRAP_MODES = {
    "questions": (Q_HEAD, STRUCT_Q, "question"),
    "answers": (S_HEAD, STRUCT_S, "answer"),
}
# 生成答案块转成 LaTeX 后的两种形态：`**答案：X**` 独立段落走 \gkanswer；答案值里含
# `*`（如 $\mathbf N^{*}$）时转换器的 ANSLINE 认不出，退化成 \textbf。两种都算数——
# 数的是「这一题的最终答案有没有落地」，不是转换器把它归到了哪一类。
_ANSWER_MARK = re.compile(r"^\\(?:gkanswer|textbf)\{答案")
INDEX_METADATA: Dict[str, Dict[str, Any]] = {
    "2017_全国Ⅰ卷_理科": {
        "id": "2017li",
        "base": "2017_g1_li",
        "paper": "全国Ⅰ卷",
        "track": "理科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [1, 6],
        "pages_s": [7, 33],
        "note": "含现已取消的选做题第 22/23 题与已删除的三视图、程序框图考点",
    },
    "2017_全国Ⅰ卷_文科": {
        "id": "2017wen",
        "base": "2017_g1_wen",
        "paper": "全国Ⅰ卷",
        "track": "文科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [34, 39],
        "pages_s": [40, 64],
        "note": "含现已取消的选做题第 22/23 题与已删除的三视图、程序框图考点",
    },
    "2018_全国Ⅰ卷_理科": {
        "id": "2018li",
        "base": "2018_g1_li",
        "paper": "全国Ⅰ卷",
        "track": "理科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [65, 69],
        "pages_s": [70, 92],
        "note": "含现已取消的选做题第 22/23 题",
    },
    "2018_全国Ⅰ卷_文科": {
        "id": "2018wen",
        "base": "2018_g1_wen",
        "paper": "全国Ⅰ卷",
        "track": "文科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [93, 97],
        "pages_s": [98, 116],
        "note": "含现已取消的选做题第 22/23 题",
    },
    "2019_全国Ⅰ卷_理科": {
        "id": "2019li",
        "base": "2019_g1_li",
        "paper": "全国Ⅰ卷",
        "track": "理科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [117, 121],
        "pages_s": [122, 147],
        "note": "含现已取消的选做题第 22/23 题",
    },
    "2019_全国Ⅰ卷_文科": {
        "id": "2019wen",
        "base": "2019_g1_wen",
        "paper": "全国Ⅰ卷",
        "track": "文科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [148, 152],
        "pages_s": [153, 171],
        "note": "含现已取消的选做题第 22/23 题",
    },
    "2020_全国Ⅰ卷_理科": {
        "id": "2020li",
        "base": "2020_g1_li",
        "paper": "全国Ⅰ卷",
        "track": "理科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [172, 176],
        "pages_s": [177, 202],
        "note": "含现已取消的选做题第 22/23 题",
    },
    "2020_全国Ⅰ卷_文科": {
        "id": "2020wen",
        "base": "2020_g1_wen",
        "paper": "全国Ⅰ卷",
        "track": "文科",
        "variant": None,
        "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
        "pages_q": [203, 207],
        "pages_s": [208, 226],
        "note": "含现已取消的选做题第 22/23 题",
    },
    "2020_新高考Ⅱ卷": {
        "id": "2020x2",
        "base": "2020_xgk2",
        "paper": "新高考Ⅱ卷",
        "track": None,
        "variant": "新高考Ⅱ",
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2020新高考2·海南），不在合并书 main.pdf 内",
    },
    "2021_新高考Ⅰ卷": {
        "id": "2021",
        "base": "2021_xgk1",
        "paper": "新高考Ⅰ卷",
        "track": None,
        "variant": None,
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": [227, 230],
        "pages_s": [231, 257],
        "note": None,
    },
    "2021_新高考Ⅱ卷": {
        "id": "2021x2",
        "base": "2021_xgk2",
        "paper": "新高考Ⅱ卷",
        "track": None,
        "variant": "新高考Ⅱ",
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2021新高考2），不在合并书 main.pdf 内",
    },
    "2022_新高考Ⅰ卷": {
        "id": "2022",
        "base": "2022_xgk1",
        "paper": "新高考Ⅰ卷",
        "track": None,
        "variant": None,
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": [258, 261],
        "pages_s": [262, 293],
        "note": None,
    },
    "2022_新高考Ⅱ卷": {
        "id": "2022x2",
        "base": "2022_xgk2",
        "paper": "新高考Ⅱ卷",
        "track": None,
        "variant": "新高考Ⅱ",
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2022新高考2），不在合并书 main.pdf 内",
    },
    "2023_新高考Ⅰ卷": {
        "id": "2023",
        "base": "2023_xgk1",
        "paper": "新高考Ⅰ卷",
        "track": None,
        "variant": None,
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": [294, 297],
        "pages_s": [298, 325],
        "note": None,
    },
    "2023_新高考Ⅱ卷": {
        "id": "2023x2",
        "base": "2023_xgk2",
        "paper": "新高考Ⅱ卷",
        "track": None,
        "variant": "新高考Ⅱ",
        "structure": {"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2023新高考2），不在合并书 main.pdf 内",
    },
    "2024_新高考Ⅰ卷": {
        "id": "2024",
        "base": "2024_xgk1",
        "paper": "新高考Ⅰ卷",
        "track": None,
        "variant": None,
        "structure": {"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
        "pages_q": [326, 329],
        "pages_s": [330, 356],
        "note": None,
    },
    "2024_新高考Ⅱ卷": {
        "id": "2024x2",
        "base": "2024_xgk2",
        "paper": "新高考Ⅱ卷",
        "track": None,
        "variant": "新高考Ⅱ",
        "structure": {"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2024新高考2），不在合并书 main.pdf 内",
    },
    "2025_全国1卷": {
        "id": "2025",
        "base": "2025_g1",
        "paper": "全国 1 卷",
        "track": None,
        "variant": None,
        "structure": {"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
        "pages_q": [357, 360],
        "pages_s": [361, 383],
        "note": None,
    },
    "2025_全国2卷": {
        "id": "2025g2",
        "base": "2025_g2",
        "paper": "全国 2 卷",
        "track": None,
        "variant": "全国2",
        "structure": {"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2025全国2），不在合并书 main.pdf 内",
    },
    "2026_全国1卷_回忆版": {
        "id": "2026",
        "base": "2026_g1",
        "paper": "全国 1 卷",
        "track": None,
        "variant": None,
        "structure": {"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
        "pages_q": [384, 387],
        "pages_s": [388, 420],
        "note": "回忆版：依据考生回忆整理，正式卷公开后应以官方版本校订",
    },
    "2026_全国2卷": {
        "id": "2026g2",
        "base": "2026_g2",
        "paper": "全国 2 卷",
        "track": None,
        "variant": "全国2",
        "structure": {"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
        "pages_q": None,
        "pages_s": None,
        "note": "批次扩展卷：转录自 deekur/gaokaomath 源 PDF（2026全国2），不在合并书 main.pdf 内",
    },
}


class GenerationError(ValueError):
    """生成或校验失败；抛出即代表本次运行一个字节都没落盘。"""


@dataclass(frozen=True)
class ProjectSources:
    """一卷的生成输入：manifest 身份 + 三份规范 Markdown + 已登记 figure。

    `questions`/`answer_key`/`solution_body` 是**仓库相对**路径；
    `figures` 的路径是**项目相对**（manifest 里就是两套基准，不可混用）。
    """

    paper_id: str
    project_dir: str
    title: str
    question_count: int
    questions: str
    answer_key: str
    solution_body: str
    figures: Tuple[Tuple[str, int], ...]


@dataclass(frozen=True)
class ProjectResult:
    """一卷的内存生成结果与三道门禁各自的实测值。"""

    paper_id: str
    project_dir: str
    targets: Mapping[str, bytes]
    inputs: Tuple[str, ...]
    question_numbers: Mapping[str, Tuple[int, ...]]
    answer_counts: Mapping[int, int]
    expected_answer_counts: Mapping[int, int]
    figure_occurrences: Mapping[str, int]


def wrap(text: str, mode: str) -> Tuple[str, List[int]]:
    """按行首题头切分并包裹环境；返回 (包裹后文本, 题号列表)。"""
    try:
        head_re, struct_re, env = _WRAP_MODES[mode]
    except KeyError:
        raise GenerationError(f"未知包裹模式：{mode}")
    out: List[str] = []
    nums: List[int] = []
    in_block = False
    for line in text.split("\n"):
        match = head_re.match(line)
        if match:
            if in_block:
                out.append("\\end{%s}" % env)
            out.append("\\begin{%s}" % env)
            out.append(line)
            nums.append(int(match.group(1)))
            in_block = True
        elif struct_re.match(line):
            if in_block:
                out.append("\\end{%s}" % env)
                in_block = False
            out.append(line)
        else:
            out.append(line)
    if in_block:
        out.append("\\end{%s}" % env)
    return "\n".join(out), nums


# ---------------------------------------------------------------- 身份与读取


def paper_sources(paper: Mapping[str, Any]) -> ProjectSources:
    files = paper["source_files"]
    figures = tuple(
        (str(item["path"]), int(item["expected_occurrences"]))
        for item in paper["figure_files"]
    )
    return ProjectSources(
        paper_id=paper["paper_id"],
        project_dir=paper["project_dir"],
        title=paper["title"],
        question_count=paper["question_count"],
        questions=files["questions"],
        answer_key=files["answer_key"],
        solution_body=files["solution_body"],
        figures=figures,
    )


def _select(
    manifest: Mapping[str, Any], selector: str, value: Optional[str]
) -> Tuple[ProjectSources, ...]:
    return cli_common.select_papers(
        manifest, selector, value, paper_sources, GenerationError
    )


# ---------------------------------------------------------------- 单卷生成


def _answer_counts(wrapped: str) -> Dict[int, int]:
    """逐题数 answers.tex 里落地的最终答案块。"""
    counts: Dict[int, int] = {}
    current: Optional[int] = None
    for line in wrapped.split("\n"):
        match = S_HEAD.match(line)
        if match:
            current = int(match.group(1))
            counts.setdefault(current, 0)
        elif current is not None and _ANSWER_MARK.match(line):
            counts[current] += 1
    return counts


def generate_project(
    repo_root: Path,
    sources: ProjectSources,
    figure_map: Optional[Mapping[str, str]] = None,
) -> ProjectResult:
    """在内存里生成本卷的 questions.tex / answers.tex，并数出三道门禁的实测值。"""
    figure_map = md2tex.FIGMAP if figure_map is None else figure_map
    root = Path(repo_root)
    questions_text = cli_common.read_text(root / sources.questions, GenerationError)
    answer_text = cli_common.read_text(root / sources.answer_key, GenerationError)
    solution_raw = cli_common.read_text(root / sources.solution_body, GenerationError)

    figure_inputs = []
    for relative, _ in sources.figures:
        target = PROJECT_RELATIVE + "/" + relative
        if not (root / target).is_file():
            raise GenerationError(f"{sources.paper_id}: 缺图 {relative}")
        figure_inputs.append(target)

    try:
        # 解析正文即使是事实源也要再过一遍提取：人工回填进去的题面或答案会被规范化
        # 掉，而不是悄悄留在源里造出第二份题面。
        solution_text = extract_solution_blocks(solution_raw, questions_text)
        combined_text = render_combined(questions_text, solution_text, answer_text)
        points = parse_answer_points(answer_text)
    except SolutionSourceError as error:
        raise GenerationError(f"{sources.paper_id}: {error}") from error

    context = md2tex.ConversionContext(figure_map=figure_map, strict=True)
    try:
        converted_questions = md2tex.convert_markdown(questions_text, context)
        converted_answers = md2tex.convert_markdown(combined_text, context)
    except md2tex.ConversionError as error:
        raise GenerationError(
            "%s: 转换告警 %s" % (sources.paper_id, "；".join(error.warnings))
        ) from error

    wrapped_questions, question_numbers = wrap(converted_questions.text, "questions")
    wrapped_answers, answer_numbers = wrap(converted_answers.text, "answers")

    questions_target = "%s/%s/questions.tex" % (PROJECT_RELATIVE, sources.project_dir)
    answers_target = "%s/%s/answers.tex" % (PROJECT_RELATIVE, sources.project_dir)
    # 注意 `.format()` 不认 `%%` 转义，注释符必须逐字写成单个 `%`。
    questions_header = (
        "% questions.tex —— {0} · 题目内容片段（无答案）\n"
        "% 由 tools/generate_projects.py 依来源总账自 {1} 生成，勿手改（改源 MD 后重跑）\n"
    ).format(sources.title, sources.questions)
    answers_header = (
        "% answers.tex —— {0} · 参考答案与详细解析片段\n"
        "% 由 tools/generate_projects.py 依来源总账自 {1} + {2} + {3} 生成，"
        "勿手改（改源 MD 后重跑）\n"
    ).format(sources.title, sources.questions, sources.solution_body, sources.answer_key)

    occurrences: Dict[str, int] = {}
    for stem in tuple(converted_questions.referenced_figures) + tuple(
        converted_answers.referenced_figures
    ):
        path = "%s/figures/%s.tex" % (sources.project_dir, stem)
        occurrences[path] = occurrences.get(path, 0) + 1

    return ProjectResult(
        paper_id=sources.paper_id,
        project_dir=sources.project_dir,
        targets={
            questions_target: (questions_header + wrapped_questions).encode("utf-8"),
            answers_target: (answers_header + wrapped_answers).encode("utf-8"),
        },
        inputs=tuple(
            [sources.questions, sources.answer_key, sources.solution_body] + figure_inputs
        ),
        question_numbers={
            "questions": tuple(question_numbers),
            "answers": tuple(answer_numbers),
        },
        answer_counts=_answer_counts(wrapped_answers),
        expected_answer_counts={
            point.number: len(point.subparts) or 1 for point in points
        },
        figure_occurrences=occurrences,
    )


def validate_project_result(
    sources: ProjectSources, result: ProjectResult
) -> Tuple[str, ...]:
    """三道门禁：题号连续、逐题最终答案齐、figure 引用集合与复用计数与 manifest 一致。"""
    problems: List[str] = []
    expected = tuple(range(1, sources.question_count + 1))
    for label in ("questions", "answers"):
        numbers = tuple(result.question_numbers.get(label, ()))
        if numbers != expected:
            problems.append(
                "%s: %s 题号异常，期望 %s、实际 %s"
                % (sources.paper_id, label, list(expected), list(numbers))
            )
    counts = result.answer_counts
    wanted = result.expected_answer_counts
    for number in sorted(set(counts) | set(wanted)):
        if counts.get(number, 0) != wanted.get(number, 0):
            problems.append(
                "%s: 第 %d 题落地答案块 %d 个，答案要点登记 %d 个"
                % (sources.paper_id, number, counts.get(number, 0), wanted.get(number, 0))
            )
    registered = dict(sources.figures)
    for path in sorted(set(registered) | set(result.figure_occurrences)):
        want = registered.get(path)
        got = result.figure_occurrences.get(path)
        if want != got:
            problems.append(
                "%s: figure %s 实际引用 %s 次，manifest 登记 %s 次"
                % (sources.paper_id, path, got, want)
            )
    return tuple(problems)


# ---------------------------------------------------------------- index 投影


def build_legacy_index(
    manifest: Mapping[str, Any],
    metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> Dict[str, Any]:
    """按 manifest 重建**迁移前形状**的 index；身份三键由 project_legacy_index 补。

    `base`/`paper`/`variant`/`track`/`structure`/`pdf_pages`/`note` 这些旧字段
    manifest 不携带，只能来自静态表；能从 manifest 取的一律取 manifest。
    """
    metadata = INDEX_METADATA if metadata is None else metadata
    papers: List[Dict[str, Any]] = []
    for paper in manifest["papers"]:
        directory = paper["project_dir"]
        static = metadata.get(directory) or paper.get("index_metadata")
        if static is None:
            raise GenerationError(f"index 静态元数据缺少试卷目录：{directory}")
        count = paper["question_count"]
        covered: set = set()
        for low, high in static["structure"].values():
            covered.update(range(int(low), int(high) + 1))
        if covered != set(range(1, count + 1)):
            raise GenerationError(
                f"{directory}: structure 覆盖的题号与题量 {count} 不一致"
            )
        papers.append({
            "dir": directory,
            "id": static["id"],
            "base": static["base"],
            "year": paper["year"],
            "paper": static["paper"],
            "track": static["track"],
            "variant": static["variant"],
            "title": paper["title"],
            "questions": count,
            "structure": static["structure"],
            "pdf_pages": {
                "questions": static["pages_q"], "solutions": static["pages_s"]
            },
            "figures": [
                PurePosixPath(str(item["path"])).name for item in paper["figure_files"]
            ],
            "note": static["note"],
        })
    return {
        # T13 把写实现搬到本工具时曾把这里的字面值留在 `tools/split_project.py`，裁定
        # 「留待 index 下次合法变更时一并改」；T16 剔除运行态投影正是那次合法变更，于是
        # 一并落实。该键与 legacy 侧取值不同是登记在案的正当改写（见 baseline.py 的
        # `_REWRITTEN_FIELDS`）；它的现值由 LiveIndexIsUnchangedTests 逐字节守住。
        "generated_by": "tools/generate_projects.py",
        "source_project": "../math-gaokao-2017-2026",
        "source_pdf": "../math-gaokao-2017-2026/main.pdf",
        "page_numbering_note": "pdf_pages 为合并书正文逻辑页码（书内页脚所印）；"
                               "换算 PDF 物理页需加前言罗马页偏移。",
        "editions": ["试题版", "解析版", "简答版", "印刷版"],
        "papers": papers,
    }


def project_index_bytes(
    manifest: Mapping[str, Any],
    metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> bytes:
    return canonical_json(
        project_legacy_index(manifest, build_legacy_index(manifest, metadata))
    ).encode("utf-8")


# ---------------------------------------------------------------- 原子提交


def commit_project_result(
    repo_root: Path,
    manifest_path: Path,
    results: Sequence[ProjectResult],
    index_bytes: bytes,
    event_hook: Any = None,
) -> Dict[str, Any]:
    """把全批目标放进**一个** `content` 事务提交；全等则跳过，不做空事务。

    与卷无关的只读输入 = 生成器 / 渲染器 / 转换器三份源码；`index.json` 是与卷无关的
    额外目标（manifest 投影），随同一事务落盘。
    """
    return cli_common.commit_content(
        Path(repo_root), Path(manifest_path), MANIFEST_TARGET,
        (GENERATOR_SOURCE_TARGET, RENDERER_SOURCE_TARGET, CONVERTER_SOURCE_TARGET),
        results, GenerationError,
        extra_targets={INDEX_TARGET: index_bytes}, event_hook=event_hook,
    )


# ---------------------------------------------------------------- 驱动


def run(
    manifest_path: Path,
    selector: str,
    value: Optional[str] = None,
    write: bool = False,
    figure_map: Optional[Mapping[str, str]] = None,
    index_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
    event_hook: Any = None,
) -> Dict[str, Any]:
    """生成一批试卷；`write=False` 只比对不落盘，`write=True` 先全过再一次性提交。"""
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        selected = _select(manifest, selector, value)
        index_bytes = project_index_bytes(manifest, index_metadata)

        problems: List[str] = []
        results: List[ProjectResult] = []
        for sources in selected:
            try:
                result = generate_project(root, sources, figure_map=figure_map)
            except GenerationError as error:
                if write:
                    raise
                problems.append(str(error))
                continue
            found = validate_project_result(sources, result)
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
                raise GenerationError("；".join(problems))
            report.update(
                commit_project_result(
                    root, manifest_path, results, index_bytes, event_hook
                )
            )
            return report

        found, listed = cli_common.compare_targets(
            root, results, {INDEX_TARGET: index_bytes}
        )
        problems.extend(found)
        report["targets"] = listed
        return report


def _parser() -> argparse.ArgumentParser:
    return cli_common.build_parser(
        "由来源总账生成各卷 questions.tex / answers.tex 与 index.json", DEFAULT_MANIFEST
    )


selection = cli_common.selection


def main(
    argv: Optional[Sequence[str]] = None,
    figure_map: Optional[Mapping[str, str]] = None,
    index_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> int:
    """退出码契约：0 全过、1 校验失败或输入无效、2 命令行用法错（argparse）。

    `figure_map`/`index_metadata` 不是命令行开关，只是与 `run()` 同一个注入缝——
    夹具仓库里的虚构试卷既不在 FIGMAP 也不在 INDEX_METADATA 里。
    """
    arguments = _parser().parse_args(argv)
    selector, value = selection(arguments)
    return cli_common.execute(
        lambda: run(
            Path(arguments.manifest), selector, value, write=arguments.write,
            figure_map=figure_map, index_metadata=index_metadata,
        ),
        arguments.write, "个目标", "套试卷与生成结果一致",
    )


if __name__ == "__main__":
    sys.exit(main())

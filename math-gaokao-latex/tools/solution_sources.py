"""解析正文唯一源提取与「含解析」确定性生成器。

三份规范源与一份展示文档的关系（见阶段 0 设计文档）：

- `_试题.md`     —— 唯一拥有题面；
- `_答案要点.md` —— 唯一拥有逐题最终答案；
- `_解析正文.md` —— 唯一拥有详细推导，**不得复制题面或最终答案**；
- `_含解析.md`   —— 由上面三份确定性生成的展示文档，本身不是事实源。

`extract-batch --write` 把一个批次的两类派生物（`_解析正文.md` 与 `_含解析.md`）
放进**同一个** Task 1 `content` 事务提交：先在内存生成并校验整批目标，再一次性落盘。
只读输入的哈希固定为 manifest 整文件、每卷 `_试题.md`、`_答案要点.md` 和本工具源码；
原 `_含解析.md` 是被重写目标，其旧哈希只出现在事务的 target precondition 里。

Markdown 约定（两种题号写法，解析器自动识别，`### 第 N 题` 优先）：

- heading 式：`### 第 N 题（标题）`，小问用 `#### (k) 小标题`；`_解析正文.md`
  与 `_含解析.md` 使用这一式。
- inline 式：`**N．（12 分）** 题面……`，小问用行首 `(k) ……`；`_试题.md`
  与 `_答案要点.md` 使用这一式。

段落约定：以空行分段，段内原样保留。只有**单行且以加粗答案块开头**的段落
（`**答案：X**`、`**答案（k）：X**`，允许 `**答案：$4$**（约 $11.85$）这类尾注）
才是提取边界——证明正文里出现「答案」二字不会被误删。
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from manifest import atomic_write_json, canonical_json, file_sha256, load_manifest
from transaction import RepoLock, Transaction

# 本工具源码自身进入事务只读输入：工具变了，派生物就该重算。
TOOL_SOURCE_TARGET = "math-gaokao-latex/tools/solution_sources.py"
# 阶段 0 唯一的共享迁移报告路径，`report --output` 与 `--include-report` 都钉死在这里。
REPORT_TARGET = "math-gaokao-latex/reports/solution-source-migration.json"
REPORT_VERSION = 1

QUESTION_MARKER = "**题目**"
SOLUTION_MARKER = "**解析**"

# 标题后缀连分隔符一起原样保留：真题里既有 `第 1 题（集合运算）`，也有
# `第 22 题　〔坐标系与参数方程〕`。只认圆括号会让后者整块不被识别，而未被识别的
# 块之后的一切都会被静默丢掉——曾使三套卷的整个选考题章节消失。
_HEADING_QUESTION = re.compile(r"^### 第 (\d+) 题(|[ \t　（(〔【].*)$")
_INLINE_QUESTION = re.compile(r"^\*\*(\d+)．(.*?)\*\*(.*)$")
_ATX_HEADING = re.compile(r"^(#{1,6}) ")
_HEADING_SUBPART = re.compile(r"^####[ \t]*[（(](\d+)[）)]")
_INLINE_SUBPART = re.compile(r"^[ \t　]*[（(](\d+)[）)][ \t　]")
_BLOCKQUOTE_PREFIX = re.compile(r"^(?:[ \t]*>)+[ \t]?")
_PARAGRAPH_SPLIT = re.compile(r"\n(?:[ \t　]*\n)+")
_IMAGE_PARAGRAPH = re.compile(r"^!\[[^\]]*\]\([^)\s]*\)$")
# 加粗答案块：`**答案：X**`、`**(1) 答案：X**`、`**答案（1）：X**` 三种写法。
# 只要求以加粗答案块**开头**：真题里常见 `**答案：$4$**（约 $11.85$）` 这种尾注，
# 要求整行恰好收在 `**` 会让这些行漏网，最终答案就会留在解析正文里。
_ANSWER_LINE = re.compile(
    r"^\*\*"
    r"(?:[（(](?P<pre>\d+)[）)][ \t　]*)?"
    r"答案"
    r"(?:[（(](?P<post>\d+)[）)])?"
    r"[ \t　]*[:：][ \t　]*"
    r"(?P<value>.*?)\*\*(?P<trailer>.*)$"
)


class SolutionSourceError(ValueError):
    """解析正文契约错误：格式、题号对齐或派生物不一致。"""


@dataclass(frozen=True)
class QuestionBlock:
    number: int
    title: str
    body: str
    subparts: Tuple[int, ...]
    # 本题之前、上一题之后的非题目文本（章节标题、分隔线等），原样保留以便重建文档。
    lead: str


@dataclass(frozen=True)
class AnswerPoint:
    number: int
    # (小问号或 None, 答案文本)；None 表示整题只有一个最终答案。
    answers: Tuple[Tuple[Optional[int], str], ...]

    @property
    def subparts(self) -> Tuple[int, ...]:
        return tuple(key for key, _ in self.answers if key is not None)


@dataclass(frozen=True)
class PaperSources:
    paper_id: str
    question_count: int
    questions: str
    answer_key: str
    solution_body: str
    combined_rendered: str


# ---------------------------------------------------------------- Markdown 解析


def _strip_quote(line: str) -> str:
    return _BLOCKQUOTE_PREFIX.sub("", line)


def _paragraphs(text: str) -> List[str]:
    if not text.strip():
        return []
    return [part for part in _PARAGRAPH_SPLIT.split(text.strip()) if part.strip()]


def _detect_style(lines: Sequence[str]) -> str:
    for line in lines:
        if _HEADING_QUESTION.match(line) is not None:
            return "heading"
    for line in lines:
        if _INLINE_QUESTION.match(line) is not None:
            return "inline"
    raise SolutionSourceError("文档中没有可识别的题目块（既无 `### 第 N 题` 也无 `**N．**`）")


def _question_start(style: str, line: str) -> Optional[Tuple[int, str, str]]:
    if style == "heading":
        match = _HEADING_QUESTION.match(line)
        if match is None:
            return None
        return int(match.group(1)), match.group(2), ""
    match = _INLINE_QUESTION.match(line)
    if match is None:
        return None
    return int(match.group(1)), match.group(2), match.group(3)


def _terminates_block(style: str, line: str) -> bool:
    match = _ATX_HEADING.match(line)
    if match is None:
        return False
    # heading 式里 `#### (k)` 是小问标题，必须留在题内；`###` 及以上结束本题。
    return len(match.group(1)) <= 3 if style == "heading" else True


def _subparts(style: str, lines: Sequence[str]) -> Tuple[int, ...]:
    """取本题的小问集合。

    同一小问可以拆成多段标题（真题里 `#### (2) ①` 与 `#### (2) ②` 常见），
    因此只要求编号非递减、去重后是从 1 开始的连续升序。
    """
    pattern = _HEADING_SUBPART if style == "heading" else _INLINE_SUBPART
    found: List[int] = []
    for line in lines:
        match = pattern.match(line)
        if match is not None:
            found.append(int(match.group(1)))
    if found != sorted(found):
        raise SolutionSourceError(f"小问编号必须非递减，实际 {found}")
    distinct = tuple(sorted(set(found)))
    if distinct and distinct != tuple(range(1, len(distinct) + 1)):
        raise SolutionSourceError(f"小问编号必须是从 1 开始的连续整数，实际 {distinct}")
    return distinct


def parse_question_blocks(
    text: str, style: Optional[str] = None
) -> Tuple[QuestionBlock, ...]:
    """把一份 Markdown 文档切成题目块。

    `style` 省略时自动识别；`### 第 N 题` 优先于 `**N．**`。
    重复题号、题号乱序、小问编号不连续都会立即报错。
    """
    lines = text.split("\n")
    if style is None:
        style = _detect_style(lines)
    elif style not in {"heading", "inline"}:
        raise SolutionSourceError(f"未知题号写法：{style!r}")

    starts: List[Tuple[int, int, str, str]] = []
    stops: List[int] = []
    for index, line in enumerate(lines):
        start = _question_start(style, line)
        if start is not None:
            starts.append((index, start[0], start[1], start[2]))
        elif _terminates_block(style, line):
            stops.append(index)
    if not starts:
        raise SolutionSourceError("文档中没有可识别的题目块")

    blocks: List[QuestionBlock] = []
    previous_end = 0
    for position, (index, number, title, remainder) in enumerate(starts):
        limit = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        for stop in stops:
            if index < stop < limit:
                limit = stop
                break
        body_lines = ([remainder] if remainder.strip() else []) + lines[index + 1:limit]
        blocks.append(QuestionBlock(
            number=number,
            title=title.rstrip(),
            body="\n".join(body_lines).strip(),
            subparts=_subparts(style, body_lines),
            lead="\n".join(lines[previous_end:index]).strip(),
        ))
        previous_end = limit

    # 最后一题之后的内容没有归属，重建文档时会被静默丢掉——一个写成
    # `### 第 22 题　〔…〕` 的标题就曾让整个选考题章节人间蒸发。宁可报错。
    trailer = "\n".join(lines[previous_end:]).strip()
    if trailer:
        raise SolutionSourceError(
            "最后一题之后还有未归属的内容，重建时会丢失：{0!r}".format(trailer[:80])
        )

    numbers = [block.number for block in blocks]
    duplicates = sorted({number for number in numbers if numbers.count(number) > 1})
    if duplicates:
        raise SolutionSourceError(f"重复题号：{duplicates}")
    if numbers != sorted(numbers):
        raise SolutionSourceError(f"题号乱序：{numbers}")
    return tuple(blocks)


def parse_answer_points(text: str) -> Tuple[AnswerPoint, ...]:
    """从 `_答案要点.md` 取出逐题最终答案。"""
    points: List[AnswerPoint] = []
    for block in parse_question_blocks(text, style="inline"):
        answers: List[Tuple[Optional[int], str]] = []
        for line in block.body.split("\n"):
            match = _ANSWER_LINE.match(_strip_quote(line).strip())
            if match is None:
                continue
            pre, post = match.group("pre"), match.group("post")
            if pre is not None and post is not None:
                raise SolutionSourceError(
                    f"第 {block.number} 题的答案块同时写了两处小问号：{line.strip()}"
                )
            key = pre if pre is not None else post
            answers.append((
                int(key) if key is not None else None,
                match.group("value").strip(),
            ))
        if not answers:
            raise SolutionSourceError(f"第 {block.number} 题没有可识别的加粗答案块")
        keys = [key for key, _ in answers]
        if None in keys and len(keys) > 1:
            raise SolutionSourceError(
                f"第 {block.number} 题混用了整题答案与小问答案，无法唯一识别答案块"
            )
        if None not in keys and keys != list(range(1, len(keys) + 1)):
            raise SolutionSourceError(
                f"第 {block.number} 题的小问答案编号必须是从 1 开始的连续升序，实际 {keys}"
            )
        points.append(AnswerPoint(number=block.number, answers=tuple(answers)))
    return tuple(points)


def _is_answer_paragraph(paragraph: str) -> bool:
    """整段只有一行、且以加粗答案块开头，才算提取边界。

    多行段落即使首行像答案块也不丢——那会连带吞掉后续说明文字。
    """
    stripped = paragraph.strip()
    return "\n" not in stripped and _ANSWER_LINE.match(stripped) is not None


def _is_question_restatement(paragraph: str) -> bool:
    return paragraph.strip().startswith(QUESTION_MARKER)


def _is_solution_marker(paragraph: str) -> bool:
    return paragraph.split("\n", 1)[0].strip() == SOLUTION_MARKER


def _derivation_paragraphs(body: str) -> List[str]:
    """取出一题的详细推导段落，丢掉题面复述与显式最终答案块。

    两级边界：

    1. 段首是规范 `**解析**` 标记时，标记之前的一切都是题面区，整体丢弃。本工具
       自己生成的 `_含解析.md` 走这条路——题面在那里横跨多段（选项、配图、小问），
       只靠逐段识别是分不干净的，所以规范标记必须是权威边界。
    2. 没有规范标记时（真题里 `**解析要点**`、`**(1) 解**` 和直接的 `#### (1)`
       都出现过，把任何一种当成必需标记都会让绝大多数解答题无法提取），退化为逐段
       识别：丢掉题面复述段及其紧随的纯图片段。题面配图总是紧跟题面复述、由
       `_试题.md` 拥有；推导中间引用的图片不在这个位置，不会被误删。
    """
    paragraphs = _paragraphs(body)
    for index, paragraph in enumerate(paragraphs):
        if _is_solution_marker(paragraph):
            paragraphs = paragraphs[index:]
            break

    kept: List[str] = []
    skipping_figures = False
    for paragraph in paragraphs:
        stripped = paragraph.strip()
        if _is_answer_paragraph(stripped):
            continue
        if _is_question_restatement(stripped):
            skipping_figures = True
            continue
        if skipping_figures and _IMAGE_PARAGRAPH.match(stripped) is not None:
            continue
        skipping_figures = False
        kept.append(paragraph)
    return kept


def _join_segments(segments: Sequence[str]) -> str:
    body = "\n\n".join(segment for segment in segments if segment)
    return body + "\n" if body else ""


def _heading(number: int, title: str) -> str:
    """标题后缀原样重建，不重新加括号。"""
    return f"### 第 {number} 题{title}"


def _canonical_derivation(body: str) -> str:
    """把一题的正文规范成「`**解析**` 打头的详细推导」。"""
    paragraphs = _derivation_paragraphs(body)
    if paragraphs and _is_solution_marker(paragraphs[0]):
        return "\n\n".join(paragraphs)
    return "\n\n".join([SOLUTION_MARKER] + paragraphs)


def extract_solution_blocks(combined: str) -> str:
    """从 `_含解析.md` 提取规范的 `_解析正文.md` 文本。

    每题固定输出 `### 第 N 题（原解析标题）` + `**解析**` + 原详细推导；
    独立的题面复述（含紧随其后的题面配图）与显式最终答案块一律丢弃。
    对已经规范的 `_解析正文.md` 再跑一次是恒等变换。
    """
    segments: List[str] = []
    for block in parse_question_blocks(combined, style="heading"):
        if block.lead:
            segments.append(block.lead)
        segments.append(_heading(block.number, block.title))
        segments.append(_canonical_derivation(block.body))
    return _join_segments(segments)


def validate_solution_body(text: str) -> Tuple[QuestionBlock, ...]:
    """校验 `_解析正文.md` 没有复制题面或最终答案。"""
    blocks = parse_question_blocks(text, style="heading")
    for block in blocks:
        for paragraph in _paragraphs(block.body):
            if _is_question_restatement(paragraph):
                raise SolutionSourceError(
                    f"第 {block.number} 题的解析正文复制了题面：{paragraph.strip()!r}"
                )
            if _is_answer_paragraph(paragraph):
                raise SolutionSourceError(
                    f"第 {block.number} 题的解析正文含独立加粗答案块：{paragraph.strip()!r}"
                )
    return blocks


def _aligned(label: str, expected: Set[int], actual: Set[int]) -> None:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise SolutionSourceError(
            f"{label}题号集合与试题不一致：缺 {missing}、多 {extra}"
        )


def _render_answer_paragraphs(point: AnswerPoint) -> List[str]:
    rendered: List[str] = []
    for key, value in point.answers:
        rendered.append(
            f"**答案：{value}**" if key is None else f"**答案（{key}）：{value}**"
        )
    return rendered


def render_combined(questions_text: str, solution_text: str, answer_text: str) -> str:
    """由三份规范源确定性生成 `_含解析.md`：题目 → 解析 → 生成答案块。"""
    question_blocks = parse_question_blocks(questions_text)
    solution_blocks = validate_solution_body(solution_text)
    answer_points = parse_answer_points(answer_text)

    questions = {block.number: block for block in question_blocks}
    expected = set(questions)
    _aligned("解析正文", expected, {block.number for block in solution_blocks})
    _aligned("答案要点", expected, {point.number for point in answer_points})
    answers = {point.number: point for point in answer_points}

    for block in solution_blocks:
        question = questions[block.number]
        for label, actual in (
            ("解析正文", set(block.subparts)),
            ("答案要点", set(answers[block.number].subparts)),
        ):
            if actual != set(question.subparts):
                raise SolutionSourceError(
                    "第 {0} 题的{1}小问集合与试题不一致：试题 {2}、{1} {3}".format(
                        block.number, label,
                        sorted(question.subparts), sorted(actual),
                    )
                )

    segments: List[str] = []
    for block in solution_blocks:
        if block.lead:
            segments.append(block.lead)
        question = questions[block.number]
        segments.append(_heading(block.number, block.title))
        segments.append(
            f"{QUESTION_MARKER}{question.title}："
            if question.title else f"{QUESTION_MARKER}："
        )
        if question.body:
            segments.append(question.body)
        segments.append(_canonical_derivation(block.body))
        segments.extend(_render_answer_paragraphs(answers[block.number]))
    return _join_segments(segments)


# ---------------------------------------------------------------- manifest 与仓库


def _repository_root(path: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(Path(path).resolve()), "rev-parse", "--show-toplevel"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return Path(result.stdout.strip()).resolve()


def _relative_to_repo(root: Path, path: Path) -> str:
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError as error:
        raise SolutionSourceError(f"路径不在仓库内：{path}") from error


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise SolutionSourceError(f"无法读取 {path}：{error}") from error


def _paper_sources(paper: Mapping[str, Any]) -> PaperSources:
    files = paper["source_files"]
    return PaperSources(
        paper_id=paper["paper_id"],
        question_count=paper["question_count"],
        questions=files["questions"],
        answer_key=files["answer_key"],
        solution_body=files["solution_body"],
        combined_rendered=files["combined_rendered"],
    )


def batch_papers(manifest: Mapping[str, Any], batch_id: str) -> Tuple[PaperSources, ...]:
    batches = [item for item in manifest["batches"] if item["batch_id"] == batch_id]
    if len(batches) != 1:
        raise SolutionSourceError(f"未知批次：{batch_id}")
    papers = {paper["paper_id"]: paper for paper in manifest["papers"]}
    selected: List[PaperSources] = []
    for paper_id in batches[0]["paper_ids"]:
        if paper_id not in papers:
            raise SolutionSourceError(f"批次 {batch_id} 引用了不存在的 paper_id：{paper_id}")
        selected.append(_paper_sources(papers[paper_id]))
    return tuple(selected)


def all_papers(manifest: Mapping[str, Any]) -> Tuple[PaperSources, ...]:
    return tuple(_paper_sources(paper) for paper in manifest["papers"])


def build_paper_targets(repo_root: Path, sources: PaperSources) -> Dict[str, bytes]:
    """在内存里生成本卷的 `_解析正文.md` 与 `_含解析.md` 字节。

    `_解析正文.md` 已存在时以它为提取源（它才是事实源）；只有首次迁移才回退到
    现有 `_含解析.md`。两条路径都要过一遍 `extract_solution_blocks`，因此人工
    回填进解析正文的题面或答案会被规范化掉，而不是悄悄留在事实源里。
    """
    try:
        questions_text = _read_text(repo_root / sources.questions)
        answer_text = _read_text(repo_root / sources.answer_key)
        solution_path = repo_root / sources.solution_body
        if solution_path.is_file():
            raw = _read_text(solution_path)
        else:
            combined_path = repo_root / sources.combined_rendered
            if not combined_path.is_file():
                raise SolutionSourceError(
                    f"解析正文与含解析都不存在，无法提取：{sources.solution_body}"
                )
            raw = _read_text(combined_path)
        solution_text = extract_solution_blocks(raw)
        combined_text = render_combined(questions_text, solution_text, answer_text)
        count = len(parse_question_blocks(solution_text, style="heading"))
        if count != sources.question_count:
            raise SolutionSourceError(
                f"题目数与 manifest 不一致：manifest {sources.question_count}、实际 {count}"
            )
    except SolutionSourceError as error:
        raise SolutionSourceError(f"{sources.paper_id}: {error}") from error
    return {
        sources.solution_body: solution_text.encode("utf-8"),
        sources.combined_rendered: combined_text.encode("utf-8"),
    }


def _file_record(
    repo_root: Path, relative: str, expected: Optional[bytes]
) -> Dict[str, Any]:
    path = repo_root / relative
    record: Dict[str, Any] = {
        "path": relative,
        "sha256": file_sha256(path) if path.is_file() else None,
    }
    if expected is not None:
        record["expected_sha256"] = hashlib.sha256(expected).hexdigest()
    return record


def check_paper(repo_root: Path, sources: PaperSources) -> Dict[str, Any]:
    """只读核对一卷：四份文件齐全、题号/小问对齐、两份派生物等于确定性生成结果。"""
    problems: List[str] = []
    for label, relative in (
        ("试题", sources.questions),
        ("答案要点", sources.answer_key),
        ("解析正文", sources.solution_body),
        ("含解析", sources.combined_rendered),
    ):
        if not (repo_root / relative).is_file():
            problems.append(f"{label}缺失：{relative}")

    targets: Dict[str, bytes] = {}
    if not problems:
        try:
            targets = build_paper_targets(repo_root, sources)
        except SolutionSourceError as error:
            problems.append(str(error))
    for relative, expected in sorted(targets.items()):
        if (repo_root / relative).read_bytes() != expected:
            problems.append(f"{relative} 与确定性生成结果不一致")

    numbers: Optional[List[int]] = None
    questions_path = repo_root / sources.questions
    if questions_path.is_file():
        try:
            numbers = [
                block.number
                for block in parse_question_blocks(_read_text(questions_path))
            ]
        except SolutionSourceError as error:
            problems.append(f"{sources.paper_id}: 试题无法解析：{error}")

    return {
        "paper_id": sources.paper_id,
        "question_count": sources.question_count,
        "question_numbers": numbers,
        "files": {
            "questions": _file_record(repo_root, sources.questions, None),
            "answer_key": _file_record(repo_root, sources.answer_key, None),
            "solution_body": _file_record(
                repo_root, sources.solution_body, targets.get(sources.solution_body)
            ),
            "combined_rendered": _file_record(
                repo_root, sources.combined_rendered,
                targets.get(sources.combined_rendered),
            ),
        },
        "problems": problems,
        "ok": not problems,
    }


def render_migration_report(
    manifest: Mapping[str, Any], repo_root: Path, manifest_path: Path
) -> Dict[str, Any]:
    """聚合全部试卷的题号、原/新文件哈希与检查结果。"""
    papers = [check_paper(repo_root, sources) for sources in all_papers(manifest)]
    papers.sort(key=lambda record: record["paper_id"])
    return {
        "report_version": REPORT_VERSION,
        "inputs": {
            "manifest_sha256": file_sha256(manifest_path),
            "manifest_revision": manifest["revision"],
            "tool_sha256": file_sha256(repo_root / TOOL_SOURCE_TARGET),
        },
        "papers": papers,
        "summary": {
            "paper_count": len(papers),
            "ok_count": sum(1 for record in papers if record["ok"]),
            "problem_count": sum(1 for record in papers if not record["ok"]),
        },
    }


# ---------------------------------------------------------------- 批次提取（content 事务）


def extract_batch(
    manifest_path: Path,
    batch_id: str,
    event_hook: Any = None,
) -> Dict[str, Any]:
    """整批提取并以单个 `content` 事务提交两类派生物。

    先在内存生成并校验全批目标，任何一卷失败都不落盘。
    """
    manifest_path = Path(manifest_path)
    root = _repository_root(manifest_path.parent)
    manifest_relative = _relative_to_repo(root, manifest_path)
    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        selected = batch_papers(manifest, batch_id)
        manifest_sha256 = file_sha256(manifest_path)
        inputs: Dict[str, Optional[str]] = {
            manifest_relative: manifest_sha256,
            TOOL_SOURCE_TARGET: file_sha256(root / TOOL_SOURCE_TARGET),
        }
        targets: Dict[str, bytes] = {}
        for sources in selected:
            for relative in (sources.questions, sources.answer_key):
                inputs[relative] = file_sha256(root / relative)
            for relative, value in build_paper_targets(root, sources).items():
                if relative in targets:
                    raise SolutionSourceError(f"批次内目标路径重复：{relative}")
                targets[relative] = value

        overlap = sorted(set(inputs) & set(targets))
        if overlap:
            raise SolutionSourceError(f"只读输入与写目标重叠：{overlap}")

        unchanged = all(
            (root / relative).is_file() and (root / relative).read_bytes() == value
            for relative, value in targets.items()
        )
        if unchanged:
            return {"batch_id": batch_id, "written": False, "targets": sorted(targets)}

        transaction = Transaction(root, event_hook=event_hook)
        transaction.prepare("content", targets, inputs)
        try:
            transaction.commit()
        except RuntimeError as error:
            # manifest 属于业务投影，不在通用事务层解释：这里翻译成「从新快照重跑」。
            if file_sha256(manifest_path) != manifest_sha256:
                raise SolutionSourceError(
                    "manifest 在提取期间发生变化，本次提取已安全中止；"
                    "请从新的 manifest 快照重跑 extract-batch"
                ) from error
            raise
        return {"batch_id": batch_id, "written": True, "targets": sorted(targets)}


# ---------------------------------------------------------------- git 范围核对


def _git_lines(root: Path, arguments: Sequence[str]) -> List[str]:
    raw = subprocess.run(
        ["git", "-C", str(root)] + list(arguments),
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def _read_pathspec(path: Path) -> List[str]:
    try:
        raw = Path(path).read_bytes()
    except OSError as error:
        raise SolutionSourceError(f"无法读取 pathspec 文件：{path}：{error}") from error
    entries: List[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            entry = item.decode("utf-8")
        except UnicodeDecodeError as error:
            raise SolutionSourceError("pathspec 文件中存在非 UTF-8 路径") from error
        candidate = Path(entry)
        if candidate.is_absolute() or any(
            part in {"", ".", ".."} for part in candidate.parts
        ):
            raise SolutionSourceError(f"pathspec 必须是安全的仓库相对路径：{entry}")
        entries.append(candidate.as_posix())
    if not entries:
        raise SolutionSourceError(f"pathspec 文件为空：{path}")
    return entries


def check_staged(root: Path, scope: Sequence[str]) -> List[str]:
    """核对暂存区恰好覆盖所有权范围内相对 HEAD 的实际变更。

    返回问题清单；空清单表示通过。字节未变的目标不要求出现在 staged diff 里。
    """
    scoped = set(scope)
    staged = set(_git_lines(root, ["diff", "--cached", "--name-only", "-z", "HEAD", "--"]))
    unstaged = set(_git_lines(root, ["diff", "--name-only", "-z", "--"]))
    untracked = set(_git_lines(root, ["ls-files", "--others", "--exclude-standard", "-z"]))
    # 相对 HEAD 的实际变更/新增/删除：tracked 侧由 diff HEAD 给出，新增文件补上 untracked。
    actual = set(
        _git_lines(root, ["diff", "--name-only", "-z", "HEAD", "--"])
    ) | untracked

    problems: List[str] = []
    outside = sorted(staged - scoped)
    if outside:
        problems.append(f"范围外存在 staged 变更：{outside}")
    missing = sorted((actual & scoped) - staged)
    if missing:
        problems.append(f"范围内的实际变更未全部 staged：{missing}")
    residue = sorted((unstaged | untracked) & scoped)
    if residue:
        problems.append(f"范围内存在 unstaged 残留：{residue}")
    return problems


# ---------------------------------------------------------------- CLI


def _print_checks(records: Sequence[Mapping[str, Any]]) -> int:
    for record in records:
        if record["ok"]:
            print("ok   {0}（{1} 题）".format(
                record["paper_id"], record["question_count"]
            ))
            continue
        print("FAIL {0}".format(record["paper_id"]), file=sys.stderr)
        for problem in record["problems"]:
            print("       {0}".format(problem), file=sys.stderr)
    failed = [record for record in records if not record["ok"]]
    if failed:
        print("共 {0}/{1} 套未通过".format(len(failed), len(records)), file=sys.stderr)
        return 1
    print("{0} 套全部通过".format(len(records)))
    return 0


def _check_command(arguments: argparse.Namespace) -> int:
    manifest_path = Path(arguments.manifest)
    root = _repository_root(manifest_path.parent)
    manifest = load_manifest(manifest_path)
    if arguments.command == "check-batch":
        selected = batch_papers(manifest, arguments.batch)
    else:
        selected = all_papers(manifest)
    return _print_checks([check_paper(root, sources) for sources in selected])


def _extract_batch_command(arguments: argparse.Namespace) -> int:
    result = extract_batch(Path(arguments.manifest), arguments.batch)
    if result["written"]:
        print("已提交 {0} 个目标：{1}".format(
            len(result["targets"]), result["batch_id"]
        ))
    else:
        print("{0} 的目标已是最新，未开启事务".format(result["batch_id"]))
    return 0


def _report_command(arguments: argparse.Namespace) -> int:
    manifest_path = Path(arguments.manifest)
    root = _repository_root(manifest_path.parent)
    output_relative = _relative_to_repo(root, Path(arguments.output))
    if output_relative != REPORT_TARGET:
        raise SolutionSourceError(
            f"--output 必须是 {REPORT_TARGET}，实际 {output_relative}"
        )
    # 单文件生成器：取仓库锁并恢复未完成事务后，同目录临时文件 + os.replace。
    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        report = render_migration_report(manifest, root, manifest_path)
        (root / output_relative).parent.mkdir(parents=True, exist_ok=True)
        atomic_write_json(root / output_relative, report)
    print("已写入 {0}：{1}".format(output_relative, canonical_json(report["summary"])))
    return 0 if report["summary"]["problem_count"] == 0 else 1


def _output_paths_command(arguments: argparse.Namespace) -> int:
    manifest_path = Path(arguments.manifest)
    root = _repository_root(manifest_path.parent)
    manifest = load_manifest(manifest_path)
    paths: List[str] = []
    for sources in batch_papers(manifest, arguments.batch):
        paths.append(sources.solution_body)
        paths.append(sources.combined_rendered)
    if arguments.include_report is not None:
        report_relative = _relative_to_repo(root, Path(arguments.include_report))
        if report_relative != REPORT_TARGET:
            raise SolutionSourceError(
                f"--include-report 必须是 {REPORT_TARGET}，实际 {report_relative}"
            )
        paths.append(report_relative)
    duplicates = sorted({item for item in paths if paths.count(item) > 1})
    if duplicates:
        raise SolutionSourceError(f"所有权范围内路径重复：{duplicates}")
    sys.stdout.buffer.write(b"".join(item.encode("utf-8") + b"\0" for item in paths))
    sys.stdout.buffer.flush()
    return 0


def _check_staged_command(arguments: argparse.Namespace) -> int:
    pathspec_path = Path(arguments.pathspec_file)
    root = _repository_root(Path.cwd())
    problems = check_staged(root, _read_pathspec(pathspec_path))
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("暂存区与所有权范围一致")
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="解析正文唯一源与含解析确定性生成器")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract-batch")
    extract.add_argument("--manifest", required=True, type=Path)
    extract.add_argument("--batch", required=True)
    # 显式必填：不给 --write 就不该以为自己在演练，写入是本子命令唯一语义。
    extract.add_argument("--write", required=True, action="store_true")

    check_batch = subparsers.add_parser("check-batch")
    check_batch.add_argument("--manifest", required=True, type=Path)
    check_batch.add_argument("--batch", required=True)

    check_all = subparsers.add_parser("check-all")
    check_all.add_argument("--manifest", required=True, type=Path)

    report = subparsers.add_parser("report")
    report.add_argument("--manifest", required=True, type=Path)
    report.add_argument("--output", required=True, type=Path)

    output_paths = subparsers.add_parser("output-paths")
    output_paths.add_argument("--manifest", required=True, type=Path)
    output_paths.add_argument("--batch", required=True)
    output_paths.add_argument("--include-report", type=Path, default=None)
    output_paths.add_argument("--nul", required=True, action="store_true")

    staged = subparsers.add_parser("check-staged")
    staged.add_argument("--pathspec-file", required=True, type=Path)
    staged.add_argument("--nul", required=True, action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "extract-batch":
        return _extract_batch_command(arguments)
    if arguments.command in {"check-batch", "check-all"}:
        return _check_command(arguments)
    if arguments.command == "report":
        return _report_command(arguments)
    if arguments.command == "output-paths":
        return _output_paths_command(arguments)
    if arguments.command == "check-staged":
        return _check_staged_command(arguments)
    raise SolutionSourceError(f"未知命令：{arguments.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

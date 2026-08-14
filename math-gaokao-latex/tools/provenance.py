#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""provenance.py —— 逐题来源核验、三角色 `.work` 导入与真实 facts adapter。

**本模块只产 facts，不产状态。** `derive_status()` / `reconcile_batch_status()` 的唯一
属主仍是 `status.py`（Task 15）——这里既不复制它的规则，也不建第二套 reconciler。理由
与 status.py 顶部那两条一字不差：混合状态下的第二套规则不会报错，只会静默给出两个都
自洽的答案。

三种哈希，口径逐字冻结（任一变化都使核验失效）：

1. `question_text_sha256` —— `_试题.md` 中该题**题面块**去掉行尾空白、统一 LF 后的
   UTF-8 SHA-256。块边界取 `solution_sources.parse_question_blocks()`，不另立一套切分；
2. `answer_sha256` —— **绝不对自由文本直接取哈希**。先由 `parse_answer_points()` 折出
   `AnswerRecord`（`make_short_answers.expected_answer_records()` 就是这条链），按
   `question_id` 与小问序号的 UTF-8 码点排序，构造
   `{"question_id":…,"parts":[{"part":…,"answer":…}]}`，再用 Task 1 的
   `canonical_json()` 序列化取 UTF-8 SHA-256。整题答案的 `part` 是空串；
3. `source_sha256` —— 上游卷取 manifest artifact 的 SHA-256，本地 legacy 卷现场重算
   文件 SHA-256。

来源引用是 oneOf：上游 `{"source_id": …}` 或本地 `{"path": …}`。**有效 ≠ 属于本卷**是
本模块最贵的一条判据：一个 ready、artifact 当前、双向关系成立的 source 只要不在本卷的
`source_ids` 里就必须被拒；本地路径只认 paper 显式登记的 `legacy_source_files`，且仅在
该卷没有确认上游 source 时才允许。回忆版的身份 blocker 由问题总账继续阻止 `complete`。

`invalid` 与 `stale` 的分界：文档自身写错（Schema、题号、角色重复、引用不属于本卷）是
`invalid`；文档当时对、世界变了（源文件被改、source 不再 ready、页数缩了）是 `stale`。
两者在状态核心里都是「不是 current」，分开只为让报错说得清该修哪一边。
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_projects
import cli_common
import generate_projects
import issues as issues_module
import make_editions
import make_short_answers
import source_manifest
import status as status_core
from manifest import canonical_json, file_sha256, load_manifest
from schema_validate import SchemaError
from schema_validate import validate as validate_schema
from solution_sources import SolutionSourceError, parse_question_blocks
from status import (
    ISSUES_TARGET,
    MANIFEST_TARGET,
    PROJECT_RELATIVE,
    REVIEW_STATES,
    StatusError,
    build_receipt_path,
    derive_git_state,
    derive_status,
    paper_provenance_paths,
    provenance_path,
    reconcile_batch_status,
    review_receipt_path,
)
from transaction import RepoLock, Transaction

INDEX_TARGET = PROJECT_RELATIVE + "/index.json"
SCHEMA_TARGET = PROJECT_RELATIVE + "/schemas/provenance.schema.json"
WORK_RELATIVE = PROJECT_RELATIVE + "/.work"
DEFAULT_MANIFEST = PROJECT_ROOT / "source-manifest.json"
DEFAULT_ISSUES = PROJECT_ROOT / "missing-issues.md"

GENERATED_BY = "tools/provenance.py"
SCHEMA_VERSION = 1

STAGES: Tuple[str, ...] = ("question-review", "answer-solve", "answer-review")
TRANSCRIPTION_RESULTS: Tuple[str, ...] = ("passed", "failed", "uncertain")
ANSWER_GRADES: Tuple[str, ...] = ("A", "B", "C", "D", "U")
CONFLICT_STATES: Tuple[str, ...] = ("none", "resolved", "unresolved")

# `confirm-source` 固定写这个关系：阶段 0 不产生 duplicate 类关系，做成参数只会给
# 「随手标成 duplicate」留口子。
PAPER_RELATION = "canonical"
# 「尚未了结」= 未 resolved（deferred 也算未了结——推迟不是解决）。**由 issues 的状态
# 全集取反派生，而不是手写白名单**：白名单在 `issues.STATUSES` 新增状态时会让这条一票
# 否决的守卫默认放行，而它的默认必须是拒绝。判据本身也用取反（见 `_identity_blockers`），
# 这个常量只为让「哪些算未了结」在报错与文档里可读。
UNFINISHED_ISSUE_STATES: Tuple[str, ...] = tuple(
    sorted(issues_module.STATUSES - {"resolved"})
)

QUESTION_FIELDS: Tuple[str, ...] = (
    "question_id", "printed_number", "source_ref", "source_sha256", "source_pages",
    "question_text_sha256", "answer_sha256", "transcription_review",
    "answer_evidence", "solver_role", "reviewer_role", "conflict_status", "issue_ids",
)

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_INVALID = 4

# 工具链解析不出来时的哨兵：它与任何真实指纹都不相等，于是既有回执一律降级为 stale。
# 传 `None` 会让 `receipt_currency()` **跳过**第四条证据——那正是 fail-open。
UNRESOLVED_TOOLCHAIN: Dict[str, Any] = {"toolchain": "unresolved"}


class ProvenanceError(ValueError):
    """Schema、语义、导入与只读核对的唯一异常类型。"""


class _StaleProvenance(ProvenanceError):
    """文档当时对、世界变了：源文件被改、source 不再 ready、页数缩了。"""


# ---------------------------------------------------------------- 小件


def _paper(manifest: Mapping[str, Any], paper_id: str) -> Mapping[str, Any]:
    for paper in manifest.get("papers", []):
        if paper["paper_id"] == paper_id:
            return paper
    raise ProvenanceError(f"未知 paper_id：{paper_id}")


def _batch(manifest: Mapping[str, Any], batch_id: str) -> Mapping[str, Any]:
    found = [
        item for item in manifest.get("batches", []) if item["batch_id"] == batch_id
    ]
    if len(found) != 1:
        raise ProvenanceError(f"未知批次：{batch_id}")
    return found[0]


def _batch_of(manifest: Mapping[str, Any], paper_id: str) -> Optional[str]:
    for batch in manifest.get("batches", []):
        if paper_id in batch["paper_ids"]:
            return batch["batch_id"]
    return None


def _relative_to(root: Path, path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError as error:
        raise ProvenanceError(f"路径不在仓库内：{path}") from error


def _require_canonical(root: Path, path: Path, expected: str, option: str) -> Path:
    resolved = Path(path).resolve()
    if _relative_to(root, resolved) != expected:
        raise ProvenanceError(f"{option} 必须是 {expected}")
    return resolved


def _read_text(root: Path, relative: str) -> str:
    try:
        return (Path(root) / relative).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise _StaleProvenance(f"无法读取规范源 {relative}：{error}") from error


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def question_id(paper_id: str, printed_number: int) -> str:
    """题号 ID 由 paper_id 与印刷题号确定性派生，不接受人工命名。

    自由命名的题号 ID 会让「同一道题在两份文档里叫两个名字」成为可能，而问题总账的
    fingerprint 身份正是 (type, paper_id, question_id, source_id)。
    """
    if not isinstance(printed_number, int) or isinstance(printed_number, bool):
        raise ProvenanceError("printed_number 必须是整数")
    if printed_number <= 0:
        raise ProvenanceError("printed_number 必须是正整数")
    return "%s-q%02d" % (paper_id, printed_number)


# ---------------------------------------------------------------- 三种哈希


def _normalized(text: str) -> str:
    """统一 LF、去每行行尾空白、去首尾空行。"""
    unified = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in unified.split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


_THEMATIC_BREAK = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})$")
_BLOCKQUOTE = re.compile(r"^[ \t]*>")


def _strip_file_footer(lines: Sequence[str]) -> List[str]:
    """剥掉文末页脚段：末条 thematic break 之后只剩引用块时，连同那条 break 一起剥。

    判据依据真库 21 份 `_试题.md` 的实测形状——每一份都以

    ```text
    ---

    > **原卷影印件**：[`../_raw/….pdf`](…)      # 或 `> **试题来源**：deekur/gaokaomath…`
    ```

    收尾，break 之后**恰好一行非空且是引用块**。因此判据取「break 之后的非空行全部是
    引用块、且至少有一行」，而不是「剥掉最后一段」——后者会连真正的题面一起吃掉。

    这条规则**只对最后一题块生效**（见 `question_text_digests`）：题间的 `---` 落在
    上一题正文里，跨卷逐字相同、本来就不构成差异；只有末题后面没有下一题来接管，才会
    把页脚吸进正文。判不准时**宁可不剥**：多算进页脚只会让摘要更严，少算才会让核验
    静默失效。
    """
    lines = list(lines)
    positions = [
        index for index, line in enumerate(lines)
        if _THEMATIC_BREAK.fullmatch(line.strip())
    ]
    if not positions:
        return lines
    cut = positions[-1]
    trailing = [item for item in lines[cut + 1:] if item.strip()]
    if not trailing or any(_BLOCKQUOTE.match(item) is None for item in trailing):
        return lines
    return lines[:cut]


def question_block_text(block: Any, strip_footer: bool = False) -> str:
    """题面块的规范文本：标题行余部 + 正文，规范化后拼接。

    题号本身不进哈希——它由 `printed_number` 单独记录；块间的 `lead`（章节标题、
    分隔线）也不进，那是题与题之间的东西，改动它不该让整卷核验失效。

    `strip_footer` 只由最后一题传 True：文末页脚没有下一题来接管，会被解析器算进末题
    正文，于是末题摘要不再是题面的纯函数——2017 理/文两卷 q23 题面逐字相同却算出两个
    摘要，差异全在页脚里的那条 PDF 路径。
    """
    lines = _normalized("%s\n%s" % (block.title, block.body)).split("\n")
    if strip_footer:
        lines = _strip_file_footer(lines)
    return _normalized("\n".join(lines))


def question_text_digests(questions_text: str) -> Dict[int, str]:
    """`_试题.md` 逐题题面哈希，键为印刷题号。"""
    try:
        blocks = parse_question_blocks(questions_text)
    except SolutionSourceError as error:
        raise _StaleProvenance(f"试题规范源无法解析：{error}") from error
    last = blocks[-1].number if blocks else None
    return {
        block.number: _sha256_text(
            question_block_text(block, strip_footer=block.number == last)
        )
        for block in blocks
    }


def answer_digests(paper_id: str, answer_key_text: str) -> Dict[int, str]:
    """`_答案要点.md` 逐题答案哈希，键为印刷题号。

    走的是 `parse_answer_points()` → `AnswerRecord` 这条唯一答案真值链：直接对
    Markdown 取哈希会让「改个标点」与「改掉一个答案」在证据上不可区分。
    """
    try:
        records = make_short_answers.expected_answer_records(answer_key_text)
    except (make_short_answers.ShortAnswerError, SolutionSourceError) as error:
        raise _StaleProvenance(f"答案规范源无法解析：{error}") from error
    grouped: Dict[int, List[Any]] = {}
    for record in records:
        grouped.setdefault(record.number, []).append(record)
    digests: Dict[int, str] = {}
    # 题间按 question_id 的码点序，题内按小问序号的码点序（整题答案的 part 是空串，
    # 码点序里它排在最前）。两级排序都固定，哈希才与遍历顺序无关。
    for number in sorted(grouped, key=lambda item: question_id(paper_id, item)):
        parts = sorted(
            (
                {
                    "part": "" if item.subpart is None else str(item.subpart),
                    "answer": item.value,
                }
                for item in grouped[number]
            ),
            key=lambda item: item["part"],
        )
        payload = {"question_id": question_id(paper_id, number), "parts": parts}
        digests[number] = _sha256_text(canonical_json(payload))
    return digests


def source_identity(source_ref: Mapping[str, Any]) -> str:
    """问题总账用的来源身份：上游取 source_id，本地取 `legacy:<路径>`。"""
    if "source_id" in source_ref:
        return str(source_ref["source_id"])
    return "legacy:%s" % source_ref["path"]


# ---------------------------------------------------------------- Schema


_SCHEMA_CACHE: Dict[str, Any] = {}


def schema() -> Mapping[str, Any]:
    if not _SCHEMA_CACHE:
        path = PROJECT_ROOT / "schemas" / "provenance.schema.json"
        try:
            _SCHEMA_CACHE.update(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ProvenanceError(f"无法读取 provenance Schema：{error}") from error
    return _SCHEMA_CACHE


def new_provenance(
    paper_id: str, batch_id: str, questions: Sequence[Mapping[str, Any]]
) -> Dict[str, Any]:
    """组装一份 provenance 文档（按印刷题号升序），不做落盘也不做语义校验。"""
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": GENERATED_BY,
        "paper_id": paper_id,
        "batch_id": batch_id,
        "questions": [
            copy.deepcopy(dict(item))
            for item in sorted(questions, key=lambda item: item["printed_number"])
        ],
    }


# ---------------------------------------------------------------- 语义校验


def _validate_structure(
    document: Mapping[str, Any], manifest: Mapping[str, Any]
) -> Mapping[str, Any]:
    """文档自身写错的那一层——失败即 `invalid`，与工作树现值无关。"""
    try:
        validate_schema(document, schema())
    except SchemaError as error:
        raise ProvenanceError(f"provenance Schema 不通过：{error}") from error

    paper_id = document["paper_id"]
    paper = _paper(manifest, paper_id)
    expected_batch = _batch_of(manifest, paper_id)
    if expected_batch is None:
        raise ProvenanceError(f"{paper_id} 不属于任何批次")
    if document["batch_id"] != expected_batch:
        raise ProvenanceError(
            "%s 的 batch_id 应为 %s，实际 %s"
            % (paper_id, expected_batch, document["batch_id"])
        )

    numbers = [item["printed_number"] for item in document["questions"]]
    if numbers != list(range(1, int(paper["question_count"]) + 1)):
        raise ProvenanceError(
            "%s 的题号必须是 1..%d 且升序无缺，实际 %s"
            % (paper_id, paper["question_count"], numbers)
        )

    registered = {item["path"] for item in paper.get("legacy_source_files", [])}
    for record in document["questions"]:
        number = record["printed_number"]
        if record["question_id"] != question_id(paper_id, number):
            raise ProvenanceError(
                "第 %d 题的 question_id 与印刷题号不符：%s"
                % (number, record["question_id"])
            )
        roles = [
            record["transcription_review"]["role"],
            record["solver_role"],
            record["reviewer_role"],
        ]
        if len(set(roles)) != 3:
            raise ProvenanceError(
                "第 %d 题的三个角色必须两两不同，实际 %s" % (number, roles)
            )
        reference = record["source_ref"]
        pages = record["source_pages"]
        if pages != sorted(set(pages)):
            raise ProvenanceError(f"第 {number} 题的 source_pages 必须去重升序")
        if "source_id" in reference:
            if reference["source_id"] not in set(paper.get("source_ids", [])):
                raise ProvenanceError(
                    "第 %d 题引用的 source 不属于本卷：%s"
                    % (number, reference["source_id"])
                )
            if not pages:
                raise ProvenanceError(f"第 {number} 题引用上游 source 却没有页码")
        else:
            if paper.get("source_ids"):
                raise ProvenanceError(
                    "%s 已有确认上游 source，第 %d 题不得改用本地 legacy 路径"
                    % (paper_id, number)
                )
            if reference["path"] not in registered:
                raise ProvenanceError(
                    "第 %d 题的本地路径不属于本卷登记的 legacy_source_files：%s"
                    % (number, reference["path"])
                )
            if pages:
                raise ProvenanceError(
                    f"第 {number} 题引用本地 Markdown，没有页码可言"
                )
    return paper


def _validate_current_values(
    document: Mapping[str, Any], manifest: Mapping[str, Any], root: Path
) -> None:
    """文档当时对、世界变了的那一层——失败即 `stale`。"""
    paper_id = document["paper_id"]
    paper = _paper(manifest, paper_id)
    sources = {item["source_id"]: item for item in manifest.get("sources", [])}
    texts = question_text_digests(_read_text(root, paper["source_files"]["questions"]))
    answers = answer_digests(
        paper_id, _read_text(root, paper["source_files"]["answer_key"])
    )
    registered = {
        item["path"]: item["sha256"]
        for item in paper.get("legacy_source_files", [])
    }

    for record in document["questions"]:
        number = record["printed_number"]
        reference = record["source_ref"]
        if "source_id" in reference:
            source = sources.get(reference["source_id"])
            if source is None:
                raise _StaleProvenance(
                    "第 %d 题引用的 source 已不在总账：%s"
                    % (number, reference["source_id"])
                )
            if source.get("source_state") != "ready":
                raise _StaleProvenance(
                    "第 %d 题引用的 source 不是 ready：%s"
                    % (number, source.get("source_state"))
                )
            artifact = source.get("artifact")
            if not isinstance(artifact, Mapping):
                raise _StaleProvenance(f"第 {number} 题引用的 source 没有 artifact")
            if (
                source.get("paper_id") != paper_id
                or source.get("paper_relation") is None
            ):
                raise _StaleProvenance(
                    f"第 {number} 题引用的 source 与本卷的双向关系已不成立"
                )
            page_count = int(artifact["page_count"])
            outside = [item for item in record["source_pages"] if item > page_count]
            if outside:
                raise _StaleProvenance(
                    "第 %d 题的页码越出 artifact 的 %d 页：%s"
                    % (number, page_count, outside)
                )
            if record["source_sha256"] != artifact["sha256"]:
                raise _StaleProvenance(f"第 {number} 题的来源哈希与 artifact 不符")
        else:
            relative = reference["path"]
            path = Path(root) / relative
            if not path.is_file():
                raise _StaleProvenance(f"第 {number} 题的本地来源缺失：{relative}")
            actual = file_sha256(path)
            if actual != record["source_sha256"] or actual != registered.get(relative):
                raise _StaleProvenance(
                    f"第 {number} 题的本地来源哈希已变化：{relative}"
                )
        if texts.get(number) != record["question_text_sha256"]:
            raise _StaleProvenance(f"第 {number} 题的题面哈希已变化")
        if answers.get(number) != record["answer_sha256"]:
            raise _StaleProvenance(f"第 {number} 题的答案哈希已变化")


def validate_provenance(
    document: Mapping[str, Any],
    manifest: Mapping[str, Any],
    root: Path,
    recompute: bool = True,
) -> None:
    """校验一份 provenance；`recompute=False` 只查文档自身那一层。"""
    _validate_structure(document, manifest)
    if recompute:
        _validate_current_values(document, manifest, root)


# ---------------------------------------------------------------- facts 探针


def default_artifacts_state(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    figure_map: Optional[Mapping[str, str]] = None,
    index_metadata: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> str:
    """生成物当前性：**现场重算三个生成器的全部目标再逐字节比对**。

    不取巧读文件时间戳、也不信任任何自述——「生成物当前」是 `complete` 证据链上的一环，
    唯一站得住的算法就是把它重新算一遍。任何一步算不出来都返回 `stale`（fail closed），
    而不是把算不出来当成没变。

    这些都是三个生成器的**纯函数**入口，不经 `run()`，因此不会二次获取 `RepoLock`
    ——本函数会在 `run_formal()` 已持锁的情况下被调用。
    """
    root = Path(root)
    paper = _paper(manifest, paper_id)
    metadata = (
        generate_projects.INDEX_METADATA if index_metadata is None else index_metadata
    )
    targets: Dict[str, bytes] = {}
    try:
        result = generate_projects.generate_project(
            root, generate_projects.paper_sources(paper), figure_map=figure_map
        )
        targets.update(result.targets)
        targets[INDEX_TARGET] = generate_projects.project_index_bytes(
            manifest, index_metadata
        )
        targets.update(make_editions.build_shells(
            make_editions.load_templates(root), make_editions.paper_shell(paper)
        ))
        short, problems = make_short_answers.generate_short_answers(
            root, make_short_answers.paper_sources(paper, metadata)
        )
        if problems:
            return "stale"
        targets.update(short.targets)
    except (ValueError, OSError, KeyError):
        return "stale"

    if any(not (root / relative).is_file() for relative in targets):
        return "missing"
    for relative, value in targets.items():
        if (root / relative).read_bytes() != value:
            return "stale"
    return "current"


def default_review_state(
    root: Path, manifest: Mapping[str, Any], paper_id: str
) -> Tuple[str, str]:
    """review 回执的状态与当前性。

    读不出、状态不在冻结取值域内，一律折成 `missing`——「没有可用裁决」比「有一份读不懂
    的裁决」更接近事实，而 REVIEW_STATES 里没有 `invalid` 这一档。当前性要求 review 与
    **当前那次 build** 逐项绑定（attempt 与四条证据），否则 stale。
    """
    root = Path(root)
    paper = _paper(manifest, paper_id)
    path = root / review_receipt_path(paper)
    if not path.is_file():
        return "missing", "stale"
    try:
        review = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return "missing", "stale"
    if not isinstance(review, Mapping) or review.get("status") not in REVIEW_STATES:
        return "missing", "stale"
    state = review["status"]

    receipt_path = root / build_receipt_path(paper)
    if not receipt_path.is_file():
        return state, "stale"
    try:
        receipt = build_projects.load_receipt(receipt_path)
    except build_projects.BuildError:
        return state, "stale"
    bound = (
        review.get("paper_id") == paper_id
        and review.get("build_attempt_id") == receipt["attempt_id"]
        and review.get("input_projection") == receipt["input_projection"]
        and review.get("generation_input_tree_sha256")
        == receipt["generation_input_tree"]["tree_sha256"]
        and review.get("dependency_tree_sha256")
        == receipt["dependency_tree"]["tree_sha256"]
        and review.get("toolchain_fingerprint") == receipt["toolchain_fingerprint"]
    )
    return state, "current" if bound else "stale"


def default_batch_report_valid(
    root: Path, manifest: Mapping[str, Any], paper_id: str
) -> bool:
    """报告有没有效，唯一属主是 `review_receipts.check_batch()` 的 finalize 门禁。

    对已落盘的批次报告做只读转发，逐字段核对当前事实。报告缺失、对不上、或门禁非
    FINALIZED 都返回 False——绝不自作主张「报告存在即有效」，那会拿没验证过的报告给
    状态背书（status.py 顶部那条 report 门禁正是为此存在）。
    """
    import review_receipts  # 运行时才加载：与 review_receipts 侧的 import 环保持一致

    batch_id = _batch_of(manifest, paper_id)
    if batch_id is None:
        return False
    if not (Path(root) / review_receipts.report_target(batch_id)).is_file():
        return False

    def _facts_without_report(
        root_: Path, manifest_: Mapping[str, Any], paper_ids_: Sequence[str]
    ) -> Mapping[str, Mapping[str, Any]]:
        # 恒 False 的探针切断递归：check_batch 内部会再走 load_provenance_facts，
        # 沿用默认探针就会回到本函数。「报告有效」由 check_batch 自己在终裁阶段以
        # batch_report_valid=True 对账，这里只转发它的结论，不需要再算一遍。
        return load_provenance_facts(
            root_, manifest_, paper_ids_,
            issues_path=Path(root_) / ISSUES_TARGET,
            batch_report_valid=lambda *_args: False,
        )

    try:
        result = review_receipts.check_batch(
            Path(root) / MANIFEST_TARGET,
            Path(root) / ISSUES_TARGET,
            batch_id,
            facts_loader=_facts_without_report,
        )
    except (ValueError, OSError):
        # 门禁本身算不出来（清单损坏、路径不规范）就是「没验证过」，与非 FINALIZED 同解。
        # 不向上抛：状态随即降级，漂移会被 check_batch 当场报成 INVALID，既闭且响。
        return False
    return result["code"] == "FINALIZED"


# ---------------------------------------------------------------- facts adapter


def _provenance_observation(
    root: Path,
    manifest: Mapping[str, Any],
    paper: Mapping[str, Any],
    document: Optional[Mapping[str, Any]],
) -> Tuple[str, bool, bool]:
    """返回 (provenance 状态, 是否有未知, 是否有未解决冲突)。"""
    if document is None:
        path = Path(root) / provenance_path(paper)
        if not path.is_file():
            return "missing", False, False
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return "invalid", False, False
        if not isinstance(document, Mapping):
            return "invalid", False, False

    try:
        _validate_structure(document, manifest)
    except ProvenanceError:
        return "invalid", False, False

    unknown = any(
        item["transcription_review"]["result"] != "passed"
        or item["answer_evidence"]["grade"] == "U"
        for item in document["questions"]
    )
    conflicts = any(
        item["conflict_status"] == "unresolved" for item in document["questions"]
    )
    try:
        _validate_current_values(document, manifest, root)
    except ProvenanceError:
        return "stale", unknown, conflicts
    return "current", unknown, conflicts


def load_provenance_facts(
    root: Path,
    manifest: Mapping[str, Any],
    paper_ids: Sequence[str],
    issues_path: Optional[Path] = None,
    artifacts_state: Optional[Callable[..., str]] = None,
    review_state: Optional[Callable[..., Tuple[str, str]]] = None,
    batch_report_valid: Optional[Callable[..., bool]] = None,
    provenance_documents: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> Dict[str, Dict[str, Any]]:
    """真实 provenance facts adapter：显式消费 manifest、问题总账与当前生成物。

    **不搜索自然语言**，也不返回 build/build_currency——那两维只有构建回执说得算
    （`build_projects.merge_facts()` 会当场拒绝越权字段）。

    `provenance_documents` 是导入事务专用的内存覆盖：文档尚未落盘时也要能算出
    reconciler 需要的 facts，而绝不能为此先把文件写出去再读回来。
    """
    root = Path(root)
    artifacts_probe = artifacts_state or default_artifacts_state
    review_probe = review_state or default_review_state
    report_probe = batch_report_valid or default_batch_report_valid
    ledger = issues_module.load_issues(
        Path(issues_path) if issues_path is not None else root / ISSUES_TARGET
    )

    facts: Dict[str, Dict[str, Any]] = {}
    for paper_id in paper_ids:
        paper = _paper(manifest, paper_id)
        state, unknown, conflicts = _provenance_observation(
            root, manifest, paper, (provenance_documents or {}).get(paper_id)
        )
        review, review_currency = review_probe(root, manifest, paper_id)
        facts[paper_id] = {
            "provenance": state,
            "provenance_unknown": unknown,
            "provenance_conflicts": conflicts,
            "artifacts": artifacts_probe(root, manifest, paper_id),
            "review": review,
            "review_currency": review_currency,
            "issues": tuple(
                item for item in ledger
                if item.get("paper_id") == paper_id
                or paper_id in set(item.get("affected_paper_ids") or [])
            ),
            "batch_report_valid": bool(report_probe(root, manifest, paper_id)),
        }
    return facts


def facts_loader(**options: Any) -> Callable[..., Mapping[str, Mapping[str, Any]]]:
    """把探针注入折成 `run_formal(facts_loader=…)` 要的三参数可调用体。"""
    def loader(
        root: Path, manifest: Mapping[str, Any], paper_ids: Sequence[str]
    ) -> Mapping[str, Mapping[str, Any]]:
        return load_provenance_facts(root, manifest, paper_ids, **options)
    return loader


# ---------------------------------------------------------------- .work 布局


def _validated_work_dir(root: Path, work_dir: Path) -> Path:
    """work-dir 必须落在 ignored 的 `.work` 内。

    这是**唯一**能保证「角色草稿不会被误当成正式证据提交」的机械约束：`.work/` 已被
    `.gitignore` 覆盖，写到别处就等于把未核验的中间态放进了 tracked 树。
    """
    resolved = Path(work_dir).resolve()
    allowed = (Path(root) / WORK_RELATIVE).resolve()
    if resolved != allowed and allowed not in resolved.parents:
        raise ProvenanceError(f"--work-dir 必须落在 {WORK_RELATIVE} 之内：{work_dir}")
    return resolved


def work_paths(work_dir: Path, batch_id: str, paper_id: str) -> Dict[str, Path]:
    """三角色的三条独占路径；同一角色永远只写自己那一条。"""
    base = Path(work_dir) / batch_id / "provenance"
    return {stage: base / stage / ("%s.json" % paper_id) for stage in STAGES}


def _skeleton(stage: str, batch_id: str, paper_id: str, count: int) -> Dict[str, Any]:
    records: List[Dict[str, Any]] = []
    for number in range(1, count + 1):
        record: Dict[str, Any] = {
            "question_id": question_id(paper_id, number),
            "printed_number": number,
            "issue_ids": [],
        }
        if stage == "question-review":
            record.update({
                "source_ref": None, "source_sha256": None, "source_pages": [],
                "question_text_sha256": None, "result": None, "evidence": None,
            })
        elif stage == "answer-solve":
            record.update({
                "answer_sha256": None, "grade": None, "evidence": None,
            })
        else:
            # 盲核：骨架里**没有**求解角色的任何答案，连哈希都不预填。
            record.update({"answer_sha256": None, "conflict_status": None})
        records.append(record)
    return {
        "stage": stage,
        "role": None,
        "batch_id": batch_id,
        "paper_id": paper_id,
        "questions": records,
    }


def init_batch(
    manifest_path: Path, batch_id: str, work_dir: Path
) -> Dict[str, Any]:
    """为批次内每套试卷创建三条独占的角色路径；只写 ignored `.work`。"""
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    resolved = _validated_work_dir(root, work_dir)
    manifest = load_manifest(manifest_path)
    batch = _batch(manifest, batch_id)

    planned: List[Tuple[Path, Dict[str, Any]]] = []
    for paper_id in batch["paper_ids"]:
        paper = _paper(manifest, paper_id)
        paths = work_paths(resolved, batch_id, paper_id)
        for stage in STAGES:
            if paths[stage].exists():
                raise ProvenanceError(
                    "角色文件已存在，拒绝覆盖：%s" % _relative_to(root, paths[stage])
                )
            planned.append((
                paths[stage],
                _skeleton(stage, batch_id, paper_id, int(paper["question_count"])),
            ))

    created: List[str] = []
    for path, document in planned:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical_json(document).encode("utf-8"))
        created.append(_relative_to(root, path))
    return {"code": "OK", "batch_id": batch_id, "created": sorted(created)}


# ---------------------------------------------------------------- 导入


def _load_work_document(path: Path, stage: str, batch_id: str, paper_id: str) -> Mapping[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProvenanceError(f"无法读取角色文件 {path.name}（{stage}）：{error}") from error
    if not isinstance(document, Mapping):
        raise ProvenanceError(f"角色文件顶层必须是对象：{stage}/{paper_id}")
    for field, expected in (
        ("stage", stage), ("batch_id", batch_id), ("paper_id", paper_id)
    ):
        if document.get(field) != expected:
            raise ProvenanceError(
                "%s/%s 的 %s 应为 %s，实际 %r"
                % (stage, paper_id, field, expected, document.get(field))
            )
    role = document.get("role")
    if not isinstance(role, str) or not role.strip():
        raise ProvenanceError(f"{stage}/{paper_id} 缺少角色身份")
    records = document.get("questions")
    if not isinstance(records, list) or not records:
        raise ProvenanceError(f"{stage}/{paper_id} 没有题目记录")
    return document


def _read_work(work_dir: Path, batch_id: str, paper_ids: Sequence[str]) -> Dict[str, Dict[str, Mapping[str, Any]]]:
    """三组 paper 集合必须**恰好等于**批次；多一个少一个都整批中止。"""
    expected = set(paper_ids)
    for stage in STAGES:
        directory = Path(work_dir) / batch_id / "provenance" / stage
        if not directory.is_dir():
            raise ProvenanceError(f"缺少角色目录：{stage}")
        found = {item.stem for item in sorted(directory.glob("*.json"))}
        if found != expected:
            raise ProvenanceError(
                "%s 的试卷集合与批次不符：多 %s，缺 %s"
                % (stage, sorted(found - expected), sorted(expected - found))
            )
    return {
        paper_id: {
            stage: _load_work_document(
                work_paths(work_dir, batch_id, paper_id)[stage],
                stage, batch_id, paper_id,
            )
            for stage in STAGES
        }
        for paper_id in paper_ids
    }


def _by_number(document: Mapping[str, Any], stage: str, paper_id: str) -> Dict[int, Mapping[str, Any]]:
    records: Dict[int, Mapping[str, Any]] = {}
    for item in document["questions"]:
        number = item.get("printed_number")
        if not isinstance(number, int) or isinstance(number, bool):
            raise ProvenanceError(f"{stage}/{paper_id} 的 printed_number 必须是整数")
        if number in records:
            raise ProvenanceError(f"{stage}/{paper_id} 的第 {number} 题记录重复")
        records[number] = item
    return records


def _require_linked_blocker(
    ledger: Sequence[Mapping[str, Any]],
    paper_id: str,
    record: Mapping[str, Any],
    kind: str,
    detail: str,
) -> None:
    """未知 / U 级 / 未解决冲突都必须挂上一条**当前且仍在阻断**的同身份问题。

    「同身份」是重点：fingerprint 由 (type, paper_id, question_id, source_id) 唯一确定，
    随便挂一条别的问题顶数是过不了的；已 resolved 或 non_blocking 的也不算——那等于用
    一条已经结案的问题给一个仍然未知的答案背书。
    """
    expected = issues_module.question_issue_fingerprint(
        paper_id, record["question_id"], source_identity(record["source_ref"]), kind
    )
    declared = set(record["issue_ids"])
    for item in ledger:
        if (
            item["fingerprint"] == expected
            and item["issue_id"] in declared
            and item["impact"] == "blocks_completion"
            and item["status"] != "resolved"
        ):
            return
    raise ProvenanceError(
        "%s 第 %d 题%s，必须关联一条 fingerprint 当前、仍在阻断的 %s 问题"
        % (paper_id, record["printed_number"], detail,
           issues_module.QUESTION_ISSUE_TYPES[kind])
    )


def _build_document(
    root: Path,
    manifest: Mapping[str, Any],
    batch_id: str,
    paper_id: str,
    work: Mapping[str, Mapping[str, Any]],
    ledger: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    paper = _paper(manifest, paper_id)
    roles = {stage: work[stage]["role"] for stage in STAGES}
    if len(set(roles.values())) != len(STAGES):
        raise ProvenanceError(f"{paper_id} 的三个角色身份必须两两不同：{roles}")

    numbers: Optional[List[int]] = None
    tables: Dict[str, Dict[int, Mapping[str, Any]]] = {}
    for stage in STAGES:
        tables[stage] = _by_number(work[stage], stage, paper_id)
        ordered = sorted(tables[stage])
        if numbers is None:
            numbers = ordered
        elif ordered != numbers:
            raise ProvenanceError(f"{paper_id} 三个角色的题号集合不一致")
    assert numbers is not None

    # work 文件里的哈希只是**待比较声明**：真值一律从当前 tracked 规范源现场重算。
    texts = question_text_digests(_read_text(root, paper["source_files"]["questions"]))
    answers = answer_digests(
        paper_id, _read_text(root, paper["source_files"]["answer_key"])
    )

    records: List[Dict[str, Any]] = []
    for number in numbers:
        review = tables["question-review"][number]
        solve = tables["answer-solve"][number]
        blind = tables["answer-review"][number]
        reference = review.get("source_ref")
        if not isinstance(reference, Mapping):
            raise ProvenanceError(f"{paper_id} 第 {number} 题缺少 source_ref")
        record = {
            "question_id": question_id(paper_id, number),
            "printed_number": number,
            "source_ref": copy.deepcopy(dict(reference)),
            "source_sha256": review.get("source_sha256"),
            "source_pages": list(review.get("source_pages") or []),
            "question_text_sha256": texts.get(number),
            "answer_sha256": answers.get(number),
            "transcription_review": {
                "role": roles["question-review"],
                "result": review.get("result"),
                "evidence": review.get("evidence"),
            },
            "answer_evidence": {
                "grade": solve.get("grade"), "evidence": solve.get("evidence"),
            },
            "solver_role": roles["answer-solve"],
            "reviewer_role": roles["answer-review"],
            "conflict_status": blind.get("conflict_status"),
            "issue_ids": sorted(set(
                list(review.get("issue_ids") or [])
                + list(solve.get("issue_ids") or [])
                + list(blind.get("issue_ids") or [])
            )),
        }
        for stage, declared in (
            ("question-review", review.get("question_text_sha256")),
            ("answer-solve", solve.get("answer_sha256")),
            ("answer-review", blind.get("answer_sha256")),
        ):
            expected = (
                record["question_text_sha256"] if stage == "question-review"
                else record["answer_sha256"]
            )
            if declared != expected:
                raise ProvenanceError(
                    "%s 第 %d 题：%s 声明的哈希与现场重算不符"
                    % (paper_id, number, stage)
                )
        records.append(record)

    document = new_provenance(paper_id, batch_id, records)
    validate_provenance(document, manifest, root)

    for record in document["questions"]:
        if record["transcription_review"]["result"] != "passed":
            _require_linked_blocker(
                ledger, paper_id, record, "transcription", "的题面核对未通过"
            )
        if record["answer_evidence"]["grade"] == "U":
            _require_linked_blocker(
                ledger, paper_id, record, "answer", "的答案证据是 U 级"
            )
        if record["conflict_status"] == "unresolved":
            _require_linked_blocker(
                ledger, paper_id, record, "conflict", "的盲核冲突未解决"
            )
    return document


def _toolchain(
    root: Path,
    manifest: Mapping[str, Any],
    paper_ids: Sequence[str],
    search_path: Optional[str] = None,
) -> Mapping[str, Any]:
    """只在确实存在 build 回执时才去解析工具链；解析不出来就用哨兵（fail closed）。"""
    if not any(
        (Path(root) / build_receipt_path(_paper(manifest, paper_id))).is_file()
        for paper_id in paper_ids
    ):
        return UNRESOLVED_TOOLCHAIN
    try:
        return build_projects.resolve_toolchain(search_path=search_path)
    except build_projects.BuildError:
        return UNRESOLVED_TOOLCHAIN


def _facts_for(
    root: Path,
    manifest: Mapping[str, Any],
    paper_ids: Sequence[str],
    issues_path: Path,
    ledger: Sequence[Mapping[str, Any]],
    documents: Optional[Mapping[str, Mapping[str, Any]]] = None,
    probes: Optional[Mapping[str, Any]] = None,
    search_path: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """装配完整 facts：本模块出 provenance 侧，build 侧仍由 build_projects 出。"""
    loaded = load_provenance_facts(
        root, manifest, paper_ids, issues_path=issues_path,
        provenance_documents=documents, **(probes or {})
    )
    chain = _toolchain(root, manifest, paper_ids, search_path=search_path)
    return build_projects.assemble_facts(
        root, manifest, paper_ids, loaded, {}, issue_records=ledger, toolchain=chain
    )


def import_batch(
    manifest_path: Path,
    issues_path: Path,
    batch_id: str,
    work_dir: Path,
    write: bool = False,
    search_path: Optional[str] = None,
    **probes: Any
) -> Dict[str, Any]:
    """把一个批次的三角色 `.work` 折成正式 provenance，并在**一个** state 事务里提交。

    事务目标：各卷 provenance、问题总账（字节不变也参与 CAS，防的是另一个会话同时改它）、
    最后是 manifest 并递增 revision。失败或崩溃由 journal 恢复，绝不留半提交。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    issues_path = _require_canonical(
        root, Path(issues_path), ISSUES_TARGET, "--issues"
    )
    resolved_work = _validated_work_dir(root, work_dir)

    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        batch = _batch(manifest, batch_id)
        paper_ids = list(batch["paper_ids"])
        ledger = issues_module.load_issues(issues_path)
        work = _read_work(resolved_work, batch_id, paper_ids)

        documents = {
            paper_id: _build_document(
                root, manifest, batch_id, paper_id, work[paper_id], ledger
            )
            for paper_id in paper_ids
        }
        report = {
            "code": "OK", "batch_id": batch_id, "papers": list(paper_ids),
            "written": False,
        }
        if not write:
            return report

        facts = _facts_for(
            root, manifest, paper_ids, issues_path, ledger,
            documents=documents, probes=probes, search_path=search_path,
        )
        targets = {
            provenance_path(_paper(manifest, paper_id)):
                canonical_json(documents[paper_id]).encode("utf-8")
            for paper_id in paper_ids
        }
        issue_ids = issues_module.issue_ids_by_paper(ledger)
        updated = build_projects.commit_state(
            root, manifest, targets, {ISSUES_TARGET: issues_path.read_bytes()},
            lambda transaction_id: build_projects.reconciled_manifest(
                manifest, transaction_id, facts, [batch], issue_ids
            ),
        )
        report["written"] = True
        report["revision"] = updated["revision"]
        report["batch_status"] = next(
            item["status"] for item in updated["batches"]
            if item["batch_id"] == batch_id
        )
        return report


# ---------------------------------------------------------------- 来源绑定


def _identity_blockers(
    ledger: Sequence[Mapping[str, Any]], paper_id: str
) -> List[str]:
    """覆盖本卷、尚未了结的 `identity-ambiguous` 问题编号。

    这条守卫把「2026 全国 1 回忆版不得自动绑定上游正式卷」从纪律变成机器强制，也顺带
    强制 2017 两卷必须先解决身份问题再绑定。判据只看 **status 未 resolved**、不看
    `impact`——身份不明本身就让「这条 source 属于这一卷」这个断言无从谈起，哪怕问题被
    标成 non_blocking 也一样。

    ⚠️ 判据写成**取反**（`!= "resolved"`）而非枚举白名单：白名单与 docstring 今天等价，
    但方向相反——`issues.STATUSES` 将来加任何新状态（wontfix / superseded…），白名单
    会让这条一票否决的守卫默认放行。默认必须是拒绝。
    """
    return sorted(
        item["issue_id"] for item in ledger
        if item.get("type") == "identity-ambiguous"
        and item.get("status") != "resolved"
        and (
            item.get("paper_id") == paper_id
            or paper_id in set(item.get("affected_paper_ids") or [])
        )
    )


def _bound_manifest(
    manifest: Mapping[str, Any], paper_id: str, source_id: str
) -> Dict[str, Any]:
    """返回写入了双向绑定的新 manifest（不动 revision，也不动任何状态字段）。

    绑定不是状态推进：`production_state` 与 batch `status` 一律不碰——它们由
    `status.py` 从 facts 现场派生，这里顺手改一格就等于绕过整条证据链。
    """
    document = copy.deepcopy(dict(manifest))
    for source in document["sources"]:
        if source["source_id"] == source_id:
            source["paper_id"] = paper_id
            source["paper_relation"] = PAPER_RELATION
    for paper in document["papers"]:
        if paper["paper_id"] == paper_id:
            paper["source_ids"] = sorted(set(paper["source_ids"]) | {source_id})
    return document


def confirm_source(
    manifest_path: Path,
    issues_path: Path,
    paper_id: str,
    source_id: str,
    write: bool = False,
    event_hook: Any = None,
) -> Dict[str, Any]:
    """确认一条上游 source 属于某一卷，双向写入 manifest。

    这是 `import-batch` 的前置：T4 的迁移**刻意不建立任何绑定**，于是各卷的
    `source_ids` 与 `legacy_source_files` 都是空的，`source_ref` 的两条通道都还不通。
    绑定属批次导入期的产出，故五道守卫全部前置——**没有 unbind 子命令**，绑错一次只能
    走升级流程。

    `paper_relation` 固定 `canonical`：阶段 0 不产生其它关系，做成参数只会给「随手标成
    duplicate」留口子。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    issues_path = _require_canonical(
        root, Path(issues_path), ISSUES_TARGET, "--issues"
    )

    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        _paper(manifest, paper_id)                               # ③ paper 必须存在
        sources = {item["source_id"]: item for item in manifest.get("sources", [])}
        source = sources.get(source_id)
        if source is None:                                       # ① 必须存在
            raise ProvenanceError(f"未知 source_id：{source_id}")
        if source.get("source_state") != "ready":                # ① 必须 ready
            raise ProvenanceError(
                "%s 的 source_state 是 %r，只有 ready 的来源可以确认绑定"
                % (source_id, source.get("source_state"))
            )
        # ② 必须未绑定。已绑到本卷同样报错：静默幂等会把「绑错了」伪装成「本来就这样」，
        # 而这条命令没有反向操作可以救。半绑定（只有一侧非空）更要拦——那是上一次崩在
        # 半路的痕迹，须人工判明后再动。
        if (
            source.get("paper_id") is not None
            or source.get("paper_relation") is not None
        ):
            raise ProvenanceError(
                "%s 已绑定（paper_id=%r，paper_relation=%r），拒绝重复绑定；"
                "确需改绑请走升级流程"
                % (source_id, source.get("paper_id"), source.get("paper_relation"))
            )
        blockers = _identity_blockers(                           # ④ 身份问题一票否决
            issues_module.load_issues(issues_path), paper_id
        )
        if blockers:
            raise ProvenanceError(
                "%s 仍被未了结的身份问题覆盖（%s），拒绝绑定上游 source"
                % (paper_id, "、".join(blockers))
            )

        document = _bound_manifest(manifest, paper_id, source_id)
        try:                                                     # ⑤ 绑定后必须自洽
            source_manifest.validate_source_state(
                next(
                    item for item in document["sources"]
                    if item["source_id"] == source_id
                ),
                {item["paper_id"] for item in document["papers"]},
            )
            source_manifest.validate_manifest_document(manifest_path, document)
        except (ValueError, SchemaError) as error:
            raise ProvenanceError(f"绑定后的 manifest 校验不通过：{error}") from error

        bound_paper = next(
            item for item in document["papers"] if item["paper_id"] == paper_id
        )
        report: Dict[str, Any] = {
            "code": "OK",
            "paper_id": paper_id,
            "source_id": source_id,
            "paper_relation": PAPER_RELATION,
            "source_ids": list(bound_paper["source_ids"]),
            "upstream_path": source.get("upstream_path"),
            "written": False,
            "revision": int(manifest["revision"]),
        }
        if not write:
            return report

        # 单文件也走 `state` 事务：这是业务状态变更，不是确定性派生物重建。CAS 钉住
        # expected_revision，manifest 作为唯一目标最后提交并递增 revision。
        transaction = Transaction(root, event_hook=event_hook)
        document["revision"] = int(manifest["revision"]) + 1
        document["last_transaction_id"] = transaction.transaction_id
        transaction.prepare(
            "state", {MANIFEST_TARGET: canonical_json(document).encode("utf-8")},
            {}, expected_revision=int(manifest["revision"]),
        )
        transaction.commit()
        report["written"] = True
        report["revision"] = document["revision"]
        return report


# ---------------------------------------------------------------- 只读核对


def check_batch(
    manifest_path: Path,
    issues_path: Path,
    batch_id: Optional[str] = None,
    search_path: Optional[str] = None,
    **probes: Any
) -> Dict[str, Any]:
    """现场重算并拒绝任何缓存漂移；一个字节都不写。

    两件事同时核：provenance 本身能否重新验算通过，以及 manifest 里缓存的
    `production_state` / batch `status` 是否与**现场派生**逐字相等。缓存对不上时报错
    而不是顺手改写——只读命令改状态就是把「核对」变成了「刷新」。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    issues_path = _require_canonical(
        root, Path(issues_path), ISSUES_TARGET, "--issues"
    )
    manifest = load_manifest(manifest_path)
    batches = (
        [_batch(manifest, batch_id)] if batch_id is not None
        else list(manifest.get("batches", []))
    )
    ledger = issues_module.load_issues(issues_path)

    problems: List[str] = []
    counted = 0
    for batch in batches:
        paper_ids = list(batch["paper_ids"])
        counted += len(paper_ids)
        facts = _facts_for(
            root, manifest, paper_ids, issues_path, ledger,
            probes=probes, search_path=search_path,
        )
        for paper_id in paper_ids:
            paper = _paper(manifest, paper_id)
            path = Path(root) / provenance_path(paper)
            if path.is_file():
                try:
                    validate_provenance(
                        json.loads(path.read_text(encoding="utf-8")), manifest, root
                    )
                except (ProvenanceError, OSError, UnicodeError,
                        json.JSONDecodeError) as error:
                    problems.append("%s: provenance 不通过重算：%s" % (paper_id, error))
            derived = derive_status(facts[paper_id])
            if paper["production_state"] != derived:
                problems.append(
                    "%s: 缓存状态 %s 与现场派生 %s 不符"
                    % (paper_id, paper["production_state"], derived)
                )
        derived_batch = reconcile_batch_status(
            {paper_id: facts[paper_id] for paper_id in paper_ids}
        )
        if batch["status"] != derived_batch:
            problems.append(
                "%s: 缓存批次状态 %s 与现场派生 %s 不符"
                % (batch["batch_id"], batch["status"], derived_batch)
            )
    return {
        "code": "INVALID" if problems else "OK",
        "papers": counted,
        "batches": [item["batch_id"] for item in batches],
        "problems": problems,
    }


def paper_status(
    manifest_path: Path,
    issues_path: Path,
    batch_id: Optional[str] = None,
    require_git_state: Optional[str] = None,
    search_path: Optional[str] = None,
    **probes: Any
) -> Dict[str, Any]:
    """只读汇报：逐卷现场派生状态、批次状态，以及可选的 git 持久化要求。"""
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    issues_path = _require_canonical(
        root, Path(issues_path), ISSUES_TARGET, "--issues"
    )
    manifest = load_manifest(manifest_path)
    batches = (
        [_batch(manifest, batch_id)] if batch_id is not None
        else list(manifest.get("batches", []))
    )
    ledger = issues_module.load_issues(issues_path)

    papers: Dict[str, str] = {}
    batch_states: Dict[str, str] = {}
    selected: List[str] = []
    for batch in batches:
        paper_ids = list(batch["paper_ids"])
        selected.extend(paper_ids)
        facts = _facts_for(
            root, manifest, paper_ids, issues_path, ledger,
            probes=probes, search_path=search_path,
        )
        for paper_id in paper_ids:
            papers[paper_id] = derive_status(facts[paper_id])
        batch_states[batch["batch_id"]] = reconcile_batch_status(
            {paper_id: facts[paper_id] for paper_id in paper_ids}
        )

    problems: List[str] = []
    git_state = None
    if require_git_state is not None:
        scope = list(paper_provenance_paths(manifest, selected))
        scope += [MANIFEST_TARGET, ISSUES_TARGET]
        try:
            git_state = derive_git_state(root, scope)
        except StatusError as error:
            problems.append(f"git 状态不可派生：{error}")
        else:
            if git_state != require_git_state:
                problems.append(
                    "git 持久化状态是 %s，要求 %s" % (git_state, require_git_state)
                )
    return {
        "code": "INVALID" if problems else "OK",
        "papers": papers,
        "batches": batch_states,
        "git_state": git_state,
        "problems": problems,
    }


# ---------------------------------------------------------------- CLI


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="逐题来源核验与完成状态验证")
    subparsers = parser.add_subparsers(dest="command", required=True)

    initialize = subparsers.add_parser("init-batch")
    initialize.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    initialize.add_argument("--batch", required=True)
    initialize.add_argument("--work-dir", required=True)

    confirm = subparsers.add_parser("confirm-source")
    confirm.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    confirm.add_argument("--issues", required=True)
    confirm.add_argument("--paper", required=True)
    confirm.add_argument("--source", required=True)
    confirm.add_argument("--write", action="store_true")

    imports = subparsers.add_parser("import-batch")
    imports.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    imports.add_argument("--issues", default=str(DEFAULT_ISSUES))
    imports.add_argument("--batch", required=True)
    imports.add_argument("--work-dir", required=True)
    # `--write` 只此一处：其余命令一律只读，连「顺手刷新缓存」的入口都不留。
    imports.add_argument("--write", action="store_true")

    check = subparsers.add_parser("check-batch")
    check.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    check.add_argument("--issues", default=str(DEFAULT_ISSUES))
    check.add_argument("--batch", required=True)

    check_all = subparsers.add_parser("check-all")
    check_all.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    check_all.add_argument("--issues", default=str(DEFAULT_ISSUES))

    state = subparsers.add_parser("status")
    state.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    state.add_argument("--issues", default=str(DEFAULT_ISSUES))
    state.add_argument("--batch")
    state.add_argument("--require-git-state", choices=list(status_core.GIT_STATES))
    return parser


def main(argv: Optional[Sequence[str]] = None, **probes: Any) -> int:
    """退出码契约：0 通过、2 命令行用法错（argparse）、4 数据无效或核对未过。"""
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "init-batch":
            report = init_batch(
                Path(arguments.manifest), arguments.batch, Path(arguments.work_dir)
            )
            print("✓ %s：已创建 %d 条角色路径" % (
                report["batch_id"], len(report["created"])
            ))
            return EXIT_OK

        if arguments.command == "confirm-source":
            report = confirm_source(
                Path(arguments.manifest), Path(arguments.issues),
                arguments.paper, arguments.source, write=arguments.write,
            )
            print("✓ %s ← %s（%s）%s" % (
                report["paper_id"], report["source_id"], report["paper_relation"],
                "已提交 revision %s" % report["revision"] if report["written"]
                else "仅校验，未落盘",
            ))
            return EXIT_OK

        if arguments.command == "import-batch":
            report = import_batch(
                Path(arguments.manifest), Path(arguments.issues), arguments.batch,
                Path(arguments.work_dir), write=arguments.write, **probes
            )
            print("✓ %s：%d 卷，%s" % (
                report["batch_id"], len(report["papers"]),
                "已提交 revision %s" % report["revision"] if report["written"]
                else "仅校验，未落盘",
            ))
            return EXIT_OK

        if arguments.command in {"check-batch", "check-all"}:
            report = check_batch(
                Path(arguments.manifest), Path(arguments.issues),
                getattr(arguments, "batch", None), **probes
            )
            for problem in report["problems"]:
                print("  ✗ %s" % problem, file=sys.stderr)
            print("%s：%d 卷" % (report["code"], report["papers"]))
            return EXIT_OK if report["code"] == "OK" else EXIT_INVALID

        report = paper_status(
            Path(arguments.manifest), Path(arguments.issues), arguments.batch,
            require_git_state=arguments.require_git_state, **probes
        )
        for paper_id in sorted(report["papers"]):
            print("%s %s" % (report["papers"][paper_id], paper_id))
        for batch_id in sorted(report["batches"]):
            print("%s %s" % (report["batches"][batch_id], batch_id))
        for problem in report["problems"]:
            print("  ✗ %s" % problem, file=sys.stderr)
        return EXIT_OK if report["code"] == "OK" else EXIT_INVALID
    except (ProvenanceError, StatusError, OSError, RuntimeError) as error:
        print("error: %s" % error, file=sys.stderr)
        return EXIT_INVALID


if __name__ == "__main__":
    sys.exit(main())

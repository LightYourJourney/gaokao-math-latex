from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from manifest import atomic_write_bytes

ISSUE_TYPES = {
    "source-unavailable",
    "source-unreadable",
    "identity-ambiguous",
    "transcription-ambiguous",
    "figure-missing",
    "answer-missing",
    "answer-conflict",
    "compile-error",
    "layout-warning",
    "source-mismatch",
}
STATUSES = {"open", "investigating", "resolved", "deferred"}
IMPACTS = {"blocks_completion", "non_blocking"}
REQUIRED_FIELDS = {
    "fingerprint",
    "paper_id",
    "affected_paper_ids",
    "type",
    "status",
    "impact",
    "resume_action",
}
_SOURCE_TYPES = {"source-unavailable", "source-unreadable", "source-mismatch"}
_QUESTION_TYPES = {"transcription-ambiguous", "answer-missing", "answer-conflict"}
_VISUAL_TYPES = {"figure-missing", "compile-error", "layout-warning"}
_ISSUE_HEADING = re.compile(r"(?m)^## (ISSUE-[^ \t\r\n]+)[ \t]*$")
_ANY_ISSUE_HEADING = re.compile(r"(?m)^##[ \t]+ISSUE[^\r\n]*$")
_ISSUE_ID = re.compile(r"^ISSUE-([0-9]{4,})$")


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _nonempty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"问题字段 {field} 必须是非空字符串")
    return value.strip()


def _normalized_warning(value: Any) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError("视觉 warning 必须是对象")
    source_file = _nonempty_string(value.get("source_file"), "warning.source_file")
    raw_line = value.get("line")
    try:
        line = int(raw_line)
    except (TypeError, ValueError) as error:
        raise ValueError("warning.line 必须是正整数") from error
    if line <= 0 or isinstance(raw_line, bool):
        raise ValueError("warning.line 必须是正整数")
    width = _nonempty_string(value.get("width"), "warning.width")
    width = re.sub(r"\s+", "", width).lower()
    if width.endswith("pt"):
        width = width[:-2]
    try:
        numeric_width = Decimal(width)
    except InvalidOperation as error:
        raise ValueError("warning.width 必须是 pt 数值") from error
    if not numeric_width.is_finite() or numeric_width < 0:
        raise ValueError("warning.width 必须是非负有限 pt 数值")
    normalized_width = format(numeric_width.normalize(), "f")
    if "." in normalized_width:
        normalized_width = normalized_width.rstrip("0").rstrip(".")
    if normalized_width == "-0":
        normalized_width = "0"
    return {
        "source_file": source_file,
        "line": line,
        "width_pt": normalized_width,
    }


def _fingerprint_identity(issue: Mapping[str, Any]) -> Dict[str, Any]:
    issue_type = _nonempty_string(issue.get("type"), "type")
    if issue_type not in ISSUE_TYPES:
        raise ValueError(f"未知问题类型：{issue_type}")

    affected = issue.get("affected_paper_ids", [])
    if not isinstance(affected, list) or any(
        not isinstance(item, str) or not item.strip() or item != item.strip()
        for item in affected
    ):
        raise ValueError("affected_paper_ids 必须是无首尾空白的非空字符串数组")
    canonical_affected = sorted(set(affected))
    if affected:
        return {
            "type": issue_type,
            "affected_paper_ids": canonical_affected,
            "conflict_code": _nonempty_string(
                issue.get("conflict_code"), "conflict_code"
            ),
        }

    paper_id = issue.get("paper_id")
    source = issue.get("source_id")
    question = issue.get("question_id")
    if question is not None or issue_type in _QUESTION_TYPES:
        return {
            "type": issue_type,
            "paper_id": _nonempty_string(paper_id, "paper_id"),
            "question_id": _nonempty_string(question, "question_id"),
            "source_id": _nonempty_string(source, "source_id"),
        }

    visual_markers = (
        "edition", "page", "check_code", "figure_id", "warning"
    )
    if issue_type in _VISUAL_TYPES or any(key in issue for key in visual_markers):
        page = issue.get("page")
        if isinstance(page, bool) or not isinstance(page, int) or page <= 0:
            raise ValueError("视觉问题 page 必须是正整数")
        identity: Dict[str, Any] = {
            "type": issue_type,
            "paper_id": _nonempty_string(paper_id, "paper_id"),
            "edition": _nonempty_string(issue.get("edition"), "edition"),
            "page": page,
            "check_code": _nonempty_string(
                issue.get("check_code"), "check_code"
            ),
        }
        figure_id = issue.get("figure_id")
        warning = issue.get("warning")
        if figure_id is None and warning is None:
            raise ValueError("视觉问题必须包含 figure_id 或 warning")
        if figure_id is not None:
            identity["figure_id"] = _nonempty_string(figure_id, "figure_id")
        if warning is not None:
            identity["warning"] = _normalized_warning(warning)
        return identity

    if source is not None or issue_type in _SOURCE_TYPES:
        return {
            "type": issue_type,
            "source_id": _nonempty_string(source, "source_id"),
        }

    return {
        "type": issue_type,
        "paper_id": _nonempty_string(paper_id, "paper_id"),
        "conflict_code": _nonempty_string(
            issue.get("conflict_code"), "conflict_code"
        ),
    }


def issue_fingerprint(issue: Mapping[str, Any]) -> str:
    if not isinstance(issue, Mapping):
        raise ValueError("issue 必须是对象")
    return hashlib.sha256(_canonical_bytes(_fingerprint_identity(issue))).hexdigest()


def _validate_issue(issue: Mapping[str, Any], require_fingerprint: bool) -> None:
    if not isinstance(issue, Mapping):
        raise ValueError("问题块 JSON 必须是对象")
    required = set(REQUIRED_FIELDS)
    if not require_fingerprint:
        required.remove("fingerprint")
    missing = sorted(field for field in required if field not in issue)
    if missing:
        raise ValueError("问题块缺少字段：" + ", ".join(missing))

    issue_type = issue.get("type")
    if issue_type not in ISSUE_TYPES:
        raise ValueError(f"未知问题类型：{issue_type}")
    status = issue.get("status")
    if status not in STATUSES:
        raise ValueError(f"未知 status：{status}")
    impact = issue.get("impact")
    if impact not in IMPACTS:
        raise ValueError(f"未知 impact：{impact}")
    _nonempty_string(issue.get("resume_action"), "resume_action")

    paper_id = issue.get("paper_id")
    if paper_id is not None:
        normalized_paper_id = _nonempty_string(paper_id, "paper_id")
        if normalized_paper_id != paper_id:
            raise ValueError("paper_id 不得包含首尾空白")
    affected = issue.get("affected_paper_ids")
    if not isinstance(affected, list) or any(
        not isinstance(item, str) or not item.strip() or item != item.strip()
        for item in affected
    ):
        raise ValueError("affected_paper_ids 必须是无首尾空白的非空字符串数组")
    if affected != sorted(set(affected)):
        raise ValueError("affected_paper_ids 必须去重排序")
    if paper_id is not None and affected:
        raise ValueError("单卷问题 affected_paper_ids 必须为空")
    source = issue.get("source_id")
    if source is not None:
        normalized_source = _nonempty_string(source, "source_id")
        if normalized_source != source:
            raise ValueError("source_id 不得包含首尾空白")
    if paper_id is None and not affected and source is None:
        raise ValueError("问题目标至少需要 paper_id/affected_paper_ids/source_id 之一")

    expected = issue_fingerprint(issue)
    if require_fingerprint:
        fingerprint = issue.get("fingerprint")
        if fingerprint != expected:
            raise ValueError(
                f"fingerprint 不匹配：期望 {expected}，实际 {fingerprint}"
            )


def blocks_completion(issue: Mapping[str, Any], paper_id: str) -> bool:
    targets = set(issue.get("affected_paper_ids") or [])
    if issue.get("paper_id") is not None:
        targets.add(issue["paper_id"])
    return (
        paper_id in targets
        and issue.get("impact") == "blocks_completion"
        and issue.get("status") != "resolved"
    )


# 逐题缺陷 → 问题类型。Task 16 的 provenance 导入按这张表建问题、也按它算期望
# fingerprint：类型选错时 fingerprint 就对不上，于是「随便挂一条 issue 顶数」这条路
# 是走不通的。表在这里而不在 provenance.py，理由与 `issue_fingerprint()` 同——问题的
# 身份口径只此一份，复制出去就等于给格式漂移开口子。
QUESTION_ISSUE_TYPES = {
    "transcription": "transcription-ambiguous",
    "answer": "answer-missing",
    "conflict": "answer-conflict",
}


def question_issue(
    paper_id: str,
    question_id: str,
    source_id: str,
    kind: str,
    resume_action: str,
    status: str = "open",
    impact: str = "blocks_completion",
) -> Dict[str, Any]:
    """构造一条逐题问题（含 fingerprint）。

    `source_id` 对上游卷是 manifest 的 source_id，对只有本地 legacy 源的回忆版是
    `legacy:<仓库相对路径>`——问题身份必须能区分「同一题、不同来源」，而
    `_fingerprint_identity()` 对 question 类问题要求 source_id 非空。
    """
    issue_type = QUESTION_ISSUE_TYPES.get(kind)
    if issue_type is None:
        raise ValueError(f"未知逐题问题类别：{kind!r}")
    candidate: Dict[str, Any] = {
        "paper_id": _nonempty_string(paper_id, "paper_id"),
        "affected_paper_ids": [],
        "type": issue_type,
        "status": status,
        "impact": impact,
        "question_id": _nonempty_string(question_id, "question_id"),
        "source_id": _nonempty_string(source_id, "source_id"),
        "resume_action": _nonempty_string(resume_action, "resume_action"),
    }
    _validate_issue(candidate, require_fingerprint=False)
    candidate["fingerprint"] = issue_fingerprint(candidate)
    return candidate


def question_issue_fingerprint(
    paper_id: str, question_id: str, source_id: str, kind: str
) -> str:
    """逐题问题的期望 fingerprint；`resume_action`/`status`/`impact` 不进身份。"""
    return question_issue(
        paper_id, question_id, source_id, kind, resume_action="占位"
    )["fingerprint"]


def issue_ids_by_paper(
    records: Sequence[Mapping[str, Any]]
) -> Dict[str, List[str]]:
    """把问题总账折成 `{paper_id: [issue_id]}`；共享问题登记进每一卷。"""
    by_paper: Dict[str, List[str]] = {}
    for item in records:
        targets = set(item.get("affected_paper_ids") or [])
        if item.get("paper_id") is not None:
            targets.add(item["paper_id"])
        for paper_id in targets:
            by_paper.setdefault(paper_id, []).append(item["issue_id"])
    return {key: sorted(value) for key, value in by_paper.items()}


def _strict_json_object(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    value: Dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"重复 JSON 字段：{key}")
        value[key] = item
    return value


def _parse_document(raw: str) -> Tuple[str, List[Tuple[str, Dict[str, Any], int, int]]]:
    matches = list(_ISSUE_HEADING.finditer(raw))
    all_headings = list(_ANY_ISSUE_HEADING.finditer(raw))
    if [match.span() for match in matches] != [match.span() for match in all_headings]:
        raise ValueError("问题块格式错误：存在无法识别的 ISSUE 标题")
    prefix = raw[:matches[0].start()] if matches else raw
    records: List[Tuple[str, Dict[str, Any], int, int]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw)
        block = raw[match.start():end]
        issue_id = match.group(1)
        if _ISSUE_ID.fullmatch(issue_id) is None:
            raise ValueError(f"问题编号格式错误：{issue_id}")
        body_pattern = re.compile(
            r"^## " + re.escape(issue_id)
            + r"[ \t]*\n+```json[ \t]*\n(.*?)\n```[ \t]*\n*$",
            re.DOTALL,
        )
        body_match = body_pattern.fullmatch(block)
        if body_match is None:
            raise ValueError(f"{issue_id}: 问题块格式错误")
        try:
            payload = json.loads(
                body_match.group(1), object_pairs_hook=_strict_json_object
            )
        except json.JSONDecodeError as error:
            raise ValueError(f"{issue_id}: JSON 无效：{error}") from error
        except ValueError as error:
            raise ValueError(f"{issue_id}: {error}") from error
        if not isinstance(payload, dict):
            raise ValueError(f"{issue_id}: JSON 顶层必须是对象")
        records.append((issue_id, payload, match.start(), end))
    return prefix, records


def load_issues(path: Path) -> List[Dict[str, Any]]:
    path = Path(path)
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"无法读取问题总账：{path}: {error}") from error
    _, records = _parse_document(raw)
    seen_ids = set()
    seen_fingerprints = set()
    result = []
    for issue_id, payload, _, _ in records:
        if issue_id in seen_ids:
            raise ValueError(f"重复问题编号：{issue_id}")
        seen_ids.add(issue_id)
        if _ISSUE_ID.fullmatch(issue_id) is None:
            raise ValueError(f"问题编号格式错误：{issue_id}")
        _validate_issue(payload, require_fingerprint=True)
        fingerprint = payload["fingerprint"]
        if fingerprint in seen_fingerprints:
            raise ValueError(f"重复 fingerprint：{fingerprint}")
        seen_fingerprints.add(fingerprint)
        value = copy.deepcopy(payload)
        value["issue_id"] = issue_id
        result.append(value)
    return result


def _serialize_block(issue_id: str, issue: Mapping[str, Any]) -> str:
    return (
        f"## {issue_id}\n\n```json\n"
        + json.dumps(
            issue,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n```\n"
    )


def _default_header() -> str:
    return (
        "# 高考数学 LaTeX 缺失与问题总账\n\n"
        "每个问题块使用稳定编号和可重算 fingerprint；已解决问题保留记录。\n\n"
    )


def upsert_issue(path: Path, issue: Mapping[str, Any]) -> str:
    path = Path(path)
    candidate = copy.deepcopy(dict(issue))
    candidate.pop("issue_id", None)
    candidate.pop("fingerprint", None)
    _validate_issue(candidate, require_fingerprint=False)
    candidate["fingerprint"] = issue_fingerprint(candidate)

    if path.exists():
        raw = path.read_text(encoding="utf-8")
        prefix, records = _parse_document(raw)
        existing = load_issues(path)
    else:
        raw = _default_header()
        prefix, records = raw, []
        existing = []

    matched_id = None
    for item in existing:
        if item["fingerprint"] == candidate["fingerprint"]:
            matched_id = item["issue_id"]
            break
    if matched_id is None:
        numbers = [int(_ISSUE_ID.fullmatch(item["issue_id"]).group(1)) for item in existing]
        matched_id = f"ISSUE-{(max(numbers, default=0) + 1):04d}"

    block = _serialize_block(matched_id, candidate)
    replacement = None
    for issue_id, _, start, end in records:
        if issue_id == matched_id:
            replacement = (start, end)
            break
    if replacement is None:
        separator = "" if raw.endswith("\n\n") else "\n"
        new_raw = raw + separator + block
    else:
        start, end = replacement
        new_raw = raw[:start] + block + raw[end:]
    if new_raw.encode("utf-8") != raw.encode("utf-8") or not path.exists():
        atomic_write_bytes(path, new_raw.encode("utf-8"))
    return matched_id


PHASE0_SEEDS = [
    {
        "paper_id": "gk-2026-regular-national-1-recall",
        "affected_paper_ids": [],
        "type": "identity-ambiguous",
        "status": "open",
        "impact": "blocks_completion",
        "resume_action": "正式卷公开后人工核验身份；回忆版不得自动绑定正式卷",
        "conflict_code": "recall-vs-official",
    },
    {
        "paper_id": None,
        "affected_paper_ids": [
            "gk-2017-regular-national-1-arts",
            "gk-2017-regular-national-1-science",
        ],
        "type": "identity-ambiguous",
        "status": "open",
        "impact": "blocks_completion",
        "resume_action": "逐卷核验规范源地区与固定上游全国 1 路径，不按地区字符串自动绑定",
        "conflict_code": "regions-vs-upstream-path",
    },
]


def _seed_bytes() -> bytes:
    raw = _default_header()
    for index, seed in enumerate(PHASE0_SEEDS, start=1):
        payload = copy.deepcopy(seed)
        _validate_issue(payload, require_fingerprint=False)
        payload["fingerprint"] = issue_fingerprint(payload)
        raw += _serialize_block(f"ISSUE-{index:04d}", payload)
    return raw.encode("utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理稳定编号的问题总账")
    subparsers = parser.add_subparsers(dest="command", required=True)
    initialize = subparsers.add_parser("init")
    initialize.add_argument("--phase0-seed", required=True, action="store_true")
    initialize.add_argument("--output", required=True, type=Path)
    validate = subparsers.add_parser("validate")
    validate.add_argument("--file", required=True, type=Path)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "validate":
        load_issues(arguments.file)
        return 0
    expected = _seed_bytes()
    output = arguments.output
    if output.exists():
        actual = output.read_bytes()
        if actual != expected:
            raise ValueError("现有问题总账与 phase0 seed 内容不同，拒绝覆盖")
        load_issues(output)
        return 0
    atomic_write_bytes(output, expected)
    load_issues(output)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=os.sys.stderr)
        raise SystemExit(1)

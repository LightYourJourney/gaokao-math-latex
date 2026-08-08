#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""status.py —— 只消费闭合 facts 的单卷/批次状态核心。

**这个模块不 import provenance / build / review**，方向是单向的：那三层各自把自己
的观察折成 facts 递进来，本模块只做纯映射。理由有两条，都不是洁癖：

1. 反向 import 会立刻成环（build 要问状态、状态要问 build），Python 层面只能靠
   延迟 import 绕，而延迟 import 会把「谁是权威」这件事藏进函数体；
2. 更要命的是**第二套 reconciler**——一旦状态判断散落在 build/review 两处，混合状态
   下的分歧不会报错，只会静默产出两个都自洽的答案。

状态优先级是 fail-closed 的：证据不全一律往回退，绝不往前进。`complete` 需要整条
证据链（provenance 当前、生成物当前、build succeeded 且回执当前、review passed 且
回执当前、批次报告已验证、无未解决的 completion blocker）同时成立。

`derive_content_outcome()` 与 `derive_status()` 的分家是 report 门禁：报告尚未逐字段
验证时只能拿到 `eligible_complete|eligible_blocked` **候选**，供报告渲染读取；把候选
持久化成 `complete/closed` 就等于用未验证的报告给自己背书。
"""
from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from issues import blocks_completion

PROJECT_RELATIVE = "math-gaokao-latex"
MANIFEST_TARGET = PROJECT_RELATIVE + "/source-manifest.json"
ISSUES_TARGET = PROJECT_RELATIVE + "/missing-issues.md"
BUILD_RECEIPT_NAME = "receipts/build.json"
REVIEW_RECEIPT_NAME = "receipts/review.json"
PROVENANCE_NAME = "provenance.json"

PROVENANCE_STATES: Tuple[str, ...] = ("missing", "invalid", "stale", "current")
BUILD_STATES: Tuple[str, ...] = (
    "missing", "running", "failed", "compiled_pending_review", "succeeded",
)
REVIEW_STATES: Tuple[str, ...] = ("missing", "pending", "failed", "passed")
ARTIFACT_STATES: Tuple[str, ...] = ("missing", "stale", "current")
CURRENCY_STATES: Tuple[str, ...] = ("current", "stale")

PRODUCTION_STATES: Tuple[str, ...] = (
    "legacy_unverified", "planned", "source_ready", "transcription_draft",
    "questions_verified", "answers_draft", "answers_verified", "shared_frozen",
    "editions_generated", "compiled", "complete", "blocked",
)
BATCH_STATES: Tuple[str, ...] = (
    "planned", "provenance_verified", "compiled_pending_review", "closed",
    "closed_with_blockers",
)
CONTENT_OUTCOMES: Tuple[str, ...] = (
    "legacy_unverified", "answers_verified", "editions_generated", "compiled",
    "eligible_blocked", "eligible_complete",
)

GIT_STATES: Tuple[str, ...] = ("validated", "committed")

# facts 的字段表与取值域一起冻结：多一个键、少一个键、值不在域内，都是调用方漏了
# 一层观察，绝不能按默认值放行。
_ENUM_FIELDS = {
    "provenance": PROVENANCE_STATES,
    "artifacts": ARTIFACT_STATES,
    "build": BUILD_STATES,
    "build_currency": CURRENCY_STATES,
    "review": REVIEW_STATES,
    "review_currency": CURRENCY_STATES,
}
_BOOLEAN_FIELDS = (
    "provenance_unknown", "provenance_conflicts", "batch_report_valid",
)
_CONTENT_FIELDS = frozenset(
    ["paper_id", "issues"] + list(_ENUM_FIELDS) + list(_BOOLEAN_FIELDS)
) - frozenset(["batch_report_valid"])
_FULL_FIELDS = _CONTENT_FIELDS | frozenset(["batch_report_valid"])


class StatusError(ValueError):
    """状态核心的唯一异常类型：facts 不合法或状态机未命中任何分支。"""


# ---------------------------------------------------------------- facts 构造


def paper_facts(
    paper_id: str,
    provenance: str = "missing",
    provenance_unknown: bool = False,
    provenance_conflicts: bool = False,
    artifacts: str = "missing",
    build: str = "missing",
    build_currency: str = "stale",
    review: str = "missing",
    review_currency: str = "stale",
    issues: Sequence[Mapping[str, Any]] = (),
    batch_report_valid: bool = False,
) -> Dict[str, Any]:
    """构造并当场校验一份完整 facts。

    默认值一律取最保守档（缺失 / stale / 未验证）：调用方漏传某一维时得到的是
    「证据不足」而不是「默认通过」。
    """
    facts = {
        "paper_id": paper_id,
        "provenance": provenance,
        "provenance_unknown": provenance_unknown,
        "provenance_conflicts": provenance_conflicts,
        "artifacts": artifacts,
        "build": build,
        "build_currency": build_currency,
        "review": review,
        "review_currency": review_currency,
        "issues": tuple(issues),
        "batch_report_valid": batch_report_valid,
    }
    validate_facts(facts)
    return facts


def validate_facts(facts: Mapping[str, Any], with_report: bool = True) -> None:
    if not isinstance(facts, Mapping):
        raise StatusError("facts 必须是映射")
    expected = _FULL_FIELDS if with_report else _CONTENT_FIELDS
    actual = frozenset(facts)
    if actual != expected:
        missing = sorted(expected - actual)
        unknown = sorted(actual - expected)
        raise StatusError(f"facts 字段不匹配：缺 {missing}，多 {unknown}")
    if not isinstance(facts["paper_id"], str) or not facts["paper_id"].strip():
        raise StatusError("facts.paper_id 必须是非空字符串")
    for field, domain in _ENUM_FIELDS.items():
        if facts[field] not in domain:
            raise StatusError(f"facts.{field} 取值非法：{facts[field]!r}")
    for field in _BOOLEAN_FIELDS:
        if field in facts and not isinstance(facts[field], bool):
            raise StatusError(f"facts.{field} 必须是布尔值")
    if not isinstance(facts["issues"], (list, tuple)):
        raise StatusError("facts.issues 必须是数组")
    for issue in facts["issues"]:
        if not isinstance(issue, Mapping):
            raise StatusError("facts.issues 的元素必须是对象")


def facts_without_report(facts: Mapping[str, Any]) -> Dict[str, Any]:
    """剥掉 report 事实，得到内容候选阶段的输入。"""
    validate_facts(facts, with_report=True)
    return {key: value for key, value in facts.items() if key != "batch_report_valid"}


# ---------------------------------------------------------------- 有效状态


def effective_build(facts: Mapping[str, Any]) -> str:
    """把 build 状态与回执当前性折成一个值。

    `missing/running/failed` 与当前性无关（分别是「没有」「未完成」「有定论的负结果」）；
    只有正结果需要当前性背书——过期的正结果一律降级为 `stale`，这正是「旧 PDF 不能假绿」
    在状态层的落点。
    """
    build = facts["build"]
    if build in {"missing", "running", "failed"}:
        return build
    return build if facts["build_currency"] == "current" else "stale"


def effective_review(facts: Mapping[str, Any]) -> str:
    review = facts["review"]
    if review in {"missing", "pending", "failed"}:
        return review
    return review if facts["review_currency"] == "current" else "stale"


def _has_blocker(facts: Mapping[str, Any]) -> bool:
    return any(
        blocks_completion(issue, facts["paper_id"]) for issue in facts["issues"]
    )


# ---------------------------------------------------------------- 单卷状态


def derive_content_outcome(facts_without_report_value: Mapping[str, Any]) -> str:
    """内容候选：只看内容事实，**不看批次报告**。

    返回值里没有 `complete`，只有 `eligible_complete`——命名上就堵死「候选被当成结论
    持久化」这条路。
    """
    facts = facts_without_report_value
    validate_facts(facts, with_report=False)

    if facts["provenance"] != "current":
        return "legacy_unverified"
    if facts["provenance_unknown"] or facts["provenance_conflicts"]:
        return "eligible_blocked"
    if facts["build"] == "failed" or facts["review"] == "failed":
        return "eligible_blocked"
    if _has_blocker(facts):
        return "eligible_blocked"
    if facts["artifacts"] != "current":
        return "answers_verified"
    build = effective_build(facts)
    if build in {"missing", "running", "stale"}:
        return "editions_generated"
    if build != "succeeded" or effective_review(facts) != "passed":
        return "compiled"
    return "eligible_complete"


def derive_status(facts: Mapping[str, Any]) -> str:
    """最终 paper 状态：内容候选 + 批次报告验证结果。

    `eligible_complete` 但报告未验证时退回 `compiled`——计划散文没有为这一格点名状态，
    退回最近的已验证事实（XeLaTeX 通过）是唯一 fail-closed 的读法。
    """
    validate_facts(facts, with_report=True)
    outcome = derive_content_outcome(facts_without_report(facts))
    if outcome == "eligible_blocked":
        return "blocked"
    if outcome == "eligible_complete":
        return "complete" if facts["batch_report_valid"] else "compiled"
    return outcome


# ---------------------------------------------------------------- 批次状态


def reconcile_batch_status(facts_by_paper: Mapping[str, Mapping[str, Any]]) -> str:
    """批次状态**只由现场 facts 直接派生**，不从 paper 缓存状态反推，也没有 setter。

    优先级逐条对应计划的表；末尾的 raise 不是防御性代码而是状态机自检：前五条已经把
    「不是全员 succeeded/passed/report-valid」全部吸收，落到最后还不满足 6/7 条，只能
    是这份表被改坏了。
    """
    if not isinstance(facts_by_paper, Mapping) or not facts_by_paper:
        raise StatusError("批次必须至少包含一卷 facts")
    values = [facts_by_paper[key] for key in sorted(facts_by_paper)]
    for facts in values:
        validate_facts(facts, with_report=True)

    if any(facts["provenance"] != "current" for facts in values):
        return "planned"
    # 计划散文说 reconciler「直接检查 provenance、生成物、build、review 和 issues」，
    # 但它给的表里没有生成物那一行——于是「生成物已漂移、build 回执却仍当前」这一格
    # 落不到任何分支（单卷是 answers_verified，批次无处可去）。现实里生成物漂移必然
    # 连带 build 回执 stale（generation_input_tree 含四壳），但状态机不能依赖调用方的
    # 自觉。按 fail-closed 补进本行：没有当前生成物就谈不上编译，退回 provenance_verified。
    if any(
        facts["artifacts"] != "current"
        or effective_build(facts) in {"missing", "running", "failed", "stale"}
        for facts in values
    ):
        return "provenance_verified"
    if any(effective_build(facts) == "compiled_pending_review" for facts in values):
        return "compiled_pending_review"
    if any(
        effective_build(facts) == "succeeded" and effective_review(facts) != "passed"
        for facts in values
    ):
        return "compiled_pending_review"
    if any(not facts["batch_report_valid"] for facts in values):
        return "compiled_pending_review"

    derived = [derive_status(facts) for facts in values]
    if all(item == "complete" for item in derived):
        return "closed"
    if all(item in {"complete", "blocked"} for item in derived) and any(
        item == "blocked" for item in derived
    ):
        return "closed_with_blockers"
    raise StatusError(f"批次状态机未命中任何分支：{sorted(set(derived))}")


# ---------------------------------------------------------------- 所有权路径


def _papers_by_id(manifest: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    papers = manifest.get("papers")
    if not isinstance(papers, list):
        raise StatusError("manifest.papers 必须是数组")
    return {paper["paper_id"]: paper for paper in papers}


def build_receipt_path(paper: Mapping[str, Any]) -> str:
    return "%s/%s/%s" % (PROJECT_RELATIVE, paper["project_dir"], BUILD_RECEIPT_NAME)


def review_receipt_path(paper: Mapping[str, Any]) -> str:
    return "%s/%s/%s" % (PROJECT_RELATIVE, paper["project_dir"], REVIEW_RECEIPT_NAME)


def provenance_path(paper: Mapping[str, Any]) -> str:
    """该卷 provenance 的规范路径。

    三条路径（build / review / provenance）的拼法住在同一处，理由与
    `paper_ownership_paths()` 相同：路径是 `git add --pathspec-from-file` 与事务目标
    的唯一来源，两份拼法漂移一次就会写到别处去。这里只做拼接，**不引入任何状态规则**。
    """
    return "%s/%s/%s" % (PROJECT_RELATIVE, paper["project_dir"], PROVENANCE_NAME)


def paper_provenance_paths(
    manifest: Mapping[str, Any], paper_ids: Iterable[str]
) -> Tuple[str, ...]:
    """给定若干卷的 provenance 路径，排序去重（构成同上的窄所有权范围）。"""
    known = _papers_by_id(manifest)
    paths = []
    for paper_id in paper_ids:
        if paper_id not in known:
            raise StatusError(f"未知 paper_id：{paper_id}")
        paths.append(provenance_path(known[paper_id]))
    unique = sorted(set(paths))
    if len(unique) != len(paths):
        raise StatusError("所有权范围内路径重复")
    return tuple(unique)


def paper_ownership_paths(
    manifest: Mapping[str, Any], paper_ids: Iterable[str]
) -> Tuple[str, ...]:
    """给定若干卷的构建 ownership 路径（各卷 build 回执），排序去重。

    这一组路径是 `git add --pathspec-from-file` 的唯一来源：多一条就会夹带别的会话的
    改动，少一条就会把诊断状态留在工作区。
    """
    known = _papers_by_id(manifest)
    paths = []
    for paper_id in paper_ids:
        if paper_id not in known:
            raise StatusError(f"未知 paper_id：{paper_id}")
        paths.append(build_receipt_path(known[paper_id]))
    unique = sorted(set(paths))
    if len(unique) != len(paths):
        raise StatusError("所有权范围内路径重复")
    return tuple(unique)


def batch_ownership_paths(
    manifest: Mapping[str, Any], batch_id: str
) -> Tuple[str, ...]:
    batches = [
        item for item in manifest.get("batches", []) if item["batch_id"] == batch_id
    ]
    if len(batches) != 1:
        raise StatusError(f"未知批次：{batch_id}")
    return paper_ownership_paths(manifest, batches[0]["paper_ids"])


# ---------------------------------------------------------------- git 派生


def _git_lines(root: Path, arguments: Sequence[str]) -> List[str]:
    raw = subprocess.run(
        ["git", "-C", str(root)] + list(arguments),
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def derive_git_state(repo: Path, paths: Sequence[str]) -> str:
    """git 持久化是**只读派生**，不是可写字段：validated / committed 二选一，否则失败。

    `validated` = 内容门禁已过但 ownership paths 相对 HEAD 仍有变化（含未跟踪新增）；
    `committed` = 这些路径已入 HEAD、工作树与索引对其零 diff，且能由 `git log` 定位到
    提交。既非二者（例如路径根本不在 HEAD 也没有变化）时失败——那说明调用方给的路径集
    与实际产物对不上，猜一个状态只会把错误写进报告。
    """
    root = Path(repo)
    cleaned: List[str] = []
    for raw in paths:
        candidate = PurePosixPath(str(raw))
        if candidate.is_absolute() or any(
            part in {"", ".", ".."} for part in candidate.parts
        ):
            raise StatusError(f"ownership 路径必须是安全的仓库相对路径：{raw}")
        cleaned.append(candidate.as_posix())
    if not cleaned:
        raise StatusError("ownership 路径不得为空")
    ordered = sorted(set(cleaned))

    try:
        changed = set(
            _git_lines(root, ["diff", "--name-only", "-z", "HEAD", "--"] + ordered)
        )
        untracked = set(
            _git_lines(
                root,
                ["ls-files", "--others", "--exclude-standard", "-z", "--"] + ordered,
            )
        )
        if changed or untracked:
            return "validated"
        tracked = set(
            _git_lines(root, ["ls-tree", "-r", "-z", "--name-only", "HEAD", "--"] + ordered)
        )
        missing = sorted(set(ordered) - tracked)
        if missing:
            raise StatusError(f"ownership 路径未进入 HEAD：{missing}")
        history = subprocess.run(
            ["git", "-C", str(root), "log", "-1", "--format=%H", "--"] + ordered,
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout.strip()
    except subprocess.SubprocessError as error:
        raise StatusError(f"无法读取 git 状态：{error}") from error
    if not history:
        raise StatusError("ownership 路径没有可定位的提交历史")
    return "committed"

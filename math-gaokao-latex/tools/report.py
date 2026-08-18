#!/usr/bin/env python3
"""从阶段 0 的结构化事实生成六份一致的 Markdown 报告。"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

import build_projects
import cli_common
import review_receipts
from status import batch_ownership_paths, derive_git_state
from transaction import Transaction

BASE = Path("math-gaokao-latex")
MANIFEST_TARGET = BASE / "source-manifest.json"
ISSUES_TARGET = BASE / "missing-issues.md"
OUTPUT_TARGETS = (
    "docs/source-inventory.md",
    "report.md",
    "README_数学.md",
    "math-gaokao-latex/README.md",
    "math-gaokao-2017-2026/README.md",
    "math-gaokao-latex/reports/baseline.md",
)
REPORT_SOURCE = "math-gaokao-latex/tools/report.py"


class ReportError(RuntimeError):
    pass


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReportError(f"无法读取 {path}: {error}") from error
    if not isinstance(value, dict):
        raise ReportError(f"{path} 顶层必须是对象")
    return value


def _canonical(root: Path, path: Path, expected: Path, label: str) -> None:
    if path.resolve() != (root / expected).resolve():
        raise ReportError(f"{label} 必须是固定路径 {expected.as_posix()}")


def _warning_counts(builds: Sequence[Mapping[str, Any]], reviews: Sequence[Mapping[str, Any]]) -> Counter:
    result: Counter = Counter()
    for build in builds:
        for edition in build["editions"]:
            log = edition["log"]
            for warning in log.get("overfull", []):
                result[str(warning.get("kind", "Overfull")).lower()] += 1
            result["underfull"] += len(log.get("underfull", []))
    for review in reviews:
        result["warning_exemptions"] += len(review.get("warning_exemptions", []))
    return result


def collect_report_facts(manifest_path: Path, issues_path: Path) -> Dict[str, Any]:
    """读取当前结构化账本并重跑 build/review、状态及提交门禁。"""
    manifest_path = Path(manifest_path).resolve()
    issues_path = Path(issues_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    _canonical(root, issues_path, ISSUES_TARGET, "--issues")
    manifest = _load_json(manifest_path)
    inventory = manifest.get("inventory", {})
    roots = inventory.get("root_counts", {})
    total = inventory.get("total_sources")
    regular, spring = roots.get("regular"), roots.get("spring")
    if (total, regular, spring) != (775, 734, 41) or total != regular + spring:
        raise ReportError("来源守恒失败：要求 775 = 734 + 41")
    historical_papers = [
        paper for paper in manifest.get("papers", []) if paper.get("legacy_ids")
    ]
    if len(historical_papers) != 21:
        raise ReportError("历史产出应恰好覆盖 21 套试卷")

    historical_ids = {paper["paper_id"] for paper in historical_papers}
    historical_batches = []
    for batch in manifest.get("batches", []):
        paper_ids = set(batch.get("paper_ids", []))
        if paper_ids & historical_ids and not paper_ids <= historical_ids:
            raise ReportError(f"{batch['batch_id']}: 不允许混合历史卷与非历史卷")
        if paper_ids and paper_ids <= historical_ids:
            historical_batches.append(batch)
    validations = {}
    validation_problems = []
    for batch in historical_batches:
        result = review_receipts.check_batch(
            manifest_path, issues_path, batch["batch_id"], require_current_build=True
        )
        validations[batch["batch_id"]] = result["code"]
        validation_problems.extend(result["problems"])
    if any(code != "FINALIZED" for code in validations.values()):
        raise ReportError("批次重算失败：" + "；".join(validation_problems))
    validation = {"batches": validations}

    papers = {paper["paper_id"]: paper for paper in historical_papers}
    statuses = Counter()
    builds, reviews = [], []
    batches = []
    for batch in historical_batches:
        batch_id = batch["batch_id"]
        paper_statuses = [papers[paper_id]["production_state"] for paper_id in batch["paper_ids"]]
        expected = "closed" if all(value == "complete" for value in paper_statuses) else "closed_with_blockers" if any(value == "blocked" for value in paper_statuses) else None
        if expected is None or batch.get("status") != expected:
            raise ReportError(f"{batch_id}: manifest 已关闭但重算不一致")
        paths = review_receipts.batch_review_paths(manifest, batch_id, include_state=True, report=True)
        git_state = derive_git_state(root, paths)
        if git_state != "committed":
            raise ReportError(f"{batch_id}: ownership paths 尚未提交（{git_state}）")
        batches.append({"batch_id": batch_id, "status": expected, "validation": validation["batches"][batch_id], "git_state": git_state})

    for paper in historical_papers:
        status = paper["production_state"]
        statuses[status if status in {"complete", "blocked"} else "in_progress"] += 1
        receipt_dir = root / BASE / paper["project_dir"] / "receipts"
        builds.append(build_projects.load_receipt(receipt_dir / "build.json"))
        reviews.append(review_receipts.load_review(receipt_dir / "review.json"))
    succeeded = sum(
        edition["result"] == "succeeded"
        for build in builds for edition in build["editions"]
    )
    if succeeded != 84:
        raise ReportError(f"当前构建成功数不是 84：{succeeded}")
    warnings = _warning_counts(builds, reviews)
    legacy = _load_json(root / BASE / "reports/legacy-baseline.json")
    legacy_summary = legacy.get("summary", {})
    if legacy_summary.get("overfull_count") != 1:
        raise ReportError("legacy baseline 的 Overfull 事实必须为 1")

    return {
        "root": root,
        "sources": {"total": total, "regular": regular, "spring": spring},
        "legacy": {"papers": legacy_summary.get("paper_count"), "targets": legacy_summary.get("target_count"), "overfull": 1},
        "current": {
            "statuses": {key: statuses[key] for key in ("complete", "blocked", "in_progress")},
            "builds_succeeded": succeeded,
            "overfull": warnings["overfull"],
            "underfull": warnings["underfull"],
            "warning_exemptions": warnings["warning_exemptions"],
        },
        "batches": batches,
    }


def _summary(facts: Mapping[str, Any]) -> str:
    current, statuses = facts["current"], facts["current"]["statuses"]
    return (
        f"- 来源守恒：**775 = 734 + 41**（普通高考 734，春季高考 41；2004 `.txt` 不计入 PDF 来源）\n"
        f"- 历史口径：21 套、84 个版本；legacy baseline 的 Overfull 为 **1**\n"
        f"- 当前口径：complete {statuses['complete']}，blocked {statuses['blocked']}，in_progress {statuses['in_progress']}\n"
        f"- 当前构建：{current['builds_succeeded']}/84 succeeded\n"
        f"- 当前警告重算：Overfull {current['overfull']}，Underfull {current['underfull']}，警告豁免 {current['warning_exemptions']}\n"
        "- 上游题面不含答案的说法仅有三份抽样证据，不外推为 775 份全部无答案。\n"
    )


def _batch_table(facts: Mapping[str, Any]) -> str:
    lines = ["| 批次 | 重算终态 | 回执门禁 | ownership |", "|---|---|---|---|"]
    lines += [f"| {b['batch_id']} | {b['status']} | {b['validation']} | {b['git_state']} |" for b in facts["batches"]]
    return "\n".join(lines) + "\n"


def render_outputs(facts: Mapping[str, Any]) -> Dict[str, str]:
    """只在内存中从同一事实快照渲染固定六目标。"""
    summary, batches = _summary(facts), _batch_table(facts)
    bodies = {
        OUTPUT_TARGETS[0]: "# 高考数学来源清单\n\n" + summary + "\n## 阶段 0 批次\n\n" + batches,
        OUTPUT_TARGETS[1]: "# 高考数学资料报告\n\n阶段 0 的机器事实如下。blocked 与 complete 分开统计。\n\n" + summary + "\n" + batches,
        OUTPUT_TARGETS[2]: "# 高考数学资料说明\n\n## 阶段 0 状态\n\n" + summary + "\n" + batches,
        OUTPUT_TARGETS[3]: "# 高考数学 LaTeX 项目\n\n## 阶段 0 机器报告\n\n" + summary + "\n" + batches + "\n来源清单：`manifest.csv` 是 `source-manifest.json` 的来源级清单投影，每个上游 PDF 一行。重建命令：\n\n```bash\npython3 tools/manifest_csv.py \\\n  --manifest source-manifest.json \\\n  --output manifest.csv \\\n  --write\n```\n\n运行 `python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md` 校验。\n",
        OUTPUT_TARGETS[4]: "# 高考数学 2017—2026\n\n## 与阶段 0 的关系\n\n" + summary + "\n本目录是历史来源工程；当前 21 套 LaTeX 产出位于相邻的 `math-gaokao-latex/`。\n",
        OUTPUT_TARGETS[5]: "# 高考数学 LaTeX 阶段 0 基线\n\n" + summary + "\n## 六批终态\n\n" + batches,
    }
    return {path: text if text.endswith("\n") else text + "\n" for path, text in bodies.items()}


def check_outputs(outputs: Mapping[str, str], root: Optional[Path] = None) -> Sequence[str]:
    root = Path(root or Path.cwd()).resolve()
    drift = []
    for relative in OUTPUT_TARGETS:
        path = root / relative
        expected = outputs[relative]
        try:
            actual = path.read_text(encoding="utf-8")
        except OSError:
            actual = None
        if actual != expected:
            drift.append(relative)
    return tuple(drift)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _transaction_inputs(root: Path, manifest: Mapping[str, Any]) -> Dict[str, str]:
    paths = {REPORT_SOURCE, MANIFEST_TARGET.as_posix(), ISSUES_TARGET.as_posix(), (BASE / "reports/legacy-baseline.json").as_posix()}
    historical_papers = [paper for paper in manifest["papers"] if paper.get("legacy_ids")]
    historical_ids = {paper["paper_id"] for paper in historical_papers}
    for batch in manifest["batches"]:
        paper_ids = set(batch.get("paper_ids", []))
        if paper_ids & historical_ids and not paper_ids <= historical_ids:
            raise ReportError(f"{batch['batch_id']}: 不允许混合历史卷与非历史卷")
        if paper_ids and paper_ids <= historical_ids:
            paths.add((BASE / "reports" / f"{batch['batch_id']}.md").as_posix())
    for paper in historical_papers:
        base = BASE / paper["project_dir"]
        paths.update({(base / "provenance.json").as_posix(), (base / "receipts/build.json").as_posix(), (base / "receipts/review.json").as_posix()})
    return {path: _sha256(root / path) for path in sorted(paths)}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("render", "check"):
        child = sub.add_parser(command)
        child.add_argument("--all", action="store_true", required=True)
        child.add_argument("--manifest", type=Path, required=True)
        child.add_argument("--issues", type=Path, required=True)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parser().parse_args(argv)
    try:
        facts = collect_report_facts(args.manifest, args.issues)
        outputs = render_outputs(facts)
        root = facts["root"]
        if args.command == "check":
            drift = check_outputs(outputs, root)
            if drift:
                raise ReportError("输出不一致：" + "、".join(drift))
            print("报告输出当前且六批门禁通过")
            return 0
        manifest = _load_json(Path(args.manifest))
        targets = {path: value.encode("utf-8") for path, value in outputs.items()}
        transaction = Transaction(root)
        transaction.prepare("content", targets, _transaction_inputs(root, manifest)).commit()
        print("已用一个 content 事务写入六个报告目标")
        return 0
    except (ReportError, OSError, ValueError, build_projects.BuildError, review_receipts.ReviewError) as error:
        print(str(error), file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""从全量 manifest、构建/复核回执及问题总账生成一致的项目报告。"""
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
import issues as issues_module
import review_receipts
from status import StatusError, derive_git_state
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
REPORT_DEPENDENCIES = (
    "build_projects.py",
    "cli_common.py",
    "issues.py",
    "manifest.py",
    "provenance.py",
    "review_receipts.py",
    "schema_validate.py",
    "status.py",
    "transaction.py",
)


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
    """读取全量结构化账本；未完成/失败状态作为事实返回，不阻止报告生成。"""
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
    sources = manifest.get("sources", [])
    papers = manifest.get("papers", [])
    manifest_batches = manifest.get("batches", [])
    if not isinstance(sources, list) or not isinstance(papers, list) or not isinstance(manifest_batches, list):
        raise ReportError("manifest 的 sources/papers/batches 必须是数组")
    if total != len(sources) or regular is None or spring is None or total != regular + spring:
        raise ReportError("来源守恒失败：inventory 与 sources 数量不一致")

    try:
        chain = build_projects.resolve_toolchain()
        validation = review_receipts.check_all(
            manifest_path, issues_path, require_current_build=True, toolchain=chain
        )
        validation_codes = validation["batches"]
    except build_projects.BuildError as error:
        validation_codes = {batch["batch_id"]: "TOOLCHAIN_UNAVAILABLE" for batch in manifest_batches}
        validation = {"problems": [str(error)]}

    paper_states = Counter(str(paper.get("production_state") or "unknown") for paper in papers)
    source_states = Counter(str(source.get("source_state") or "unknown") for source in sources)
    builds: list[Dict[str, Any]] = []
    reviews: list[Dict[str, Any]] = []
    build_states: Counter = Counter()
    review_states: Counter = Counter()
    edition_results: Counter = Counter()
    missing_builds = invalid_builds = missing_reviews = invalid_reviews = 0
    for paper in papers:
        receipt_dir = root / BASE / paper["project_dir"] / "receipts"
        build_path, review_path = receipt_dir / "build.json", receipt_dir / "review.json"
        if not build_path.is_file():
            missing_builds += 1
        else:
            try:
                build = build_projects.load_receipt(build_path)
                builds.append(build)
                build_states[str(build.get("status") or "unknown")] += 1
                for edition in build.get("editions", []):
                    edition_results[str(edition.get("result") or "unknown")] += 1
            except build_projects.BuildError:
                invalid_builds += 1
        if not review_path.is_file():
            missing_reviews += 1
        else:
            try:
                review = review_receipts.load_review(review_path)
                reviews.append(review)
                review_states[str(review.get("status") or "unknown")] += 1
            except review_receipts.ReviewError:
                invalid_reviews += 1

    issue_records = issues_module.load_issues(issues_path)
    issue_summary = _issue_summary(issue_records)
    batches = []
    for batch in manifest_batches:
        batch_id = batch["batch_id"]
        try:
            paths = review_receipts.batch_review_paths(manifest, batch_id, include_state=True, report=True)
            git_state = derive_git_state(root, paths)
        except StatusError:
            git_state = "unavailable"
        batches.append({
            "batch_id": batch_id,
            "status": str(batch.get("status") or "unknown"),
            "validation": validation_codes.get(batch_id, "MISSING"),
            "git_state": git_state,
            "paper_count": len(batch.get("paper_ids", [])),
        })
    warnings = _warning_counts(builds, reviews)
    return {
        "root": root,
        "sources": {"total": total, "regular": regular, "spring": spring},
        "source_states": dict(source_states),
        "papers": {"total": len(papers), "states": dict(paper_states)},
        "issues": issue_summary,
        "current": {
            "build_states": dict(build_states),
            "review_states": dict(review_states),
            "edition_results": dict(edition_results),
            "edition_total": sum(edition_results.values()),
            "editions_compiled": edition_results["succeeded"],
            "missing_builds": missing_builds,
            "invalid_builds": invalid_builds,
            "missing_reviews": missing_reviews,
            "invalid_reviews": invalid_reviews,
            "overfull": warnings["overfull"],
            "underfull": warnings["underfull"],
            "warning_exemptions": warnings["warning_exemptions"],
        },
        "batches": batches,
        "validation_problems": validation.get("problems", []),
    }


def _issue_summary(records: Sequence[Mapping[str, Any]]) -> Dict[str, int]:
    states = Counter(str(issue.get("status") or "unknown") for issue in records)
    return {
        "total": len(records),
        "open": sum(count for state, count in states.items() if state != "resolved"),
        "resolved": states["resolved"],
        "blocks_completion": sum(
            issue.get("status") != "resolved" and issue.get("impact") == "blocks_completion"
            for issue in records
        ),
    }


def _summary(facts: Mapping[str, Any]) -> str:
    current, paper_states = facts["current"], facts["papers"]["states"]
    validation_counts = Counter(batch["validation"] for batch in facts["batches"])
    failed_batches = [batch["batch_id"] for batch in facts["batches"] if batch["validation"] != "FINALIZED"]
    return (
        f"- 来源总数：**{facts['sources']['total']}**（普通高考 {facts['sources']['regular']}，春季高考 {facts['sources']['spring']}）。\n"
        f"- 来源状态：{_counter_text(facts.get('source_states', {}))}\n"
        f"- 试卷总数：**{facts['papers']['total']}**；生产状态：{_counter_text(paper_states)}\n"
        f"- 批次总数：**{len(facts['batches'])}**；manifest 状态：{_counter_text(Counter(batch['status'] for batch in facts['batches']))}\n"
        f"- 正式复核门禁：{_counter_text(validation_counts)}\n"
        f"- 已编译版本：{current['editions_compiled']}/{current['edition_total']}；构建回执状态：{_counter_text(current['build_states'])}\n"
        f"- review 回执状态：{_counter_text(current['review_states'])}\n"
        f"- 问题总账：{facts['issues']['total']} 条，未解决问题：{facts['issues']['open']}，阻塞完成 {facts['issues']['blocks_completion']}。\n"
        f"- 回执日志警告汇总（包含待复核回执）：Overfull {current['overfull']}，Underfull {current['underfull']}，豁免记录 {current['warning_exemptions']}。\n"
        f"- 回执完整性：build 缺失 {current['missing_builds']} / 无效 {current['invalid_builds']}；review 缺失 {current['missing_reviews']} / 无效 {current['invalid_reviews']}。\n"
        + ("- 门禁未通过批次：" + "、".join(failed_batches) + "。\n" if failed_batches else "- 所有批次复核门禁通过。\n")
    )


def _counter_text(values: Mapping[str, int]) -> str:
    return "，".join(f"{key} {values[key]}" for key in sorted(values)) or "无"


def _batch_table(facts: Mapping[str, Any]) -> str:
    lines = ["| 批次 | 试卷数 | manifest 状态 | 回执门禁 | ownership |", "|---|---:|---|---|---|"]
    lines += [f"| {b['batch_id']} | {b['paper_count']} | {b['status']} | {b['validation']} | {b['git_state']} |" for b in facts["batches"]]
    return "\n".join(lines) + "\n"


def render_outputs(facts: Mapping[str, Any]) -> Dict[str, str]:
    """只在内存中从同一全量事实快照渲染固定六目标。"""
    summary, batches = _summary(facts), _batch_table(facts)
    bodies = {
        OUTPUT_TARGETS[0]: "# 高考数学来源清单\n\n" + summary + "\n来源逐项信息见 `../math-gaokao-latex/manifest.csv`。\n",
        OUTPUT_TARGETS[1]: "# 高考数学真题 LaTeX 项目报告\n\n" + summary + "\n## 批次明细\n\n" + batches,
        OUTPUT_TARGETS[2]: "# 高考数学资料说明\n\n" + summary + "\n完整构建、复核和缺失事项见 `report.md` 与 `math-gaokao-latex/missing-issues.md`。\n",
        OUTPUT_TARGETS[3]: "# 高考数学 LaTeX 项目\n\n## 全量状态\n\n" + summary + "\n## 交付物与校验\n\n来源清单：`manifest.csv` 是 `source-manifest.json` 的来源级清单投影，每个上游 PDF 一行。\n\n```bash\npython3 math-gaokao-latex/tools/manifest_csv.py --manifest math-gaokao-latex/source-manifest.json --output math-gaokao-latex/manifest.csv --write\npython3 math-gaokao-latex/tools/report.py render --all --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md\npython3 math-gaokao-latex/tools/report.py check --all --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md\n```\n\n### 题目级 IR 导出（增量能力）\n\n可从已登记的规范 Markdown 题面与逐题 `provenance.json` 生成确定性 JSON，不重新 OCR 或重录题面：\n\n```bash\npython3 math-gaokao-latex/tools/export_question_ir.py gk-2017-regular-national-1-science --output /tmp/2017-national-1-science.ir.json\n```\n\n导出前会核对 `paper_id`、唯一 canonical 来源绑定、manifest 与逐题 provenance 中登记的来源 PDF SHA-256、题数、逐题 ID、source ID 和题面哈希；它不重新打开/哈希 PDF 原件。任一记录不一致即失败。题面以 `body_markdown` 保留解析题块，当前没有结构化证据的 `options`、`equations`、`tables` 与 `source_bbox` 保持 null；图像 Markdown 引用独立列出。项目答案材料只作为 `answer_evidence`，`official_answer` 固定为 null。该工具目前只覆盖已登记规范 Markdown 的导出，不代表 OCR→IR 自动接入或整卷验收。\n\nOCR 整页结果使用独立候选格式，不能自动分配给题号；例如把已登记 JSONL 第 2 条 MinerU 结果绑定到 manifest 来源：\n\n```bash\npython3 math-gaokao-latex/tools/ocr_candidate_ir.py math-gaokao-latex/benchmarks/ocr-runs.jsonl --line 2 --output /tmp/2008-page05-ocr-candidate.json\n```\n\n只有在 source ID、PDF SHA、页码与引擎字段匹配时才导出；结果始终 `recognized_unverified` / `needs-review`，并保留页级原文、区域坐标（如有）及已有耗时/缓存/资源记录。`question_id` 为空；人工按原图切分、核对并确认前，不得导入规范题面。\n",
        OUTPUT_TARGETS[4]: "# 高考数学 2017—2026\n\n## 题库工程状态\n\n" + summary + "本目录保存 2017—2026 年转录与来源材料；统一 LaTeX 项目目录及完整批次清单位于相邻的 `math-gaokao-latex/`。\n",
        OUTPUT_TARGETS[5]: "# 高考数学 LaTeX 全量状态快照\n\n" + summary + "## 批次明细\n\n" + batches,
    }
    bodies[OUTPUT_TARGETS[3]] += (
        "\n### 本地 OCR 与转录规范\n\n"
        "部署、模型下载、路由、交叉核对、人工校对和阶段提交统一遵循 "
        "[OCR_WORKFLOW.md](docs/OCR_WORKFLOW.md)。首选 Xiaomi-OCR-0，"
        "复杂文档与公式用 PaddleOCR-VL-1.6 交叉验证，批量 PDF 使用 MinerU。"
        "统一入口为 `python3 tools/local_ocr.py --help`；"
        "模型与依赖固定记录在 `tools/ocr-local-models.json`，运行资产放在忽略目录 `.work/ocr-local/`。\n"
    )
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
    paths = {REPORT_SOURCE, MANIFEST_TARGET.as_posix(), ISSUES_TARGET.as_posix()}
    paths.update((BASE / "tools" / name).as_posix() for name in REPORT_DEPENDENCIES)
    paths.update({
        (BASE / "schemas/build-receipt.schema.json").as_posix(),
        (BASE / "schemas/provenance.schema.json").as_posix(),
        (BASE / "schemas/review-receipt.schema.json").as_posix(),
        (BASE / "schemas/source-manifest.schema.json").as_posix(),
    })
    for batch in manifest["batches"]:
        paths.add((BASE / "reports" / f"{batch['batch_id']}.md").as_posix())
    for paper in manifest["papers"]:
        base = BASE / paper["project_dir"]
        paths.update({(base / "provenance.json").as_posix(), (base / "receipts/build.json").as_posix(), (base / "receipts/review.json").as_posix()})
    # 在途批次可能尚无 receipts/review.json 或 reports/<batch>.md（build 完成、review 未
    # 完成的中间态）：每条路径仍逐一经 _sha256 记录（输入追踪完整性），缺失文件记 null
    # （事务约定的「不存在」态），不得让全量报告渲染因他批中间态而整体失败。
    snapshot = {}
    for path in sorted(paths):
        try:
            snapshot[path] = _sha256(root / path)
        except FileNotFoundError:
            snapshot[path] = None
    return snapshot


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
            print("报告输出与全量 manifest 当前一致；未完成状态已在报告中保留")
            return 0
        manifest = _load_json(Path(args.manifest))
        targets = {path: value.encode("utf-8") for path, value in outputs.items()}
        transaction = Transaction(root)
        transaction.prepare("content", targets, _transaction_inputs(root, manifest)).commit()
        drift = check_outputs(outputs, root)
        if drift:
            raise ReportError("写入后报告输出仍不一致：" + "、".join(drift))
        print("已用一个 content 事务写入并回读校验六个全量报告目标")
        return 0
    except (ReportError, OSError, ValueError, build_projects.BuildError, review_receipts.ReviewError) as error:
        print(str(error), file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())

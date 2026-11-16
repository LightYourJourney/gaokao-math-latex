from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "math-gaokao-latex/tools"
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("report", TOOLS / "report.py")
report = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(report)

MANIFEST = ROOT / "math-gaokao-latex/source-manifest.json"
ISSUES = ROOT / "math-gaokao-latex/missing-issues.md"


class ReportFactsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # collect 会全量重算每个 manifest 批次；同一事实快照只读复用即可。
        cls.facts = report.collect_report_facts(MANIFEST, ISSUES)

    def test_collects_conserved_sources_and_full_manifest_paper_states(self):
        facts = self.facts
        self.assertEqual(facts["sources"], {"total": 775, "regular": 734, "spring": 41})
        self.assertGreater(facts["papers"]["total"], 21)
        self.assertEqual(sum(facts["papers"]["states"].values()), facts["papers"]["total"])
        self.assertGreater(facts["papers"]["states"]["blocked"], 0)
        self.assertGreater(facts["current"]["edition_total"], 84)
        self.assertEqual(facts["current"]["editions_compiled"], facts["current"]["edition_total"])

    def test_recomputes_warnings_for_all_available_build_and_review_receipts(self):
        facts = self.facts
        self.assertGreaterEqual(facts["current"]["overfull"], 0)
        self.assertGreaterEqual(facts["current"]["underfull"], 0)
        self.assertGreaterEqual(facts["current"]["warning_exemptions"], 0)

    def test_reports_every_batch_even_when_review_or_ownership_is_incomplete(self):
        facts = self.facts
        self.assertGreater(len(facts["batches"]), 6)
        self.assertEqual(
            len(facts["batches"]), len({row["batch_id"] for row in facts["batches"]})
        )
        self.assertTrue(all(
            row["git_state"] in {"validated", "committed", "unavailable"}
            for row in facts["batches"]
        ))
        # 全库批次可能已全部 FINALIZED；用一条降级副本验证未完成批次仍进入报告，
        # 不依赖 live 仓库恰好存在失败批次。
        incomplete = dict(
            facts["batches"][0], validation="VISUAL_FAILED", git_state="unavailable"
        )
        report_text = report.render_outputs(dict(facts, batches=[incomplete]))[
            "report.md"
        ]
        self.assertIn(
            f"| {incomplete['batch_id']} | {incomplete['paper_count']} | {incomplete['status']}"
            " | VISUAL_FAILED | unavailable |",
            report_text,
        )
        self.assertIn(f"门禁未通过批次：{incomplete['batch_id']}", report_text)

    def test_render_outputs_has_exactly_six_targets(self):
        outputs = report.render_outputs(self.facts)
        self.assertEqual(set(outputs), set(report.OUTPUT_TARGETS))
        self.assertTrue(all(value.endswith("\n") for value in outputs.values()))
        self.assertIn("来源总数：**775**", outputs["math-gaokao-latex/reports/baseline.md"])

    def test_readme_points_to_the_source_manifest_csv_projection(self):
        outputs = report.render_outputs(self.facts)
        readme = outputs["math-gaokao-latex/README.md"]
        self.assertIn("manifest.csv", readme)
        self.assertIn("manifest_csv.py", readme)

    def test_readme_preserves_question_ir_and_ocr_candidate_guidance(self):
        readme = report.render_outputs(self.facts)["math-gaokao-latex/README.md"]
        self.assertIn("### 题目级 IR 导出（增量能力）", readme)
        self.assertIn("python3 tools/export_question_ir.py", readme)
        self.assertIn("python3 tools/ocr_candidate_ir.py", readme)
        self.assertIn("recognized_unverified", readme)

    def test_check_outputs_reports_drifted_targets(self):
        outputs = report.render_outputs(self.facts)
        with tempfile.TemporaryDirectory() as temporary:
            temp_root = Path(temporary)
            for relative, text in outputs.items():
                path = temp_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            self.assertEqual(report.check_outputs(outputs, temp_root), ())
            drifted = report.OUTPUT_TARGETS[0]
            (temp_root / drifted).write_text(outputs[drifted] + "漂移\n", encoding="utf-8")
            self.assertEqual(report.check_outputs(outputs, temp_root), (drifted,))


class ReportCurrentScopeContractTest(unittest.TestCase):
    def test_resolved_blocking_issues_do_not_count_as_open_completion_blockers(self):
        result = report._issue_summary([
            {"status": "open", "impact": "blocks_completion"},
            {"status": "resolved", "impact": "blocks_completion"},
            {"status": "open", "impact": "non_blocking"},
        ])

        self.assertEqual(result, {"total": 3, "open": 2, "resolved": 1, "blocks_completion": 1})

    def test_render_includes_incomplete_current_corpus_without_relabeling_it_as_stage_zero(self):
        facts = {
            "sources": {"total": 3, "regular": 2, "spring": 1, "states": {"ready": 3}},
            "papers": {"total": 2, "states": {"complete": 1, "blocked": 1}},
            "batches": [
                {"batch_id": "phase0-b01", "status": "closed", "validation": "FINALIZED", "git_state": "committed", "paper_count": 1},
                {"batch_id": "phase2-b04", "status": "compiled_pending_review", "validation": "INVALID_OR_STALE", "git_state": "validated", "paper_count": 1},
            ],
            "current": {
                "build_states": {"succeeded": 1, "compiled_pending_review": 1},
                "review_states": {"passed": 1, "pending": 1},
                "edition_total": 8,
                "editions_compiled": 8,
                "missing_builds": 0,
                "invalid_builds": 0,
                "missing_reviews": 0,
                "invalid_reviews": 0,
                "overfull": 0,
                "underfull": 1,
                "warning_exemptions": 1,
            },
            "issues": {"total": 2, "open": 1, "resolved": 1, "blocks_completion": 1},
        }

        outputs = report.render_outputs(facts)
        inventory = outputs["docs/source-inventory.md"]
        project = outputs["math-gaokao-latex/README.md"]
        full_report = outputs["report.md"]

        self.assertIn("来源总数：**3**", inventory)
        self.assertIn("试卷总数：**2**", project)
        self.assertIn("已编译版本：8/8", project)
        self.assertIn("review 回执状态：passed 1，pending 1", project)
        self.assertIn("回执日志警告汇总", full_report)
        self.assertNotIn("当前警告", full_report)
        self.assertIn("门禁未通过批次：phase2-b04", full_report)
        self.assertIn("未解决问题：1", full_report)
        self.assertNotIn("阶段 0 的机器事实", full_report)

class ReportTransactionInputsTest(unittest.TestCase):
    def test_tracks_every_batch_and_paper_artifact_in_the_full_report_snapshot(self):
        manifest = {
            "batches": [
                {"batch_id": "phase0-b01", "paper_ids": ["historical"]},
                {"batch_id": "phase1-b07", "paper_ids": ["new-paper"]},
            ],
            "papers": [
                {"paper_id": "historical", "legacy_ids": ["legacy"], "project_dir": "historical"},
                {"paper_id": "new-paper", "legacy_ids": [], "project_dir": "new-paper"},
            ],
        }
        seen = []

        def digest(path):
            seen.append(path.relative_to(ROOT).as_posix())
            return "digest"

        with mock.patch.object(report, "_sha256", side_effect=digest):
            report._transaction_inputs(ROOT, manifest)
        self.assertIn("math-gaokao-latex/reports/phase0-b01.md", seen)
        self.assertIn("math-gaokao-latex/reports/phase1-b07.md", seen)
        self.assertIn("math-gaokao-latex/new-paper/provenance.json", seen)
        self.assertIn("math-gaokao-latex/new-paper/receipts/build.json", seen)
        self.assertIn("math-gaokao-latex/new-paper/receipts/review.json", seen)
        self.assertIn("math-gaokao-latex/tools/review_receipts.py", seen)

    def test_does_not_reject_a_batch_containing_legacy_and_new_papers(self):
        manifest = {
            "batches": [{"batch_id": "mixed", "paper_ids": ["historical", "new-paper"]}],
            "papers": [
                {"paper_id": "historical", "legacy_ids": ["legacy"], "project_dir": "historical"},
                {"paper_id": "new-paper", "legacy_ids": [], "project_dir": "new-paper"},
            ],
        }
        with mock.patch.object(report, "_sha256", return_value="digest"):
            report._transaction_inputs(ROOT, manifest)


class ReportCliTest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(TOOLS / "report.py"), *args], cwd=ROOT, text=True, capture_output=True)

    def test_all_is_required(self):
        result = self.run_cli("check", "--manifest", str(MANIFEST), "--issues", str(ISSUES))
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()

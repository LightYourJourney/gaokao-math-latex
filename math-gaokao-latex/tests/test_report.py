from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[4]
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
        # collect 会全量重算六批门禁，代价高；同一事实快照只读复用即可。
        cls.facts = report.collect_report_facts(MANIFEST, ISSUES)

    def test_collects_conserved_sources_and_two_status_denominators(self):
        facts = self.facts
        self.assertEqual(facts["sources"], {"total": 775, "regular": 734, "spring": 41})
        self.assertEqual(facts["legacy"]["papers"], 21)
        self.assertEqual(facts["current"]["builds_succeeded"], 84)
        self.assertEqual(sum(facts["current"]["statuses"].values()), 21)
        self.assertGreater(facts["current"]["statuses"]["blocked"], 0)
        self.assertEqual(facts["current"]["statuses"]["complete"] + facts["current"]["statuses"]["blocked"] + facts["current"]["statuses"]["in_progress"], 21)

    def test_recomputes_current_warning_counts_without_forging_legacy(self):
        facts = self.facts
        self.assertEqual(facts["legacy"]["overfull"], 1)
        self.assertEqual(facts["current"]["overfull"], 0)
        self.assertEqual(facts["current"]["underfull"], 13)
        self.assertEqual(facts["current"]["warning_exemptions"], 13)

    def test_all_batches_are_current_and_committed(self):
        facts = self.facts
        self.assertEqual(len(facts["batches"]), 6)
        self.assertTrue(all(row["validation"] == "FINALIZED" for row in facts["batches"]))
        self.assertTrue(all(row["git_state"] == "committed" for row in facts["batches"]))

    def test_render_outputs_has_exactly_six_targets(self):
        outputs = report.render_outputs(self.facts)
        self.assertEqual(set(outputs), set(report.OUTPUT_TARGETS))
        self.assertTrue(all(value.endswith("\n") for value in outputs.values()))
        self.assertIn("775 = 734 + 41", outputs["math-gaokao-latex/reports/baseline.md"])

    def test_readme_points_to_the_source_manifest_csv_projection(self):
        outputs = report.render_outputs(self.facts)
        readme = outputs["math-gaokao-latex/README.md"]
        self.assertIn("manifest.csv", readme)
        self.assertIn("manifest_csv.py", readme)

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


class ReportTransactionInputsTest(unittest.TestCase):
    def test_ignores_incomplete_nonhistorical_artifacts(self):
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
        self.assertNotIn("math-gaokao-latex/reports/phase1-b07.md", seen)
        self.assertFalse(any("new-paper" in path for path in seen))

    def test_rejects_mixed_historical_and_nonhistorical_batch(self):
        manifest = {
            "batches": [
                {"batch_id": "mixed", "paper_ids": ["historical", "new-paper"]},
            ],
            "papers": [
                {"paper_id": "historical", "legacy_ids": ["legacy"], "project_dir": "historical"},
                {"paper_id": "new-paper", "legacy_ids": [], "project_dir": "new-paper"},
            ],
        }
        with self.assertRaisesRegex(report.ReportError, "不允许混合历史卷与非历史卷"):
            report._transaction_inputs(ROOT, manifest)


class ReportCliTest(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(TOOLS / "report.py"), *args], cwd=ROOT, text=True, capture_output=True)

    def test_all_is_required(self):
        result = self.run_cli("check", "--manifest", str(MANIFEST), "--issues", str(ISSUES))
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()

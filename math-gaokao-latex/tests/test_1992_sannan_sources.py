"""1992三南卷固定来源与题面结构检查；不代表独立审题通过。"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_三南卷"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Sannan1992SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.draft = (PROJECT / "题面转录草稿.md").read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.draft)
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_fixed_manifest_identity_and_source_binding_are_unchanged(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(s for s in manifest["sources"] if s["source_id"] == self.record["source_id"])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(hashlib.sha256((PROJECT / "题面转录草稿.md").read_bytes()).hexdigest(),
                         self.record["draft_sha256"])

    def test_all_28_questions_are_contiguous_with_stable_source_ids(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 29)))
        refs = self.record["question_sources"]
        self.assertEqual([r["question_number"] for r in refs], list(range(1, 29)))
        self.assertEqual([r["question_id"] for r in refs],
                         [f"1992-sannan-q{i:03d}" for i in range(1, 29)])
        self.assertTrue(all(r["source_page"] == 1 for r in refs))
        self.assertEqual(self.record["question_count"], 28)
        self.assertEqual(self.record["page_map"][0]["printed_page"], "44")
        self.assertEqual(self.record["page_map"][0]["columns"], ["1—10", "11—23", "24—28"])
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 17},
            {"type": "fill-in", "first": 18, "last": 23},
            {"type": "solution", "first": 24, "last": 28},
        ])

    def test_all_choices_are_present_and_math_delimiters_are_balanced(self):
        for question in self.questions[:17]:
            for letter in "ABCD":
                self.assertEqual(question.body.count("（" + letter + "）"), 1,
                                 f"question {question.number}, option {letter}")
        self.assertEqual(self.draft.count("$") % 2, 0)
        self.assertEqual(self.draft.count(r"\begin{cases}"),
                         self.draft.count(r"\end{cases}"))

    def test_high_risk_original_notation_and_endpoints_are_preserved(self):
        by_number = {q.number: q.body for q in self.questions}
        self.assertIn(r"\arg z", by_number[1])
        self.assertIn(r"-\dfrac{4\pi}{3}", by_number[1])
        self.assertIn(r"\sqrt{x^2}>2", by_number[13])
        self.assertIn(r"\log_x7>\log_3 7", by_number[13])
        self.assertIn(r"2a^{2x-2}-7a^{x-1}+3=0", by_number[24])
        self.assertIn(r"4\sqrt{10}", by_number[27])
        self.assertIn(r"1<z+\dfrac{10}{z}\le6", by_number[28])

    def test_answers_scores_and_figures_are_not_fabricated_as_source_content(self):
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["question_figures_pending"], [])
        self.assertEqual(self.record["figure_files"], [])
        self.assertEqual(self.record["generated_solution"]["attribution"], "agent-derived-non-official")
        self.assertEqual(self.record["generated_solution"]["status"], "pending-independent-review")
        self.assertEqual([n["question_number"] for n in self.record["review_notes"]], [1])
        self.assertIn("同终边", self.record["review_notes"][0]["note"])

    def test_only_native_text_and_ignored_render_are_claimed(self):
        self.assertEqual(self.record["text_analysis"]["classification"], "text_layer_candidate")
        self.assertEqual(self.record["text_analysis"]["ocr_calls"], 0)
        self.assertEqual(self.record["text_analysis"]["selected_pages_for_ocr"], [])
        render = self.record["render"]
        self.assertEqual(render["page"], 1)
        self.assertEqual(render["dimensions_px"], [1985, 1404])
        render_path = Path(render["path"])
        self.assertFalse(render_path.is_absolute())
        self.assertEqual(render_path.parts[0], ".work")
        self.assertRegex(render["sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()

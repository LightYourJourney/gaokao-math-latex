"""Source intake checks; not an answer or authenticity certification."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_全国卷_理科"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class NationalScience1992SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "题面转录草稿.md").read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.text)
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_source_identity_and_draft_hash(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(s for s in manifest["sources"] if s["source_id"] == self.record["source_id"])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(hashlib.sha256((PROJECT / "题面转录草稿.md").read_bytes()).hexdigest(),
                         self.record["draft_sha256"])

    def test_continuous_28_questions_and_only_printed_subparts(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 29)))
        self.assertEqual({q.number: q.subparts for q in self.questions if q.subparts}, {27: (1, 2)})
        self.assertEqual(self.record["question_count"], 28)
        self.assertEqual(self.record["page_map"][0]["printed_page"], "42")
        self.assertEqual(len(self.record["page_map"][0]["columns"]), 3)

    def test_18_choices_have_four_options_and_math_delimiters(self):
        for question in self.questions[:18]:
            for letter in "ABCD":
                self.assertEqual(question.body.count("（" + letter + "）"), 1)
        self.assertEqual(self.text.count("$") % 2, 0)
        self.assertEqual(self.text.count(r"\begin{cases}"), self.text.count(r"\end{cases}"))

    def test_q16_source_error_is_preserved_instead_of_invented_correction(self):
        body = self.questions[15].body
        self.assertIn(r"\dfrac{e^x-e^x}{2}", body.split("\n\n")[0])
        self.assertIn("不擅改", body)
        issues = self.record["source_issues"]
        self.assertEqual([r["question_number"] for r in issues], [16, 26])
        self.assertEqual(issues[0]["category"], "suspected-source-error")
        self.assertEqual(issues[0]["status"], "needs-review")

    def test_q26_endpoint_assignment_ambiguity_is_not_hidden(self):
        q26 = self.questions[25].body
        self.assertIn(r"A_1E=m", q26)
        self.assertIn(r"AF=n", q26)
        issue = self.record["source_issues"][1]
        self.assertEqual(issue["question_number"], 26)
        self.assertEqual(issue["category"], "notation-ambiguity")
        self.assertEqual(issue["status"], "needs-review")
        self.assertIn("未明确", issue["issue"])

    def test_q24_both_conjugates_and_q19_negative_exponent_preserved(self):
        self.assertEqual(self.questions[23].body.count(r"\overline z"), 2)
        self.assertIn(r"z\overline z-3i\overline z=1+3i", self.questions[23].body)
        self.assertIn(r"\dfrac{1+3^{-x}}{1+3^x}=3", self.questions[18].body)
        self.assertEqual(self.record["confirmed_high_risk_details"][0]["question_number"], 24)

    def test_unavailable_scores_answers_and_figures_are_not_claimed(self):
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "independently-reviewed")
        pending = [q.number for q in self.questions if "题图待重绘" in q.body]
        self.assertEqual(pending, [])
        self.assertEqual(pending, self.record["question_figures_pending"])

    def test_vector_figure_hashes_links_and_no_raster_dependencies(self):
        figures = self.record["figure_files"]
        self.assertEqual([f["question_number"] for f in figures], [6, 14])
        for f in figures:
            file = PROJECT / f["path"]
            self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), f["sha256"])
            target = "../math-gaokao-latex/1992_全国卷_理科/" + f["path"]
            self.assertEqual((ROOT.parent / "1992" / target).resolve(), file.resolve())
            self.assertEqual(self.questions[f["question_number"] - 1].body.count(f"]({target})"), 1)
            text = file.read_text(encoding="utf-8")
            self.assertEqual(text.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(text.count(r"\end{tikzpicture}"), 1)
            for command in (r"\includegraphics", r"\input", r"\write18", r"\documentclass"):
                self.assertNotIn(command, text)

    def test_text_layer_is_a_candidate_even_without_suspicious_characters(self):
        analysis = self.record["text_analysis"]
        self.assertEqual(analysis["classification"], "text_layer_candidate")
        self.assertEqual(analysis["ocr_calls"], 0)
        self.assertTrue(analysis["requires_content_review"])
        self.assertEqual(analysis["resume_check"]["hits"], 1)
        self.assertEqual(analysis["resume_check"]["misses"], 0)
        for key in (analysis["cache_path"], self.record["render"]["path"]):
            path = Path(key)
            self.assertFalse(path.is_absolute())
            self.assertNotIn("..", path.parts)
            self.assertEqual(path.parts[0], ".work")

    def test_conflicting_alternate_sources_do_not_silently_override_conditions(self):
        alternate = json.loads((PROJECT / "另版核源.json").read_text(encoding="utf-8"))
        self.assertEqual(alternate["fixed_pdf_sha256"], self.record["pdf_sha256"])
        self.assertEqual(self.record["alternate_review"]["sha256"],
                         hashlib.sha256((PROJECT / "另版核源.json").read_bytes()).hexdigest())
        self.assertEqual(alternate["source_id"], self.record["source_id"])
        self.assertEqual(alternate["status"], "unresolved-conflicting-secondary-sources")
        for key in ("accepted_correction", "accepted_scores", "accepted_official_answer"):
            self.assertIsNone(alternate[key])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["generated_solution"]["choice_key"][15], None)
        self.assertIn(r"\dfrac{e^x-e^x}{2}", self.questions[15].body)
        candidates = alternate["candidates"]
        self.assertEqual(len(candidates), 3)
        self.assertTrue(all(not c["publisher_authority_verified"] for c in candidates))
        self.assertEqual(candidates[0]["q16_formula"], "y=(e^x+e^{-x})/2")
        self.assertEqual(candidates[0]["disposition"], "rejected-for-correction")

    def test_unreadable_browser_preview_is_not_mathematical_evidence(self):
        alternate = json.loads((PROJECT / "另版核源.json").read_text(encoding="utf-8"))
        preview = alternate["candidates"][1]
        self.assertIsNone(preview["q16_formula"])
        self.assertTrue(preview["browser_tab_closed"])
        self.assertEqual(preview["disposition"], "unreadable-formula-and-content-conflict")
        self.assertTrue(preview["screenshot_path"].startswith("/tmp/"))
        self.assertRegex(preview["screenshot_sha256"], r"^[0-9a-f]{64}$")
        self.assertFalse(self.record["canonical_question_source_ready"])


if __name__ == "__main__":
    unittest.main()

"""Source-bound checks for the 1993 old-track science transcription."""
import hashlib
import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1993_旧科目组_理科"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
CONVERTER_TOOLS = ROOT.parent / "math-gaokao-2017-2026" / "tools"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(CONVERTER_TOOLS))
import solution_sources
import md2tex


class OldTrackScience1993SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if DRAFT.is_file():
            cls.text = DRAFT.read_text(encoding="utf-8")
            cls.questions = solution_sources.parse_question_blocks(cls.text)
        else:
            cls.text = ""
            cls.questions = []
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}

    def test_fixed_source_transcription_has_all_29_numbered_questions(self):
        self.assertTrue(DRAFT.is_file(), "1993 old-track science transcription is missing")
        self.assertEqual([q.number for q in self.questions], list(range(1, 30)))
        self.assertEqual(self.record.get("question_count"), 29)

    def test_each_question_has_a_stable_id_and_printed_page_column(self):
        references = self.record["question_sources"]
        self.assertEqual([item["question_number"] for item in references], list(range(1, 30)))
        self.assertEqual(
            [item["question_id"] for item in references],
            [f"1993-old-science-q{number:03d}" for number in range(1, 30)],
        )
        self.assertEqual([item["source_page"] for item in references], [1] * 29)
        self.assertEqual(
            [item["column"] for item in references],
            [1] * 10 + [2] * 15 + [3] * 4,
        )

    def test_source_identity_and_draft_hash_match_the_fixed_manifest(self):
        self.assertTrue(RECORD.is_file(), "source record is missing")
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(
            s for s in manifest["sources"]
            if s["source_id"] == "src-cb514fd810e6a797f6e968a2009a69f8d5b9b570e257d44b4a1bd517657646ff"
        )
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())

    def test_question_ranges_and_unprovided_answers_remain_uninvented(self):
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 18},
            {"type": "fill-in", "first": 19, "last": 25},
            {"type": "solution", "first": 26, "last": 29},
        ])
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")

    def test_source_sensitive_formulas_and_suspected_original_issue_are_preserved(self):
        self.assertIn(r"z=-\dfrac{1-i}{\sqrt2}", self.questions[3].body)
        self.assertIn(r"\dfrac{2}{2^x-1}", self.questions[7].body)
        self.assertIn(r"0\le t\le5", self.questions[8].body)
        self.assertIn(r"\left(\dfrac\ell6\right)^3\pi", self.questions[13].body)
        self.assertIn(r"(\sqrt3x+\sqrt[3]2)^{100}", self.questions[14].body)
        self.assertIn(r"3a=4b=6c", self.questions[15].body)
        self.assertIn(r"\dfrac2a+\dfrac2b", self.questions[15].body)
        self.assertIn(r"\sum_{i=1}^{n}\dfrac1{a_i a_{i+1}}", self.questions[23].body)
        self.assertIn(r"\log_{\frac12}(5-x)", self.questions[24].body)
        self.assertIn(r"(\overline z)^4", self.questions[27].body)
        self.assertIn(r"2|a|<4+b", self.questions[28].body)
        self.assertEqual([issue["question_number"] for issue in self.record["source_issues"]], [8, 16])
        self.assertTrue(all(issue["status"] == "needs-review" for issue in self.record["source_issues"]))

    def test_prism_redraw_is_hash_verified_and_strict_conversion_resolves_its_link(self):
        relative = "figures/f1993_old_science_q26_prism.tex"
        figure = PAPER / relative
        metadata = self.record["figure_files"][0]
        self.assertEqual(metadata["question_number"], 26)
        self.assertEqual(metadata["path"], relative)
        self.assertEqual(hashlib.sha256(figure.read_bytes()).hexdigest(), metadata["sha256"])
        reuse = metadata["reuse_of"]
        prior_figure = ROOT / reuse["paper"] / reuse["path"]
        self.assertEqual(hashlib.sha256(prior_figure.read_bytes()).hexdigest(), reuse["sha256"])
        self.assertIn(relative, self.questions[25].body)
        source = figure.read_text(encoding="utf-8")
        self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
        self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
        for forbidden in (r"\includegraphics", r"\write18", r"\documentclass"):
            self.assertNotIn(forbidden, source)

        target = "../math-gaokao-latex/1993_旧科目组_理科/" + relative
        result = md2tex.convert_markdown(
            self.text,
            md2tex.ConversionContext(
                figure_map={target: "f1993_old_science_q26_prism"}, strict=True
            ),
        )
        self.assertEqual(result.warnings, ())
        self.assertEqual(result.referenced_figures, ("f1993_old_science_q26_prism",))
        self.assertEqual(
            result.text.count(r"\input{figures/f1993_old_science_q26_prism}"), 1
        )


if __name__ == "__main__":
    unittest.main()

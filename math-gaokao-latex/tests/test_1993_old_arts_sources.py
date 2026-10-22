"""Source-bound transcription checks for the 1993 old-track arts paper."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1993_旧科目组_文科"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
CONVERTER_TOOLS = ROOT.parent / "math-gaokao-2017-2026" / "tools"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(CONVERTER_TOOLS))
import solution_sources
import md2tex


class OldTrackArts1993SourceTests(unittest.TestCase):
    def test_source_transcription_is_a_full_numbered_sequence(self):
        self.assertTrue(DRAFT.is_file(), "1993 old-track arts transcription is missing")
        self.assertTrue(RECORD.is_file(), "1993 old-track arts source record is missing")

        text = DRAFT.read_text(encoding="utf-8")
        questions = solution_sources.parse_question_blocks(text)
        record = json.loads(RECORD.read_text(encoding="utf-8"))

        self.assertEqual([q.number for q in questions], list(range(1, 30)))
        self.assertEqual(record["question_count"], 29)
        self.assertEqual(record["source_id"], "src-0a960477fc7d186c82e4c8cfd17a60ff77947338db3fb5ab6f57fd4446e71924")
        self.assertEqual(record["page_map"][0]["printed_page"], "48")

    @classmethod
    def setUpClass(cls):
        cls.text = DRAFT.read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.text)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_source_identity_and_draft_hash_match_the_fixed_manifest(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(s for s in manifest["sources"] if s["source_id"] == self.record["source_id"])
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "gk-1993-old-arts")
        self.assertEqual(source["paper_relation"], "canonical")
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())

    def test_question_type_ranges_and_source_answers_are_not_invented(self):
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 18},
            {"type": "fill-in", "first": 19, "last": 26},
            {"type": "solution", "first": 27, "last": 29},
        ])
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["paper_id"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")

    def test_source_sensitive_formulas_and_unresolved_wording_remain_visible(self):
        self.assertIn(r"\sqrt3x+\sqrt[3]2", self.questions[14].body)
        self.assertIn(r"\dfrac{8n}{(2n-1)^2(2n+1)^2}", self.questions[25].body)
        self.assertIn(r"(\overline z)^4", self.questions[28].body)
        self.assertIn("直径分为两段", self.questions[8].body)
        self.assertIn(r"x\ne0", self.questions[7].body)
        self.assertEqual([issue["question_number"] for issue in self.record["source_issues"]], [8, 9])
        self.assertTrue(all(issue["status"] == "needs-review" for issue in self.record["source_issues"]))

    def test_both_printed_diagrams_are_linked_and_hash_verified_vector_sources(self):
        expected = {
            18: "figures/f1993_old_arts_q18_cube.tex",
            27: "figures/f1993_old_arts_q27_prism.tex",
        }
        figures = {item["question_number"]: item for item in self.record["figure_files"]}
        self.assertEqual(set(figures), set(expected))
        self.assertEqual(self.record["question_figures_pending"], [])
        for number, relative in expected.items():
            figure = PAPER / relative
            metadata = figures[number]
            self.assertEqual(metadata["path"], relative)
            self.assertEqual(hashlib.sha256(figure.read_bytes()).hexdigest(), metadata["sha256"])
            self.assertIn(relative, self.questions[number - 1].body)
            source = figure.read_text(encoding="utf-8")
            self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
            for forbidden in (r"\includegraphics", r"\write18", r"\documentclass"):
                self.assertNotIn(forbidden, source)

    def test_strict_markdown_conversion_resolves_both_local_tex_figures(self):
        targets = [
            "../math-gaokao-latex/1993_旧科目组_文科/figures/f1993_old_arts_q18_cube.tex",
            "../math-gaokao-latex/1993_旧科目组_文科/figures/f1993_old_arts_q27_prism.tex",
        ]
        slugs = ["f1993_old_arts_q18_cube", "f1993_old_arts_q27_prism"]
        result = md2tex.convert_markdown(
            self.text,
            md2tex.ConversionContext(
                figure_map=dict(zip(targets, slugs)), strict=True
            ),
        )

        self.assertEqual(result.warnings, ())
        self.assertEqual(result.referenced_figures, tuple(slugs))
        for slug in slugs:
            self.assertEqual(result.text.count(r"\input{figures/" + slug + "}"), 1)


if __name__ == "__main__":
    unittest.main()

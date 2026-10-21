"""Source-bound transcription checks for the 1993 new-track arts paper."""
import hashlib
import json
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1993_新科目组_文科"
DRAFT = PAPER / "题面转录草稿.md"
SOLUTIONS = PAPER / "解答草稿.md"
RECORD = PAPER / "来源校对.json"
CONVERTER_TOOLS = ROOT.parent / "math-gaokao-2017-2026" / "tools"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(CONVERTER_TOOLS))
import solution_sources
import md2tex


class NewTrackArts1993SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DRAFT.read_text(encoding="utf-8")
        cls.solution_text = SOLUTIONS.read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.text)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_source_is_a_full_28_question_transcription(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 29)))
        self.assertEqual(self.record["question_count"], 28)
        self.assertEqual(self.record["page_map"][0]["printed_page"], "46")
        self.assertEqual(
            self.record["question_type_ranges"],
            [
                {"type": "single-choice", "first": 1, "last": 17},
                {"type": "fill-in", "first": 18, "last": 23},
                {"type": "solution", "first": 24, "last": 28},
            ],
        )
        self.assertEqual(
            [item["question_number"] for item in self.record["question_sources"]],
            list(range(1, 29)),
        )
        self.assertEqual(
            [q for q in self.record["question_sources"] if q["column"] == 1][-1]["question_number"],
            12,
        )
        self.assertEqual(
            [q for q in self.record["question_sources"] if q["column"] == 2][0]["question_number"],
            13,
        )
        self.assertEqual(
            [q for q in self.record["question_sources"] if q["column"] == 3][0]["question_number"],
            24,
        )

    def test_source_identity_and_artifact_hash_match_the_fixed_manifest(self):
        manifest = json.loads(
            (ROOT / "source-manifest.json").read_text(encoding="utf-8")
        )
        source = next(
            s for s in manifest["sources"] if s["source_id"] == self.record["source_id"]
        )
        self.assertEqual(
            self.record["source_id"],
            "src-3c9130a8330fea27cd218b212fb8cd30d26545b82ee8c080d5c2060770f6d5d5",
        )
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["upstream_path"], self.record["upstream_path"])
        self.assertEqual(
            self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest()
        )
        self.assertEqual(
            self.record["generated_solution"]["sha256"],
            hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest(),
        )

    def test_blind_review_receipt_binds_inputs_and_keeps_open_gates(self):
        review = self.record.get("independent_blind_review")
        self.assertIsInstance(review, dict)
        self.assertEqual(review.get("status"), "reviewed-with-open-issues")
        self.assertEqual(review.get("reviewers"), 1)
        self.assertEqual(review.get("reviewed_question_numbers"), list(range(1, 29)))
        self.assertEqual(
            review.get("independently_solved_question_numbers"), list(range(1, 29))
        )
        self.assertEqual(
            review.get("verified_answer_question_numbers"),
            [n for n in range(1, 29) if n != 21],
        )
        self.assertEqual(review.get("conditional_interpretation_question_numbers"), [21])
        self.assertEqual(review.get("transcription_discrepancy_question_numbers"), [])
        self.assertEqual(review.get("reviewer_correction_question_numbers"), [15])
        self.assertEqual(review.get("source_pdf_sha256"), self.record["pdf_sha256"])
        self.assertEqual(review.get("source_render_sha256"), self.record["render"]["sha256"])
        self.assertEqual(review.get("question_draft_sha256"), self.record["draft_sha256"])
        solution_sha = hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest()
        self.assertEqual(review.get("solution_draft_sha256"), solution_sha)
        self.assertEqual(review.get("current_solution_draft_sha256"), solution_sha)
        report_path = review.get("report_path")
        self.assertIsInstance(report_path, str)
        self.assertFalse(Path(report_path).is_absolute())
        report = PAPER / report_path
        self.assertTrue(report.is_file())
        self.assertEqual(
            hashlib.sha256(report.read_bytes()).hexdigest(), review.get("report_sha256")
        )
        self.assertEqual(
            self.record["generated_solution"]["status"],
            "independently-reviewed-with-open-issues",
        )
        self.assertEqual(self.record["mathematical_verification_status"], "independently-reviewed")
        self.assertEqual(self.record["transcription_status"], "transcribed-independently-reviewed")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertIsNone(self.record["paper_id"])
        self.assertIsNone(self.record["official_answer"])

    def test_unprinted_answers_are_not_claimed_as_official(self):
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(
            self.record["mathematical_verification_status"], "independently-reviewed"
        )
        self.assertEqual(
            self.record["generated_solution"]["attribution"],
            "agent-derived-non-official",
        )
        self.assertEqual(
            self.record["generated_solution"]["status"],
            "independently-reviewed-with-open-issues",
        )
        self.assertEqual(
            self.record["generated_solution"]["question_numbers"], list(range(1, 29))
        )

    def test_source_sensitive_formulas_and_conditionals_are_preserved(self):
        self.assertIn(r"(\sqrt{x}+1)^4(x-1)^5", self.questions[12].body)
        self.assertIn(r"\dfrac32", self.questions[13].body)
        self.assertIn(r"\dfrac{1-a^{n+1}}{1+a^{n-1}}", self.questions[18].body)
        self.assertIn(r"\log_a\dfrac{1+x}{1-x}", self.questions[24].body)
        self.assertIn(r"\tan\angle MNP=-2", self.questions[27].body)
        self.assertIn("使 $AE$ 与 $BE$ 重合", self.questions[22].body)

    def test_diagram_is_linked_and_hash_verified_vector_source(self):
        expected = "figures/f1993_new_arts_q23_fold.tex"
        entries = self.record["figure_files"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["question_number"], 23)
        self.assertEqual(entries[0]["path"], expected)
        figure = PAPER / expected
        self.assertEqual(
            hashlib.sha256(figure.read_bytes()).hexdigest(), entries[0]["sha256"]
        )
        self.assertIn(expected, self.questions[22].body)
        source = figure.read_text(encoding="utf-8")
        self.assertEqual(source.count(r"\begin{tikzpicture}"), 1)
        self.assertEqual(source.count(r"\end{tikzpicture}"), 1)
        for forbidden in (r"\includegraphics", r"\write18", r"\documentclass"):
            self.assertNotIn(forbidden, source)
        self.assertEqual(self.record["question_figures_pending"], [])
        self.assertFalse(
            [
                path
                for path in PAPER.rglob("*")
                if path.is_file()
                and ".work" not in path.parts
                and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
            ]
        )

    def test_all_generated_answers_and_key_steps_are_present(self):
        questions = self.record["generated_solution"]["choice_key"]
        self.assertEqual(
            questions,
            ["A", "C", "B", "B", "A", "D", "C", "A", "B", "D", "C", "A", "D", "D", "A", "C", "B"],
        )
        for fragment in (
            r"7\pi/3",
            r"\dfrac{\sqrt3+2\sqrt2}{6}",
            r"1-\dfrac1{(2n+1)^2}",
            r"\frac{\sqrt3}{2}",
            r"\frac{x^2}{15/4}+\frac{y^2}{3}=1",
        ):
            self.assertIn(fragment, self.solution_text)
        self.assertEqual(
            self.record["generated_solution"]["fill_in_answers"],
            {
                "18": r"\dfrac{\sqrt3+2\sqrt2}{6}",
                "19": "-a^2",
                "20": "100",
                "21": "1",
                "22": "1760",
                "23": r"30^\circ",
            },
        )
        self.assertEqual(
            [int(number) for number in re.findall(r"^\*\*(\d+)．\*\*", self.solution_text, re.M)],
            list(range(1, 29)),
        )

    def test_strict_markdown_conversion_resolves_the_local_tex_figure(self):
        target = "../math-gaokao-latex/1993_新科目组_文科/figures/f1993_new_arts_q23_fold.tex"
        slug = "f1993_new_arts_q23_fold"
        result = md2tex.convert_markdown(
            self.text,
            md2tex.ConversionContext(figure_map={target: slug}, strict=True),
        )
        self.assertEqual(result.warnings, ())
        self.assertEqual(result.referenced_figures, (slug,))
        self.assertEqual(result.text.count(r"\input{figures/" + slug + "}"), 1)


if __name__ == "__main__":
    unittest.main()

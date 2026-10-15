"""Source-bound transcription checks for the 1993 new-track science paper."""
import hashlib
import json
import re
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1993_新科目组_理科"
DRAFT = PAPER / "题面转录草稿.md"
SOLUTIONS = PAPER / "解答草稿.md"
RECORD = PAPER / "来源校对.json"
CONVERTER_TOOLS = ROOT.parent / "math-gaokao-2017-2026" / "tools"
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(CONVERTER_TOOLS))
import solution_sources
import md2tex


class NewTrackScience1993SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DRAFT.read_text(encoding="utf-8")
        cls.solution_text = SOLUTIONS.read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.text)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))

    def test_source_is_a_full_28_question_transcription_with_three_columns(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 29)))
        self.assertEqual(self.record["question_count"], 28)
        self.assertEqual(self.record["page_map"][0]["printed_page"], "45")
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
            [q["question_number"] for q in self.record["question_sources"] if q["column"] == 1][-1],
            9,
        )
        self.assertEqual(
            [q["question_number"] for q in self.record["question_sources"] if q["column"] == 2][0],
            10,
        )
        self.assertEqual(
            [q["question_number"] for q in self.record["question_sources"] if q["column"] == 3][0],
            19,
        )

    def test_source_identity_and_artifact_hash_match_the_fixed_manifest(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(
            s for s in manifest["sources"] if s["source_id"] == self.record["source_id"]
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

    def test_unprinted_answers_are_not_claimed_as_official(self):
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(
            self.record["generated_solution"]["attribution"], "agent-derived-non-official"
        )
        self.assertEqual(
            self.record["generated_solution"]["status"], "pending-independent-review"
        )
        self.assertEqual(
            self.record["generated_solution"]["question_numbers"], list(range(1, 29))
        )

    def test_source_sensitive_formulas_and_ambiguous_arg_are_preserved(self):
        self.assertIn(r"\rho=\dfrac4{3-5\cos\theta}", self.questions[3].body)
        self.assertIn(r"\cos\dfrac\theta2+\sin\dfrac\theta2", self.questions[8].body)
        self.assertIn(r"\dfrac{x^2}{9k^2}-\dfrac{y^2}{4k^2}=1", self.questions[18].body)
        self.assertIn(r"\omega=\dfrac{1-(\overline z)^4}{1+z^4}", self.questions[27].body)
        issue = self.record["source_issues"][0]
        self.assertEqual(issue["category"], "argument-convention")
        self.assertEqual(issue["question_number"], 28)
        self.assertEqual(issue["status"], "needs-review")
        self.assertIn("arg", issue["note"])

    def test_shared_question_stems_map_to_the_arts_paper_without_retranscription_drift(self):
        arts = ROOT / "1993_新科目组_文科" / "题面转录草稿.md"
        arts_questions = {
            q.number: q
            for q in solution_sources.parse_question_blocks(
                arts.read_text(encoding="utf-8")
            )
        }
        science_questions = {q.number: q for q in self.questions}
        shared_map = {
            **{n: n for n in range(1, 4)},
            **{n: n for n in range(5, 9)},
            **{n: n for n in range(10, 19)},
            **{n: n for n in range(20, 24)},
            24: 25,
            25: 26,
            26: 27,
            27: 28,
        }
        for science_number, arts_number in shared_map.items():
            science_body = science_questions[science_number].body
            arts_body = arts_questions[arts_number].body
            science_body = re.sub(r"\[第23题折叠正方形示意图\]\([^)]+\)", "", science_body)
            arts_body = re.sub(r"\[第23题折叠正方形示意图\]\([^)]+\)", "", arts_body)
            science_body = re.sub(r"\s+", "", science_body)
            arts_body = re.sub(r"\s+", "", arts_body)
            self.assertEqual(science_body, arts_body, (science_number, arts_number))

    def test_diagram_is_linked_and_hash_verified_vector_source(self):
        expected = "figures/f1993_new_science_q23_fold.tex"
        entries = self.record["figure_files"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["question_number"], 23)
        self.assertEqual(entries[0]["path"], expected)
        self.assertEqual(
            entries[0]["reused_from"],
            "../1993_新科目组_文科/figures/f1993_new_arts_q23_fold.tex",
        )
        figure = PAPER / expected
        self.assertEqual(hashlib.sha256(figure.read_bytes()).hexdigest(), entries[0]["sha256"])
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

    def test_generated_answers_and_all_solution_blocks_are_present(self):
        self.assertEqual(
            self.record["generated_solution"]["choice_key"],
            ["A", "C", "B", "B", "A", "D", "C", "A", "B", "D", "C", "A", "D", "D", "A", "C", "B"],
        )
        self.assertEqual(
            self.record["generated_solution"]["fill_in_answers"],
            {
                "18": r"\dfrac{\sqrt3+2\sqrt2}{6}",
                "19": r"|k|>\dfrac13",
                "20": "100",
                "21": "1",
                "22": "1760",
                "23": r"30^\circ",
            },
        )
        self.assertIn("原题记号有待核", self.solution_text)
        self.assertIn(r"\theta=\pi/12,7\pi/12", self.solution_text)
        self.assertIn(r"\theta=\pi/12,5\pi/12,7\pi/12,11\pi/12", self.solution_text)
        self.assertEqual(
            [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.solution_text, re.M)],
            list(range(1, 29)),
        )

    def test_strict_markdown_conversion_resolves_the_local_tex_figure(self):
        target = "../math-gaokao-latex/1993_新科目组_理科/figures/f1993_new_science_q23_fold.tex"
        slug = "f1993_new_science_q23_fold"
        result = md2tex.convert_markdown(
            self.text,
            md2tex.ConversionContext(figure_map={target: slug}, strict=True),
        )
        self.assertEqual(result.warnings, ())
        self.assertEqual(result.referenced_figures, (slug,))
        self.assertEqual(result.text.count(r"\input{figures/" + slug + "}"), 1)


if __name__ == "__main__":
    unittest.main()

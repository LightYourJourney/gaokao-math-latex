import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER_DIR = PROJECT / "2004_上海卷_文科"
TRANSCRIPT = ROOT / "2004/2004_数学真题_上海文_试题.md"
SOURCE_ID = "src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290"
SOURCE_SHA256 = "4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad"
PAPER_ID = "gk-2004-regular-shanghai-arts"


class ShanghaiArts2004TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription draft must exist")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")

    def test_fixed_source_fingerprint_is_formally_bound_with_limits_preserved(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["raw_paper_name"], "2004上海文.pdf")
        self.assertEqual(source["upstream_path"], "普通高考/2004/2004上海文.pdf")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["paper_id"], PAPER_ID)
        self.assertEqual(source["paper_relation"], "canonical")

        paper = next(item for item in self.manifest["papers"] if item["paper_id"] == PAPER_ID)
        self.assertEqual(paper["legacy_ids"], [])
        self.assertEqual(paper["source_ids"], [SOURCE_ID])
        self.assertEqual(paper["question_count"], 22)
        self.assertEqual(paper["year"], 2004)
        self.assertEqual(paper["track"], "arts")
        self.assertEqual(paper["production_state"], "blocked")
        self.assertTrue({"ISSUE-1384", "ISSUE-1385"}.issubset(set(paper["issue_ids"])))

        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn(PAPER_ID, self.transcript)

    def test_transcription_covers_all_22_questions_in_source_order(self):
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_high_risk_formulas_and_disputed_wording_match_source(self):
        expected = (
            r"\tan\left(\alpha + \dfrac{\pi}{4}\right)",
            r"x = -1",
            r"A \cap B = \{2\}",
            r"k = 3x - 2y",
            r"x = 2",
            r"A(0, -4)",
            r"(x + 1)^{10}",
            r"f(x) = a|x - b| + 2",
            r"2\sin\left(\dfrac{\pi}{2} - x\right) = 1",
            r"x = k\pi + (-1)^k",
            r"(1 + \mathrm{i})z_1 = -1 + 5\mathrm{i}",
            r"z_2 = a - 2 - \mathrm{i}",
            r"|z_1 - z_2| < |z_1|",
            r"8\text{ cm}^2",
            r"f(x) = \sqrt{2 - \dfrac{x + 3}{x + 1}}",
            r"g(x) = \lg[(x - a - 1)(2a - x)]",
            r"B \subseteq A",
            r"y = \dfrac{1}{8}x^2 - 4",
            r"DEF - ABC",
            r"\dfrac{x^2}{9} - y^2 = 1",
            r"y^2 = 2px",
            r"\dfrac{x^2}{a^2} + \dfrac{y^2}{b^2} = 1",
        )
        for formula in expected:
            self.assertIn(formula, self.transcript)

    def test_all_four_source_figures_are_registered_without_raster_embedding(self):
        figures = (
            "f2004_shanghai_arts_q05_function_graph.tex",
            "f2004_shanghai_arts_q18_frame_geometry.tex",
            "f2004_shanghai_arts_q20_parabola_geometry.tex",
            "f2004_shanghai_arts_q21_pyramid_frustum.tex",
        )
        for fig in figures:
            fig_path = PAPER_DIR / "figures" / fig
            self.assertTrue(fig_path.is_file(), f"figure file {fig} must exist")
            content = fig_path.read_text(encoding="utf-8")
            self.assertIn("\\begin{tikzpicture}", content)
            self.assertNotIn("\\includegraphics", content)
            self.assertIn(fig, self.transcript)

        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    def test_provenance_and_receipts_reflect_unresolved_blockers(self):
        prov_path = PAPER_DIR / "provenance.json"
        self.assertTrue(prov_path.is_file())
        prov = json.loads(prov_path.read_text(encoding="utf-8"))
        self.assertEqual(prov["paper_id"], PAPER_ID)
        questions = {q["question_order"]: q for q in prov["questions"]}
        self.assertEqual(set(questions), set(range(1, 23)))

        # Q17 must be U grade with ISSUE-1384
        q17 = questions[17]
        self.assertEqual(q17["answer_evidence"]["grade"], "U")
        self.assertEqual(q17["conflict_status"], "none")
        self.assertIn("ISSUE-1384", q17["issue_ids"])

        # Q19 must be U grade with ISSUE-1385
        q19 = questions[19]
        self.assertEqual(q19["answer_evidence"]["grade"], "U")
        self.assertEqual(q19["conflict_status"], "none")
        self.assertIn("ISSUE-1385", q19["issue_ids"])

        # Check receipts exist and reflect final states
        build_receipt = json.loads((PAPER_DIR / "receipts/build.json").read_text(encoding="utf-8"))
        self.assertEqual(build_receipt["status"], "succeeded")
        self.assertEqual(len(build_receipt["editions"]), 4)

        review_receipt = json.loads((PAPER_DIR / "receipts/review.json").read_text(encoding="utf-8"))
        self.assertEqual(review_receipt["status"], "passed")
        self.assertEqual(review_receipt["batch_id"], "phase4-b45")


if __name__ == "__main__":
    unittest.main()

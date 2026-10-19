import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2015/2015_数学真题_福建文_试题.md"
REVIEW = ROOT / "2015/2015_福建文科_来源校对.json"
FIGURES = ROOT / "2015/2015_数学真题_福建文_图表清单.md"
ANSWER_KEY = ROOT / "2015/2015_数学真题_福建文_答案要点.md"
SOLUTIONS = ROOT / "2015/2015_数学真题_福建文_解析正文.md"
PAPER_ROOT = ROOT / "math-gaokao-latex/2015_福建卷_文科"


class FujianArtsTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))
        cls.figures = FIGURES.read_text(encoding="utf-8")
        cls.answer_key = ANSWER_KEY.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")

    def test_source_identity_and_transcription_hash(self):
        self.assertEqual(
            self.review["source"]["sha256"],
            "4ca0fbac9967c9a73bdb0bc00eceb3d0181c57285ee72fc260a02c9c24172383",
        )
        self.assertEqual(self.review["source"]["page_count"], 2)
        self.assertEqual(self.review["source"]["printed_pages"], [945, 946])
        self.assertIsNone(self.review["paper_id"])
        self.assertIsNone(self.review["official_answer"])
        self.assertEqual(
            hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
            self.review["transcription"]["sha256"],
        )

    def test_all_questions_are_present_in_their_source_order(self):
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.review["transcription"]["question_count"], 22)
        self.assertEqual(self.review["transcription"]["question_types"], {
            "single_choice": list(range(1, 13)),
            "fill_in": list(range(13, 17)),
            "written_response": list(range(17, 23)),
        })
        self.assertLess(self.transcript.index("**12．**"), self.transcript.index("## 二、填空题"))
        self.assertGreater(self.transcript.index("## 二、填空题"), self.transcript.index("**12．**"))

    def test_high_risk_formula_and_condition_strings_are_preserved(self):
        for expression in (
            r"\sin\alpha=-\dfrac{5}{13}",
            r"x-2y+2\geqslant0",
            r"\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1",
            r"k\sin x\cos x<x",
            r"b_n=2^{a_n-2}+n",
            r"10\sqrt3\sin\dfrac{x}{2}\cos\dfrac{x}{2}",
            r"f(x)=\ln x-\dfrac{(x-1)^2}{2}",
        ):
            self.assertIn(expression, self.transcript)
        self.assertIn("结果如表所示", self.transcript)
        self.assertNotIn("结果如下表所示", self.transcript)
        self.assertIn(r"当 \(x\in(1,x_0)\)，恒有 \(f(x)>k(x-1)\)", self.transcript)
        self.assertNotIn(r"当 \(x\in(1,x_0)\) 时，恒有", self.transcript)
        for option in (r"(A) \((0,\dfrac{\sqrt3}{2}]\)", r"(B) \((0,\dfrac34]\)", r"(C) \([\dfrac{\sqrt3}{2},1)\)", r"(D) \([\dfrac34,1)\)", "充分而不必要条件", "必要而不充分条件", "充分必要条件", "既不充分也不必要条件"):
            self.assertIn(option, self.transcript)

    def test_independent_solution_sources_are_complete_and_not_official(self):
        for source in (self.answer_key, self.solutions):
            self.assertIn("official_answer: null", source)
            self.assertIn("非官方", source)
            self.assertIn("draft-independent-solutions-cross-verified-pending-formal-acceptance", source)
        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题", self.solutions, re.M)]
        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．", self.answer_key, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 23)))
        self.assertEqual(answer_numbers, list(range(1, 23)))
        for expression in (r"m=\pm2\sqrt2", r"n_k", r"k<1", r"\frac{1+\sqrt3}{\sqrt2}"):
            self.assertIn(expression, self.solutions)

    def test_diagrams_and_table_are_accounted_for_without_raster_assets(self):
        self.assertEqual(
            self.review["figures_and_tables"]["items"],
            ["q4-flowchart", "q8-shaded-region", "q9-three-views", "q18-frequency-table", "q19-parabola-geometry", "q20-solid-geometry"],
        )
        self.assertIn("TikZ 已重绘", self.figures)
        self.assertFalse(self.review["figures_and_tables"]["raster_source_committed"])
        self.assertEqual(
            self.review["figures_and_tables"]["vector_reconstruction_status"],
            "draft-linked-independently-reviewed-pending-formal-acceptance",
        )
        self.assertFalse(self.review["generated_solution"]["is_official"])
        self.assertEqual(
            self.review["generated_solution"]["status"],
            "draft-independent-solutions-cross-verified-pending-formal-acceptance",
        )

    def test_vector_assets_are_linked_hashed_and_tikz_only(self):
        assets = self.review["figures_and_tables"]["vector_assets"]
        self.assertEqual(len(assets), 5)
        for asset in assets:
            path = ROOT / asset["path"]
            self.assertTrue(path.is_file(), asset["path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), asset["sha256"])
            source = path.read_text(encoding="utf-8")
            self.assertIn(r"\begin{tikzpicture}", source)
            self.assertIn(r"\end{tikzpicture}", source)
            relative_target = asset["path"].removeprefix("math-gaokao-latex/")
            self.assertIn(f"](../math-gaokao-latex/{relative_target})", self.transcript)
        raster_suffixes = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".bmp"}
        tracked_rasters = [path for path in PAPER_ROOT.rglob("*") if path.suffix.lower() in raster_suffixes]
        self.assertEqual(tracked_rasters, [])

    def test_geometry_assets_preserve_only_registered_structure_and_given_dimensions(self):
        q8 = (PAPER_ROOT / "figures/f2015fj_arts_q08_shaded_region.tex").read_text(encoding="utf-8")
        for point in ("(-2,0)", "(1,0)", "(1,2)", "(-2,2)", "(0,1)"):
            self.assertIn(point, q8)
        q9 = (PAPER_ROOT / "figures/f2015fj_arts_q09_three_views.tex").read_text(encoding="utf-8")
        self.assertIn(r"{\(2\)}", q9)
        self.assertEqual(q9.count(r"{\(1\)}"), 3)
        self.assertIn("(2,1)", q9)
        self.assertNotIn("2.35", q9)
        q19 = (PAPER_ROOT / "figures/f2015fj_arts_q19_parabola_geometry.tex").read_text(encoding="utf-8")
        self.assertIn("y^2=4x", q19)
        self.assertIn("domain=-2.35:3.0", q19)
        self.assertIn("(2.25,{13*sqrt(2)/6})", q19)
        self.assertIn("(1.1,{-7*sqrt(2)/5})", q19)
        q4 = (PAPER_ROOT / "figures/f2015fj_arts_q04_flowchart.tex").read_text(encoding="utf-8")
        self.assertIn(r"\draw[->] (test.east)", q4)
        self.assertIn(r"\draw[->] (merge) -- (output.north)", q4)
        self.assertIn(r"\draw[->] (no.south)", q4)
        self.assertIn(r"(yes.south |- merge) -- (merge)", q4)
        self.assertIn(r"(no.south |- merge) -- (merge)", q4)
        q20 = (PAPER_ROOT / "figures/f2015fj_arts_q20_solid_geometry.tex").read_text(encoding="utf-8")
        for edge in ("(P) -- (A)", "(P) -- (B)", "(P) -- (C)", "(P) -- (D)", "(C) -- (E)", "(D) -- (E)"):
            self.assertIn(edge, q20)

    def test_inline_math_delimiters_are_balanced_in_transcript_and_inventory(self):
        for text in (self.transcript, self.figures, self.answer_key, self.solutions):
            self.assertEqual(text.count(r"\("), text.count(r"\)"))
            self.assertGreater(text.count(r"\("), 0)
            self.assertEqual(text.count(r"\["), text.count(r"\]"))


if __name__ == "__main__":
    unittest.main()

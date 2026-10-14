from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUESTION = ROOT.parent / "1991" / "1991_数学真题_全国文_试题.md"
ANSWER = ROOT.parent / "1991" / "1991_数学真题_全国文_答案要点.md"
SOLUTION = ROOT.parent / "1991" / "1991_数学真题_全国文_解析正文.md"
FIGURE = ROOT / "1991_全国卷_文科" / "figures" / "f1991_national_arts_q23_frustum.tex"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class NationalArts1991SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = QUESTION.read_text(encoding="utf-8")
        cls.answers = ANSWER.read_text(encoding="utf-8")
        cls.solution = SOLUTION.read_text(encoding="utf-8")

    def test_question_and_solution_numbering_are_complete(self):
        expected = [str(n) for n in range(1, 27)]
        self.assertEqual(re.findall(r"(?m)^\*\*(\d+)．\*\*$", self.questions), expected)
        self.assertEqual(re.findall(r"(?m)^### 第 (\d+) 题$", self.solution), expected)

    def test_every_question_has_one_answer_block(self):
        self.assertEqual(len(re.findall(r"(?m)^\*\*答案：", self.answers)), 26)

    def test_source_documents_have_balanced_display_math(self):
        for label, text in (
            ("试题", self.questions),
            ("答案", self.answers),
            ("解析", self.solution),
        ):
            in_display = False
            delimiters = 0
            for line in text.splitlines():
                if line.strip() == "$$":
                    in_display = not in_display
                    delimiters += 1
                elif in_display:
                    self.assertNotIn("。", line, f"{label}把中文句号放进了数学模式")
            self.assertEqual(delimiters % 2, 0, f"{label}的 $$ 块未配对")

    def test_conditional_answers_parse_and_round_trip(self):
        points = solution_sources.parse_answer_points(self.answers)
        self.assertEqual(len(points), 26)
        self.assertIn("若 $a>1$", points[24].answer_for(None))
        self.assertIn("题设未确定长轴方向", points[25].answer_for(None))
        for point in points[24:26]:
            answer = point.answer_for(None)
            self.assertEqual(answer.count("$") % 2, 0, f"第 {point.number} 题行内公式未配对")
        combined = solution_sources.render_combined(
            self.questions, self.solution, self.answers
        )
        self.assertEqual(
            solution_sources.extract_solution_blocks(combined, self.questions),
            self.solution,
        )

    def test_answer_key_matches_the_combinatorial_derivation_for_q5(self):
        self.assertRegex(self.answers, r"(?s)\*\*5．\*\*\s+\*\*答案：B\*\*")
        self.assertIn("异面直线对数为 24", self.solution)

    def test_q17_answer_point_preserves_the_sine_shift_sign(self):
        points = solution_sources.parse_answer_points(self.answers)
        self.assertEqual(points[16].answer_for(None), r"$2-\sqrt5$")

    def test_q13_opposite_coefficient_signs_exclude_quadrant_three(self):
        points = solution_sources.parse_answer_points(self.answers)
        self.assertEqual(points[12].answer_for(None), "C")

    def test_source_uncertainties_are_preserved(self):
        self.assertRegex(self.questions, r"\$b_1\s+\+\s+\+b_2\s*\+\s*b_3=")
        self.assertIn("$a_n=2n-3$ 或 $a_n=5-2n$", self.answers)
        self.assertIn("\u539f\u9898\u6ca1\u6709\u8bf4\u660e\u957f\u8f74\u5e73\u884c", self.solution)
        self.assertIn("\u975e\u5b98\u65b9", self.answers)
        self.assertIn("待独立复核", self.answers)

    def test_q23_figure_is_a_local_vector_source(self):
        relative = "../math-gaokao-latex/1991_全国卷_文科/figures/f1991_national_arts_q23_frustum.tex"
        self.assertIn(relative, self.questions)
        self.assertTrue(FIGURE.is_file())
        figure = FIGURE.read_text(encoding="utf-8")
        self.assertIn(r"\begin{tikzpicture}", figure)
        self.assertIn(r"\draw[dashed] (A)--(C);", figure)


if __name__ == "__main__":
    unittest.main()

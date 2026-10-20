import re
import unittest
import math
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季安徽理_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_春季安徽理_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_春季安徽理_解析正文.md"
SOURCE_ID = "src-7c00191d50c17971e6f514bf6066e92693aa2b71f0ff05a054e2abe22acb5075"
SOURCE_SHA256 = "51038ba6ecdfbb8c5c7edc417f871eda5a5a5c03cc5af510da08131ec0dbb151"


class AnhuiSpring2004ScienceSolutionsTests(unittest.TestCase):
    def test_answer_and_solution_sources_are_nonofficial_and_complete(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        self.assertIn("official_answer: null", answers)
        self.assertIn("非来源印载答案", answers)
        self.assertIn("非来源印载解析", solutions)
        for document in (answers, solutions):
            self.assertIn(SOURCE_ID, document)
            self.assertIn(SOURCE_SHA256, document)
            self.assertEqual(document.count("$") % 2, 0)

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))
        self.assertEqual(solution_numbers, list(range(1, 23)))

    def test_key_answers_and_parameter_cases_are_explicit(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"1-38i", answers)
        self.assertIn(r"\dfrac{\sqrt3}{3}", answers)
        self.assertIn(r"-27", answers)
        self.assertIn(r"b_n=2n-1", answers)
        self.assertIn(r"\dfrac{\sqrt{10}}5", answers)
        self.assertIn(r"E\xi=\dfrac{22}{9}", answers)
        self.assertIn("若 $a>1$", solutions)
        self.assertIn("若 $0<a<1$", solutions)
        self.assertIn("正项", solutions)
        self.assertIn(r"a>-\frac{45}{14}", solutions)
        self.assertIn("法线为竖直线", solutions)

    def test_q16_constant_term_and_q18_positive_sequence(self):
        matching_n = [
            n for n in range(1, 10)
            if (-1) ** n * math.comb(2 * n, n) == -20
        ]
        self.assertEqual(matching_n, [3])

        prefix_sum = 0
        for n in range(1, 9):
            b_n = 2 * n - 1
            self.assertGreater(b_n, 0)
            prefix_sum += b_n
            self.assertEqual(4 * prefix_sum, (b_n + 1) ** 2)

        answers = ANSWERS.read_text(encoding="utf-8")
        self.assertRegex(answers, r"\*\*16．\*\*.*\bn=3\b")
        self.assertIn(r"b_n=2n-1", answers)

    def test_q21_distribution_normalizes_and_expectation_is_reproducible(self):
        probabilities = (Fraction(28, 45), Fraction(14, 45), Fraction(1, 15))
        self.assertEqual(sum(probabilities), 1)
        expected = sum(
            count * probability
            for count, probability in zip((2, 3, 4), probabilities)
        )
        self.assertEqual(expected, Fraction(22, 9))

        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        for document in (answers, solutions):
            for numerator, denominator in ((28, 45), (14, 45), (1, 15), (22, 9)):
                self.assertRegex(
                    document,
                    rf"\\d?frac\{{{numerator}\}}\{{{denominator}\}}",
                )

    def test_q22_handles_vertex_normal_and_additional_normals(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"(-1,-\dfrac{19}{7})", answers)
        self.assertIn(r"M=(-2,-\dfrac{26}{7})", answers)
        self.assertIn(r"a>-\dfrac{45}{14}", answers)
        self.assertIn(r"y-a=\mp\dfrac{x+2}{2\sqrt{a+\dfrac{45}{14}}}", answers)
        self.assertIn("处的竖直法线", answers)
        self.assertIn("法线为竖直线", solutions)


if __name__ == "__main__":
    unittest.main()

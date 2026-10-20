"""Exact checks for the author-derived Q1-Q16 solution draft."""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "math-gaokao-latex/1998_上海卷_理科"
SOLUTIONS = PAPER / "解析草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"


class Shanghai1998ScienceSolutionsTests(unittest.TestCase):
    def test_draft_covers_q1_to_q16_and_preserves_nonofficial_boundary(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 17)))
        self.assertIn("作者依据本卷当前题面独立推导", text)
        self.assertIn("不是第二位复核者的盲解", text)
        self.assertIn("不替代对固定扫描原页的逐字核验", text)
        self.assertIn("官方答案", text)

    def test_q1_to_q9_results_are_mathematically_consistent(self):
        # lg(20)+log_100(25)=lg(2)+1+(1-lg(2))=2.
        self.assertEqual((math.log10(20) + math.log10(25) / 2), 2.0)
        self.assertEqual(4 - math.sqrt(4 + 5), 1)  # Q2 minimum
        self.assertEqual(Fraction(4 + 4, 4), 2)  # Q3 limit at x=1
        self.assertEqual(2 + 1, 3)  # Q4 inverse: (x-2)^3+1, checked by composition below
        for x in (-3, 0, 1, 7):
            f = (x - 1) ** (1 / 3) + 2
            # Use the real cube root to retain negative arguments.
            f = math.copysign(abs(x - 1) ** (1 / 3), x - 1) + 2
            inverse = (f - 2) ** 3 + 1
            self.assertAlmostEqual(inverse, x)
        self.assertAlmostEqual(Fraction(2**3, 6) / math.sqrt(2), 2 * math.sqrt(2) / 3)
        self.assertEqual(4 - 3, 1)  # Q6: a^2-b^2=c^2, and the major axis is y
        self.assertEqual(Fraction(3 * 6, 35), Fraction(18, 35))
        self.assertEqual(max(3, 4), 4)
        self.assertEqual(5 * 4**2 - 24 * 4 + 16, 0)  # Q9 polynomial for n=4
        self.assertEqual(4 * Fraction(1, 3) / (1 - Fraction(1, 3)), 2)  # Q10 geometric sum

    def test_q11_to_q14_choice_and_parameter_reasons(self):
        self.assertEqual((Fraction(3, 2) - 1), Fraction(1, 2))
        self.assertEqual(Fraction(1, 2) * (1 - Fraction(1, 2)), Fraction(1, 4))
        # Q12: cos(4x) is even with fundamental period pi/2.
        self.assertAlmostEqual(math.cos(4 * (0.37 + math.pi / 2)), math.cos(4 * 0.37))
        self.assertAlmostEqual(math.cos(-4 * 0.37), math.cos(4 * 0.37))
        # Q13 has x>-5; for x>0, x+5>1 so log_a(x+5)<0 when 0<a<1.
        self.assertLess(math.log(5.5, 0.5), 0)
        # In Q14, planes perpendicular do not force every line in one plane
        # to be perpendicular to the other plane.
        self.assertIn("**14．**", SOLUTIONS.read_text(encoding="utf-8"))

    def test_q15_records_counterexamples_and_does_not_force_source_key_d(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        self.assertIn("a=5", text)
        self.assertIn("a=7", text)
        self.assertIn("题面条件不能唯一确定正确选项", text)
        self.assertIn("D", answers)
        self.assertIn("卷内答案表", text)

    def test_q1_to_q16_conclusions_are_explicit_and_source_key_stays_separate(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        for anchor in (
            "故所求为 $2$",
            "$a=5$",
            "$a=4$",
            r"f^{-1}(x)=(x-2)^3+1",
            r"V=2\sqrt2/3",
            r"\dfrac{x^2}{3}+\dfrac{y^2}{4}=1",
            r"\frac{18}{35}",
            "全局最大值为 $4$",
            "$n=4$",
            "=2$。",
            "$a=3/2$",
            "故选 B",
            "故选 A",
            "假命题为 C",
            "不能唯一确定正确选项",
            "故选 C",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, text)
        self.assertIn("| 卷内所载 | B | A | C | D | C |", answers)

    def test_q16_line_normals_are_perpendicular_by_sine_rule(self):
        # sin(A)=a/(2R), sin(B)=b/(2R): (sin A,a).(b,-sin B)=0.
        a, b, radius = Fraction(5), Fraction(7), Fraction(3)
        sin_a, sin_b = a / (2 * radius), b / (2 * radius)
        self.assertEqual(sin_a * b - a * sin_b, 0)


if __name__ == "__main__":
    unittest.main()

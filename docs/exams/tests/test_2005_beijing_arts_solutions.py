# -*- coding: utf-8 -*-
"""2005 年高考数学真题（北京卷文科 gk-2005-regular-beijing-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_北京文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_北京文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_北京文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_北京文科_含解析.md"


class Beijing2005ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 218–219 的两页题面", solutions)
        self.assertIn("独立推导复算", solutions)

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 21)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 21)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 21)))

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-8 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["C", "A", "B", "C", "B", "D", "C", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（9-14 题）与解答题结论（15-20 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"x = -1", answers)
        self.assertIn(r"(1, 0)", answers)
        self.assertIn(r"-20", answers)
        self.assertIn(r"[-1, 2) \cup (2, +\infty)", answers)
        self.assertIn(r"\sqrt{2}", answers)
        self.assertIn(r"②③", answers)
        self.assertIn(r"65", answers)
        self.assertIn(r"20", answers)

        # 解答题
        self.assertIn(r"-\dfrac{1}{7}", answers)
        self.assertIn(r"\dfrac{7}{6}", answers)
        self.assertIn(r"\dfrac{2\sqrt{2}}{5}", answers)
        self.assertIn(r"a_2 = \dfrac{1}{3}", answers)
        self.assertIn(r"\dfrac{3}{7}\left[\left(\dfrac{16}{9}\right)^n - 1\right]", answers)
        self.assertIn(r"\dfrac{3}{8}", answers)
        self.assertIn(r"\dfrac{20}{27}", answers)
        self.assertIn(r"\dfrac{1}{6}", answers)
        self.assertIn(r"-7", answers)
        self.assertIn(r"k^2 x^2 - y^2 = (k^2 + 1)d^2", answers)

    def test_mathematical_derivations(self):
        """独立复算核心数学公式与数值逻辑。"""
        # Q03: (m+2)(m-2) + 3m(m+2) = 0 => 2(m+2)(2m-1) = 0 => m = -2 or 1/2
        roots_q03 = [m for m in [-2, 0.5] if (m+2)*(m-2) + 3*m*(m+2) == 0]
        self.assertEqual(roots_q03, [-2, 0.5])

        # Q04: |a|=1, |b|=2, c=a+b perp a => |a|^2 + a.b = 0 => 1 + 2*cos(theta) = 0 => cos(theta) = -1/2 => theta = 120
        self.assertAlmostEqual(math.degrees(math.acos(-0.5)), 120.0)

        # Q05: x^2 + (y-6)^2 = 9. Dist(O, C) = 6, R = 3. sin(theta/2) = 3/6 = 0.5 => theta = 60 deg = pi/3
        self.assertAlmostEqual(2 * math.asin(3 / 6), math.pi / 3)

        # Q06: For acute alpha, beta: cos(alpha+beta) < cos(alpha) + cos(beta)
        for a_deg in [1, 10, 45, 80, 89]:
            for b_deg in [1, 10, 45, 80, 89]:
                a, b = math.radians(a_deg), math.radians(b_deg)
                self.assertLess(math.cos(a + b), math.cos(a) + math.cos(b))

        # Q08: C(4, 1) * A(4, 4) = 4 * 24 = 96
        self.assertEqual(4 * math.factorial(4), 96)

        # Q10: C(6, 3) * (-1)^3 = -20
        self.assertEqual(-math.comb(6, 3), -20)

        # Q12: AC=sqrt(3), A=45, C=75 => B=60. BC = sqrt(3) * sin(45)/sin(60) = sqrt(2)
        bc = math.sqrt(3) * math.sin(math.radians(45)) / math.sin(math.radians(60))
        self.assertAlmostEqual(bc, math.sqrt(2))

        # Q14: sum_{k=1}^9 k = 45. total = 45 + 10 + 10 = 65. Horner = 2 * 10 = 20.
        self.assertEqual(sum(range(1, 10)) + 10 + 10, 65)
        self.assertEqual(2 * 10, 20)

        # Q15: tan(alpha/2) = 2 => tan(alpha) = 4 / (1 - 4) = -4/3
        # (1) tan(alpha + pi/4) = (-4/3 + 1) / (1 - (-4/3)) = -1/7
        # (2) (6*tan + 1) / (3*tan - 2) = (-8 + 1) / (-4 - 2) = 7/6
        t = -Fraction(4, 3)
        self.assertEqual((t + 1) / (1 - t), -Fraction(1, 7))
        self.assertEqual((6 * t + 1) / (3 * t - 2), Fraction(7, 6))

        # Q16: AC1 = (-3, 0, 4), B1C = (0, -4, -4). dot = 16, |AC1|=5, |B1C|=4*sqrt(2)
        # cos = 16 / (20*sqrt(2)) = 4 / (5*sqrt(2)) = 2*sqrt(2)/5
        cos_theta = 16 / (5 * 4 * math.sqrt(2))
        self.assertAlmostEqual(cos_theta, 2 * math.sqrt(2) / 5)

        # Q17: a_n: a1 = 1, a2 = 1/3, q = 4/3.
        # T_n: c1 = 1/3, Q = 16/9. T_n = 1/3 * (Q^n - 1) / (7/9) = 3/7 * ((16/9)^n - 1)
        c1 = Fraction(1, 3)
        Q = Fraction(16, 9)
        def t_n(n):
            return Fraction(3, 7) * (Q**n - 1)
        self.assertEqual(t_n(1), Fraction(1, 3))
        self.assertEqual(t_n(2), Fraction(1, 3) + Fraction(1, 3) * Fraction(16, 9))

        # Q18:
        # (1) C(3, 2) * (1/2)^3 = 3/8
        # (2) C(3, 2)*(2/3)^2*(1/3) + (2/3)^3 = 12/27 + 8/27 = 20/27
        # (3) Y=2,X=0 => 4/9 * 1/8 = 1/18; Y=3,X=1 => 8/27 * 3/8 = 1/9. Sum = 3/18 = 1/6
        self.assertEqual(Fraction(1, 18) + Fraction(1, 9), Fraction(1, 6))

        # Q19: f(x) = -x^3 + 3x^2 + 9x + a.
        # max on [-2, 2] is f(2) = 20 => -8 + 12 + 18 + a = 20 => a + 22 = 20 => a = -2
        # min on [-2, 2] is f(-1) = 1 + 3 - 9 + a = a - 5 = -7
        self.assertEqual(-2 - 5, -7)


if __name__ == "__main__":
    unittest.main()

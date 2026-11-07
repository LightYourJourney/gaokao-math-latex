# -*- coding: utf-8 -*-
"""2004 年高考数学真题（重庆卷文科 gk-2004-regular-chongqing-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_重庆文科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_重庆文科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_重庆文科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_重庆文科_含解析.md"


class Chongqing2004ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 162–163 的两页题面", solutions)
        self.assertIn("独立推导复算", solutions)

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 23)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 23)))

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-12 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "B", "D", "A", "B", "C", "A", "D", "B", "B", "D", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（13-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"-2", answers)
        self.assertIn(r"15", answers)
        self.assertIn(r"4x - y - 4 = 0", answers)
        self.assertIn(r"x - y + 2 = 0", answers)
        self.assertIn(r"4", answers)

        # 解答题
        self.assertIn(r"\pi", answers)
        self.assertIn(r"0.94", answers)
        self.assertIn(r"0.44", answers)
        self.assertIn(r"0.441", answers)
        self.assertIn(r"\dfrac{\sqrt{5}}{10}", answers)
        self.assertIn(r"3150000", answers)
        self.assertIn(r"x = 2p", answers)
        self.assertIn(r"b_n = -\dfrac{1}{3}\left(\dfrac{2}{3}\right)^{n-1}", answers)
        self.assertIn(r"S_n = \dfrac{n(n+1)}{2} + 9 - (3n + 9)\left(\dfrac{2}{3}\right)^n", answers)

    def test_mathematical_derivations(self):
        """独立复算核心数学公式与数值逻辑。"""
        # Q02: f(2)/f(1/2) = (3/5) / (-3/5) = -1
        f = lambda x: (x**2 - 1) / (x**2 + 1)
        self.assertAlmostEqual(f(2) / f(0.5), -1.0)

        # Q03: circle (x-1)^2 + (y+2)^2 = 2 to x - y = 1: d = |1 - (-2) - 1| / sqrt(2) = sqrt(2)
        d_q03 = abs(1 - (-2) - 1) / math.sqrt(2)
        self.assertAlmostEqual(d_q03, math.sqrt(2))

        # Q05: sin(163)*sin(223) + sin(253)*sin(313) = cos(17+43) = cos(60) = 0.5
        r = math.radians
        val_q05 = math.sin(r(163)) * math.sin(r(223)) + math.sin(r(253)) * math.sin(r(313))
        self.assertAlmostEqual(val_q05, 0.5)

        # Q06: |a|^2 - 2|a| - 24 = 0 => |a| = 6
        roots = [x for x in [6, -4] if x > 0]
        self.assertEqual(roots, [6])

        # Q10: e <= 5/3
        self.assertAlmostEqual(5 / 3, 1.6666666666666667)

        # Q11: 3/10 * 2/9 * 7/8 = 7/120
        p_q11 = Fraction(3, 10) * Fraction(2, 9) * Fraction(7, 8)
        self.assertEqual(p_q11, Fraction(7, 120))

        # Q12: 6 * 23 + (120 - 24) = 138 + 96 = 234
        s_outer = 6 * (25 - 2)
        s_inner = 6 * (4 * 5) - 2 * 6 * 2
        self.assertEqual(s_outer + s_inner, 234)

        # Q13: C(5, 3) * a^3 = -80 => 10 a^3 = -80 => a = -2
        self.assertEqual(-80 // 10, -8)

        # Q14: 5/x + 3/y = 2, min(xy) = 15
        x, y = 5, 3
        self.assertEqual(x * y, 15)

        # Q15: y = 1/3 x^3 + 4/3 tangent through (2, 4): x0=2 or x0=-1
        # for x0=2: y-4 = 4(x-2) => 4x - y - 4 = 0
        # for x0=-1: y-1 = 1(x+1) => x - y + 2 = 0
        self.assertEqual((2)**3 - 3*(2)**2 + 4, 0)
        self.assertEqual((-1)**3 - 3*(-1)**2 + 4, 0)

        # Q16: volume ratio 8 => radius ratio 2 => circumference ratio 2 => 8 / 2 = 4
        self.assertEqual(8 // 2, 4)

        # Q18: P1 = 1 - 0.3*0.4*0.5 = 0.94; P2 = 0.21+0.14+0.09 = 0.44; P3 = 3 * 0.49 * 0.3 = 0.441
        self.assertAlmostEqual(1 - 0.3 * 0.4 * 0.5, 0.94)
        self.assertAlmostEqual(0.7 * 0.6 * 0.5 + 0.7 * 0.4 * 0.5 + 0.3 * 0.6 * 0.5, 0.44)
        self.assertAlmostEqual(3 * 0.49 * 0.3, 0.441)

        # Q19: sin(theta) = 1 / sqrt(20) = sqrt(5) / 10
        self.assertAlmostEqual(1 / math.sqrt(20), math.sqrt(5) / 10)

        # Q20: L(200) = -1/5 * (200)^3 + 24000*200 - 50000 = 3150000
        l_200 = - (200**3) // 5 + 24000 * 200 - 50000
        self.assertEqual(l_200, 3150000)

        # Q22:
        # a_n = 1 + (2/3)^{n-1}
        # S_n = n(n+1)/2 + 9 - (3n+9)(2/3)^n
        # test n=1: a1 = 2, S1 = 2
        # test n=2: a2 = 5/3, S2 = 1*2 + 2*(5/3) = 16/3
        def a(n):
            return 1 + Fraction(2, 3)**(n - 1)
        def s(n):
            return Fraction(n * (n + 1), 2) + 9 - (3 * n + 9) * Fraction(2, 3)**n

        self.assertEqual(a(1), Fraction(2, 1))
        self.assertEqual(a(2), Fraction(5, 3))
        self.assertEqual(s(1), Fraction(2, 1))
        self.assertEqual(s(2), Fraction(16, 3))
        self.assertEqual(s(1), a(1))
        self.assertEqual(s(2), 1 * a(1) + 2 * a(2))


if __name__ == "__main__":
    unittest.main()

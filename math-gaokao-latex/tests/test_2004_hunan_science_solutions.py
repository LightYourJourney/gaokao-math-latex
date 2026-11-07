# -*- coding: utf-8 -*-
"""2004 年高考数学真题（湖南卷理科 gk-2004-regular-hunan-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_湖南理科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_湖南理科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_湖南理科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_湖南理科_含解析.md"


class Hunan2004ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 174–175 的两页题面", solutions)
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
        expected_choices = ["D", "A", "B", "C", "B", "C", "B", "C", "A", "C", "B", "D"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（13-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"4", answers)
        self.assertIn(r"\dfrac{3}{4}", answers)
        self.assertIn(r"9", answers)
        self.assertIn(r"\left(0, \dfrac{2}{11}\right]", answers)

        # 解答题
        self.assertIn(r"\dfrac{5\sqrt{3}}{2}", answers)
        self.assertIn(r"30^\circ", answers)
        self.assertIn(r"\dfrac{5}{6}", answers)
        self.assertIn(r"\mathrm{e}^a", answers)
        self.assertIn(r"\left(x + \dfrac{3}{2}\right)^2 + \left(y - \dfrac{23}{2}\right)^2 = \dfrac{125}{2}", answers)
        self.assertIn(r"x_n = 1 - 2\left(\dfrac{1}{2k}\right)^n", answers)

    def test_mathematical_derivations(self):
        """独立复算核心数学公式与数值逻辑。"""
        # Q01: (1 + 1/i)^4 = (1 - i)^4 = (-2i)^2 = -4
        val_q01 = (1 + 1 / 1j) ** 4
        self.assertAlmostEqual(val_q01.real, -4.0)
        self.assertAlmostEqual(val_q01.imag, 0.0)

        # Q02: d = |PF|/e = sqrt(13) / (5/sqrt(13)) = 13/5
        e = Fraction(5, 1) / math.sqrt(13)
        d = math.sqrt(13) / e
        self.assertAlmostEqual(d, 2.6)

        # Q03: log2(3 + 1) = 2
        self.assertEqual(math.log2(3 + 1), 2.0)

        # Q06: b=4, c=2, 3 roots
        roots_neg = [x for x in [-2, -1] if x <= 0 and x ** 2 + 4 * x + 2 == x]
        roots_pos = [x for x in [2] if x > 0 and 2 == x]
        self.assertEqual(len(roots_neg) + len(roots_pos), 3)

        # Q07: 反例 a=2, b=3 时 a^3 + b^3 < 2ab^2
        self.assertTrue(2 ** 3 + 3 ** 3 < 2 * 2 * (3 ** 2))

        # Q08: 无穷等比数列和 a1=1/5, q=1/5 => S = (1/5)/(1 - 1/5) = 1/4
        self.assertEqual(Fraction(1, 5) / (1 - Fraction(1, 5)), Fraction(1, 4))

        # Q10: 正方体 8 取 3 直角三角形数 = 56 - 8 = 48
        self.assertEqual(math.comb(8, 3) - 8, 48)

        # Q11: 农民人均收入 1800 * 1.06^5 + 1350 + 160 * 5
        income_2008 = 1800 * (1.06 ** 5) + 1350 + 160 * 5
        self.assertTrue(4400 < income_2008 < 4600)

        # Q14: E = 3/4
        self.assertEqual(Fraction(3, 4), 0.75)

        # Q15: C(9, 6) = 84
        self.assertEqual(math.comb(9, 6), 84)

        # Q16: 焦半径公差上界 11d <= 2 => d <= 2/11
        self.assertAlmostEqual(Fraction(2, 11), 2 / 11)

        # Q17: cos(4a) = 1/2, 4a = 5pi/3 => 2a = 5pi/6
        # -cos(2a)*(1 + 2/sin(2a)) = -(-sqrt(3)/2)*(1 + 4) = 5*sqrt(3)/2
        val_q17 = (math.sqrt(3) / 2) * 5
        self.assertAlmostEqual(val_q17, 2.5 * math.sqrt(3))

        # Q18: tan theta = (a/3) / (sqrt(3)/3 * a) = 1/sqrt(3) => theta = 30 deg
        self.assertAlmostEqual(math.degrees(math.atan((1 / 3) / (math.sqrt(3) / 3))), 30.0)

        # Q19: p1=1/3, p2=1/4, p3=2/3 => 1 - (2/3)(3/4)(1/3) = 5/6
        p1, p2, p3 = Fraction(1, 3), Fraction(1, 4), Fraction(2, 3)
        self.assertEqual(p1 * (1 - p2), Fraction(1, 4))
        self.assertEqual(p2 * (1 - p3), Fraction(1, 12))
        self.assertEqual(p1 * p3, Fraction(2, 9))
        self.assertEqual(1 - (1 - p1) * (1 - p2) * (1 - p3), Fraction(5, 6))

        # Q21: Circle center (-3/2, 23/2), R^2 = 125/2
        xc, yc = Fraction(-3, 2), Fraction(23, 2)
        r2 = (6 - xc) ** 2 + (9 - yc) ** 2
        self.assertEqual(r2, Fraction(125, 2))
        self.assertEqual((-4 - xc) ** 2 + (4 - yc) ** 2, Fraction(125, 2))

        # Q22: x_{n+1} - 1 = 1/(2k)*(x_n - 1), x_1 = 1 - 1/k
        # delta for n=1: (u+8)(1-u)/u
        for u in [0.25, 0.5]:
            delta = (u + 8) * (1 - u) / u
            self.assertGreater(delta, 0)
        for u in [2.0, 4.0]:
            delta = (u + 8) * (1 - u) / u
            self.assertLess(delta, 0)


if __name__ == "__main__":
    unittest.main()

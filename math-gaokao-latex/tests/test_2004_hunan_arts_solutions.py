# -*- coding: utf-8 -*-
"""2004 年高考数学真题（湖南卷文科 gk-2004-regular-hunan-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_湖南文科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_湖南文科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_湖南文科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_湖南文科_含解析.md"


class Hunan2004ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 176–177 的两页题面", solutions)
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
        expected_choices = ["D", "D", "C", "A", "C", "B", "D", "D", "A", "C", "B", "A"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（13-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"2x - y + 4 = 0", answers)
        self.assertIn(r"84", answers)
        self.assertIn(r"2", answers)
        self.assertIn(r"\left(0, \dfrac{1}{2}\right)", answers)

        # 解答题
        self.assertIn(r"\dfrac{2}{3}", answers)
        self.assertIn(r"\dfrac{2\sqrt{3}}{3}", answers)
        self.assertIn(r"\dfrac{5}{6}", answers)
        self.assertIn(r"T_n = \dfrac{16a}{25} - \dfrac{4a(5n+4)}{25}\left(-\dfrac{1}{4}\right)^n", answers)
        self.assertIn(r"f(t) = \dfrac{3}{2}(t - t^3)", answers)
        self.assertIn(r"\left(x + \dfrac{3}{2}\right)^2 + \left(y - \dfrac{23}{2}\right)^2 = \dfrac{125}{2}", answers)

    def test_mathematical_derivations(self):
        """独立复算核心数学公式与数值逻辑。"""
        # Q04: d = |PF|/e = sqrt(13) / (5/sqrt(13)) = 13/5
        e = Fraction(5, 1) / math.sqrt(13)
        d = math.sqrt(13) / e
        self.assertAlmostEqual(d, 2.6)

        # Q10: 正方体 8 取 3 直角三角形数 = 56 - 8 = 48
        self.assertEqual(math.comb(8, 3) - 8, 48)

        # Q11: 农民人均收入 1800 * 1.06^5 + 1350 + 160 * 5
        income_2008 = 1800 * (1.06 ** 5) + 1350 + 160 * 5
        self.assertTrue(4400 < income_2008 < 4600)

        # Q14: C(9, 6) = 84
        self.assertEqual(math.comb(9, 6), 84)

        # Q17: tan(pi/4 + a) = 2 => tan a = 1/3
        tan_a = Fraction(1, 3)
        res_q17 = (tan_a ** 2 + 1) / (2 * tan_a + 1)
        self.assertEqual(res_q17, Fraction(2, 3))

        # Q18: tan theta = (a/2) / (sqrt(3)/4 * a) = 2/sqrt(3) = 2*sqrt(3)/3
        self.assertAlmostEqual(0.5 / (math.sqrt(3) / 4), 2 / math.sqrt(3))

        # Q19: p1=1/3, p2=1/4, p3=2/3 => 1 - (2/3)(3/4)(1/3) = 5/6
        p1, p2, p3 = Fraction(1, 3), Fraction(1, 4), Fraction(2, 3)
        self.assertEqual(p1 * (1 - p2), Fraction(1, 4))
        self.assertEqual(p2 * (1 - p3), Fraction(1, 12))
        self.assertEqual(p1 * p3, Fraction(2, 9))
        self.assertEqual(1 - (1 - p1) * (1 - p2) * (1 - p3), Fraction(5, 6))

        # Q20: 错位相减求和 Tn
        a = 1.0
        t = -0.25
        for n in range(1, 5):
            direct_sum = sum(k * a * (t ** (k - 1)) for k in range(1, n + 1))
            formula_sum = (16 * a / 25) * (1 - ((5 * n + 4) / 4) * (t ** n))
            self.assertAlmostEqual(direct_sum, formula_sum)

        # Q21: f(t) = 1.5 * (t - t^3), 最大值在 t = 1/sqrt(3) 时取 1/sqrt(3)
        t_crit = 1.0 / math.sqrt(3)
        max_f = 1.5 * (t_crit - t_crit ** 3)
        self.assertAlmostEqual(max_f, 1.0 / math.sqrt(3))

        # Q22: 圆 C 的方程与半径
        # A(6, 9), B(-4, 4), 圆心 C(-1.5, 11.5)
        # R^2 = (6 - (-1.5))^2 + (9 - 11.5)^2 = 7.5^2 + (-2.5)^2 = 56.25 + 6.25 = 62.5 = 125/2
        self.assertEqual(Fraction(15, 2) ** 2 + Fraction(-5, 2) ** 2, Fraction(125, 2))


if __name__ == "__main__":
    unittest.main()

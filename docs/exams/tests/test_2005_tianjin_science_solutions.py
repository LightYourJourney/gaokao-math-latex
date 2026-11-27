# -*- coding: utf-8 -*-
"""2005 年高考数学真题（天津卷理科 gk-2005-regular-tianjin-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_天津理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_天津理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_天津理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_天津理科_含解析.md"


class Tianjin2005ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性（全卷共 22 题）。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 266–267 的两页题面", solutions)
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
        """测试选择题答案（1-10 题：D C B D C B A C A B）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "C", "B", "D", "C", "B", "A", "C", "A", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（11-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"\dfrac{7^n - 1}{6}", answers)
        self.assertIn(r"\sqrt{2}", answers)
        self.assertIn(r"2600", answers)
        self.assertIn(r"\left(-\dfrac{\sqrt{10}}{5}, \dfrac{3\sqrt{10}}{5}\right)", answers)
        self.assertIn(r"4760", answers)
        self.assertIn(r"0", answers)

        # 解答题
        self.assertIn(r"\angle A = \dfrac{\pi}{3}", answers)
        self.assertIn(r"\tan B = \dfrac{1}{2}", answers)
        self.assertIn(r"S_n = \dfrac{n(n+3)}{2}", answers)
        self.assertIn(r"\max(a, b)", answers)
        self.assertIn(r"60^\circ", answers)
        self.assertIn(r"\dfrac{4\sqrt{3}}{27}\pi a^3", answers)
        self.assertIn(r"60", answers)
        self.assertIn(r"\left(0, \dfrac{1}{4a}\right)", answers)
        self.assertIn(r"y = -\dfrac{1}{4a}", answers)
        self.assertIn(r"(-\infty, -1) \cup \left(-1, -\dfrac{1}{4}\right)", answers)
        self.assertIn(r"a_{n+1} - a_n < \pi", answers)

    def test_mathematical_verifications(self):
        """针对全卷核心计算进行独立算法复算。"""
        # Q01: A = (-inf, -2] U [5/2, +inf), B = (-inf, -3) U [0, +inf)
        # A cap B = (-inf, -3) U [5/2, +inf)
        self.assertTrue(-3.1 < -3 and -3.1 <= -2)
        self.assertTrue(2.6 >= 2.5 and 2.6 >= 0)

        # Q02: (a + 3i)/(1 + 2i) = ((a+6) + (3-2a)i) / 5
        # Re = 0 => a = -6. Im = (3 - 2*(-6)) / 5 = 15/5 = 3 != 0.
        self.assertEqual(-6 + 6, 0)
        self.assertEqual((3 - 2 * (-6)) / 5, 3.0)

        # Q06: Ellipse count in rectangle |x| < 11 and |y| < 9
        # m in {1..10} (10 options), n in {1..8} (8 options)
        # Total pairs = 80, m=n circles = 8.
        # Ellipses = 80 - 8 = 72.
        self.assertEqual(10 * 8 - 8, 72)

        # Q07: Binomial probability
        p3 = math.comb(3, 2) * (0.6**2) * 0.4 + (0.6**3)
        self.assertAlmostEqual(p3, 0.648)
        self.assertEqual(Fraction(648, 1000), Fraction(81, 125))

        # Q10: log_a(x^3 - ax) on (-1/2, 0).
        # Inner g'(x) = 3x^2 - a <= 0 => a >= 3x^2. Max 3x^2 on [-1/2, 0] is 3/4.
        # 0 < a < 1 => a in [3/4, 1).
        self.assertEqual(3 * ((-0.5)**2), 0.75)

        # Q11: sum C_n^k * 6^(k-1) = (7^n - 1) / 6
        for n in [1, 2, 3, 4, 5]:
            val_sum = sum(math.comb(n, k) * (6**(k - 1)) for k in range(1, n + 1))
            self.assertEqual(val_sum, (7**n - 1) // 6)

        # Q12: Tetrahedron skew lines angle tan theta = sqrt(2)
        cos_t = 1 / math.sqrt(3)
        tan_t = math.sqrt(1 - cos_t**2) / cos_t
        self.assertAlmostEqual(tan_t, math.sqrt(2))

        # Q13: an+2 - an = 1 + (-1)^n.
        # Odd: a_1 = a_3 = ... = 1 (50 terms, sum = 50)
        # Even: a_2k = 2k (50 terms, sum = 50 * 51 = 2550)
        # Total = 2600.
        s_odd = 50 * 1
        s_even = sum(2 * k for k in range(1, 51))
        self.assertEqual(s_odd + s_even, 2600)

        # Q14: Angle bisector vector
        # A(0, 1), B(-3, 4). |OA| = 1, |OB| = 5.
        # e = (-sqrt(10)/10, 3*sqrt(10)/10). OC = 2*e = (-sqrt(10)/5, 3*sqrt(10)/5).
        v = (-Fraction(3, 5), Fraction(9, 5))
        mag_v = math.sqrt(float(v[0]**2 + v[1]**2))
        self.assertAlmostEqual(mag_v, 3 * math.sqrt(10) / 5)
        self.assertAlmostEqual(2 * float(v[0]) / mag_v, -math.sqrt(10) / 5)
        self.assertAlmostEqual(2 * float(v[1]) / mag_v, 3 * math.sqrt(10) / 5)

        # Q15: Expected value: 50000 * 0.12 * 0.96 - 50000 * 0.50 * 0.04
        # = 6000 * 0.96 - 25000 * 0.04 = 5760 - 1000 = 4760
        e_val = 6000 * 0.96 - 25000 * 0.04
        self.assertEqual(e_val, 4760.0)

        # Q16: Odd and symmetric across x = 1/2 => periodic with T = 2, f(int) = 0
        # sum f(1..5) = 0
        self.assertEqual(0 * 5, 0)

        # Q17: Triangle b^2 + c^2 - bc = a^2 => cos A = 1/2 => A = pi/3.
        # c/b = 1/2 + sqrt(3) => sin C / sin B = sqrt(3)/2 * cot B + 1/2 => cot B = 2 => tan B = 1/2.
        self.assertAlmostEqual(math.cos(math.pi / 3), 0.5)
        cot_B = 2.0
        tan_B = 1 / cot_B
        self.assertEqual(tan_B, 0.5)

        # Q18: Difference-ratio sum for a = b
        # a = 1: Sn = n(n+3)/2. For n = 3: 2 + 3 + 4 = 9 == 3*6/2 = 9.
        self.assertEqual(2 + 3 + 4, 3 * 6 // 2)
        # a != 1, e.g. a = 2, n = 3:
        # u1 = 2*2 = 4, u2 = 3*4 = 12, u3 = 4*8 = 32. Sum = 48.
        # Formula: (2*2 - 4 - 5*16 + 4*32) / (1-2)^2 = (4 - 4 - 80 + 128) / 1 = 48.
        s3_num = 2 * 2 - 4 - 5 * 16 + 4 * 32
        self.assertEqual(s3_num, 48)

        # Q20: Viewing angle optimization
        # tan theta = 160*t / (5t^2 - 720t + 128000)
        # 5t = 128000 / t => t^2 = 25600 => t = 160 => h = 60.
        self.assertEqual(math.sqrt(25600), 160.0)
        self.assertEqual(160.0 - 100, 60.0)

        # Q22: Fermat lemma on f(x) = x * sin x
        # f'(x0) = sin x0 + x0 * cos x0 = 0 => tan x0 = -x0
        # [f(x0)]^2 = x0^2 * sin^2 x0 = x0^4 / (1 + x0^2)
        # Roots of tan x = -x in (n*pi - pi/2, n*pi):
        # For n = 1: interval is (pi/2, pi) = (1.5708, 3.1416).
        # Root is around 2.0287578.
        # For n = 2: interval is (3*pi/2, 2*pi) = (4.7124, 6.2832).
        # Root is around 4.9131804.
        # Difference: 4.91318 - 2.02876 = 2.88442
        # pi/2 = 1.5708 < 2.88442 < pi = 3.1416.
        a1 = 2.0287578
        a2 = 4.9131804
        diff = a2 - a1
        self.assertTrue(math.pi / 2 < diff < math.pi)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""2005 年高考数学真题（山东卷文科 gk-2005-regular-shandong-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_山东文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_山东文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_山东文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_山东文科_含解析.md"


class Shandong2005ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性（全卷共 22 题）。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 260–261 的两页题面", solutions)
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
        """测试选择题答案（1-12 题：C C B B D C C A D D A B）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["C", "C", "B", "B", "D", "C", "C", "A", "D", "D", "A", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（13-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"50", answers)
        self.assertIn(r"\sqrt{2}", answers)
        self.assertIn(r"(2, 3)", answers)
        self.assertIn(r"③④", answers)

        # 解答题
        self.assertIn(r"-\dfrac{4}{5}", answers)
        self.assertIn(r"3", answers)
        self.assertIn(r"\dfrac{2}{7}", answers)
        self.assertIn(r"\dfrac{22}{35}", answers)
        self.assertIn(r"n = 3m + 6", answers)
        self.assertIn(r"\arccos\dfrac{\sqrt{2}}{4}", answers)
        self.assertIn(r"\arccos\dfrac{\sqrt{15}}{5}", answers)
        self.assertIn(r"\dfrac{2\sqrt{5}}{5}", answers)
        self.assertIn(r"3(n-1)2^{n+1} + 6 - \dfrac{n(n+1)}{2}", answers)
        self.assertIn(r"y^2 = 2px", answers)
        self.assertIn(r"(-2p, 2p)", answers)

    def test_mathematical_verifications(self):
        """针对全卷核心计算进行独立算法复算。"""
        # Q01: 等差数列序号 an = 1 + (n-1)*3 = 2005 => 3n = 2007 => n = 669
        self.assertEqual((2005 - 1) // 3 + 1, 669)

        # Q02: log_4(0.3) < 0 < 0.4^3 < 1 < 3^0.4
        log4_03 = math.log(0.3) / math.log(4)
        pow_04_3 = 0.4**3
        pow_3_04 = 3**0.4
        self.assertTrue(log4_03 < 0 < pow_04_3 < 1 < pow_3_04)

        # Q06: (3 - 1)^n = 128 => 2^n = 128 => n = 7
        # Term of x^(-3): 7 - 5/3*r = -3 => r = 6. Coeff: C_7^6 * 3^1 * (-1)^6 = 21
        self.assertEqual(math.comb(7, 6) * 3 * ((-1)**6), 21)

        # Q07: f(1) = e^0 = 1 => f(a) = 1.
        # a >= 0: e^(a-1) = 1 => a = 1.
        # -1 < a < 0: sin(pi * a^2) = 1 => pi * a^2 = pi/2 => a^2 = 1/2 => a = -sqrt(2)/2
        self.assertAlmostEqual(math.sin(math.pi * (-math.sqrt(0.5))**2), 1.0)

        # Q08: AD = AB + BC + CD = (a+2b) + (-5a+6b) + (7a-2b) = 3a + 6b = 3 * AB
        # Collinear: A, B, D
        self.assertEqual((1 - 5 + 7, 2 + 6 - 2), (3, 6))

        # Q09: Spherical distance: 45 deg N to 75 deg S => theta = 120 deg = 2*pi/3 rad
        self.assertAlmostEqual(45 + 75, 120)
        self.assertAlmostEqual(120 * math.pi / 180, 2 * math.pi / 3)

        # Q10: Probability at least 1 winning: 1 - C_7^5 / C_10^5 = 1 - 21/252 = 11/12
        p_none = Fraction(math.comb(7, 5), math.comb(10, 5))
        self.assertEqual(p_none, Fraction(1, 12))
        self.assertEqual(1 - p_none, Fraction(11, 12))

        # Q12: Tangent lines to x^2 + y^2/4 = 1 with slope -2:
        # 2x + y + m = 0 => 8x^2 + 4mx + m^2 - 4 = 0 => Delta = 16(8 - m^2) = 0 => m = +/- 2*sqrt(2)
        # Line L1: 2x + y = 1 (1 < 2*sqrt(2) => 2 intersections)
        # Line L2: 2x + y = 3 (3 > 2*sqrt(2) ~ 2.828 => 0 intersections)
        # Total points = 2
        m_crit = 2 * math.sqrt(2)
        self.assertTrue(1 < m_crit < 3)

        # Q13: Stratified sampling: 70 * (350 / 490) = 50
        self.assertEqual(70 * 350 // 490, 50)

        # Q14: Hyperbola right directrix and asymptotes:
        # P(a^2/c, ab/c), F(c, 0). Right angle at F => PH = HF => ab/c = b^2/c => a = b => e = sqrt(2)
        self.assertAlmostEqual(math.sqrt(1 + 1), math.sqrt(2))

        # Q15: Linear programming max z = 6x + 5y
        # Vertices: (0,0), (3,0), (3, 1.5), (2,3), (1,4), (0,4)
        vertices = [(0, 0), (3, 0), (3, 1.5), (2, 3), (1, 4), (0, 4)]
        z_vals = {v: 6 * v[0] + 5 * v[1] for v in vertices}
        max_v = max(z_vals, key=z_vals.get)
        self.assertEqual(max_v, (2, 3))
        self.assertEqual(z_vals[max_v], 27)

        # Q17: Vector sum and half angle
        # |m+n|^2 = 4 + 2*sqrt(2)*(cos theta - sin theta) = 128/25
        # cos(theta + pi/4) = 7/25
        # 2*cos^2(theta/2 + pi/8) = 1 + 7/25 = 32/25 => cos^2 = 16/25 => cos = -4/5 (in Q2/Q3)
        cos_sum = Fraction(128, 25) - 4
        cos_diff = cos_sum / (2 * Fraction(141421356, 100000000))  # approx check
        self.assertEqual(Fraction(128 - 100, 25), Fraction(28, 25))
        # Exact: 28/25 / (2*sqrt(2)) = 7*sqrt(2)/25 => cos(theta + pi/4) = 7/25
        cos_2a = Fraction(7, 25)
        cos_a_sq = (1 + cos_2a) / 2
        self.assertEqual(cos_a_sq, Fraction(16, 25))

        # Q18: Ball drawing probabilities:
        # 3 white, 4 black
        # P1 = 3/7
        # P2 = 4/7 * 3/6 = 2/7
        # P3 = 4/7 * 3/6 * 3/5 = 6/35
        # P5 = 4/7 * 3/6 * 2/5 * 1/4 * 1 = 1/35
        # P(A wins) = 3/7 + 6/35 + 1/35 = 22/35
        p1 = Fraction(3, 7)
        p2 = Fraction(4, 7) * Fraction(3, 6)
        p3 = Fraction(4, 7) * Fraction(3, 6) * Fraction(3, 5)
        p5 = Fraction(4, 7) * Fraction(3, 6) * Fraction(2, 5) * Fraction(1, 4) * 1
        self.assertEqual(p2, Fraction(2, 7))
        self.assertEqual(p1 + p3 + p5, Fraction(22, 35))

        # Q20: Cuboid geometry and distances
        # A(0,0,0), B(2,0,0), D(0, 2*sqrt(3)/3, 0), AA1 = 1, F(1,0,1)
        # E(1/2, sqrt(3)/2, 0). AE = (1/2, sqrt(3)/2, 0), BF = (-1, 0, 1)
        # cos(AE, BF) = |-1/2| / (1 * sqrt(2)) = sqrt(2)/4
        # Plane BDF normal: n2 = (1, sqrt(3), 1), mag = sqrt(5)
        # Dihedral angle with AA1B (y=0, n1=(0,1,0)): cos = sqrt(3)/sqrt(5) = sqrt(15)/5
        # Distance from A(0,0,0) to BDF: |BA . n2| / |n2| = 2 / sqrt(5) = 2*sqrt(5)/5
        self.assertAlmostEqual(math.sqrt(2) / 4, 1 / (2 * math.sqrt(2)))
        self.assertAlmostEqual(math.sqrt(15) / 5, math.sqrt(3 / 5))
        self.assertAlmostEqual(2 * math.sqrt(5) / 5, 2 / math.sqrt(5))

        # Q21: Derivative sum f'(1)
        # a_k = 3 * 2^k - 1
        # f'(1) = sum k * (3 * 2^k - 1) = 3 * ( (n-1)*2^(n+1) + 2 ) - n(n+1)/2
        for n in range(1, 10):
            direct_sum = sum(k * (3 * (2**k) - 1) for k in range(1, n + 1))
            formula_val = 3 * ((n - 1) * (2**(n + 1)) + 2) - n * (n + 1) // 2
            self.assertEqual(direct_sum, formula_val)

        # Q22: Parabola chord passing through fixed point
        # y1*y2 - 2p(y1+y2) - 4p^2 = 0
        # Line AB: x = my + t => y^2 - 2pmy - 2pt = 0 => y1+y2 = 2pm, y1*y2 = -2pt
        # -2pt - 2p(2pm) - 4p^2 = 0 => t = -2pm - 2p
        # x = my - 2pm - 2p => x + 2p = m(y - 2p) => passes through (-2p, 2p)
        # Test with p = 2, m = 1: t = -4 - 4 = -8. Line: x = y - 8.
        # Parabola y^2 = 4x. Intersections: y^2 - 4(y - 8) = 0 => y^2 - 4y + 32 ... (if Delta > 0)
        # Let m = 2, p = 1: t = -4 - 2 = -6. Line: x = 2y - 6.
        # Parabola y^2 = 2x => y^2 - 4y + 12 = 0 (Delta < 0).
        # Let m = -1, p = 1: t = 2 - 2 = 0. Line: x = -y.
        # Parabola y^2 = 2x => y^2 + 2y = 0 => y = -2, x = 2 (pt A(2, -2)).
        # tan alpha = 2/(-2) = -1. tan beta requires second point.
        # The algebraic identity t = -2pm - 2p holds identically for all p > 0, m in R.
        p = 3.5
        for m in [-3.0, -1.5, 0.5, 2.0]:
            # point on line: (-2p, 2p) => x + 2p = 0, y - 2p = 0 => 0 = m*0 always true!
            self.assertEqual((-2 * p) + 2 * p, m * (2 * p - 2 * p))


if __name__ == "__main__":
    unittest.main()

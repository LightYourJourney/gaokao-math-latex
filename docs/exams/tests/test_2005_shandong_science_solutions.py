# -*- coding: utf-8 -*-
"""2005 年高考数学真题（山东卷理科 gk-2005-regular-shandong-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_山东理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_山东理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_山东理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_山东理科_含解析.md"


class Shandong2005ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性（全卷共 22 题）。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 23)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 23)))

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-12 题：D B B D C C A D D A A B）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "B", "B", "D", "C", "C", "A", "D", "D", "A", "A", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（13-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"\dfrac{3}{2}", answers)
        self.assertIn(r"\sqrt{2}", answers)
        self.assertIn(r"(2, 3)", answers)
        self.assertIn(r"③④", answers)

        # 解答题
        self.assertIn(r"-\dfrac{4}{5}", answers)
        self.assertIn(r"3", answers)
        self.assertIn(r"\dfrac{22}{35}", answers)
        self.assertIn(r"n = 3m + 6", answers)
        self.assertIn(r"\left(-\dfrac{4}{3}, 0\right)", answers)
        self.assertIn(r"\arccos\dfrac{\sqrt{2}}{4}", answers)
        self.assertIn(r"\arccos\dfrac{\sqrt{15}}{5}", answers)
        self.assertIn(r"\dfrac{2\sqrt{5}}{5}", answers)
        self.assertIn(r"3(n-1)2^{n+1} + 6 - \dfrac{n(n+1)}{2}", answers)
        self.assertIn(r"y^2 = 2px", answers)
        self.assertIn(r"(-2p, 2p\cot\theta)", answers)

    def test_mathematical_verifications(self):
        """针对全卷核心计算进行独立算法复算。"""
        # Q01: (1-i)/(1+i)^2 + (1+i)/(1-i)^2 = (1-i)/(2i) + (1+i)/(-2i) = (-2i)/(2i) = -1
        i = 1j
        z1 = (1 - i) / ((1 + i)**2)
        z2 = (1 + i) / ((1 - i)**2)
        self.assertAlmostEqual((z1 + z2).real, -1.0)
        self.assertAlmostEqual((z1 + z2).imag, 0.0)

        # Q05: (3 - 1)^n = 128 => 2^n = 128 => n = 7
        # Term of x^(-3): 7 - 5/3*r = -3 => r = 6. Coeff: C_7^6 * 3^1 * (-1)^6 = 21
        self.assertEqual(math.comb(7, 6) * 3 * ((-1)**6), 21)

        # Q06: f(1) = e^0 = 1 => f(a) = 1.
        # a >= 0: e^(a-1) = 1 => a = 1.
        # -1 < a < 0: sin(pi * a^2) = 1 => pi * a^2 = pi/2 => a^2 = 1/2 => a = -sqrt(2)/2
        self.assertAlmostEqual(math.sin(math.pi * (-math.sqrt(0.5))**2), 1.0)

        # Q07: BD = BC + CD = (-5a+6b) + (7a-2b) = 2a + 4b = 2 * AB
        # Collinear: A, B, D
        self.assertEqual((-5 + 7, 6 - 2), (2, 4))

        # Q08: Spherical distance: 45 deg N to 75 deg S => theta = 120 deg = 2*pi/3 rad
        self.assertAlmostEqual(45 + 75, 120)
        self.assertAlmostEqual(120 * math.pi / 180, 2 * math.pi / 3)

        # Q09: Probability at least 1 winning: 1 - C_7^5 / C_10^5 = 1 - 21/252 = 11/12
        p_none = Fraction(math.comb(7, 5), math.comb(10, 5))
        self.assertEqual(p_none, Fraction(1, 12))
        self.assertEqual(1 - p_none, Fraction(11, 12))

        # Q11: Logarithmic inequality: |log_{1+a}(1-a)| + |log_{1-a}(1+a)| > 2 for all 0 < a < 1
        for a_val in [0.1, 0.3, 0.5, 0.7, 0.9]:
            x = math.log(1 - a_val, 1 + a_val)
            inv_x = math.log(1 + a_val, 1 - a_val)
            val = abs(x) + abs(inv_x)
            self.assertTrue(val > 2.0)

        # Q12: Ellipse tangent lines and triangle area
        m_crit = 2 * math.sqrt(2)
        self.assertTrue(1 < m_crit < 3)

        # Q13: Limit of (C_n^2 + 2 C_n^{n-2}) / (n+1)^2 = 3/2
        # Exact: 3 * n * (n-1) / (2 * (n+1)^2) -> 3/2 as n -> infty
        for n_val in [1000, 10000, 100000]:
            c_val = math.comb(n_val, 2)
            ratio = (c_val + 2 * c_val) / ((n_val + 1)**2)
            self.assertAlmostEqual(ratio, 1.5, places=1)
        self.assertAlmostEqual(
            (math.comb(100000, 2) * 3) / ((100000 + 1)**2),
            1.5,
            places=3
        )

        # Q14: Hyperbola right directrix and asymptotes: e = sqrt(2)
        self.assertAlmostEqual(math.sqrt(1 + 1), math.sqrt(2))

        # Q15: Linear programming max z = 6x + 5y
        vertices = [(0, 0), (3, 0), (3, 1.5), (2, 3), (1, 4), (0, 4)]
        z_vals = {v: 6 * v[0] + 5 * v[1] for v in vertices}
        max_v = max(z_vals, key=z_vals.get)
        self.assertEqual(max_v, (2, 3))
        self.assertEqual(z_vals[max_v], 27)

        # Q17: Vector sum and half angle
        cos_sum = Fraction(128, 25) - 4
        self.assertEqual(cos_sum, Fraction(28, 25))
        cos_2a = Fraction(7, 25)
        cos_a_sq = (1 + cos_2a) / 2
        self.assertEqual(cos_a_sq, Fraction(16, 25))

        # Q18: Ball drawing probabilities:
        # 3 white, 4 black. xi in {1, 2, 3, 4, 5}
        p_xi = [
            Fraction(3, 7),
            Fraction(4, 7) * Fraction(3, 6),
            Fraction(4, 7) * Fraction(3, 6) * Fraction(3, 5),
            Fraction(4, 7) * Fraction(3, 6) * Fraction(2, 5) * Fraction(3, 4),
            Fraction(4, 7) * Fraction(3, 6) * Fraction(2, 5) * Fraction(1, 4) * Fraction(3, 3),
        ]
        self.assertEqual(p_xi[0], Fraction(3, 7))
        self.assertEqual(p_xi[1], Fraction(2, 7))
        self.assertEqual(p_xi[2], Fraction(6, 35))
        self.assertEqual(p_xi[3], Fraction(3, 35))
        self.assertEqual(p_xi[4], Fraction(1, 35))
        self.assertEqual(sum(p_xi), 1)
        # Jia draws at 1, 3, 5:
        p_jia = p_xi[0] + p_xi[2] + p_xi[4]
        self.assertEqual(p_jia, Fraction(22, 35))

        # Q19: Tangent slope f'(x) > 3m on [-1, 1]
        # g(x) = mx^2 - 2(m+1)x + 2 > 0 on [-1, 1]. For m < 0, concave:
        # g(-1) = 3m + 4 > 0 => m > -4/3
        # g(1) = -m > 0 => m < 0
        # Range is (-4/3, 0)
        for m_test in [-1.3, -1.0, -0.5, -0.1]:
            # Minimum on [-1, 1] is at endpoints
            g_neg1 = 3 * m_test + 4
            g_pos1 = -m_test
            self.assertTrue(g_neg1 > 0 and g_pos1 > 0)

        # Q20: Cuboid geometry and distances
        self.assertAlmostEqual(math.sqrt(2) / 4, 1 / (2 * math.sqrt(2)))
        self.assertAlmostEqual(math.sqrt(15) / 5, math.sqrt(3 / 5))
        self.assertAlmostEqual(2 * math.sqrt(5) / 5, 2 / math.sqrt(5))

        # Q21: Derivative sum f'(1) and comparison with 23n^2 - 13n
        for n in range(1, 10):
            direct_sum = sum(k * (3 * (2**k) - 1) for k in range(1, n + 1))
            formula_val = 3 * ((n - 1) * (2**(n + 1)) + 2) - n * (n + 1) // 2
            self.assertEqual(direct_sum, formula_val)

            diff = 2 * formula_val - (23 * (n**2) - 13 * n)
            if n == 1:
                self.assertEqual(diff, 0)
            elif n == 2:
                self.assertTrue(diff < 0)
            else:
                self.assertTrue(diff > 0)

        # Q22: Parabola chord passing through fixed point (-2p, 2p*cot theta)
        for theta_deg in [30, 45, 60, 90, 120, 135]:
            theta_rad = math.radians(theta_deg)
            cot_theta = 1.0 / math.tan(theta_rad)
            p = 2.5
            # Line equation: (x + 2p) - (y1 + y2)/(2p) * (y - 2p*cot theta) = 0
            # Fixed point (x0, y0) = (-2p, 2p*cot_theta) satisfies equation for ANY y1+y2:
            x0 = -2 * p
            y0 = 2 * p * cot_theta
            for y_sum in [-5.0, 0.0, 3.2, 7.8]:
                val = (x0 + 2 * p) - (y_sum / (2 * p)) * (y0 - 2 * p * cot_theta)
                self.assertAlmostEqual(val, 0.0)


if __name__ == "__main__":
    unittest.main()

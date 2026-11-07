# -*- coding: utf-8 -*-
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_福建理科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_福建理科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_福建理科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_福建理科_含解析.md"


class Fujian2004ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 164–165 的两页题面，不附官方答案", solutions)
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
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["A", "C", "D", "B", "B", "B", "C", "B", "A", "D", "D", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        # Fill-in answers (Q13 - Q16)
        self.assertIn(r"4\sqrt{5}", answers)
        self.assertIn(r"\dfrac{1}{2}", answers)
        self.assertIn("①③", answers)
        self.assertIn(r"\dfrac{2}{3}", answers)

        # Solution key answers (Q17 - Q22)
        self.assertIn(r"-\dfrac{\pi}{4}", answers)
        self.assertIn(r"m = -\dfrac{\pi}{12}, n = 1", answers)
        self.assertIn(r"\mathrm{E}\xi = \dfrac{9}{5}", answers)
        self.assertIn(r"\dfrac{44}{45}", answers)
        self.assertIn(r"\arccos\dfrac{1}{3}", answers)
        self.assertIn(r"\dfrac{4\sqrt{2}}{3}", answers)
        self.assertIn(r"A_n = 490n - 10n^2", answers)
        self.assertIn(r"B_n = 500n - 100 - \dfrac{500}{2^n}", answers)
        self.assertIn("4", answers)
        self.assertIn(r"A = \{a \mid -1 \leqslant a \leqslant 1\}", answers)
        self.assertIn(r"m \leqslant -2", answers)
        self.assertIn(r"y = x^2 + \dfrac{1}{2x^2} + 1", answers)
        self.assertIn(r"(2, +\infty)", answers)

        # Analytical derivations inside solutions
        self.assertIn(r"2\sin\left(2x + \frac{\pi}{6}\right) + 1", solutions)
        self.assertIn(r"\vec{a} \cdot \vec{b}", solutions)
        self.assertIn(r"d + |MC| = |MM'| + |MC| \geqslant |CH|", solutions)

    def test_mathematical_verifications(self):
        # Q1: ((1 - i)/(1 + i))^10 = (-i)^10 = -1
        c = (1 - 1j) / (1 + 1j)
        self.assertAlmostEqual(c.imag, -1.0)
        self.assertAlmostEqual((c**10).real, -1.0)

        # Q2: tan 15° + cot 15° = 4
        rad15 = math.radians(15)
        self.assertAlmostEqual(math.tan(rad15) + 1 / math.tan(rad15), 4.0)

        # Q6: 6 classes, 4 students into 2 classes (2 each)
        ways = math.comb(6, 2) * math.comb(4, 2)
        self.assertEqual(ways, 90)
        self.assertEqual(0.5 * (6 * 5) * math.comb(4, 2), 90)

        # Q10: Sphere surface 48*pi => R = sqrt(12) = 2*sqrt(3).
        # Triangle ABC: AB=2, BC=4, angle B=60° => AC = sqrt(4 + 16 - 2*2*4*cos(60°)) = 2*sqrt(3).
        # Right triangle with circumradius r = BC / 2 = 2.
        # Line OA with plane ABC: cos(theta) = r / R = 2 / (2*sqrt(3)) = sqrt(3)/3.
        R_sphere = math.sqrt(48 / 4)
        ac_len = math.sqrt(2**2 + 4**2 - 2 * 2 * 4 * math.cos(math.radians(60)))
        self.assertAlmostEqual(ac_len, 2 * math.sqrt(3))
        r_circum = 4 / 2
        cos_theta = r_circum / R_sphere
        self.assertAlmostEqual(cos_theta, math.sqrt(3) / 3)

        # Q12: Hyperbola focal-directrix property gives min cost 5a
        # C is at (2 + 2*sin(30°), 2*cos(30°)) = (3, sqrt(3))
        # Directrix is at x = 1/2. Distance = 3 - 0.5 = 2.5.
        # Cost factor = 2a * 2.5 = 5a.
        c_x = 2 + 2 * math.sin(math.radians(30))
        dist_directrix = c_x - 0.5
        min_cost_ratio = 2 * dist_directrix
        self.assertAlmostEqual(min_cost_ratio, 5.0)

        # Q13: Circle (x-3)^2 + (y-1)^2 = 25, line x + 2y = 0
        # d = |3 + 2| / sqrt(5) = sqrt(5)
        # chord = 2 * sqrt(25 - 5) = 4 * sqrt(5)
        d_center = abs(3 + 2 * 1) / math.sqrt(1**2 + 2**2)
        chord = 2 * math.sqrt(25 - d_center**2)
        self.assertAlmostEqual(chord, 4 * math.sqrt(5))

        # Q16: V(x) = (9/4) * (x^2 - x^3), V'(x) = 0 => x = 2/3
        def v(x):
            return 9.0 / 4.0 * (x**2 - x**3)
        self.assertGreater(v(2 / 3), v(2 / 3 - 0.01))
        self.assertGreater(v(2 / 3), v(2 / 3 + 0.01))

        # Q18: Discrete distribution and expectation
        total_comb = math.comb(10, 3)
        p0 = math.comb(6, 0) * math.comb(4, 3) / total_comb
        p1 = math.comb(6, 1) * math.comb(4, 2) / total_comb
        p2 = math.comb(6, 2) * math.comb(4, 1) / total_comb
        p3 = math.comb(6, 3) * math.comb(4, 0) / total_comb
        self.assertAlmostEqual(p0 + p1 + p2 + p3, 1.0)
        ex = 0 * p0 + 1 * p1 + 2 * p2 + 3 * p3
        self.assertAlmostEqual(ex, 9 / 5)
        p_a_fail = p0 + p1  # 40/120 = 1/3
        self.assertAlmostEqual(p_a_fail, 1 / 3)
        p_b_fail = (math.comb(8, 1) * math.comb(2, 2)) / total_comb  # 8/120 = 1/15
        self.assertAlmostEqual(p_b_fail, 1 / 15)
        p_at_least_one = 1 - p_a_fail * p_b_fail
        self.assertAlmostEqual(p_at_least_one, 44 / 45)

        # Q19: Pyramid dihedral angle and distance
        # Normal CMN n2 = (sqrt(2), sqrt(6), -1)
        # Normal base n1 = (0, 0, 1)
        # cos(theta) = |-1| / (1 * 3) = 1/3
        n2 = (math.sqrt(2), math.sqrt(6), -1)
        norm_n2 = math.sqrt(sum(k**2 for k in n2))
        self.assertAlmostEqual(norm_n2, 3.0)
        cos_dihedral = abs(n2[2]) / norm_n2
        self.assertAlmostEqual(cos_dihedral, 1 / 3)
        # Vector CB = (-2, 2*sqrt(3), 0)
        cb_dot_n2 = -2 * math.sqrt(2) + 2 * math.sqrt(3) * math.sqrt(6) + 0
        dist_b = abs(cb_dot_n2) / norm_n2
        self.assertAlmostEqual(dist_b, 4 * math.sqrt(2) / 3)

        # Q20: Technical upgrade profit crossover year
        # f(n) = n^2 + n - 10 - 50 / (2^n)
        def f_n(n):
            return n**2 + n - 10 - 50 / (2**n)
        self.assertLess(f_n(1), 0)
        self.assertLess(f_n(2), 0)
        self.assertLess(f_n(3), 0)
        self.assertGreater(f_n(4), 0)

        # Q21: Root distance max over a in [-1, 1] is sqrt(1 + 8) = 3
        # m^2 + t*m - 2 >= 0 for t in [-1, 1] requires m >= 2 or m <= -2
        def h_val(m, t):
            return m**2 + t * m - 2
        for m_test in [2.0, 2.5, -2.0, -3.0]:
            self.assertGreaterEqual(h_val(m_test, -1), 0)
            self.assertGreaterEqual(h_val(m_test, 1), 0)
        for m_test in [1.9, 0.0, -1.9]:
            min_val = min(h_val(m_test, -1), h_val(m_test, 1))
            self.assertLess(min_val, 0)

        # Q22: Distance ratio sum = 2*(k^2 + b) / |b|
        # For b > 0, 2*k^2/b + 2 > 2.
        # For b < 0, let b = -B (B>0), k^2 > 2B => 2*(k^2 - B)/B = 2*k^2/B - 2 > 4 - 2 = 2.
        for b_val in [1.0, 3.0, 0.5]:
            for k_val in [0.1, 1.0, 5.0]:
                ratio_sum = 2 * (k_val**2 + b_val) / abs(b_val)
                self.assertGreater(ratio_sum, 2.0)
        for b_neg in [-1.0, -2.0]:
            # k^2 > -2*b_neg
            min_k_sq = -2 * b_neg
            for delta in [0.01, 1.0, 10.0]:
                k_val = math.sqrt(min_k_sq + delta)
                ratio_sum = 2 * (k_val**2 + b_neg) / abs(b_neg)
                self.assertGreater(ratio_sum, 2.0)


if __name__ == "__main__":
    unittest.main()

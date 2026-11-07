# -*- coding: utf-8 -*-
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_福建文科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_福建文科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_福建文科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_福建文科_含解析.md"


class Fujian2004ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 166–167 的两页题面，不附官方答案", solutions)
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
        expected_choices = ["A", "C", "D", "B", "A", "B", "C", "B", "C", "D", "C", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        # Fill-in answers (Q13 - Q16)
        self.assertIn(r"4\sqrt{5}", answers)
        self.assertIn(r"(-\infty, -1)", answers)
        self.assertIn("63", answers)
        self.assertIn(r"\dfrac{2}{3}", answers)

        # Solution key answers (Q17 - Q22)
        self.assertIn(r"-\dfrac{\pi}{4}", answers)
        self.assertIn(r"m = -\dfrac{\pi}{12}, n = 1", answers)
        self.assertIn(r"\dfrac{2}{3}", answers)
        self.assertIn(r"\dfrac{14}{15}", answers)
        self.assertIn(r"\dfrac{44}{45}", answers)
        self.assertIn(r"\arccos\dfrac{\sqrt{5}}{5}", answers)
        self.assertIn(r"\dfrac{4\sqrt{5}}{5}", answers)
        self.assertIn(r"A_n = 490n - 10n^2", answers)
        self.assertIn(r"B_n = 500n - 100 - \dfrac{500}{2^n}", answers)
        self.assertIn("4", answers)
        self.assertIn(r"x + 2y - 6 = 0", answers)
        self.assertIn(r"y = x^2 + \dfrac{1}{2x^2} + 1", answers)
        self.assertIn(r"\sqrt{2} + 1", answers)
        self.assertIn(r"A = \{a \mid -1 \leqslant a \leqslant 1\}", answers)
        self.assertIn(r"m \leqslant -2", answers)

        # Analytical derivations inside solutions
        self.assertIn(r"2\sin\left(2x + \frac{\pi}{6}\right) + 1", solutions)
        self.assertIn(r"\vec{a} \cdot \vec{b}", solutions)
        self.assertIn(r"|MA| - |MB| = 2", solutions)
        self.assertIn(r"(2\sqrt{7} - 2)a", solutions)

    def test_mathematical_verifications(self):
        # Q1: U = {1, 2, 3, 4, 5}, A = {1, 3, 5}, B = {2, 3, 5}
        u = {1, 2, 3, 4, 5}
        a_set = {1, 3, 5}
        b_set = {2, 3, 5}
        self.assertEqual(u - (a_set & b_set), {1, 2, 4})

        # Q2: tan 15° + cot 15° = 4
        rad15 = math.radians(15)
        self.assertAlmostEqual(math.tan(rad15) + 1 / math.tan(rad15), 4.0)

        # Q5: AP S_9 / S_5 = (9/5) * (a_5 / a_3) = (9/5) * (5/9) = 1
        self.assertEqual(9 / 5 * (5 / 9), 1.0)

        # Q9: (x - a/x)^8 constant term is C_8^4 * a^4 = 70*a^4 = 1120 => a^4 = 16 => a = +/- 2
        comb8_4 = math.comb(8, 4)
        self.assertEqual(comb8_4, 70)
        self.assertEqual(1120 / 70, 16.0)
        self.assertEqual((1 - 2)**8, 1)
        self.assertEqual((1 - (-2))**8, 3**8)

        # Q10: Sphere surface 48*pi => R = 2*sqrt(3).
        # Triangle ABC: AB=2, BC=4, angle B=60° => AC = 2*sqrt(3).
        # Right triangle with circumradius r = BC / 2 = 2.
        # Line OA with plane ABC: cos(theta) = r / R = 2 / (2*sqrt(3)) = sqrt(3)/3.
        R_sphere = math.sqrt(48 / 4)
        ac_len = math.sqrt(2**2 + 4**2 - 2 * 2 * 4 * math.cos(math.radians(60)))
        self.assertAlmostEqual(ac_len, 2 * math.sqrt(3))
        r_circum = 4 / 2
        cos_theta = r_circum / R_sphere
        self.assertAlmostEqual(cos_theta, math.sqrt(3) / 3)

        # Q11: Even function with period 2, on [0, 1] f(x) = 2 - x (strictly decreasing)
        # 1 rad in (pi/4, pi/2) => sin 1 > cos 1 > 0 => f(sin 1) < f(cos 1)
        self.assertGreater(math.sin(1), math.cos(1))
        self.assertGreater(math.cos(1), 0)

        # Q12: Hyperbola right branch |MA| - |MB| = 2.
        # A(-2, 0), B(2, 0), C(3, sqrt(3)).
        # |AC| = sqrt(5^2 + 3) = sqrt(28) = 2*sqrt(7).
        # Min cost W = a*(|MB| + |MC|) = a*(|MA| - 2 + |MC|) >= a*(|AC| - 2) = (2*sqrt(7) - 2)*a.
        ac_dist = math.sqrt((3 - (-2))**2 + (math.sqrt(3) - 0)**2)
        self.assertAlmostEqual(ac_dist, 2 * math.sqrt(7))
        self.assertAlmostEqual(ac_dist - 2, 2 * math.sqrt(7) - 2)

        # Q13: Circle (x-3)^2 + (y-1)^2 = 25, line x + 2y = 0
        d_center = abs(3 + 2 * 1) / math.sqrt(1**2 + 2**2)
        chord = 2 * math.sqrt(25 - d_center**2)
        self.assertAlmostEqual(chord, 4 * math.sqrt(5))

        # Q14: f(a) > a => a < -1
        # For a in [-0.9, -0.5, 0, 1], f(a) <= a
        def f_piecewise(x):
            return 0.5 * x - 1 if x >= 0 else 1.0 / x
        for val in [-2.0, -1.5, -1.01]:
            self.assertGreater(f_piecewise(val), val)
        for val in [-1.0, -0.5, 0.0, 2.0]:
            self.assertLessEqual(f_piecewise(val), val)

        # Q15: System sampling, group 7 is 60..69, m = 6, k = 7 => (6 + 7) % 10 = 3 => 63
        self.assertEqual(60 + (6 + 7) % 10, 63)

        # Q16: V(x) = (9/4) * (x^2 - x^3), V'(x) = 0 => x = 2/3
        def v(x):
            return 9.0 / 4.0 * (x**2 - x**3)
        self.assertGreater(v(2 / 3), v(2 / 3 - 0.01))
        self.assertGreater(v(2 / 3), v(2 / 3 + 0.01))

        # Q18: Oral exam probabilities
        total_comb = math.comb(10, 3)
        p_jia = (math.comb(6, 2) * math.comb(4, 1) + math.comb(6, 3)) / total_comb
        self.assertAlmostEqual(p_jia, 2 / 3)
        p_yi = (math.comb(8, 2) * math.comb(2, 1) + math.comb(8, 3)) / total_comb
        self.assertAlmostEqual(p_yi, 14 / 15)
        p_at_least_one = 1 - (1 - p_jia) * (1 - p_yi)
        self.assertAlmostEqual(p_at_least_one, 44 / 45)

        # Q19: Pyramid dihedral angle and distance
        # Base normal n1 = (0, 0, 1)
        # SCM normal n2 = (1, -sqrt(3), -1)
        # cos(theta) = |-1| / (1 * sqrt(1 + 3 + 1)) = 1/sqrt(5) = sqrt(5)/5
        n2 = (1, -math.sqrt(3), -1)
        norm_n2 = math.sqrt(sum(k**2 for k in n2))
        self.assertAlmostEqual(norm_n2, math.sqrt(5))
        cos_dihedral = abs(n2[2]) / norm_n2
        self.assertAlmostEqual(cos_dihedral, math.sqrt(5) / 5)
        # Vector CB = (2, 2*sqrt(3), 0)
        cb_dot_n2 = 2 * 1 + 2 * math.sqrt(3) * (-math.sqrt(3)) + 0
        dist_b = abs(cb_dot_n2) / norm_n2
        self.assertAlmostEqual(dist_b, 4 * math.sqrt(5) / 5)

        # Q20: Technical upgrade profit crossover year
        def f_n(n):
            return n**2 + n - 10 - 50 / (2**n)
        self.assertLess(f_n(1), 0)
        self.assertLess(f_n(2), 0)
        self.assertLess(f_n(3), 0)
        self.assertGreater(f_n(4), 0)

        # Q21: Parabola y = 0.5 * x^2
        # P(x0, 0.5*x0^2), normal slope k = -1/x0
        # M(x, y): x = -1/x0, y = x^2 + 1/(2*x^2) + 1
        # Min y = 2*sqrt(0.5) + 1 = sqrt(2) + 1
        min_y = 2 * math.sqrt(0.5) + 1
        self.assertAlmostEqual(min_y, math.sqrt(2) + 1)

        # Q22: f'(x) = -2(x^2 - ax - 2) >= 0 on [-1, 1] => a in [-1, 1]
        # |x1 - x2| = sqrt(a^2 + 8) in [2*sqrt(2), 3]
        # m^2 + t*m - 2 >= 0 for t in [-1, 1] => m >= 2 or m <= -2
        def h_val(m, t):
            return m**2 + t * m - 2
        for m_test in [2.0, 2.5, -2.0, -3.0]:
            self.assertGreaterEqual(h_val(m_test, -1), 0)
            self.assertGreaterEqual(h_val(m_test, 1), 0)
        for m_test in [1.9, 0.0, -1.9]:
            min_val = min(h_val(m_test, -1), h_val(m_test, 1))
            self.assertLess(min_val, 0)


if __name__ == "__main__":
    unittest.main()

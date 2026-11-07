# -*- coding: utf-8 -*-
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_湖北文科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_湖北文科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_湖北文科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_湖北文科_含解析.md"


class Hubei2004ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 172–173 的两页题面，不附官方答案", solutions)
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
        expected_choices = ["D", "D", "A", "B", "C", "C", "B", "D", "C", "D", "B", "A"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        # Fill-in answers (Q13 - Q16)
        self.assertIn(r"\dfrac{\sqrt{3}}{3}", answers)
        self.assertIn("0", answers)
        self.assertIn("192", answers)
        self.assertIn("④", answers)

        # Solution key answers (Q17 - Q22)
        self.assertIn(r"\dfrac{5\sqrt{3} - 12}{26}", answers)
        self.assertIn(r"\arccos\left(-\dfrac{1}{3}\right)", answers)
        self.assertIn(r"\theta = 0", answers)
        self.assertIn(r"(-2, -\sqrt{2})", answers)
        self.assertIn(r"-\dfrac{6 + \sqrt{6}}{5}", answers)
        self.assertIn("0.976", answers)
        self.assertIn("100", answers)
        self.assertIn(r"b = 2\sqrt{c} - 1", answers)
        self.assertIn(r"(0, 7 - 4\sqrt{3}) \cup (7 + 4\sqrt{3}, +\infty)", answers)

        # Analytical derivations inside solutions
        self.assertIn(r"a^2(\cos\theta - 1)", solutions)
        self.assertIn(r"5k^2 + 2\sqrt{6}k - 6 = 0", solutions)
        self.assertIn(r"c - 4\sqrt{c} + 1 > 0", solutions)

    def test_mathematical_verifications(self):
        # Q1: A = {sqrt(5k+1) | k in N}, B = {x <= 6, x in Q}
        # k=0: 1; k=3: 4; k=7: 6.
        a_elements = []
        for k in range(10):
            val = math.isqrt(5 * k + 1)
            if val * val == 5 * k + 1:
                a_elements.append(val)
        a_cap_b = [x for x in a_elements if x <= 6]
        self.assertEqual(a_cap_b, [1, 4, 6])

        # Q2: Section formula lambda = 3/2
        # M1(6, 2), M2(1, 7) => M = ( (6 + 1.5*1)/2.5, (2 + 1.5*7)/2.5 ) = (3, 5)
        # 5 = 3m - 7 => 3m = 12 => m = 4
        xm = (6 + 1.5 * 1) / 2.5
        ym = (2 + 1.5 * 7) / 2.5
        self.assertAlmostEqual(xm, 3.0)
        self.assertAlmostEqual(ym, 5.0)
        m = (ym + 7) / xm
        self.assertAlmostEqual(m, 4.0)

        # Q3: f'(1) = 3
        # f(x) = (x-1)^2 + 3(x-1) => f'(1) = 3
        def f_test(x):
            return (x - 1)**2 + 3 * (x - 1)
        h = 1e-6
        num_deriv = (f_test(1 + h) - f_test(1 - h)) / (2 * h)
        self.assertAlmostEqual(num_deriv, 3.0, places=5)

        # Q4: Circles C1: center (-1, -1), r=2. C2: center (2, 1), r=2.
        # dist = sqrt(3^2 + 2^2) = sqrt(13) approx 3.605 in (0, 4) => 2 common tangents
        dist_c = math.sqrt((2 - (-1))**2 + (1 - (-1))**2)
        self.assertTrue(0 < dist_c < 4)

        # Q6: Tetrahedron centroid homothety ratio = -1/3 => Area ratio = 1/9
        self.assertAlmostEqual((1 / 3)**2, 1 / 9)

        # Q8: f(x) = (x^2 - 4x + 5)/(2x - 4) = 0.5*(t + 1/t) with t = x - 2 >= 0.5
        # Min at t = 1 (x = 3) is 1.0
        def f_q8(x):
            return (x**2 - 4 * x + 5) / (2 * x - 4)
        self.assertAlmostEqual(f_q8(3), 1.0)
        self.assertGreater(f_q8(2.5), 1.0)
        self.assertGreater(f_q8(4.0), 1.0)

        # Q9: S_n = a[2 - (1/2)^{n-1}] - b[2 - (n+1)(1/2)^{n-1}]
        # a_n = (-bn + a + b)(1/2)^{n-1}
        a_param, b_param = 3.0, 2.0
        def s_n(n):
            return a_param * (2 - (0.5)**(n - 1)) - b_param * (2 - (n + 1) * (0.5)**(n - 1))
        def a_n_formula(n):
            return (-b_param * n + a_param + b_param) * (0.5)**(n - 1)
        self.assertAlmostEqual(s_n(1), a_n_formula(1))
        for n in range(2, 6):
            self.assertAlmostEqual(s_n(n) - s_n(n - 1), a_n_formula(n))

        # Q10: 1 < 1/a < 1/b => 0 < b < a < 1
        # log_a(b) > 1 and log_b(a) in (0, 1)
        a_val, b_val = 0.5, 0.25
        log_a_b = math.log(b_val, a_val)
        log_b_a = math.log(a_val, b_val)
        self.assertGreater(log_a_b, 1.0)
        self.assertTrue(0 < log_b_a < 1.0)
        self.assertEqual(abs(log_a_b) + abs(log_b_a), abs(log_a_b + log_b_a))

        # Q11: Balls into boxes with exactly 3 mismatched
        # C(10, 3) * D_3 = 120 * 2 = 240
        self.assertEqual(math.comb(10, 3) * 2, 240)

        # Q12: Tidal model y = 12 + 3*sin(pi*t/6)
        def y_tide(t):
            return 12 + 3 * math.sin(math.pi * t / 6)
        self.assertAlmostEqual(y_tide(0), 12.0)
        self.assertAlmostEqual(y_tide(3), 15.0)
        self.assertAlmostEqual(y_tide(6), 12.0)
        self.assertAlmostEqual(y_tide(9), 9.0)
        self.assertAlmostEqual(y_tide(12), 12.0)

        # Q13: tan 2010° = tan 30° = sqrt(3)/3
        self.assertAlmostEqual(math.tan(math.radians(2010)), math.sqrt(3) / 3)

        # Q14: (x^{1/2} + x^{-1/2})^7 has terms with powers 7/2, 5/2, ..., -7/2, never 5
        powers = [(7 - 2 * r) / 2 for r in range(8)]
        self.assertNotIn(5.0, powers)

        # Q15: Stratified sampling: 2400 * (80 / 1000) = 192
        self.assertEqual(2400 * 80 / 1000, 192.0)

        # Q17: tan alpha = -2/3
        # sin 2alpha = -12/13, cos 2alpha = 5/13
        # sin(2alpha + pi/3) = (-12/13)*0.5 + (5/13)*(sqrt(3)/2) = (5*sqrt(3) - 12) / 26
        t_alpha = -2 / 3
        sin2a = 2 * t_alpha / (1 + t_alpha**2)
        cos2a = (1 - t_alpha**2) / (1 + t_alpha**2)
        self.assertAlmostEqual(sin2a, -12 / 13)
        self.assertAlmostEqual(cos2a, 5 / 13)
        res_q17 = sin2a * 0.5 + cos2a * (math.sqrt(3) / 2)
        self.assertAlmostEqual(res_q17, (5 * math.sqrt(3) - 12) / 26)

        # Q18: Dihedral angle cos(theta) = -1/3
        # BH = sqrt(6)/4, CH = sqrt(6)/4, BC = 1
        bh = math.sqrt(6) / 4
        cos_dihedral = (bh**2 + bh**2 - 1) / (2 * bh * bh)
        self.assertAlmostEqual(cos_dihedral, -1 / 3)

        # Q19: BP . CQ = a^2 * (cos theta - 1) <= 0, max 0 at theta = 0
        for th in [0.0, 0.5, 1.0, math.pi]:
            self.assertLessEqual(math.cos(th) - 1, 0.0)

        # Q20: (2 - k^2)x^2 - 2kx - 2 = 0
        # Right branch: Delta = 16 - 4k^2 > 0 => k^2 < 4
        # x1 * x2 = -2 / (2 - k^2) > 0 => 2 - k^2 < 0 => k^2 > 2
        # x1 + x2 = 2k / (2 - k^2) > 0 => 2k < 0 => k < 0
        # So k in (-2, -sqrt(2))
        # Equation for circle through F: 5k^2 + 2*sqrt(6)*k - 6 = 0
        # Roots: (-sqrt(6) +/- 6) / 5
        k_pos = (-math.sqrt(6) + 6) / 5
        k_neg = (-math.sqrt(6) - 6) / 5
        self.assertGreater(k_pos, 0)
        self.assertTrue(-2 < k_neg < -math.sqrt(2))

        # Q21: Prevention cost <= 120
        # Scheme {Yi, Bing, Ding}: cost = 60 + 30 + 10 = 100 <= 120, P = 1 - 0.2*0.3*0.4 = 0.976
        # Scheme {Jia, Bing}: cost = 90 + 30 = 120, P = 1 - 0.1*0.3 = 0.970
        p_ybd = 1 - 0.2 * 0.3 * 0.4
        p_jb = 1 - 0.1 * 0.3
        self.assertAlmostEqual(p_ybd, 0.976)
        self.assertAlmostEqual(p_jb, 0.970)
        self.assertGreater(p_ybd, p_jb)

        # Q22: (b + 1)^2 = 4c => b = 2*sqrt(c) - 1
        # Extrema exist <=> Delta_F' = 4(b^2 - 3c) > 0 <=> c - 4*sqrt(c) + 1 > 0
        # Roots of t^2 - 4t + 1 = 0 are 2 +/- sqrt(3)
        # c in (0, 7 - 4*sqrt(3)) U (7 + 4*sqrt(3), +inf)
        t1 = 2 - math.sqrt(3)
        t2 = 2 + math.sqrt(3)
        c1 = (2 - math.sqrt(3))**2
        c2 = (2 + math.sqrt(3))**2
        self.assertAlmostEqual(c1, 7 - 4 * math.sqrt(3))
        self.assertAlmostEqual(c2, 7 + 4 * math.sqrt(3))


if __name__ == "__main__":
    unittest.main()

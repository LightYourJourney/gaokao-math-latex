"""Exact arithmetic and semantic regressions; proof/review gates remain separate."""
from fractions import Fraction as F
from itertools import product
from math import comb, cos, isclose, log, pi, sin, sqrt, tan
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_三南卷"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Sannan1992MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "解答草稿.md").read_text(encoding="utf-8")
        cls.blocks = {q.number: q for q in solution_sources.parse_question_blocks(cls.text)}
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_28_solutions_are_bound_to_exact_draft_and_not_official(self):
        record = self.record["generated_solution"]
        self.assertEqual(list(self.blocks), list(range(1, 29)))
        self.assertEqual(record["question_numbers"], list(range(1, 29)))
        self.assertEqual(record["question_draft_sha256"], self.record["draft_sha256"])
        self.assertEqual(record["sha256"],
                         hashlib.sha256((PROJECT / "解答草稿.md").read_bytes()).hexdigest())
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(record["status"], "pending-independent-review")
        self.assertEqual(record["choice_key"], [
            "C", "D", "A", "B", "C", "A", "D", "B", "C", "A", "A", "D", "B", "B", "D", "C", "A"
        ])
        self.assertEqual(record["fill_in_answers"]["18"], r"\sqrt2-1")

    def test_q1_argument_convention_is_not_hidden(self):
        self.assertIn("主值约定下答案", self.blocks[1].body)
        self.assertIn(r"-4\pi/3", self.blocks[1].body)
        self.assertIn("同终边", self.blocks[1].body)

    def test_q3_inverse_trigonometric_principal_values(self):
        self.assertEqual(F(1, 3) - F(2, 3), F(-1, 3))
        self.assertEqual(F(-1, 3) / F(-1, 3), 1)

    def test_q5_point_to_line_distance(self):
        v = (F(1), F(1), F(-2))
        w = (F(0), F(0), F(-2))
        dot = sum(a * b for a, b in zip(v, w))
        norm2 = sum(a * a for a in v)
        distance2 = sum(a * a for a in w) - dot * dot / norm2
        self.assertEqual(distance2, F(4, 3))

    def test_q6_combined_trigonometric_coefficients_have_period_pi(self):
        self.assertIn(r"\sin\left(2x+\frac\pi3\right)", self.blocks[6].body)
        f = lambda x: 0.5 * sin(2 * x) + sqrt(3) / 2 * cos(2 * x)
        self.assertTrue(isclose(f(0), f(pi)))
        self.assertFalse(isclose(f(0), f(pi / 2)))

    def test_q8_absolute_value_and_square_root_interval(self):
        lower, upper = 2, 4
        self.assertEqual((lower * lower + 2, upper * upper + 2), (6, 18))

    def test_q9_arithmetic_sequence_and_q10_cosine_roots(self):
        self.assertEqual([-n * n + (n - 1) ** 2 for n in range(2, 7)], [-3, -5, -7, -9, -11])
        self.assertEqual((2 * F(-1, 2) ** 2 - 3 * F(-1, 2) - 2), 0)

    def test_q11_spherical_cap_surface_area(self):
        radius = 2
        cap_height = radius * (1 - sqrt(3) / 2)
        self.assertAlmostEqual(2 * pi * radius * cap_height, 4 * pi * (2 - sqrt(3)))

    def test_q12_combinatorics_and_q13_log_domain_intersection(self):
        self.assertEqual(comb(10, 2) - comb(7, 2), 24)
        m = lambda x: abs(x) > 2
        n = lambda x: 1 < x < 3
        self.assertTrue(m(-3) and not n(-3))
        self.assertFalse(m(-2))
        self.assertFalse(m(2.5) and not n(2.5))
        self.assertTrue(m(3) and not n(3))

    def test_q14_geometric_products(self):
        self.assertEqual(sum(range(30)), 435)
        self.assertEqual(sum(3 * k - 1 for k in range(1, 11)), 155)
        self.assertEqual(-135 + 155, 20)

    def test_q15_two_valid_triangles_refute_both_implications(self):
        a, b = pi / 6, 2 * pi / 3
        self.assertLess(a, b)
        self.assertFalse(tan(a) < tan(b))
        a, b = 2 * pi / 3, pi / 6
        self.assertFalse(a < b)
        self.assertTrue(tan(a) < tan(b))
        self.assertEqual(30 + 120 + 30, 180)

    def test_q16_odd_function_product_sign_includes_zero(self):
        for value in (-7, -1, 0, 2, 11):
            self.assertLessEqual(-value * value, 0)

    def test_q17_hyperbola_directrix_distance(self):
        a2 = F(8)
        b2 = F(18)
        c2 = a2 + b2
        self.assertEqual(c2, 26)
        self.assertEqual(b2 / a2, F(9, 4))
        self.assertTrue(isclose((2 * sqrt(float(a2))) / (sqrt(float(c2)) / sqrt(float(a2))),
                                16 / sqrt(26)))

    def test_q19_slope_and_intercept(self):
        for t in (-2, 0, 3):
            x, y = 2 + t / 2, 3 + sqrt(3) * t / 2
            self.assertTrue(isclose(y - sqrt(3) * x, 3 - 2 * sqrt(3)))
        # The source direction ratio is exact: (sqrt(3)/2)/(1/2)=sqrt(3).
        self.assertIn(r"y=\sqrt3x+3-2\sqrt3", self.blocks[19].body)

    def test_q20_incircle_and_q21_telescoping_sum(self):
        self.assertEqual((F(8) + F(15) - F(17)) / 2, F(3))
        for n in range(1, 30):
            partial = sum((F(1, (3 * k - 2) * (3 * k + 1)) for k in range(1, n + 1)), F(0))
            self.assertEqual(partial, F(1, 3) * (1 - F(1, 3 * n + 1)))

    def test_q22_modular_remainder(self):
        self.assertEqual(pow(91, 92, 100), 81)

    def test_q23_volume_dihedral_relation(self):
        a, h1, h2 = F(5), F(6), F(4)
        s1, s2 = a * h1 / 2, a * h2 / 2
        volume_factor = s1 * h2 / 3
        self.assertEqual(F(3) * a * volume_factor / (2 * s1 * s2), 1)

    def test_q24_exponential_substitution(self):
        self.assertEqual([a for a in (F(1, 2), F(3)) if 2 * a * a - 7 * a + 3 == 0],
                         [F(1, 2), F(3)])
        self.assertTrue(isclose((0.5) ** (-log(3, 2)), 3))
        self.assertTrue(isclose(3 ** (-log(2, 3)), 0.5))
        self.assertIn(r"1-\log_2 3", self.blocks[24].body)
        self.assertIn(r"1-\log_3 2", self.blocks[24].body)

    def test_q25_proof_uses_unique_perpendicular_direction(self):
        body = self.blocks[25].body
        self.assertIn(r"\alpha\cap\beta", body)
        self.assertIn(r"m\perp\beta", body)
        self.assertIn(r"a\parallel m", body)

    def test_q26_telescoping_majorant_is_strict(self):
        for k in range(1, 100):
            left = 1 / sqrt(k)
            right = 2 * (sqrt(k) - sqrt(k - 1))
            self.assertLess(left, right)
        self.assertIn("逐项相加", self.blocks[26].body)

    def test_q27_parabola_line_cut_length_exactly_matches_condition(self):
        p, h = F(8), F(-3, 2)
        self.assertEqual(p * (-1 - h), 4)
        # Substitution of y=2x+7 gives 4x^2-12x-23=0.
        discriminant = F((-12) ** 2 - 4 * 4 * (-23))
        dx2 = discriminant / 16
        segment_length2 = 5 * dx2
        self.assertEqual(segment_length2, 160)
        self.assertIn(r"(y-2)^2=32\left(x+\dfrac32\right)", self.blocks[27].body)

    def test_q28_integer_complex_solutions_satisfy_both_conditions(self):
        solutions = {(1, 3), (1, -3), (3, 1), (3, -1)}
        self.assertEqual({(m, n) for m, n in product(range(-4, 5), repeat=2)
                          if m * m + n * n == 10 and m in (1, 3)}, solutions)
        for m, n in solutions:
            real_value = 2 * m
            self.assertTrue(1 < real_value <= 6)


if __name__ == "__main__":
    unittest.main()

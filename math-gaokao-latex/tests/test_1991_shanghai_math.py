"""Exact calculation and counterexample checks; not a whole-paper proof gate."""
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1991_上海卷"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Shanghai1991RecomputationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.draft = (PROJECT / "复算草稿.md").read_text(encoding="utf-8")
        cls.answers = solution_sources.parse_answer_points(
            (ROOT.parent / "1991/1991_数学真题_上海_答案要点.md").read_text(encoding="utf-8")
        )

    def test_recomputed_scope_excludes_unread_and_unworked_questions(self):
        expected = [*range(1, 8), *range(9, 14), *range(15, 20), *range(21, 28)]
        self.assertEqual([q.number for q in solution_sources.parse_question_blocks(self.draft)], expected)
        self.assertIn("pending-independent-review", self.draft)
        self.assertIn("不能称盲解", self.draft)
        record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))
        self.assertEqual(record["math_recomputation"]["question_numbers"], expected)
        self.assertEqual(record["math_recomputation"]["status"], "pending-independent-review")
        self.assertEqual(record["math_recomputation"]["sha256"],
                         hashlib.sha256((PROJECT / "复算草稿.md").read_bytes()).hexdigest())
        self.assertEqual(record["math_recomputation"]["question_draft_sha256"], record["draft_sha256"])
        self.assertEqual(record["mathematical_verification_status"], "not-verified")

    def test_q2_half_angle_branch_and_q3_volume_dimensionless_ratio(self):
        squared_half_cos = (1 + F(-4, 5)) / 2
        self.assertEqual(squared_half_cos, F(1, 10))
        self.assertIn(r"-\dfrac{\sqrt{10}}{10}", self.answers[1].answer_for(None))
        self.assertIn("第二象限", self.draft)
        self.assertEqual(F(2) / F(4, 3), F(3, 2))

    def test_q5_eccentricity_and_q6_both_common_ratio_signs(self):
        self.assertEqual(1 - F(1, 2) ** 2, F(3, 4))
        q_squared = F(1, 3)
        self.assertEqual(F(3) / (1 - q_squared), F(9, 2))
        self.assertIn("无需错误地排除负公比", self.draft)

    def test_q7_equal_radius_and_height_and_q13_diagonal_projections(self):
        self.assertEqual(16 - 2 * 8, 0)  # (r-h)^2=0
        radius_squared = F(8)
        self.assertEqual(16 * radius_squared, 128)  # (S/pi)^2
        a = b = F(4) * F(1, 2)
        c_squared = 16 - a * a - b * b
        self.assertEqual(c_squared, 8)
        self.assertEqual(a * a * b * b * c_squared, 128)
        self.assertEqual(self.answers[12].answer_for(None), "B")

    def test_q9_reflection_and_q10_circle_polar_identity(self):
        # Reflection expansion coefficients, not a few sampled x values.
        coefficients = [0, 0, 0]
        for power, coefficient in enumerate((1, 0, 1)):
            for k in range(power + 1):
                coefficients[k] += coefficient * comb(power, k) * 2 ** (power - k) * (-1) ** k
        self.assertEqual(coefficients, [5, -4, 1])
        self.assertIn("x^2-4x+5", self.answers[8].answer_for(None))
        # Expanding (x+4)^2+y^2-16 yields rho^2+8rho*cos(theta).
        self.assertEqual(4 ** 2 - 16, 0)
        self.assertIn("极点仍包含", self.draft)

    def test_q11_log_domain_filters_algebraic_roots(self):
        roots = [-1, 2]
        self.assertTrue(all(x * x - x - 2 == 0 for x in roots))
        domain_roots = [x for x in roots if x > 0 and x * x - 2 > 0]
        self.assertEqual(domain_roots, [2])
        self.assertEqual({-1} - set(domain_roots), {-1})
        self.assertEqual(self.answers[10].answer_for(None), "B")

    def test_q12_arithmetic_sequence_identity(self):
        # Pair each coefficient of a1 and d: indices 3..7 -> offsets 2..6.
        self.assertEqual(sum(range(2, 7)), 5 * 4)
        middle = F(450, 5)
        self.assertEqual(2 * middle, 180)
        self.assertEqual(1 + 7, 2 * 4)  # offsets of a2+a8
        self.assertEqual(self.answers[11].answer_for(None), "C")

    def test_q16_all_permutations_exactly_two_fixed_points(self):
        count = sum(sum(i == v for i, v in enumerate(p)) == 2
                    for p in permutations(range(5)))
        self.assertEqual(count, comb(5, 2) * 2)
        self.assertEqual(count, 20)
        self.assertEqual(self.answers[15].answer_for(None), "A")

    def test_q17_comparison_after_sign_partition(self):
        self.assertLess(1 - F(2, 3) ** 2, 1 - F(1, 3) ** 2)
        self.assertLess(F(5, 4), 8)  # positive tangent squares
        self.assertEqual(self.answers[16].answer_for(None), "D")
        self.assertIn(r"-\sqrt5/2>-\sqrt8", self.draft)

    def test_q18_explicit_counterexample_planes_intersect(self):
        for t in (F(-2), F(0), F(5, 2)):
            line = (t, F(0), F(0))
            intersection = (t, F(1), F(0))
            self.assertEqual(line[2], 0)  # a in M
            self.assertNotEqual(line[1], 1)  # all a have y=0, none in N
            self.assertEqual((intersection[1], intersection[2]), (1, 0))
        self.assertEqual(self.answers[17].answer_for(None), "A")
        self.assertIn("任意实数", self.draft)

    def test_q19_half_angle_elimination_is_polynomial_identity(self):
        # Let s=sin^2(t); cos^2(t)=1-s. For D, both sides of
        # (1-cos2t)*cos^2(t) = (1+cos2t)*sin^2(t) have coefficients 2s-2s^2.
        def multiply(a, b):
            result = [F(0)] * (len(a) + len(b) - 1)
            for i, ai in enumerate(a):
                for j, bj in enumerate(b):
                    result[i + j] += ai * bj
            return result
        cos_2t = [F(1), F(-2)]
        numerator = [1 - cos_2t[0], -cos_2t[1]]
        denominator = [1 + cos_2t[0], cos_2t[1]]
        self.assertEqual(multiply(numerator, [1, -1]), multiply(denominator, [0, 1]))
        self.assertEqual(multiply(numerator, [1, -1]), [0, 2, -2])
        self.assertIn(r"t=\arctan x", self.draft)  # surjectivity, not just elimination
        self.assertIn(r"\cos t\ne0", self.draft)
        self.assertEqual(self.answers[18].answer_for(None), "D")

    def test_q21_double_angle_without_square_root_sign_loss(self):
        cos_u_squared = F(1, 4)
        sin_2x = 2 * cos_u_squared - 1
        self.assertEqual(sin_2x, F(-1, 2))
        self.assertEqual(1 - 2 * sin_2x ** 2, F(1, 2))
        self.assertIn(r"\dfrac12", self.answers[20].answer_for(None))

    def test_q22_both_focus_directions_in_quadratic_field(self):
        # p/d = 1/2 +/- sqrt(3)/4. Check 2p/d +/- sqrt(3)/2 = 1.
        coefficients = []
        for direction in (-1, 1):
            p = (F(1, 2), F(-direction, 4))
            self.assertEqual((2 * p[0], 2 * p[1] + F(direction, 2)), (1, 0))
            self.assertGreater(p[0] ** 2, 3 * p[1] ** 2)  # both p > 0
            coefficients.append(p)
        self.assertNotEqual(*coefficients)
        answer = self.answers[21].answer_for(None)
        self.assertIn(r"2-\sqrt3", answer)
        self.assertIn(r"2+\sqrt3", answer)

    def test_q22_drawn_points_lie_on_parabola_and_have_unit_focus_distance(self):
        def multiply(a, b):
            return (a[0] * b[0] + 3 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])
        for direction in (-1, 1):
            p = (F(1, 2), F(-direction, 4))
            ex = (F(1, 2), F(direction, 4))
            four_p = (4 * p[0], 4 * p[1])
            self.assertEqual(multiply(four_p, ex), (F(1, 4), 0))  # y_E^2
            dx = (ex[0] - p[0], ex[1] - p[1])
            dx_squared = multiply(dx, dx)
            self.assertEqual((dx_squared[0] + F(1, 4), dx_squared[1]), (1, 0))

    def test_q23_absolute_value_partition_and_strict_boundaries(self):
        # Test in the bijective variable t=log_a(x); full proof in the draft.
        def partition(a, t):
            if a < F(1, 2):
                return True
            if a == F(1, 2):
                return t * t != 1
            if a < 1:
                return t * t > 2 * a or t * t < 2 * (1 - a)
            return t * t > 2 * a
        for a in (F(1, 4), F(1, 2), F(3, 4), F(2)):
            for t in map(F, (-3, -2, -1, 0, 1, 2, 3)):
                with self.subTest(a=a, t=t):
                    self.assertEqual(abs(t * t - 1) > 2 * a - 1, partition(a, t))
        # At a=1/2, t=+/-1 excluded; at a=2, t=+/-2 excluded.
        for a, t in ((F(1, 2), F(1)), (F(1, 2), F(-1)), (F(2), F(2)), (F(2), F(-2))):
            self.assertFalse(partition(a, t))
        self.assertIn("$a=1$根本不在题设范围", self.draft)
        self.assertIn(r"a^{\sqrt{2(1-a)}}<x<a^{-\sqrt{2(1-a)}}", self.draft)

    def test_q24_gram_projection_gives_obtuse_dihedral(self):
        # Gram values from AB=BC=BD=2 and perpendicular planes about BC.
        aa = cc = dd = F(4)
        ac = cd = F(-2)
        ad = ac * cd / cc  # transverse components perpendicular
        self.assertEqual(ad, 1)
        line_squared = aa + dd - 2 * ad
        self.assertEqual(line_squared, 6)
        self.assertEqual(F(3) / line_squared, F(1, 2))  # sin^2(line-plane angle)
        self.assertEqual(ac - cd, 0)  # AD perpendicular BC
        projected_dot = ac - ad * cd / dd
        projected_a_squared = aa - ad * ad / dd
        projected_c_squared = cc - cd * cd / dd
        self.assertLess(projected_dot, 0)
        self.assertEqual(projected_dot ** 2 / (projected_a_squared * projected_c_squared), F(1, 5))
        self.assertIn(r"\pi-\arctan2", self.draft)

    def test_q25_circle_equivalence_and_zero_not_excluded(self):
        def multiply(a, b):
            return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
        def divide(a, b):
            norm = b[0] ** 2 + b[1] ** 2
            product = multiply(a, (b[0], -b[1]))
            return product[0] / norm, product[1] / norm
        for t in (F(-2), F(-1, 2), F(1, 2), F(2)):
            z = (2 * t / (1 + t * t), 2 / (1 + t * t))
            self.assertEqual(z[0] ** 2 + (z[1] - 1) ** 2, 1)
            factor = divide((z[0], z[1] - 2), z)
            self.assertEqual(factor[0], 0)
            self.assertNotEqual(factor[1], 0)
            for s in (F(-3), F(0), F(1), F(3)):
                w = (2 * s / (1 + s * s), 2 * s * s / (1 + s * s))
                ratio = divide(w, (w[0], w[1] - 2))
                self.assertEqual(multiply(ratio, factor)[1], 0)
            for w in ((F(0), F(1)), (F(2), F(2))):
                ratio = divide(w, (w[0], w[1] - 2))
                self.assertNotEqual(multiply(ratio, factor)[1], 0)
        with self.assertRaises(ZeroDivisionError):
            divide((F(0), F(2)), (F(0), F(0)))
        self.assertIn("$\\omega=0$，原乘积为0", self.draft)
        self.assertIn(r"3\theta-\pi/2+2k\pi", self.draft)

    def test_q26_original_intersections_ratio_and_centroid_exactly(self):
        # Rational root parameterization (u-2)(v-2)=6; both slope branches.
        for t in (F(-6), F(-3), F(-2), F(-1), F(-1, 2), F(1, 2), F(1), F(2), F(3), F(6)):
            u, v = 2 + t, 2 + 6 / t
            m = u + v
            self.assertNotEqual(u, v)
            self.assertGreater((m - 4) ** 2 - 24, 0)
            yb, yc = u * u + 2, v * v + 2
            self.assertEqual(yb, m * (u - 2))
            self.assertEqual(yc, m * (v - 2))
            px = (yc * u + yb * v) / (yb + yc)
            py = 2 * yb * yc / (yb + yc)
            self.assertEqual((u - px) / (px - v), yb / yc)
            self.assertEqual(py, m * (px - 2))
            x, y = (px + 2) / 3, py / 3
            self.assertEqual(12 * x - 3 * y - 4, 0)
            self.assertLess((y - 4) ** 2, F(32, 3))
            self.assertNotEqual(y, 4)
            self.assertEqual(m, 4 * y / (y - 4))
        # Reverse construction in both open components; exclude missing point.
        for y in map(F, (1, 2, 3, 5, 6, 7)):
            m = 4 * y / (y - 4)
            self.assertGreater((m - 4) ** 2 - 24, 0)
            self.assertEqual(4 * m / (m - 4), y)
        self.assertIn("两端对应相切", self.draft)
        self.assertIn("$Y\\ne4$", self.draft)

    def test_q27_cone_sum_or_difference_covers_external_altitude_foot(self):
        side, height = F(3), F(4)
        for foot in (F(-3), F(0), F(1, 2), side, side + 3):
            if foot < 0:
                volume_over_pi = (side - foot) * height ** 2 / 3 - (-foot) * height ** 2 / 3
            elif foot > side:
                volume_over_pi = foot * height ** 2 / 3 - (foot - side) * height ** 2 / 3
            else:
                volume_over_pi = foot * height ** 2 / 3 + (side - foot) * height ** 2 / 3
            self.assertEqual(volume_over_pi, side * height ** 2 / 3)

    def test_q27_domain_and_maximum_with_equality_configuration(self):
        for cosine in (F(1, 2), F(0), F(-1, 2)):
            for a, b in ((F(1), F(1)), (F(1), F(2)), (F(1), F(10))):
                c_squared = a * a + b * b - 2 * a * b * cosine
                x_squared = (a + b) ** 2 / c_squared
                self.assertGreater(x_squared, 1)
                self.assertLessEqual(x_squared, 2 / (1 - cosine))
                t_squared = (a * b) ** 2 / (c_squared * (a + b) ** 2)
                maximum_squared = 1 / (8 * (1 - cosine))
                self.assertLessEqual(t_squared, maximum_squared)
                self.assertEqual(t_squared == maximum_squared, a == b)
        self.assertEqual(1 / (8 * (1 - F(1, 2))), F(1, 4))
        self.assertIn("$x=1$只在边长比趋于0或无穷时趋近，不能包含", self.draft)


if __name__ == "__main__":
    unittest.main()

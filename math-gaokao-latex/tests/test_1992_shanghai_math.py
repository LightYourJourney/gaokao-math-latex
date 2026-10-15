"""Exact recomputation supports written proofs; not independent blind review."""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_上海卷"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


def dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def subtract(u, v):
    return tuple(x - y for x, y in zip(u, v))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0])


class Shanghai1992MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "解答草稿.md").read_text(encoding="utf-8")
        cls.blocks = {q.number: q for q in solution_sources.parse_question_blocks(cls.text)}
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_complete_pending_solution_and_input_fingerprints(self):
        self.assertEqual(list(self.blocks), list(range(1, 27)))
        self.assertEqual({n: b.subparts for n, b in self.blocks.items() if b.subparts},
                         {24: (1, 2, 3), 25: (1, 2)})
        generated = self.record["generated_solution"]
        self.assertEqual(generated["question_numbers"], list(range(1, 27)))
        self.assertEqual(generated["sha256"], hashlib.sha256((PROJECT / "解答草稿.md").read_bytes()).hexdigest())
        self.assertEqual(generated["question_draft_sha256"], self.record["draft_sha256"])
        self.assertEqual(generated["status"], "pending-independent-review")
        self.assertFalse(generated["independent_review"])
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.text.count("$") % 2, 0)
        self.assertEqual(self.text.count("{"), self.text.count("}"))

    def test_generated_choice_key_matches_printed_key_without_official_attribution(self):
        generated = self.record["generated_solution"]
        self.assertEqual(generated["choice_numbers"], list(range(11, 21)))
        self.assertEqual(generated["choice_key"], self.record["source_answer_excerpt"]["choice_key"])
        for n, letter in zip(generated["choice_numbers"], generated["choice_key"]):
            self.assertIn(f"**答案：{letter}。**", self.blocks[n].body)

    def test_q2_unique_binomial_term_and_q9_permutations(self):
        matches = [(r, comb(8, r)) for r in range(9) if 8 - 2 * r == -2]
        self.assertEqual(matches, [(5, 56)])
        self.assertEqual(3 * factorial(4), 72)

    def test_q4_extraneous_root_is_excluded_and_q7_units(self):
        roots = [x for x in range(-10, 11) if (x + 1) * (x - 3) == 5]
        self.assertEqual(roots, [-2, 4])
        self.assertEqual([x for x in roots if x > 3], [4])
        lower, height = F(8), F(6)
        upper = lower - height
        self.assertEqual(upper, 2)
        self.assertEqual((lower + upper) * height, 60)  # times sqrt(2)*pi cm^2
        self.assertIn(r"\mathrm{cm}^2", self.blocks[7].body)

    def test_q5_binomial_exact_complex_power_detects_old_exponent(self):
        # Basis 1, sqrt(3), i, sqrt(3)*i; no floating point.
        def power(n):
            coefficients = [0, 0, 0, 0]
            for k in range(n + 1):
                radical_power = n - k
                value = comb(n, k) * 3 ** (radical_power // 2) * (-1) ** (k // 2)
                coefficients[radical_power % 2 + 2 * (k % 2)] += value
            return coefficients
        self.assertEqual(power(3), [0, 0, 8, 0])
        self.assertEqual(power(6), [-64, 0, 0, 0])
        self.assertEqual(power(8), [-128, 0, 0, -128])
        self.assertIn("原图指数为6", self.blocks[5].body)

    def test_q10_gram_matrix_with_b1m_not_bm(self):
        gram = ((F(1), F(1, 2), F(0)), (F(1, 2), F(1), F(0)), (F(0), F(0), F(1)))
        def inner(a, b):
            return sum(a[i] * gram[i][j] * b[j] for i in range(3) for j in range(3))
        ef = (F(-1, 2), F(0), F(1, 2))
        b1m = (F(-1, 2), F(1, 2), F(1))
        bm = (F(-1, 2), F(1, 2), F(0))
        self.assertEqual(inner(ef, ef), F(1, 2))
        self.assertEqual(inner(b1m, b1m), F(5, 4))
        self.assertEqual(inner(ef, b1m), F(5, 8))
        cosine_squared = inner(ef, b1m) ** 2 / (inner(ef, ef) * inner(b1m, b1m))
        self.assertEqual(1 - cosine_squared, F(6, 16))
        old_cosine_squared = inner(ef, bm) ** 2 / (inner(ef, ef) * inner(bm, bm))
        self.assertNotEqual(1 - old_cosine_squared, F(6, 16))
        self.assertIn(r"B_1M", self.blocks[10].body)

    def test_q13_equal_unsigned_distances_do_not_imply_parallel_planes(self):
        points = ((1, 0, 1), (1, 1, 1), (-1, 0, -1))
        self.assertTrue(all(p[2] == p[0] and abs(p[2]) == 1 for p in points))
        self.assertNotEqual(cross(subtract(points[1], points[0]), subtract(points[2], points[0])), (0, 0, 0))
        self.assertNotEqual(cross((-1, 0, 1), (0, 0, 1)), (0, 0, 0))

    def test_q14_domain_holes_are_retained(self):
        body = self.blocks[14].body
        self.assertIn(r"\mathbb R\setminus", body)
        self.assertIn(r"\pi/2+k\pi", body)
        self.assertIn("不能因恒等变形而补回缺失点", body)

    def test_q15_parametric_curve_options_have_unique_valid_point(self):
        options = [(F(2), F(-7)), (F(1, 3), F(2, 3)),
                   (F(1, 2), F(1, 2)), (F(1), F(0))]
        self.assertEqual([n for n, (x, y) in enumerate(options) if -1 <= x <= 1 and y == 1 - 2 * x * x], [2])

    def test_q17_isosceles_trapezoid_prismoid_is_not_pyramid_frustum(self):
        bottom = [(-2, -2, 0), (2, -2, 0), (2, 2, 0), (-2, 2, 0)]
        top = [(F(-1), F(-1, 2), F(1)), (F(1), F(-1, 2), F(1)),
               (F(1), F(1, 2), F(1)), (F(-1), F(1, 2), F(1))]
        for i in range(4):
            j = (i + 1) % 4
            lower_edge, upper_edge = subtract(bottom[j], bottom[i]), subtract(top[j], top[i])
            self.assertEqual(cross(lower_edge, upper_edge), (0, 0, 0))
            left, right = subtract(top[i], bottom[i]), subtract(top[j], bottom[j])
            self.assertEqual(dot(left, left), dot(right, right))
            self.assertEqual(dot(cross(lower_edge, left), right), 0)
        self.assertNotEqual(F(2, 4), F(1, 4))  # bottom/top edge ratios differ

    def test_q21_exact_trig_values_and_quadrant(self):
        sa, ca, sb, cb = F(3, 5), F(4, 5), F(-5, 13), F(-12, 13)
        self.assertEqual(ca * ca - sa * sa, F(7, 25))
        self.assertEqual(sb * sb + cb * cb, 1)
        cosine, sine = ca * cb - sa * sb, sa * cb + ca * sb
        self.assertEqual((cosine, sine), (F(-33, 65), F(-56, 65)))
        self.assertEqual(cosine * cosine + sine * sine, 1)
        self.assertIn("第三象限", self.blocks[21].body)

    def test_q22_complex_division_and_closed_modulus_bounds(self):
        def multiply(u, v):
            return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])
        product = multiply((1, -4), (1, 1))
        numerator = (product[0] + 2, product[1] + 4)
        self.assertEqual(numerator, (7, 1))
        self.assertEqual(multiply((1, -1), (3, 4)), numerator)
        for a in (F(-1), F(0), F(1, 2), F(1), F(2), F(3)):
            self.assertEqual(1 + (a - 1) ** 2 <= 2, 0 <= a <= 2)
        self.assertIn(r"[7\pi/4,2\pi)", self.blocks[22].body)

    def test_q23_both_branches_and_distinct_intersection_boundary(self):
        for x in (F(0), F(1), F(3, 2), F(2), F(-2)):
            b_squared = 2 - x * x / 2
            self.assertEqual(b_squared > 0, -2 < x < 2)
            for sign in (-1, 1):
                y_squared = b_squared + sign
                if y_squared < 0 or b_squared <= 0:
                    continue
                self.assertEqual(abs(y_squared - b_squared), 1)
                if sign == -1:
                    self.assertEqual(x * x / 2 + y_squared, 1)
                else:
                    self.assertEqual(x * x / 6 + y_squared / 3, 1)
        self.assertIn("反过来", self.blocks[23].body)

    def test_q24_projection_normal_and_volume_and_half_angle(self):
        for radius in (F(1), F(2)):
            for t in (F(1, 4), F(1, 2), F(1), F(2)):
                cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
                s, b = (F(0), F(0), radius), (radius, F(0), F(0))
                q = (-radius * cosine, radius * sine, F(0))
                c = tuple((x + y) / 2 for x, y in zip(q, b))
                sc, qb = subtract(c, s), subtract(b, q)
                h = tuple(x - dot(s, sc) / dot(sc, sc) * y for x, y in zip(s, sc))
                self.assertEqual(dot(h, sc), 0)
                self.assertEqual(dot(h, qb), 0)
                self.assertNotEqual(dot(h, h), 0)
        self.assertEqual(F(2) ** 3 / 3, F(8, 3))  # volume coefficient of pi
        self.assertEqual(2 * F(1, 3), F(6, 9))  # tan(delta)^2=2*tan(alpha/2)^2

    def test_q25_geometric_ratio_for_q_equal_one_and_below_one(self):
        for a in (F(1), F(5, 2)):
            for q in (F(1), F(1, 2), F(3, 4)):
                for n in range(1, 9):
                    sequence = [a * q ** k for k in range(n)]
                    ratio = sum(sequence) / sum(x * x for x in sequence)
                    self.assertEqual(ratio, 1 / a if q == 1 else (1 + q) / (a * (1 + q ** n)))
        self.assertIn("不能在 $q=1$", self.blocks[25].body)

    def test_q25_integer_comparison_and_polynomial_recurrence(self):
        polynomial = lambda n: -3 * n * n + 11 * n - 2
        self.assertEqual([polynomial(n) for n in (2, 3, 4)], [8, 4, -6])
        for n in range(2, 101):
            self.assertEqual(9 * n * n * (n + 1) - (3 * n - 1) ** 2 * (n + 2), polynomial(n))
            self.assertEqual(polynomial(n + 1) - polynomial(n), 8 - 6 * n)
            self.assertEqual(polynomial(n) > 0, n in (2, 3))
            self.assertNotEqual(polynomial(n), 0)

    def test_q26_quadratic_root_and_slope_equations_exactly(self):
        for a in (F(2), F(5, 2), F(3)):
            discriminant = 2 * a * a - 2 * a + 1
            def multiply(u, v):
                return (u[0] * v[0] + discriminant * u[1] * v[1], u[0] * v[1] + u[1] * v[0])
            m = ((1 + a) / 2, F(1, 2))
            product = multiply((m[0] - 1, m[1]), (m[0] - a, m[1]))
            self.assertEqual(tuple(4 * x for x in product), (a * a, 0))
            self.assertGreater(discriminant, (a - 1) ** 2)  # positive branch m>a; minus branch <1
            self.assertTrue(F(3, 4) <= (a * a - 1) / (a * a) <= F(8, 9))
            k = ((m[0] - a) / a, m[1] / a)
            k_squared = multiply(k, k)
            self.assertEqual((4 * a * k_squared[0] + 4 * a * k[0] - a - 4 * k[0],
                              4 * a * k_squared[1] + 4 * a * k[1] - 4 * k[1]), (0, 0))
        self.assertIn("严格递减", self.blocks[26].body)
        self.assertIn(r"a=2", self.blocks[26].body)
        self.assertIn(r"(\sqrt5-1)/4", self.blocks[26].body)


if __name__ == "__main__":
    unittest.main()

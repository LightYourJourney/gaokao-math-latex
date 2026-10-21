"""Exact arithmetic/regression checks; proofs and independent review remain separate."""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_全国卷_理科"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


class NationalScience1992MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "解答草稿.md").read_text(encoding="utf-8")
        cls.blocks = {q.number: q for q in solution_sources.parse_question_blocks(cls.text)}
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_27_draft_solutions_and_two_unverified_without_official_attribution(self):
        self.assertEqual(list(self.blocks), list(range(1, 29)))
        self.assertEqual(self.blocks[27].subparts, (1, 2))
        self.assertIn("待核，未给选项答案", self.blocks[16].body)
        record = self.record["generated_solution"]
        self.assertEqual(record["question_numbers"], [n for n in range(1, 29) if n != 16])
        self.assertEqual(record["status"], "independently-reviewed")
        self.assertEqual(record["sha256"], hashlib.sha256((PROJECT / "解答草稿.md").read_bytes()).hexdigest())
        self.assertEqual(record["question_draft_sha256"], self.record["draft_sha256"])
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "independently-reviewed")

    def test_independent_blind_review_coverage_hashes_and_open_issues(self):
        review = self.record["independent_blind_review"]
        self.assertEqual(review["status"], "reviewed-with-source-issues")
        self.assertEqual(review["reviewers"], 3)
        self.assertEqual(review["full_range_reviewers"], 2)
        self.assertEqual(review["reviewed_question_numbers"], list(range(1, 29)))
        self.assertEqual(
            review["verified_answer_question_numbers"],
            [n for n in range(1, 29) if n not in (16, 26)],
        )
        self.assertEqual(review["confirmed_source_issue_question_numbers"], [16, 26])
        self.assertEqual(review["conditional_interpretation_question_numbers"], [26])
        self.assertEqual(review["semantic_caveat_question_numbers"], [2])
        self.assertEqual(review["transcription_discrepancy_question_numbers"], [])
        self.assertEqual(review["source_pdf_sha256"], self.record["pdf_sha256"])
        self.assertEqual(review["source_render_sha256"], self.record["render"]["sha256"])
        self.assertEqual(review["question_draft_sha256"], self.record["draft_sha256"])
        self.assertEqual(review["solution_draft_sha256"], "c678e5a3206863d984da812abaf3e69c4ad62a1d6af0924a80c0a1231ac0cedf")
        self.assertEqual(
            review["current_solution_draft_sha256"],
            hashlib.sha256((PROJECT / "解答草稿.md").read_bytes()).hexdigest(),
        )
        self.assertEqual(
            hashlib.sha256((PROJECT / review["report_path"]).read_bytes()).hexdigest(),
            review["report_sha256"],
        )
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertIsNone(self.record["paper_id"])

    def test_generated_choice_key_includes_no_guessed_q16_answer(self):
        key = ["A", "D", "D", "B", "D", "B", "B", "C", "D", "D", "B", "B", "A", "D", "D", None, "A", "C"]
        self.assertEqual(self.record["generated_solution"]["choice_key"], key)
        for number, answer in enumerate(key, 1):
            if answer is not None:
                self.assertIn(f"**答案：{answer}**", self.blocks[number].body)
        self.assertIn(r"\omega=\pm1/4", self.blocks[2].body)
        self.assertIn("原题未设", self.blocks[2].body)

    def test_q26_solution_is_explicitly_conditional_on_foot_assignment(self):
        body = self.blocks[26].body
        self.assertIn(r"A_1\in a,A\in b", body)
        self.assertIn("原题未显式规定", body)
        self.assertIn(r"\sqrt3d", body)

    def test_q3_circle_distance_and_q5_full_surface_ratio(self):
        self.assertEqual(F(1, 2) ** 2 + F(1, 2) ** 2, F(1, 2))
        self.assertEqual((2 * 2 + 2) / F(4), F(3, 2))
        self.assertEqual(9 * 20 % 180, 0)  # Q4 listed 20 degrees
        self.assertEqual([x for x in (10, 20, 50, 70) if 9 * x % 180 == 0], [20])

    def test_q9_non_degenerate_pyramid_has_four_right_side_faces(self):
        s = (0, 0, 1)
        a, b, c, d = (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)
        for origin, p, q in ((a, s, b), (a, s, d), (b, s, c), (d, s, c)):
            self.assertEqual(dot(subtract(p, origin), subtract(q, origin)), 0)
            self.assertNotEqual(p, origin)
            self.assertNotEqual(q, origin)
        self.assertNotEqual(s[2], a[2])

    def test_q10_circle_options_satisfy_all_three_geometric_constraints(self):
        valid = []
        for letter, dx, dy, constant in (
            ("A", -1, -2, F(-1, 4)), ("B", 1, -2, F(1)),
            ("C", -1, -2, F(1)), ("D", -1, -2, F(1, 4)),
        ):
            h, k = F(-dx, 2), F(-dy, 2)
            radius_squared = h * h + k * k - constant
            if radius_squared > 0 and k * k == 2 * h and radius_squared == k * k == (h + F(1, 2)) ** 2:
                valid.append(letter)
        self.assertEqual(valid, ["D"])
        self.assertIn("下方圆也满足题设", self.blocks[10].body)

    def test_q11_polynomial_convolution_coefficient(self):
        polynomial = [1]
        for _ in range(5):
            result = [0] * (len(polynomial) + 2)
            for i, ai in enumerate(polynomial):
                for j, bj in enumerate((2, 3, 1)):
                    result[i + j] += ai * bj
            polynomial = result
        self.assertEqual(polynomial[1], 240)

    def test_q14_midpoint_geometry_and_exact_cosine_squared(self):
        a, b, c = (F(0), F(0), F(0)), (F(1), F(0), F(0)), (F(1), F(1), F(0))
        a1, b1 = (F(0), F(0), F(1)), (F(1), F(0), F(1))
        m = tuple((x + y) / 2 for x, y in zip(a1, b1))
        n = tuple((x + y) / 2 for x, y in zip(b, b1))
        am, cn = subtract(m, a), subtract(n, c)
        self.assertEqual(dot(am, cn), F(1, 2))
        self.assertEqual(dot(am, cn) ** 2 / (dot(am, am) * dot(cn, cn)), F(4, 25))
        self.assertEqual(dot(m, m), F(5, 4))

    def test_q17_axis_order_and_q18_diagonal_square(self):
        relative_values = [(x - 2) ** 2 for x in (2, 1, 4)]
        self.assertEqual(relative_values, [0, 1, 4])
        self.assertEqual(F(24, 4) ** 2 - 11, 25)

    def test_q19_positive_substitution_q21_subsets_and_q23_denominator(self):
        t = F(1, 3)
        self.assertEqual((1 + 1 / t) / (1 + t), 3)
        self.assertEqual(F(comb(10, 3), 2 ** 10), F(15, 128))
        for d in (F(-2), F(1), F(5, 2)):
            a = lambda n: d + (n - 1) * d
            self.assertEqual(a(3) ** 2, a(1) * a(9))
            self.assertNotEqual(a(2) + a(4) + a(10), 0)
            self.assertEqual((a(1) + a(3) + a(9)) / (a(2) + a(4) + a(10)), F(13, 16))

    def test_q22_hyperbola_focus_and_eccentricity(self):
        center, c, a_squared, b_squared = F(2), F(4), F(4), F(12)
        self.assertEqual((center - c, center + c), (-2, 6))
        self.assertEqual(a_squared + b_squared, c * c)
        self.assertEqual(c * c / a_squared, 4)

    def test_q24_original_conjugate_equation_filters_wrong_sign(self):
        def multiply(a, b):
            return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
        for z, expected in (((-1, 0), True), ((-1, 3), True), ((-1, -3), False)):
            conjugate = (z[0], -z[1])
            norm = multiply(z, conjugate)
            term = multiply((0, 3), conjugate)
            self.assertEqual(subtract(norm, term) == (1, 3), expected)

    def test_q25_quadrant_signs_and_angle_sum(self):
        cos_delta, sin_delta = F(12, 13), F(5, 13)
        sin_sigma, cos_sigma = F(-3, 5), F(-4, 5)
        self.assertEqual(cos_delta ** 2 + sin_delta ** 2, 1)
        self.assertEqual(sin_sigma ** 2 + cos_sigma ** 2, 1)
        self.assertEqual(sin_sigma * cos_delta + cos_sigma * sin_delta, F(-56, 65))
        self.assertRegex(self.blocks[25].body, r"\\sigma[^$]*\\in\(\\pi,3\\pi/2\)")

    def test_q26_spatial_vectors_cover_both_signs_and_zero_offsets(self):
        u, v = (F(1), F(0), F(0)), (F(3, 5), F(4, 5), F(0))
        for m, n in ((F(2), F(3)), (F(0), F(3)), (F(2), F(0))):
            for epsilon in (-1, 1):
                for eta in (-1, 1):
                    e = tuple(epsilon * m * x for x in u)
                    f = tuple(eta * n * x + offset for x, offset in zip(v, (0, 0, 4)))
                    vector = subtract(f, e)
                    expected = 16 + m * m + n * n - 2 * epsilon * eta * m * n * dot(u, v)
                    self.assertEqual(dot(vector, vector), expected)
                    self.assertGreaterEqual(expected, 16 + (m - n) ** 2)

    def test_q27_open_boundaries_and_unique_maximum_six(self):
        def total(n, d):
            return F(n, 2) * (24 + (n - 5) * d)
        self.assertEqual(total(12, F(-24, 7)), 0)
        self.assertEqual(total(13, F(-3)), 0)
        for d in (F(-17, 5), F(-13, 4), F(-31, 10)):
            self.assertGreater(total(12, d), 0)
            self.assertLess(total(13, d), 0)
            sums = {n: total(n, d) for n in range(1, 13)}
            self.assertEqual([n for n, s in sums.items() if s == max(sums.values())], [6])

    def test_q28_perpendicular_bisector_and_strict_endpoint_exclusion(self):
        a, b = F(3), F(2)
        points = [(-a, F(0))]
        for t in (F(-3), F(-1), F(0), F(1, 2), F(1), F(3)):
            points.append((a * (1 - t * t) / (1 + t * t), b * 2 * t / (1 + t * t)))
        for first, second in combinations(points, 2):
            if first[0] == second[0]:
                continue  # coincident bisector/x axis is not a unique intersection
            x0 = (a * a - b * b) * (first[0] + second[0]) / (2 * a * a)
            self.assertEqual((x0 - first[0]) ** 2 + first[1] ** 2,
                             (x0 - second[0]) ** 2 + second[1] ** 2)
            self.assertLess(abs(x0), (a * a - b * b) / a)
        # Degenerate interpretation would give a counterexample: any x0 is equidistant.
        p, first, second = (F(10), F(0)), (F(0), b), (F(0), -b)
        pa, pb = subtract(p, first), subtract(p, second)
        self.assertEqual(dot(pa, pa), dot(pb, pb))
        self.assertGreater(10, (a * a - b * b) / a)
        self.assertIn("唯一交点", self.blocks[28].body)
        self.assertIn(r"x_1\ne x_2", self.blocks[28].body)


if __name__ == "__main__":
    unittest.main()

"""Arts-specific exact calculations and bounded solution reuse; not blind review."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1992_全国卷_文科"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class NationalArts1992MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (PROJECT / "解答草稿.md").read_text(encoding="utf-8")
        cls.question_text = (PROJECT / "题面转录草稿.md").read_text(encoding="utf-8")
        cls.blocks = {q.number: q for q in solution_sources.parse_question_blocks(cls.text)}
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))

    def test_26_solved_and_two_unresolved_with_non_official_attribution(self):
        self.assertEqual(list(self.blocks), list(range(1, 29)))
        generated = self.record["generated_solution"]
        self.assertEqual(generated["question_numbers"], [n for n in range(1, 29) if n not in (16, 27)])
        for number in (16, 27):
            self.assertIn("待核", self.blocks[number].body)
            self.assertNotIn("**答案：", self.blocks[number].body)
        self.assertEqual(self.blocks[28].subparts, (1, 2))
        self.assertEqual(generated["sha256"], hashlib.sha256((PROJECT / "解答草稿.md").read_bytes()).hexdigest())
        self.assertEqual(generated["question_draft_sha256"], self.record["draft_sha256"])
        self.assertEqual(generated["status"], "independently-reviewed")
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "independently-reviewed")
        review = self.record["independent_blind_review"]
        self.assertEqual(review["status"], "reviewed-with-source-issues")
        self.assertEqual(review["reviewers"], 2)
        self.assertEqual(review["reviewed_question_numbers"], list(range(1, 29)))
        self.assertEqual(review["verified_answer_question_numbers"], [n for n in range(1, 29) if n not in (16, 27)])
        self.assertEqual(review["confirmed_source_issue_question_numbers"], [16, 27])
        self.assertEqual(review["transcription_discrepancy_question_numbers"], [])
        self.assertEqual(review["source_pdf_sha256"], self.record["pdf_sha256"])
        self.assertEqual(review["question_draft_sha256"], self.record["draft_sha256"])
        self.assertEqual(review["current_solution_draft_sha256"], generated["sha256"])
        self.assertNotEqual(review["solution_draft_sha256"], review["current_solution_draft_sha256"])
        review_report = PROJECT / review["report_path"]
        self.assertEqual(hashlib.sha256(review_report.read_bytes()).hexdigest(), review["report_sha256"])
        self.assertIn("状态`independently-reviewed`", (PROJECT / generated["path"]).read_text(encoding="utf-8"))

    def test_choice_key_and_arts_numbering(self):
        key = ["A", "D", "D", "C", "D", "B", "B", "D", "D", "D", "B", "A", "C", "D", "D", None, "A", "C"]
        self.assertEqual(self.record["generated_solution"]["choice_key"], key)
        for number, answer in enumerate(key, 1):
            if answer is not None:
                self.assertIn(f"**答案：{answer}**", self.blocks[number].body)

    def test_q3_preserves_full_frequency_sign_solution(self):
        self.assertIn(r"y=\sin(\omega x)\cos(\omega x)", self.question_text)
        self.assertIn(r"\omega=\pm1/4", self.blocks[3].body)
        self.assertIn("原题未设", self.blocks[3].body)
        self.assertIn("选项只有正值", self.blocks[3].body)

    def test_q9_four_right_lateral_faces_are_constructible(self):
        points = {
            "A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0),
            "D": (0, 1, 0), "S": (0, 0, 1),
        }

        def subtract(a, b):
            return tuple(x - y for x, y in zip(a, b))

        def dot(a, b):
            return sum(x * y for x, y in zip(a, b))

        def cross(a, b):
            return (
                a[1] * b[2] - a[2] * b[1],
                a[2] * b[0] - a[0] * b[2],
                a[0] * b[1] - a[1] * b[0],
            )

        right_angle_edges = (
            (subtract(points["S"], points["A"]), subtract(points["B"], points["A"])),
            (subtract(points["S"], points["B"]), subtract(points["C"], points["B"])),
            (subtract(points["S"], points["D"]), subtract(points["C"], points["D"])),
            (subtract(points["S"], points["A"]), subtract(points["D"], points["A"])),
        )
        base_normal = cross(subtract(points["B"], points["A"]), subtract(points["D"], points["A"]))
        self.assertNotEqual(base_normal, (0, 0, 0))
        self.assertNotEqual(dot(base_normal, subtract(points["S"], points["A"])), 0)
        self.assertTrue(all(dot(first, second) == 0 for first, second in right_angle_edges))
        self.assertTrue(all(cross(first, second) != (0, 0, 0) for first, second in right_angle_edges))
        self.assertIn("四个侧面全为直角三角形", self.blocks[9].body)
        self.assertIn("上界可达", self.blocks[9].body)

    def test_q28_strict_difference_interval_makes_s6_unique_maximum(self):
        lower, upper = -F(24, 7), F(-3)

        def partial_sum(n, difference):
            return F(n, 2) * (24 + (n - 5) * difference)

        self.assertEqual(partial_sum(12, lower), 0)
        self.assertEqual(partial_sum(13, upper), 0)
        difference = -F(13, 4)
        self.assertLess(lower, difference)
        self.assertLess(difference, upper)
        self.assertGreater(partial_sum(12, difference), 0)
        self.assertLess(partial_sum(13, difference), 0)
        self.assertGreater(12 + 3 * difference, 0)  # a_6
        self.assertLess(12 + 4 * difference, 0)  # a_7
        self.assertLess(difference, 0)  # later a_n continue decreasing
        self.assertIn(r"-\dfrac{24}{7}<d<-3", self.blocks[28].body)
        self.assertIn("$S_6$ 唯一最大", self.blocks[28].body)

    def test_16_reused_solutions_preserve_input_hash_and_question_mapping(self):
        generated = self.record["generated_solution"]
        file = (PROJECT / generated["reused_from"]).resolve()
        self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), generated["reused_sha256"])
        science = {q.number: q for q in solution_sources.parse_question_blocks(file.read_text(encoding="utf-8"))}
        mapping = generated["arts_to_science"]
        self.assertEqual(len(mapping), 16)
        for arts, original in mapping.items():
            self.assertEqual(self.blocks[int(arts)].body, science[original].body)
        self.assertEqual(set(map(int, mapping)) | set(generated["newly_derived_questions"]), set(generated["question_numbers"]))
        self.assertFalse(set(map(int, mapping)) & set(generated["newly_derived_questions"]))

    def test_q2_ellipse_focus_sum_and_attainable_input_distance(self):
        a, b_squared, given_distance = F(5), F(16), F(3)
        c_squared = a * a - b_squared
        self.assertEqual(c_squared, 9)
        self.assertTrue(a - 3 <= given_distance <= a + 3)
        self.assertEqual(2 * a - given_distance, 7)

    def test_q4_fractional_exponents_select_unique_constant_term(self):
        constant_terms = [(r, F(comb(8, r) * (-1) ** r, 2 ** (8 - r)))
                          for r in range(9) if 8 - F(4 * r, 3) == 0]
        self.assertEqual(constant_terms, [(6, F(7))])
        self.assertIn(r"x\ne0", self.blocks[4].body)

    def test_q8_reflection_is_twice_foot_not_the_foot(self):
        normal = (F(8), F(6))
        norm_squared = sum(v * v for v in normal)
        foot = tuple(25 * v / norm_squared for v in normal)
        reflected = tuple(2 * v for v in foot)
        self.assertEqual(foot, (2, F(3, 2)))
        self.assertEqual(reflected, (4, 3))
        self.assertEqual(8 * foot[0] + 6 * foot[1], 25)
        self.assertEqual(8 * reflected[1] - 6 * reflected[0], 0)

    def test_q13_tangent_branch_and_strict_boundary(self):
        # alpha=pi-atan(p), beta=pi-atan(q), p,q>0.
        # sin(atan(p)+atan(q))>0; cos sign is sign(1-p*q).
        orders = set()
        for p, q in ((F(2), F(1)), (F(1), F(2)), (F(2), F(1, 2)), (F(1, 2), F(1)), (F(3), F(2))):
            premise = -p < -1 / q
            self.assertEqual(premise, 1 - p * q < 0)
            if premise:
                orders.add(p > q)
        self.assertEqual(orders, {True, False})  # neither alpha<beta nor beta<alpha necessary
        self.assertFalse(-F(2) < -1 / F(1, 2))  # equality is excluded

    def test_q19_alternating_finite_sum_and_limit(self):
        ratio = F(-1, 3)
        self.assertLess(abs(ratio), 1)
        for n in range(1, 21):
            actual = sum(F(1, 3) * ratio ** i for i in range(n))
            self.assertEqual(actual, F(1, 4) * (1 - ratio ** n))

    def test_q20_third_quadrant_negative_cosine(self):
        self.assertEqual(1 / (1 + F(2) ** 2), F(1, 5))
        self.assertIn("第三象限余弦负", self.blocks[20].body)
        self.assertIn(r"-\dfrac{\sqrt5}{5}", self.blocks[20].body)

    def test_q24_exact_polynomial_identity_in_quadratic_field(self):
        # monomial key = (cos(10) power, sin(10) power, sqrt(3) power mod 2)
        def multiply(first, second):
            result = {}
            for (c1, s1, r1), a in first.items():
                for (c2, s2, r2), b in second.items():
                    exponent = r1 + r2
                    key = (c1 + c2, s1 + s2, exponent % 2)
                    result[key] = result.get(key, F(0)) + a * b * 3 ** (exponent // 2)
            return result
        u = {(1, 0, 0): F(1, 2), (0, 1, 1): F(-1, 2)}
        v, radical = {(0, 1, 0): F(1)}, {(0, 0, 1): F(1)}
        terms = [multiply(u, u), multiply(v, v), multiply(radical, multiply(u, v))]
        expression = {}
        for term in terms:
            for key, value in term.items():
                expression[key] = expression.get(key, F(0)) + value
        self.assertEqual({k: v for k, v in expression.items() if v},
                         {(2, 0, 0): F(1, 4), (0, 2, 0): F(1, 4)})

    def test_q25_both_complex_roots_satisfy_unsquared_equation(self):
        for real, modulus in ((F(3), F(5)), (F(5, 3), F(13, 3))):
            self.assertEqual(real * real + 16, modulus * modulus)
            self.assertGreaterEqual(real + 7, 0)
            self.assertEqual(real - 2 * modulus, -7)
            self.assertEqual(3 * real * real - 14 * real + 15, 0)
        self.assertIn(r"z=3+4i", self.blocks[25].body)
        self.assertIn(r"z=\dfrac53+4i", self.blocks[25].body)

    def test_q26_midpoints_parallelogram_and_pyramid_volume_exactly(self):
        def subtract(a, b):
            return tuple(x - y for x, y in zip(a, b))
        def cross(u, v):
            return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
        for a in (F(1), F(2), F(5, 2)):
            origin, apex = (F(0), F(0), F(0)), (F(0), F(0), a)
            b, c, c1, d1 = (a, F(0), F(0)), (a, a, F(0)), (a, a, a), (F(0), a, a)
            e = tuple((x + y) / 2 for x, y in zip(origin, apex))
            f = tuple((x + y) / 2 for x, y in zip(c, c1))
            eb, ed1, ef, ea1 = subtract(b, e), subtract(d1, e), subtract(f, e), subtract(apex, e)
            self.assertEqual(ef, tuple(x + y for x, y in zip(eb, ed1)))
            normal = cross(eb, ed1)
            self.assertEqual(sum(x * y for x, y in zip(normal, ef)), 0)
            triple = sum(x * y for x, y in zip(normal, ea1))
            self.assertEqual(abs(triple) / 3, a ** 3 / 6)
        self.assertIn(r"\dfrac{a^3}{6}", self.blocks[26].body)


if __name__ == "__main__":
    unittest.main()

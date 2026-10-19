"""Exact-arithmetic regression checks for selected 1997 Shanghai science answers."""

import unittest
from fractions import Fraction
import hashlib
from pathlib import Path


def f6(n):
    return sum((Fraction(1, k) for k in range(n + 1, 2 * n + 1)), Fraction())


def b(n):
    return Fraction(2 * n + 1, 3)


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1997_上海卷_理科"
MATH_REVIEW = PAPER / "数学独立核验草稿.md"
PROVENANCE = PAPER / "来源校对.json"


class ShanghaiScienceMathChecks(unittest.TestCase):
    def test_math_status_stays_unverified_after_rejected_blind_attempts(self):
        import json

        record = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        self.assertEqual(record["mathematical_verification_status"], "not-verified")
        self.assertIn("not-accepted", record["verification"]["independent_math_review"])
        attempts = record["verification"]["blind_math_review_attempts"]
        self.assertEqual([attempt["status"] for attempt in attempts],
                         ["not-accepted", "partial-not-accepted"])
        self.assertEqual(record["math_review_draft_sha256"], hashlib.sha256(MATH_REVIEW.read_bytes()).hexdigest())

    def test_question_19_coordinate_review_preserves_angle_dependent_terms(self):
        # B=(0,0,0), A=(4,0,0), B'=(2,2sqrt(3),0), C=(0,0,3), C'=B'+C.
        # AC' has squared length 25; its normal component to plane BCC' has squared length 12.
        ac_squared = 2**2 + 12 + 3**2
        unit_normal_dot_coefficient_of_sqrt3 = Fraction(-2, 2) + Fraction(-2, 2)
        normal_component_squared = unit_normal_dot_coefficient_of_sqrt3**2 * 3
        self.assertEqual(ac_squared, 25)
        self.assertEqual(normal_component_squared, 12)
        self.assertEqual(Fraction(normal_component_squared, ac_squared), Fraction(12, 25))

    def test_question_20_a2_argument_range_uses_interior_maximum(self):
        def tangent_ratio(m):
            return Fraction(2 * m, 1 + m * m)

        self.assertEqual(tangent_ratio(1), Fraction(1))
        for m in (Fraction(1, 2), 2, 3, 10):
            ratio = tangent_ratio(m)
            self.assertGreater(ratio, 0)
            self.assertLess(ratio, 1)

    def test_question_6_difference_identity(self):
        for n in range(1, 25):
            self.assertEqual(f6(n + 1) - f6(n), Fraction(1, 2 * n + 1) - Fraction(1, 2 * n + 2))

    def test_question_16_distinct_line_ratios(self):
        nonzero = (1, 2, 3, 5, 7, 11)
        ratios = {Fraction(a, bb) for a in nonzero for bb in nonzero if a != bb}
        self.assertEqual(len(ratios), 30)
        self.assertEqual(Fraction(30, 7 * 6 * 5), Fraction(1, 7))

    def test_question_18_and_20_b2_exact_polynomial_results(self):
        self.assertEqual((Fraction(5, 2) - 1) ** 2, Fraction(9, 4))
        self.assertEqual((Fraction(-1, 2) - 1) ** 2, Fraction(9, 4))
        # For a=1, the washer integral is integral(-4*x^3 + 4*x^2) dx on [0,1].
        volume_coefficient = -Fraction(4, 4) + Fraction(4, 3)
        self.assertEqual(volume_coefficient, Fraction(1, 3))
        for a in range(1, 9):
            self.assertEqual(Fraction((3 * a) ** 3, 6), Fraction(9 * a**3, 2))
            self.assertEqual(-Fraction((-3 * a) ** 3, 6), Fraction(9 * a**3, 2))

    def test_question_21_branch_endpoints_and_ranges(self):
        p = lambda m: Fraction(m * m, m + 2)
        self.assertEqual(p(-1), Fraction(1))
        self.assertEqual(p(1), Fraction(1, 3))
        self.assertEqual(p(Fraction(-1, 2)), Fraction(1, 6))
        self.assertEqual(p(Fraction(1, 2)), Fraction(1, 10))

    def test_question_22_alternating_sum_closed_forms(self):
        for n in range(1, 31):
            actual = sum(((-1) ** (k - 1) * b(k) * b(k + 1) for k in range(1, n + 1)), Fraction())
            if n % 2 == 0:
                expected = -Fraction(2 * n * n + 6 * n, 9)
            else:
                expected = Fraction(2 * n * n + 6 * n + 7, 9)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

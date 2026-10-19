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
    def test_math_status_requires_full_independent_question_variant_coverage(self):
        import json

        record = json.loads(PROVENANCE.read_text(encoding="utf-8"))
        self.assertEqual(record["mathematical_verification_status"], "verified")
        self.assertEqual(record["source"]["source_authenticity"], "publisher-unverified")
        self.assertFalse(record["canonical_question_source_ready"])
        self.assertIsNone(record["official_answer"])
        self.assertEqual(record["review_status"], "needs-review")
        attempts = record["verification"]["blind_math_review_attempts"]
        self.assertTrue(any(attempt["status"] == "not-accepted" for attempt in attempts))
        self.assertTrue(any(attempt["status"] == "partial-not-accepted" for attempt in attempts))
        self.assertEqual([attempt["status"] for attempt in attempts],
                         [
                             "not-accepted",
                             "partial-not-accepted",
                             "accepted-partial",
                             "accepted-partial",
                             "accepted-partial",
                             "partial-not-accepted",
                             "accepted-partial",
                         ])
        partial = record["verification"]["independent_math_review_partial"]
        self.assertEqual(partial["scope"], "question 19(2) only")
        self.assertEqual(partial["status"], "accepted")
        self.assertEqual(partial["result"], r"arcsin(2√3/5)")
        self.assertEqual(
            record["verification"]["independent_math_review_accepted_scopes"],
            [
                "Q1-Q8", "Q9-Q16 including A1/B1", "Q17-Q18",
                "Q19(1)", "Q19(2)", "Q20 A2(1)", "Q20 A2(2)",
                "Q20 B2(1-2)", "Q21(1-3)", "Q22(1-3)",
            ],
        )
        self.assertIn(
            "Q20 A2(2) reports (pi/2, pi), omitting the attained minimum 3pi/4 at m=1",
            attempts[-2]["rejected_errors"],
        )
        self.assertEqual(attempts[-2]["status"], "partial-not-accepted")
        self.assertEqual(attempts[-2]["scope"], "Q17-Q22 except Q19(2), including Q20 A2/B2 variants")
        self.assertEqual(attempts[-2]["independently_matching_results"], [
            "Q17", "Q18", "Q19(1)", "Q20 A2(1)", "Q20 B2(1-2)",
            "Q21(1-3)", "Q22(1-3)",
        ])
        self.assertEqual(attempts[-2]["rejected_errors"], [
            "Q20 A2(2) reports (pi/2, pi), omitting the attained minimum 3pi/4 at m=1",
        ])
        self.assertEqual(attempts[-1]["reviewer"], "subagent-01a15662-347f-7921-9f78-390878ed9f5b")
        self.assertEqual(attempts[-1]["scope"], "Q20 A2(2) only")
        self.assertEqual(attempts[-1]["result"], "[3pi/4, pi)")
        self.assertEqual(record["verification"]["independent_math_review_q20_a2_2"]["status"], "accepted")
        self.assertEqual(record["verification"]["independent_math_review_q20_a2_2"]["result"], "[3pi/4, pi)")
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

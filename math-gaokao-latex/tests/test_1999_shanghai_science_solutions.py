"""Guards the independent first-pass solutions for 1999 Shanghai science Q1-Q16."""
import json
import math
import re
import unittest
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "math-gaokao-latex/1999_上海卷_理科"
SOLUTIONS = PAPER / "解析草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
SOURCE_RECORD = PAPER / "来源校对.json"

EXPECTED = {
    1: r"\boxed{2-\sqrt3}",
    2: r"\boxed{[3,+\infty)}",
    3: r"\boxed{40}",
    4: r"\boxed{2\sqrt3\text{或}\sqrt3}",
    5: r"\boxed{(2,2)}",
    6: r"\boxed{\pi}",
    7: r"\boxed{[-5\pi/6,-\pi/3]}",
    8: r"\boxed{\{\sqrt2/2,3\sqrt2/2\}}",
    9: r"\boxed{(\sqrt{10},0),(\sqrt{10},\pi)}",
    10: r"\boxed{9}",
    11: r"\boxed{8/36=2/9}",
    12: r"\boxed{\sqrt{11}/12}",
    13: r"\boxed{\text{C}}",
    14: r"\boxed{\text{D}}",
    15: r"\boxed{\text{B}}",
    16: r"\boxed{\text{C}}",
}

EXPECTED_ADVANCED = {
    17: r"\boxed{0\le a\le1}",
    18: r"\boxed{\frac32\lg2}",
    19: r"\boxed{[0,\frac\pi4)\cup(\frac{7\pi}4,2\pi)}",
    20: r"\boxed{\arccos\frac{\sqrt2}{4}}",
    21: r"2\sqrt6/3",
    22: r"(0,\sqrt2)",
}

EXTRA_ADVANCED = (
    r"400\sqrt6/9",
    r"\frac{\sqrt2}{2}\text{米}",
    r"P=\left(\frac a{\sqrt2},\frac{\sqrt2}{a}\right)",
    r"\sqrt{2\left(1-\frac4{a^4}\right)}",
    r"a^2-\dfrac4{a^2}",
    r"a>\sqrt[4]6",
)


class Shanghai1999ScienceIndependentSolutionsTests(unittest.TestCase):
    def test_independent_solution_draft_covers_q1_to_q16_with_checked_conclusions(self):
        self.assertTrue(SOLUTIONS.is_file(), "independent solution draft for Q1-Q16 is missing")
        text = SOLUTIONS.read_text(encoding="utf-8")
        numbers = [int(n) for n in re.findall(r"^### 第(\d+)题", text, re.MULTILINE)]
        self.assertEqual(numbers[:16], list(range(1, 17)))
        for number, conclusion in EXPECTED.items():
            with self.subTest(question=number):
                self.assertIn(conclusion, text)
        self.assertIn("独立推导草稿", text)
        self.assertIn("已完成首轮分段异人盲核", text)

    def test_machine_state_does_not_promote_draft_to_verified_solution(self):
        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        self.assertEqual(record["generated_solution_status"], "independent-draft-pending-review")
        self.assertEqual(record["review_status"], "pending")
        self.assertIsNone(record["official_answer"])
        review = record["independent_review"]
        self.assertEqual(review["status"], "partial-needs-adjudication")
        self.assertEqual(review["reviewed_question_ranges"], [[1, 12], [13, 22]])
        self.assertEqual(review["unresolved_questions"], [21])
        self.assertEqual(review["reviewer_errors"], [12, 15])

    def test_exact_counting_and_geometry_examples_match_the_written_proofs(self):
        self.assertEqual(comb(5, 2) * 2**2, 40)
        favorable = sum(m * m + n * n < 16 for m in range(1, 7) for n in range(1, 7))
        self.assertEqual(favorable, 8)
        self.assertEqual(favorable / 36, 2 / 9)
        base_area = math.sqrt(3) / 4
        height = math.sqrt(11 / 3)
        self.assertTrue(math.isclose(base_area * height / 3, math.sqrt(11) / 12, rel_tol=1e-14))

        # Exact squared-coordinate check for the blind review's second Q12
        # construction; determinant^2/36 yields V^2 = 7/72, i.e. (sqrt(14)/12)^2.
        x2 = y2 = Fraction(1, 8)
        z2 = Fraction(7, 8)
        self.assertEqual(4 * (x2 + y2), 1)
        self.assertEqual(4 * (x2 + z2), 4)
        self.assertEqual(4 * (y2 + z2), 4)
        determinant_squared = 256 * x2 * y2 * z2
        self.assertEqual(determinant_squared, Fraction(7, 2))
        self.assertEqual(determinant_squared / 36, Fraction(7, 72))

    def test_independent_solution_draft_covers_q17_to_q22_and_flags_argument_convention(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        numbers = [int(n) for n in re.findall(r"^### 第(\d+)题", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 23)))
        for number, conclusion in EXPECTED_ADVANCED.items():
            with self.subTest(question=number):
                self.assertIn(conclusion, text)
        self.assertIn("[0,2\\pi)", text)
        self.assertIn("不需填土", text)
        for conclusion in EXTRA_ADVANCED:
            with self.subTest(conclusion=conclusion):
                self.assertIn(conclusion, text)

    def test_exact_relations_for_q18_q20_q21_and_q22(self):
        for n in range(1, 20):
            self.assertEqual(sum(range(n + 1, 2 * n + 1)), n * (3 * n + 1) // 2)
        # In Q20, AE has unit length, CD has squared length 2, and their dot product is 1/2.
        self.assertEqual((1 / 2) ** 2 / 2, 1 / 8)
        self.assertAlmostEqual(1 - 1 / (2 * (1 / math.sqrt(2)) ** 2), 0)
        # The Q22 branch boundary is a^4=6, distinct from the admissible lower limit a^4>4.
        self.assertEqual(6**2 - 10 * 6 + 24, 0)
        self.assertEqual(4**2 - 10 * 4 + 24, 0)

    def test_q10_common_difference_and_unique_partial_sum_maximum(self):
        a1 = Fraction(1)
        d = -Fraction(4, 33) * a1
        term = lambda n: a1 + (n - 1) * d
        self.assertEqual(3 * term(4), 7 * term(7))
        self.assertEqual(term(9), Fraction(1, 33))
        self.assertEqual(term(10), -Fraction(1, 11))
        self.assertLess(d, 0)
        self.assertTrue(all(term(n) > 0 for n in range(1, 10)))
        self.assertTrue(all(term(n) < 0 for n in range(10, 40)))

    def test_q21_tangent_envelope_and_q22_valid_boundary_counterexample(self):
        # Q21: at t^2=1/2, the tangent-envelope half-base is t/2 and
        # its top half-width is >1, so it contains the original 1m half-span.
        t_squared = Fraction(1, 2)
        self.assertEqual(1 - Fraction(1, 2) / t_squared, 0)
        top_half_width_squared = (1 + t_squared) ** 2 / (4 * t_squared)
        self.assertEqual(top_half_width_squared, Fraction(9, 8))
        self.assertGreater(top_half_width_squared, 1)
        tangent_half_area_squared = Fraction(9, 16) * (
            t_squared + 1 / (4 * t_squared) + 1
        )
        tangent_total_area_squared = 4 * tangent_half_area_squared
        fixed_mouth_half_area = Fraction(3, 4) * (1 + Fraction(1, 2))
        fixed_mouth_total_area_squared = (2 * fixed_mouth_half_area) ** 2
        self.assertEqual(tangent_total_area_squared, Fraction(9, 2))
        self.assertEqual(fixed_mouth_total_area_squared, Fraction(81, 16))
        self.assertLess(tangent_total_area_squared, fixed_mouth_total_area_squared)
        # If the top opening were constrained to remain 2m, that is a
        # different optimization constraint; record its distinct candidate.
        self.assertEqual(2 * Fraction(1, 2), 1)

        # Q22: a=2,b=1 satisfies a>b>0 and ab=2, so the stated condition
        # does not imply the stricter a>2 claimed by the blind reviewer.
        a, b, u = Fraction(2), Fraction(1), Fraction(2)
        self.assertGreater(a, b)
        self.assertEqual(a * b, 2)
        self.assertEqual(u / a**2 + 1 / (u * b**2), 1)

    def test_q21_no_fill_does_not_impose_a_fixed_mouth_width(self):
        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        note = next(
            item for item in record["transcription_notes"]
            if item["question_number"] == 21
        )
        self.assertEqual(note["issue"], "q21-no-fill-mouth-width-interpretation")
        self.assertEqual(note["source_answer_transcription"], "√2/2 m")
        self.assertEqual(note["fixed_original_mouth_alternative"], "1 m")
        self.assertEqual(note["original_ditch_area"], "2 m²")
        self.assertEqual(note["tangent_candidate_area"], "3√2/2 m²")
        self.assertEqual(note["tangent_candidate_additional_area"], "3√2/2−2 m²")
        self.assertEqual(note["fixed_mouth_candidate_area"], "9/4 m²")
        self.assertEqual(note["fixed_mouth_candidate_additional_area"], "1/4 m²")
        self.assertEqual(note["source_diagram_scope"]["illustrates_question_part"], 2)
        self.assertEqual(note["source_diagram_scope"]["question_part_3_fixes_new_mouth_width"], False)
        self.assertEqual(
            note["source_diagram_scope"]["review_status"],
            "independently-reviewed-part-2-and-part-3-constraint-scope",
        )
        review = note["independent_review"]
        self.assertEqual(review["status"], "interpretation-remains-source-ambiguous")
        self.assertEqual(review["free_mouth_bottom_width"], "1/√2 m")
        self.assertEqual(review["fixed_original_mouth_bottom_width"], "1 m")
        self.assertEqual(note["status"], "independent-review-confirms-source-ambiguity")

        solution = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn("没有要求新沟口仍固定", solution)
        self.assertIn("若另加“沟口宽度固定为2米”", solution)
        self.assertIn("$3\\sqrt2/2$ 平方米", solution)
        self.assertIn("$9/4$ 平方米", solution)
        self.assertIn("独立数学复核已基于固定源题面与原图核验", solution)
        self.assertIn("题意仍有来源歧义", solution)

        answers = ANSWERS.read_text(encoding="utf-8")
        self.assertIn("未认证为官方答案", answers)
        self.assertIn("独立数学复核结合原图与题面确认", answers)
        self.assertIn("题意仍有来源歧义", answers)
        self.assertNotIn("仍待另一复核者裁定", answers)

    def test_q20_figure_review_confirms_source_topology_including_dashed_be(self):
        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        figure = next(item for item in record["figures"] if item["question_number"] == 20)
        review = figure["independent_review"]
        self.assertEqual(figure["status"], "vector-draft-rendered-independent-topology-review-passed")
        self.assertEqual(review["result"], "source-topology-and-labels-match")
        self.assertTrue(review["dashed_be_present_in_source"])
        self.assertEqual(review["proportions"], "schematic-not-assessed")

    def test_q21_global_minimum_covers_all_linear_trapezoid_sides(self):
        candidate_area_sum_squared = Fraction(2)
        nonpositive_slope_bound_squared = Fraction(2) ** 2
        shallow_slope_bound_squared = Fraction(3, 2) ** 2
        self.assertGreater(nonpositive_slope_bound_squared, candidate_area_sum_squared)
        self.assertGreater(shallow_slope_bound_squared, candidate_area_sum_squared)

        for slope in (Fraction(1, 2), Fraction(1), Fraction(3, 2)):
            excess_squared = (slope + 1 / (2 * slope)) ** 2 - 2
            square_identity = (2 * slope**2 - 1) ** 2 / (4 * slope**2)
            self.assertEqual(excess_squared, square_identity)
            self.assertGreaterEqual(excess_squared, 0)

        def add(left, right):
            return left[0] + right[0], left[1] + right[1]

        def multiply(left, right):
            return (
                left[0] * right[0] + 2 * left[1] * right[1],
                left[0] * right[1] + left[1] * right[0],
            )

        inverse_two_t = (Fraction(0), Fraction(1, 2))
        for root_s in (Fraction(0), Fraction(1, 2), Fraction(1)):
            s = root_s**2
            tangent_difference = add(
                multiply((s + Fraction(1, 2), Fraction(0)), inverse_two_t),
                (-root_s, Fraction(0)),
            )
            root_minus_t = (root_s, Fraction(-1, 2))
            squared_difference = multiply(root_minus_t, root_minus_t)
            factored_difference = multiply(squared_difference, inverse_two_t)
            self.assertEqual(tangent_difference, factored_difference)

        solution = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"h(s)\ge\sqrt{s}", solution)
        self.assertIn(r"q(x)=a+dx^2-x\ge0", solution)
        self.assertIn(r"\frac{s+t^2}{2t}-\sqrt{s}", solution)
        self.assertIn(r"\frac{(\sqrt{s}-t)^2}{2t}\ge0", solution)
        self.assertIn("h(s)=a+ds", solution)
        self.assertIn("q(x)=a+dx^2-x", solution)
        self.assertIn(r"d\le0", solution)
        self.assertIn(r"0<d\le1/2", solution)
        self.assertIn(r"d\ge1/2", solution)
        self.assertIn(r"a\ge1/(4d)", solution)
        self.assertIn(r"\ge d+\frac1{2d}\ge\sqrt2", solution)
        self.assertIn("c=1", solution)
        self.assertIn(r"4d(1-d)\ge1", solution)

    def test_q15_reciprocal_and_squared_inequality_truth_values(self):
        for a, b in ((Fraction(-3), Fraction(-2)),
                     (Fraction(-2), Fraction(-1)),
                     (Fraction(-5, 2), Fraction(-3, 2))):
            self.assertLess(a, b)
            self.assertLess(b, 0)
            first_a_inequality = Fraction(1, 1) / a > Fraction(1, 1) / b
            second_a_inequality = (
                Fraction(1, 1) / abs(a) > Fraction(1, 1) / abs(b)
            )
            self.assertTrue(first_a_inequality)
            self.assertFalse(second_a_inequality)
            self.assertFalse(Fraction(1, 1) / (a - b) > Fraction(1, 1) / a)
            self.assertFalse(Fraction(1, 1) / abs(a) > Fraction(1, 1) / abs(b))
            left = (a + Fraction(1, 1) / b) ** 2
            right = (b + Fraction(1, 1) / a) ** 2
            self.assertGreater(left, right)
            option_truth = (
                not first_a_inequality and not second_a_inequality,
                not (Fraction(1, 1) / (a - b) > Fraction(1, 1) / a)
                and not second_a_inequality,
                not (Fraction(1, 1) / (a - b) > Fraction(1, 1) / a)
                and not (left > right),
                not second_a_inequality and not (left > right),
            )
            self.assertEqual(option_truth, (False, True, False, False))
            self.assertEqual(
                left - right,
                (a - b) * (a + b) * (1 + Fraction(1, 1) / (a * b)) ** 2,
            )

        solution = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(
            r"\left(a+\frac1b\right)^2-\left(b+\frac1a\right)^2" + "\n=(a-b)",
            solution,
        )
        self.assertIn(
            r"(a-b)(a+b)\left(1+\frac1{ab}\right)^2",
            solution,
        )
        self.assertIn("选项B所列两个", solution)


if __name__ == "__main__":
    unittest.main()

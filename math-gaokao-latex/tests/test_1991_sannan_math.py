from fractions import Fraction
from itertools import permutations
from math import comb, sqrt
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "1991"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Sannan1991MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = (SOURCE / "1991_数学真题_三南_试题.md").read_text(encoding="utf-8")
        cls.answers = (SOURCE / "1991_数学真题_三南_答案要点.md").read_text(encoding="utf-8")
        cls.solution = (SOURCE / "1991_数学真题_三南_解析正文.md").read_text(encoding="utf-8")
        cls.points = solution_sources.parse_answer_points(cls.answers)

    def test_all_30_questions_solutions_and_answer_points_align(self):
        questions = solution_sources.parse_question_blocks(self.questions)
        solutions = solution_sources.parse_question_blocks(self.solution)
        expected = list(range(1, 31))
        self.assertEqual([q.number for q in questions], expected)
        self.assertEqual([q.number for q in solutions], expected)
        self.assertEqual([p.number for p in self.points], expected)
        self.assertEqual([q.subparts for q in questions], [q.subparts for q in solutions])
        self.assertEqual(questions[-1].subparts, (1, 2))
        self.assertIn("严格递增", self.points[-1].answer_for(1))
        self.assertIn(r"n\ge3", self.points[-1].answer_for(2))

    def test_choice_key_and_answer_attribution(self):
        self.assertEqual(
            [p.answer_for(None) for p in self.points[:18]],
            ["B", "A", "C", "B", "C", "B", "D", "D", "C",
             "A", "D", "B", "B", "D", "B", "A", "C", "D"],
        )
        self.assertIn("非官方", self.answers)
        self.assertIn("待独立复核", self.answers)
        self.assertIn("非官方", self.solution)
        self.assertIn("原题未预设坐标系", self.points[28].answer_for(None))

    def test_combined_renderer_round_trip(self):
        combined = solution_sources.render_combined(self.questions, self.solution, self.answers)
        self.assertEqual(
            solution_sources.extract_solution_blocks(combined, self.questions), self.solution
        )

    def test_local_section_break_is_not_copied_into_answer_bodies(self):
        hook = r"\AddToHookNext{file/questions.tex/after}{\clearpage}"
        self.assertTrue(hook in self.questions, "缺少本卷题面结束换页钩子")
        question_tex = (ROOT / "1991_三南卷" / "questions.tex").read_text(encoding="utf-8")
        answer_tex = (ROOT / "1991_三南卷" / "answers.tex").read_text(encoding="utf-8")
        self.assertEqual(question_tex.count(hook), 1)
        self.assertNotIn(hook, answer_tex)
        self.assertTrue(all(
            hook not in q.body
            for q in solution_sources.parse_question_blocks(self.questions)
        ))

    def test_q9_fourth_quadrant_and_explicit_argument_conventions(self):
        # sin(4pi/3)=-sqrt(3)/2, cos(4pi/3)=-1/2 in the source expression.
        real_radical_coefficient = -3 * Fraction(-1, 2)
        imaginary = -3 * (-Fraction(-1, 2))
        self.assertEqual(3 * real_radical_coefficient ** 2 + imaginary ** 2, 9)
        self.assertGreater(real_radical_coefficient, 0)
        self.assertLess(imaginary, 0)
        self.assertIn(r"\dfrac{11\pi}6", self.answers)
        self.assertIn(r"(-\pi,\pi]", self.solution)
        self.assertIn(r"-\pi/6", self.solution)

    def test_q11_reflection_has_midpoint_on_line_and_normal_displacement(self):
        point, normal = (4, 0), (5, 4)
        offset = Fraction(5 * point[0] + 4 * point[1] + 21, 5 ** 2 + 4 ** 2)
        reflected = tuple(v - 2 * offset * n for v, n in zip(point, normal))
        self.assertEqual(reflected, (-6, -8))
        midpoint = tuple(Fraction(v + w, 2) for v, w in zip(point, reflected))
        self.assertEqual(5 * midpoint[0] + 4 * midpoint[1] + 21, 0)
        self.assertEqual(self.points[10].answer_for(None), "D")

    def test_q13_full_permutation_enumeration(self):
        valid = [p for p in permutations(range(6)) if p[0] != 0]
        self.assertEqual(len(valid), 600)
        self.assertEqual(sum(p[-1] < p[-2] for p in valid), 300)
        self.assertEqual(self.points[12].answer_for(None), "B")

    def test_q16_constant_term_and_q18_real_intersection_filter(self):
        self.assertEqual(comb(6, 3) * (-2) ** 3, -160)
        roots = (Fraction(-1), Fraction(13, 2))
        self.assertTrue(all(2 * x * x - 11 * x - 13 == 0 for x in roots))
        allowed = [(x, -3 * (x + 1) / 2) for x in roots if -3 * (x + 1) / 2 >= 0]
        self.assertEqual(allowed, [(Fraction(-1), Fraction(0))])
        self.assertEqual(self.points[15].answer_for(None), "A")
        self.assertEqual(self.points[17].answer_for(None), "D")

    def test_q20_exact_complex_arithmetic(self):
        denominator_real, denominator_imaginary = 2, -1
        norm_squared = denominator_real ** 2 + denominator_imaginary ** 2
        quotient = (
            Fraction(denominator_imaginary, norm_squared),
            Fraction(denominator_real, norm_squared),
        )
        conjugate_term = (Fraction(1, 5), Fraction(3, 5))
        self.assertEqual(tuple(a + b for a, b in zip(quotient, conjugate_term)), (0, 1))
        self.assertEqual(self.points[19].answer_for(None), "$1$")

    def test_q25_acute_angle_difference(self):
        tan_alpha, tan_delta = Fraction(3, 4), Fraction(1, 3)
        tan_beta = (tan_alpha - tan_delta) / (1 + tan_alpha * tan_delta)
        self.assertEqual(tan_beta, Fraction(1, 3))
        self.assertEqual(1 / (1 + tan_beta ** 2), Fraction(9, 10))
        self.assertIn(r"\dfrac{3\sqrt{10}}{10}", self.points[24].answer_for(None))

    def test_q26_root_endpoint_and_unsquared_negative_branch(self):
        # r=-1+sqrt(14)/2: check 2r^2+4r-5=0 in Q(sqrt(14)).
        rational, radical = Fraction(-1), Fraction(1, 2)
        self.assertEqual(2 * (rational ** 2 + 14 * radical ** 2) + 4 * rational - 5, 0)
        self.assertEqual(4 * rational * radical + 4 * radical, 0)
        upper = -1 + sqrt(14) / 2
        for x in (-6, -5, -4, -1, 0, Fraction(1, 2), 1, 2):
            with self.subTest(x=x):
                radicand = 5 - 4 * x - x * x
                original = radicand >= 0 and sqrt(radicand) >= x
                self.assertEqual(original, -5 <= x <= upper)
        self.assertIn(r"\left[-5,-1+\dfrac{\sqrt{14}}2\right]", self.points[25].answer_for(None))

    def test_q27_orthogonality_uses_the_given_height_and_midpoint(self):
        self.assertIn(r"AA_1=\sqrt6", self.questions)
        ca_squared, height_squared = Fraction(3), Fraction(6)
        self.assertEqual(ca_squared - height_squared / 2, 0)
        self.assertIn(r"AB_1\perp A_1M", self.points[26].answer_for(None))

    def test_q28_unique_admissible_ratio_satisfies_all_three_constraints(self):
        candidates = (Fraction(1, 3), Fraction(4, 3))
        self.assertTrue(all(9 * q * q - 15 * q + 4 == 0 for q in candidates))
        self.assertEqual([q for q in candidates if abs(q) < 1], [Fraction(1, 3)])
        q, b1, d = Fraction(1, 3), Fraction(6), Fraction(1, 2)
        self.assertEqual(b1 / (1 - q), 9)
        self.assertEqual(1 + 2 * d, b1 * q)
        self.assertEqual(5 + 10 * d, 2 * b1 * (1 + q) - 6)
        self.assertIn(r"a_n=\dfrac{n+1}2", self.points[27].answer_for(None))

    def test_q29_positive_axis_ratio_and_segment_division(self):
        ratios = (Fraction(3), Fraction(-7, 16))
        self.assertTrue(all(16 * t * t - 41 * t - 21 == 0 for t in ratios))
        self.assertEqual([t for t in ratios if t > 0], [Fraction(3)])
        a_squared, b_squared, c = Fraction(1), Fraction(3), Fraction(2)
        self.assertEqual(a_squared * b_squared, 3)
        self.assertEqual(a_squared + b_squared, c * c)
        x, y_squared = Fraction(4, 3), Fraction(7, 3)
        self.assertTrue(0 < x < c)
        self.assertEqual(x * x / a_squared - y_squared / b_squared, 1)
        qf2_squared = (x - c) ** 2 + y_squared
        pq_squared = x * x + 21 * (Fraction(1, 3) - 1) ** 2
        self.assertEqual(qf2_squared, Fraction(25, 9))
        self.assertEqual(pq_squared / qf2_squared, 4)
        self.assertIn(r"x^2-\dfrac{y^2}3=1", self.points[28].answer_for(None))

    def test_q30_integer_checks_supplement_the_induction_proof(self):
        for n in range(3, 101):
            self.assertGreater(2 ** n, 2 * n + 1)
            self.assertGreater(Fraction(2 ** n - 1, 2 ** n + 1), Fraction(n, n + 1))
        values = [(Fraction(2) ** n - 1) / (Fraction(2) ** n + 1) for n in range(-5, 6)]
        self.assertTrue(all(a < b for a, b in zip(values, values[1:])))
        self.assertIn("数学归纳法", self.solution)


if __name__ == "__main__":
    unittest.main()

"""Exact-arithmetic regression checks for the 1998 Shanghai arts solution draft."""
import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
sys.path.insert(0, str(PROJECT / "tools"))
import issues as issue_ledger

PAPER = ROOT / "math-gaokao-latex/1998_上海卷_文科"
DRAFT = PAPER / "解析草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
QUESTIONS = PAPER / "题面转录草稿.md"


class Shanghai1998ArtsSolutionTests(unittest.TestCase):
    def test_q1_logarithm_terms_combine_to_logarithm_of_100(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\lg 20+\log_{100}25", questions)
        self.assertEqual(20 * 5, 100)
        self.assertEqual(math.log10(100), 2.0)
        self.assertIn(r"\lg20+\lg5=2", draft)

    def test_q2_amplitude_and_minimum_force_a_to_equal_five(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\sqrt a\cos x", questions)
        self.assertIn("最小值为 $1$", questions)
        a = 3**2 - 2**2
        self.assertEqual(a, 5)
        self.assertEqual(4 - math.sqrt(4 + a), 1.0)
        self.assertIn(r"a=5", draft)

    def test_q3_limit_at_one_forces_a_to_equal_four(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"x^2+ax+3}{x^3+3}", questions)
        denominator_at_one = 1**3 + 3
        numerator_at_one = 2 * denominator_at_one
        a = numerator_at_one - 1**2 - 3
        self.assertEqual(Fraction(numerator_at_one, denominator_at_one), 2)
        self.assertEqual(a, 4)
        self.assertIn(r"得 $a=4$", draft)

    def test_q4_inverse_composes_with_the_real_cube_root_transform(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"(x-1)^{1/3}+2", questions)
        for x in range(-3, 4):
            inverse_x = (x - 2) ** 3 + 1
            real_cube_root = next(
                root for root in range(-10, 11) if root**3 == inverse_x - 1
            )
            self.assertEqual(real_cube_root + 2, x)
        self.assertIn(r"f^{-1}(x)=(x-2)^3+1", draft)

    def test_q5_regular_tetrahedron_volume_is_two_sqrt_two_over_three(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"棱长为 $2$ 的正四面体", questions)
        base_area_squared = 3
        height_squared = Fraction(8, 3)
        volume_squared = Fraction(base_area_squared, 9) * height_squared
        self.assertEqual(volume_squared, Fraction(8, 9))
        self.assertIn(r"V=\frac{2\sqrt2}{3}", draft)

    def test_q7_hypergeometric_probability_is_eighteen_thirty_fifths(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn("4个白球和3个黑球", questions)
        favorable = math.comb(3, 1) * math.comb(4, 2)
        total = math.comb(7, 3)
        self.assertEqual(Fraction(favorable, total), Fraction(18, 35))
        self.assertIn(r"=18/35", draft)

    def test_q8_piecewise_function_attains_global_maximum_four_at_one(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"2x+3,&x\le 0", questions)
        self.assertIn(r"x+3,&0<x\le1", questions)
        self.assertIn(r"-x+5,&x>1", questions)
        self.assertEqual(2 * 0 + 3, 3)
        self.assertEqual(1 + 3, 4)
        self.assertLess(Fraction(5) - Fraction(101, 100), 4)
        self.assertIn("故最大值4", draft)

    def test_q9_binomial_coefficient_condition_has_unique_natural_solution_four(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\left(1+\dfrac{x}{n}\right)^n", questions)
        self.assertEqual(Fraction(math.comb(4, 3), 4**3), Fraction(1, 16))
        roots = (Fraction(24 + 16, 10), Fraction(24 - 16, 10))
        for root in roots:
            self.assertEqual(5 * root**2 - 24 * root + 16, 0)
        admissible = [root for root in roots if root.denominator == 1 and root >= 3]
        self.assertEqual(admissible, [Fraction(4)])
        self.assertIn(r"自然数解为$n=4$", draft)

    def test_q10_arithmetic_means_form_a_geometric_series_with_sum_two(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn("$a_1=2$", questions)
        self.assertIn(r"3a_{n+1}-a_n=0", questions)
        partial_sum = Fraction()
        for n in range(1, 9):
            a_n = Fraction(2, 3 ** (n - 1))
            a_next = a_n / 3
            b_n = (a_n + a_next) / 2
            self.assertEqual(b_n, Fraction(4, 3**n))
            partial_sum += b_n
        self.assertEqual(partial_sum, 2 * (1 - Fraction(1, 3**8)))
        self.assertIn(
            r"\sum_{n=1}^\infty b_n=(2/3)\cdot 2/(1-1/3)=2", draft
        )

    def test_q11_shared_foci_and_asymptotes_force_hyperbola_axes(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\dfrac{x^2}{49}+\dfrac{y^2}{24}=1", questions)
        self.assertIn(r"y=\pm\dfrac43x", questions)
        focal_distance_squared = 49 - 24
        scale_squared = Fraction(focal_distance_squared, 3**2 + 4**2)
        self.assertEqual(focal_distance_squared, 25)
        self.assertEqual(scale_squared, 1)
        self.assertEqual((9 * scale_squared, 16 * scale_squared), (9, 16))
        self.assertIn(r"\frac{x^2}{9}-\frac{y^2}{16}=1", draft)

    def test_q12_only_option_b_is_even_with_fundamental_period_pi_over_two(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        x = math.pi / 11
        option_b = lambda value: math.cos(4 * value)
        self.assertAlmostEqual(option_b(-x), option_b(x))
        self.assertAlmostEqual(option_b(x + math.pi / 2), option_b(x))
        self.assertAlmostEqual(math.sin(4 * math.pi / 8), 1.0)
        self.assertAlmostEqual(math.sin(-4 * math.pi / 8), -1.0)
        self.assertAlmostEqual(math.tan(2 * math.pi / 8), 1.0)
        self.assertAlmostEqual(math.tan(-2 * math.pi / 8), -1.0)
        self.assertAlmostEqual(math.cos(2 * (0 + math.pi / 2)), -1.0)
        self.assertIn(r"\cos^22x-\sin^22x", questions)
        self.assertIn("选B", draft)

    def test_q13_logarithm_graph_never_enters_the_first_quadrant(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn("$0<a<1$", questions)
        base = 0.5
        second_quadrant_y = math.log(-4.5 + 5, base)
        third_quadrant_y = math.log(-3.5 + 5, base)
        fourth_quadrant_y = math.log(1 + 5, base)
        self.assertGreater(second_quadrant_y, 0)
        self.assertLess(third_quadrant_y, 0)
        self.assertLess(fourth_quadrant_y, 0)
        self.assertIn("第一象限不经过，选A", draft)

    def test_q15_eleventh_element_in_b_makes_only_option_d_true(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"11\in B", questions)
        self.assertIn(r"A=\{x\mid x^2-5x-6>0\}", questions)
        self.assertIn(r"B=\{x\mid |x-5|<a\}", questions)
        q15_solution = draft.split("**15．**", 1)[1].split("**16．**", 1)[0]
        self.assertIn(r"$a>6$", q15_solution)

        # |11-5|<a forces a>6. Then B contains [-1, 6], the
        # complement of A=(-infinity,-1) union (6,infinity).
        for a in (Fraction(601, 100), Fraction(7), Fraction(100)):
            self.assertGreater(a, 6)
            self.assertLess(Fraction(5) - a, -1)
            self.assertGreater(Fraction(5) + a, 6)

            # Witnesses disprove options A, B, and C respectively.
            witness_a = 6 + a
            self.assertGreater(witness_a, 6)  # in A, not in complement(A)
            self.assertGreater(abs(witness_a - 5), a)  # outside B
            self.assertGreater(5, -1)
            self.assertLess(5, 6)  # 5 is in complement(A)
            self.assertGreater(a, abs(5 - 5))  # 5 is in B
            self.assertGreater(7, 6)  # 7 is in A
            self.assertGreater(a, abs(7 - 5))  # and also in B

        self.assertIn(r"\overline A=[-1,6]", q15_solution)
        self.assertIn(r"\overline A\subset B", q15_solution)
        self.assertIn("故D是唯一正确项", q15_solution)

    def test_q16_sine_rule_makes_the_two_lines_perpendicular(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\sin A\,x+ay+c=0", questions)
        self.assertIn(r"bx-\sin B\,y+\sin C=0", questions)
        a, b, circumradius = 4, 6, 5
        sin_a = Fraction(a, 2 * circumradius)
        sin_b = Fraction(b, 2 * circumradius)
        normal_dot = sin_a * b - a * sin_b
        self.assertEqual(normal_dot, 0)
        self.assertIn("故两直线垂直，选C", draft)

    def test_q17_second_quadrant_angle_gives_the_exact_sine_value(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\alpha$ 是第二象限角", questions)
        sin_alpha = Fraction(3, 5)
        cos_alpha = Fraction(-4, 5)
        sin_double = 2 * sin_alpha * cos_alpha
        cos_double = cos_alpha**2 - sin_alpha**2
        self.assertEqual(sin_double, Fraction(-24, 25))
        self.assertEqual(cos_double, Fraction(7, 25))
        value_without_sqrt = Fraction(7, 50)
        sqrt3_coefficient = Fraction(24, 50)
        exact_value = float(value_without_sqrt) + float(sqrt3_coefficient) * math.sqrt(3)
        reduced_angle_value = math.sin(math.pi / 6 - 2 * (math.pi - math.asin(3 / 5)))
        self.assertAlmostEqual(exact_value, reduced_angle_value)
        self.assertIn(r"\frac{7+24\sqrt3}{50}", draft)

    def test_q18_complex_conditions_force_the_recorded_modulus(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"复数 $z_2$ 的虚部为 $2$", questions)
        self.assertIn(r"z_1\cdot z_2", questions)

        # (x-2+yi)i=-y+(x-2)i=1+i, hence z1=3-i.
        z1 = (3, -1)
        self.assertEqual((-z1[1], z1[0] - 2), (1, 1))
        # For z2=u+2i, Im(z1*z2)=3*2-u=0, so u=6.
        z2 = (6, 2)
        self.assertEqual(z1[0] * z2[1] + z1[1] * z2[0], 0)
        self.assertEqual(z1[0] * z2[0] - z1[1] * z2[1], 20)
        self.assertEqual(z2[0] ** 2 + z2[1] ** 2, 40)
        self.assertIn(r"z_2=6+2i", draft)
        self.assertIn(r"|z_2|=2\sqrt{10}", draft)

    def test_q20_chord_area_forces_the_two_reported_slopes(self):
        # For y=k(x-2) on y^2=4(x-1), the triangle area is
        # 2*sqrt(1+k^2)/|k|.  Squaring area=4 gives k^2=1/3.
        k_squared = Fraction(1, 3)
        area_squared = 4 * (1 + k_squared) / k_squared
        self.assertEqual(area_squared, 16)
        self.assertAlmostEqual(math.tan(math.pi / 6) ** 2, float(k_squared))
        self.assertAlmostEqual(math.tan(5 * math.pi / 6) ** 2, float(k_squared))

    def test_q21_cubic_satisfies_measurements_extrema_and_average(self):
        temperature = lambda t: t**3 - 3 * t + 60
        derivative = lambda t: 3 * t**2 - 3
        self.assertEqual((temperature(-4), temperature(0), temperature(1)), (8, 60, 58))
        self.assertEqual(derivative(-4), derivative(4))
        candidates = [temperature(t) for t in (-2, -1, 1, 2)]
        self.assertEqual(max(candidates), 62)
        self.assertEqual((temperature(-1), temperature(2)), (62, 62))
        # Exact antiderivative evaluation on [-4,4].
        integral = Fraction(4**4 - (-4) ** 4, 4) - (4**2 - (-4) ** 2) + 60 * (4 - (-4))
        average = Fraction(1, 8) * integral
        self.assertEqual(average, 60)

    def test_q22_sequence_identities_and_limits_are_consistent(self):
        for n in range(1, 12):
            a_n = Fraction(-(2 * n + 3), 2)
            b_n = Fraction(-(12 * n + 5), 4)
            sum_a = sum((Fraction(-(2 * j + 3), 2) for j in range(1, n + 1)), Fraction())
            sum_b = sum((Fraction(-(12 * j + 5), 4) for j in range(1, n + 1)), Fraction())
            self.assertEqual(4 * sum_b - 12 * sum_a, 13 * n)
            self.assertEqual(2 * a_n, -2 * n - 3)
            self.assertEqual(4 * b_n, -12 * n - 5)
            self.assertEqual(sum(2 * j + 3 for j in range(1, n + 1)), n**2 + 4 * n)
        # Leading coefficients of sum(k_i) and a_n*b_n are 1 and 24/8.
        numerator_lead = Fraction(1)
        denominator_lead = Fraction(2 * 12, 8)
        self.assertEqual(numerator_lead / denominator_lead, Fraction(1, 3))

    def test_q22_set_indices_follow_the_defined_positive_sequence_domain(self):
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"集合指标沿用题设数列项的正整数定义域，不另加未定义的$n=0$项", draft)
        self.assertIn(r"$4b_n=-12n-5=2a_{6n+1}$", draft)
        self.assertIn(r"$c_n=-101-12(n-1)=-12n-89$", draft)

        x = lambda n: -2 * n - 3
        y = lambda n: -12 * n - 5
        for n in range(1, 21):
            self.assertEqual(y(n), x(6 * n + 1))

        # n=7 gives -89 (excluded); n=8 is the first term below -100.
        self.assertEqual(y(7), -89)
        self.assertEqual(y(8), -101)
        self.assertEqual([y(n) for n in range(8, 11)], [-101, -113, -125])
        self.assertEqual([-12 * j - 89 for j in range(1, 4)], [-101, -113, -125])

    def test_drafts_preserve_corrected_q15_condition_and_review_boundary(self):
        draft = DRAFT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        questions = QUESTIONS.read_text(encoding="utf-8")
        self.assertIn(r"且 $11\in B$", questions)
        self.assertIn("a>6", draft)
        self.assertIn("D是唯一正确项", draft)
        self.assertIn("此前登记的 `ISSUE-1115`", answers)
        self.assertIn("现已按原页更正并解决", answers)
        self.assertIn("经过第三象限", draft)
        self.assertIn("123.6", draft)
        self.assertIn(r"\theta=\arccos\!\left(\frac{7\sqrt{10}}{40}\right)", draft)
        self.assertIn("原题未另作定义", draft)
        self.assertIn("y=a(x-a_n)^2+b_n", questions)
        self.assertIn("不能标作官方答案", answers)
        self.assertNotIn("canonical", draft)
        self.assertNotIn("complete", draft)

    def test_q15_condition_11_in_b_makes_d_the_unique_true_option(self):
        # 11 in (5-a,5+a) implies a>6. At a=7, B=(-2,12) contains
        # the complement of A, while each other option has a counterexample.
        a_parameter = 7
        a_contains = lambda x: x < -1 or x > 6
        b_contains = lambda x: 5 - a_parameter < x < 5 + a_parameter
        self.assertTrue(b_contains(11))
        self.assertGreater(a_parameter, 6)
        self.assertLess(5 - a_parameter, -1)
        self.assertGreater(5 + a_parameter, 6)
        self.assertFalse((not a_contains(-3)) or b_contains(-3))
        self.assertFalse(a_contains(0) or (not b_contains(0)))
        self.assertFalse((not a_contains(7)) or (not b_contains(7)))
        self.assertTrue(a_contains(-2) or b_contains(-2))
        self.assertTrue(a_contains(0) or b_contains(0))
        self.assertTrue(a_contains(7) or b_contains(7))

    def test_q15_transcription_issue_is_resolved_without_inventing_paper_identity(self):
        manifest = json.loads(
            (PROJECT / "source-manifest.json").read_text(encoding="utf-8")
        )
        source_id = "src-8c86b3e592e594953609fe09d0c182d5252c944006503dfb10e8efa1962aeca7"
        source = next(
            item for item in manifest["sources"]
            if item["source_id"] == source_id
        )
        self.assertEqual(source["paper_id"], "gk-1998-regular-shanghai-arts")
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["issue_ids"], [])

        issue = next(
            item for item in issue_ledger.load_issues(PROJECT / "missing-issues.md")
            if item["issue_id"] == "ISSUE-1115"
        )
        self.assertEqual(issue["source_id"], source_id)
        self.assertIsNone(issue["paper_id"])
        self.assertEqual(issue["type"], "source-mismatch")
        self.assertEqual(issue["status"], "resolved")
        self.assertEqual(issue["impact"], "blocks_completion")
        self.assertIn("11∈B", issue["resolved_evidence"])

    def test_q19_1_cross_section_selects_the_named_dihedral_sector(self):
        questions = QUESTIONS.read_text(encoding="utf-8")
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn(r"\angle DAB=60^\circ", questions)
        self.assertIn(r"二面角 $O_1-BC-D$", questions)

        side_squared = 4**2
        cosine_60 = Fraction(1, 2)
        diagonal_ac_squared = 2 * side_squared * (1 + cosine_60)
        diagonal_bd_squared = 2 * side_squared * (1 - cosine_60)
        oa_squared = diagonal_ac_squared / 4
        ob_squared = diagonal_bd_squared / 4
        triangle_obc_area_squared = oa_squared * ob_squared / 4
        distance_of_squared = 4 * triangle_obc_area_squared / 4**2
        tangent_squared = Fraction(6**2, 1) / distance_of_squared
        self.assertEqual((oa_squared, ob_squared), (12, 4))
        self.assertEqual(triangle_obc_area_squared, 12)
        self.assertEqual(distance_of_squared, 3)
        self.assertEqual(tangent_squared, 12)

        # O and D are on the same side of BC, so the section rays FO and FO1
        # represent the sector named by O1-BC-D rather than its supplement.
        root3 = math.sqrt(3)
        b, c, o, d = (0, 2), (-2 * root3, 0), (0, 0), (0, -2)
        bc = (c[0] - b[0], c[1] - b[1])
        bo = (o[0] - b[0], o[1] - b[1])
        bd = (d[0] - b[0], d[1] - b[1])
        cross_to_o = bc[0] * bo[1] - bc[1] * bo[0]
        cross_to_d = bc[0] * bd[1] - bc[1] * bd[0]
        self.assertGreater(cross_to_o * cross_to_d, 0)
        self.assertIn(r"\arctan(2\sqrt3)", draft)

    def test_q19_2_coordinates_and_line_angle_match_exact_dot_products(self):
        draft = DRAFT.read_text(encoding="utf-8")
        origin = (0, 0, 0)
        a = (2 * math.sqrt(3), 0, 0)
        b1 = (0, 2, 6)
        d1 = (0, -2, 6)
        o1 = (0, 0, 6)
        e = tuple((u + v) / 2 for u, v in zip(o1, a))
        self.assertEqual(e, (math.sqrt(3), 0, 3))

        left = tuple(u - v for u, v in zip(b1, origin))
        dot = 0 * 0 + 2 * 2 + 6 * (-3)
        left_norm_squared = sum(value * value for value in left)
        right_norm_squared = 3 + 2**2 + (-3) ** 2
        self.assertEqual(dot, -14)
        self.assertEqual(left_norm_squared, 40)
        self.assertEqual(right_norm_squared, 16)
        self.assertEqual(Fraction(dot**2, left_norm_squared * right_norm_squared), Fraction(49, 160))
        cosine = dot / math.sqrt(left_norm_squared * right_norm_squared)
        self.assertLess(cosine, 0)
        self.assertAlmostEqual(abs(cosine), 7 * math.sqrt(10) / 40)
        line_angle = math.acos(abs(cosine))
        self.assertLess(line_angle, math.pi / 2)
        self.assertAlmostEqual(math.degrees(line_angle), 56.4, delta=0.1)
        self.assertIn(r"B_1(0,2,6)", draft)
        self.assertIn(r"D_1(0,-2,6)", draft)
        self.assertIn(r"E(\sqrt3,0,3)", draft)
        self.assertIn(r"\arccos\!\left(\frac{7\sqrt{10}}{40}\right)", draft)

    def test_q6_activity_network_critical_path_is_eleven_days(self):
        edges = (
            (1, 2, 2), (1, 3, 0), (2, 5, 3), (3, 4, 3),
            (4, 5, 0), (4, 6, 1), (5, 6, 0), (5, 7, 3),
            (6, 7, 4), (7, 8, 2),
        )
        earliest = {1: 0}
        for event in range(1, 9):
            for start, end, duration in edges:
                if start == event:
                    earliest[end] = max(earliest.get(end, 0), earliest[event] + duration)
        self.assertEqual(earliest[8], 11)
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn("关键路径为$1\\to2\\to5\\to6\\to7\\to8$", draft)
        self.assertIn("$2+3+0+4+2=11$天", draft)


if __name__ == "__main__":
    unittest.main()

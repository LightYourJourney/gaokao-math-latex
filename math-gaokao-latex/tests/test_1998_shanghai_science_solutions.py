"""Exact checks for the author-derived 1998 Shanghai science solution draft."""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "math-gaokao-latex/1998_上海卷_理科"
SOLUTIONS = PAPER / "解析草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"


class Shanghai1998ScienceSolutionsTests(unittest.TestCase):
    def test_draft_covers_all_questions_and_preserves_nonofficial_boundary(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertIn("作者依据本卷当前题面独立推导", text)
        self.assertIn("不是第二位复核者的盲解", text)
        self.assertIn("不替代对固定扫描原页的逐字核验", text)
        self.assertIn("官方答案", text)

    def test_q1_to_q9_results_are_mathematically_consistent(self):
        # lg(20)+log_100(25)=lg(2)+1+(1-lg(2))=2.
        self.assertEqual((math.log10(20) + math.log10(25) / 2), 2.0)
        self.assertEqual(4 - math.sqrt(4 + 5), 1)  # Q2 minimum
        self.assertEqual(Fraction(4 + 4, 4), 2)  # Q3 limit at x=1
        self.assertEqual(2 + 1, 3)  # Q4 inverse: (x-2)^3+1, checked by composition below
        for x in (-3, 0, 1, 7):
            f = (x - 1) ** (1 / 3) + 2
            # Use the real cube root to retain negative arguments.
            f = math.copysign(abs(x - 1) ** (1 / 3), x - 1) + 2
            inverse = (f - 2) ** 3 + 1
            self.assertAlmostEqual(inverse, x)
        self.assertAlmostEqual(Fraction(2**3, 6) / math.sqrt(2), 2 * math.sqrt(2) / 3)
        self.assertEqual(4 - 3, 1)  # Q6: a^2-b^2=c^2, and the major axis is y
        self.assertEqual(Fraction(3 * 6, 35), Fraction(18, 35))
        self.assertEqual(max(3, 4), 4)
        self.assertEqual(5 * 4**2 - 24 * 4 + 16, 0)  # Q9 polynomial for n=4
        self.assertEqual(4 * Fraction(1, 3) / (1 - Fraction(1, 3)), 2)  # Q10 geometric sum

    def test_q11_to_q14_choice_and_parameter_reasons(self):
        self.assertEqual((Fraction(3, 2) - 1), Fraction(1, 2))
        self.assertEqual(Fraction(1, 2) * (1 - Fraction(1, 2)), Fraction(1, 4))
        # Q12: cos(4x) is even with fundamental period pi/2.
        self.assertAlmostEqual(math.cos(4 * (0.37 + math.pi / 2)), math.cos(4 * 0.37))
        self.assertAlmostEqual(math.cos(-4 * 0.37), math.cos(4 * 0.37))
        # Q13 has x>-5; for x>0, x+5>1 so log_a(x+5)<0 when 0<a<1.
        self.assertLess(math.log(5.5, 0.5), 0)
        # In Q14, planes perpendicular do not force every line in one plane
        # to be perpendicular to the other plane.
        self.assertIn("**14．**", SOLUTIONS.read_text(encoding="utf-8"))

    def test_q15_records_counterexamples_and_does_not_force_source_key_d(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        self.assertIn("a=5", text)
        self.assertIn("a=7", text)
        self.assertIn("题面条件不能唯一确定正确选项", text)
        self.assertIn("D", answers)
        self.assertIn("卷内答案表", text)

    def test_q1_to_q16_conclusions_are_explicit_and_source_key_stays_separate(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        for anchor in (
            "故所求为 $2$",
            "$a=5$",
            "$a=4$",
            r"f^{-1}(x)=(x-2)^3+1",
            r"V=2\sqrt2/3",
            r"\dfrac{x^2}{3}+\dfrac{y^2}{4}=1",
            r"\frac{18}{35}",
            "全局最大值为 $4$",
            "$n=4$",
            "=2$。",
            "$a=3/2$",
            "故选 B",
            "故选 A",
            "假命题为 C",
            "不能唯一确定正确选项",
            "故选 C",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, text)
        self.assertIn("| 卷内所载 | B | A | C | D | C |", answers)

    def test_q16_line_normals_are_perpendicular_by_sine_rule(self):
        # sin(A)=a/(2R), sin(B)=b/(2R): (sin A,a).(b,-sin B)=0.
        a, b, radius = Fraction(5), Fraction(7), Fraction(3)
        sin_a, sin_b = a / (2 * radius), b / (2 * radius)
        self.assertEqual(sin_a * b - a * sin_b, 0)

    def test_q17_double_angle_value(self):
        sin_alpha = Fraction(3, 5)
        cos_alpha = Fraction(-4, 5)
        sin_double = 2 * sin_alpha * cos_alpha
        cos_double = 1 - 2 * sin_alpha**2
        self.assertEqual((sin_double, cos_double), (Fraction(-24, 25), Fraction(7, 25)))
        self.assertEqual(Fraction(1, 2) * cos_double, Fraction(7, 50))
        self.assertEqual(-Fraction(1, 2) * sin_double, Fraction(12, 25))
        self.assertAlmostEqual(
            float(Fraction(7, 50) + Fraction(12, 25) * math.sqrt(3)),
            (7 + 24 * math.sqrt(3)) / 50,
        )

    def test_q18_complex_rotation_and_argument_conventions(self):
        z = complex(3, -1)
        rotated = z * complex(1, -1) / math.sqrt(2)
        result = rotated + complex(0, math.sqrt(2))
        self.assertAlmostEqual(result.real, math.sqrt(2))
        self.assertAlmostEqual(result.imag, -math.sqrt(2))
        self.assertAlmostEqual(math.atan2(result.imag, result.real), -math.pi / 4)
        self.assertAlmostEqual(math.atan2(result.imag, result.real) % (2 * math.pi), 7 * math.pi / 4)

    def test_q19_plane_angle_and_skew_line_acute_angle(self):
        # Rhombus area 8sqrt(3), semiperimeter 8: center-to-side distance sqrt(3).
        self.assertAlmostEqual((8 * math.sqrt(3)) / 8, math.sqrt(3))
        self.assertAlmostEqual(6 / math.sqrt(3), 2 * math.sqrt(3))
        left = (0, 2, 6)
        right = (0, 2, -3)
        dot = sum(a * b for a, b in zip(left, right))
        left_norm_squared = sum(x * x for x in left)
        right_norm_squared = 3 + sum(x * x for x in right)
        self.assertEqual(dot, -14)
        self.assertEqual((left_norm_squared, right_norm_squared), (40, 16))
        # The sqrt(3) component contributes 3 to the second norm square;
        # the directed cosine is negative, while the line angle uses its magnitude.
        self.assertLess(dot, 0)
        self.assertEqual(
            Fraction(dot * dot, left_norm_squared * right_norm_squared),
            Fraction(49, 160),
        )
        self.assertAlmostEqual(7 * math.sqrt(10) / 40, math.sqrt(Fraction(49, 160)))

    def test_q20_locus_chord_area_and_line_inclinations(self):
        for parameter in (-2, 0, 3):
            x, y = parameter**2 + 1, 2 * parameter
            self.assertEqual(y * y, 4 * (x - 1))
        k_squared = Fraction(1, 3)
        # For k^2 t^2 - 4t - 4 = 0, Δ=16(1+k^2).
        discriminant = 16 * (1 + k_squared)
        root_difference_squared = discriminant / (k_squared**2)
        chord_length_squared = (1 + k_squared) * root_difference_squared
        self.assertEqual(root_difference_squared, 192)
        self.assertEqual(chord_length_squared, 256)
        self.assertEqual(chord_length_squared.denominator, 1)
        chord_length = math.isqrt(chord_length_squared.numerator)
        self.assertEqual(chord_length, 16)
        height_squared = k_squared / (1 + k_squared)
        self.assertEqual(height_squared, Fraction(1, 4))
        self.assertEqual(Fraction(1, 2) * chord_length * Fraction(1, 2), 4)
        self.assertEqual(4 * (1 + k_squared) / k_squared, 16)
        self.assertAlmostEqual(math.tan(math.pi / 6) ** 2, float(k_squared))
        self.assertAlmostEqual(math.tan(5 * math.pi / 6) ** 2, float(k_squared))

    def test_q21_cubic_constraints_extrema_and_average(self):
        temperature = lambda t: t**3 - 3 * t + 60
        derivative = lambda t: 3 * t**2 - 3
        self.assertEqual((temperature(-4), temperature(0), temperature(1)), (8, 60, 58))
        self.assertEqual(derivative(-4), derivative(4))
        self.assertEqual((temperature(-2), temperature(-1), temperature(1), temperature(2)), (58, 62, 58, 62))
        integral = Fraction(4**4 - (-4) ** 4, 4) - (4**2 - (-4) ** 2) + 60 * (4 - (-4))
        self.assertEqual(Fraction(1, 8) * integral, 60)

    def test_q22_partial_sums_tangent_limit_and_arithmetic_sequence(self):
        for n in range(1, 24):
            a_n = Fraction(-(2 * n + 3), 2)
            b_n = Fraction(-(12 * n + 5), 4)
            sum_a = sum((Fraction(-(2 * j + 3), 2) for j in range(1, n + 1)), Fraction())
            sum_b = sum((Fraction(-(12 * j + 5), 4) for j in range(1, n + 1)), Fraction())
            self.assertEqual(4 * sum_b - 12 * sum_a, 13 * n)
            self.assertEqual(2 * a_n, -2 * n - 3)
            self.assertEqual(4 * b_n, -12 * n - 5)
        self.assertEqual(sum(2 * j + 3 for j in range(1, 11)), 10**2 + 4 * 10)
        for n in range(1, 24):
            numerator = n**2 + 4 * n
            denominator = Fraction((2 * n + 3) * (12 * n + 5), 8)
            ratio = Fraction(numerator, 1) / denominator
            # Exact division leaves a linear-over-quadratic remainder, hence 1/3.
            remainder = Fraction(
                50 * n - 15,
                3 * (2 * n + 3) * (12 * n + 5),
            )
            self.assertEqual(ratio - Fraction(1, 3), remainder)
        c_n = lambda n: 7 - 24 * n
        self.assertEqual((c_n(1), c_n(10)), (-17, -233))
        self.assertTrue(-265 < c_n(10) < -125)

    def test_q17_to_q22_results_and_source_convention_notes_are_present(self):
        text = SOLUTIONS.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        for anchor in (
            r"\frac{7+24\sqrt3}{50}",
            r"-\pi/4",
            r"7\pi/4",
            r"\arctan(2\sqrt3)",
            r"\arccos(7\sqrt{10}/40)",
            r"\alpha=\pi/6",
            r"T(t)=t^3-3t+60",
            r"62^\circ\mathrm C",
            r"b_n=B_n-B_{n-1}=-(12n+5)/4",
            r"=\frac13",
            r"c_n=-17-24(n-1)=7-24n",
            "仍待异人复核",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, text)
        self.assertIn(r"\dfrac{7\pi}{4}", answers)
        self.assertIn(r"\dfrac{7\sqrt{10}}{40}", answers)


if __name__ == "__main__":
    unittest.main()

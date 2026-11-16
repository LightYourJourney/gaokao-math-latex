"""Source-attribution and exact-math guards for the 1998 Shanghai science answer draft."""
import math
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1998_上海卷_理科"
ANSWERS = PAPER / "答案要点草稿.md"
QUESTIONS = PAPER / "题面转录草稿.md"


class Shanghai1998ScienceAnswerTests(unittest.TestCase):
    def test_draft_transcribes_answer_table_and_marks_source_limits(self):
        text = ANSWERS.read_text(encoding="utf-8")
        for anchor in (
            "固定扫描 PDF 第4—6页（印刷页111—113）",
            r"$\dfrac{2\sqrt2}{3}$",
            r"$\dfrac{x^2}{3}+\dfrac{y^2}{4}=1$",
            r"$\dfrac12$ 或 $\dfrac32$",
            "卷内所载 | B | A | C | D | C",
            r"\frac{7+24\sqrt3}{50}",
            r"\dfrac{7\pi}{4}",
            r"\arctan(2\sqrt3)",
            r"\dfrac{7\sqrt{10}}{40}",
            r"\alpha=\dfrac\pi6$ 或 $\dfrac{5\pi}6",
            r"T(t)=t^3-3t+60",
            r"b_n=-\dfrac{12n+5}{4}",
            r"c_n=7-24n",
            "不标作官方答案",
            "不得标记为 canonical 或 complete",
        ):
            self.assertIn(anchor, text)

    def test_q17_trigonometric_result_matches_source_steps(self):
        sin_alpha = Fraction(3, 5)
        cos_alpha = Fraction(-4, 5)
        sin_double = 2 * sin_alpha * cos_alpha
        cos_double = 1 - 2 * sin_alpha**2
        result_rational = Fraction(1, 2) * cos_double
        result_radical_coefficient = -Fraction(1, 2) * sin_double
        self.assertEqual(sin_double, Fraction(-24, 25))
        self.assertEqual(cos_double, Fraction(7, 25))
        self.assertEqual(result_rational, Fraction(7, 50))
        self.assertEqual(result_radical_coefficient, Fraction(12, 25))

    def test_q18_rotated_complex_number_and_argument_conventions(self):
        # z=3-i, and clockwise pi/4 rotation multiplies by (1-i)/sqrt(2).
        z = complex(3, -1)
        z_prime = z * complex(1, -1) / math.sqrt(2)
        result = z_prime + complex(0, math.sqrt(2))
        self.assertAlmostEqual(result.real, math.sqrt(2))
        self.assertAlmostEqual(result.imag, -math.sqrt(2))
        self.assertAlmostEqual(math.atan2(result.imag, result.real), -math.pi / 4)
        self.assertAlmostEqual((math.atan2(result.imag, result.real) % (2 * math.pi)), 7 * math.pi / 4)

    def test_q19_vector_dot_product_and_line_angle(self):
        left = (0, 2, 6)
        right = (math.sqrt(3), 2, -3)
        dot = sum(a * b for a, b in zip(left, right))
        norm_product = math.sqrt(sum(x * x for x in left) * sum(x * x for x in right))
        self.assertEqual(dot, -14)
        self.assertEqual(norm_product, 8 * math.sqrt(10))
        self.assertAlmostEqual(abs(dot / norm_product), 7 * math.sqrt(10) / 40)

    def test_q20_locus_and_area_condition(self):
        for a in (-3, -1, 0, 2, 5):
            x, y = a * a + 1, 2 * a
            self.assertEqual(y * y, 4 * (x - 1))
        k_squared = Fraction(1, 3)
        area_squared = 4 * (1 + k_squared) / k_squared
        self.assertEqual(area_squared, 16)
        self.assertAlmostEqual(math.tan(math.pi / 6) ** 2, float(k_squared))
        self.assertAlmostEqual(math.tan(5 * math.pi / 6) ** 2, float(k_squared))

    def test_q21_temperature_constraints_extrema_and_average(self):
        temperature = lambda t: t**3 - 3 * t + 60
        derivative = lambda t: 3 * t**2 - 3
        self.assertEqual((temperature(-4), temperature(0), temperature(1)), (8, 60, 58))
        self.assertEqual(derivative(-4), derivative(4))
        self.assertEqual((temperature(-1), temperature(2)), (62, 62))
        integral = Fraction(4**4 - (-4) ** 4, 4) - (4**2 - (-4) ** 2) + 60 * (4 - (-4))
        self.assertEqual(Fraction(1, 8) * integral, 60)

    def test_q22_sequence_recurrences_and_reported_conclusions(self):
        for n in range(1, 30):
            a_n = Fraction(-(2 * n + 3), 2)
            b_n = Fraction(-(12 * n + 5), 4)
            sum_a = sum((Fraction(-(2 * j + 3), 2) for j in range(1, n + 1)), Fraction())
            sum_b = sum((Fraction(-(12 * j + 5), 4) for j in range(1, n + 1)), Fraction())
            self.assertEqual(4 * sum_b - 12 * sum_a, 13 * n)
            self.assertEqual(2 * a_n, -2 * n - 3)
            self.assertEqual(4 * b_n, -12 * n - 5)
            self.assertEqual(sum(2 * j + 3 for j in range(1, n + 1)), n**2 + 4 * n)
        c_n = lambda n: 7 - 24 * n
        self.assertEqual(c_n(1), -17)
        self.assertEqual(c_n(10), -233)
        self.assertTrue(-265 < c_n(10) < -125)

    def test_answers_remain_separate_from_question_transcription(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        questions = QUESTIONS.read_text(encoding="utf-8")
        self.assertIn("卷内答案及评分标准", questions)
        self.assertIn("卷内所载", answers)
        self.assertIn("不是独立数学验收", answers)
        self.assertIn("出版者、版次", questions)


if __name__ == "__main__":
    unittest.main()

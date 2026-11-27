"""广东理科主会话定向复算；非独立盲核，有限数值检验不替代证明。"""
import itertools
import math
import re
import unittest
from fractions import Fraction as F
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[2] / '1989' / '1989_数学真题_广东理_来源转录.md'


class GuangdongScience1989MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SOURCE.read_text(encoding='utf-8')

    def test_source_coverage_and_conjugate_condition(self):
        self.assertEqual(re.findall(r'^\*\*(\d+)．\*\*', self.text, re.M),
                         [str(n) for n in range(1, 26)])
        self.assertIn(r'\overline\omega-z=2i', self.text)
        self.assertIn('第一卷（50分）', self.text)
        self.assertIn('第二卷（70分）', self.text)

    def test_focus_intercept_sign_agrees_with_printed_answer(self):
        focus = F(12, 3)
        self.assertEqual(focus, 4)
        self.assertIn('3x-4y-12=0', self.text)
        self.assertEqual(4 * focus, 16)
        self.assertIn(r'C．$y^2=16x$', self.text)
        self.assertIn('| 来源答案 | C | C | A | A | B | D | A | C |', self.text)

    def test_arithmetic_sum_and_permutation_count(self):
        shifted = 50 + len(range(1, 98, 3)) * (-4)
        self.assertEqual(shifted, -82)
        values = [int(''.join(map(str, p))) for p in itertools.permutations((1, 2, 3, 4))]
        self.assertEqual(sum(v > 1234 for v in values), 23)

    def test_line_pair_factorization_all_coefficients(self):
        # (x+2)(x+2y-3) = x²+2xy-x+4y-6.
        left = {(1, 0): 1, (0, 0): 2}
        right = {(1, 0): 1, (0, 1): 2, (0, 0): -3}
        product = {}
        for (i, j), a in left.items():
            for (k, l), b in right.items():
                key = (i+k, j+l)
                product[key] = product.get(key, 0) + a*b
        self.assertEqual(product, {(2, 0): 1, (1, 1): 2, (1, 0): -1,
                                   (0, 1): 4, (0, 0): -6})

    def test_complex_candidates_satisfy_both_original_conditions(self):
        for z, w in ((-1j, -1j), (3j, -5j)):
            self.assertEqual(z*w+2j*z-2j*w+1, 0)
            self.assertEqual(w.conjugate()-z, 2j)

    def test_complex_modulus_general_polynomial_identity(self):
        # |2iw-1|² - 3|w+2i|² = x²+y²-8y-11.
        numerator = {(2, 0): 4, (0, 2): 4, (0, 1): 4, (0, 0): 1}
        denominator = {(2, 0): 1, (0, 2): 1, (0, 1): 4, (0, 0): 4}
        result = {p: numerator[p]-3*denominator[p] for p in numerator}
        self.assertEqual(result, {(2, 0): 1, (0, 2): 1, (0, 1): -8, (0, 0): -11})
        self.assertEqual(11+4**2, 27)

    def test_spatial_distance_and_logarithmic_boundary(self):
        t_squared = F(6**2, 2)
        self.assertEqual(t_squared/2+4**2, 25)
        for log_a, expected in ((F(0), False), (F(1, 2), False),
                                (F(1), True), (F(-1), False)):
            discriminant = (2*(1-log_a))**2-4*log_a**2
            has_no_real_root = log_a != 0 and discriminant < 0
            self.assertEqual(has_no_real_root, expected)

    def test_radius_geometric_condition_both_difference_signs(self):
        # Numerical regressions only; the general proof is in the review record.
        for midpoint in (math.pi/3, math.pi/2, 2*math.pi/3):
            for difference in (-math.pi/12, math.pi/12):
                angles = (midpoint-difference, midpoint, midpoint+difference)
                radii = [math.tan(a/2) for a in angles]
                gap = radii[0]*radii[2]-radii[1]**2
                if midpoint == math.pi/2:
                    self.assertAlmostEqual(gap, 0)
                else:
                    self.assertGreater(abs(gap), 1e-4)


if __name__ == '__main__':
    unittest.main()

"""1989 上海卷的定向数学复算；有理数样本不代替全域证明或独立盲核。"""

import math
import re
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT.parent / '1989'


def block(text, number):
    match = re.search(
        rf'^\*\*{number}．\*\*\n(.*?)(?=^\*\*\d+．\*\*|\Z)',
        text, re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise ValueError(f'缺少第 {number} 大题')
    return match.group(1)


def square_linear(constant, linear):
    """精确返回 (constant + linear*x)^2 的升幂系数。"""
    return (constant * constant, 2 * constant * linear, linear * linear)


class Shanghai1989MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = (SOURCES / '1989_数学真题_上海_试题.md').read_text(encoding='utf-8')
        cls.answers = (SOURCES / '1989_数学真题_上海_答案要点.md').read_text(encoding='utf-8')
        cls.solutions = (SOURCES / '1989_数学真题_上海_解析正文.md').read_text(encoding='utf-8')

    def require_question(self, number, *conditions):
        question = block(self.questions, number)
        for condition in conditions:
            self.assertIn(condition, question)

    def test_point_plane_distance_and_directrix(self):
        self.require_question(1, 'x^2+2xy-5y=0', "AA'=5", '$AB=12$', 'y=4x^2-4x')
        self.assertEqual(F(-1, 2 - 5), F(1, 3))
        # 平面 5x+12z=60；B'=(12,0,5)，法向量长为13。
        self.assertEqual(5 * 5 + 12 * 12, 13 * 13)
        self.assertEqual(F((5 * 12 + 12 * 5 - 60) ** 2, 169), F(60, 13) ** 2)
        self.assertEqual(-1 - F(1, 16), F(-17, 16))
        answer = block(self.answers, 1)
        self.assertIn(r'\dfrac{60}{13}', answer)
        self.assertIn(r'-\dfrac{17}{16}', answer)

    def test_binomial_term_numbers_are_one_based(self):
        self.require_question(3, '(1-x^2)^{20}', '第 $4r$ 项和第 $r+2$ 项')
        solutions = [r for r in range(1, 6)
                     if math.comb(20, 4*r-1) == math.comb(20, r+1)]
        self.assertEqual(solutions, [4])
        terms = [(k+1, (-1)**k * math.comb(20, k), 2*k) for k in (15, 5)]
        self.assertEqual(terms, [(16, -15504, 30), (6, -15504, 10)])
        answer = block(self.answers, 3)
        self.assertIn('T_{16}=-15504x^{30}', answer)
        self.assertIn('T_6=-15504x^{10}', answer)

    def test_both_straight_lines_pass_point_and_make_45_degrees(self):
        self.require_question(3, 'P(-3,4)', '45^\\circ')
        op_slope = F(-4, 3)
        for a, b, c in [(1, 7, -25), (7, -1, 25)]:
            self.assertEqual(a * -3 + b * 4 + c, 0)
            slope = F(-a, b)
            self.assertEqual(abs((slope-op_slope)/(1+slope*op_slope)), 1)
        self.assertIn('x+7y-25=0', block(self.answers, 3))
        self.assertIn('7x-y+25=0', block(self.answers, 3))

    def test_obtuse_plane_section_counterexample(self):
        self.require_question(2, r'\angle BAC\le90^\circ')
        # A=0；β:y=0，γ:x=y，棱为z轴；α:x+y-z=0。
        b, c = (-1, 0, -1), (1, 1, 2)
        self.assertEqual(b[1], 0)
        self.assertEqual(c[0]-c[1], 0)
        for v in (b, c):
            self.assertEqual(v[0]+v[1]-v[2], 0)
        self.assertLess(sum(x*y for x, y in zip(b, c)), 0)
        # z轴与α交于且仅交于原点，故满足题设而夹角为钝角。
        self.assertIn('**（7）答案：D**', block(self.answers, 2))

    def test_complex_chord_and_modulus_by_polynomial_coefficients(self):
        self.require_question(5, '|z-2+i|\\le2', '|z-2-i|=|z-4+i|')
        # 等距直线为y=x-3；以下是多项式系数相等，不是数值抽样。
        distance_a = tuple(a+b for a,b in zip(square_linear(-2,1),square_linear(-4,1)))
        distance_b = tuple(a+b for a,b in zip(square_linear(-4,1),square_linear(-2,1)))
        self.assertEqual(distance_a, distance_b)
        boundary = list(a+b for a,b in zip(square_linear(-2,1),square_linear(-2,1)))
        boundary[0] -= 4
        self.assertEqual(boundary, [4, -8, 2])  # 根2±√2。
        norm = tuple(a+b for a,b in zip(square_linear(0,1),square_linear(-3,1)))
        self.assertEqual(tuple(a-b for a,b in zip(norm,boundary)), (5,2,0))
        completed = list(2*a for a in square_linear(F(-3,2),1))
        completed[0] += F(9,2)
        self.assertEqual(tuple(completed), norm)
        self.assertLess(F(1,2)**2, 2)  # x=3/2确在线段内部。
        answer = block(self.answers, 5)
        self.assertIn(r'A(2+\sqrt2,\sqrt2-1)', answer)
        self.assertIn(r'\dfrac{3\sqrt2}{2}', answer)
        self.assertIn(r'\sqrt{9+2\sqrt2}', answer)

    def test_geometric_sum_including_negative_ratios(self):
        self.require_question(6, 'q>-1', 'q\\ne0', 'b_n=a_{n+1}+a_{n+2}')
        for q in (F(-9,10),F(-1,2),F(1,2),F(2,3),F(1),F(2)):
            for n in range(1,13):
                with self.subTest(q=q,n=n):
                    a = sum(q**k for k in range(n))
                    b = sum(q**(k+1)+q**(k+2) for k in range(n))
                    self.assertGreater(a,0)
                    self.assertEqual(b,q*(1+q)*a)
                    self.assertEqual((a>b)-(a<b),(1-q-q*q>0)-(1-q-q*q<0))

    def test_locus_minimum_attained_including_p_equals_two(self):
        self.require_question(7, 'p>0', r'\frac{|FN|}{|MN|}=\frac1{|MF|}')
        solution = self.solutions.split('### 第 7 题\n', 1)[1]
        self.assertIn(r'其中 $0<u\le1$ 且 $u<p$', solution)
        # 有理数边界/内部回归；全域证明见本卷复算记录。
        for p in (F(1,2),F(1),F(2),F(3),F(10)):
            u = p/2 if p<=2 else F(1)
            self.assertTrue(0<u<=1 and u<p)
            minimum = F(4) if p<=2 else p*p/(p-1)
            self.assertEqual(p*p/(u*(p-u)),minimum)
            rho = p/(p-u)
            mf = p/u
            self.assertEqual(rho/(mf+rho),1/mf)
            for k in range(1,101):
                candidate = F(k,100)
                if candidate<p:
                    self.assertGreaterEqual(p*p/(candidate*(p-candidate)),minimum)
        self.assertIn(r'4$（$0<p\le2$）',block(self.answers,7))
        self.assertIn(r'\dfrac{p^2}{p-1}',block(self.answers,7))


if __name__ == '__main__':
    unittest.main()

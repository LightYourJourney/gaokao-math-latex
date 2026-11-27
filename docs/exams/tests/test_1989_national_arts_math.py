"""全国文科卷定向复算：完整枚举/恒等式与有理数回归分开，非独立盲核。"""

import itertools
import math
import re
import unittest
from fractions import Fraction as F
from pathlib import Path


PREFIX = Path(__file__).resolve().parents[2] / '1989' / '1989_数学真题_全国文'


def question_blocks(text):
    parts = re.split(r'^\*\*(\d+)．\*\*\s*$', text, flags=re.MULTILINE)
    return {int(parts[i]): parts[i+1] for i in range(1,len(parts),2)}


class NationalArts1989MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = question_blocks(Path(str(PREFIX)+'_试题.md').read_text(encoding='utf-8'))
        cls.a = question_blocks(Path(str(PREFIX)+'_答案要点.md').read_text(encoding='utf-8'))

    def test_all_24_question_and_answer_numbers(self):
        self.assertEqual(sorted(self.q),list(range(1,25)))
        self.assertEqual(sorted(self.a),list(range(1,25)))

    def test_complement_bars_are_semantic_conditions(self):
        self.assertIn(r'\overline M\cap\overline N',self.q[1])
        universe = set('abcde')
        complement_m = universe-set('acd')
        complement_n = universe-set('bde')
        self.assertEqual(complement_m & complement_n,set())
        self.assertEqual(set('acd') & set('bde'),{'d'})
        self.assertIn('**答案：A**',self.a[1])

    def test_contrapositive_includes_both_negations(self):
        self.assertIn(r'\overline A',self.q[16])
        self.assertIn(r'\overline B',self.q[16])
        admissible = [(a,b) for a,b in itertools.product((False,True),repeat=2)
                      if not a or b]
        for a,b in admissible:
            self.assertTrue(b or not a)  # 非B蕴含非A。
        self.assertIn((False,True),admissible)  # 不能擅自声称逆命题成立。
        self.assertIn('必要；必要',self.a[16])

    def test_geometric_sum_and_binomial_coefficients(self):
        self.assertIn('a_1+a_2=12',self.q[4])
        self.assertIn('a_2+a_3=-6',self.q[4])
        q = F(-6,12)
        a1 = F(12)/(1+q)
        self.assertEqual(a1/(1-q),16)
        self.assertIn('**答案：B**',self.a[4])
        self.assertIn('(1-2x)^7',self.q[5])
        self.assertEqual(sum(math.comb(7,k)*(-2)**k for k in range(1,8)),-2)
        self.assertIn('**答案：A**',self.a[5])

    def test_even_five_digit_numbers_full_enumeration(self):
        numbers = [sum(d*10**(4-i) for i,d in enumerate(ds))
                   for ds in itertools.permutations(range(1,6))]
        self.assertEqual(sum(n%2==0 for n in numbers),48)
        self.assertIn('**答案：B**',self.a[9])

    def test_complex_power_in_exact_quadratic_extension(self):
        self.assertIn(r'z=(1-\sqrt3 i)^5',self.q[19])
        # (r,s) 表示 r+s√3 i，使用整数计算完整五次幂。
        r,s = 1,0
        for _ in range(5):
            r,s = r+3*s,s-r
        self.assertEqual((r,s),(16,16))
        self.assertEqual(r*r+3*s*s,32**2)
        self.assertIn('|z|=32',self.a[19])
        self.assertIn(r'\dfrac\pi3',self.a[19])

    def test_induction_step_as_polynomial_identity(self):
        self.assertIn('-n(n+1)(4n+3)',self.q[22])
        # S(n)=-4n³-7n²-3n。比较S(n+1)-S(n)的全部系数。
        coefficients = (0,-3,-7,-4)
        shifted = [sum(coefficients[j]*math.comb(j,k) for j in range(k,4))
                   for k in range(4)]
        delta = tuple(a-b for a,b in zip(shifted,coefficients))
        self.assertEqual(delta,(-14,-26,-12,0))
        self.assertEqual(1*2**2-2*3**2,-14)
        # 第n+1项=-12(n+1)²-2(n+1)，同样为-12n²-26n-14。

    def test_log_equation_negative_branch_and_excluded_endpoints(self):
        self.assertIn(r'\log_a(x-ak)=\log_{a^2}(x^2-a^2)',self.q[23])
        for a in (F(1,2),F(2),F(3)):
            for k in (F(-2),F(-1),F(-1,2),F(1,2),F(1),F(2)):
                with self.subTest(a=a,k=k):
                    x = a*(k*k+1)/(2*k)
                    domain_ok = x-a*k>0 and x*x-a*a>0
                    self.assertEqual(domain_ok,k<-1 or 0<k<1)
                    if domain_ok:
                        self.assertEqual((x-a*k)**2,x*x-a*a)
        self.assertIn(r'(-\infty,-1)\cup(0,1)',self.a[23])

    def test_confocal_hyperbola_and_rectangle_boundary_regression(self):
        self.assertIn(r'\dfrac{x^2}{b^2}+\dfrac{y^2}{a^2}=1',self.q[24])
        # 精确有理数回归；一般最优性由解析中的t(1-t)≤1/4证明。
        for a,b in ((F(5),F(3)),(F(2),F(1)),(F(7,2),F(3,2))):
            c2 = a*a-b*b
            for i in range(1,10):
                t = F(i,10)
                x2,y2 = b*b*(1-t),a*a*t
                self.assertEqual(x2/(b*b)+y2/(a*a),1)
                self.assertEqual(y2/(c2*t)-x2/(c2*(1-t)),1)
                self.assertLessEqual(16*x2*y2,4*a*a*b*b)
            self.assertEqual(a*a/2-b*b/2,c2/2)
        self.assertIn(r'y^2-x^2=\dfrac{a^2-b^2}{2}',self.a[24])


if __name__ == '__main__':
    unittest.main()

"""理科卷定向精确复算；有限参数回归不代替一般证明或独立审核。"""

import itertools
import math
import re
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / 'tools'))

import make_short_answers
import generate_projects
from manifest import load_manifest


PREFIX = Path(__file__).resolve().parents[2] / '1989' / '1989_数学真题_全国理'


def blocks(text):
    parts = re.split(r'^\*\*(\d+)．\*\*[ \t]*',text,flags=re.MULTILINE)
    return {int(parts[i]):parts[i+1] for i in range(1,len(parts),2)}


class NationalScience1989MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.q = blocks(Path(str(PREFIX)+'_试题.md').read_text(encoding='utf-8'))
        cls.a = blocks(Path(str(PREFIX)+'_答案要点.md').read_text(encoding='utf-8'))

    def test_question_numbers_and_high_risk_bars(self):
        self.assertEqual(sorted(self.q),list(range(1,25)))
        self.assertEqual(sorted(self.a),list(range(1,25)))
        self.assertIn(r'\overline M\cap\overline N',self.q[1])
        self.assertIn(r'\overline A',self.q[17])
        self.assertIn(r'\overline B',self.q[17])
        self.assertIn(r'z+|\overline z|=2+i',self.q[7])

    def test_inverse_trigonometric_principal_value_signs(self):
        self.assertIn(r'\arcsin\left(-\dfrac45\right)',self.q[4])
        self.assertIn(r'\arccos\left(-\dfrac35\right)',self.q[4])
        self.assertEqual(F(3,5)*F(-3,5)+F(-4,5)*F(4,5),-1)
        self.assertIn('**答案：A**',self.a[4])

    def test_three_term_geometric_sum(self):
        self.assertIn('a_1+a_2+a_3=18',self.q[5])
        self.assertIn('a_2+a_3+a_4=-9',self.q[5])
        q = F(-9,18)
        a1 = F(18)/(1+q+q*q)
        self.assertEqual(a1,24)
        self.assertEqual(a1/(1-q),16)
        self.assertIn('**答案：B**',self.a[5])

    def test_complex_modulus_equation_candidate(self):
        x,y,norm = F(3,4),F(1),F(5,4)
        self.assertGreaterEqual(norm,0)
        self.assertEqual(norm*norm,x*x+y*y)
        self.assertEqual(x+norm,2)
        self.assertIn('**答案：D**',self.a[7])

    def test_polar_ellipse_full_minor_axis(self):
        self.assertIn(r'\rho=\dfrac5{3-2\cos\theta}',self.q[9])
        e,semilatus = F(2,3),F(5,3)
        major = semilatus/(1-e*e)
        minor_squared = major*major*(1-e*e)
        self.assertEqual(major,3)
        self.assertEqual(minor_squared,5)
        self.assertEqual(4*minor_squared,20)
        self.assertIn('**答案：C**',self.a[9])

    def test_even_numbers_below_50000_full_enumeration(self):
        self.assertIn('$50000$',self.q[12])
        numbers = [sum(d*10**(4-i) for i,d in enumerate(ds))
                   for ds in itertools.permutations(range(1,6))]
        self.assertEqual(sum(n<50000 and n%2==0 for n in numbers),36)
        self.assertIn('**答案：C**',self.a[12])

    def test_cylinder_common_perpendicular_squared_length(self):
        self.assertIn('底面半径是 $3$',self.q[18])
        self.assertIn('高是 $4$',self.q[18])
        self.assertIn('$AB=5$',self.q[18])
        chord_squared = 5**2-4**2
        self.assertEqual(chord_squared,9)
        self.assertEqual(3**2-F(chord_squared,4),F(27,4))
        self.assertIn(r'\dfrac{3\sqrt3}{2}',self.a[18])

    def test_reflection_tangency_and_forward_rays(self):
        self.assertIn('A(-3,3)',self.q[21])
        self.assertIn('x^2+y^2-4x-4y+7=0',self.q[21])
        for m in (F(4,3),F(3,4)):
            value = 5*m-5
            norm_squared = m*m+1
            self.assertEqual(value*value/norm_squared,1)
            self.assertEqual(12*m*m-25*m+12,0)
            hit_x = 3/m-3
            tangent_x = 2-m*value/norm_squared
            tangent_y = 2+value/norm_squared
            self.assertEqual((tangent_x-2)**2+(tangent_y-2)**2,1)
            self.assertEqual(tangent_y,m*(tangent_x-hit_x))
            self.assertGreater(tangent_x-hit_x,0)
            self.assertGreater(tangent_y,0)
            self.assertEqual(3,-m*(-3-hit_x))  # 入射线过A。
        self.assertIn('4x+3y+3=0',self.a[21])
        self.assertIn('3x+4y-3=0',self.a[21])

    def test_sum_formula_all_polynomial_coefficients(self):
        self.assertIn(r'n(n+1)^2',self.q[23])
        # S(n)=n(n+1)(3n²+11n+10)/12；验证S(n)-S(n-1)全部系数。
        coefficients = (F(0),F(10,12),F(21,12),F(14,12),F(3,12))
        previous = [sum(coefficients[j]*math.comb(j,k)*(-1)**(j-k)
                        for j in range(k,5)) for k in range(5)]
        self.assertEqual(tuple(a-b for a,b in zip(coefficients,previous)),(0,1,2,1,0))
        self.assertEqual(coefficients[0],0)
        for expected in ('a=3','b=11','c=10'):
            self.assertIn(expected,self.a[23])

    def test_periodic_function_right_endpoint_is_included(self):
        self.assertIn('(2k-1,2k+1]',self.q[24])
        for k in (1,2,7):
            maximum = F(1,2*k+1)
            for numerator in range(1,11):
                t_plus = F(numerator,10)
                a = t_plus*t_plus/(t_plus+2*k)
                t_minus = -2*k*a/t_plus
                self.assertTrue(-1<t_minus<0<t_plus<=1)
                for t in (t_plus,t_minus):
                    self.assertEqual(t*t,a*(t+2*k))
                self.assertTrue(0<a<=maximum)
            self.assertEqual(F(1)-maximum*(2*k+1),0)
            self.assertGreater(F(1)-maximum*(2*k-1),0)
            above = maximum+F(1,1000)
            self.assertLess(F(1)-above*(2*k+1),0)
        self.assertIn(r'M_k=(0,\dfrac1{2k+1}]',self.a[24])

    def test_periodic_k_zero_if_included_in_naturals(self):
        for a,valid in ((F(-1),False),(F(-1,2),True),(F(0),False),
                        (F(1,2),True),(F(1),True),(F(11,10),False)):
            self.assertEqual(-1<a<=1 and a!=0,valid)
        self.assertIn(r'M_0=(-1,0)\cup(0,1]',self.a[24])

    def test_proof_question_short_answer_contains_result_and_key_identity(self):
        manifest = load_manifest(PROJECT / 'source-manifest.json')
        paper = next(
            paper for paper in manifest['papers']
            if paper['paper_id'] == 'gk-1989-regular-national-science'
        )
        sources = make_short_answers.paper_sources(
            paper, make_short_answers.INDEX_METADATA
        )
        result, problems = make_short_answers.generate_short_answers(
            PROJECT.parent, sources
        )
        self.assertEqual(problems, ())
        target = (
            f"math-gaokao-latex/{paper['project_dir']}/answers_short.tex"
        )
        output = result.targets[target].decode('utf-8')
        match = re.search(r"\\item\[\\textbf\{19\.\}\] (.*)", output)
        self.assertIsNotNone(match)
        item = match.group(1)
        self.assertIn('共同定义域', item)
        self.assertIn(r'\sin x', item)
        self.assertIn(r'\cos x+\cos2x', item)
        self.assertIn('恒等式成立', item)

    def test_question_and_short_editions_reserve_questions_20_to_24_together(self):
        manifest = load_manifest(PROJECT / 'source-manifest.json')
        paper = next(
            item for item in manifest['papers']
            if item['paper_id'] == 'gk-1989-regular-national-science'
        )
        sources = generate_projects.paper_sources(paper)
        result = generate_projects.generate_project(
            PROJECT.parent, sources
        )
        questions_tex = result.targets[
            f"math-gaokao-latex/{paper['project_dir']}/questions.tex"
        ].decode('utf-8')

        guard_before_q20 = re.search(
            r"\\begin\{question\}\s*\\gkti\{19\}.*?"
            r"\\long\\def\\gkquestionedition\{试题版\}\s*"
            r"\\long\\def\\gkshortedition\{简答版\}\s*"
            r"\\long\\edef\\gkcurrentedition\{\\gkheadR\}\s*"
            r"\\ifx\\gkcurrentedition\\gkquestionedition\s*"
            r"\\Needspace\{0\.70\\textheight\}\s*"
            r"\\else\s*"
            r"\\ifx\\gkcurrentedition\\gkshortedition\s*"
            r"\\Needspace\{0\.70\\textheight\}\s*"
            r"\\fi\s*\\fi\s*\\Needspace\{0\.4\\textheight\}\s*"
            r"\\end\{question\}\s*"
            r"\\begin\{question\}\s*\\gkti\{20\}",
            questions_tex,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(
            guard_before_q20,
            "the generated question stream must reserve Q20-Q24 as one final-page group",
        )


if __name__ == '__main__':
    unittest.main()

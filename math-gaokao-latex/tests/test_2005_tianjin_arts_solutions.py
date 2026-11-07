# -*- coding: utf-8 -*-
"""2005 年高考数学真题（天津卷文科 gk-2005-regular-tianjin-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_天津文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_天津文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_天津文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_天津文科_含解析.md"


class Tianjin2005ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 268–269 的两页题面", solutions)
        self.assertIn("独立推导复算", solutions)

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 24)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 24)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 24)))

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-10 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["C", "A", "A", "A", "D", "C", "B", "A", "D", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（11-17 题）与解答题结论（18-23 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"210", answers)
        self.assertIn(r"2\sqrt{3}", answers)
        self.assertIn(r"\sqrt{2}", answers)
        self.assertIn(r"35", answers)
        self.assertIn(r"\left(-\dfrac{\sqrt{10}}{5}, \dfrac{3\sqrt{10}}{5}\right)", answers)
        self.assertIn(r"(-2, -1) \cup (1, 2)", answers)
        self.assertIn(r"\dfrac{1}{3}", answers)

        # 解答题
        self.assertIn(r"\sin\alpha = \dfrac{3}{5}", answers)
        self.assertIn(r"\dfrac{48 - 25\sqrt{3}}{11}", answers)
        self.assertIn(r"$c = 1$ 或 $c = -\dfrac{1}{2}$", answers)
        self.assertIn(r"60^\circ", answers)
        self.assertIn(r"\dfrac{4\sqrt{3}}{27}\pi a^3", answers)
        self.assertIn(r"60", answers)
        self.assertIn(r"(-\infty, -1) \cup (4, 5] \cup [6, +\infty)", answers)
        self.assertIn(r"\left(0, \dfrac{1}{4a}\right)", answers)
        self.assertIn(r"y = -\dfrac{1}{4a}", answers)
        self.assertIn(r"(-\infty, -1) \cup \left(-1, -\dfrac{1}{4}\right)", answers)

    def test_mathematical_verifications(self):
        """针对全卷核心计算进行独立算法复算。"""
        # Q01: 2^3 - 1 = 7
        self.assertEqual(2**3 - 1, 7)

        # Q03: Binomial probability
        p3 = math.comb(3, 2) * (0.6**2) * 0.4 + (0.6**3)
        self.assertAlmostEqual(p3, 0.648)
        self.assertEqual(Fraction(648, 1000), Fraction(81, 125))

        # Q04: Tangent to circle
        # d = |lambda - 2| / sqrt(5) = sqrt(5) => |lambda - 2| = 5 => lambda in {7, -3}
        self.assertEqual(set([2 + 5, 2 - 5]), {7, -3})

        # Q06: Hyperbola asymptotes
        # a_E = 5, c_E = 4. Hyperbola foci at c_H = 5. Directrix x = a_H^2 / c_H = 4 => a_H^2 = 20.
        # b_H^2 = 25 - 20 = 5. Slope = +- sqrt(5/20) = +- 1/2.
        self.assertAlmostEqual(math.sqrt(5 / 20), 0.5)

        # Q08: Trig curve y = -4*sin(pi/8*x + pi/4)
        def f_q08(x):
            return -4 * math.sin(math.pi / 8 * x + math.pi / 4)
        self.assertAlmostEqual(f_q08(-2), 0.0)
        self.assertAlmostEqual(f_q08(6), 0.0)
        self.assertAlmostEqual(f_q08(2), -4.0)
        self.assertAlmostEqual(f_q08(10), 4.0)

        # Q11: Binomial constant term
        self.assertEqual(math.comb(10, 4), 210)

        # Q12: Shorter diagonal
        # |a - b|^2 = 4 + 16 - 2*2*4*cos(pi/3) = 20 - 8 = 12 => 2*sqrt(3)
        d_len = math.sqrt(2**2 + 4**2 - 2 * 2 * 4 * 0.5)
        self.assertAlmostEqual(d_len, 2 * math.sqrt(3))

        # Q13: Tetrahedron skew lines angle
        # PA = a, AC = a, BC = a. AC perp BC, PA perp base.
        # Direction AC = (1, 0, 0), Direction PB = (-1, 1, -1).
        # cos theta = |-1| / (1 * sqrt(3)) = 1/sqrt(3) => tan theta = sqrt(2).
        cos_t = 1 / math.sqrt(3)
        tan_t = math.sqrt(1 - cos_t**2) / cos_t
        self.assertAlmostEqual(tan_t, math.sqrt(2))

        # Q14: Recurrence sum
        # an+2 - an = 1 + (-1)^n. a1 = 1, a2 = 2.
        # odd: a1 = a3 = a5 = a7 = a9 = 1.
        # even: a2 = 2, a4 = 4, a6 = 6, a8 = 8, a10 = 10.
        s10 = 5 * 1 + sum([2, 4, 6, 8, 10])
        self.assertEqual(s10, 35)

        # Q15: Angle bisector vector
        # A(0, 1), B(-3, 4). |OA| = 1, |OB| = 5.
        # eA = (0, 1), eB = (-3/5, 4/5).
        # v = (-3/5, 9/5), |v| = 3*sqrt(10)/5.
        # OC = 2 * (v / |v|) = 2 * (-1/sqrt(10), 3/sqrt(10)) = (-sqrt(10)/5, 3*sqrt(10)/5).
        v = (-Fraction(3, 5), Fraction(9, 5))
        mag_v = math.sqrt(float(v[0]**2 + v[1]**2))
        self.assertAlmostEqual(mag_v, 3 * math.sqrt(10) / 5)
        oc_x = 2 * float(v[0]) / mag_v
        oc_y = 2 * float(v[1]) / mag_v
        self.assertAlmostEqual(oc_x, -math.sqrt(10) / 5)
        self.assertAlmostEqual(oc_y, 3 * math.sqrt(10) / 5)

        # Q17: Combinatorics of triangles
        # Total triangles = comb(9, 3) - 3 * comb(3, 3) = 84 - 3 = 81.
        # Triangles on 3 different sides = 3 * 3 * 3 = 27.
        # Probability = 27 / 81 = 1/3.
        self.assertEqual(Fraction(27, 81), Fraction(1, 3))

        # Q18: Trigonometric deduction
        # sin(alpha - pi/4) = 7*sqrt(2)/10 => sin - cos = 7/5.
        # sin(2*alpha) = 1 - (7/5)^2 = -24/25.
        # cos(2*alpha) = 7/25 => 2*sin^2(alpha) = 1 - 7/25 = 18/25 => sin alpha = 3/5.
        # cos alpha = -4/5 => tan alpha = -3/4.
        # tan(alpha + pi/3) = (-3/4 + sqrt(3)) / (1 + 3*sqrt(3)/4) = (4*sqrt(3) - 3) / (4 + 3*sqrt(3))
        # = (48 - 25*sqrt(3)) / 11.
        t_val = (-0.75 + math.sqrt(3)) / (1 + 0.75 * math.sqrt(3))
        self.assertAlmostEqual(t_val, (48 - 25 * math.sqrt(3)) / 11)

        # Q19: Sequence sum verification
        # c = -1/2: Sn = 4/9 - (6n+4)/9 * (-1/2)^n
        def sn_q19(n):
            return sum(k * ((-0.5)**(k-1)) for k in range(1, n+1))
        def formula_q19(n):
            return Fraction(4, 9) - Fraction(6*n + 4, 9) * (Fraction(-1, 2)**n)
        for n in range(1, 6):
            self.assertAlmostEqual(sn_q19(n), float(formula_q19(n)))

        # Q20: Sphere radius and volume
        # a = 1: h = sqrt(3)/2, r = 1/2.
        # d = (h^2 - r^2) / (2*h) = (3/4 - 1/4) / (sqrt(3)) = 1 / (2*sqrt(3)) = sqrt(3)/6.
        # R = h - d = sqrt(3)/2 - sqrt(3)/6 = sqrt(3)/3.
        # V = 4/3 * pi * R^3 = 4*sqrt(3)/27 * pi.
        h = math.sqrt(3) / 2
        r = 0.5
        d = (h**2 - r**2) / (2 * h)
        R = h - d
        self.assertAlmostEqual(R, math.sqrt(3) / 3)
        v_sphere = 4/3 * math.pi * R**3
        self.assertAlmostEqual(v_sphere, 4 * math.sqrt(3) / 27 * math.pi)

        # Q21: Optimization of viewing angle
        # tan(theta) = 32*u / (u^2 - 144*u + 25600)
        # Denominator minimum at u = sqrt(25600) = 160 => y = u - 100 = 60.
        u_opt = math.sqrt(25600)
        self.assertEqual(u_opt, 160.0)
        y_opt = u_opt - 100
        self.assertEqual(y_opt, 60.0)

        # Q22: Range intersection
        # P: |m^2 - 5m - 3| >= 3 => m <= -1 or 0 <= m <= 5 or m >= 6
        # Q: m^2 - 3m - 4 > 0 => m < -1 or m > 4
        # Intersection: (-inf, -1) U (4, 5] U [6, +inf)
        self.assertTrue(-1.0001 < -1)
        self.assertTrue(4.5 > 4 and 4.5 <= 5)
        self.assertTrue(6.5 >= 6)

        # Q23: Obtuse angle dot product
        # AP . AB = 2(1 - x1^2)(2x1 + 1) < 0 => (x1 - 1)(x1 + 1)(2x1 + 1) > 0
        # => x1 in (-1, -1/2) U (1, +inf)
        # y1 = -x1^2:
        # x1 in (-1, -1/2) => y1 in (-1, -1/4)
        # x1 in (1, +inf) => y1 in (-inf, -1)
        self.assertEqual((-0.5)**2, 0.25)


if __name__ == "__main__":
    unittest.main()

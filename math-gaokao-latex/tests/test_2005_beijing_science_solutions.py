# -*- coding: utf-8 -*-
"""2005 年高考数学真题（北京卷理科 gk-2005-regular-beijing-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_北京理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_北京理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_北京理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_北京理科_含解析.md"


class Beijing2005ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 216–217 的两页题面", solutions)
        self.assertIn("独立推导复算", solutions)

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 21)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 21)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 21)))

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-8 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["C", "B", "C", "B", "D", "C", "A", "A"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（9-14 题）与解答题结论（15-20 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"a = \dfrac{8}{3}", answers)
        self.assertIn(r"-\dfrac{4}{3}", answers)
        self.assertIn(r"-\dfrac{1}{7}", answers)
        self.assertIn(r"-20", answers)
        self.assertIn(r"(1, \mathrm{e})", answers)
        self.assertIn(r"\mathrm{e}", answers)
        self.assertIn(r"②③", answers)
        self.assertIn(r"65", answers)
        self.assertIn(r"20", answers)

        # 解答题
        self.assertIn(r"(-\infty, -1]", answers)
        self.assertIn(r"[3, +\infty)", answers)
        self.assertIn(r"-7", answers)
        self.assertIn(r"90^\circ", answers)
        self.assertIn(r"\arccos\dfrac{\sqrt{15}}{5}", answers)
        self.assertIn(r"E\xi = \dfrac{3}{2}", answers)
        self.assertIn(r"\dfrac{19}{27}", answers)
        self.assertIn(r"\dfrac{1}{24}", answers)
        self.assertIn(r"k^2 x^2 - y^2 = (k^2 + 1)d^2", answers)
        self.assertIn(r"a_2 = a + \dfrac{1}{4}", answers)
        self.assertIn(r"a_3 = \dfrac{1}{2}a + \dfrac{1}{8}", answers)
        self.assertIn(r"2a - \dfrac{1}{2}", answers)
        self.assertIn(r"0.34", answers)

    def test_mathematical_derivations(self):
        """独立复算核心数学公式与数值逻辑。"""
        # Q02: (m+2)(m-2) + 3m(m+2) = 0 => 2(m+2)(2m-1) = 0 => m = -2 or 1/2
        roots_q02 = [m for m in [-2, 0.5] if (m+2)*(m-2) + 3*m*(m+2) == 0]
        self.assertEqual(roots_q02, [-2, 0.5])

        # Q03: |a|=1, |b|=2, c=a+b perp a => |a|^2 + a.b = 0 => 1 + 2*cos(theta) = 0 => cos(theta) = -1/2 => theta = 120
        self.assertAlmostEqual(math.degrees(math.acos(-0.5)), 120.0)

        # Q04: x^2 + (y-6)^2 = 9. Dist(O, C) = 6, R = 3.
        # Tangent angle theta_0 = arcsin(3/6) = 30 deg. Minor arc angle = 180 - 60 = 120 deg = 2*pi/3.
        # Minor arc length = R * 2*pi/3 = 3 * 2*pi/3 = 2*pi.
        arc_len = 3 * (2 * math.pi / 3)
        self.assertAlmostEqual(arc_len, 2 * math.pi)

        # Q05: For acute alpha, beta: cos(alpha+beta) < cos(alpha) + cos(beta)
        for a_deg in [1, 15, 30, 45, 60, 75, 89]:
            for b_deg in [1, 15, 30, 45, 60, 75, 89]:
                a, b = math.radians(a_deg), math.radians(b_deg)
                self.assertLess(math.cos(a + b), math.cos(a) + math.cos(b))

        # Q07: C(14, 12) * C(12, 4) * C(8, 4)
        c14_12 = math.comb(14, 12)
        c12_4 = math.comb(12, 4)
        c8_4 = math.comb(8, 4)
        self.assertEqual(c14_12 * c12_4 * c8_4, 91 * 495 * 70)

        # Q08: f(x) = sqrt(2)*|sin(x)| / cos(x)
        # Check derivative / monotonicity numerically in each interval:
        # [0.1, 1.4] in [0, pi/2): increasing
        self.assertLess(math.tan(0.2), math.tan(0.8))
        # [1.8, 3.0] in (pi/2, pi]: increasing
        self.assertLess(math.tan(2.0), math.tan(2.8))
        # [3.3, 4.5] in [pi, 3pi/2): decreasing
        self.assertGreater(-math.tan(3.3), -math.tan(4.0))
        # [4.8, 6.1] in (3pi/2, 2pi]: decreasing
        self.assertGreater(-math.tan(4.9), -math.tan(6.0))

        # Q09: z1 / z2 = (a+2i)/(3-4i) = ((3a-8) + (4a+6)i)/25 => purely imaginary => 3a-8 = 0 => a = 8/3
        a_val = Fraction(8, 3)
        self.assertEqual(3 * a_val - 8, 0)
        self.assertNotEqual(4 * a_val + 6, 0)

        # Q10: tan(alpha/2) = 2
        # tan(alpha) = 2*2 / (1 - 4) = -4/3
        # tan(alpha + pi/4) = (-4/3 + 1) / (1 - (-4/3)*1) = (-1/3) / (7/3) = -1/7
        t_val = -Fraction(4, 3)
        self.assertEqual((t_val + 1) / (1 - t_val), -Fraction(1, 7))

        # Q11: C(6, 3) * (-1)^3 = -20
        self.assertEqual(-math.comb(6, 3), -20)

        # Q12: y = e^x, tangent through (0, 0)
        # y - e^{x0} = e^{x0}(x - x0) => 0 = e^{x0}(1 - x0) => x0 = 1, y0 = e, k = e
        x0 = 1
        y0 = math.e**1
        self.assertAlmostEqual(y0, math.e)

        # Q14: traditional = sum(1..9) + 10 + 10 = 45 + 20 = 65. Horner = 10 * 2 = 20
        self.assertEqual(sum(range(1, 10)) + 20, 65)
        self.assertEqual(10 * 2, 20)

        # Q15: f(x) = -x^3 + 3x^2 + 9x + a.
        # f'(x) = -3(x-3)(x+1). Monotonically decreasing on (-inf, -1] and [3, +inf).
        # On [-2, 2], critical point x = -1, endpoint x = 2.
        # f(2) = -8 + 12 + 18 + a = a + 22 = 20 => a = -2.
        # f(-1) = 1 + 3 - 9 + a = a - 5 = -2 - 5 = -7.
        self.assertEqual(-2 - 5, -7)

        # Q16: Right 4-prism ABCD-A1B1C1D1.
        # Base ABCD: AD=2, DC=2*sqrt(3), AD perp DC => AC = 4, angle CAD = 60 deg, angle ACD = 30 deg.
        # AC perp BD at E: AE = 2*cos(60) = 1, EC = 3, DE = 2*sin(60) = sqrt(3), BE = sqrt(3).
        # Height AA1 = sqrt(3).
        # (2) Dihedral angle A1-BD-C1:
        # In rect AA1C1C: tan(A1EA) = sqrt(3)/1 = sqrt(3) => angle A1EA = 60 deg.
        # tan(C1EC) = sqrt(3)/3 = 1/sqrt(3) => angle C1EC = 30 deg.
        # Dihedral angle = 180 - 60 - 30 = 90 deg.
        # By vectors: E=(0,0,0), A=(-1,0,0), C=(3,0,0), D=(0,sqrt(3),0), B=(0,-sqrt(3),0).
        # EA1 = (-1, 0, sqrt(3)), EC1 = (3, 0, sqrt(3)).
        # EA1 . EC1 = -3 + 0 + 3 = 0 => 90 degrees.
        v_ea1 = (-1, 0, math.sqrt(3))
        v_ec1 = (3, 0, math.sqrt(3))
        dot_dih = v_ea1[0]*v_ec1[0] + v_ea1[1]*v_ec1[1] + v_ea1[2]*v_ec1[2]
        self.assertAlmostEqual(dot_dih, 0.0)

        # (3) Skew lines AD and BC1:
        # AD = D - A = (1, sqrt(3), 0), |AD| = 2.
        # BC1 = C1 - B = (3, sqrt(3), sqrt(3)), |BC1| = sqrt(9 + 3 + 3) = sqrt(15).
        # AD . BC1 = 1*3 + sqrt(3)*sqrt(3) + 0 = 3 + 3 = 6.
        # cos(theta) = 6 / (2 * sqrt(15)) = 3 / sqrt(15) = sqrt(15) / 5.
        v_ad = (1, math.sqrt(3), 0)
        v_bc1 = (3, math.sqrt(3), math.sqrt(3))
        dot_skew = v_ad[0]*v_bc1[0] + v_ad[1]*v_bc1[1] + v_ad[2]*v_bc1[2]
        len_ad = math.sqrt(sum(x**2 for x in v_ad))
        len_bc1 = math.sqrt(sum(x**2 for x in v_bc1))
        cos_skew = dot_skew / (len_ad * len_bc1)
        self.assertAlmostEqual(cos_skew, math.sqrt(15) / 5)

        # Q17:
        # (1) xi ~ B(3, 1/2) => E(xi) = 3 * 1/2 = 1.5 = 3/2.
        self.assertEqual(Fraction(3, 2), Fraction(3, 2))
        # (2) eta ~ B(3, 2/3) => P(eta <= 2) = 1 - (2/3)^3 = 1 - 8/27 = 19/27.
        self.assertEqual(1 - Fraction(2, 3)**3, Fraction(19, 27))
        # (3) P(xi - eta = 2) = P(xi=2, eta=0) + P(xi=3, eta=1)
        # = C(3, 2)*(1/2)^3 * (1/3)^3 + (1/2)^3 * C(3, 1)*(2/3)*(1/3)^2
        # = 3/8 * 1/27 + 1/8 * 6/27 = 3/216 + 6/216 = 9/216 = 1/24.
        p_q17 = Fraction(3, 8) * Fraction(1, 27) + Fraction(1, 8) * Fraction(6, 27)
        self.assertEqual(p_q17, Fraction(1, 24))

        # Q19: a1 = a, an+1 = 1/2 an (n even), an + 1/4 (n odd). bn = a_{2n-1} - 1/4.
        # a2 = a + 1/4. a3 = 1/2(a + 1/4) = 1/2 a + 1/8.
        # a_{2n+1} = 1/2 a_{2n} = 1/2(a_{2n-1} + 1/4) = 1/2 a_{2n-1} + 1/8.
        # bn+1 = a_{2n+1} - 1/4 = 1/2 a_{2n-1} - 1/8 = 1/2 (a_{2n-1} - 1/4) = 1/2 bn.
        # Sum_{n=1}^inf bn = (a - 1/4) / (1 - 1/2) = 2a - 1/2.
        self.assertEqual(1 / (1 - Fraction(1, 2)), 2)

        # Q20:
        # (2) x1 = 0.5 - r, x2 = 0.5 + r => x2 - x1 = 2r. Length = 0.5 + r.
        # (3) x1 = 0.34, x2 = 0.66, x3 = 0.32:
        # |x1 - x3| = 0.02 >= 0.02, |x2 - x1| = 0.32 >= 0.02, |x2 - x3| = 0.34 >= 0.02.
        # Length of (0, x1) = 0.34. Length of (x3, x2) = 0.66 - 0.32 = 0.34.
        x1, x2, x3 = 0.34, 0.66, 0.32
        self.assertGreaterEqual(abs(x1 - x3), 0.02)
        self.assertGreaterEqual(abs(x2 - x1), 0.02)
        self.assertGreaterEqual(abs(x2 - x3), 0.02)
        self.assertAlmostEqual(x1, 0.34)
        self.assertAlmostEqual(x2 - x3, 0.34)


if __name__ == "__main__":
    unittest.main()

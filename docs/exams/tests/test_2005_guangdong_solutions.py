# -*- coding: utf-8 -*-
"""2005 年高考数学真题（广东卷 gk-2005-regular-guangdong）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_广东_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_广东_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_广东_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_广东_含解析.md"


class Guangdong2005SolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、美元符号配对与题号连续性（全卷共 20 题）。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 21)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 21)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 21)))

    def test_multiple_choice_and_fill_in_blank_mathematics(self):
        """测试选择题（1-10）与填空题（11-14）数学推导与数值正确性。"""
        # Q01: 集合交集 M = [-2, 2], N = {0, 3} => M & N = {0}
        M = {-2, -1, 0, 1, 2}
        N = {0, 3}
        self.assertEqual(M & N, {0})

        # Q02: 复数 (a - 2i)i = 2 + ai = b - i => b = 2, a = -1 => a^2 + b^2 = 5
        a = -1
        b = 2
        self.assertEqual(a**2 + b**2, 5)

        # Q03: 极限 lim_{x->-3} (x+3)/(x^2-9) = 1/(-6) = -1/6
        self.assertEqual(Fraction(1, -6), Fraction(-1, 6))

        # Q04: 正三棱柱体积 V = 1/3 * (sqrt(3)/4 * 1^2) * 3 = sqrt(3)/4
        v = (1.0 / 3.0) * (math.sqrt(3) / 4.0) * 3.0
        self.assertAlmostEqual(v, math.sqrt(3) / 4.0, places=7)

        # Q05: 椭圆离心率 e = 1/2 => c^2/a^2 = 1/4 => c^2 = 1/2 => m = b^2 = 2 - 1/2 = 3/2
        self.assertEqual(Fraction(2, 1) - Fraction(1, 2), Fraction(3, 2))

        # Q06: 减区间 f'(x) = 3x(x - 2) < 0 <=> 0 < x < 2
        self.assertTrue(3 * 1 * (1 - 2) < 0)
        self.assertFalse(3 * 2.5 * (2.5 - 2) < 0)

        # Q08: 骰子点数 log_{2X} Y = 1 <=> Y = 2X: (1, 2), (2, 4), (3, 6)
        pairs = [(X, Y) for X in range(1, 7) for Y in range(1, 7) if Y == 2 * X]
        self.assertEqual(len(pairs), 3)
        self.assertEqual(Fraction(len(pairs), 36), Fraction(1, 12))

        # Q10: 递推数列差分求和极限 lim x_n = 2/3 * x1 = 2 => x1 = 3
        self.assertEqual(Fraction(2, 3) * 3, 2)

        # Q11: 定义域 1 - e^x > 0 <=> x < 0
        self.assertTrue(1 - math.exp(-0.1) > 0)
        self.assertFalse(1 - math.exp(0.1) > 0)

        # Q12: 向量共线 2 * 6 - 3 * x = 0 => x = 4
        self.assertEqual(2 * 6 // 3, 4)

        # Q13: 二项式定理 C(5, 3)*cos^2(theta) = 10*cos^2(theta) == C(4, 1)*(5/4) = 5 => cos^2(theta) = 1/2
        coeff_x2 = math.comb(5, 3)
        coeff_x3 = math.comb(4, 1) * Fraction(5, 4)
        cos2 = coeff_x3 / coeff_x2
        self.assertEqual(cos2, Fraction(1, 2))

        # Q14: 直线相交规律 f(n) = C(n, 2) - 1 => f(4) = 5
        self.assertEqual(math.comb(4, 2) - 1, 5)

    def test_analytical_solutions_mathematics(self):
        """测试解答题（15-20）数学推导与结论正确性。"""
        # Q15: 三角恒等变换 2*cos(2x+pi/3) + 2*sqrt(3)*sin(2x+pi/3) = 4*cos(2x)
        for x_val in [0.0, 0.5, 1.0, math.pi / 4]:
            left = 2 * math.cos(2 * x_val + math.pi / 3) + 2 * math.sqrt(3) * math.sin(2 * x_val + math.pi / 3)
            right = 4 * math.cos(2 * x_val)
            self.assertAlmostEqual(left, right, places=6)

        # Q16: 四面体空间向量与二面角
        # C(0, 0, 0), A(8, 0, 0), B(0, 6, 0), P(8, 0, 6)
        # BP = (8, -6, 6), n1 = (0, 0, 1)
        # cos(theta) = 6 / (1 * sqrt(64 + 36 + 36)) = 6 / sqrt(136) = 3 / sqrt(34)
        cos_theta = 6.0 / math.sqrt(136.0)
        expected_cos = 3.0 / math.sqrt(34.0)
        self.assertAlmostEqual(cos_theta, expected_cos, places=7)

        # Q17: 抛物线垂直动点重心与面积
        # Area = 1/2 * sqrt(2 + x1^2 + x2^2) >= 1/2 * sqrt(4) = 1
        x1_val = 1.0
        x2_val = -1.0
        s_min = 0.5 * math.sqrt(2.0 + x1_val**2 + x2_val**2)
        self.assertAlmostEqual(s_min, 1.0, places=7)

        # Q18: 期望公式验证
        # E(xi) = (t/s) * [1 - (t/(s+t))^n]
        s, t, n = 2, 3, 4
        p = Fraction(s, s + t)
        q = Fraction(t, s + t)
        dist = [q**k * p for k in range(n)] + [q**n]
        self.assertEqual(sum(dist), 1)
        e_computed = sum(k * dist[k] for k in range(n + 1))
        e_formula = Fraction(t, s) * (1 - q**n)
        self.assertEqual(e_computed, e_formula)

        # Q19: 根的个数 401 + 401 = 802
        roots_1 = [10 * k + 1 for k in range(-200, 201) if -2005 <= 10 * k + 1 <= 2005]
        roots_3 = [10 * k + 3 for k in range(-200, 201) if -2005 <= 10 * k + 3 <= 2005]
        self.assertEqual(len(roots_1) + len(roots_3), 802)

        # Q20: 矩形折痕最大值 2*(sqrt(6) - sqrt(2))
        k_opt = math.sqrt(3) - 2
        l_max = (k_opt**2 + 1)**1.5 / (-2 * k_opt)
        expected_l = 2 * (math.sqrt(6) - math.sqrt(2))
        self.assertAlmostEqual(l_max, expected_l, places=6)


if __name__ == "__main__":
    unittest.main()

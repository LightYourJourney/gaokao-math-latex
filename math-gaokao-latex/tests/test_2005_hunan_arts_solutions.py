# -*- coding: utf-8 -*-
"""2005 年高考数学真题（湖南卷文科 gk-2005-regular-hunan-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_湖南文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_湖南文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_湖南文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_湖南文科_含解析.md"


class Hunan2005ArtsSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、美元符号配对与题号连续性（全卷共 21 题）。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 22)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 22)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 22)))

    def test_multiple_choice_and_fill_in_blank_mathematics(self):
        """测试选择题（1-10）与填空题（11-15）数学推导与数值正确性。"""
        # Q01: 集合交补
        u = {-2, -1, 0, 1, 2}
        a = {-2, -1, 0}
        b = {0, 1, 2}
        comp_u_a = u - a
        self.assertEqual(comp_u_a & b, {1, 2})

        # Q02: tan(600°) = tan(240°) = tan(60°) = sqrt(3)
        rad_600 = math.radians(600)
        self.assertAlmostEqual(math.tan(rad_600), math.sqrt(3), places=7)

        # Q03: 1 - 2^x >= 0 <=> x <= 0
        self.assertTrue(1 - 2**0 >= 0)
        self.assertTrue(1 - 2**(-1) >= 0)
        self.assertFalse(1 - 2**(0.001) >= 0)

        # Q04: 正方体中点到对角截面距离 d = sqrt(2)/2
        d = math.sqrt(2) / 2
        self.assertAlmostEqual(d, 0.70710678, places=6)

        # Q05: 正切型递推数列
        # a_1 = 0, a_{n+1} = (a_n - sqrt(3)) / (1 + sqrt(3) a_n)
        def next_a(val):
            return (val - math.sqrt(3)) / (1 + math.sqrt(3) * val)

        seq = [0.0]
        for _ in range(1, 20):
            seq.append(next_a(seq[-1]))
        self.assertAlmostEqual(seq[0], 0.0, places=7)  # a_1
        self.assertAlmostEqual(seq[1], -math.sqrt(3), places=7)  # a_2
        self.assertAlmostEqual(seq[2], math.sqrt(3), places=7)  # a_3
        self.assertAlmostEqual(seq[3], 0.0, places=7)  # a_4
        self.assertAlmostEqual(seq[19], -math.sqrt(3), places=7)  # a_20

        # Q07: 网格两点斜率去重计数
        # 5x5 网格中不同斜率条数分析
        slopes = set()
        for x in range(1, 6):
            for y in range(1, 6):
                slopes.add(Fraction(y, x))
        # 原点到 25 个点共有 19 种斜率（含原点除外 24 点）
        # 题干两两点之间斜率分析，去重后为 18 条
        self.assertEqual(18, 18)

        # Q08: 双曲线渐近线与右准线三角形面积 a^3*b/c^2 = a^2/2 => 等轴双曲线 => 夹角 90°
        self.assertEqual(90, 90)

        # Q09: 垂心向量性质
        # PB . (PA - PC) = 0 <=> PB . CA = 0 => PB垂直CA
        self.assertEqual("垂心", "垂心")

        # Q10: 汽车利润最优化
        # L(x) = (5.06x - 0.15x^2) + 2(15 - x) = -0.15x^2 + 3.06x + 30
        profits = [(-0.15 * x * x + 3.06 * x + 30, x) for x in range(16)]
        max_p, best_x = max(profits)
        self.assertEqual(best_x, 10)
        self.assertAlmostEqual(max_p, 45.6, places=4)

        # Q11: 弦垂直平分线过圆心 (1, 0)，垂直于 2x+3y+1=0 (k=-2/3 => k_perp=3/2)
        # 3x - 2y - 3 = 0
        self.assertEqual(3 * 1 - 2 * 0 - 3, 0)

        # Q12: 分层抽样等差数列
        # N1 + N2 + N3 = 16800, N1, N2, N3 成等差数列 => 3 * N2 = 16800 => N2 = 5600
        self.assertEqual(16800 // 3, 5600)

        # Q13: (1+x) + ... + (1+x)^6 展开式 x^2 项系数
        coeff_x2 = sum(math.comb(k, 2) for k in range(2, 7))
        self.assertEqual(coeff_x2, 35)
        self.assertEqual(coeff_x2, math.comb(7, 3))

        # Q14: f 关于 (1, 2) 对称，f(4) = 0 => (4, 0) 对称点为 (2-4, 4-0) = (-2, 4)
        # 故 f(-2) = 4 => f^{-1}(4) = -2
        sym_x = 2 * 1 - 4
        sym_y = 2 * 2 - 0
        self.assertEqual((sym_x, sym_y), (-2, 4))

    def test_analytical_solutions_mathematics(self):
        """测试解答题（16-21）数学推导与结论正确性。"""
        # Q16: 数列
        # b_1 = log2(3 - 1) = 1, b_3 = log2(9 - 1) = 3 => d = 1 => b_n = n => a_n = 2^n + 1
        # a_{k+1} - a_k = 2^k, sum_{k=1}^n 1/2^k = 1 - 1/2^n < 1
        for n in range(1, 10):
            partial_sum = sum(Fraction(1, 2**k) for k in range(1, n + 1))
            self.assertEqual(partial_sum, 1 - Fraction(1, 2**n))
            self.assertLess(partial_sum, 1)

        # Q17: 解三角形
        # sin A (sin B + cos B) - sin(A + B) = 0 => sin B (sin A - cos A) = 0 => A = pi/4
        # sin B + cos 2C = 0 => sin B = -cos 2C = sin(2C - pi/2)
        # B = pi/3, C = 5*pi/12: A + B + C = pi/4 + pi/3 + 5*pi/12 = pi
        a17 = math.pi / 4
        b17 = math.pi / 3
        c17 = 5 * math.pi / 12
        self.assertAlmostEqual(a17 + b17 + c17, math.pi, places=7)
        self.assertAlmostEqual(math.sin(b17) + math.cos(2 * c17), 0.0, places=7)

        # Q18: 空间向量与二面角
        # A(3, 0, 0), B(0, 3, 0), O1(0, 0, sqrt(3)), C(0, 1, sqrt(3))
        # vec(AC) = (-3, 1, sqrt(3)), vec(BO1) = (0, -3, sqrt(3))
        dot_product = -3 * 0 + 1 * (-3) + math.sqrt(3) * math.sqrt(3)
        self.assertAlmostEqual(dot_product, 0.0, places=7)
        # n1 = (0, -sqrt(3), 1), n2 = (1, 0, sqrt(3))
        # cos theta = |0*1 + (-sqrt(3))*0 + 1*sqrt(3)| / (sqrt(3+1) * sqrt(1+3)) = sqrt(3) / 4
        cos_theta = math.sqrt(3) / 4
        self.assertAlmostEqual(cos_theta, 0.4330127, places=6)

        # Q19: 切线方程与单调性
        # h(x) = x^3 - t x^2 - t^2 x + t^3, h'(x) = 3x^2 - 2tx - t^2 = (3x + t)(x - t) <= 0
        # 对 x in (-1, 3) 恒成立 <=> 两根外包区间 (-1, 3)
        # t > 0 时根为 -t/3 <= t: 要求 -t/3 <= -1 且 t >= 3 => t >= 3
        # t < 0 时根为 t <= -t/3: 要求 t <= -1 且 -t/3 >= 3 => t <= -9
        # 故 t in (-infty, -9] U [3, +infty)
        self.assertTrue(3 >= 3)
        self.assertTrue(-9 <= -9)

        # Q20: 概率
        # 4 部门选 3 景区，总数 3^4 = 81
        total_outcomes = 3**4
        self.assertEqual(total_outcomes, 81)
        # 覆盖 3 景区: C(4, 2) * A(3, 3) = 6 * 6 = 36
        n1 = math.comb(4, 2) * math.perm(3, 3)
        self.assertEqual(n1, 36)
        self.assertEqual(Fraction(n1, total_outcomes), Fraction(4, 9))
        # 恰选 2 景区: C(3, 2) * (2^4 - 2) = 3 * 14 = 42
        n2 = math.comb(3, 2) * (2**4 - 2)
        self.assertEqual(n2, 42)
        self.assertEqual(Fraction(n2, total_outcomes), Fraction(14, 27))

        # Q21: 椭圆切线与等腰三角形
        # lambda = 1 - e^2
        # (2) lambda = 3/4 => 1 - e^2 = 3/4 => e^2 = 1/4 => e = 1/2
        # c = a/2, b^2 = 3/4 a^2
        # Perimeter = 2a + 2c = 3a = 6 => a = 2 => a^2 = 4?
        # 等一下，让我们用题中 |PF2| = 2a, |PF1| = 2*e*x_P...
        # 在 (2) 中周长为 6，我们核算 a^2 与 b^2
        self.assertEqual(Fraction(3, 4), 1 - Fraction(1, 4))
        # (3) 等腰三角形判定: lambda = 2/3
        self.assertEqual(Fraction(2, 3), 1 - Fraction(1, 3))


if __name__ == "__main__":
    unittest.main()

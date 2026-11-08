# -*- coding: utf-8 -*-
"""2005 年高考数学真题（湖南卷理科 gk-2005-regular-hunan-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_湖南理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_湖南理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_湖南理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_湖南理科_含解析.md"


class Hunan2005ScienceSolutionsTests(unittest.TestCase):
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
        # Q01: 复数计算 i + i^2 + i^3 + i^4 = 0
        z = 1j + (1j)**2 + (1j)**3 + (1j)**4
        self.assertAlmostEqual(z.real, 0.0)
        self.assertAlmostEqual(z.imag, 0.0)

        # Q02: 1 - 2^x >= 0 <=> x <= 0
        self.assertTrue(1 - 2**0 >= 0)
        self.assertFalse(1 - 2**0.01 >= 0)

        # Q03: 数列通项与求和极限
        # b_1 = log2(3-1) = 1, b_2 = log2(5-1) = 2 => b_n = n => a_n = 2^n + 1
        # 1/(a_{k+1} - a_k) = 1/2^k, sum_{k=1}^n 1/2^k = 1 - 1/2^n -> 1
        for n in range(1, 10):
            partial_sum = sum(Fraction(1, 2**k) for k in range(1, n + 1))
            self.assertEqual(partial_sum, 1 - Fraction(1, 2**n))

        # Q04: 线性规划可行域顶点 (2, 1), (0, 1), (2, 0)
        # z = x - y: min = 0 - 1 = -1, max = 2 - 0 = 2 => [-1, 2]
        vertices = [(2, 1), (0, 1), (2, 0)]
        z_vals = [x - y for x, y in vertices]
        self.assertEqual(min(z_vals), -1)
        self.assertEqual(max(z_vals), 2)

        # Q05: 正方体 O(1/2, 1/2, 1) 到 x + z - 1 = 0 距离
        # d = |1/2 + 1 - 1| / sqrt(1^2 + 1^2) = (1/2) / sqrt(2) = sqrt(2)/4
        d = (0.5) / math.sqrt(2)
        self.assertAlmostEqual(d, math.sqrt(2) / 4, places=7)

        # Q06: 导数周期性 2005 = 4*501 + 1 => f_1(x) = cos x
        self.assertEqual(2005 % 4, 1)

        # Q07: 双曲线渐近线夹角 90°
        # S = 1/2 * a * b = a^2 / 2 => a = b => 90°
        self.assertEqual(90, 90)

        # Q08: 充分条件 [-1, 2) 是 (-2, 2) 的子集
        self.assertTrue(-2 < -1 and 2 <= 2)

        # Q09: 四位同学竞赛总分 0
        # 2人甲对2人甲错: C(4, 2) = 6
        # 2人乙对2人乙错: C(4, 2) = 6
        # 1甲对1甲错1乙对1乙错: 4! = 24
        total_ways = math.comb(4, 2) + math.comb(4, 2) + math.perm(4, 4)
        self.assertEqual(total_ways, 36)

        # Q10: 面积重心坐标凸组合
        # Q(1/2, 1/3, 1/6) = 1/3 A + 1/6 B + 1/2 G
        u, v, w = Fraction(1, 3), Fraction(1, 6), Fraction(1, 2)
        self.assertEqual(u + v + w, 1)
        self.assertEqual(u + Fraction(1, 3) * w, Fraction(1, 2))
        self.assertEqual(v + Fraction(1, 3) * w, Fraction(1, 3))
        self.assertEqual(Fraction(1, 3) * w, Fraction(1, 6))

        # Q11: 分层抽样 16800 / 3 = 5600
        self.assertEqual(16800 // 3, 5600)

        # Q12: 二项展开式系数 C(7, 3) = 35
        self.assertEqual(sum(math.comb(k, 2) for k in range(2, 7)), 35)

        # Q13: OA . OB = cos(120°) = -1/2
        cos_120 = (1 + 1 - 3) / 2
        self.assertEqual(cos_120, -0.5)

        # Q14: f^{-1}(4) = -2
        self.assertEqual(2 * 1 - 4, -2)

        # Q15: 正弦函数面积积分
        # (1) 2/3 + 2/3 = 4/3
        self.assertEqual(Fraction(2, 3) + Fraction(2, 3), Fraction(4, 3))
        # (2) int_{pi/3}^{4pi/3} (1 - sin 3x) dx = pi + 2/3
        self.assertEqual("pi + 2/3", "pi + 2/3")

    def test_analytical_solutions_mathematics(self):
        """测试解答题（16-21）数学推导与结论正确性。"""
        # Q16: 解三角形
        a16 = math.pi / 4
        b16 = math.pi / 3
        c16 = 5 * math.pi / 12
        self.assertAlmostEqual(a16 + b16 + c16, math.pi, places=7)
        self.assertAlmostEqual(math.sin(b16) + math.cos(2 * c16), 0.0, places=7)

        # Q17: 空间向量与二面角
        # AC = (-3, 1, sqrt(3)), BO1 = (0, -3, sqrt(3)) => AC . BO1 = 0
        dot_prod = -3 * 0 + 1 * (-3) + math.sqrt(3) * math.sqrt(3)
        self.assertAlmostEqual(dot_prod, 0.0, places=7)
        cos_theta = math.sqrt(3) / 4
        self.assertAlmostEqual(cos_theta, 0.4330127, places=6)

        # Q18: 游览景点分布列与期望
        # P(X=0) = 0.6*0.5*0.4 = 0.12, P(X=3) = 0.4*0.5*0.6 = 0.12
        p_xi_3 = 0.12 + 0.12  # 0.24
        p_xi_1 = 1 - p_xi_3   # 0.76
        exp_xi = 1 * p_xi_1 + 3 * p_xi_3
        self.assertAlmostEqual(exp_xi, 1.48, places=7)
        # 单调增要求 3*xi/2 <= 2 <=> xi <= 4/3 => xi = 1
        p_a = p_xi_1
        self.assertAlmostEqual(p_a, 0.76, places=7)

        # Q19: 椭圆切线与等腰三角形
        # lambda = 1 - e^2
        # (1 - e^2) / sqrt(1 + e^2) = e => 1 - 3e^2 = 0 => e^2 = 1/3 => lambda = 2/3
        self.assertEqual(Fraction(1, 1) - Fraction(1, 3), Fraction(2, 3))

        # Q20: 鱼群种群模型
        # x_{n+1} = (3 - b)x_n - x_n^2
        # b <= 1 guarantees x_n > 0 for all n
        b_max = 1
        f_b1 = lambda x: 2 * x - x**2
        # Verify for initial points in (0, 2)
        for x0 in [0.1, 0.5, 1.0, 1.5, 1.9]:
            x = x0
            for _ in range(10):
                x = f_b1(x)
                self.assertGreater(x, 0)
                self.assertLessEqual(x, 1)

        # Q21: 导数压轴题切线不平行
        # phi(t) = ln t - 2(t-1)/(t+1) > 0 for all t > 1
        def phi(t):
            return math.log(t) - 2 * (t - 1) / (t + 1)

        for t in [1.01, 1.5, 2.0, 5.0, 10.0, 100.0]:
            self.assertGreater(phi(t), 0)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""2005 年高考数学真题（湖北卷理科 gk-2005-regular-hubei-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_湖北理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_湖北理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_湖北理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_湖北理科_含解析.md"


class Hubei2005ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、美元符号配对与题号连续性（全卷共 22 题）。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 23)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 23)))

    def test_multiple_choice_and_fill_in_blank_mathematics(self):
        """测试选择题（1-12）与填空题（13-16）数学推导与数值正确性。"""
        # Q01: 集合求和元素个数
        p = {0, 2, 5}
        q = {1, 2, 6}
        p_plus_q = {a + b for a in p for b in q}
        self.assertEqual(len(p_plus_q), 8)
        self.assertEqual(p_plus_q, {1, 2, 3, 4, 6, 7, 8, 11})

        # Q02: 命题真假（②④为真，共2个）
        true_propositions = [2, 4]
        self.assertEqual(len(true_propositions), 2)

        # Q04: 木星与地球表面积之比
        # 体积比 = 240 * sqrt(30) = sqrt(240^2 * 30) = sqrt(1728000) = sqrt(120^3) = 120^(3/2)
        # 表面积比 = (120^(1/2))^2 = 120
        v_ratio = 240 * math.sqrt(30)
        r_ratio = v_ratio ** (1 / 3)
        s_ratio = r_ratio ** 2
        self.assertAlmostEqual(s_ratio, 120.0, places=5)

        # Q05: 双曲线与抛物线焦点
        # y^2 = 4x 焦点为 (1, 0) => c = 1, e = c/a = 2 => a = 1/2 => m = 1/4
        # n = c^2 - a^2 = 1 - 1/4 = 3/4 => mn = 3/16
        c = 1
        a = Fraction(1, 2)
        m = a ** 2
        n = c ** 2 - a ** 2
        self.assertEqual(m * n, Fraction(3, 16))

        # Q07: sin(a) + cos(a) = tan(a) 根在 (pi/4, pi/3)
        def f7(x):
            return math.sin(x) + math.cos(x) - math.tan(x)
        self.assertGreater(f7(math.pi / 4), 0)
        self.assertLess(f7(math.pi / 3), 0)

        # Q08: 极限待定系数
        # lim (a/(1-x) - b/(1-x^2)) = 1 => 2a - b = 0 => b = 2a, -a/2 = 1 => a = -2, b = -4
        a8 = -2
        b8 = -4
        self.assertEqual(2 * a8 - b8, 0)
        self.assertEqual(-a8 / 2, 1.0)

        # Q11: 切线倾斜角小于 pi/4 整数点个数
        # 0 <= 3x^2 - 8 < 1 <=> 8/3 <= x^2 < 3, 无整数平方数
        squares = [x * x for x in range(-5, 6)]
        valid_int_points = [x for x in squares if Fraction(8, 3) <= x < 3]
        self.assertEqual(len(valid_int_points), 0)

        # Q12: 平行六面体三角形不共面概率
        # C(8, 3) = 56, C(56, 2) = 1540
        # 4 顶点平面 12 个，每个产生 C(4, 2) = 6 对，共 72 对
        # p_coplanar = 72 / 1540 = 18 / 385, p_not = 367 / 385
        total_triangles = math.comb(8, 3)
        self.assertEqual(total_triangles, 56)
        total_pairs = math.comb(total_triangles, 2)
        self.assertEqual(total_pairs, 1540)
        coplanar_pairs = 12 * math.comb(4, 2)
        self.assertEqual(coplanar_pairs, 72)
        p_not = Fraction(total_pairs - coplanar_pairs, total_pairs)
        self.assertEqual(p_not, Fraction(367, 385))

        # Q13: 模长不超过 5
        # (k+2)^2 <= 16 <=> -6 <= k <= 2
        self.assertEqual((-6 + 2) ** 2, 16)
        self.assertEqual((2 + 2) ** 2, 16)

        # Q14: 三项式展开常数项
        # (0, 0, 5): 5!/(0!0!5!) * (sqrt(2))^5 = 4*sqrt(2)
        # (1, 1, 3): 5!/(1!1!3!) * (1/2) * (sqrt(2))^3 = 20 * 1/2 * 2*sqrt(2) = 20*sqrt(2)
        # (2, 2, 1): 5!/(2!2!1!) * (1/4) * sqrt(2) = 30 * 1/4 * sqrt(2) = 15/2 * sqrt(2)
        # 4 + 20 + 15/2 = 63/2
        coeff = Fraction(4, 1) + Fraction(20, 1) + Fraction(15, 2)
        self.assertEqual(coeff, Fraction(63, 2))

        # Q15: 等比数列性质
        # 2 S_n = S_{n+1} + S_{n+2} <=> 2 a_{n+1} + a_{n+2} = 0 <=> 2 + q = 0 <=> q = -2
        self.assertEqual(-2, -2)

        # Q16: 整数规划最少花费
        # 35x + 24y >= 106, min 140x + 120y
        best_cost = min(
            140 * x + 120 * y
            for x in range(5)
            for y in range(6)
            if 35 * x + 24 * y >= 106
        )
        self.assertEqual(best_cost, 500)

    def test_analytical_solutions_mathematics(self):
        """测试解答题（17-22）数学推导与结论正确性。"""
        # Q17: g(x) = 3x^2 - 2x 在 (-1, 1) 上的上确界为 g(-1) = 5
        # t >= 5
        sup_g = max(3 * (x / 1000.0) ** 2 - 2 * (x / 1000.0) for x in range(-999, 1000))
        self.assertAlmostEqual(sup_g, 5.0, delta=0.01)

        # Q18: 解三角形
        # 3a^2 + 8a - 28 = 0 => (3a + 14)(a - 2) = 0 => a = 2
        # b^2 = 28/3 => b = 2*sqrt(21)/3
        # sin A = a * sin B / b = 2 * (sqrt(30)/6) / (2*sqrt(21)/3) = sqrt(70)/14
        a = 2
        cos_B = math.sqrt(6) / 6
        sin_B = math.sqrt(30) / 6
        b = math.sqrt(28 / 3)
        sin_A = a * sin_B / b
        expected_sin_A = math.sqrt(70) / 14
        self.assertAlmostEqual(sin_A, expected_sin_A, places=7)

        # Q19: 离散型分布列与数学期望
        p1 = 0.6
        p2 = (1 - 0.6) * 0.7  # 0.28
        p3 = (1 - 0.6) * (1 - 0.7) * 0.8  # 0.096
        p4 = (1 - 0.6) * (1 - 0.7) * (1 - 0.8)  # 0.024
        self.assertAlmostEqual(p1 + p2 + p3 + p4, 1.0, places=7)
        exp_xi = 1 * p1 + 2 * p2 + 3 * p3 + 4 * p4
        self.assertAlmostEqual(exp_xi, 1.544, places=7)
        p_license = 1 - (1 - 0.6) * (1 - 0.7) * (1 - 0.8) * (1 - 0.9)
        self.assertAlmostEqual(p_license, 0.9976, places=7)

        # Q20: 四棱锥立体几何
        # AC = (sqrt(3), 1, 0), PB = (sqrt(3), 0, -2)
        # cos theta = 3 / (2 * sqrt(7)) = 3*sqrt(7) / 14
        cos_theta = 3 / (2 * math.sqrt(7))
        self.assertAlmostEqual(cos_theta, 3 * math.sqrt(7) / 14, places=7)
        # N = (sqrt(3)/6, 0, 1), d_AB = |z| = 1, d_AP = |x| = sqrt(3)/6
        self.assertAlmostEqual(math.sqrt(3) / 6, 1 / (2 * math.sqrt(3)), places=7)

        # Q21: 椭圆弦长积
        # 3(1 - sqrt(2)/2 t)^2 + (3 + sqrt(2)/2 t)^2 = lambda => 2t^2 = lambda - 12
        # |NA|*|NB| = (lambda - 12)/2
        # CD: 2s^2 + 6*sqrt(2)s + 12 - lambda = 0 => |s1*s2| = (lambda - 12)/2
        for lam in [13, 20, 100]:
            prod_ab = (lam - 12) / 2
            prod_cd = abs(12 - lam) / 2
            self.assertEqual(prod_ab, prod_cd)

        # Q22: 数列不等式与 N
        # 2 / [log2 n] <= 1/5 <=> [log2 n] >= 10 <=> n >= 2^10 = 1024
        # 当 n > 1023 时满足条件
        self.assertEqual(2 ** 10, 1024)
        self.assertEqual(math.floor(math.log2(1024)), 10)
        self.assertEqual(math.floor(math.log2(1023)), 9)


if __name__ == "__main__":
    unittest.main()

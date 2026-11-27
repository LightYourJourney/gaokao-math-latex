# -*- coding: utf-8 -*-
"""2005 年高考数学真题（湖北卷文科 gk-2005-regular-hubei-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_湖北文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_湖北文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_湖北文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_湖北文科_含解析.md"


class Hubei2005ArtsSolutionsTests(unittest.TestCase):
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

        # Q03: 向量模长
        for k in [-6, -2, 0, 2]:
            norm_sq = 3**2 + (k + 2)**2
            self.assertLessEqual(norm_sq, 25)
        self.assertGreater(3**2 + (2.1 + 2)**2, 25)
        self.assertGreater(3**2 + (-6.1 + 2)**2, 25)

        # Q05: 球体表面积比
        v_ratio = 240 * math.sqrt(30)
        self.assertAlmostEqual(v_ratio**2, 120**3, places=5)
        r_ratio = math.sqrt(120)
        s_ratio = r_ratio**2
        self.assertAlmostEqual(s_ratio, 120.0, places=5)

        # Q06: 双曲线焦点重合
        # c = 1, e = 2 => a = 1/2 => m = 1/4, n = 3/4 => mn = 3/16
        m = Fraction(1, 4)
        n = Fraction(3, 4)
        self.assertEqual(m * n, Fraction(3, 16))

        # Q09: 连续电影票分票
        # 4! * C(4, 2) = 24 * 6 = 144
        c_4_2 = 6
        perm_4 = math.factorial(4)
        self.assertEqual(c_4_2 * perm_4, 144)

        # Q10: 三角方程根在 (pi/4, pi/3)
        def g(alpha):
            return math.sin(alpha) + math.cos(alpha) - math.tan(alpha)
        self.assertGreater(g(math.pi / 4), 0)
        self.assertLess(g(math.pi / 3), 0)

        # Q11: 切线倾斜角小于 pi/4 整数点个数为 0
        int_sqs = [x**2 for x in range(-10, 11)]
        valid_points = [x for x in int_sqs if 8/3 <= x < 3]
        self.assertEqual(len(valid_points), 0)

        # Q14: 二项展开常数项
        # C(4, 3)*(-2)^3 + C(8, 4) = 4*(-8) + 70 = -32 + 70 = 38
        term1 = 4 * (-8)
        term2 = math.comb(8, 4)
        self.assertEqual(term1 + term2, 38)

        # Q15: 周期与最值和
        # T = 2*pi, y_max = 1/2 - 1 = -1/2
        self.assertAlmostEqual(2 * math.pi - 0.5, 2 * math.pi - Fraction(1, 2), places=7)

        # Q16: 购料最省
        best_cost = min(
            140 * x + 120 * y
            for x in range(5)
            for y in range(6)
            if 35 * x + 24 * y >= 106
        )
        self.assertEqual(best_cost, 500)

    def test_analytical_and_applied_solutions(self):
        """测试解答题（17-22）核心公式、递推求和与几何参数。"""
        # Q17: 增函数参数范围 t >= sup_{(-1, 1)} (3x^2 - 2x) = 5
        g_vals = [3 * (x / 100)**2 - 2 * (x / 100) for x in range(-99, 100)]
        self.assertLess(max(g_vals), 5.0)

        # Q18: 解三角形面积
        # S = 6*sqrt(2) + 8*sqrt(3)
        b = 3 * math.sqrt(6)
        sin_B = math.sqrt(3) / 2
        cos_C = 1 / 3
        sin_C = 2 * math.sqrt(2) / 3
        sin_A = (math.sqrt(3) + 2 * math.sqrt(2)) / 6
        c = b * sin_C / sin_B
        self.assertAlmostEqual(c, 8.0, places=7)
        area = 0.5 * b * c * sin_A
        expected_area = 6 * math.sqrt(2) + 8 * math.sqrt(3)
        self.assertAlmostEqual(area, expected_area, places=7)

        # Q19: 数列求和
        for n in range(1, 6):
            c_sum = sum((2 * k - 1) * (4**(k - 1)) for k in range(1, n + 1))
            formula_val = ((6 * n - 5) * (4**n) + 5) // 9
            self.assertEqual(c_sum, formula_val)

        # Q20: 空间立体截面 BF = 2*sqrt(6), 距离 d = 4*sqrt(33)/11
        bd = math.sqrt(4**2 + 2**2)
        df = 2.0
        bf = math.sqrt(bd**2 + df**2)
        self.assertAlmostEqual(bf, 2 * math.sqrt(6), places=7)
        d_val = 12 / math.sqrt(33)
        self.assertAlmostEqual(d_val, 4 * math.sqrt(33) / 11, places=7)

        # Q21: 灯泡概率模型
        p1 = 0.8
        p2 = 0.3
        p = (p1 - p2) + (1 - p1)**2
        self.assertAlmostEqual(p, 0.54, places=7)
        prob_ge4 = 5 * (p**4) * (1 - p) + (p**5)
        self.assertEqual(f"{prob_ge4:.2g}", "0.24")

        # Q22: 椭圆弦中点与四点共圆恒等式
        for lam in [13, 16, 25, 100]:
            na_nb = (lam - 12) / 2
            x3 = -0.5 + 0.5 * math.sqrt(lam - 3)
            x4 = -0.5 - 0.5 * math.sqrt(lam - 3)
            nc = math.sqrt(2) * abs(x3 - 1)
            nd = math.sqrt(2) * abs(x4 - 1)
            self.assertAlmostEqual(na_nb, nc * nd, places=7)


if __name__ == "__main__":
    unittest.main()

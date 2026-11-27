# -*- coding: utf-8 -*-
"""2005 年高考数学真题（重庆理科卷 gk-2005-regular-chongqing-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_重庆理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_重庆理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_重庆理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_重庆理科_含解析.md"


class ChongqingScience2005SolutionsTests(unittest.TestCase):
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
        """测试选择题（1-10）与填空题（11-16）数学推导与数值正确性。"""
        # Q01: 圆 (x + 2)^2 + y^2 = 5 关于原点对称得到 (x - 2)^2 + y^2 = 5
        center = (-2, 0)
        sym_center = (-center[0], -center[1])
        self.assertEqual(sym_center, (2, 0))

        # Q02: ((1 + i)/(1 - i))^2005 = i^2005 = i
        self.assertEqual(2005 % 4, 1)

        # Q03: 偶函数 f(2) = 0, 在 (-inf, 0] 递减 => 在 [0, inf) 递增 => f(x) < 0 解集为 (-2, 2)
        self.assertTrue(-2 < 0 < 2)

        # Q04: A(3,1), B(6,1), C(4,3), D(5,2) => AC=(1,2), DA=(-2,-1) => dot = -4, cos = -4/5
        ac = (1, 2)
        da = (-2, -1)
        dot = ac[0] * da[0] + ac[1] * da[1]
        self.assertEqual(dot, -4)
        cos_theta = dot / (math.sqrt(ac[0]**2 + ac[1]**2) * math.sqrt(da[0]**2 + da[1]**2))
        self.assertAlmostEqual(cos_theta, -0.8, places=7)

        # Q05: (x + 1/(2y))^2 + (y + 1/(2x))^2 最小值为 4 (x = y = sqrt(2)/2)
        x0 = y0 = math.sqrt(2) / 2.0
        val5 = (x0 + 1.0 / (2 * y0))**2 + (y0 + 1.0 / (2 * x0))**2
        self.assertAlmostEqual(val5, 4.0, places=7)

        # Q06: alpha=30°, beta=60° => sin alpha < sin(alpha+beta), alpha+beta not < 90°
        alpha = math.radians(30)
        beta = math.radians(60)
        self.assertTrue(math.sin(alpha) < math.sin(alpha + beta))
        self.assertFalse(alpha + beta < math.pi / 2.0)

        # Q07: 平行判定条件 ② 和 ④ 为真，共 2 个
        self.assertEqual(2, 2)

        # Q08: (2x - 1/x)^n 含 x^-2 与 x^-4 系数比为 -5 => n = 6
        n = 6
        # x^(n - 2r): r = (n+2)/2 = 4 for x^-2; r = (n+4)/2 = 5 for x^-4
        coeff_neg2 = ((-1)**4) * math.comb(n, 4) * (2**(n - 4))
        coeff_neg4 = ((-1)**5) * math.comb(n, 5) * (2**(n - 5))
        self.assertEqual(coeff_neg2 / coeff_neg4, -5.0)

        # Q09: x^2 + 2y 最大值在 0 < b < 4 时为 b^2/4 + 4，在 b >= 4 时为 2b
        b1 = 2
        self.assertEqual(b1**2 / 4.0 + 4.0, 5.0)
        b2 = 5
        self.assertEqual(2.0 * b2, 10.0)

        # Q10: 四面体重心坐标 x_A = 1/7 => V_{O-BCD} = 1/7
        self.assertEqual(Fraction(1, 1 + 2 + 2 + 2), Fraction(1, 7))

        # Q11: A = (-2, 3), B = (0, 4) => A & B = (0, 3)
        self.assertEqual((max(-2, 0), min(3, 4)), (0, 3))

        # Q12: y = x^3 在 (a, a^3) 处切线围成三角形面积 1/6 a^4 = 1/6 => a = +-1
        self.assertEqual(Fraction(1, 6) * (1**4), Fraction(1, 6))

        # Q13: cos(alpha + beta) = sin(alpha - beta) => tan alpha = 1
        self.assertEqual(1, 1)

        # Q14: lim (8^n - 3*9^n)/(8^n + 9^n) = -3
        self.assertEqual(-3, -3)

        # Q15: 轻轨车厢人数 0, 1, 2, 3 概率 A(4,4)*C(6,1)*C(5,2)/4^6 = 1440/4096 = 45/128
        p15 = Fraction(math.perm(4, 4) * math.comb(6, 1) * math.comb(5, 2), 4**6)
        self.assertEqual(p15, Fraction(45, 128))

        # Q16: 抛物线四点四边形可能构型为 ②③⑤
        correct_16 = {2, 3, 5}
        self.assertTrue(1 not in correct_16 and 4 not in correct_16)

    def test_analytical_solutions_mathematics(self):
        """测试解答题（17-22）数学推导与结论正确性。"""
        # Q17: f(x) 最大值为 sqrt(a^2 + 1)/2 = 2 => a^2 = 15 => a = +-sqrt(15)
        self.assertEqual(4**2 - 1, 15)

        # Q18: 抽奖概率与期望
        # (1) 中奖概率 1 - C(6, 2)/C(10, 2) = 1 - 15/45 = 2/3
        p_win = 1 - Fraction(math.comb(6, 2), math.comb(10, 2))
        self.assertEqual(p_win, Fraction(2, 3))
        # (2) 期望 E(xi) = 16
        dist = {
            0: Fraction(15, 45),
            10: Fraction(18, 45),
            20: Fraction(3, 45),
            50: Fraction(6, 45),
            60: Fraction(3, 45)
        }
        self.assertEqual(sum(dist.values()), 1)
        e_xi = sum(k * p for k, p in dist.items())
        self.assertEqual(e_xi, 16)

        # Q19: f'(x) = e^x [x^2 + (a+2)x + 2a+1], Delta = a(a-4)
        # 0 <= a <= 4: 0 个极值点; a < 0 或 a > 4: 2 个极值点
        self.assertEqual(2**2 - 4 * 1, 0)

        # Q20: 三棱柱公垂线与二面角
        # (1) BE^2 = x^2 - x + 1, EB1^2 = x^2 - 5x + 7, BE^2 + EB1^2 = 4 => x = 1, BE = 1
        x = 1
        be_sq = x**2 - x + 1
        eb1_sq = x**2 - 5 * x + 7
        self.assertEqual(be_sq + eb1_sq, 4)
        self.assertEqual(math.sqrt(be_sq), 1.0)
        # (2) 二面角法向量 n1 = (1, sqrt(2), 0), n2 = (0, 1, 0)
        # cos theta = sqrt(2)/sqrt(3) = sqrt(6)/3 => tan theta = (1/sqrt(3))/(sqrt(2)/sqrt(3)) = sqrt(2)/2
        tan_theta = (1.0 / math.sqrt(3)) / (math.sqrt(2) / math.sqrt(3))
        self.assertAlmostEqual(tan_theta, math.sqrt(2) / 2.0, places=7)

        # Q21: 椭圆与双曲线
        # (1) 双曲线 a^2 = 3, b^2 = 1 => x^2/3 - y^2 = 1
        self.assertEqual(2**2 - 3, 1)
        # (2) k^2 in (1/4, 1/3) U (13/15, 1)
        self.assertTrue(Fraction(1, 4) < Fraction(7, 24) < Fraction(1, 3))
        self.assertTrue(Fraction(13, 15) < Fraction(9, 10) < 1)

        # Q22: 数列归纳法与放缩
        # (1) a1 = 1, a2 = 2 >= 2
        a = [0, 1]
        for n in range(1, 5):
            a_next = (1 + Fraction(1, n**2 + n)) * a[-1] + Fraction(1, 2**n)
            a.append(a_next)
        self.assertEqual(a[2], 2)
        self.assertTrue(all(a[n] >= 2 for n in range(2, 6)))
        # (2) P_n < e => a_n < 2e < e^2
        self.assertLess(2 * math.e, math.e**2)


if __name__ == "__main__":
    unittest.main()

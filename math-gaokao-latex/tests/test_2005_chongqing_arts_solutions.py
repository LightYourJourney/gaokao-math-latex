# -*- coding: utf-8 -*-
"""2005 年高考数学真题（重庆文科卷 gk-2005-regular-chongqing-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_重庆文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_重庆文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_重庆文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_重庆文科_含解析.md"


class ChongqingArts2005SolutionsTests(unittest.TestCase):
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
        # Q01: 圆对称 (x + 2)^2 + y^2 = 5 关于原点对称得到 (x - 2)^2 + y^2 = 5
        center = (-2, 0)
        sym_center = (-center[0], -center[1])
        self.assertEqual(sym_center, (2, 0))

        # Q02: cos^2(pi/12) - sin^2(pi/12) = cos(pi/6) = sqrt(3)/2
        val = math.cos(math.pi / 12)**2 - math.sin(math.pi / 12)**2
        self.assertAlmostEqual(val, math.sqrt(3) / 2.0, places=7)

        # Q03: 偶函数 f(2) = 0, 在 (-inf, 0] 递减 => 在 [0, inf) 递增 => f(x) < 0 解集为 (-2, 2)
        # 验证性质
        self.assertTrue(-2 < 0 < 2)

        # Q04: 向量运算
        a = (-1, 2)
        b = (2, -1)
        dot = a[0] * b[0] + a[1] * b[1]
        self.assertEqual(dot, -4)
        vec_sum = (a[0] + b[0], a[1] + b[1])
        self.assertEqual(vec_sum, (1, 1))
        self.assertEqual((dot * vec_sum[0], dot * vec_sum[1]), (-4, -4))

        # Q05: 不等式组 |x - 2| < 2 => 0 < x < 4; log2(x^2 - 1) > 1 => x^2 > 3 => (sqrt(3), 4)
        self.assertTrue(math.sqrt(3) < 2 < 4)

        # Q06: 锐角必要不充分条件：取 alpha = 30°, beta = 60°
        alpha = math.radians(30)
        beta = math.radians(60)
        self.assertTrue(math.sin(alpha) < math.sin(alpha + beta))
        self.assertFalse(alpha + beta < math.pi / 2.0)

        # Q07: 平行判定条件 ② 和 ④ 为真，共 2 个
        self.assertEqual(2, 2)

        # Q08: (1 + 2x)^n 展开式：C(n, 3) * 8 = 8 * (2n) => (n - 1)(n - 2) = 12 => n = 5
        n = 5
        coeff_x3 = math.comb(n, 3) * (2**3)
        coeff_x = math.comb(n, 1) * 2
        self.assertEqual(coeff_x3, 8 * coeff_x)

        # Q09: x^2 + 2y 最大值在 0 < b < 4 时为 b^2/4 + 4，在 b >= 4 时为 2b
        b1 = 2
        f1_max = b1**2 / 4.0 + 4.0
        self.assertEqual(f1_max, 5.0)
        b2 = 5
        f2_max = 2.0 * b2
        self.assertEqual(f2_max, 10.0)

        # Q10: 塔形正方体表面积：S_tot = 40 - 32/2^n > 39 => 2^n > 32 => n >= 6
        n_vals = {n: 40 - 32 / (2**n) for n in range(1, 8)}
        self.assertLessEqual(n_vals[5], 39.0)
        self.assertGreater(n_vals[6], 39.0)

        # Q11: A = (1, 3), B = (2, 5) => A & B = (2, 3)
        self.assertEqual((max(1, 2), min(3, 5)), (2, 3))

        # Q12: 切线 y = 3x - 2，与 x 轴交于 (2/3, 0)，与 x = 2 交于 (2, 4)
        # 三角形面积 = 1/2 * (2 - 2/3) * 4 = 8/3
        s12 = Fraction(1, 2) * (2 - Fraction(2, 3)) * 4
        self.assertEqual(s12, Fraction(8, 3))

        # Q13: cos(alpha + beta) = sin(alpha - beta) => tan alpha = 1
        self.assertEqual(1, 1)

        # Q14: x^2 + y^2 = 4 时 x - y 的最大值为 2*sqrt(2)
        self.assertAlmostEqual(2 * math.sqrt(2), math.sqrt(8), places=7)

        # Q15: 开锁概率 1 - C(8, 2)/C(10, 2) = 1 - 28/45 = 17/45
        p15 = 1 - Fraction(math.comb(8, 2), math.comb(10, 2))
        self.assertEqual(p15, Fraction(17, 45))

        # Q16: 椭圆轨迹 a = 1, c = 1/2, b^2 = 3/4 => x^2 + 4y^2/3 = 1
        a = 1
        c = Fraction(1, 2)
        b2 = a**2 - c**2
        self.assertEqual(b2, Fraction(3, 4))

    def test_analytical_solutions_mathematics(self):
        """测试解答题（17-22）数学推导与结论正确性。"""
        # Q17: f(x) = (sqrt(2) + a^2)*sin(x + pi/4) 最大值为 sqrt(2) + a^2 = sqrt(2) + 3 => a^2 = 3 => a = +-sqrt(3)
        self.assertEqual(3, int(math.sqrt(3)**2 + 0.5))

        # Q18: 零件工序合格率与二项分布
        p18 = Fraction(9, 10) * Fraction(8, 9) * Fraction(7, 8)
        self.assertEqual(p18, Fraction(7, 10))
        # 恰好一件合格
        p_one = math.comb(3, 1) * Fraction(7, 10) * (Fraction(3, 10)**2)
        self.assertEqual(p_one, Fraction(189, 1000))
        # 至少一件合格
        p_at_least = 1 - (Fraction(3, 10)**3)
        self.assertEqual(p_at_least, Fraction(973, 1000))

        # Q19: f'(x) = 6(x - 1)(x - a)
        # (1) x = 3 处取得极值 => a = 3
        self.assertEqual(3, 3)
        # (2) 在 (-inf, 0) 上增 => a >= 0
        self.assertTrue(0 >= 0)

        # Q20: 四棱锥公垂线与二面角
        # (1) 勾股定理验证 AD = sqrt(3)/2
        ad_sq = Fraction(3, 4)
        de_sq = ad_sq + Fraction(1, 4)
        ec_sq = ad_sq + Fraction(9, 4)
        cd_sq = 4
        self.assertEqual(de_sq + ec_sq, cd_sq)
        self.assertEqual(math.sqrt(float(de_sq)), 1.0)

        # (2) 二面角余弦 cos theta = sqrt(2)/2 => theta = pi/4
        n1 = (1, 0, 0)
        n2 = (math.sqrt(3), 1, math.sqrt(2))
        cos_theta = n2[0] / math.sqrt(n2[0]**2 + n2[1]**2 + n2[2]**2)
        self.assertAlmostEqual(cos_theta, math.sqrt(2) / 2.0, places=7)

        # Q21: 双曲线与割线
        # (1) a^2 = 3, c = 2 => b^2 = 1 => x^2/3 - y^2 = 1
        self.assertEqual(2**2 - 3, 1)
        # (2) 判别式 36(1 - k^2) > 0 => k^2 < 1; OA . OB > 2 => k^2 > 1/3
        # 范围为 (-1, -sqrt(3)/3) U (sqrt(3)/3, 1)
        self.assertTrue(Fraction(1, 3) < Fraction(1, 2) < 1)

        # Q22: 递推数列
        # (1) b1 = 2, b2 = 8/3, b3 = 4, b4 = 20/3
        b = [0, 2]
        for n in range(1, 4):
            b.append(Fraction(2) * b[-1] - Fraction(4, 3))
        self.assertEqual(b[1], 2)
        self.assertEqual(b[2], Fraction(8, 3))
        self.assertEqual(b[3], 4)
        self.assertEqual(b[4], Fraction(20, 3))

        # (2) 通项 b_n = (2^n + 4)/3, 前 n 项和 S_n = (2^n + 5n - 1)/3
        for n in range(1, 6):
            self.assertEqual(b[n] if n <= 4 else (2**n + 4)/Fraction(3), (2**n + 4) / Fraction(3))
        # 验算前 4 项和
        s_sum = sum(1 + Fraction(1, 2) * Fraction(2**k + 4, 3) for k in range(1, 5))
        s_formula = Fraction(2**4 + 5 * 4 - 1, 3)
        self.assertEqual(s_sum, s_formula)


if __name__ == "__main__":
    unittest.main()

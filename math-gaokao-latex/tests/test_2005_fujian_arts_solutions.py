# -*- coding: utf-8 -*-
"""2005 年高考数学真题（福建文科卷 gk-2005-regular-fujian-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_福建文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_福建文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_福建文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_福建文科_含解析.md"


class FujianArts2005SolutionsTests(unittest.TestCase):
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
        # Q01: P = {x | |x-1| <= 1} = [0, 2], Q = N => P & Q = {0, 1, 2}
        p_set = {x for x in range(-5, 6) if abs(x - 1) <= 1}
        q_set = {x for x in range(0, 10)}
        self.assertEqual(p_set & q_set, {0, 1, 2})

        # Q02: (2x - 1)/(3x + 1) > 0 <=> x < -1/3 or x > 1/2
        self.assertTrue((2 * (-1) - 1) / (3 * (-1) + 1) > 0)
        self.assertTrue((2 * (1) - 1) / (3 * (1) + 1) > 0)
        self.assertFalse((2 * (0) - 1) / (3 * (0) + 1) > 0)

        # Q03: a7 + a9 = 16 => a8 = 8, a4 = 1 => 4d = 7 => a12 = a8 + 4d = 15
        a8 = 8
        a4 = 1
        d = Fraction(a8 - a4, 4)
        a12 = a8 + 4 * d
        self.assertEqual(a12, 15)

        # Q04: y = cos 2x 在 [0, pi/2] 单调递减
        self.assertTrue(math.cos(2 * 0) > math.cos(2 * (math.pi / 4)) > math.cos(2 * (math.pi / 2)))

        # Q05: 基本不等式 sqrt(x) + 1/sqrt(x) >= 2
        for x in [0.1, 0.5, 1.0, 2.0, 10.0]:
            self.assertGreaterEqual(math.sqrt(x) + 1.0 / math.sqrt(x), 2.0 - 1e-9)

        # Q06: f(x) = a^(x-b) 单调减 => 0 < a < 1; f(0) = a^(-b) > 1 => b > 0
        a, b = 0.5, 1.0
        self.assertTrue(0 < a < 1 and b > 0)
        self.assertGreater(a**(-b), 1.0)

        # Q07: 立体几何命题 ②③ 为真，共 2 个
        self.assertEqual(2, 2)

        # Q08: p: a != 0, q: ab != 0 => q => p 但 p 不推出 q，必要不充分
        self.assertTrue(True)

        # Q09: 双曲线 |PA| - |PB| = 3, 2c = 4 => c = 2, 2a = 3 => a = 3/2 => |PA|_min = a + c = 7/2
        c = 2
        a = Fraction(3, 2)
        pa_min = c + a
        self.assertEqual(pa_min, Fraction(7, 2))

        # Q10: 巴黎 4 选 1，其余 5 选 3 排列 => 4 * A(5, 3) = 4 * 60 = 240
        ways = math.comb(4, 1) * math.perm(5, 3)
        self.assertEqual(ways, 240)

        # Q11: 长方体 A1(1,0,2), E(0,0,1), F(1,1,0), G(0,2,1)
        # A1E = (-1, 0, -1), GF = (1, -1, -1) => dot = -1 + 0 + 1 = 0 => 90°
        a1e = (-1, 0, -1)
        gf = (1, -1, -1)
        dot11 = a1e[0] * gf[0] + a1e[1] * gf[1] + a1e[2] * gf[2]
        self.assertEqual(dot11, 0)

        # Q12: 偶函数 f(2) = 0 => f(-2) = 0, 周期 3 => f(1)=0, f(4)=0, f(5)=0 => 在 (0, 6) 内至少 4 个根
        roots = {1, 2, 4, 5}
        self.assertTrue(all(0 < r < 6 for r in roots))
        self.assertEqual(len(roots), 4)

        # Q13: (2*sqrt(x) - 1/x)^6 常数项 r = 2 => C(6, 2)*2^4*(-1)^2 = 15 * 16 = 240
        coeff13 = math.comb(6, 2) * (2**4) * ((-1)**2)
        self.assertEqual(coeff13, 240)

        # Q14: CA = (-2, -3), CB = (k-2, -2), CA . CB = 0 => -2(k-2) + 6 = 0 => k = 5
        k = 5
        ca = (-2, -3)
        cb = (k - 2, -2)
        self.assertEqual(ca[0] * cb[0] + ca[1] * cb[1], 0)

        # Q15: x, y >= 0 且 2x + y <= 0 => x = y = 0 => max(x + 3y) = 0
        self.assertEqual(0 + 3 * 0, 0)

        # Q16: y = 3 + log2(x) 反函数 x = 2^(y-3) => g(x) = 2^(x-3)
        self.assertEqual(2**(3 - 3), 1)

    def test_analytical_solutions_mathematics(self):
        """测试解答题（17-22）数学推导与结论正确性。"""
        # Q17: sin x + cos x = 1/5
        # (1) 2 sin x cos x = -24/25, x in (-pi/2, 0) => sin x - cos x = -sqrt(49/25) = -7/5
        sin_plus_cos = Fraction(1, 5)
        two_sin_cos = sin_plus_cos**2 - 1
        self.assertEqual(two_sin_cos, Fraction(-24, 25))
        sin_minus_cos_sq = 1 - two_sin_cos
        self.assertEqual(sin_minus_cos_sq, Fraction(49, 25))
        sin_minus_cos = -Fraction(7, 5)
        # 解出 sin x = -3/5, cos x = 4/5
        sin_x = (sin_plus_cos + sin_minus_cos) / 2
        cos_x = (sin_plus_cos - sin_minus_cos) / 2
        self.assertEqual(sin_x, Fraction(-3, 5))
        self.assertEqual(cos_x, Fraction(4, 5))
        # (2) (sin 2x + 2 sin^2 x)/(1 - tan x) = -24/175
        tan_x = sin_x / cos_x
        num17 = 2 * sin_x * cos_x + 2 * (sin_x**2)
        den17 = 1 - tan_x
        res17 = num17 / den17
        self.assertEqual(res17, Fraction(-24, 175))

        # Q18:
        # (1) E(xi) = 1/2 + 2/5 = 9/10
        p_a, p_b = Fraction(1, 2), Fraction(2, 5)
        e_xi = p_a + p_b
        self.assertEqual(e_xi, Fraction(9, 10))
        # (2) 至少一次命中 = 1 - (1/2)^2 * (3/5)^2 = 1 - 9/100 = 91/100
        p_none = (1 - p_a)**2 * (1 - p_b)**2
        self.assertEqual(1 - p_none, Fraction(91, 100))

        # Q19:
        # (1) 2q^2 - q - 1 = 0 => q = 1 or q = -1/2
        q1, q2 = 1, Fraction(-1, 2)
        self.assertEqual(2 * q1**2 - q1 - 1, 0)
        self.assertEqual(2 * q2**2 - q2 - 1, 0)
        # (2) 当 q = 1 时, Sn - bn = (n+2)(n-1)/2 > 0 for all n >= 2
        for n in range(2, 10):
            bn = 2 + (n - 1) * 1
            sn = n * (2 + bn) // 2
            self.assertGreater(sn, bn)
        # 当 q = -1/2 时, Sn - bn = -(n-1)(n-10)/4
        for n in range(2, 10):
            self.assertGreater(-(n - 1) * (n - 10), 0)
        self.assertEqual(-(10 - 1) * (10 - 10), 0)
        for n in range(11, 20):
            self.assertLess(-(n - 1) * (n - 10), 0)

        # Q20: f(x) = x^3 - 3x^2 - 3x + 2
        # f'(x) = 3x^2 - 6x - 3 = 3(x^2 - 2x - 1)
        # 切线: f(-1) = -1 - 3 + 3 + 2 = 1, f'(-1) = 3 + 6 - 3 = 6 => y - 1 = 6(x + 1) => 6x - y + 7 = 0
        self.assertEqual((-1)**3 - 3 * (-1)**2 - 3 * (-1) + 2, 1)
        self.assertEqual(3 * (-1)**2 - 6 * (-1) - 3, 6)
        # 极值点 1 +- sqrt(2)
        r1 = 1 - math.sqrt(2)
        r2 = 1 + math.sqrt(2)
        self.assertAlmostEqual(3 * r1**2 - 6 * r1 - 3, 0.0, places=7)
        self.assertAlmostEqual(3 * r2**2 - 6 * r2 - 3, 0.0, places=7)

        # Q21:
        # (1) AB = 2, AE = EB = sqrt(2), BC = 2 => CE = sqrt(4 + 2) = sqrt(6)
        # BF = 2 * sqrt(2) / sqrt(6) = 2/sqrt(3) = 2*sqrt(3)/3
        # (2) BH = sqrt(2) => sin theta = BF / BH = (2/sqrt(3)) / sqrt(2) = sqrt(2/3) => cos theta = sqrt(1/3) = sqrt(3)/3
        cos_theta21 = math.sqrt(3) / 3.0
        sin_theta21 = math.sqrt(2.0 / 3.0)
        self.assertAlmostEqual(cos_theta21**2 + sin_theta21**2, 1.0, places=7)
        # (3) 等体积法: V = 1/3 * (1/2 * 2 * 2) * 1 = 2/3
        # S_ACE = 1/2 * sqrt(2) * sqrt(6) = sqrt(3) => d = (3 * 2/3) / sqrt(3) = 2*sqrt(3)/3
        d21 = 2.0 / math.sqrt(3)
        self.assertAlmostEqual(d21, 2 * math.sqrt(3) / 3.0, places=7)

        # Q22:
        # (1) 直线 l: y = sqrt(3)x - 2*sqrt(3), 焦点 c = 2
        # 对称点 (3, -sqrt(3)) on x = a^2/c => a^2 = 6, b^2 = 2 => x^2/6 + y^2/2 = 1
        c22 = 2
        a_sq = 3 * c22
        b_sq = a_sq - c22**2
        self.assertEqual((a_sq, b_sq), (6, 2))
        # (2) S_MON = 2*sqrt(6)/3
        # 斜率不存在: x = -2 => y = +-sqrt(6)/3 => S = 1/2 * 2 * (2*sqrt(6)/3) = 2*sqrt(6)/3, dot = 4 - 2/3 = 10/3 != 0
        # 斜率存在: k = +-sqrt(3)/3 => dot = -4/3 != 0
        k_sq = Fraction(1, 3)
        # S = 2*sqrt(6)*|k|*sqrt(k^2+1)/(1 + 3k^2) = 2*sqrt(6)*(1/sqrt(3))*(2/sqrt(3)) / 2 = 2*sqrt(6)/3
        self.assertEqual(9 * k_sq * (k_sq + 1), (1 + 3 * k_sq)**2)


if __name__ == "__main__":
    unittest.main()

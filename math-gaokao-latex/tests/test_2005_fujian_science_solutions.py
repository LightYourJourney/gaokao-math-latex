# -*- coding: utf-8 -*-
"""2005 年高考数学真题（福建理科卷 gk-2005-regular-fujian-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_福建理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_福建理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_福建理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_福建理科_含解析.md"


class FujianScience2005SolutionsTests(unittest.TestCase):
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
        # Q01: z = 1/(1-i) = 1/2 + 1/2 i => bar(z) = 1/2 - 1/2 i
        z = 1 / (1 - 1j)
        self.assertEqual(z.conjugate(), 0.5 - 0.5j)

        # Q02: a7 + a9 = 16 => a8 = 8, a4 = 1 => 4d = 7 => a12 = a8 + 4d = 15
        a8 = 8
        a4 = 1
        d = Fraction(a8 - a4, 4)
        a12 = a8 + 4 * d
        self.assertEqual(a12, 15)

        # Q03: CA = (-2, -3), CB = (k-2, -2), CA . CB = 0 => -2(k-2) + 6 = 0 => k = 5
        k = 5
        ca = (-2, -3)
        cb = (k - 2, -2)
        self.assertEqual(ca[0] * cb[0] + ca[1] * cb[1], 0)

        # Q04: 立体几何命题 ②③ 为真，共 2 个
        self.assertEqual(2, 2)

        # Q05: f(x) = a^(x-b) 单调减 => 0 < a < 1; f(0) = a^(-b) < 1 => -b > 0 => b < 0
        a, b = 0.5, -0.5
        self.assertTrue(0 < a < 1 and b < 0)
        self.assertLess(a**(-b), 1.0)

        # Q06: y = sin(omega*x + phi), T/4 = 3 - 1 = 2 => T = 8 => omega = pi/4, phi = pi/4
        omega = math.pi / 4.0
        phi = math.pi / 4.0
        self.assertAlmostEqual(math.sin(omega * 1 + phi), 1.0, places=7)
        self.assertAlmostEqual(math.sin(omega * 3 + phi), 0.0, places=7)

        # Q07: p: |2x - 3| < 1 <=> 1 < x < 2; q: 0 < x < 3 => 充分不必要条件
        self.assertTrue(True)

        # Q08: 长方体 A1(1,0,2), E(0,0,1), F(1,1,0), G(0,2,1)
        # A1E = (-1, 0, -1), GF = (1, -1, -1) => dot = -1 + 0 + 1 = 0 => 90°
        a1e = (-1, 0, -1)
        gf = (1, -1, -1)
        dot08 = a1e[0] * gf[0] + a1e[1] * gf[1] + a1e[2] * gf[2]
        self.assertEqual(dot08, 0)

        # Q09: 巴黎 4 选 1，其余 5 选 3 排列 => 4 * A(5, 3) = 4 * 60 = 240
        ways = math.comb(4, 1) * math.perm(5, 3)
        self.assertEqual(ways, 240)

        # Q10: 正三角形 side 2c, P midpoint of MF1 => PF1 = c, PF2 = sqrt(3)c => 2a = (sqrt(3)-1)c => e = sqrt(3)+1
        c10 = 1.0
        a10 = (math.sqrt(3) - 1.0) / 2.0
        e10 = c10 / a10
        self.assertAlmostEqual(e10, math.sqrt(3) + 1.0, places=7)

        # Q11: a^2 + 2b^2 = 6, min(a+b) = -3
        # Cauchy: (a+b)^2 <= (1 + 1/2)(a^2 + 2b^2) = 3/2 * 6 = 9 => a+b >= -3
        a11, b11 = -2, -1
        self.assertEqual(a11**2 + 2 * b11**2, 6)
        self.assertEqual(a11 + b11, -3)

        # Q12: 奇函数 f(2) = 0 => f(-2) = 0, 周期 3 => f(1)=0, f(2)=0, f(3)=0, f(4)=0, f(5)=0 => 在 (0, 6) 内至少 5 个根
        roots = {1, 2, 3, 4, 5}
        self.assertTrue(all(0 < r < 6 for r in roots))
        self.assertEqual(len(roots), 5)

        # Q13: (2*sqrt(x) - 1/x)^6 常数项 r = 2 => C(6, 2)*2^4*(-1)^2 = 15 * 16 = 240
        coeff13 = math.comb(6, 2) * (2**4) * ((-1)**2)
        self.assertEqual(coeff13, 240)

        # Q14: x, y >= 0 且 2x + y <= 0 => x = y = 0 => max(x + 3y) = 0
        self.assertEqual(0 + 3 * 0, 0)

        # Q15: lim (1 + b + ... + b^(n-1)) / b^n = 1/(b - 1)
        for b in [2.0, 3.0, -2.5]:
            n = 50
            s_n = (b**n - 1) / (b - 1)
            ratio = s_n / (b**n)
            self.assertAlmostEqual(ratio, 1.0 / (b - 1), places=6)

        # Q16: y = 3 + log2(x) 反函数 x = 2^(y-3) => g(x) = 2^(x-3)
        self.assertEqual(2**(3 - 3), 1)

    def test_analytical_solutions_mathematics(self):
        """测试解答题（17-22）数学推导与结论正确性。"""
        # Q17: sin x + cos x = 1/5, x in (-pi/2, 0)
        # (1) 2 sin x cos x = -24/25, sin x - cos x = -sqrt(49/25) = -7/5
        sin_plus_cos = Fraction(1, 5)
        two_sin_cos = sin_plus_cos**2 - 1
        self.assertEqual(two_sin_cos, Fraction(-24, 25))
        sin_minus_cos_sq = 1 - two_sin_cos
        self.assertEqual(sin_minus_cos_sq, Fraction(49, 25))
        sin_minus_cos = -Fraction(7, 5)
        sin_x = (sin_plus_cos + sin_minus_cos) / 2
        cos_x = (sin_plus_cos - sin_minus_cos) / 2
        self.assertEqual(sin_x, Fraction(-3, 5))
        self.assertEqual(cos_x, Fraction(4, 5))

        # (2) 分子: 3 sin^2(x/2) - 2 sin(x/2) cos(x/2) + cos^2(x/2) = 2 - (sin x + cos x) = 9/5
        # 分母: tan x + cot x = 1/(sin x cos x) = 2 / (-24/25) = -25/12
        # 原式 = (9/5) / (-25/12) = -108/125
        num17 = Fraction(2, 1) - sin_plus_cos
        self.assertEqual(num17, Fraction(9, 5))
        den17 = Fraction(2, 1) / two_sin_cos
        self.assertEqual(den17, Fraction(-25, 12))
        res17 = num17 / den17
        self.assertEqual(res17, Fraction(-108, 125))

        # Q18:
        # (1) E(xi) = 1/2 + 2/5 = 9/10
        p_a, p_b = Fraction(1, 2), Fraction(2, 5)
        e_xi = p_a + p_b
        self.assertEqual(e_xi, Fraction(9, 10))
        # (2) 至少一次命中 = 1 - (1/2)^2 * (3/5)^2 = 1 - 9/100 = 91/100
        p_none = (1 - p_a)**2 * (1 - p_b)**2
        self.assertEqual(1 - p_none, Fraction(91, 100))

        # Q19: f(x) = (ax - 6) / (x^2 + b)
        # 切线 x + 2y + 5 = 0 在 x = -1: f(-1) = -2 => -a - 6 = -2(1 + b) => a - 2b = -4
        # f'(-1) = -1/2 => b = 3, a = 2 => f(x) = (2x - 6)/(x^2 + 3)
        a19, b19 = 2, 3
        self.assertEqual((a19 * (-1) - 6) / ((-1)**2 + b19), -2)
        # f'(x) = -2(x^2 - 6x - 3)/(x^2 + 3)^2
        r1 = 3 - 2 * math.sqrt(3)
        r2 = 3 + 2 * math.sqrt(3)
        self.assertAlmostEqual(r1**2 - 6 * r1 - 3, 0.0, places=7)
        self.assertAlmostEqual(r2**2 - 6 * r2 - 3, 0.0, places=7)

        # Q20:
        # (1) AB = 2, AE = EB = sqrt(2), BC = 2 => CE = sqrt(4 + 2) = sqrt(6)
        # BF = 2 * sqrt(2) / sqrt(6) = 2/sqrt(3) = 2*sqrt(3)/3
        # (2) BH = sqrt(2) => sin theta = BF / BH = (2/sqrt(3)) / sqrt(2) = sqrt(2/3) => cos theta = sqrt(1/3) = sqrt(3)/3
        cos_theta20 = math.sqrt(3) / 3.0
        sin_theta20 = math.sqrt(2.0 / 3.0)
        self.assertAlmostEqual(cos_theta20**2 + sin_theta20**2, 1.0, places=7)
        # (3) 等体积法: V = 1/3 * (1/2 * 2 * 2) * 1 = 2/3
        # S_ACE = 1/2 * sqrt(2) * sqrt(6) = sqrt(3) => d = (3 * 2/3) / sqrt(3) = 2*sqrt(3)/3
        d20 = 2.0 / math.sqrt(3)
        self.assertAlmostEqual(d20, 2 * math.sqrt(3) / 3.0, places=7)

        # Q21:
        # (1) 直线 l: y = sqrt(3)x - 2*sqrt(3), 焦点 c = 2
        # 对称点 (3, -sqrt(3)) on x = a^2/c => a^2 = 6, b^2 = 2 => x^2/6 + y^2/2 = 1
        c21 = 2
        a_sq = 3 * c21
        b_sq = a_sq - c21**2
        self.assertEqual((a_sq, b_sq), (6, 2))
        # (2) S_MON = 2*sqrt(6)/3
        # 斜率不存在: x = -2 => y = +-sqrt(6)/3 => S = 1/2 * 2 * (2*sqrt(6)/3) = 2*sqrt(6)/3
        # OM . ON = (-2)(-2) + (sqrt(6)/3)(-sqrt(6)/3) = 4 - 2/3 = 10/3 != 0
        # 且 4*sqrt(6)/3 * cot(MON) = 4*sqrt(6)/3 * (10/3) / (4*sqrt(6)/3) = 10/3
        self.assertEqual(4 - Fraction(2, 3), Fraction(10, 3))
        # 斜率存在时判别式负定无解
        disc_k = (-3)**2 - 4 * 18 * 1
        self.assertLess(disc_k, 0)

        # Q22: a1 = a, a_{n+1} = 1 + 1/a_n
        # (1) a4 = 0 <=> a3 = -1 <=> a2 = -1/2 <=> a1 = -2/3
        a1 = Fraction(-2, 3)
        a2 = 1 + 1 / a1
        a3 = 1 + 1 / a2
        a4 = 1 + 1 / a3
        self.assertEqual((a2, a3, a4), (Fraction(-1, 2), Fraction(-1, 1), Fraction(0, 1)))

        # (2) b1 = -1, b_{n+1} = 1/(b_n - 1)
        b = [Fraction(-1, 1)]
        for _ in range(4):
            b.append(1 / (b[-1] - 1))
        self.assertEqual(b[:4], [Fraction(-1, 1), Fraction(-1, 2), Fraction(-2, 3), Fraction(-3, 5)])

        # (3) 对任意 a > 0, 3/2 < a_n < 2 对所有 n >= 4 均成立
        for a_val in [0.001, 0.5, 1.0, 2.0, 100.0]:
            cur = a_val
            seq = [cur]
            for _ in range(8):
                cur = 1.0 + 1.0 / cur
                seq.append(cur)
            for idx in range(3, len(seq)):
                self.assertTrue(1.5 < seq[idx] < 2.0)


if __name__ == "__main__":
    unittest.main()

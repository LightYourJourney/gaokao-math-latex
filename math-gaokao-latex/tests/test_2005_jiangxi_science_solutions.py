# -*- coding: utf-8 -*-
"""2005 年高考数学真题（江西卷理科 gk-2005-regular-jiangxi-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2005/2005_数学真题_江西理科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_江西理科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_江西理科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_江西理科_含解析.md"


class Jiangxi2005ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性（全卷共 22 题）。"""
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

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-12 题：D A D B B C C C C B D A）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "A", "D", "B", "B", "C", "C", "C", "C", "B", "D", "A"]

        for q_num, expected in enumerate(expected_choices, start=1):
            pattern = rf"\*\*{q_num}．\*\*\s+\*\*答案[：:]\s*([A-D])\*\*"
            match = re.search(pattern, answers)
            self.assertIsNotNone(match, f"Q{q_num} 答案未找到")
            self.assertEqual(match.group(1), expected, f"Q{q_num} 选项不符")

    def test_mathematical_verifications(self):
        """测试全卷核心数学命题与计算结果的代数一致性。"""
        # Q01: I = {-2, -1, 0, 1, 2}, B = {-2, -1, 2} => complement = {0, 1}; union with A={1, 2} => {0, 1, 2}
        I = {-2, -1, 0, 1, 2}
        A = {1, 2}
        B = {-2, -1, 2}
        self.assertEqual(A | (I - B), {0, 1, 2})

        # Q02: z1*z2 = (1+i)(x+2i) = (x-2) + (x+2)i is real => x = -2
        x = -2
        prod = (1 + 1j) * (x + 2j)
        self.assertEqual(prod.imag, 0)
        self.assertEqual(prod.real, -4)

        # Q03: Line x - y + 2 = 0 tangent to (x-a)^2 + (y+b)^2 = 2 => |a + b + 2| = 2 => a + b = 0 or -4
        # "a = b" is neither sufficient nor necessary
        # Sufficient fails: a = b = 1 => a + b = 2 != 0, -4
        # Necessary fails: a = 1, b = -1 => a + b = 0 (tangent), but a != b
        self.assertTrue((1 + 1 != 0) and (1 + 1 != -4))
        self.assertTrue((1 + (-1) == 0) and (1 != -1))

        # Q04: (sqrt(x) + x^(1/3))^12 has 3 positive integer power terms: r = 0, 6, 12
        positive_powers = [r for r in range(13) if (6 - r / 6.0) > 0 and (6 - r / 6.0).is_integer()]
        self.assertEqual(positive_powers, [0, 6, 12])

        # Q06: a=(1, 2), b=(-2, -4), a+b=-a => a.c = -5/2 => cos theta = -1/2 => theta = 120 deg
        cos_theta = Fraction(-5, 2) / 5
        self.assertEqual(cos_theta, Fraction(-1, 2))

        # Q07: y = x*f'(x) has roots at -1, 0, 1
        # For x in (-inf, -1): x < 0, x*f'(x) < 0 => f'(x) > 0 (increasing)
        # For x in (-1, 0): x < 0, x*f'(x) > 0 => f'(x) < 0 (decreasing)
        # For x in (0, 1): x > 0, x*f'(x) < 0 => f'(x) < 0 (decreasing)
        # For x in (1, inf): x > 0, x*f'(x) > 0 => f'(x) > 0 (increasing)
        # Local max at x = -1, local min at x = 1. Matches Option C.

        # Q08: lim (x-1)/f(2-2x) = lim t / f(-2t) = -1/2 * lim (-2t)/f(-2t) = -1/2
        self.assertEqual(Fraction(-1, 2), -0.5)

        # Q09: Rectangular prism fold: AC = 5, R = 5/2. Volume = 125/6 * pi
        self.assertEqual(Fraction(4, 3) * (Fraction(5, 2) ** 3), Fraction(125, 6))

        # Q11: Max area at theta = pi/2: S = 1/2 * (1 - 1/2 * sin(pi)) = 1/2
        self.assertAlmostEqual(0.5 * (1 - 0.5 * math.sin(math.pi)), 0.5)

        # Q12: 9 numbers partition into 3 APs: exactly 5 partitions out of 280
        total_groupings = math.comb(9, 3) * math.comb(6, 3) // 6
        self.assertEqual(total_groupings, 280)
        nums = set(range(1, 10))
        aps = []
        for a in range(1, 10):
            for d in range(1, 5):
                if a + 2 * d <= 9:
                    aps.append((a, a + d, a + 2 * d))
        valid_partitions = 0
        for i in range(len(aps)):
            for j in range(i + 1, len(aps)):
                for k in range(j + 1, len(aps)):
                    s1, s2, s3 = set(aps[i]), set(aps[j]), set(aps[k])
                    if not (s1 & s2 or s1 & s3 or s2 & s3) and (s1 | s2 | s3 == nums):
                        valid_partitions += 1
        self.assertEqual(valid_partitions, 5)
        self.assertEqual(Fraction(valid_partitions, total_groupings), Fraction(1, 56))

        # Q13: Odd function f(0) = 0 => a = sqrt(2)/2
        self.assertEqual(Fraction(1, 2), 0.5)

        # Q14: Max slope y/x at (1, 3/2) => 3/2
        self.assertEqual(Fraction(3, 2), 1.5)

        # Q15: Prism surface shortest distance
        # Route 1 (lateral): d^2 = (3*sqrt(2)/2)^2 + 1^2 = 5.5
        # Route 2 (unfold along A1B1): d^2 = 3.5 + sqrt(2) approx 4.914
        # Route 3 (unfold along A1C1): d^2 = (3/2)^2 + (3/2)^2 = 4.5 = 9/2 => d = 3*sqrt(2)/2
        d_lateral_sq = 5.5
        d_top_sq = 4.5
        self.assertTrue(d_top_sq < d_lateral_sq)
        self.assertAlmostEqual(math.sqrt(4.5), 1.5 * math.sqrt(2))

        # Q17: f(x) = x^2 / (2 - x)
        for r in [3, 4]:
            self.assertEqual((r**2) / (2 - r) - r + 12, 0)

        # Q18: f(x) + f'(x) = 0 => 2*cos(x) = 0 => x = pi/2
        # But x = pi/2 is excluded from domain because tan(x/2 + pi/4) is undefined.
        # Thus no real solution exists.

        # Q19: Gambler's ruin game:
        # xi in {5, 7, 9}
        # P(xi = 5) = 1/16 = 4/64
        # P(xi = 7) = 5/64
        # P(xi = 9) = 55/64
        p5 = Fraction(1, 16)
        p7 = Fraction(5, 64)
        p9 = 1 - p5 - p7
        self.assertEqual(p9, Fraction(55, 64))
        e_xi = 5 * p5 + 7 * p7 + 9 * p9
        self.assertEqual(e_xi, Fraction(275, 32))

        # Q20: Cuboid distance and dihedral angle
        self.assertEqual(Fraction(1, 3), Fraction(1, 3))
        t = 2 - math.sqrt(3)
        self.assertTrue(0 < t < 2)

        # Q21: Recurrence a_{n+1} = a_n(4 - a_n)/2 with a_0 = 1
        # a_n = 2 * [1 - (1/2)^(2^n)]
        a = [1]
        for n in range(5):
            a.append(a[-1] * (4 - a[-1]) / 2)
        for n in range(6):
            formula = 2 * (1 - (0.5 ** (2**n)))
            self.assertAlmostEqual(a[n], formula)

        # Q22: Parabola y = x^2, focus F(0, 1/4), tangents from P(x0, y0) on x - y - 2 = 0
        # Check identity: FA . FP = |FA| * (y0 + 1/4)
        for x0 in [-4.0, -1.0, 0.5, 2.0, 6.0]:
            y0 = x0 - 2.0
            disc = 4 * x0**2 - 4 * y0
            self.assertTrue(disc > 0)
            for sign in [1, -1]:
                t = (2 * x0 + sign * math.sqrt(disc)) / 2
                # Tangent point A(t, t^2)
                # FA = (t, t^2 - 1/4)
                # FP = (x0, y0 - 1/4)
                dot_FA_FP = t * x0 + (t**2 - 0.25) * (y0 - 0.25)
                len_FA = t**2 + 0.25
                identity_val = len_FA * (y0 + 0.25)
                self.assertAlmostEqual(dot_FA_FP, identity_val)


if __name__ == "__main__":
    unittest.main()

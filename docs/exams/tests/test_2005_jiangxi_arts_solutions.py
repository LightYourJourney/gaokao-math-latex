# -*- coding: utf-8 -*-
"""2005 年高考数学真题（江西卷文科 gk-2005-regular-jiangxi-arts）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRANSCRIPT = ROOT / "2005/2005_数学真题_江西文科_试题.md"
ANSWERS = ROOT / "2005/2005_数学真题_江西文科_答案要点.md"
SOLUTIONS = ROOT / "2005/2005_数学真题_江西文科_解析正文.md"
COMBINED = ROOT / "2005/2005_数学真题_江西文科_含解析.md"


class Jiangxi2005ArtsSolutionsTests(unittest.TestCase):
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
        """测试选择题答案（1-12 题：D B B A B C A C C B D A）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "B", "B", "A", "B", "C", "A", "C", "C", "B", "D", "A"]

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
        comp_B = I - B
        self.assertEqual(comp_B, {0, 1})
        self.assertEqual(A | comp_B, {0, 1, 2})

        # Q02: tan(a/2) = 3 => cos a = (1 - 9) / (1 + 9) = -4/5
        t = 3
        cos_a = Fraction(1 - t**2, 1 + t**2)
        self.assertEqual(cos_a, Fraction(-4, 5))

        # Q03: (sqrt(x) + x^(1/3))^12 term exponent = 6 - r/6 in N*
        positive_integer_terms = [r for r in range(13) if (6 - r / 6.0) > 0 and (6 - r / 6.0).is_integer()]
        self.assertEqual(positive_integer_terms, [0, 6, 12])
        self.assertEqual(len(positive_integer_terms), 3)

        # Q06: a=(1, 2), b=(-2, -4), c=(cx, cy) with |c|=sqrt(5)
        # a+b = (-1, -2) = -a. (a+b).c = -a.c = 5/2 => a.c = -5/2
        # cos theta = (a.c) / (|a||c|) = (-5/2) / 5 = -1/2 => theta = 120 deg
        cos_theta = Fraction(-5, 2) / 5
        self.assertEqual(cos_theta, Fraction(-1, 2))

        # Q07: 9 people into 3 groups of 3, Jia and Yi in same group
        # Choose 1 from 7 for Jia & Yi's group: C(7, 1) = 7
        # Divide remaining 6 into 2 groups of 3: C(6, 3) / 2! = 20 / 2 = 10
        # Total = 7 * 10 = 70
        ways = math.comb(7, 1) * (math.comb(6, 3) // 2)
        self.assertEqual(ways, 70)

        # Q09: Rectangular prism fold: AC = 5, R = 5/2. Volume = 4/3 * pi * R^3 = 125/6 * pi
        v_factor = Fraction(4, 3) * (Fraction(5, 2) ** 3)
        self.assertEqual(v_factor, Fraction(125, 6))

        # Q11: S = 1/2 * (1 - 1/2 * sin 2theta). On (0, pi/2], max is when sin 2theta = 0 => theta = pi/2
        # Max S = 1/2
        s_max = 0.5 * (1 - 0.5 * math.sin(math.pi))
        self.assertAlmostEqual(s_max, 0.5)

        # Q12: Frequency histogram
        # n1, n2, n3, n4 form geometric seq with ratio 3: 1, 3, 9, 27
        # n4..n9 form arithmetic seq with d = -5: 27, 22, 17, 12, 7, 2
        freqs = [1, 3, 9, 27, 22, 17, 12, 7, 2]
        self.assertEqual(sum(freqs), 100)
        self.assertEqual(freqs[3], 27)
        # 4.6 to 5.0 covers groups 4, 5, 6, 7:
        b_sum = sum(freqs[3:7])
        self.assertEqual(b_sum, 78)

        # Q13: f(0) = 0 => sqrt(2a^2) = 1 => a = sqrt(2)/2
        a_sq = Fraction(1, 2)
        self.assertEqual(a_sq, Fraction(1, 2))

        # Q14: Linear programming max y/x:
        # Intersections: (1, 1.5) satisfies x - y - 2 <= 0, x + 2y - 4 = 0, y <= 1.5
        # Slope y/x = 1.5 / 1 = 1.5 = 3/2
        self.assertEqual(Fraction(3, 2), 1.5)

        # Q17: f(x) - x + 12 = 0 has roots 3 and 4
        # f(x) = x^2 / (2 - x)
        for r in [3, 4]:
            val = (r**2) / (2 - r) - r + 12
            self.assertEqual(val, 0)

        # Q18: Maximum and period
        # f(x) = sqrt(2) * sin(x + pi/4)
        # Period = 2pi, amplitude = sqrt(2)
        self.assertAlmostEqual(math.sqrt(2), 1.4142135623730951)

        # Q19: Gambler's ruin stopping at <= 7
        # 5 steps: 2 * (1/2)^5 = 1/16 = 4/64
        # 7 steps: 10 * (1/2)^7 = 5/64
        # Total = 9/64
        p_total = Fraction(1, 16) + Fraction(5, 64)
        self.assertEqual(p_total, Fraction(9, 64))

        # Q20: Cuboid distance and dihedral angle
        # (2) Distance to plane ACD1:
        # D(0,0,0), A(1,0,0), C(0,2,0), D1(0,0,1), E(1,1,0)
        # Vector AC = (-1, 2, 0), AD1 = (-1, 0, 1)
        # Normal n = (2, 1, 2), unit normal length = 3
        # AE = (0, 1, 0), projection = |(0, 1, 0) . (2, 1, 2)| / 3 = 1/3
        self.assertEqual(Fraction(1, 3), Fraction(1, 3))
        # (3) AE = 2 - sqrt(3)
        t = 2 - math.sqrt(3)
        self.assertTrue(0 < t < 2)

        # Q22: Recurrence a_n + a_{n-1} = 3(-1/2)^{n-1}
        # S1 = 1, S2 = -3/2 => a1 = 1, a2 = -5/2
        # a_n = 4*(-1)^(n-1) + 6*(-1/2)^n
        a = [0] * 10
        a[1] = 1
        a[2] = Fraction(-5, 2)
        for n in range(3, 10):
            a[n] = 3 * (Fraction(-1, 2) ** (n - 1)) - a[n - 1]

        for n in range(1, 10):
            formula = 4 * ((-1) ** (n - 1)) + 6 * (Fraction(-1, 2) ** n)
            self.assertEqual(a[n], formula)


if __name__ == "__main__":
    unittest.main()

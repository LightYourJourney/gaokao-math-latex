# -*- coding: utf-8 -*-
"""2004 年高考数学真题（重庆卷理科 gk-2004-regular-chongqing-science）自动化测试套件。"""
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_重庆理科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_重庆理科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_重庆理科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_重庆理科_含解析.md"


class Chongqing2004ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        """测试 Markdown 文件的结构完整性、标点与题号连续性。"""
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 160–161 的两页题面", solutions)
        self.assertIn("独立推导复算", solutions)

        for document in (transcript, answers, solutions, combined):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 23)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 23)))

    def test_multiple_choice_answers(self):
        """测试选择题答案（1-12 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "A", "D", "A", "B", "C", "C", "C", "B", "B", "B", "D"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        """测试填空题（13-16 题）与解答题结论（17-22 题）。"""
        answers = ANSWERS.read_text(encoding="utf-8")

        # 填空题
        self.assertIn(r"-2", answers)
        self.assertIn(r"\dfrac{\pi}{4}", answers)
        self.assertIn(r"\dfrac{\pi}{3}", answers)
        self.assertIn(r"[-1, 3]", answers)

        # 解答题
        self.assertIn(r"\pi", answers)
        self.assertIn(r"-2", answers)
        self.assertIn(r"E\xi = \dfrac{525}{256}", answers)
        self.assertIn(r"\dfrac{175}{256}", answers)
        self.assertIn(r"\dfrac{\sqrt{5}}{10}", answers)
        self.assertIn(r"[2, +\infty)", answers)
        self.assertIn(r"x = 2p", answers)
        self.assertIn(r"b_n > b_{n+1}", answers)

    def test_mathematical_derivations(self):
        """独立复算核心数学公式与数值逻辑。"""
        # Q02: Z = 1 + sqrt(2)i => Z^2 - 2Z = (1 + sqrt(2)i)^2 - 2(1 + sqrt(2)i) = -3
        z = complex(1, math.sqrt(2))
        res_q02 = z**2 - 2 * z
        self.assertAlmostEqual(res_q02.real, -3.0)
        self.assertAlmostEqual(res_q02.imag, 0.0)

        # Q06: |a|^2 - 2|a| - 24 = 0 => (|a| - 6)(|a| + 4) = 0 => |a| = 6
        roots_q06 = [x for x in [6, -4] if x > 0]
        self.assertEqual(roots_q06, [6])

        # Q07: ax^2 + 2x + 1 = 0 has opposite signs iff 1/a < 0 <=> a < 0.
        # {a | a < -1} is a strict subset of {a | a < 0}, so it is sufficient and not necessary.
        self.assertTrue(all(a < 0 for a in [-2, -10, -1.01]))

        # Q08: Dihedral 60 deg => angle APB = 120 deg. |AB|^2 = 4^2 + 2^2 - 2*4*2*cos(120) = 28
        ab_sq = 4**2 + 2**2 - 2 * 4 * 2 * math.cos(math.radians(120))
        self.assertAlmostEqual(ab_sq, 28.0)
        self.assertAlmostEqual(math.sqrt(ab_sq), 2 * math.sqrt(7))

        # Q11: 3! * 6! * A(7, 2) / 10! = 1/20
        total_p = math.factorial(10)
        fav_p = math.factorial(3) * math.factorial(6) * (7 * 6)
        self.assertEqual(Fraction(fav_p, total_p), Fraction(1, 20))

        # Q14: intersection of 2 - 1/2 x^2 and 1/4 x^3 - 2 => x = 2
        # k1 = -2, k2 = 3 => tan(theta) = |(3 - (-2)) / (1 - 6)| = 1 => theta = pi/4
        k1 = -2
        k2 = 3
        tan_theta = abs((k2 - k1) / (1 + k1 * k2))
        self.assertEqual(tan_theta, 1)

        # Q15: limit area = pi/2 - (pi/8) / (1 - 1/4) = pi/2 - pi/6 = pi/3
        s_initial = Fraction(1, 2)
        s_cut_sum = Fraction(1, 8) / (1 - Fraction(1, 4))
        self.assertEqual(s_initial - s_cut_sum, Fraction(1, 3))

        # Q16: (0 - sqrt(3))^2 / 4 + (b - 1)^2 / 16 <= 1 => (b - 1)^2 <= 4 => -1 <= b <= 3
        self.assertEqual(3 / 4 + 4 / 16, 1.0)

        # Q18:
        # P(xi=0) = 1/4 = 64/256
        # P(xi=1) = 3/16 = 48/256
        # P(xi=2) = 9/64 = 36/256
        # P(xi=3) = 27/256
        # P(xi=4) = 81/256
        p = [Fraction(64, 256), Fraction(48, 256), Fraction(36, 256), Fraction(27, 256), Fraction(81, 256)]
        self.assertEqual(sum(p), Fraction(1, 1))
        e_xi = sum(i * p[i] for i in range(5))
        self.assertEqual(e_xi, Fraction(525, 256))
        p_le_3 = 1 - p[4]
        self.assertEqual(p_le_3, Fraction(175, 256))

        # Q19: sin(alpha) = 1 / sqrt(20) = sqrt(5) / 10
        self.assertAlmostEqual(1 / math.sqrt(20), math.sqrt(5) / 10)

        # Q20: f(x1) + f(x2) = -2(a+1)/27 * (2a - 1)(a - 2) <= 0 for a > 1 <=> a >= 2
        for a_val in [2.0, 2.5, 3.0, 10.0]:
            val = -2 * (a_val + 1) / 27 * (2 * a_val - 1) * (a_val - 2)
            self.assertLessEqual(val, 0)
        for a_val in [1.1, 1.5, 1.99]:
            val = -2 * (a_val + 1) / 27 * (2 * a_val - 1) * (a_val - 2)
            self.assertGreater(val, 0)

        # Q22: a1 = 2, a_{n+1} = a_n + 1/a_n
        a_seq = [2.0]
        for _ in range(15):
            a_seq.append(a_seq[-1] + 1.0 / a_seq[-1])
        # test a_n > sqrt(2n + 1)
        for n_idx, val in enumerate(a_seq, start=1):
            self.assertGreater(val, math.sqrt(2 * n_idx + 1))
        # test b_n = a_n / sqrt(n) is strictly decreasing
        b_seq = [a_seq[i] / math.sqrt(i + 1) for i in range(len(a_seq))]
        for i in range(len(b_seq) - 1):
            self.assertGreater(b_seq[i], b_seq[i + 1])


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
import cmath
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_湖北理科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_湖北理科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_湖北理科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_湖北理科_含解析.md"


class Hubei2004ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 170–171 的两页题面，不附官方答案", solutions)
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
        answers = ANSWERS.read_text(encoding="utf-8")
        expected_choices = ["D", "A", "C", "B", "B", "D", "B", "C", "C", "A", "D", "A"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        # Fill-in answers (Q13 - Q16)
        self.assertIn("4", answers)
        self.assertIn("240", answers)
        self.assertIn("④", answers)
        self.assertIn("-1.6", answers)

        # Solution key answers (Q17 - Q22)
        self.assertIn(r"\dfrac{5\sqrt{3} - 12}{26}", answers)
        self.assertIn(r"\arccos\left(-\dfrac{1}{3}\right)", answers)
        self.assertIn(r"\theta = 0", answers)
        self.assertIn(r"(-2, -\sqrt{2})", answers)
        self.assertIn(r"-\dfrac{6 + \sqrt{6}}{5}", answers)
        self.assertIn("81", answers)
        self.assertIn(r"\dfrac{a + \sqrt{a^2 + 4}}{2}", answers)
        self.assertIn(r"a \geqslant \dfrac{3}{2}", answers)

        # Content in solutions text
        self.assertIn("2x - y - 1 = 0", solutions)
        self.assertIn("-16", solutions)
        self.assertIn(r"\dfrac{2x}{1 + x^2}", solutions)
        self.assertIn(r"\frac{9}{4}", solutions)
        self.assertIn(r"\frac{1}{2}", solutions)
        self.assertIn("a < 0", solutions)
        self.assertIn(r"P \subsetneqq Q", solutions)
        self.assertIn("$2 + 2 = 4$ 条", solutions)
        self.assertIn(r"12 + 3\sin\frac{\pi}{6}t", solutions)

    def test_mathematical_derivations(self):
        # Q02: Complex value
        z1 = complex(-1, math.sqrt(3))
        z2 = complex(1, math.sqrt(3))
        val = (z1 ** 5) / z2
        self.assertAlmostEqual(val.real, -16.0, places=7)
        self.assertAlmostEqual(val.imag, 0.0, places=7)

        # Q06: Ellipse focal distance
        # a=4, b=3, c=sqrt(7), focal chord y = b^2/a = 9/4 = 2.25
        self.assertEqual(3**2 / 4, 2.25)

        # Q14: Combinatorics
        c10_3 = math.comb(10, 3)
        d3 = 2
        self.assertEqual(c10_3 * d3, 240)

        # Q16: Related rates at t = 0.5
        x = 16 * 0.5
        y = 18 - 24 * 0.5
        s = math.sqrt(x**2 + y**2)
        ds_dt = (x * 16 + y * (-24)) / s
        self.assertAlmostEqual(ds_dt, -1.6, places=7)

        # Q17: Trigonometry
        tan_alpha = -2.0 / 3.0
        sin_2alpha = 2 * tan_alpha / (1 + tan_alpha**2)
        cos_2alpha = (1 - tan_alpha**2) / (1 + tan_alpha**2)
        res = sin_2alpha * 0.5 + cos_2alpha * (math.sqrt(3) / 2.0)
        expected = (5 * math.sqrt(3) - 12) / 26.0
        self.assertAlmostEqual(res, expected, places=7)

        # Q20: Hyperbola circle through right focus
        # 5k^2 + 2*sqrt(6)*k - 6 = 0
        k = (-math.sqrt(6) - 6) / 5.0
        self.assertTrue(-2.0 < k < -math.sqrt(2))

        # Q21: Expected cost comparison
        c_none = 400 * 0.3
        c_beta = 30 + 400 * 0.15
        c_alpha = 45 + 400 * 0.1
        c_both = 45 + 30 + 400 * (0.1 * 0.15)
        self.assertEqual(c_both, 81.0)
        self.assertTrue(c_both < c_alpha < c_beta < c_none)

        # Q22: Sequence recursion for a >= 1.5
        for a in [1.5, 2.0, 3.5]:
            A = (a + math.sqrt(a**2 + 4)) / 2.0
            an = a
            for n in range(1, 15):
                bn = an - A
                self.assertLessEqual(abs(bn), (0.5**n) + 1e-12)
                an = a + 1.0 / an


if __name__ == "__main__":
    unittest.main()

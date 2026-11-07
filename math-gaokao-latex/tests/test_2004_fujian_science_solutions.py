# -*- coding: utf-8 -*-
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_福建理科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_福建理科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_福建理科_解析正文.md"
COMBINED = ROOT / "2004/2004_数学真题_福建理科_含解析.md"


class Fujian2004ScienceSolutionsTests(unittest.TestCase):
    def test_markdown_documents_completeness_and_delimiters(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        combined = COMBINED.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 164–165 的两页题面，不附官方答案", solutions)
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
        expected_choices = ["A", "C", "D", "B", "B", "B", "C", "B", "A", "D", "D", "B"]

        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

    def test_fill_in_and_solution_answers(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        # Fill-in answers (Q13 - Q16)
        self.assertIn(r"4\sqrt{5}", answers)
        self.assertIn(r"\dfrac{1}{2}", answers)
        self.assertIn("①③", answers)
        self.assertIn(r"\dfrac{2}{3}", answers)

        # Solution key answers (Q17 - Q22)
        self.assertIn(r"-\dfrac{\pi}{4}", answers)
        self.assertIn(r"m = -\dfrac{\pi}{12}, n = 1", answers)
        self.assertIn(r"\mathrm{E}\xi = \dfrac{9}{5}", answers)
        self.assertIn(r"\dfrac{44}{45}", answers)
        self.assertIn(r"\arccos\dfrac{1}{3}", answers)
        self.assertIn(r"\dfrac{4\sqrt{2}}{3}", answers)
        self.assertIn(r"A_n = 490n - 10n^2", answers)
        self.assertIn(r"B_n = 500n - 100 - \dfrac{500}{2^n}", answers)
        self.assertIn("4", answers)
        self.assertIn(r"A = \{a \mid -1 \leqslant a \leqslant 1\}", answers)
        self.assertIn(r"m \leqslant -2", answers)
        self.assertIn(r"y = x^2 + \dfrac{1}{2x^2} + 1", answers)
        self.assertIn(r"(2, +\infty)", answers)

        # Analytical derivations inside solutions
        self.assertIn(r"2\sin\left(2x + \frac{\pi}{6}\right) + 1", solutions)
        self.assertIn(r"\vec{a} \cdot \vec{b}", solutions)
        self.assertIn(r"d + |MC| = |MM'| + |MC| \geqslant |CH|", solutions)

    def test_mathematical_verifications(self):
        # Q1: ((1 - i)/(1 + i))^10 = (-i)^10 = -1
        c = (1 - 1j) / (1 + 1j)
        self.assertAlmostEqual(c.imag, -1.0)
        self.assertAlmostEqual((c**10).real, -1.0)

        # Q2: tan 15° + cot 15° = 4
        rad15 = math.radians(15)
        self.assertAlmostEqual(math.tan(rad15) + 1 / math.tan(rad15), 4.0)

        # Q6: 6 classes, 4 students into 2 classes (2 each)
        ways = math.comb(6, 2) * math.comb(4, 2)
        self.assertEqual(ways, 90)
        self.assertEqual(0.5 * (6 * 5) * math.comb(4, 2), 90)

        # Q10: Sphere R=2, distance d=1 -> small circle r = sqrt(3) -> side = sqrt(3)*r = 3
        r_circle = math.sqrt(2**2 - 1**2)
        side = math.sqrt(3) * r_circle
        self.assertAlmostEqual(side, 3.0)

        # Q12: Hyperbola focal-directrix property gives min cost 5a
        # C is at (2 + 2*sin(30°), 2*cos(30°)) = (3, sqrt(3))
        # Directrix is at x = 1/2. Distance = 3 - 0.5 = 2.5.
        # Cost factor = 2a * 2.5 = 5a.
        c_x = 2 + 2 * math.sin(math.radians(30))
        dist_directrix = c_x - 0.5
        min_cost_ratio = 2 * dist_directrix
        self.assertAlmostEqual(min_cost_ratio, 5.0)

        # Q13: Circle (x-3)^2 + (y-1)^2 = 25, line x + 2y = 0
        # d = |3 + 2| / sqrt(5) = sqrt(5)
        # chord = 2 * sqrt(25 - 5) = 4 * sqrt(5)
        d_center = abs(3 + 2 * 1) / math.sqrt(1**2 + 2**2)
        chord = 2 * math.sqrt(25 - d_center**2)
        self.assertAlmostEqual(chord, 4 * math.sqrt(5))

        # Q16: V(x) = (9/4) * (x^2 - x^3), V'(x) = 0 => x = 2/3
        def v(x):
            return 9.0 / 4.0 * (x**2 - x**3)
        self.assertGreater(v(2 / 3), v(2 / 3 - 0.01))
        self.assertGreater(v(2 / 3), v(2 / 3 + 0.01))


if __name__ == "__main__":
    unittest.main()

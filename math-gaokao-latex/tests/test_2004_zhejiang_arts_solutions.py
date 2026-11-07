# -*- coding: utf-8 -*-
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_浙江文科_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_浙江文科_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_浙江文科_解析正文.md"


class Zhejiang2004ArtsSolutionsTests(unittest.TestCase):
    def test_answers_and_solutions_are_complete_and_nonofficial(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        self.assertIn("固定源 PDF 为印刷页码 208–209 的两页题面，不附答案", solutions)
        self.assertIn("独立复算", solutions)

        for document in (transcript, answers, solutions):
            self.assertEqual(document.count("$") % 2, 0)

        choice_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(choice_numbers, list(range(1, 23)))

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))

        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(solution_numbers, list(range(1, 23)))

    def test_key_answers_and_choices(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        # Choice answers: B, A, B, A, A, C, C, B, D, D, D, B
        expected_choices = ["B", "A", "B", "A", "A", "C", "C", "B", "D", "D", "D", "B"]
        choice_table_match = re.search(r"\| 答案 \| ([A-D \|]+) \|", answers)
        self.assertIsNotNone(choice_table_match)
        actual_choices = [c.strip() for c in choice_table_match.group(1).split("|")]
        self.assertEqual(actual_choices, expected_choices)

        # Fill-in answers:
        self.assertIn(r"\left(-\infty, \dfrac{3}{2}\right]", answers)
        self.assertIn("-25", answers)
        self.assertIn(r"\sqrt{5}", answers)
        self.assertIn("5", answers)

        # Solution results:
        self.assertIn(r"a_1 = -\dfrac{1}{2}, a_2 = \dfrac{1}{4}", answers)
        self.assertIn(r"-\dfrac{1}{9}", answers)
        self.assertIn(r"\dfrac{9}{4}", answers)
        self.assertIn(r"60^\circ", answers)
        self.assertIn(r"\dfrac{1}{16807}", answers)
        self.assertIn(r"\dfrac{2041}{2401}", answers)
        self.assertIn(r"f'(x) = 3x^2 - 2ax - 4", answers)
        self.assertIn(r"\dfrac{9}{2}", answers)
        self.assertIn(r"-\dfrac{50}{27}", answers)
        self.assertIn(r"[-2, 2]", answers)
        self.assertIn(r"x^2 - (2\sqrt{2}-1)y^2 = 1", answers)

    def test_q12_fixed_point_contradiction(self):
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"x^2 + \dfrac{1}{5} = 0", solutions)
        self.assertIn("方程无实数解", solutions)

    def test_q19_vector_proof(self):
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"\vec{AM} = (0, 1, 1)", solutions)
        self.assertIn("(-2, 0, 0)", solutions)
        self.assertIn(r"\vec{BF} = (0 - 1, -1 - 0, 1 - 0) = (-1, -1, 1)", solutions)

    def test_q22_hyperbola_derivation(self):
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"x_0 = \sqrt{2} + 2", solutions)
        self.assertIn(r"y_P = (\sqrt{2} + 2) - 1 = \sqrt{2} + 1", solutions)
        self.assertIn(r"\frac{2\sqrt{2} + 1}{7}", solutions)
        self.assertIn(r"2\sqrt{2} - 1", solutions)


if __name__ == "__main__":
    unittest.main()

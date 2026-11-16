"""Checks for the 2019 Shanghai spring source draft and unresolved boundaries."""
import itertools
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
sys.path.insert(0, str(PROJECT / "tools"))
import solution_sources  # noqa: E402

BASE = ROOT / "2019/2019_数学真题_春季上海_"


def read(name):
    return Path(str(BASE) + name + ".md").read_text(encoding="utf-8")


class ShanghaiSpring2019DraftTests(unittest.TestCase):
    def test_three_sources_and_combined_are_aligned(self):
        question, answer, solution, combined = (
            read(name) for name in ("试题", "答案要点", "解析正文", "含解析")
        )
        questions = solution_sources.parse_question_blocks(question)
        self.assertEqual([q.number for q in questions], list(range(1, 21)))
        self.assertEqual([q.subparts for q in questions[-4:]], [
            (1, 2), (1, 2), (1, 2, 3), (1, 2, 3)
        ])
        self.assertEqual(combined, solution_sources.render_combined(question, solution, answer))
        self.assertIn("official_answer: null", combined)
        for n in (9, 11, 16, 19):
            block = next(b for b in solution_sources.parse_question_blocks(combined) if b.number == n)
            self.assertIn("待核", block.body)
        for name in ("q10_curves.tex", "q17_pyramid.tex"):
            self.assertEqual(combined.count(name), 1)

    def test_q9_two_interpretations_are_preserved(self):
        schedules = [(start, others) for start in range(4)
                     for others in itertools.product(range(5), repeat=3)]
        covered = [s for s, others in schedules
                   if set((s, s + 1, *others)) == set(range(5))]
        self.assertEqual((len(schedules), len(covered)), (500, 24))
        q9 = next(b for b in solution_sources.parse_question_blocks(read("答案要点")) if b.number == 9)
        self.assertIn("$24$", q9.body)
        self.assertIn("$500$", q9.body)
        self.assertIn("待核", q9.body)

    def test_q16_and_q19_boundary_examples(self):
        for x in (Fraction(-3), Fraction(-1), Fraction(3), Fraction(5)):
            y = 2 - x
            a, b = 1 / x, 1 / y
            self.assertLess(a, Fraction(1, 2))
            self.assertLess(b, Fraction(1, 2))
            self.assertEqual((1 - 2 * a) * (1 - 2 * b), 1)
        h = lambda t: 1 + math.sqrt(4 + t * t) / 2
        self.assertLess(2 * h(0), 2 * h(2))
        self.assertGreater(2 * h(2), 2 * h(0))

    def test_q20_period_witnesses(self):
        cases = ((0, 2 * math.pi / 3, 3), (0, math.pi / 2, 4),
                 (math.pi / 2, 2 * math.pi / 5, 5), (0, 2 * math.pi / 3, 6))
        for first, step, period in cases:
            with self.subTest(period=period):
                vals = [math.sin(first + n * step) for n in range(2 * period)]
                self.assertEqual(len({round(v, 9) for v in vals}), 3)
                for n in range(period):
                    self.assertAlmostEqual(vals[n], vals[n + period])


if __name__ == "__main__":
    unittest.main()

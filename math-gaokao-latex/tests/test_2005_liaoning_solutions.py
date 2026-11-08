# -*- coding: utf-8 -*-
"""2005 年高考数学（辽宁卷 gk-2005-regular-liaoning）自动化测试套件。"""
import math
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "2005"
TRANSCRIPT = D / "2005_数学真题_辽宁_试题.md"
ANSWERS = D / "2005_数学真题_辽宁_答案要点.md"
SOLUTIONS = D / "2005_数学真题_辽宁_解析正文.md"
COMBINED = D / "2005_数学真题_辽宁_含解析.md"
SHORT = ROOT / "math-gaokao-latex/2005_辽宁卷/answers_short.tex"


class Liaoning2005Tests(unittest.TestCase):
    def test_structure_and_delimiters(self):
        docs = [p.read_text(encoding="utf-8") for p in (TRANSCRIPT, ANSWERS, SOLUTIONS, COMBINED)]
        for doc in docs:
            self.assertEqual(doc.count("$") % 2, 0)
        self.assertEqual([int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", docs[0], re.M)], list(range(1, 23)))
        self.assertEqual([int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", docs[1], re.M)], list(range(1, 23)))
        self.assertEqual([int(n) for n in re.findall(r"^### 第 (\d+) 题$", docs[2], re.M)], list(range(1, 23)))

    def test_choice_answers_match_key(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        table = re.search(r"\| 答案 \|(.+)\|\n", answers).group(1)
        letters = [c for c in table if c in "ABCD"]
        self.assertEqual(letters, list("BBDDCCCBAAB" + "A"))
        short = SHORT.read_text(encoding="utf-8")
        row = re.search(r"题号 & 1 &.*?\\\\\n\\midrule\n(.+?)\\\\", short, re.S)
        self.assertIsNotNone(row)

    def test_q09_translation_parameter(self):
        # |c-3|/sqrt(5) = sqrt(5)
        self.assertEqual(sorted([3 + 5, 3 - 5]), [-2, 8])

    def test_q11_hyperbola_intersection(self):
        a, c = math.sqrt(3), 3.0
        b2 = c * c - a * a
        self.assertAlmostEqual(b2, 6.0)
        x = 3.0
        self.assertAlmostEqual(x * x / 3 - 4 * x / 6, 1.0)
        self.assertAlmostEqual(math.hypot(x, math.sqrt(4 * x)), math.sqrt(21))

    def test_q14_section_plane_distance(self):
        d = 1 / math.sqrt(1 + 1 + 0.25)
        self.assertAlmostEqual(d, 2 / 3)

    def test_q15_adjacent_permutations(self):
        self.assertEqual(math.factorial(5) * 2**3 - math.factorial(4) * 2**4, 576)

    def test_q16_omega_range(self):
        lo = math.pi / 1.0  # pi/omega >= 1/2 且 pi/omega < 1
        hi = math.pi / 0.5
        self.assertTrue(math.isclose(hi, 2 * math.pi) and math.isclose(lo, math.pi))

    def test_q17_circumradius(self):
        s2 = 8.0
        r2 = 3 * s2 / 8
        self.assertAlmostEqual(4 * math.pi * r2, 12 * math.pi)

    def test_q18_cross_area_max(self):
        best = max((math.sin(2 * t) - math.sin(t) ** 2, t) for t in
                   [0.001 * k for k in range(1, 785)])
        self.assertAlmostEqual(best[0], (math.sqrt(5) - 1) / 2, places=5)
        self.assertAlmostEqual(math.tan(best[1]), (math.sqrt(5) - 1) / 2, places=2)

    def test_q19_geometric_bound(self):
        r = (math.sqrt(3) - 1) / 2
        self.assertAlmostEqual((math.sqrt(3) - 1) / (1 - r), 2 * math.sqrt(3) / 3)

    def test_q20_expectations_and_lp(self):
        self.assertAlmostEqual(5 * 0.68 + 2.5 * 0.32, 4.2)
        self.assertAlmostEqual(2.5 * 0.6 + 1.5 * 0.4, 2.1)
        best = max(4.2 * x + 2.1 * y for x in range(6) for y in range(7)
                   if 8 * x + 2 * y <= 40 and 8 * x + 10 * y <= 60)
        self.assertAlmostEqual(best, 21.0)

    def test_q21_locus_and_tangent(self):
        a, c = 4.0, 3.0
        b2 = a * a - c * c
        self.assertLessEqual(b2, a * c)
        y = abs(b2 / c)
        self.assertLessEqual(y, a)
        dot = a * a - c * c
        self.assertAlmostEqual(2 * c * y / dot, 2.0)

    def test_q22_range_endpoints(self):
        lo = (2 - math.sqrt(2)) / 4
        hi = (2 + math.sqrt(2)) / 4
        self.assertAlmostEqual(1 / (2 * (2 + math.sqrt(2))), lo)
        self.assertAlmostEqual(1 / (2 * (2 - math.sqrt(2))), hi)


if __name__ == "__main__":
    unittest.main()

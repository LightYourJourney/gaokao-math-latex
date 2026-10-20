"""Guards the independent first-pass solutions for 1999 Shanghai science Q1-Q16."""
import json
import math
import re
import unittest
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "math-gaokao-latex/1999_上海卷_理科"
SOLUTIONS = PAPER / "解析草稿.md"
SOURCE_RECORD = PAPER / "来源校对.json"

EXPECTED = {
    1: r"\boxed{2-\sqrt3}",
    2: r"\boxed{[3,+\infty)}",
    3: r"\boxed{40}",
    4: r"\boxed{2\sqrt3\text{或}\sqrt3}",
    5: r"\boxed{(2,2)}",
    6: r"\boxed{\pi}",
    7: r"\boxed{[-5\pi/6,-\pi/3]}",
    8: r"\boxed{\{\sqrt2/2,3\sqrt2/2\}}",
    9: r"\boxed{(\sqrt{10},0),(\sqrt{10},\pi)}",
    10: r"\boxed{9}",
    11: r"\boxed{8/36=2/9}",
    12: r"\boxed{\sqrt{11}/12}",
    13: r"\boxed{\text{C}}",
    14: r"\boxed{\text{D}}",
    15: r"\boxed{\text{B}}",
    16: r"\boxed{\text{C}}",
}


class Shanghai1999ScienceIndependentSolutionsTests(unittest.TestCase):
    def test_independent_solution_draft_covers_q1_to_q16_with_checked_conclusions(self):
        self.assertTrue(SOLUTIONS.is_file(), "independent solution draft for Q1-Q16 is missing")
        text = SOLUTIONS.read_text(encoding="utf-8")
        numbers = [int(n) for n in re.findall(r"^### 第(\d+)题", text, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 17)))
        for number, conclusion in EXPECTED.items():
            with self.subTest(question=number):
                self.assertIn(conclusion, text)
        self.assertIn("独立推导草稿", text)
        self.assertIn("还没有第二位复核者复算", text)

    def test_machine_state_does_not_promote_draft_to_verified_solution(self):
        record = json.loads(SOURCE_RECORD.read_text(encoding="utf-8"))
        self.assertEqual(record["generated_solution_status"], "independent-draft-pending-review")
        self.assertEqual(record["review_status"], "pending")
        self.assertIsNone(record["official_answer"])

    def test_exact_counting_and_geometry_examples_match_the_written_proofs(self):
        self.assertEqual(comb(5, 2) * 2**2, 40)
        favorable = sum(m * m + n * n < 16 for m in range(1, 7) for n in range(1, 7))
        self.assertEqual(favorable, 8)
        self.assertEqual(favorable / 36, 2 / 9)
        base_area = math.sqrt(3) / 4
        height = math.sqrt(11 / 3)
        self.assertTrue(math.isclose(base_area * height / 3, math.sqrt(11) / 12, rel_tol=1e-14))


if __name__ == "__main__":
    unittest.main()

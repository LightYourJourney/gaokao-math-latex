"""Checks that 1993 science-paper derivations stay source-bound and non-official."""
import hashlib
import json
import re
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1993_旧科目组_理科"
SOURCE = PAPER / "题面转录草稿.md"
SOLUTIONS = PAPER / "解答草稿.md"
RECORD = PAPER / "来源校对.json"


class OldTrackScience1993MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.text = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.headings = [
            int(number)
            for number in re.findall(r"^\*\*(\d+)．\*\*", cls.text, flags=re.MULTILINE)
        ]
        cls.outcomes = {
            int(number): (kind, conclusion.strip().strip("$").rstrip("。"))
            for number, kind, conclusion in re.findall(
                r"^\*\*(\d+)．\*\*\s+\*\*(答案|待核|结论)：(.*?)\*\*",
                cls.text,
                flags=re.MULTILINE,
            )
        }

    def test_all_numbered_items_have_a_solution_or_explicit_pending_status(self):
        self.assertTrue(SOLUTIONS.is_file(), "solution draft is missing")
        self.assertEqual(self.headings, list(range(1, 30)))
        self.assertEqual(set(self.outcomes), set(range(1, 30)))
        self.assertEqual(
            [n for n, (kind, _) in self.outcomes.items() if kind == "待核"],
            [8, 16, 28],
        )

    def test_generated_solution_is_bound_to_this_question_version_and_not_official(self):
        generated = self.record["generated_solution"]
        self.assertEqual(generated["path"], "解答草稿.md")
        self.assertEqual(generated["question_draft_sha256"], self.record["draft_sha256"])
        self.assertEqual(generated["question_draft_sha256"], hashlib.sha256(SOURCE.read_bytes()).hexdigest())
        self.assertEqual(generated["sha256"], hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest())
        self.assertEqual(generated["status"], "pending-independent-review")
        self.assertEqual(generated["unresolved_question_numbers"], [8, 16, 28])
        self.assertEqual(generated["question_numbers"], [n for n in range(1, 30) if n not in (8, 16, 28)])
        self.assertEqual(generated["choice_key"], ["C", "B", "C", "D", "C", "B", "B", None, "A", "D", "A", "C", "D", "A", "B", None, "B", "B"])
        self.assertFalse(generated["official"])
        self.assertIsNone(self.record["official_answer"])

    def test_hand_derived_answer_anchors_and_originally_unresolved_items(self):
        expected = {
            1: ("答案", "C"), 2: ("答案", "B"), 3: ("答案", "C"),
            4: ("答案", "D"), 5: ("答案", "C"), 6: ("答案", "B"),
            7: ("答案", "B"), 9: ("答案", "A"), 10: ("答案", "D"),
            11: ("答案", "A"), 12: ("答案", "C"), 13: ("答案", "D"),
            14: ("答案", "A"), 15: ("答案", "B"), 17: ("答案", "B"),
            18: ("答案", "B"), 19: ("答案", "2"), 20: ("答案", "17.3"),
            21: ("答案", "4186"), 22: ("答案", "1760"), 23: ("答案", r"\{1\}"),
            24: ("答案", r"\dfrac{1}{a_1d}"),
            25: ("答案", r"(0,1)\cup(4,5)"),
            26: ("答案", r"l\parallel A_1C_1；\dfrac{13}{5}"),
            27: ("答案", r"\dfrac{x^2}{15/4}+\dfrac{y^2}{3}=1"),
            29: ("结论", "两项等价关系均成立"),
        }
        for number, answer in expected.items():
            with self.subTest(question=number):
                self.assertEqual(self.outcomes[number], answer)
        for number in (8, 16, 28):
            self.assertEqual(self.outcomes[number][0], "待核")
        self.assertIn(r"\dfrac{13}{5}", self.text)

    def test_high_risk_derivations_include_domain_geometry_and_equivalence_checks(self):
        required_fragments = (
            "x=\\pi/4+k\\pi/2", "没有最小值", "f(0)=0", "f(0)=1",
            "没有一个选项成立", "\\cos^2 25^\\circ", "4\\sqrt3",
            "不等号严格", "13/5", "MN=2R\\sin P=\\sqrt3", "arg\\omega",
            "p(2)", "p(-2)",
        )
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_exact_combinatorial_counts_and_geometry(self):
        self.assertEqual(len(list(range(4, 101, 6))), 17)
        self.assertEqual(4 * 1035 + 46, 4186)

        # Q26: squared point-to-line distance, avoiding floating-point rounding.
        point, direction = (F(4), F(0), F(1)), (F(4), F(-3), F(0))
        dot = sum(x * y for x, y in zip(point, direction))
        norm2 = sum(x * x for x in direction)
        distance2 = sum(x * x for x in point) - dot * dot / norm2
        self.assertEqual(distance2, F(169, 25))

        # Q27: exact circumradius consequences for the ellipse's focal data.
        radius2 = F(25, 12)
        focal_distance2 = 4 * radius2 * F(3, 5) ** 2
        focal_sum2 = 36 * radius2 / 5
        self.assertEqual(focal_distance2, 3)
        self.assertEqual(focal_sum2, 15)
        self.assertEqual(focal_sum2 / 4 - focal_distance2 / 4, 3)

    def test_telescoping_limit_and_logarithmic_solution_boundaries(self):
        a1, d, n = F(2), F(3), 7
        partial = sum(
            (F(1, 1) / ((a1 + i * d) * (a1 + (i + 1) * d)) for i in range(n)),
            F(0),
        )
        self.assertEqual(partial, (1 / a1 - 1 / (a1 + n * d)) / d)
        self.assertEqual((1 * (5 - 1), 4 * (5 - 4)), (4, 4))
        self.assertLess(F(1, 2) * (5 - F(1, 2)), 4)
        self.assertLess(F(9, 2) * (5 - F(9, 2)), 4)


if __name__ == "__main__":
    unittest.main()

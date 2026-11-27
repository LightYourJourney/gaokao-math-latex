"""Independent-review regressions for the 1995 Shanghai science paper."""
import hashlib
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1995_上海卷_理工农医类"
QUESTIONS = PAPER / "题面转录草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
SOLUTIONS = PAPER / "解析草稿.md"
RECORD = PAPER / "来源校对.json"


class ShanghaiScience1995MathReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.questions = QUESTIONS.read_text(encoding="utf-8")
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")

    def test_independent_review_is_bound_to_all_30_question_variants(self):
        review = self.record.get("independent_math_review", {})
        self.assertEqual(review.get("status"), "reviewed-with-open-issues")
        self.assertEqual(review.get("question_draft_sha256"), hashlib.sha256(QUESTIONS.read_bytes()).hexdigest())
        self.assertEqual(review.get("question_count"), 25)
        self.assertEqual(review.get("prompt_variant_count"), 30)
        self.assertEqual(review.get("open_question_numbers"), [6, 21])
        self.assertEqual(review.get("confirmed_source_answer_corrections"), [24])

    def test_q6_source_answer_is_preserved_but_schematic_is_not_treated_as_unique_proof(self):
        self.assertIn("**答案：A。**", self.answers)
        self.assertIn("A、B", self.solutions)
        self.assertIn("待核", self.solutions)
        issue = next(
            issue for issue in self.record["source_issues"]
            if issue.get("question_number") == 6
        )
        self.assertEqual(issue["type"], "schematic-option-ambiguity")
        self.assertEqual(issue["status"], "awaiting-source-image")

    def test_q21_b2_mirror_changes_od_sign_but_not_the_requested_cosine(self):
        self.assertIn("关于 $xy$ 平面对称", self.solutions)
        self.assertIn(r"-\frac{\sqrt{10}}5", self.solutions)

        root3 = math.sqrt(3) / 2
        expected = -math.sqrt(10) / 5
        bc = (0.0, 2.0, 0.0)
        for z_sign in (-1.0, 1.0):
            ad = (-root3, -1.0, z_sign * root3)
            dot = sum(a * b for a, b in zip(ad, bc))
            norm_ad = math.sqrt(sum(value * value for value in ad))
            cosine = dot / (norm_ad * 2.0)
            self.assertAlmostEqual(cosine, expected)

    def test_q24_preserves_source_omission_and_records_confirmed_correct_range(self):
        self.assertIn(r"\dfrac mn\in(2-\sqrt3,1)\cup(1,+\infty)", self.answers)
        self.assertIn("独立盲核已再次确认此结论", self.answers)
        self.assertIn(r"m/n\in(2-\sqrt3,+\infty)", self.solutions)
        self.assertIn("n=m", self.solutions)
        self.assertIn("m/n=1", self.solutions)

        lower = 2 - math.sqrt(3)
        self.assertAlmostEqual(4 * lower / (lower * lower + 1), 1.0)
        self.assertGreater(2.0, 1.0)  # at m=n, u=2mn>mn
        issue = next(issue for issue in self.record["source_issues"] if issue["question_number"] == 24)
        self.assertEqual(issue["type"], "source-answer-boundary-omission")
        self.assertEqual(
            issue["independent_review"]["status"],
            "mathematical-omission-independently-confirmed",
        )


if __name__ == "__main__":
    unittest.main()

import hashlib
import json
import math
import re
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1998_全国卷_文科"
QUESTION = PAPER / "题面转录草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
SOLUTIONS = PAPER / "解析草稿.md"
RECORD = PAPER / "来源校对.json"
PROGRESS = ROOT / "PROGRESS.md"


class NationalArts1998MathDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.question = QUESTION.read_text(encoding="utf-8") if QUESTION.is_file() else ""
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.progress = PROGRESS.read_text(encoding="utf-8") if PROGRESS.is_file() else ""

    def test_answer_and_solution_drafts_are_registered_by_content_hash(self):
        self.assertTrue(ANSWERS.is_file())
        self.assertTrue(SOLUTIONS.is_file())
        artifacts = self.record.get("artifacts", {})
        for key, path in (("answer_draft", ANSWERS), ("solution_draft", SOLUTIONS)):
            with self.subTest(artifact=key):
                self.assertEqual(artifacts[key]["path"], path.name)
                self.assertEqual(artifacts[key]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertTrue(artifacts["answer_draft_generated"])
        self.assertTrue(artifacts["solution_draft_generated"])

    def test_every_question_has_a_result_and_no_generated_answer_is_called_official(self):
        rows = re.findall(r"^\|\s*(\d{1,2})\s*\|\s*([^|]+)\|", self.answers, re.MULTILINE)
        by_number = {int(number): value.strip() for number, value in rows}
        self.assertEqual(sorted(by_number), list(range(1, 26)))
        self.assertEqual(by_number[1], "D")
        self.assertEqual(by_number[2], "D")
        self.assertEqual(by_number[3], "C")
        self.assertEqual(by_number[4], "A")
        self.assertEqual(by_number[5], "B")
        self.assertEqual(by_number[6], "B")
        self.assertEqual(by_number[7], "C")
        self.assertEqual(by_number[8], "D")
        self.assertEqual(by_number[9], "A")
        self.assertEqual(by_number[10], "B")
        self.assertEqual(by_number[11], "B")
        self.assertIn("不选字母", by_number[12])
        self.assertIn("不选字母", by_number[13])
        self.assertEqual(by_number[14], "B")
        self.assertEqual(by_number[15], "D")
        nonchoice_answers = " ".join(by_number[number] for number in range(16, 25))
        for phrase in ("16/3", "-5120", r"AC\perp BD", r"②、③", r"[0,1]", r"\sqrt{39}/8", r"y^2=8x-16", r"45^\circ", r"60^\circ", r"2\sqrt6/3", "a=6", "b=3"):
            self.assertIn(phrase, nonchoice_answers, f"missing answer evidence: {phrase}")
        self.assertIn("按固定来源公式字面", by_number[25])
        self.assertEqual(self.record["official_answer"], None)
        self.assertEqual(self.record["answer_attribution"], "none-found-in-fixed-source-pdf")
        self.assertEqual(self.record["generated_answer_attribution"], "agent-derived-unverified-not-official")
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")

    def test_solutions_keep_all_three_fixed_source_ambiguities_open(self):
        headings = [int(number) for number in re.findall(r"^## 第\s*(\d+)\s*题", self.solutions, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 26)), "solution draft must cover all questions in order")
        self.assertIn("不根据另一扫描件改动固定来源题文", self.solutions)
        self.assertIn("base 10", self.solutions)
        self.assertIn("未经过异人盲核", self.solutions)
        observations = "\n".join(self.record.get("source_observations", []))
        self.assertIn("新浪旧扫描", observations)
        self.assertIn("145", observations)
        self.assertIn("100", observations)

    def test_key_exact_arithmetic_checks(self):
        # These are regression checks for the written derivations, not substitutes for their proofs.
        self.assertEqual(Fraction(145 - 10, 45), 3)
        self.assertEqual(Fraction(2, 3) ** 2, Fraction(4, 9))
        self.assertEqual(Fraction(144, 9) + Fraction(112, 9), Fraction(256, 9))
        self.assertEqual(Fraction(144, 9) + Fraction(112, 9), Fraction(256, 9))
        self.assertAlmostEqual(math.sqrt(39) / 8, 0.7806247497997998)

    def test_quadratic_trigonometric_and_geometric_consequences(self):
        # Q12 midpoint ordinate and Q13 small-circle/sphere radii.
        self.assertAlmostEqual(math.sqrt(3) / 4, 0.4330127018922193)
        self.assertAlmostEqual((2 * math.pi * 2) / (2 * math.pi / math.sqrt(3)), 2 * math.sqrt(3))
        # Q14: sin(alpha) = cos(alpha)^2 gives the positive root of t^2+t-1=0.
        t = (math.sqrt(5) - 1) / 2
        self.assertAlmostEqual(t * t + t - 1, 0.0, places=14)
        # Q15: S_infinity = a1/(1+1/2) = 1/a1.
        self.assertAlmostEqual(2 * (math.sqrt(6) / 2) ** 2 / 3, 1.0)

    def test_q20_q22_q23_and_q24_constraints(self):
        # Q20 factorization (a-b)^2*x*(1-x), tested at exact rational samples.
        for a, b, x in ((Fraction(2), Fraction(1), Fraction(1, 3)), (Fraction(-1), Fraction(3), Fraction(1)), (Fraction(5), Fraction(2), Fraction(0))):
            lhs_minus_rhs = a * a * x + b * b * (1 - x) - (a * x + b * (1 - x)) ** 2
            self.assertEqual(lhs_minus_rhs, (a - b) ** 2 * x * (1 - x))
        # Q22: A=(3,2sqrt2), B=(6,4sqrt2), focus N=(4,0), directrix x=0.
        self.assertAlmostEqual(3**2 + (2 * math.sqrt(2)) ** 2, 17)
        self.assertAlmostEqual((3 - 4) ** 2 + (2 * math.sqrt(2)) ** 2, 9)
        self.assertAlmostEqual((6 - 4) ** 2 + (4 * math.sqrt(2)) ** 2, 36)
        # Q23: the selected coordinate construction meets the printed right-triangle lengths.
        self.assertAlmostEqual((2 / math.sqrt(3)) ** 2 + (2 * math.sqrt(6) / 3) ** 2, 4)
        self.assertAlmostEqual((4 / math.sqrt(3)) ** 2 + (2 * math.sqrt(6) / 3) ** 2, 8)
        # Q24: material constraint and stationary maximum of ab at (a,b)=(6,3).
        self.assertEqual(2 * 6 + 2 * 6 * 3 + 4 * 3, 60)
        self.assertEqual(30 - 6 - 2 * 3, 18)

    def test_q25_termwise_bound_and_progress_receipt(self):
        for k in range(2, 40):
            lhs = Fraction(3 * k - 1, 3 * k - 2) ** 2
            rhs = Fraction(3 * k - 1, 3 * k - 4)
            self.assertLess(lhs, rhs)
        self.assertIn("1998 全国卷文科：非官方答案与解析草稿完成", self.progress, "progress receipt is missing")
        self.assertIn("test_1998_national_arts_math.py", self.progress, "progress receipt omits the test suite")
        self.assertIn("Q25", self.progress, "progress receipt omits unresolved source issue")


if __name__ == "__main__":
    unittest.main()

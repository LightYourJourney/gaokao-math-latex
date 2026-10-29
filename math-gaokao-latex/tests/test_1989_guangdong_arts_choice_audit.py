import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
AUDIT = ROOT / "1989/1989_数学真题_广东文_选择题独立核算草稿.md"
ANSWERS = ROOT / "1989/1989_数学真题_广东文_答案要点草稿.md"
RECORD = PROJECT / "1989_广东卷_文科/来源校对.json"
PROGRESS = PROJECT / "PROGRESS.md"
EXPECTED_DERIVED = (
    "A", "C", "D", "C", "A", "B", "D", "D", "B", "A", "B", "B", "A",
    "B", "C", "D", "A", "D", "C", "B", "-", "B", "D", "B", "B",
)


class GuangdongArtsChoiceAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = AUDIT.read_text(encoding="utf-8") if AUDIT.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.progress = PROGRESS.read_text(encoding="utf-8")

    def test_independent_candidates_cover_choices_and_isolate_q9_q21_source_problems(self):
        derived_rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([ABCD-])\s*\|", self.audit, re.MULTILINE)
        source_rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([ABCD])\s*\|", self.answers, re.MULTILINE)

        self.assertEqual([int(n) for n, _ in derived_rows], list(range(1, 26)))
        derived = tuple(answer for _, answer in derived_rows)
        source = tuple(answer for _, answer in source_rows)
        self.assertEqual(derived, EXPECTED_DERIVED)
        self.assertEqual([n for n, (left, right) in enumerate(zip(derived, source), 1) if left != right], [9, 21])

        q9 = next(item for item in self.record["source_discrepancies"] if item["question_number"] == 9)
        self.assertEqual((derived[8], source[8]), ("B", "C"))
        self.assertEqual(q9["status"], "unresolved-source-conflict")
        q21 = next(item for item in self.record["source_discrepancies"] if item["question_number"] == 21)
        self.assertEqual(q21["printed_option_a"], "a≤3")
        self.assertEqual(q21["stem_derived_range"], "a≤−3")
        self.assertEqual(q21["printed_answer"], "A")
        self.assertEqual(q21["status"], "unresolved-source-defect")

    def test_choice_audit_is_provenanced_and_keeps_source_conditions(self):
        self.assertTrue(AUDIT.is_file(), "choice audit draft is missing")
        artifact = self.record.get("artifacts", {}).get("independent_choice_audit", {})
        self.assertEqual(artifact.get("path"), str(AUDIT.relative_to(ROOT)))
        self.assertEqual(artifact.get("sha256"), hashlib.sha256(AUDIT.read_bytes()).hexdigest())
        self.assertEqual(artifact.get("questions"), list(range(1, 26)))
        self.assertEqual(artifact.get("attribution"), "agent-derived-unverified-not-official")
        self.assertEqual(self.record.get("mathematical_verification_status"), "conditionally-reviewed-with-source-conditions")
        self.assertEqual(self.record.get("verification", {}).get("independent_math_review", {}).get("status"), "conditional-pass")
        self.assertTrue(
            "1989 广东卷文科：第一卷选择题独立核算" in self.progress,
            "missing progress receipt for the choice audit",
        )


if __name__ == "__main__":
    unittest.main()

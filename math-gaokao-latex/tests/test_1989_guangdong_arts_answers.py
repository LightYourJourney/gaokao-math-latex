import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
PAPER = PROJECT / "1989_广东卷_文科"
ANSWERS = ROOT / "1989/1989_数学真题_广东文_答案要点草稿.md"
SOLUTIONS = ROOT / "1989/1989_数学真题_广东文_解析草稿.md"
RECORD = PAPER / "来源校对.json"
PROGRESS = PROJECT / "PROGRESS.md"
SOURCE_ID = "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766"
EXPECTED_KEY = [
    "A", "C", "D", "C", "A", "B", "D", "D", "C", "A", "B", "B", "A",
    "B", "C", "D", "A", "D", "C", "B", "A", "B", "D", "B", "B",
]


class GuangdongArtsAnswerSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.progress = PROGRESS.read_text(encoding="utf-8") if PROGRESS.is_file() else ""

    def test_transcribed_choice_key_matches_all_25_source_cells(self):
        rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([ABCD])\s*\|", self.answers, re.MULTILINE)
        self.assertEqual([int(number) for number, _ in rows], list(range(1, 26)))
        self.assertEqual([answer for _, answer in rows], EXPECTED_KEY)

    def test_second_volume_answers_and_source_gaps_are_explicit(self):
        for fragment in (
            "一（1）", r"\(-1\)", r"\dfrac{1-x}{3x}", r"3x+\sqrt3\,y=12",
            r"\dfrac12", "23", r"x=-\dfrac12", r"SC=5\text{ cm}",
            r"-1-i", r"\sqrt2\left(\cos\dfrac{5\pi}{4}+i\sin\dfrac{5\pi}{4}\right)",
            "四（2）", "未见最终结论", "第五题", "未见答案或解析",
        ):
            self.assertTrue(
                fragment in self.answers + self.solutions,
                f"missing expected source text: {fragment}",
            )
        self.assertNotIn(r"(-1,-\dfrac12]", self.answers)
        self.assertNotIn(r"\theta=0,\pi", self.answers)

    def test_source_provenance_does_not_claim_official_or_verified_answers(self):
        self.assertEqual(self.record.get("source_id"), SOURCE_ID)
        self.assertEqual(self.record.get("official_answer"), None)
        self.assertEqual(self.record.get("source", {}).get("source_authenticity"), "unverified")
        self.assertEqual(self.record.get("review_status"), "needs-review")
        self.assertEqual(self.record.get("mathematical_verification_status"), "not-verified")
        self.assertTrue("固定 PDF 印载" in self.answers, "missing source attribution label")
        self.assertTrue("出版者身份未核" in self.answers, "missing source identity caveat")

    def test_answer_solution_and_question_sources_are_hash_registered(self):
        artifacts = self.record.get("artifacts", {})
        expected = {
            "question_draft": ROOT / "1989/1989_数学真题_广东文_试题.md",
            "answer_draft": ANSWERS,
            "solution_draft": SOLUTIONS,
        }
        for name, path in expected.items():
            with self.subTest(artifact=name):
                self.assertTrue(path.is_file())
                self.assertEqual(artifacts[name]["path"], str(path.relative_to(ROOT)))
                self.assertEqual(artifacts[name]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        for figure in self.record.get("artifacts", {}).get("figures", []):
            with self.subTest(figure=figure["path"]):
                path = ROOT / figure["path"]
                self.assertTrue(path.is_file())
                self.assertEqual(figure["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
        solution_links = re.findall(r"\]\(([^)]+\.tex)\)", self.solutions)
        self.assertEqual(len(solution_links), 1)
        self.assertTrue((SOLUTIONS.parent / solution_links[0]).resolve().is_file())
        self.assertTrue(
            "1989 广东卷文科：固定扫描答案与解析转录" in self.progress,
            "missing progress receipt",
        )
        self.assertTrue(
            "test_1989_guangdong_arts_answers.py" in self.progress,
            "progress omits the focused test",
        )


if __name__ == "__main__":
    unittest.main()

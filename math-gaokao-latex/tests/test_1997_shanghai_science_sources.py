"""Source-bound transcription checks for the 1997 Shanghai science paper."""

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1997_上海卷_理科"
QUESTION = PAPER / "题面转录草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
SOLUTIONS = PAPER / "解析草稿.md"
SOURCE = PAPER / "来源校对.json"
SOURCE_SHA256 = "8bdb6c445fd984ff6e06d4fd9848af80c33f7de177e8aebcab51d4dad1b827e9"
SOURCE_BLOB = "aedb00f81b60d133034602250130d9079b440761"


class ShanghaiScienceTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.question = QUESTION.read_text(encoding="utf-8")
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")
        cls.record = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_source_and_exam_identity_are_bound_and_unverified(self):
        self.assertEqual(self.record["source"]["pdf_sha256"], SOURCE_SHA256)
        self.assertEqual(self.record["pdf_sha256"], SOURCE_SHA256)
        self.assertEqual(self.record["git_blob_oid"], SOURCE_BLOB)
        self.assertEqual(self.record["source"]["page_count"], 7)
        self.assertIsNone(self.record["exam"]["paper_id"])
        self.assertEqual(self.record["source"]["source_authenticity"], "publisher-unverified")
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertFalse(self.record["canonical_question_source_ready"])

    def test_question_sequence_scores_and_optional_variants(self):
        headings = [int(n) for n in re.findall(r"^\*\*(\d+)．", self.question, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 23)))
        items = self.record["question_sources"]
        self.assertEqual([row["question_number"] for row in items], list(range(1, 23)))
        self.assertEqual([row["question_id"] for row in items], [
            f"1997-shanghai-science-q{n:03d}" for n in range(1, 23)
        ])
        self.assertEqual(sum(row["score"] for row in items), 150)
        self.assertEqual(sum(len(row["variants"]) for row in items), 27)
        self.assertEqual(self.record["exam"]["question_count"], 22)
        self.assertEqual(self.record["exam"]["total_score"], 150)
        self.assertEqual(self.record["optional_groups"], [
            {"groups": ["A1", "B1"], "question_numbers": [13, 14, 15, 16], "choose_one": True},
            {"groups": ["A2", "B2"], "question_numbers": [20], "choose_one": True},
        ])
        for group in ("A₁组", "B₁组", "A₂组", "B₂组"):
            self.assertIn(group, self.question)

    def test_source_specific_high_risk_notation_and_stems_are_retained(self):
        for fragment in (
            r"\overline M\cap N",
            r"x^2\csc\theta-y^2\sec\theta=1",
            r"\sin 2x=\dfrac12",
            r"\dfrac{-3-i}{1+2i}",
            r"3\sin x\cos x-4\cos^2x",
            r"(\vec a+\vec b)\perp(\vec a-\vec b)",
            r"z_1^2=z_2",
            r"y^2=p(x+1)",
            r"3tS_n-(2t+3)S_{n-1}=3t",
            "交点在抛物线的准线右边",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.question)
        self.assertNotIn(r"\csc^2\theta", self.question)
        self.assertIn("| 1—6 | B、D、B、C、A、D |", self.answers)

    def test_printed_answers_are_distinguished_from_verified_official_answers(self):
        self.assertTrue(self.record["source_has_answers"])
        self.assertEqual(self.record["answer_attribution"], "printed-in-fixed-source-pdf")
        self.assertEqual(self.record["printed_solutions_attribution"], "printed-in-fixed-source-pdf")
        self.assertIn("来源印载答案", self.answers)
        self.assertIn("not-verified", self.answers)
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["review_status"], "needs-review")

    def test_page_map_ocr_provenance_and_figures_are_auditable(self):
        self.assertEqual([row["source_page"] for row in self.record["page_map"]], list(range(1, 8)))
        self.assertEqual(self.record["ocr"]["initial_pages_processed"], 7)
        self.assertEqual(self.record["ocr"]["current_turn_new_ocr_calls"], 0)
        self.assertEqual(self.record["token_usage"]["external_chat_api_calls"], 0)
        figures = self.record["figure_files"]
        self.assertEqual({row["question_number"] for row in figures}, {18, 19, 20, 21})
        for row in figures:
            path = PAPER / row["path"]
            self.assertTrue(path.is_file(), row["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(row["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertIn(path.name, self.question)
            self.assertIn("\\begin{tikzpicture}", path.read_text(encoding="utf-8"))
        rasters = [p for p in PAPER.rglob("*") if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
        self.assertEqual(rasters, [])

    def test_record_hashes_match_current_drafts(self):
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(QUESTION.read_bytes()).hexdigest())
        self.assertEqual(self.record["answers_draft_sha256"], hashlib.sha256(ANSWERS.read_bytes()).hexdigest())
        self.assertEqual(self.record["solutions_draft_sha256"], hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest())

    def test_printed_solution_transcription_covers_all_six_written_questions(self):
        for number in range(17, 23):
            self.assertIn(f"## 第 {number} 题", self.solutions)
        self.assertIn("来源印载解答转录", self.solutions)
        self.assertIn("独立数学验证", self.solutions)
        self.assertIn(r"p=f(m)=\frac{m^2}{m+2}", self.solutions)


if __name__ == "__main__":
    unittest.main()

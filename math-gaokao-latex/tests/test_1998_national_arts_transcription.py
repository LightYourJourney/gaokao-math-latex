import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1998_全国卷_文科"
QUESTION_FILE = PAPER / "题面转录草稿.md"
RECORD_FILE = PAPER / "来源校对.json"
PROGRESS_FILE = ROOT / "PROGRESS.md"
PROGRESS_HEADING = "## 1998 全国卷文科：25题固定来源转录完成（2026-10-15；三处源文疑点待核）"


class NationalArts1998TranscriptionTests(unittest.TestCase):
    def test_source_bundle_exists_before_its_contents_are_read(self):
        required = [QUESTION_FILE, RECORD_FILE, PROGRESS_FILE]
        for path in required:
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file(), f"missing transcription artifact: {path}")

    def test_fixed_pdf_fingerprint_and_unverified_status_are_preserved(self):
        if not RECORD_FILE.is_file():
            self.fail("source audit record must exist before validating its pinned source")
        record = json.loads(RECORD_FILE.read_text(encoding="utf-8"))
        self.assertEqual(record["source"]["source_id"], "src-19546ffe511fd8607988e9153f3b24ef24704bd592b19f95cfcde2844ab83cc5")
        self.assertEqual(record["source"]["upstream_path"], "普通高考/1998/1998全国文.pdf")
        self.assertEqual(record["source"]["pdf_sha256"], "dbf7bd3f4e11621d7d31e38ed304f3617f20ecb070e96ac0ec0fbc5a17b9748b")
        self.assertEqual(record["source"]["git_blob_oid"], "187701f7207338551455492be912749f669207e5")
        self.assertEqual(record["source"]["page_count"], 1)
        self.assertEqual(record["source"]["source_authenticity"], "publisher-unverified")
        self.assertEqual(record["review_status"], "needs-review")
        self.assertEqual(record["mathematical_verification_status"], "conditionally-reviewed-with-source-conditions")
        self.assertEqual(record["verification"]["independent_math_review"]["status"], "conditional-pass")
        self.assertFalse(record["verification"]["independent_math_review"]["full_paper_acceptance"])
        self.assertFalse(record["canonical_question_source_ready"])
        self.assertIsNone(record["official_answer"])
        self.assertFalse(record["source_has_answers"])

    def test_all_25_question_numbers_and_types_are_recorded_in_order(self):
        if not (QUESTION_FILE.is_file() and RECORD_FILE.is_file()):
            self.fail("question draft and source record are required for completeness checks")
        question = QUESTION_FILE.read_text(encoding="utf-8")
        record = json.loads(RECORD_FILE.read_text(encoding="utf-8"))
        headings = [int(number) for number in re.findall(r"^## 第 (\d+) 题", question, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 26)))
        self.assertEqual(
            record["artifacts"]["question_draft"]["sha256"],
            hashlib.sha256(QUESTION_FILE.read_bytes()).hexdigest(),
        )
        self.assertEqual(record["exam"]["question_count"], 25)
        self.assertEqual([item["question_number"] for item in record["question_sources"]], list(range(1, 26)))
        self.assertEqual([item["question_id"] for item in record["question_sources"]], [f"1998-national-arts-q{n:03d}" for n in range(1, 26)])
        self.assertTrue(all(item["score"] is None for item in record["question_sources"]))

    def test_high_risk_source_notation_and_source_anomalies_are_not_silently_repaired(self):
        if not (QUESTION_FILE.is_file() and RECORD_FILE.is_file()):
            self.fail("question draft and source record are required for fidelity checks")
        question = QUESTION_FILE.read_text(encoding="utf-8")
        record = json.loads(RECORD_FILE.read_text(encoding="utf-8"))
        for fragment in (
            r"\sin 600^\circ",
            r"y=a^{|x|}",
            r"(x-1)^2+y^2=4",
            r"\dfrac{x^2}{12}+\dfrac{y^2}{3}=1",
            r"大圆周长的 \(\dfrac16\)",
            "不必考虑所有可能的情形",
            r"a_n=\lg\left(1+\dfrac1{b_n}\right)",
        ):
            with self.subTest(fragment=fragment):
                self.assertTrue(fragment in question, f"missing source fragment: {fragment}")
        notes = "\n".join(record["source_observations"])
        for question_number in (12, 13, 25):
            self.assertIn(f"第{question_number}题", notes)
        self.assertIn("改写题面", notes)
        self.assertEqual(record["transcription_status"], "transcribed-pending-independent-review")

    def test_vector_figure_sources_are_registered_and_no_raster_is_committed(self):
        if not RECORD_FILE.is_file():
            self.fail("source audit record must register the vector figure sources")
        record = json.loads(RECORD_FILE.read_text(encoding="utf-8"))
        figures = record["figure_files"]
        self.assertEqual({item["question_number"] for item in figures}, {2, 11, 22, 23, 24})
        question = QUESTION_FILE.read_text(encoding="utf-8")
        for item in figures:
            with self.subTest(path=item["path"]):
                path = PAPER / item["path"]
                self.assertTrue(path.is_file())
                self.assertEqual(path.suffix, ".tex")
                self.assertEqual(item["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertIn(path.name, question)
                self.assertIn("\\begin{tikzpicture}", path.read_text(encoding="utf-8"))
        raster_files = [p for p in PAPER.rglob("*") if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
        self.assertEqual(raster_files, [])

    def test_progress_receipt_names_the_completed_transcription_stage(self):
        if not PROGRESS_FILE.is_file():
            self.fail("project progress file must exist")
        progress = PROGRESS_FILE.read_text(encoding="utf-8")
        self.assertTrue(PROGRESS_HEADING in progress, "missing 1998 transcription receipt")
        self.assertTrue("test_1998_national_arts_transcription.py" in progress, "receipt omits its test file")
        self.assertTrue("答案与解析尚未完成" in progress, "receipt must state the remaining work")


if __name__ == "__main__":
    unittest.main()

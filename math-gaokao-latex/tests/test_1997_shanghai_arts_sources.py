"""Fixed-source transcription integrity checks for 1997 Shanghai arts mathematics."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1997_上海卷_文科"
QUESTION = PAPER / "题面转录草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
SOLUTIONS = PAPER / "解析草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
PROGRESS = ROOT / "PROGRESS.md"
SOURCE_ID = "src-a9a7c39b5916052fa3afb91395913a6018084816eb8c8996044eb9a5b475d6ef"
PDF_SHA256 = "843b55901dacb8cea8d37ff0cedd6a2d00b54d7176bc2096edb1ce773dfd5250"
PDF_BLOB = "c7f82660289f11b66b2129583a813e3fdbc624a0"
PROGRESS_HEADING = "## 1997 上海卷文科：22题转录与来源答案/解析覆盖完成"


class ShanghaiArts1997SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next(
            (item for item in cls.manifest["sources"] if item.get("source_id") == SOURCE_ID),
            None,
        )
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.question = QUESTION.read_text(encoding="utf-8") if QUESTION.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.progress = PROGRESS.read_text(encoding="utf-8") if PROGRESS.is_file() else ""

    def test_transcription_is_bound_to_the_fixed_unbound_source(self):
        self.assertIsNotNone(self.source)
        self.assertEqual(self.source["source_state"], "ready")
        self.assertIsNone(self.source["paper_id"])
        self.assertEqual(self.source["upstream_path"], "普通高考/1997/1997上海文.pdf")
        self.assertEqual(self.source["artifact"]["sha256"], PDF_SHA256)
        self.assertEqual(self.source["git_blob_oid"], PDF_BLOB)
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["source"]["source_manifest_revision"], 4152)
        self.assertEqual(self.record["source"]["pdf_sha256"], PDF_SHA256)
        self.assertEqual(self.record["source"]["git_blob_oid"], PDF_BLOB)
        self.assertIsNone(self.record["exam"]["paper_id"])
        expected_hashes = {
            "draft_sha256": QUESTION,
            "answers_draft_sha256": ANSWERS,
            "solutions_draft_sha256": SOLUTIONS,
        }
        for key, path in expected_hashes.items():
            self.assertEqual(self.record[key], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_question_sequence_scores_and_optional_variants_are_complete(self):
        headings = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.question, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 23)))
        self.assertEqual(self.record["exam"]["question_count"], 22)
        self.assertEqual(self.record["exam"]["prompt_variant_count"], 27)
        items = self.record["question_sources"]
        self.assertEqual([item["question_number"] for item in items], list(range(1, 23)))
        self.assertEqual(
            [item["question_id"] for item in items],
            [f"1997-shanghai-arts-q{number:03d}" for number in range(1, 23)],
        )
        self.assertEqual(sum(item["score"] for item in items), 150)
        self.assertEqual(sum(len(item["variants"]) for item in items), 27)
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 6, "section_score": 24},
            {"type": "fill-in", "first": 7, "last": 16, "section_score": 40},
            {"type": "solution", "first": 17, "last": 22, "section_score": 86},
        ])
        self.assertEqual(self.record["optional_groups"], [
            {"groups": ["A1", "B1"], "question_numbers": [13, 14, 15, 16], "choose_one": True},
            {"groups": ["A2", "B2"], "question_numbers": [20], "choose_one": True},
        ])
        for track in ("A₁组", "B₁组", "A₂组", "B₂组"):
            self.assertIn(track, self.question)

    def test_source_specific_stems_and_high_risk_notation_are_preserved(self):
        for fragment in (
            r"\overline M\cap N",
            r"(1-k)x^2+y^2=k^2-1",
            r"\lg(1-3x)=\lg(3-x)+\lg(7+x)",
            r"\dfrac{-3-i}{1+2i}",
            r"C'B'\perp AB",
            r"$CA'B\perp$",
            r"y^2=p(x+1)",
            "交点在抛物线的准线右边",
            r"b_{2n}b_{2n+1}",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.question)
        for number in range(17, 23):
            self.assertIn(f"## 第 {number} 题", self.solutions)

    def test_source_printed_answers_are_not_claimed_as_official_or_verified(self):
        self.assertTrue(self.record["source_has_answers"])
        self.assertEqual(self.record["answer_attribution"], "printed-in-fixed-source-pdf")
        self.assertEqual(self.record["printed_solutions_attribution"], "printed-in-fixed-source-pdf")
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["source"]["source_authenticity"], "publisher-unverified")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertFalse(self.record["canonical_question_source_ready"])
        for fragment in ("来源印载答案", "不标作已核实官方答案", "not-verified"):
            self.assertIn(fragment, self.answers)

    def test_vector_figure_sources_are_registered_and_rasters_are_absent(self):
        figures = self.record["figure_files"]
        self.assertEqual({item["question_number"] for item in figures}, {18, 19, 20, 21})
        for item in figures:
            path = PAPER / item["path"]
            self.assertTrue(path.is_file(), item["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(item["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertIn(path.name, self.question)
            self.assertIn("\\begin{tikzpicture}", path.read_text(encoding="utf-8"))
        rasters = [
            path for path in PAPER.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
            and ".work" not in path.parts
        ]
        self.assertEqual(rasters, [])
        self.assertTrue(any("第22题" in note and "不为第22题另登记" in note
                            for note in self.record["source_image_observations"]))

    def test_page_map_and_ocr_caching_are_auditable(self):
        self.assertEqual([item["source_page"] for item in self.record["page_map"]], list(range(1, 9)))
        self.assertEqual(self.record["ocr"]["initial_pages_processed"], 8)
        self.assertEqual(self.record["ocr"]["current_turn_new_ocr_calls"], 0)
        self.assertEqual(self.record["ocr"]["current_turn_cached_page_retrievals"], 8)
        self.assertEqual(self.record["token_usage"]["external_chat_api_calls"], 0)

    def test_transcription_and_figure_smoke_receipts_are_recorded(self):
        verification = self.record["verification"]
        self.assertEqual(verification["source_page_visual_review"]["pages"], list(range(1, 9)))
        self.assertEqual(verification["transcription_tests"], {
            "suite": "test_1997_shanghai_arts_sources.py", "passed": 8, "status": "passed"
        })
        self.assertEqual(verification["figure_smoke"]["status"], "passed")
        self.assertEqual(verification["figure_smoke"]["page_count"], 4)
        self.assertEqual(verification["figure_smoke"]["paper_size"], "A4")
        self.assertFalse(verification["figure_smoke"]["raster_outputs_committed"])

    def test_completed_transcription_is_registered_in_project_progress(self):
        self.assertIn(PROGRESS_HEADING, self.progress)
        self.assertIn("来源校对.json", self.progress)
        self.assertIn("test_1997_shanghai_arts_sources.py", self.progress)


if __name__ == "__main__":
    unittest.main()

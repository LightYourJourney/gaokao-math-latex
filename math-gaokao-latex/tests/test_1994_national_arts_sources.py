"""Source-bound integrity checks for the 1994 national arts paper draft."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1994_全国卷_文科"
PAPER_ID = "gk-1994-national-arts"
SOURCE_ID = "src-cafef4608133fbbf6e430e07061b30e714dded069fecffebce620e84186c5dbe"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"


class NationalArts1994SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next((s for s in cls.manifest["sources"] if s["source_id"] == SOURCE_ID), None)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.text = DRAFT.read_text(encoding="utf-8") if DRAFT.is_file() else ""

    def test_draft_is_bound_to_the_fixed_manifest_pdf(self):
        self.assertIsNotNone(self.source)
        if not RECORD.is_file():
            self.fail("1994 national arts source record is missing")
            return
        self.assertEqual(self.source["source_state"], "ready")
        self.assertEqual(self.source["paper_id"], PAPER_ID)
        self.assertEqual(self.source["paper_relation"], "canonical")
        self.assertEqual(self.source["upstream_path"], "普通高考/1994/1994全国文.pdf")
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["git_blob_oid"], self.source["git_blob_oid"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())

    def test_all_25_question_numbers_and_type_ranges_are_preserved(self):
        if not DRAFT.is_file() or not RECORD.is_file():
            self.fail("question draft and source record must exist")
            return
        headings = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.text, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 26)))
        self.assertEqual(self.record["question_count"], 25)
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 15},
            {"type": "fill-in", "first": 16, "last": 20},
            {"type": "solution", "first": 21, "last": 25},
        ])
        expected_columns = [1] * 11 + [2] * 10 + [3] * 4
        self.assertEqual([q["question_number"] for q in self.record["question_sources"]], headings)
        self.assertEqual([q["column"] for q in self.record["question_sources"]], expected_columns)
        self.assertTrue(all(q["source_page"] == 1 for q in self.record["question_sources"]))

    def test_unavailable_official_answers_and_scores_remain_uninvented(self):
        if not RECORD.is_file():
            self.fail("1994 national arts source record is missing")
            return
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["review_status"], "needs-review")

    def test_source_sensitive_formulas_and_wording_are_transcribed(self):
        required = (
            "1994 普通高等学校招生考试（全国卷文）",
            r"x^2+ky^2=2",
            r"\dfrac\pi2",
            r"f(x)=1-\sqrt{1-x^2}",
            r"\lg(10^x+1)",
            r"y^2=8-4x",
            r"\sin\theta+\cos\theta=\dfrac15",
            r"\cos^2 2x",
            "正三棱柱",
            "射影长",
            "最佳近似值",
            "证明",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_diagrams_resolve_to_registered_vector_sources(self):
        if not RECORD.is_file():
            self.fail("1994 national arts source record is missing")
            return
        figures = self.record.get("figure_files", [])
        self.assertEqual({f["question_number"] for f in figures}, {12, 23})
        for figure in figures:
            path = PAPER / figure["path"]
            self.assertTrue(path.is_file(), figure["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), figure["sha256"])
            self.assertIn(f"]({figure['path']})", self.text)
        raster_suffixes = {".png", ".jpg", ".jpeg"}
        paper_files = [p for p in PAPER.rglob("*") if p.is_file() and ".work" not in p.parts]
        self.assertFalse([p for p in paper_files if p.suffix.lower() in raster_suffixes])


if __name__ == "__main__":
    unittest.main()

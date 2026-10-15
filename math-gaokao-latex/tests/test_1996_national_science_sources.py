"""Source-bound integrity checks for the 1996 national science paper draft."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1996_全国卷_理科"
SOURCE_ID = "src-fb045a4a0667851f33004aec1c020d6220dfa5733a9ee28cc4eeb10d7f6b7aa6"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
PROGRESS = ROOT / "PROGRESS.md"


class NationalScience1996SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next((s for s in cls.manifest["sources"] if s["source_id"] == SOURCE_ID), None)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.text = DRAFT.read_text(encoding="utf-8") if DRAFT.is_file() else ""
        cls.progress = PROGRESS.read_text(encoding="utf-8")

    def test_draft_is_bound_to_the_fixed_manifest_pdf(self):
        self.assertIsNotNone(self.source)
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("1996 national science draft and source record are missing")
            return
        self.assertEqual(self.source["source_state"], "ready")
        self.assertIsNone(self.source["paper_id"])
        self.assertEqual(self.source["upstream_path"], "普通高考/1996/1996全国理.pdf")
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["source_manifest_revision"], 4152)
        self.assertEqual(self.record["pdf_sha256"], "cf9952ef5be41c7604605d651ada54a85217a4da09dfab19670a7a54cdc02bd4")
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["git_blob_oid"], "2ae88cb4f08ce91c3b372c4d82bf40a3bebc2c13")
        self.assertEqual(self.record["git_blob_oid"], self.source["git_blob_oid"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())

    def test_all_25_question_numbers_types_and_columns_are_preserved(self):
        if not DRAFT.is_file() or not RECORD.is_file():
            self.fail("question draft and source record must exist")
            return
        headings = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.text, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 26)))
        self.assertEqual(self.record["question_count"], 25)
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 15},
            {"type": "fill-in", "first": 16, "last": 19},
            {"type": "solution", "first": 20, "last": 25},
        ])
        expected_columns = [1] * 6 + [2] * 11 + [3] * 8
        questions = self.record["question_sources"]
        self.assertEqual([q["question_id"] for q in questions], [f"1996-national-science-q{n:03d}" for n in headings])
        self.assertEqual([q["question_number"] for q in questions], headings)
        self.assertEqual([q["column"] for q in questions], expected_columns)
        self.assertTrue(all(q["source_page"] == 1 for q in questions))
        self.assertEqual(self.record["page_map"][0]["printed_page"], "52")

    def test_source_specific_math_and_conditions_are_transcribed(self):
        required = (
            "1996 普通高等学校招生考试（全国卷理）",
            r"I=\mathbb{N}",
            r"x=2n,\ n\in\mathbb{N}",
            r"x=4n,\ n\in\mathbb{N}",
            r"x=3+3\cos\varphi",
            r"y=-1+5\sin\varphi",
            r"0<\alpha<\dfrac{\pi}{2}",
            r"\arcsin\left[\cos\left(\frac{\pi}{2}+\alpha\right)\right]",
            r"\dfrac{S_{10}}{S_5}=\dfrac{31}{32}",
            r"\rho=\dfrac{3}{2-\cos\theta}",
            r"\dfrac{2\sqrt{2}}{3}\pi",
            r"x^2+y^2-6x-7=0",
            r"y^2=2px",
            r"\log_a\left(1-\dfrac{1}{x}\right)>1",
            r"E\in BB_1",
            r"A_1EC\perp\text{侧面 }AC_1",
            r"AA_1=A_1B_1",
            "$10000$ 公顷",
            r"\left|A_1B_1\right|=\sqrt{5}\left|A_2B_2\right|",
            r"\left|A_1B_1\right|=\sqrt{5}\left|A_2B_2\right|$，$l_1$，求",
            r"f(x)=ax^2+bx+c",
            r"g(x)=ax+b",
            r"-1\le x\le1",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_source_figures_resolve_to_registered_vector_sources(self):
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("question draft and source record must exist")
            return
        figures = self.record.get("figure_files", [])
        self.assertEqual({f["question_number"] for f in figures}, {2, 19, 22})
        for figure in figures:
            path = PAPER / figure["path"]
            self.assertTrue(path.is_file(), figure["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), figure["sha256"])
            self.assertIn(f"]({figure['path']})", self.text)
        raster_suffixes = {".png", ".jpg", ".jpeg"}
        paper_files = [p for p in PAPER.rglob("*") if p.is_file() and ".work" not in p.parts]
        self.assertFalse([p for p in paper_files if p.suffix.lower() in raster_suffixes])

    def test_answers_scores_and_acceptance_state_are_not_fabricated(self):
        if not RECORD.is_file():
            self.fail("source record must exist")
            return
        self.assertFalse(self.record["source_has_answers"])
        self.assertIsNone(self.record["official_answer"])
        self.assertIsNone(self.record["question_scores"])
        self.assertIsNone(self.record["total_score"])
        self.assertIsNone(self.record["paper_id"])
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertEqual(
            [issue["question_number"] for issue in self.record["source_issues"]],
            [24],
        )
        self.assertEqual(self.record["source_issues"][0]["issue_code"], "possible-source-typo")
        self.assertIn("1996 全国卷理科：25题固定来源题面转录完成", self.progress)


if __name__ == "__main__":
    unittest.main()

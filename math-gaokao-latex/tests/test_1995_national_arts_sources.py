"""Source-bound integrity checks for the 1995 national arts paper draft."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1995_全国卷_文科"
SOURCE_ID = "src-0c51704136436568d67830f04de25d0a93485e4840a20d2586fc0614304e3c46"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"


class NationalArts1995SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next((s for s in cls.manifest["sources"] if s["source_id"] == SOURCE_ID), None)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.text = DRAFT.read_text(encoding="utf-8") if DRAFT.is_file() else ""

    def test_draft_is_bound_to_the_fixed_manifest_pdf(self):
        self.assertIsNotNone(self.source)
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("1995 national arts draft and source record are missing")
            return
        self.assertEqual(self.source["source_state"], "ready")
        self.assertIsNone(self.source["paper_id"])
        self.assertEqual(self.source["upstream_path"], "普通高考/1995/1995全国文.pdf")
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["pdf_sha256"], "eafe29dd184aded8687308b5eb0765c8a51b2b4c1ab954b4bbf0a454791b57fb")
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["git_blob_oid"], self.source["git_blob_oid"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())

    def test_all_26_question_numbers_types_and_columns_are_preserved(self):
        if not DRAFT.is_file() or not RECORD.is_file():
            self.fail("question draft and source record must exist")
            return
        headings = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.text, re.MULTILINE)]
        self.assertEqual(headings, list(range(1, 27)))
        self.assertEqual(self.record["question_count"], 26)
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 15},
            {"type": "fill-in", "first": 16, "last": 20},
            {"type": "solution", "first": 21, "last": 26},
        ])
        expected_columns = [1] * 8 + [2] * 12 + [3] * 6
        questions = self.record["question_sources"]
        self.assertEqual([q["question_number"] for q in questions], headings)
        self.assertEqual([q["column"] for q in questions], expected_columns)
        self.assertTrue(all(q["source_page"] == 1 for q in questions))
        self.assertEqual(self.record["page_map"][0]["printed_page"], "52")

    def test_source_specific_formulas_and_wording_are_transcribed(self):
        required = (
            "1995 普通高等学校招生考试（全国卷文）",
            r"\overline{M}\cap N",
            r"y=\dfrac{1}{x+1}",
            r"4\sin\left(3x+\frac\pi4\right)+3\cos\left(3x+\frac\pi4\right)",
            r"\sin^4\theta+\cos^4\theta=\dfrac59",
            r"B_1E_1=D_1F_1=\dfrac{A_1B_1}{4}",
            r"\log_2(x+1)^2+\log_4(x+1)=5",
            r"\theta\in(\pi,2\pi)",
            r"\log_{0.5}S_n+\log_{0.5}S_{n+2}",
            r"P=1000(x+t-8)",
            r"Q=500\sqrt{40-(x-8)^2}",
            r"\frac{x^2}{24}+\frac{y^2}{16}=1",
            r"|OQ|\cdot|OP|=|OR|^2",
            "射线 $OP$",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_source_figures_resolve_to_registered_vector_sources(self):
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("question draft and source record must exist")
            return
        figures = self.record.get("figure_files", [])
        self.assertEqual({f["question_number"] for f in figures}, {2, 5, 10, 24})
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


if __name__ == "__main__":
    unittest.main()

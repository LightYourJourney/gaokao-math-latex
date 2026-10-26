"""Source-bound integrity checks for the 1996 national arts paper draft."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1996_全国卷_文科"
SOURCE_ID = "src-14b5e41702770e8e042a2012628b4977636412e2adfb4e564c6ce6d4e72b063a"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
PROGRESS = ROOT / "PROGRESS.md"


class NationalArts1996SourceTests(unittest.TestCase):
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
            self.fail("1996 national arts draft and source record are missing")
            return
        self.assertEqual(self.source["source_state"], "ready")
        self.assertIsNone(self.source["paper_id"])
        self.assertEqual(self.source["upstream_path"], "普通高考/1996/1996全国文.pdf")
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["source_manifest_revision"], 4152)
        self.assertEqual(self.record["pdf_sha256"], "0470ab13b1cd6af91b1268e91fdf8baa4412db573b0f411196a06f054776bca2")
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["git_blob_oid"], "c214378b9ed2ebedd5ef555b720daacbd99a699a")
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
        expected_columns = [1] * 7 + [2] * 12 + [3] * 6
        questions = self.record["question_sources"]
        self.assertEqual([q["question_id"] for q in questions], [f"1996-national-arts-q{n:03d}" for n in headings])
        self.assertEqual([q["question_number"] for q in questions], headings)
        self.assertEqual([q["column"] for q in questions], expected_columns)
        self.assertTrue(all(q["source_page"] == 1 for q in questions))
        self.assertEqual(self.record["page_map"][0]["printed_page"], "53")

    def test_source_specific_math_and_conditions_are_transcribed(self):
        required = (
            "1996 普通高等学校招生考试（全国卷文）",
            r"I=\{1,2,3,4,5,6,7\}",
            r"y=a^{-x}",
            r"y=\log_a x",
            r"\sin^2 x>\cos^2 x",
            r"\dfrac{(2+2i)^4}{(1-\sqrt{3}i)^5}",
            r"\sin\alpha=-\dfrac{24}{25}",
            r"-\dfrac{\pi}{2}\le x\le\dfrac{\pi}{2}",
            r"25x^2-150x+9y^2+18y+9=0",
            r"\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1",
            r"f(x+2)=-f(x)",
            r"y^2=2px",
            r"\tan20^\circ+\tan40^\circ+\sqrt{3}\tan20^\circ\tan40^\circ",
            r"\log_a(x+1-a)>1",
            r"S_3+S_6=2S_9",
            r"\dfrac{1}{\cos A}+\dfrac{1}{\cos C}=-\dfrac{\sqrt{2}}{\cos B}",
            r"AB=\dfrac{AA_1}{3}=a",
            r"CF=2a",
            "$10000$ 公顷",
            r"粮食单产比现在增加 $22\%$",
            r"人均粮食占有量比现在提高 $10\%$",
            r"人口年增长率为 $1\%$",
            r"y^2-x^2=1",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_source_figures_resolve_to_registered_vector_sources(self):
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("question draft and source record must exist")
            return
        figures = self.record.get("figure_files", [])
        self.assertEqual({f["question_number"] for f in figures}, {2, 19, 23})
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
        self.assertTrue(self.record["canonical_question_source_ready"])
        self.assertEqual(self.record["transcription_status"], "transcribed-independently-reviewed")
        self.assertIn("该圆锥的体积（", self.text)
        self.assertNotIn("该圆锥的体积为（", self.text)
        self.assertIn("平均每年至多只能减少", self.text)
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertIn("1996 全国卷文理科：题面独立复核与源内疑点登记", self.progress)
        self.assertIn("1996 全国卷文科：25题固定来源题面转录完成", self.progress)


if __name__ == "__main__":
    unittest.main()

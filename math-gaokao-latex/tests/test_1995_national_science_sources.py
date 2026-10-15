"""Source-bound integrity checks for the 1995 national science paper draft."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1995_全国卷_理科"
SOURCE_ID = "src-57e24f3b0726bbd53b079d006cf45d201003b5e40b63aa30c2d19a12ea330ed5"
DRAFT = PAPER / "题面转录草稿.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
PROGRESS = ROOT / "PROGRESS.md"


class NationalScience1995SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next((s for s in cls.manifest["sources"] if s["source_id"] == SOURCE_ID), None)
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.text = DRAFT.read_text(encoding="utf-8") if DRAFT.is_file() else ""

    def test_draft_is_bound_to_the_fixed_manifest_pdf(self):
        self.assertIsNotNone(self.source)
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("1995 national science draft and source record are missing")
            return
        self.assertEqual(self.source["source_state"], "ready")
        self.assertIsNone(self.source["paper_id"])
        self.assertEqual(self.source["upstream_path"], "普通高考/1995/1995全国理.pdf")
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["pdf_sha256"], "b973fca6da3cf130d0279a4c327dd4222852a7402f7154c98fc7f1a2ccc00133")
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
        expected_columns = [1] * 8 + [2] * 10 + [3] * 8
        questions = self.record["question_sources"]
        self.assertEqual([q["question_number"] for q in questions], headings)
        self.assertEqual(
            [q["question_id"] for q in questions],
            [f"1995-national-science-q{n:03d}" for n in range(1, 27)],
        )
        self.assertEqual([q["column"] for q in questions], expected_columns)
        self.assertTrue(all(q["source_page"] == 1 for q in questions))
        self.assertEqual(self.record["page_map"][0]["printed_page"], "51")

    def test_source_specific_formulas_and_wording_are_transcribed(self):
        required = (
            "1995 普通高等学校招生考试（全国卷理）",
            r"\overline{M}\supseteq\overline{N}",
            r"M\subseteq\overline{N}",
            r"\overline{M}\subseteq\overline{N}",
            r"M\supseteq\overline{N}",
            r"y=-\dfrac{1}{x+1}",
            r"\left(\dfrac13\right)^{x^2-8}>3^{-2x}",
            r"y=\sin\left(x-\dfrac\pi6\right)\cos x",
            r"y^2=a(x+1)\quad(a>0)",
            r"Z_2=1+\sqrt3i",
            r"\sin^2 20^\circ+\cos^2 50^\circ+\sin20^\circ\cos50^\circ",
            r"\sin^4\theta+\cos^4\theta=\dfrac59",
            r"BC=CA=CC_1",
            r"AF\perp DE",
            r"\frac{\lg S_n+\lg S_{n+2}}{2}<\lg S_{n+1}",
            r"\lg S_n+\lg S_{n+2}",
            r"\lg(S_n-c)+\lg(S_{n+2}-c)",
            r"P=1000(x+t-8)",
            r"Q=500\sqrt{40-(x-8)^2}",
            r"\frac{x^2}{24}+\frac{y^2}{16}=1",
            r"\frac{x}{12}+\frac{y}{8}=1",
            r"|OQ|\cdot|OP|=|OR|^2",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_apparently_duplicate_q14_choices_are_preserved_and_flagged(self):
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("question draft and source record must exist")
            return
        repeated_choice = r"\rho=\dfrac{c(1-e)}{1-e\cos\theta}"
        self.assertEqual(self.text.count(repeated_choice), 2)
        self.assertTrue(any(
            issue.get("question_number") == 14
            and issue.get("type") == "possible-duplicate-options"
            for issue in self.record.get("source_issues", [])
        ))

    def test_source_figures_resolve_to_registered_vector_sources(self):
        if not RECORD.is_file() or not DRAFT.is_file():
            self.fail("question draft and source record must exist")
            return
        figures = self.record.get("figure_files", [])
        self.assertEqual({f["question_number"] for f in figures}, {2, 5, 15, 23})
        for figure in figures:
            path = PAPER / figure["path"]
            self.assertTrue(path.is_file(), figure["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), figure["sha256"])
            self.assertIn(f"]({figure['path']})", self.text)
        raster_suffixes = {".png", ".jpg", ".jpeg"}
        paper_files = [p for p in PAPER.rglob("*") if p.is_file() and ".work" not in p.parts]
        self.assertFalse([p for p in paper_files if p.suffix.lower() in raster_suffixes])

    def test_source_answers_scores_and_acceptance_state_are_not_fabricated(self):
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

    def test_completed_transcription_has_a_stage_record_before_the_next_paper(self):
        progress = PROGRESS.read_text(encoding="utf-8")
        marker = "## 1995 全国卷理科：固定来源26题题面转录完成"
        start = progress.find(marker)
        self.assertGreaterEqual(start, 0, "completed paper transcription is absent from PROGRESS.md")
        next_heading = progress.find("\n## ", start + len(marker))
        entry = progress[start:next_heading if next_heading >= 0 else len(progress)]
        for section in ("已完成：", "修改文件：", "验证：", "剩余/下一步："):
            with self.subTest(section=section):
                self.assertIn(section, entry)
        self.assertIn("OCR 0次", entry)
        self.assertIn("独立核", entry)


if __name__ == "__main__":
    unittest.main()

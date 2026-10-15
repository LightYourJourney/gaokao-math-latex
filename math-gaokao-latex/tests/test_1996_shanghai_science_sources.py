"""Fixed-source integrity checks for the 1996 Shanghai science paper."""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1996_上海卷_理科"
YEAR_DIR = ROOT.parent / "1996"
SOURCE_ID = "src-544d6951d540a551546ce474b93c3b9bc08e1863472ea0998f971dd4b619de21"
PDF_SHA256 = "3c0c6b1da5ad37389f6cccf555c72188500787510e60b9902af8d51c97bb1f18"
PDF_BLOB = "6da50ed1a5c26c6337afa8c8d0613b6113e974b4"
QUESTION = YEAR_DIR / "1996_数学真题_上海理工农医_试题.md"
ANSWERS = YEAR_DIR / "1996_数学真题_上海理工农医_答案要点.md"
SOLUTIONS = YEAR_DIR / "1996_数学真题_上海理工农医_解析正文.md"
COMBINED = YEAR_DIR / "1996_数学真题_上海理工农医_含解析.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class ShanghaiScience1996SourceTests(unittest.TestCase):
    REQUIRED_ARTIFACTS = (QUESTION, ANSWERS, SOLUTIONS, COMBINED, RECORD)

    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next(
            (item for item in cls.manifest["sources"] if item["source_id"] == SOURCE_ID),
            None,
        )
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.question = QUESTION.read_text(encoding="utf-8") if QUESTION.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.combined = COMBINED.read_text(encoding="utf-8") if COMBINED.is_file() else ""

    def setUp(self):
        if self._testMethodName != "test_transcription_is_bound_to_the_fixed_manifest_pdf":
            missing = [path.name for path in self.REQUIRED_ARTIFACTS if not path.is_file()]
            if missing:
                self.skipTest("transcription artifacts not written yet; binding test reports expected RED")

    def test_transcription_is_bound_to_the_fixed_manifest_pdf(self):
        self.assertIsNotNone(self.source)
        for path in self.REQUIRED_ARTIFACTS:
            self.assertTrue(path.is_file(), f"missing transcription artifact: {path}")
        self.assertEqual(self.source["source_state"], "ready")
        self.assertIsNone(self.source["paper_id"])
        self.assertEqual(self.source["upstream_path"], "普通高考/1996/1996上海理.pdf")
        self.assertEqual(self.source["artifact"]["sha256"], PDF_SHA256)
        self.assertEqual(self.source["git_blob_oid"], PDF_BLOB)
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["source_manifest_revision"], 4152)
        self.assertEqual(self.record["pdf_sha256"], PDF_SHA256)
        self.assertEqual(self.record["git_blob_oid"], PDF_BLOB)
        self.assertIsNone(self.record["paper_id"])
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(QUESTION.read_bytes()).hexdigest())

    def test_all_questions_sections_and_optional_tracks_are_preserved(self):
        self.assertEqual(
            [int(number) for number in re.findall(r"^\*\*(\d+)．", self.question, re.MULTILINE)],
            list(range(1, 25)),
        )
        self.assertEqual(self.record["question_count"], 24)
        self.assertEqual(self.record["total_score"], 150)
        self.assertEqual(self.record["section_scores"], {"single-choice": 24, "fill-in": 40, "solution": 86})
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 8},
            {"type": "fill-in", "first": 9, "last": 18},
            {"type": "solution", "first": 19, "last": 24},
        ])
        self.assertEqual(self.record["optional_groups"], [
            {"groups": ["A1", "B1"], "question_numbers": [15, 16, 17, 18]},
            {"groups": ["A2", "B2"], "question_numbers": [22]},
        ])
        self.assertEqual(
            [item["question_number"] for item in self.record["question_sources"]],
            list(range(1, 25)),
        )
        self.assertEqual(
            [item["question_id"] for item in self.record["question_sources"]],
            [f"1996-shanghai-science-q{number:03d}" for number in range(1, 25)],
        )
        self.assertEqual([item["printed_page"] for item in self.record["page_map"][:8]],
                         [str(number) for number in range(74, 82)])
        self.assertEqual(
            self.record["page_map"][8]["role"],
            "blank reverse scan with faint show-through; final solution 24 lines at top",
        )

    def test_source_specific_stems_and_printed_answers_are_retained(self):
        for fragment in (
            "1996 年全国普通高等学校招生统一考试（上海·理工农医类）",
            r"\sin\left(x+\dfrac{\pi}{4}\right)",
            r"y=\left(\dfrac{b}{a}\right)^x",
            r"\log_2(9^x-5)=\log_2(3^x-2)+2",
            r"y=ax^2+c",
            r"A(\sqrt2,0)",
            "A1 组", "B1 组", "A2 组", "B2 组",
            r"A_n=\dfrac32(a_n-1)",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.question)
        for fragment in (
            "1—8 | D，B，B，C，C，D，D，A",
            r"\dfrac1{28}",
            r"-\dfrac{4\sqrt2}{9}",
            r"\dfrac98",
            "A2 组", "B2 组",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.answers)
        for fragment in (
            r"\cos2\alpha=\dfrac13",
            r"-\dfrac14<a<-\dfrac9{49}",
            r"MN\perp AB",
            r"4x+y+2=0",
            r"d_n=3^{2n+1}",
            r"\dfrac{y^2}{2}-\dfrac{x^2}{2}=1",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.solutions)

    def test_source_answers_are_not_claimed_as_official_or_independently_verified(self):
        self.assertTrue(self.record["source_has_answers"])
        self.assertTrue(self.record["source_has_solutions"])
        self.assertEqual(self.record["answer_attribution"], "printed-in-fixed-source-pdf")
        self.assertEqual(self.record["solution_attribution"], "printed-in-fixed-source-pdf")
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["source_authenticity"], "publisher-unverified")
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertIn("固定来源 PDF", self.answers)
        self.assertIn("官方标准答案", self.answers)
        self.assertIn("官方性尚待核验", self.answers)

    def test_figures_are_registered_tex_and_no_scan_rasters_are_added(self):
        figures = self.record["figure_files"]
        self.assertEqual({item["question_number"] for item in figures}, {7, 8, 18, 20, 21, 23})
        for item in figures:
            path = PAPER / item["path"]
            self.assertTrue(path.is_file(), item["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
            self.assertIn(path.name, self.combined)
        rasters = [path for path in PAPER.rglob("*") if path.is_file()
                   and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
                   and ".work" not in path.parts]
        self.assertEqual(rasters, [])

    def test_combined_document_is_reproducible_from_canonical_sources(self):
        self.assertEqual(
            solution_sources.render_combined(self.question, self.solutions, self.answers),
            self.combined,
        )
        self.assertEqual(len(re.findall(r"^### 第 \d+ 题$", self.combined, re.MULTILINE)), 24)
        self.assertEqual(self.record["canonical_source_files"], {
            "question": "1996/1996_数学真题_上海理工农医_试题.md",
            "answers": "1996/1996_数学真题_上海理工农医_答案要点.md",
            "solutions": "1996/1996_数学真题_上海理工农医_解析正文.md",
            "combined": "1996/1996_数学真题_上海理工农医_含解析.md",
        })


if __name__ == "__main__":
    unittest.main()

"""Fixed-source integrity checks for the 1996 Shanghai arts paper transcription."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1996_上海卷_文科"
YEAR_DIR = ROOT.parent / "1996"
SOURCE_ID = "src-2cd0e37e0e31e5698fdc0f84ba902576f04a18869a73ec0f15565f94f2c0bd35"
PDF_SHA256 = "c1ab3c4cbe34a089b34b295330d594a9da2543601bed06ddddc519d9fbcf0ab1"
PDF_BLOB = "34660c7f035f71d803a1f05fff75eef960f877bd"
QUESTION = YEAR_DIR / "1996_数学真题_上海文史_试题.md"
ANSWERS = YEAR_DIR / "1996_数学真题_上海文史_答案要点.md"
SOLUTIONS = YEAR_DIR / "1996_数学真题_上海文史_解析正文.md"
COMBINED = YEAR_DIR / "1996_数学真题_上海文史_含解析.md"
DRAFT = QUESTION
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"


class ShanghaiArts1996SourceTests(unittest.TestCase):
    REQUIRED_ARTIFACTS = (DRAFT, RECORD, ANSWERS, SOLUTIONS, COMBINED)

    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next(
            (source for source in cls.manifest["sources"] if source["source_id"] == SOURCE_ID),
            None,
        )
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.draft = DRAFT.read_text(encoding="utf-8") if DRAFT.is_file() else ""
        cls.question = QUESTION.read_text(encoding="utf-8") if QUESTION.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.combined = COMBINED.read_text(encoding="utf-8") if COMBINED.is_file() else ""

    def setUp(self):
        if self._testMethodName != "test_transcription_is_bound_to_the_fixed_manifest_pdf":
            missing = [str(path.relative_to(ROOT.parents[1])) for path in self.REQUIRED_ARTIFACTS if not path.is_file()]
            if missing:
                self.skipTest("transcription artifacts not written yet; artifact-binding test reports the expected RED")

    def test_transcription_is_bound_to_the_fixed_manifest_pdf(self):
        self.assertIsNotNone(self.source)
        for path in (DRAFT, RECORD, QUESTION, ANSWERS, SOLUTIONS, COMBINED):
            self.assertTrue(path.is_file(), f"missing transcription artifact: {path}")
        self.assertEqual(self.source["source_state"], "ready")
        self.assertEqual(self.source["paper_id"], "gk-1996-regular-shanghai-arts")
        self.assertEqual(self.source["paper_relation"], "canonical")
        self.assertEqual(self.source["upstream_path"], "普通高考/1996/1996上海文.pdf")
        self.assertEqual(self.source["artifact"]["sha256"], PDF_SHA256)
        self.assertEqual(self.source["git_blob_oid"], PDF_BLOB)
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["upstream_path"], "普通高考/1996/1996上海文.pdf")
        self.assertEqual(self.record["source_manifest_revision"], 4152)
        self.assertIsNone(self.record["paper_id"])
        self.assertEqual(self.record["pdf_sha256"], PDF_SHA256)
        self.assertEqual(self.record["git_blob_oid"], PDF_BLOB)
        self.assertEqual(self.record["draft_sha256"], hashlib.sha256(DRAFT.read_bytes()).hexdigest())

    def test_all_24_question_numbers_and_optional_groups_are_preserved(self):
        self.assertEqual(
            [int(number) for number in re.findall(r"^\*\*(\d+)．\*\*", self.draft, re.MULTILINE)],
            list(range(1, 25)),
        )
        self.assertEqual(self.record["question_count"], 24)
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 8},
            {"type": "fill-in", "first": 9, "last": 18},
            {"type": "solution", "first": 19, "last": 24},
        ])
        self.assertEqual(self.record["total_score"], 150)
        self.assertEqual(self.record["section_scores"], {"single-choice": 24, "fill-in": 40, "solution": 86})
        self.assertEqual(
            [page["printed_page"] for page in self.record["page_map"]],
            [str(number) for number in range(83, 91)],
        )
        for variant in ("A1", "B1"):
            self.assertIn(variant, self.draft)
        for variant in ("A2", "B2"):
            self.assertIn(variant, self.draft)
        self.assertEqual(self.record["optional_groups"], [
            {"groups": ["A1", "B1"], "question_numbers": [15, 16, 17, 18]},
            {"groups": ["A2", "B2"], "question_numbers": [22]},
        ])
        question_sources = self.record["question_sources"]
        self.assertEqual([item["question_number"] for item in question_sources], list(range(1, 25)))
        self.assertEqual(
            [item["question_id"] for item in question_sources],
            [f"1996-shanghai-arts-q{number:03d}" for number in range(1, 25)],
        )
        self.assertTrue(all(1 <= item["source_page"] <= 8 for item in self.record["question_sources"]))

    def test_source_specific_math_and_printed_answer_conclusions_are_retained(self):
        question_fragments = (
            r"M=\{(x,y)\mid x+y=2\}",
            r"N=\{(x,y)\mid x-y=4\}",
            r"\sin\left(x+\dfrac{\pi}{4}\right)",
            r"\dfrac{x^2}{25}+\dfrac{y^2}{9}=1",
            r"\log_2(9^x-5)",
            r"(x-2)^2+y^2=1",
            "A1、B1",
            "A2、B2",
            r"A_n=\dfrac{3}{2}(a_n-1)",
        )
        for fragment in question_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.draft)
        for fragment in (
            "**答案：D**", "**答案：A**", "A1 组", "B1 组", "1440", r"\dfrac1{28}",
            r"-\dfrac{4\sqrt2}{9}",
            "A2 组", "B2 组", "\\dfrac{2\\sqrt2\\pi}{3}", "房地产",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.answers)
        for fragment in (
            r"2\cdot\left(-\dfrac{2\sqrt2}{3}\right)\cdot\dfrac13",
            r"-\dfrac14<a<-\dfrac9{49}",
            r"MN\perp AB",
            r"|z|=1",
            r"\dfrac{y^2}{2}-\dfrac{x^2}{2}=1",
            r"d_n=a_{2n+1}=3^{2n+1}",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.solutions)

    def test_printed_answers_are_not_mislabeled_as_verified_official_answers(self):
        self.assertTrue(self.record["source_has_answers"])
        self.assertEqual(self.record["answer_attribution"], "printed-in-fixed-source-pdf")
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["source_authenticity"], "publisher-unverified")
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")
        self.assertEqual(self.record["review_status"], "needs-review")
        self.assertFalse(self.record["canonical_question_source_ready"])
        self.assertIn("转录自固定来源 PDF", self.answers)
        self.assertIn("不是已核实的官方标准答案", self.answers)

    def test_figures_are_registered_vector_sources_and_no_raster_is_committed(self):
        figures = self.record["figure_files"]
        self.assertEqual({item["question_number"] for item in figures}, {8, 20, 21, 23})
        for item in figures:
            path = PAPER / item["path"]
            self.assertTrue(path.is_file(), item["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item["sha256"])
            self.assertIn(path.name, self.combined)
        tracked_rasters = [
            path for path in PAPER.rglob("*")
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
            and ".work" not in path.parts
        ]
        self.assertEqual(tracked_rasters, [])

    def test_generated_combined_source_contains_the_transcribed_question_and_answers(self):
        self.assertEqual(
            len(re.findall(r"^### 第 \d+ 题$", self.combined, re.MULTILINE)),
            24,
        )
        for fragment in (
            "1996 年上海卷文史类数学解析正文",
            "### 第 24 题",
            "**答案：D**",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.combined)
        self.assertIn("1996_数学真题_上海文史_试题.md", self.record["canonical_source_files"]["question"])
        self.assertIn("1996_数学真题_上海文史_答案要点.md", self.record["canonical_source_files"]["answers"])
        self.assertIn("1996_数学真题_上海文史_解析正文.md", self.record["canonical_source_files"]["solutions"])


if __name__ == "__main__":
    unittest.main()

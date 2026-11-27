import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2006/2006_数学真题_上海文_试题.md"
SOURCE_ID = "src-99308f47f68d68564b8892365d9d5f2f0634fe95a4a3de74fa5be5fb5fcf9d23"
SOURCE_SHA256 = "1881e13e917febc73882254c59200be192286802042d650c82956f8901c2d174"
PAPER_ID = "gk-2006-regular-shanghai-arts"


class ShanghaiArts2006TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription draft must exist")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")

    def test_fixed_source_fingerprint_is_formally_bound_with_limits_preserved(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["raw_paper_name"], "2006上海文.pdf")
        self.assertEqual(source["upstream_path"], "普通高考/2006/2006上海文.pdf")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["paper_id"], PAPER_ID)
        self.assertEqual(source["paper_relation"], "canonical")
        paper = next(item for item in self.manifest["papers"] if item["paper_id"] == PAPER_ID)
        self.assertEqual(paper["legacy_ids"], [])
        self.assertEqual(paper["source_ids"], [SOURCE_ID])
        self.assertEqual(paper["question_count"], 22)
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn(PAPER_ID, self.transcript)
        self.assertIn("publisher_edition_status: unknown", self.transcript)
        self.assertIn("scan_lineage_status: unknown", self.transcript)
        self.assertIn("不证明该镜像 PDF 是官方原件", self.transcript)

    def test_transcription_covers_all_22_questions_in_source_order(self):
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)

    def test_high_risk_symbols_match_the_fixed_source_pages(self):
        expected = (
            r"f(x)=a^x",
            r"\log_3(x^2-10)=1+\log_3x",
            r"x+y-3\geqslant0",
            r"x+2y-5\leqslant0",
            r"|y|=2^x+1",
            r"\sqrt{-a}<\sqrt b",
            r"a_n+S_n=4096",
            r"T_n<-509",
            r"F(-\sqrt3,0)",
            r"D(2,0)",
            r"\dfrac12",
            r"y=x+\dfrac ax",
            r"y=x+\dfrac{2^b}{x}",
            r"g(x)=x^n+\dfrac c{x^n}",
        )
        for expression in expected:
            with self.subTest(expression=expression):
                self.assertIn(expression, self.transcript, f"missing high-risk source expression: {expression}")

    def test_linear_constraints_are_separate_cases_rows(self):
        match = re.search(
            r"\\begin\{cases\}\n(.*?)\n\\end\{cases\}",
            self.transcript,
            re.S,
        )
        self.assertIsNotNone(match)
        self.assertEqual(
            match.group(1).splitlines(),
            [
                r"x+y-3\geqslant0,\\",
                r"x+2y-5\leqslant0,\\",
                r"x\geqslant0,\\",
                r"y\geqslant0,",
            ],
        )

    def test_source_figures_are_linked_to_vector_sources_without_raster_embedding(self):
        self.assertEqual(self.transcript.count("](../math-gaokao-latex/2006_上海卷_文科/figures/"), 4)
        self.assertNotIn(r"\includegraphics", self.transcript)
        self.assertNotIn(".png", self.transcript)
        self.assertNotIn("![", self.transcript)

    def test_q18_figure_link_preserves_the_north_arrow_from_the_source(self):
        q18 = re.search(r"^\*\*18．\*\*.*?(?=^\*\*19．\*\*)", self.transcript, re.M | re.S)
        self.assertIsNotNone(q18)
        figure_link = next(line for line in q18.group(0).splitlines() if "](../math-gaokao-latex/2006_上海卷_文科/figures/" in line)
        self.assertIn("北", figure_link)

    def test_source_identity_and_review_limits_are_explicit(self):
        self.assertIn("source_identity_status: exam_identity_verified", self.transcript)
        self.assertIn("source_bytes_status: fixed_upstream_git_blob_verified", self.transcript)
        self.assertIn("publisher_edition_status: unknown", self.transcript)
        self.assertIn("scan_lineage_status: unknown", self.transcript)
        self.assertIn("不证明该镜像 PDF 是官方原件", self.transcript)
        self.assertIn("未将原卷截图作为图形资产入库", self.transcript)

    def test_official_answers_are_separate_from_the_question_only_scan(self):
        self.assertIn("固定 PDF 共两页 A3 题面，不附答案页", self.transcript)
        self.assertIn("用于确认考试身份并核对官方答案", self.transcript)
        self.assertNotIn("官方答案：", self.transcript)


if __name__ == "__main__":
    unittest.main()

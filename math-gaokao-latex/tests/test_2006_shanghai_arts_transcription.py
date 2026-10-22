import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2006/2006_数学真题_上海文_题面转录草稿.md"
SOURCE_ID = "src-99308f47f68d68564b8892365d9d5f2f0634fe95a4a3de74fa5be5fb5fcf9d23"
SOURCE_SHA256 = "1881e13e917febc73882254c59200be192286802042d650c82956f8901c2d174"


class ShanghaiArts2006TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription draft must exist")
        self.transcript = TRANSCRIPT.read_text(encoding="utf-8")

    def test_fixed_source_fingerprint_is_ready_but_not_formally_bound(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["raw_paper_name"], "2006上海文.pdf")
        self.assertEqual(source["upstream_path"], "普通高考/2006/2006上海文.pdf")
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertIsNone(source["paper_id"])
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn("`paper_id` 未绑定", self.transcript)
        self.assertIn("版次及扫描件来源链未核", self.transcript)

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
        self.assertEqual(self.transcript.count("](figures/"), 4)
        self.assertNotIn(r"\includegraphics", self.transcript)
        self.assertNotIn(".png", self.transcript)
        self.assertNotIn("![", self.transcript)

    def test_q18_figure_link_preserves_the_north_arrow_from_the_source(self):
        q18 = re.search(r"^\*\*18．\*\*.*?(?=^\*\*19．\*\*)", self.transcript, re.M | re.S)
        self.assertIsNotNone(q18)
        figure_link = next(line for line in q18.group(0).splitlines() if "](figures/" in line)
        self.assertIn("北", figure_link)

    def test_review_status_distinguishes_checked_text_from_pending_artwork(self):
        self.assertIn(
            "**状态：题面文字已独立核对；答案与解析待独立推导，四幅原图待矢量重绘及复核。**",
            self.transcript,
        )

    def test_source_answers_are_not_invented_or_mislabeled_official(self):
        self.assertIn("题面文字已独立核对；答案与解析待独立推导", self.transcript)
        self.assertIn("固定 PDF 仅含题面，未见答案页", self.transcript)
        self.assertNotIn("官方答案：", self.transcript)


if __name__ == "__main__":
    unittest.main()

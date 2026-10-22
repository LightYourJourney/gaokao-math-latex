import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2017/2017_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2017/2017_数学真题_春季上海_图表清单.md"
SOURCE_ID = "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9"
SOURCE_SHA256 = "5379de046c452e20504865f84b019a4ad6b8e9edf73c209efe484fcbf68adc37"


class ShanghaiSpring2017TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def test_fixed_source_fingerprint_is_preserved_without_claiming_official_original(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 4)
        self.assertEqual(source["source_state"], "ready")
        self.assertIsNone(source["paper_id"])
        self.assertEqual(source["upstream_path"], "春季高考/2017/2017春季上海.pdf")

        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription must be committed as a canonical input")
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        self.assertIn(SOURCE_ID, transcript)
        self.assertIn(SOURCE_SHA256, transcript)
        self.assertIn("上游公开副本", transcript)
        self.assertIn("未核验为官方原件", transcript)
        self.assertIn("PDF 第 1–3 页", transcript)

    def test_transcription_covers_all_21_questions_and_preserves_high_risk_notation(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the fixed-source transcription must exist before it can be checked")
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        numbers = [int(value) for value in re.findall(r"^\*\*(\d+)．\*\*", transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 22)))
        self.assertEqual(transcript.count("## 一、填空题"), 1)
        self.assertEqual(transcript.count("## 二、选择题"), 1)
        self.assertEqual(transcript.count("## 三、解答题"), 1)
        normalized = transcript.replace(r"\dfrac", r"\frac")

        for source_detail in (
            r"2\bar z-1=3+6i",
            r"\left(x+\frac2x\right)^n",
            r"\frac{x^2}{2}+y^2=1",
            r"|a_1-a_2|+|a_3-a_4|+|a_5-a_6|=3",
            r"$(1,2)$ 上有两个不同的零点",
            r"\overrightarrow{A_1A_3}\cdot\overrightarrow{A_1P}",
            r"A_1C",
            r"DD_1",
            r"f(x)=\frac{2^x+a}{2^x+1}",
            r"AB\perp AC",
            r"AB=AC=AD=60",
            r"每米 0.8 千元与每米 0.9 千元",
            r"x^2-\frac{y^2}{b^2}=1",
            r"\overrightarrow{NP'}=\frac32\overrightarrow{P'Q}",
            r"(-1)^{n+1}\frac{3x_n-1}{3-x_n}",
        ):
            self.assertIn(source_detail, normalized, f"missing source-critical anchor: {source_detail}")

    def test_source_figures_are_inventoried_as_vector_redraw_work_not_raster_assets(self):
        self.assertTrue(FIGURES.is_file(), "the source diagrams must be inventoried before redraw")
        figures = FIGURES.read_text(encoding="utf-8")
        for question in (16, 17, 19):
            self.assertIn(f"第 {question} 题", figures)
        self.assertIn("待重绘为 TikZ/PGFPlots", figures)
        raster_embed = r"!\[[^\]]*\]\([^)]*\.(?:png|jpe?g)(?:\?[^)]*)?\)"
        self.assertNotRegex(figures, raster_embed)
        self.assertNotRegex(TRANSCRIPT.read_text(encoding="utf-8"), raster_embed)


if __name__ == "__main__":
    unittest.main()

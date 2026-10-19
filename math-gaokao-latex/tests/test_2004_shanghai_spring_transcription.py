import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季上海_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季上海_图表清单.md"
SOURCE_ID = "src-eda3090af4489c2848005279f9f1f65a561d4fa54daf91ccd574cfbff213be4f"
SOURCE_SHA256 = "e09d135e7814d1d5dd658ac51829a170edae1267b408f30a4edfa44d2312ca8a"


class ShanghaiSpring2004TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.figures = FIGURES.read_text(encoding="utf-8")
        cls.manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))

    def test_fixed_source_identity_matches_manifest_and_stays_unbound(self):
        source = next(item for item in self.manifest["sources"] if item["source_id"] == SOURCE_ID)
        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季上海.pdf")
        self.assertIsNone(source["paper_id"])
        self.assertIn(SOURCE_ID, self.transcript)
        self.assertIn(SOURCE_SHA256, self.transcript)
        self.assertIn("paper_id 未绑定", self.transcript)

    def test_question_numbers_sections_and_math_delimiters_are_complete(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.transcript.count("## 一、填空题"), 1)
        self.assertEqual(self.transcript.count("## 二、选择题"), 1)
        self.assertEqual(self.transcript.count("## 三、解答题"), 1)
        self.assertEqual(self.transcript.count("$") % 2, 0)

    def test_source_wording_and_high_risk_formulas_are_preserved(self):
        for expected in (
            r"f(x)=\log_3\left(\dfrac{4}{x}+2\right)",
            r"(\sqrt{a_n},\sqrt{a_{n-1}})",
            r"4(x+3)^2+9y^2=36",
            r"\overrightarrow{AB}-\overrightarrow{AC}=\overrightarrow{BC}",
            r"\dfrac{2x+1}{x+2}<0",
            r"10^{f(n)}\cdot\left(\dfrac{4}{5}\right)^{g(n)}<4",
            r"\dfrac{x^2}{a^2}-y^2=1",
        ):
            self.assertIn(expected, self.transcript)
        self.assertIn("实数 $p$ 满足不等式", self.transcript)
        self.assertIn("未将 $x$ 擅改为 $p$", self.transcript)

    def test_all_source_figures_are_registered_without_raster_embedding(self):
        for question in ("第 6 题", "第 8 题", "第 20 题"):
            self.assertIn(question, self.figures)
            self.assertIn(question, self.transcript)
        self.assertNotIn("![", self.transcript)
        self.assertNotRegex(self.transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")


if __name__ == "__main__":
    unittest.main()

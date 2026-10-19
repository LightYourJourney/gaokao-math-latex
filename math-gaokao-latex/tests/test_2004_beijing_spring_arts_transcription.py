import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季北京文_试题.md"
FIGURES = ROOT / "2004/2004_数学真题_春季北京文_图表清单.md"
SOURCE_ID = "src-417d865aa928e69f32b3fcbc80abe4fa227259b79ababcce8765ea981117119b"
SOURCE_SHA256 = "4670b402354afd088d6993fbc473490158f27e232b1c54730e5989b64a21ec26"


class BeijingSpring2004ArtsTranscriptionTests(unittest.TestCase):
    def test_transcription_is_complete_traceable_and_faithful_to_source(self):
        self.assertTrue(TRANSCRIPT.is_file(), "2004 Beijing spring arts transcription is missing")
        self.assertTrue(FIGURES.is_file(), "source figure/table inventory is missing")

        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        figures = FIGURES.read_text(encoding="utf-8")
        manifest = json.loads((PROJECT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["source_id"] == SOURCE_ID)

        self.assertEqual(source["artifact"]["sha256"], SOURCE_SHA256)
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertEqual(source["upstream_path"], "春季高考/2004/2004春季北京文.pdf")
        self.assertIsNone(source["paper_id"])
        self.assertIn(SOURCE_ID, transcript)
        self.assertIn(SOURCE_SHA256, transcript)
        self.assertIn("paper_id 未绑定", transcript)
        self.assertIn("official_answer: null", transcript)

        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 21)))
        self.assertEqual(transcript.count("## 一、选择题"), 1)
        self.assertEqual(transcript.count("## 二、填空题"), 1)
        self.assertEqual(transcript.count("## 三、解答题"), 1)
        self.assertEqual(transcript.count("$") % 2, 0)

        for expected in (
            r"y=\tan\dfrac{x}{2}",
            r"\dfrac{x^2}{4}-\dfrac{y^2}{9}=1",
            r"\dfrac{c}{a}-\dfrac{d}{b}",
            r"\sqrt{2x-1}>x-2",
            r"\dfrac{x^2}{7}+\dfrac{y^2}{3}=1",
            r"R=6371\,\text{km}",
            r"6\times10^5\,\text{km}",
        ):
            self.assertIn(expected, transcript)
        self.assertIn(r"\sqrt", transcript)
        self.assertIn("$2003$ 年 $10$ 月 $15$ 日 $9$ 时", transcript)
        self.assertIn("实数", transcript)
        self.assertIn(r"计算公以及 $2008$", transcript)
        self.assertIn("疑脱“式”字；本稿照录原文", transcript)

        for question in (17, 18, 20):
            self.assertIn(f"| {question} |", figures)
        self.assertIn("四棱锥 `S-ABCD`", figures)
        self.assertNotIn("正四棱锥", figures)
        self.assertIn("`4,7`", figures)
        self.assertIn("`7,12`", figures)
        self.assertNotIn("![", transcript)
        self.assertNotRegex(transcript, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")


if __name__ == "__main__":
    unittest.main()

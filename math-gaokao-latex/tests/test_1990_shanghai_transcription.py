"""1990 上海卷题面应忠实保留固定单页来源中的题目与疑似印文。"""
from pathlib import Path
import re
import unittest


PROJECT = Path(__file__).resolve().parents[1]
TRANSCRIPT = PROJECT.parent / "1990" / "1990_数学真题_上海_试题.md"


class Shanghai1990TranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = TRANSCRIPT.read_text(encoding="utf-8")

    def test_all_27_question_blocks_are_present_in_order(self):
        numbers = [int(value) for value in re.findall(r"(?m)^\*\*(\d+)．\*\*", self.text)]
        self.assertEqual(numbers, list(range(1, 28)))

    def test_source_fingerprint_and_paper_structure_are_recorded(self):
        self.assertIn("src-bda5db939e3a48de23ec63fc5992d73c8e4a0e6a0ea39d36a5a81d4adf09a987", self.text)
        self.assertIn("48ff97de01ef245a42bb95f1a67f9e38ea9490f6a781c045026e31a910f0b4a2", self.text)
        self.assertIn("第 1—10 题为填空题，第 11—20 题为选择题，第 21—27 题为解答题", self.text)

    def test_high_risk_source_glyphs_and_suspected_print_are_preserved(self):
        self.assertIn(r"\dfrac{\sqrt{x+4}}{x+2}", self.text)
        self.assertIn(r"\left|\cos\dfrac\alpha2\right|=-\cos\dfrac\alpha2", self.text)
        self.assertIn(r"b=\log_d(\log_d x)", self.text)
        self.assertIn(r"x^2-3(a+1)x+2(3a+1)\leq0", self.text)
        self.assertIn(r"\sqrt{5\cos x+\cos 2x}+\sin x=0", self.text)
        self.assertIn("则它的矩形共有", self.text)
        self.assertIn("不擅自改正", self.text)

    def test_question_26_diagram_is_explicitly_pending_vector_redraw(self):
        self.assertIn(r"\angle ACM=\angle BCN=45^\circ", self.text)
        self.assertIn("待按原图点线关系矢量重绘", self.text)
        self.assertNotIn("![](", self.text)


if __name__ == "__main__":
    unittest.main()

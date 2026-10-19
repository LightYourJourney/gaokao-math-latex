import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2003/2003_数学真题_春季上海_试题.md"


class ShanghaiSpring2003TranscriptionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TRANSCRIPT.is_file(), "the source-bound transcription must exist")
        self.text = TRANSCRIPT.read_text(encoding="utf-8")

    def test_fixed_source_identity_and_scope_are_traceable(self):
        self.assertIn("src-81eebf19510de69780c4af1cec507bd6428e6a877b52bfd8d45b26539eab4be1", self.text)
        self.assertIn("a998ae0b65e90af8518be09b5dabfba5ad488c1b94cc81483dfe472858051f0f", self.text)
        self.assertIn("2003 普通高等学校春季招生考试（上海卷）", self.text)
        self.assertIn("PDF 第 1–2 页", self.text)
        self.assertIn("原卷印刷页码 123–124", self.text)
        self.assertIn("正式 paper_id gk-2003-spring-shanghai", self.text)

    def test_question_numbers_are_complete_and_grouped_by_source_sections(self):
        numbers = [int(number) for number in re.findall(r"^\*\*(\d+)．", self.text, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertIn("## 一、填空题", self.text)
        self.assertIn("## 二、选择题", self.text)
        self.assertIn("## 三、解答题", self.text)
        self.assertIn("**12．**", self.text)
        self.assertIn("**13．**", self.text)
        self.assertIn("**16．**", self.text)
        self.assertIn("**17．", self.text)
        self.assertIn("**22．", self.text)

    def test_source_figures_are_linked_to_vector_art(self):
        self.assertIn("第 18 题函数图象和第 19 题三棱柱图形均在 PDF 第 1 页", self.text)
        self.assertIn("figures/gaokao_2003_shanghai_spring_q18_sine.tex", self.text)
        self.assertIn("figures/gaokao_2003_shanghai_spring_q19_prism.tex", self.text)
        self.assertNotRegex(self.text, r"(?i)\]\([^)]*\.(?:png|jpe?g|gif|webp|tiff?)\)")

    def test_high_risk_formula_transcription_matches_the_visual_source(self):
        for source_detail in (
            r"f(x)=\sqrt{x}+1",
            r"y=\sqrt3x+3",
            r"f(x)=(\sin x)^2-\left(\dfrac23\right)^{|x|}+\dfrac12",
            r"(\lg 20)^{2\cos x}>1\ (x\in(0,\pi))",
            r"f(x)=\dfrac{1}{2^x+\sqrt2}",
            r"f(x)=\dfrac{x^{1/3}-x^{-1/3}}{5}",
            r"g(x)=\dfrac{x^{1/3}+x^{-1/3}}{5}",
            r"\overrightarrow{AB}=\left\{\dfrac m2,-\dfrac{\sqrt3m}{2},0\right\}",
            r"A\left(1,\dfrac32\right)",
        ):
            self.assertIn(source_detail, self.text)


if __name__ == "__main__":
    unittest.main()

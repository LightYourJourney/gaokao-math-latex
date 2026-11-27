"""Keep the source's unknown operator without leaking the solution interpretation."""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
sys.path.insert(0, str(ROOT.parent / "math-gaokao-2017-2026/tools"))
import md2tex

QUESTIONS = REPO / "1986/1986_数学真题_广东文_试题.md"
SOLUTIONS = REPO / "1986/1986_数学真题_广东文_解析正文.md"


class GuangdongArts1986QuestionBoundaryTests(unittest.TestCase):
    def test_question_and_editorial_notes_do_not_identify_the_unknown_operator(self):
        source = QUESTIONS.read_text(encoding="utf-8")
        header = source.split("**1．**", 1)[0]
        question2 = source.split("**2．**", 1)[1]
        part = question2.split("（2） 将极坐标方程", 1)[1].split("（3）", 1)[0]
        rendered = md2tex.convert_markdown(header + "\n" + part, md2tex.ConversionContext(figure_map={}))
        self.assertNotRegex(rendered.text, r"乘法|乘号|解答页|x\^2\s*=\s*y")
        self.assertIn(r"\rho=\operatorname{tg}\theta\ \square\ \sec\theta", rendered.text)
        self.assertRegex(rendered.text, r"待核|待补|未确定")
        self.assertEqual(rendered.warnings, ())

    def test_original_formula_and_all_ten_subquestions_remain(self):
        source = QUESTIONS.read_text(encoding="utf-8")
        body = source.split("**2．**", 1)[1].split("**3．**", 1)[0]
        numbers = re.findall(r"^（(\d+)）", body, re.MULTILINE)
        self.assertEqual(numbers, [str(n) for n in range(1, 11)])
        self.assertIn(r"\rho=\operatorname{tg}\theta\ \square\ \sec\theta", body)
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        # The interpretation belongs in the solution, not the printable question.
        self.assertIn(r"\rho=\tan\theta\sec\theta", solutions)
        self.assertIn(r"\Longrightarrow x^2=y", solutions)


if __name__ == "__main__":
    unittest.main()

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANSWERS = ROOT / "2000/2000_数学真题_春季上海_答案要点.md"
SOLUTIONS = ROOT / "2000/2000_数学真题_春季上海_解析正文.md"
SOURCE_ID = "src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0"
SOURCE_SHA256 = "f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954"


class ShanghaiSpring2000SolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")

    def test_solution_provenance_is_separate_from_official_answers(self):
        for document in (self.answers, self.solutions):
            self.assertIn(SOURCE_ID, document)
            self.assertIn(SOURCE_SHA256, document)
            self.assertIn("official_answer: null", document)
            self.assertIn("非官方", document)
            self.assertIn("印刷附录", document)

    def test_answer_key_covers_all_22_questions_and_records_cross_check(self):
        rows = re.findall(r"^\|\s*(\d+)\s*\|", self.answers, re.M)
        self.assertEqual([int(number) for number in rows], list(range(1, 23)))
        self.assertIn("两路独立推导复核", self.answers)
        self.assertIn("逐题比对", self.answers)

    def test_detailed_solutions_cover_all_22_questions(self):
        numbers = [
            int(number)
            for number in re.findall(r"^### 第 (\d+) 题$", self.solutions, re.M)
        ]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertIn("两路独立求解者交叉复算", self.solutions)
        self.assertIn("三幅题图已矢量重绘并局部核对，正式构建尚未完成", self.solutions)

    def test_high_risk_conclusions_match_independent_checks(self):
        self.assertIn(r"| 18 | $z=\pm", self.answers)
        self.assertIn("m=0,2", self.answers)
        self.assertIn("m=0,-2", self.answers)
        self.assertIn("混合积绝对值 $48$，为该体积的 $3$ 倍", self.answers)
        self.assertIn(r"| 22 | $A=(1,3)$，$F=(1,1)$", self.answers)
        self.assertIn(r"$\dfrac43$", self.answers)
        self.assertIn("48=3V", self.solutions)
        self.assertIn("A=(1,3)", self.solutions)
        self.assertIn("F=(1,1)", self.solutions)
        self.assertIn(r"\frac{3t^2}{2(3t-2)}", self.solutions)


if __name__ == "__main__":
    unittest.main()

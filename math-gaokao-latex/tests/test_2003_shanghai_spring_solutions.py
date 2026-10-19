import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ANSWERS = ROOT / "2003/2003_数学真题_春季上海_答案要点.md"
SOLUTIONS = ROOT / "2003/2003_数学真题_春季上海_解析正文.md"
QUESTIONS = ROOT / "2003/2003_数学真题_春季上海_试题.md"
COMBINED = ROOT / "2003/2003_数学真题_春季上海_含解析.md"
SOURCE_ID = "src-81eebf19510de69780c4af1cec507bd6428e6a877b52bfd8d45b26539eab4be1"
SOURCE_SHA256 = "a998ae0b65e90af8518be09b5dabfba5ad488c1b94cc81483dfe472858051f0f"
sys.path.insert(0, str(ROOT / "math-gaokao-latex/tools"))
from solution_sources import extract_solution_blocks, parse_answer_points, render_combined


class ShanghaiSpring2003SolutionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(ANSWERS.is_file(), "answer key artifact is missing")
        self.assertTrue(SOLUTIONS.is_file(), "detailed solution artifact is missing")
        self.assertTrue(QUESTIONS.is_file(), "question transcript is missing")
        self.assertTrue(COMBINED.is_file(), "generated combined source is missing")
        self.answers = ANSWERS.read_text(encoding="utf-8")
        self.solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.questions = QUESTIONS.read_text(encoding="utf-8")

    def test_independent_solutions_are_not_claimed_as_official(self):
        for document in (self.answers, self.solutions):
            self.assertIn(SOURCE_ID, document)
            self.assertIn(SOURCE_SHA256, document)
            self.assertIn("official_answer: null", document)
            self.assertIn("非官方", document)

    def test_answer_key_covers_each_of_the_22_questions_once(self):
        points = parse_answer_points(self.answers)
        self.assertEqual([point.number for point in points], list(range(1, 23)))
        self.assertTrue(all(len(point.answers) == 1 for point in points))

    def test_detailed_solutions_cover_each_of_the_22_questions_once(self):
        numbers = [int(number) for number in re.findall(r"^### 第 (\d+) 题$", self.solutions, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))

    def test_formal_solution_source_renderer_round_trips_all_questions(self):
        combined = render_combined(self.questions, self.solutions, self.answers)
        self.assertEqual(COMBINED.read_text(encoding="utf-8"), combined)
        extracted = extract_solution_blocks(combined, self.questions)
        self.assertEqual(render_combined(self.questions, extracted, self.answers), combined)
        self.assertEqual(len(re.findall(r"^### 第 (\d+) 题", combined, re.M)), 22)

    def test_high_risk_answers_match_independent_derivations(self):
        for answer in (
            r"**答案：$4$。**",
            r"**答案：$\dfrac{\pi}{3}$（$60^\circ$）。**",
            r"**答案：$\arctan\dfrac{3}{8}$。**",
            r"**答案：非退化时 $b=6$；若允许退化区间，另有 $a=b=1$。**",
            r"**答案：$\left(\dfrac{\pi}{6}+4k\pi,\sqrt3\right)$",
            r"**答案：（1）正三棱柱；（2）$45^\circ$。**",
            r"f(x^2)=5f(x)g(x)$",
            r"**答案：（1）$\dfrac{x^2}{4}+\dfrac{y^2}{3}=1$",
            r"**答案：（1）A：$1500+230(n-1)$元，B：$2000(1.05)^{n-1}$元",
            r"最大约$827$元，发生在第19年",
        ):
            self.assertIn(answer, self.answers)
        self.assertIn(r"D_{k+1}-D_k=230-100(1.05)^k", self.solutions)
        self.assertIn(r"\left(\frac\pi6+4k\pi,\sqrt3\right)", self.solutions)
        self.assertIn(r"\frac{y^2-v^2}{x^2-u^2}=\frac{b^2}{a^2}", self.solutions)


if __name__ == "__main__":
    unittest.main()

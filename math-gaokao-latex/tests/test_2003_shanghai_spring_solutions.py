import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ANSWERS = ROOT / "2003/2003_数学真题_春季上海_答案要点.md"
SOLUTIONS = ROOT / "2003/2003_数学真题_春季上海_解析正文.md"
SOURCE_ID = "src-81eebf19510de69780c4af1cec507bd6428e6a877b52bfd8d45b26539eab4be1"
SOURCE_SHA256 = "a998ae0b65e90af8518be09b5dabfba5ad488c1b94cc81483dfe472858051f0f"


class ShanghaiSpring2003SolutionTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(ANSWERS.is_file(), "answer key artifact is missing")
        self.assertTrue(SOLUTIONS.is_file(), "detailed solution artifact is missing")
        self.answers = ANSWERS.read_text(encoding="utf-8")
        self.solutions = SOLUTIONS.read_text(encoding="utf-8")

    def test_independent_solutions_are_not_claimed_as_official(self):
        for document in (self.answers, self.solutions):
            self.assertIn(SOURCE_ID, document)
            self.assertIn(SOURCE_SHA256, document)
            self.assertIn("official_answer: null", document)
            self.assertIn("非官方", document)

    def test_answer_key_covers_each_of_the_22_questions_once(self):
        rows = re.findall(r"^\|\s*(\d+)\s*\|", self.answers, re.M)
        self.assertEqual([int(number) for number in rows], list(range(1, 23)))

    def test_detailed_solutions_cover_each_of_the_22_questions_once(self):
        numbers = [int(number) for number in re.findall(r"^### 第 (\d+) 题$", self.solutions, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))

    def test_high_risk_answers_match_independent_derivations(self):
        for answer in (
            r"| 1 | $4$ |",
            r"| 2 | $\dfrac{\pi}{3}$",
            r"| 10 | $\arctan\dfrac{3}{8}$ |",
            r"| 11 | 非退化时 $b=6$；若允许退化区间，另有 $a=b=1$ |",
            r"| 18 | $\left(\dfrac{\pi}{6}+4k\pi,\sqrt3\right)$",
            r"| 19 | （1）正三棱柱；（2）$45^\circ$ |",
            r"f(x^2)=5f(x)g(x)$",
            r"| 21 | （1）$\dfrac{x^2}{4}+\dfrac{y^2}{3}=1$",
            r"| 22 | （1）A：$1500+230(n-1)$元，B：$2000(1.05)^{n-1}$元",
            r"最大约$827$元，发生在第19年",
        ):
            self.assertIn(answer, self.answers)
        self.assertIn(r"D_{k+1}-D_k=230-100(1.05)^k", self.solutions)
        self.assertIn(r"\left(\frac\pi6+4k\pi,\sqrt3\right)", self.solutions)
        self.assertIn(r"\frac{y^2-v^2}{x^2-u^2}=\frac{b^2}{a^2}", self.solutions)


if __name__ == "__main__":
    unittest.main()

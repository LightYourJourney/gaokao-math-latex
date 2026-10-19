import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ANSWERS = ROOT / "2004/2004_数学真题_春季北京理_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_春季北京理_解析正文.md"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季北京理_试题.md"


class BeijingSpring2004ScienceSolutionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not ANSWERS.is_file() or not SOLUTIONS.is_file():
            raise AssertionError("independent answer and solution drafts must both exist")
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")

    def test_independent_answers_are_not_misrepresented_as_official(self):
        self.assertIn("official_answer: null", self.answers)
        self.assertIn("非来源印载答案", self.answers)
        self.assertIn("数学盲核状态: 一名独立复核者", self.answers)
        self.assertIn("paper_id 未绑定", self.transcript)
        self.assertIn("official_answer: null", self.transcript)

    def test_all_questions_have_answer_and_solution_sections(self):
        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.answers, re.M)]
        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", self.solutions, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 21)))
        self.assertEqual(solution_numbers, list(range(1, 21)))

    def test_high_risk_results_and_derivations_are_present(self):
        self.assertIn("| 答案 | A | D | A | C | B | B | D | C | C | B |", self.answers)
        for expected in (
            r"| 答案 | $(-1,+\infty)$ | $1$ | $a(1+b)$；$a(1+b)^5$",
            r"$BC\perp SC$",
            r"$45^\circ$",
            r"$90^\circ$",
            r"$y^2=32x$",
        ):
            self.assertIn(expected, self.answers)
        for expected in (
            r"$m^2+n^2<3$",
            r"$[\dfrac12,5)$",
            r"$\dfrac{\sqrt3}{2}$",
            r"$p=16$",
            r"$M=(11,-4)$",
            r"$4x+y-40=0$",
            r"$550$",
            r"$6\,000$",
            r"$11\,000$",
            r"$a_{ij}=2ij+i+j$",
            r"(2i+1)(2j+1)",
        ):
            self.assertIn(expected, self.answers + self.solutions)
        self.assertIn("不依赖 $\\theta$ 取主值角", self.solutions)
        self.assertIn("定义域为 $x\\ge\\dfrac12$", self.solutions)
        self.assertIn("官方答案", self.solutions)


if __name__ == "__main__":
    unittest.main()

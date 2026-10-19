from fractions import Fraction
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[4]
ANSWERS = ROOT / "2004/2004_数学真题_春季上海_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_春季上海_解析正文.md"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季上海_试题.md"


class ShanghaiSpring2004SolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")

    def test_generated_answers_are_not_mislabeled_as_official(self):
        self.assertIn("official_answer: null", self.answers)
        self.assertIn("非来源印载答案", self.answers)
        self.assertIn("非来源印载解析", self.solutions)
        self.assertIn("本库已有独立推导首稿，尚未独立盲核", self.transcript)

    def test_all_questions_have_answer_and_solution_entries(self):
        answer_numbers = re.findall(r"^\*\*(\d+)．\*\*", self.answers, re.MULTILINE)
        solution_numbers = re.findall(r"^### 第 (\d+) 题$", self.solutions, re.MULTILINE)
        self.assertEqual(answer_numbers, [str(n) for n in range(1, 23)])
        self.assertEqual(solution_numbers, [str(n) for n in range(1, 23)])

    def test_source_ambiguity_is_preserved_as_conditional(self):
        self.assertIn(r"\dfrac{2x+1}{x+2}<0", self.transcript)
        self.assertIn(r"|p|\ge2", self.solutions)
        self.assertIn(r"若经可靠原件证据确认", self.solutions)
        self.assertIn(r"official_answer: null", self.answers)

    def test_2004_bus_fleet_threshold_and_annual_term(self):
        terms = [128 * Fraction(3, 2) ** year for year in range(8)]
        self.assertEqual(terms[6], 1458)
        self.assertEqual(sum(terms[:7]), 4118)
        self.assertEqual(sum(terms[:8]), 6305)
        self.assertLess(sum(terms[:7]), 5000)
        self.assertGreater(sum(terms[:8]), 5000)
        self.assertIn("2011 年底", self.answers)

    def test_inequality_maximum_occurs_at_n_four(self):
        values = {
            n: Fraction(10 ** (n - 1), 1) * Fraction(4, 5) ** ((n + 1) ** 2)
            for n in range(1, 30)
        }
        self.assertEqual(max(values, key=values.get), 4)
        self.assertLess(values[4], 4)
        self.assertIn(r"u_4=1000(4/5)^{25}<4", self.solutions)

    def test_diagram_status_and_links_are_current(self):
        for question, figure in (
            (6, "q06_pyramid"),
            (8, "q08_patterns"),
            (11, "q11_pascal"),
            (20, "q20_oblique_prism"),
        ):
            self.assertIn(f"第 {question} 题", self.transcript)
            self.assertIn(f"gaokao_2004_shanghai_spring_{figure}.tex", self.transcript)
        self.assertIn("仍待独立图像终核", self.transcript)
        self.assertNotIn("尚待依据原图逐项矢量重绘", self.transcript)


if __name__ == "__main__":
    unittest.main()

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季安徽文_试题.md"
ANSWERS = ROOT / "2004/2004_数学真题_春季安徽文_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_春季安徽文_解析正文.md"


class AnhuiSpring2004ArtsSolutionsTests(unittest.TestCase):
    def test_answers_and_solutions_are_complete_and_nonofficial(self):
        transcript = TRANSCRIPT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")

        self.assertIn("official_answer: null", answers)
        self.assertIn("非来源印载答案", answers)
        self.assertIn("非来源印载解析", solutions)
        self.assertIn("第二位解题者逐题交叉核对", answers)
        for document in (answers, solutions):
            self.assertIn("src-9c46c959fc97e9d53c91e510403e97f1810d192e5049962539d9d4b54331c35d", document)
            self.assertIn("17f32ff6f385dfd59d80f5bccfa548dd9b7f8d20e697ce4a66b4de185b95d7a8", document)
            self.assertEqual(document.count("$") % 2, 0)

        answer_numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", answers, re.M)]
        solution_numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题$", solutions, re.M)]
        self.assertEqual(answer_numbers, list(range(1, 23)))
        self.assertEqual(solution_numbers, list(range(1, 23)))
        self.assertIn(r"\log_a^{2}x", transcript)

    def test_parameter_cases_and_under_specified_sequence_are_explicit(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn("若 $a>1$，解集为 $(1,a^2)$", answers)
        self.assertIn("若 $0<a<1$，解集为 $(a^2,1)$", answers)
        self.assertIn("通项不唯一", answers)
        self.assertIn(r"b_n=b_{n-1}+2", solutions)
        self.assertIn(r"b_n=-b_{n-1}", solutions)
        self.assertIn("未给该条件", solutions)

    def test_high_risk_geometry_optimization_and_normal_cases_are_locked(self):
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"\dfrac{\sqrt{10}}5", answers)
        self.assertIn(r"\sqrt{10}/5", solutions)
        self.assertIn(r"23000", answers)
        self.assertIn(r"23000", solutions)
        self.assertIn(r"x=-2", answers)
        self.assertIn("顶点法线", solutions)
        self.assertIn(r"a=(t+2)^2", solutions)
        self.assertIn(r"w^2=3a^2/4", solutions)
        self.assertIn("若 $a>1$", solutions)
        self.assertIn("若 $0<a<1$", solutions)

    def test_q18_nonuniqueness_witnesses_satisfy_the_prefix_sum_identity(self):
        for sequence in (
            [2 * n - 1 for n in range(1, 9)],
            [(-1) ** (n - 1) for n in range(1, 9)],
        ):
            prefix_sum = 0
            for value in sequence:
                prefix_sum += value
                self.assertEqual(4 * prefix_sum, (value + 1) ** 2)


if __name__ == "__main__":
    unittest.main()

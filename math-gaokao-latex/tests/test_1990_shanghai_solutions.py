"""1990 上海卷答案与解析须覆盖全部题目并保留未决来源边界。"""
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
QUESTIONS = ROOT / "1990/1990_数学真题_上海_试题.md"
ANSWERS = ROOT / "1990/1990_数学真题_上海_答案要点.md"
SOLUTIONS = ROOT / "1990/1990_数学真题_上海_解析正文.md"
sys.path.insert(0, str(PROJECT / "tools"))
import solution_sources
import make_short_answers


class Shanghai1990SolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = QUESTIONS.read_text(encoding="utf-8")
        cls.answers = ANSWERS.read_text(encoding="utf-8")
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8")

    def test_answer_and_solution_sources_cover_all_27_questions(self):
        answer_numbers = [int(n) for n in re.findall(r"(?m)^\*\*(\d+)．\*\*", self.answers)]
        solution_numbers = [int(n) for n in re.findall(r"(?m)^### 第 (\d+) 题", self.solutions)]
        self.assertEqual(answer_numbers, list(range(1, 28)))
        self.assertEqual(solution_numbers, list(range(1, 28)))

    def test_answers_are_independent_not_official_and_keep_source_issues_open(self):
        self.assertIn("official_answer: null", self.answers)
        self.assertIn("独立推导", self.answers)
        self.assertIn("非官方", self.answers)
        self.assertIn("**15．**\n\n**答案：C", self.answers)
        self.assertIn(r"\alpha=\alpha_0+2k\pi", self.solutions)
        self.assertIn("k$ 为奇数", self.solutions)
        self.assertIn("**18．**\n\n**答案：U/PENDING；原文两次定义 $b$", self.answers)
        self.assertIn("条件性答案", self.answers)
        self.assertIn("若只把第三个量记号假设为 $c$", self.solutions)
        self.assertIn("假设原文意为点 $P$ 在直线 $x=2$ 上移动", self.solutions)
        self.assertIn(r"3\cos^2x+5\cos x-2=0", self.solutions)
        self.assertIn(r"(\frac12,\pm\frac12)", self.answers)
        self.assertNotIn(r"(\frac12\pm\frac{1}{2\sqrt2},0)", self.answers)

    def test_high_risk_results_are_explicit(self):
        for expected in (
            r"m=-\frac43",
            r"\frac{2}{\sqrt5}",
            r"x=2\pi-\arccos\frac13",
            r"a\in\{-1\}\cup[1,3]",
            r"\frac{\sqrt6}{4}",
            r"\arccos\sqrt{\frac35}",
            r"\pi-\arctan\frac{5}{2\sqrt6}",
        ):
            self.assertIn(expected, self.answers)

    def test_choice_quick_table_keeps_q18_explicitly_pending(self):
        self.assertEqual(
            make_short_answers.parse_quick_table(self.answers, 10),
            ("C", "B", "A", "A", "C", "B", "B", "U", "B", "D"),
        )
        records = make_short_answers.expected_answer_records(self.answers)
        q18_answer = next(record.value for record in records if record.number == 18)
        self.assertTrue(q18_answer.startswith("U/PENDING；"))
        self.assertIn("条件性答案为 D", q18_answer)

    def test_project_solution_contract_accepts_sources_and_question_subparts(self):
        combined = solution_sources.render_combined(
            self.questions, self.solutions, self.answers
        )
        self.assertIn("### 第 15 题", combined)
        self.assertIn("### 第 18 题", combined)
        self.assertIn("### 第 26 题", combined)
        self.assertIn("**答案（1）：", combined)
        self.assertIn("**答案（2）：", combined)
        self.assertIn("U/PENDING", combined)


if __name__ == "__main__":
    unittest.main()

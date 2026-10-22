"""Regression checks for editor-derived 2006 Shanghai arts answers."""
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ANSWER_KEY = ROOT / "2006/2006_数学真题_上海文_答案要点草稿.md"
SOLUTIONS = ROOT / "2006/2006_数学真题_上海文_解析正文草稿.md"
QUESTION_NUMBERS = set(range(1, 23))


class ShanghaiArts2006SolutionTests(unittest.TestCase):
    def require_file(self, path):
        self.assertTrue(path.is_file(), f"required answer artifact is missing: {path}")
        return path.read_text(encoding="utf-8")

    def test_official_answer_source_is_recorded_and_solution_prose_is_distinguished(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)

        for document in (answer_key, solutions):
            with self.subTest(document=document[:80]):
                self.assertIn("official_answer_status: verified", document)
                self.assertIn(
                    'official_answer_source: "https://www.shmeea.edu.cn/page/02200/20061015/3886.html"',
                    document,
                )
        self.assertIn("编者独立撰写", solutions)
        self.assertIn("非官方推导与说明", solutions)
        self.assertIn("Q1–Q22 的最终答案要点均一致", answer_key)
        for image_name in ("00007817.jpg", "00007819.jpg", "00007820.jpg", "00007822.jpg"):
            with self.subTest(image=image_name):
                self.assertIn(f"https://www.shmeea.edu.cn/u/cms/www/wdcms/{image_name}", answer_key)

    def test_both_documents_cover_each_question_once(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)

        answer_numbers = [
            int(value)
            for value in re.findall(r"(?m)^\*\*(\d{1,2})．\*\* 答案：", answer_key)
        ]
        solution_numbers = [
            int(value)
            for value in re.findall(r"(?m)^### 第 (\d{1,2}) 题$", solutions)
        ]
        self.assertEqual(set(answer_numbers), QUESTION_NUMBERS)
        self.assertEqual(len(answer_numbers), 22)
        self.assertEqual(set(solution_numbers), QUESTION_NUMBERS)
        self.assertEqual(len(solution_numbers), 22)

    def test_each_solution_conclusion_matches_the_answer_key(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)
        answers = {
            int(number): value.strip()
            for number, value in re.findall(
                r"(?m)^\*\*(\d{1,2})．\*\* 答案：(.*)$", answer_key
            )
        }
        sections = {
            int(number): body
            for number, body in re.findall(
                r"(?ms)^### 第 (\d{1,2}) 题\s*\n(.*?)(?=^### 第 \d{1,2} 题\s*$|\Z)",
                solutions,
            )
        }

        self.assertEqual(set(answers), QUESTION_NUMBERS)
        self.assertEqual(set(sections), QUESTION_NUMBERS)
        for number in sorted(QUESTION_NUMBERS):
            with self.subTest(question=number):
                conclusion = re.search(r"(?m)^\*\*答案：\*\*\s*(.*)$", sections[number])
                self.assertIsNotNone(conclusion, f"Q{number} has no explicit conclusion")
                self.assertEqual(conclusion.group(1).strip(), answers[number])

    def test_high_risk_results_and_q22_domain_cases_remain_explicit(self):
        answer_key = self.require_file(ANSWER_KEY)
        solutions = self.require_file(SOLUTIONS)
        for expected in (
            r"\frac{x^2}{9}-\frac{y^2}{16}=1",
            r"\frac{14}{33}",
            r"b\in[-1,1]",
            "D（36个）",
            r"-\frac{13\sqrt2}{14}",
            r"71^\circ",
            r"\dfrac{\sqrt2}{6}",
            "第 $46$ 项起",
            r"\sqrt2",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, answer_key)

        q22 = re.search(r"(?ms)^### 第 22 题\s*\n(.*)\Z", solutions)
        self.assertIsNotNone(q22)
        for marker in ("定义域", "$x>0$", "$x<0$", "偶数", "奇数"):
            with self.subTest(marker=marker):
                self.assertIn(marker, q22.group(1))


if __name__ == "__main__":
    unittest.main()

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ANSWERS = ROOT / "1990/1990_数学真题_全国文_答案要点.md"
SOLUTIONS = ROOT / "1990/1990_数学真题_全国文_解析正文.md"

EXPECTED_RESULTS = {
    1: "A",
    2: "C",
    3: "D",
    4: "D",
    5: "C",
    6: "C",
    7: "A",
    8: "B",
    9: "A",
    10: "C",
    11: "B",
    12: "B",
    13: "A",
    14: "C",
    15: "B",
    16: r"$\dfrac{3}{\sqrt{10}}$",
    17: r"$-20$",
    18: r"$2$",
    19: r"$\sqrt3$",
    20: "待核（A侧:其余=7:5；V1/V2顺序未标）",
    21: r"$\{(0,4,8,16),(15,9,3,1)\}$",
    22: r"$\dfrac{24}{7}$",
    23: r"$60^\circ$",
    24: r"$a>1:(\frac12,2);\ 0<a<1:(2,4)$",
    25: r"$z=\pm(\sqrt{1+a}-1)$；$0\le a\le1$ 时另有 $z=\pm i(1\pm\sqrt{1-a})$",
    26: r"$\frac{x^2}{4}+y^2=1$；$(\pm\sqrt3,-\frac12)$",
}


class NationalArts1990SolutionDraftTests(unittest.TestCase):
    def test_answer_and_solution_sources_are_explicitly_generated_not_official(self):
        self.assertTrue(ANSWERS.is_file(), f"missing generated answer key: {ANSWERS}")
        self.assertTrue(SOLUTIONS.is_file(), f"missing generated solution draft: {SOLUTIONS}")
        answer_text = ANSWERS.read_text(encoding="utf-8")
        solution_text = SOLUTIONS.read_text(encoding="utf-8")
        self.assertRegex(answer_text, r"(?m)^official_answer:\s*null\s*$")
        self.assertIn("自行推导", answer_text)
        self.assertIn("非官方", answer_text)
        self.assertIn("非来源印载解析", solution_text)
        self.assertIn("pending", answer_text.lower())
        self.assertIn("pending", solution_text.lower())

    def test_answer_table_covers_each_question_once_with_expected_result_values(self):
        self.assertTrue(ANSWERS.is_file(), f"missing generated answer key: {ANSWERS}")
        text = ANSWERS.read_text(encoding="utf-8")
        table = text.split("## 答案速查", 1)[1].split("## 分题答案", 1)[0]
        rows = {
            int(number): result.strip()
            for number, result in re.findall(r"(?m)^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*$", table)
        }
        self.assertEqual(list(rows), list(range(1, 27)))
        self.assertEqual(rows, EXPECTED_RESULTS)

    def test_solution_sections_cover_all_questions_and_match_the_answer_key(self):
        self.assertTrue(SOLUTIONS.is_file(), f"missing generated solution draft: {SOLUTIONS}")
        text = SOLUTIONS.read_text(encoding="utf-8")
        sections = re.split(r"(?m)^### 第 (\d+) 题\s*$", text)
        actual_numbers = [int(sections[index]) for index in range(1, len(sections), 2)]
        self.assertEqual(actual_numbers, list(range(1, 27)))
        for index in range(1, len(sections), 2):
            number = int(sections[index])
            body = sections[index + 1]
            with self.subTest(question=number):
                self.assertIn(f"结论：{EXPECTED_RESULTS[number]}", body)

    def test_ambiguous_prism_ratio_stays_pending_despite_computed_unordered_volumes(self):
        self.assertTrue(ANSWERS.is_file(), f"missing generated answer key: {ANSWERS}")
        self.assertTrue(SOLUTIONS.is_file(), f"missing generated solution draft: {SOLUTIONS}")
        answer_text = ANSWERS.read_text(encoding="utf-8")
        solution_text = SOLUTIONS.read_text(encoding="utf-8")
        answer_section = re.split(r"(?m)^### 第 20 题\s*$", answer_text)[1].split("### 第 21 题", 1)[0]
        solution_section = re.split(r"(?m)^### 第 20 题\s*$", solution_text)[1].split("### 第 21 题", 1)[0]
        self.assertIn("待核", answer_section)
        self.assertIn("7:5", solution_section)
        self.assertIn("V_1", solution_section)
        self.assertIn("V_2", solution_section)
        self.assertIn("顺序未标", solution_section)


if __name__ == "__main__":
    unittest.main()

import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "math-gaokao-latex/tools"))
from solution_sources import parse_answer_points, render_combined
from make_short_answers import parse_quick_table


QUESTIONS = ROOT / "1990/1990_数学真题_全国文_试题.md"
ANSWERS = ROOT / "1990/1990_数学真题_全国文_答案要点.md"
SOLUTIONS = ROOT / "1990/1990_数学真题_全国文_解析正文.md"

EXPECTED_RESULTS = {
    1: "A",
    2: "C",
    3: "D",
    4: "B",
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

    def test_answer_and_solution_state_math_blind_review_is_complete(self):
        answer_text = ANSWERS.read_text(encoding="utf-8")
        solution_text = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn("状态: pending", answer_text)
        self.assertIn("状态: pending", solution_text)
        self.assertIn("26题独立盲核已完成", answer_text)
        self.assertIn("26题独立盲核已完成", solution_text)
        self.assertNotIn("尚未完成独立盲核", answer_text)
        self.assertNotIn("尚未完成独立盲核", solution_text)

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

    def test_short_answer_generator_can_read_the_choice_quick_reference(self):
        text = ANSWERS.read_text(encoding="utf-8")
        self.assertEqual(
            parse_quick_table(text, 15),
            ("A", "C", "D", "B", "C", "C", "A", "B", "A", "C", "B", "B", "A", "C", "B"),
        )

    def test_answer_source_is_parseable_and_keeps_q20_pending(self):
        points = parse_answer_points(ANSWERS.read_text(encoding="utf-8"))
        self.assertEqual([point.number for point in points], list(range(1, 27)))
        answers = {point.number: point.answers[0][1] for point in points}
        self.assertEqual(
            {number: answers[number] for number in range(1, 16)},
            {number: EXPECTED_RESULTS[number] for number in range(1, 16)},
        )
        self.assertTrue(answers[20].startswith("待核"), answers[20])

    def test_canonical_sources_render_all_questions_without_resolving_q20(self):
        rendered = render_combined(
            QUESTIONS.read_text(encoding="utf-8"),
            SOLUTIONS.read_text(encoding="utf-8"),
            ANSWERS.read_text(encoding="utf-8"),
        )
        numbers = [
            int(line.split()[2])
            for line in rendered.splitlines()
            if line.startswith("### 第 ")
        ]
        self.assertEqual(numbers, list(range(1, 27)))
        q20 = rendered.split("### 第 20 题", 1)[1].split("### 第 21 题", 1)[0]
        self.assertIn("**答案：待核（A侧:其余=7:5；V1/V2顺序未标）**", q20)

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

    def test_q04_clockwise_rotation_matches_the_exact_option_b_value(self):
        question_text = QUESTIONS.read_text(encoding="utf-8")
        answer_text = ANSWERS.read_text(encoding="utf-8")
        solution_text = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"（B）$\dfrac{-1+\sqrt3}{2}+\dfrac{-1-\sqrt3}{2}i$", question_text)
        answer_section = re.split(r"(?m)^\*\*4．\*\*\s*$", answer_text)[1].split("**5．**", 1)[0]
        solution_section = re.split(r"(?m)^### 第 4 题\s*$", solution_text)[1].split("### 第 5 题", 1)[0]
        self.assertIn(r"**答案：B**，$\dfrac{-1+\sqrt3}{2}+\dfrac{-1-\sqrt3}{2}i$。", answer_section)
        self.assertIn(r"(1+i)e^{-2\pi i/3}=\frac{-1+\sqrt3}{2}-\frac{1+\sqrt3}{2}i", solution_section)

    def test_ambiguous_prism_ratio_stays_pending_despite_computed_unordered_volumes(self):
        self.assertTrue(ANSWERS.is_file(), f"missing generated answer key: {ANSWERS}")
        self.assertTrue(SOLUTIONS.is_file(), f"missing generated solution draft: {SOLUTIONS}")
        answer_text = ANSWERS.read_text(encoding="utf-8")
        solution_text = SOLUTIONS.read_text(encoding="utf-8")
        answer_section = re.split(r"(?m)^\*\*20．\*\*\s*$", answer_text)[1].split("**21．**", 1)[0]
        solution_section = re.split(r"(?m)^### 第 20 题\s*$", solution_text)[1].split("### 第 21 题", 1)[0]
        self.assertIn("待核", answer_section)
        self.assertIn("7:5", solution_section)
        self.assertIn("V_1", solution_section)
        self.assertIn("V_2", solution_section)
        self.assertIn("顺序未标", solution_section)


if __name__ == "__main__":
    unittest.main()

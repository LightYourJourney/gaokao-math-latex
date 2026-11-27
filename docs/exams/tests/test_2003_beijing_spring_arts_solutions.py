import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ANSWERS = ROOT / "2003/2003_数学真题_春季北京文_答案要点.md"
SOLUTIONS = ROOT / "2003/2003_数学真题_春季北京文_解析正文.md"
QUESTIONS = ROOT / "2003/2003_数学真题_春季北京文_试题.md"
COMBINED = ROOT / "2003/2003_数学真题_春季北京文_含解析.md"
SOURCE_ID = "src-4ac986eba3d22fd3034252b57e1fed7e2b7b90eaaef7706499eb43fad52756e1"
SOURCE_SHA256 = "fbb6d54c9af88a7fc594be969b8e61c24bb37d98c05061cceaaf5d1be999c5c6"

sys.path.insert(0, str(ROOT / "math-gaokao-latex/tools"))
from solution_sources import (  # noqa: E402
    extract_solution_blocks,
    parse_answer_points,
    render_combined,
    validate_solution_body,
)


class BeijingSpring2003ArtsSolutionTests(unittest.TestCase):
    def setUp(self):
        for path, label in (
            (ANSWERS, "answer key"),
            (SOLUTIONS, "detailed solution"),
            (QUESTIONS, "question transcript"),
            (COMBINED, "generated combined source"),
        ):
            self.assertTrue(path.is_file(), f"{label} artifact is missing")
        self.answers = ANSWERS.read_text(encoding="utf-8")
        self.solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.questions = QUESTIONS.read_text(encoding="utf-8")

    def test_generated_answers_are_not_mislabeled_as_official(self):
        for document in (self.answers, self.solutions):
            self.assertIn(SOURCE_ID, document)
            self.assertIn(SOURCE_SHA256, document)
            self.assertIn("official_answer: null", document)
            self.assertIn("不是官方答案", document)

    def test_answer_key_covers_all_22_questions(self):
        points = parse_answer_points(self.answers)
        self.assertEqual([point.number for point in points], list(range(1, 23)))
        self.assertTrue(all(point.answers for point in points))

    def test_detailed_solutions_cover_all_22_questions(self):
        blocks = validate_solution_body(self.solutions)
        self.assertEqual([block.number for block in blocks], list(range(1, 23)))
        self.assertEqual(
            [int(number) for number in re.findall(r"^### 第 (\d+) 题$", self.solutions, re.M)],
            list(range(1, 23)),
        )

    def test_combined_source_round_trips_through_project_renderer(self):
        rendered = render_combined(self.questions, self.solutions, self.answers)
        self.assertEqual(COMBINED.read_text(encoding="utf-8"), rendered)
        extracted = extract_solution_blocks(rendered, self.questions)
        self.assertEqual(render_combined(self.questions, extracted, self.answers), rendered)

    def test_independently_derived_multiple_choice_answers(self):
        points = {point.number: point for point in parse_answer_points(self.answers)}
        expected = {1: "A", 2: "D", 3: "D", 4: "C", 5: "C", 6: "A", 7: "B", 8: "C", 9: "D", 10: "D", 11: "B", 12: "B"}
        for number, answer in expected.items():
            self.assertEqual(points[number].answer_for(None), answer, f"Q{number}")

    def test_geometry_and_optimization_results_are_present(self):
        for result in (
            r"$\dfrac{2}{\sqrt3}$",
            r"$2\sqrt3$",
            r"$\dfrac{2}{3}$",
            r"$\dfrac{\sqrt5}{2}$",
            r"$\dfrac{3\pi l^2}{32}$",
            r"$4050$ 元",
            r"$307050$ 元",
        ):
            self.assertIn(result, self.answers)
        self.assertIn(r"\mathbb R\setminus\{\dfrac{\pi}{4}+\dfrac{k\pi}{2}:k\in\mathbb Z\}", self.answers)
        self.assertIn(r"[-1,2]\setminus\{\dfrac12\}", self.answers)


if __name__ == "__main__":
    unittest.main()

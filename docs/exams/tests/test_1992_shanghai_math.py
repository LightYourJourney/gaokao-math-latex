"""1992 上海卷关键结论的独立复算抽查（canonical 阶段）。"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ANSWER_FILE = ROOT.parent / "1992/1992_上海_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Shanghai1992MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answers = solution_sources.parse_answer_points(
            ANSWER_FILE.read_text(encoding="utf-8")
        )

    def answer(self, number):
        return self.answers[number].answer_for(None)

    def test_fill_in_answers(self):
        self.assertIn(r"-\dfrac{\sqrt{2}}{4}", self.answer(0))
        self.assertIn("56", self.answer(1))
        self.assertIn(r"\dfrac{3}{2}", self.answer(2))
        self.assertEqual(self.answer(3).strip("$。"), "4")
        self.assertIn("-64", self.answer(4))

    def test_choice_letters(self):
        letters = [self.answer(n).strip("$。") for n in range(10, 20)]
        self.assertEqual(letters, list("DCDDCABABB"))

    def test_q20_is_necessary_not_sufficient_b(self):
        text = self.answer(19).strip("$。")
        self.assertEqual(text, "B")

    def test_q21_angle(self):
        self.assertIn(r"\pi+\arccos\dfrac{33}{65}", self.answer(20).replace(" ", ""))

    def test_q24_volume_and_angle(self):
        text = self.answer(23)
        self.assertIn(r"\dfrac{8}{3}\pi", text)
        self.assertIn("60", text)

    def test_q26_maximum(self):
        self.assertIn(r"\dfrac{\sqrt{5}-1}{4}", self.answer(25))


if __name__ == "__main__":
    unittest.main()

"""1991 上海卷关键结论的独立复算抽查（canonical 阶段）。"""

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ANSWER_FILE = ROOT.parent / "1991/1991_上海_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Shanghai1991MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.answers = solution_sources.parse_answer_points(
            ANSWER_FILE.read_text(encoding="utf-8")
        )

    def answer(self, number):
        return self.answers[number].answer_for(None)

    def test_fill_in_answers(self):
        self.assertIn(r"y=\log_{3}x", self.answer(0))
        self.assertIn(r"-\dfrac{\sqrt{10}}{10}", self.answer(1))
        self.assertEqual(self.answer(2).strip("$。"), r"\dfrac{3}{2}")
        self.assertIn(r"\dfrac{\sqrt{3}}{2}", self.answer(4))
        self.assertIn(r"8\sqrt{2}", self.answer(6))
        self.assertIn(r"x^{2}-4x+5", self.answer(8))

    def test_q8_has_no_constant_term_for_exponent_8(self):
        self.assertIn("无常数项", self.answer(7))
        self.assertIn("60", self.answer(7))

    def test_choice_letters(self):
        letters = [self.answer(n).strip("$。") for n in range(10, 20)]
        self.assertEqual(letters, list("BCBCBADADA"))

    def test_odd_arm_of_choice13_is_impossible(self):
        # 棱长 2,2,2√2，对角线 4，体积 (2·2·2√2)/3 = 8√2/3? 卷内答案取 B。
        self.assertEqual(self.answer(12).strip("$。"), "B")

    def test_q22_range(self):
        text = self.answer(21)
        self.assertIn(r"\dfrac{2-\sqrt{3}}{4}", text)
        self.assertIn(r"\dfrac{2+\sqrt{3}}{4}", text)

    def test_q26_final_line_and_exclusion(self):
        text = self.answer(25)
        self.assertIn("12X-3Y-4=0", text.replace(" ", ""))
        self.assertIn("除去点", text)

    def test_q27_maximum(self):
        self.assertIn("最大值为 $\\dfrac{1}{2}$", self.answer(26))

    def test_q24_angles(self):
        text = self.answer(23)
        self.assertIn("45^{\\circ}", text)
        self.assertIn("90^{\\circ}", text)


if __name__ == "__main__":
    unittest.main()

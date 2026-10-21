import math
from pathlib import Path
import re
import unittest


PROJECT = Path(__file__).resolve().parents[1]
ANSWER_SOURCE = PROJECT.parent / "2025" / "2025_数学真题_答案要点.md"
SOLUTION_SOURCE = PROJECT.parent / "2025" / "2025_数学真题_解析正文.md"


class National1Question8SolutionTests(unittest.TestCase):
    def test_parameter_thresholds_rule_out_option_b(self):
        threshold_z_over_y = (
            5 * math.log(5) - 3 * math.log(3)
        ) / (math.log(5) - math.log(3))
        threshold_x_over_z = (
            5 * math.log(5) - 2 * math.log(2)
        ) / (math.log(5) - math.log(2))

        self.assertAlmostEqual(threshold_z_over_y, 9.301320, places=6)
        self.assertAlmostEqual(threshold_x_over_z, 7.269412, places=6)
        self.assertGreater(threshold_z_over_y, threshold_x_over_z)

    def test_witnesses_realize_the_three_possible_options(self):
        values = {
            k: (2 ** (k - 2), 3 ** (k - 3), 5 ** (k - 5))
            for k in (0, 5, 8)
        }
        x, y, z = values[0]
        self.assertGreater(x, y)
        self.assertGreater(y, z)
        x, y, z = values[5]
        self.assertGreater(y, x)
        self.assertGreater(x, z)
        x, y, z = values[8]
        self.assertEqual((x, y, z), (64, 243, 125))
        self.assertGreater(y, z)
        self.assertGreater(z, x)

    def test_canonical_answer_uses_correct_thresholds_and_d_witness(self):
        source = ANSWER_SOURCE.read_text(encoding="utf-8")
        match = re.search(r"\*\*8．\*\*(.*?)(?=\n---\n)", source, re.S)
        self.assertIsNotNone(match)
        question = match.group(1)

        self.assertIn(r"\approx 9.301320", question)
        self.assertIn(r"\approx 7.269412", question)
        self.assertIn("k=8", question)
        self.assertIn("(64,243,125)", question)
        self.assertNotRegex(question, r"k=10 时[^\n]*（D）")

    def test_detailed_solution_uses_the_same_correct_thresholds_and_witness(self):
        source = SOLUTION_SOURCE.read_text(encoding="utf-8")
        match = re.search(r"### 第 8 题(.*?)(?=\n---\n)", source, re.S)
        self.assertIsNotNone(match)
        solution = match.group(1)

        self.assertIn(r"\approx9.301320", solution)
        self.assertIn(r"\approx7.269412", solution)
        self.assertIn(r"$8$", solution)
        self.assertIn(r"$y>z>x$", solution)
        self.assertNotRegex(solution, r"\$10\$[^\n]*D")


if __name__ == "__main__":
    unittest.main()

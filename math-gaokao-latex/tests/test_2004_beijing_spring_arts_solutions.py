import re
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "math-gaokao-latex"
ANSWERS = ROOT / "2004/2004_数学真题_春季北京文_答案要点.md"
SOLUTIONS = ROOT / "2004/2004_数学真题_春季北京文_解析正文.md"
TRANSCRIPT = ROOT / "2004/2004_数学真题_春季北京文_试题.md"
SOURCE_ID = "src-417d865aa928e69f32b3fcbc80abe4fa227259b79ababcce8765ea981117119b"
SOURCE_SHA256 = "4670b402354afd088d6993fbc473490158f27e232b1c54730e5989b64a21ec26"


class BeijingSpring2004ArtsSolutionTests(unittest.TestCase):
    def test_answers_are_source_traced_non_official_and_cover_all_questions(self):
        missing = [str(path) for path in (ANSWERS, SOLUTIONS) if not path.is_file()]
        self.assertFalse(missing, f"answer artifacts are missing: {missing}")
        answers = ANSWERS.read_text(encoding="utf-8")
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        transcript = TRANSCRIPT.read_text(encoding="utf-8")

        self.assertIn("official_answer: null", answers)
        self.assertIn("非来源印载答案", answers)
        self.assertIn(SOURCE_ID, answers)
        self.assertIn(SOURCE_SHA256, answers)
        self.assertIn("非来源印载解析", solutions)
        answer_numbers = re.findall(r"^\*\*(\d+)．\*\*", answers, re.MULTILINE)
        solution_numbers = re.findall(r"^### 第 (\d+) 题$", solutions, re.MULTILINE)
        self.assertEqual(answer_numbers, [str(n) for n in range(1, 21)])
        self.assertEqual(solution_numbers, [str(n) for n in range(1, 21)])

        for expected in (
            r"答案：D。",
            r"答案：C，即 $5\sqrt5\,\text{cm}$",
            r"答案：B，即 $M:N=1:1$",
            r"答案：$m^2+n^2<3$；所述直线与椭圆有 $2$ 个公共点",
            r"答案：$[\dfrac12,5)$",
            r"答案：$\angle A=60^\circ$，$\dfrac{b\sin B}{c}=\dfrac{\sqrt3}{2}$",
            r"答案：$8\,\text{km/s}$",
            r"$a_{45}=49$",
        ):
            self.assertIn(expected, answers)
        self.assertIn("(i,j)", answers)
        self.assertIn("74950", solutions)
        self.assertIn("4017=3\\cdot13\\cdot103", solutions)
        self.assertIn(r"x\ge1/2", solutions)
        self.assertIn("首轮独立盲解完成", answers)
        self.assertIn("Q16报告结论经主会话复算", answers)
        self.assertIn("首轮独立逐题盲核完成", transcript)
        self.assertIn("Q20疑脱字按源文照录并标注", transcript)
        self.assertIn("paper_id: gk-2004-spring-beijing-arts", transcript)
        self.assertIn("绑定为内部 canonical 输入", transcript)
        self.assertNotIn("官方答案", answers.split("答案归属")[1].split("---")[0])

    def test_arithmetic_values_and_factorized_positions_recompute_exactly(self):
        a, c, earth_radius = 6646, 75, 6371
        self.assertEqual(a - c, earth_radius + 200)
        self.assertEqual(a + c, earth_radius + 350)
        self.assertEqual(a * a - c * c, 44163691)
        speed = Fraction(600000, 20 * 3600 + 49 * 60 + 10)
        self.assertGreater(speed, 8)
        self.assertLess(speed, Fraction(17, 2))
        self.assertEqual(max((77, 98, 125)), 125)

        positions = set()
        for i in range(1, 2009):
            numerator = 2008 - i
            denominator = 2 * i + 1
            if numerator > 0 and numerator % denominator == 0:
                j = numerator // denominator
                if j > 0:
                    positions.add((i, j))
        self.assertEqual(
            positions,
            {(1, 669), (6, 154), (19, 51), (51, 19), (154, 6), (669, 1)},
        )

    def test_q14_line_distance_and_q18_time_window_boundaries_are_safe(self):
        solutions = SOLUTIONS.read_text(encoding="utf-8")
        self.assertIn(r"m^2+n^2>0", solutions)
        self.assertIn("发射时刻计时", solutions)
        self.assertIn("7.943", solutions)

        # For a genuine line mx+ny=3, (m,n) cannot be (0,0); then d^2=9/(m^2+n^2).
        for norm_squared, expected_no_intersection in (
            (Fraction(2), True),
            (Fraction(3), False),
            (Fraction(5), False),
        ):
            self.assertEqual(Fraction(9, norm_squared) > 3, expected_no_intersection)

        orbit_seconds = 20 * 3600 + 49 * 60 + 10
        launch_seconds = 20 * 3600 + 59 * 60
        self.assertEqual(round(600000 / orbit_seconds), 8)
        self.assertEqual(round(600000 / launch_seconds), 8)

    def test_project_combiner_consumes_all_questions_and_answer_blocks(self):
        sys.path.insert(0, str(PROJECT / "tools"))
        try:
            import solution_sources

            rendered = solution_sources.render_combined(
                TRANSCRIPT.read_text(encoding="utf-8"),
                SOLUTIONS.read_text(encoding="utf-8"),
                ANSWERS.read_text(encoding="utf-8"),
            )
        finally:
            sys.path.remove(str(PROJECT / "tools"))
        rendered_numbers = re.findall(r"^### 第 (\d+) 题$", rendered, re.MULTILINE)
        self.assertEqual(rendered_numbers, [str(n) for n in range(1, 21)])
        self.assertIn(r"$a_{ij}=2ij+i+j$", rendered)
        self.assertIn(r"$8\,\text{km/s}$", rendered)


if __name__ == "__main__":
    unittest.main()

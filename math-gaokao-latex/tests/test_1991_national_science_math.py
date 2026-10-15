import json
from fractions import Fraction
from math import comb
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
QUESTION = ROOT.parent / "1991" / "1991_数学真题_全国理_试题.md"
ANSWER = ROOT.parent / "1991" / "1991_数学真题_全国理_答案要点.md"
SOLUTION = ROOT.parent / "1991" / "1991_数学真题_全国理_解析正文.md"
SOURCE_MANIFEST = ROOT / "source-manifest.json"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class NationalScience1991SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = QUESTION.read_text(encoding="utf-8")
        cls.answers = ANSWER.read_text(encoding="utf-8")
        cls.solution = SOLUTION.read_text(encoding="utf-8")

    def test_question_and_solution_numbering_are_complete(self):
        expected = [str(n) for n in range(1, 27)]
        self.assertEqual(re.findall(r"(?m)^\*\*(\d+)．\*\*$", self.questions), expected)
        self.assertEqual(re.findall(r"(?m)^### 第 (\d+) 题$", self.solution), expected)

    def test_every_question_has_one_answer_block(self):
        points = solution_sources.parse_answer_points(self.answers)
        self.assertEqual(len(points), 26)
        self.assertEqual(len(re.findall(r"(?m)^\*\*答案：", self.answers)), 26)

    def test_type_ranges_follow_the_source_question_boundaries(self):
        expected = {"选择题": [1, 15], "填空题": [16, 20], "解答题": [21, 26]}
        manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        paper = next(
            p for p in manifest["papers"]
            if p["paper_id"] == "gk-1991-regular-national-science"
        )
        index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        projected = next(p for p in index["papers"] if p["paper_id"] == paper["paper_id"])
        self.assertEqual(paper["index_metadata"]["structure"], expected)
        self.assertEqual(projected["structure"], expected)
        questions = solution_sources.parse_question_blocks(self.questions)
        self.assertTrue(questions[20].body.startswith("求函数"))
        self.assertTrue(questions[21].body.startswith("已知复数"))

    def test_math_source_documents_have_balanced_display_math_without_chinese_stop(self):
        for label, text in (
            ("试题", self.questions),
            ("答案", self.answers),
            ("解析", self.solution),
        ):
            in_display = False
            for line in text.splitlines():
                stripped = line.strip()
                if stripped == "$$":
                    in_display = not in_display
                elif not in_display and stripped == r"\[":
                    in_display = True
                elif in_display and stripped == r"\]":
                    in_display = False
                elif in_display:
                    self.assertNotIn("。", line, f"{label}把中文句号放进了数学模式")
            self.assertFalse(in_display, f"{label}的行间数学环境未配对")

    def test_choice_answers_and_high_risk_transcriptions(self):
        points = solution_sources.parse_answer_points(self.answers)
        self.assertEqual([points[i].answer_for(None) for i in range(15)], [
            "A", "D", "B", "B", "A", "D", "A", "D", "C", "C", "A", "C", "B", "C", "D",
        ])
        self.assertIn(r"\overline M\cup\overline N", self.questions)
        self.assertIn(r"\log_{a^2}x", self.questions)
        self.assertIn(r"\sqrt{\dfrac35}", self.questions)
        self.assertIn("1991全国理.pdf", self.questions)
        manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
        paper = next(
            record for record in manifest["papers"]
            if record["paper_id"] == "gk-1991-regular-national-science"
        )
        source_id = "src-46d610089dad2e2020d262785761b9cf06ab946f66af6c4d56adbb086f1bc21c"
        source = next(record for record in manifest["sources"] if record["source_id"] == source_id)
        self.assertIn(source_id, self.questions)
        self.assertEqual(paper["source_ids"], [source_id])
        self.assertEqual(source["paper_id"], paper["paper_id"])
        self.assertEqual(
            source["artifact"]["sha256"],
            "b2d5fd64fbae7b988c4a0ae36bba5006ff50f5ff1e64e12650b91dedfc99855c",
        )

    def test_derived_answers_are_not_mislabeled_official(self):
        self.assertIn("非官方", self.answers)
        self.assertIn("待独立复核", self.answers)
        self.assertIn("非官方", self.solution)
        points = solution_sources.parse_answer_points(self.answers)
        self.assertIn("奇数", points[24].answer_for(None))
        self.assertIn("偶数", points[24].answer_for(None))
        self.assertIn(r"x^2-\dfrac{y^2}3=1", points[25].answer_for(None))

    def test_combined_renderer_preserves_the_solution_body(self):
        combined = solution_sources.render_combined(self.questions, self.solution, self.answers)
        self.assertEqual(
            solution_sources.extract_solution_blocks(combined, self.questions),
            self.solution,
        )

    def test_q14_distance_locus_uses_both_shifted_lines(self):
        # |x+y+1| / sqrt(2) = sqrt(2) gives x+y+1 = +/-2.
        center = (-1, -2)
        radius_squared = 8
        distances_squared = [Fraction((sum(center) + k) ** 2, 2) for k in (-1, 3)]
        self.assertEqual(distances_squared, [radius_squared, 0])
        points = solution_sources.parse_answer_points(self.answers)
        self.assertEqual(points[13].answer_for(None), "C")
        section = self.solution.split("### 第 14 题", 1)[1].split("### 第 15 题", 1)[0]
        self.assertIn("x+y-1=0", section)
        self.assertIn("x+y+3=0", section)

    def test_q18_frustum_volume_from_linear_side_length(self):
        # h*sqrt(3)=2; integrate sqrt(3)/4 * side(t)^2 over the height.
        lower_side, upper_side = 4, 2
        mean_side_squared = Fraction(
            lower_side ** 2 + lower_side * upper_side + upper_side ** 2, 3
        )
        volume = Fraction(2, 4) * mean_side_squared
        self.assertEqual(volume, Fraction(14, 3))
        points = solution_sources.parse_answer_points(self.answers)
        self.assertIn(r"\dfrac{14}3", points[17].answer_for(None))

    def test_q19_binomial_coefficients_and_admissible_radical_root(self):
        self.assertEqual((comb(7, 2), comb(7, 3), comb(7, 4)), (21, 35, 35))
        # In Q(sqrt(10)), a = 1 + sqrt(10)/5 satisfies 5a^2-10a+3=0.
        rational, radical = Fraction(1), Fraction(1, 5)
        square_rational = rational ** 2 + 10 * radical ** 2
        square_radical = 2 * rational * radical
        self.assertEqual(5 * square_rational - 10 * rational + 3, 0)
        self.assertEqual(5 * square_radical - 10 * radical, 0)
        self.assertGreater(radical, 0)  # Only the plus root is greater than 1.
        points = solution_sources.parse_answer_points(self.answers)
        self.assertIn(r"1+\dfrac{\sqrt{10}}5", points[18].answer_for(None))

    def test_q23_plane_normal_and_squared_distance(self):
        e, f, g, b = (2, 0, 0), (0, 2, 0), (4, 4, 2), (4, 0, 0)
        ef = tuple(v - u for u, v in zip(e, f))
        eg = tuple(v - u for u, v in zip(e, g))
        normal = (
            ef[1] * eg[2] - ef[2] * eg[1],
            ef[2] * eg[0] - ef[0] * eg[2],
            ef[0] * eg[1] - ef[1] * eg[0],
        )
        dot = lambda v, w: sum(a * b for a, b in zip(v, w))
        plane_constant = dot(normal, e)
        self.assertEqual([dot(normal, p) for p in (e, f, g)], [plane_constant] * 3)
        distance_squared = Fraction((dot(normal, b) - plane_constant) ** 2, dot(normal, normal))
        self.assertEqual(distance_squared, Fraction(4, 11))
        points = solution_sources.parse_answer_points(self.answers)
        self.assertIn(r"\dfrac2{\sqrt{11}}", points[22].answer_for(None))

    def test_q25_geometric_sum_sign_domain_and_strict_boundary(self):
        points = solution_sources.parse_answer_points(self.answers)
        self.assertIn(r"n\ge1", points[24].answer_for(None))
        section = self.solution.split("### 第 25 题", 1)[1].split("### 第 26 题", 1)[0]
        self.assertIn("n=0", section)
        # Finite checks supplement the geometric-series identity in the proof.
        for n in range(1, 13):
            with self.subTest(n=n):
                coefficient = sum((-2) ** (k - 1) for k in range(1, n + 1))
                self.assertEqual(coefficient, Fraction(1 - (-2) ** n, 3))
                self.assertEqual(coefficient > 0, n % 2 == 1)
                # For a=2, the positive root of x^2-x-a is exactly 2.
                for x in (Fraction(-3), Fraction(1), Fraction(3, 2), Fraction(2), Fraction(3)):
                    in_domain = x > 0 and x * x - 2 > 0
                    reduced_inequality = in_domain and coefficient * (x - (x * x - 2)) > 0
                    expected = in_domain and (x < 2 if n % 2 else x > 2)
                    self.assertEqual(reduced_inequality, expected, (n, x))

    def test_q26_hyperbola_perpendicular_radii_and_chord_length(self):
        # 8u^2-14u+3 = (4u-1)(2u-3), and 0<u<1 leaves u=1/4.
        candidates = (Fraction(1, 4), Fraction(3, 2))
        self.assertTrue(all(8 * u * u - 14 * u + 3 == 0 for u in candidates))
        self.assertEqual([u for u in candidates if 0 < u < 1], [Fraction(1, 4)])
        a_squared, b_squared, c, slope_squared = Fraction(1), Fraction(3), Fraction(2), Fraction(3, 5)
        self.assertEqual(c * c, a_squared + b_squared)
        qa = b_squared - slope_squared * a_squared
        qb = 2 * slope_squared * a_squared * c
        qc = -a_squared * (b_squared + slope_squared * c * c)
        root_sum, root_product = -qb / qa, qc / qa
        difference_squared = root_sum * root_sum - 4 * root_product
        self.assertGreater(difference_squared, 0)
        dot_product = (
            (1 + slope_squared) * root_product
            - slope_squared * c * root_sum + slope_squared * c * c
        )
        self.assertEqual(dot_product, 0)
        self.assertEqual((1 + slope_squared) * difference_squared, 16)
        section = self.solution.split("### 第 26 题", 1)[1]
        self.assertIn("16x^2+8cx-9c^2=0", section)


if __name__ == "__main__":
    unittest.main()

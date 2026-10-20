import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT.parent / "2002"
QUESTIONS = PAPER / "2002_数学真题_北京文_试题.md"
ANSWERS = PAPER / "2002_数学真题_北京文_答案要点.md"
SOLUTIONS = PAPER / "2002_数学真题_北京文_解析正文.md"
RECORD = PAPER / "2002_北京文科_来源校对.json"
PROGRESS = ROOT / "PROGRESS.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class BeijingArts2002SolutionDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions_text = QUESTIONS.read_text(encoding="utf-8")
        cls.answers_text = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions_text = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.progress = PROGRESS.read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.questions_text)

    def test_answer_and_solution_sources_cover_and_align_all_questions(self):
        self.assertTrue(ANSWERS.is_file())
        self.assertTrue(SOLUTIONS.is_file())
        answer_points = solution_sources.parse_answer_points(self.answers_text)
        solution_blocks = solution_sources.validate_solution_body(self.solutions_text)
        self.assertEqual([q.number for q in self.questions], list(range(1, 23)))
        self.assertEqual([a.number for a in answer_points], list(range(1, 23)))
        self.assertEqual([s.number for s in solution_blocks], list(range(1, 23)))
        self.assertEqual([q.subparts for q in self.questions], [a.subparts for a in answer_points])
        self.assertEqual([q.subparts for q in self.questions], [s.subparts for s in solution_blocks])
        rendered = solution_sources.render_combined(
            self.questions_text, self.solutions_text, self.answers_text
        )
        self.assertEqual(len(solution_sources.parse_question_blocks(rendered)), 22)

    def test_answers_are_hash_bound_and_never_mislabeled_as_official(self):
        generated = self.record["generated_solution"]
        self.assertEqual(self.record["official_answer"], None)
        self.assertEqual(self.record["source"]["contains_answers"], False)
        self.assertFalse(generated["is_official"])
        self.assertEqual(generated["status"], "draft-generated-needs-independent-review")
        self.assertEqual(
            self.record["answer_key"]["sha256"],
            hashlib.sha256(ANSWERS.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            self.record["solution_body"]["sha256"],
            hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest(),
        )
        self.assertIn("独立推导", self.answers_text)
        self.assertTrue("尚未经过异人独立数学盲核" in self.solutions_text, "solution draft must remain unverified")

    def test_choice_key_matches_hand_derived_results(self):
        answer_points = solution_sources.parse_answer_points(self.answers_text)
        actual = [(answer_points[n - 1].answer_for(None) or "").removesuffix("。") for n in range(1, 13)]
        self.assertEqual(actual, list("CDBACBDABDCA"))

    def test_exact_arithmetic_and_geometry_results_are_preserved(self):
        answer_points = solution_sources.parse_answer_points(self.answers_text)
        expected = {
            13: r"\cos\frac{6\pi}{5}<\sin\frac{2\pi}{5}<\tan\frac{7\pi}{5}",
            14: "4",
            15: "①②③④⑤",
            16: "2",
            17: r"\left[\frac12,5\right)",
        }
        for number, value in expected.items():
            with self.subTest(question=number):
                self.assertIn(value, answer_points[number - 1].answer_for(None) or "")
        self.assertIn(r"\tan\theta=\dfrac{2h}{b-d}", answer_points[17].answer_for(1) or "")
        self.assertIn(r"V_{\mathrm{估}}<V", answer_points[17].answer_for(2) or "")
        self.assertIn("至少2个单位时间", answer_points[19].answer_for(1) or "")
        self.assertIn("第二轮：1读3、2读4、3读1、4读2", answer_points[19].answer_for(1) or "")
        self.assertIn("7个单位时间", answer_points[19].answer_for(2) or "")
        self.assertIn(r"3\left(b-\frac12\right)^2+c^2=\frac34", answer_points[20].answer_for(2) or "")
        self.assertIn(r"u_n=n2^n", answer_points[21].answer_for(3) or "")
        self.assertIn(r"(a-c)(d-b)", self.solutions_text)
        self.assertIn("H=3G-2F", self.solutions_text)
        self.assertIn("正三角形，$F=H$", self.solutions_text)
        self.assertIn(r"u_0=f(1)=0", self.solutions_text)
        self.assertIn(r"\cos2\theta=\frac{\cot^2\theta-1}{\cot^2\theta+1}=\frac35", self.solutions_text)
        self.assertIn(r"m^2=8n^2", self.solutions_text)
        self.assertIn(r"\pm\frac{\sqrt3}{4}x", self.solutions_text)
        self.assertIn("③与④虽然文字重复", self.solutions_text)
        self.assertIn(r"(n+2)2^n>0", answer_points[21].answer_for(3) or "")

    def test_q4_orthogonality_uses_orthonormal_cube_edge_coordinates(self):
        dot = lambda u, v: sum(a * b for a, b in zip(u, v))
        option_directions = {
            "A": ((1, -1, -1), (0, -1, 1)),
            "B": ((0, -1, -1), (1, -1, 0)),
            "C": ((0, -1, 1), (0, -1, 0)),
            "D": ((1, -1, -1), (0, -1, 0)),
        }
        products = {option: dot(*directions) for option, directions in option_directions.items()}
        self.assertEqual(products, {"A": 0, "B": 1, "C": 1, "D": 1})
        answers = solution_sources.parse_answer_points(self.answers_text)
        self.assertEqual((answers[3].answer_for(None) or "").removesuffix("。"), "A")

    def test_progress_records_solution_stage_without_claiming_paper_acceptance(self):
        self.assertTrue("2002 北京文科卷：非官方答案与解析草稿完成" in self.progress, "progress receipt is missing")
        self.assertTrue("test_2002_beijing_arts_solutions.py" in self.progress, "progress receipt omits the test")
        self.assertTrue("仍未完成整卷验收" in self.progress, "progress must not claim final acceptance")
        self.assertTrue("2002 北京文科卷：独立盲解分歧定向裁定" in self.progress, "review adjudication is not recorded")
        self.assertTrue("整体数学验证仍为`not-verified`" in self.progress, "progress must retain the partial-review boundary")


if __name__ == "__main__":
    unittest.main()

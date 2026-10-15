"""Integrity and derivation checks for generated 1994 national science solutions."""
import hashlib
import json
import re
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "1994_全国卷_理科"
QUESTIONS = PAPER / "题面转录草稿.md"
SOLUTIONS = PAPER / "解答草稿.md"
RECORD = PAPER / "来源校对.json"


class NationalScience1994MathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(RECORD.read_text(encoding="utf-8"))
        cls.text = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""
        cls.headings = [
            int(number)
            for number in re.findall(r"^\*\*(\d+)．\*\*", cls.text, flags=re.MULTILINE)
        ]
        cls.outcomes = {
            int(number): (kind, result.strip().strip("$").rstrip("。"))
            for number, kind, result in re.findall(
                r"^\*\*(\d+)．\*\*\s+\*\*(答案|待核|结论)：(.*?)\*\*",
                cls.text,
                flags=re.MULTILINE,
            )
        }

    def test_every_question_has_a_generated_solution_or_explicit_pending_state(self):
        self.assertTrue(SOLUTIONS.is_file(), "generated solution draft is missing")
        self.assertEqual(self.headings, list(range(1, 26)))
        self.assertEqual(set(self.outcomes), set(range(1, 26)))
        self.assertEqual([n for n, (kind, _) in self.outcomes.items() if kind == "待核"], [])

    def test_generated_solutions_are_bound_to_this_draft_and_not_official(self):
        generated = self.record.get("generated_solution", {})
        self.assertEqual(generated.get("path"), "解答草稿.md")
        self.assertEqual(generated.get("question_draft_sha256"), hashlib.sha256(QUESTIONS.read_bytes()).hexdigest())
        self.assertEqual(generated.get("sha256"), hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest())
        self.assertEqual(generated.get("status"), "pending-independent-review")
        self.assertEqual(generated.get("question_numbers"), list(range(1, 26)))
        self.assertEqual(generated.get("unresolved_question_numbers"), [])
        self.assertEqual(generated.get("choice_key"), [
            "D", "D", "D", "A", "B", "D", "B", "A", "A", "C", "C", "B", "D", "B", "C"
        ])
        self.assertFalse(generated.get("official"))
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["mathematical_verification_status"], "not-verified")

    def test_hand_derived_answers_include_the_source_specific_conclusions(self):
        if not SOLUTIONS.is_file():
            self.fail("generated solution draft is missing")
            return
        expected = {
            1: ("答案", "D"), 2: ("答案", "D"), 3: ("答案", "D"),
            4: ("答案", "A"), 5: ("答案", "B"), 6: ("答案", "D"),
            7: ("答案", "B"), 8: ("答案", "A"), 9: ("答案", "A"),
            10: ("答案", "C"), 11: ("答案", "C"), 12: ("答案", "B"),
            13: ("答案", "D"), 14: ("答案", "B"), 15: ("答案", "C"),
            16: ("答案", "-189"), 18: ("答案", "-\\dfrac34"),
            23: ("答案", "45^\\circ"),
        }
        for number, outcome in expected.items():
            with self.subTest(question=number):
                self.assertEqual(self.outcomes[number], outcome)
        self.assertIn(r"(x-2)^2+y^2=1", self.text)
        self.assertIn(r"\frac{2\sqrt2\pi}{3}", self.text)
        self.assertIn(r"y=\dfrac{1+\sqrt5}{2}x", self.text)
        self.assertIn(r"y^2=\dfrac4{\sqrt5}x", self.text)
        self.assertIn(r"a_n=4n-2", self.text)
        self.assertIn(r"\omega=\sqrt{26}", self.text)
        self.assertIn("a=-1,b=2", self.text)
        self.assertIn("a_1=2,a_2=6,a_3=10", self.text)
        self.assertIn("极限为1", self.text)

    def test_high_risk_proofs_show_the_required_sign_and_domain_reasoning(self):
        if not SOLUTIONS.is_file():
            self.fail("generated solution draft is missing")
            return
        required = (
            "焦点在 $y$ 轴上",
            r"x^2+y^2=\frac{x+y}{\sqrt2}",
            r"x_1\ne x_2",
            r"\frac34R^2=\frac43",
            r"\theta\in(0,\pi)",
            "严格凸",
            "棱柱高",
            "正半轴",
            "等差中项",
            "等比中项",
            "负号分支",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.text)

    def test_exact_checks_for_combinatorics_geometry_and_telescoping(self):
        self.assertEqual(10 * 9 // 2 * 8 * 7, 2520)
        radius2 = F(16, 9)
        section_radius2 = F(4, 3)
        self.assertEqual(radius2 - section_radius2, F(4, 9))
        self.assertEqual(F(3, 4) * radius2, section_radius2)

        # Q18: both roots satisfy the squared equation, but only one keeps the
        # original positive value of sin(theta)+cos(theta).
        roots = (F(-3, 4), F(-4, 3))
        sums = {
            F(-3, 4): F(4, 5) - F(3, 5),
            F(-4, 3): F(3, 5) - F(4, 5),
        }
        self.assertEqual(sums[roots[0]], F(1, 5))
        self.assertEqual(sums[roots[1]], F(-1, 5))

        # Q23: exact squared cosine between the two plane normals is 1/2.
        h2 = F(1, 2)
        dot2 = (F(3, 4) * h2) ** 2
        norm_p2 = (12 * h2 + 3) / 16
        norm_q2 = h2
        self.assertEqual(dot2 / (norm_p2 * norm_q2), F(1, 2))

        # Q24: slope satisfies the golden-ratio quadratic; the positive root
        # is selected by the reflected points lying on the positive-x parabola.
        t = (1 + 5 ** 0.5) / 2
        self.assertAlmostEqual(t * t - t - 1, 0)

        # Q25 telescopes exactly to 1 - 1/(2n+1).
        n = 40
        partial = sum(
            (F(1, 2 * k - 1) - F(1, 2 * k + 1) for k in range(1, n + 1)),
            F(0),
        )
        self.assertEqual(partial, 1 - F(1, 2 * n + 1))


if __name__ == "__main__":
    unittest.main()

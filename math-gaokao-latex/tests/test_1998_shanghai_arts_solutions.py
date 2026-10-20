"""Exact-arithmetic regression checks for the 1998 Shanghai arts solution draft."""
import json
import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
PROJECT = ROOT / "math-gaokao-latex"
sys.path.insert(0, str(PROJECT / "tools"))
import issues as issue_ledger

PAPER = ROOT / "math-gaokao-latex/1998_上海卷_文科"
DRAFT = PAPER / "解析草稿.md"
ANSWERS = PAPER / "答案要点草稿.md"
QUESTIONS = PAPER / "题面转录草稿.md"


class Shanghai1998ArtsSolutionTests(unittest.TestCase):
    def test_q20_chord_area_forces_the_two_reported_slopes(self):
        # For y=k(x-2) on y^2=4(x-1), the triangle area is
        # 2*sqrt(1+k^2)/|k|.  Squaring area=4 gives k^2=1/3.
        k_squared = Fraction(1, 3)
        area_squared = 4 * (1 + k_squared) / k_squared
        self.assertEqual(area_squared, 16)
        self.assertAlmostEqual(math.tan(math.pi / 6) ** 2, float(k_squared))
        self.assertAlmostEqual(math.tan(5 * math.pi / 6) ** 2, float(k_squared))

    def test_q21_cubic_satisfies_measurements_extrema_and_average(self):
        temperature = lambda t: t**3 - 3 * t + 60
        derivative = lambda t: 3 * t**2 - 3
        self.assertEqual((temperature(-4), temperature(0), temperature(1)), (8, 60, 58))
        self.assertEqual(derivative(-4), derivative(4))
        candidates = [temperature(t) for t in (-2, -1, 1, 2)]
        self.assertEqual(max(candidates), 62)
        self.assertEqual((temperature(-1), temperature(2)), (62, 62))
        # Exact antiderivative evaluation on [-4,4].
        integral = Fraction(4**4 - (-4) ** 4, 4) - (4**2 - (-4) ** 2) + 60 * (4 - (-4))
        average = Fraction(1, 8) * integral
        self.assertEqual(average, 60)

    def test_q22_sequence_identities_and_limits_are_consistent(self):
        for n in range(1, 12):
            a_n = Fraction(-(2 * n + 3), 2)
            b_n = Fraction(-(12 * n + 5), 4)
            sum_a = sum((Fraction(-(2 * j + 3), 2) for j in range(1, n + 1)), Fraction())
            sum_b = sum((Fraction(-(12 * j + 5), 4) for j in range(1, n + 1)), Fraction())
            self.assertEqual(4 * sum_b - 12 * sum_a, 13 * n)
            self.assertEqual(2 * a_n, -2 * n - 3)
            self.assertEqual(4 * b_n, -12 * n - 5)
            self.assertEqual(sum(2 * j + 3 for j in range(1, n + 1)), n**2 + 4 * n)
        # Leading coefficients of sum(k_i) and a_n*b_n are 1 and 24/8.
        numerator_lead = Fraction(1)
        denominator_lead = Fraction(2 * 12, 8)
        self.assertEqual(numerator_lead / denominator_lead, Fraction(1, 3))

    def test_drafts_preserve_source_discrepancies_and_unverified_status(self):
        draft = DRAFT.read_text(encoding="utf-8")
        answers = ANSWERS.read_text(encoding="utf-8")
        questions = QUESTIONS.read_text(encoding="utf-8")
        self.assertIn("不能保证唯一正确选项", draft)
        self.assertIn("a=7", draft)
        self.assertIn("选A", draft)
        self.assertIn("A、D", answers)
        self.assertIn("ISSUE-1115", answers)
        self.assertIn("经过第三象限", draft)
        self.assertIn("123.6", draft)
        self.assertIn(r"\theta=\arccos\!\left(\frac{7\sqrt{10}}{40}\right)", draft)
        self.assertIn("原题未另作定义", draft)
        self.assertIn("y=a(x-a_n)^2+b_n", questions)
        self.assertIn("不能标作官方答案", answers)
        self.assertNotIn("canonical", draft)
        self.assertNotIn("complete", draft)

    def test_q15_source_options_have_counterexamples_when_a_is_five(self):
        # A=(-inf,-1) U (6,inf), B=(0,10); each witness is outside the
        # corresponding union in the order transcribed from the fixed scan.
        a_contains = lambda x: x < -1 or x > 6
        b_contains = lambda x: 0 < x < 10
        self.assertFalse((not a_contains(-2)) or b_contains(-2))
        self.assertFalse(a_contains(1) or (not b_contains(1)))
        self.assertFalse((not a_contains(7)) or (not b_contains(7)))
        self.assertFalse(a_contains(0) or b_contains(0))
        # But a=7 is also allowed: B=(-2,12) contains complement(A)=[-1,6],
        # so both options A and D hold. The item does not determine one answer.
        a = 7
        self.assertGreater(a, 4)  # equivalent to 1 in (5-a, 5+a)
        self.assertLess(5 - a, -1)
        self.assertGreater(5 + a, 6)

    def test_q15_source_issue_is_linked_without_inventing_paper_identity(self):
        manifest = json.loads(
            (PROJECT / "source-manifest.json").read_text(encoding="utf-8")
        )
        source_id = "src-8c86b3e592e594953609fe09d0c182d5252c944006503dfb10e8efa1962aeca7"
        source = next(
            item for item in manifest["sources"]
            if item["source_id"] == source_id
        )
        self.assertIsNone(source["paper_id"])
        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["issue_ids"], ["ISSUE-1115"])

        issue = next(
            item for item in issue_ledger.load_issues(PROJECT / "missing-issues.md")
            if item["issue_id"] == "ISSUE-1115"
        )
        self.assertEqual(issue["source_id"], source_id)
        self.assertIsNone(issue["paper_id"])
        self.assertEqual(issue["type"], "source-mismatch")
        self.assertEqual(issue["status"], "open")
        self.assertEqual(issue["impact"], "blocks_completion")

    def test_q19_2_distinguishes_directed_vector_angle_from_line_angle(self):
        left = (0, 2, 6)
        right = (math.sqrt(3), 2, -3)
        dot = sum(a * b for a, b in zip(left, right))
        norm_product = math.sqrt(sum(x * x for x in left) * sum(x * x for x in right))
        self.assertEqual(dot, -14)
        cosine = dot / norm_product
        self.assertLess(cosine, 0)
        self.assertAlmostEqual(abs(cosine), 7 * math.sqrt(10) / 40)
        line_angle = math.acos(abs(cosine))
        self.assertLess(line_angle, math.pi / 2)
        self.assertAlmostEqual(math.degrees(line_angle), 56.4, delta=0.1)

    def test_q6_activity_network_critical_path_is_eleven_days(self):
        edges = (
            (1, 2, 2), (1, 3, 0), (2, 5, 3), (3, 4, 3),
            (4, 5, 0), (4, 6, 1), (5, 6, 0), (5, 7, 3),
            (6, 7, 4), (7, 8, 2),
        )
        earliest = {1: 0}
        for event in range(1, 9):
            for start, end, duration in edges:
                if start == event:
                    earliest[end] = max(earliest.get(end, 0), earliest[event] + duration)
        self.assertEqual(earliest[8], 11)
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn("关键路径为$1\\to2\\to5\\to6\\to7\\to8$", draft)
        self.assertIn("$2+3+0+4+2=11$天", draft)


if __name__ == "__main__":
    unittest.main()

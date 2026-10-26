"""1997 全国文科项目独立解答草稿与未决边界的定向回归检查。"""

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / '1997_全国卷_文科'
DRAFTS = ROOT.parent / '1997'
ANSWER = DRAFTS / '1997_数学真题_全国文_答案要点.md'
SOLUTION = DRAFTS / '1997_数学真题_全国文_解析正文.md'
INDEPENDENT_DRAFT = DRAFTS / '1997_数学真题_全国文_独立解答草稿.md'


class NationalArts1997MathDraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((PAPER / '来源校对.json').read_text(encoding='utf-8'))
        cls.answer = ANSWER.read_text(encoding='utf-8')
        cls.solution = SOLUTION.read_text(encoding='utf-8')
        cls.independent_draft = INDEPENDENT_DRAFT.read_text(encoding='utf-8')

    def test_answer_and_solution_fingerprints_match_record(self):
        self.assertEqual(self.record['artifacts']['answer_draft']['path'], '../../1997/1997_数学真题_全国文_答案要点.md')
        self.assertEqual(self.record['artifacts']['solution_draft']['path'], '../../1997/1997_数学真题_全国文_解析正文.md')
        self.assertEqual(self.record['artifacts']['answer_draft']['sha256'], hashlib.sha256(ANSWER.read_bytes()).hexdigest())
        self.assertEqual(self.record['artifacts']['solution_draft']['sha256'], hashlib.sha256(SOLUTION.read_bytes()).hexdigest())
        self.assertEqual(self.record['artifacts']['independent_solution_draft']['path'], '../../1997/1997_数学真题_全国文_独立解答草稿.md')
        self.assertEqual(self.record['artifacts']['independent_solution_draft']['sha256'], hashlib.sha256(INDEPENDENT_DRAFT.read_bytes()).hexdigest())

    def test_answer_key_covers_all_questions_and_keeps_source_gap(self):
        for number in range(1, 23):
            self.assertIn(f'| {number} |', self.answer)
        self.assertIn('| 24(1) |', self.answer)
        self.assertIn('| 24(2) |', self.answer)
        self.assertIn('| 25 |', self.answer)
        self.assertIn('| 23(3) |', self.answer)
        self.assertIn('未决', self.answer)
        self.assertIn('Q23(3)', self.answer)
        self.assertIn('Q23(3)', self.solution)
        self.assertIn('不是官方', self.answer)
        self.assertIsNone(self.record['official_answer'])
        self.assertIsNone(self.record['paper_id'])
        self.assertFalse(self.record['canonical_question_source_ready'])
        self.assertEqual(self.record['transcription_status'], 'incomplete-source-gap-q23-relation')

    def test_q15_exact_rational_determinant_count(self):
        points = {
            'B': (Fraction(1), Fraction(0), Fraction(0)),
            'C': (Fraction(0), Fraction(1), Fraction(0)),
            'D': (Fraction(0), Fraction(0), Fraction(1)),
            'AB': (Fraction(1, 2), Fraction(0), Fraction(0)),
            'AC': (Fraction(0), Fraction(1, 2), Fraction(0)),
            'AD': (Fraction(0), Fraction(0), Fraction(1, 2)),
            'BC': (Fraction(1, 2), Fraction(1, 2), Fraction(0)),
            'BD': (Fraction(1, 2), Fraction(0), Fraction(1, 2)),
            'CD': (Fraction(0), Fraction(1, 2), Fraction(1, 2)),
        }

        def determinant(a, b, c):
            return (a[0] * (b[1] * c[2] - b[2] * c[1])
                    - a[1] * (b[0] * c[2] - b[2] * c[0])
                    + a[2] * (b[0] * c[1] - b[1] * c[0]))

        counts = [0, 0, 0, 0]
        midpoints = {'AB', 'AC', 'AD'}
        for group in itertools.combinations(points, 3):
            if determinant(*(points[name] for name in group)) == 0:
                counts[sum(name in midpoints for name in group)] += 1
        self.assertEqual(counts, [3, 21, 9, 0])
        self.assertEqual(sum(counts), 33)
        self.assertIn('33 组', self.answer)

    def test_q21_both_signed_geometric_means_satisfy_arithmetic_conditions(self):
        cases = [(Fraction(4), Fraction(-12, 5)), (Fraction(-3), Fraction(16, 5))]
        for first, difference in cases:
            x = first + difference
            y = first + Fraction(3, 2) * difference
            self.assertEqual((x + y) / 2, 1)
            self.assertEqual((first / 5) ** 2, x * y)
        self.assertIn(r'\frac{16}{5}', self.answer)
        self.assertIn('负', self.solution)

    def test_q23_relationship_is_not_fabricated(self):
        issue, = self.record['source_issues']
        self.assertEqual((issue['question_number'], issue['subpart'], issue['status']), (23, 3, 'unresolved'))
        self.assertIn('若关系为垂直', self.solution)
        self.assertNotIn('official_answer', self.solution)


if __name__ == '__main__':
    unittest.main()

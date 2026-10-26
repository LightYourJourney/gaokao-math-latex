"""1997 全国文科固定来源草稿的可追溯性检查，不作数学或整卷验收。"""

import hashlib
import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / '1997_全国卷_文科'
SOURCE_ID = 'src-c2f96b8723b85758e1407771ee05f1bb5c457c71a0bc567c01f84ea8c3fadbd9'
SOURCE_SHA = '16fdb675583e09b4e3353e9903365aa152e21e3327b24a56b0101dbff5ceb6e9'
sys.path.insert(0, str(ROOT / 'tools'))
import solution_sources
sys.path.insert(0, str(ROOT.parent / 'math-gaokao-2017-2026' / 'tools'))
import md2tex


class NationalArts1997SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((PAPER / '来源校对.json').read_text(encoding='utf-8'))
        cls.text = (PAPER / '题面转录草稿.md').read_text(encoding='utf-8')
        cls.questions = solution_sources.parse_question_blocks(cls.text)

    def test_fixed_source_identity_and_unbound_review_state(self):
        manifest = json.loads((ROOT / 'source-manifest.json').read_text(encoding='utf-8'))
        source = next(s for s in manifest['sources'] if s['source_id'] == SOURCE_ID)
        self.assertEqual(source['upstream_path'], '普通高考/1997/1997全国文.pdf')
        self.assertEqual(source['source_state'], 'ready')
        self.assertEqual(source['artifact']['sha256'], SOURCE_SHA)
        self.assertEqual(source['artifact']['page_count'], 1)
        self.assertEqual(source['git_blob_oid'], self.record['git_blob_oid'])
        self.assertIsNone(source['paper_id'])
        self.assertEqual(self.record['source_id'], SOURCE_ID)
        self.assertEqual(self.record['pdf_sha256'], SOURCE_SHA)
        self.assertIsNone(self.record['paper_id'])
        self.assertFalse(self.record['canonical_question_source_ready'])
        self.assertEqual(self.record['review_status'], 'needs-review')

    def test_all_question_ids_and_body_fingerprints_are_stable(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 26)))
        self.assertEqual(self.record['question_count'], 25)
        rows = self.record['question_sources']
        self.assertEqual(len(rows), 25)
        for question, row in zip(self.questions, rows):
            self.assertEqual(row['question_number'], question.number)
            self.assertEqual(row['question_id'], SOURCE_ID + f':q{question.number:03d}')
            self.assertEqual(row['body_sha256'], hashlib.sha256(question.body.encode()).hexdigest())
            self.assertEqual(row['source_pages'], [1])
        self.assertEqual(self.record['question_draft']['sha256'],
                         hashlib.sha256((PAPER / '题面转录草稿.md').read_bytes()).hexdigest())

    def test_choice_options_type_ranges_and_unknown_scores(self):
        for question in self.questions[:15]:
            self.assertEqual(re.findall(r'（([ABCD])）', question.body), list('ABCD'))
        self.assertEqual(self.record['question_type_ranges'],
                         {'single-choice': [1, 15], 'fill-in': [16, 19], 'solution': [20, 25]})
        self.assertIsNone(self.record['total_score'])
        self.assertIn('分组为项目编辑结构', self.text)

    def test_high_risk_roots_absolute_values_and_missing_native_symbols(self):
        q = {item.number: item.body for item in self.questions}
        self.assertIn(r'\dfrac12x-\dfrac\pi3', q[3])
        self.assertIn(r'AB=AC=\sqrt3', q[4])
        self.assertIn(r'\left[\dfrac\pi4,\dfrac\pi2\right)', q[6])
        self.assertIn(r'\left|\dfrac{2-x}{2+x}\right|', q[14])
        self.assertIn(r'\sqrt{\dfrac x2}', q[16])
        self.assertIn(r'\alpha\parallel\beta', q[19])
        self.assertIn(r'm\parallel l', q[19])
        self.assertIn(r'z\omega+z\omega^3', q[20])
        self.assertIn(r'\dfrac{\sqrt5}{5}', q[25])

    def test_missing_relation_is_preserved_without_inventing_perpendicularity(self):
        q23 = self.questions[22].body
        part3 = q23.split('（3）', 1)[1].split('（4）', 1)[0]
        self.assertIn('面 $AED$ 面 $A_1FD_1$', part3)
        self.assertNotIn(r'\perp', part3)
        self.assertIn('来源缺口', part3)
        self.assertEqual(self.record['complete_question_count'], 24)
        self.assertEqual(self.record['transcription_status'], 'incomplete-source-gap-q23-relation')
        issue, = self.record['source_issues']
        self.assertEqual((issue['question_number'], issue['subpart'], issue['status']), (23, 3, 'unresolved'))
        self.assertEqual(self.record['question_sources'][22]['review_status'], 'needs-source-recovery')

    def test_no_official_answer_is_fabricated_and_project_review_is_labeled(self):
        self.assertFalse(self.record['source_has_answers'])
        self.assertFalse(self.record['source_has_solutions'])
        self.assertIsNone(self.record['official_answer'])
        self.assertEqual(self.record['generated_solution']['attribution'], 'project-independent-derivation')
        self.assertTrue(self.record['generated_solution']['independent_review'])
        self.assertEqual(self.record['mathematical_verification_status'], 'conditionally-reviewed-with-source-conditions')

    def test_registered_figures_are_self_contained_vectors_and_convert_strictly(self):
        figures = self.record['figure_files']
        self.assertEqual([f['question_number'] for f in figures], [3, 23])
        figure_map = {}
        for item in figures:
            path = PAPER / item['path']
            self.assertEqual(path.suffix, '.tex')
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), item['sha256'])
            text = path.read_text(encoding='utf-8')
            for forbidden in [r'\includegraphics', r'\input', r'\write18', r'\documentclass']:
                self.assertNotIn(forbidden, text)
            self.assertEqual(text.count(r'\begin{tikzpicture}'), 1)
            self.assertEqual(self.text.count(f"]({item['path']})"), 1)
            figure_map[item['path']] = path.stem
        converted = md2tex.convert_markdown(self.text, md2tex.ConversionContext(figure_map=figure_map, strict=True))
        self.assertEqual(converted.warnings, ())
        self.assertEqual(set(converted.referenced_figures), set(figure_map.values()))

    def test_progress_records_incomplete_source_and_next_action(self):
        progress = (ROOT / 'PROGRESS.md').read_text(encoding='utf-8')
        stage = re.search(r'(?ms)^## 1997 全国文科：固定来源25题草稿与Q23缺符号登记.*?(?=^## |\Z)', progress)
        self.assertIsNotNone(stage)
        for value in ['已完成：', '修改文件：', '验证：', '剩余/下一步：', 'Q23']:
            self.assertIn(value, stage.group(0))


if __name__ == '__main__':
    unittest.main()

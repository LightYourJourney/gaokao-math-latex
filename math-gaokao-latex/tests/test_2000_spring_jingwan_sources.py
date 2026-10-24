"""固定源逐题定位与矢量图登记完整性回归。"""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class JingwanSourceIntegrityTests(unittest.TestCase):
    def test_question_locations_and_identity_match_registered_papers(self):
        manifest = json.loads((ROOT / 'source-manifest.json').read_text())
        for track, cn, first_column_last in [('arts', '文', 11), ('science', '理', 10)]:
            pid = f'gk-2000-spring-jingwan-{track}'
            paper = next(p for p in manifest['papers'] if p['paper_id'] == pid)
            record = json.loads((ROOT / paper['project_dir'] / '来源校对.json').read_text())
            provenance = json.loads((ROOT / paper['project_dir'] / 'provenance.json').read_text())
            source = next(s for s in manifest['sources'] if s['source_id'] == record['source_id'])
            with self.subTest(paper=pid):
                self.assertEqual(record['paper_id'], pid)
                self.assertEqual(record['pdf_sha256'], source['artifact']['sha256'])
                self.assertEqual(record['git_blob_oid'], source['git_blob_oid'])
                self.assertFalse(record['source_has_answers'])
                qs = record['question_sources']
                self.assertEqual([q['question_number'] for q in qs], list(range(1,25)))
                self.assertEqual([q['question_id'] for q in qs], [q['question_id'] for q in provenance['questions']])
                expected = [(1,1)] * first_column_last + [(1,2)] * (19-first_column_last) + [(1,3)]*2 + [(2,1),(2,2),(2,3)]
                self.assertEqual([(q['source_page'],q['column']) for q in qs], expected)
                self.assertEqual({i['question_number'] for i in record['source_issues']}, {18,24 if track=='arts' else 23})

    def test_vector_figures_are_bound_and_solution_graph_is_separate(self):
        for cn in ['文','理']:
            project = ROOT / f'2000_春季京皖{cn}卷'
            record = json.loads((project/'来源校对.json').read_text())
            for f in record['figure_files']:
                self.assertEqual(hashlib.sha256((project/f['path']).read_bytes()).hexdigest(),f['sha256'])
        project = ROOT/'2000_春季京皖理卷'
        name = 'f2000_spring_jingwan_science_q24_solution'
        questions = (project/'questions.tex').read_text()
        answers = (project/'answers.tex').read_text()
        self.assertNotIn(name, questions)
        self.assertEqual(answers.count('\\input{figures/'+name+'}'),1)
        self.assertTrue((project/'figures'/f'{name}.tex').is_file())

if __name__ == '__main__':
    unittest.main()

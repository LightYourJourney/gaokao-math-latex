"""1989 广东理科规范源必须完整对齐并与来源答案保持清晰归属。"""
from pathlib import Path
import math
import re
import sys
import unittest
import json
import shutil
import subprocess
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
EXAMS = PROJECT.parent
QUESTIONS = EXAMS / '1989' / '1989_数学真题_广东理_试题.md'
ANSWERS = EXAMS / '1989' / '1989_数学真题_广东理_答案要点.md'
SOLUTIONS = EXAMS / '1989' / '1989_数学真题_广东理_解析正文.md'
ISSUES = PROJECT / 'missing-issues.md'
FIGURES = PROJECT / '1989_广东卷_理科' / 'figures'
sys.path.insert(0, str(PROJECT / 'tools'))
import issues
import solution_sources
import make_short_answers
import generate_projects
import build_projects


class GuangdongScience1989CanonicalSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions_text = QUESTIONS.read_text(encoding='utf-8')
        cls.answers_text = ANSWERS.read_text(encoding='utf-8')
        cls.solutions_text = SOLUTIONS.read_text(encoding='utf-8')

    def test_question_source_has_30_blocks_and_original_second_volume_labels(self):
        blocks = solution_sources.parse_question_blocks(self.questions_text)
        self.assertEqual(len(blocks), 30)
        self.assertEqual([block.number for block in blocks], list(range(1, 31)))
        self.assertEqual([block.printed_label for block in blocks[25:]],
                         ['一', '二', '三', '四', '五'])
        self.assertEqual([block.subparts for block in blocks[25:]],
                         [(1, 2, 3, 4, 5), (1, 2), (1, 2), (1, 2), (1, 2)])

    def test_source_notes_do_not_leak_into_printable_question_copy(self):
        self.assertNotIn('来源第1页此处确实', self.questions_text)
        self.assertNotIn('这是待重绘图稿的内容索引', self.questions_text)
        self.assertIn('printed-label: 一', self.questions_text)
        self.assertIn('3x-4y-12=0', self.questions_text)

    def test_q19_and_q30_preserve_the_source_tangent_notation(self):
        blocks = solution_sources.parse_question_blocks(self.questions_text)
        self.assertIn(r'\operatorname{tg}', blocks[18].body)
        self.assertNotIn(r'\tan', blocks[18].body)
        self.assertIn(r'\operatorname{tg}', blocks[29].body)
        self.assertNotIn(r'\tan', blocks[29].body)

    def test_q21_solution_covers_all_coterminal_third_quadrant_angles(self):
        blocks = solution_sources.validate_solution_body(self.solutions_text)
        q21 = blocks[20].body
        self.assertIn(r'\theta=\theta_0+2k\pi', q21)
        self.assertIn(r'$k$ 为偶数', q21)
        self.assertIn('第二象限', q21)

    def test_q8_solution_does_not_resolve_ambiguous_source_wording_by_assumption(self):
        blocks = solution_sources.validate_solution_body(self.solutions_text)
        q8 = blocks[7].body
        self.assertIn('字面不能唯一确定抛物线对称轴的方位', q8)
        self.assertIn('若将其理解为对称轴为 $x$ 轴', q8)

    def test_q8_interpretation_ambiguity_is_a_blocking_answer_issue(self):
        matches = [issue for issue in issues.load_issues(ISSUES)
                   if issue.get('paper_id') == 'gk-1989-regular-guangdong-science'
                   and issue.get('question_id') ==
                   'gk-1989-regular-guangdong-science-q08'
                   and issue.get('type') == 'answer-conflict']
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]['status'], 'open')
        self.assertEqual(matches[0]['impact'], 'blocks_completion')

    def test_q30_solution_uses_completed_square_radius(self):
        blocks = solution_sources.validate_solution_body(self.solutions_text)
        q30 = blocks[29].body
        question = solution_sources.parse_question_blocks(self.questions_text)[29].body
        self.assertIn(r'x^2+y^2-2x', question)
        self.assertNotIn(r'-x^2+y^2', question)
        self.assertIn(r'(x-t^2)^2+(y-t)^2=t^2', q30)
        self.assertIn(r'半径为 $t$', q30)

    def test_q30_proof_and_final_answers_share_the_last_detailed_page(self):
        manifest = json.loads((PROJECT / 'source-manifest.json').read_text(encoding='utf-8'))
        paper = next(p for p in manifest['papers']
                     if p['paper_id'] == 'gk-1989-regular-guangdong-science')
        with tempfile.TemporaryDirectory(prefix='gk1989-layout-') as temporary:
            root = Path(temporary)
            project_copy = root / 'docs' / 'exams' / 'math-gaokao-latex'
            project_copy.mkdir(parents=True)
            shutil.copytree(PROJECT / 'common', project_copy / 'common')
            shutil.copytree(
                PROJECT / paper['project_dir'],
                project_copy / paper['project_dir'],
                ignore=shutil.ignore_patterns('build', 'receipts', '.work'),
            )
            toolchain = build_projects.resolve_toolchain()
            result = build_projects.build_target(
                root,
                paper['project_dir'],
                '解析版',
                toolchain,
            )
            pdf = root / result['record']['pdf']['path']
            pdftotext = next(tool['path'] for tool in toolchain['tools']
                             if tool['name'] == 'pdftotext')
            last_page = result['record']['pdf']['page_count']
            extracted = subprocess.run(
                [pdftotext, '-f', str(last_page), '-l', str(last_page),
                 str(pdf), '-'],
                check=True, capture_output=True, text=True,
            ).stdout
            previous_page = subprocess.run(
                [pdftotext, '-f', str(last_page - 1), '-l', str(last_page - 1),
                 str(pdf), '-'],
                check=True, capture_output=True, text=True,
            ).stdout
        self.assertEqual([], result['record']['problems'])
        self.assertIn('三数成等比', previous_page)
        self.assertIn('正切和角公式', extracted)
        self.assertIn('答案（2）', extracted)

    def test_q30_print_solution_heading_is_not_orphaned_at_page_bottom(self):
        manifest = json.loads((PROJECT / 'source-manifest.json').read_text(encoding='utf-8'))
        paper = next(p for p in manifest['papers']
                     if p['paper_id'] == 'gk-1989-regular-guangdong-science')
        with tempfile.TemporaryDirectory(prefix='gk1989-print-layout-') as temporary:
            root = Path(temporary)
            project_copy = root / 'docs' / 'exams' / 'math-gaokao-latex'
            project_copy.mkdir(parents=True)
            shutil.copytree(PROJECT / 'common', project_copy / 'common')
            shutil.copytree(
                PROJECT / paper['project_dir'],
                project_copy / paper['project_dir'],
                ignore=shutil.ignore_patterns('build', 'receipts', '.work'),
            )
            toolchain = build_projects.resolve_toolchain()
            result = build_projects.build_target(
                root,
                paper['project_dir'],
                '印刷版',
                toolchain,
            )
            pdf = root / result['record']['pdf']['path']
            pdftotext = next(tool['path'] for tool in toolchain['tools']
                             if tool['name'] == 'pdftotext')
            extracted = subprocess.run(
                [pdftotext, '-layout', str(pdf), '-'],
                check=True, capture_output=True, text=True,
            ).stdout
        self.assertEqual([], result['record']['problems'])
        pages = extracted.split('\f')
        q30_page = next(i for i, page in enumerate(pages)
                        if '第五题（原卷：五）' in page)
        q30_content_lines = [
            line.strip() for line in pages[q30_page].splitlines()
            if line.strip() and not line.strip().startswith('——第 ')
        ]
        self.assertNotEqual('解析', q30_content_lines[-1])
        self.assertTrue(any(
            '解析' in page and '令 t' in page
            for page in pages[q30_page:]
        ))

    def test_vector_figure_sources_have_valid_text_and_q25_intercepts(self):
        figures = {path.name: path.read_text(encoding='utf-8')
                   for path in FIGURES.glob('*.tex')}
        self.assertEqual(len(figures), 3)
        self.assertTrue(all(r'\不表示' not in text for text in figures.values()))
        choices = figures['f1989_guangdong_science_q25_options.tex']
        self.assertIn('(-2,2)--(2,-2)', choices)
        self.assertIn('(-2,2.5)--(3,0)', choices)
        self.assertIn('(-2,0)--(0,1.5)', choices)
        # The D lines were extended beyond their intercepts to match the scan.
        # Check the line through (-2, 0) and (0, -2) geometrically.
        d_scope = choices.split(r"\begin{scope}[xshift=9.62cm", 1)[1]
        lines = re.findall(r"\\draw\[graph\] \(([-\d.]+),([-\d.]+)\)--\(([-\d.]+),([-\d.]+)\);", d_scope)
        self.assertEqual(len(lines), 2)
        for line, points in zip(lines, (((-2, 0), (0, -2)), ((3, 0), (0, 1.5)))):
            x1, y1, x2, y2 = map(float, line)
            for x, y in points:
                self.assertAlmostEqual((y - y1) * (x2 - x1), (y2 - y1) * (x - x1))
        self.assertIn(r'\draw[graph] (0,1.5) circle', choices)

    def test_q30_locus_curve_endpoint_precedes_horizontal_axis_arrow(self):
        figure = (FIGURES / 'f1989_guangdong_science_q30_locus.tex').read_text(
            encoding='utf-8')
        axis_match = re.search(
            r'\\draw\[->,thin\].*--\(([-\d.]+),0\)', figure)
        curve_match = re.search(r'domain=[\d.]+:([\d.]+),samples=90', figure)
        self.assertIsNotNone(axis_match)
        self.assertIsNotNone(curve_match)
        axis_end_x = float(axis_match.group(1))
        curve_end_parameter = float(curve_match.group(1))
        curve_end_x = curve_end_parameter ** 2
        self.assertLessEqual(
            curve_end_x, axis_end_x - 0.25,
            'the y^2=x curve must end before the x-axis arrow, not beyond it')

    def test_q30_locus_label_has_clearance_above_the_curve(self):
        figure = (FIGURES / 'f1989_guangdong_science_q30_locus.tex').read_text(
            encoding='utf-8')
        label_match = re.search(
            r'\\node\[above right\] at \(([-\d.]+),([-\d.]+)\) '
            r'\{\$y\^2=x,\\ y>0\$\};',
            figure)
        self.assertIsNotNone(label_match)
        label_x, label_y = (float(value) for value in label_match.groups())
        clearance = label_y - math.sqrt(label_x)
        self.assertGreaterEqual(
            clearance, 0.6,
            'the locus label must sit visibly above y=sqrt(x) at its anchor')

    def test_short_answer_table_is_split_to_avoid_overfull_for_25_choices(self):
        manifest = json.loads((PROJECT / 'source-manifest.json').read_text(encoding='utf-8'))
        paper = next(p for p in manifest['papers']
                     if p['paper_id'] == 'gk-1989-regular-guangdong-science')
        sources = make_short_answers.paper_sources(
            paper, make_short_answers.INDEX_METADATA)
        result, problems = make_short_answers.generate_short_answers(
            PROJECT.parents[2], sources)
        self.assertEqual(problems, ())
        output = result.targets[
            f"math-gaokao-latex/{paper['project_dir']}/answers_short.tex"
        ].decode('utf-8')
        self.assertEqual(output.count(r'\begin{tabular}'), 2)

    def test_answers_and_solutions_align_with_every_question_and_keep_provenance(self):
        question_blocks = solution_sources.parse_question_blocks(self.questions_text)
        answer_points = solution_sources.parse_answer_points(self.answers_text)
        solution_blocks = solution_sources.validate_solution_body(self.solutions_text)
        self.assertEqual(len(answer_points), 30)
        self.assertEqual(len(solution_blocks), 30)
        self.assertEqual([point.printed_label for point in answer_points[25:]],
                         ['一', '二', '三', '四', '五'])
        self.assertEqual([block.printed_label for block in solution_blocks[25:]],
                         ['一', '二', '三', '四', '五'])
        self.assertEqual(answer_points[7].answers, ((None, 'C'),))
        self.assertIn('B型', self.answers_text)
        self.assertIn('待独立复核', self.answers_text)
        solution_sources.render_combined(
            self.questions_text, self.solutions_text, self.answers_text)


if __name__ == '__main__':
    unittest.main()

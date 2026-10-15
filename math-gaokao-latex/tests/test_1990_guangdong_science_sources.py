"""1990 广东理科合并稿应忠实保留原卷的分数与希腊字母。"""
from pathlib import Path
import re
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
EXAMS = PROJECT.parent
QUESTIONS = EXAMS / '1990' / '1990_数学真题_广东理_试题.md'
ANSWERS = EXAMS / '1990' / '1990_数学真题_广东理_答案要点.md'
SOLUTIONS = EXAMS / '1990' / '1990_数学真题_广东理_解析正文.md'
COMBINED = EXAMS / '1990' / '1990_数学真题_广东理_含解析.md'
sys.path.insert(0, str(PROJECT / 'tools'))
import solution_sources


class GuangdongScience1990SourceTests(unittest.TestCase):
    def test_short_answers_retain_printed_attribution_and_q12_blocker(self):
        short = (PROJECT / '1990_广东卷_理科' / 'answers_short.tex').read_text(encoding='utf-8')
        self.assertIn('来源印载答案', short)
        self.assertIn('第12题', short)
        self.assertIn('题图缺失', short)
        self.assertIn('B仅为来源印载', short)
        self.assertNotIn('答案为编写者独立推导', short)
        self.assertEqual([len(columns) for columns in re.findall(
            r'\\begin\{tabular\}\{(c+)\}', short)], [14, 13])

    def test_q1_fraction_options_and_q2_alpha_survive_combined_render(self):
        combined = solution_sources.render_combined(
            QUESTIONS.read_text(encoding='utf-8'),
            SOLUTIONS.read_text(encoding='utf-8'),
            ANSWERS.read_text(encoding='utf-8'),
        )

        self.assertTrue(
            COMBINED.read_bytes() == combined.encode('utf-8'),
            'persisted combined markdown must byte-match render_combined',
        )
        self.assertTrue(
            r'B．$-\dfrac{1}{3}$　C．$-\dfrac{2}{3}$' in combined,
            'rendered Q1 fractions should match the source PDF',
        )
        self.assertTrue(
            r'平面 $\alpha$ 的斜线' in combined,
            'rendered Q2 plane label should use Greek alpha',
        )

    def test_q15_logarithm_base_range_matches_the_source_answer(self):
        solution = SOLUTIONS.read_text(encoding='utf-8')
        q15 = solution.split('### 第 15 题', 1)[1].split('### 第 16 题', 1)[0]

        self.assertIn(r'由 $\log_b 2>0$ 得 $b>1$', q15)
        self.assertIn(r'又因 $\log_a 2>\log_b 2>0$，故 $a>1$', q15)
        self.assertIn(r'在 $t>1$ 上', q15)
        self.assertIn(r'即 $1<a<b$，对应答案 A', q15)
        self.assertNotIn(r'$0<a,b<1$', q15)
        self.assertIn(
            '**15．**\n\n**答案：A**', ANSWERS.read_text(encoding='utf-8')
        )


if __name__ == '__main__':
    unittest.main()

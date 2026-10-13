import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import score_ocr


def source_manifest():
    return {
        'sources': [{
            'source_id': 'src-sample',
            'artifact': {
                'sha256': 'a' * 64,
                'page_count': 2,
            },
        }],
    }


def run_record(case, output, *, engine='ocr-a', engine_version='1'):
    identity = ('source_id', 'source_sha256', 'source_page',
                'bbox_pixels_top_left_xywh', 'task')
    return {
        'case_id': case['case_id'], 'engine': engine,
        'engine_version': engine_version, 'output': output,
        'metadata': {field: case[field] for field in identity},
    }


class OcrScoringTests(unittest.TestCase):
    def test_text_cer_and_math_exactness_are_scored_separately(self):
        gold = {
            'schema_version': 1,
            'cases': [
                {
                    'case_id': 'prose-1',
                    'source_id': 'src-sample',
                    'source_sha256': 'a' * 64,
                    'source_page': 1,
                    'bbox_pixels_top_left_xywh': [0, 0, 100, 20],
                    'task': 'text',
                    'reference_text': '我爱数学',
                    'review_status': 'human_verified',
                    'reviewed_by': 'reviewer-a',
                    'reviewed_at': '2026-10-13',
                },
                {
                    'case_id': 'formula-1',
                    'source_id': 'src-sample',
                    'source_sha256': 'a' * 64,
                    'source_page': 2,
                    'bbox_pixels_top_left_xywh': None,
                    'task': 'formula',
                    'reference_text': 'x-1=0',
                    'review_status': 'human_verified',
                    'reviewed_by': 'reviewer-a',
                    'reviewed_at': '2026-10-13',
                },
            ],
        }
        runs = [run_record(gold['cases'][0], '我爱数'),
                run_record(gold['cases'][1], 'x + 1 = 0')]

        report = score_ocr.score_benchmark(gold, runs, source_manifest())

        self.assertEqual(report['gold_case_count'], 2)
        self.assertEqual(report['scored_runs'], 2)
        self.assertEqual(report['pending_cases'], 0)
        self.assertEqual(report['results'][0]['score'], {
            'metric': 'cer', 'edit_distance': 1, 'reference_length': 4, 'value': 0.25,
        })
        self.assertEqual(report['results'][1]['score'], {
            'metric': 'exact_match', 'matched': False,
        })

    def test_text_summary_is_micro_averaged_across_cases(self):
        gold = {
            'schema_version': 1,
            'cases': [
                {
                    'case_id': 'short', 'source_id': 'src-sample', 'source_sha256': 'a' * 64,
                    'source_page': 1, 'bbox_pixels_top_left_xywh': None, 'task': 'text',
                    'reference_text': '我爱数学', 'review_status': 'human_verified',
                    'reviewed_by': 'reviewer-a', 'reviewed_at': '2026-10-13',
                },
                {
                    'case_id': 'long', 'source_id': 'src-sample', 'source_sha256': 'a' * 64,
                    'source_page': 2, 'bbox_pixels_top_left_xywh': None, 'task': 'text',
                    'reference_text': 'abcdef', 'review_status': 'human_verified',
                    'reviewed_by': 'reviewer-a', 'reviewed_at': '2026-10-13',
                },
            ],
        }
        runs = [run_record(gold['cases'][0], '我爱数'),
                run_record(gold['cases'][1], 'abc')]

        report = score_ocr.score_benchmark(gold, runs, source_manifest())

        self.assertEqual(report['summary'], [{
            'engine': 'ocr-a', 'engine_version': '1', 'task': 'text',
            'metric': 'cer', 'edit_distance': 4, 'reference_length': 10, 'value': 0.4,
        }])

    def test_unverified_gold_is_reported_but_never_scored(self):
        gold = {
            'schema_version': 1,
            'cases': [{
                'case_id': 'pending',
                'source_id': 'src-sample',
                'source_sha256': 'a' * 64,
                'source_page': 1,
                'bbox_pixels_top_left_xywh': None,
                'task': 'formula',
                'reference_text': 'x^2=1',
                'review_status': 'pending_human_review',
            }],
        }
        runs = [run_record(gold['cases'][0], 'x^2=1')]

        report = score_ocr.score_benchmark(gold, runs, source_manifest())

        self.assertEqual(report['pending_cases'], 1)
        self.assertEqual(report['scored_runs'], 0)
        self.assertEqual(report['results'][0]['status'], 'pending_gold')
        self.assertNotIn('score', report['results'][0])

    def test_empty_ocr_output_counts_as_deleting_the_entire_reference(self):
        gold = {
            'schema_version': 1,
            'cases': [{
                'case_id': 'blank-output', 'source_id': 'src-sample', 'source_sha256': 'a' * 64,
                'source_page': 1, 'bbox_pixels_top_left_xywh': None, 'task': 'text',
                'reference_text': '数学', 'review_status': 'human_verified',
                'reviewed_by': 'reviewer-a', 'reviewed_at': '2026-10-13',
            }],
        }
        runs = [run_record(gold['cases'][0], '')]

        report = score_ocr.score_benchmark(gold, runs, source_manifest())

        self.assertEqual(report['results'][0]['score'], {
            'metric': 'cer', 'edit_distance': 2, 'reference_length': 2, 'value': 1.0,
        })

    def test_source_identity_page_and_bbox_are_enforced(self):
        base = {
            'case_id': 'case-1',
            'source_id': 'src-sample',
            'source_sha256': 'a' * 64,
            'source_page': 1,
            'bbox_pixels_top_left_xywh': [0, 0, 100, 20],
            'task': 'text',
            'reference_text': '题目',
            'review_status': 'human_verified',
            'reviewed_by': 'reviewer-a',
            'reviewed_at': '2026-10-13',
        }
        for changes, message in (
            ({'source_sha256': 'b' * 64}, 'source SHA-256 mismatch'),
            ({'source_page': 3}, 'source page out of range'),
            ({'bbox_pixels_top_left_xywh': [0, 0, 0, 20]}, 'positive width and height'),
            ({'task': []}, 'unsupported OCR task'),
        ):
            with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, message):
                score_ocr.score_benchmark(
                    {'schema_version': 1, 'cases': [{**base, **changes}]},
                    [],
                    source_manifest(),
                )

    def test_human_verified_gold_requires_reviewer_and_date(self):
        case = {
            'case_id': 'case-1', 'source_id': 'src-sample', 'source_sha256': 'a' * 64,
            'source_page': 1, 'bbox_pixels_top_left_xywh': None, 'task': 'formula',
            'reference_text': 'x=1', 'review_status': 'human_verified',
            'reviewed_at': '2026-10-13',
        }

        with self.assertRaisesRegex(ValueError, 'reviewed_by'):
            score_ocr.score_benchmark(
                {'schema_version': 1, 'cases': [case]}, [], source_manifest(),
            )

    def test_ocr_run_metadata_must_match_the_scored_source_region(self):
        case = {
            'case_id': 'case-1', 'source_id': 'src-sample', 'source_sha256': 'a' * 64,
            'source_page': 1, 'bbox_pixels_top_left_xywh': [0, 0, 100, 20],
            'task': 'text', 'reference_text': '题目', 'review_status': 'human_verified',
            'reviewed_by': 'reviewer-a', 'reviewed_at': '2026-10-13',
        }
        run = {
            'case_id': 'case-1', 'engine': 'ocr-a', 'engine_version': '1', 'output': '题目',
            'metadata': {
                'source_id': 'src-sample', 'source_sha256': 'b' * 64,
                'source_page': 1, 'bbox_pixels_top_left_xywh': [0, 0, 100, 20],
                'task': 'text',
            },
        }

        with self.assertRaisesRegex(ValueError, 'source_sha256 mismatch for case-1'):
            score_ocr.score_benchmark(
                {'schema_version': 1, 'cases': [case]}, [run], source_manifest(),
            )


if __name__ == '__main__':
    unittest.main()

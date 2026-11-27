from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import recognize_formula as formula


class FormulaRecognitionTests(unittest.TestCase):
    def test_verified_cache_and_model_invalidation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = root / 'formula.png'
            image.write_bytes(b'image fixture')
            model = root / 'model'
            model.mkdir()
            weights = model / 'weights'
            weights.write_bytes(b'first model')
            result = {'latex': 'x^2-2x=0', 'predict_seconds': 0.1}
            with patch.object(formula, 'engine_metadata', return_value={'paddleocr': '3.7.0'}), patch.object(formula, 'run_prediction', return_value=result) as worker:
                a = formula.recognize(image, model, cache_dir=root / 'cache')
                self.assertEqual(a['review_status'], 'needs-review')
                self.assertFalse(a['cache_hit'])
                b = formula.recognize(image, model, cache_dir=root / 'cache')
                self.assertTrue(b['cache_hit'])
                self.assertEqual(worker.call_count, 1)
                weights.write_bytes(b'changed model')
                c = formula.recognize(image, model, cache_dir=root / 'cache')
                self.assertFalse(c['cache_hit'])
                self.assertNotEqual(a['cache_key'], c['cache_key'])
                cache = root / 'cache' / (c['cache_key'] + '.json')
                cache.write_text('{}')
                formula.recognize(image, model, cache_dir=root / 'cache')
                self.assertEqual(worker.call_count, 3)

    def test_worker_failure_and_empty_results_are_not_cached(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            image = root / 'formula.png'
            image.write_bytes(b'image fixture')
            model = root / 'model'
            model.mkdir()
            (model / 'weights').write_bytes(b'model')
            with patch.object(formula, 'engine_metadata', return_value={}), patch.object(formula, 'run_prediction', side_effect=formula.FormulaError('timeout')):
                with self.assertRaises(formula.FormulaError):
                    formula.recognize(image, model, cache_dir=root / 'cache')
            with patch.object(formula, 'engine_metadata', return_value={}), patch.object(formula, 'run_prediction', return_value={'latex': ''}):
                with self.assertRaises(formula.FormulaError):
                    formula.recognize(image, model, cache_dir=root / 'cache')
            self.assertFalse(list(root.glob('cache/*.json')))

    def test_worker_timeout_and_invalid_protocol_fail_closed(self):
        with patch.object(formula.subprocess, 'run', side_effect=subprocess.TimeoutExpired('worker', 1)) as run:
            with self.assertRaises(formula.FormulaError):
                formula.run_prediction('python', 'image.png', 'model', 'model-name', 1)
            self.assertEqual(run.call_count, 1)
        for output in ('not JSON', formula.MARKER + '{broken', formula.MARKER + '{}\n' + formula.MARKER + '{}'):
            with patch.object(formula.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, output, '')):
                with self.assertRaises(formula.FormulaError):
                    formula.run_prediction('python', 'image.png', 'model', 'model-name', 1)

    def test_environment_failure_reports_actionable_error(self):
        with patch.object(formula.subprocess, 'run', side_effect=FileNotFoundError('python')):
            with self.assertRaisesRegex(formula.FormulaError, 'venv'):
                formula.engine_metadata('missing-python', 1)


if __name__ == '__main__':
    unittest.main()

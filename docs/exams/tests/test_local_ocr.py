"""Routing, integrity and error boundaries; no model downloads or inference."""
import hashlib
import contextlib
import io
import json
import os
from pathlib import Path
import sys
import signal
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import local_ocr as ocr


class LocalOcrTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work_patch = patch.object(ocr, 'WORK', self.root/'work')
        self.work_patch.start()
        self.addCleanup(self.work_patch.stop)
        self.image = self.root/'image.png'
        self.image.write_bytes(b'input')
        self.worker = self.root/'worker.py'
        self.worker.write_text('''import argparse,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('image');p.add_argument('--output');p.add_argument('--model-dir')
p.add_argument('--max-tokens');p.add_argument('--task')
a=p.parse_args()
Path(a.output).write_text(json.dumps({'output':'candidate '+a.max_tokens}))
''')
        model = self.root/'model'
        model.mkdir()
        (model/'weights').write_bytes(b'model')
        self.spec = {'python': sys.executable, 'worker': str(self.worker),
                     'model_dir': str(model), 'engine_name': 'xiaomi',
                     'revision': 'a'*40, 'repo_id': 'test', 'packages': {},
                     'model_tree_sha256': ocr.model_tree(model), 'worker_sha256': ocr.sha(self.worker)}

    def test_cache_hit_and_parameter_change(self):
        first = ocr.invoke(self.spec, self.image)
        second = ocr.invoke(self.spec, self.image)
        changed = ocr.invoke(self.spec, self.image, max_tokens=32)
        self.assertFalse(first['cache_hit'])
        self.assertTrue(second['cache_hit'])
        self.assertEqual(first['model_calls_this_run'], 1)
        self.assertEqual(second['model_calls_this_run'], 0)
        self.assertFalse(changed['cache_hit'])
        self.assertEqual(changed['output'], 'candidate 32')

    def test_cache_tampering_is_not_accepted(self):
        ocr.invoke(self.spec, self.image)
        cache = next((ocr.WORK/'cache').glob('*.json'))
        value = json.loads(cache.read_text())
        value['body']['result']['output'] = 'tampered'
        cache.write_text(json.dumps(value))
        result = ocr.invoke(self.spec, self.image)
        self.assertFalse(result['cache_hit'])
        self.assertNotEqual(result['output'], 'tampered')

    def test_failed_worker_has_no_cached_success(self):
        self.worker.write_text('raise RuntimeError("failed inference")')
        with self.assertRaisesRegex(RuntimeError, 'exited'):
            ocr.invoke(self.spec, self.image)
        self.assertFalse((ocr.WORK/'cache').exists())

    def test_timeout_retains_log_and_no_cached_success(self):
        self.worker.write_text('import time;time.sleep(5)')
        with self.assertRaisesRegex(RuntimeError, 'terminated'):
            ocr.invoke(self.spec, self.image, timeout=0.05)
        self.assertEqual(json.loads(next((ocr.WORK/'logs').glob('*.json')).read_text())['status'], 'timeout')
        self.assertFalse((ocr.WORK/'cache').exists())

    def test_keyboard_interrupt_reaps_worker_before_unlocking(self):
        marker = self.root/'child-pid'
        self.worker.write_text('import os,time\nfrom pathlib import Path\n'
                               f'Path({str(marker)!r}).write_text(str(os.getpid()))\ntime.sleep(30)')
        code = (f'import sys;sys.path.insert(0,{str(Path(ocr.__file__).parent)!r});'
                'import local_ocr as o;from pathlib import Path;'
                f'o.WORK=Path({str(ocr.WORK)!r});'
                f'o.invoke({self.spec!r},Path({str(self.image)!r}))')
        parent = subprocess.Popen([sys.executable, '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child = None
        try:
            deadline = time.monotonic()+5
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(marker.exists())
            child = int(marker.read_text())
            os.kill(parent.pid, signal.SIGINT)
            parent.communicate(timeout=5)
            with self.assertRaises(ProcessLookupError):
                os.kill(child, 0)
            log = json.loads(next((ocr.WORK/'logs').glob('*.json')).read_text())
            self.assertEqual(log['status'], 'interrupted')
        finally:
            if parent.poll() is None:
                parent.kill()
                parent.communicate()
            if child:
                try:
                    os.kill(child, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_doctor_rejects_python_version_drift(self):
        spec = dict(self.spec, python_version='0.0.0')
        config = self.root/'config.json'
        config.write_text(json.dumps({'engines': {'xiaomi': spec}}))
        with self.assertRaisesRegex(ValueError, 'Python version'):
            ocr.engine_config('xiaomi', config)

    def manifest(self, expected=None):
        self.pdf = self.root/'source.pdf'
        self.pdf.write_bytes(b'%PDF-test')
        source = {'source_id': 'source', 'source_state': 'ready',
                  'artifact': {'sha256': expected or ocr.sha(self.pdf), 'page_count': 2}}
        path = self.root/'manifest.json'
        path.write_text(json.dumps({'sources': [source]}))
        return path

    def test_wrong_source_hash_fails_before_model_or_pdf_analysis(self):
        manifest = self.manifest('a'*64)
        with patch.object(ocr.analyze_pdf, 'analyze') as analyze:
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                ocr.process_pdf(self.pdf, 'source', manifest=manifest)
            analyze.assert_not_called()

    def test_native_text_and_suspect_text_are_not_automatically_ocrd(self):
        manifest = self.manifest()
        analysis = {'page_count': 2, 'pages': [
            {'page': 1, 'classification': 'text_candidate', 'content_evidence': 'text_layer'},
            {'page': 2, 'classification': 'review', 'content_evidence': 'text_and_raster'}]}
        with patch.object(ocr.analyze_pdf, 'analyze', return_value=analysis), \
             patch.object(ocr, 'engine_config') as engine, \
             patch.object(ocr.ocr_pdf, '_executable'):
            result = ocr.process_pdf(self.pdf, 'source', manifest=manifest)
        engine.assert_not_called()
        self.assertEqual(result['selected_pages'], [])
        self.assertEqual(result['pages_requiring_manual_routing'], [2])

    def test_ocr_candidates_preserve_model_evidence_and_unverified_status(self):
        manifest = self.manifest()
        analysis = {'page_count': 2, 'pages': [
            {'page': 2, 'classification': 'needs_ocr_or_blank', 'content_evidence': 'raster_only'}]}
        with patch.object(ocr.analyze_pdf, 'analyze', return_value=analysis), \
             patch.object(ocr, 'engine_config', return_value=self.spec), \
             patch.object(ocr.ocr_pdf, '_executable', return_value=({'path':'pdftoppm'}, 'version')), \
             patch.object(ocr.ocr_pdf, 'render_page', return_value=(self.image, (300,400),False,None)) as render:
            result = ocr.process_pdf(self.pdf, 'source', manifest=manifest)
        self.assertEqual(render.call_args.args[3], {'path': 'pdftoppm'})
        candidate = result['candidates'][0]
        self.assertEqual(candidate['source_page'], 2)
        self.assertIsNone(candidate['question_id'])
        self.assertEqual(candidate['review_status'], 'needs-review')
        self.assertEqual(candidate['model_evidence']['revision'], self.spec['revision'])

    def test_mineru_missing_page_is_rejected(self):
        self.spec['engine_name'] = 'mineru'
        self.worker.write_text('''import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('pdf');p.add_argument('--pages');p.add_argument('--output')
a=p.parse_args();Path(a.output).write_text(json.dumps({'pages':[{'page':1,'output':'text'}]}))
''')
        with self.assertRaisesRegex(ValueError, 'source page'):
            ocr.invoke(self.spec, self.image, pages=[2])

    def test_cli_never_overwrites_its_input(self):
        before = self.image.read_bytes()
        with contextlib.redirect_stderr(io.StringIO()):
            code = ocr.main(['image', str(self.image), '--output', str(self.image)])
        self.assertEqual(code, 1)
        self.assertEqual(self.image.read_bytes(), before)

    def test_batch_retains_success_after_a_failed_job_and_returns_failure(self):
        jobs = self.root/'jobs.json'
        jobs.write_text(json.dumps([{'pdf':'a.pdf','source_id':'a'}, {'pdf':'b.pdf','source_id':'b'}]))
        output = self.root/'result.json'
        with patch.object(ocr, 'process_pdf', side_effect=[ValueError('source mismatch'), {'candidates': []}]):
            code = ocr.main(['batch', str(jobs), '--output', str(output)])
        self.assertEqual(code, 1)
        self.assertEqual([r['status'] for r in json.loads(output.read_text())['jobs']], ['failed','succeeded'])

    def test_matching_cross_engine_outputs_still_require_review(self):
        manifest = self.manifest()
        analysis = {'page_count':2, 'pages':[
            {'page':2,'classification':'needs_ocr_or_blank','content_evidence':'raster_only'}]}
        with patch.object(ocr.analyze_pdf,'analyze',return_value=analysis), \
             patch.object(ocr,'engine_config',side_effect=lambda name, config: dict(self.spec,engine_name=name)), \
             patch.object(ocr.ocr_pdf,'_executable',return_value=({'path':'pdftoppm'},'version')), \
             patch.object(ocr.ocr_pdf,'render_page',return_value=(self.image,(300,400),False,None)):
            result = ocr.process_pdf(self.pdf,'source',manifest=manifest,cross_check=True)
        self.assertEqual([r['engine'] for r in result['runs']], ['xiaomi','paddle'])
        self.assertTrue(result['comparisons'][0]['exact_match'])
        self.assertTrue(all(c['review_status']=='needs-review' and c['question_id'] is None for c in result['candidates']))


if __name__ == '__main__':
    unittest.main()

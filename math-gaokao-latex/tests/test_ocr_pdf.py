import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import ocr_pdf


PNG = (b'\x89PNG\r\n\x1a\n' + b'\x00\x00\x00\rIHDR'
       + b'\x00\x00\x00d\x00\x00\x00\xc8' + b'\x08\x02\x00\x00\x00')


def analysis_for(pdf):
    return {
        'pdf_sha256': hashlib.sha256(Path(pdf).read_bytes()).hexdigest(),
        'page_count': 4,
            'complete_document': True,
        'pages': [
            {'page': 1, 'classification': 'text_candidate', 'content_evidence': 'text_layer',
             'non_whitespace_chars': 120, 'image_objects': 0},
            {'page': 2, 'classification': 'needs_ocr_or_blank', 'content_evidence': 'raster_only',
             'non_whitespace_chars': 0, 'image_objects': 1},
            {'page': 3, 'classification': 'needs_ocr_or_blank', 'content_evidence': 'no_text_or_raster',
             'non_whitespace_chars': 0, 'image_objects': 0},
            {'page': 4, 'classification': 'review', 'content_evidence': 'text_and_raster',
             'non_whitespace_chars': 12, 'image_objects': 1},
        ],
    }


def fake_toolchain(languages='chi_sim+eng'):
    return {
        'renderer': {'path': '/tools/pdftoppm', 'version': '26.10.0', 'sha256': 'renderer-sha'},
        'tesseract': {'path': '/tools/tesseract', 'version': '5.5.3', 'sha256': 'engine-sha',
                      'tessdata_dir': '/models/tessdata', 'languages': languages,
                      'traineddata_sha256': {'chi_sim': 'chi-sha', 'eng': 'eng-sha'}},
    }


class PdfOcrPipelineTests(unittest.TestCase):
    def test_invalid_source_identity_is_rejected_before_external_tools(self):
        with tempfile.TemporaryDirectory() as temp:
            pdf = Path(temp) / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')
            with patch.object(ocr_pdf.analyze_pdf, 'analyze', side_effect=AssertionError('must fail before analysis')):
                with self.assertRaisesRegex(ocr_pdf.OcrPdfError, 'source_id'):
                    ocr_pdf.process_pdf(pdf, source_id=' source-123 ')

    def test_non_object_cache_body_is_treated_as_corrupt(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'cache.json'
            body = []
            checksum = hashlib.sha256(ocr_pdf.analyze_pdf.canonical(body).encode()).hexdigest()
            path.write_text(ocr_pdf.analyze_pdf.canonical({'body': body, 'sha256': checksum}), encoding='utf-8')
            self.assertIsNone(ocr_pdf.read_enveloped_cache(path, {}))

    def test_automatic_selection_ocr_cache_and_unverified_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')
            calls = []

            def run_tool(command, timeout):
                calls.append(command)
                if Path(command[0]).name == 'pdftoppm':
                    Path(command[-1] + '.png').write_bytes(PNG)
                    return subprocess.CompletedProcess(command, 0, '', '')
                return subprocess.CompletedProcess(command, 0, 'OCR 候选文本 x+1\n', '')

            with patch.object(ocr_pdf.analyze_pdf, 'analyze', side_effect=lambda source, **kwargs: analysis_for(source)), \
                    patch.object(ocr_pdf, 'tool_fingerprints', return_value=fake_toolchain()), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                first = ocr_pdf.process_pdf(pdf, source_id='source-123', cache_dir=root / 'cache')
                self.assertEqual([page['source_page'] for page in first['pages']], [2])
                self.assertEqual(first['pages'][0]['output'], 'OCR 候选文本 x+1')
                self.assertEqual(first['pages'][0]['review_status'], 'needs-review')
                self.assertEqual(first['pages'][0]['extraction_status'], 'recognized_unverified')
                self.assertEqual(first['ocr_calls'], 1)
                self.assertEqual(first['skipped_pages'], [
                    {'page': 1, 'reason': 'native_text_candidate'},
                    {'page': 3, 'reason': 'no_raster_evidence'},
                    {'page': 4, 'reason': 'text_layer_requires_review_or_override'},
                ])
                second = ocr_pdf.process_pdf(pdf, source_id='source-123', cache_dir=root / 'cache')

            self.assertEqual(second['cache_hits'], 1)
            self.assertEqual(second['ocr_calls'], 0)
            self.assertTrue(second['pages'][0]['cache_hit'])
            self.assertEqual(len(calls), 2)
            self.assertEqual(Path(calls[0][0]).name, 'pdftoppm')
            self.assertEqual(Path(calls[1][0]).name, 'tesseract')

    def test_explicit_page_override_never_marks_text_as_verified(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')

            def run_tool(command, timeout):
                if Path(command[0]).name == 'pdftoppm':
                    Path(command[-1] + '.png').write_bytes(PNG)
                    return subprocess.CompletedProcess(command, 0, '', '')
                return subprocess.CompletedProcess(command, 0, 'manual override result\n', '')

            with patch.object(ocr_pdf.analyze_pdf, 'analyze', side_effect=lambda source, **kwargs: analysis_for(source)), \
                    patch.object(ocr_pdf, 'tool_fingerprints', return_value=fake_toolchain()), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                result = ocr_pdf.process_pdf(pdf, pages=[1], cache_dir=root / 'cache')

            self.assertEqual(result['selection_mode'], 'explicit_page_override')
            self.assertEqual(result['pages'][0]['source_page'], 1)
            self.assertEqual(result['pages'][0]['selection_reason'], 'explicit_page_override')
            self.assertEqual(result['pages'][0]['review_status'], 'needs-review')
            self.assertEqual(result['pages'][0]['extraction_status'], 'recognized_unverified')

    def test_render_and_ocr_cache_are_invalidated_by_dpi_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')
            calls = []

            def run_tool(command, timeout):
                calls.append(command)
                if Path(command[0]).name == 'pdftoppm':
                    Path(command[-1] + '.png').write_bytes(PNG)
                    return subprocess.CompletedProcess(command, 0, '', '')
                return subprocess.CompletedProcess(command, 0, 'OCR candidate\n', '')

            with patch.object(ocr_pdf.analyze_pdf, 'analyze', side_effect=lambda source, **kwargs: analysis_for(source)), \
                    patch.object(ocr_pdf, 'tool_fingerprints', return_value=fake_toolchain()), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                first = ocr_pdf.process_pdf(pdf, cache_dir=root / 'cache', dpi=180)
                second = ocr_pdf.process_pdf(pdf, cache_dir=root / 'cache', dpi=220)

            self.assertNotEqual(first['pages'][0]['cache_key'], second['pages'][0]['cache_key'])
            self.assertEqual([Path(command[0]).name for command in calls],
                             ['pdftoppm', 'tesseract', 'pdftoppm', 'tesseract'])

    def test_corrupt_render_cache_is_rebuilt_without_repeating_ocr(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')
            calls = []

            def run_tool(command, timeout):
                calls.append(command)
                if Path(command[0]).name == 'pdftoppm':
                    Path(command[-1] + '.png').write_bytes(PNG)
                    return subprocess.CompletedProcess(command, 0, '', '')
                return subprocess.CompletedProcess(command, 0, 'OCR candidate\n', '')

            with patch.object(ocr_pdf.analyze_pdf, 'analyze', side_effect=lambda source, **kwargs: analysis_for(source)), \
                    patch.object(ocr_pdf, 'tool_fingerprints', return_value=fake_toolchain()), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                first = ocr_pdf.process_pdf(pdf, cache_dir=root / 'cache')
                render = next((root / 'cache' / 'render').glob('*.png'))
                render.write_bytes(render.read_bytes() + b'corrupt-but-header-remains')
                second = ocr_pdf.process_pdf(pdf, cache_dir=root / 'cache')

            self.assertFalse(second['render_cache_hits'])
            self.assertEqual(second['cache_hits'], 1)
            self.assertEqual(second['ocr_calls'], 0)
            self.assertEqual([Path(command[0]).name for command in calls],
                             ['pdftoppm', 'tesseract', 'pdftoppm'])
            self.assertEqual(first['pages'][0]['cache_key'], second['pages'][0]['cache_key'])

    def test_ocr_failure_is_not_cached_or_retried(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')
            calls = []

            def run_tool(command, timeout):
                calls.append(command)
                if Path(command[0]).name == 'pdftoppm':
                    Path(command[-1] + '.png').write_bytes(PNG)
                    return subprocess.CompletedProcess(command, 0, '', '')
                raise ocr_pdf.OcrPdfError('tesseract failed')

            with patch.object(ocr_pdf.analyze_pdf, 'analyze', side_effect=lambda source, **kwargs: analysis_for(source)), \
                    patch.object(ocr_pdf, 'tool_fingerprints', return_value=fake_toolchain()), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                with self.assertRaisesRegex(ocr_pdf.OcrPdfError, 'tesseract failed'):
                    ocr_pdf.process_pdf(pdf, cache_dir=root / 'cache')

            self.assertEqual([Path(command[0]).name for command in calls], ['pdftoppm', 'tesseract'])
            self.assertFalse(list((root / 'cache' / 'results').glob('*.json')))

    def test_no_raster_candidates_do_not_initialize_or_call_ocr(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixed-source')
            analysis = analysis_for(pdf)
            analysis['pages'] = [analysis['pages'][0]]
            analysis['page_count'] = 1
            analysis['complete_document'] = True
            with patch.object(ocr_pdf.analyze_pdf, 'analyze', return_value=analysis), \
                    patch.object(ocr_pdf, 'tool_fingerprints', side_effect=AssertionError('must not initialize OCR')):
                result = ocr_pdf.process_pdf(pdf, cache_dir=root / 'cache')
            self.assertEqual(result['selected_pages'], [])
            self.assertEqual(result['ocr_calls'], 0)
            self.assertEqual(result['skipped_pages'], [{'page': 1, 'reason': 'native_text_candidate'}])

    def test_toolchain_fingerprint_binds_requested_language_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            renderer = root / 'pdftoppm'
            engine = root / 'tesseract'
            tessdata = root / 'tessdata'
            tessdata.mkdir()
            renderer.write_bytes(b'renderer executable fixture')
            engine.write_bytes(b'tesseract executable fixture')
            (tessdata / 'chi_sim.traineddata').write_bytes(b'chinese model v1')
            (tessdata / 'eng.traineddata').write_bytes(b'english model v1')

            def run_tool(command, timeout):
                executable = Path(command[0]).name
                if executable == 'pdftoppm':
                    return subprocess.CompletedProcess(command, 0, '', 'pdftoppm version 26.10.0')
                if command[-1] == '--version':
                    return subprocess.CompletedProcess(command, 0, 'tesseract 5.5.3\n', '')
                return subprocess.CompletedProcess(command, 0,
                    f'List of available languages in "{tessdata}" (2):\nchi_sim\neng\n', '')

            with patch.object(ocr_pdf.shutil, 'which', side_effect=lambda name: str({'pdftoppm': renderer, 'tesseract': engine}[name])), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                first = ocr_pdf.tool_fingerprints('chi_sim+eng', 10)
                (tessdata / 'chi_sim.traineddata').write_bytes(b'chinese model v2')
                second = ocr_pdf.tool_fingerprints('chi_sim+eng', 10)

            self.assertNotEqual(first['tesseract']['traineddata_sha256']['chi_sim'],
                                second['tesseract']['traineddata_sha256']['chi_sim'])
            self.assertEqual(first['tesseract']['traineddata_sha256']['eng'],
                             second['tesseract']['traineddata_sha256']['eng'])

    def test_missing_requested_language_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            renderer = root / 'pdftoppm'
            engine = root / 'tesseract'
            tessdata = root / 'tessdata'
            tessdata.mkdir()
            renderer.write_bytes(b'renderer executable fixture')
            engine.write_bytes(b'tesseract executable fixture')
            (tessdata / 'eng.traineddata').write_bytes(b'english model')

            def run_tool(command, timeout):
                if Path(command[0]).name == 'pdftoppm':
                    return subprocess.CompletedProcess(command, 0, '', 'pdftoppm version 1.0')
                if command[-1] == '--version':
                    return subprocess.CompletedProcess(command, 0, 'tesseract 1.0\n', '')
                return subprocess.CompletedProcess(command, 0,
                    f'List of available languages in "{tessdata}" (1):\neng\n', '')

            with patch.object(ocr_pdf.shutil, 'which', side_effect=lambda name: str({'pdftoppm': renderer, 'tesseract': engine}[name])), \
                    patch.object(ocr_pdf, 'run_tool', side_effect=run_tool):
                with self.assertRaisesRegex(ocr_pdf.OcrPdfError, 'chi_sim'):
                    ocr_pdf.tool_fingerprints('chi_sim+eng', 10)


if __name__ == '__main__':
    unittest.main()

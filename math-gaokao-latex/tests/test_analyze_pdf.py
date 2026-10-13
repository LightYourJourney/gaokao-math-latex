import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import analyze_pdf


class PdfAnalysisTests(unittest.TestCase):
    def test_text_is_only_a_candidate_and_symbols_trigger_review(self):
        result = analyze_pdf.assess_text('中文数学题 x ≤ 3 ' * 8, 40)
        self.assertEqual(result['classification'], 'text_candidate')
        self.assertTrue(result['requires_content_review'])
        self.assertEqual(analyze_pdf.assess_text('', 40)['classification'], 'needs_ocr_or_blank')
        self.assertEqual(analyze_pdf.assess_text('题目\ufffd' * 30, 40)['classification'], 'review')
        self.assertEqual(analyze_pdf.assess_text('短标题', 40)['classification'], 'review')

    def test_cache_reuses_pages_and_extends_only_missing_page(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixture')
            def run(command, timeout):
                if command[0] == 'pdfinfo':
                    output = 'Pages: 3\n'
                else:
                    output = ('原题条件 x = 2 ' * 20) if command[command.index('-f') + 1] != '2' else ''
                return subprocess.CompletedProcess(command, 0, output, '')
            with patch.object(analyze_pdf, 'tool_fingerprints', return_value={'pdfinfo': {'path': 'pdfinfo'}, 'pdftotext': {'path': 'pdftotext'}}), patch.object(analyze_pdf, 'run_tool', side_effect=run) as runner:
                first = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1, 2])
                self.assertEqual(first['cache']['misses'], 2)
                runner.reset_mock()
                second = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1, 2, 3])
                self.assertEqual(second['cache']['hits'], 2)
                self.assertEqual(second['cache']['misses'], 1)
                self.assertEqual(runner.call_count, 1)
                self.assertEqual(second['document_classification'], 'mixed_candidates')
                cache = next((root / 'cache').glob('*.json'))
                cache.write_text('{}')
                third = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1])
                self.assertEqual(third['cache']['misses'], 1)
                pdf.write_bytes(b'%PDF-1.4 changed')
                fourth = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1])
                self.assertNotEqual(first['pdf_sha256'], fourth['pdf_sha256'])

    def test_failure_and_invalid_page_do_not_write_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixture')
            with patch.object(analyze_pdf, 'tool_fingerprints', return_value={'pdfinfo': {'path': 'pdfinfo'}, 'pdftotext': {'path': 'pdftotext'}}), patch.object(analyze_pdf, 'run_tool', return_value=subprocess.CompletedProcess([], 0, 'Pages: 1\n', '')):
                with self.assertRaises(analyze_pdf.AnalysisError):
                    analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[2])
            self.assertFalse(list(root.glob('cache/*.json')))
            with patch.object(analyze_pdf, 'tool_fingerprints', return_value={'pdfinfo': {'path': 'pdfinfo'}, 'pdftotext': {'path': 'pdftotext'}}), patch.object(analyze_pdf, 'run_tool', side_effect=analyze_pdf.AnalysisError('failed')):
                with self.assertRaises(analyze_pdf.AnalysisError):
                    analyze_pdf.analyze(pdf, cache_dir=root / 'cache')
            self.assertFalse(list(root.glob('cache/*.json')))

    def test_checkpoint_survives_failure_and_config_invalidates_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf = root / 'source.pdf'
            pdf.write_bytes(b'%PDF-1.4 fixture')
            tools = {'pdfinfo': {'path': 'pdfinfo'}, 'pdftotext': {'path': 'pdftotext'}}
            def run(command, timeout):
                if command[0] == 'pdfinfo':
                    return subprocess.CompletedProcess(command, 0, 'Pages: 2\n', '')
                if command[command.index('-f') + 1] == '2':
                    raise analyze_pdf.AnalysisError('page failed')
                return subprocess.CompletedProcess(command, 0, 'math question ' * 10, '')
            with patch.object(analyze_pdf, 'tool_fingerprints', return_value=tools), patch.object(analyze_pdf, 'run_tool', side_effect=run):
                with self.assertRaises(analyze_pdf.AnalysisError):
                    analyze_pdf.analyze(pdf, cache_dir=root / 'cache')
                resumed = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1])
                self.assertEqual(resumed['cache']['hits'], 1)
                changed = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1], min_chars=200)
                self.assertEqual(changed['cache']['misses'], 1)
                self.assertEqual(changed['pages'][0]['classification'], 'review')
                with patch.object(analyze_pdf, 'VERSION', 2):
                    versioned = analyze_pdf.analyze(pdf, cache_dir=root / 'cache', pages=[1])
                    self.assertEqual(versioned['cache']['misses'], 1)
                uncached = analyze_pdf.analyze(pdf, cache_dir=None, pages=[1])
                self.assertFalse(uncached['cache']['enabled'])
                self.assertEqual(uncached['cache']['misses'], 1)

    def test_tool_errors_are_bounded_and_do_not_retry(self):
        with patch.object(analyze_pdf.subprocess, 'run', side_effect=subprocess.TimeoutExpired('pdfinfo', 1)) as run:
            with self.assertRaises(analyze_pdf.AnalysisError):
                analyze_pdf.run_tool(['pdfinfo', 'source.pdf'], 1)
            self.assertEqual(run.call_count, 1)
        with patch.object(analyze_pdf.subprocess, 'run', return_value=subprocess.CompletedProcess([], 3, '', 'broken PDF')):
            with self.assertRaisesRegex(analyze_pdf.AnalysisError, 'exited 3'):
                analyze_pdf.run_tool(['pdfinfo', 'source.pdf'], 1)

    @unittest.skipUnless(shutil.which('pdfinfo') and shutil.which('pdftotext'), 'Poppler required')
    def test_real_poppler_text_image_and_blank_pages(self):
        # A valid three-page PDF: native text, image-only, genuinely blank.
        # This distinction cannot be resolved from text extraction alone.
        text = b'BT /F1 12 Tf 30 700 Td (A real text-layer mathematical question x = 2 repeated for testing.) Tj ET'
        image = b'q 100 0 0 100 30 500 cm /Im1 Do Q'
        objects = [
            b'<< /Type /Catalog /Pages 2 0 R >>',
            b'<< /Type /Pages /Kids [3 0 R 4 0 R 5 0 R] /Count 3 >>',
            b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 6 0 R >> >> /Contents 7 0 R >>',
            b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /XObject << /Im1 8 0 R >> >> /Contents 9 0 R >>',
            b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << >> /Contents 10 0 R >>',
            b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
            b'<< /Length ' + str(len(text)).encode() + b' >>\nstream\n' + text + b'\nendstream',
            b'<< /Type /XObject /Subtype /Image /Width 1 /Height 1 /ColorSpace /DeviceGray /BitsPerComponent 8 /Length 1 >>\nstream\n\x00\nendstream',
            b'<< /Length ' + str(len(image)).encode() + b' >>\nstream\n' + image + b'\nendstream',
            b'<< /Length 0 >>\nstream\n\nendstream',
        ]
        value = b'%PDF-1.4\n'
        offsets = [0]
        for number, obj in enumerate(objects, 1):
            offsets.append(len(value))
            value += str(number).encode() + b' 0 obj\n' + obj + b'\nendobj\n'
        xref = len(value)
        value += b'xref\n0 11\n0000000000 65535 f \n'
        value += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
        value += f'trailer\n<< /Size 11 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode()
        with tempfile.TemporaryDirectory() as temp:
            pdf = Path(temp) / 'mixed.pdf'
            pdf.write_bytes(value)
            result = analyze_pdf.analyze(pdf, cache_dir=Path(temp) / 'cache')
            self.assertEqual(result['page_count'], 3)
            self.assertEqual([p['classification'] for p in result['pages']],
                             ['text_candidate', 'needs_ocr_or_blank', 'needs_ocr_or_blank'])
            self.assertEqual(result['document_classification'], 'mixed_candidates')
            repeat = analyze_pdf.analyze(pdf, cache_dir=Path(temp) / 'cache')
            self.assertEqual(repeat['cache']['hits'], 3)
            self.assertEqual(repeat['cache']['misses'], 0)


if __name__ == '__main__':
    unittest.main()

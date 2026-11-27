#!/usr/bin/env python3
"""OCR only selected raster-backed PDF pages; every result remains unverified."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import time

import analyze_pdf

VERSION = 1
DEFAULT_CACHE = Path(__file__).resolve().parents[1] / '.work/ocr-page-cache'
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
LANGUAGE_CODE = re.compile(r'^[A-Za-z0-9_]+$')


class OcrPdfError(ValueError):
    pass


def run_tool(command, timeout):
    try:
        return analyze_pdf.run_tool(command, timeout)
    except analyze_pdf.AnalysisError as error:
        raise OcrPdfError(str(error)) from error


def parse_languages(value):
    languages = value.split('+')
    if not value or any(not LANGUAGE_CODE.fullmatch(language) for language in languages):
        raise OcrPdfError('Languages must be Tesseract codes joined by +, for example chi_sim+eng')
    if len(set(languages)) != len(languages):
        raise OcrPdfError('Duplicate Tesseract language codes are not allowed')
    return languages


def manifest_source_sha256(manifest_path, source_id):
    if source_id is None:
        raise OcrPdfError('source_id is required when a source manifest is supplied')
    try:
        manifest = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise OcrPdfError(f'Cannot read source manifest: {error}') from error
    sources = manifest.get('sources') if isinstance(manifest, dict) else None
    if not isinstance(sources, list):
        raise OcrPdfError('Source manifest must contain a sources array')
    matches = [source for source in sources
               if isinstance(source, dict) and source.get('source_id') == source_id]
    if len(matches) != 1:
        raise OcrPdfError(f'source_id must identify exactly one manifest entry: {source_id}')
    artifact = matches[0].get('artifact')
    sha256 = artifact.get('sha256') if isinstance(artifact, dict) else None
    if not isinstance(sha256, str) or re.fullmatch(r'[0-9a-fA-F]{64}', sha256) is None:
        raise OcrPdfError(f'Manifest source_id has no valid artifact SHA-256: {source_id}')
    return sha256.lower()


def _executable(name, args, pattern, timeout):
    path = shutil.which(name)
    if not path:
        raise OcrPdfError(f'Missing executable: {name}')
    path = str(Path(path).resolve())
    result = run_tool([path, *args], timeout)
    output = result.stdout + '\n' + result.stderr
    match = re.search(pattern, output, re.IGNORECASE)
    if not match:
        raise OcrPdfError(f'Unrecognized {name} version output')
    return {'path': path, 'version': match.group(1), 'sha256': analyze_pdf.digest_file(path)}, output


def tool_fingerprints(languages, timeout):
    requested = parse_languages(languages)
    renderer, _ = _executable('pdftoppm', ['-v'], r'pdftoppm\s+version\s+(\S+)', timeout)
    engine, _ = _executable('tesseract', ['--version'], r'tesseract\s+(\S+)', timeout)
    listed = run_tool([engine['path'], '--list-langs'], timeout)
    output = listed.stdout + '\n' + listed.stderr
    header = next((line for line in output.splitlines()
                   if line.startswith('List of available languages in ')), None)
    if not header:
        raise OcrPdfError('Tesseract did not report its tessdata directory')
    directory_match = re.search(r'List of available languages in ["\']?(.+?)["\']?\s+\(\d+\)', header)
    if not directory_match:
        raise OcrPdfError('Cannot parse Tesseract tessdata directory')
    tessdata_dir = str(Path(directory_match.group(1)).resolve())
    available = {line.strip() for line in output.splitlines()
                 if LANGUAGE_CODE.fullmatch(line.strip())}
    missing = sorted(set(requested) - available)
    if missing:
        raise OcrPdfError(f'Tesseract language data unavailable: {", ".join(missing)}')
    model_hashes = {}
    for language in requested:
        model = Path(tessdata_dir) / f'{language}.traineddata'
        if not model.is_file():
            raise OcrPdfError(f'Missing Tesseract traineddata: {model.name}')
        model_hashes[language] = analyze_pdf.digest_file(model)
    engine.update({'tessdata_dir': tessdata_dir,
                   'languages': requested, 'traineddata_sha256': model_hashes})
    return {'renderer': renderer, 'tesseract': engine}


def png_dimensions(path):
    data = Path(path).read_bytes()
    if len(data) < 24 or not data.startswith(PNG_SIGNATURE) or data[12:16] != b'IHDR':
        raise OcrPdfError('Page renderer did not produce a valid PNG header')
    width, height = struct.unpack('>II', data[16:24])
    if width < 1 or height < 1:
        raise OcrPdfError('Rendered page has invalid dimensions')
    return width, height


def render_page(pdf, page, dpi, renderer, cache_dir, timeout):
    key = {'version': VERSION, 'pdf_sha256': analyze_pdf.digest_file(pdf), 'page': page,
           'dpi': dpi, 'renderer': renderer, 'format': 'png'}
    key_hash = hashlib.sha256(analyze_pdf.canonical(key).encode()).hexdigest()
    cached_path = Path(cache_dir) / 'render' / f'{key_hash}.png' if cache_dir is not None else None
    if cached_path is not None and cached_path.is_file():
        try:
            cached_record = read_enveloped_cache(cached_path.with_suffix('.json'), key)
            dimensions = png_dimensions(cached_path)
            if (cached_record is not None
                    and cached_record.get('image_sha256') == analyze_pdf.digest_file(cached_path)
                    and cached_record.get('dimensions_px') == list(dimensions)):
                return cached_path, dimensions, True, None
        except (OcrPdfError, OSError):
            pass

    temporary = None
    if cached_path is None:
        temporary = tempfile.TemporaryDirectory(prefix='gaokao-ocr-page-')
        render_directory = Path(temporary.name)
        destination = render_directory / 'page.png'
        output_base = render_directory / 'page'
    else:
        render_directory = cached_path.parent
        render_directory.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix='.render-', dir=render_directory)
        output_base = Path(temporary.name) / 'page'
        destination = cached_path

    try:
        run_tool([renderer['path'], '-f', str(page), '-l', str(page), '-r', str(dpi),
                  '-png', '-singlefile', str(pdf), str(output_base)], timeout)
        rendered = Path(str(output_base) + '.png')
        dimensions = png_dimensions(rendered)
        if cached_path is None:
            return rendered, dimensions, False, temporary
        os.replace(rendered, destination)
        analyze_pdf.write_cache(cached_path.with_suffix('.json'), {
            'key': key, 'image_sha256': analyze_pdf.digest_file(destination),
            'dimensions_px': list(dimensions)})
        return destination, dimensions, False, temporary
    except Exception:
        temporary.cleanup()
        raise


def read_enveloped_cache(path, key):
    try:
        record = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(record, dict) or not isinstance(record.get('body'), dict):
            return None
        body = record['body']
        if (record.get('sha256') != hashlib.sha256(analyze_pdf.canonical(body).encode()).hexdigest()
                or body.get('key') != key):
            return None
        return body
    except (OSError, ValueError, KeyError, TypeError):
        return None


def read_result_cache(path, key):
    body = read_enveloped_cache(path, key)
    return body if body is not None and isinstance(body.get('output'), str) else None


def recognize_page(image, page, pdf_hash, source_id, dimensions, dpi,
                   languages, psm, engine, cache_dir, timeout):
    image_hash = analyze_pdf.digest_file(image)
    language_codes = parse_languages(languages)
    key = {'version': VERSION, 'pdf_sha256': pdf_hash, 'page': page,
           'image_sha256': image_hash, 'dpi': dpi, 'languages': language_codes,
           'psm': psm, 'engine': engine}
    key_hash = hashlib.sha256(analyze_pdf.canonical(key).encode()).hexdigest()
    cache_path = Path(cache_dir) / 'results' / f'{key_hash}.json' if cache_dir is not None else None
    body = read_result_cache(cache_path, key) if cache_path is not None and cache_path.is_file() else None
    cache_hit = body is not None
    if not cache_hit:
        result = run_tool([engine['path'], str(image), 'stdout', '--tessdata-dir', engine['tessdata_dir'],
                           '-l', '+'.join(language_codes), '--psm', str(psm), '--dpi', str(dpi)], timeout)
        output = result.stdout.strip()
        body = {'key': key, 'output': output}
        if cache_path is not None:
            analyze_pdf.write_cache(cache_path, body)

    status = 'recognized_unverified' if body['output'] else 'empty_unverified'
    metadata = {'source_sha256': pdf_hash, 'source_page': page, 'task': 'page_text',
                'render_dpi': dpi, 'bbox_px': [0, 0, dimensions[0], dimensions[1]],
                'bbox_coordinate_space': 'rendered_page_px_top_left',
                'image_sha256': image_hash}
    if source_id:
        metadata['source_id'] = source_id
    return {'case_id': f'{source_id or pdf_hash}:page-{page}:page_text',
            'engine': 'tesseract', 'engine_version': engine['version'],
            'output': body['output'], 'metadata': metadata,
            'extraction_status': status, 'review_status': 'needs-review',
            'mathematical_verification_status': 'not_verified',
            'cache_key': key_hash, 'cache_hit': cache_hit,
            'image_sha256': image_hash, 'page_width_px': dimensions[0],
            'page_height_px': dimensions[1]}


def process_pdf(pdf, *, source_id=None, expected_sha256=None, manifest_path=None, pages=None, dpi=180, languages='chi_sim+eng',
                psm=3, cache_dir=DEFAULT_CACHE,
                analysis_cache_dir=analyze_pdf.DEFAULT_CACHE, min_chars=40, timeout=120):
    started = time.monotonic()
    pdf = Path(pdf).resolve()
    if not pdf.is_file() or dpi < 72 or dpi > 600 or not 0 <= psm <= 13 or timeout <= 0 or min_chars < 1:
        raise OcrPdfError('Require an existing PDF, DPI 72..600, PSM 0..13, positive timeout and min_chars')
    if source_id is not None and (not isinstance(source_id, str)
                                  or not source_id.strip() or source_id != source_id.strip()):
        raise OcrPdfError('source_id must be a non-empty, trimmed string when supplied')
    if expected_sha256 is not None:
        if not isinstance(expected_sha256, str) or re.fullmatch(r'[0-9a-fA-F]{64}', expected_sha256) is None:
            raise OcrPdfError('expected_sha256 must contain exactly 64 hexadecimal characters')
        expected_sha256 = expected_sha256.lower()
    source_identity_status = 'unbound'
    if manifest_path is not None:
        manifest_sha256 = manifest_source_sha256(manifest_path, source_id)
        if expected_sha256 is not None and expected_sha256 != manifest_sha256:
            raise OcrPdfError('expected_sha256 conflicts with manifest source identity')
        expected_sha256 = manifest_sha256
        source_identity_status = 'manifest_verified'
    elif source_id is not None:
        source_identity_status = 'caller_supplied'
    languages = '+'.join(parse_languages(languages))
    if pages is not None:
        if not pages or any(type(page) is not int or page < 1 for page in pages):
            raise OcrPdfError('Explicit page numbers must be positive integers')
        selected_pages = sorted(set(pages))
        selection_mode = 'explicit_page_override'
    else:
        selected_pages = None
        selection_mode = 'automatic_raster_candidates'
    with pdf.open('rb') as stream:
        if not stream.read(1024).lstrip().startswith(b'%PDF-'):
            raise OcrPdfError('Input has no PDF header')
    pdf_hash = analyze_pdf.digest_file(pdf)
    if expected_sha256 is not None and pdf_hash != expected_sha256:
        if source_identity_status == 'manifest_verified':
            raise OcrPdfError(f'PDF manifest SHA-256 mismatch: expected {expected_sha256}, got {pdf_hash}')
        raise OcrPdfError(f'PDF SHA-256 mismatch: expected {expected_sha256}, got {pdf_hash}')

    try:
        analysis = analyze_pdf.analyze(pdf, cache_dir=analysis_cache_dir,
                                       pages=selected_pages, min_chars=min_chars, timeout=timeout)
    except analyze_pdf.AnalysisError as error:
        raise OcrPdfError(str(error)) from error
    if analysis.get('pdf_sha256') != pdf_hash or type(analysis.get('page_count')) is not int:
        raise OcrPdfError('PDF identity or page count changed during pre-analysis')
    page_count = analysis['page_count']
    if selected_pages is not None and any(page > page_count for page in selected_pages):
        raise OcrPdfError(f'Pages must lie in 1..{page_count}')
    page_map = {item.get('page'): item for item in analysis.get('pages', [])}

    selected = []
    skipped = []
    if selected_pages is not None:
        for page in selected_pages:
            if page not in page_map:
                raise OcrPdfError(f'Pre-analysis omitted explicitly selected page {page}')
            selected.append((page, 'explicit_page_override'))
    else:
        if not analysis.get('complete_document'):
            raise OcrPdfError('Automatic page selection requires complete-document analysis')
        for page in range(1, page_count + 1):
            evidence = page_map.get(page)
            if evidence is None:
                raise OcrPdfError(f'Pre-analysis omitted page {page}')
            if evidence.get('classification') == 'needs_ocr_or_blank' and evidence.get('content_evidence') == 'raster_only':
                selected.append((page, 'no_text_layer_raster_evidence'))
            elif evidence.get('classification') == 'text_candidate':
                skipped.append({'page': page, 'reason': 'native_text_candidate'})
            elif evidence.get('classification') == 'review':
                skipped.append({'page': page, 'reason': 'text_layer_requires_review_or_override'})
            elif evidence.get('content_evidence') != 'raster_only':
                skipped.append({'page': page, 'reason': 'no_raster_evidence'})
            else:
                skipped.append({'page': page, 'reason': 'text_layer_requires_review_or_override'})

    if not selected:
        return {'schema_version': VERSION, 'pdf_sha256': pdf_hash, 'source_id': source_id,
                'source_identity_status': source_identity_status,
                'page_count': page_count, 'selection_mode': selection_mode,
                'selected_pages': [], 'skipped_pages': skipped, 'pages': [],
                'cache_hits': 0, 'render_cache_hits': 0, 'ocr_calls': 0,
                'elapsed_seconds': round(time.monotonic() - started, 6),
                'limitation': 'No OCR candidates selected; page analysis is not a content acceptance gate.'}

    toolchain = tool_fingerprints(languages, timeout)
    if cache_dir is not None:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
    output = []
    ocr_calls = cache_hits = render_cache_hits = 0
    for page, reason in selected:
        image, dimensions, render_cache_hit, temporary = render_page(
            pdf, page, dpi, toolchain['renderer'], cache_dir, timeout)
        render_cache_hits += int(render_cache_hit)
        try:
            result = recognize_page(image, page, pdf_hash, source_id, dimensions,
                                    dpi, languages, psm, toolchain['tesseract'], cache_dir, timeout)
            if analyze_pdf.digest_file(pdf) != pdf_hash:
                raise OcrPdfError('PDF changed during OCR; result not accepted')
            result.update({'source_page': page, 'selection_reason': reason,
                           'render_cache_hit': render_cache_hit})
            cache_hits += int(result['cache_hit'])
            ocr_calls += int(not result['cache_hit'])
            output.append(result)
        finally:
            if temporary is not None:
                temporary.cleanup()

    return {'schema_version': VERSION, 'pdf_sha256': pdf_hash, 'source_id': source_id,
            'source_identity_status': source_identity_status,
            'page_count': page_count, 'selection_mode': selection_mode,
            'selected_pages': [page for page, _ in selected], 'skipped_pages': skipped,
            'pages': output, 'toolchain': toolchain,
            'cache_hits': cache_hits, 'render_cache_hits': render_cache_hits,
            'ocr_calls': ocr_calls,
            'elapsed_seconds': round(time.monotonic() - started, 6),
            'limitation': 'OCR text is an unverified candidate. It never updates canonical question, answer or solution sources.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--source-id', help='Optional source-manifest ID for traceable run metadata')
    parser.add_argument('--manifest', type=Path,
                        help='Bind --source-id and the input PDF SHA-256 to source-manifest.json')
    parser.add_argument('--expected-sha256', help='Reject a PDF not matching this SHA-256 before analysis or OCR')
    parser.add_argument('--page', type=int, action='append', help='Repeat to OCR explicit pages, even if text exists')
    parser.add_argument('--dpi', type=int, default=180)
    parser.add_argument('--languages', default='chi_sim+eng')
    parser.add_argument('--psm', type=int, default=3)
    parser.add_argument('--cache-dir', type=Path, default=DEFAULT_CACHE)
    parser.add_argument('--no-cache', action='store_true')
    parser.add_argument('--include-text', action='store_true', help='Include OCR output; default compact metadata only')
    parser.add_argument('--min-chars', type=int, default=40)
    parser.add_argument('--timeout', type=float, default=120)
    args = parser.parse_args(argv)
    try:
        result = process_pdf(args.pdf, source_id=args.source_id, expected_sha256=args.expected_sha256,
                             manifest_path=args.manifest, pages=args.page,
                             dpi=args.dpi, languages=args.languages, psm=args.psm,
                             cache_dir=None if args.no_cache else args.cache_dir,
                             analysis_cache_dir=None if args.no_cache else analyze_pdf.DEFAULT_CACHE,
                             min_chars=args.min_chars, timeout=args.timeout)
    except (OcrPdfError, OSError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False))
        return 1
    if not args.include_text:
        for page in result['pages']:
            page.pop('output', None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

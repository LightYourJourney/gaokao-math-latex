#!/usr/bin/env python3
"""Deterministic, cached PDF text-layer triage; never a content acceptance gate."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import unicodedata

VERSION = 2
DEFAULT_CACHE = Path(__file__).resolve().parents[1] / '.work/pdf-analysis-cache'
IMAGE_ROW = re.compile(r'^\s*(\d+)\s+\d+\s+(\w+)\s+(\d+)\s+(\d+)\b')


class AnalysisError(ValueError):
    pass


def digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def run_tool(command, timeout):
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                encoding='utf-8', errors='strict', timeout=timeout)
    except (OSError, subprocess.SubprocessError, UnicodeError) as error:
        raise AnalysisError(f'{Path(command[0]).name}: {error}') from error
    if result.returncode:
        raise AnalysisError(f'{Path(command[0]).name} exited {result.returncode}: {result.stderr[:1200]}')
    return result


def tool_fingerprints(timeout):
    tools = {}
    for name in ('pdfinfo', 'pdftotext', 'pdfimages'):
        executable = shutil.which(name)
        if not executable:
            raise AnalysisError(f'Missing executable: {name}')
        executable = str(Path(executable).resolve())
        result = run_tool([executable, '-v'], timeout)
        match = re.search(rf'{name} version (\S+)', result.stdout + result.stderr)
        if not match:
            raise AnalysisError(f'Unrecognized {name} version')
        tools[name] = {'path': executable, 'version': match.group(1),
                       'sha256': digest_file(executable)}
    return tools


def parse_image_inventory(output, page_count):
    """Return per-page raster-object evidence from Poppler's pdfimages -list."""
    if not re.search(r'^\s*page\s+num\s+type\s+width\s+height\b', output, re.MULTILINE):
        raise AnalysisError('pdfimages output has no recognized image-list header')
    pages = {number: {'image_objects': 0, 'auxiliary_mask_objects': 0,
                      'largest_image_px': None}
             for number in range(1, page_count + 1)}
    for line in output.splitlines():
        match = IMAGE_ROW.match(line)
        if not match:
            if re.match(r'^\s*\d+\s+\d+\s+', line):
                raise AnalysisError(f'Unrecognized pdfimages row: {line[:160]}')
            continue
        page_number, image_type, width, height = match.groups()
        page_number, width, height = int(page_number), int(width), int(height)
        if not 1 <= page_number <= page_count or width < 1 or height < 1:
            raise AnalysisError('pdfimages reported an invalid page or image dimension')
        stats = pages[page_number]
        if image_type.lower() in ('image', 'stencil'):
            stats['image_objects'] += 1
        elif image_type.lower() in ('mask', 'smask'):
            stats['auxiliary_mask_objects'] += 1
        else:
            raise AnalysisError(f'Unsupported pdfimages object type: {image_type}')
        size = [width, height]
        if stats['largest_image_px'] is None or width * height > stats['largest_image_px'][0] * stats['largest_image_px'][1]:
            stats['largest_image_px'] = size
    return pages


def content_evidence(text_chars, image_stats):
    has_text = text_chars > 0
    has_raster = image_stats['image_objects'] + image_stats['auxiliary_mask_objects'] > 0
    if has_text and has_raster:
        return 'text_and_raster'
    if has_text:
        return 'text_layer'
    if has_raster:
        return 'raster_only'
    return 'no_text_or_raster'


def document_content_classification(pages):
    evidence = {page['content_evidence'] for page in pages}
    has_text = bool(evidence & {'text_layer', 'text_and_raster'})
    has_raster = bool(evidence & {'raster_only', 'text_and_raster'})
    has_raster_only_page = 'raster_only' in evidence
    if has_text and has_raster_only_page:
        return 'mixed_text_and_raster_candidates'
    if has_text and has_raster:
        return 'text_with_raster_content_candidate'
    if has_text:
        return 'text_layer_candidate'
    if has_raster:
        return 'raster_only_candidate'
    return 'blank_or_unrecognized'


def assess_text(text, min_chars):
    count = sum(not char.isspace() for char in text)
    suspicious = sum(char == '\ufffd' or unicodedata.category(char) in ('Co', 'Cn')
                     or (unicodedata.category(char) == 'Cc' and char not in '\n\r\t\f')
                     for char in text)
    classification = ('needs_ocr_or_blank' if count == 0 else
                      'review' if count < min_chars or suspicious else 'text_candidate')
    return {'text': text, 'non_whitespace_chars': count,
            'suspicious_chars': suspicious, 'classification': classification,
            'requires_content_review': True}


def read_cache(path, key):
    try:
        record = json.loads(path.read_text(encoding='utf-8'))
        body = record['body']
        if record['sha256'] != hashlib.sha256(canonical(body).encode()).hexdigest():
            return None
        if body['key'] != key or type(body['page_count']) is not int or body['page_count'] < 1:
            return None
        if not isinstance(body['pages'], dict) or not isinstance(body.get('raster_pages'), dict):
            return None
        if set(body['raster_pages']) != {str(number) for number in range(1, body['page_count'] + 1)}:
            return None
        for stats in body['raster_pages'].values():
            if (not isinstance(stats, dict)
                    or type(stats.get('image_objects')) is not int or stats['image_objects'] < 0
                    or type(stats.get('auxiliary_mask_objects')) is not int or stats['auxiliary_mask_objects'] < 0
                    or (stats.get('largest_image_px') is not None
                        and (not isinstance(stats['largest_image_px'], list)
                             or len(stats['largest_image_px']) != 2
                             or any(type(value) is not int or value < 1 for value in stats['largest_image_px'])))):
                return None
        for number, page in body['pages'].items():
            if str(int(number)) != number or not 1 <= int(number) <= body['page_count']:
                return None
            if not isinstance(page, dict) or not isinstance(page.get('text'), str):
                return None
        return body
    except (OSError, ValueError, KeyError, TypeError):
        return None


def write_cache(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {'body': body, 'sha256': hashlib.sha256(canonical(body).encode()).hexdigest()}
    descriptor, temporary = tempfile.mkstemp(prefix='.analysis-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            stream.write(canonical(record) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def analyze(pdf, *, cache_dir=DEFAULT_CACHE, pages=None, min_chars=40, timeout=60):
    started = time.monotonic()
    pdf = Path(pdf).resolve()
    if not pdf.is_file() or min_chars < 1 or timeout <= 0:
        raise AnalysisError('Require an existing PDF, positive min_chars and timeout')
    with pdf.open('rb') as stream:
        if not stream.read(1024).lstrip().startswith(b'%PDF-'):
            raise AnalysisError('Input has no PDF header')
    pdf_hash = digest_file(pdf)
    tools = tool_fingerprints(timeout)
    key = {'version': VERSION, 'pdf_sha256': pdf_hash, 'tools': tools,
           'min_chars': min_chars, 'extraction': 'layout-utf8+pdfimages-list'}
    key_hash = hashlib.sha256(canonical(key).encode()).hexdigest()
    cache_path = Path(cache_dir) / (key_hash + '.json') if cache_dir is not None else None
    body = read_cache(cache_path, key) if cache_path is not None else None
    if body is None:
        info = run_tool([tools['pdfinfo']['path'], str(pdf)], timeout).stdout
        match = re.search(r'^Pages:\s*(\d+)\s*$', info, re.MULTILINE)
        if not match or int(match.group(1)) < 1:
            raise AnalysisError('pdfinfo did not provide a positive page count')
        page_count = int(match.group(1))
        image_listing = run_tool([tools['pdfimages']['path'], '-list', str(pdf)], timeout).stdout
        raster_pages = parse_image_inventory(image_listing, page_count)
        body = {'key': key, 'page_count': page_count, 'pages': {},
                'raster_pages': {str(number): stats for number, stats in raster_pages.items()}}
    selected = sorted(set(pages)) if pages is not None else list(range(1, body['page_count'] + 1))
    if not selected or any(type(p) is not int or not 1 <= p <= body['page_count'] for p in selected):
        raise AnalysisError(f'Pages must lie in 1..{body["page_count"]}')
    hits = 0
    output = []
    for number in selected:
        page = body['pages'].get(str(number))
        if page is None:
            result = run_tool([tools['pdftotext']['path'], '-enc', 'UTF-8', '-layout',
                               '-f', str(number), '-l', str(number), str(pdf), '-'], timeout)
            page = assess_text(result.stdout.rstrip('\f'), min_chars)
            body['pages'][str(number)] = page
            if digest_file(pdf) != pdf_hash:
                raise AnalysisError('PDF changed during analysis; current page not cached')
            if cache_path is not None:
                write_cache(cache_path, body)
        else:
            hits += 1
            page = assess_text(page['text'], min_chars)
        image_stats = body['raster_pages'][str(number)]
        output.append({'page': number, **page, **image_stats,
                       'content_evidence': content_evidence(page['non_whitespace_chars'], image_stats)})
    if digest_file(pdf) != pdf_hash:
        raise AnalysisError('PDF changed during analysis; no cache written')
    kinds = {page['classification'] for page in output}
    classification = next(iter(kinds)) if len(kinds) == 1 else 'mixed_candidates'
    return {'schema_version': VERSION, 'pdf_sha256': pdf_hash, 'source_path': str(pdf),
            'page_count': body['page_count'], 'analyzed_pages': selected,
            'complete_document': len(selected) == body['page_count'],
            'document_classification': classification, 'pages': output,
            'document_content_classification': document_content_classification(output),
            'toolchain': tools, 'cache': {'enabled': cache_path is not None,
                'key': key_hash, 'hits': hits, 'misses': len(selected) - hits},
            'elapsed_seconds': round(time.monotonic() - started, 6),
            'model_calls': 0, 'ocr_calls': 0,
            'limitation': 'Text presence does not prove fidelity; empty pages may be blank or scanned. Mathematical and visual review remain required.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--page', type=int, action='append', help='Repeat for selected pages; default all')
    parser.add_argument('--cache-dir', type=Path, default=DEFAULT_CACHE)
    parser.add_argument('--no-cache', action='store_true')
    parser.add_argument('--include-text', action='store_true', help='Include extracted text; default compact metrics only')
    parser.add_argument('--min-chars', type=int, default=40)
    parser.add_argument('--timeout', type=float, default=60)
    args = parser.parse_args(argv)
    try:
        result = analyze(args.pdf, pages=args.page, cache_dir=None if args.no_cache else args.cache_dir,
                         min_chars=args.min_chars, timeout=args.timeout)
    except (AnalysisError, OSError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False))
        return 1
    if not args.include_text:
        for page in result['pages']:
            page.pop('text')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

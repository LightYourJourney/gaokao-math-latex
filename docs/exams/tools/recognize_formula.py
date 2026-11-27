#!/usr/bin/env python3
"""Local PaddleOCR formula crops with content-addressed results and explicit review."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from analyze_pdf import canonical, digest_file, write_cache

VERSION = 1
DEFAULT_CACHE = Path(__file__).resolve().parents[1] / '.work/formula-cache'
MARKER = 'GK_FORMULA_RESULT='


class FormulaError(ValueError):
    pass


def engine_metadata(python, timeout):
    # Retain the venv executable path: resolving its symlink would lose the venv.
    code = ('import json,platform; from importlib.metadata import version; '
            'print(json.dumps({"python":platform.python_version(), '
            '"packages":{name:version(name) for name in '
            '("paddleocr","paddlepaddle","paddlex","numpy")}}))')
    try:
        result = subprocess.run([str(python), '-c', code], capture_output=True,
                                text=True, timeout=timeout, check=True)
        return json.loads(result.stdout)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        raise FormulaError('OCR environment unavailable; install the pinned optional dependencies in a venv') from error


def model_fingerprint(directory):
    files = {path.relative_to(directory).as_posix(): digest_file(path)
             for path in sorted(directory.rglob('*')) if path.is_file()}
    if not files:
        raise FormulaError('Model directory must contain local model files')
    return hashlib.sha256(canonical(files).encode()).hexdigest()


def run_prediction(python, image, model_dir, model_name, timeout):
    command = [str(python), str(Path(__file__).resolve()), str(image),
               '--model-dir', str(model_dir), '--model-name', model_name, '--worker']
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError) as error:
        raise FormulaError(f'OCR worker failed or timed out: {error}') from error
    records = [line[len(MARKER):] for line in result.stdout.splitlines() if line.startswith(MARKER)]
    if result.returncode or len(records) != 1:
        raise FormulaError(f'OCR worker exited {result.returncode}: {result.stderr[-1800:]}')
    try:
        return json.loads(records[0])
    except ValueError as error:
        raise FormulaError('OCR worker returned invalid JSON') from error


def recognize(image, model_dir, *, engine_python=sys.executable,
              model_name='PP-FormulaNet_plus-S', cache_dir=DEFAULT_CACHE, timeout=300):
    started = time.monotonic()
    image, model_dir = Path(image).resolve(), Path(model_dir).resolve()
    python = Path(engine_python).absolute()
    if not image.is_file() or not model_dir.is_dir() or timeout <= 0:
        raise FormulaError('Require an input image, local model directory and positive timeout')
    image_hash = digest_file(image)
    model_hash = model_fingerprint(model_dir)
    metadata = engine_metadata(python, min(timeout, 30))
    key = {'version': VERSION, 'image_sha256': image_hash,
           'model_tree_sha256': model_hash, 'model_name': model_name,
           'engine_python': str(python), 'engine': metadata,
           'config': {'device': 'cpu', 'cpu_threads': 4, 'enable_mkldnn': False}}
    key_hash = hashlib.sha256(canonical(key).encode()).hexdigest()
    cache_path = Path(cache_dir) / (key_hash + '.json') if cache_dir is not None else None
    body = None
    if cache_path is not None:
        try:
            envelope = json.loads(cache_path.read_text(encoding='utf-8'))
            candidate = envelope['body']
            valid = envelope['sha256'] == hashlib.sha256(canonical(candidate).encode()).hexdigest()
            if valid and candidate['key'] == key and isinstance(candidate['prediction']['latex'], str) and candidate['prediction']['latex'].strip():
                body = candidate
        except (OSError, ValueError, KeyError, TypeError):
            pass
    cache_hit = body is not None
    if not cache_hit:
        prediction = run_prediction(python, image, model_dir, model_name, timeout)
        if not isinstance(prediction, dict) or not isinstance(prediction.get('latex'), str) or not prediction['latex'].strip():
            raise FormulaError('No formula recognized; do not accept or cache an empty result')
        if digest_file(image) != image_hash or model_fingerprint(model_dir) != model_hash:
            raise FormulaError('Image or model changed during inference; result not cached')
        body = {'key': key, 'prediction': prediction}
        if cache_path is not None:
            write_cache(cache_path, body)
    return {'schema_version': VERSION, 'image_sha256': image_hash,
            'model_name': model_name, 'model_tree_sha256': model_hash,
            'engine': metadata, 'prediction': body['prediction'],
            'extraction_status': 'recognized_unverified', 'review_status': 'needs-review',
            'mathematical_verification_status': 'not_verified',
            'cache_key': key_hash, 'cache_hit': cache_hit,
            'local_ocr_calls_this_run': 0 if cache_hit else 1,
            'elapsed_seconds': round(time.monotonic() - started, 6)}


def worker(image, model_dir, model_name):
    import resource
    from paddleocr import FormulaRecognition

    started = time.monotonic()
    model = FormulaRecognition(model_name=model_name, model_dir=str(model_dir),
                               device='cpu', cpu_threads=4, enable_mkldnn=False)
    loaded = time.monotonic()
    output = list(model.predict(input=str(image), batch_size=1))
    finished = time.monotonic()
    if len(output) != 1:
        raise FormulaError('Expected exactly one formula crop result')
    result = {'latex': output[0]['rec_formula'],
              'model_load_seconds': round(loaded - started, 6),
              'predict_seconds': round(finished - loaded, 6),
              'peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                               * (1 if sys.platform == 'darwin' else 1024)}
    print(MARKER + json.dumps(result, ensure_ascii=False))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('--model-dir', type=Path, required=True)
    parser.add_argument('--model-name', default='PP-FormulaNet_plus-S')
    parser.add_argument('--engine-python', type=Path, default=Path(sys.executable))
    parser.add_argument('--cache-dir', type=Path, default=DEFAULT_CACHE)
    parser.add_argument('--no-cache', action='store_true')
    parser.add_argument('--timeout', type=float, default=300)
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        if args.worker:
            worker(args.image, args.model_dir, args.model_name)
        else:
            result = recognize(args.image, args.model_dir, engine_python=args.engine_python,
                               model_name=args.model_name, cache_dir=None if args.no_cache else args.cache_dir,
                               timeout=args.timeout)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except (FormulaError, OSError) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

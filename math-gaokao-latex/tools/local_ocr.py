#!/usr/bin/env python3
"""Local OCR routing. Outputs are candidates, never canonical question sources."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import tempfile
import time

import analyze_pdf
import ocr_pdf
from ocr_candidate_ir import convert_run

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'tools/ocr-local-models.json'
WORK = ROOT / '.work/ocr-local'
VERSION = 1


def sha(path):
    return analyze_pdf.digest_file(path)


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Atomic publication: do not leave a partial JSON on interruption.
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     prefix='.ocr-', delete=False) as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        temp = Path(stream.name)
    os.replace(temp, path)


def model_tree(directory):
    directory = Path(directory)
    files = {p.relative_to(directory).as_posix(): sha(p)
             for p in sorted(directory.rglob('*'))
             if p.is_file() and not any(s.startswith('.') for s in p.relative_to(directory).parts)}
    if not files:
        raise ValueError(f'Model files missing: {directory}')
    return hashlib.sha256(analyze_pdf.canonical(files).encode()).hexdigest()


def engine_config(name, config=CONFIG):
    spec = load(config)['engines'][name]
    spec = dict(spec)
    for key in ('python', 'worker', 'model_dir'):
        spec[key] = str((ROOT / spec[key]).resolve()) if key != 'python' else str(ROOT / spec[key])
        if not Path(spec[key]).exists():
            raise ValueError(f'{name}: missing {key}: {spec[key]}')
    actual = model_tree(spec['model_dir'])
    if actual != spec['model_tree_sha256']:
        raise ValueError(f'{name}: model content changed; redeploy and verify weights')
    result = subprocess.run([spec['python'], '-c',
        'import json,platform,importlib.metadata as m; '
        'print(json.dumps({"python":platform.python_version(),"packages":'
        '{p:m.version(p) for p in '+repr(list(spec['packages']))+'}}))'],
        capture_output=True, text=True, timeout=30, check=True)
    runtime = json.loads(result.stdout)
    if runtime['packages'] != spec['packages']:
        raise ValueError(f'{name}: dependency versions differ from deployment lock')
    if runtime['python'] != spec['python_version']:
        raise ValueError(f'{name}: Python version differs from deployment lock')
    spec['runtime_python'] = runtime['python']
    spec['worker_sha256'] = sha(spec['worker'])
    spec['engine_name'] = name
    return spec


def invoke(spec, image, *, task='document', max_tokens=4096, timeout=900, pages=None):
    """One subprocess at a time. Never fall back to another model on failure."""
    image = Path(image).resolve()
    key = {'schema_version': VERSION, 'input_sha256': sha(image),
           'engine': spec, 'task': task, 'max_tokens': max_tokens, 'pages': pages}
    digest = hashlib.sha256(analyze_pdf.canonical(key).encode()).hexdigest()
    cache = WORK / 'cache' / (digest+'.json')
    if cache.exists():
        try:
            record = load(cache)
            body = record['body']
            if body['key'] == key and record['sha256'] == hashlib.sha256(analyze_pdf.canonical(body).encode()).hexdigest():
                return dict(body['result'], cache_hit=True)
        except (ValueError, KeyError, TypeError):
            pass
    with tempfile.TemporaryDirectory(prefix='ocr-worker-') as directory:
        output = Path(directory)/'output.json'
        command = [spec['python'], spec['worker'], str(image), '--output', str(output)]
        if spec['engine_name'] == 'mineru':
            if pages is not None:
                command += ['--pages', ','.join(map(str, pages))]
        else:
            command += ['--model-dir', spec['model_dir'], '--task', task,
                        '--max-tokens', str(max_tokens)]
        started = time.monotonic()
        env = dict(os.environ, HF_HUB_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
        WORK.mkdir(parents=True, exist_ok=True)
        with (WORK/'inference.lock').open('a') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise RuntimeError('Another local OCR process is running; retry after it finishes') from error
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, env=env, start_new_session=True)
            try:
                stdout, stderr = proc.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                stdout, stderr = proc.communicate()
                save(WORK/'logs'/(digest+'.json'), {'command': command, 'stdout': stdout,
                                                  'stderr': stderr, 'status': 'timeout'})
                raise RuntimeError(f'{spec["engine_name"]} exceeded timeout; process group terminated')
            except BaseException:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                stdout, stderr = proc.communicate()
                save(WORK/'logs'/(digest+'.json'), {'command': command, 'stdout': stdout,
                                                  'stderr': stderr, 'status': 'interrupted'})
                raise
        save(WORK/'logs'/(digest+'.json'), {'command': command, 'stdout': stdout,
                                          'stderr': stderr, 'returncode': proc.returncode})
        if proc.returncode:
            raise RuntimeError(f'{spec["engine_name"]} exited {proc.returncode}: {stderr[-3000:]}')
        result = load(output)
        if spec['engine_name'] == 'mineru':
            rows = result.get('pages', [])
            returned = [p['page'] for p in rows]
            if not rows or len(returned) != len(set(returned)) or (pages is not None and sorted(returned) != sorted(pages)):
                raise ValueError('MinerU returned missing/duplicate/unexpected source page numbers')
            if any(not isinstance(p.get('output'), str) or not p['output'].strip() for p in rows):
                raise ValueError('MinerU returned an empty page; inspect original instead of accepting it')
        elif not isinstance(result.get('output'), str) or not result['output'].strip() or result.get('truncated'):
            raise ValueError('Empty or truncated model result')
        if sha(image) != key['input_sha256']:
            raise ValueError('Input changed during recognition')
        if (sha(spec['worker']) != spec['worker_sha256']
                or model_tree(spec['model_dir']) != spec['model_tree_sha256']):
            raise ValueError('Model or worker changed during recognition; result not cached')
        result['elapsed_seconds'] = round(time.monotonic()-started, 6)
        body = {'key': key, 'result': result}
        save(cache, {'body': body, 'sha256': hashlib.sha256(analyze_pdf.canonical(body).encode()).hexdigest()})
        return dict(result, cache_hit=False)


def make_run(spec, result, metadata):
    evidence = {k: spec.get(k) for k in ('repo_id', 'revision', 'model_tree_sha256', 'packages',
                                        'worker_sha256', 'runtime_python')}
    output = result['output']
    return {'engine': spec['engine_name'],
            'engine_version': spec['revision'] + '/' + spec['model_tree_sha256'],
            'output': output, 'extraction_status': 'recognized_unverified',
            'review_status': 'needs-review', 'mathematical_verification_status': 'not_verified',
            'metadata': {**metadata, 'model_evidence': evidence,
                         'output_sha256': hashlib.sha256(output.encode()).hexdigest(),
                         'elapsed_seconds': result.get('elapsed_seconds'),
                         'cache_hit': result.get('cache_hit'), 'device': result.get('device'),
                         'completion': {k: result.get(k) for k in
                                        ('truncated', 'completion_status', 'truncation_status', 'generated_tokens')}}}


def process_pdf(pdf, source_id, *, engine='xiaomi', cross_check=False, pages=None,
                dpi=180, max_tokens=4096, timeout=900, manifest=ROOT/'source-manifest.json', config=CONFIG):
    pdf = Path(pdf).resolve()
    manifest_data = load(manifest)
    source = next((s for s in manifest_data['sources'] if s['source_id'] == source_id), None)
    if source is None or source.get('source_state') != 'ready':
        raise ValueError('Source must be registered and ready')
    expected = ocr_pdf.manifest_source_sha256(manifest, source_id)
    if sha(pdf) != expected:
        raise ValueError('PDF SHA-256 does not match registered source')
    if not 72 <= dpi <= 600 or max_tokens < 1 or timeout <= 0:
        raise ValueError('Invalid DPI, token budget or timeout')
    analysis = analyze_pdf.analyze(pdf, pages=pages)
    if analysis['page_count'] != source['artifact']['page_count']:
        raise ValueError('Page count does not match registered source')
    selected = [p['page'] for p in analysis['pages'] if pages is not None or p['content_evidence'] == 'raster_only']
    review = [p['page'] for p in analysis['pages'] if p['classification'] == 'review' and p['page'] not in selected]
    native = [p for p in analysis['pages'] if p['page'] not in selected]
    names = [engine] + (['paddle' if engine != 'paddle' else 'xiaomi'] if cross_check else [])
    specs = {n: engine_config(n, config) for n in names} if selected else {}
    renderer = None
    if selected:
        renderer, _ = ocr_pdf._executable('pdftoppm', ['-v'], r'pdftoppm version (\S+)', 30)
    runs, candidates, comparisons = [], [], []
    rendered = {}
    for page in selected:
        image, dims, hit, temp = ocr_pdf.render_page(pdf, page, dpi, renderer, WORK/'pages', 120)
        if temp:
            temp.cleanup()
        rendered[page] = (image, dims)
    mineru = {}
    if engine == 'mineru' and selected:
        batch = invoke(specs['mineru'], pdf, pages=selected, timeout=timeout)
        mineru = {p['page']: {**batch, 'output': p['output']} for p in batch['pages']}
    for page in selected:
        image, dims = rendered[page]
        outputs = {}
        for name in names:
            spec = specs[name]
            result = mineru[page] if name == 'mineru' else invoke(spec, image, max_tokens=max_tokens, timeout=timeout)
            metadata = {'source_id': source_id, 'source_sha256': expected,
                        'source_page': page, 'task': 'page_text', 'render_dpi': dpi,
                        'render_sha256': sha(image), 'bbox_px': [0,0,*dims],
                        'bbox_coordinate_space': 'rendered_page_px_top_left'}
            run = make_run(spec, result, metadata)
            runs.append(run)
            candidates.append(convert_run(run, manifest_data))
            outputs[name] = run['metadata']['output_sha256']
        if len(outputs) > 1:
            comparisons.append({'source_page': page, 'engine_output_sha256': outputs,
                                'exact_match': len(set(outputs.values())) == 1,
                                'review_status': 'needs-review'})
    if sha(pdf) != expected:
        raise ValueError('Source changed during OCR')
    return {'schema_version': VERSION, 'source_id': source_id, 'pdf_sha256': expected,
            'primary_engine': engine, 'selected_pages': selected,
            'native_text_candidates': native, 'pages_requiring_manual_routing': review,
            'runs': runs, 'candidates': candidates, 'comparisons': comparisons,
            'review_status': 'needs-review', 'canonical_question_source_ready': False}


def main(argv=None):
    def terminate(signum, frame):
        raise KeyboardInterrupt('Termination requested')
    signal.signal(signal.SIGTERM, terminate)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=CONFIG)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    image = sub.add_parser('image')
    image.add_argument('input', type=Path)
    image.add_argument('--engine', choices=['xiaomi', 'paddle'], default='xiaomi')
    image.add_argument('--task', choices=['document', 'text', 'formula'], default='document')
    pdf = sub.add_parser('pdf')
    pdf.add_argument('input', type=Path)
    pdf.add_argument('--source-id', required=True)
    pdf.add_argument('--page', type=int, action='append')
    pdf.add_argument('--dpi', type=int, default=180)
    pdf.add_argument('--manifest', type=Path, default=ROOT/'source-manifest.json')
    pdf.add_argument('--engine', choices=['xiaomi', 'paddle', 'mineru'], default='xiaomi')
    pdf.add_argument('--cross-check', action='store_true')
    batch = sub.add_parser('batch')
    batch.add_argument('jobs', type=Path, help='JSON array of {pdf, source_id, pages?}; paths relative to jobs file')
    batch.add_argument('--manifest', type=Path, default=ROOT/'source-manifest.json')
    batch.add_argument('--engine', choices=['xiaomi', 'paddle', 'mineru'], default='mineru')
    batch.add_argument('--cross-check', action='store_true')
    for p in (image, pdf, batch):
        p.add_argument('--output', required=True, type=Path)
        p.add_argument('--max-tokens', type=int, default=4096)
        p.add_argument('--timeout', type=int, default=900)
    args = parser.parse_args(argv)
    try:
        if args.command != 'doctor':
            destination = args.output.resolve()
            if destination.is_relative_to(ROOT) and not destination.is_relative_to(ROOT/'.work'):
                raise ValueError('Runtime output inside the project must stay under .work/')
            inputs = [getattr(args, n, None) for n in ('input', 'manifest', 'jobs')]
            if any(p is not None and Path(p).resolve() == destination for p in inputs):
                raise ValueError('Output must not overwrite an input, jobs file or manifest')
        if args.command == 'doctor':
            results = {}
            for name in load(args.config)['engines']:
                try:
                    spec = engine_config(name, args.config)
                    results[name] = {'status': 'ready', 'revision': spec['revision']}
                except Exception as error:
                    results[name] = {'status': 'failed', 'error': str(error)}
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return int(any(r['status'] != 'ready' for r in results.values()))
        if args.command == 'image':
            if args.max_tokens < 1 or args.timeout <= 0:
                raise ValueError('Positive token budget and timeout required')
            spec = engine_config(args.engine, args.config)
            result = invoke(spec, args.input, task=args.task, max_tokens=args.max_tokens, timeout=args.timeout)
            data = make_run(spec, result, {'task': args.task, 'image_sha256': sha(args.input)})
        elif args.command == 'pdf':
            data = process_pdf(args.input, args.source_id, engine=args.engine, cross_check=args.cross_check,
                               pages=args.page, dpi=args.dpi, max_tokens=args.max_tokens,
                               timeout=args.timeout, manifest=args.manifest, config=args.config)
        else:
            jobs = load(args.jobs)
            if not isinstance(jobs, list) or not jobs:
                raise ValueError('Batch jobs must be a nonempty JSON array')
            results = []
            for job in jobs:
                try:
                    data = process_pdf(args.jobs.parent / job['pdf'], job['source_id'], engine=args.engine,
                                       cross_check=args.cross_check, max_tokens=args.max_tokens,
                                       pages=job.get('pages'), timeout=args.timeout,
                                       manifest=args.manifest, config=args.config)
                    results.append({'status': 'succeeded', 'result': data})
                except Exception as error:
                    results.append({'status': 'failed', 'job': job, 'error': str(error)})
                save(args.output, {'jobs': results})
            return int(any(r['status'] != 'succeeded' for r in results))
        save(args.output, data)
        print(json.dumps({'status': 'succeeded', 'output': str(args.output)}, ensure_ascii=False))
        return 0
    except Exception as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

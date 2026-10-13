#!/usr/bin/env python3
"""Score OCR outputs against source-bound, explicitly reviewed gold snippets."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import unicodedata

VERSION = 1
TASKS = {'text', 'formula', 'structure'}
REVIEW_STATES = {'human_verified', 'pending_human_review'}


def _normalized(value, *, ignore_whitespace):
    value = unicodedata.normalize('NFC', value)
    return ''.join(character for character in value
                   if not (ignore_whitespace and character.isspace()))


def edit_distance(left, right):
    """Return Levenshtein distance using O(min(len(left), len(right))) space."""
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for row, left_char in enumerate(left, 1):
        current = [row]
        for column, right_char in enumerate(right, 1):
            current.append(min(
                current[-1] + 1,
                previous[column] + 1,
                previous[column - 1] + (left_char != right_char),
            ))
        previous = current
    return previous[-1]


def _validated_cases(gold, manifest):
    if not isinstance(gold, dict) or gold.get('schema_version') != VERSION:
        raise ValueError(f'gold schema_version must be {VERSION}')
    cases = gold.get('cases')
    if not isinstance(cases, list):
        raise ValueError('gold cases must be a list')
    source_records = manifest.get('sources') if isinstance(manifest, dict) else None
    if not isinstance(source_records, list):
        raise ValueError('manifest sources must be a list')
    sources = {}
    for record in source_records:
        if not isinstance(record, dict) or not isinstance(record.get('source_id'), str):
            raise ValueError('manifest contains an invalid source record')
        if record['source_id'] in sources:
            raise ValueError(f'duplicate source_id in manifest: {record["source_id"]}')
        sources[record['source_id']] = record

    validated = {}
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError('gold case must be an object')
        case_id = case.get('case_id')
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError('gold case requires a non-empty case_id')
        if case_id in validated:
            raise ValueError(f'duplicate case_id: {case_id}')
        source_id = case.get('source_id')
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f'gold case requires a non-empty source_id: {case_id}')
        source = sources.get(source_id)
        if source is None:
            raise ValueError(f'unknown source_id for {case_id}: {source_id}')
        artifact = source.get('artifact')
        if not isinstance(artifact, dict):
            raise ValueError(f'manifest source has no artifact metadata: {case_id}')
        source_sha = case.get('source_sha256')
        if source_sha != artifact.get('sha256'):
            raise ValueError(f'source SHA-256 mismatch for {case_id}')
        page = case.get('source_page')
        page_count = artifact.get('page_count')
        if (type(page) is not int or type(page_count) is not int
                or page < 1 or page > page_count):
            raise ValueError(f'source page out of range for {case_id}')
        bbox = case.get('bbox_pixels_top_left_xywh')
        if bbox is not None and (
                not isinstance(bbox, list) or len(bbox) != 4
                or any(type(value) is not int for value in bbox)
                or bbox[0] < 0 or bbox[1] < 0 or bbox[2] <= 0 or bbox[3] <= 0):
            raise ValueError(f'bbox must contain x,y >= 0 and positive width and height for {case_id}')
        task = case.get('task')
        if not isinstance(task, str) or task not in TASKS:
            raise ValueError(f'unsupported OCR task for {case_id}: {task}')
        review_status = case.get('review_status')
        if not isinstance(review_status, str) or review_status not in REVIEW_STATES:
            raise ValueError(f'unsupported review_status for {case_id}')
        reference = case.get('reference_text')
        if reference is not None and not isinstance(reference, str):
            raise ValueError(f'reference_text must be text or null for {case_id}')
        if case['review_status'] == 'human_verified':
            reviewer = case.get('reviewed_by')
            if not isinstance(reviewer, str) or not reviewer.strip():
                raise ValueError(f'human_verified gold requires reviewed_by for {case_id}')
            try:
                date.fromisoformat(case.get('reviewed_at', ''))
            except (TypeError, ValueError) as error:
                raise ValueError(f'human_verified gold requires ISO reviewed_at for {case_id}') from error
        if case['review_status'] == 'human_verified' and (
                not isinstance(reference, str) or not reference.strip()):
            raise ValueError(f'human_verified gold requires non-empty reference_text for {case_id}')
        validated[case_id] = case
    return validated


def score_benchmark(gold, runs, manifest):
    """Validate source identity and score only human-verified reference cases."""
    cases = _validated_cases(gold, manifest)
    if not isinstance(runs, list):
        raise ValueError('OCR runs must be a list')
    results = []
    aggregates = {}
    for run in runs:
        if not isinstance(run, dict):
            raise ValueError('OCR run must be an object')
        case_id = run.get('case_id')
        if not isinstance(case_id, str) or case_id not in cases:
            raise ValueError(f'OCR run references unknown case_id: {case_id}')
        for field in ('engine', 'engine_version'):
            if not isinstance(run.get(field), str) or not run[field].strip():
                raise ValueError(f'OCR run requires non-empty {field}: {case_id}')
        if not isinstance(run.get('output'), str):
            raise ValueError(f'OCR run requires string output: {case_id}')
        case = cases[case_id]
        metadata = run.get('metadata')
        if not isinstance(metadata, dict):
            raise ValueError(f'OCR run requires source metadata: {case_id}')
        for field in ('source_sha256', 'source_page', 'task'):
            if field not in metadata:
                raise ValueError(f'OCR run metadata requires {field}: {case_id}')
        if case['bbox_pixels_top_left_xywh'] is not None and 'bbox_pixels_top_left_xywh' not in metadata:
            raise ValueError(f'OCR run metadata requires bbox_pixels_top_left_xywh: {case_id}')
        for field in ('source_id', 'source_sha256', 'source_page',
                      'bbox_pixels_top_left_xywh', 'task'):
            if field in metadata and metadata[field] != case[field]:
                raise ValueError(f'OCR run metadata {field} mismatch for {case_id}')
        result = {
            'case_id': case_id,
            'engine': run['engine'],
            'engine_version': run['engine_version'],
            'task': case['task'],
        }
        if case['review_status'] != 'human_verified':
            result['status'] = 'pending_gold'
        elif case['task'] == 'text':
            reference = _normalized(case['reference_text'], ignore_whitespace=True)
            hypothesis = _normalized(run['output'], ignore_whitespace=True)
            distance = edit_distance(reference, hypothesis)
            result.update(status='scored', score={
                'metric': 'cer',
                'edit_distance': distance,
                'reference_length': len(reference),
                'value': distance / len(reference),
            })
        else:
            reference = _normalized(case['reference_text'], ignore_whitespace=True)
            hypothesis = _normalized(run['output'], ignore_whitespace=True)
            result.update(status='scored', score={
                'metric': 'exact_match',
                'matched': reference == hypothesis,
            })
        if result['status'] == 'scored':
            key = (run['engine'], run['engine_version'], case['task'])
            aggregate = aggregates.setdefault(key, {
                'engine': run['engine'], 'engine_version': run['engine_version'],
                'task': case['task'], 'metric': result['score']['metric'],
                'count': 0, 'edit_distance': 0, 'reference_length': 0, 'matched': 0,
            })
            aggregate['count'] += 1
            if case['task'] == 'text':
                aggregate['edit_distance'] += result['score']['edit_distance']
                aggregate['reference_length'] += result['score']['reference_length']
            elif result['score']['matched']:
                aggregate['matched'] += 1
        results.append(result)
    summary = []
    for key in sorted(aggregates):
        aggregate = aggregates[key]
        if aggregate['metric'] == 'cer':
            summary.append({
                'engine': aggregate['engine'], 'engine_version': aggregate['engine_version'],
                'task': aggregate['task'], 'metric': 'cer',
                'edit_distance': aggregate['edit_distance'],
                'reference_length': aggregate['reference_length'],
                'value': aggregate['edit_distance'] / aggregate['reference_length'],
            })
        else:
            summary.append({
                'engine': aggregate['engine'], 'engine_version': aggregate['engine_version'],
                'task': aggregate['task'], 'metric': 'exact_match',
                'matched': aggregate['matched'], 'total': aggregate['count'],
                'value': aggregate['matched'] / aggregate['count'],
            })
    return {
        'schema_version': VERSION,
        'gold_case_count': len(cases),
        'scored_runs': sum(result['status'] == 'scored' for result in results),
        'pending_cases': sum(case['review_status'] != 'human_verified' for case in cases.values()),
        'summary': summary,
        'results': results,
        'limitations': [
            'Text CER removes whitespace and NFC-normalizes Unicode; punctuation and math symbols are retained.',
            'Formula/structure scores remove whitespace only; symbols are compared exactly after NFC normalization.',
            'A score is not an acceptance gate for source fidelity or mathematical correctness.',
        ],
    }


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f'cannot read JSON {path}: {error}') from error


def _read_jsonl(path):
    try:
        lines = Path(path).read_text(encoding='utf-8').splitlines()
        return [json.loads(line) for line_number, line in enumerate(lines, 1)
                if line.strip()]
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f'cannot read JSONL {path}: {error}') from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('gold', type=Path, help='Versioned gold JSON document')
    parser.add_argument('runs', type=Path, help='OCR run records, one JSON object per line')
    parser.add_argument('--manifest', type=Path, required=True,
                        help='source-manifest.json used to verify source IDs and hashes')
    args = parser.parse_args(argv)
    try:
        report = score_benchmark(_read_json(args.gold), _read_jsonl(args.runs),
                                _read_json(args.manifest))
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

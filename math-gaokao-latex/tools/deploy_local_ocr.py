#!/usr/bin/env python3
"""Rebuild the pinned macOS arm64 OCR environments and model assets."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from local_ocr import CONFIG, ROOT, engine_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', choices=['all', 'xiaomi', 'paddle', 'mineru'], default='all')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    config = json.loads(CONFIG.read_text())['engines']
    names = list(config) if args.engine == 'all' else [args.engine]
    for name in names:
        spec = config[name]
        python = ROOT/spec['python']
        envdir = python.parents[1]
        if not args.verify_only:
            if not python.exists():
                subprocess.run(['uv', 'venv', '--python', spec['python_version'], str(envdir)], check=True)
            install = ['uv', 'pip', 'sync', '--python', str(python), str(ROOT/spec['requirements_lock'])]
            if spec.get('extra_index_url'):
                install += ['--extra-index-url', spec['extra_index_url']]
            subprocess.run(install, check=True)
            env = dict(os.environ, HF_HOME=str(ROOT/'.work/ocr-local'/name/'hf-cache'))
            env.pop('HF_HUB_OFFLINE', None)
            code = ('import json,sys; from huggingface_hub import snapshot_download; '
                    'd=json.loads(sys.argv[1]); '
                    'snapshot_download(d["repo_id"], revision=d["revision"], '
                    'local_dir=d["local_dir"], allow_patterns=d["allow_patterns"],max_workers=2)')
            for source in spec['downloads']:
                source = dict(source, local_dir=str(ROOT/source['local_dir']))
                subprocess.run([str(python), '-c', code, json.dumps(source)], check=True, env=env)
        verified = engine_config(name)
        print(json.dumps({'engine': name, 'installation': 'verified',
                          'model_tree_sha256': verified['model_tree_sha256'],
                          'note': 'Run the documented real-source acceptance checks before transcription.'}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}), file=sys.stderr)
        raise SystemExit(1)

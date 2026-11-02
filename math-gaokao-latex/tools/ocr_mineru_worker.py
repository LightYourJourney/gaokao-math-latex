#!/usr/bin/env python3
"""Single-process MinerU 4 worker with page-numbered JSON output."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / '.work/ocr-local/mineru'
VENV_BIN = HERE / ".venv" / "bin"
MINERU = VENV_BIN / "mineru-kit"


def parse_pages(spec: str | None, total: int) -> list[int] | None:
    if spec is None or spec.strip().lower() == "all":
        return None
    values: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        match = re.fullmatch(r"(\d+)(?:-(\d+))?", part)
        if not match:
            raise ValueError(f"Invalid --pages item: {part!r}; use e.g. 1,3-5")
        first = int(match.group(1))
        last = int(match.group(2) or first)
        if first < 1 or last < first or last > total:
            raise ValueError(f"Page range {part!r} is outside 1-{total}")
        values.extend(range(first, last + 1))
    if len(values) != len(set(values)):
        raise ValueError("--pages must not contain duplicate pages")
    return values


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input_pdf", type=Path)
    ap.add_argument("--output", required=True, type=Path, help="Destination JSON path")
    ap.add_argument("--pages", help="1-based page selector, e.g. 1,3-5; default: all")
    ap.add_argument("--ocr-mode", choices=("auto", "txt", "ocr"), default="auto")
    args = ap.parse_args()

    source = args.input_pdf.expanduser().resolve()
    dest = args.output.expanduser().resolve()
    if not source.is_file():
        ap.error(f"input PDF does not exist: {source}")
    if source.suffix.lower() != ".pdf":
        ap.error("input must be a PDF")
    if not MINERU.is_file():
        ap.error(f"MinerU is not installed in {HERE / '.venv'}")

    from pypdf import PdfReader
    from mineru.types import MiddleJson
    from mineru.render import render_markdown

    pdf_reader = PdfReader(str(source), strict=False)
    page_count = len(pdf_reader.pages)
    selected = parse_pages(args.pages, page_count)

    env = os.environ.copy()
    env.update(
        {
            "MINERU_HOME": str(HERE / "mineru-home"),
            "MINERU_MODEL_SOURCE": "local",
            "MINERU_MODEL_SMALL_BACKEND": "onnx",
            "MINERU_MODEL_ONNX_DEVICE": "cpu",
        }
    )

    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mineru-worker-", dir=dest.parent) as td:
        raw_json = Path(td) / "middle.json"
        command = [
            str(MINERU), "parse", str(source), "--output", str(raw_json),
            "--format", "middle_json", "--tier", "basic", "--ocr-mode", args.ocr_mode,
        ]
        if args.pages:
            command.extend(["--pages", args.pages])
        proc = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log_path = dest.with_suffix(dest.suffix + ".log")
        log_path.write_text(proc.stdout, encoding="utf-8")
        if proc.returncode:
            print(proc.stdout, file=sys.stderr, end="")
            return proc.returncode
        parsed = json.loads(raw_json.read_text(encoding="utf-8"))
        middle = MiddleJson.from_dict(parsed)
        pages = []
        for page in middle.pages:
            single = middle.model_copy(update={"pages": [page]})
            pages.append({"page": page.page_idx + 1, "output": render_markdown(single)})

    result = {
        "schema": "mineru.local-pages.v1",
        "engine": "MinerU",
        "mineru_version": "4.1.4",
        "tier": "basic",
        "small_backend": "onnx",
        "device": "cpu",
        "ocr_mode": args.ocr_mode,
        "source_pdf": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "source_page_count": page_count,
        "selected_pages": [p["page"] for p in pages],
        "pages": pages,
    }
    dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(dest), "pages": len(pages), "log": str(dest.with_suffix(dest.suffix + '.log'))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

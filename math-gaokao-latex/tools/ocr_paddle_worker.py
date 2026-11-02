#!/usr/bin/env python3
"""Run one local image through PaddleOCR-VL 1.6 and emit a JSON envelope."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parents[1] / '.work/ocr-local/paddle'


def configure_local_caches() -> None:
    """Keep model and library caches inside the authorized deployment folder."""
    cache_map = {
        "TMPDIR": HERE / "temp",
        "HF_HOME": HERE / "hf_cache",
        "HUGGINGFACE_HUB_CACHE": HERE / "hf_cache" / "hub",
        "MODELSCOPE_CACHE": HERE / "modelscope_cache",
        "XDG_CACHE_HOME": HERE / "xdg_cache",
        "PADDLE_HOME": HERE / "paddle_cache",
        "PADDLE_PDX_HOME": HERE / "paddlex_cache",
        "PADDLE_PDX_CACHE_HOME": HERE / "paddlex_cache",
    }
    for name, value in cache_map.items():
        path = Path(value)
        path.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(path)
        if name == "TMPDIR":
            tempfile.tempdir = str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path, help="one local image file")
    parser.add_argument("--output", required=True, help="JSON output path, including caller temp paths, or '-' for stdout")
    parser.add_argument("--task", choices=("document", "text", "formula"), default="document")
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--model-dir", type=Path, default=None,
                        help="directory containing PaddleOCR-VL-1.6 and optional PP-DocLayoutV3 subdirectories")
    parser.add_argument(
        "--markdown-dir",
        type=Path,
        default=None,
        help="directory where PaddleOCR stores its Markdown result",
    )
    args = parser.parse_args()

    image_path = args.image.expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve() if args.output != "-" else None
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_dir = (args.markdown_dir.expanduser().resolve() if args.markdown_dir else
                    Path(tempfile.mkdtemp(prefix="paddle-md-", dir=output_path.parent if output_path else HERE)))
    if not image_path.is_file():
        parser.error(f"image file does not exist: {image_path}")
    model_dir = args.model_dir.expanduser().resolve() if args.model_dir else None
    if model_dir is not None and not model_dir.is_dir():
        parser.error(f"model directory does not exist: {model_dir}")
    if args.max_tokens < 1:
        parser.error("--max-tokens must be a positive integer")
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_dir.mkdir(parents=True, exist_ok=True)
    configure_local_caches()

    try:
        import paddle
        from paddleocr import PaddleOCRVL

        load_started = time.perf_counter()
        init_options = {"pipeline_version": "v1.6", "device": "cpu"}
        if model_dir is not None:
            vl_model_dir = model_dir / "PaddleOCR-VL-1.6"
            if not vl_model_dir.is_dir():
                vl_model_dir = model_dir
            init_options["vl_rec_model_dir"] = str(vl_model_dir)
            layout_model_dir = model_dir / "PP-DocLayoutV3"
            if layout_model_dir.is_dir():
                init_options["layout_detection_model_dir"] = str(layout_model_dir)
        pipeline = PaddleOCRVL(**init_options)
        model_load_seconds = time.perf_counter() - load_started
        predict_options = {"max_new_tokens": args.max_tokens}
        if args.task in ("text", "formula"):
            predict_options["use_layout_detection"] = False
            predict_options["prompt_label"] = "ocr" if args.task == "text" else "formula"
        inference_started = time.perf_counter()
        results = list(pipeline.predict(str(image_path), **predict_options))
        inference_seconds = time.perf_counter() - inference_started

        for result in results:
            result.save_to_markdown(save_path=str(markdown_dir))

        markdown_path = markdown_dir / f"{image_path.stem}.md"
        if not markdown_path.is_file():
            raise RuntimeError(f"PaddleOCR did not create the expected Markdown output: {markdown_path}")
        output_text = markdown_path.read_text(encoding="utf-8")

        payload = {
            "ok": True,
            "model": "PaddlePaddle/PaddleOCR-VL-1.6",
            "pipeline_version": "v1.6",
            "task": args.task,
            "max_tokens": args.max_tokens,
            "device": "cpu",
            "paddle_version": paddle.__version__,
            "paddleocr_version": __import__("importlib.metadata", fromlist=["version"]).version("paddleocr"),
            "input_image": str(image_path),
            "model_load_seconds": round(model_load_seconds, 3),
            "inference_seconds": round(inference_seconds, 3),
            "total_seconds": round(model_load_seconds + inference_seconds, 3),
            "output": output_text,
            "completion_status": "unknown",
            "truncation_status": "not_exposed_by_official_pipeline_api",
            "model_dir": str(model_dir) if model_dir else None,
            "markdown_path": str(markdown_path) if markdown_path.is_file() else None,
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if output_path is None:
            print(encoded, end="")
        else:
            output_path.write_text(encoded, encoding="utf-8")
            print(json.dumps(payload, ensure_ascii=False))
        return 0
    except Exception as exc:
        payload = {
            "ok": False,
            "model": "PaddlePaddle/PaddleOCR-VL-1.6",
            "pipeline_version": "v1.6",
            "task": args.task,
            "max_tokens": args.max_tokens,
            "input_image": str(image_path),
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if output_path is not None:
            output_path.write_text(encoded, encoding="utf-8")
        print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

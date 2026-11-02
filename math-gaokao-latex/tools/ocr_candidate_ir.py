#!/usr/bin/env python3
"""Bind an OCR run to a verified source page without assigning it to a question."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class OcrCandidateError(ValueError):
    """An OCR run cannot be safely bound to a manifest source page."""


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _single_source(manifest: Dict[str, Any], source_id: str) -> Dict[str, Any]:
    matches = [
        row for row in manifest.get("sources", [])
        if isinstance(row, dict) and row.get("source_id") == source_id
    ]
    if len(matches) != 1:
        raise OcrCandidateError(f"source_id 必须在 manifest 中唯一：{source_id}（匹配数 {len(matches)}）")
    return matches[0]


def _bbox(metadata: Dict[str, Any]) -> tuple[Optional[List[int]], Optional[str]]:
    value = metadata.get("bbox_px")
    space = metadata.get("bbox_coordinate_space")
    if value is None:
        value = metadata.get("bbox_pixels_top_left_xywh")
        space = metadata.get("bbox_coordinate_space") or "rendered_page_px_top_left_xywh"
    if value is None:
        return None, None
    if (not isinstance(value, list) or len(value) != 4
            or any(type(part) is not int or part < 0 for part in value)
            or value[2] == 0 or value[3] == 0):
        raise OcrCandidateError("OCR bbox 必须是正尺寸的非负整数 [x,y,width,height]")
    if not isinstance(space, str) or not space:
        raise OcrCandidateError("OCR bbox 缺少坐标系")
    return value, space


def convert_run(run: Dict[str, Any], manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Convert one stored OCR run into an unverified, page-level candidate IR.

    This function deliberately never guesses question boundaries or creates a
    question_id. OCR output remains a candidate until a reviewer segments and
    confirms it against the source image.
    """
    if not isinstance(run, dict):
        raise OcrCandidateError("OCR run 必须是 JSON 对象")
    metadata = run.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise OcrCandidateError("OCR metadata 必须是 JSON 对象")
    root_source_id = run.get("source_id")
    metadata_source_id = metadata.get("source_id")
    if root_source_id is not None and metadata_source_id is not None and root_source_id != metadata_source_id:
        raise OcrCandidateError("source_id 字段冲突：OCR run 与 metadata 不一致")
    source_id = root_source_id or metadata_source_id
    if not isinstance(source_id, str) or not source_id:
        raise OcrCandidateError("source_id 缺失；不能安全绑定 OCR 候选")
    source = _single_source(manifest, source_id)
    artifact = source.get("artifact") or {}
    expected_sha = artifact.get("sha256")
    metadata_sha = metadata.get("source_sha256")
    root_sha = run.get("pdf_sha256")
    if metadata_sha is not None and root_sha is not None and metadata_sha != root_sha:
        raise OcrCandidateError("PDF SHA-256 字段冲突：OCR run 与 metadata 不一致")
    source_sha = metadata_sha or root_sha
    if not isinstance(expected_sha, str) or re.fullmatch(r"[0-9a-f]{64}", expected_sha) is None:
        raise OcrCandidateError(f"manifest 来源缺少有效 PDF SHA-256：{source_id}")
    if source.get("source_state") != "ready":
        raise OcrCandidateError(f"来源状态不是 ready：{source_id}")
    if source_sha != expected_sha:
        raise OcrCandidateError(f"OCR 来源 SHA-256 与 manifest 不一致：{source_id}")

    metadata_page = metadata.get("source_page")
    root_page = run.get("source_page")
    if metadata_page is not None and root_page is not None and metadata_page != root_page:
        raise OcrCandidateError("页码字段冲突：OCR run 与 metadata 不一致")
    page = metadata_page if metadata_page is not None else root_page
    page_count = artifact.get("page_count")
    if (type(page) is not int or type(page_count) is not int
            or page < 1 or page > page_count):
        raise OcrCandidateError(f"OCR 页码超出来源页数或无效：page={page!r}, pages={page_count!r}")
    output = run.get("output")
    if not isinstance(output, str) or not output.strip():
        raise OcrCandidateError("OCR run 缺少非空 output 文本")
    engine = run.get("engine")
    engine_version = run.get("engine_version")
    if not isinstance(engine, str) or not engine or not isinstance(engine_version, str) or not engine_version:
        raise OcrCandidateError("OCR run 缺少引擎名称或版本")
    task = metadata.get("task")
    if not isinstance(task, str) or not task:
        raise OcrCandidateError("OCR run 缺少任务类型")

    bbox, coordinate_space = _bbox(metadata)
    text_sha = hashlib.sha256(output.encode("utf-8")).hexdigest()
    recorded_output_sha = metadata.get("output_sha256") or run.get("output_sha256")
    if recorded_output_sha is not None and recorded_output_sha != text_sha:
        raise OcrCandidateError("OCR 输出 SHA-256 不匹配")
    rendered_sha = metadata.get("render_sha256") or metadata.get("image_sha256")
    if rendered_sha is not None and (
        not isinstance(rendered_sha, str) or re.fullmatch(r"[0-9a-f]{64}", rendered_sha) is None
    ):
        raise OcrCandidateError("渲染图像 SHA-256 格式错误")
    page_width, page_height = run.get("page_width_px"), run.get("page_height_px")
    if bbox is not None and type(page_width) is int and type(page_height) is int:
        if bbox[0] + bbox[2] > page_width or bbox[1] + bbox[3] > page_height:
            raise OcrCandidateError("OCR bbox 超出渲染页范围")
    candidate_identity = {
        "source_id": source_id,
        "pdf_sha256": expected_sha,
        "source_page": page,
        "task": task,
        "engine": engine,
        "engine_version": engine_version,
        "rendered_image_sha256": rendered_sha,
        "bbox": bbox,
        "candidate_text_sha256": text_sha,
    }
    candidate_id = "ocr-page-" + hashlib.sha256(_canonical(candidate_identity).encode("utf-8")).hexdigest()
    timing = metadata.get("page_inference_seconds")
    if timing is None:
        timing = metadata.get("elapsed_seconds", run.get("elapsed_seconds"))
    return {
        "schema_version": 1,
        "ir_kind": "ocr-page-candidate",
        "candidate_id": candidate_id,
        "case_id": run.get("case_id"),
        "paper_id": source.get("paper_id"),
        "source_id": source_id,
        "upstream_path": source.get("upstream_path"),
        "pdf_sha256": expected_sha,
        "source_page": page,
        "render_dpi": metadata.get("render_dpi"),
        "rendered_image_sha256": rendered_sha,
        "task": task,
        "source_bbox": bbox,
        "bbox_coordinate_space": coordinate_space,
        "engine": engine,
        "engine_version": engine_version,
        "candidate_text": output,
        "model_evidence": metadata.get("model_evidence"),
        "recognition_completion": metadata.get("completion"),
        "candidate_text_sha256": text_sha,
        "question_id": None,
        "assignment_status": "unassigned-page-level",
        "extraction_status": "recognized_unverified",
        "review_status": "needs-review",
        "prior_review_status": metadata.get("review_status") or run.get("review_status"),
        "mathematical_verification_status": "not_verified",
        "cost_evidence": {
            "cache_hit": metadata.get("cache_hit", run.get("cache_hit")),
            "render_cache_hit": run.get("render_cache_hit"),
            "elapsed_seconds": timing,
            "model_init_seconds": metadata.get("model_init_seconds"),
            "device": metadata.get("device"),
            "peak_rss_bytes": metadata.get("process_max_rss_bytes") or metadata.get("cli_max_rss_bytes"),
        },
    }


def _load_run(path: Path, line: Optional[int]) -> Dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonl":
        if line is None or line < 1:
            raise OcrCandidateError("读取 JSONL 时必须提供从 1 开始的 --line")
        rows = [row for row in content.splitlines() if row.strip()]
        if line > len(rows):
            raise OcrCandidateError(f"JSONL 行号超出范围：{line}（共 {len(rows)} 条）")
        value = json.loads(rows[line - 1])
    else:
        if line is not None:
            raise OcrCandidateError("--line 仅适用于 JSONL 输入")
        value = json.loads(content)
    if not isinstance(value, dict):
        raise OcrCandidateError("OCR 输入记录必须是 JSON 对象")
    return value


def main(argv: Optional[List[str]] = None) -> int:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_record", type=Path, help="一个 OCR JSON 对象，或 JSONL 文件")
    parser.add_argument("--line", type=int, help="从 1 开始选取 JSONL 行")
    parser.add_argument("--manifest", type=Path, default=project_root / "source-manifest.json")
    parser.add_argument("--output", type=Path, help="输出 JSON 路径；省略时写 stdout")
    args = parser.parse_args(argv)
    try:
        run = _load_run(args.run_record, args.line)
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = convert_run(run, manifest)
        rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OcrCandidateError, OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"ocr_candidate_ir: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

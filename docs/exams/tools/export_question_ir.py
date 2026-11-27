#!/usr/bin/env python3
"""Export registered Markdown questions as a deterministic, source-bound IR."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from provenance import question_text_digests
from solution_sources import SolutionSourceError, parse_question_blocks


class QuestionIRExportError(ValueError):
    """The registered paper, transcription, or provenance is inconsistent."""


_IMAGE_LINK = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def _read_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise QuestionIRExportError(f"无法读取有效 JSON：{path}: {error}") from error
    if not isinstance(value, dict):
        raise QuestionIRExportError(f"JSON 根节点必须是对象：{path}")
    return value


def _unique(items: List[Dict[str, Any]], key: str, value: str, label: str) -> Dict[str, Any]:
    matches = [item for item in items if item.get(key) == value]
    if len(matches) != 1:
        raise QuestionIRExportError(f"未找到唯一{label}：{value}（匹配数 {len(matches)}）")
    return matches[0]


def _inside(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise QuestionIRExportError(f"清单路径越出仓库根目录：{relative}") from error
    return candidate


def build_question_ir(repo_root: Path, paper_id: str) -> Dict[str, Any]:
    """Build IR from existing canonical Markdown and per-question provenance.

    The exporter intentionally does not infer stem/options/equations or official
    answers. Exact parsed Markdown and explicit review/source fields are retained.
    """
    repo_root = Path(repo_root).resolve()
    project_root = repo_root / "docs/exams"
    manifest = _read_json(project_root / "source-manifest.json")
    paper = _unique(manifest.get("papers", []), "paper_id", paper_id, "试卷记录")
    if len(paper.get("source_ids", [])) != 1:
        raise QuestionIRExportError(f"试卷必须且只能绑定一个来源：{paper_id}")
    source = _unique(manifest.get("sources", []), "source_id", paper["source_ids"][0], "来源记录")
    if (
        source.get("paper_id") != paper_id
        or source.get("source_state") != "ready"
        or source.get("paper_relation") != "canonical"
    ):
        raise QuestionIRExportError(f"来源未就绪、非 canonical 或与试卷绑定不一致：{paper_id}")
    artifact = source.get("artifact", {})
    pdf_sha256 = artifact.get("sha256")
    if not isinstance(pdf_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", pdf_sha256):
        raise QuestionIRExportError(f"来源记录缺少有效 PDF SHA-256：{paper_id}")

    source_files = paper.get("source_files", {})
    if not isinstance(source_files.get("questions"), str) or not isinstance(paper.get("project_dir"), str):
        raise QuestionIRExportError(f"试卷缺少规范题面路径或项目目录：{paper_id}")
    question_path = _inside(repo_root, source_files.get("questions", ""))
    provenance_path = _inside(project_root, f"{paper.get('project_dir', '')}/provenance.json")
    questions_text = question_path.read_text(encoding="utf-8")
    provenance = _read_json(provenance_path)
    if provenance.get("paper_id") != paper_id:
        raise QuestionIRExportError(f"provenance paper_id 与清单不一致：{paper_id}")
    if len(provenance.get("questions", [])) != paper.get("question_count"):
        raise QuestionIRExportError(f"provenance 题数与 manifest 不一致：{paper_id}")

    try:
        blocks = parse_question_blocks(questions_text)
        digests = question_text_digests(questions_text)
    except SolutionSourceError as error:
        raise QuestionIRExportError(f"规范题面无法解析：{error}") from error
    if len(blocks) != paper.get("question_count"):
        raise QuestionIRExportError(f"题面题数与 manifest 不一致：{paper_id}")

    evidence_by_number: Dict[int, Dict[str, Any]] = {}
    for row in provenance["questions"]:
        number = row.get("printed_number")
        if not isinstance(number, int) or number in evidence_by_number:
            raise QuestionIRExportError(f"provenance 题号缺失或重复：{number!r}")
        evidence_by_number[number] = row
    if set(evidence_by_number) != {block.number for block in blocks}:
        raise QuestionIRExportError(f"题面题号与 provenance 不一致：{paper_id}")

    questions = []
    question_ids = set()
    for block in blocks:
        row = evidence_by_number[block.number]
        expected_digest = row.get("question_text_sha256")
        if digests.get(block.number) != expected_digest:
            raise QuestionIRExportError(f"第 {block.number} 题题面哈希与 provenance 不一致")
        if row.get("source_sha256") != pdf_sha256:
            raise QuestionIRExportError(f"第 {block.number} 题来源 PDF 哈希与 manifest 不一致")
        if row.get("source_ref", {}).get("source_id") != source["source_id"]:
            raise QuestionIRExportError(f"第 {block.number} 题 source_id 与 manifest 不一致")
        if not row.get("question_id"):
            raise QuestionIRExportError(f"第 {block.number} 题缺少稳定 question_id")
        if row["question_id"] in question_ids:
            raise QuestionIRExportError(f"question_id 重复：{row['question_id']}")
        question_ids.add(row["question_id"])

        content_markdown = f"{block.title}\n\n{block.body}".strip()
        answer_evidence = row.get("answer_evidence")
        questions.append({
            "question_id": row["question_id"],
            "question_number": block.number,
            "printed_label": block.printed_label,
            "question_type": None,
            "body_markdown": content_markdown,
            "options": None,
            "equations": None,
            "figures": _IMAGE_LINK.findall(content_markdown),
            "tables": None,
            "official_answer": None,
            "answer_evidence": ({
                "origin": "project-answer-evidence",
                "grade": answer_evidence.get("grade"),
                "evidence": answer_evidence.get("evidence"),
                "sha256": row.get("answer_sha256"),
            } if answer_evidence else None),
            "source_pages": row.get("source_pages", []),
            "source_bbox": None,
            "source_bbox_status": "not-recorded-in-current-provenance",
            "source_pdf_sha256": row["source_sha256"],
            "question_text_sha256": expected_digest,
            "transcription_review": row.get("transcription_review"),
            "review_status": (
                row.get("transcription_review", {}).get("result", "not-reviewed")
            ),
            "extraction_status": "canonical-markdown-transcription",
            "ocr_engine": None,
            "ocr_model_version": None,
        })

    return {
        "schema_version": 1,
        "ir_kind": "gaokao-question-set",
        "paper_id": paper_id,
        "exam": {
            "title": paper.get("title"),
            "year": paper.get("year"),
            "track": paper.get("track"),
            "exam_type": source.get("exam_type"),
        },
        "source": {
            "source_id": source["source_id"],
            "upstream_path": source.get("upstream_path"),
            "sha256": pdf_sha256,
            "page_count": artifact.get("page_count"),
            "source_state": source["source_state"],
        },
        "question_source_path": source_files["questions"],
        "question_count": len(questions),
        "manifest_revision": manifest.get("revision"),
        "extraction_status": "exported-from-existing-transcription",
        "questions": questions,
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_id", help="source-manifest.json 中的稳定 paper_id")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2], help="仓库根目录")
    parser.add_argument("--output", type=Path, help="输出 JSON 路径；省略时写 stdout")
    args = parser.parse_args(argv)
    try:
        result = build_question_ir(args.root, args.paper_id)
    except (QuestionIRExportError, OSError) as error:
        print(f"export_question_ir: {error}", file=sys.stderr)
        return 2
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except OSError as error:
        print(f"export_question_ir: 无法写入输出：{error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

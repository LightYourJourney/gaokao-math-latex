#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把来源总账稳定投影为可审阅的 CSV 清单。

`source-manifest.json` 仍是唯一事实源；CSV 是来源级只读投影，每个上游 PDF 一行。
未绑定到独立题面的来源也必须出现，并以 `production_state=pending` 标出，不能因为
尚未注册 paper 就从可见清单中消失。
"""
from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

from cli_common import repository_root
from manifest import file_sha256, load_manifest
from transaction import RepoLock, Transaction


PROJECT_RELATIVE = "math-gaokao-latex"
MANIFEST_TARGET = PROJECT_RELATIVE + "/source-manifest.json"
CSV_TARGET = PROJECT_RELATIVE + "/manifest.csv"
DEFAULT_MANIFEST = Path(PROJECT_RELATIVE) / "source-manifest.json"
DEFAULT_OUTPUT = Path(PROJECT_RELATIVE) / "manifest.csv"

CSV_FIELDS = [
    "record_type",
    "source_id",
    "year",
    "upstream_path",
    "source_state",
    "paper_relation",
    "paper_id",
    "project_dir",
    "title",
    "production_state",
    "question_count",
    "source_sha256",
    "batch_ids",
    "issue_ids",
    "status_note",
]


def _batch_ids(manifest: Mapping[str, Any], paper_id: Optional[str]) -> str:
    if paper_id is None:
        return ""
    values = sorted(
        str(batch.get("batch_id"))
        for batch in manifest.get("batches", [])
        if paper_id in (batch.get("paper_ids") or [])
    )
    return ";".join(values)


def _issue_ids(source: Mapping[str, Any], paper: Optional[Mapping[str, Any]]) -> str:
    values = set(source.get("issue_ids") or [])
    if paper is not None:
        values.update(paper.get("issue_ids") or [])
    return ";".join(sorted(str(value) for value in values))


def _row(manifest: Mapping[str, Any], source: Mapping[str, Any]) -> Dict[str, str]:
    papers = {
        paper.get("paper_id"): paper
        for paper in manifest.get("papers", [])
        if isinstance(paper, Mapping)
    }
    paper_id = source.get("paper_id")
    paper = papers.get(paper_id)
    artifact = source.get("artifact")
    if not isinstance(artifact, Mapping):
        artifact = {}

    if paper is None:
        production_state = "pending" if source.get("source_state") == "ready" else "missing-source"
        status_note = "未注册独立题面"
    else:
        production_state = str(paper.get("production_state") or "pending")
        status_note = ""
        if production_state == "blocked":
            status_note = str(paper.get("resume_action") or "存在未解决阻塞项")

    values = {
        "record_type": "source",
        "source_id": str(source.get("source_id") or ""),
        "year": str(source.get("year") or ""),
        "upstream_path": str(source.get("upstream_path") or ""),
        "source_state": str(source.get("source_state") or ""),
        "paper_relation": str(source.get("paper_relation") or ""),
        "paper_id": str(paper_id or ""),
        "project_dir": str((paper or {}).get("project_dir") or ""),
        "title": str((paper or {}).get("title") or ""),
        "production_state": production_state,
        "question_count": str((paper or {}).get("question_count") or ""),
        "source_sha256": str(artifact.get("sha256") or ""),
        "batch_ids": _batch_ids(manifest, paper_id),
        "issue_ids": _issue_ids(source, paper),
        "status_note": status_note,
    }
    return values


def render_manifest_csv(manifest: Mapping[str, Any]) -> str:
    """返回稳定 UTF-8 CSV；排序键为年份、上游路径、source_id。"""
    sources = list(manifest.get("sources", []))
    sources.sort(
        key=lambda source: (
            int(source.get("year") or 0),
            str(source.get("upstream_path") or ""),
            str(source.get("source_id") or ""),
        )
    )
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=CSV_FIELDS, lineterminator="\n", extrasaction="raise"
    )
    writer.writeheader()
    for source in sources:
        writer.writerow(_row(manifest, source))
    return stream.getvalue()


def _canonical_target(root: Path, path: Path, expected: str, label: str) -> str:
    relative = path.resolve().relative_to(root.resolve()).as_posix()
    if relative != expected:
        raise ValueError(f"{label} 必须是 {expected}，实际是 {relative}")
    return relative


def write_manifest_csv(manifest_path: Path, output_path: Path) -> Dict[str, Any]:
    manifest_path = Path(manifest_path).resolve()
    output_path = Path(output_path).resolve()
    root = repository_root(manifest_path.parent)
    manifest_relative = _canonical_target(root, manifest_path, MANIFEST_TARGET, "manifest")
    output_relative = _canonical_target(root, output_path, CSV_TARGET, "output")
    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        value = render_manifest_csv(manifest).encode("utf-8")
        if output_path.is_file() and output_path.read_bytes() == value:
            return {"written": False, "rows": len(manifest.get("sources", []))}
        transaction = Transaction(root)
        transaction.prepare(
            "content",
            {output_relative: value},
            {manifest_relative: file_sha256(manifest_path)},
        )
        transaction.commit()
        return {"written": True, "rows": len(manifest.get("sources", []))}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成来源总账的 CSV 投影")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    manifest_path = Path(arguments.manifest).resolve()
    output_path = Path(arguments.output).resolve()
    root = repository_root(manifest_path.parent)
    _canonical_target(root, manifest_path, MANIFEST_TARGET, "manifest")
    _canonical_target(root, output_path, CSV_TARGET, "output")
    manifest = load_manifest(manifest_path)
    expected = render_manifest_csv(manifest).encode("utf-8")
    if arguments.check:
        if not output_path.is_file() or output_path.read_bytes() != expected:
            print("manifest.csv 与 manifest 生成结果不一致", file=sys.stderr)
            return 1
        print(f"manifest.csv 当前且 {len(manifest.get('sources', []))} 行")
        return 0
    report = write_manifest_csv(manifest_path, output_path)
    verb = "已写入" if report["written"] else "无需改动"
    print(f"manifest.csv：{verb}，{report['rows']} 行")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

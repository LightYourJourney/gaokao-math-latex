from __future__ import annotations

import fcntl
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, Mapping, Optional

from schema_validate import validate

EventHook = Optional[Callable[[str, Path], None]]


def _emit(event_hook: EventHook, event: str, path: Path) -> None:
    if event_hook is not None:
        event_hook(event, path)


def durable_fsync(fd: int) -> str:
    full = getattr(fcntl, "F_FULLFSYNC", None)
    if full is not None:
        try:
            fcntl.fcntl(fd, full)
            return "fullfsync"
        except OSError:
            pass
    os.fsync(fd)
    return "fsync"


def fsync_directory(path: Path, event_hook: EventHook = None) -> None:
    path = Path(path)
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    fd = os.open(str(path), flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    _emit(event_hook, "directory_fsynced", path)


def ensure_durable_directory(path: Path, event_hook: EventHook = None) -> None:
    path = Path(path)
    missing = []
    current = path
    while not current.exists():
        missing.append(current)
        parent = current.parent
        if parent == current:
            raise OSError(f"无法找到已存在的父目录：{path}")
        current = parent
    if not current.is_dir():
        raise NotADirectoryError(str(current))
    for directory in reversed(missing):
        directory.mkdir()
        _emit(event_hook, "directory_created", directory)
        fsync_directory(directory, event_hook)
        fsync_directory(directory.parent, event_hook)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"


def atomic_write_bytes(path: Path, value: bytes, event_hook: EventHook = None) -> str:
    path = Path(path)
    ensure_durable_directory(path.parent, event_hook)
    fd, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    temporary = Path(raw)
    capability = "fsync"
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(value)
            handle.flush()
            capability = durable_fsync(handle.fileno())
        os.replace(str(temporary), str(path))
        fsync_directory(path.parent, event_hook)
        return capability
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_json(path: Path, value: Any, event_hook: EventHook = None) -> str:
    return atomic_write_bytes(
        Path(path), canonical_json(value).encode("utf-8"), event_hook=event_hook
    )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def optional_file_sha256(path: Path) -> Optional[str]:
    path = Path(path)
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"不是普通文件：{path}")
    return file_sha256(path)


def validate_manifest_semantics(manifest: Mapping[str, Any]) -> None:
    sources = manifest.get("sources")
    papers = manifest.get("papers")
    batches = manifest.get("batches")
    if not isinstance(sources, list) or not isinstance(papers, list) or not isinstance(batches, list):
        raise ValueError("manifest 的 sources/papers/batches 必须是数组")

    source_ids = [item["source_id"] for item in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("source_id 不唯一")
    paper_ids = [item["paper_id"] for item in papers]
    if len(paper_ids) != len(set(paper_ids)):
        raise ValueError("paper_id 不唯一")
    known_papers = set(paper_ids)
    for source in sources:
        source_id = source["source_id"]
        relation = source.get("paper_relation")
        paper_id = source.get("paper_id")
        if relation is not None and paper_id is None:
            raise ValueError(f"{source_id}: paper_relation 存在但 paper_id 为空")
        if paper_id is not None and paper_id not in known_papers:
            raise ValueError(f"{source_id}: paper_id 不存在")
        if source.get("source_state") == "non_paper" and (
            relation is not None or paper_id is not None
        ):
            raise ValueError(f"{source_id}: non_paper 不得绑定试卷")

    for paper in papers:
        source_list = paper.get("source_ids", [])
        if len(source_list) != len(set(source_list)):
            raise ValueError(f"{paper['paper_id']}: source_ids 不唯一")
        reverse = sorted(
            source["source_id"]
            for source in sources
            if source.get("paper_id") == paper["paper_id"]
            and source.get("paper_relation") is not None
        )
        if sorted(source_list) != reverse:
            raise ValueError(f"{paper['paper_id']}: source_ids 双向关系不一致")


def project_index(manifest: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    result: Dict[str, Mapping[str, Any]] = {}
    for paper in manifest["papers"]:
        paper_id = paper["paper_id"]
        if paper_id in result:
            raise ValueError(f"paper_id 不唯一：{paper_id}")
        result[paper_id] = paper
    return result


def load_manifest(path: Path) -> Mapping[str, Any]:
    path = Path(path)
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"无法读取 manifest：{path}: {error}") from error
    if not isinstance(manifest, Mapping):
        raise ValueError("manifest 顶层必须是对象")

    schema_reference = manifest.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference:
        raise ValueError("manifest 缺少 $schema")
    schema_path = Path(schema_reference)
    if schema_path.is_absolute() or ".." in schema_path.parts:
        raise ValueError(f"manifest $schema 必须是安全的相对路径：{schema_reference}")
    schema_path = path.parent / schema_path
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"无法读取 manifest Schema：{schema_path}: {error}") from error
    if not isinstance(schema, Mapping):
        raise ValueError("manifest Schema 顶层必须是对象")
    validate(manifest, schema)
    validate_manifest_semantics(manifest)
    return manifest

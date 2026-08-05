from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence

from manifest import (
    atomic_write_json,
    canonical_json,
    validate_manifest_semantics,
)

ROOTS = {
    "普通高考": "regular",
    "春季高考": "spring",
}
OWNED_SOURCE_FIELDS = (
    "source_id",
    "upstream_path",
    "git_blob_oid",
    "year",
    "exam_type",
    "raw_paper_name",
)
_OID_RE = re.compile(r"^[0-9a-f]{40,64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def parse_ls_tree(raw: bytes) -> List[Dict[str, str]]:
    if not isinstance(raw, bytes):
        raise TypeError("ls-tree 输出必须是 bytes")
    if not raw:
        return []
    if not raw.endswith(b"\0"):
        raise ValueError("ls-tree -z 输出缺少结尾 NUL")

    entries: List[Dict[str, str]] = []
    seen_paths = set()
    for record in raw[:-1].split(b"\0"):
        if not record or b"\t" not in record:
            raise ValueError("ls-tree 记录格式错误")
        header, encoded_path = record.split(b"\t", 1)
        fields = header.split(b" ")
        if len(fields) != 3:
            raise ValueError("ls-tree 记录头格式错误")
        encoded_mode, object_type, encoded_oid = fields
        if object_type != b"blob":
            raise ValueError("递归 tree 清单只允许 blob 记录")
        try:
            mode = encoded_mode.decode("ascii")
            oid = encoded_oid.decode("ascii")
            path = encoded_path.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("ls-tree 记录不是有效 UTF-8/ASCII") from error
        if not re.fullmatch(r"[0-7]{6}", mode):
            raise ValueError(f"无效 Git mode：{mode}")
        if not _OID_RE.fullmatch(oid):
            raise ValueError(f"无效 Git blob OID：{oid}")
        if not path or path in seen_paths:
            raise ValueError(f"空路径或重复路径：{path!r}")
        seen_paths.add(path)
        entries.append({"mode": mode, "oid": oid, "path": path})
    return entries


def git_tree(repo: Path, commit: str) -> List[Dict[str, str]]:
    repo = Path(repo)
    environment = os.environ.copy()
    environment["GIT_NO_LAZY_FETCH"] = "1"
    completed = subprocess.run(
        [
            "git", "-C", str(repo), "ls-tree", "-r", "-z", "--full-tree",
            commit,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        env=environment,
    )
    return parse_ls_tree(completed.stdout)


def source_id(url: str, commit: str, path: str) -> str:
    identity = json.dumps(
        [url, commit, path],
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "src-" + hashlib.sha256(identity).hexdigest()


def _source_from_entry(
    entry: Mapping[str, str], url: str, commit: str
) -> Optional[Dict[str, Any]]:
    path = entry.get("path")
    oid = entry.get("oid")
    if not isinstance(path, str) or not isinstance(oid, str):
        raise ValueError("tree entry 缺少 path/oid")
    parts = path.split("/")
    if not parts or parts[0] not in ROOTS:
        return None
    if not path.lower().endswith(".pdf"):
        return None
    if len(parts) < 3 or not re.fullmatch(r"[0-9]{4}", parts[1]):
        raise ValueError(f"来源 PDF 路径缺少四位年份：{path}")
    if not _OID_RE.fullmatch(oid):
        raise ValueError(f"来源 PDF blob OID 无效：{path}")
    return {
        "source_id": source_id(url, commit, path),
        "upstream_path": path,
        "git_blob_oid": oid,
        "year": int(parts[1]),
        "exam_type": ROOTS[parts[0]],
        "track": None,
        "regions": [],
        "raw_paper_name": parts[-1],
        "source_state": "not_started",
        "paper_relation": None,
        "paper_id": None,
        "artifact": None,
        "issue_ids": [],
    }


def build_inventory(
    entries: Sequence[Mapping[str, str]], url: str, commit: str
) -> Dict[str, Any]:
    sources = []
    for entry in entries:
        source = _source_from_entry(entry, url, commit)
        if source is not None:
            sources.append(source)
    sources.sort(key=lambda item: item["upstream_path"])
    source_ids = [item["source_id"] for item in sources]
    paths = [item["upstream_path"] for item in sources]
    if len(source_ids) != len(set(source_ids)) or len(paths) != len(set(paths)):
        raise ValueError("来源清单包含重复 source_id 或路径")

    root_counts = {"regular": 0, "spring": 0}
    for source in sources:
        root_counts[source["exam_type"]] += 1
    manifest = {
        "$schema": "schemas/source-manifest.schema.json",
        "schema_version": 1,
        "revision": 0,
        "last_transaction_id": None,
        "upstream": {
            "url": url,
            "commit": commit,
            "scoped_roots": list(ROOTS),
        },
        "inventory": {
            "total_sources": len(sources),
            "root_counts": root_counts,
        },
        "sources": sources,
        "papers": [],
        "batches": [],
    }
    validate_manifest_semantics(manifest)
    return manifest


def _source_map(manifest: Mapping[str, Any], label: str) -> Dict[str, Mapping[str, Any]]:
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError(f"{label} manifest 的 sources 必须是数组")
    result: Dict[str, Mapping[str, Any]] = {}
    for source in sources:
        if not isinstance(source, Mapping):
            raise ValueError(f"{label} manifest 含非对象 source")
        identifier = source.get("source_id")
        if not isinstance(identifier, str) or identifier in result:
            raise ValueError(f"{label} manifest 的 source_id 缺失或重复")
        result[identifier] = source
    return result


def merge_inventory(
    existing: Mapping[str, Any], fresh: Mapping[str, Any]
) -> Dict[str, Any]:
    if not isinstance(existing, Mapping) or not isinstance(fresh, Mapping):
        raise ValueError("inventory merge 输入必须是对象")
    old_upstream = existing.get("upstream")
    new_upstream = fresh.get("upstream")
    if not isinstance(old_upstream, Mapping) or not isinstance(new_upstream, Mapping):
        raise ValueError("manifest 缺少 upstream")
    for field in ("url", "commit", "scoped_roots"):
        if old_upstream.get(field) != new_upstream.get(field):
            raise ValueError(f"上游 Git 身份变化：{field}")

    old_sources = _source_map(existing, "existing")
    new_sources = _source_map(fresh, "fresh")
    if set(old_sources) != set(new_sources):
        raise ValueError("来源集合变化，拒绝覆盖 existing manifest")

    for identifier in old_sources:
        old = old_sources[identifier]
        new = new_sources[identifier]
        if old.get("upstream_path") != new.get("upstream_path"):
            raise ValueError(f"来源路径变化：{identifier}")
        if old.get("git_blob_oid") != new.get("git_blob_oid"):
            raise ValueError(f"来源 blob OID 变化：{identifier}")

    merged = copy.deepcopy(dict(existing))
    merged["upstream"] = copy.deepcopy(dict(new_upstream))
    merged["inventory"] = copy.deepcopy(fresh.get("inventory"))
    merged_sources = merged.get("sources")
    if not isinstance(merged_sources, list):
        raise ValueError("existing manifest 的 sources 必须是数组")
    for target in merged_sources:
        identifier = target["source_id"]
        source = new_sources[identifier]
        for field in OWNED_SOURCE_FIELDS:
            target[field] = copy.deepcopy(source[field])
    return merged


def _remote_url(repo: Path) -> str:
    environment = os.environ.copy()
    environment["GIT_NO_LAZY_FETCH"] = "1"
    completed = subprocess.run(
        ["git", "-C", str(repo), "config", "--get", "remote.origin.url"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        env=environment,
    )
    url = completed.stdout.strip()
    if not url:
        raise ValueError("上游仓库缺少 remote.origin.url")
    return url


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"无法读取 source manifest：{path}: {error}") from error
    if not isinstance(value, dict):
        raise ValueError("source manifest 顶层必须是对象")
    return value


def _validate_expectations(
    manifest: Mapping[str, Any], expected_total: int,
    expected_roots: Mapping[str, int],
) -> None:
    inventory = manifest.get("inventory")
    if not isinstance(inventory, Mapping):
        raise ValueError("manifest 缺少 inventory")
    actual_total = inventory.get("total_sources")
    actual_roots = inventory.get("root_counts")
    if actual_total != expected_total:
        raise ValueError(f"来源总数不符：期望 {expected_total}，实际 {actual_total}")
    if dict(actual_roots) != dict(expected_roots):
        raise ValueError(
            f"来源根计数不符：期望 {dict(expected_roots)}，实际 {actual_roots}"
        )
    if expected_total != sum(expected_roots.values()):
        raise ValueError("--expect-total 与 --expect-root 之和不一致")


class _ExpectRootAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str,
        option_string: Optional[str] = None,
    ) -> None:
        match = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*)=([0-9]+)", values)
        if match is None:
            parser.error(f"{option_string} 必须是 NAME=N：{values}")
        name, raw_count = match.groups()
        current = dict(getattr(namespace, self.dest, None) or {})
        if name in current:
            parser.error(f"重复 {option_string}：{name}")
        current[name] = int(raw_count)
        setattr(namespace, self.dest, current)


def _commit(value: str) -> str:
    if _COMMIT_RE.fullmatch(value) is None:
        raise argparse.ArgumentTypeError("commit 必须是 40 位小写十六进制 SHA")
    return value


def _nonnegative(value: str) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("必须是非负整数") from error
    if number < 0:
        raise argparse.ArgumentTypeError("必须是非负整数")
    return number


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="建立固定上游来源清单")
    subparsers = parser.add_subparsers(dest="command", required=True)
    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--repo", required=True, type=Path)
    inventory.add_argument("--commit", required=True, type=_commit)
    destination = inventory.add_mutually_exclusive_group(required=True)
    destination.add_argument("--output", type=Path)
    destination.add_argument("--check", type=Path)
    inventory.add_argument("--expect-total", required=True, type=_nonnegative)
    inventory.add_argument(
        "--expect-root",
        required=True,
        action=_ExpectRootAction,
        default=None,
        metavar="NAME=N",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command != "inventory":
        raise ValueError(f"未知命令：{arguments.command}")
    repo = arguments.repo
    if not repo.is_dir():
        raise ValueError(f"上游仓库目录不存在：{repo}")
    url = _remote_url(repo)
    fresh = build_inventory(git_tree(repo, arguments.commit), url, arguments.commit)
    _validate_expectations(fresh, arguments.expect_total, arguments.expect_root)

    destination = arguments.output or arguments.check
    if arguments.output is not None:
        result = fresh
        if destination.exists():
            result = merge_inventory(_load_json(destination), fresh)
        _validate_expectations(result, arguments.expect_total, arguments.expect_root)
        atomic_write_json(destination, result)
        return 0

    existing = _load_json(destination)
    expected = merge_inventory(existing, fresh)
    _validate_expectations(expected, arguments.expect_total, arguments.expect_root)
    raw = destination.read_bytes()
    expected_bytes = canonical_json(expected).encode("utf-8")
    if raw != expected_bytes:
        raise ValueError("source manifest 字节或语义与固定 inventory 不一致")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=os.sys.stderr)
        raise SystemExit(1)

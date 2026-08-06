from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import posixpath
import re
import shutil
import stat
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, List, Mapping, MutableMapping, Optional, Sequence

from issues import load_issues, upsert_issue
from manifest import (
    canonical_json,
    durable_fsync,
    validate_manifest_semantics,
)
from schema_validate import validate as validate_schema
from transaction import MANIFEST_TARGET, RepoLock, Transaction

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
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PAGES_RE = re.compile(r"(?m)^Pages:\s*([0-9]+)\s*$")
_PDFINFO_VERSION_RE = re.compile(r"(?i)pdfinfo\s+version\s+([^\r\n]+)")
_GIT_BACKOFFS = (2, 5, 10)
_HTTP_CONNECT_TIMEOUT = 15
_HTTP_READ_DEADLINE = 120
_RAW_LIMIT = 100 * 1024 * 1024
_ZIP_LIMIT = 1024 * 1024 * 1024
_SOURCE_ISSUE_TYPES = {
    "source-unavailable", "source-unreadable", "source-mismatch",
}


@dataclass
class FetchContext:
    commit: str
    pdfinfo: Optional[Path] = None
    deadline: Optional[float] = None
    monotonic: Callable[[], float] = time.monotonic
    sleep: Callable[[float], None] = time.sleep
    http_timeout: int = _HTTP_CONNECT_TIMEOUT
    read_deadline_seconds: int = _HTTP_READ_DEADLINE
    raw_limit: int = _RAW_LIMIT
    zip_limit: int = _ZIP_LIMIT
    zip_downloaded: bool = False
    zip_download_count: int = 0
    sleeps: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if _COMMIT_RE.fullmatch(self.commit) is None:
            raise ValueError("commit 必须是 40 位小写十六进制 SHA")
        self.pdfinfo = _resolve_pdfinfo(self.pdfinfo)
        if self.deadline is not None and self.deadline <= 0:
            raise ValueError("deadline 必须是正数")

    def check_deadline(self) -> None:
        if self.deadline is not None and self.monotonic() >= self.deadline:
            raise RuntimeError("materialize 总 deadline 已到")

    def backoff(self, seconds: int) -> None:
        self.check_deadline()
        if (
            self.deadline is not None
            and self.monotonic() + seconds >= self.deadline
        ):
            raise RuntimeError("materialize 总 deadline 将在重试前到达")
        self.sleep(seconds)
        self.check_deadline()


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
    for field_name in ("url", "commit", "scoped_roots"):
        if old_upstream.get(field_name) != new_upstream.get(field_name):
            raise ValueError(f"上游 Git 身份变化：{field_name}")

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

    new_inventory = fresh.get("inventory")
    if not isinstance(new_inventory, Mapping):
        raise ValueError("fresh manifest 缺少 inventory")

    merged = copy.deepcopy(dict(existing))
    merged_upstream = merged.get("upstream")
    merged_inventory = merged.get("inventory")
    if not isinstance(merged_upstream, MutableMapping):
        raise ValueError("existing manifest 的 upstream 必须是对象")
    if not isinstance(merged_inventory, MutableMapping):
        raise ValueError("existing manifest 的 inventory 必须是对象")
    for field_name in ("url", "commit", "scoped_roots"):
        merged_upstream[field_name] = copy.deepcopy(new_upstream[field_name])
    for field_name in ("total_sources", "root_counts"):
        merged_inventory[field_name] = copy.deepcopy(new_inventory[field_name])
    merged_sources = merged.get("sources")
    if not isinstance(merged_sources, list):
        raise ValueError("existing manifest 的 sources 必须是数组")
    for target in merged_sources:
        identifier = target["source_id"]
        source = new_sources[identifier]
        for field_name in OWNED_SOURCE_FIELDS:
            target[field_name] = copy.deepcopy(source[field_name])
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
    if not isinstance(actual_roots, Mapping) or dict(actual_roots) != dict(expected_roots):
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


def _positive(value: str) -> int:
    number = _nonnegative(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("必须是正整数")
    return number


def _absolute_path(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("工具必须使用绝对路径")
    return path


def _resolve_pdfinfo(value: Optional[Path]) -> Path:
    if value is None:
        discovered = shutil.which("pdfinfo")
        if discovered is None:
            raise ValueError("找不到 pdfinfo")
        value = Path(discovered)
    path = Path(value)
    if not path.is_absolute():
        raise ValueError("pdfinfo 必须使用绝对路径")
    return path


def _git_blob_oid(value: bytes, length: int) -> str:
    payload = (f"blob {len(value)}\0").encode("ascii") + value
    if length == 40:
        return hashlib.sha1(payload).hexdigest()
    if length == 64:
        return hashlib.sha256(payload).hexdigest()
    raise ValueError("Git blob OID 长度必须是 40 或 64")


def verify_fetched_bytes(source: Mapping[str, Any], value: bytes) -> Dict[str, Any]:
    if not isinstance(value, bytes):
        raise TypeError("来源内容必须是 bytes")
    expected = source.get("git_blob_oid")
    if not isinstance(expected, str) or _OID_RE.fullmatch(expected) is None:
        raise ValueError("来源缺少合法 git_blob_oid")
    actual = _git_blob_oid(value, len(expected))
    if actual != expected:
        raise RuntimeError(f"下载内容 blob OID 不匹配：期望 {expected}，实际 {actual}")
    if not value.startswith(b"%PDF-"):
        raise RuntimeError("来源内容缺少 %PDF- 文件头")
    sha256 = hashlib.sha256(value).hexdigest()
    previous = source.get("artifact")
    if isinstance(previous, Mapping):
        expected_sha256 = previous.get("sha256")
        if expected_sha256 is not None and expected_sha256 != sha256:
            raise RuntimeError("来源内容 SHA-256 与既有 artifact 不匹配")
    return {
        "size_bytes": len(value),
        "sha256": sha256,
        "media_type": "application/pdf",
        "header_is_pdf": True,
        "git_oid_verified": True,
    }


def inspect_existing(path: Path, expected_oid: str) -> str:
    path = Path(path)
    if not path.exists() and not path.is_symlink():
        return "missing"
    try:
        status = path.lstat()
    except OSError as error:
        raise RuntimeError(f"无法检查已有来源：{path}: {error}") from error
    if not stat.S_ISREG(status.st_mode):
        return "mismatched"
    completed = subprocess.run(
        ["git", "hash-object", str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
    )
    actual = completed.stdout.strip()
    if len(expected_oid) == 64 and len(actual) != 64:
        actual = _git_blob_oid(path.read_bytes(), 64)
    return "matching" if actual == expected_oid else "mismatched"


def inspect_pdf(path: Path, pdfinfo: Path) -> Dict[str, Any]:
    path = Path(path)
    tool = _resolve_pdfinfo(pdfinfo)
    if not tool.is_file() or not os.access(str(tool), os.X_OK):
        raise ValueError(f"pdfinfo 不存在或不可执行：{tool}")
    version_result = subprocess.run(
        [str(tool), "-v"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=_HTTP_READ_DEADLINE,
    )
    if version_result.returncode != 0:
        raise RuntimeError(f"pdfinfo -v 失败：{version_result.returncode}")
    version_text = version_result.stdout + "\n" + version_result.stderr
    version_match = _PDFINFO_VERSION_RE.search(version_text)
    if version_match is None or not version_match.group(1).strip():
        raise RuntimeError("pdfinfo -v 缺少版本号")
    completed = subprocess.run(
        [str(tool), str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=_HTTP_READ_DEADLINE,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"pdfinfo 校验失败：{path}（exit {completed.returncode}）"
        )
    pages_match = _PAGES_RE.search(completed.stdout)
    if pages_match is None or int(pages_match.group(1)) <= 0:
        raise RuntimeError(f"pdfinfo 缺少正数 Pages：{path}")
    return {
        "page_count": int(pages_match.group(1)),
        "pdf_check": "passed",
        "pdfinfo_version": version_match.group(1).strip(),
    }


def _artifact_from_path(
    path: Path, source: Mapping[str, Any], pdfinfo: Path
) -> Dict[str, Any]:
    try:
        value = Path(path).read_bytes()
    except OSError as error:
        raise RuntimeError(f"无法读取 PDF：{path}: {error}") from error
    artifact = verify_fetched_bytes(source, value)
    artifact.update(inspect_pdf(path, pdfinfo))
    return artifact


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(str(path), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_verified_cache(
    cache_path: Path,
    source: Mapping[str, Any],
    value: bytes,
    pdfinfo: Path,
) -> Path:
    verify_fetched_bytes(source, value)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache_path.with_name(cache_path.name + ".tmp")
    try:
        temporary.unlink(missing_ok=True)
        descriptor = os.open(
            str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        try:
            offset = 0
            while offset < len(value):
                offset += os.write(descriptor, value[offset:])
            durable_fsync(descriptor)
        finally:
            os.close(descriptor)
        _artifact_from_path(temporary, source, pdfinfo)
        os.replace(str(temporary), str(cache_path))
        _fsync_directory(cache_path.parent)
        return cache_path
    finally:
        temporary.unlink(missing_ok=True)


def _verified_cache(
    cache_path: Path, source: Mapping[str, Any], pdfinfo: Path
) -> bool:
    if not cache_path.exists() and not cache_path.is_symlink():
        return False
    try:
        if not stat.S_ISREG(cache_path.lstat().st_mode):
            raise RuntimeError("cache 不是普通文件")
        _artifact_from_path(cache_path, source, pdfinfo)
        return True
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError):
        cache_path.unlink(missing_ok=True)
        return False


def cache_directory(repo: Path) -> Path:
    repo = Path(repo)
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-dir"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
    )
    git_dir = Path(completed.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = repo / git_dir
    return git_dir.resolve() / "gaokao-pdf-cache"


def _git_cat_file(repo: Path, oid: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", oid],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=_HTTP_READ_DEADLINE,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"git cat-file 失败：{message or completed.returncode}")
    return completed.stdout


def _git_has_blob(repo: Path, oid: str) -> bool:
    environment = os.environ.copy()
    environment["GIT_NO_LAZY_FETCH"] = "1"
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", oid + "^{blob}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=environment,
    )
    return completed.returncode == 0


def _download_http_to(
    url: str, destination: Path, limit: int, context: FetchContext
) -> None:
    destination = Path(destination)
    context.check_deadline()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)
    started = context.monotonic()
    request = urllib.request.Request(
        url, headers={"User-Agent": "gaokao-latex-source-materializer/1"}
    )
    total = 0
    try:
        with urllib.request.urlopen(request, timeout=context.http_timeout) as response:
            raw_length = response.headers.get("Content-Length")
            if raw_length is not None:
                try:
                    declared = int(raw_length)
                except ValueError as error:
                    raise RuntimeError("HTTP Content-Length 无效") from error
                if declared < 0 or declared > limit:
                    raise RuntimeError(f"HTTP 响应超过限制 {limit} bytes")
            with destination.open("xb") as handle:
                while True:
                    context.check_deadline()
                    if context.monotonic() - started >= context.read_deadline_seconds:
                        raise RuntimeError("HTTP 单次读取 deadline 已到")
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > limit:
                        raise RuntimeError(f"HTTP 响应超过限制 {limit} bytes")
                    handle.write(chunk)
                handle.flush()
                durable_fsync(handle.fileno())
            if raw_length is not None and total != declared:
                raise RuntimeError(
                    f"HTTP 响应长度不符：声明 {declared}，实际 {total}"
                )
    except BaseException:
        destination.unlink(missing_ok=True)
        raise


def _normalized_zip_name(name: str) -> str:
    if not name or "\x00" in name or "\\" in name:
        raise RuntimeError(f"ZIP 路径非法：{name!r}")
    raw = name[:-1] if name.endswith("/") else name
    if not raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise RuntimeError(f"ZIP 包含绝对路径：{name!r}")
    parts = raw.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise RuntimeError(f"ZIP 路径未规范化或包含 ..：{name!r}")
    normalized = posixpath.normpath(raw)
    if normalized != raw or PurePosixPath(normalized).is_absolute():
        raise RuntimeError(f"ZIP 路径未规范化：{name!r}")
    return normalized


def _validated_zip_infos(archive: zipfile.ZipFile) -> Dict[str, zipfile.ZipInfo]:
    result: Dict[str, zipfile.ZipInfo] = {}
    for info in archive.infolist():
        normalized = _normalized_zip_name(info.filename)
        mode = (info.external_attr >> 16) & 0o170000
        if mode == stat.S_IFLNK:
            raise RuntimeError(f"ZIP 包含 symlink：{info.filename}")
        if normalized in result:
            raise RuntimeError(f"ZIP 包含重复规范路径：{normalized}")
        result[normalized] = info
    bad = archive.testzip()
    if bad is not None:
        raise RuntimeError(f"ZIP CRC/结构校验失败：{bad}")
    return result


def safe_zip_member_bytes(
    zip_path: Path, member_name: str, limit: int = _RAW_LIMIT
) -> bytes:
    expected = _normalized_zip_name(member_name)
    try:
        with zipfile.ZipFile(str(zip_path)) as archive:
            infos = _validated_zip_infos(archive)
            info = infos.get(expected)
            if info is None or info.is_dir():
                raise RuntimeError(f"ZIP 缺少精确成员：{expected}")
            if info.file_size > limit:
                raise RuntimeError(f"ZIP 精确成员超过限制 {limit} bytes")
            chunks = []
            total = 0
            with archive.open(info, "r") as handle:
                while True:
                    chunk = handle.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > limit:
                        raise RuntimeError(f"ZIP 精确成员超过限制 {limit} bytes")
                    chunks.append(chunk)
            return b"".join(chunks)
    except zipfile.BadZipFile as error:
        raise RuntimeError(f"ZIP 结构损坏：{zip_path}") from error


def _ensure_codeload_zip(
    cache_dir: Path, context: FetchContext
) -> Path:
    zip_path = cache_dir / (context.commit + ".zip")
    cache_dir.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        try:
            with zipfile.ZipFile(str(zip_path)) as archive:
                _validated_zip_infos(archive)
            return zip_path
        except (OSError, RuntimeError, zipfile.BadZipFile):
            zip_path.unlink(missing_ok=True)
    if context.zip_download_count >= 1:
        raise RuntimeError("本次运行的 codeload ZIP 下载额度已用尽")
    context.check_deadline()
    temporary = zip_path.with_name(zip_path.name + ".tmp")
    context.zip_download_count += 1
    context.zip_downloaded = True
    url = "https://codeload.github.com/deekur/gaokaomath/zip/" + context.commit
    try:
        _download_http_to(url, temporary, context.zip_limit, context)
        with zipfile.ZipFile(str(temporary)) as archive:
            _validated_zip_infos(archive)
        os.replace(str(temporary), str(zip_path))
        _fsync_directory(cache_dir)
        return zip_path
    except zipfile.BadZipFile as error:
        raise RuntimeError("codeload ZIP 结构损坏") from error
    finally:
        temporary.unlink(missing_ok=True)


def _zip_member_to_cache(
    repo: Path,
    source: Mapping[str, Any],
    cache_dir: Path,
    context: FetchContext,
) -> Path:
    del repo
    zip_path = _ensure_codeload_zip(cache_dir, context)
    member = "gaokaomath-%s/%s" % (context.commit, source["upstream_path"])
    value = safe_zip_member_bytes(zip_path, member, context.raw_limit)
    temporary = cache_dir / (str(source["git_blob_oid"]) + ".pdf.zip.tmp")
    temporary.unlink(missing_ok=True)
    temporary.write_bytes(value)
    return temporary


def _accept_candidate(
    candidate: Path,
    cache_path: Path,
    source: Mapping[str, Any],
    context: FetchContext,
) -> Path:
    try:
        value = Path(candidate).read_bytes()
        return _write_verified_cache(cache_path, source, value, context.pdfinfo)
    finally:
        if Path(candidate) != cache_path:
            Path(candidate).unlink(missing_ok=True)


def fetch_blob(
    repo: Path,
    source: Mapping[str, Any],
    cache_dir: Path,
    context: Optional[FetchContext] = None,
) -> Path:
    repo = Path(repo)
    cache_dir = Path(cache_dir)
    if context is None:
        completed = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
            env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
        )
        context = FetchContext(commit=completed.stdout.strip())
    context.check_deadline()
    oid = source.get("git_blob_oid")
    upstream_path = source.get("upstream_path")
    if not isinstance(oid, str) or _OID_RE.fullmatch(oid) is None:
        raise ValueError("source 缺少合法 git_blob_oid")
    if not isinstance(upstream_path, str) or not upstream_path:
        raise ValueError("source 缺少 upstream_path")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / (oid + ".pdf")
    if _verified_cache(cache_path, source, context.pdfinfo):
        return cache_path

    errors = []
    for delay in _GIT_BACKOFFS:
        context.check_deadline()
        try:
            value = _git_cat_file(repo, oid)
            return _write_verified_cache(
                cache_path, source, value, context.pdfinfo
            )
        except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
            errors.append("git: " + str(error))
            context.backoff(delay)

    encoded = urllib.parse.quote(upstream_path, safe="/")
    raw_url = (
        "https://raw.githubusercontent.com/deekur/gaokaomath/"
        + context.commit + "/" + encoded
    )
    raw_temporary = cache_dir / (oid + ".pdf.raw.tmp")
    try:
        _download_http_to(raw_url, raw_temporary, context.raw_limit, context)
        return _accept_candidate(
            raw_temporary, cache_path, source, context
        )
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        raw_temporary.unlink(missing_ok=True)
        errors.append("raw: " + str(error))

    try:
        zip_temporary = _zip_member_to_cache(
            repo, source, cache_dir, context
        )
        return _accept_candidate(
            zip_temporary, cache_path, source, context
        )
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        errors.append("zip: " + str(error))
    raise RuntimeError(
        f"source-unavailable：{source.get('source_id')}；" + "；".join(errors)
    )


def _copy_verified_target(
    candidate: Path,
    source: Mapping[str, Any],
    target: Path,
    pdfinfo: Path,
) -> Dict[str, Any]:
    candidate = Path(candidate)
    target = Path(target)
    _artifact_from_path(candidate, source, pdfinfo)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_temporary = tempfile.mkstemp(
        prefix="." + target.name + ".", suffix=".tmp", dir=str(target.parent)
    )
    temporary = Path(raw_temporary)
    try:
        with candidate.open("rb") as source_handle, os.fdopen(descriptor, "wb") as target_handle:
            shutil.copyfileobj(source_handle, target_handle, length=1024 * 1024)
            target_handle.flush()
            durable_fsync(target_handle.fileno())
        artifact = _artifact_from_path(temporary, source, pdfinfo)
        try:
            os.link(str(temporary), str(target))
        except FileExistsError:
            state = inspect_existing(target, str(source["git_blob_oid"]))
            if state != "matching":
                raise RuntimeError(
                    f"已有文件与固定 blob 不一致，拒绝覆盖：{target}"
                )
            return _artifact_from_path(target, source, pdfinfo)
        _fsync_directory(target.parent)
        return artifact
    finally:
        temporary.unlink(missing_ok=True)


def materialize_source(
    source: Mapping[str, Any],
    *,
    target: Path,
    fetcher: Callable[[Mapping[str, Any]], Any],
    pdfinfo: Optional[Path] = None,
) -> Dict[str, Any]:
    target = Path(target)
    tool = _resolve_pdfinfo(pdfinfo)
    state = inspect_existing(target, str(source.get("git_blob_oid", "")))
    if state == "mismatched":
        raise RuntimeError(f"已有文件与固定 blob 不一致，拒绝覆盖：{target}")
    if state == "matching":
        return _artifact_from_path(target, source, tool)

    fetched = fetcher(source)
    if isinstance(fetched, bytes):
        verify_fetched_bytes(source, fetched)
        with tempfile.TemporaryDirectory() as temporary_dir:
            candidate = Path(temporary_dir) / "candidate.pdf"
            candidate.write_bytes(fetched)
            return _copy_verified_target(candidate, source, target, tool)
    candidate = Path(fetched)
    return _copy_verified_target(candidate, source, target, tool)


def materialization_status(repo: Path, manifest_path: Path) -> Dict[str, int]:
    manifest = _load_json(manifest_path)
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError("manifest sources 必须是数组")
    result = {
        "total": len(sources), "matching": 0, "mismatched": 0,
        "missing": 0, "artifacts": 0,
    }
    for source in sources:
        if not isinstance(source, Mapping):
            raise ValueError("manifest source 必须是对象")
        state = inspect_existing(
            Path(repo) / str(source["upstream_path"]),
            str(source["git_blob_oid"]),
        )
        result[state] += 1
        if source.get("artifact") is not None:
            result["artifacts"] += 1
    return result


def probe_transports(
    repo: Path, commit: str, pdfinfo: Optional[Path] = None
) -> Dict[str, Any]:
    repo = Path(repo)
    tool = _resolve_pdfinfo(pdfinfo)
    entries = git_tree(repo, commit)
    sources = []
    for entry in entries:
        source = _source_from_entry(entry, "https://github.com/deekur/gaokaomath", commit)
        if source is not None:
            sources.append(source)
    cache_dir = cache_directory(repo)
    first_missing = None
    used_cache = False
    for source in sources:
        oid = str(source["git_blob_oid"])
        if _git_has_blob(repo, oid):
            continue
        cache_path = cache_dir / (oid + ".pdf")
        if _verified_cache(cache_path, source, tool):
            used_cache = True
            continue
        first_missing = source
        break
    if first_missing is None:
        return {
            "ok": True,
            "channel": "local-or-cache" if used_cache else "local",
            "probe_source_id": None,
            "total_sources": len(sources),
        }

    context = FetchContext(commit=commit, pdfinfo=tool)
    oid = str(first_missing["git_blob_oid"])
    cache_path = cache_dir / (oid + ".pdf")
    errors = []
    try:
        value = _git_cat_file(repo, oid)
        _write_verified_cache(cache_path, first_missing, value, tool)
        return {
            "ok": True, "channel": "git",
            "probe_source_id": first_missing["source_id"],
            "total_sources": len(sources),
        }
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        errors.append("git: " + str(error))

    encoded = urllib.parse.quote(str(first_missing["upstream_path"]), safe="/")
    raw_url = (
        "https://raw.githubusercontent.com/deekur/gaokaomath/"
        + commit + "/" + encoded
    )
    temporary = cache_dir / (oid + ".pdf.preflight.tmp")
    try:
        _download_http_to(raw_url, temporary, context.raw_limit, context)
        _accept_candidate(temporary, cache_path, first_missing, context)
        return {
            "ok": True, "channel": "raw",
            "probe_source_id": first_missing["source_id"],
            "total_sources": len(sources),
        }
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        temporary.unlink(missing_ok=True)
        errors.append("raw: " + str(error))

    try:
        zip_temporary = _zip_member_to_cache(
            repo, first_missing, cache_dir, context
        )
        _accept_candidate(zip_temporary, cache_path, first_missing, context)
        return {
            "ok": True, "channel": "zip",
            "probe_source_id": first_missing["source_id"],
            "total_sources": len(sources),
        }
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
        errors.append("zip: " + str(error))
    raise RuntimeError("transport preflight 全部失败：" + "；".join(errors))


def _repository_root(path: Path) -> Path:
    completed = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
    )
    return Path(completed.stdout.strip()).resolve()


def _relative_to_repo(root: Path, path: Path) -> str:
    resolved = Path(path).resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise ValueError(f"state 文件不在仓库内：{path}") from error
    return relative.as_posix()


def _validated_manifest_value(manifest_path: Path, value: Mapping[str, Any]) -> None:
    schema_reference = value.get("$schema")
    if not isinstance(schema_reference, str) or not schema_reference:
        raise ValueError("manifest 缺少 $schema")
    schema_relative = Path(schema_reference)
    if schema_relative.is_absolute() or ".." in schema_relative.parts:
        raise ValueError("manifest $schema 必须是安全相对路径")
    schema = _load_json(Path(manifest_path).parent / schema_relative)
    validate_schema(value, schema)
    validate_manifest_semantics(value)


def _issue_candidate(
    source_id_value: str, issue_type: str, evidence: str
) -> Dict[str, Any]:
    resume = {
        "source-mismatch": "保留已有文件并人工核验或移走后重跑，禁止覆盖",
        "source-unreadable": "检查固定 blob 的 PDF 结构与 pdfinfo 输出后重跑",
        "source-unavailable": "恢复 Git/raw/codeload 任一可验证通道后重跑",
    }[issue_type]
    return {
        "paper_id": None,
        "affected_paper_ids": [],
        "source_id": source_id_value,
        "type": issue_type,
        "status": "open",
        "impact": "blocks_completion",
        "resume_action": resume,
        "current_evidence": evidence,
    }


def _updated_issue_ledger(
    issues_path: Path,
    source_id_value: str,
    issue_type: Optional[str],
    evidence: str,
) -> tuple:
    if not issues_path.is_file():
        raise ValueError(f"问题总账不存在：{issues_path}")
    with tempfile.TemporaryDirectory() as temporary_dir:
        scratch = Path(temporary_dir) / "issues.md"
        scratch.write_bytes(issues_path.read_bytes())
        added_id = None
        resolved_ids = []
        if issue_type is not None:
            if issue_type not in _SOURCE_ISSUE_TYPES:
                raise ValueError(f"非法来源问题类型：{issue_type}")
            added_id = upsert_issue(
                scratch, _issue_candidate(source_id_value, issue_type, evidence)
            )
        else:
            for issue in load_issues(scratch):
                if (
                    issue.get("source_id") == source_id_value
                    and issue.get("type") in _SOURCE_ISSUE_TYPES
                    and issue.get("status") != "resolved"
                ):
                    updated = copy.deepcopy(issue)
                    updated["status"] = "resolved"
                    updated["resume_action"] = "无需动作；固定 blob 已重新验证并物化"
                    updated["resolved_evidence"] = evidence
                    resolved_ids.append(upsert_issue(scratch, updated))
        return scratch.read_bytes(), added_id, resolved_ids


def state_source_result(
    repo: Path,
    manifest_path: Path,
    issues_path: Path,
    source_id_value: str,
    *,
    artifact: Optional[Mapping[str, Any]],
    issue_type: Optional[str] = None,
    evidence: str = "固定 blob、SHA-256、PDF 文件头和 pdfinfo 已验证",
) -> None:
    root = _repository_root(Path(repo))
    manifest_path = Path(manifest_path)
    issues_path = Path(issues_path)
    manifest_relative = _relative_to_repo(root, manifest_path)
    issues_relative = _relative_to_repo(root, issues_path)
    if manifest_relative != MANIFEST_TARGET:
        raise ValueError(
            f"state manifest 必须是 {MANIFEST_TARGET}，实际 {manifest_relative}"
        )
    with RepoLock(root):
        manifest = _load_json(manifest_path)
        revision = manifest.get("revision")
        if type(revision) is not int or revision < 0:
            raise ValueError("manifest revision 必须是非负整数")
        matching = [
            source for source in manifest.get("sources", [])
            if isinstance(source, MutableMapping)
            and source.get("source_id") == source_id_value
        ]
        if len(matching) != 1:
            raise ValueError(f"source_id 不存在或重复：{source_id_value}")
        source = matching[0]
        ledger_bytes, added_id, resolved_ids = _updated_issue_ledger(
            issues_path, source_id_value, issue_type, evidence
        )
        if issue_type is None:
            if artifact is None:
                raise ValueError("成功来源更新必须包含 artifact")
            source["artifact"] = copy.deepcopy(dict(artifact))
            source["source_state"] = "ready"
            source["issue_ids"] = [
                item for item in source.get("issue_ids", [])
                if item not in set(resolved_ids)
            ]
        else:
            if artifact is not None:
                raise ValueError("失败来源更新不得提供 artifact")
            source["source_state"] = "blocked"
            issue_ids = list(source.get("issue_ids", []))
            if added_id not in issue_ids:
                issue_ids.append(added_id)
            source["issue_ids"] = issue_ids

        transaction = Transaction(root)
        manifest["revision"] = revision + 1
        manifest["last_transaction_id"] = transaction.transaction_id
        _validated_manifest_value(manifest_path, manifest)
        targets = {
            issues_relative: ledger_bytes,
            MANIFEST_TARGET: canonical_json(manifest).encode("utf-8"),
        }
        transaction.prepare(
            "state", targets, inputs={}, expected_revision=revision
        )
        transaction.commit()


def validate_source_manifest(
    manifest_path: Path, require_artifacts: Optional[int] = None
) -> int:
    manifest_path = Path(manifest_path)
    manifest = _load_json(manifest_path)
    _validated_manifest_value(manifest_path, manifest)
    sources = manifest.get("sources")
    if not isinstance(sources, list):
        raise ValueError("manifest sources 必须是数组")
    count = sum(
        1 for source in sources
        if isinstance(source, Mapping) and source.get("artifact") is not None
    )
    if require_artifacts is not None and count != require_artifacts:
        raise ValueError(
            f"artifact 数量不符：期望 {require_artifacts}，实际 {count}"
        )
    return count


def _materialize_command(arguments: argparse.Namespace) -> int:
    if arguments.jobs != 1:
        raise ValueError("阶段 0 materialize 要求 --jobs 1")
    manifest_path = Path(arguments.manifest)
    issues_path = Path(arguments.issues)
    manifest = _load_json(manifest_path)
    upstream = manifest.get("upstream")
    if not isinstance(upstream, Mapping):
        raise ValueError("manifest 缺少 upstream")
    commit = upstream.get("commit")
    if not isinstance(commit, str) or _COMMIT_RE.fullmatch(commit) is None:
        raise ValueError("manifest upstream.commit 无效")

    # This is intentionally before RepoLock and before every tracked write.
    probe_transports(arguments.repo, commit, arguments.pdfinfo)

    all_sources = manifest.get("sources")
    if not isinstance(all_sources, list):
        raise ValueError("manifest sources 必须是数组")
    if arguments.source is not None:
        selected = [
            source for source in all_sources
            if isinstance(source, Mapping)
            and source.get("source_id") == arguments.source
        ]
        if len(selected) != 1:
            raise ValueError(f"未知 source_id：{arguments.source}")
    else:
        selected = [
            source for source in all_sources
            if isinstance(source, Mapping) and source.get("artifact") is None
        ]

    deadline = time.monotonic() + arguments.deadline_seconds
    context = FetchContext(
        commit=commit, pdfinfo=arguments.pdfinfo, deadline=deadline
    )
    upstream_cache = cache_directory(arguments.repo)
    failed = False
    for index, source in enumerate(selected):
        if time.monotonic() >= deadline:
            for unfinished in selected[index:]:
                state_source_result(
                    _repository_root(manifest_path.parent), manifest_path,
                    issues_path, str(unfinished["source_id"]), artifact=None,
                    issue_type="source-unavailable",
                    evidence="materialize 总 deadline 已到，未开始新的下载",
                )
            failed = True
            break
        target = Path(arguments.repo) / str(source["upstream_path"])
        existed = target.exists() or target.is_symlink()
        try:
            artifact = materialize_source(
                source,
                target=target,
                fetcher=lambda item: fetch_blob(
                    arguments.repo, item, upstream_cache, context
                ),
                pdfinfo=arguments.pdfinfo,
            )
        except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
            failed = True
            issue_type = "source-unavailable"
            message = str(error)
            if "已有文件与固定 blob 不一致" in message:
                issue_type = "source-mismatch"
            elif "pdfinfo" in message or "%PDF-" in message:
                issue_type = "source-unreadable"
            state_source_result(
                _repository_root(manifest_path.parent), manifest_path,
                issues_path, str(source["source_id"]), artifact=None,
                issue_type=issue_type, evidence=message,
            )
            continue

        try:
            project_repo = _repository_root(manifest_path.parent)
            state_source_result(
                project_repo, manifest_path, issues_path,
                str(source["source_id"]), artifact=artifact,
            )
        except BaseException:
            recovery_error = None
            try:
                with RepoLock(project_repo):
                    pass
            except BaseException as error:
                recovery_error = error
            current = _load_json(manifest_path)
            current_source = next(
                item for item in current.get("sources", [])
                if item.get("source_id") == source["source_id"]
            )
            if current_source.get("artifact") == artifact:
                continue
            if not existed:
                if inspect_existing(target, str(source["git_blob_oid"])) == "matching":
                    target.unlink(missing_ok=True)
                    _fsync_directory(target.parent)
            if recovery_error is not None:
                raise recovery_error
            raise
    return 1 if failed else 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="建立并物化固定上游来源清单")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inventory = subparsers.add_parser("inventory")
    inventory.add_argument("--repo", required=True, type=Path)
    inventory.add_argument("--commit", required=True, type=_commit)
    destination = inventory.add_mutually_exclusive_group(required=True)
    destination.add_argument("--output", type=Path)
    destination.add_argument("--check", type=Path)
    inventory.add_argument("--expect-total", required=True, type=_nonnegative)
    inventory.add_argument(
        "--expect-root", required=True, action=_ExpectRootAction,
        default=None, metavar="NAME=N",
    )

    preflight = subparsers.add_parser("transport-preflight")
    preflight.add_argument("--repo", required=True, type=Path)
    preflight.add_argument("--commit", required=True, type=_commit)

    status_parser = subparsers.add_parser("materialization-status")
    status_parser.add_argument("--repo", required=True, type=Path)
    status_parser.add_argument("--manifest", required=True, type=Path)

    materialize = subparsers.add_parser("materialize")
    materialize.add_argument("--repo", required=True, type=Path)
    materialize.add_argument("--manifest", required=True, type=Path)
    materialize.add_argument("--issues", required=True, type=Path)
    selector = materialize.add_mutually_exclusive_group(required=True)
    selector.add_argument("--all", action="store_true")
    selector.add_argument("--source")
    materialize.add_argument("--jobs", required=True, type=_positive)
    materialize.add_argument("--deadline-seconds", required=True, type=_positive)
    materialize.add_argument("--pdfinfo", required=True, type=_absolute_path)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--manifest", required=True, type=Path)
    validate_parser.add_argument("--require-artifacts", type=_nonnegative)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "inventory":
        repo = arguments.repo
        if not repo.is_dir():
            raise ValueError(f"上游仓库目录不存在：{repo}")
        url = _remote_url(repo)
        fresh = build_inventory(git_tree(repo, arguments.commit), url, arguments.commit)
        _validate_expectations(
            fresh, arguments.expect_total, arguments.expect_root
        )

        destination = arguments.output or arguments.check
        if arguments.output is not None:
            result = fresh
            if destination.exists():
                result = merge_inventory(_load_json(destination), fresh)
            _validate_expectations(
                result, arguments.expect_total, arguments.expect_root
            )
            from manifest import atomic_write_json
            atomic_write_json(destination, result)
            return 0

        existing = _load_json(destination)
        expected = merge_inventory(existing, fresh)
        _validate_expectations(
            expected, arguments.expect_total, arguments.expect_root
        )
        validate_manifest_semantics(expected)
        raw = destination.read_bytes()
        expected_bytes = canonical_json(expected).encode("utf-8")
        if raw != expected_bytes:
            raise ValueError("source manifest 字节或语义与固定 inventory 不一致")
        return 0

    if arguments.command == "transport-preflight":
        result = probe_transports(arguments.repo, arguments.commit)
        os.sys.stdout.write(canonical_json(result))
        return 0
    if arguments.command == "materialization-status":
        result = materialization_status(arguments.repo, arguments.manifest)
        os.sys.stdout.write(canonical_json(result))
        return 0
    if arguments.command == "validate":
        validate_source_manifest(
            arguments.manifest, arguments.require_artifacts
        )
        return 0
    if arguments.command == "materialize":
        return _materialize_command(arguments)
    raise ValueError(f"未知命令：{arguments.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError, RuntimeError, ValueError, subprocess.SubprocessError,
        urllib.error.URLError,
    ) as error:
        print(f"error: {error}", file=os.sys.stderr)
        raise SystemExit(1)

from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import os
import posixpath
import re
import shutil
import socket
import stat
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from collections import namedtuple
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Iterator, List, Mapping, MutableMapping, Optional, Sequence

from issues import IMPACTS as ISSUE_IMPACTS
from issues import issue_fingerprint, load_issues, question_issue, upsert_issue
from manifest import (
    canonical_json,
    durable_fsync,
    file_sha256,
    project_index,
    validate_index_metadata,
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
_PDFINFO_VERSION_RE = re.compile(
    r"(?i)pdfinfo\s+version\s+([0-9]+(?:\.[0-9]+)+(?:[-+._A-Za-z0-9]*)?)"
)
_GIT_BACKOFFS = (2, 5, 10)
_HTTP_CONNECT_TIMEOUT = 15
_HTTP_READ_DEADLINE = 120
_RAW_LIMIT = 100 * 1024 * 1024
_ZIP_LIMIT = 1024 * 1024 * 1024
_SOURCE_ISSUE_TYPES = {
    "source-unavailable", "source-unreadable", "source-mismatch",
}
_FIGURE_INPUT_RE = re.compile(r"\\input\{figures/([^{}/]+)\}")
_MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_MARKDOWN_TEX_FIGURE_LINK_RE = re.compile(
    r"(?m)^[ \t]*\[[^\]]*\]\(([^)\s]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)[ \t]*$"
)
_MARKDOWN_LINK_ANY_RE = re.compile(
    r"(?<!!)\[[^\]]*\]\(([^)\s]+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)

# 规范工程根目录由 manifest 目标路径固定，迁移时不另行猜测。
PROJECT_RELATIVE = PurePosixPath(MANIFEST_TARGET).parent.as_posix()
# 兼容 index 与问题总账各自只有一份规范路径；与 MANIFEST_TARGET 一起钉死事务目标。
INDEX_TARGET = PROJECT_RELATIVE + "/index.json"
ISSUES_TARGET = PROJECT_RELATIVE + "/missing-issues.md"
SOURCE_STATES = ("not_started", "ready", "blocked", "non_paper")
PAPER_RELATIONS = ("canonical", "exact_duplicate", "semantic_duplicate")
PRODUCTION_STATES = (
    "legacy_unverified", "planned", "source_ready", "transcription_draft",
    "questions_verified", "answers_draft", "answers_verified", "shared_frozen",
    "editions_generated", "compiled", "complete", "blocked",
)
BATCH_STATUSES = (
    "planned", "provenance_verified", "compiled_pending_review",
    "closed", "closed_with_blockers",
)
SOURCE_FILE_KEYS = ("questions", "answer_key", "solution_body", "combined_rendered")
MARKDOWN_SUFFIXES = {
    "questions": "_试题.md",
    "answer_key": "_答案要点.md",
    "solution_body": "_解析正文.md",
    "combined_rendered": "_含解析.md",
}
# 解析正文由 Task 6–12 建立，迁移时只登记路径、不要求存在。
REQUIRED_SOURCE_FILE_KEYS = ("questions", "answer_key", "combined_rendered")
# figure 引用次数只数当前已存在的两份规范 Markdown。
FIGURE_COUNT_SOURCE_KEYS = ("questions", "combined_rendered")
TRACK_BY_LEGACY = {"理科": "science", "文科": "arts", None: "none"}
# 规范 Markdown 路径固定分四类，后续生成器读登记值、不按规则拼路径。
MARKDOWN_GROUPS = ("文理", "默认卷", "新高考Ⅱ", "全国 2")
RECALL_PAPER_ID = "gk-2026-regular-national-1-recall"
# 回忆版唯一允许的本地 legacy 规范源；显式登记，禁止目录 glob。
RECALL_LEGACY_SOURCE = "2026/2026_数学真题_试题.md"

LegacyPaper = namedtuple(
    "LegacyPaper", "legacy_id paper_id track markdown_group markdown_prefix"
)
# 旧 ID → 稳定 paper_id 与规范 Markdown 前缀，逐字固定，禁止动态构造。
LEGACY_PAPERS = (
    LegacyPaper("2017li", "gk-2017-regular-national-1-science", "science",
                "文理", "2017/2017_数学真题_理"),
    LegacyPaper("2017wen", "gk-2017-regular-national-1-arts", "arts",
                "文理", "2017/2017_数学真题_文"),
    LegacyPaper("2018li", "gk-2018-regular-national-1-science", "science",
                "文理", "2018/2018_数学真题_理"),
    LegacyPaper("2018wen", "gk-2018-regular-national-1-arts", "arts",
                "文理", "2018/2018_数学真题_文"),
    LegacyPaper("2019li", "gk-2019-regular-national-1-science", "science",
                "文理", "2019/2019_数学真题_理"),
    LegacyPaper("2019wen", "gk-2019-regular-national-1-arts", "arts",
                "文理", "2019/2019_数学真题_文"),
    LegacyPaper("2020li", "gk-2020-regular-national-1-science", "science",
                "文理", "2020/2020_数学真题_理"),
    LegacyPaper("2020wen", "gk-2020-regular-national-1-arts", "arts",
                "文理", "2020/2020_数学真题_文"),
    LegacyPaper("2020x2", "gk-2020-regular-new-gaokao-2", "none",
                "新高考Ⅱ", "2020/2020_数学真题_新高考Ⅱ"),
    LegacyPaper("2021", "gk-2021-regular-new-gaokao-1", "none",
                "默认卷", "2021/2021_数学真题"),
    LegacyPaper("2021x2", "gk-2021-regular-new-gaokao-2", "none",
                "新高考Ⅱ", "2021/2021_数学真题_新高考Ⅱ"),
    LegacyPaper("2022", "gk-2022-regular-new-gaokao-1", "none",
                "默认卷", "2022/2022_数学真题"),
    LegacyPaper("2022x2", "gk-2022-regular-new-gaokao-2", "none",
                "新高考Ⅱ", "2022/2022_数学真题_新高考Ⅱ"),
    LegacyPaper("2023", "gk-2023-regular-new-gaokao-1", "none",
                "默认卷", "2023/2023_数学真题"),
    LegacyPaper("2023x2", "gk-2023-regular-new-gaokao-2", "none",
                "新高考Ⅱ", "2023/2023_数学真题_新高考Ⅱ"),
    LegacyPaper("2024", "gk-2024-regular-new-gaokao-1", "none",
                "默认卷", "2024/2024_数学真题"),
    LegacyPaper("2024x2", "gk-2024-regular-new-gaokao-2", "none",
                "新高考Ⅱ", "2024/2024_数学真题_新高考Ⅱ"),
    LegacyPaper("2025", "gk-2025-regular-national-1", "none",
                "默认卷", "2025/2025_数学真题"),
    LegacyPaper("2025g2", "gk-2025-regular-national-2", "none",
                "全国 2", "2025/2025_数学真题_全国2"),
    LegacyPaper("2026", RECALL_PAPER_ID, "none",
                "默认卷", "2026/2026_数学真题"),
    LegacyPaper("2026g2", "gk-2026-regular-national-2", "none",
                "全国 2", "2026/2026_数学真题_全国2"),
)
# paper_id → 冻结的 legacy_ids；`_validate_paper_semantics()` 用它定向核对迁移卷身份。
_LEGACY_IDS_BY_PAPER = {
    entry.paper_id: [entry.legacy_id] for entry in LEGACY_PAPERS
}
# 六个不可变阶段 0 子批次；成员顺序即常量表顺序。
PHASE0_BATCHES = (
    ("phase0-b01", (
        "gk-2017-regular-national-1-science", "gk-2017-regular-national-1-arts",
        "gk-2018-regular-national-1-science", "gk-2018-regular-national-1-arts",
    )),
    ("phase0-b02", (
        "gk-2019-regular-national-1-science", "gk-2019-regular-national-1-arts",
        "gk-2020-regular-national-1-science", "gk-2020-regular-national-1-arts",
    )),
    ("phase0-b03", (
        "gk-2020-regular-new-gaokao-2", "gk-2021-regular-new-gaokao-1",
        "gk-2021-regular-new-gaokao-2",
    )),
    ("phase0-b04", (
        "gk-2022-regular-new-gaokao-1", "gk-2022-regular-new-gaokao-2",
        "gk-2023-regular-new-gaokao-1", "gk-2023-regular-new-gaokao-2",
    )),
    ("phase0-b05", (
        "gk-2024-regular-new-gaokao-1", "gk-2024-regular-new-gaokao-2",
        "gk-2025-regular-national-1", "gk-2025-regular-national-2",
    )),
    ("phase0-b06", (RECALL_PAPER_ID, "gk-2026-regular-national-2")),
)
# Task 2 已建立的两条身份问题；迁移只验证不重建，漂移即零写入。
PHASE0_ISSUE_SEEDS = (
    {
        "issue_id": "ISSUE-0001",
        "type": "identity-ambiguous",
        "paper_id": RECALL_PAPER_ID,
        "affected_paper_ids": [],
        "conflict_code": "recall-vs-official",
    },
    {
        "issue_id": "ISSUE-0002",
        "type": "identity-ambiguous",
        "paper_id": None,
        "affected_paper_ids": [
            "gk-2017-regular-national-1-arts",
            "gk-2017-regular-national-1-science",
        ],
        "conflict_code": "regions-vs-upstream-path",
    },
)


@dataclass
class FetchContext:
    commit: str
    pdfinfo: Optional[Path] = None
    pdfinfo_version: Optional[str] = None
    deadline: Optional[float] = None
    monotonic: Callable[[], float] = time.monotonic
    sleep: Callable[[float], None] = time.sleep
    http_timeout: int = _HTTP_CONNECT_TIMEOUT
    read_deadline_seconds: int = _HTTP_READ_DEADLINE
    raw_limit: int = _RAW_LIMIT
    zip_limit: int = _ZIP_LIMIT
    zip_downloaded: bool = False
    zip_download_count: int = 0
    zip_path: Optional[Path] = None
    zip_infos: Optional[Dict[str, zipfile.ZipInfo]] = None
    sleeps: List[float] = field(default_factory=list)

    def __post_init__(self) -> None:
        if _COMMIT_RE.fullmatch(self.commit) is None:
            raise ValueError("commit 必须是 40 位小写十六进制 SHA")
        self.pdfinfo = _resolve_pdfinfo(self.pdfinfo)
        if self.deadline is not None and self.deadline <= 0:
            raise ValueError("deadline 必须是正数")

    def remaining(self, cap: Optional[float] = None) -> Optional[float]:
        if self.deadline is None:
            return cap
        remaining = self.deadline - self.monotonic()
        if remaining <= 0:
            raise RuntimeError("materialize 总 deadline 已到")
        return remaining if cap is None else min(remaining, cap)

    def check_deadline(self) -> None:
        self.remaining()

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


def git_tree(
    repo: Path, commit: str, context: Optional[FetchContext] = None
) -> List[Dict[str, str]]:
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
        timeout=(context.remaining() if context is not None else None),
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


def validate_pdfinfo_tool(
    value: Optional[Path], context: Optional[FetchContext] = None
) -> str:
    path = _resolve_pdfinfo(value)
    if not path.exists() or not path.is_file() or not os.access(str(path), os.X_OK):
        raise ValueError(f"pdfinfo 不存在、不是普通文件或不可执行：{path}")
    timeout = _HTTP_READ_DEADLINE
    if context is not None:
        timeout = context.remaining(_HTTP_READ_DEADLINE)
    try:
        completed = subprocess.run(
            [str(path), "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"pdfinfo -v 无法成功执行：{error}") from error
    if completed.returncode != 0:
        raise RuntimeError(f"pdfinfo -v 失败：{completed.returncode}")
    version_match = _PDFINFO_VERSION_RE.search(
        completed.stdout + "\n" + completed.stderr
    )
    if version_match is None or not version_match.group(1).strip():
        raise RuntimeError("pdfinfo -v 缺少版本号")
    return version_match.group(1).strip()


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


def inspect_pdf(
    path: Path,
    pdfinfo: Path,
    *,
    pdfinfo_version: Optional[str] = None,
    context: Optional[FetchContext] = None,
) -> Dict[str, Any]:
    path = Path(path)
    tool = _resolve_pdfinfo(pdfinfo)
    version = pdfinfo_version or validate_pdfinfo_tool(tool, context)
    timeout = _HTTP_READ_DEADLINE
    if context is not None:
        timeout = context.remaining(_HTTP_READ_DEADLINE)
    completed = subprocess.run(
        [str(tool), str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
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
        "pdfinfo_version": version,
    }


def _artifact_from_path(
    path: Path,
    source: Mapping[str, Any],
    pdfinfo: Path,
    *,
    pdfinfo_version: Optional[str] = None,
    context: Optional[FetchContext] = None,
) -> Dict[str, Any]:
    try:
        value = Path(path).read_bytes()
    except OSError as error:
        raise RuntimeError(f"无法读取 PDF：{path}: {error}") from error
    artifact = verify_fetched_bytes(source, value)
    artifact.update(inspect_pdf(
        path, pdfinfo, pdfinfo_version=pdfinfo_version, context=context
    ))
    return artifact


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(str(path), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class MaterializedArtifact(dict):
    def __init__(
        self, value: Mapping[str, Any], installed_identity: Optional[tuple] = None
    ) -> None:
        super().__init__(value)
        self.installed_identity = installed_identity


@contextmanager
def _directory_lock(path: Path) -> Iterator[None]:
    descriptor = os.open(
        str(path), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    )
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _target_temp_pattern(target: Path) -> re.Pattern:
    return re.compile(
        r"^\." + re.escape(target.name)
        + r"\.gaokao-materialize-[0-9a-f]{32}\.tmp$"
    )


def _clean_target_orphans(target: Path) -> None:
    pattern = _target_temp_pattern(target)
    for entry in target.parent.iterdir():
        if pattern.fullmatch(entry.name) is None:
            continue
        try:
            status = entry.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISREG(status.st_mode):
            entry.unlink()
    _fsync_directory(target.parent)


def _write_verified_cache(
    cache_path: Path,
    source: Mapping[str, Any],
    value: bytes,
    pdfinfo: Path,
    *,
    context: Optional[FetchContext] = None,
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
        _artifact_from_path(
            temporary, source, pdfinfo,
            pdfinfo_version=context.pdfinfo_version if context else None,
            context=context,
        )
        os.replace(str(temporary), str(cache_path))
        _fsync_directory(cache_path.parent)
        return cache_path
    finally:
        temporary.unlink(missing_ok=True)


def _verified_cache(
    cache_path: Path,
    source: Mapping[str, Any],
    pdfinfo: Path,
    context: Optional[FetchContext] = None,
) -> bool:
    if not cache_path.exists() and not cache_path.is_symlink():
        return False
    try:
        if not stat.S_ISREG(cache_path.lstat().st_mode):
            raise RuntimeError("cache 不是普通文件")
        _artifact_from_path(
            cache_path, source, pdfinfo,
            pdfinfo_version=context.pdfinfo_version if context else None,
            context=context,
        )
        return True
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError):
        cache_path.unlink(missing_ok=True)
        return False


def cache_directory(
    repo: Path, context: Optional[FetchContext] = None
) -> Path:
    repo = Path(repo)
    completed = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-dir"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
        timeout=(context.remaining() if context is not None else None),
    )
    git_dir = Path(completed.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = repo / git_dir
    return git_dir.resolve() / "gaokao-pdf-cache"


def _git_cat_file(
    repo: Path, oid: str, context: Optional[FetchContext] = None
) -> bytes:
    environment = os.environ.copy()
    environment.pop("GIT_NO_LAZY_FETCH", None)
    timeout = _HTTP_READ_DEADLINE
    if context is not None:
        timeout = context.remaining(_HTTP_READ_DEADLINE)
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", oid],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        env=environment,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"git cat-file 失败：{message or completed.returncode}")
    return completed.stdout


def _git_has_blob(
    repo: Path, oid: str, context: Optional[FetchContext] = None
) -> bool:
    environment = os.environ.copy()
    environment["GIT_NO_LAZY_FETCH"] = "1"
    completed = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", oid + "^{blob}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=environment,
        timeout=(context.remaining() if context is not None else None),
    )
    return completed.returncode == 0


def _set_http_read_timeout(response: Any, seconds: float) -> None:
    candidates = [response]
    for attributes in (("fp", "raw", "_sock"), ("fp", "_sock"), ("_sock",)):
        node = response
        try:
            for attribute in attributes:
                node = getattr(node, attribute)
        except AttributeError:
            continue
        candidates.append(node)
    for candidate in candidates:
        setter = getattr(candidate, "settimeout", None)
        if callable(setter):
            setter(max(0.001, seconds))
            return


def _download_http_to(
    url: str, destination: Path, limit: int, context: FetchContext
) -> None:
    destination = Path(destination)
    context.check_deadline()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)
    request = urllib.request.Request(
        url, headers={"User-Agent": "gaokao-latex-source-materializer/1"}
    )
    total = 0
    declared: Optional[int] = None
    try:
        connect_timeout = context.remaining(context.http_timeout)
        with urllib.request.urlopen(request, timeout=connect_timeout) as response:
            context.check_deadline()
            read_started = context.monotonic()
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
                    remaining_read = (
                        context.read_deadline_seconds
                        - (context.monotonic() - read_started)
                    )
                    if remaining_read <= 0:
                        raise RuntimeError("HTTP 单次读取 deadline 已到")
                    context.check_deadline()
                    socket_timeout = context.remaining(remaining_read)
                    assert socket_timeout is not None
                    _set_http_read_timeout(response, socket_timeout)
                    try:
                        chunk = response.read(1024 * 1024)
                    except (TimeoutError, socket.timeout) as error:
                        raise RuntimeError("HTTP 单次读取 deadline 已到") from error
                    context.check_deadline()
                    if context.monotonic() - read_started >= context.read_deadline_seconds:
                        raise RuntimeError("HTTP 单次读取 deadline 已到")
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > limit:
                        raise RuntimeError(f"HTTP 响应超过限制 {limit} bytes")
                    handle.write(chunk)
                handle.flush()
                durable_fsync(handle.fileno())
            if declared is not None and total != declared:
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
    zip_path: Path,
    member_name: str,
    limit: int = _RAW_LIMIT,
    *,
    context: Optional[FetchContext] = None,
) -> bytes:
    zip_path = Path(zip_path).resolve()
    expected = _normalized_zip_name(member_name)
    try:
        with zipfile.ZipFile(str(zip_path)) as archive:
            if (
                context is not None
                and context.zip_path == zip_path
                and context.zip_infos is not None
            ):
                infos = context.zip_infos
            else:
                infos = _validated_zip_infos(archive)
                if context is not None:
                    context.zip_path = zip_path
                    context.zip_infos = infos
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


def _validate_zip_for_context(
    zip_path: Path, context: FetchContext
) -> Dict[str, zipfile.ZipInfo]:
    resolved = Path(zip_path).resolve()
    if context.zip_path == resolved and context.zip_infos is not None:
        return context.zip_infos
    try:
        with zipfile.ZipFile(str(resolved)) as archive:
            infos = _validated_zip_infos(archive)
    except zipfile.BadZipFile as error:
        raise RuntimeError(f"ZIP 结构损坏：{resolved}") from error
    context.zip_path = resolved
    context.zip_infos = infos
    return infos


def _ensure_codeload_zip(
    cache_dir: Path, context: FetchContext
) -> Path:
    zip_path = cache_dir / (context.commit + ".zip")
    cache_dir.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        try:
            _validate_zip_for_context(zip_path, context)
            return zip_path
        except (OSError, RuntimeError):
            context.zip_path = None
            context.zip_infos = None
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
        context.zip_path = None
        context.zip_infos = None
        _validate_zip_for_context(temporary, context)
        os.replace(str(temporary), str(zip_path))
        _fsync_directory(cache_dir)
        context.zip_path = zip_path.resolve()
        return zip_path
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
    value = safe_zip_member_bytes(
        zip_path, member, context.raw_limit, context=context
    )
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
        return _write_verified_cache(
            cache_path, source, value, context.pdfinfo, context=context
        )
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
    if _verified_cache(cache_path, source, context.pdfinfo, context):
        return cache_path

    errors = []
    for delay in _GIT_BACKOFFS:
        context.check_deadline()
        try:
            value = _git_cat_file(repo, oid, context)
            return _write_verified_cache(
                cache_path, source, value, context.pdfinfo, context=context
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
    *,
    pdfinfo_version: Optional[str] = None,
    context: Optional[FetchContext] = None,
) -> Dict[str, Any]:
    candidate = Path(candidate)
    target = Path(target)
    _artifact_from_path(
        candidate, source, pdfinfo,
        pdfinfo_version=pdfinfo_version, context=context,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    with _directory_lock(target.parent):
        _clean_target_orphans(target)
        current = inspect_existing(target, str(source["git_blob_oid"]))
        if current == "mismatched":
            raise RuntimeError(
                f"已有文件与固定 blob 不一致，拒绝覆盖：{target}"
            )
        if current == "matching":
            return _artifact_from_path(
                target, source, pdfinfo,
                pdfinfo_version=pdfinfo_version, context=context,
            )
        temporary = target.with_name(
            ".%s.gaokao-materialize-%s.tmp" % (target.name, uuid.uuid4().hex)
        )
        descriptor = os.open(
            str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        try:
            with candidate.open("rb") as source_handle, os.fdopen(
                descriptor, "wb"
            ) as target_handle:
                shutil.copyfileobj(source_handle, target_handle, length=1024 * 1024)
                target_handle.flush()
                durable_fsync(target_handle.fileno())
            artifact = _artifact_from_path(
                temporary, source, pdfinfo,
                pdfinfo_version=pdfinfo_version, context=context,
            )
            try:
                os.link(str(temporary), str(target))
            except FileExistsError:
                state = inspect_existing(target, str(source["git_blob_oid"]))
                if state != "matching":
                    raise RuntimeError(
                        f"已有文件与固定 blob 不一致，拒绝覆盖：{target}"
                    )
                return _artifact_from_path(
                    target, source, pdfinfo,
                    pdfinfo_version=pdfinfo_version, context=context,
                )
            _fsync_directory(target.parent)
            installed = target.stat()
            return MaterializedArtifact(
                artifact, (installed.st_dev, installed.st_ino)
            )
        finally:
            temporary.unlink(missing_ok=True)


def materialize_source(
    source: Mapping[str, Any],
    *,
    target: Path,
    fetcher: Callable[[Mapping[str, Any]], Any],
    pdfinfo: Optional[Path] = None,
    context: Optional[FetchContext] = None,
) -> Dict[str, Any]:
    target = Path(target)
    tool = _resolve_pdfinfo(pdfinfo)
    target.parent.mkdir(parents=True, exist_ok=True)
    with _directory_lock(target.parent):
        _clean_target_orphans(target)
    state = inspect_existing(target, str(source.get("git_blob_oid", "")))
    if state == "mismatched":
        raise RuntimeError(f"已有文件与固定 blob 不一致，拒绝覆盖：{target}")
    if state == "matching":
        with _directory_lock(target.parent):
            _clean_target_orphans(target)
            return _artifact_from_path(
                target, source, tool,
                pdfinfo_version=context.pdfinfo_version if context else None,
                context=context,
            )

    fetched = fetcher(source)
    if isinstance(fetched, bytes):
        verify_fetched_bytes(source, fetched)
        with tempfile.TemporaryDirectory() as temporary_dir:
            candidate = Path(temporary_dir) / "candidate.pdf"
            candidate.write_bytes(fetched)
            return _copy_verified_target(
                candidate, source, target, tool,
                pdfinfo_version=context.pdfinfo_version if context else None,
                context=context,
            )
    candidate = Path(fetched)
    return _copy_verified_target(
        candidate, source, target, tool,
        pdfinfo_version=context.pdfinfo_version if context else None,
        context=context,
    )


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
        if (
            source.get("source_state") == "ready"
            and source.get("artifact") is not None
        ):
            result["artifacts"] += 1
    return result


def probe_transports(
    repo: Path,
    commit: str,
    pdfinfo: Optional[Path] = None,
    context: Optional[FetchContext] = None,
) -> Dict[str, Any]:
    repo = Path(repo)
    tool = _resolve_pdfinfo(pdfinfo)
    if context is None:
        context = FetchContext(commit=commit, pdfinfo=tool)
    context.check_deadline()
    entries = git_tree(repo, commit, context=context)
    sources = []
    for entry in entries:
        source = _source_from_entry(entry, "https://github.com/deekur/gaokaomath", commit)
        if source is not None:
            sources.append(source)
    cache_dir = cache_directory(repo, context=context)
    first_missing = None
    used_cache = False
    for source in sources:
        oid = str(source["git_blob_oid"])
        if _git_has_blob(repo, oid, context):
            continue
        cache_path = cache_dir / (oid + ".pdf")
        if _verified_cache(cache_path, source, tool, context):
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

    oid = str(first_missing["git_blob_oid"])
    cache_path = cache_dir / (oid + ".pdf")
    errors = []
    try:
        value = _git_cat_file(repo, oid, context)
        _write_verified_cache(
            cache_path, first_missing, value, tool, context=context
        )
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


def validate_source_state(
    source: Mapping[str, Any], known_papers: Any
) -> None:
    """校验单条来源的状态、artifact 与试卷关系耦合是否自洽。"""
    if not isinstance(source, Mapping):
        raise ValueError("manifest source 必须是对象")
    identifier = source.get("source_id", "<unknown>")
    state = source.get("source_state")
    if state not in SOURCE_STATES:
        raise ValueError(f"{identifier}: 未知 source_state：{state}")
    artifact = source.get("artifact")
    if (state == "ready") != (artifact is not None):
        raise ValueError(
            f"{identifier}: ready 当且仅当包含完整 artifact；"
            f"{state} 状态 artifact 必须为 null"
        )
    relation = source.get("paper_relation")
    paper_id = source.get("paper_id")
    if relation is not None:
        # 只有已验证 artifact 的来源才能承载确认关系。
        if state != "ready":
            raise ValueError(f"{identifier}: {state} 不得携带确认关系")
        if relation not in PAPER_RELATIONS:
            raise ValueError(f"{identifier}: 未知 paper_relation：{relation}")
        if paper_id is None:
            raise ValueError(f"{identifier}: paper_relation 存在但 paper_id 为空")
    if state == "non_paper" and paper_id is not None:
        raise ValueError(f"{identifier}: non_paper 不得绑定试卷")
    if paper_id is not None and paper_id not in known_papers:
        raise ValueError(f"{identifier}: paper_id 不存在：{paper_id}")


def _known_paper_ids(value: Mapping[str, Any]) -> set:
    papers = value.get("papers")
    if not isinstance(papers, list):
        raise ValueError("manifest papers 必须是数组")
    return set(
        paper.get("paper_id") for paper in papers if isinstance(paper, Mapping)
    )


def _validate_source_artifact_semantics(value: Mapping[str, Any]) -> None:
    sources = value.get("sources")
    if not isinstance(sources, list):
        raise ValueError("manifest sources 必须是数组")
    known_papers = _known_paper_ids(value)
    for source in sources:
        validate_source_state(source, known_papers)


def _validate_sorted_unique_paths(label: str, paths: Sequence[Any]) -> None:
    if list(paths) != sorted(paths) or len(set(paths)) != len(paths):
        raise ValueError(f"{label} 必须按 path 唯一排序")


def _validate_paper_semantics(value: Mapping[str, Any]) -> None:
    """校验 papers/batches 的跨字段不变量（Schema 之外的部分）。"""
    papers = value.get("papers")
    batches = value.get("batches")
    if not isinstance(papers, list) or not isinstance(batches, list):
        raise ValueError("manifest 的 papers/batches 必须是数组")

    known_papers = set()
    for paper in papers:
        if not isinstance(paper, Mapping):
            raise ValueError("manifest paper 必须是对象")
        paper_id = paper.get("paper_id")
        known_papers.add(paper_id)
        # Schema 允许 legacy_ids 为空（阶段 1 起新转录的卷本就没有旧 ID，编一个即伪造
        # 历史身份）；迁移卷的身份约束改由这里定向机检，比 minItems 更严也更准。
        if paper_id in _LEGACY_IDS_BY_PAPER:
            if list(paper.get("legacy_ids") or []) != _LEGACY_IDS_BY_PAPER[paper_id]:
                raise ValueError(f"{paper_id}: legacy_ids 与冻结常量表不一致")
        validate_index_metadata(
            paper_id,
            paper.get("question_count"),
            paper.get("index_metadata"),
            required=(
                not paper.get("legacy_ids")
                and paper.get("production_state") != "legacy_unverified"
            ),
        )
        source_files = paper.get("source_files")
        if not isinstance(source_files, Mapping) or set(source_files) != set(
            SOURCE_FILE_KEYS
        ):
            raise ValueError(f"{paper_id}: source_files 必须恰好包含四个键")
        values = list(source_files.values())
        if len(set(values)) != len(values):
            raise ValueError(f"{paper_id}: source_files 路径必须唯一")
        figures = paper.get("figure_files")
        if not isinstance(figures, list) or any(
            not isinstance(figure, Mapping) for figure in figures
        ):
            raise ValueError(f"{paper_id}: figure_files 必须是对象数组")
        _validate_sorted_unique_paths(
            f"{paper_id}: figure_files", [figure.get("path") for figure in figures]
        )
        prefix = "%s/figures/" % paper.get("project_dir")
        for figure in figures:
            if not str(figure.get("path")).startswith(prefix):
                raise ValueError(f"{paper_id}: figure_files 必须位于本卷 figures 目录")
            occurrences = figure.get("expected_occurrences")
            if (
                isinstance(occurrences, bool)
                or not isinstance(occurrences, int)
                or occurrences < 1
            ):
                raise ValueError(f"{paper_id}: expected_occurrences 必须是正整数")
        legacy_files = paper.get("legacy_source_files")
        if not isinstance(legacy_files, list) or any(
            not isinstance(item, Mapping) for item in legacy_files
        ):
            raise ValueError(f"{paper_id}: legacy_source_files 必须是对象数组")
        _validate_sorted_unique_paths(
            f"{paper_id}: legacy_source_files",
            [item.get("path") for item in legacy_files],
        )

    batch_ids = set()
    batched_papers = set()
    for batch in batches:
        if not isinstance(batch, Mapping):
            raise ValueError("manifest batch 必须是对象")
        batch_id = batch.get("batch_id")
        if batch_id in batch_ids:
            raise ValueError(f"batch_id 不唯一：{batch_id}")
        batch_ids.add(batch_id)
        paper_ids = batch.get("paper_ids")
        if not isinstance(paper_ids, list):
            raise ValueError(f"{batch_id}: paper_ids 必须是数组")
        for paper_id in paper_ids:
            if paper_id not in known_papers:
                raise ValueError(f"{batch_id}: paper_id 不存在：{paper_id}")
            if paper_id in batched_papers:
                raise ValueError(f"{batch_id}: paper_id 属于多个批次：{paper_id}")
            batched_papers.add(paper_id)


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
    _validate_source_artifact_semantics(value)
    _validate_paper_semantics(value)


# 对外别名：`provenance.confirm-source` 在提交绑定前必须跑同一套四层校验
# （Schema + manifest 语义 + 来源语义 + 试卷语义）。**不复制、只借用**——校验少跑一层，
# 「绑定成功」就可能是一份自己都过不了 `load-*` 的 manifest。
validate_manifest_document = _validated_manifest_value


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


class StateTransactionError(RuntimeError):
    def __init__(self, transaction_id: str, cause: BaseException) -> None:
        super().__init__(str(cause))
        self.transaction_id = transaction_id
        self.cause = cause


def state_source_result(
    repo: Path,
    manifest_path: Path,
    issues_path: Path,
    source_id_value: str,
    *,
    artifact: Optional[Mapping[str, Any]],
    issue_type: Optional[str] = None,
    evidence: str = "固定 blob、SHA-256、PDF 文件头和 pdfinfo 已验证",
) -> str:
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
            source["artifact"] = None
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
        try:
            transaction.prepare(
                "state", targets, inputs={}, expected_revision=revision
            )
            transaction.commit()
        except BaseException as error:
            try:
                setattr(error, "transaction_id", transaction.transaction_id)
                setattr(error, "expected_manifest", copy.deepcopy(manifest))
                setattr(error, "expected_issues", ledger_bytes)
            except BaseException:
                raise StateTransactionError(transaction.transaction_id, error) from error
            raise
        return transaction.transaction_id


def _state_postconditions_match(
    manifest_path: Path,
    issues_path: Path,
    transaction_id: str,
    expected_manifest: Any,
    expected_issues: Any,
) -> bool:
    if not isinstance(expected_manifest, Mapping) or not isinstance(
        expected_issues, bytes
    ):
        return False
    current = _load_json(manifest_path)
    return (
        current.get("last_transaction_id") == transaction_id
        and current == expected_manifest
        and issues_path.read_bytes() == expected_issues
    )


def _state_result_with_recovery(
    repo: Path,
    manifest_path: Path,
    issues_path: Path,
    source_id_value: str,
    *,
    artifact: Optional[Mapping[str, Any]],
    issue_type: Optional[str] = None,
    evidence: str = "固定 blob、SHA-256、PDF 文件头和 pdfinfo 已验证",
) -> str:
    try:
        return state_source_result(
            repo, manifest_path, issues_path, source_id_value,
            artifact=artifact, issue_type=issue_type, evidence=evidence,
        )
    except BaseException as original:
        transaction_id = getattr(original, "transaction_id", None)
        expected_manifest = getattr(original, "expected_manifest", None)
        expected_issues = getattr(original, "expected_issues", None)
        if not isinstance(transaction_id, str):
            raise
        try:
            with RepoLock(repo):
                pass
        except BaseException:
            raise
        if _state_postconditions_match(
            manifest_path, issues_path, transaction_id,
            expected_manifest, expected_issues,
        ):
            return transaction_id
        raise


def _restore_new_target(
    target: Path, expected_oid: str, installed_identity: Optional[tuple]
) -> None:
    if installed_identity is None:
        return
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with _directory_lock(target.parent):
        try:
            status = target.lstat()
        except FileNotFoundError:
            return
        if (status.st_dev, status.st_ino) != installed_identity:
            return
        if inspect_existing(target, expected_oid) == "matching":
            target.unlink()
            _fsync_directory(target.parent)


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
        if isinstance(source, Mapping)
        and source.get("source_state") == "ready"
        and source.get("artifact") is not None
    )
    if require_artifacts is not None and count != require_artifacts:
        raise ValueError(
            f"artifact 数量不符：期望 {require_artifacts}，实际 {count}"
        )
    return count


def _read_repo_text(repo_root: Path, relative: str) -> str:
    path = Path(repo_root) / relative
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"无法读取迁移输入：{relative}: {error}") from error


def _ordered_reference_counts(
    texts: Sequence[str], pattern: Any
) -> tuple:
    """按首次出现顺序统计引用，返回 (顺序列表, 计数字典)。"""
    order: List[str] = []
    counts: Dict[str, int] = {}
    for text in texts:
        for match in pattern.finditer(text):
            key = match.group(1)
            if key not in counts:
                order.append(key)
                counts[key] = 0
            counts[key] += 1
    return order, counts


def _figure_files(
    repo_root: Path,
    project_dir: str,
    figure_names: Sequence[str],
    source_files: Mapping[str, str],
) -> List[Dict[str, Any]]:
    """把 legacy figure tree 迁成带引用次数的登记表。

    次数取自当前规范 Markdown——内容迁移后它才是图引用的唯一事实源；哪一张图对应
    哪一次引用由 legacy TeX 的引用**顺序**定位。两者的**图数**不一致时立即失败，
    不猜测配对；**逐图次数不再与 legacy TeX 比对**（理由见函数体内注释），live 树的
    防丢图职责改由 `validate_figure_occurrences()` 对 manifest 登记值承担。
    """
    if any(not str(name).endswith(".tex") for name in figure_names):
        raise ValueError(f"{project_dir}: figure 登记必须全部是 .tex")
    # 无图卷（figure_files 为空）不要求 figures 目录存在：早期卷（如 1952）纯文字题，
    # 没有任何配图，figures/ 目录根本不该被创建。
    if not figure_names:
        return []
    figure_dir = Path(repo_root) / PROJECT_RELATIVE / project_dir / "figures"
    try:
        actual = sorted(item.name for item in figure_dir.iterdir() if item.is_file())
    except OSError as error:
        raise ValueError(f"{project_dir}: 无法列出 figures 目录：{error}") from error
    if actual != list(figure_names):
        raise ValueError(f"{project_dir}: figures 目录与 legacy index 登记不一致")

    stems = [str(name)[: -len(".tex")] for name in figure_names]
    source_texts = [
        (key, source_files[key], _read_repo_text(repo_root, source_files[key]))
        for key in FIGURE_COUNT_SOURCE_KEYS
    ]
    image_order, image_counts = _ordered_reference_counts(
        [text for _, _, text in source_texts], _MARKDOWN_IMAGE_RE
    )

    # 新稿可直接链接到本卷已登记的 TikZ 源。此模式不依赖尚未生成的
    # questions.tex/answers.tex；相对链接按各自 Markdown 文件所在目录解析。
    direct_links = []
    inline_tex_links = []
    for key, source_path, text in source_texts:
        standalone = list(_MARKDOWN_TEX_FIGURE_LINK_RE.finditer(text))
        standalone_tex = []
        for match in standalone:
            target = match.group(1)
            parsed = urllib.parse.urlsplit(urllib.parse.unquote(target))
            if not parsed.scheme and not parsed.netloc and parsed.path.lower().endswith(".tex"):
                standalone_tex.append((source_path, target))
        for match in _MARKDOWN_LINK_ANY_RE.finditer(text):
            target = match.group(1)
            parsed = urllib.parse.urlsplit(urllib.parse.unquote(target))
            if not parsed.scheme and not parsed.netloc and parsed.path.lower().endswith(".tex"):
                inline_tex_links.append((source_path, target))
        direct_links.extend(standalone_tex)

    if len(inline_tex_links) != len(direct_links):
        raise ValueError(f"{project_dir}: 图稿链接必须独立成段")

    if direct_links:
        if image_order:
            raise ValueError(
                f"{project_dir}: 图稿链接与旧式 Markdown 图片不能混用"
            )
        registered = {
            "%s/%s/figures/%s" % (PROJECT_RELATIVE, project_dir, name):
            "%s/figures/%s" % (project_dir, name)
            for name in figure_names
        }
        link_counts: Dict[str, int] = {}
        for source_path, target in direct_links:
            parsed = urllib.parse.urlsplit(urllib.parse.unquote(target))
            if (
                parsed.scheme or parsed.netloc or parsed.query or parsed.fragment
                or not parsed.path or parsed.path.startswith("/")
            ):
                raise ValueError(
                    f"{project_dir}: 图稿链接必须是本卷 figures/*.tex 的相对路径：{target}"
                )
            resolved = posixpath.normpath(
                posixpath.join(posixpath.dirname(source_path), parsed.path)
            )
            if resolved not in registered:
                raise ValueError(
                    f"{project_dir}: 图稿链接指向未登记的本卷图稿：{target}"
                )
            link_counts[resolved] = link_counts.get(resolved, 0) + 1
        if set(link_counts) != set(registered):
            raise ValueError(f"{project_dir}: 图稿链接与 figure 登记不一致")
        return [
            {"path": relative, "expected_occurrences": link_counts[repo_path]}
            for repo_path, relative in sorted(registered.items())
        ]

    tex_order, _ = _ordered_reference_counts(
        [
            _read_repo_text(
                repo_root, "%s/%s/%s" % (PROJECT_RELATIVE, project_dir, name)
            )
            for name in ("questions.tex", "answers.tex")
        ],
        _FIGURE_INPUT_RE,
    )
    if sorted(tex_order) != sorted(stems):
        raise ValueError(f"{project_dir}: 存在未引用或未登记的 figure")

    if len(image_order) != len(tex_order):
        raise ValueError(
            "%s: 规范 Markdown 图片数 %d 与登记 figure 数 %d 不一致"
            % (project_dir, len(image_order), len(tex_order))
        )
    # 次数**只**取自规范 Markdown：内容迁移（T6/T7）之后规范 Markdown 才是图引用的
    # 唯一事实源，legacy TeX 成了滞后派生物（T13 重生成 editions 时追平）。
    # 曾经的「Markdown 计数 == legacy TeX 计数」硬断言只对**冻结迁移态**成立——
    # 它在 f2018wen_t19_grid 上恰好成立于「旧 _含解析.md 用占位符丢了那张图」这个
    # bug 之上，迁移修掉 bug 后等式即破。该等式已移到 test_legacy_migration.py 的
    # git 锚点测试里（钉在迁移前的树上），live 树的防丢图职责改由
    # validate_figure_occurrences() 对 manifest 登记值承担。
    records = [
        {
            "path": "%s/figures/%s.tex" % (project_dir, stem),
            "expected_occurrences": image_counts[image],
        }
        for stem, image in zip(tex_order, image_order)
    ]
    records.sort(key=lambda item: item["path"])
    return records


def _registered_figure_occurrences(
    repo_root: Path, paper: Mapping[str, Any]
) -> Dict[str, int]:
    """按 manifest 里这一卷的登记，重新数一遍规范 Markdown 的图引用次数。"""
    project_dir = str(paper.get("project_dir"))
    figure_names = [
        PurePosixPath(str(figure.get("path"))).name
        for figure in paper.get("figure_files", [])
    ]
    records = _figure_files(
        repo_root, project_dir, figure_names, paper.get("source_files", {})
    )
    return {record["path"]: record["expected_occurrences"] for record in records}


def validate_figure_occurrences(
    manifest: Mapping[str, Any], repo_root: Path
) -> int:
    """live 树主守卫：规范 Markdown 的图引用数必须等于 manifest 登记的次数。

    内容迁移后 legacy TeX 不再有资格给 live 树对账（见 `_figure_files` 注释），
    改由 manifest 承担登记职责。**任何未经登记的漂移都硬错，两个方向都拦**：
    少一次是静默丢图（本项目反复出现的那类失败：占位符顶掉真内容），
    多一次是重复插图。要改次数只能走 `state_figure_occurrences()` 的正规事务，
    不许改代码或手编 JSON 绕过。返回核对过的 figure 总数。
    """
    papers = manifest.get("papers")
    if not isinstance(papers, list):
        raise ValueError("manifest papers 必须是数组")
    total = 0
    for paper in papers:
        if not isinstance(paper, Mapping):
            raise ValueError("manifest paper 必须是对象")
        paper_id = paper.get("paper_id")
        actual = _registered_figure_occurrences(repo_root, paper)
        for figure in paper.get("figure_files", []):
            path = str(figure.get("path"))
            registered = figure.get("expected_occurrences")
            if path not in actual:
                raise ValueError(f"{paper_id}: figure 登记与实际不匹配：{path}")
            if actual[path] != registered:
                raise ValueError(
                    "%s: %s 引用次数与 manifest 登记不一致：规范 Markdown %d，登记 %d"
                    % (paper_id, path, actual[path], registered)
                )
            total += 1
        if len(actual) != len(paper.get("figure_files", [])):
            raise ValueError(f"{paper_id}: figure 登记数与实际数不一致")
    return total


def _without_figure_occurrences(manifest: Mapping[str, Any]) -> Dict[str, Any]:
    """抹掉全部 expected_occurrences，用来自证「窄入口只改了这一个字段」。"""
    scrubbed = copy.deepcopy(dict(manifest))
    for paper in scrubbed.get("papers", []):
        for figure in paper.get("figure_files", []):
            figure.pop("expected_occurrences", None)
    return scrubbed


def state_figure_occurrences(repo: Path, manifest_path: Path) -> Optional[str]:
    """把 manifest 的 expected_occurrences 对齐到规范 Markdown 的实际引用数。

    这是**唯一**允许改写 expected_occurrences 的正规路径：RepoLock + Task 1
    `state` 事务 + revision 递增，绝不手编 JSON。内容迁移会合法地改变图引用数
    （例如题面从 `**题目**：见试题。` 占位还原成真实题面，把图一并带回），此时登记值
    必须随之推进，否则 `validate_figure_occurrences()` 会一直红。

    **窄入口**：只允许 expected_occurrences 变化，出现任何其他字段差异一律拒绝提交，
    以免它被当成通用 manifest 改写器绕过 migrate-legacy-index 的覆盖保护。
    已对齐时返回 None（不开事务）。
    """
    root = _repository_root(Path(repo))
    manifest_path = Path(manifest_path)
    manifest_relative = _relative_to_repo(root, manifest_path)
    if manifest_relative != MANIFEST_TARGET:
        raise ValueError(
            f"state manifest 必须是 {MANIFEST_TARGET}，实际 {manifest_relative}"
        )
    with RepoLock(root):
        manifest = _load_json(manifest_path)
        revision = manifest.get("revision")
        if type(revision) is not int or revision < 0:
            raise ValueError("manifest revision 必须是非负整数")
        updated = copy.deepcopy(manifest)
        papers = updated.get("papers")
        if not isinstance(papers, list):
            raise ValueError("manifest papers 必须是数组")
        for paper in papers:
            actual = _registered_figure_occurrences(root, paper)
            for figure in paper.get("figure_files", []):
                path = str(figure.get("path"))
                if path not in actual:
                    raise ValueError(
                        "%s: figure 登记与实际不匹配：%s"
                        % (paper.get("paper_id"), path)
                    )
                figure["expected_occurrences"] = actual[path]
        if updated == manifest:
            return None
        if _without_figure_occurrences(updated) != _without_figure_occurrences(
            manifest
        ):
            raise ValueError(
                "本入口只允许改写 expected_occurrences，检测到其他字段变化"
            )
        transaction = Transaction(root)
        updated["revision"] = revision + 1
        updated["last_transaction_id"] = transaction.transaction_id
        _validated_manifest_value(manifest_path, updated)
        targets = {MANIFEST_TARGET: canonical_json(updated).encode("utf-8")}
        transaction.prepare(
            "state", targets, inputs={}, expected_revision=revision
        )
        transaction.commit()
        return transaction.transaction_id


def _legacy_paper_metadata(legacy_index: Any) -> Dict[str, Mapping[str, Any]]:
    papers = legacy_index.get("papers") if isinstance(legacy_index, Mapping) else None
    if not isinstance(papers, list) or any(
        not isinstance(paper, Mapping) for paper in papers
    ):
        raise ValueError("legacy index papers 必须是对象数组")
    metadata: Dict[str, Mapping[str, Any]] = {}
    for paper in papers:
        legacy_id = paper.get("id")
        if not isinstance(legacy_id, str) or legacy_id in metadata:
            raise ValueError(f"legacy index 旧 ID 缺失或重复：{legacy_id!r}")
        metadata[legacy_id] = paper
    expected = set(entry.legacy_id for entry in LEGACY_PAPERS)
    if set(metadata) != expected:
        raise ValueError(
            "legacy index 旧 ID 必须与常量表逐字一致：缺 %s，多 %s"
            % (sorted(expected - set(metadata)), sorted(set(metadata) - expected))
        )
    return metadata


def verify_phase0_issue_seeds(issues: Sequence[Mapping[str, Any]]) -> None:
    """确认 Task 2 建立的两条身份问题**身份**没有漂移；status 允许合法推进。

    校验的是身份四元组 `type/paper_id/affected_paper_ids/conflict_code`——对这两条问题
    来说它恰好就是 `issue_fingerprint()` 取的那组字段——外加 fingerprint 必须与身份重算
    一致。**不校验 status 停在 open**：`open → resolved` 是业务生命周期（T17 逐卷核验
    后收口 ISSUE-0002），不是漂移。把状态钉死会让「这条种子问题被解决了」与「这条种子
    问题被人换掉了」在报错上不可区分，而本函数要拦的是后者。

    仍然 fail-closed 的两条：编号必须在、身份必须逐字相同；**且尚未了结时必须仍是
    `blocks_completion`**——把一条没解决的身份问题降级成 non_blocking，等于在不解决它
    的前提下解除封锁，那是绕过而不是推进。
    """
    by_id: Dict[Any, Mapping[str, Any]] = {}
    for issue in issues:
        issue_id = issue.get("issue_id")
        if issue_id in by_id:
            raise ValueError(f"重复问题编号：{issue_id}")
        by_id[issue_id] = issue
    for seed in PHASE0_ISSUE_SEEDS:
        issue = by_id.get(seed["issue_id"])
        if issue is None:
            raise ValueError(f"缺少种子问题：{seed['issue_id']}")
        for field_name in ("type", "paper_id", "affected_paper_ids", "conflict_code"):
            if issue.get(field_name) != seed[field_name]:
                raise ValueError(
                    "%s: %s 已漂移：期望 %r，实际 %r"
                    % (seed["issue_id"], field_name, seed[field_name],
                       issue.get(field_name))
                )
        if issue.get("fingerprint") != issue_fingerprint(issue):
            raise ValueError(f"{seed['issue_id']}: fingerprint 与身份字段不一致")
        if issue.get("impact") not in ISSUE_IMPACTS:
            raise ValueError(
                "%s: 未知 impact：%r" % (seed["issue_id"], issue.get("impact"))
            )
        if (
            issue.get("status") != "resolved"
            and issue.get("impact") != "blocks_completion"
        ):
            raise ValueError(
                f"{seed['issue_id']}: 尚未了结的身份问题必须保持 blocks_completion"
            )


def _issue_ids_by_paper(
    issues: Sequence[Mapping[str, Any]], known_papers: Any
) -> Dict[str, List[str]]:
    result: Dict[str, set] = {}
    for issue in issues:
        if issue.get("status") == "resolved":
            continue
        targets = list(issue.get("affected_paper_ids") or [])
        if issue.get("paper_id") is not None:
            targets.append(issue["paper_id"])
        for target in targets:
            if target not in known_papers:
                raise ValueError(
                    f"{issue.get('issue_id')}: 引用未知 paper_id：{target}"
                )
            result.setdefault(target, set()).add(issue["issue_id"])
    return {key: sorted(value) for key, value in result.items()}


def _paper_record(
    entry: LegacyPaper,
    legacy: Mapping[str, Any],
    repo_root: Path,
    issue_ids: Sequence[str],
) -> Dict[str, Any]:
    project_dir = legacy.get("dir")
    title = legacy.get("title")
    year = legacy.get("year")
    question_count = legacy.get("questions")
    figure_names = legacy.get("figures")
    if not isinstance(project_dir, str) or not project_dir:
        raise ValueError(f"{entry.legacy_id}: legacy index 缺少 dir")
    if not isinstance(title, str) or not title:
        raise ValueError(f"{entry.legacy_id}: legacy index 缺少 title")
    if isinstance(year, bool) or not isinstance(year, int):
        raise ValueError(f"{entry.legacy_id}: legacy index 缺少 year")
    if (
        isinstance(question_count, bool)
        or not isinstance(question_count, int)
        or question_count < 1
    ):
        raise ValueError(f"{entry.legacy_id}: legacy index questions 必须是正整数")
    if not isinstance(figure_names, list):
        raise ValueError(f"{entry.legacy_id}: legacy index figures 必须是数组")
    legacy_track = legacy.get("track")
    if legacy_track not in TRACK_BY_LEGACY:
        raise ValueError(f"{entry.legacy_id}: 未知 legacy track：{legacy_track!r}")
    if TRACK_BY_LEGACY[legacy_track] != entry.track:
        raise ValueError(f"{entry.legacy_id}: legacy track 与常量表不一致")

    source_files = {
        key: entry.markdown_prefix + MARKDOWN_SUFFIXES[key]
        for key in SOURCE_FILE_KEYS
    }
    for key in REQUIRED_SOURCE_FILE_KEYS:
        if not (Path(repo_root) / source_files[key]).is_file():
            raise ValueError(
                f"{entry.paper_id}: 规范 Markdown 缺失：{source_files[key]}"
            )
    legacy_source_files: List[Dict[str, Any]] = []
    if entry.paper_id == RECALL_PAPER_ID:
        if source_files["questions"] != RECALL_LEGACY_SOURCE:
            raise ValueError("回忆版 legacy 规范源路径与常量不一致")
        legacy_source_files = [{
            "path": RECALL_LEGACY_SOURCE,
            "sha256": file_sha256(Path(repo_root) / RECALL_LEGACY_SOURCE),
        }]
    return {
        "paper_id": entry.paper_id,
        "legacy_ids": [entry.legacy_id],
        "project_dir": project_dir,
        "title": title,
        "year": year,
        "track": entry.track,
        "question_count": question_count,
        "source_files": source_files,
        "figure_files": _figure_files(
            repo_root, project_dir, figure_names, source_files
        ),
        "legacy_source_files": legacy_source_files,
        # 阶段 0 不建立上游绑定；回忆版更必须保持空集直到身份问题裁决。
        "source_ids": [],
        "production_state": "legacy_unverified",
        "issue_ids": list(issue_ids),
        # blocked 摘要三字段由 Task 15 derive_status() 填写，迁移时一律为 null。
        "blocked_from": None,
        "last_verified_hash": None,
        "resume_action": None,
    }


def migrate_legacy_index(
    manifest: Mapping[str, Any],
    legacy_index: Mapping[str, Any],
    *,
    repo_root: Path,
    issues: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    """把 21 套 legacy 试卷迁入 manifest；返回新 manifest，不写盘。"""
    if not isinstance(manifest, Mapping):
        raise ValueError("manifest 必须是对象")
    metadata = _legacy_paper_metadata(legacy_index)
    verify_phase0_issue_seeds(issues)
    known_papers = set(entry.paper_id for entry in LEGACY_PAPERS)
    issue_ids = _issue_ids_by_paper(issues, known_papers)
    papers = [
        _paper_record(
            entry, metadata[entry.legacy_id], repo_root,
            issue_ids.get(entry.paper_id, []),
        )
        for entry in LEGACY_PAPERS
    ]
    batches = [
        {
            "batch_id": batch_id,
            "paper_ids": list(paper_ids),
            "status": "planned",
            "issues": [],
        }
        for batch_id, paper_ids in PHASE0_BATCHES
    ]

    migrated = copy.deepcopy(dict(manifest))
    # 已迁移的 manifest 只允许逐字重放；状态已推进时拒绝回退成 legacy_unverified。
    if migrated.get("papers") and migrated["papers"] != papers:
        raise ValueError("现有 manifest papers 与迁移结果不一致，拒绝覆盖")
    if migrated.get("batches") and migrated["batches"] != batches:
        raise ValueError("现有 manifest batches 与迁移结果不一致，拒绝覆盖")
    migrated["papers"] = papers
    migrated["batches"] = batches
    validate_manifest_semantics(migrated)
    _validate_paper_semantics(migrated)
    return migrated


def _registered_paper_record(
    repo_root: Path, entry: Mapping[str, Any], known: Mapping[str, Mapping[str, Any]]
) -> Dict[str, Any]:
    """把一条注册规格折成 paper 记录；一切字段都必须是对已有产物的事实登记。"""
    paper_id = entry.get("paper_id")
    if not isinstance(paper_id, str) or not re.match(r"^gk-[0-9]{4}-[a-z0-9-]+$", paper_id):
        raise ValueError(f"paper_id 不合式样：{paper_id!r}")
    prefix = entry.get("markdown_prefix")
    if not isinstance(prefix, str) or not prefix.startswith(""):
        raise ValueError(f"{paper_id}: markdown_prefix 必须是  下的路径前缀")
    question_count = entry.get("question_count")
    if (
        isinstance(question_count, bool)
        or not isinstance(question_count, int)
        or question_count < 1
    ):
        raise ValueError(f"{paper_id}: question_count 必须是正整数")
    project_dir = entry.get("project_dir")
    if not isinstance(project_dir, str) or "/" in project_dir or not project_dir:
        raise ValueError(f"{paper_id}: project_dir 必须是单层目录名")
    track = entry.get("track")
    if track not in ("science", "arts", "none"):
        raise ValueError(f"{paper_id}: 未知 track：{track!r}")

    index_metadata = entry.get("index_metadata")
    validate_index_metadata(paper_id, question_count, index_metadata, required=True)

    source_files = {
        key: prefix + MARKDOWN_SUFFIXES[key] for key in SOURCE_FILE_KEYS
    }
    # solution_body 按既有约定只登记路径；其余三份是转录成果，必须已在盘上。
    for key in REQUIRED_SOURCE_FILE_KEYS:
        if not (Path(repo_root) / source_files[key]).is_file():
            raise ValueError(f"{paper_id}: 规范 Markdown 缺失：{source_files[key]}")

    source_ids = list(entry.get("source_ids") or [])
    for value in source_ids:
        source = known.get(value)
        if source is None:
            raise ValueError(f"{paper_id}: 来源不存在：{value}")
        if source.get("paper_id") is not None:
            raise ValueError(
                "%s: 来源 %s 已绑定 %s" % (paper_id, value, source["paper_id"])
            )
    return {
        "paper_id": paper_id,
        # 新转录的卷没有旧 ID；编一个即伪造历史身份，一律留空。
        "legacy_ids": [],
        "project_dir": project_dir,
        "title": entry.get("title"),
        "year": entry.get("year"),
        "track": track,
        "question_count": question_count,
        "index_metadata": copy.deepcopy(dict(index_metadata)),
        "source_files": source_files,
        "figure_files": list(entry.get("figure_files") or []),
        "legacy_source_files": [],
        "source_ids": source_ids,
        "production_state": "planned",
        "issue_ids": [],
        "blocked_from": None,
        "last_verified_hash": None,
        "resume_action": None,
    }


def _prepare_registration_question_issues(
    repo_root: Path,
    entries: Sequence[Mapping[str, Any]],
    records: Sequence[MutableMapping[str, Any]],
) -> tuple[Optional[bytes], Dict[str, List[str]], Dict[str, List[str]]]:
    """Validate and serialize optional question blockers without touching the repo."""
    specs_by_paper: Dict[str, List[Mapping[str, Any]]] = {}
    allowed_fields = {
        "kind", "question_id", "source_id", "current_evidence", "resume_action",
    }
    for entry, record in zip(entries, records):
        raw_specs = entry.get("question_issues", [])
        if not isinstance(raw_specs, list):
            raise ValueError(f"{record['paper_id']}: question_issues 必须是数组")
        checked: List[Mapping[str, Any]] = []
        seen = set()
        for item in raw_specs:
            if not isinstance(item, Mapping):
                raise ValueError(f"{record['paper_id']}: question_issue 必须是对象")
            if set(item) != allowed_fields:
                raise ValueError(
                    f"{record['paper_id']}: question_issue 字段必须恰好为 "
                    + ", ".join(sorted(allowed_fields))
                )
            question_id = item.get("question_id")
            match = (
                re.fullmatch(
                    re.escape(record["paper_id"]) + r"-q([1-9][0-9]*)",
                    question_id,
                )
                if isinstance(question_id, str) else None
            )
            if match is None or int(match.group(1)) > record["question_count"]:
                raise ValueError(
                    f"{record['paper_id']}: question_id 不属于登记卷或题号越界："
                    f"{question_id!r}"
                )
            source_id_value = item.get("source_id")
            if source_id_value not in record["source_ids"]:
                raise ValueError(
                    f"{record['paper_id']}: 问题来源未绑定到该卷：{source_id_value!r}"
                )
            kind = item.get("kind")
            identity = (question_id, source_id_value, kind)
            if identity in seen:
                raise ValueError(f"{record['paper_id']}: 重复逐题问题：{identity}")
            seen.add(identity)
            for field_name in ("current_evidence", "resume_action"):
                value = item.get(field_name)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(
                        f"{record['paper_id']}: {field_name} 必须是非空字符串"
                    )
            checked.append(item)
        specs_by_paper[record["paper_id"]] = checked

    if not any(specs_by_paper.values()):
        return None, {}, {}

    issue_path = Path(repo_root) / ISSUES_TARGET
    prior_bytes = issue_path.read_bytes() if issue_path.is_file() else None
    issue_ids_by_paper: Dict[str, List[str]] = {}
    resume_actions_by_paper: Dict[str, List[str]] = {}
    with tempfile.TemporaryDirectory(prefix="gaokao-register-issues-") as scratch:
        scratch_path = Path(scratch) / "missing-issues.md"
        if prior_bytes is not None:
            scratch_path.write_bytes(prior_bytes)
        for record in records:
            paper_id = record["paper_id"]
            for item in specs_by_paper.get(paper_id, []):
                issue = question_issue(
                    paper_id=paper_id,
                    question_id=item["question_id"],
                    source_id=item["source_id"],
                    kind=item["kind"],
                    resume_action=item["resume_action"],
                )
                issue["current_evidence"] = item["current_evidence"].strip()
                issue_id = upsert_issue(scratch_path, issue)
                issue_ids_by_paper.setdefault(paper_id, []).append(issue_id)
                resume_actions_by_paper.setdefault(paper_id, []).append(
                    item["resume_action"].strip()
                )
        return (
            scratch_path.read_bytes(),
            {paper_id: sorted(set(issue_ids))
             for paper_id, issue_ids in issue_ids_by_paper.items()},
            resume_actions_by_paper,
        )


def register_papers(
    repo: Path,
    manifest_path: Path,
    spec: Mapping[str, Any],
    *,
    write: bool = False,
) -> Dict[str, Any]:
    """把未绑定来源、paper/batch 记录及可选逐题 blocker 纳入一个 state 事务。

    这是阶段 1 起新增试卷的**唯一**写入口：阶段 0 的 21 套由 `migrate_legacy_index()`
    从冻结常量一次性种入且拒绝覆盖，此前没有任何通路能新建一套卷。

    `write=False` 时不写仓库，只把计划算出来给人看；`write=True` 时 paper 记录、
    批次记录、来源反向绑定和可选问题总账在**同一个** state 事务里落盘。
    """
    root = _repository_root(Path(repo))
    manifest_path = Path(manifest_path)
    if _relative_to_repo(root, manifest_path) != MANIFEST_TARGET:
        raise ValueError(f"manifest 必须是 {MANIFEST_TARGET}")
    if not isinstance(spec, Mapping):
        raise ValueError("注册规格必须是对象")
    batch_id = spec.get("batch_id")
    if not isinstance(batch_id, str) or not re.match(r"^phase[0-9]+-b[0-9]{2}$", batch_id):
        raise ValueError(f"batch_id 不合式样：{batch_id!r}")
    entries = spec.get("papers")
    if not isinstance(entries, list) or not entries:
        raise ValueError("注册规格的 papers 必须是非空数组")

    with RepoLock(root):
        manifest = _load_json(manifest_path)
        revision = manifest.get("revision")
        if type(revision) is not int or revision < 0:
            raise ValueError("manifest revision 必须是非负整数")
        if any(
            batch.get("batch_id") == batch_id for batch in manifest.get("batches", [])
        ):
            raise ValueError(f"batch_id 已存在：{batch_id}")
        known_sources = {
            source["source_id"]: source
            for source in manifest.get("sources", [])
            if isinstance(source, MutableMapping)
        }
        existing_papers = {
            paper.get("paper_id"): paper for paper in manifest.get("papers", [])
        }
        existing_dirs = {
            paper.get("project_dir") for paper in manifest.get("papers", [])
        }

        records = []
        for entry in entries:
            if not isinstance(entry, Mapping):
                raise ValueError("注册规格的 paper 必须是对象")
            record = _registered_paper_record(root, entry, known_sources)
            if record["paper_id"] in existing_papers:
                raise ValueError(f"paper_id 已存在：{record['paper_id']}")
            if record["project_dir"] in existing_dirs:
                raise ValueError(f"project_dir 已存在：{record['project_dir']}")
            existing_papers[record["paper_id"]] = record
            existing_dirs.add(record["project_dir"])
            records.append(record)

        issue_bytes, issue_ids_by_paper, resume_actions_by_paper = (
            _prepare_registration_question_issues(root, entries, records)
        )
        for record in records:
            issue_ids = issue_ids_by_paper.get(record["paper_id"], [])
            if issue_ids:
                record["production_state"] = "blocked"
                record["issue_ids"] = issue_ids
                record["blocked_from"] = "planned"
                record["resume_action"] = "；".join(
                    dict.fromkeys(resume_actions_by_paper[record["paper_id"]])
                )

        paper_ids = [record["paper_id"] for record in records]
        report = {
            "code": "OK", "batch_id": batch_id, "paper_ids": paper_ids,
            "issue_ids": issue_ids_by_paper,
            "written": False, "revision": revision,
        }
        if not write:
            return report

        manifest["papers"] = list(manifest.get("papers", [])) + records
        manifest["batches"] = list(manifest.get("batches", [])) + [{
            "batch_id": batch_id, "paper_ids": list(paper_ids),
            "status": "planned", "issues": [],
        }]
        for record in records:
            for value in record["source_ids"]:
                bound = known_sources[value]
                bound["paper_id"] = record["paper_id"]
                bound["paper_relation"] = "canonical"

        transaction = Transaction(root)
        manifest["revision"] = revision + 1
        manifest["last_transaction_id"] = transaction.transaction_id
        _validated_manifest_value(manifest_path, manifest)
        validate_manifest_semantics(manifest)
        _validate_paper_semantics(manifest)
        targets = {}
        if issue_bytes is not None:
            targets[ISSUES_TARGET] = issue_bytes
        targets[MANIFEST_TARGET] = canonical_json(manifest).encode("utf-8")
        transaction.prepare(
            "state",
            targets,
            inputs={},
            expected_revision=revision,
        )
        transaction.commit()
        report["written"] = True
        report["revision"] = revision + 1
        return report


def project_legacy_index(
    manifest: Mapping[str, Any], legacy_index: Mapping[str, Any]
) -> Dict[str, Any]:
    """把 manifest 身份投影回兼容 index.json：**只增静态身份** paper_id/legacy_ids。

    ⚠️ 这里刻意**不投影任何运行态**（`batches` 段、`production_state`、`issue_ids`）。
    原因是 index.json 落在 build 回执的 `generation_input_tree` 里：把批次状态投影进来，
    每推进一次批次状态就会改动 index.json 的字节，于是要么 `generate_projects --check`
    当场失配、要么 21 份回执连锁 stale——推进状态与「保持已编译产物当前」变成互斥的
    两件事。运行态的唯一住处是 manifest 本身。
    """
    by_legacy: Dict[str, Mapping[str, Any]] = {}
    by_paper_id = project_index(manifest)
    for paper in by_paper_id.values():
        for legacy_id in paper.get("legacy_ids", []):
            if legacy_id in by_legacy:
                raise ValueError(f"manifest legacy_ids 重复：{legacy_id}")
            by_legacy[legacy_id] = paper
    projected = copy.deepcopy(dict(legacy_index))
    entries = projected.get("papers")
    if not isinstance(entries, list):
        raise ValueError("legacy index papers 必须是数组")
    for entry in entries:
        if not isinstance(entry, MutableMapping):
            raise ValueError("legacy index paper 必须是对象")
        legacy_id = entry.get("id")
        paper = by_legacy.get(legacy_id)
        if paper is None and isinstance(legacy_id, str):
            paper = by_paper_id.get(legacy_id)
        if paper is None:
            raise ValueError(f"manifest 未覆盖 index ID：{legacy_id!r}")
        entry["paper_id"] = paper["paper_id"]
        entry["legacy_ids"] = list(paper["legacy_ids"])
    projected.pop("batches", None)
    return projected


def _migrate_legacy_index_command(arguments: argparse.Namespace) -> int:
    manifest_path = Path(arguments.manifest)
    legacy_index_path = Path(arguments.legacy_index)
    issues_path = Path(arguments.issues)
    output_manifest_path = Path(arguments.output_manifest)
    output_index_path = Path(arguments.output_index)
    root = _repository_root(manifest_path.parent)
    manifest_relative = _relative_to_repo(root, output_manifest_path)
    index_relative = _relative_to_repo(root, output_index_path)
    issues_relative = _relative_to_repo(root, issues_path)
    # 三个 tracked 目标全部钉死在规范路径：既不许把投影写到任意仓库文件，
    # 也不许用非规范的问题总账副本去推导 paper 的 issue_ids。
    for relative, expected, option in (
        (manifest_relative, MANIFEST_TARGET, "--output-manifest"),
        (index_relative, INDEX_TARGET, "--output-index"),
        (issues_relative, ISSUES_TARGET, "--issues"),
    ):
        if relative != expected:
            raise ValueError(f"{option} 必须是 {expected}，实际 {relative}")
    # targets 是以路径为键的字典：任意两个目标同名都会静默吞掉一次写入，
    # 而 transaction.py 的 manifest 唯一性检查看不到被字典去重掉的那一个。
    relatives = [index_relative, issues_relative, manifest_relative]
    if len(set(relatives)) != len(relatives):
        raise ValueError(f"事务目标路径必须两两不同：{relatives}")

    with RepoLock(root):
        manifest = _load_json(manifest_path)
        revision = manifest.get("revision")
        if type(revision) is not int or revision < 0:
            raise ValueError("manifest revision 必须是非负整数")
        legacy_index = _load_json(legacy_index_path)
        issues = load_issues(issues_path)
        migrated = migrate_legacy_index(
            manifest, legacy_index, repo_root=root, issues=issues
        )
        index_bytes = canonical_json(
            project_legacy_index(migrated, legacy_index)
        ).encode("utf-8")
        # 两条种子问题只被验证，不被改写；随事务一起提交以固定它们的字节。
        issues_bytes = issues_path.read_bytes()
        if (
            migrated == manifest
            and output_manifest_path.read_bytes() == canonical_json(
                migrated
            ).encode("utf-8")
            and output_index_path.is_file()
            and output_index_path.read_bytes() == index_bytes
        ):
            return 0

        transaction = Transaction(root)
        migrated["revision"] = revision + 1
        migrated["last_transaction_id"] = transaction.transaction_id
        _validated_manifest_value(manifest_path, migrated)
        targets = {
            index_relative: index_bytes,
            issues_relative: issues_bytes,
            MANIFEST_TARGET: canonical_json(migrated).encode("utf-8"),
        }
        transaction.prepare(
            "state", targets, inputs={}, expected_revision=revision
        )
        transaction.commit()
        return 0


def _materialize_command(arguments: argparse.Namespace) -> int:
    started = time.monotonic()
    deadline = started + arguments.deadline_seconds
    if arguments.jobs != 1:
        raise ValueError("阶段 0 materialize 要求 --jobs 1")
    manifest_path = Path(arguments.manifest)
    issues_path = Path(arguments.issues)
    manifest = _load_json(manifest_path)
    _validate_source_artifact_semantics(manifest)
    upstream = manifest.get("upstream")
    if not isinstance(upstream, Mapping):
        raise ValueError("manifest 缺少 upstream")
    commit = upstream.get("commit")
    if not isinstance(commit, str) or _COMMIT_RE.fullmatch(commit) is None:
        raise ValueError("manifest upstream.commit 无效")

    context = FetchContext(
        commit=commit,
        pdfinfo=arguments.pdfinfo,
        deadline=deadline,
        monotonic=time.monotonic,
    )
    # Tool/environment validation is global and precedes transport/cache/tracked writes.
    context.pdfinfo_version = validate_pdfinfo_tool(arguments.pdfinfo, context)
    # Preflight shares the command-entry deadline and remains before tracked writes.
    probe_transports(
        arguments.repo, commit, arguments.pdfinfo, context=context
    )
    context.check_deadline()

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
            if isinstance(source, Mapping)
            and source.get("source_state") != "ready"
            and source.get("artifact") is None
        ]

    upstream_cache = cache_directory(arguments.repo, context=context)
    project_repo = _repository_root(manifest_path.parent)
    failed = False
    for index, source in enumerate(selected):
        if time.monotonic() >= deadline:
            for unfinished in selected[index:]:
                _state_result_with_recovery(
                    project_repo, manifest_path, issues_path,
                    str(unfinished["source_id"]), artifact=None,
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
                context=context,
            )
        except (OSError, RuntimeError, ValueError, subprocess.SubprocessError) as error:
            failed = True
            issue_type = "source-unavailable"
            message = str(error)
            if "已有文件与固定 blob 不一致" in message:
                issue_type = "source-mismatch"
            elif "pdfinfo" in message or "%PDF-" in message:
                issue_type = "source-unreadable"
            _state_result_with_recovery(
                project_repo, manifest_path, issues_path,
                str(source["source_id"]), artifact=None,
                issue_type=issue_type, evidence=message,
            )
            continue

        try:
            _state_result_with_recovery(
                project_repo, manifest_path, issues_path,
                str(source["source_id"]), artifact=artifact,
            )
        except BaseException:
            if not existed:
                _restore_new_target(
                    target,
                    str(source["git_blob_oid"]),
                    getattr(artifact, "installed_identity", None),
                )
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

    migrate = subparsers.add_parser("migrate-legacy-index")
    migrate.add_argument("--manifest", required=True, type=Path)
    migrate.add_argument("--legacy-index", required=True, type=Path)
    migrate.add_argument("--issues", required=True, type=Path)
    migrate.add_argument("--output-manifest", required=True, type=Path)
    migrate.add_argument("--output-index", required=True, type=Path)

    register = subparsers.add_parser("register-papers")
    register.add_argument("--repo", required=True, type=Path)
    register.add_argument("--manifest", required=True, type=Path)
    register.add_argument("--spec", required=True, type=Path)
    register.add_argument("--write", action="store_true")

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--manifest", required=True, type=Path)
    validate_parser.add_argument("--require-artifacts", type=_nonnegative)

    # 窄入口：内容迁移合法改变图引用数后，把登记值推进到规范 Markdown 的实际值。
    sync_figures = subparsers.add_parser("sync-figure-occurrences")
    sync_figures.add_argument("--manifest", required=True, type=Path)
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
    if arguments.command == "register-papers":
        report = register_papers(
            arguments.repo, arguments.manifest, _load_json(arguments.spec),
            write=arguments.write,
        )
        print("%s：%d 卷，%s" % (
            report["batch_id"], len(report["paper_ids"]),
            "已提交 revision %s" % report["revision"] if report["written"]
            else "仅校验，未落盘",
        ))
        return 0
    if arguments.command == "validate":
        validate_source_manifest(
            arguments.manifest, arguments.require_artifacts
        )
        # live 树防丢图主守卫：规范 Markdown 图引用数 == manifest 登记值。
        root = _repository_root(Path(arguments.manifest).parent)
        validate_figure_occurrences(_load_json(Path(arguments.manifest)), root)
        return 0
    if arguments.command == "sync-figure-occurrences":
        transaction_id = state_figure_occurrences(
            _repository_root(Path(arguments.manifest).parent), arguments.manifest
        )
        os.sys.stdout.write(
            "already-aligned\n" if transaction_id is None
            else "%s\n" % transaction_id
        )
        return 0
    if arguments.command == "migrate-legacy-index":
        return _migrate_legacy_index_command(arguments)
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

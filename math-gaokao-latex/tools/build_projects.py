#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_projects.py —— 严格 XeLaTeX 构建、实际依赖闭包、两阶段回执与安全清理。

**一份 build 回执的唯一价值是「可反驳」**：它必须能被后来的任何人用手上的字节重新
验算一遍，验算不过就降级为 stale。仓库里那 21 个项目根目录的旧 PDF 就是没有回执的
反面样本——文件在、内容老、任何机制都不得让它算数。

因此 currency 由四条独立证据共同背书，缺一即 stale：

1. `build_manifest_projection()` 的规范 JSON SHA-256——**只含静态装配字段**
   （见 `PROJECTION_FIELDS`）。manifest 的运行态（`revision`/`last_transaction_id`/
   batch 状态/paper `production_state`/`issue_ids`）刻意排除在外：每推进一次状态就让
   84 个目标全部 stale，等于逼着人不重编也宣称当前；
2. `generation_input_tree`——三份规范 Markdown、figure、index、四模板、四壳与**全部**
   生成器源码（含 `cli_common.py` 与 `md2tex.py`）。它守的是「规范源已改但 TeX 尚未
   重跑」这一格：`.fls` 只认 TeX 实际读到的文件，看不见上游 Markdown；
3. 两遍 `.fls` 的仓库内 INPUT 并集——第二遍才被 `\\input` 的文件只出现在第二遍的
   `.fls` 里，取并集才是真闭包；
4. `toolchain_fingerprint`——四个 executable 的解析后路径、规范化版本、真实二进制
   SHA-256 与 TeX Live 版本。版本认不出来时 fail closed，绝不写一份「未知版本」的回执。

状态机：`running → failed` / `running → compiled_pending_review → succeeded`。
0.4588pt 的 Overfull 也只能候选 `compiled_pending_review`——排版警告由 Task 24 的视觉
审查裁决，`finalize_receipt()` 只在逐项匹配后返回 `succeeded` 候选，自己不写盘。

formal 模式是**两个 state 事务**：先写 `running` 回执（进程被杀也留下痕迹，且永远不能
被当作 final），串行构建后再写结果回执 / issues / reconciled manifest。中间没有第三种
状态可以「顺便」被人当成成功。

四条证据**并列、没有开关**：`validate-receipts` 与 `cleanup_legacy()` 都无条件重算全部四条，
工具链解析不出来即 INVALID / 零删除。`--require-current-inputs` 保留为显式声明（Interfaces
冻结了它的存在），语义已并入默认校验、传不传结果一致——把工具链做成可选项就是 fail-open：
换了 TeX Live 的机器上旧回执照样绿。

退出码（`--json` 时调用方必须同时校验 `code`）：0 通过、2 usage、3 仅 `PENDING_REVIEW`、
4 invalid/failed/stale receipt 或门禁未过、5 `BUILD_FAILED`（诊断状态已保存）。
"""
from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent                       # math-gaokao-latex
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import cli_common
import issues as issues_module
import status as status_core
from manifest import atomic_write_json, canonical_json, file_sha256, load_manifest
from schema_validate import SchemaError
from schema_validate import validate as validate_schema
from status import (
    ISSUES_TARGET,
    MANIFEST_TARGET,
    PROJECT_RELATIVE,
    StatusError,
    build_receipt_path,
    derive_status,
    paper_facts,
    paper_ownership_paths,
    reconcile_batch_status,
)
from transaction import RepoLock, Transaction

INDEX_TARGET = PROJECT_RELATIVE + "/index.json"
SCHEMA_TARGET = PROJECT_RELATIVE + "/schemas/build-receipt.schema.json"
DEFAULT_MANIFEST = PROJECT_ROOT / "source-manifest.json"
DEFAULT_ISSUES = PROJECT_ROOT / "missing-issues.md"

EDITIONS: Tuple[str, ...] = ("试题版", "解析版", "简答版", "印刷版")
BUILD_DIR_NAME = "build"
RECEIPT_RELATIVE = status_core.BUILD_RECEIPT_NAME
REVIEW_RELATIVE = status_core.REVIEW_RECEIPT_NAME
PROVENANCE_RELATIVE = status_core.PROVENANCE_NAME

# 「全部生成器源码」逐条列全：漏一条就是溯源缺口——改了 cli_common.py 却让 84 份回执
# 继续宣称当前，正是 Task 14 抽取共享骨架后新增的那条缝。
GENERATOR_SOURCES: Tuple[str, ...] = (
    PROJECT_RELATIVE + "/tools/cli_common.py",
    PROJECT_RELATIVE + "/tools/generate_projects.py",
    PROJECT_RELATIVE + "/tools/make_editions.py",
    PROJECT_RELATIVE + "/tools/make_short_answers.py",
    PROJECT_RELATIVE + "/tools/solution_sources.py",
    "math-gaokao-2017-2026/tools/md2tex.py",
)
CANONICAL_SOURCE_KEYS: Tuple[str, ...] = ("answer_key", "questions", "solution_body")

# 生成器实际读取的静态装配字段，全集。运行态字段一个都不在这里。
PROJECTION_FIELDS: Tuple[str, ...] = (
    "figure_files", "legacy_ids", "paper_id", "project_dir", "question_count",
    "source_files", "title", "track", "year",
)

TOOL_NAMES: Tuple[str, ...] = ("pdfinfo", "pdftoppm", "pdftotext", "xelatex")
LEGACY_SUFFIXES: Tuple[str, ...] = (
    ".pdf", ".log", ".aux", ".out", ".toc", ".fls", ".xdv", ".synctex.gz",
)
_EXCLUDED_FLS_PARTS = frozenset([".git", ".work", BUILD_DIR_NAME])

STATUS_TRANSITIONS: Tuple[Tuple[str, str], ...] = (
    ("running", "failed"),
    ("running", "compiled_pending_review"),
    ("compiled_pending_review", "succeeded"),
)

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_PENDING_REVIEW = 3
EXIT_INVALID = 4
EXIT_BUILD_FAILED = 5

ISSUE_ORIGIN = "formal-build"
ISSUE_CHECK_CODE = "formal-build"


class BuildError(ValueError):
    """构建、回执与清理门禁的唯一异常类型。"""


class UsageError(BuildError):
    """调用方把命令写错了（未知项目目录/版本），与「数据有问题」区分开。

    退出码不同：usage 是 2，invalid/stale 是 4。混成一个会让 CI 分不清「命令写错」
    和「回执失效」——前者重打一遍就好，后者必须去查证据链。
    """


# ---------------------------------------------------------------- 小件


def _now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _repo_relative(path: Path) -> str:
    return PurePosixPath(path).as_posix()


def _assert_safe_relative(relative: str) -> str:
    candidate = PurePosixPath(relative)
    if candidate.is_absolute() or any(
        part in {"", ".", ".."} for part in candidate.parts
    ):
        raise BuildError(f"路径必须是安全的仓库相对路径：{relative}")
    return candidate.as_posix()


def _paper(manifest: Mapping[str, Any], paper_id: str) -> Mapping[str, Any]:
    for paper in manifest.get("papers", []):
        if paper["paper_id"] == paper_id:
            return paper
    raise BuildError(f"未知 paper_id：{paper_id}")


def _project_path(root: Path, paper: Mapping[str, Any]) -> Path:
    relative = _assert_safe_relative(
        "%s/%s" % (PROJECT_RELATIVE, paper["project_dir"])
    )
    return Path(root) / relative


def _read_text_lenient(path: Path) -> str:
    """TeX 的 log/fls 不保证是干净 UTF-8——解析失败绝不能把整次构建带走。"""
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def select_paper_ids(
    manifest: Mapping[str, Any], selector: str, value: Optional[str] = None
) -> Tuple[str, ...]:
    papers = [paper["paper_id"] for paper in manifest.get("papers", [])]
    if selector == "all":
        return tuple(papers)
    if selector == "paper":
        if value not in papers:
            raise BuildError(f"未知 paper_id：{value}")
        return (value,)
    if selector == "batch":
        found = [
            item for item in manifest.get("batches", []) if item["batch_id"] == value
        ]
        if len(found) != 1:
            raise BuildError(f"未知批次：{value}")
        for paper_id in found[0]["paper_ids"]:
            if paper_id not in papers:
                raise BuildError(f"批次 {value} 引用了不存在的 paper_id：{paper_id}")
        return tuple(found[0]["paper_ids"])
    raise BuildError(f"未知选择器：{selector}")


# ---------------------------------------------------------------- manifest 投影


def build_manifest_projection(
    manifest: Mapping[str, Any], paper_id: str
) -> Dict[str, Any]:
    """该卷参与 currency 的 manifest 切片：只有生成器真正读取的静态装配字段。"""
    paper = _paper(manifest, paper_id)
    missing = [field for field in PROJECTION_FIELDS if field not in paper]
    if missing:
        raise BuildError(f"{paper_id}: manifest 缺少静态装配字段 {missing}")
    projection = copy.deepcopy({field: paper[field] for field in PROJECTION_FIELDS})
    if paper.get("index_metadata") is not None:
        projection["index_metadata"] = copy.deepcopy(paper["index_metadata"])
    return projection


def projection_digest(manifest: Mapping[str, Any], paper_id: str) -> str:
    return _sha256_text(canonical_json(build_manifest_projection(manifest, paper_id)))


# ---------------------------------------------------------------- 文件树


def file_tree(root: Path, relatives: Sequence[str]) -> Dict[str, Any]:
    """一组仓库内输入的逐字节哈希；缺一个文件就是算不出来，绝不用 null 混过去。"""
    records: List[Dict[str, str]] = []
    for relative in sorted(set(_assert_safe_relative(item) for item in relatives)):
        path = Path(root) / relative
        if not path.is_file():
            raise BuildError(f"输入缺失：{relative}")
        records.append({"path": relative, "sha256": file_sha256(path)})
    return {"tree_sha256": _sha256_text(canonical_json(records)), "files": records}


def dependency_tree(root: Path, relatives: Sequence[str]) -> Dict[str, Any]:
    return file_tree(root, relatives)


def generation_input_paths(
    manifest: Mapping[str, Any], paper_id: str
) -> Tuple[str, ...]:
    paper = _paper(manifest, paper_id)
    directory = paper["project_dir"]
    paths = list(GENERATOR_SOURCES)
    for edition in EDITIONS:
        paths.append("%s/templates/%s.tex.tpl" % (PROJECT_RELATIVE, edition))
        paths.append("%s/%s/%s.tex" % (PROJECT_RELATIVE, directory, edition))
    for item in paper["figure_files"]:
        # figure_files.path 是 project-relative（Task 4 冻结），source_files 是 repo-relative。
        paths.append("%s/%s" % (PROJECT_RELATIVE, item["path"]))
    for key in CANONICAL_SOURCE_KEYS:
        paths.append(paper["source_files"][key])
    return tuple(sorted(set(paths)))


def generation_input_tree(
    root: Path, manifest: Mapping[str, Any], paper_id: str
) -> Dict[str, Any]:
    return file_tree(root, generation_input_paths(manifest, paper_id))


# ---------------------------------------------------------------- .fls 与日志


def parse_fls(text: str, root: Path) -> Tuple[str, ...]:
    """取 `.fls` 里落在仓库内的 INPUT，排除 `.git` / `build` / `.work`。

    相对路径按 `PWD` 行解析；没有 `PWD` 行就说明这份 `.fls` 不可信，直接失败——按 cwd
    猜一遍会把依赖闭包悄悄算错。
    """
    root_path = Path(root).resolve()
    pwd: Optional[Path] = None
    found = set()
    for line in text.splitlines():
        if line.startswith("PWD "):
            pwd = Path(line[4:].strip())
            continue
        if not line.startswith("INPUT "):
            continue
        if pwd is None:
            raise BuildError(".fls 在 INPUT 之前没有 PWD 行")
        raw = line[len("INPUT "):].strip()
        if not raw:
            continue
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = pwd / candidate
        try:
            resolved = Path(os.path.normpath(str(candidate))).resolve()
            relative = resolved.relative_to(root_path)
        except (OSError, ValueError):
            continue
        if any(part in _EXCLUDED_FLS_PARTS for part in relative.parts):
            continue
        found.add(relative.as_posix())
    if pwd is None:
        raise BuildError(".fls 缺少 PWD 行")
    return tuple(sorted(found))


_MISSING_CHARACTER = re.compile(r"^Missing character: ")
_UNDEFINED = re.compile(r"Warning: .*undefined", re.IGNORECASE)
_BOX_WARNING = re.compile(r"^(Overfull|Underfull) \\(hbox|vbox) \(([^)]*)\)")
_BOX_WIDTH = re.compile(r"^([0-9]+(?:\.[0-9]+)?)pt too ")
_BOX_LINES = re.compile(r"at lines ([0-9]+--[0-9]+)|at line ([0-9]+)")
_FILE_LINE_ERROR = re.compile(r"^\S.*?:[0-9]+: .*(?:Error|Emergency|Fatal)")


def scan_log(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """把 log 折成四个桶。警告不等于失败——它们是 Task 24 视觉审查的输入。"""
    found: Dict[str, List[Dict[str, Any]]] = {
        "missing_characters": [], "undefined_references": [], "overfull": [],
        "errors": [],
    }
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            continue
        if _MISSING_CHARACTER.search(line):
            found["missing_characters"].append({"text": line})
            continue
        if _UNDEFINED.search(line):
            found["undefined_references"].append({"text": line})
            continue
        box = _BOX_WARNING.match(line)
        if box is not None:
            width = _BOX_WIDTH.match(box.group(3))
            lines = _BOX_LINES.search(line)
            found["overfull"].append({
                "kind": box.group(1),
                "box": box.group(2),
                "width_pt": width.group(1) if width is not None else None,
                "lines": (lines.group(1) or lines.group(2)) if lines else None,
                "text": line,
            })
            continue
        if line.startswith("!") or _FILE_LINE_ERROR.match(line):
            found["errors"].append({"text": line})
    return found


def _merge_findings(
    left: Mapping[str, List[Dict[str, Any]]],
    right: Mapping[str, List[Dict[str, Any]]],
) -> Dict[str, List[Dict[str, Any]]]:
    merged: Dict[str, List[Dict[str, Any]]] = {}
    for key in ("missing_characters", "undefined_references", "overfull", "errors"):
        seen = []
        for item in list(left.get(key, [])) + list(right.get(key, [])):
            if item not in seen:
                seen.append(item)
        merged[key] = seen
    return merged


# ---------------------------------------------------------------- 工具链指纹


_VERSION_FLAG = {
    "xelatex": "--version", "pdfinfo": "-v", "pdftotext": "-v", "pdftoppm": "-v",
}
_VERSION_PATTERN = {
    "xelatex": re.compile(r"^XeTeX \S+"),
    "pdfinfo": re.compile(r"^pdfinfo version \S+"),
    "pdftotext": re.compile(r"^pdftotext version \S+"),
    "pdftoppm": re.compile(r"^pdftoppm version \S+"),
}
_TEXLIVE_PATTERN = re.compile(r"\((TeX Live [^)]+)\)")


def _tool_version(name: str, path: str) -> str:
    result = subprocess.run(
        [path, _VERSION_FLAG[name]],
        cwd=str(Path(path).parent), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        raise BuildError(
            "%s %s 退出码 %d，无法识别版本" % (name, _VERSION_FLAG[name], result.returncode)
        )
    text = result.stdout.decode("utf-8", errors="replace")
    for raw in text.splitlines():
        line = " ".join(raw.split())
        if _VERSION_PATTERN[name].match(line):
            return line
    raise BuildError(f"{name} 的版本输出无法识别，拒绝写入回执")


def resolve_toolchain(search_path: Optional[str] = None) -> Dict[str, Any]:
    """四个实际 executable 的指纹。任一环节说不清就 fail closed，不生成伪回执。"""
    tools: List[Dict[str, str]] = []
    texlive_revision: Optional[str] = None
    for name in TOOL_NAMES:
        located = shutil.which(name, path=search_path)
        if located is None:
            raise BuildError(f"找不到工具：{name}")
        path = str(Path(located).absolute())
        real_path = os.path.realpath(path)
        if not Path(real_path).is_file():
            raise BuildError(f"{name} 解析后不是普通文件：{real_path}")
        version = _tool_version(name, path)
        if name == "xelatex":
            found = _TEXLIVE_PATTERN.search(version)
            if found is None:
                raise BuildError("xelatex 版本串里没有 TeX Live 版本，拒绝写入回执")
            texlive_revision = found.group(1)
        tools.append({
            "name": name,
            "path": path,
            "real_path": real_path,
            "sha256": file_sha256(Path(real_path)),
            "version": version,
        })
    if texlive_revision is None:
        raise BuildError("未能确定 TeX Live 版本")
    return {"texlive_revision": texlive_revision, "tools": tools}


def _tool(toolchain: Mapping[str, Any], name: str) -> str:
    for item in toolchain["tools"]:
        if item["name"] == name:
            return item["path"]
    raise BuildError(f"工具链指纹里没有 {name}")


# ---------------------------------------------------------------- 单目标构建


def build_target(
    root: Path,
    project_dir: str,
    edition: str,
    toolchain: Mapping[str, Any],
    runner: Optional[Callable[..., Any]] = None,
) -> Dict[str, Any]:
    """两遍 XeLaTeX + pdfinfo，只写 `<project>/build/`。

    返回 `{"record": <回执 edition 段>, "dependencies": (...)}`。argv 是冻结的：
    `-halt-on-error` 让第一遍就炸的目标不必空跑第二遍，`-no-shell-escape` 关掉外部命令，
    `-recorder` 才有 `.fls`。全部走参数数组 + `cwd=`，没有 shell。
    """
    if edition not in EDITIONS:
        raise BuildError(f"未知版本：{edition}")
    call = runner or subprocess.run
    project_path = Path(root) / PROJECT_RELATIVE / project_dir
    source = "%s/%s/%s.tex" % (PROJECT_RELATIVE, project_dir, edition)
    if not (Path(root) / source).is_file():
        raise BuildError(f"版本壳不存在：{source}")
    build_dir = project_path / BUILD_DIR_NAME
    build_dir.mkdir(parents=True, exist_ok=True)

    argv = [
        _tool(toolchain, "xelatex"), "-interaction=nonstopmode", "-halt-on-error",
        "-file-line-error", "-no-shell-escape", "-recorder",
        "-output-directory=%s" % BUILD_DIR_NAME, "%s.tex" % edition,
    ]
    passes: List[Dict[str, int]] = []
    problems: List[str] = []
    findings: Dict[str, List[Dict[str, Any]]] = {
        "missing_characters": [], "undefined_references": [], "overfull": [],
        "errors": [],
    }
    dependencies: set = set()
    for index in (1, 2):
        result = call(
            argv, cwd=str(project_path), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        code = int(result.returncode)
        passes.append({"pass": index, "exit_code": code})
        findings = _merge_findings(
            findings, scan_log(_read_text_lenient(build_dir / (edition + ".log")))
        )
        fls_text = _read_text_lenient(build_dir / (edition + ".fls"))
        if fls_text:
            try:
                dependencies.update(parse_fls(fls_text, root))
            except BuildError as error:
                problems.append("第 %d 遍的 .fls 无法解析：%s" % (index, error))
        if code != 0:
            problems.append("第 %d 遍 XeLaTeX 退出码 %d" % (index, code))
            break

    pdf_record: Optional[Dict[str, Any]] = None
    if not problems:
        pdf_path = build_dir / (edition + ".pdf")
        if not pdf_path.is_file():
            problems.append("两遍都通过但没有产出 PDF")
        else:
            pages = _pdf_pages(toolchain, pdf_path, problems)
            if pages is not None:
                pdf_record = {
                    "path": _repo_relative(pdf_path.relative_to(Path(root))),
                    "sha256": file_sha256(pdf_path),
                    "size_bytes": pdf_path.stat().st_size,
                    "page_count": pages,
                }
        if not dependencies:
            problems.append("两遍都通过但没有可用的 .fls 依赖闭包")

    record = {
        "edition": edition,
        "source": source,
        "result": "failed" if problems else "succeeded",
        "passes": passes,
        "pdf": pdf_record,
        "log": findings,
        "problems": problems,
    }
    return {"record": record, "dependencies": tuple(sorted(dependencies))}


def _pdf_pages(
    toolchain: Mapping[str, Any], pdf_path: Path, problems: List[str]
) -> Optional[int]:
    result = subprocess.run(
        [_tool(toolchain, "pdfinfo"), str(pdf_path)],
        cwd=str(pdf_path.parent), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        problems.append("pdfinfo 退出码 %d" % result.returncode)
        return None
    for raw in result.stdout.decode("utf-8", errors="replace").splitlines():
        if raw.startswith("Pages:"):
            try:
                pages = int(raw.split(":", 1)[1].strip())
            except ValueError:
                break
            if pages > 0:
                return pages
            break
    problems.append("pdfinfo 没有给出可用的页数")
    return None


# ---------------------------------------------------------------- 回执


def _receipt_skeleton(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    toolchain: Mapping[str, Any],
    attempt_id: str,
    previous_attempt_id: Optional[str],
    started_at: str,
) -> Dict[str, Any]:
    paper = _paper(manifest, paper_id)
    return {
        "schema_version": 1,
        "paper_id": paper_id,
        "project_dir": paper["project_dir"],
        "attempt_id": attempt_id,
        "previous_attempt_id": previous_attempt_id,
        "started_at": started_at,
        "finished_at": None,
        "status": "running",
        "input_projection": projection_digest(manifest, paper_id),
        "manifest_revision": int(manifest["revision"]),
        "toolchain_fingerprint": copy.deepcopy(dict(toolchain)),
        "generation_input_tree": generation_input_tree(root, manifest, paper_id),
        "dependency_tree": None,
        "editions": [],
    }


def running_receipt(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    toolchain: Mapping[str, Any],
    existing: Optional[Mapping[str, Any]] = None,
    started_at: Optional[str] = None,
) -> Dict[str, Any]:
    """开工回执。中断留下的 `running` 是**证据**，不是垃圾：它让「没跑完」可被机器识别。

    重跑时若上一份也是 `running` 且三项输入（投影 / 生成输入树 / 工具链）逐字节相同，
    就**复用**同一个 attempt——那确实是同一次尝试的续跑；否则**替换**，并把旧 attempt
    记进 `previous_attempt_id`，不假装它没发生过。
    """
    attempt_id = str(uuid.uuid4())
    previous: Optional[str] = None
    receipt = _receipt_skeleton(
        root, manifest, paper_id, toolchain, attempt_id, previous,
        started_at or _now(),
    )
    if existing is not None:
        same_inputs = (
            existing.get("input_projection") == receipt["input_projection"]
            and (existing.get("generation_input_tree") or {}).get("tree_sha256")
            == receipt["generation_input_tree"]["tree_sha256"]
            and existing.get("toolchain_fingerprint") == receipt["toolchain_fingerprint"]
        )
        if existing.get("status") == "running" and same_inputs:
            receipt["attempt_id"] = existing["attempt_id"]
            receipt["previous_attempt_id"] = existing.get("previous_attempt_id")
            receipt["started_at"] = existing["started_at"]
        else:
            receipt["previous_attempt_id"] = existing.get("attempt_id")
    validate_receipt(receipt)
    return receipt


def build_paper_result(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    toolchain: Mapping[str, Any],
    runner: Optional[Callable[..., Any]] = None,
    attempt_id: Optional[str] = None,
    previous_attempt_id: Optional[str] = None,
    started_at: Optional[str] = None,
) -> Dict[str, Any]:
    """一卷四版本的完整构建结果；任一版本失败则整卷 `failed`，其余版本照编不误。"""
    paper = _paper(manifest, paper_id)
    receipt = _receipt_skeleton(
        root, manifest, paper_id, toolchain,
        attempt_id or str(uuid.uuid4()), previous_attempt_id, started_at or _now(),
    )
    dependencies: set = set()
    records: List[Dict[str, Any]] = []
    for edition in EDITIONS:
        outcome = build_target(
            root, paper["project_dir"], edition, toolchain, runner=runner
        )
        records.append(outcome["record"])
        dependencies.update(outcome["dependencies"])
    receipt["editions"] = records
    receipt["dependency_tree"] = dependency_tree(root, sorted(dependencies))
    receipt["status"] = (
        "failed" if any(item["result"] == "failed" for item in records)
        else "compiled_pending_review"
    )
    receipt["finished_at"] = _now()
    validate_receipt(receipt)
    return receipt


_SCHEMA_CACHE: Dict[str, Any] = {}


def receipt_schema() -> Mapping[str, Any]:
    if "schema" not in _SCHEMA_CACHE:
        _SCHEMA_CACHE["schema"] = json.loads(
            (PROJECT_ROOT / "schemas" / "build-receipt.schema.json").read_text(
                encoding="utf-8"
            )
        )
    return _SCHEMA_CACHE["schema"]


def validate_receipt(receipt: Mapping[str, Any]) -> None:
    """Schema + 状态形状。受限验证器没有 if/then，形状约束落在这里。"""
    try:
        validate_schema(receipt, receipt_schema())
    except SchemaError as error:
        raise BuildError(f"回执不符合 Schema：{error}") from error
    for item in receipt["editions"]:
        _assert_safe_relative(item["source"])
        if item["pdf"] is not None:
            _assert_safe_relative(item["pdf"]["path"])
    for item in receipt["generation_input_tree"]["files"]:
        _assert_safe_relative(item["path"])

    editions = [item["edition"] for item in receipt["editions"]]
    if receipt["status"] == "running":
        if editions or receipt["dependency_tree"] is not None or receipt["finished_at"]:
            raise BuildError("running 回执不得携带版本结果、依赖闭包或结束时间")
        return
    if tuple(editions) != EDITIONS:
        raise BuildError(f"结束态回执必须恰好四版本且顺序固定，实际 {editions}")
    if receipt["dependency_tree"] is None or receipt["finished_at"] is None:
        raise BuildError("结束态回执必须携带依赖闭包与结束时间")
    failed = [item for item in receipt["editions"] if item["result"] == "failed"]
    if receipt["status"] == "failed" and not failed:
        raise BuildError("failed 回执里没有任何失败版本")
    if receipt["status"] != "failed" and failed:
        raise BuildError("非 failed 回执里出现失败版本")
    # succeeded 版本没有 PDF 记录 = 零证据绿灯。本工具的写入路径产不出这种回执，但回执
    # 是 tracked 证据、后续任务（T24 finalize）还会重写它，尺子必须自己认得出这种形状。
    without_pdf = [
        item["edition"] for item in receipt["editions"]
        if item["result"] == "succeeded" and item["pdf"] is None
    ]
    if without_pdf:
        raise BuildError(f"succeeded 版本必须带 PDF 记录：{without_pdf}")


def load_receipt(path: Path) -> Dict[str, Any]:
    try:
        receipt = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BuildError(f"无法读取 build 回执：{path}: {error}") from error
    if not isinstance(receipt, dict):
        raise BuildError(f"build 回执顶层必须是对象：{path}")
    validate_receipt(receipt)
    return receipt


def assert_transition(
    old: Mapping[str, Any], new: Mapping[str, Any]
) -> None:
    if old["paper_id"] != new["paper_id"]:
        raise BuildError("回执转移不得跨卷")
    if old["attempt_id"] != new["attempt_id"]:
        if new["status"] != "running":
            raise BuildError("新的 attempt 只能从 running 开始")
        return
    if (old["status"], new["status"]) not in STATUS_TRANSITIONS:
        raise BuildError(
            "非法状态转移：%s → %s" % (old["status"], new["status"])
        )


# ---------------------------------------------------------------- 当前性


def receipt_currency(
    root: Path,
    manifest: Mapping[str, Any],
    receipt: Mapping[str, Any],
    toolchain: Optional[Mapping[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """重算四条证据；返回 (是否当前, 失效原因清单)。

    ⚠️ `toolchain=None` 会**跳过**第四条证据（工具链指纹），那正是 fail-open：换了
    TeX Live 的机器上旧回执照样绿。调用方一律显式传 toolchain；解析不出工具链时传一个
    与任何真实指纹都不相等的哨兵（见 `provenance.UNRESOLVED_TOOLCHAIN`），让回执当场
    降级为 stale——绝不要靠传 None 蒙混过去。默认值保留只为兼容既有调用点。
    """
    reasons: List[str] = []
    if receipt["status"] == "running":
        return False, ["running 回执尚无依赖闭包，永远不能算作当前"]

    try:
        expected = projection_digest(manifest, receipt["paper_id"])
    except BuildError as error:
        return False, [f"manifest 投影算不出来：{error}"]
    if receipt["input_projection"] != expected:
        reasons.append("manifest 投影变化")

    try:
        tree = generation_input_tree(root, manifest, receipt["paper_id"])
    except BuildError as error:
        reasons.append(f"生成输入缺失：{error}")
    else:
        if tree["tree_sha256"] != receipt["generation_input_tree"]["tree_sha256"]:
            reasons.append("生成输入树变化")

    for item in receipt["dependency_tree"]["files"]:
        path = Path(root) / item["path"]
        if not path.is_file():
            reasons.append("依赖缺失：%s" % item["path"])
        elif file_sha256(path) != item["sha256"]:
            reasons.append("依赖变化：%s" % item["path"])

    for edition in receipt["editions"]:
        record = edition["pdf"]
        if record is None:
            # 失败版本没有 PDF 是正常的（那正是它失败的记录）；succeeded 版本没有则是
            # 「零 PDF 证据」，重算尺子必须当场报失效，而不是跳过。
            if edition["result"] == "succeeded":
                reasons.append("succeeded 版本没有 PDF 记录：%s" % edition["edition"])
            continue
        path = Path(root) / record["path"]
        if not path.is_file():
            reasons.append("PDF 缺失：%s" % record["path"])
            continue
        if file_sha256(path) != record["sha256"] or path.stat().st_size != record[
            "size_bytes"
        ]:
            reasons.append("PDF 已变化：%s" % record["path"])

    if toolchain is not None and toolchain != receipt["toolchain_fingerprint"]:
        reasons.append("工具链指纹变化")
    return not reasons, reasons


# ---------------------------------------------------------------- finalize


def _warning_key(edition: str, warning: Mapping[str, Any]) -> Tuple[Any, ...]:
    return (
        edition, warning["kind"], warning["box"], warning["width_pt"], warning["lines"],
    )


def finalize_receipt(
    build: Mapping[str, Any], review: Mapping[str, Any]
) -> Dict[str, Any]:
    """纯函数：逐项核对 review 与 build 的绑定后，返回 `succeeded` 候选。

    **不写任何文件**——写盘属于 Task 24 的 finalize 事务。这里只负责「凭什么可以升级」
    这个判断：attempt、投影、两棵输入树、工具链、每一版 PDF 的 SHA 与页数、以及警告集合
    与豁免的逐项匹配。少核一项，`succeeded` 就变成了「看起来像成功」。
    """
    if build["status"] != "compiled_pending_review":
        raise BuildError(
            "只有 compiled_pending_review 的回执可以 finalize，实际 %s" % build["status"]
        )
    if review.get("status") != "passed":
        raise BuildError("review 未通过，build 保持 compiled_pending_review")
    if review.get("paper_id") != build["paper_id"]:
        raise BuildError("review 与 build 不是同一卷")
    if review.get("build_attempt_id") != build["attempt_id"]:
        raise BuildError("review 绑定的 attempt 与当前 build 不一致")
    if review.get("input_projection") != build["input_projection"]:
        raise BuildError("review 绑定的 manifest 投影与当前 build 不一致")
    if review.get("generation_input_tree_sha256") != build["generation_input_tree"][
        "tree_sha256"
    ]:
        raise BuildError("review 绑定的生成输入树与当前 build 不一致")
    if review.get("dependency_tree_sha256") != build["dependency_tree"]["tree_sha256"]:
        raise BuildError("review 绑定的依赖闭包与当前 build 不一致")
    if review.get("toolchain_fingerprint") != build["toolchain_fingerprint"]:
        raise BuildError("review 绑定的工具链指纹与当前 build 不一致")

    reviewed = {item["edition"]: item for item in review.get("editions", [])}
    if sorted(reviewed) != sorted(EDITIONS):
        raise BuildError("review 必须覆盖四个版本")
    for item in build["editions"]:
        seen = reviewed[item["edition"]]
        if item["pdf"] is None:
            raise BuildError("%s 没有 PDF，不能 finalize" % item["edition"])
        if seen.get("pdf_sha256") != item["pdf"]["sha256"]:
            raise BuildError("%s 的 PDF SHA 与 review 不一致" % item["edition"])
        if seen.get("page_count") != item["pdf"]["page_count"]:
            raise BuildError("%s 的页数与 review 不一致" % item["edition"])

    expected = sorted(
        _warning_key(item["edition"], warning)
        for item in build["editions"] for warning in item["log"]["overfull"]
    )
    exemptions = review.get("warning_exemptions", [])
    for item in exemptions:
        if not str(item.get("reason", "")).strip():
            raise BuildError("警告豁免必须写明理由")
    actual = sorted(_warning_key(item["edition"], item) for item in exemptions)
    if expected != actual:
        raise BuildError("警告集合与豁免没有逐项匹配")

    finalized = copy.deepcopy(dict(build))
    finalized["status"] = "succeeded"
    assert_transition(build, finalized)
    validate_receipt(finalized)
    return finalized


# ---------------------------------------------------------------- 清理门禁


def _git_output(root: Path, arguments: Sequence[str]) -> bytes:
    return subprocess.run(
        ["git", "-C", str(root)] + list(arguments),
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def _guard_removable(root: Path, relative: str, expect_dir: bool) -> None:
    """删除前的五道门：存在性、非 symlink、类型、仓库内、未 tracked、已 ignore。

    任一门不过就抛异常——**先产生完整计划再统一执行**的意义正在于此：宁可一个都不删，
    也不要删到一半才发现第 7 个目标是符号链接。
    """
    path = Path(root) / relative
    try:
        info = os.lstat(str(path))
    except OSError as error:
        raise BuildError(f"无法检查删除目标 {relative}：{error}") from error
    if stat.S_ISLNK(info.st_mode):
        raise BuildError(f"删除目标是符号链接，零删除：{relative}")
    if expect_dir and not stat.S_ISDIR(info.st_mode):
        raise BuildError(f"删除目标不是目录：{relative}")
    if not expect_dir and not stat.S_ISREG(info.st_mode):
        raise BuildError(f"删除目标不是普通文件：{relative}")

    real = os.path.realpath(str(path))
    root_real = os.path.realpath(str(root))
    if not (real == root_real or real.startswith(root_real + os.sep)):
        raise BuildError(f"删除目标越出仓库根：{relative}")

    pathspec = relative + "/" if expect_dir else relative
    tracked = _git_output(root, ["ls-files", "-z", "--", pathspec])
    if tracked:
        raise BuildError(f"删除目标含 tracked 内容，零删除：{relative}")
    ignored = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", "--", pathspec],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if ignored.returncode != 0:
        raise BuildError(f"删除目标未被 .gitignore 覆盖，零删除：{relative}")


def clean_build(
    root: Path,
    manifest: Mapping[str, Any],
    paper_ids: Sequence[str],
    execute: bool = False,
) -> Dict[str, List[str]]:
    """只删精确的 `<project_dir>/build/`。没有任何递归 glob。"""
    root = Path(root)
    targets: List[str] = []
    for paper_id in paper_ids:
        paper = _paper(manifest, paper_id)
        relative = _assert_safe_relative(
            "%s/%s/%s" % (PROJECT_RELATIVE, paper["project_dir"], BUILD_DIR_NAME)
        )
        if not os.path.lexists(str(root / relative)):
            continue
        _guard_removable(root, relative, expect_dir=True)
        targets.append(relative)

    removed: List[str] = []
    if execute:
        for relative in sorted(targets):
            shutil.rmtree(str(root / relative))
            removed.append(relative)
    return {"targets": sorted(targets), "removed": sorted(removed)}


def _legacy_evidence(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    toolchain: Mapping[str, Any],
) -> None:
    """删除前的证据链：provenance + review(passed) + build(succeeded 且**四条证据**当前)。

    工具链是必传的，不是可选的：这是全流程唯一不可逆的删除，换过 TeX Live 之后那份
    succeeded 回执描述的已经不是这台机器能复现的产物，此时删掉旧编译产物就是销毁唯一
    的对照物。
    """
    paper = _paper(manifest, paper_id)
    project = "%s/%s" % (PROJECT_RELATIVE, paper["project_dir"])
    provenance = Path(root) / project / PROVENANCE_RELATIVE
    if not provenance.is_file():
        raise BuildError(f"{paper_id}: 缺 provenance，零删除")
    review_path = Path(root) / project / REVIEW_RELATIVE
    if not review_path.is_file():
        raise BuildError(f"{paper_id}: 缺 review 回执，零删除")
    try:
        review = json.loads(review_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise BuildError(f"{paper_id}: review 回执不可读：{error}") from error
    if not isinstance(review, dict) or review.get("status") != "passed":
        raise BuildError(f"{paper_id}: review 未通过，零删除")

    receipt_path = Path(root) / project / RECEIPT_RELATIVE
    if not receipt_path.is_file():
        raise BuildError(f"{paper_id}: 缺 build 回执，零删除")
    receipt = load_receipt(receipt_path)
    if receipt["status"] != "succeeded":
        raise BuildError(
            "%s: build 回执状态是 %s，零删除" % (paper_id, receipt["status"])
        )
    current, reasons = receipt_currency(root, manifest, receipt, toolchain=toolchain)
    if not current:
        raise BuildError(f"{paper_id}: build 回执已失效（{reasons}），零删除")


def cleanup_legacy(
    root: Path,
    manifest: Mapping[str, Any],
    execute: bool = False,
    toolchain: Optional[Mapping[str, Any]] = None,
    search_path: Optional[str] = None,
) -> Dict[str, List[str]]:
    """只删项目根目录四版本的八类旧编译产物，且要求整条证据链齐全。

    阶段 0 固定全量：这是**一次性的历史清扫**，按卷零敲碎打只会留下半清理的目录。
    工具链解析不出来就直接抛错——解析不出就核对不了第四条证据，零删除。
    """
    root = Path(root)
    chain = toolchain or resolve_toolchain(search_path=search_path)
    targets: List[str] = []
    for paper in manifest.get("papers", []):
        paper_id = paper["paper_id"]
        _legacy_evidence(root, manifest, paper_id, chain)
        for edition in EDITIONS:
            for suffix in LEGACY_SUFFIXES:
                relative = _assert_safe_relative(
                    "%s/%s/%s%s"
                    % (PROJECT_RELATIVE, paper["project_dir"], edition, suffix)
                )
                if not os.path.lexists(str(root / relative)):
                    continue
                _guard_removable(root, relative, expect_dir=False)
                targets.append(relative)

    removed: List[str] = []
    if execute:
        for relative in sorted(targets):
            (root / relative).unlink()
            removed.append(relative)
    return {"targets": sorted(targets), "removed": sorted(removed)}


# ---------------------------------------------------------------- issues 对账


def _compile_issue(
    paper_id: str, edition: str, resolved: bool, detail: str
) -> Dict[str, Any]:
    """`origin=formal-build` 的 compile-error 问题。

    ⚠️ `compile-error` 的 fingerprint 身份（issues.py 冻结）是为 Task 24 的逐页视觉检查
    设计的：必须带 `page` 与 `figure_id|warning`。整卷编译失败没有页码，这里用固定的
    `page=1` / `check_code=figure_id=formal-build` 充当判别位——身份由
    type+paper_id+edition+check_code 已经唯一确定，两个常量只是把形状凑齐。
    """
    return {
        "paper_id": paper_id,
        "affected_paper_ids": [],
        "type": "compile-error",
        "status": "resolved" if resolved else "open",
        "impact": "non_blocking" if resolved else "blocks_completion",
        "origin": ISSUE_ORIGIN,
        "edition": edition,
        "page": 1,
        "check_code": ISSUE_CHECK_CODE,
        "figure_id": ISSUE_ORIGIN,
        "resume_action": (
            "已在新一次正式构建中通过，无需动作"
            if resolved else
            "修正 %s 的 %s 后重跑 build --formal（%s）" % (paper_id, edition, detail)
        ),
    }


def reconcile_issues(
    issues_path: Path, results: Mapping[str, Mapping[str, Any]]
) -> Tuple[bytes, Dict[str, List[str]]]:
    """按 paper+edition 对账：当前失败 upsert，当前成功 resolve 旧 attempt 的问题。

    实现刻意**绕道临时副本调用 `issues.upsert_issue()`**，而不是自己拼 Markdown：
    问题总账的编号分配、fingerprint 计算与块序在 issues.py，复制一份出来就等于给格式
    漂移开了口子。事务需要的是最终字节，这里就把最终字节算出来。
    """
    issues_path = Path(issues_path)
    original = issues_path.read_bytes() if issues_path.is_file() else b""
    with tempfile.TemporaryDirectory() as temporary:
        scratch = Path(temporary) / issues_path.name
        if original:
            scratch.write_bytes(original)
        existing = issues_module.load_issues(scratch) if original else []
        known = {item["fingerprint"] for item in existing}

        for paper_id in sorted(results):
            receipt = results[paper_id]
            for record in receipt["editions"]:
                failed = record["result"] == "failed"
                candidate = _compile_issue(
                    paper_id, record["edition"], not failed,
                    "；".join(record["problems"]) or "编译失败",
                )
                fingerprint = issues_module.issue_fingerprint(candidate)
                if failed or fingerprint in known:
                    issues_module.upsert_issue(scratch, candidate)
                    known.add(fingerprint)
        recorded = issues_module.load_issues(scratch) if scratch.is_file() else []
        payload = scratch.read_bytes() if scratch.is_file() else original

    by_paper: Dict[str, List[str]] = {}
    for item in recorded:
        targets = set(item.get("affected_paper_ids") or [])
        if item.get("paper_id") is not None:
            targets.add(item["paper_id"])
        for paper_id in targets:
            by_paper.setdefault(paper_id, []).append(item["issue_id"])
    return payload, {key: sorted(value) for key, value in by_paper.items()}


def _issue_records(payload: bytes) -> List[Dict[str, Any]]:
    with tempfile.TemporaryDirectory() as temporary:
        scratch = Path(temporary) / "issues.md"
        scratch.write_bytes(payload)
        return issues_module.load_issues(scratch)


# ---------------------------------------------------------------- facts 装配


def default_facts_loader(
    root: Path, manifest: Mapping[str, Any], paper_ids: Sequence[str]
) -> Mapping[str, Mapping[str, Any]]:
    """真实 provenance facts adapter 由 Task 16 提供；在此之前一律 fail closed。"""
    try:
        import provenance  # type: ignore
    except ImportError as error:
        raise BuildError(
            "provenance facts adapter 尚不可用（Task 16 提供），拒绝以默认值开工"
        ) from error
    return provenance.load_provenance_facts(root, manifest, paper_ids)


_LOADED_FIELDS = frozenset([
    "provenance", "provenance_unknown", "provenance_conflicts", "artifacts",
    "review", "review_currency", "issues", "batch_report_valid",
])


def merge_facts(
    paper_id: str,
    loaded: Mapping[str, Any],
    build: str,
    build_currency: str,
    issue_records: Sequence[Mapping[str, Any]] = (),
) -> Dict[str, Any]:
    """把 loader 的观察与本工具持有的 build 事实合成一份完整 facts。

    loader **不得**提供 build/build_currency：那两维只有构建回执说了算，允许外部注入
    就等于给「自称已编译」开后门。
    """
    unknown = sorted(set(loaded) - _LOADED_FIELDS)
    if unknown:
        raise BuildError(f"{paper_id}: facts_loader 返回了越权字段 {unknown}")
    values = dict(loaded)
    values["issues"] = tuple(issue_records) if issue_records else tuple(
        values.get("issues") or ()
    )
    try:
        return paper_facts(
            paper_id, build=build, build_currency=build_currency, **values
        )
    except StatusError as error:
        raise BuildError(f"{paper_id}: facts 不合法：{error}") from error


def _build_facts(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    receipt: Optional[Mapping[str, Any]],
    toolchain: Optional[Mapping[str, Any]] = None,
) -> Tuple[str, str]:
    if receipt is None:
        return "missing", "stale"
    current, _ = receipt_currency(root, manifest, receipt, toolchain=toolchain)
    return receipt["status"], "current" if current else "stale"


def _existing_receipt(
    root: Path, manifest: Mapping[str, Any], paper_id: str
) -> Optional[Dict[str, Any]]:
    path = Path(root) / build_receipt_path(_paper(manifest, paper_id))
    if not path.is_file():
        return None
    return load_receipt(path)


# ---------------------------------------------------------------- 状态事务


def _affected(
    manifest: Mapping[str, Any], selected: Sequence[str]
) -> Tuple[List[str], List[Mapping[str, Any]]]:
    """选中的卷 + 它们所在批次的其余卷：批次状态不能只看被重编的那几卷。"""
    chosen = set(selected)
    batches = [
        batch for batch in manifest.get("batches", [])
        if chosen & set(batch["paper_ids"])
    ]
    papers = set(selected)
    for batch in batches:
        papers.update(batch["paper_ids"])
    return sorted(papers), batches


def _reconciled_manifest(
    manifest: Mapping[str, Any],
    transaction_id: str,
    facts_by_paper: Mapping[str, Mapping[str, Any]],
    batches: Sequence[Mapping[str, Any]],
    issue_ids: Mapping[str, Sequence[str]],
) -> Dict[str, Any]:
    document = copy.deepcopy(dict(manifest))
    for paper in document["papers"]:
        paper_id = paper["paper_id"]
        if paper_id not in facts_by_paper:
            continue
        previous = paper["production_state"]
        derived = derive_status(facts_by_paper[paper_id])
        paper["production_state"] = derived
        if paper_id in issue_ids:
            paper["issue_ids"] = list(issue_ids[paper_id])
        if derived == "blocked":
            blockers = [
                item for item in facts_by_paper[paper_id]["issues"]
                if issues_module.blocks_completion(item, paper_id)
            ]
            if not blockers or not paper["issue_ids"]:
                raise BuildError(
                    f"{paper_id}: blocked 必须带 issue 与 resume_action，拒绝写入"
                )
            paper["blocked_from"] = (
                paper["blocked_from"] if previous == "blocked" else previous
            )
            paper["resume_action"] = sorted(
                blockers, key=lambda item: item["issue_id"]
            )[0]["resume_action"]
        else:
            paper["blocked_from"] = None
            paper["resume_action"] = None

    affected = {batch["batch_id"] for batch in batches}
    for batch in document["batches"]:
        if batch["batch_id"] not in affected:
            continue
        batch["status"] = reconcile_batch_status({
            paper_id: facts_by_paper[paper_id] for paper_id in batch["paper_ids"]
        })
    document["revision"] = int(manifest["revision"]) + 1
    document["last_transaction_id"] = transaction_id
    return document


def _commit_state(
    root: Path,
    manifest: Mapping[str, Any],
    receipts: Mapping[str, bytes],
    extra: Mapping[str, bytes],
    build_manifest: Callable[[str], Mapping[str, Any]],
) -> Dict[str, Any]:
    """一个 `state` 事务：回执 / issues 先，manifest 最后并递增 revision。"""
    transaction = Transaction(root)
    document = build_manifest(transaction.transaction_id)
    targets: Dict[str, bytes] = {}
    for relative in sorted(receipts):
        targets[relative] = receipts[relative]
    for relative in sorted(extra):
        targets[relative] = extra[relative]
    targets[MANIFEST_TARGET] = canonical_json(document).encode("utf-8")
    transaction.prepare(
        "state", targets, {}, expected_revision=int(manifest["revision"])
    )
    transaction.commit()
    return document


# ---------------------------------------------------------------- formal


def run_formal(
    manifest_path: Path,
    issues_path: Path,
    selector: str,
    value: Optional[str] = None,
    facts_loader: Optional[Callable[..., Mapping[str, Mapping[str, Any]]]] = None,
    toolchain: Optional[Mapping[str, Any]] = None,
    builder: Optional[Callable[..., Mapping[str, Any]]] = None,
    runner: Optional[Callable[..., Any]] = None,
    search_path: Optional[str] = None,
) -> Dict[str, Any]:
    """两阶段正式构建：running 事务 → 串行构建 → 结果事务。"""
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    if _relative_to(root, manifest_path) != MANIFEST_TARGET:
        raise BuildError(f"--manifest 必须是 {MANIFEST_TARGET}")
    issues_path = Path(issues_path).resolve()
    if _relative_to(root, issues_path) != ISSUES_TARGET:
        raise BuildError(f"--issues 必须是 {ISSUES_TARGET}")
    loader = facts_loader or default_facts_loader
    build_one = builder or build_paper_result

    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        selected = select_paper_ids(manifest, selector, value)
        if not selected:
            raise BuildError("选择器没有命中任何试卷")
        chain = toolchain or resolve_toolchain(search_path=search_path)

        affected, batches = _affected(manifest, selected)
        loaded = dict(loader(root, manifest, affected))
        missing = sorted(set(affected) - set(loaded))
        if missing:
            raise BuildError(f"facts_loader 没有覆盖 {missing}")
        for paper_id in selected:
            if loaded[paper_id].get("provenance") != "current":
                raise BuildError(
                    "%s 的 provenance 不是 current（%s），拒绝开始正式构建"
                    % (paper_id, loaded[paper_id].get("provenance"))
                )

        # ---- 事务 1：running
        running: Dict[str, Dict[str, Any]] = {}
        receipts: Dict[str, bytes] = {}
        for paper_id in selected:
            receipt = running_receipt(
                root, manifest, paper_id, chain,
                existing=_existing_receipt(root, manifest, paper_id),
            )
            running[paper_id] = receipt
            receipts[build_receipt_path(_paper(manifest, paper_id))] = (
                canonical_json(receipt).encode("utf-8")
            )
        manifest = _commit_state(
            root, manifest, receipts, {},
            lambda transaction_id: _reconciled_manifest(
                manifest, transaction_id,
                _assemble_facts(
                    root, manifest, affected, loaded, running, toolchain=chain
                ),
                batches, {},
            ),
        )

        # ---- 串行构建
        results: Dict[str, Dict[str, Any]] = {}
        for paper_id in selected:
            started = running[paper_id]
            results[paper_id] = dict(build_one(
                root, manifest, paper_id, chain,
                runner=runner,
                attempt_id=started["attempt_id"],
                previous_attempt_id=started["previous_attempt_id"],
                started_at=started["started_at"],
            ))
            assert_transition(started, results[paper_id])

        # ---- 事务 2：结果 + issues + reconciled manifest
        payload, issue_ids = reconcile_issues(issues_path, results)
        records = _issue_records(payload)
        receipts = {
            build_receipt_path(_paper(manifest, paper_id)):
                canonical_json(results[paper_id]).encode("utf-8")
            for paper_id in selected
        }
        extra: Dict[str, bytes] = {}
        if payload != (issues_path.read_bytes() if issues_path.is_file() else b""):
            extra[ISSUES_TARGET] = payload
        facts = _assemble_facts(
            root, manifest, affected, loaded, results, issue_records=records,
            toolchain=chain,
        )
        manifest = _commit_state(
            root, manifest, receipts, extra,
            lambda transaction_id: _reconciled_manifest(
                manifest, transaction_id, facts, batches, issue_ids
            ),
        )

    failed = sorted(
        paper_id for paper_id in selected if results[paper_id]["status"] == "failed"
    )
    pending = [
        paper_id for paper_id in selected
        if results[paper_id]["status"] == "compiled_pending_review"
    ]
    return {
        "code": "BUILD_FAILED" if failed else "COMPILED_PENDING_REVIEW",
        "papers": list(selected),
        "pending": len(pending),
        "failed": len(failed),
        "failed_papers": failed,
        "revision": manifest["revision"],
        "batches": {
            batch["batch_id"]: next(
                item["status"] for item in manifest["batches"]
                if item["batch_id"] == batch["batch_id"]
            )
            for batch in batches
        },
    }


def _assemble_facts(
    root: Path,
    manifest: Mapping[str, Any],
    affected: Sequence[str],
    loaded: Mapping[str, Mapping[str, Any]],
    receipts: Mapping[str, Mapping[str, Any]],
    issue_records: Sequence[Mapping[str, Any]] = (),
    toolchain: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Dict[str, Any]]:
    facts: Dict[str, Dict[str, Any]] = {}
    for paper_id in affected:
        receipt = receipts.get(paper_id)
        if receipt is None:
            receipt = _existing_receipt(root, manifest, paper_id)
        build, currency = _build_facts(
            root, manifest, paper_id, receipt, toolchain=toolchain
        )
        selected_issues = [
            item for item in issue_records
            if paper_id in set(item.get("affected_paper_ids") or [])
            or item.get("paper_id") == paper_id
        ] if issue_records else list(loaded[paper_id].get("issues") or ())
        facts[paper_id] = merge_facts(
            paper_id, loaded[paper_id], build, currency, selected_issues
        )
    return facts


def _relative_to(root: Path, path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError as error:
        raise BuildError(f"路径不在仓库内：{path}") from error


# ---------------------------------------------------------------- 只读核对


def validate_receipts(
    manifest_path: Path,
    selector: str,
    value: Optional[str] = None,
    require_final: bool = False,
    require_current_inputs: bool = False,
    search_path: Optional[str] = None,
) -> Dict[str, Any]:
    """只读：逐卷重算**四条证据**（投影、生成输入树、依赖闭包、工具链）与 PDF；不写盘。

    四条并列、没有开关：换了 TeX Live 的机器上旧回执必须当场 stale。
    `require_current_inputs` 只是显式声明（Interfaces 冻结了这个参数的存在），
    语义已并入默认行为，传不传结果一致。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    manifest = load_manifest(manifest_path)
    selected = select_paper_ids(manifest, selector, value)

    counters = {
        "missing": 0, "invalid": 0, "running": 0, "failed": 0, "stale": 0,
        "pending": 0, "succeeded": 0,
    }
    try:
        chain = resolve_toolchain(search_path=search_path)
    except BuildError as error:
        # 解析不出工具链就核对不了第四条证据；与 check-tools 一致地 fail closed，
        # 而不是退化成「只核三条」——那正是 fail-open。
        report = {
            "code": "INVALID", "papers": len(selected),
            "problems": [f"工具链不可用：{error}"],
        }
        report.update(counters)
        return report
    problems: List[str] = []
    for paper_id in selected:
        path = Path(root) / build_receipt_path(_paper(manifest, paper_id))
        if not path.is_file():
            counters["missing"] += 1
            problems.append(f"{paper_id}: 缺 build 回执")
            continue
        try:
            receipt = load_receipt(path)
        except BuildError as error:
            counters["invalid"] += 1
            problems.append(f"{paper_id}: {error}")
            continue
        if receipt["status"] == "running":
            counters["running"] += 1
            problems.append(f"{paper_id}: 回执停在 running，不能算作 final")
            continue
        if receipt["status"] == "failed":
            counters["failed"] += 1
            problems.append(f"{paper_id}: 构建失败")
            continue
        current, reasons = receipt_currency(root, manifest, receipt, toolchain=chain)
        if not current:
            counters["stale"] += 1
            problems.append("%s: 回执已失效（%s）" % (paper_id, "；".join(reasons)))
            continue
        counters["pending" if receipt["status"] == "compiled_pending_review"
                 else "succeeded"] += 1

    blocked = (
        counters["missing"] + counters["invalid"] + counters["running"]
        + counters["failed"] + counters["stale"]
    )
    if blocked:
        code = "INVALID"
    elif require_final and counters["pending"]:
        code = "PENDING_REVIEW"
    else:
        code = "OK"
    report = {"code": code, "papers": len(selected), "problems": problems}
    report.update(counters)
    return report


VALIDATE_EXIT = {"OK": EXIT_OK, "PENDING_REVIEW": EXIT_PENDING_REVIEW,
                 "INVALID": EXIT_INVALID}


# ---------------------------------------------------------------- 暂存区核对

# 门禁逻辑只此一份，住在 cli_common.py——与 Task 14 把三个生成器的 CLI 骨架收敛到那里
# 是同一条理由：两份逐字副本意味着修了一处、另一处照旧，而**没有任何测试会发现只改了
# 一处**。这里只把本工具的异常类绑上去。
check_staged = cli_common.check_staged

# ---------------------------------------------------------------- 对外别名

# Task 16 的 `provenance.py` 是这三件的第二个调用方。**不复制、只借用**：
# `_reconciled_manifest()` 里住着「blocked 必须带 issue 与 resume_action」这类不变量，
# 抄一份出去就是第二套 reconciler——status.py 顶部那条警告点名的正是这种分裂。
assemble_facts = _assemble_facts
reconciled_manifest = _reconciled_manifest
commit_state = _commit_state
affected_papers = _affected


def read_pathspec(path: Path) -> List[str]:
    return cli_common.read_pathspec(path, BuildError)


# ---------------------------------------------------------------- 位置参数


def build_smoke(
    manifest_path: Path,
    project_dir: str,
    edition: Optional[str] = None,
    search_path: Optional[str] = None,
    runner: Optional[Callable[..., Any]] = None,
) -> Dict[str, Any]:
    """位置参数 smoke：只写 ignored 的 `build/`，**不碰任何 tracked 文件**。

    诊断落在 `build/<edition>.diagnostics.json`——同样在 ignored 目录里，绝不会被误当
    成正式回执提交。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    manifest = load_manifest(manifest_path)
    matched = [
        paper for paper in manifest["papers"] if paper["project_dir"] == project_dir
    ]
    if len(matched) != 1:
        raise UsageError(f"manifest 里没有项目目录：{project_dir}")
    if edition is not None and edition not in EDITIONS:
        raise UsageError(f"未知版本：{edition}")
    chain = resolve_toolchain(search_path=search_path)

    records = []
    for item in (EDITIONS if edition is None else (edition,)):
        outcome = build_target(root, project_dir, item, chain, runner=runner)
        record = outcome["record"]
        records.append(record)
        atomic_write_json(
            _project_path(root, matched[0]) / BUILD_DIR_NAME
            / ("%s.diagnostics.json" % item),
            record,
        )
    return {
        "code": "BUILD_FAILED" if any(
            item["result"] == "failed" for item in records
        ) else "OK",
        "project_dir": project_dir,
        "editions": records,
    }


# ---------------------------------------------------------------- CLI


def _selection(arguments: argparse.Namespace) -> Tuple[str, Optional[str]]:
    if getattr(arguments, "all", False):
        return "all", None
    if getattr(arguments, "batch", None) is not None:
        return "batch", arguments.batch
    return "paper", arguments.paper


def _add_selector(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="全部试卷")
    group.add_argument("--batch", metavar="BATCH_ID", help="按批次")
    group.add_argument("--paper", metavar="PAPER_ID", help="按 manifest paper_id")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="严格 XeLaTeX 构建与构建回执")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build")
    build.add_argument("target", nargs="?", help="项目目录名（smoke 模式）")
    build.add_argument("edition", nargs="?", help="版本名（缺省编四版）")
    build.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    build.add_argument("--issues", default=str(DEFAULT_ISSUES))
    build.add_argument("--formal", action="store_true", help="写正式回执与状态")
    build.add_argument("--all", action="store_true")
    build.add_argument("--batch", metavar="BATCH_ID")
    build.add_argument("--paper", metavar="PAPER_ID")
    build.add_argument("--json", action="store_true")

    validate = subparsers.add_parser("validate-receipts")
    validate.add_argument("--manifest", required=True)
    _add_selector(validate)
    validate.add_argument("--require-final", action="store_true")
    validate.add_argument(
        "--require-current-inputs", action="store_true",
        help="显式声明「要求输入当前」；语义已并入默认校验，传不传结果一致",
    )
    validate.add_argument("--json", action="store_true")

    clean = subparsers.add_parser("clean-build")
    clean.add_argument("--manifest", required=True)
    _add_selector(clean)
    action = clean.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--execute", action="store_true")

    legacy = subparsers.add_parser("cleanup-legacy")
    legacy.add_argument("--manifest", required=True)
    legacy_action = legacy.add_mutually_exclusive_group(required=True)
    legacy_action.add_argument("--dry-run", action="store_true")
    legacy_action.add_argument("--execute", action="store_true")

    tools = subparsers.add_parser("check-tools")
    tools.add_argument("--json", action="store_true")

    output = subparsers.add_parser("output-paths")
    output.add_argument("--manifest", required=True)
    output.add_argument("--issues", required=True)
    _add_selector(output)
    output.add_argument("--include-state", action="store_true")
    output.add_argument("--nul", required=True, action="store_true")

    staged = subparsers.add_parser("check-staged")
    staged.add_argument("--pathspec-file", required=True)
    staged.add_argument("--nul", required=True, action="store_true")
    return parser


def _emit(payload: Mapping[str, Any], as_json: bool, lines: Sequence[str]) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    for line in lines:
        print(line)


def _build_command(
    arguments: argparse.Namespace,
    parser: argparse.ArgumentParser,
    facts_loader: Optional[Callable[..., Any]],
    search_path: Optional[str],
) -> int:
    selected = [
        item for item in (arguments.all, arguments.batch, arguments.paper) if item
    ]
    if arguments.formal:
        if arguments.target is not None or arguments.edition is not None:
            parser.error("--formal 与位置参数互斥")
        if len(selected) != 1:
            parser.error("--formal 必须且只能给一个 --all/--batch/--paper")
        selector, value = _selection(arguments)
        report = run_formal(
            Path(arguments.manifest), Path(arguments.issues), selector, value,
            facts_loader=facts_loader, search_path=search_path,
        )
        _emit(report, arguments.json, [
            "%s：%d 待审、%d 失败" % (report["code"], report["pending"], report["failed"])
        ])
        return EXIT_BUILD_FAILED if report["code"] == "BUILD_FAILED" else EXIT_OK

    if selected:
        parser.error("smoke 模式不接受 --all/--batch/--paper")
    if arguments.target is None:
        parser.error("smoke 模式需要项目目录名")
    try:
        report = build_smoke(
            Path(arguments.manifest), arguments.target, arguments.edition,
            search_path=search_path,
        )
    except UsageError as error:
        print("error: %s" % error, file=sys.stderr)
        return EXIT_USAGE
    _emit(report, arguments.json, [
        "%s %s" % (item["result"], item["edition"]) for item in report["editions"]
    ])
    return EXIT_BUILD_FAILED if report["code"] == "BUILD_FAILED" else EXIT_OK


def _output_paths_command(arguments: argparse.Namespace) -> int:
    manifest_path = Path(arguments.manifest).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    manifest = load_manifest(manifest_path)
    selector, value = _selection(arguments)
    paths = list(paper_ownership_paths(
        manifest, select_paper_ids(manifest, selector, value)
    ))
    if arguments.include_state:
        if _relative_to(root, Path(arguments.issues)) != ISSUES_TARGET:
            raise BuildError(f"--issues 必须是 {ISSUES_TARGET}")
        paths.extend([MANIFEST_TARGET, ISSUES_TARGET])
    duplicates = sorted({item for item in paths if paths.count(item) > 1})
    if duplicates:
        raise BuildError(f"所有权范围内路径重复：{duplicates}")
    sys.stdout.buffer.write(
        b"".join(item.encode("utf-8") + b"\0" for item in paths)
    )
    sys.stdout.buffer.flush()
    return EXIT_OK


def main(
    argv: Optional[Sequence[str]] = None,
    facts_loader: Optional[Callable[..., Any]] = None,
    search_path: Optional[str] = None,
) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)

    if arguments.command == "build":
        return _build_command(arguments, parser, facts_loader, search_path)

    if arguments.command == "validate-receipts":
        selector, value = _selection(arguments)
        report = validate_receipts(
            Path(arguments.manifest), selector, value,
            require_final=arguments.require_final,
            require_current_inputs=arguments.require_current_inputs,
            search_path=search_path,
        )
        _emit(report, arguments.json, ["  ✗ %s" % item for item in report["problems"]]
              + ["%s：%d 卷" % (report["code"], report["papers"])])
        return VALIDATE_EXIT[report["code"]]

    if arguments.command in {"clean-build", "cleanup-legacy"}:
        manifest_path = Path(arguments.manifest).resolve()
        root = cli_common.repository_root(manifest_path.parent)
        manifest = load_manifest(manifest_path)
        with RepoLock(root):
            if arguments.command == "clean-build":
                selector, value = _selection(arguments)
                report = clean_build(
                    root, manifest, select_paper_ids(manifest, selector, value),
                    execute=arguments.execute,
                )
            else:
                report = cleanup_legacy(
                    root, manifest, execute=arguments.execute,
                    search_path=search_path,
                )
        for relative in report["targets"]:
            print("%s %s" % ("removed" if arguments.execute else "plan", relative))
        print("共 %d 个目标，%d 个已删除" % (
            len(report["targets"]), len(report["removed"])
        ))
        return EXIT_OK

    if arguments.command == "check-tools":
        try:
            chain = resolve_toolchain(search_path=search_path)
        except BuildError as error:
            _emit(
                {"code": "INVALID", "problem": str(error)}, arguments.json,
                ["✗ %s" % error],
            )
            return EXIT_INVALID
        _emit(
            {"code": "OK", "toolchain": chain}, arguments.json,
            ["%s %s" % (item["name"], item["version"]) for item in chain["tools"]],
        )
        return EXIT_OK

    if arguments.command == "output-paths":
        return _output_paths_command(arguments)

    if arguments.command == "check-staged":
        root = cli_common.repository_root(Path.cwd())
        problems = check_staged(root, read_pathspec(Path(arguments.pathspec_file)))
        if problems:
            for problem in problems:
                print(problem, file=sys.stderr)
            return EXIT_INVALID
        print("暂存区与所有权范围一致")
        return EXIT_OK

    raise BuildError(f"未知命令：{arguments.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildError, OSError, RuntimeError, StatusError,
            subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(EXIT_INVALID)

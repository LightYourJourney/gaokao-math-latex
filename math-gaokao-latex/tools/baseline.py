from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from manifest import atomic_write_json, file_sha256, load_manifest
from source_manifest import project_legacy_index
from transaction import RepoLock

EDITIONS = ("试题版", "解析版", "简答版", "印刷版")
CONTENT_FILES = ("questions.tex", "answers.tex", "answers_short.tex")
PLAN_PATH = "docs/superpowers/plans/2026-08-04-高考数学LaTeX阶段0实施计划.md"
# 已裁定漂移登记表：规范工程根目录固定，故这里由工具自身位置推出，两个子命令共用。
ADJUDICATED_DRIFTS_PATH = (
    Path(__file__).resolve().parent.parent / "reports" / "adjudicated-drifts.json"
)
LEDGER_VERSION = 1
DRIFT_CLASSES = (
    "header", "migration", "stale-artifact", "short-answers-regeneration",
    "visual-layout-repair", "layout-regeneration",
)
ADJUDICATION_SOURCES = (
    "task-13-review", "task-14-review", "task-25-visual-review",
    "task-26-regeneration", "task-27-regeneration",
)
_BUILD_INPUT_SUFFIXES = {".tex", ".md", ".py", ".sh"}
_PAPER_ID_RE = re.compile(r"\\renewcommand\{\\gkpaperid\}\{([^{}]+)\}")
_QUESTION_ID_RE = re.compile(r"\\gkti\{([0-9]+)\}")
_OVERFULL_RE = re.compile(r"Overfull \\hbox \(([0-9.]+)pt too wide\)(.*)")
_UNDERFULL_RE = re.compile(r"Underfull \\hbox \(badness ([0-9]+)\)(.*)")
_OUTPUT_PAGES_RE = re.compile(r"Output written on .*?\(([0-9]+) pages?[,)]")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

# 身份迁移只允许给兼容 index 加这三个键：顶层 batches，每条 paper 的 paper_id/legacy_ids。
_INDEX_ADDED_KEYS = ("batches",)
_INDEX_PAPER_ADDED_KEYS = ("paper_id", "legacy_ids")

# 比较视图的七个层级，及其在报告里的显示前缀。
_LEVEL_PATHS = {
    "baseline": "",
    "repository": "repository.",
    "index": "index.",
    "paper": "papers[].",
    "target": "papers[].targets[].",
    "warnings": "papers[].targets[].warnings.",
    "warning": "papers[].targets[].warnings[].",
}

# 已审查、不计入漂移的字段：或不可字节复现，或是身份迁移的正当新增。
# 每条写成 (层级, 字段名, 理由)——层级让 tests 能机械核对"采集器吐出的键要么被比较、
# 要么在这张表里"，避免比较维度因字段名写旧而静默失效。
_REVIEWED_FIELDS = (
    ("baseline", "kind", "legacy 与迁移后基线的种类标记本就不同"),
    ("baseline", "build_inputs", "阶段 0 新增了 tools/ 与 tests/ 源文件，且工作树可能正在重新生成"),
    ("repository", "head", "阶段 0 的提交推进了仓库 HEAD"),
    ("repository", "compile_sha256",
     "Task 15 把 compile.sh 换成 tools/build_projects.py 的薄包装；legacy 侧冻结的本就是"
     "旧脚本（计划原文：记录「旧 compile.sh SHA-256」）"),
    ("index", "sha256", "身份迁移重写了 index.json；兼容字段改由 legacy_compat 逐字段比较"),
    ("paper", "paper_id", "身份迁移新增的稳定 ID，legacy 侧不存在"),
    ("target", "pdf_sha256", "XeLaTeX 输出内嵌时间戳，PDF 非字节可复现"),
    ("target", "log_sha256", "同上，日志同样内嵌时间戳"),
    ("warning", "log_line", "行号只是警告在日志内的位置，随环境位移"),
)

# 迁移边界两侧取值不同、且这种不同已被裁定为正当的**「路径 + 取值对」**。与
# `_REVIEWED_FIELDS` 分开的理由：那张表是「整个字段不参与比较」，粒度是层级里的键名，
# 而这里要豁免的是 `legacy_compat` 深处的**一个叶子**——把整个 legacy_compat 划进
# reviewed 会让 structure/pdf_pages/title 全部失去保护。
#
# 每条登记 (路径, legacy 取值, current 取值, 理由) **四元组**，放行判据与
# `_split_adjudicated()` 的双哈希口径一字不差：两侧取值都要与登记的那一对逐字相等。
# 只登记路径是不够的——`_diff()` 的 Mapping 分支用 `left.get(key, _ABSENT)` 把「键被整个
# 删掉」也汇进同一条标量比较，于是「只看路径」会把删键、改成任意第三个值一并静默吞掉，
# 那正是 `_split_adjudicated()` docstring 点名要避免的「一次裁定 = 永久免检」。
# 路径同样逐字精确、不做前缀匹配：写成前缀就等于把它下面的整棵子树一起赦免了。
#
# 被豁免那一维的守护者由此有三层，且都盯**取值**而不是路径：本表登记的 current 取值
# 本身（改字面量并重生成 index.json 会让 current 侧对不上登记值，当场重新报漂移）、
# `test_baseline.test_every_pre_migration_index_field_value_is_unchanged`、以及
# `test_generate_projects.IndexProjectionExcludesRuntimeStateTests` 对
# `index["generated_by"]` 的逐字断言。
# ⚠️ `LiveIndexIsUnchangedTests` **不在其中**：它比对的是在库 index 与
# `build_legacy_index()` 的现场重建，而字面量就住在 `build_legacy_index()` 里——改字面量
# 再重生成，它照样绿。
_REWRITTEN_FIELDS = (
    (
        "index.legacy_compat.generated_by",
        "tools/split_project.py",
        "tools/generate_projects.py",
        "T16 控制器授权：index 投影剔除运行态时一并落实 T13 递延裁定，"
        "generated_by 由 tools/split_project.py 改为 tools/generate_projects.py；"
        "legacy 侧冻结的仍是迁移前的旧值",
    ),
)
_REWRITTEN_PAIRS = {
    field: (legacy_value, current_value)
    for field, legacy_value, current_value, _ in _REWRITTEN_FIELDS
}

_COMPARED_BASELINE_FIELDS = (
    "baseline_version", "repository", "index", "papers", "summary",
)
# compile_sha256 不在此列（见 _REVIEWED_FIELDS）；compile_path 仍然比较——入口脚本可以
# 被改写，但不得改名或搬家，否则调用方的命令会静默指向别处。
_COMPARED_REPOSITORY_FIELDS = ("plan_path", "plan_sha256", "compile_path")
# legacy_compat 是迁移前 index 的兼容投影：legacy 侧由 git 锚点取回后填入，
# 迁移后侧由采集器记录，两侧逐字段比较——这是 index 深层字段唯一的持续护栏。
_COMPARED_INDEX_FIELDS = ("path", "paper_count", "legacy_ids", "legacy_compat")
_COMPARED_PAPER_FIELDS = (
    "legacy_id", "project_dir", "question_ids", "content_sha256", "figures", "shells",
)
_COMPARED_TARGET_FIELDS = ("path", "edition", "log_path", "pages")
# 只有共享 TeX 的内容哈希能被裁定放行——登记表是窄入口，题号、图树、index 投影等
# 维度的漂移永远进不来。字段形状由 _diff() 的递归路径决定：papers[N].content_sha256.X
_CONTENT_DRIFT_FIELD = re.compile(r"^papers\[([0-9]+)\]\.content_sha256\.(.+)$")
_COMPARED_WARNING_COUNTERS = (
    "hard_errors", "missing_characters", "undefined_references",
)
_COMPARED_WARNING_LISTS = ("overfull", "underfull", "latex_warnings")
_TARGET_SUMMARY_FIELDS = (
    "target_count", "total_pages", "hard_errors", "missing_characters",
    "undefined_references", "overfull_count",
)


class _Absent:
    """比较视图里"这一侧没有该字段"的哨兵，与任何真实取值都不相等。"""

    __slots__ = ()

    def __repr__(self) -> str:
        return "<缺失>"


_ABSENT = _Absent()


def _run_text(arguments: Sequence[str], **kwargs: Any) -> str:
    return subprocess.check_output(list(arguments), text=True, **kwargs).strip()


def _repository_root(project_root: Path) -> Path:
    raw = _run_text([
        "git", "-C", str(project_root), "rev-parse", "--show-toplevel"
    ])
    return Path(raw).resolve()


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"路径不在基线项目内：{path}") from error


def _record_tree_sha256(files: Sequence[Mapping[str, str]]) -> str:
    tree_payload = json.dumps(
        files,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(tree_payload).hexdigest()


def _tracked_build_inputs(repo: Path, project_root: Path) -> Dict[str, Any]:
    project_relative = _relative(project_root, repo)
    raw = subprocess.check_output([
        "git", "-C", str(repo), "ls-tree", "-r", "-z", "--name-only",
        "HEAD", "--", project_relative,
    ])
    records = raw.split(b"\0")
    files = []
    for encoded in records:
        if not encoded:
            continue
        try:
            relative = encoded.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("tracked build input 路径不是 UTF-8") from error
        path = repo / relative
        if path.suffix not in _BUILD_INPUT_SUFFIXES:
            continue
        if not path.is_file():
            raise ValueError(f"tracked build input 缺失或不是普通文件：{relative}")
        files.append({"path": relative, "sha256": file_sha256(path)})
    files.sort(key=lambda item: item["path"])
    if files:
        completed = subprocess.run(
            [
                "git", "-C", str(repo), "diff", "--quiet", "HEAD", "--",
                *[item["path"] for item in files],
            ],
            check=False,
        )
        if completed.returncode == 1:
            raise ValueError("legacy build input 工作树/索引与 HEAD 不一致")
        if completed.returncode != 0:
            raise subprocess.CalledProcessError(completed.returncode, completed.args)
    return {
        "files": files,
        "tree_sha256": _record_tree_sha256(files),
    }


def _pdf_pages(path: Path) -> int:
    try:
        output = _run_text(["pdfinfo", str(path)])
    except (OSError, subprocess.CalledProcessError) as error:
        raise ValueError(f"无法读取 PDF 页数：{path}: {error}") from error
    for line in output.splitlines():
        if line.startswith("Pages:"):
            raw = line.split(":", 1)[1].strip()
            try:
                pages = int(raw)
            except ValueError as error:
                raise ValueError(f"PDF Pages 非整数：{path}: {raw}") from error
            if pages <= 0:
                raise ValueError(f"PDF 页数必须为正数：{path}")
            return pages
    raise ValueError(f"pdfinfo 缺少 Pages：{path}")


def _log_warnings(path: Path, expected_pages: int) -> Dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        raise ValueError(f"无法读取 XeLaTeX 日志：{path}: {error}") from error
    output_pages = [int(value) for value in _OUTPUT_PAGES_RE.findall(raw)]
    if not output_pages or output_pages[-1] != expected_pages:
        raise ValueError(
            f"PDF/log 页数不一致：{path}: PDF={expected_pages}, log={output_pages[-1:] or 'missing'}"
        )

    overfull = []
    underfull = []
    latex_warnings = []
    for number, line in enumerate(raw.splitlines(), start=1):
        overfull_match = _OVERFULL_RE.search(line)
        if overfull_match is not None:
            overfull.append({
                "log_line": number,
                "width_pt": overfull_match.group(1),
                "context": overfull_match.group(2).strip(),
                "message": line,
            })
        underfull_match = _UNDERFULL_RE.search(line)
        if underfull_match is not None:
            underfull.append({
                "log_line": number,
                "badness": int(underfull_match.group(1)),
                "context": underfull_match.group(2).strip(),
                "message": line,
            })
        if "Warning:" in line and (
            line.startswith("LaTeX Warning:")
            or line.startswith("Package ")
            or line.startswith("Class ")
        ):
            latex_warnings.append({"log_line": number, "message": line})

    hard_errors = sum(1 for line in raw.splitlines() if line.startswith("!"))
    missing_characters = raw.count("Missing character:")
    undefined_references = sum(
        1
        for line in raw.splitlines()
        if (
            re.search(r"Reference .* undefined", line) is not None
            or "There were undefined references" in line
        )
    )
    return {
        "hard_errors": hard_errors,
        "missing_characters": missing_characters,
        "undefined_references": undefined_references,
        "overfull": overfull,
        "underfull": underfull,
        "latex_warnings": latex_warnings,
    }


def _shell_record(project_root: Path, paper_dir: Path, edition: str) -> Dict[str, Any]:
    path = paper_dir / f"{edition}.tex"
    if not path.is_file():
        raise ValueError(f"缺少 legacy 壳：{path}")
    raw = path.read_text(encoding="utf-8")
    matches = _PAPER_ID_RE.findall(raw)
    if len(matches) != 1:
        raise ValueError(f"legacy 壳必须恰有一个 \\gkpaperid：{path}")
    return {
        "path": _relative(path, project_root),
        "edition": edition,
        "paper_id": matches[0],
        "sha256": file_sha256(path),
    }


def _target_record(project_root: Path, paper_dir: Path, edition: str) -> Dict[str, Any]:
    pdf = paper_dir / f"{edition}.pdf"
    log = paper_dir / f"{edition}.log"
    if not pdf.is_file() or not log.is_file():
        raise ValueError(f"缺少当前 worktree 重建的 PDF/log：{paper_dir.name}/{edition}")
    pages = _pdf_pages(pdf)
    return {
        "path": _relative(pdf, project_root),
        "edition": edition,
        "pages": pages,
        "pdf_sha256": file_sha256(pdf),
        "log_path": _relative(log, project_root),
        "log_sha256": file_sha256(log),
        "warnings": _log_warnings(log, pages),
    }


def _paper_record(
    project_root: Path,
    metadata: Mapping[str, Any],
    include_targets: bool = True,
) -> Dict[str, Any]:
    project_dir = metadata.get("dir")
    legacy_id = metadata.get("id")
    if not isinstance(project_dir, str) or not isinstance(legacy_id, str):
        raise ValueError("index paper 缺少 dir/id")
    paper_dir = project_root / project_dir
    if not paper_dir.is_dir():
        raise ValueError(f"index paper 目录不存在：{project_dir}")

    content_sha256 = {}
    for name in CONTENT_FILES:
        path = paper_dir / name
        if not path.is_file():
            raise ValueError(f"缺少共享内容文件：{path}")
        content_sha256[name] = file_sha256(path)
    questions = (paper_dir / "questions.tex").read_text(encoding="utf-8")
    question_ids = [int(value) for value in _QUESTION_ID_RE.findall(questions)]
    expected_count = metadata.get("questions")
    if question_ids != list(range(1, expected_count + 1)):
        raise ValueError(f"题号序列与 index 不一致：{project_dir}")

    # 项目 <试卷>/figures/ 是图形的唯一永久源：基线冻结它的哈希树，任何改动都算漂移。
    # 合并书里的副本只是下游，只允许"项目 → 合并书"单向同步，同名不同哈希必须失败。
    figure_dir = paper_dir / "figures"
    figures = []
    if figure_dir.is_dir():
        for path in sorted(figure_dir.iterdir(), key=lambda item: item.name):
            if path.is_file():
                figures.append({
                    "path": _relative(path, project_root),
                    "sha256": file_sha256(path),
                })
    shells = [_shell_record(project_root, paper_dir, edition) for edition in EDITIONS]
    if any(shell["paper_id"] != legacy_id for shell in shells):
        raise ValueError(f"legacy 壳 paper_id 与 index.id 不一致：{project_dir}")
    record = {
        "project_dir": project_dir,
        "legacy_id": legacy_id,
        "question_ids": question_ids,
        "content_sha256": content_sha256,
        "figures": figures,
        "shells": shells,
    }
    if include_targets:
        record["targets"] = [
            _target_record(project_root, paper_dir, edition) for edition in EDITIONS
        ]
    return record


def _load_index(project_root: Path) -> Dict[str, Any]:
    index_path = project_root / "index.json"
    if not index_path.is_file():
        raise ValueError(f"项目缺少 index.json：{project_root}")
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"index.json 无效：{error}") from error
    papers_metadata = index.get("papers")
    if not isinstance(papers_metadata, list) or any(
        not isinstance(paper, Mapping) for paper in papers_metadata
    ):
        raise ValueError("index papers 必须是对象数组")
    legacy_ids = [paper.get("id") for paper in papers_metadata]
    if len(legacy_ids) != 21 or len(legacy_ids) != len(set(legacy_ids)):
        raise ValueError("index 必须包含 21 个唯一旧 ID")
    return index


def _repository_record(repo: Path, project_root: Path) -> Dict[str, Any]:
    plan = repo / PLAN_PATH
    compile_script = project_root / "compile.sh"
    if not plan.is_file() or not compile_script.is_file():
        raise ValueError("缺少 phase 0 计划或 legacy compile.sh")
    return {
        "head": _run_text(["git", "-C", str(repo), "rev-parse", "HEAD"]),
        "plan_path": PLAN_PATH,
        "plan_sha256": file_sha256(plan),
        "compile_path": _relative(compile_script, repo),
        "compile_sha256": file_sha256(compile_script),
    }


def _summary(papers: Sequence[Mapping[str, Any]], include_targets: bool) -> Dict[str, Any]:
    summary: Dict[str, Any] = {"paper_count": len(papers)}
    if not include_targets:
        summary.update({field: None for field in _TARGET_SUMMARY_FIELDS})
        return summary
    targets = [target for paper in papers for target in paper["targets"]]
    summary.update({
        "target_count": len(targets),
        "total_pages": sum(target["pages"] for target in targets),
        "hard_errors": sum(target["warnings"]["hard_errors"] for target in targets),
        "missing_characters": sum(
            target["warnings"]["missing_characters"] for target in targets
        ),
        "undefined_references": sum(
            target["warnings"]["undefined_references"] for target in targets
        ),
        "overfull_count": sum(len(target["warnings"]["overfull"]) for target in targets),
    })
    return summary


def collect_legacy_baseline(project_root: Path) -> Dict[str, Any]:
    project_root = Path(project_root).resolve()
    index = _load_index(project_root)
    papers_metadata = index["papers"]
    repo = _repository_root(project_root)
    papers = [_paper_record(project_root, metadata) for metadata in papers_metadata]
    baseline = {
        "baseline_version": 1,
        "kind": "legacy",
        "repository": _repository_record(repo, project_root),
        "build_inputs": _tracked_build_inputs(repo, project_root),
        "index": {
            "path": "index.json",
            "sha256": file_sha256(project_root / "index.json"),
            "paper_count": len(papers_metadata),
            "legacy_ids": [paper["id"] for paper in papers_metadata],
        },
        "papers": papers,
        "summary": _summary(papers, True),
    }
    validate_legacy_baseline(baseline)
    return baseline


def legacy_index_projection(index: Mapping[str, Any]) -> Dict[str, Any]:
    """去掉身份迁移新增的三个键，还原迁移前的兼容 index 形状。"""
    projected = copy.deepcopy(dict(index))
    for key in _INDEX_ADDED_KEYS:
        projected.pop(key, None)
    papers = projected.get("papers")
    if not isinstance(papers, list):
        raise ValueError("index papers 必须是数组")
    for paper in papers:
        if not isinstance(paper, dict):
            raise ValueError("index paper 必须是对象")
        for key in _INDEX_PAPER_ADDED_KEYS:
            paper.pop(key, None)
    return projected


def recover_legacy_index(
    legacy: Mapping[str, Any], repo_root: Path
) -> Dict[str, Any]:
    """按 legacy 基线钉死的 HEAD 与 SHA-256，从 git 取回迁移前的 index.json。

    这是"旧 index 字段未变"唯一有效的锚点：迁移整体重写了 index.json（键序与缩进都
    变了），字节比较已不可能，而冻结基线里只留了那份 blob 的哈希。故必须 fail-closed
    ——取不到 blob 或哈希对不上一律报错，静默跳过等于让兼容投影比较失效。
    """
    repository = legacy.get("repository")
    index = legacy.get("index")
    if not isinstance(repository, Mapping) or not isinstance(index, Mapping):
        raise ValueError("legacy 基线缺少 repository/index，无法定位 git 锚点")
    head = repository.get("head")
    compile_path = repository.get("compile_path")
    relative = index.get("path")
    expected = index.get("sha256")
    if (
        not isinstance(head, str)
        or not head
        or not isinstance(compile_path, str)
        or not compile_path
        or not isinstance(relative, str)
        or not relative
        or _SHA256_RE.fullmatch(str(expected)) is None
    ):
        raise ValueError("legacy 基线的 git 锚点字段无效（head/compile_path/index）")
    target = (PurePosixPath(compile_path).parent / relative).as_posix()
    repo = _repository_root(Path(repo_root))
    try:
        blob = subprocess.check_output(
            ["git", "-C", str(repo), "show", f"{head}:{target}"],
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as error:
        raise ValueError(
            f"无法从 git 取回迁移前 index.json：{head}:{target}"
        ) from error
    actual = hashlib.sha256(blob).hexdigest()
    if actual != expected:
        raise ValueError(
            f"取回的迁移前 index.json 与 legacy 基线钉死的 SHA-256 不符：{actual} != {expected}"
        )
    try:
        recovered = json.loads(blob.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"迁移前 index.json 无效：{error}") from error
    if not isinstance(recovered, Mapping):
        raise ValueError("迁移前 index.json 顶层必须是对象")
    return recovered


def collect_current_baseline(
    project_root: Path,
    manifest: Mapping[str, Any],
    include_targets: bool = True,
) -> Dict[str, Any]:
    """采集身份迁移后的基线。

    `include_targets=False` 供 PDF 尚未重编译的检查点使用（配 `--sources-only`）。
    与 legacy 基线不同，这里不记录 `build_inputs`：迁移后工作树里的 tracked 源本来就
    可能正在被后续任务重新生成，记录它只会让只读比较无谓失败。
    """
    project_root = Path(project_root).resolve()
    index = _load_index(project_root)
    papers_metadata = index["papers"]
    # 迁移只准新增 paper_id/legacy_ids/batches：把 manifest 身份重新投影回兼容 index，
    # 必须逐字复原当前 index.json，否则说明迁移动了别的东西。
    if project_legacy_index(manifest, legacy_index_projection(index)) != index:
        raise ValueError("当前 index.json 不是 manifest 身份在兼容 index 上的投影")
    paper_ids: Dict[str, str] = {}
    for paper in manifest["papers"]:
        for legacy_id in paper["legacy_ids"]:
            paper_ids[legacy_id] = paper["paper_id"]

    repo = _repository_root(project_root)
    papers = []
    for metadata in papers_metadata:
        record = _paper_record(project_root, metadata, include_targets)
        legacy_id = record["legacy_id"]
        if legacy_id not in paper_ids:
            raise ValueError(f"manifest 未覆盖旧 ID：{legacy_id}")
        record["paper_id"] = paper_ids[legacy_id]
        papers.append(record)
    return {
        "baseline_version": 1,
        "kind": "current",
        "repository": _repository_record(repo, project_root),
        "index": {
            "path": "index.json",
            "sha256": file_sha256(project_root / "index.json"),
            "paper_count": len(papers_metadata),
            "legacy_ids": [paper["id"] for paper in papers_metadata],
            # 兼容投影随基线落盘，file-to-file 的 compare 才能比 index 深层字段。
            "legacy_compat": legacy_index_projection(index),
        },
        "papers": papers,
        "summary": _summary(papers, include_targets),
    }


def _picked(value: Mapping[str, Any], fields: Sequence[str]) -> Dict[str, Any]:
    return {field: value.get(field, _ABSENT) for field in fields}


def _comparable_warnings(warnings: Mapping[str, Any]) -> Dict[str, Any]:
    view = _picked(warnings, _COMPARED_WARNING_COUNTERS)
    for name in _COMPARED_WARNING_LISTS:
        entries = warnings.get(name)
        if not isinstance(entries, list) or any(
            not isinstance(entry, Mapping) for entry in entries
        ):
            raise ValueError(f"warnings.{name} 必须是对象数组")
        view[name] = [
            {key: entry[key] for key in sorted(entry) if key != "log_line"}
            for entry in entries
        ]
    return view


def _comparable_target(target: Mapping[str, Any]) -> Dict[str, Any]:
    view = _picked(target, _COMPARED_TARGET_FIELDS)
    warnings = target.get("warnings")
    if not isinstance(warnings, Mapping):
        raise ValueError("target 缺少 warnings")
    view["warnings"] = _comparable_warnings(warnings)
    return view


def _comparable_paper(paper: Mapping[str, Any], sources_only: bool) -> Dict[str, Any]:
    view = _picked(paper, _COMPARED_PAPER_FIELDS)
    if not sources_only:
        targets = paper.get("targets")
        if not isinstance(targets, list):
            raise ValueError(
                "基线未采集 PDF/log 目标，只能以 --sources-only 比较"
            )
        view["targets"] = [_comparable_target(target) for target in targets]
    return view


def _comparable(baseline: Mapping[str, Any], sources_only: bool) -> Dict[str, Any]:
    repository = baseline.get("repository")
    index = baseline.get("index")
    papers = baseline.get("papers")
    summary = baseline.get("summary")
    if (
        not isinstance(repository, Mapping)
        or not isinstance(index, Mapping)
        or not isinstance(papers, list)
        or not isinstance(summary, Mapping)
    ):
        raise ValueError("基线缺少 repository/index/papers/summary")
    if any(not isinstance(paper, Mapping) for paper in papers):
        raise ValueError("基线 paper 必须是对象")
    summary_fields = ("paper_count",)
    if not sources_only:
        summary_fields = summary_fields + _TARGET_SUMMARY_FIELDS
    view = _picked(baseline, _COMPARED_BASELINE_FIELDS)
    view.update({
        "repository": _picked(repository, _COMPARED_REPOSITORY_FIELDS),
        "index": _picked(index, _COMPARED_INDEX_FIELDS),
        "papers": [_comparable_paper(paper, sources_only) for paper in papers],
        "summary": _picked(summary, summary_fields),
    })
    return view


def _plain(value: Any) -> Any:
    return repr(value) if value is _ABSENT else value


def _diff(field: str, left: Any, right: Any, drift: List[Dict[str, Any]]) -> None:
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        for key in sorted(set(left) | set(right)):
            _diff(
                f"{field}.{key}" if field else str(key),
                left.get(key, _ABSENT),
                right.get(key, _ABSENT),
                drift,
            )
        return
    if isinstance(left, list) and isinstance(right, list):
        for position in range(max(len(left), len(right))):
            _diff(
                f"{field}[{position}]",
                left[position] if position < len(left) else _ABSENT,
                right[position] if position < len(right) else _ABSENT,
                drift,
            )
        return
    # 命中路径**且**两侧取值就是登记的那一对才豁免；对不上一律照旧计漂移——与
    # `_split_adjudicated()` 的双哈希放行判据同一口径。
    if left != right and _REWRITTEN_PAIRS.get(field) != (left, right):
        drift.append({
            "field": field, "legacy": _plain(left), "current": _plain(right),
        })


def with_legacy_compat(
    legacy: Mapping[str, Any], legacy_index: Optional[Mapping[str, Any]] = None
) -> Dict[str, Any]:
    """把迁移前 index 的兼容投影补进 legacy 基线，使两侧可对称比较。

    冻结的 legacy 基线（baseline_version 1）没有记录该投影，必须由
    `recover_legacy_index()` 从 git 锚点取回后传入；两处都没有就报错，不得静默跳过。
    """
    index = dict(legacy.get("index") or {})
    compat = legacy_index if legacy_index is not None else index.get("legacy_compat")
    if not isinstance(compat, Mapping):
        raise ValueError(
            "缺少迁移前 index 的兼容投影：须先用 recover_legacy_index() 由 git 锚点取回"
        )
    index["legacy_compat"] = compat
    normalized = dict(legacy)
    normalized["index"] = index
    return normalized


def load_adjudicated_drifts(
    path: Path = ADJUDICATED_DRIFTS_PATH,
) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """读已裁定漂移登记表，键为 (paper_id, artifact)。

    **缺文件 = 现状**：返回空表，于是所有漂移照旧未裁定。这条不能改成「缺文件即放行」
    ——那会让删掉一个文件就变成全面豁免。

    文件存在但内容不合格（版本号不对、字段缺失、哈希不是 sha256、class 不在名单、
    同一 (paper_id, artifact) 重复登记）一律**报错**：一张读不懂的登记表比没有更危险，
    静默降级成空表会把「登记表写坏了」伪装成「什么都没裁定过」。
    """
    path = Path(path)
    if not path.exists():
        return {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"无法读取已裁定漂移登记表：{path}: {error}") from error
    if not isinstance(document, Mapping):
        raise ValueError("已裁定漂移登记表顶层必须是对象")
    if document.get("ledger_version") != LEDGER_VERSION:
        raise ValueError(
            f"已裁定漂移登记表版本必须为 {LEDGER_VERSION}，实际 {document.get('ledger_version')!r}"
        )
    records = document.get("drifts")
    if not isinstance(records, list):
        raise ValueError("已裁定漂移登记表的 drifts 必须是数组")
    ledger: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError("已裁定漂移条目必须是对象")
        paper_id = record.get("paper_id")
        artifact = record.get("artifact")
        adjudicated_by = record.get("adjudicated_by")
        drift_class = record.get("class")
        if not all(
            isinstance(value, str) and value
            for value in (paper_id, artifact, adjudicated_by, drift_class)
        ):
            raise ValueError(f"已裁定漂移条目字段缺失或非字符串：{dict(record)}")
        if adjudicated_by not in ADJUDICATION_SOURCES:
            raise ValueError(f"未知的漂移裁定来源：{adjudicated_by!r}")
        if drift_class not in DRIFT_CLASSES:
            raise ValueError(f"未知的漂移类别：{drift_class!r}")
        if artifact not in CONTENT_FILES:
            raise ValueError(f"已裁定漂移只针对共享 TeX，未知 artifact：{artifact!r}")
        for field in ("legacy_sha256", "current_sha256"):
            if _SHA256_RE.fullmatch(str(record.get(field))) is None:
                raise ValueError(f"{paper_id}/{artifact} 的 {field} 不是 sha256")
        key = (paper_id, artifact)
        if key in ledger:
            raise ValueError(f"已裁定漂移重复登记：{key}")
        ledger[key] = dict(record)
    return ledger


def _split_adjudicated(
    drift: Sequence[Mapping[str, Any]],
    current: Mapping[str, Any],
    ledger: Mapping[Tuple[str, str], Mapping[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """把已裁定的漂移从清单里摘出来；**双哈希都精确匹配**才算数。

    legacy 侧对不上说明冻结基线被换过，current 侧对不上说明产物又变了一次——两种都
    必须重新报警，否则一次裁定就成了对该文件的永久免检。
    """
    papers = current.get("papers")
    remaining: List[Dict[str, Any]] = []
    adjudicated: List[Dict[str, Any]] = []
    for item in drift:
        matched = _CONTENT_DRIFT_FIELD.match(str(item.get("field")))
        record = None
        if matched is not None and isinstance(papers, list):
            position = int(matched.group(1))
            if position < len(papers) and isinstance(papers[position], Mapping):
                paper_id = papers[position].get("paper_id")
                candidate = ledger.get((paper_id, matched.group(2)))
                if (
                    candidate is not None
                    and candidate["legacy_sha256"] == item.get("legacy")
                    and candidate["current_sha256"] == item.get("current")
                ):
                    record = candidate
        if record is None:
            remaining.append(dict(item))
            continue
        entry = dict(item)
        entry.update({
            "paper_id": record["paper_id"],
            "artifact": record["artifact"],
            "class": record["class"],
            "adjudicated_by": record["adjudicated_by"],
        })
        adjudicated.append(entry)
    return remaining, adjudicated


def compare_baselines(
    legacy: Mapping[str, Any],
    current: Mapping[str, Any],
    sources_only: bool = False,
    legacy_index: Optional[Mapping[str, Any]] = None,
    adjudicated: Optional[Mapping[Tuple[str, str], Mapping[str, Any]]] = None,
) -> Dict[str, Any]:
    """比较 legacy 与迁移后基线；`drift` 为空即"零未裁定漂移"。

    `legacy_index` 是 `recover_legacy_index()` 从 git 锚点取回的迁移前 index.json；
    冻结的 legacy 基线里没有记录兼容投影，所以拿不到它就**报错而非跳过**——否则
    `structure`/`pdf_pages`/`title` 等深层字段会在"零漂移"的假象下失去保护。

    `_REVIEWED_FIELDS` 列出的字段不计漂移（不可复现，或身份迁移的正当新增），
    `_REWRITTEN_FIELDS` 登记的**「路径 + 取值对」**同样不计（两侧取值都与登记值逐字
    相等才放行，与已裁定漂移的双哈希口径一致；改成第三个值或整键删除都会重新报警）；
    两张表都会原样出现在报告的 `reviewed` 里——豁免必须是看得见的，不能只活在代码里；
    `adjudicated` 是 `load_adjudicated_drifts()` 读来的已裁定登记表，命中的漂移移入
    报告的 `adjudicated` 而不计入 `drift`；其余任何差异都是漂移。省略 `adjudicated`
    等于没有登记表，一切照旧报警。
    """
    if not isinstance(legacy, Mapping) or not isinstance(current, Mapping):
        raise ValueError("基线必须是对象")
    drift: List[Dict[str, Any]] = []
    _diff(
        "",
        _comparable(with_legacy_compat(legacy, legacy_index), sources_only),
        _comparable(current, sources_only),
        drift,
    )
    drift, resolved = _split_adjudicated(drift, current, adjudicated or {})
    return {
        "sources_only": sources_only,
        "drift": drift,
        "adjudicated": resolved,
        "reviewed": [
            {"field": _LEVEL_PATHS[level] + field, "reason": reason}
            for level, field, reason in _REVIEWED_FIELDS
        ] + [
            {
                "field": field, "reason": reason,
                "legacy": legacy_value, "current": current_value,
            }
            for field, legacy_value, current_value, reason in _REWRITTEN_FIELDS
        ],
        "summary": dict(current.get("summary") or {}),
    }


def validate_legacy_baseline(baseline: Mapping[str, Any]) -> None:
    if not isinstance(baseline, Mapping):
        raise ValueError("legacy baseline 顶层必须是对象")
    summary = baseline.get("summary")
    papers = baseline.get("papers")
    if not isinstance(summary, Mapping) or not isinstance(papers, list):
        raise ValueError("legacy baseline 缺少 summary/papers")
    exact = {
        "paper_count": 21,
        "target_count": 84,
        "total_pages": 1336,
        "hard_errors": 0,
        "missing_characters": 0,
        "undefined_references": 0,
        "overfull_count": 1,
    }
    for field, expected in exact.items():
        if summary.get(field) != expected:
            raise ValueError(
                f"legacy baseline {field} 必须为 {expected}，实际 {summary.get(field)}"
            )
    if len(papers) != 21:
        raise ValueError("legacy baseline 必须记录 21 套试卷")
    legacy_ids = []
    shells = []
    targets = []
    for paper in papers:
        if not isinstance(paper, Mapping):
            raise ValueError("legacy baseline paper 必须是对象")
        legacy_id = paper.get("legacy_id")
        if not isinstance(legacy_id, str) or not legacy_id:
            raise ValueError("legacy baseline paper 缺少 legacy_id")
        legacy_ids.append(legacy_id)
        project_dir = paper.get("project_dir")
        if not isinstance(project_dir, str) or not project_dir:
            raise ValueError(f"{legacy_id}: project_dir 无效")
        question_ids = paper.get("question_ids")
        if (
            not isinstance(question_ids, list)
            or not question_ids
            or question_ids != list(range(1, len(question_ids) + 1))
        ):
            raise ValueError(f"{legacy_id}: 题号序列无效")
        content_sha256 = paper.get("content_sha256")
        if (
            not isinstance(content_sha256, Mapping)
            or set(content_sha256) != set(CONTENT_FILES)
            or any(
                _SHA256_RE.fullmatch(str(content_sha256.get(name))) is None
                for name in CONTENT_FILES
            )
        ):
            raise ValueError(f"{legacy_id}: 共享内容 SHA-256 无效")
        figures = paper.get("figures")
        if not isinstance(figures, list) or any(
            not isinstance(figure, Mapping)
            or not isinstance(figure.get("path"), str)
            or not figure["path"].startswith(project_dir + "/figures/")
            or _SHA256_RE.fullmatch(str(figure.get("sha256"))) is None
            for figure in figures
        ):
            raise ValueError(f"{legacy_id}: figure tree 无效")
        figure_paths = [figure["path"] for figure in figures]
        if figure_paths != sorted(figure_paths) or len(figure_paths) != len(set(figure_paths)):
            raise ValueError(f"{legacy_id}: figure tree 路径必须唯一排序")

        paper_shells = paper.get("shells")
        paper_targets = paper.get("targets")
        if not isinstance(paper_shells, list) or len(paper_shells) != 4:
            raise ValueError(f"{legacy_id}: legacy 壳必须恰有四份")
        if not isinstance(paper_targets, list) or len(paper_targets) != 4:
            raise ValueError(f"{legacy_id}: PDF/log 目标必须恰有四份")
        if any(not isinstance(item, Mapping) for item in paper_shells + paper_targets):
            raise ValueError(f"{legacy_id}: 壳或目标记录必须是对象")
        shell_editions = {shell.get("edition") for shell in paper_shells}
        target_editions = {target.get("edition") for target in paper_targets}
        if shell_editions != set(EDITIONS) or target_editions != set(EDITIONS):
            raise ValueError(f"{legacy_id}: 壳或目标版本集合不完整")
        if any(shell.get("paper_id") != legacy_id for shell in paper_shells):
            raise ValueError(f"{legacy_id}: 壳 paper_id 漂移")
        if any(
            shell.get("path") != f"{project_dir}/{shell.get('edition')}.tex"
            or _SHA256_RE.fullmatch(str(shell.get("sha256"))) is None
            for shell in paper_shells
        ):
            raise ValueError(f"{legacy_id}: 壳路径或 SHA-256 无效")
        if any(
            target.get("path") != f"{project_dir}/{target.get('edition')}.pdf"
            or target.get("log_path") != f"{project_dir}/{target.get('edition')}.log"
            for target in paper_targets
        ):
            raise ValueError(f"{legacy_id}: PDF/log 目标路径无效")
        shells.extend(paper_shells)
        targets.extend(paper_targets)
    if len(legacy_ids) != len(set(legacy_ids)):
        raise ValueError("legacy baseline 旧 ID 不唯一")
    index = baseline.get("index")
    if not isinstance(index, Mapping) or index.get("legacy_ids") != legacy_ids:
        raise ValueError("legacy baseline index 旧 ID 与 paper 顺序不一致")
    if len(shells) != 84 or len(targets) != 84:
        raise ValueError("legacy baseline 必须记录 84 个壳和 84 个 PDF/log 目标")
    if any(
        isinstance(target.get("pages"), bool)
        or not isinstance(target.get("pages"), int)
        or target["pages"] <= 0
        or _SHA256_RE.fullmatch(str(target.get("pdf_sha256"))) is None
        or _SHA256_RE.fullmatch(str(target.get("log_sha256"))) is None
        or not isinstance(target.get("warnings"), Mapping)
        for target in targets
    ):
        raise ValueError("legacy baseline PDF/log 目标记录无效")
    if sum(target["pages"] for target in targets) != 1336:
        raise ValueError("legacy baseline 目标页数之和必须为 1336")
    derived_warning_summary = {
        "hard_errors": sum(
            target["warnings"].get("hard_errors", -1) for target in targets
        ),
        "missing_characters": sum(
            target["warnings"].get("missing_characters", -1) for target in targets
        ),
        "undefined_references": sum(
            target["warnings"].get("undefined_references", -1) for target in targets
        ),
        "overfull_count": sum(
            len(target["warnings"].get("overfull", [])) for target in targets
        ),
    }
    if any(summary.get(key) != value for key, value in derived_warning_summary.items()):
        raise ValueError("legacy baseline warning summary 与目标记录不一致")

    build_inputs = baseline.get("build_inputs")
    if not isinstance(build_inputs, Mapping):
        raise ValueError("legacy baseline 缺少 build_inputs")
    files = build_inputs.get("files")
    if not isinstance(files, list) or not files:
        raise ValueError("legacy baseline build input files 必须是非空数组")
    paths = [item.get("path") for item in files if isinstance(item, Mapping)]
    if len(paths) != len(files) or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise ValueError("legacy baseline build input 路径必须唯一排序")
    if any(
        not isinstance(item.get("path"), str)
        or Path(item["path"]).suffix not in _BUILD_INPUT_SUFFIXES
        or _SHA256_RE.fullmatch(str(item.get("sha256"))) is None
        for item in files
    ):
        raise ValueError("legacy baseline build input 记录无效")
    if build_inputs.get("tree_sha256") != _record_tree_sha256(files):
        raise ValueError("legacy baseline build input tree SHA-256 不匹配")
    overfull = [
        (target.get("path"), warning)
        for target in targets
        for warning in target.get("warnings", {}).get("overfull", [])
    ]
    if len(overfull) != 1:
        raise ValueError("legacy baseline 必须只有一条 Overfull")
    path, warning = overfull[0]
    if path != "2025_全国2卷/印刷版.pdf" or warning.get("width_pt") != "0.4588":
        raise ValueError("legacy baseline 唯一 Overfull 必须是 2025 全国2 印刷版 0.4588pt")


def _load_baseline(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"无法读取 legacy baseline：{path}: {error}") from error
    if not isinstance(value, Mapping):
        raise ValueError("legacy baseline 顶层必须是对象")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="冻结并比较 LaTeX 构建基线")
    subparsers = parser.add_subparsers(dest="command", required=True)
    write = subparsers.add_parser("write-legacy")
    write.add_argument("--project-root", required=True, type=Path)
    write.add_argument("--output", required=True, type=Path)
    current = subparsers.add_parser("write-current")
    current.add_argument("--manifest", required=True, type=Path)
    current.add_argument("--output", required=True, type=Path)
    # 省略时取 manifest 所在目录，即规范工程根目录。
    current.add_argument("--project-root", type=Path, default=None)
    compare = subparsers.add_parser("compare")
    compare.add_argument("--legacy", required=True, type=Path)
    compare.add_argument("--current", required=True, type=Path)
    compare.add_argument("--sources-only", action="store_true")
    compare.add_argument("--adjudicated", type=Path, default=ADJUDICATED_DRIFTS_PATH)
    working = subparsers.add_parser("compare-working")
    working.add_argument("--legacy", required=True, type=Path)
    working.add_argument("--project-root", required=True, type=Path)
    working.add_argument("--manifest", required=True, type=Path)
    working.add_argument("--sources-only", action="store_true")
    working.add_argument("--adjudicated", type=Path, default=ADJUDICATED_DRIFTS_PATH)
    check = subparsers.add_parser("check-legacy")
    check.add_argument("--baseline", required=True, type=Path)
    return parser


def _print_report(report: Mapping[str, Any]) -> int:
    summary = report["summary"]
    if report["sources_only"]:
        print("仅比较来源维度：index 兼容投影、旧 ID、84 壳、共享 TeX、题号、figure tree")
    else:
        print(
            "目标 {0} 个、总页数 {1}、Overfull {2} 条".format(
                summary.get("target_count"),
                summary.get("total_pages"),
                summary.get("overfull_count"),
            )
        )
    for item in report["reviewed"]:
        print("已审查（不计漂移）：{0} —— {1}".format(item["field"], item["reason"]))
    adjudicated = report.get("adjudicated") or []
    if adjudicated:
        counts: Dict[str, int] = {}
        for item in adjudicated:
            counts[item["class"]] = counts.get(item["class"], 0) + 1
        print(
            "已裁定漂移 {0} 条（{1}）".format(
                len(adjudicated),
                "、".join(f"{name} {counts[name]}" for name in sorted(counts)),
            )
        )
    if not report["drift"]:
        print("零未裁定漂移")
        return 0
    for item in report["drift"]:
        print(
            "漂移：{0}：legacy={1!r} current={2!r}".format(
                item["field"], item["legacy"], item["current"]
            ),
            file=os.sys.stderr,
        )
    print(f"共 {len(report['drift'])} 处未裁定漂移", file=os.sys.stderr)
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.command == "write-legacy":
        atomic_write_json(
            arguments.output,
            collect_legacy_baseline(arguments.project_root),
        )
        return 0
    if arguments.command == "write-current":
        project_root = arguments.project_root or arguments.manifest.parent
        # 写 tracked 文件：先取仓库锁并恢复未完成事务，再单文件原子替换。
        with RepoLock(project_root):
            baseline = collect_current_baseline(
                project_root, load_manifest(arguments.manifest)
            )
            atomic_write_json(arguments.output, baseline)
        return 0
    if arguments.command == "check-legacy":
        validate_legacy_baseline(_load_baseline(arguments.baseline))
        return 0
    legacy = _load_baseline(arguments.legacy)
    validate_legacy_baseline(legacy)
    if arguments.command == "compare":
        current = _load_baseline(arguments.current)
        # 基线文件可以放在仓库外，但迁移前的 blob 一定在本工具所属的仓库里。
        repo_root = Path(__file__).resolve().parent
    else:
        current = collect_current_baseline(
            arguments.project_root,
            load_manifest(arguments.manifest),
            include_targets=not arguments.sources_only,
        )
        repo_root = arguments.project_root
    return _print_report(
        compare_baselines(
            legacy,
            current,
            arguments.sources_only,
            recover_legacy_index(legacy, repo_root),
            load_adjudicated_drifts(arguments.adjudicated),
        )
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=os.sys.stderr)
        raise SystemExit(1)

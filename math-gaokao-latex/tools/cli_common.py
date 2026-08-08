#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cli_common.py —— manifest 驱动的三个生成器共用的 CLI 骨架与仓库小件。

`generate_projects.py` / `make_editions.py` / `make_short_answers.py` 是同一个形状：
`--all|--batch|--paper` × `--write|--check`，全批目标先在内存生成、校验全过后以**一个**
Task 1 `content` 事务提交，`--check` 只读比对。这套骨架原本是三份近逐字重复的副本——
任一处修 bug 要改三处，而**没有任何测试能发现只改了两处**。这里收敛成一份。

差异点全部参数化，共四类：

- `error_type`：各工具抛自己的异常类（`GenerationError` / `EditionError` /
  `ShortAnswerError`），调用方据此区分失败来源；
- `build`：把 manifest 里的一条 paper 折成该工具的输入对象（`paper_sources` /
  `paper_shell` / 带结构表的 `paper_sources`）；
- `fixed_inputs`：该工具**与卷无关**的只读输入（工具源码、模板、转换器源码等）；
- 打印文案：`target_unit`（个目标 / 个壳 / 份简答）与 `check_message`。

**本模块只做机械抽取，不改行为**：错误文案、退出码、互斥组、事务输入清单的构成方式
全部逐字沿用三份副本原样，各工具的冻结契约测试不需要任何修改。

`commit_content()` 对 `results` 只要求两个属性：`inputs`（仓库相对的只读输入路径）与
`targets`（仓库相对路径 -> 目标字节）。三个工具的结果 dataclass 都满足，无需继承。
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from manifest import file_sha256
from transaction import Transaction

ErrorType = Callable[[str], BaseException]


# ---------------------------------------------------------------- 仓库小件


def repository_root(path: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(Path(path).resolve()), "rev-parse", "--show-toplevel"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return Path(result.stdout.strip()).resolve()


def relative_to_repo(root: Path, path: Path, error_type: ErrorType) -> str:
    try:
        return Path(path).resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise error_type(f"路径不在仓库内：{path}") from error


def read_text(path: Path, error_type: ErrorType) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise error_type(f"无法读取 {path}：{error}") from error


def required_sha256(root: Path, relative: str, error_type: ErrorType) -> str:
    """只读输入必须存在：缺一个就说明这批目标算不出来，绝不用 None 混过去。"""
    path = Path(root) / relative
    if not path.is_file():
        raise error_type(f"只读输入缺失：{relative}")
    return file_sha256(path)


# ---------------------------------------------------------------- 暂存区门禁


def git_lines(root: Path, arguments: Sequence[str]) -> List[str]:
    raw = subprocess.run(
        ["git", "-C", str(root)] + list(arguments),
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout
    return [item.decode("utf-8") for item in raw.split(b"\0") if item]


def read_pathspec(path: Path, error_type: ErrorType) -> List[str]:
    """读 NUL 分隔的 pathspec 文件；每条都必须是安全的仓库相对路径。

    `error_type` 参数化的理由同 `relative_to_repo()`：各工具抛自己的异常类，调用方据此
    区分失败来源，而门禁逻辑只此一份。
    """
    try:
        raw = Path(path).read_bytes()
    except OSError as error:
        raise error_type(f"无法读取 pathspec 文件：{path}：{error}") from error
    entries: List[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            entry = item.decode("utf-8")
        except UnicodeDecodeError as error:
            raise error_type("pathspec 文件中存在非 UTF-8 路径") from error
        candidate = Path(entry)
        if candidate.is_absolute() or any(
            part in {"", ".", ".."} for part in candidate.parts
        ):
            raise error_type(f"pathspec 必须是安全的仓库相对路径：{entry}")
        entries.append(candidate.as_posix())
    if not entries:
        raise error_type(f"pathspec 文件为空：{path}")
    return entries


def check_staged(root: Path, scope: Sequence[str]) -> List[str]:
    """核对暂存区恰好覆盖所有权范围内相对 HEAD 的实际变更。

    返回问题清单；空清单表示通过。字节未变的目标不要求出现在 staged diff 里。

    **只此一份**：`solution_sources.py` 与 `build_projects.py` 曾各存一份逐字副本，
    那意味着修了一处、另一处照旧，而没有任何测试会发现只改了一处。
    """
    scoped = set(scope)
    staged = set(git_lines(root, ["diff", "--cached", "--name-only", "-z", "HEAD", "--"]))
    unstaged = set(git_lines(root, ["diff", "--name-only", "-z", "--"]))
    untracked = set(git_lines(root, ["ls-files", "--others", "--exclude-standard", "-z"]))
    # 相对 HEAD 的实际变更/新增/删除：tracked 侧由 diff HEAD 给出，新增文件补上 untracked。
    actual = set(git_lines(root, ["diff", "--name-only", "-z", "HEAD", "--"])) | untracked

    problems: List[str] = []
    outside = sorted(staged - scoped)
    if outside:
        problems.append(f"范围外存在 staged 变更：{outside}")
    missing = sorted((actual & scoped) - staged)
    if missing:
        problems.append(f"范围内的实际变更未全部 staged：{missing}")
    residue = sorted((unstaged | untracked) & scoped)
    if residue:
        problems.append(f"范围内存在 unstaged 残留：{residue}")
    return problems


# ---------------------------------------------------------------- 选择器


def select_papers(
    manifest: Mapping[str, Any],
    selector: str,
    value: Optional[str],
    build: Callable[[Mapping[str, Any]], Any],
    error_type: ErrorType,
) -> Tuple[Any, ...]:
    """按 `all|batch|paper` 从 manifest 取卷，逐条交给 `build` 折成工具自己的输入对象。"""
    papers = {paper["paper_id"]: paper for paper in manifest["papers"]}
    if selector == "all":
        return tuple(build(paper) for paper in manifest["papers"])
    if selector == "paper":
        if value not in papers:
            raise error_type(f"未知 paper_id：{value}")
        return (build(papers[value]),)
    if selector == "batch":
        batches = [item for item in manifest["batches"] if item["batch_id"] == value]
        if len(batches) != 1:
            raise error_type(f"未知批次：{value}")
        selected = []
        for paper_id in batches[0]["paper_ids"]:
            if paper_id not in papers:
                raise error_type(f"批次 {value} 引用了不存在的 paper_id：{paper_id}")
            selected.append(build(papers[paper_id]))
        return tuple(selected)
    raise error_type(f"未知选择器：{selector}")


# ---------------------------------------------------------------- 提交与比对


def commit_content(
    root: Path,
    manifest_path: Path,
    manifest_target: str,
    fixed_inputs: Sequence[str],
    results: Sequence[Any],
    error_type: ErrorType,
    extra_targets: Optional[Mapping[str, bytes]] = None,
    event_hook: Any = None,
) -> Dict[str, Any]:
    """把全批目标放进**一个** `content` 事务提交；全等则跳过，不做空事务。"""
    root = Path(root)
    manifest_relative = relative_to_repo(root, Path(manifest_path), error_type)
    if manifest_relative != manifest_target:
        raise error_type(f"manifest 必须是 {manifest_target}，实际 {manifest_relative}")

    inputs: Dict[str, Optional[str]] = {
        manifest_relative: required_sha256(root, manifest_relative, error_type)
    }
    for relative in fixed_inputs:
        inputs[relative] = required_sha256(root, relative, error_type)

    targets: Dict[str, bytes] = dict(extra_targets or {})
    for result in results:
        for relative in result.inputs:
            inputs[relative] = required_sha256(root, relative, error_type)
        for relative, value in result.targets.items():
            if relative in targets:
                raise error_type(f"批内目标路径重复：{relative}")
            targets[relative] = value

    # 被重写的目标绝不能同时充当只读输入——那等于拿新值去 CAS 旧值。
    overlap = sorted(set(inputs) & set(targets))
    if overlap:
        raise error_type(f"只读输入与写目标重叠：{overlap}")

    unchanged = all(
        (root / relative).is_file() and (root / relative).read_bytes() == value
        for relative, value in targets.items()
    )
    if unchanged:
        return {"written": False, "targets": sorted(targets)}

    transaction = Transaction(root, event_hook=event_hook)
    transaction.prepare("content", targets, inputs)
    transaction.commit()
    return {"written": True, "targets": sorted(targets)}


def compare_targets(
    root: Path,
    results: Sequence[Any],
    extra_targets: Optional[Mapping[str, bytes]] = None,
) -> Tuple[List[str], List[str]]:
    """`--check` 的只读比对：返回 (问题清单, 目标路径清单)，一个字节都不写。"""
    problems: List[str] = []
    listed: List[str] = []
    pairs = [
        (relative, value)
        for result in results for relative, value in sorted(result.targets.items())
    ]
    pairs += sorted((extra_targets or {}).items())
    for relative, expected in pairs:
        listed.append(relative)
        path = Path(root) / relative
        if not path.is_file() or path.read_bytes() != expected:
            problems.append(f"{relative} 与生成结果不一致")
    return problems, sorted(listed)


# ---------------------------------------------------------------- 命令行


def build_parser(description: str, default_manifest: Path) -> argparse.ArgumentParser:
    """两个互斥组都是必选：默认值会让「以为在只读比对，其实写了盘」成为可能。"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--manifest", default=str(default_manifest))
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--all", action="store_true", help="全部试卷")
    selector.add_argument("--batch", metavar="BATCH_ID", help="按批次")
    selector.add_argument("--paper", metavar="PAPER_ID", help="按 manifest paper_id")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="校验全过后原子写入")
    mode.add_argument("--check", action="store_true", help="只读比对，绝不落盘")
    return parser


def selection(arguments: argparse.Namespace) -> Tuple[str, Optional[str]]:
    if arguments.all:
        return "all", None
    if arguments.batch is not None:
        return "batch", arguments.batch
    return "paper", arguments.paper


def execute(
    runner: Callable[[], Mapping[str, Any]],
    write: bool,
    target_unit: str,
    check_message: str,
) -> int:
    """跑 `run()` 并把报告落成退出码契约：0 全过、1 校验失败或输入无效。

    命令行用法错（2）由 argparse 在更早的 `parse_args()` 里以 SystemExit 抛出。
    """
    try:
        report = runner()
    except ValueError as error:
        print("✗", error)
        return 1
    for problem in report["problems"]:
        print("  ✗", problem)
    if report["problems"]:
        print("\n== 校验失败：%d 项 ==" % len(report["problems"]))
        return 1
    if write:
        print(
            "✓ %d 套试卷，%s%d %s"
            % (
                len(report["papers"]),
                "已写入 " if report["written"] else "无需改动 ",
                len(report["targets"]),
                target_unit,
            )
        )
    else:
        print("✓ %d %s" % (len(report["papers"]), check_message))
    return 0

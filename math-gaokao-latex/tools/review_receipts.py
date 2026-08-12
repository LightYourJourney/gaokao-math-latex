#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""review_receipts.py —— 视觉候选页、review 回执、批次聚合与单事务 finalizer。

**一份 review 回执的唯一价值和 build 回执一样：可反驳。** 它必须能被后来的任何人用手上
的字节重新验算一遍——同一次 attempt、同一份 manifest 投影、同两棵输入树、同一条工具链、
同一批 PDF 的 SHA 与页数、以及同一对 pdftotext/pdftoppm 指纹。任一项对不上，这份裁决就
不是「稍旧」而是**不成立**（`is_stale()`）。

三条不建第二套的纪律：

1. **状态判断只在 `status.py`**——本模块不自己算 paper/batch 状态，只把观察折成 facts
   递给 `derive_content_outcome()` / `derive_status()` / `reconcile_batch_status()`；
2. **升级判断只在 `build_projects.finalize_receipt()`**——「凭什么可以从
   `compiled_pending_review` 变成 `succeeded`」那套逐项核对住在那里，本模块只调用；
   report-only 复核走 `_revalidate_final()`：把现成的 `succeeded` 回执降回
   `compiled_pending_review` 再跑同一把尺子，跑完必须逐字节等于原件；
3. **事务与 reconciler 只在 `build_projects._commit_state()/_reconciled_manifest()`**
   ——抄一份出来就是第二套 reconciler，混合状态下不会报错，只会静默给出两个都自洽的答案。

候选页启发式（`candidate_pages()`）是**诚实的**：三个指标（pdftotext 每页非空白字符数、
数学符号计数、pdftoppm 灰度图非白像素比）在同一 PDF 内 min-max 归一化后等权平均，最高分
标为重点二次复核锚点。它不宣称理解公式或 TikZ，**更不缩小全页审查集合**——`pages` 永远
必须精确覆盖 `1..page_count`。

⚠️ build 回执的 `log.overfull` 是**混装**的，三个坑连在一起（T23 实证）：

1. Overfull 与 Underfull 两类共处一个数组，靠每条的 `kind` 区分；
2. **`width_pt` 是 JSON 字符串不是数字**，且 **Underfull 的 `width_pt` 是必填的 `null`**
   （不是「没有这个字段」）。`float(None)` 是 TypeError；而直接对字符串排序/比阈值更坏
   ——它**静默**按字典序错排（`"86.97256" > "506.01268"` 为真）。故：与 build 回执的匹配
   一律用**逐字相等的多重集比对**（`Counter`，不排序、不数值化），任何需要顺序的地方先按
   `kind` 分流再 `float()`（见 `_warning_sort_key()`）；
3. 日志的 `at lines` **不带文件名**，行号指向被 `\\input` 的内容文件（实测是 `answers.tex`）
   而非二三十行的版本壳。因此豁免必须另写 `source_file`——只有行号的「源行」无法复核。

退出码（`--json` 时调用方必须同时校验 `code`）：0=`FINALIZED`、2=usage、
4=`VISUAL_FAILED`（诊断状态已事务保存）、6=`INVALID_OR_STALE`（零修改）。
"""
from __future__ import annotations

import argparse
import collections
import copy
import datetime
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent                       # math-gaokao-latex
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_projects
import cli_common
import issues as issues_module
import status as status_core
from manifest import canonical_json, load_manifest
from schema_validate import SchemaError
from schema_validate import validate as validate_schema
from status import (
    ISSUES_TARGET,
    MANIFEST_TARGET,
    PROJECT_RELATIVE,
    StatusError,
    build_receipt_path,
    derive_content_outcome,
    facts_without_report,
    review_receipt_path,
)
from transaction import RepoLock

DEFAULT_MANIFEST = PROJECT_ROOT / "source-manifest.json"
DEFAULT_ISSUES = PROJECT_ROOT / "missing-issues.md"

EDITIONS: Tuple[str, ...] = build_projects.EDITIONS
WORK_RELATIVE = PROJECT_RELATIVE + "/.work"
REPORTS_RELATIVE = PROJECT_RELATIVE + "/reports"
SCHEMA_TARGET = PROJECT_RELATIVE + "/schemas/review-receipt.schema.json"

REVIEW_STATES: Tuple[str, ...] = ("pending", "passed", "failed")
PAGE_RESULTS: Tuple[str, ...] = ("pass", "fail")
CHECK_RESULTS: Tuple[str, ...] = ("pass", "fail", "not_applicable")

# 八项统一检查，逐页全覆盖。少一项不是「省了一步」，而是这一页根本没被完整看过。
CHECK_CODES: Tuple[str, ...] = (
    "glyph",                     # 字形（缺字、豆腐块、错误回退字体）
    "heading_number",            # 标题与题号
    "option_formula_alignment",  # 选项与公式对齐
    "figure_label",              # 图形与标注
    "header_footer",             # 页眉页脚
    "pagination_whitespace",     # 分页、空白与重复
    "font_size",                 # 字号
    "answer_leak",               # 答案泄漏
)

VISUAL_TOOL_NAMES: Tuple[str, ...] = ("pdftoppm", "pdftotext")

# 数学符号代理。刻意只数**符号**：它不理解公式，只用于把「这一页符号密」抬进锚点集合。
MATH_GLYPHS = frozenset("=+-×÷∑∫√≤≥∈")

CANDIDATE_DPI = 36
_INK_THRESHOLD = 250  # 8 位灰度里低于此值即算「有墨」

EXIT_FINALIZED = 0
EXIT_USAGE = 2
EXIT_VISUAL_FAILED = 4
EXIT_INVALID = 6

ISSUE_ORIGIN = "visual-review"
ISSUE_TYPE = "layout-warning"
ISSUE_FIGURE_MARKER = "visual-review"

DIAGNOSTIC_MESSAGE_TEMPLATE = "fix(exams): 保存 %s 视觉审查诊断状态"


class ReviewError(ValueError):
    """视觉审查层的唯一异常类型：结构、绑定、当前性或门禁不成立。"""


class UsageError(ReviewError):
    """调用方把命令写错了（未知批次、路径不规范）。退出码 2，与 6 区分开。"""


# ---------------------------------------------------------------- 小件


def _now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()


def _relative_to(root: Path, path: Path) -> str:
    try:
        return Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError as error:
        raise UsageError(f"路径不在仓库内：{path}") from error


def _require_canonical(root: Path, path: Path, target: str, flag: str) -> Path:
    resolved = Path(path).resolve()
    if _relative_to(root, resolved) != target:
        raise UsageError(f"{flag} 必须是 {target}")
    return resolved


def _paper(manifest: Mapping[str, Any], paper_id: str) -> Mapping[str, Any]:
    for paper in manifest.get("papers", []):
        if paper["paper_id"] == paper_id:
            return paper
    raise UsageError(f"未知 paper_id：{paper_id}")


def _batch(manifest: Mapping[str, Any], batch_id: str) -> Mapping[str, Any]:
    found = [
        item for item in manifest.get("batches", []) if item["batch_id"] == batch_id
    ]
    if len(found) != 1:
        raise UsageError(f"未知批次：{batch_id}")
    return found[0]


def _validate_batch_size(
    manifest: Mapping[str, Any], batch_id: str
) -> Mapping[str, Any]:
    batch = _batch(manifest, batch_id)
    count = len(batch["paper_ids"])
    if count < 2 or count > 4:
        raise ReviewError(
            "%s 必须包含 2–4 套试卷，实际 %d 套" % (batch_id, count)
        )
    return batch


def _assert_safe_relative(relative: str) -> str:
    candidate = PurePosixPath(str(relative))
    if candidate.is_absolute() or any(
        part in {"", ".", ".."} for part in candidate.parts
    ):
        raise ReviewError(f"路径必须是安全的仓库相对路径：{relative}")
    return candidate.as_posix()


def report_target(batch_id: str) -> str:
    """批次报告的规范路径。只此一份拼法——报告既是事务目标又是 ownership path。"""
    return "%s/%s.md" % (REPORTS_RELATIVE, batch_id)


def _require_report_path(root: Path, path: Path, batch_id: str) -> str:
    expected = report_target(batch_id)
    relative = _relative_to(root, Path(path))
    if relative != expected:
        raise UsageError(f"--output-report 必须是 {expected}，实际 {relative}")
    return expected


def _validated_work_dir(root: Path, work_dir: Optional[Path] = None) -> Path:
    """work 目录必须落在 ignored 的 `.work` 内。

    与 `provenance._validated_work_dir()` 同一条理由：`.work/` 已被 `.gitignore` 覆盖，
    写到别处就等于把未核验的中间态放进了 tracked 树。
    """
    allowed = (Path(root) / WORK_RELATIVE).resolve()
    resolved = allowed if work_dir is None else Path(work_dir).resolve()
    if resolved != allowed and allowed not in resolved.parents:
        raise UsageError(f"work 目录必须落在 {WORK_RELATIVE} 之内：{resolved}")
    return resolved


def work_item_path(work_dir: Path, batch_id: str, edition: str, paper_id: str) -> Path:
    """四个版本代理各写各的一条独占路径，互不相交。"""
    if edition not in EDITIONS:
        raise UsageError(f"未知版本：{edition}")
    return Path(work_dir) / batch_id / "review" / edition / ("%s.json" % paper_id)


# ---------------------------------------------------------------- Schema 与形状


_SCHEMA_CACHE: Dict[str, Any] = {}


def review_schema() -> Mapping[str, Any]:
    if "schema" not in _SCHEMA_CACHE:
        _SCHEMA_CACHE["schema"] = json.loads(
            (PROJECT_ROOT / "schemas" / "review-receipt.schema.json").read_text(
                encoding="utf-8"
            )
        )
    return _SCHEMA_CACHE["schema"]


def _validate_pages(edition: Mapping[str, Any]) -> None:
    """页集合必须**精确**覆盖 `1..page_count`，且每页八项检查齐全。

    缺页/重页/越界三种形态分开报：它们的成因完全不同（漏审 / 复制粘贴 / 页码错位），
    合成一句「页集合不对」会让执行者不知道该去查哪一种。
    """
    count = edition["page_count"]
    numbers = [item["page"] for item in edition["pages"]]
    duplicates = sorted({item for item in numbers if numbers.count(item) > 1})
    if duplicates:
        raise ReviewError("%s 存在重页：%s" % (edition["edition"], duplicates))
    out_of_range = sorted(item for item in numbers if item < 1 or item > count)
    if out_of_range:
        raise ReviewError("%s 存在越界页：%s" % (edition["edition"], out_of_range))
    missing = sorted(set(range(1, count + 1)) - set(numbers))
    if missing:
        raise ReviewError("%s 缺页：%s" % (edition["edition"], missing))

    for page in edition["pages"]:
        codes = [item["check"] for item in page["checks"]]
        if sorted(codes) != sorted(CHECK_CODES):
            raise ReviewError(
                "%s 第 %d 页的检查项不是完整八项：%s"
                % (edition["edition"], page["page"], sorted(codes))
            )
        for check in page["checks"]:
            if check["result"] != "pass" and not check["note"].strip():
                raise ReviewError(
                    "%s 第 %d 页的 %s 是 %s，必须写明理由"
                    % (
                        edition["edition"], page["page"], check["check"],
                        check["result"],
                    )
                )
        failed = [item["check"] for item in page["checks"] if item["result"] == "fail"]
        if failed and page["result"] != "fail":
            raise ReviewError(
                "%s 第 %d 页有 fail 检查项却判为 %s"
                % (edition["edition"], page["page"], page["result"])
            )
        if not failed and page["result"] != "pass":
            raise ReviewError(
                "%s 第 %d 页没有 fail 检查项却判为 %s"
                % (edition["edition"], page["page"], page["result"])
            )

    anchors = sorted(set(edition["candidate_pages"]))
    stray = [item for item in anchors if item < 1 or item > count]
    if stray:
        raise ReviewError("%s 的候选锚点越界：%s" % (edition["edition"], stray))
    override = edition["candidate_override"]
    if override is not None:
        for field in ("original_pages", "chosen_pages"):
            bad = [item for item in override[field] if item < 1 or item > count]
            if bad:
                raise ReviewError(
                    "%s 的 candidate_override.%s 越界：%s"
                    % (edition["edition"], field, bad)
                )
        if sorted(set(override["chosen_pages"])) != anchors:
            raise ReviewError(
                "%s 的 candidate_pages 必须等于 candidate_override.chosen_pages"
                % edition["edition"]
            )


def validate_review(receipt: Mapping[str, Any]) -> None:
    """Schema + 形状。受限验证器没有 if/then，跨字段的约束全部落在这里。"""
    try:
        validate_schema(receipt, review_schema())
    except SchemaError as error:
        raise ReviewError(f"review 回执不符合 Schema：{error}") from error

    editions = [item["edition"] for item in receipt["editions"]]
    if receipt["status"] != "pending" and tuple(editions) != EDITIONS:
        raise ReviewError(f"正式 review 必须恰好四版本且顺序固定，实际 {editions}")
    if len(set(editions)) != len(editions):
        raise ReviewError(f"review 版本重复：{editions}")

    for edition in receipt["editions"]:
        _validate_pages(edition)
        failed = [item["page"] for item in edition["pages"] if item["result"] == "fail"]
        if failed and edition["result"] != "fail":
            raise ReviewError(
                "%s 有 fail 页却判为 %s" % (edition["edition"], edition["result"])
            )
        if not failed and edition["result"] != "pass":
            raise ReviewError(
                "%s 没有 fail 页却判为 %s" % (edition["edition"], edition["result"])
            )

    counts = {item["edition"]: item["page_count"] for item in receipt["editions"]}
    for item in receipt["warning_exemptions"]:
        if item["edition"] not in counts:
            raise ReviewError("警告豁免引用了不存在的版本：%s" % item["edition"])
        if item["pdf_page"] > counts[item["edition"]]:
            raise ReviewError(
                "%s 的警告豁免 pdf_page 越界：%s"
                % (item["edition"], item["pdf_page"])
            )
        if (item["width_pt"] is None) != (item["kind"] == "Underfull"):
            # Underfull 没有「超出多少 pt」这回事（回执里恒为 null）；Overfull 一定有。
            # 把两者混着写，逐项匹配就会在真实回执上悄悄错位。
            raise ReviewError(
                "%s 的 %s 豁免与 width_pt=%r 不相容"
                % (item["edition"], item["kind"], item["width_pt"])
            )
        # 行号必须有归属：日志的 `at lines` 不带文件名，实测指向 answers.tex 这类被
        # \input 的内容文件而非版本壳。只有数字的「源行」是复核不了的。
        _assert_safe_relative(item["source_file"])

    any_fail = any(item["result"] == "fail" for item in receipt["editions"])
    if receipt["status"] == "passed":
        if any_fail:
            raise ReviewError("passed 的 review 里出现了 fail 版本")
        vetoed = [
            item["edition"] for item in receipt["warning_exemptions"]
            if item["visual_result"] == "fail"
        ]
        if vetoed:
            raise ReviewError(f"passed 的 review 里有 visual_result=fail 的豁免：{vetoed}")
    if receipt["status"] == "failed" and not any_fail:
        raise ReviewError("failed 的 review 里没有任何 fail 版本")


def load_review(path: Path) -> Dict[str, Any]:
    try:
        receipt = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReviewError(f"无法读取 review 回执：{path}: {error}") from error
    if not isinstance(receipt, dict):
        raise ReviewError(f"review 回执顶层必须是对象：{path}")
    validate_review(receipt)
    return receipt


# ---------------------------------------------------------------- 视觉工具指纹


def visual_fingerprint(toolchain: Mapping[str, Any]) -> Dict[str, Any]:
    """从已解析的四件工具链里取出 pdftotext / pdftoppm 两件。

    刻意**不另起一个解析器**：多一处 `resolve_toolchain()` 就多一处「这台机器上是哪个
    poppler」的答案，而两个答案不一致时没有任何机制会报错。
    """
    tools = {item["name"]: item for item in toolchain.get("tools", [])}
    missing = [name for name in VISUAL_TOOL_NAMES if name not in tools]
    if missing:
        raise ReviewError(f"工具链里缺少视觉工具：{missing}")
    return {
        "tools": [copy.deepcopy(dict(tools[name])) for name in VISUAL_TOOL_NAMES]
    }


# ---------------------------------------------------------------- 候选页启发式


def _normalize(values: Sequence[float]) -> List[float]:
    """min-max 归一化。全等时一律给 0——没有差异就没有「更值得看」的页。"""
    if not values:
        return []
    low = min(values)
    high = max(values)
    if high <= low:
        return [0.0 for _ in values]
    return [(item - low) / (high - low) for item in values]


def candidate_pages(metrics: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """纯函数：三指标等权平均，最高分为候选锚点。

    **它只做加法。** 返回的 `pages` 是「另标为重点二次复核」的锚点集合，不是审查范围；
    审查范围永远是 `1..page_count` 全页（由 `_validate_pages()` 强制）。

    最高分为候选，平局全取——并列时挑一个是主观的，而主观选择在这里没有任何依据。
    """
    if not metrics:
        raise ReviewError("候选页启发式需要至少一页的指标")
    pages = [int(item["page"]) for item in metrics]
    if sorted(pages) != list(range(1, len(pages) + 1)):
        raise ReviewError(f"指标的页集合必须精确覆盖 1..N，实际 {sorted(pages)}")

    columns = {
        name: _normalize([float(item[name]) for item in metrics])
        for name in ("text_chars", "math_glyph_proxy", "ink_ratio")
    }
    scores: List[Dict[str, Any]] = []
    for index, item in enumerate(metrics):
        score = sum(columns[name][index] for name in columns) / len(columns)
        scores.append({
            "page": int(item["page"]),
            "text_chars": int(item["text_chars"]),
            "math_glyph_proxy": int(item["math_glyph_proxy"]),
            "ink_ratio": float(item["ink_ratio"]),
            "score": score,
        })

    highest = max(item["score"] for item in scores)
    dense = [item["page"] for item in scores if item["score"] >= highest]
    return {"pages": sorted(dense), "dense_pages": sorted(dense), "scores": scores}


def _parse_pgm(payload: bytes) -> Tuple[int, bytes]:
    """解析 pdftoppm -gray 的 P5 PGM；返回 (maxval, 像素字节)。"""
    if not payload.startswith(b"P5"):
        raise ReviewError("pdftoppm 没有输出 P5 灰度图")
    fields: List[bytes] = []
    index = 2
    while len(fields) < 3:
        while index < len(payload) and payload[index : index + 1].isspace():
            index += 1
        if index < len(payload) and payload[index : index + 1] == b"#":
            while index < len(payload) and payload[index : index + 1] != b"\n":
                index += 1
            continue
        start = index
        while index < len(payload) and not payload[index : index + 1].isspace():
            index += 1
        if start == index:
            raise ReviewError("pdftoppm 输出的 PGM 头不完整")
        fields.append(payload[start:index])
    index += 1  # 头与像素之间恰好一个空白字节
    try:
        width, height, maxval = (int(item) for item in fields)
    except ValueError as error:
        raise ReviewError("pdftoppm 输出的 PGM 头不是整数") from error
    pixels = payload[index : index + width * height]
    if len(pixels) != width * height or maxval <= 0:
        raise ReviewError("pdftoppm 输出的 PGM 像素数与头不符")
    return maxval, pixels


def default_page_metrics(
    root: Path,
    pdf_relative: str,
    page_count: int,
    toolchain: Mapping[str, Any],
) -> List[Dict[str, Any]]:
    """现场跑 pdftotext / pdftoppm 逐页取三个指标。任何一步失败都 fail closed。"""
    tools = {item["name"]: item["path"] for item in toolchain.get("tools", [])}
    for name in VISUAL_TOOL_NAMES:
        if name not in tools:
            raise ReviewError(f"工具链里缺少视觉工具：{name}")
    pdf_path = Path(root) / _assert_safe_relative(pdf_relative)
    if not pdf_path.is_file():
        raise ReviewError(f"PDF 缺失，算不出候选页：{pdf_relative}")

    records: List[Dict[str, Any]] = []
    for page in range(1, page_count + 1):
        number = str(page)
        try:
            text = subprocess.run(
                [tools["pdftotext"], "-f", number, "-l", number, "-q",
                 str(pdf_path), "-"],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ).stdout.decode("utf-8", errors="replace")
            raster = subprocess.run(
                [tools["pdftoppm"], "-gray", "-r", str(CANDIDATE_DPI),
                 "-f", number, "-l", number, str(pdf_path)],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ).stdout
        except (OSError, subprocess.SubprocessError) as error:
            raise ReviewError(f"{pdf_relative} 第 {page} 页取指标失败：{error}") from error
        maxval, pixels = _parse_pgm(raster)
        threshold = _INK_THRESHOLD * maxval // 255
        records.append({
            "page": page,
            "text_chars": sum(1 for item in text if not item.isspace()),
            "math_glyph_proxy": sum(1 for item in text if item in MATH_GLYPHS),
            "ink_ratio": (
                sum(1 for item in pixels if item < threshold) / len(pixels)
            ),
        })
    return records


# ---------------------------------------------------------------- 工作项


def new_review_work_item(
    manifest: Mapping[str, Any],
    batch_id: str,
    paper_id: str,
    edition: str,
    build: Mapping[str, Any],
    visual: Mapping[str, Any],
    anchors: Sequence[int],
) -> Dict[str, Any]:
    """一个版本代理的独占工作项：全页骨架 + 该版本的警告清单 + 全部绑定。

    骨架把 `1..page_count` 全部列出来，每页八项都摆在那里等着被填。**页是发下去的，
    不是收上来的**——只收上来的页集合永远解释不清「没交的那几页是漏审还是判过了」。
    """
    paper = _paper(manifest, paper_id)
    record = next(
        (item for item in build["editions"] if item["edition"] == edition), None
    )
    if record is None or record["pdf"] is None:
        raise ReviewError(f"{paper_id} 的 {edition} 没有 PDF，无法准备视觉审查")
    count = record["pdf"]["page_count"]
    return {
        "schema_version": 1,
        "batch_id": batch_id,
        "paper_id": paper_id,
        "project_dir": paper["project_dir"],
        "edition": edition,
        "build_attempt_id": build["attempt_id"],
        "input_projection": build["input_projection"],
        "generation_input_tree_sha256": build["generation_input_tree"]["tree_sha256"],
        "dependency_tree_sha256": build["dependency_tree"]["tree_sha256"],
        "toolchain_fingerprint": copy.deepcopy(dict(build["toolchain_fingerprint"])),
        "visual_tool_fingerprint": copy.deepcopy(dict(visual)),
        "pdf": {
            "path": record["pdf"]["path"],
            "sha256": record["pdf"]["sha256"],
            "page_count": count,
        },
        "candidate_pages": sorted(set(int(item) for item in anchors)),
        "candidate_override": None,
        # 该版本的全部 Overfull/Underfull 原样带下来（含 width_pt=null 的 Underfull），
        # 代理据此逐条写豁免；漏一条，finalize 时逐项匹配就会当场失败。
        "warnings": copy.deepcopy(list(record["log"]["overfull"])),
        "warning_exemptions": [],
        "result": "pending",
        "pages": [
            {
                "page": page,
                "result": "pending",
                "checks": [
                    {"check": code, "result": "pending", "note": ""}
                    for code in CHECK_CODES
                ],
            }
            for page in range(1, count + 1)
        ],
    }


def _require_build(
    root: Path,
    manifest: Mapping[str, Any],
    paper_id: str,
    toolchain: Mapping[str, Any],
    expected_status: str,
) -> Dict[str, Any]:
    """逐卷直接问 build 回执，**不信缓存 batch status**。"""
    path = Path(root) / build_receipt_path(_paper(manifest, paper_id))
    if not path.is_file():
        raise ReviewError(f"{paper_id}: 缺 build 回执")
    receipt = build_projects.load_receipt(path)
    if receipt["status"] != expected_status:
        raise ReviewError(
            "%s: build 回执状态是 %s，要求 %s"
            % (paper_id, receipt["status"], expected_status)
        )
    current, reasons = build_projects.receipt_currency(
        root, manifest, receipt, toolchain=toolchain
    )
    if not current:
        raise ReviewError("%s: build 回执已失效（%s）" % (paper_id, "；".join(reasons)))
    return receipt


def prepare_batch(
    manifest_path: Path,
    batch_id: str,
    toolchain: Optional[Mapping[str, Any]] = None,
    search_path: Optional[str] = None,
    work_dir: Optional[Path] = None,
    metrics_probe: Optional[Callable[..., Sequence[Mapping[str, Any]]]] = None,
) -> Dict[str, Any]:
    """只写 ignored `.work`：为批内每卷每版本生成一个独占工作项。"""
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    manifest = load_manifest(manifest_path)
    batch = _validate_batch_size(manifest, batch_id)
    resolved = _validated_work_dir(root, work_dir)
    probe = metrics_probe or default_page_metrics
    chain = toolchain or build_projects.resolve_toolchain(search_path=search_path)
    visual = visual_fingerprint(chain)

    planned: List[Tuple[Path, Dict[str, Any]]] = []
    for paper_id in batch["paper_ids"]:
        build = _require_build(
            root, manifest, paper_id, chain, "compiled_pending_review"
        )
        for edition in EDITIONS:
            target = work_item_path(resolved, batch_id, edition, paper_id)
            if target.is_file():
                existing = _read_work_item(target, batch_id, paper_id, edition)
                if existing.get("build_attempt_id") == build["attempt_id"]:
                    # 同一次 attempt 的工作项就是**正在进行中的审查**。覆盖它等于把代理
                    # 已填的页判全部丢掉，而丢失是不可逆的；重编后 attempt 会变，那时才
                    # 允许替换。要重来就人工删掉那个文件。
                    raise ReviewError(
                        "工作项已存在且绑定当前 attempt，拒绝覆盖：%s"
                        % _relative_to(root, target)
                    )
            record = next(
                item for item in build["editions"] if item["edition"] == edition
            )
            metrics = probe(
                root, record["pdf"]["path"], record["pdf"]["page_count"], chain
            )
            anchors = candidate_pages(metrics)["pages"]
            planned.append((
                target,
                new_review_work_item(
                    manifest, batch_id, paper_id, edition, build, visual, anchors
                ),
            ))

    created: List[str] = []
    for target, document in planned:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(canonical_json(document).encode("utf-8"))
        created.append(_relative_to(root, target))
    return {
        "code": "PREPARED", "batch_id": batch_id, "created": sorted(created),
        "papers": list(batch["paper_ids"]),
    }


def _read_work_item(
    path: Path, batch_id: str, paper_id: str, edition: str
) -> Dict[str, Any]:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ReviewError(f"无法读取工作项 {path.name}（{edition}）：{error}") from error
    if not isinstance(document, dict):
        raise ReviewError(f"工作项顶层必须是对象：{edition}/{paper_id}")
    for field, expected in (
        ("batch_id", batch_id), ("paper_id", paper_id), ("edition", edition)
    ):
        if document.get(field) != expected:
            raise ReviewError(
                "%s/%s 的 %s 应为 %s，实际 %r"
                % (edition, paper_id, field, expected, document.get(field))
            )
    return document


# ---------------------------------------------------------------- 当前性


def is_stale(
    build: Mapping[str, Any],
    review: Mapping[str, Any],
    visual: Optional[Mapping[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """review 相对 build 与视觉工具链的当前性；返回 (是否 stale, 原因清单)。

    ⚠️ `visual=None` 会**跳过**视觉工具指纹那一条，那正是 fail-open：换了 poppler 的机器上
    旧 review 照样绿。调用方一律显式传；默认值只为纯粹的绑定比对留一个入口。
    """
    reasons: List[str] = []
    if review.get("paper_id") != build["paper_id"]:
        reasons.append("review 与 build 不是同一卷")
    if review.get("build_attempt_id") != build["attempt_id"]:
        reasons.append("build attempt 变化")
    if review.get("input_projection") != build["input_projection"]:
        reasons.append("manifest 投影变化")
    if review.get("generation_input_tree_sha256") != build["generation_input_tree"][
        "tree_sha256"
    ]:
        reasons.append("生成输入树变化")
    dependency = build.get("dependency_tree")
    if dependency is None:
        reasons.append("build 尚无依赖闭包")
    elif review.get("dependency_tree_sha256") != dependency["tree_sha256"]:
        reasons.append("依赖闭包变化")
    if review.get("toolchain_fingerprint") != build["toolchain_fingerprint"]:
        reasons.append("构建工具链指纹变化")
    if visual is not None and review.get("visual_tool_fingerprint") != visual:
        reasons.append("视觉工具指纹变化")

    reviewed = {item["edition"]: item for item in review.get("editions", [])}
    for record in build["editions"]:
        seen = reviewed.get(record["edition"])
        if seen is None:
            reasons.append("缺少版本：%s" % record["edition"])
            continue
        if record["pdf"] is None:
            reasons.append("%s 没有 PDF" % record["edition"])
            continue
        if seen.get("pdf_sha256") != record["pdf"]["sha256"]:
            reasons.append("%s 的 PDF 已变化" % record["edition"])
        if seen.get("page_count") != record["pdf"]["page_count"]:
            reasons.append("%s 的页数变化" % record["edition"])

    expected = collections.Counter(
        _warning_key(item["edition"], warning)
        for item in build["editions"] for warning in item["log"]["overfull"]
    )
    actual = collections.Counter(
        _warning_key(item["edition"], item)
        for item in review.get("warning_exemptions", [])
    )
    if expected != actual:
        # 「警告集合变化时旧豁免失效」：行号挪了一行、宽度多了 0.01pt，都是新的一条警告，
        # 旧那句「版心内可接受」没有看过它。
        missing = sorted((expected - actual).elements(), key=_warning_sort_key)
        extra = sorted((actual - expected).elements(), key=_warning_sort_key)
        reasons.append(
            "警告集合与豁免不再逐项匹配（缺 %d 条、多 %d 条）%s%s"
            % (
                sum((expected - actual).values()), sum((actual - expected).values()),
                "；缺：%s" % (missing,) if missing else "",
                "；多：%s" % (extra,) if extra else "",
            )
        )
    return bool(reasons), reasons


def _warning_key(edition: str, warning: Mapping[str, Any]) -> Tuple[Any, ...]:
    """与 `build_projects._warning_key()` 逐字同构的身份键。

    宽度按**字符串逐字**比较，绝不数值化：这把尺子的下游是
    `build_projects.finalize_receipt()`，它比的就是原串。放宽成 `float()` 相等会造出
    「本模块认可、finalize 拒绝」的夹缝，而夹缝里的那份回执两边都解释不了。
    """
    return (
        edition, warning["kind"], warning["box"], warning["width_pt"], warning["lines"],
    )


def _warning_sort_key(key: Sequence[Any]) -> Tuple[Any, ...]:
    """只用于把差异**打印**成稳定顺序的全序键。

    必须先按 kind 分流：只有 Overfull 才允许 `float(width_pt)`；Underfull 的宽度必须是
    null。这样错误形状不会在诊断排序里被误解释成另一个数值域。
    """
    edition, kind, box, width_pt, lines = key
    if kind == "Overfull":
        if width_pt is None:
            raise ReviewError("Overfull 的 width_pt 不能是 null")
        width_order = float(width_pt)
    elif kind == "Underfull":
        if width_pt is not None:
            raise ReviewError("Underfull 的 width_pt 必须是 null")
        width_order = 0.0
    else:
        raise ReviewError("未知警告 kind：%r" % kind)
    return (
        edition, kind, box, width_pt is None, width_order,
        lines is None, lines or "",
    )


# ---------------------------------------------------------------- 批次聚合


def _validate_work_binding(
    item: Mapping[str, Any], build: Mapping[str, Any], edition: str,
    visual: Mapping[str, Any],
) -> None:
    record = next(
        (part for part in build["editions"] if part["edition"] == edition), None
    )
    if record is None or record["pdf"] is None:
        raise ReviewError("%s 没有当前 PDF" % edition)
    expected = {
        "build_attempt_id": build["attempt_id"],
        "input_projection": build["input_projection"],
        "generation_input_tree_sha256": build["generation_input_tree"]["tree_sha256"],
        "dependency_tree_sha256": build["dependency_tree"]["tree_sha256"],
        "toolchain_fingerprint": build["toolchain_fingerprint"],
        "visual_tool_fingerprint": visual,
        "pdf": {
            "path": record["pdf"]["path"],
            "sha256": record["pdf"]["sha256"],
            "page_count": record["pdf"]["page_count"],
        },
        "warnings": record["log"]["overfull"],
    }
    mismatched = [field for field, value in expected.items() if item.get(field) != value]
    if mismatched:
        raise ReviewError(
            "%s 工作项与当前 build 不匹配：%s" % (edition, mismatched)
        )


def _review_from_work_items(
    manifest: Mapping[str, Any],
    batch_id: str,
    paper_id: str,
    build: Mapping[str, Any],
    items: Mapping[str, Mapping[str, Any]],
    visual: Mapping[str, Any],
    reviewed_at: str,
) -> Dict[str, Any]:
    paper = _paper(manifest, paper_id)
    editions: List[Dict[str, Any]] = []
    exemptions: List[Dict[str, Any]] = []
    for edition in EDITIONS:
        item = items[edition]
        _validate_work_binding(item, build, edition, visual)
        record = next(
            (part for part in build["editions"] if part["edition"] == edition), None
        )
        if record is None or record["pdf"] is None:
            raise ReviewError(f"{paper_id} 的 {edition} 没有 PDF")
        pages = []
        for page in item.get("pages", []):
            if not isinstance(page, Mapping):
                raise ReviewError(f"{paper_id}/{edition} 的页记录必须是对象")
            pages.append({
                "page": page.get("page"),
                "result": page.get("result"),
                "checks": [
                    {
                        "check": check.get("check"),
                        "result": check.get("result"),
                        "note": str(check.get("note", "")),
                    }
                    for check in page.get("checks", [])
                    if isinstance(check, Mapping)
                ],
            })
        editions.append({
            "edition": edition,
            "pdf_sha256": record["pdf"]["sha256"],
            "page_count": record["pdf"]["page_count"],
            "result": (
                "fail" if any(page["result"] == "fail" for page in pages) else "pass"
            ),
            "candidate_pages": sorted(set(item.get("candidate_pages") or [])),
            "candidate_override": item.get("candidate_override"),
            "pages": pages,
        })
        for exemption in item.get("warning_exemptions") or []:
            if not isinstance(exemption, Mapping):
                raise ReviewError(f"{paper_id}/{edition} 的警告豁免必须是对象")
            exemptions.append(dict(exemption, edition=edition))

    status = (
        "failed" if any(item["result"] == "fail" for item in editions) else "passed"
    )
    receipt = {
        "schema_version": 1,
        "paper_id": paper_id,
        "project_dir": paper["project_dir"],
        "batch_id": batch_id,
        "status": status,
        "reviewed_at": reviewed_at,
        "build_attempt_id": build["attempt_id"],
        "input_projection": build["input_projection"],
        "generation_input_tree_sha256": build["generation_input_tree"]["tree_sha256"],
        "dependency_tree_sha256": build["dependency_tree"]["tree_sha256"],
        "toolchain_fingerprint": copy.deepcopy(dict(build["toolchain_fingerprint"])),
        "visual_tool_fingerprint": copy.deepcopy(dict(visual)),
        "editions": editions,
        "warning_exemptions": exemptions,
    }
    validate_review(receipt)
    return receipt


def aggregate_batch_in_memory(
    root: Path,
    manifest: Mapping[str, Any],
    batch_id: str,
    builds: Mapping[str, Mapping[str, Any]],
    work_dir: Path,
    visual: Mapping[str, Any],
    reviewed_at: Optional[str] = None,
) -> Dict[str, Any]:
    """把四版本工作项折成每卷一份 review 候选；**全在内存，一个字节都不写**。

    paper 集合与 edition 集合必须恰好等于批次 × 四版本：多一个少一个都整批中止，
    因为「差一份就先按通过算」正是视觉审查最容易失守的地方。
    """
    batch = _batch(manifest, batch_id)
    paper_ids = list(batch["paper_ids"])
    stamp = reviewed_at or _now()

    for edition in EDITIONS:
        directory = Path(work_dir) / batch_id / "review" / edition
        if not directory.is_dir():
            raise ReviewError(f"缺少版本目录：{edition}")
        found = {item.stem for item in sorted(directory.glob("*.json"))}
        if found != set(paper_ids):
            raise ReviewError(
                "%s 的试卷集合与批次不符：多 %s，缺 %s"
                % (edition, sorted(found - set(paper_ids)), sorted(set(paper_ids) - found))
            )

    reviews: Dict[str, Dict[str, Any]] = {}
    fails: List[Dict[str, Any]] = []
    for paper_id in paper_ids:
        build = builds[paper_id]
        items = {}
        for edition in EDITIONS:
            path = work_item_path(Path(work_dir), batch_id, edition, paper_id)
            items[edition] = _read_work_item(path, batch_id, paper_id, edition)
        review = _review_from_work_items(
            manifest, batch_id, paper_id, build, items, visual, stamp
        )
        stale, reasons = is_stale(build, review, visual)
        if stale:
            raise ReviewError("%s: review 与 build 不匹配（%s）" % (paper_id, "；".join(reasons)))
        reviews[paper_id] = review
        fails.extend(_fail_records(review, build))
    return {"reviews": reviews, "fails": fails, "papers": paper_ids}


def _fail_records(
    review: Mapping[str, Any], build: Mapping[str, Any]
) -> List[Dict[str, Any]]:
    """当前 fail 集合：逐（版本, 页, 检查项）一条，带 attempt 与 PDF SHA 供对账。"""
    records: List[Dict[str, Any]] = []
    for edition in review["editions"]:
        for page in edition["pages"]:
            for check in page["checks"]:
                if check["result"] != "fail":
                    continue
                records.append({
                    "paper_id": review["paper_id"],
                    "edition": edition["edition"],
                    "page": page["page"],
                    "check_code": check["check"],
                    "note": check["note"],
                    "build_attempt_id": build["attempt_id"],
                    "pdf_sha256": edition["pdf_sha256"],
                })
    return records


# ---------------------------------------------------------------- issues 对账


def _visual_issue(
    paper_id: str,
    edition: str,
    page: int,
    check_code: str,
    build_attempt_id: str,
    pdf_sha256: str,
    resume_action: str,
    resolved: bool,
) -> Dict[str, Any]:
    """`origin=visual-review` 的 layout-warning。

    身份（`issues._fingerprint_identity()`）由 type+paper_id+edition+page+check_code+
    figure_id 唯一确定；`build_attempt_id`/`pdf_sha256` 刻意**不进身份**——同一处版式缺陷
    重编一次就换个编号，问题总账会变成流水账，而「这条还在不在」才是要回答的问题。
    """
    return {
        "paper_id": paper_id,
        "affected_paper_ids": [],
        "type": ISSUE_TYPE,
        "status": "resolved" if resolved else "open",
        "impact": "non_blocking" if resolved else "blocks_completion",
        "origin": ISSUE_ORIGIN,
        "edition": edition,
        "page": int(page),
        "check_code": check_code,
        "figure_id": ISSUE_FIGURE_MARKER,
        "build_attempt_id": build_attempt_id,
        "pdf_sha256": pdf_sha256,
        "resume_action": resume_action,
    }


def reconcile_visual_issues(
    issues_path: Path,
    paper_ids: Sequence[str],
    fails: Sequence[Mapping[str, Any]],
) -> Tuple[bytes, Dict[str, List[str]], List[Dict[str, Any]]]:
    """当前 fail upsert；旧的自动视觉问题若已不在当前 fail 集合则 resolve。

    **人工/来源问题绝不自动解决**：只有 `origin=visual-review` 且属于本批次的条目才在
    对账范围内。绕道临时副本调用 `issues.upsert_issue()` 的理由同
    `build_projects.reconcile_issues()`——编号分配、fingerprint 与块序只此一份。
    """
    issues_path = Path(issues_path)
    original = issues_path.read_bytes() if issues_path.is_file() else b""
    scope = set(paper_ids)

    with tempfile.TemporaryDirectory() as temporary:
        scratch = Path(temporary) / issues_path.name
        if original:
            scratch.write_bytes(original)
        existing = issues_module.load_issues(scratch) if original else []

        current: Dict[str, Dict[str, Any]] = {}
        for record in sorted(
            fails, key=lambda item: (item["paper_id"], item["edition"], item["page"],
                                    item["check_code"])
        ):
            candidate = _visual_issue(
                record["paper_id"], record["edition"], record["page"],
                record["check_code"], record["build_attempt_id"],
                record["pdf_sha256"],
                "修正 %s 的 %s 第 %d 页 %s（%s）后重跑 build --formal 并重新全页审查"
                % (
                    record["paper_id"], record["edition"], record["page"],
                    record["check_code"], record["note"].strip() or "视觉审查未通过",
                ),
                resolved=False,
            )
            current[issues_module.issue_fingerprint(candidate)] = candidate

        for fingerprint, candidate in current.items():
            issues_module.upsert_issue(scratch, candidate)

        for item in existing:
            if item.get("origin") != ISSUE_ORIGIN or item.get("paper_id") not in scope:
                continue
            if item["fingerprint"] in current or item["status"] == "resolved":
                continue
            issues_module.upsert_issue(scratch, _visual_issue(
                item["paper_id"], item["edition"], item["page"], item["check_code"],
                item.get("build_attempt_id", ""), item.get("pdf_sha256", ""),
                "已在新一次全页视觉审查中通过，无需动作",
                resolved=True,
            ))

        recorded = issues_module.load_issues(scratch) if scratch.is_file() else []
        payload = scratch.read_bytes() if scratch.is_file() else original

    return payload, issues_module.issue_ids_by_paper(recorded), recorded


# ---------------------------------------------------------------- 批次报告


_REPORT_TITLE = re.compile(r"^# 批次 (\S+) 视觉审查报告$", re.MULTILINE)
_REPORT_FIELD = re.compile(r"^- ([^：\n]+)：(.*)$", re.MULTILINE)
_REPORT_SECTION = re.compile(r"^## (\S+)$", re.MULTILINE)


def _joined(values: Sequence[str]) -> str:
    return "、".join(values) if values else "无"


def render_batch_report(payload: Mapping[str, Any]) -> str:
    """渲染最终批次报告。

    只渲染**内容候选**（`eligible_complete|eligible_blocked`）与批次结论候选，绝不写入
    `complete/closed` 这类最终状态：报告尚未验证时就把最终状态印上去，等于用未验证的报告
    给自己背书（`status.py` 顶部那条 report 门禁正是为此存在）。
    """
    lines = [
        "# 批次 %s 视觉审查报告" % payload["batch_id"],
        "",
        "- 批次结论：`%s`" % payload["batch_outcome"],
        "- 试卷数：%d" % payload["paper_count"],
        "- 版本数：%d" % payload["edition_count"],
        "- 审查页数：%d" % payload["page_total"],
        "",
    ]
    for paper in payload["papers"]:
        lines += [
            "## %s" % paper["paper_id"],
            "",
            "- 标题：%s" % paper["title"],
            "- 项目目录：`%s`" % paper["project_dir"],
            "- 构建：`%s`（attempt `%s`）" % (
                paper["build_status"], paper["build_attempt_id"]
            ),
            "- 审查：`%s`（%s）" % (paper["review_status"], paper["reviewed_at"]),
            "- 内容候选：`%s`" % paper["content_outcome"],
            "- 页数：%s" % "；".join(
                "%s %d" % (edition, paper["page_counts"][edition])
                for edition in EDITIONS
            ),
            "- 警告豁免：%d" % paper["exemption_count"],
            "- 视觉问题：%s" % _joined(paper["visual_issue_ids"]),
            "- 阻塞问题：%s" % _joined(paper["blocker_issue_ids"]),
            "",
        ]
    return "\n".join(lines).rstrip("\n") + "\n"


def _parse_batch_report(text: str) -> Dict[str, Any]:
    """把渲染结果重新读回结构。逐字段验证靠的是这条回路，而不是「渲染函数应该没错」。"""
    title = _REPORT_TITLE.search(text)
    if title is None:
        raise ReviewError("批次报告缺少标题行")
    sections = list(_REPORT_SECTION.finditer(text))
    header = text[: sections[0].start()] if sections else text
    fields = dict(_REPORT_FIELD.findall(header))

    papers = []
    for index, match in enumerate(sections):
        end = sections[index + 1].start() if index + 1 < len(sections) else len(text)
        body = dict(_REPORT_FIELD.findall(text[match.end():end]))
        papers.append({"paper_id": match.group(1), "fields": body})
    return {"batch_id": title.group(1), "fields": fields, "papers": papers}


def verify_batch_report(text: str, payload: Mapping[str, Any]) -> None:
    """逐字段核对渲染结果与候选载荷；任何一项对不上就是零修改。"""
    parsed = _parse_batch_report(text)
    if parsed["batch_id"] != payload["batch_id"]:
        raise ReviewError("批次报告的批次不符：%s" % parsed["batch_id"])
    expected_header = {
        "批次结论": "`%s`" % payload["batch_outcome"],
        "试卷数": str(payload["paper_count"]),
        "版本数": str(payload["edition_count"]),
        "审查页数": str(payload["page_total"]),
    }
    for key, value in expected_header.items():
        if parsed["fields"].get(key) != value:
            raise ReviewError(
                "批次报告的「%s」应为 %s，实际 %r" % (key, value, parsed["fields"].get(key))
            )
    if [item["paper_id"] for item in parsed["papers"]] != [
        item["paper_id"] for item in payload["papers"]
    ]:
        raise ReviewError("批次报告的试卷小节与候选不符")
    for parsed_paper, paper in zip(parsed["papers"], payload["papers"]):
        expected = {
            "标题": paper["title"],
            "项目目录": "`%s`" % paper["project_dir"],
            "构建": "`%s`（attempt `%s`）" % (
                paper["build_status"], paper["build_attempt_id"]
            ),
            "审查": "`%s`（%s）" % (paper["review_status"], paper["reviewed_at"]),
            "内容候选": "`%s`" % paper["content_outcome"],
            "页数": "；".join(
                "%s %d" % (edition, paper["page_counts"][edition])
                for edition in EDITIONS
            ),
            "警告豁免": str(paper["exemption_count"]),
            "视觉问题": _joined(paper["visual_issue_ids"]),
            "阻塞问题": _joined(paper["blocker_issue_ids"]),
        }
        for key, value in expected.items():
            if parsed_paper["fields"].get(key) != value:
                raise ReviewError(
                    "%s 的「%s」应为 %s，实际 %r"
                    % (paper["paper_id"], key, value, parsed_paper["fields"].get(key))
                )


def _report_payload(
    manifest: Mapping[str, Any],
    batch_id: str,
    paper_ids: Sequence[str],
    builds: Mapping[str, Mapping[str, Any]],
    reviews: Mapping[str, Mapping[str, Any]],
    outcomes: Mapping[str, str],
    records: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    papers = []
    page_total = 0
    for paper_id in paper_ids:
        review = reviews[paper_id]
        counts = {item["edition"]: item["page_count"] for item in review["editions"]}
        page_total += sum(counts.values())
        mine = [
            item for item in records
            if item.get("paper_id") == paper_id
            or paper_id in set(item.get("affected_paper_ids") or [])
        ]
        papers.append({
            "paper_id": paper_id,
            "title": _paper(manifest, paper_id)["title"],
            "project_dir": _paper(manifest, paper_id)["project_dir"],
            "build_status": builds[paper_id]["status"],
            "build_attempt_id": builds[paper_id]["attempt_id"],
            "review_status": review["status"],
            "reviewed_at": review["reviewed_at"],
            "content_outcome": outcomes[paper_id],
            "page_counts": counts,
            "exemption_count": len(review["warning_exemptions"]),
            "visual_issue_ids": sorted(
                item["issue_id"] for item in mine
                if item.get("origin") == ISSUE_ORIGIN
            ),
            "blocker_issue_ids": sorted(
                item["issue_id"] for item in mine
                if issues_module.blocks_completion(item, paper_id)
            ),
        })
    return {
        "batch_id": batch_id,
        "batch_outcome": (
            "closed" if all(
                outcomes[paper_id] == "eligible_complete" for paper_id in paper_ids
            ) else "closed_with_blockers"
        ),
        "paper_count": len(paper_ids),
        "edition_count": len(paper_ids) * len(EDITIONS),
        "page_total": page_total,
        "papers": papers,
    }


# ---------------------------------------------------------------- finalize


def _revalidate_final(
    build: Mapping[str, Any], review: Mapping[str, Any]
) -> Dict[str, Any]:
    """report-only 路径：把现成的 `succeeded` 回执降回待审再跑同一把尺子。

    「复用现有回执」不等于「相信现有回执」——降级后重跑 `finalize_receipt()`，逐项核对
    绑定、PDF SHA、页数与警告豁免，跑完还必须逐字节等于原件，否则拒绝。
    """
    probe = copy.deepcopy(dict(build))
    probe["status"] = "compiled_pending_review"
    finalized = build_projects.finalize_receipt(probe, review)
    if canonical_json(finalized) != canonical_json(dict(build)):
        raise ReviewError(
            "%s: 现有 succeeded 回执与重新验证的结果不一致" % build["paper_id"]
        )
    return finalized


def _loaded_facts(
    root: Path,
    manifest: Mapping[str, Any],
    paper_ids: Sequence[str],
    issues_path: Path,
    facts_loader: Optional[Callable[..., Mapping[str, Mapping[str, Any]]]],
) -> Dict[str, Dict[str, Any]]:
    if facts_loader is not None:
        loaded = dict(facts_loader(root, manifest, paper_ids))
    else:
        import provenance  # 运行时才加载：避免与 provenance 形成 import 环

        loaded = dict(provenance.load_provenance_facts(
            root, manifest, paper_ids, issues_path=issues_path
        ))
    missing = sorted(set(paper_ids) - set(loaded))
    if missing:
        raise ReviewError(f"facts_loader 没有覆盖 {missing}")
    return {key: dict(value) for key, value in loaded.items()}


def finalize_batch(
    manifest_path: Path,
    issues_path: Path,
    batch_id: str,
    report_path: Path,
    facts_loader: Optional[Callable[..., Mapping[str, Mapping[str, Any]]]] = None,
    toolchain: Optional[Mapping[str, Any]] = None,
    search_path: Optional[str] = None,
    work_dir: Optional[Path] = None,
    renderer: Optional[Callable[[Mapping[str, Any]], str]] = None,
    reviewed_at: Optional[str] = None,
) -> Dict[str, Any]:
    """唯一的领域写入口。全部闭环在内存完成后只提交一次 `state` 事务。

    两条出口，各自一次事务、互不重叠：

    - 四版本全 `passed` → 提交 review 回执、final build 回执、issues、最终批次报告与
      paper/batch 状态（manifest 最后写），`code=FINALIZED`；
    - 任一页 fail → **只**提交 `review=failed`、视觉 issues 与 paper/batch 状态
      （build 保持 `compiled_pending_review`，不生成/覆盖报告），`code=VISUAL_FAILED`。

    结构不完整、currency/CAS 不匹配、报告渲染或逐字段验证失败时零正式修改——这些分支
    在事务 `prepare()` 之前就抛出，工作树连一个临时文件都不会多出来。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    issues_path = _require_canonical(
        root, Path(issues_path), ISSUES_TARGET, "--issues"
    )
    report_relative = _require_report_path(root, Path(report_path), batch_id)
    render = renderer or render_batch_report

    with RepoLock(root):
        manifest = load_manifest(manifest_path)
        batch = _batch(manifest, batch_id)
        paper_ids = list(batch["paper_ids"])
        affected, batches = build_projects.affected_papers(manifest, paper_ids)
        if set(affected) != set(paper_ids):
            raise ReviewError(
                "批次之间存在共享试卷，所有权范围无法闭合：%s"
                % sorted(set(affected) - set(paper_ids))
            )
        chain = toolchain or build_projects.resolve_toolchain(search_path=search_path)
        visual = visual_fingerprint(chain)
        resolved_work = _validated_work_dir(root, work_dir)

        # ---- 模式判定：有工作项就是全页审查，没有就是 report-only 复核
        present = [
            edition for edition in EDITIONS
            if (Path(resolved_work) / batch_id / "review" / edition).is_dir()
        ]
        if present and len(present) != len(EDITIONS):
            raise ReviewError(f"工作项只准备了部分版本：{sorted(present)}")
        review_mode = bool(present)

        builds = {
            paper_id: _require_build(
                root, manifest, paper_id, chain,
                "compiled_pending_review" if review_mode else "succeeded",
            )
            for paper_id in paper_ids
        }

        # ---- 1. review 候选
        if review_mode:
            aggregate = aggregate_batch_in_memory(
                root, manifest, batch_id, builds, resolved_work, visual,
                reviewed_at=reviewed_at,
            )
            reviews = aggregate["reviews"]
            fails = aggregate["fails"]
        else:
            reviews = {}
            fails = []
            for paper_id in paper_ids:
                path = Path(root) / review_receipt_path(_paper(manifest, paper_id))
                if not path.is_file():
                    raise ReviewError(f"{paper_id}: 缺 review 回执，无法只重算报告")
                review = load_review(path)
                if review["status"] != "passed":
                    raise ReviewError(
                        "%s: review 状态是 %s，只重算报告要求 passed"
                        % (paper_id, review["status"])
                    )
                stale, reasons = is_stale(builds[paper_id], review, visual)
                if stale:
                    raise ReviewError(
                        "%s: review 已失效（%s），必须重编重审"
                        % (paper_id, "；".join(reasons))
                    )
                reviews[paper_id] = review

        # ---- 2. 视觉 issues 对账
        payload, issue_ids, records = reconcile_visual_issues(
            issues_path, paper_ids, fails
        )
        extra: Dict[str, bytes] = {}
        if payload != (issues_path.read_bytes() if issues_path.is_file() else b""):
            extra[ISSUES_TARGET] = payload

        loaded = _loaded_facts(root, manifest, affected, issues_path, facts_loader)
        review_targets = {
            review_receipt_path(_paper(manifest, paper_id)):
                canonical_json(reviews[paper_id]).encode("utf-8")
            for paper_id in paper_ids
        }

        # ---- 视觉失败：有效负结果，单独一次诊断事务后停在退出码 4
        if any(reviews[paper_id]["status"] != "passed" for paper_id in paper_ids):
            for paper_id in paper_ids:
                loaded[paper_id].update({
                    "review": reviews[paper_id]["status"],
                    "review_currency": "current",
                    "batch_report_valid": False,
                })
            facts = build_projects.assemble_facts(
                root, manifest, affected, loaded, builds,
                issue_records=records, toolchain=chain,
            )
            document = build_projects.commit_state(
                root, manifest, review_targets, extra,
                lambda transaction_id: build_projects.reconciled_manifest(
                    manifest, transaction_id, facts, batches, issue_ids
                ),
            )
            return {
                "code": "VISUAL_FAILED",
                "batch_id": batch_id,
                "papers": paper_ids,
                "revision": document["revision"],
                "batch_status": _batch(document, batch_id)["status"],
                "failed_pages": len(fails),
                "problems": [
                    "%s %s 第 %d 页 %s"
                    % (item["paper_id"], item["edition"], item["page"],
                       item["check_code"])
                    for item in fails
                ],
                "report_written": False,
            }

        # ---- 3. build succeeded 候选（纯函数；review fail 时根本走不到这里）
        open_visual = sorted(
            item["issue_id"] for item in records
            if item.get("origin") == ISSUE_ORIGIN
            and item.get("paper_id") in set(paper_ids)
            and item["status"] != "resolved"
        )
        if open_visual:
            raise ReviewError(f"仍有未解决的视觉问题：{open_visual}")
        final_builds = {
            paper_id: (
                build_projects.finalize_receipt(builds[paper_id], reviews[paper_id])
                if review_mode else
                _revalidate_final(builds[paper_id], reviews[paper_id])
            )
            for paper_id in paper_ids
        }

        # ---- 4. 内容候选 → 渲染 → 逐字段验证
        for paper_id in paper_ids:
            loaded[paper_id].update({
                "review": "passed",
                "review_currency": "current",
                "batch_report_valid": False,
            })
        candidate_facts = build_projects.assemble_facts(
            root, manifest, affected, loaded, final_builds,
            issue_records=records, toolchain=chain,
        )
        outcomes = {}
        for paper_id in paper_ids:
            outcome = derive_content_outcome(
                facts_without_report(candidate_facts[paper_id])
            )
            if outcome not in {"eligible_complete", "eligible_blocked"}:
                raise ReviewError(
                    "%s 的内容候选是 %s，不足以关闭批次" % (paper_id, outcome)
                )
            outcomes[paper_id] = outcome
        report = _report_payload(
            manifest, batch_id, paper_ids, final_builds, reviews, outcomes, records
        )
        rendered = render(report)
        if not isinstance(rendered, str):
            raise ReviewError("批次报告渲染结果必须是字符串")
        verify_batch_report(rendered, report)

        # ---- 5. 报告已验证，唯一一次派生最终 paper/batch 状态并单事务提交
        for paper_id in paper_ids:
            loaded[paper_id]["batch_report_valid"] = True
        facts = build_projects.assemble_facts(
            root, manifest, affected, loaded, final_builds,
            issue_records=records, toolchain=chain,
        )
        expected_batch = status_core.reconcile_batch_status(
            {paper_id: facts[paper_id] for paper_id in paper_ids}
        )
        if expected_batch != report["batch_outcome"]:
            # 报告里印的结论与状态机现场派生的结论不一致 —— 两者必有一个错，而把哪个
            # 当真都是猜。零修改退出。
            raise ReviewError(
                "批次报告的结论 %s 与状态机派生的 %s 不一致"
                % (report["batch_outcome"], expected_batch)
            )

        targets = dict(review_targets)
        for paper_id in paper_ids:
            targets[build_receipt_path(_paper(manifest, paper_id))] = (
                canonical_json(final_builds[paper_id]).encode("utf-8")
            )
        document = build_projects.commit_state(
            root, manifest, targets,
            dict(extra, **{report_relative: rendered.encode("utf-8")}),
            lambda transaction_id: build_projects.reconciled_manifest(
                manifest, transaction_id, facts, batches, issue_ids
            ),
        )

    return {
        "code": "FINALIZED",
        "batch_id": batch_id,
        "papers": paper_ids,
        "revision": document["revision"],
        "batch_status": _batch(document, batch_id)["status"],
        "report": report_relative,
        "report_written": True,
        "mode": "review" if review_mode else "report-only",
        "problems": [],
    }


# ---------------------------------------------------------------- 只读核对


def check_batch(
    manifest_path: Path,
    issues_path: Path,
    batch_id: str,
    toolchain: Optional[Mapping[str, Any]] = None,
    search_path: Optional[str] = None,
    require_current_build: bool = True,
) -> Dict[str, Any]:
    """只读：逐卷重算 build/review 当前性与批次报告存在性；一个字节都不写。"""
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    _require_canonical(root, Path(issues_path), ISSUES_TARGET, "--issues")
    manifest = load_manifest(manifest_path)
    batch = _batch(manifest, batch_id)

    problems: List[str] = []
    visual_failed = False
    try:
        chain = toolchain or build_projects.resolve_toolchain(search_path=search_path)
    except build_projects.BuildError as error:
        return {
            "code": "INVALID_OR_STALE", "batch_id": batch_id,
            "papers": list(batch["paper_ids"]),
            "problems": [f"工具链不可用：{error}"],
        }
    visual = visual_fingerprint(chain)

    for paper_id in batch["paper_ids"]:
        paper = _paper(manifest, paper_id)
        build_path = Path(root) / build_receipt_path(paper)
        review_path = Path(root) / review_receipt_path(paper)
        if not build_path.is_file():
            problems.append(f"{paper_id}: 缺 build 回执")
            continue
        try:
            build = build_projects.load_receipt(build_path)
        except build_projects.BuildError as error:
            problems.append(f"{paper_id}: {error}")
            continue
        if require_current_build:
            current, reasons = build_projects.receipt_currency(
                root, manifest, build, toolchain=chain
            )
            if not current:
                problems.append(
                    "%s: build 回执已失效（%s）" % (paper_id, "；".join(reasons))
                )
                continue
        if not review_path.is_file():
            problems.append(f"{paper_id}: 缺 review 回执")
            continue
        try:
            review = load_review(review_path)
        except ReviewError as error:
            problems.append(f"{paper_id}: {error}")
            continue
        stale, reasons = is_stale(build, review, visual)
        if stale:
            problems.append("%s: review 已失效（%s）" % (paper_id, "；".join(reasons)))
            continue
        if review["status"] == "failed":
            visual_failed = True
            problems.append(f"{paper_id}: 视觉审查未通过")
            continue
        if review["status"] != "passed" or build["status"] != "succeeded":
            problems.append(
                "%s: build=%s review=%s，批次尚未关闭"
                % (paper_id, build["status"], review["status"])
            )

    report_path = Path(root) / report_target(batch_id)
    if not problems and not report_path.is_file():
        problems.append(f"缺批次报告：{report_target(batch_id)}")

    if not problems:
        code = "FINALIZED"
    elif visual_failed:
        code = "VISUAL_FAILED"
    else:
        code = "INVALID_OR_STALE"
    return {
        "code": code, "batch_id": batch_id,
        "papers": list(batch["paper_ids"]), "problems": problems,
    }


def check_all(
    manifest_path: Path,
    issues_path: Path,
    require_current_build: bool = False,
    toolchain: Optional[Mapping[str, Any]] = None,
    search_path: Optional[str] = None,
) -> Dict[str, Any]:
    """只读：逐批次跑 `check_batch()`，汇总成一个退出码。"""
    manifest = load_manifest(Path(manifest_path).resolve())
    problems: List[str] = []
    codes: List[str] = []
    batches: Dict[str, str] = {}
    for batch in manifest.get("batches", []):
        report = check_batch(
            manifest_path, issues_path, batch["batch_id"],
            toolchain=toolchain, search_path=search_path,
            require_current_build=require_current_build,
        )
        batches[batch["batch_id"]] = report["code"]
        codes.append(report["code"])
        problems.extend(
            "%s %s" % (batch["batch_id"], item) for item in report["problems"]
        )
    if all(item == "FINALIZED" for item in codes):
        code = "FINALIZED"
    elif "VISUAL_FAILED" in codes and "INVALID_OR_STALE" not in codes:
        code = "VISUAL_FAILED"
    else:
        code = "INVALID_OR_STALE"
    return {"code": code, "batches": batches, "problems": problems}


# ---------------------------------------------------------------- 所有权路径


def batch_review_paths(
    manifest: Mapping[str, Any],
    batch_id: str,
    include_state: bool = False,
    report: bool = False,
) -> Tuple[str, ...]:
    """当前批次的所有权范围：各卷 build + review 回执，可选 manifest/issues 与报告。

    这一组路径是 `git add --pathspec-from-file` 的唯一来源：多一条就会夹带别的会话的
    改动，少一条就会把诊断状态留在工作区。视觉失败路径用的是**不含报告**的那一版——
    那次事务根本没有写报告，把它 add 进来只会把上一批的报告一起提交掉。
    """
    batch = _batch(manifest, batch_id)
    paths: List[str] = []
    for paper_id in batch["paper_ids"]:
        paper = _paper(manifest, paper_id)
        paths.append(build_receipt_path(paper))
        paths.append(review_receipt_path(paper))
    if include_state:
        paths.extend([MANIFEST_TARGET, ISSUES_TARGET])
    if report:
        paths.append(report_target(batch_id))
    duplicates = sorted({item for item in paths if paths.count(item) > 1})
    if duplicates:
        raise ReviewError(f"所有权范围内路径重复：{duplicates}")
    return tuple(paths)


check_staged = cli_common.check_staged


def read_pathspec(path: Path) -> List[str]:
    return cli_common.read_pathspec(path, ReviewError)


# ---------------------------------------------------------------- 受测包装器


def _git(root: Path, arguments: Sequence[str]) -> subprocess.CompletedProcess:
    """一律用参数数组。`shell=True` 会让中文项目目录名与引号成为注入面。"""
    return subprocess.run(
        ["git", "-C", str(root)] + list(arguments),
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


def _tracked_tree_is_clean(root: Path) -> List[str]:
    lines = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.decode("utf-8").splitlines()
    return [item for item in lines if item.strip()]


def finalize_batch_checked(
    manifest_path: Path,
    issues_path: Path,
    batch_id: str,
    report_path: Path,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Tasks 25–30 的受测主流程包装：领域函数 + 视觉失败时的精确诊断提交。

    分支是**严格**的，因为这里是唯一会自动 `git commit` 的地方：

    - 进入时 tracked 工作树/索引必须干净——否则这次提交会夹带别的会话的改动；
    - `0/FINALIZED`：原样返回，**不 stage、不 commit**（正式关闭由执行者按流程提交）；
    - `4/VISUAL_FAILED`：用**不含报告**的 ownership paths 精确 `git add`，跑
      `check-staged` 与 `git diff --cached --check`，提交固定诊断消息后返回 4；
    - `2/6` 或其他：零 stage、零 commit。带着未提交的诊断状态继续改规范源，会让下一次
      构建的输入无法解释——那正是这条包装器要堵死的路。
    """
    manifest_path = Path(manifest_path).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    dirty = _tracked_tree_is_clean(root)
    if dirty:
        return {
            "code": "INVALID_OR_STALE", "batch_id": batch_id, "committed": False,
            "problems": ["进入时 tracked 工作树/索引不干净：%s" % dirty],
        }

    report = dict(finalize_batch(
        manifest_path, issues_path, batch_id, report_path, **kwargs
    ))
    report["committed"] = False
    if report["code"] != "VISUAL_FAILED":
        return report

    manifest = load_manifest(manifest_path)
    scope = list(batch_review_paths(
        manifest, batch_id, include_state=True, report=False
    ))
    _git(root, ["add", "--"] + scope)
    problems = check_staged(root, scope)
    if problems:
        raise ReviewError("诊断状态的暂存区与所有权范围不一致：%s" % problems)
    _git(root, ["diff", "--cached", "--check"])
    _git(root, ["commit", "-m", DIAGNOSTIC_MESSAGE_TEMPLATE % batch_id])
    report["committed"] = True
    report["committed_paths"] = scope
    return report


# ---------------------------------------------------------------- CLI


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="批次视觉审查回执与聚合")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare-batch")
    prepare.add_argument("--manifest", required=True)
    prepare.add_argument("--batch", required=True)

    for name in ("finalize-batch", "finalize-batch-checked"):
        finalize = subparsers.add_parser(name)
        finalize.add_argument("--manifest", required=True)
        finalize.add_argument("--issues", required=True)
        finalize.add_argument("--batch", required=True)
        finalize.add_argument("--output-report", required=True)
        finalize.add_argument("--json", action="store_true")

    check = subparsers.add_parser("check-batch")
    check.add_argument("--manifest", required=True)
    check.add_argument("--issues", required=True)
    check.add_argument("--batch", required=True)
    check.add_argument("--json", action="store_true")

    every = subparsers.add_parser("check-all")
    every.add_argument("--manifest", required=True)
    every.add_argument("--issues", required=True)
    every.add_argument("--require-current-build", action="store_true")
    every.add_argument("--json", action="store_true")

    output = subparsers.add_parser("output-paths")
    output.add_argument("--manifest", required=True)
    output.add_argument("--batch", required=True)
    output.add_argument("--include-state", action="store_true")
    output.add_argument("--report")
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


EXIT_BY_CODE = {
    "FINALIZED": EXIT_FINALIZED,
    "VISUAL_FAILED": EXIT_VISUAL_FAILED,
    "INVALID_OR_STALE": EXIT_INVALID,
}


def _output_paths_command(arguments: argparse.Namespace) -> int:
    manifest_path = Path(arguments.manifest).resolve()
    root = cli_common.repository_root(manifest_path.parent)
    _require_canonical(root, manifest_path, MANIFEST_TARGET, "--manifest")
    manifest = load_manifest(manifest_path)
    if arguments.report is not None:
        _require_report_path(root, Path(arguments.report), arguments.batch)
    paths = batch_review_paths(
        manifest, arguments.batch,
        include_state=arguments.include_state,
        report=arguments.report is not None,
    )
    sys.stdout.buffer.write(b"".join(item.encode("utf-8") + b"\0" for item in paths))
    sys.stdout.buffer.flush()
    return EXIT_FINALIZED


def main(
    argv: Optional[Sequence[str]] = None,
    facts_loader: Optional[Callable[..., Any]] = None,
    search_path: Optional[str] = None,
    metrics_probe: Optional[Callable[..., Any]] = None,
    renderer: Optional[Callable[..., Any]] = None,
) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    as_json = bool(getattr(arguments, "json", False))

    try:
        if arguments.command == "prepare-batch":
            report = prepare_batch(
                Path(arguments.manifest), arguments.batch,
                search_path=search_path, metrics_probe=metrics_probe,
            )
            for relative in report["created"]:
                print("prepared %s" % relative)
            print("共 %d 个工作项" % len(report["created"]))
            return EXIT_FINALIZED

        if arguments.command in {"finalize-batch", "finalize-batch-checked"}:
            runner = (
                finalize_batch if arguments.command == "finalize-batch"
                else finalize_batch_checked
            )
            report = runner(
                Path(arguments.manifest), Path(arguments.issues), arguments.batch,
                Path(arguments.output_report), facts_loader=facts_loader,
                search_path=search_path, renderer=renderer,
            )
            _emit(report, arguments.json, ["  ✗ %s" % item for item in report.get(
                "problems", []
            )] + ["%s：%s" % (report["code"], report["batch_id"])])
            return EXIT_BY_CODE[report["code"]]

        if arguments.command == "check-batch":
            report = check_batch(
                Path(arguments.manifest), Path(arguments.issues), arguments.batch,
                search_path=search_path,
            )
            _emit(report, arguments.json, ["  ✗ %s" % item for item in
                                           report["problems"]]
                  + ["%s：%s" % (report["code"], report["batch_id"])])
            return EXIT_BY_CODE[report["code"]]

        if arguments.command == "check-all":
            report = check_all(
                Path(arguments.manifest), Path(arguments.issues),
                require_current_build=arguments.require_current_build,
                search_path=search_path,
            )
            _emit(report, arguments.json, ["  ✗ %s" % item for item in
                                           report["problems"]]
                  + ["%s：%d 批次" % (report["code"], len(report["batches"]))])
            return EXIT_BY_CODE[report["code"]]

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
            return EXIT_FINALIZED
    except UsageError as error:
        # 命令写错（2）与「数据不成立」（6）必须分得开：前者重打一遍就好，后者要去查证据链。
        _emit({"code": "USAGE", "problem": str(error)}, as_json, [])
        print("error: %s" % error, file=sys.stderr)
        return EXIT_USAGE
    except (ReviewError, StatusError, build_projects.BuildError,
            subprocess.SubprocessError, OSError) as error:
        # 领域函数是**抛异常**而不是返回 code 的——异常路径全部在事务 prepare() 之前，
        # 「零修改」由此成立。退出码契约在这里统一折成 6/INVALID_OR_STALE。
        _emit({"code": "INVALID_OR_STALE", "problem": str(error)}, as_json, [])
        print("error: %s" % error, file=sys.stderr)
        return EXIT_INVALID

    raise ReviewError(f"未知命令：{arguments.command}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ReviewError, StatusError, build_projects.BuildError, OSError,
            RuntimeError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(EXIT_INVALID)

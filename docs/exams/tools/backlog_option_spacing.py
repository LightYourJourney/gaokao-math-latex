#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成选项行距待办清单（只读 projection，不改 manifest）。"""
import json
from pathlib import Path

ROOT = Path("/Users/leo/leocode/gaokao-math-latex")
BASE = ROOT / "docs/exams"
manifest = json.loads((BASE / "source-manifest.json").read_text(encoding="utf-8"))
audit = json.loads((BASE / "reports" / "option-spacing-audit.json").read_text(encoding="utf-8"))
by_q = {p["source_files"]["questions"]: p for p in manifest["papers"] if p.get("source_files")}
batch_of = {pid: b["batch_id"] for b in manifest["batches"] for pid in b["paper_ids"]}

REVIEW = {
    "gk-2011-anhui-arts", "gk-2011-sichuan-science", "gk-2011-sichuan-arts",
    "gk-2009-chongqing-science", "gk-2010-liaoning-science",
    "gk-2008-anhui-arts", "gk-2007-regular-sichuan-arts",
}

rows = []
for r in audit["risky"] + audit["mild"]:
    p = by_q.get(r["path"])
    if not p:
        continue
    rows.append({
        "paper_id": p["paper_id"],
        "batch": batch_of.get(p["paper_id"]),
        "title": p["title"],
        "max_run": r["max_run"],
        "fraction_options": r["fraction_options"],
        "questions": r["questions"],
        "state": p["production_state"],
        "needs_full_review": p["paper_id"] in REVIEW,
    })
rows.sort(key=lambda x: (x["needs_full_review"], -x["max_run"], x["paper_id"]))

lines = [
    "# 选项行距待办清单（独立 `\\dfrac` 选项）",
    "",
    "由 `tools/audit_option_spacing.py` 的 JSON 与 `source-manifest.json` 合成，只读投影。",
    "",
    "## 口径",
    "",
    "1. 选项行内的 `\\dfrac` 改为行内 `\\frac`，重生成、重算哈希、重建四版；",
    "2. 四版页数只要有一版变化，就必须四版逐页重审（实测 PDF 哈希四版全变，无法只审变化版）；",
    "3. 页数不变才可沿用旧回执，硬条件见 `.work/carry_review.py`。",
    "",
    "## 汇总",
    "",
    "- 待办卷数：**%d**（complete %d、blocked %d）" % (
        len(rows),
        sum(1 for r in rows if r["state"] == "complete"),
        sum(1 for r in rows if r["state"] == "blocked"),
    ),
    "- 其中已确认必须整卷重审：**%d** 卷" % sum(1 for r in rows if r["needs_full_review"]),
    "",
    "## 清单",
    "",
    "| 卷 | 批次 | 连续段 | 分式选项 | 涉及题号 | 状态 | 处置 |",
    "| --- | --- | --- | --- | --- | --- | --- |",
]
for r in rows:
    lines.append("| %s | `%s` | %d | %d | %s | %s | %s |" % (
        r["title"], r["batch"], r["max_run"], r["fraction_options"],
        "、".join(str(q) for q in r["questions"]), r["state"],
        "整卷重审" if r["needs_full_review"] else "改后视页数定",
    ))
lines.append("")
(BASE / "reports" / "option-spacing-backlog.md").write_text("\n".join(lines), encoding="utf-8")
print("rows", len(rows))

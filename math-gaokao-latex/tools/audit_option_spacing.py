#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_option_spacing.py —— 只读审计选项中「独立分式」的行距风险。

背景：选项在 Markdown 中是独立段落（段间空行），段与段之间只有 `\\parskip`，
不会触发 TeX 的行内 `\\lineskip` 补偿；若连续多个选项各自只放一条 `\\dfrac`，
前一项的分母会与后一项的分子、或与题干末行重叠。2011 辽宁文/理、福建理等卷已实测。

本工具不写任何生成物，只扫描各卷 `_试题.md`，输出：
- `reports/option-spacing-audit.md`：按严重度排序的清单；
- `reports/option-spacing-audit.json`：机器可读清单，供批处理脚本消费。

判定：选项行形如 `（A）$...$`，去掉 `\\dfrac` 后只剩符号/数字/π/√ 等，视为
「独立分式」。同一题内连续出现 >=2 条即为确定重叠风险；单条记为低风险。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

OPTION = re.compile(r"^（[A-D]）\s*\$(.+)\$\s*$")
QUESTION = re.compile(r"^\*\*(\d+)．\*\*")
PLAIN = re.compile(r"[+-−0123456789π√()（）\s]*$")


def strip_dfrac(math: str) -> str | None:
    """去掉全部 \\dfrac 及其参数；剩余若是纯符号串则返回剩余部分。"""
    if "\\dfrac" not in math:
        return None
    rest = re.sub(
        r"\\dfrac\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}",
        "", math,
    )
    rest = re.sub(r"\\dfrac\s*(\d|\\[a-zA-Z]+)\s*(\d|\\[a-zA-Z]+|[a-zA-Z])", "", rest)
    rest = rest.replace("\\", "").replace(" ", "")
    return rest


def audit_file(path: Path) -> dict:
    lines = [line.strip() for line in path.read_text(encoding="utf-8").split("\n") if line.strip()]
    question = None
    run = 0
    worst = 0
    hits = []
    for line in lines:
        match = QUESTION.match(line)
        if match:
            question = int(match.group(1))
            run = 0
            continue
        option = OPTION.match(line)
        if option:
            rest = strip_dfrac(option.group(1))
            if rest is not None and PLAIN.match(rest):
                run += 1
                worst = max(worst, run)
                hits.append(question)
            else:
                run = 0
        elif line.startswith("（"):
            run = 0
    return {"path": path.as_posix(), "fraction_options": len(hits), "max_run": worst,
            "questions": sorted({q for q in hits if q})}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="仓库根目录")
    parser.add_argument("--report", default="math-gaokao-latex/reports/option-spacing-audit.md")
    parser.add_argument("--json", default="math-gaokao-latex/reports/option-spacing-audit.json")
    parser.add_argument("--write", action="store_true", help="写入报告文件（默认只打印摘要）")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    files = sorted(root.glob("20*/*_试题.md")) + sorted(root.glob("19*/*_试题.md"))
    rows = [audit_file(path.relative_to(root)) for path in files]
    risky = [r for r in rows if r["max_run"] >= 2]
    mild = [r for r in rows if r["fraction_options"] and r["max_run"] < 2]
    risky.sort(key=lambda r: (-r["max_run"], -r["fraction_options"], r["path"]))

    lines = [
        "# 选项行距审计（独立 `\\dfrac` 选项）",
        "",
        "扫描范围：`19*/`、`20*/` 下全部 `_试题.md`。判定见 `tools/audit_option_spacing.py`。",
        "",
        "## 摘要",
        "",
        f"- 审计卷数：**{len(rows)}**",
        f"- 含独立分式选项：**{len(risky) + len(mild)}** 卷（确定重叠风险 {len(risky)} 卷，低风险 {len(mild)} 卷）",
        f"- 独立分式选项行合计：**{sum(r['fraction_options'] for r in rows)}**",
        "",
        "## 确定重叠风险（同题连续 >=2 条）",
        "",
        "| 卷 | 连续段长度 | 独立分式选项数 | 涉及题号 |",
        "| --- | --- | --- | --- |",
    ]
    for row in risky:
        lines.append("| `%s` | %d | %d | %s |" % (
            row["path"], row["max_run"], row["fraction_options"],
            "、".join(str(q) for q in row["questions"]),
        ))
    lines += ["", "## 低风险（单条独立分式）", "", "| 卷 | 选项数 | 涉及题号 |", "| --- | --- | --- |"]
    for row in mild:
        lines.append("| `%s` | %d | %s |" % (
            row["path"], row["fraction_options"],
            "、".join(str(q) for q in row["questions"]),
        ))
    lines += [
        "",
        "## 处置口径",
        "",
        "1. 选项行内的 `\\dfrac` 改为行内 `\\frac`（已验证不改变分页时可直接沿用原视觉回执）；",
        "2. 逐卷 `generate_projects` → 重算 provenance 哈希 → `build --formal` → `prepare/finalize`；",
        "3. 分页若有变化，必须重新逐页审查，不得沿用旧回执。",
        "",
    ]
    text = "\n".join(lines)
    print("\n".join(lines[:12]))
    if args.write:
        (root / args.report).write_text(text, encoding="utf-8")
        (root / args.json).write_text(
            json.dumps({"papers": len(rows), "risky": risky, "mild": mild},
                       ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
        )
        print("已写入 %s / %s" % (args.report, args.json))
    return 0


if __name__ == "__main__":
    sys.exit(main())

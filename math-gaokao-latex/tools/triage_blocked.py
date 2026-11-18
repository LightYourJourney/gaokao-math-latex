"""从 manifest / 回执 / provenance / issues 机械生成 blocked 分流表。

分类互斥且可按行复算：
1 缺源   : source_ids 为空
2 保留 U : provenance 存在 grade == "U" 的题
3 保留 U（源缺陷/歧义）: 无 U 但有 status != resolved 的 issue
4 可收口 : 无 U、无未结 issue
"""
import json
import os
import re
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]

# 立项时属于 111 套 blocked、本轮补源/修源后已封账的 5 套（附封账提交）
SEALED = {
    "gk-1986-regular-guangdong-arts": "1b2233070",
    "gk-1987-regular-national-science": "e65b0d18a",
    "gk-2003-spring-beijing-science": "e65b0d18a",
    "gk-2020-regular-national-1-arts": "12e987200",
    "gk-2022-regular-national-b-arts": "c30406301",
}
SRC = Path(os.environ.get("GAOKAOMATH_SRC", str(Path(__file__).resolve().parents[2] / "gaokaomath-src")))


def issue_table():
    text = (PROJ / "missing-issues.md").read_text(encoding="utf-8")
    out = {}
    for block in re.split(r"\n(?=## ISSUE-)", text):
        iid = re.match(r"## (ISSUE-\d+)", block)
        if not iid:
            continue
        pid = re.search(r'"paper_id":\s*"(gk-[^"]+)"', block) or re.search(r"paper_id[:：]\s*`?(gk-[a-z0-9\-]+)", block)
        typ = re.search(r'"type":\s*"([^"]+)"', block) or re.search(r"type[:：]\s*`?([a-z\-]+)", block)
        st = re.search(r'"status":\s*"([^"]+)"', block) or re.search(r"status[:：]\s*`?([a-z\-]+)", block)
        out[iid.group(1)] = {
            "paper_id": pid.group(1) if pid else None,
            "type": typ.group(1) if typ else "?",
            "status": st.group(1) if st else "?",
        }
    return out


U_MARK = re.compile(r"U/PENDING|答案：\s*U\b|待核|待定")


def md_u_numbers(p):
    """答案要点里被标成 U/待核 的题号（与 provenance 判定互为独立来源）。"""
    sf = p.get("source_files") or {}
    path = sf.get("answer_key")
    if not path:
        return set()
    f = PROJ.parent / path
    if not f.exists():
        return set()
    out = set()
    for block in re.split(r"(?=\*\*\d+[．.]\*\*)", f.read_text(encoding="utf-8")):
        m = re.match(r"\*\*(\d+)[．.]\*\*", block)
        if m and U_MARK.search(block):
            out.add(int(m.group(1)))
    return out


def main():
    manifest = json.loads((PROJ / "source-manifest.json").read_text(encoding="utf-8"))
    issues = issue_table()
    rows = []
    for p in manifest["papers"]:
        sealed = p["paper_id"] in SEALED
        if p["production_state"] == "complete" and not sealed:
            continue
        prov = PROJ / p["project_dir"] / "provenance.json"
        u_nums = []
        if prov.exists():
            data = json.loads(prov.read_text(encoding="utf-8"))
            for q in data.get("questions", []):
                if (q.get("answer_evidence") or {}).get("grade") == "U":
                    u_nums.append(str(q.get("printed_number")))
        mdU = md_u_numbers(p)
        provU = {int(x) for x in u_nums}
        u_all = sorted(provU | mdU)
        diverge = "—"
        if provU != mdU:
            extra_md, extra_prov = sorted(mdU - provU), sorted(provU - mdU)
            bits = []
            if extra_md:
                bits.append("题面多 " + ",".join(map(str, extra_md)))
            if extra_prov:
                bits.append("provenance 多 " + ",".join(map(str, extra_prov)))
            diverge = "；".join(bits)
        ids = p.get("issue_ids") or []
        open_ids = [i for i in ids if issues.get(i, {}).get("status") != "resolved"]
        open_types = sorted({issues[i]["type"] for i in open_ids if i in issues})
        build = PROJ / p["project_dir"] / "receipts/build.json"
        review = PROJ / p["project_dir"] / "receipts/review.json"
        bstat = json.loads(build.read_text(encoding="utf-8"))["status"] if build.exists() else "—"
        rstat = json.loads(review.read_text(encoding="utf-8"))["status"] if review.exists() else "—"
        on_disk = "—"
        if p.get("source_ids"):
            on_disk = "是"
            src = next((s for s in manifest["sources"] if s["source_id"] in p["source_ids"]), None)
            up = (src or {}).get("upstream_path")
            if not up or not (SRC / up).exists():
                on_disk = "否"

        if sealed:
            cat = f"补源后完成（本轮封账，提交 {SEALED[p['paper_id']]}）"
        elif not p.get("source_ids"):
            cat = "缺源"
        elif u_all:
            cat = "保留 U"
        elif open_ids:
            cat = "保留 U（源缺陷/歧义）"
        else:
            cat = "可收口"
        rows.append((p["year"], p["paper_id"], p.get("blocked_from") or "—", bstat, rstat,
                     ",".join(map(str, u_all)) or "—", diverge, ",".join(open_ids) or "—",
                     ",".join(open_types) or "—", on_disk, cat))

    counts = {}
    for r in rows:
        counts[r[-1]] = counts.get(r[-1], 0) + 1
    diverged = [r for r in rows if r[6] != "—"]
    out = [
        "# blocked 卷逐条复核与分流（机械生成）",
        "",
        "本文件由 `tools/triage_blocked.py` 从 manifest、各卷 `receipts/build.json`、`receipts/review.json`、",
        "`provenance.json`、`missing-issues.md` 与上游 PDF 磁盘存在性机械生成，不手写判据。",
        "",
        "## 分类规则（互斥，按序判定）",
        "",
        "1. **缺源**：`source_ids` 为空。",
        "2. **保留 U**：`provenance.json` 的 `answer_evidence.grade == \"U\"` 或答案要点里标成 `U`/`待核` 的题（两个独立来源取并集；两者不一致时在「U 判定分歧」列逐卷列出）。",
        "3. **保留 U（源缺陷/歧义）**：无 U，但仍有 `status != resolved` 的 issue。",
        "4. **可收口**：无 U、无未结 issue。",
        "",
        "机制约束：`tools/provenance.py` 把任一题 `grade == \"U\"` 记为 `provenance_unknown`，",
        "`tools/status.py` 据此派生 `eligible_blocked`；构建本身可成功（回执 `succeeded`），但派生状态落为 blocked、不予封账——含 U 的卷只能按「保留 U 并登记 ISSUE」交付。",
        "",
        "## 与 objective 三分法的对应",
        "",
        "| objective 要求 | 本表分类 | 含义 |",
        "|---|---|---|",
        "| 补源后完成 | 保留 U（源缺陷/歧义） | 固定源在盘但印面有缺字/歧义，需外部勘误或独立扫描页重证；修好后可走完 build→review→finalize |",
        "| 保留 U 并登记 ISSUE | 保留 U | 源文不足以唯一判定，按 U 政策不写确定答案，逐题 ISSUE 已登记 |",
        "| 确认 missing-source | 缺源 | `source_ids` 为空，无任何固定上游（2026 回忆版） |",
        "",
        "## 口径对账（111 套从哪来）",
        "",
        "目标里的 111 套 blocked 是立项时（2026-11-09）的口径注记，**无法从当前仓库机械复算**；本轮已封账 5 套（`gk-1986-regular-guangdong-arts`、",
        "`gk-1987-regular-national-science`、`gk-2003-spring-beijing-science`、`gk-2020-regular-national-1-arts`、",
        "`gk-2022-regular-national-b-arts`；封账提交分别为 1b2233070 / e65b0d18a / 12e987200 / c30406301），",
        "另有 3 套原为 `compiled` 的已封账（`gk-2019-regular-national-1-{arts,science}`、`gk-2020-regular-national-1-science`，提交 12e987200）。",
        "因此 111 = 本表 106 套 + 已封账 5 套。",
        "",
        "## 计数",
        "",
        f"- 复核总数：**{len(rows)}** 套（106 套当前未完成 + 5 套本轮已封账）",
    ]
    for k in ("补源后完成", "可收口", "保留 U", "保留 U（源缺陷/歧义）", "缺源"):
        n = sum(v for kk, v in counts.items() if kk.startswith(k)) if k == "补源后完成" else counts.get(k, 0)
        out.append(f"- {k}：**{n}** 套")
    out += ["", "## U 判定分歧", "",
            f"- 存在分歧的卷：**{len(diverged)}** 套（题面标记与 provenance 判定不一致，按并集仍计为保留 U）", ""]
    for r in diverged:
        out.append(f"- `{r[1]}`：{r[6]}")
    out += ["", "## 逐卷", "",
            "| 年 | 试卷 | blocked_from | build | review | U 题号 | U 判定分歧 | 未结 ISSUE | ISSUE 类型 | 上游 PDF 在盘 | 结论 |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    (PROJ / "reports/blocked-triage.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("rows", len(rows), counts)


if __name__ == "__main__":
    main()

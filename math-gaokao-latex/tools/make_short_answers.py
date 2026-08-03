#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_short_answers.py —— 为每套试卷生成简答版数据 answers_short.tex。

主源： 答案要点 MD 的逐题「> **答案：...**」行——该文档本就是
      "每题给最终答案"的口径，全题覆盖（解析 tex 的 \\gkanswer 框并非每题都有，
      实测 14 卷中 11 卷与题量不符，不能当主源）。
      MD 行内格式经合并书 tools/md2tex.py 的 conv_inline 转为 LaTeX。

交叉核对（选择题字母，三源）：
  1. MD 逐题答案行（主源）；
  2. MD 开头「答案速查表」；
  3. answers.tex 各 answer 环境内的首个 \\gkanswer（若存在且为字母形）。
  任何不一致即报错退出——宁可失败也不产出多源矛盾的速查表。

输出结构：选择题各组一张 booktabs 表；填空题、解答题逐题列表。
依赖：先运行 split_project.py（读取 index.json 与各卷 answers.tex）。
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DST = HERE.parent
SRC = DST.parent / "math-gaokao-2017-2026"
EXAMS = DST.parent          # 本项目位于  之下，父目录即真题 MD 库

sys.path.insert(0, str(SRC / "tools"))
import md2tex  # noqa: E402  复用行内 MD→LaTeX 转换（纯函数，有 __main__ 保护）

CHOICE_GROUPS = ("选择题", "单选题", "多选题")
QNUM = re.compile(r"^\*\*(\d+)．")                      # 全角句点；容忍〔选修〕后缀
# 整体答案行两种冒号位形：**答案：xxx**（冒号在内，非贪婪剥掉行尾"（同理科…）"类尾注）
# 与 **答案**：xxx（冒号在加粗外）
ANS_IN = re.compile(r"^>\s*\*\*答案[：:]\s*(.+?)\*\*")
ANS_OUT = re.compile(r"^>\s*\*\*答案[^*]*\*\*[：:]\s*(.+)$")
# 分问答案行同样两种冒号位形；SUB_ANY 兜底捕捉"**(k) 证明要点**："等非答案锚点
SUB_IN = re.compile(r"^>\s*\*\*[（(](\d+)[)）]\s*答案[^*：:]*[：:]\s*(.+?)\*\*")
SUB_OUT = re.compile(r"^>\s*\*\*[（(](\d+)[)）]\s*答案[^*]*\*\*[：:]\s*(.*)$")
SUB_ANY = re.compile(r"^>\s*\*\*[（(](\d+)[)）]")
PREFIX = re.compile(r"^答案[：:]\s*")
SEE_SOL = "见解析版"   # 证明问 / 表格式答案（分布列等）无法单行给结论时的诚实占位


def md_per_question(md_file):
    """逐题提取答案（MD 格式原文），返回 {题号: 文本}。

    每题块内优先取整体答案行；没有则把各分问锚点拼为 "(1) …；(2) …"——
    计算问取其结论，证明问/表格问记"见解析版"（不硬造单行答案）。"""
    whole, subs, head_rest = {}, {}, {}
    cur = None
    for line in md_file.read_text(encoding="utf-8").split("\n"):
        m = QNUM.match(line)
        if m:
            cur = int(m.group(1))
            # 题头行剩余若以 "(1)" 开头，是把答案直接写在题头的变体（如 2020 文选做题）
            rest = re.sub(r"^\*\*(\d+)．[^*]*\*\*\s*", "", line).strip()
            if re.match(r"^[（(]1[)）]", rest):
                head_rest[cur] = rest
            continue
        if cur is None:
            continue
        m = SUB_IN.match(line) or SUB_OUT.match(line)
        if m:
            text = m.group(2).strip() or SEE_SOL
            subs.setdefault(cur, {}).setdefault(int(m.group(1)), text)
            continue
        m = SUB_ANY.match(line)
        if m:
            subs.setdefault(cur, {}).setdefault(int(m.group(1)), SEE_SOL)
            continue
        m = ANS_IN.match(line) or ANS_OUT.match(line)
        if m and cur not in whole:
            whole[cur] = m.group(1).strip()
    ans = dict(whole)
    for q, pairs in subs.items():
        if q not in ans:
            # 各分问段末的句号在拼接前剥掉，避免 PDF 里出现"。；"连排
            ans[q] = "；".join(f"({k}) {v.rstrip('。')}"
                               for k, v in sorted(pairs.items()))
    for q, rest in head_rest.items():
        ans.setdefault(q, rest)
    return ans


def md_quick_table(md_file, n_choice):
    """从「答案速查表」抓前 n_choice 个字母；解析不出返回 None。"""
    cells = []
    for line in md_file.read_text(encoding="utf-8").split("\n"):
        s = line.strip()
        if s.startswith("| 答案"):
            cells += [c.strip() for c in s.strip("|").split("|")][1:]
    return cells[:n_choice] if len(cells) >= n_choice else None


def tex_gkanswer_letters(tex_file):
    """按 answer 环境分块，取块内首个 \\gkanswer 的前缀字母；无则 None。按题序返回列表。"""
    text = tex_file.read_text(encoding="utf-8")
    out = []
    for block in re.findall(r"\\begin\{answer\}(.*?)\\end\{answer\}", text, re.DOTALL):
        m = re.search(r"\\gkanswer\{答案[：:]\s*([A-D]+)", block)
        out.append(m.group(1) if m else None)
    return out


def md_path(p):
    y = p["year"]
    if p["track"]:
        t = "理" if p["track"] == "理科" else "文"
        return EXAMS / str(y) / f"{y}_数学真题_{t}_答案要点.md"
    return EXAMS / str(y) / f"{y}_数学真题_答案要点.md"


def build_table(nums, letters):
    head = " & ".join(str(n) for n in nums)
    body = " & ".join(letters)
    return ("\\begin{center}\\begin{tabular}{c" + "c" * len(nums) + "}\n"
            "\\toprule\n题号 & " + head + " \\\\\n\\midrule\n"
            "答案 & " + body + " \\\\\n\\bottomrule\n"
            "\\end{tabular}\\end{center}")


def main():
    index = json.loads((DST / "index.json").read_text(encoding="utf-8"))
    errors, warns = [], []
    for p in index["papers"]:
        pdir = DST / p["dir"]
        n = p["questions"]
        mdf = md_path(p)
        if not mdf.is_file():
            errors.append(f"{p['dir']}: 缺主源 {mdf.name}")
            continue

        raw = md_per_question(mdf)
        missing = [i for i in range(1, n + 1) if i not in raw]
        if missing:
            errors.append(f"{p['dir']}: MD 中提不到答案行的题号 {missing}")
            continue

        # MD → LaTeX 行内转换；conv_inline 的警告（未配对 $ 等）视为硬错误
        md2tex.warnings.clear()
        answers = {i: md2tex.conv_inline(raw[i]) for i in range(1, n + 1)}
        if md2tex.warnings:
            errors.append(f"{p['dir']}: 行内转换警告 {md2tex.warnings[:3]}")
            md2tex.warnings.clear()
            continue

        # 组装 + 收集选择题字母
        parts, choice_letters, choice_nums = [], [], []
        for gname, (lo, hi) in p["structure"].items():
            nums = list(range(lo, hi + 1))
            if gname in CHOICE_GROUPS:
                letters = []
                for i in nums:
                    m = re.match(r"^([A-D]+)", answers[i])
                    if not m:
                        errors.append(f"{p['dir']}: 第 {i} 题选择题答案非字母形：{answers[i][:40]}")
                        letters.append("?")
                    else:
                        letters.append(m.group(1))
                choice_letters += letters
                choice_nums += nums
                parts.append("\\gkpart{" + gname + "}\n" + build_table(nums, letters))
            else:
                lines = ["\\gkpart{" + gname + "}",
                         "\\begin{itemize}[leftmargin=2.6em]"]
                for i in nums:
                    lines.append(f"  \\item[\\textbf{{{i}.}}] {PREFIX.sub('', answers[i])}")
                lines.append("\\end{itemize}")
                parts.append("\n".join(lines))

        # 核对 2：MD 速查表
        quick = md_quick_table(mdf, len(choice_letters))
        if quick is None:
            warns.append(f"{p['dir']}: 速查表解析失败，跳过该路核对")
        elif quick != choice_letters:
            diff = [f"题{choice_nums[i]} 表={a} 行={b}"
                    for i, (a, b) in enumerate(zip(quick, choice_letters)) if a != b]
            errors.append(f"{p['dir']}: 速查表与逐题答案行不一致：{'; '.join(diff)}")

        # 核对 3：answers.tex 的 \gkanswer（存在且为字母形的位置）
        tex_letters = tex_gkanswer_letters(pdir / "answers.tex")
        if len(tex_letters) == n:
            for idx, qn in enumerate(choice_nums):
                t = tex_letters[qn - 1]
                if t is not None and t != choice_letters[idx]:
                    errors.append(f"{p['dir']}: 题{qn} 解析框={t} 与 MD={choice_letters[idx]} 不一致")
        else:
            warns.append(f"{p['dir']}: answer 环境数 {len(tex_letters)} ≠ 题量，跳过该路核对")

        body = "\n\n".join(parts)
        content = (f"% answers_short.tex —— {p['title']} · 简短答案速查\n"
                   f"% 由 tools/make_short_answers.py 自答案要点 MD 逐题答案行生成，勿手改；\n"
                   f"% 选择题字母经三源交叉核对（逐题行 / 速查表 / 解析 \\gkanswer 框）。\n\n"
                   "\\begin{gknotice}\n"
                   "\\textbf{使用说明}：本节只给最终答案便于快速核对，完整推导见解析版。"
                   "答案为编写者独立推导，\\textbf{非官方标准答案}。\n"
                   "\\end{gknotice}\n\n" + body + "\n")
        (pdir / "answers_short.tex").write_text(content, encoding="utf-8")
        print(f"✓ {p['dir']}: {n} 题简答就绪")

    for w in warns:
        print("⚠", w)
    if errors:
        print("\n== 校验失败 ==")
        for e in errors:
            print("  ✗", e)
        sys.exit(1)
    print("\n全部通过：14 份 answers_short.tex 已生成。")


if __name__ == "__main__":
    main()

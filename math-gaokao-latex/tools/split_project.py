#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_project.py —— 把合并书 math-gaokao-2017-2026 拆分为 14 个独立试卷项目。

每个试卷目录生成：
  questions.tex   题目内容片段（每题包 question 环境；无任何答案）
  answers.tex     解析内容片段（每题解析包 answer 环境）
  figures/        该卷引用到的 TikZ 图（从合并书 figures/ 复制副本，不改内容）

同时在项目根生成 index.json（卷别、题量、合并 PDF 中的页码范围等元数据）。

切分边界（经对合并书生成物的实测确认）：
  questions：题块起于行首 \\gkti{N}，止于下一个 \\gkti / \\gkpart / \\gksubpart / 文件尾
             （papers 里 \\gksubpart 只用作"（一）必考题"类节级标题）；
  answers  ：题块起于行首 \\gksolhead{N}{..}，止于下一个 \\gksolhead / \\gkpart / 文件尾
             （answers 里 \\gksubpart 是题内小问标题，绝不能作为边界！）。

校验（任一失败即退出码非零并打印明细）：
  1. 往返校验：生成片段删除环境行与生成头注后，须与合并书源文件逐字节一致；
  2. 计数校验：question / answer 环境数须等于已知题量表。
幂等：重复运行覆盖生成物。
"""
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DST = HERE.parent                                  # math-gaokao-latex/
SRC = DST.parent / "math-gaokao-2017-2026"         # 合并书项目

# 14 套试卷元数据。
# pdf_pages 为合并书正文逻辑页码（书内页脚所印页码，取自 main.toc）。
PAPERS = [
    dict(dir="2017_全国Ⅰ卷_理科", id="2017li",  base="2017_g1_li",
         year=2017, paper="全国Ⅰ卷", track="理科",
         title="2017 年·全国Ⅰ卷·理科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[1, 6], pages_s=[7, 33],
         note="含现已取消的选做题第 22/23 题与已删除的三视图、程序框图考点"),
    dict(dir="2017_全国Ⅰ卷_文科", id="2017wen", base="2017_g1_wen",
         year=2017, paper="全国Ⅰ卷", track="文科",
         title="2017 年·全国Ⅰ卷·文科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[34, 39], pages_s=[40, 64],
         note="含现已取消的选做题第 22/23 题与已删除的三视图、程序框图考点"),
    dict(dir="2018_全国Ⅰ卷_理科", id="2018li",  base="2018_g1_li",
         year=2018, paper="全国Ⅰ卷", track="理科",
         title="2018 年·全国Ⅰ卷·理科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[65, 69], pages_s=[70, 92],
         note="含现已取消的选做题第 22/23 题"),
    dict(dir="2018_全国Ⅰ卷_文科", id="2018wen", base="2018_g1_wen",
         year=2018, paper="全国Ⅰ卷", track="文科",
         title="2018 年·全国Ⅰ卷·文科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[93, 97], pages_s=[98, 116],
         note="含现已取消的选做题第 22/23 题"),
    dict(dir="2019_全国Ⅰ卷_理科", id="2019li",  base="2019_g1_li",
         year=2019, paper="全国Ⅰ卷", track="理科",
         title="2019 年·全国Ⅰ卷·理科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[117, 121], pages_s=[122, 147],
         note="含现已取消的选做题第 22/23 题"),
    dict(dir="2019_全国Ⅰ卷_文科", id="2019wen", base="2019_g1_wen",
         year=2019, paper="全国Ⅰ卷", track="文科",
         title="2019 年·全国Ⅰ卷·文科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[148, 152], pages_s=[153, 171],
         note="含现已取消的选做题第 22/23 题"),
    dict(dir="2020_全国Ⅰ卷_理科", id="2020li",  base="2020_g1_li",
         year=2020, paper="全国Ⅰ卷", track="理科",
         title="2020 年·全国Ⅰ卷·理科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[172, 176], pages_s=[177, 202],
         note="含现已取消的选做题第 22/23 题"),
    dict(dir="2020_全国Ⅰ卷_文科", id="2020wen", base="2020_g1_wen",
         year=2020, paper="全国Ⅰ卷", track="文科",
         title="2020 年·全国Ⅰ卷·文科", questions=23,
         structure={"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
         pages_q=[203, 207], pages_s=[208, 226],
         note="含现已取消的选做题第 22/23 题"),
    dict(dir="2021_新高考Ⅰ卷", id="2021", base="2021_xgk1",
         year=2021, paper="新高考Ⅰ卷", track=None,
         title="2021 年·新高考Ⅰ卷", questions=22,
         structure={"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
         pages_q=[227, 230], pages_s=[231, 257], note=None),
    dict(dir="2022_新高考Ⅰ卷", id="2022", base="2022_xgk1",
         year=2022, paper="新高考Ⅰ卷", track=None,
         title="2022 年·新高考Ⅰ卷", questions=22,
         structure={"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
         pages_q=[258, 261], pages_s=[262, 293], note=None),
    dict(dir="2023_新高考Ⅰ卷", id="2023", base="2023_xgk1",
         year=2023, paper="新高考Ⅰ卷", track=None,
         title="2023 年·新高考Ⅰ卷", questions=22,
         structure={"单选题": [1, 8], "多选题": [9, 12], "填空题": [13, 16], "解答题": [17, 22]},
         pages_q=[294, 297], pages_s=[298, 325], note=None),
    dict(dir="2024_新高考Ⅰ卷", id="2024", base="2024_xgk1",
         year=2024, paper="新高考Ⅰ卷", track=None,
         title="2024 年·新高考Ⅰ卷", questions=19,
         structure={"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
         pages_q=[326, 329], pages_s=[330, 356], note=None),
    dict(dir="2025_全国1卷", id="2025", base="2025_g1",
         year=2025, paper="全国 1 卷", track=None,
         title="2025 年·全国 1 卷", questions=19,
         structure={"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
         pages_q=[357, 360], pages_s=[361, 383], note=None),
    dict(dir="2026_全国1卷_回忆版", id="2026", base="2026_g1",
         year=2026, paper="全国 1 卷", track=None,
         title="2026 年·全国 1 卷（回忆版）", questions=19,
         structure={"单选题": [1, 8], "多选题": [9, 11], "填空题": [12, 14], "解答题": [15, 19]},
         pages_q=[384, 387], pages_s=[388, 420],
         note="回忆版：依据考生回忆整理，正式卷公开后应以官方版本校订"),
]

GEN_MARK = "% 【拆分生成】"          # 生成头注行前缀（往返校验时剔除）
ENV_LINES = {"\\begin{question}", "\\end{question}",
             "\\begin{answer}", "\\end{answer}"}

Q_HEAD = re.compile(r"^\\gkti\{(\d+)\}")
S_HEAD = re.compile(r"^\\gksolhead\{(\d+)\}\{")
STRUCT_Q = re.compile(r"^\\(gkpart|gksubpart)\{")   # questions 的结构标题
STRUCT_S = re.compile(r"^\\gkpart\{")               # answers 只认 gkpart（gksubpart 是题内小问）


def wrap(text, head_re, struct_re, env):
    """按行首题头切分并包裹环境；返回 (包裹后文本, 题号列表)。"""
    out, nums, in_block = [], [], False
    for line in text.split("\n"):
        m = head_re.match(line)
        if m:
            if in_block:
                out.append("\\end{%s}" % env)
            out.append("\\begin{%s}" % env)
            out.append(line)
            nums.append(int(m.group(1)))
            in_block = True
        elif struct_re.match(line):
            if in_block:
                out.append("\\end{%s}" % env)
                in_block = False
            out.append(line)
        else:
            out.append(line)
    if in_block:
        out.append("\\end{%s}" % env)
    return "\n".join(out), nums


def strip_generated(text):
    """删除生成头注与环境行，用于往返校验。"""
    kept = [l for l in text.split("\n")
            if not l.startswith(GEN_MARK) and l.strip() not in ENV_LINES]
    return "\n".join(kept)


def make_fragment(src_file, head_re, struct_re, env, header_lines):
    raw = src_file.read_text(encoding="utf-8")
    wrapped, nums = wrap(raw, head_re, struct_re, env)
    header = "\n".join(GEN_MARK + " " + h for h in header_lines)
    final = header + "\n" + wrapped
    # 往返校验：剔除生成行后必须与源文件逐字节一致
    if strip_generated(final) != raw:
        raise AssertionError(f"往返校验失败：{src_file.name}")
    return final, nums


def main():
    if not SRC.is_dir():
        sys.exit(f"找不到合并书项目：{SRC}")
    errors = []
    index_papers = []
    for p in PAPERS:
        pdir = DST / p["dir"]
        (pdir / "figures").mkdir(parents=True, exist_ok=True)

        src_q = SRC / "papers" / (p["base"] + ".tex")
        src_s = SRC / "answers" / (p["base"] + "_sol.tex")

        q_text, q_nums = make_fragment(
            src_q, Q_HEAD, STRUCT_Q, "question",
            [f"questions.tex —— {p['title']} · 题目内容片段（无答案）",
             f"由 tools/split_project.py 自合并书 papers/{p['base']}.tex 包裹 question 环境生成，勿手改"])
        s_text, s_nums = make_fragment(
            src_s, S_HEAD, STRUCT_S, "answer",
            [f"answers.tex —— {p['title']} · 参考答案与详细解析片段",
             f"由 tools/split_project.py 自合并书 answers/{p['base']}_sol.tex 包裹 answer 环境生成，勿手改"])

        (pdir / "questions.tex").write_text(q_text, encoding="utf-8")
        (pdir / "answers.tex").write_text(s_text, encoding="utf-8")

        # 计数校验：环境数与题号连续性
        expect = list(range(1, p["questions"] + 1))
        if q_nums != expect:
            errors.append(f"{p['dir']}: questions 题号异常 {q_nums}")
        if s_nums != expect:
            errors.append(f"{p['dir']}: answers 题号异常 {s_nums}")

        # figures 分发：按内容引用复制
        figs = sorted(set(re.findall(r"figures/([A-Za-z0-9_]+)", q_text + s_text)))
        for f in figs:
            src_fig = SRC / "figures" / (f + ".tex")
            if src_fig.is_file():
                shutil.copy2(src_fig, pdir / "figures" / (f + ".tex"))
            else:
                errors.append(f"{p['dir']}: 缺图 figures/{f}.tex")

        index_papers.append({
            "dir": p["dir"], "id": p["id"], "base": p["base"],
            "year": p["year"], "paper": p["paper"], "track": p["track"],
            "title": p["title"], "questions": p["questions"],
            "structure": p["structure"],
            "pdf_pages": {"questions": p["pages_q"], "solutions": p["pages_s"]},
            "figures": [f + ".tex" for f in figs],
            "note": p["note"],
        })
        print(f"✓ {p['dir']}: {len(q_nums)} 题, {len(figs)} 图")

    index = {
        "generated_by": "tools/split_project.py",
        "source_project": "../math-gaokao-2017-2026",
        "source_pdf": "../math-gaokao-2017-2026/main.pdf",
        "page_numbering_note": "pdf_pages 为合并书正文逻辑页码（书内页脚所印）；"
                               "换算 PDF 物理页需加前言罗马页偏移。",
        "editions": ["试题版", "解析版", "简答版", "印刷版"],
        "papers": index_papers,
    }
    (DST / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("\n== 校验失败 ==")
        for e in errors:
            print("  ✗", e)
        sys.exit(1)
    print(f"\n全部通过：{len(PAPERS)} 套试卷片段 + index.json 已生成。")


if __name__ == "__main__":
    main()

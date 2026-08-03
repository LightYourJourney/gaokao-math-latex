#!/usr/bin/env python3
"""md2tex.py —— 把本知识库  的真题 Markdown 转成本项目的 LaTeX 正文片段。

用法：python3 tools/md2tex.py <输入.md> <输出.tex>

只针对本库自产 MD 方言（格式规整），映射规则：
  frontmatter / 一级二级卷名标题     -> 丢弃（章标题由 main.tex 提供）
  ## 一、选择题                      -> \\gkpart{...}
  ### 第 N 题（考点）                -> \\gksolhead{N}{考点}
  ### / #### 其他标题                -> \\gksubpart{...}
  **N．** / **N．（12 分）**         -> \\gkti{N}（分值保留加粗）
  连续的选项行（A．… B．…）          -> gkopts 环境（列数按最长选项自适应）
  > 引用块                           -> gknotice / gktip（按内容分类；含"原卷影印件/配套文档"者丢弃）
  **答案：…** 独立段                  -> \\gkanswer{...}
  管道表格                           -> booktabs 三线表
  ![..](images/xxx.png)              -> \\input{figures/<slug>}（映射表见 FIGMAP）
  $$...$$                            -> \\[...\\]
  \\_ 连续下划线（填空）              -> \\gkblank
数学段（$...$ 内部）原样透传，只对文本段做加粗/链接/转义处理。
"""
import re
import sys
from pathlib import Path

# ---------- 配图映射：MD 图片基名 -> figures/ 下的 TikZ 文件名 ----------
FIGMAP = {
    "2017理-t2-太极图": "f2017_taiji",     "2017文-t4-太极图": "f2017_taiji",
    "2017理-t7-三视图": "f2017li_t7_views",
    "2017理-t8-程序框图": "f2017_flow",    "2017文-t10-程序框图": "f2017_flow",
    "2017理-t16-圆纸片": "f2017li_t16_paper",
    "2017理-t18-四棱锥": "f2017_t18_pyramid", "2017文-t18-四棱锥": "f2017_t18_pyramid",
    "2017文-t6-正方体AB": "f2017wen_t6_cubesAB",
    "2017文-t6-正方体CD": "f2017wen_t6_cubesCD",
    "2017文-t8-四图": "f2017wen_t8_panels",
    "2018理-t3-饼图": "f2018_t3_pies",     "2018文-t3-饼图": "f2018_t3_pies",
    "2018理-t7-三视图": "f2018_t7_views",  "2018文-t9-三视图": "f2018_t7_views",
    "2018理-t10-月牙": "f2018li_t10_lune",
    "2018理-t18-折叠": "f2018li_t18_fold", "2018文-t18-折叠": "f2018wen_t18_fold",
    "2018文-t19-直方图网格": "f2018wen_t19_grid",
    "2019理-t5-四图": "f2019_t5_panels",   "2019文-t5-四图": "f2019_t5_panels",
    "2019理-t8-程序框图": "f2019_flow",    "2019文-t9-程序框图": "f2019_flow",
    "2019理-t18-棱柱": "f2019_t18_prism",  "2019文-t19-棱柱": "f2019_t18_prism",
    "2020理-t5-散点图": "f2020li_t5_scatter",
    "2020理-t7-图象": "f2020li_t7_graph",
    "2020理-t16-展开图": "f2020li_t16_unfold",
    "2020理-t18-圆锥": "f2020li_t18_cone",
    "2020文-t9-程序框图": "f2020wen_t9_flow",
    "2020文-t19-圆锥": "f2020wen_t19_cone",
    "2021-t20-三棱锥": "f2021_t20_tetra",
    "2021-Ⅱ-t10-正方体": "f2021x2_t10_cubes",
    "2021-Ⅱ-t19-四棱锥": "f2021x2_t19_pyr",
    "2022-t19-棱柱": "f2022_t19_prism",
    "2023-t18-棱柱": "f2023_t18_prism",
    "2024-t11-曲线": "f2024_t11_curve",
    "2024-t17-四棱锥": "f2024_t17_pyramid",
    "2025-t6-风速": "f2025_t6_wind",
    "2025-t17-四棱锥": "f2025_t17_pyramid",
    "2026-t15-棱柱": "f2026_t15_prism",
}

EMOJI = "⚠️⚠✓✗📘⏳✅❌🔺"

warnings: list[str] = []


# ---------- 行内处理 ----------
# 文本段中裸写的数学 Unicode 符号（源 MD 少量存在）→ 等价数学命令
BARE_SYM = {
    "⟹": r"~$\Longrightarrow$~", "∩": r"$\cap$", "∪": r"$\cup$",
    "⊥": r"$\perp$", "≠": r"$\neq$", "∥": r"$\parallel$",
    "◇": r"$\Diamond$", "▭": r"$\square$", "−": r"$-$",
    "∈": r"$\in$", "⊂": r"$\subset$",
}

CJK_IN_MATH = re.compile(r"([\u4e00-\u9fff、，；：]+)")


def conv_inline(s: str) -> str:
    # 顺序要点：加粗/链接先做（它们可以跨数学段，如 **……$x$……**），
    # 再按 $ 切分，只对文本段做转义与符号替换
    for ch in EMOJI:
        s = s.replace(ch, "")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)         # 链接 -> 纯文本
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)       # 加粗（非贪婪，可含 $…$）
    s = re.sub(r"`([^`]+)`", r"\\texttt{\1}", s)           # 行内代码

    parts = s.split("$")
    if len(parts) % 2 == 0:  # $ 不配对——原样返回并记警告
        warnings.append(f"未配对的 $：{s[:60]}")
        return s
    out = []
    for i, seg in enumerate(parts):
        if i % 2 == 1:               # 数学段：仅把裸中文包进 \text（西文数学字体缺 CJK 字形）
            seg = CJK_IN_MATH.sub(r"\\text{\1}", seg)
            out.append(f"${seg}$")
        else:                        # 文本段
            out.append(conv_text(seg))
    return "".join(out)


def conv_text(s: str) -> str:
    s = re.sub(r"(?:\\_){3,}", r"\\gkblank{}", s)          # 填空下划线
    s = s.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
    for k, v in BARE_SYM.items():
        s = s.replace(k, v)
    return s


# ---------- 选项组 ----------
OPT_SPLIT = re.compile(r"(?:　+|\s{2,})(?=[A-D]．)")

def emit_options(lines: list[str]) -> list[str]:
    merged = "　　".join(x.strip() for x in lines)
    opts = [o.strip() for o in OPT_SPLIT.split(merged) if o.strip()]
    # 列数按最长选项的可见长度粗估：数学段按 0.55 倍字符数折算
    # （集合、分式等命令名长但排出来不宽；系数经 p5/p67 折行案例校准）
    longest = max(len(re.sub(r"\$[^$]*\$",
                             lambda m: "x" * max(3, int(len(m.group(0)) * 0.55)), o))
                  for o in opts)
    ncol = 4 if longest <= 10 else (2 if longest <= 26 else 1)
    out = [f"\\begin{{gkopts}}({ncol})"]
    for o in opts:
        out.append(f"\\task {conv_inline(o)}")
    out.append("\\end{gkopts}")
    return out


# ---------- 表格 ----------
def emit_table(lines: list[str]) -> list[str]:
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    if len(rows) < 2:
        return [conv_inline(lines[0])]
    sep = rows[1]
    aligns = []
    for c in sep:
        if c.startswith(":") and c.endswith(":"):
            aligns.append("c")
        elif c.endswith(":"):
            aligns.append("r")
        else:
            aligns.append("l")
    body_rows = [rows[0]] + rows[2:]
    ncol = max(len(r) for r in body_rows)
    aligns += ["c"] * (ncol - len(aligns))
    out = ["\\begin{center}", f"\\begin{{tabular}}{{{''.join(aligns[:ncol])}}}", "\\toprule"]
    for i, r in enumerate(body_rows):
        r = r + [""] * (ncol - len(r))
        out.append(" & ".join(conv_inline(c) for c in r) + r" \\")
        if i == 0:
            out.append("\\midrule")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{center}"]
    return out


# ---------- 引用块 ----------
def emit_quote(lines: list[str]) -> list[str]:
    inner = [re.sub(r"^>\s?", "", ln) for ln in lines]
    text = "\n".join(inner)
    if "原卷影印件" in text or "配套文档" in text:
        return []
    env = "gktip"
    if any(k in text for k in ("卷种提示", "解析归属", "归属声明", "重合题", "适用省份")):
        env = "gknotice"
    body = convert_block(inner)          # 递归处理引用内部（可含表格/显示公式）
    return [f"\\begin{{{env}}}"] + body + [f"\\end{{{env}}}"]


# ---------- 图片 ----------
def emit_image(name: str) -> list[str]:
    slug = FIGMAP.get(name)
    if slug is None:
        warnings.append(f"图片无映射：{name}")
        return [r"\begin{center}\fbox{图形缺失：" + conv_text(name) + r"}\end{center}"]
    return [f"\\begin{{center}}\\input{{figures/{slug}}}\\end{{center}}"]


HEAD_SOL = re.compile(r"^### 第\s*(\d+)\s*题[　\s]*(?:（(.*)）|〔(.*)〕)?\s*$")
HEAD_QNUM = re.compile(r"^\*\*(\d+)．([^*]*?)\*\*\s*(.*)$")
IMG = re.compile(r"^!\[[^\]]*\]\(images/(.+?)\.png\)\s*$")
OPTLINE = re.compile(r"^\s{0,4}[A-D]．")
ANSLINE = re.compile(r"^\*\*([^*]*答案[^*]*)\*\*\s*$")


def convert_block(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        ln = lines[i]

        if not ln.strip():
            out.append("")
            i += 1
            continue

        # --- 引用块 ---
        if ln.lstrip().startswith(">"):
            j = i
            grp = []
            while j < n and (lines[j].lstrip().startswith(">") or
                             (not lines[j].strip() and j + 1 < n and lines[j + 1].lstrip().startswith(">"))):
                if lines[j].strip():
                    grp.append(lines[j].lstrip())
                j += 1
            out += emit_quote(grp)
            i = j
            continue

        # --- 表格 ---
        if ln.strip().startswith("|"):
            j = i
            grp = []
            while j < n and lines[j].strip().startswith("|"):
                grp.append(lines[j])
                j += 1
            out += emit_table(grp)
            i = j
            continue

        # --- 显示公式 ---
        if ln.strip().startswith("$$"):
            body = ln.strip()
            j = i
            while not (body.endswith("$$") and len(body) > 2):
                j += 1
                body += "\n" + lines[j].strip()
            out += ["\\[" + body[2:-2] + "\\]"]
            i = j + 1
            continue

        # --- 标题 ---
        if ln.startswith("#"):
            m = HEAD_SOL.match(ln)
            if m:
                out.append(f"\\gksolhead{{{m.group(1)}}}{{{conv_inline(m.group(2) or m.group(3) or '')}}}")
            elif ln.startswith("####"):
                out.append(f"\\gksubpart{{{conv_inline(ln.lstrip('#').strip())}}}")
            elif ln.startswith("###"):
                out.append(f"\\gksubpart{{{conv_inline(ln.lstrip('#').strip())}}}")
            elif ln.startswith("##"):
                t = ln.lstrip("#").strip()
                # 卷名副标题（如"数学（全国 I 卷 · 理科）"）丢弃
                if t.startswith("数学（"):
                    pass
                else:
                    out.append(f"\\gkpart{{{conv_inline(t)}}}")
            # 一级标题（考试名）丢弃
            i += 1
            continue

        # --- 水平线 ---
        if re.fullmatch(r"-{3,}", ln.strip()):
            out.append("\\par\\medskip")
            i += 1
            continue

        # --- 图片 ---
        m = IMG.match(ln.strip())
        if m:
            out += emit_image(m.group(1))
            i += 1
            continue

        # --- 无序列表（- 开头的连续行）---
        if re.match(r"^\s*-\s+", ln):
            j = i
            grp = []
            while j < n and re.match(r"^\s*-\s+", lines[j]):
                grp.append(re.sub(r"^\s*-\s+", "", lines[j]))
                j += 1
            out.append("\\begin{itemize}")
            for item in grp:
                out.append("\\item " + conv_inline(item))
            out.append("\\end{itemize}")
            i = j
            continue

        # --- 选项组 ---
        if OPTLINE.match(ln):
            j = i
            grp = []
            while j < n:
                if OPTLINE.match(lines[j]):
                    grp.append(lines[j])
                    j += 1
                elif not lines[j].strip() and j + 1 < n and OPTLINE.match(lines[j + 1]):
                    j += 1        # 选项行之间的空行
                else:
                    break
            out += emit_options(grp)
            i = j
            continue

        # --- 题号 ---
        m = HEAD_QNUM.match(ln)
        if m:
            score = f"\\textbf{{{conv_inline(m.group(2))}}} " if m.group(2) else ""
            out.append(f"\\gkti{{{m.group(1)}}}{score}{conv_inline(m.group(3))}")
            i += 1
            continue

        # --- 独立答案段 ---
        m = ANSLINE.match(ln.strip())
        if m:
            out.append(f"\\gkanswer{{{conv_inline(m.group(1))}}}")
            i += 1
            continue

        # --- 普通段落 ---
        out.append(conv_inline(ln))
        i += 1

    return out


def strip_frontmatter(lines: list[str]) -> list[str]:
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                return lines[j + 1:]
    return lines


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    lines = strip_frontmatter(src.read_text(encoding="utf-8").splitlines())
    body = convert_block(lines)
    # 压掉三连以上空行
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)) + "\n"
    dst.write_text(f"% 由 tools/md2tex.py 自 {src.name} 生成，勿手改（改源 MD 后重跑）\n" + text,
                   encoding="utf-8")
    for w in warnings:
        print(f"  [warn] {src.name}: {w}")


if __name__ == "__main__":
    main()

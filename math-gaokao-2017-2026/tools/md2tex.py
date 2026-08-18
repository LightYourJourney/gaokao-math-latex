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

**纯接口**：`convert_markdown(source, ConversionContext(...))` 返回 `ConversionResult`，
警告与被引用的 figure 全部由返回值携带，模块内不再有可跨调用累积的全局状态——多卷
批量生成时，上一卷的警告混进下一卷会让「哪一卷出了问题」彻底不可判定。配图映射也
由 `ConversionContext.figure_map` 显式传入，`FIGMAP` 只是默认值。
`strict=True`（默认）时任何警告都抛 `ConversionError`，供生成器做失败零覆盖。
"""
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Mapping, Sequence, Tuple

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
    "2020-Ⅱ-t9-复工复产折线图": "f2020x2_t9_lines",
    "2020-Ⅱ-t11-正弦图象": "f2020x2_t11_sine",
    "2020-Ⅱ-t16-零件截面": "f2020x2_t16_part",
    "2020-Ⅱ-t20-四棱锥": "f2020x2_t20_pyr",
    "2021-t20-三棱锥": "f2021_t20_tetra",
    "2021甲文-t2-频率分布直方图": "f2021jw_t2_hist",
    "2021甲文-t7-三视图": "f2021jw_t7_views",
    "2021甲文-t15-图象": "f2021jw_t15_cos",
    "2021甲文-t19-三棱柱": "f2021jw_t19_prism",
    "2021甲文-t23-网格": "f2021jw_t23_grid",
    "2021-Ⅱ-t10-正方体": "f2021x2_t10_cubes",
    "2021-Ⅱ-t19-四棱锥": "f2021x2_t19_pyr",
    "2022-t19-棱柱": "f2022_t19_prism",
    "2022-Ⅱ-t3-举架结构": "f2022x2_t3_jiajia",
    "2022-Ⅱ-t3-屋顶截面": "f2022x2_t3_roof",
    "2022-Ⅱ-t11-正方形垂线": "f2022x2_t11_sq",
    "2022-Ⅱ-t19-频率分布直方图": "f2022x2_t19_hist",
    "2022-Ⅱ-t20-三棱锥": "f2022x2_t20_tetra",
    "2023-t18-棱柱": "f2023_t18_prism",
    "2023甲文-t6-程序框图": "f2023jw_t6_flow",
    "2023甲文-t18-三棱柱": "f2023jw_t18_prism",
    "2023-Ⅱ-t16-三角函数图象": "f2023x2_t16_sine",
    "2023-Ⅱ-t19-频率分布直方图": "f2023x2_t19_hist",
    "2023-Ⅱ-t20-三棱锥": "f2023x2_t20_tetra",
    "2024-t11-曲线": "f2024_t11_curve",
    "2024-t17-四棱锥": "f2024_t17_pyramid",
    "2024-Ⅱ-t17-翻折": "f2024x2_t17_fold",
    "2025-t6-风速": "f2025_t6_wind",
    "2025-t17-四棱锥": "f2025_t17_pyramid",
    "2025-2-t17-翻折四边形": "f2025g2_t17_fold",
    "2026-t15-棱柱": "f2026_t15_prism",
    "2026-2-t15-直方图": "f2026g2_t15_hist",
    "2026-2-t16-三棱锥": "f2026g2_t16_tetra",
    "1956-t3-圆": "f1956_t3_circle",
    "1956-t4-棱柱": "f1956_t4_prism",
    "1956-t4-证明": "f1956_t4_proof_prism",
    "1957-t4-四面体": "f1957_t4_tetra",
    "1957-t5-平行平面": "f1957_t5_parallel",
    "1957-t7-内切圆": "f1957_t7_incircle",
    "1957-t8-圆": "f1957_t8_circle",
    "1959-t6-体积": "f1959_t6_volume",
    "1959-t8-三角形": "f1959_t8_triangle",
    "1959-t10-圆": "f1959_t10_circle",
    "1960-t3-航行": "f1960_t3_navigation",
    "1960-t4-抛物线": "f1960_t4_parabola",
    "1960-t5-钢珠": "f1960_t5_ball",
    "1960-t6-四棱锥": "f1960_t6_pyramid",
}

EMOJI = "⚠️⚠✓✗📘⏳✅❌🔺"


@dataclass(frozen=True)
class ConversionContext:
    """一次转换的只读环境：配图映射 + 是否严格。"""

    figure_map: Mapping[str, str]
    strict: bool = True


@dataclass(frozen=True)
class ConversionResult:
    """一次转换的全部产出。

    `referenced_figures` 按出现顺序**逐次**记录成功映射到的 figure 名，重复引用会
    出现多次——调用方据此核对复用计数，所以这里绝不能去重。
    """

    text: str
    warnings: Tuple[str, ...]
    referenced_figures: Tuple[str, ...]


class ConversionError(ValueError):
    """strict 模式下出现了警告。"""

    def __init__(self, warnings: Sequence[str]) -> None:
        self.warnings = tuple(warnings)
        super().__init__("转换出现 %d 条警告：%s" % (len(self.warnings), "；".join(self.warnings)))


class _Sink:
    """一次转换的可变累积器，替代原来的模块级 warnings 全局。"""

    __slots__ = ("figure_map", "warnings", "figures")

    def __init__(self, figure_map: Mapping[str, str]) -> None:
        self.figure_map = figure_map
        self.warnings: List[str] = []
        self.figures: List[str] = []


# ---------- 行内处理 ----------
# 文本段中裸写的数学 Unicode 符号（源 MD 少量存在）→ 等价数学命令
BARE_SYM = {
    "⟹": r"~$\Longrightarrow$~", "⟺": r"~$\Longleftrightarrow$~",
    "∩": r"$\cap$", "∪": r"$\cup$",
    "⊥": r"$\perp$", "≠": r"$\neq$", "∥": r"$\parallel$",
    "◇": r"$\Diamond$", "▭": r"$\square$", "−": r"$-$",
    "∈": r"$\in$", "⊂": r"$\subset$",
}

CJK_IN_MATH = re.compile(r"([\u4e00-\u9fff、，；：「」]+)")


def conv_math_display(s: str) -> str:
    """行间公式体的清洗（$$ 块不经 conv_inline，需单独处理）：
    剥 emoji、裸中文包 \\text（西文数学字体缺 CJK 字形）。
    不剥内嵌 $ —— \\tag{$\\ast$} 等文本模式内的数学是合法嵌套（曾误剥致回归）。"""
    for ch in EMOJI:
        s = s.replace(ch, "")
    return CJK_IN_MATH.sub(r"\\text{\1}", s)


def conv_inline(s: str, sink: _Sink) -> str:
    # 顺序要点：加粗/链接先做（它们可以跨数学段，如 **……$x$……**），
    # 再按 $ 切分，只对文本段做转义与符号替换
    for ch in EMOJI:
        s = s.replace(ch, "")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)         # 链接 -> 纯文本
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)       # 加粗（非贪婪，可含 $…$）
    s = re.sub(r"`([^`]+)`", r"\\texttt{\1}", s)           # 行内代码

    parts = s.split("$")
    if len(parts) % 2 == 0:  # $ 不配对——原样返回并记警告
        sink.warnings.append(f"未配对的 $：{s[:60]}")
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
    s = s.replace("（　　）", r"\mbox{（　　）}")           # 选择题作答空括号不可拆行
    s = s.replace("%", r"\%").replace("&", r"\&").replace("#", r"\#")
    for k, v in BARE_SYM.items():
        s = s.replace(k, v)
    return s


# ---------- 选项组 ----------
OPT_SPLIT = re.compile(r"(?:　+|\s{2,})(?=[A-D]．)")

def emit_options(lines: List[str], sink: _Sink) -> List[str]:
    merged = "　　".join(x.strip() for x in lines)
    opts = [o.strip() for o in OPT_SPLIT.split(merged) if o.strip()]
    # 列数按最长选项的可见长度粗估：数学段按 0.55 倍字符数折算
    # （集合、分式等命令名长但排出来不宽；系数经 p5/p67 折行案例校准）
    longest = max(len(re.sub(r"\$[^$]*\$",
                             lambda m: "x" * max(3, int(len(m.group(0)) * 0.55)), o))
                  for o in opts)
    # 纯文本（无数学）选项每个 CJK 字都占满字宽，4 栏只容得下「标签 + 6 个 CJK」
    # （约 7.5em）。「甲与丙相互独立」这类 7 字选项在 4 栏里会把末字「立」折到
    # 下一行悬挂；含数学的选项维持 10（分数等渲染窄，0.55 折算已偏保守）。
    four_col_limit = 8 if all("$" not in o for o in opts) else 10
    ncol = 4 if longest <= four_col_limit else (2 if longest <= 26 else 1)
    out = [f"\\begin{{gkopts}}({ncol})"]
    for o in opts:
        out.append(f"\\task {conv_inline(o, sink)}")
    out.append("\\end{gkopts}")
    return out


# ---------- 表格 ----------
def emit_table(lines: List[str], sink: _Sink) -> List[str]:
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    if len(rows) < 2:
        return [conv_inline(lines[0], sink)]
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
    out = ["\\begin{center}"]
    if ncol >= 8:      # 宽表（如 9 列频率分布表）收紧列距，防 Overfull
        out.append("\\begingroup\\setlength{\\tabcolsep}{4pt}")
    out += [f"\\begin{{tabular}}{{{''.join(aligns[:ncol])}}}", "\\toprule"]
    for i, r in enumerate(body_rows):
        r = r + [""] * (ncol - len(r))
        out.append(" & ".join(conv_inline(c, sink) for c in r) + r" \\")
        if i == 0:
            out.append("\\midrule")
    out += ["\\bottomrule", "\\end{tabular}"]
    if ncol >= 8:
        out.append("\\endgroup")
    out.append("\\end{center}")
    return out


# ---------- 引用块 ----------
def emit_quote(lines: List[str], sink: _Sink) -> List[str]:
    inner = [re.sub(r"^>\s?", "", ln) for ln in lines]
    text = "\n".join(inner)
    if "原卷影印件" in text or "配套文档" in text:
        return []
    env = "gktip"
    if any(k in text for k in ("卷种提示", "解析归属", "归属声明", "重合题", "适用省份")):
        env = "gknotice"
    body = convert_block(inner, sink)    # 递归处理引用内部（可含表格/显示公式）
    return [f"\\begin{{{env}}}"] + body + [f"\\end{{{env}}}"]


# ---------- 图片 ----------
def emit_image(name: str, sink: _Sink) -> List[str]:
    slug = sink.figure_map.get(name)
    if slug is None:
        sink.warnings.append(f"图片无映射：{name}")
        return [r"\begin{center}\fbox{图形缺失：" + conv_text(name) + r"}\end{center}"]
    sink.figures.append(slug)
    return [
        r"\nopagebreak[4]",
        f"\\begin{{center}}\\input{{figures/{slug}}}\\end{{center}}",
        r"\nopagebreak[4]",
    ]


HEAD_SOL = re.compile(r"^### 第\s*(\d+)\s*题[　\s]*(?:（(.*)）|〔(.*)〕)?\s*$")
HEAD_QNUM = re.compile(r"^\*\*(\d+)．([^*]*?)\*\*\s*(.*)$")
IMG = re.compile(r"^!\[[^\]]*\]\(images/(.+?)\.png\)\s*$")
OPTLINE = re.compile(r"^\s{0,4}[A-D]．")
ANSLINE = re.compile(r"^\*\*([^*]*答案[^*]*)\*\*\s*$")


def convert_block(lines: List[str], sink: _Sink) -> List[str]:
    out: List[str] = []
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
            out += emit_quote(grp, sink)
            i = j
            continue

        # --- 表格 ---
        if ln.strip().startswith("|"):
            j = i
            grp = []
            while j < n and lines[j].strip().startswith("|"):
                grp.append(lines[j])
                j += 1
            out += emit_table(grp, sink)
            i = j
            continue

        # --- 显示公式 ---
        if ln.strip().startswith("$$"):
            s = ln.strip()
            m = re.match(r"^\$\$(.+?)\$\$(.*)$", s)
            if m:                       # 单行 $$...$$，允许带尾随文字（如括号段收尾）
                out += [r"\nopagebreak[4]", "\\[" + conv_math_display(m.group(1)) + "\\]"]
                if m.group(2).strip():
                    out += [conv_inline(m.group(2).strip(), sink)]
                i += 1
                continue
            body = s
            j = i
            while j + 1 < n and not (body.endswith("$$") and len(body) > 2):
                j += 1
                body += "\n" + lines[j].strip()
            if body.endswith("$$") and len(body) > 2:
                out += [r"\nopagebreak[4]", "\\[" + conv_math_display(body[2:-2]) + "\\]"]
            else:                       # 越界护栏：未闭合不崩溃，按行内文本退化并告警
                sink.warnings.append(f"未闭合的 $$ 块：{s[:50]}")
                out += [conv_inline(s, sink)]
                j = i
            i = j + 1
            continue

        # --- 标题 ---
        if ln.startswith("#"):
            m = HEAD_SOL.match(ln)
            if m:
                out.append(
                    f"\\gksolhead{{{m.group(1)}}}"
                    f"{{{conv_inline(m.group(2) or m.group(3) or '', sink)}}}"
                )
            elif ln.startswith("####"):
                out.append(f"\\gksubpart{{{conv_inline(ln.lstrip('#').strip(), sink)}}}")
            elif ln.startswith("###"):
                out.append(f"\\gksubpart{{{conv_inline(ln.lstrip('#').strip(), sink)}}}")
            elif ln.startswith("##"):
                t = ln.lstrip("#").strip()
                # 卷名副标题（如"数学（全国 I 卷 · 理科）"）丢弃
                if t.startswith("数学（"):
                    pass
                else:
                    out.append(f"\\gkpart{{{conv_inline(t, sink)}}}")
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
            while out and out[-1] == "":
                out.pop()
            out += emit_image(m.group(1), sink)
            i += 1
            while i < n and not lines[i].strip():
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
                out.append("\\item " + conv_inline(item, sink))
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
            out += emit_options(grp, sink)
            i = j
            continue

        # --- 题号 ---
        m = HEAD_QNUM.match(ln)
        if m:
            # 含图选择题在页尾预留四成页高：Needspace 只决定起始页，不把整题硬盒，
            # 超长题仍可自然跨页。扫描止于下一题号或节标题，避免影响无图题。
            j = i + 1
            while j < n and not HEAD_QNUM.match(lines[j]) and not lines[j].startswith("#"):
                if IMG.match(lines[j].strip()):
                    out.append(r"\Needspace{0.4\textheight}")
                    break
                j += 1
            score = f"\\textbf{{{conv_inline(m.group(2), sink)}}} " if m.group(2) else ""
            out.append(f"\\gkti{{{m.group(1)}}}{score}{conv_inline(m.group(3), sink)}")
            i += 1
            continue

        # --- 独立“解析”标题：与后续首段保持同页 ---
        if ln.strip() == "**解析**":
            out.append(r"\Needspace{4\baselineskip}")
            out.append(conv_inline(ln, sink))
            i += 1
            continue

        # --- 独立答案段 ---
        m = ANSLINE.match(ln.strip())
        if m:
            out.append(f"\\gkanswer{{{conv_inline(m.group(1), sink)}}}")
            i += 1
            continue

        # --- 普通段落 ---
        # 统计题的“附：公式”应与紧随的临界值表一起起排，避免公式与表格分居两页。
        if ln.strip().startswith("附："):
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and lines[j].strip().startswith("|"):
                out.append(r"\Needspace{10\baselineskip}")
        out.append(conv_inline(ln, sink))
        i += 1

    return out


def strip_frontmatter(lines: List[str]) -> List[str]:
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                return lines[j + 1:]
    return lines


def _finish(text: str, sink: _Sink, context: ConversionContext) -> ConversionResult:
    warnings = tuple(sink.warnings)
    if context.strict and warnings:
        raise ConversionError(warnings)
    return ConversionResult(
        text=text, warnings=warnings, referenced_figures=tuple(sink.figures)
    )


def convert_markdown(source: str, context: ConversionContext) -> ConversionResult:
    """把一份 Markdown 全文转成 LaTeX 正文片段（不含生成头注）。"""
    sink = _Sink(context.figure_map)
    body = convert_block(strip_frontmatter(source.splitlines()), sink)
    # 压掉三连以上空行
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(body)) + "\n"
    return _finish(text, sink, context)


def convert_inline(text: str, context: ConversionContext) -> ConversionResult:
    """只做行内转换（加粗/链接/数学段/转义），供简答版等按题取值的调用方使用。"""
    sink = _Sink(context.figure_map)
    return _finish(conv_inline(text, sink), sink, context)


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    # 命令行沿用宽松模式：它是排错入口，要把警告全部打出来而不是第一条就中断。
    result = convert_markdown(
        src.read_text(encoding="utf-8"),
        ConversionContext(figure_map=FIGMAP, strict=False),
    )
    dst.write_text(
        f"% 由 tools/md2tex.py 自 {src.name} 生成，勿手改（改源 MD 后重跑）\n" + result.text,
        encoding="utf-8",
    )
    for w in result.warnings:
        print(f"  [warn] {src.name}: {w}")


if __name__ == "__main__":
    main()

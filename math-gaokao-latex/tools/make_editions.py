#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_editions.py —— 为 14 套试卷生成四个版本的可编译壳文件。

  试题版.tex   只含题目（questions.tex），供测试练习；
  解析版.tex   题目 + 参考答案与详细解析（answers.tex）；
  简答版.tex   题目 + 简短答案速查（answers_short.tex），供快速核对；
  印刷版.tex   题目 + 解析的紧凑排版（五号字、窄边距、紧列表），适合打印。

壳文件只负责装配与版式，题目/解析内容一律 \\input 共享片段、不复制内容。
版式打磨（如印刷版是否双栏）可直接改壳文件——重跑本脚本会覆盖，
故长期定制应改本脚本的模板。依赖：先运行 split_project.py。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DST = HERE.parent

SHELL = """% !TeX program = xelatex
% ============================================================
% {title} · {edition}
% 由 tools/make_editions.py 生成（重跑会覆盖本文件）；
% 题目/解析内容在 questions.tex / answers*.tex，勿在本文件内写内容。
% ============================================================
\\documentclass[zihao={zihao}, a4paper]{{ctexart}}
\\input{{../common/preamble}}
\\input{{../common/macros}}
\\input{{../common/questions_env}}
{extra}\\renewcommand{{\\gkpaperid}}{{{pid}}}
\\renewcommand{{\\gkheadL}}{{{title} · 数学}}
\\renewcommand{{\\gkheadR}}{{{edition}}}
\\hypersetup{{pdftitle={{{title} 数学 · {edition}}}}}
\\begin{{document}}
\\begin{{center}}
  {{\\Large\\bfseries {title}}}\\\\[4pt]
  {{\\large 数学 · {edition}}}
\\end{{center}}
\\medskip
{body}\\end{{document}}
"""

# 印刷版的紧凑版式（在 \input 公共导言之后覆盖其设置）。
# 参数经打样卷逐项扫描定型（V0→V3，27→24 页）；更窄边距与双栏均已实测否决：
# 前者零增益且进打印机不可打区，后者行间公式/TikZ 图按全宽绘制会溢栏叠印。
COMPACT = """% 紧凑版式（印刷版）：五号字由文档类选项给定；除收窄边距与压缩列表/选项间距外，
% 再压缩行距、行间公式留白与解析小标题间距。四项合计约省 11% 页数（打样卷 27 -> 24 页）。
\\geometry{a4paper, margin=1.6cm, headheight=14pt}
\\setlist{itemsep=1pt, topsep=2pt, parsep=0pt}
\\settasks{label={}, label-width=0pt, item-indent=1.2em,
          column-sep=0.8em, after-item-skip=1pt, before-skip=1pt, after-skip=2pt}
% 行距：ctex 默认 linespread 1.3 -> 1.2（基线 16.44pt -> 15.18pt），
% 仍为字号的 1.44 倍，CJK 正文可读性不受影响。
\\linespread{1.2}
% 行间公式留白：每卷解析含 150~250 个行间公式，此项是本版面最大的杠杆。
% 用 \\AtBeginDocument 是因为 ctex/amsmath 会在 \\begin{document} 时重置这四个长度。
\\AtBeginDocument{%
  \\setlength{\\abovedisplayskip}{3pt plus 2pt minus 1pt}%
  \\setlength{\\belowdisplayskip}{3pt plus 2pt minus 1pt}%
  \\setlength{\\abovedisplayshortskip}{1pt plus 1pt}%
  \\setlength{\\belowdisplayshortskip}{2pt plus 1pt minus 1pt}}
% 标题间距：\\gkpart 用 \\subsection*，\\gksolhead 用 \\subsubsection*（每卷约 22 个）。
\\ctexset{subsection/beforeskip={6pt plus 2pt minus 1pt}, subsection/afterskip={3pt plus 1pt},
         subsubsection/beforeskip={5pt plus 2pt minus 1pt}, subsubsection/afterskip={2pt plus 1pt}}
"""

BODY_Q = "\\pdfbookmark[1]{试题}{sec:q}\n\\input{questions}\n"
BODY_QS = ("\\pdfbookmark[1]{试题}{sec:q}\n\\input{questions}\n"
           "\\clearpage\n"
           "\\pdfbookmark[1]{参考答案与详细解析}{sec:s}\n"
           "\\begin{center}{\\Large\\bfseries 参考答案与详细解析}\\end{center}\n"
           "\\medskip\n\\input{answers}\n")
BODY_QA = ("\\pdfbookmark[1]{试题}{sec:q}\n\\input{questions}\n"
           "\\clearpage\n"
           "\\pdfbookmark[1]{答案速查}{sec:a}\n"
           "\\begin{center}{\\Large\\bfseries 答案速查}\\end{center}\n"
           "\\medskip\n\\input{answers_short}\n")
# 印刷版省纸：解析紧随试题（分隔线不分页）
BODY_PRINT = ("\\pdfbookmark[1]{试题}{sec:q}\n\\input{questions}\n"
              "\\par\\bigskip\\hrule\\bigskip\n"
              "\\pdfbookmark[1]{参考答案与详细解析}{sec:s}\n"
              "\\begin{center}{\\large\\bfseries 参考答案与详细解析}\\end{center}\n"
              "\\smallskip\n\\input{answers}\n")

EDITIONS = [
    ("试题版", "-4", "", BODY_Q),
    ("解析版", "-4", "", BODY_QS),
    ("简答版", "-4", "", BODY_QA),
    ("印刷版", "5", COMPACT, BODY_PRINT),
]


def main():
    index = json.loads((DST / "index.json").read_text(encoding="utf-8"))
    n = 0
    for p in index["papers"]:
        pdir = DST / p["dir"]
        for name, zihao, extra, body in EDITIONS:
            tex = SHELL.format(title=p["title"], edition=name, zihao=zihao,
                               extra=extra, pid=p["id"], body=body)
            (pdir / f"{name}.tex").write_text(tex, encoding="utf-8")
            n += 1
        print(f"✓ {p['dir']}: 4 个版本壳")
    print(f"\n共生成 {n} 个壳文件。")


if __name__ == "__main__":
    main()

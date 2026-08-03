# 高考数学真题集 2017–2026（全国Ⅰ卷系）· XeLaTeX 项目

十年 14 套试卷（2017–2020 全国Ⅰ卷文理分科、2021–2024 新高考Ⅰ卷、2025–2026 全国 1 卷），
每套含**完整试题 + 参考答案与逐题详细解析**，全部图形为 TikZ/pgfplots 矢量绘制。

## 编译

```bash
./compile.sh          # xelatex 两遍，生成 main.pdf（约 420 页）
./compile.sh quick    # 只编译一遍（排错迭代用）
```

依赖：TeX Live（含 ctex、tikz、pgfplots、tcolorbox、tasks 等，完整安装即可）。
macOS 下默认 `fontset=mac`（Songti SC）；Linux/Windows 请把 `main.tex` 首行改为
`fontset=fandol` 或 `fontset=windows`。

## 目录结构

```
main.tex          主文档：扉页、前言、按年份装配 14 套试卷（\gkpaper 一行一套）
preamble.tex      导言区:宏包、页眉页脚、题号/解析头/提示框/选项排版等自定义命令
papers/           试题正文（不含答案），每套一个 .tex
answers/          参考答案与详细解析，每套一个 *_sol.tex
figures/          31 个 TikZ/pgfplots 矢量图，一图一文件，试题与解析共用（\input 复用）
tools/md2tex.py   由本仓库  的 Markdown 源批量生成 papers/、answers/
compile.sh        一键编译脚本
missing_list.md   未收录卷种与保留意见清单（必读）
```

## 内容来源与可靠性

- 试题原文：本仓库 年份目录（源自 [deekur/gaokaomath](https://github.com/deekur/gaokaomath)，CC BY 4.0），
  经人工转写与校对；**未收录无转写材料的其他卷种**（全国Ⅱ/Ⅲ卷、甲/乙卷），
  详见 `missing_list.md`。新高考Ⅱ卷系 7 套已批次补录为**素材**（papers/answers 内
  `*_xgk2*`、`*_g2*`，不进本书 main.pdf），四版本见 `../math-gaokao-latex/`。
- 解析：编者独立推导，**非官方标准答案**。
- 2026 年卷为**回忆版**。

## 修改与再生成

`papers/`、`answers/` 是生成物（文件头有标注），**不要手改**——改
年份目录 下对应 Markdown 源后重跑：

```bash
python3 tools/md2tex.py ../<年份>/<源文件>.md papers/<基名>.tex
```

图形在 `figures/` 下手工维护，每个文件是一个居中的 `tikzpicture`，
文件头注释注明对应的年份/题号与绘制依据。

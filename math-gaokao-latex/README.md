# 高考数学真题 · 拆分版 LaTeX 项目（2017–2026 全国Ⅰ卷系）

把合并书 [`math-gaokao-2017-2026/`](../math-gaokao-2017-2026/) 拆成 **14 个独立试卷项目**，
每套试卷一个目录、四个可独立编译的版本。全部图形 TikZ/pgfplots 矢量绘制，XeLaTeX 编译。

## 四个版本

| 版本 | 内容 | 用途 |
|---|---|---|
| 试题版 | 只有题目 | 限时测试、练习 |
| 解析版 | 题目 + 参考答案与逐题详细解析 | 学习、备课 |
| 简答版 | 题目 + 末页答案速查（选择题表格 + 填空/解答结论） | 做完快速核对 |
| 印刷版 | 题目 + 解析的紧凑排版（五号字、窄边距） | 省纸打印 |

## 编译

```bash
./compile.sh                              # 全部 14 套 × 4 版本
./compile.sh 2017_全国Ⅰ卷_理科            # 单套 4 版本
./compile.sh 2017_全国Ⅰ卷_理科 解析版     # 单个目标
```

依赖：TeX Live 完整安装（ctex、tikz、pgfplots、tcolorbox、tasks 等）。
macOS 外的系统需把各版本壳文件的 `\documentclass` 行 fontset 适配（同合并书 README 的说明）。

## 目录结构

```
common/               共享导言三件套（所有版本壳 \input 之）
  preamble.tex          宏包与版面（页眉用 \gkheadL/\gkheadR 宏，壳内设置）
  macros.tex            题号 \gkti、解析头 \gksolhead、提示框等自定义命令
  questions_env.tex     question / answer 语义环境（不产生视觉效果的结构边界）
<年份>_<卷别>/         每套试卷一个独立项目，如 2017_全国Ⅰ卷_理科/
  questions.tex         题目内容片段（无答案；每题包 question 环境）
  answers.tex           解析内容片段（每题包 answer 环境）
  answers_short.tex     简短答案速查（选择题字母经三源交叉核对）
  figures/              该卷用到的 TikZ 图（自合并书复制副本，项目自含）
  试题版.tex 解析版.tex 简答版.tex 印刷版.tex   四个可编译壳
index.json            14 套试卷元数据（卷别、题量、题型分段、合并书页码范围、图形清单）
tools/                生成脚本（见下）
compile.sh            一键编译
```

## 数据流与修改方式（源单一原则）

```
*.md（源）──md2tex──▶ 合并书 papers/ answers/ ──split_project.py──▶ 各卷 questions.tex answers.tex
*_答案要点.md ────────────────────────────────make_short_answers.py──▶ 各卷 answers_short.tex
                                                          make_editions.py ──▶ 四版本壳 ×14
```

- **内容有误**：改 年份目录 的源 MD → 重跑合并书 `tools/md2tex.py` → 重跑本项目 `tools/split_project.py`。不要手改 questions.tex / answers*.tex（文件头有生成标注）。
- **版式定制**：改 `tools/make_editions.py` 的模板后重跑（直接改壳文件会在重跑时被覆盖）。
- 三个生成脚本均自带校验（题号连续性、往返逐字节一致、答案三源交叉核对），失败即退出非零。

## 内容来源与可靠性

- 试题与解析承自合并书项目，源头为本仓库 年份目录（[deekur/gaokaomath](https://github.com/deekur/gaokaomath)，CC BY 4.0，经人工转写校对）。
- **解析非官方标准答案**（编者独立推导）；2026 卷为**回忆版**。
- **未收录卷种**（全国Ⅱ/Ⅲ卷、甲/乙卷、新高考Ⅱ卷等，因无原始材料不凭记忆默写）：
  清单与补充方法见合并书 [`missing_list.md`](../math-gaokao-2017-2026/missing_list.md)。
- 简答版中证明题的问标注"见解析版"——证明题不存在可压缩的"简短结论"，不硬造。

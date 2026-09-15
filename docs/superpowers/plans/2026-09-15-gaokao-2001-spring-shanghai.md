# 2001 年春季上海卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`（推荐）或 `superpowers:executing-plans` 执行本计划。各步骤用复选框（[ ]/[x]）跟踪。

**Goal:** 将固定源 PDF 对应的 2001 年春季上海卷数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、两份矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据固定源 `src-bbef625a2ac718c402e674edcbad44be98f097701ef4a7660ea7c79995bd7b46`，对应 `春季高考/2001/2001春季上海.pdf`；文件为 2 页 A3 题面，原卷印刷页码 83–84，不附答案。题面、答案、独立解析分别落在 `2001/`，由现有工具生成单卷 LaTeX 工程；第 19、20 题图形仅以 TikZ/PGFPlots `.tex` 永久保存。

## Global Constraints

- 固定源 PDF SHA-256 为 `6cf864aafa404b5486d781a58f15df531b6d5cf93616ca8a88ba86cf6e2ddf44`，大小 `600426` bytes；PDF 原件不复制进仓库。
- 固定源为 2 页 A3 题面，印刷页码 83–84；PDF 不附答案，答案和解析均为本库独立复算。
- 题面含 22 题：填空题 1–12、选择题 13–16、解答题 17–22；保留全部小问。
- 第 19 题钢板焊接正四棱锥容器、第 20 题长方体空间几何图形全部重绘为矢量源；不得提交截图。
- 构建目录最终只保留四个 PDF；不得留下 LaTeX 中间物、媒体文件或 `.work`。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: `2001/2001_数学真题_春季上海_试题.md`
- Create: `2001/2001_数学真题_春季上海_答案要点.md`
- Create: `2001/2001_数学真题_春季上海_解析正文.md`
- Create by tool: `2001/2001_数学真题_春季上海_含解析.md`
- Create: `math-gaokao-latex/2001_春季上海卷/figures/{f2001_spring_t19_pyramid.tex,f2001_spring_t20_cuboid.tex}`

## Tasks

- [x] Verify source facts with `pdfinfo`, SHA-256 and visual renders; record pages 1–2 / printed pages 83–84.
- [x] Transcribe Q1–Q22, including the Q19/Q20 diagrams and all subparts.
- [x] Independently solve all answers, especially Q3 period, Q4 binomial coefficient, Q7 exponential limit, Q10 arithmetic operation, Q11 trigonometric propositions, Q12 compound interest, Q17 set intersection, Q18 trigonometric parameter, Q19 container optimization, Q20 spatial angle, Q21 ellipse intersection count, and Q22 sequence inequality.
- [x] Generate `_含解析.md`, register b85, generate/check LaTeX, provenance and receipts.
- [x] Compile, visually review all pages, finalize review, run full gates and tests, clean all intermediates, and close this plan.

## Self-Review Checklist

- [x] Fixed source fingerprint and two-page A3 range are present.
- [x] Q19/Q20 are the only logical image markers and all map to committed `.tex` figures.
- [x] All 22 answers and subparts are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with preexisting unrelated source drifts reported.

# 2002 年春季上海卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development 或 superpowers:executing-plans 执行本计划。各步骤用复选框（[ ]/[x]）跟踪。

**Goal:** 将固定源 PDF 对应的 2002 年春季上海卷数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、四份矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据固定源 src-0f9719188917480467d0447b53eb4cb22d4df00c8610ea225146528cef63ab9b，对应 春季高考/2002/2002春季上海.pdf；文件为 2 页 A3 题面，原卷印刷页码 99–100，不附答案。第 10、11、12、19 题图形仅以 TikZ/PGFPlots .tex 永久保存。

## Global Constraints

- 固定源 PDF SHA-256 为 92e426f381bc0f25c16ff4a1eab7fb5ac698356f7938db6d31f9c428ca7a9774，大小 512721 bytes；原 PDF 不复制进仓库。
- 固定源为 2 页 A3 题面，印刷页码 99–100；PDF 不附答案，答案和解析均为本库独立复算。
- 题面含 22 题：填空题 1–12、选择题 13–16、解答题 17–22；保留全部小问。
- 第 10、11、12、19 题的原卷图形全部重绘为矢量源；不得提交截图。
- 构建目录最终只保留四个 PDF；不得留下 LaTeX 中间物、媒体文件或 .work。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 2002/2002_数学真题_春季上海_{试题,答案要点,解析正文,含解析}.md
- Create by tool: math-gaokao-latex/2002_春季上海卷/*
- Create: math-gaokao-latex/2002_春季上海卷/figures/{f2002_spring_t10_cube_net.tex,f2002_spring_t11_pursuit.tex,f2002_spring_t12_rays.tex,f2002_spring_t19_prism.tex}

## Tasks

- [x] Verify source facts with pdfinfo, SHA-256 and visual renders; record pages 1–2 / printed pages 99–100.
- [x] Transcribe Q1–Q22, including the Q10/Q11/Q12/Q19 diagrams and all subparts.
- [x] Independently solve all answers, especially Q1 domain, Q2 ellipse, Q3 set inequalities, Q5 fifth-root binomial term, Q6 symmetry simplification, Q7 height-order probability, Q9 trigonometric maximum, Q10 cube-net count, Q11 pursuit geometry, Q12 spatial volume ratio, Q13 vector identity, Q14 triangle shape, Q15 inverse logarithm graph, Q16 arithmetic sequence sums, and Q17–Q22.
- [x] Generate _含解析.md, register b87, generate/check LaTeX, provenance and receipts.
- [x] Compile, visually review all pages, finalize review, run full gates and tests, clean all intermediates, and close this plan.

## Self-Review Checklist

- [x] Fixed source fingerprint and two-page A3 range are present.
- [x] Q10/Q11/Q12/Q19 are the only logical image markers and all map to committed .tex figures.
- [x] All 22 answers and subparts are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with the preexisting five unrelated solution-source drifts reported.

# 2002 年普通高考上海卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development 或 superpowers:executing-plans 执行本计划。各步骤用复选框（[ ]/[x]）跟踪。

**Goal:** 将固定源 PDF 对应的 2002 年普通高考上海文、理两卷整理为可追溯 Markdown 源、四种可编译 LaTeX 版本、矢量图源和通过全页复核的 PDF。

**Architecture:** 文科固定源为 src-01548e77c3088a60e4f2c74979d0a81e6c70f4378c9b5c52e7933af3d1ae6542，对应 普通高考/2002/2002上海文.pdf，2 页 A3、印刷页码 110–111；理科固定源为 src-26712f5118c401de589db671244bf873c393342a19307f8892e8afb4c6ee8a54，对应 普通高考/2002/2002上海理.pdf，2 页 A3、印刷页码 108–109。两份固定源均不附答案；答案与解析独立复算。两卷第 13、15、16、17 题图形仅以 TikZ/PGFPlots .tex 永久保存。

## Global Constraints

- 文科源 SHA-256 0759a7d7c029cd016b09ffa69c18ce06b7a177cc9216c96b3979626a25151ee，大小 506880 bytes。
- 理科源 SHA-256 1bb58718fa4932263165d947c11e9df2a68f0cc3eb4a49493e1d1a2e323a22b1，大小 506907 bytes。
- 两卷均为 2 页 A3；题面结构需以固定源逐题核对，保留全部小问与选项。
- 所有图形重绘为矢量源；不得提交原卷截图。
- 两个项目的 build/ 最终只保留四个 PDF；不得留下 LaTeX 中间物、媒体文件或 .work。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 2002/2002_数学真题_上海文_{试题,答案要点,解析正文,含解析}.md
- Create: 2002/2002_数学真题_上海理_{试题,答案要点,解析正文,含解析}.md
- Create by tool: math-gaokao-latex/2002_上海卷_文科/*
- Create by tool: math-gaokao-latex/2002_上海卷_理科/*
- Create figures per project: f2002_shanghai_t13_complex.tex, f2002_shanghai_t15_graph.tex, f2002_shanghai_t16_temperature.tex, f2002_shanghai_t17_prism.tex.

## Tasks

- [x] Verify both source fingerprints, A3 pages and printed page ranges with pdfinfo, SHA-256 and visual renders.
- [x] Transcribe both papers, including the Q13/Q15/Q16/Q17 graph and geometry figures and all subparts.
- [x] Independently solve both papers, including complex geometry, calculus, probability, sequences, finance, spatial geometry and generalized combinations.
- [x] Generate both _含解析.md, register b89, generate/check LaTeX, provenance and receipts.
- [x] Compile all eight editions, visually review every page, finalize review, run full gates and tests, clean intermediates, and close this plan.

## Self-Review Checklist

- [x] Both fixed-source fingerprints and printed page ranges are present.
- [x] Every image marker maps to a committed TikZ/PGFPlots figure and no raster image enters the branch.
- [x] All questions and subparts are independently checked.
- [x] Eight PDFs compile, are visually reviewed, and no compiler intermediates remain.
- [x] Full tests and global receipt/report gates pass, with unrelated historical solution-source drifts reported honestly.

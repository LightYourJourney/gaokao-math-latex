# 2002 年全国新课程卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development 或 superpowers:executing-plans 执行本计划。各步骤用复选框（[ ]/[x]）跟踪。

**Goal:** 将固定源 PDF 对应的 2002 年全国新课程文、理两卷整理为可追溯 Markdown 源、四种可编译 LaTeX 版本、矢量图源和通过全页复核的 PDF。

**Architecture:** 文科固定源为 src-2cfc2db9c0f09cde88a57c79780a0b5946a263027611e86cc07ee0763b66d4c8，对应 普通高考/2002/2002全国新课程文(天津,山西,江西).pdf，2 页 A3、印刷页码 116–117；理科固定源为 src-9ede07b5a550992692db2b8bea1205667aa55bf8a58d494ea0f807259b686e78，对应 普通高考/2002/2002全国新课程理(天津,山西,江西).pdf，2 页 A3、印刷页码 114–115。两份固定源均不附答案；答案与解析独立复算。文科第 13、15、19 题以及理科第 18 题含原卷图形；甲/乙选做分支均保留并分别解析。

## Global Constraints

- 文科源 SHA-256 612a6e01e8fec4935147138ce0896df70c81bf4f8e271250a5894126f888a0ec，大小 506697 bytes。
- 理科源 SHA-256 54336c5da47c9b0053ff3521e7514798533465f9f3b3654a8930953889119ef0，大小 500259 bytes。
- 两卷均为 2 页 A3；题面 22 题，保留全部选项、甲/乙分支和小问。
- 所有图形重绘为 TikZ/PGFPlots 矢量源；不得提交原卷截图或图片文件。
- 两个项目的 build/ 最终只保留四个 PDF；不得留下 LaTeX 中间物、媒体文件或 .work。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 2002/2002_数学真题_全国新课程文_{试题,答案要点,解析正文,含解析}.md
- Create: 2002/2002_数学真题_全国新课程理_{试题,答案要点,解析正文,含解析}.md
- Create by tool: math-gaokao-latex/2002_全国新课程卷_文科/*
- Create by tool: math-gaokao-latex/2002_全国新课程卷_理科/*
- Create per fixed-source marker: committed TikZ/PGFPlots figures for the housing chart, folded-square geometry, optional prism/square geometry and any science optional diagram.

## Tasks

- [x] Verify both source fingerprints, A3 pages and printed page ranges with pdfinfo, SHA-256 and visual renders.
- [x] Transcribe both papers, including all graph/geometry figures, optional branches and subparts.
- [x] Independently solve both papers, including the optional 甲/乙 geometry branches, recurrence, calculus, probability and generalized-combination questions.
- [x] Generate both _含解析.md, register b90, generate/check LaTeX, provenance and receipts.
- [x] Compile all eight editions, visually review every page, finalize review, run full gates and tests, clean intermediates, and close this plan.

## Self-Review Checklist

- [x] Both fixed-source fingerprints and printed page ranges are present.
- [x] Every image marker maps to a vector figure source; no raster image enters the branch.
- [x] All questions, optional branches and subparts are independently checked.
- [x] Eight PDFs compile, are visually reviewed, and no compiler intermediates remain.
- [x] Full tests and global receipt/report gates pass, with unrelated historical solution-source drifts reported honestly.

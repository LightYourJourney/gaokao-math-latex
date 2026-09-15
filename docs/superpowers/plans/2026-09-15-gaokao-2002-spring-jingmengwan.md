# 2002 年春季京蒙皖卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development 或 superpowers:executing-plans 执行本计划。各步骤用复选框（[ ]/[x]）跟踪。

**Goal:** 将固定源 PDF 对应的 2002 年春季京蒙皖文、理两卷整理为可追溯 Markdown 源、四种可编译 LaTeX 版本、矢量图源和通过全页复核的 PDF。

**Architecture:** 文科固定源为 src-d4b6b4f37b6589b21946176125752f83f1799fd3debba8c90f9f34b8ec08135a， 对应 春季高考/2002/2002春季北京,安徽,内蒙古文.pdf，2 页 A3、印刷页码 97–98；理科固定源为 src-d644e6de1cae82b9335a35b1e29e383d6b90f00d185d35c69752ce1bccb0bf89，对应 春季高考/2002/2002春季北京,安徽,内蒙古理.pdf，2 页 A3、印刷页码 95–96。两份固定源均不附答案；答案与解析独立复算。第 15、19 题图形仅以 TikZ/PGFPlots .tex 永久保存。

## Global Constraints

- 文科源 SHA-256 7a3501a062fe2fd1a4fdee4ad309e75dec03a40820398766be3778dc64f21360，大小 518737 bytes。
- 理科源 SHA-256 56fae78d4d5162c4925a0801f896a88bcfcd1282859e36ba7ba20cbec06b4c7d，大小 519223 bytes。
- 两卷均为 2 页 A3；题面 22 题，选择题 1–12、填空题 13–16、解答题 17–22；保留全部小问。
- 第 15、19 题的原卷图形全部重绘为矢量源；不得提交截图或图片文件。
- 两个项目的 build/ 最终只保留四个 PDF；不得留下 LaTeX 中间物、媒体文件或 .work。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 2002/2002_数学真题_春季京蒙皖文_{试题,答案要点,解析正文,含解析}.md
- Create: 2002/2002_数学真题_春季京蒙皖理_{试题,答案要点,解析正文,含解析}.md
- Create by tool: math-gaokao-latex/2002_春季京蒙皖文卷/*
- Create by tool: math-gaokao-latex/2002_春季京蒙皖理卷/*
- Create figures in each project: figures/{f2002_spring_t15_fold.tex,f2002_spring_t19_prism.tex}

## Tasks

- [x] Verify both source fingerprints, A3 pages and printed page ranges with pdfinfo, SHA-256 and visual renders.
- [x] Transcribe both Q1–Q22, including Q15/Q19 diagrams and all subparts.
- [x] Independently solve both papers, including geometry, sequences, tax/finance, conic sections and recurrence questions.
- [x] Generate both _含解析.md, register b88, generate/check LaTeX, provenance and receipts.
- [x] Compile all eight editions, visually review every page, finalize review, run full gates and tests, clean intermediates, and close this plan.

## Self-Review Checklist

- [x] Both fixed-source fingerprints and printed page ranges are present.
- [x] Each paper has exactly the Q15/Q19 image markers, all mapping to committed .tex figures.
- [x] All 44 questions and subparts are independently checked.
- [x] Eight PDFs compile, are visually reviewed, and no compiler intermediates remain.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with unrelated historical solution-source drifts reported honestly.

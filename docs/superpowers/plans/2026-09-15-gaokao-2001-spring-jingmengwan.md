# 2001 年春季京蒙皖文理卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 执行本计划。各步骤用复选框（[ ]/[x]）跟踪。

**Goal:** 将固定源 PDF 对应的 2001 年春季京蒙皖文、理两卷数学整理为各 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、矢量图源和通过全页复核的 PDF。

**Architecture:** 两卷分别以固定源 src-e5b79db6d28d285c5149ea9e643bf5a49843dc4186b0deceb9450158fc21e05b（文科）与 src-96c06de21b4e484449b83cdf7a1efafaa6d839653ce204b865bc642edbf42486（理科）为唯一题面依据，对应 春季高考/2001/2001春季北京,安徽,内蒙古文.pdf 与 ...理.pdf。文科题面原卷印刷页码 81–82，理科为 79–80，均不附答案；题面、答案、独立解析分别落在 2001/，由现有工具生成两套单卷 LaTeX 工程。第 11 题共用正方体展开图；理科第 19 题另有空间几何图，均只保存 TikZ/PGFPlots .tex。

## Global Constraints

- 文科固定源 SHA-256 为 90c103a50f01ff4ca8d7f8d975795b359fac762dca62dc7a8635d4e844aba575，大小 606200 bytes；理科固定源 SHA-256 为 a63c8250cc11004316c1372ffa11594ab35a2a0e82683921ba68ad822c236241，大小 606615 bytes；原 PDF 不复制进仓库。
- 两份固定源均为 2 页 A3 题面；文科记录印刷页码 81–82，理科记录 79–80；PDF 均不附答案，答案和解析均为本库独立复算。
- 两卷题型均为选择题 1–12、填空题 13–16、解答题 17–22；各含 22 题并保留全部小问。
- 文科第 11 题、理科第 11 题的正方体展开图，以及理科第 19 题空间几何图全部重绘为矢量源；不得提交截图。
- 两套构建目录最终只保留各自四个 PDF；不得留下 LaTeX 中间物、媒体文件或 .work。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 2001/2001_数学真题_春季京蒙皖文_{试题,答案要点,解析正文,含解析}.md
- Create: 2001/2001_数学真题_春季京蒙皖理_{试题,答案要点,解析正文,含解析}.md
- Create by tool: math-gaokao-latex/2001_春季京蒙皖文卷/*
- Create by tool: math-gaokao-latex/2001_春季京蒙皖理卷/*
- Create: math-gaokao-latex/2001_春季京蒙皖文卷/figures/f2001_spring_t11_cube_net.tex
- Create: math-gaokao-latex/2001_春季京蒙皖理卷/figures/{f2001_spring_t11_cube_net.tex,f2001_spring_t19_space_geometry.tex}

## Tasks

- [x] Verify both source fingerprints with pdfinfo, SHA-256 and visual renders; record the printed page ranges.
- [x] Transcribe both Q1–Q22 sets, including the common Q11 net and the science Q19 spatial diagram.
- [x] Independently solve all answers, especially common Q3 binomial-ratio limit, Q4 inverse, Q5 ellipse, Q6 locus, Q7 exponential value, Q8 acute-triangle quadrant, Q9 cone angle, Q10 exponential minimum, Q11 cube-net statements, Q12 demand model, plus arts Q17–Q22 and science Q17–Q22.
- [x] Generate both _含解析.md files, register b86, generate/check LaTeX, provenance and receipts.
- [x] Compile, visually review all pages, finalize reviews, run full gates and tests, clean all intermediates, and close this plan.

## Self-Review Checklist

- [x] Both fixed source fingerprints and printed page ranges are present.
- [x] Only the registered Q11/Q19 logical image markers exist, and all map to committed .tex figures.
- [x] All 44 answers and subparts are independently checked; the arts Q22 and science Q22 geometries are not conflated.
- [x] Eight PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with the preexisting five unrelated solution-source drifts reported.

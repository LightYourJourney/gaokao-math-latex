# 1998 年全国卷理科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox ([ ]) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 1998 年全国卷理科数学整理为 25 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、四个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 src-a982bc00fed2ce1dcc11d576d4bb521585ef9565a6c52a4d28f3352e0547f40a 对应的固定源 PDF；Daxmate/math 的公开 LaTeX 只作为文字定位与交叉检查，不直接作为答案或解析事实源。题面、答案、独立解析分别落在 1998/，由现有工具生成单卷 LaTeX 工程；第 2、10、21、22、23 题的图形仅以 TikZ/PGFPlots .tex 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。

**Spec:** 用户关于继续高考数学转录、删除编译中间产物、图片不入库且保留 PDF/LaTeX 源的要求，以及仓库 CLAUDE.md 的来源、复核、状态和提交不变量。

## Global Constraints

- 固定题面 PDF 普通高考/1998/1998全国理.pdf 的 SHA-256 必须为 d65ba33846dffe2e794ff11c9ded07a6ecd7bab74328a5df5a400fa68fa2b5c2，PDF 原件不复制进仓库。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 .tex 矢量源，逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 .aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak 或 .work。
- 生成的 questions.tex、answers.tex、answers_short.tex、四个版本壳、index.json 与 manifest.csv 只能由现有工具写入。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 1998/1998_数学真题_全国理_试题.md
- Create: 1998/1998_数学真题_全国理_答案要点.md
- Create: 1998/1998_数学真题_全国理_解析正文.md
- Create by tool: 1998/1998_数学真题_全国理_含解析.md
- Create: math-gaokao-latex/1998_全国卷_理科/figures/{f1998_t2_abs_graphs.tex,f1998_t10_bottles.tex,f1998_t21_parabola.tex,f1998_t22_tank.tex,f1998_t23_prism.tex}
- Create by tools: project .tex sources, provenance.json, receipts/{build,review}.json, four local PDFs, reports/phase2-b71.md
- Modify by tools: source-manifest.json, index.json, manifest.csv, missing-issues.md

### Task 1: 固定题面、答案与独立解析

**Files:**
- Create: 1998/1998_数学真题_全国理_试题.md
- Create: 1998/1998_数学真题_全国理_答案要点.md
- Create: 1998/1998_数学真题_全国理_解析正文.md
- Create by tool: 1998/1998_数学真题_全国理_含解析.md

**Interfaces:**
- Consumes: one-page A3 fixed PDF and secondary gaokao/quanguo1998.tex.
- Produces: 25 aligned question blocks, answer blocks for 25 questions including subparts 23/24/25, and 25 independent solution blocks.

- [x] Step 1: Verify source facts. Run pdfinfo, pdftotext -layout, SHA-256 and a visual render; record one-page A3, printed page 56, 25-question structure and no-answer-page caveat.
- [x] Step 2: Transcribe the fixed题面. Preserve all formulas, domains, options and diagrams. Use logical image markers only for Q2/Q10/Q21/Q22/Q23, with no raster files.
- [x] Step 3: Independently solve all questions. Correct known secondary-source errors: Q13 uses the small-circle chord geometry to obtain 2√3; Q21 uses the acute-triangle branch to select the midpoint-origin parabola y²=8x; Q24 intersection algebra gives s=t³/4-t; Q25 comparison reverses when 0<a<1.
- [x] Step 4: Generate and check combined source. Use solution_sources.py extract-batch --write after registration; ensure no solution block copies an entire题面 or emits a fabricated final answer.
- [x] Step 5: Run parser and issue checks, inspect the complete diff, and commit with docs(exams): add 1998 national science source checkpoint.

### Task 2: 注册新来源并生成 LaTeX 工程

**Files:**
- Create temporary ignored input: /private/tmp/gaokao-1998-register.json
- Modify by tools: source-manifest.json, index.json
- Create by tools: 1998_全国卷_理科/{questions.tex,answers.tex,answers_short.tex,试题版.tex,解析版.tex,简答版.tex,印刷版.tex} and four figure sources

**Interfaces:**
- Consumes: Task 1 Markdown and source ID src-a982bc00fed2ce1dcc11d576d4bb521585ef9565a6c52a4d28f3352e0547f40a.
- Produces: paper gk-1998-regular-national-science, batch phase2-b71, four registered figures with two Markdown occurrences each.

- [x] Step 1: Create and dry-run an exact registration spec. Set project directory 1998_全国卷_理科, title 1998 年·全国卷·理科, track science, count 25, base 1998_national_science, pages [1,1], structure 题目: [1,25], and figures f1998_t10_bottles, f1998_t21_parabola, f1998_t22_tank, f1998_t23_prism, f1998_t2_abs_graphs sorted by path.
- [x] Step 2: Write the registration and run generate_projects.py, make_short_answers.py, and make_editions.py in write mode; run each corresponding check mode.
- [x] Step 3: Validate figure occurrence counts and source manifest, inspect generated answer markers, and commit with chore(exams): generate 1998 national science LaTeX source.

### Task 3: provenance、正式构建与清理

**Files:**
- Create by tools: project provenance.json, receipts/build.json, four PDFs

**Interfaces:**
- Consumes: registered current source and generated .tex tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [x] Step 1: Initialize the three .work provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Step 2: Run formal four-edition build; require no compiler errors, missing characters or overfull boxes; inspect logs before cleanup.
- [x] Step 3: Render all PDFs to /private/tmp, visually inspect contact sheets and key pages, then remove only exact build intermediates and the ignored .work directory.
- [x] Step 4: Commit source/build/provenance artifacts with docs(exams): record 1998 national science build; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Files:**
- Create by tool: receipts/review.json, reports/phase2-b71.md
- Modify by tool: source-manifest.json, manifest.csv, missing-issues.md

**Interfaces:**
- Consumes: four current PDFs, build receipt and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch and synchronized CSV/report.

- [x] Step 1: Prepare four review work items and fill all pages with the eight checks after visual inspection.
- [x] Step 2: Run review_receipts.py finalize-batch, require FINALIZED, inspect report and issue transitions.
- [x] Step 3: Run all targeted gates, full 816-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, A3/page/25-question facts and no-answer-page statement are present.
- [x] Q2/Q10/Q21/Q22/Q23 are the only logical image markers and all map to committed .tex figures.
- [x] Q13/Q21/Q24/Q25 secondary-source or algebra traps are independently checked.
- [x] All subpart answer anchors align with questions and solutions.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass.

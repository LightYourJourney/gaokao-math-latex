# 1999 年全国卷理科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 1999 年全国卷理科数学整理为 25 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、五个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID `src-5129c42c66c33e0330ffd67024b0ac5fc5167dd4fa9b76597dfb86e8e91542e7` 对应的固定源 PDF；公开转录只用于文字定位与交叉检查，不作为答案或解析事实源。题面、答案、独立解析分别落在 `1999/`，由现有工具生成单卷 LaTeX 工程；第 1、10、21、22、24 题的图形仅以 TikZ/PGFPlots `.tex` 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。

**Spec:** 用户关于继续高考数学转录、删除编译中间产物、图片不入库且保留 PDF/LaTeX 源的要求，以及仓库 `CLAUDE.md` 的来源、复核、状态和提交不变量。

## Global Constraints

- 固定题面 PDF `普通高考/1999/1999全国理.pdf` 的 SHA-256 必须为 `b51b6bd72d0c59fc472c3a6117245d76accc34f7576252b52a902bed9089a57b`，大小 507132 bytes，PDF 原件不复制进仓库。
- 固定源为 1 页 A3 横向题面，印刷页码为 58；题面不含答案或解析页，答案和解析均须独立复算并诚实标注。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 `.tex` 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 `.aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak` 或 `.work`。
- 生成的 `questions.tex`、`answers.tex`、`answers_short.tex`、四个版本壳、`index.json` 与 `manifest.csv` 只能由现有工具写入。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: `1999/1999_数学真题_全国理_试题.md`
- Create: `1999/1999_数学真题_全国理_答案要点.md`
- Create: `1999/1999_数学真题_全国理_解析正文.md`
- Create by tool: `1999/1999_数学真题_全国理_含解析.md`
- Create: `math-gaokao-latex/1999_全国卷_理科/figures/{f1999_t1_sets.tex,f1999_t10_polyhedron.tex,f1999_t21_prism.tex,f1999_t22_rolling_mill.tex,f1999_t24_locus.tex}`
- Create by tools: project `.tex` sources, `provenance.json`, `receipts/{build,review}.json`, four local PDFs, `reports/phase2-b72.md`
- Modify by tools: `source-manifest.json`, `index.json`, `manifest.csv`, `missing-issues.md`

### Task 1: 固定题面、答案与独立解析

**Files:**
- Create: `1999/1999_数学真题_全国理_试题.md`
- Create: `1999/1999_数学真题_全国理_答案要点.md`
- Create: `1999/1999_数学真题_全国理_解析正文.md`
- Create by tool: `1999/1999_数学真题_全国理_含解析.md`

**Interfaces:**
- Consumes: one-page A3 fixed PDF and any secondary transcription used only as a locator.
- Produces: 25 aligned question blocks, answer blocks for all 25 questions including subparts 21/22/23, and 25 independent solution blocks.

- [ ] Step 1: Verify source facts with `pdfinfo`, `pdftotext -layout`, SHA-256 and a visual render; record the A3/page-58/25-question/no-answer-page facts.
- [ ] Step 2: Transcribe the fixed题面. Preserve the set diagram in Q1, solid geometry diagrams in Q10/Q21, rolling-mill diagram and table in Q22, and coordinate diagram in Q24 through logical image markers only.
- [ ] Step 3: Independently solve all questions, checking the nonstandard traps in Q4/Q6/Q7/Q8/Q10/Q12/Q13/Q15/Q17/Q18/Q19/Q20 and the multi-part geometry/sequences in Q21–Q24; do not infer an answer from an unverified secondary key.
- [ ] Step 4: Generate and check the combined source with `solution_sources.py extract-batch --write` after registration; ensure no solution block copies an entire题面 or emits a fabricated final answer.
- [ ] Step 5: Run parser and issue checks, inspect the complete diff, and commit the source checkpoint with `docs(exams): add 1999 national science source checkpoint`.

### Task 2: 注册新来源并生成 LaTeX 工程

**Files:**
- Create temporary ignored input: `/private/tmp/gaokao-1999-register.json`
- Modify by tools: `source-manifest.json`, `index.json`
- Create by tools: `1999_全国卷_理科/{questions.tex,answers.tex,answers_short.tex,试题版.tex,解析版.tex,简答版.tex,印刷版.tex}` and five figure sources

**Interfaces:**
- Consumes: Task 1 Markdown and source ID `src-5129c42c66c33e0330ffd67024b0ac5fc5167dd4fa9b76597dfb86e8e91542e7`.
- Produces: paper `gk-1999-regular-national-science`, batch `phase2-b72`, five registered figures with two Markdown occurrences each.

- [ ] Step 1: Create and dry-run an exact registration spec: project directory `1999_全国卷_理科`, title `1999 年·全国卷·理科`, track `science`, count 25, base `1999_national_science`, pages `[1,1]`, structure `题目: [1,25]`, figures `f1999_t1_sets`, `f1999_t10_polyhedron`, `f1999_t21_prism`, `f1999_t22_rolling_mill`, `f1999_t24_locus` sorted by path.
- [ ] Step 2: Write the registration and run `generate_projects.py`, `make_short_answers.py`, and `make_editions.py` in write mode; run each corresponding check mode.
- [ ] Step 3: Validate figure occurrence counts, source manifest and generated answer markers, then commit with `chore(exams): generate 1999 national science LaTeX source`.

### Task 3: provenance、正式构建与清理

**Files:**
- Create by tools: project `provenance.json`, `receipts/build.json`, four PDFs

**Interfaces:**
- Consumes: registered current source and generated `.tex` tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [ ] Step 1: Initialize the three `.work` provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [ ] Step 2: Run the formal four-edition build; require no compiler errors, missing characters or overfull boxes; inspect logs before cleanup.
- [ ] Step 3: Render all PDFs to `/private/tmp`, visually inspect contact sheets and key pages, then remove only exact build intermediates and the ignored `.work` directory.
- [ ] Step 4: Commit source/build/provenance artifacts with `docs(exams): record 1999 national science build`; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Files:**
- Create by tool: `receipts/review.json`, `reports/phase2-b72.md`
- Modify by tool: `source-manifest.json`, `manifest.csv`, `missing-issues.md`

**Interfaces:**
- Consumes: four current PDFs, build receipt and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch and synchronized CSV/report.

- [ ] Step 1: Prepare four review work items and fill all pages with the eight checks after visual inspection.
- [ ] Step 2: Run `review_receipts.py finalize-batch`, require `FINALIZED`, inspect the report and issue transitions.
- [ ] Step 3: Run all targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [ ] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [ ] Fixed source fingerprint, A3/page-58/25-question facts and no-answer-page statement are present.
- [ ] Q1/Q10/Q21/Q22/Q24 are the only logical image markers and all map to committed `.tex` figures.
- [ ] All subpart answer anchors align with questions and solutions; Q22's table and Q23's three subparts are preserved.
- [ ] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [ ] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [ ] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

# 1999 年全国卷文科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 1999 年全国卷文科数学整理为 24 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、五个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID \`src-2a6d695a9010eb081aa23c3e34d36994d3c5ad1571206edfb5dc1c3e27c33a7a\` 对应的固定源 PDF；公开转录只用于文字定位与交叉检查，不作为答案或解析事实源。题面、答案、独立解析分别落在 \`1999/\`，由现有工具生成单卷 LaTeX 工程；第 1、10、22、23、24 题的图形仅以 TikZ/PGFPlots \`.tex\` 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。


## Global Constraints

- 固定题面 PDF \`普通高考/1999/1999全国文.pdf\` 的 SHA-256 必须为 \`8c15b937e5cbd7653dd1fe7eb2e4cdaa2f500b5e62f9f2cdfd675cf2db334074\`，大小 508856 bytes，PDF 原件不复制进仓库。
- 固定源为 1 页 A3 横向题面，印刷页码为 59；题面不含答案或解析页，答案和解析均须独立复算并诚实标注。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 \`.tex\` 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 \`.aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak\` 或 \`.work\`。
- 生成的 \`questions.tex\`、\`answers.tex\`、\`answers_short.tex\`、四个版本壳、\`index.json\` 与 \`manifest.csv\` 只能由现有工具写入。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: \`1999/1999_数学真题_全国文_试题.md\`
- Create: \`1999/1999_数学真题_全国文_答案要点.md\`
- Create: \`1999/1999_数学真题_全国文_解析正文.md\`
- Create by tool: \`1999/1999_数学真题_全国文_含解析.md\`
- Create: \`math-gaokao-latex/1999_全国卷_文科/figures/{f1999_t10_polyhedron.tex,f1999_t1_sets.tex,f1999_t22_prism.tex,f1999_t23_rolling_mill.tex,f1999_t24_locus.tex}\`
- Create by tools: project \`.tex\` sources, \`provenance.json\`, \`receipts/{build,review}.json\`, four local PDFs, \`reports/phase2-b73.md\`
- Modify by tools: \`source-manifest.json\`, \`index.json\`, \`manifest.csv\`, \`missing-issues.md\`

### Task 1: 固定题面、答案与独立解析

**Files:**
- Create: \`1999/1999_数学真题_全国文_试题.md\`
- Create: \`1999/1999_数学真题_全国文_答案要点.md\`
- Create: \`1999/1999_数学真题_全国文_解析正文.md\`
- Create by tool: \`1999/1999_数学真题_全国文_含解析.md\`

**Interfaces:**
- Consumes: one-page A3 fixed PDF and any secondary transcription used only as a locator.
- Produces: 24 aligned question blocks, answer blocks for all 24 questions including subparts 22/23, and 24 independent solution blocks.

- [x] Step 1: Verify source facts with \`pdfinfo\`, \`pdftotext -layout\`, SHA-256 and a visual render; record the A3/page-59/24-question/no-answer-page facts.
- [x] Step 2: Transcribe the fixed题面. Preserve the set diagram in Q1, solid geometry diagrams in Q10/Q22, rolling-mill diagram and table in Q23, and coordinate diagram in Q24 through logical image markers only.
- [x] Step 3: Independently solve all questions, checking the shared Q4/Q6/Q7/Q8/Q10/Q12/Q13/Q15/Q17/Q18 items and the arts-only Q6 circle symmetry, Q8 cubic coefficient identity, Q19 logarithmic equation and Q20 sequence limit.
- [x] Step 4: Use the existing \`solution_sources.render_combined\` pure generator to create the required \`_含解析.md\` before registration, then rerun \`solution_sources.py extract-batch --write\` after the batch is registered; ensure no solution block copies an entire题面 or emits a fabricated final answer.
- [x] Step 5: Run parser and issue checks, inspect the complete diff, and commit the source checkpoint with \`docs(exams): add 1999 national arts source checkpoint\`.

### Task 2: 注册新来源并生成 LaTeX 工程

**Files:**
- Create temporary ignored input: \`/private/tmp/gaokao-1999-national-arts-register.json\`
- Modify by tools: \`source-manifest.json\`, \`index.json\`
- Create by tools: \`1999_全国卷_文科/{questions.tex,answers.tex,answers_short.tex,试题版.tex,解析版.tex,简答版.tex,印刷版.tex}\` and five figure sources

**Interfaces:**
- Consumes: Task 1 Markdown and source ID \`src-2a6d695a9010eb081aa23c3e34d36994d3c5ad1571206edfb5dc1c3e27c33a7a\`.
- Produces: paper \`gk-1999-regular-national-arts\`, batch \`phase2-b73\`, five registered figures with two Markdown occurrences each.

- [x] Step 1: Create and dry-run an exact registration spec: project directory \`1999_全国卷_文科\`, title \`1999 年·全国卷·文科\`, track \`arts\`, count 24, base \`1999_national_arts\`, pages \`[1,1]\`, structure \`题目: [1,24]\`, figures \`f1999_t10_polyhedron\`, \`f1999_t1_sets\`, \`f1999_t22_prism\`, \`f1999_t23_rolling_mill\`, \`f1999_t24_locus\` sorted by path.
- [x] Step 2: Write the registration and run \`generate_projects.py\`, \`make_short_answers.py\`, and \`make_editions.py\` in write mode; run each corresponding check mode.
- [x] Step 3: Validate figure occurrence counts, source manifest and generated answer markers, then commit with \`chore(exams): generate 1999 national arts LaTeX source\`.

### Task 3: provenance、正式构建与清理

**Files:**
- Create by tools: project \`provenance.json\`, \`receipts/build.json\`, four PDFs

**Interfaces:**
- Consumes: registered current source and generated \`.tex\` tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [x] Step 1: Initialize the three \`.work\` provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Step 2: Run the formal four-edition build; require no compiler errors, missing characters or overfull boxes; inspect logs before cleanup.
- [x] Step 3: Render all PDFs to \`/private/tmp\`, visually inspect contact sheets and key pages, then remove only exact build intermediates and the ignored \`.work\` directory.
- [x] Step 4: Commit source/build/provenance artifacts with \`docs(exams): record 1999 national arts build\`; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Files:**
- Create by tool: \`receipts/review.json\`, \`reports/phase2-b73.md\`
- Modify by tool: \`source-manifest.json\`, \`manifest.csv\`, \`missing-issues.md\`

**Interfaces:**
- Consumes: four current PDFs, build receipt and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch and synchronized CSV/report.

- [x] Step 1: Prepare four review work items and fill all pages with the eight checks after visual inspection.
- [x] Step 2: Run \`review_receipts.py finalize-batch\`, require \`FINALIZED\`, inspect the report and issue transitions.
- [x] Step 3: Run all targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, A3/page-59/24-question facts and no-answer-page statement are present.
- [x] Q1/Q10/Q22/Q23/Q24 are the only logical image markers and all map to committed \`.tex\` figures.
- [x] Q6/Q8/Q19/Q20 arts-only calculations and all subpart answer anchors are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

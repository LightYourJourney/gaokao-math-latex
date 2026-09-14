# 2000 年全国旧课程卷理科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 2000 年全国旧课程卷理科数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、六个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID \`src-2df550ae82fa57dc70fc83d2c12364bf8a19f13cdc3e8cac49ad80fa8250d1fa\` 对应的固定源 PDF；公开转录只用于文字定位与交叉检查，不作为答案或解析事实源。题面、答案、独立解析分别落在 \`2000/\`，由现有工具生成单卷 LaTeX 工程；第 5、12、16、18、21、22 题的图形仅以 TikZ/PGFPlots \`.tex\` 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。

**Spec:** 用户关于继续高考数学转录、删除编译中间产物、图片不入库且保留 PDF/LaTeX 源的要求，以及仓库 \`CLAUDE.md\` 的来源、复核、状态和提交不变量。

## Global Constraints

- 固定题面 PDF \`普通高考/2000/2000全国旧课程理.pdf\` 的 SHA-256 必须为 \`8cc0483e5f30cdc25df99b7ae68dd4eb7f593f3dd7792c47e284368af39075ef\`，大小 621130 bytes，PDF 原件不复制进仓库。
- 固定源为 2 页 A3 横向题面，原卷印刷页码为 67–68；题面不含答案或解析页，答案和解析均须独立复算并诚实标注。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 \`.tex\` 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 \`.aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak\` 或 \`.work\`。
- 生成的 \`questions.tex\`、\`answers.tex\`、\`answers_short.tex\`、四个版本壳、\`index.json\` 与 \`manifest.csv\` 只能由现有工具写入。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: \`2000/2000_数学真题_全国旧课程理_试题.md\`
- Create: \`2000/2000_数学真题_全国旧课程理_答案要点.md\`
- Create: \`2000/2000_数学真题_全国旧课程理_解析正文.md\`
- Create by tool: \`2000/2000_数学真题_全国旧课程理_含解析.md\`
- Create: \`math-gaokao-latex/2000_全国旧课程卷_理科/figures/{f2000_t5_graphs.tex,f2000_t12_cone.tex,f2000_t16_projection.tex,f2000_t18_parallelepiped.tex,f2000_t21_market_cost.tex,f2000_t22_hyperbola.tex}\`
- Create by tools: project \`.tex\` sources, \`provenance.json\`, \`receipts/{build,review}.json\`, four local PDFs, \`reports/phase2-b74.md\`
- Modify by tools: \`source-manifest.json\`, \`index.json\`, \`manifest.csv\`, \`missing-issues.md\`

### Task 1: 固定题面、答案与独立解析

**Files:**
- Create: \`2000/2000_数学真题_全国旧课程理_试题.md\`
- Create: \`2000/2000_数学真题_全国旧课程理_答案要点.md\`
- Create: \`2000/2000_数学真题_全国旧课程理_解析正文.md\`
- Create by tool: \`2000/2000_数学真题_全国旧课程理_含解析.md\`

**Interfaces:**
- Consumes: two-page A3 fixed PDF and any secondary transcription used only as a locator.
- Produces: 22 aligned question blocks, answer blocks for all 22 questions including subparts 17/18/19/20/21/22, and 22 independent solution blocks.

- [x] Step 1: Verify source facts with \`pdfinfo\`, \`pdftotext -layout\`, SHA-256 and visual renders; record page-67/page-68 placement, 22-question structure and no-answer-page caveat.
- [x] Step 2: Transcribe the fixed题面. Preserve the Q5 graph options, Q12 cone diagram, Q16 cube/projection options, Q18 parallelepiped, Q21 two data graphs, and Q22 trapezoid/hyperbola diagram through logical image markers only.
- [x] Step 3: Independently solve all questions, explicitly checking the tax calculation, polar-coordinate circle, cone volume partition, recurrence in Q15, market/cost graph functions, and the hyperbola eccentricity range; do not infer answers from an unverified secondary key.
- [x] Step 4: Use the existing \`solution_sources.render_combined\` pure generator to create the required \`_含解析.md\` before registration, then rerun \`solution_sources.py extract-batch --write\` after the batch is registered; ensure no solution block copies an entire题面 or emits a fabricated final answer.
- [x] Step 5: Run parser and issue checks, inspect the complete diff, and commit the source checkpoint with \`docs(exams): add 2000 national old-science source checkpoint\`.

### Task 2: 注册新来源并生成 LaTeX 工程

**Files:**
- Create temporary ignored input: \`/private/tmp/gaokao-2000-national-old-science-register.json\`
- Modify by tools: \`source-manifest.json\`, \`index.json\`
- Create by tools: \`2000_全国旧课程卷_理科/{questions.tex,answers.tex,answers_short.tex,试题版.tex,解析版.tex,简答版.tex,印刷版.tex}\` and six figure sources

**Interfaces:**
- Consumes: Task 1 Markdown and source ID \`src-2df550ae82fa57dc70fc83d2c12364bf8a19f13cdc3e8cac49ad80fa8250d1fa\`.
- Produces: paper \`gk-2000-regular-national-old-science\`, batch \`phase2-b74\`, six registered figures with two Markdown occurrences each.

- [x] Step 1: Create and dry-run an exact registration spec: project directory \`2000_全国旧课程卷_理科\`, title \`2000 年·全国旧课程卷·理科\`, track \`science\`, count 22, base \`2000_national_old_science\`, pages \`[1,2]\`, structure \`题目: [1,22]\`, figures \`f2000_t12_cone\`, \`f2000_t16_projection\`, \`f2000_t18_parallelepiped\`, \`f2000_t21_market_cost\`, \`f2000_t22_hyperbola\`, \`f2000_t5_graphs\` sorted by path.
- [x] Step 2: Write the registration and run \`generate_projects.py\`, \`make_short_answers.py\`, and \`make_editions.py\` in write mode; run each corresponding check mode.
- [x] Step 3: Validate figure occurrence counts, source manifest and generated answer markers, then commit with \`chore(exams): generate 2000 national old-science LaTeX source\`.

### Task 3: provenance、正式构建与清理

**Files:**
- Create by tools: project \`provenance.json\`, \`receipts/build.json\`, four PDFs

**Interfaces:**
- Consumes: registered current source and generated \`.tex\` tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [x] Step 1: Initialize the three \`.work\` provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Step 2: Run the formal four-edition build; require no compiler errors, missing characters or overfull boxes; inspect logs before cleanup.
- [x] Step 3: Render all PDFs to \`/private/tmp\`, visually inspect contact sheets and key pages, then remove only exact build intermediates and the ignored \`.work\` directory.
- [x] Step 4: Commit source/build/provenance artifacts with \`docs(exams): record 2000 national old-science build\`; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Files:**
- Create by tool: \`receipts/review.json\`, \`reports/phase2-b74.md\`
- Modify by tool: \`source-manifest.json\`, \`manifest.csv\`, \`missing-issues.md\`

**Interfaces:**
- Consumes: four current PDFs, build receipt and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch and synchronized CSV/report.

- [x] Step 1: Prepare four review work items and fill all pages with the eight checks after visual inspection.
- [x] Step 2: Run \`review_receipts.py finalize-batch\`, require \`FINALIZED\`, inspect the report and issue transitions.
- [x] Step 3: Run all targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, A3/page-67–68/22-question facts and no-answer-page statement are present.
- [x] Q5/Q12/Q16/Q18/Q21/Q22 are the only logical image markers and all map to committed \`.tex\` figures.
- [x] Q12/Q15/Q21/Q22 calculations and all subpart answer anchors are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

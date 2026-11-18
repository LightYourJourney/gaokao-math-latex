# 2000 年全国新课程卷理科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox ([ ]/[x]) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 2000 年全国新课程卷理科数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、七个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID src-141d138f3d26910518b47759686b06eea4563ba9d9df53742fc363c6f69721b0 对应的固定源 PDF；公开转录只用于文字定位与交叉检查，不作为答案或解析事实源。题面、答案、独立解析分别落在 2000/，由现有工具生成单卷 LaTeX 工程；第 5、8、12、16、18 甲、18 乙、22 题的图形仅以 TikZ/PGFPlots .tex 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。


## Global Constraints

- 固定题面 PDF 普通高考/2000/2000全国新课程理(江西,山西,天津).pdf 的 SHA-256 必须为 14971abf14842908218855831004ccb4bfa92af6611bdd8b6788c863fcecfc34，大小 534322 bytes，PDF 原件不复制进仓库。
- 固定源为 2 页 A3 横向题面，原卷印刷页码为 74–75；题面不含答案或解析页，答案和解析均须独立复算并诚实标注。
- 第 18 题保留原卷甲/乙二选一结构；甲为直三棱柱，乙为平行六面体。两种变体都属于同一印刷题号，解析和答案不得静默丢掉任一变体。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 .tex 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 .aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak 或 .work。
- 生成的 questions.tex、answers.tex、answers_short.tex、四个版本壳、index.json 与 manifest.csv 只能由现有工具写入。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: 2000/2000_数学真题_全国新课程理_试题.md
- Create: 2000/2000_数学真题_全国新课程理_答案要点.md
- Create: 2000/2000_数学真题_全国新课程理_解析正文.md
- Create by tool: 2000/2000_数学真题_全国新课程理_含解析.md
- Create: math-gaokao-latex/2000_全国新课程卷_理科/figures/{f2000_t5_graphs.tex,f2000_t8_area.tex,f2000_t12_cone.tex,f2000_t16_projection.tex,f2000_t18a_tri_prism.tex,f2000_t18b_parallelepiped.tex,f2000_t22_hyperbola.tex}
- Create by tools: project .tex sources, provenance.json, receipts/{build,review}.json, four local PDFs, reports/phase2-b77.md
- Modify by tools: source-manifest.json, index.json, manifest.csv, missing-issues.md

### Task 1: 固定题面、答案与独立解析

**Files:**
- Create: the three canonical Markdown files listed above
- Create by tool: the deterministic _含解析.md

**Interfaces:**
- Consumes: the fixed two-page A3 PDF and secondary material only for locating text.
- Produces: 22 aligned question blocks, the complete Q18甲/乙 alternatives, answer blocks for all questions including Q17–Q22 subparts, and 22 independent solution blocks.

- [x] Step 1: Verify source facts with pdfinfo, pdftotext -layout, SHA-256 and visual renders; record page-74/page-75 placement, 22-question structure, Q18 alternatives, and the no-answer-page caveat.
- [x] Step 2: Transcribe Q1–Q22 from the fixed PDF. Preserve the Q5 graph options, Q8 shaded-area graph, Q12 cone diagram, Q16 cube/projection options, both Q18 figures, and Q22 trapezoid/hyperbola diagram using logical image markers only.
- [x] Step 3: Independently solve every question. In particular verify Q1 as (3/2,1/2), Q2 as ②④, Q8 as 32/3, Q12 as arccos(1/4√2), Q13 as (0.9025,0.095,0.0025), Q17 as (4/15,13/15), Q18甲 as (√3,3/√30,orthogonal), Q18乙 as CD/CC1=1, Q19 as T_n=n(n-9)/4, Q21 as height 1.2 m and volume 1.8 m³, and Q22 as 3≤e≤√13.
- [x] Step 4: Use solution_sources.render_combined() to generate _含解析.md from the three canonical sources, then run solution_sources.py extract-batch --write after registration; ensure the Q18 alternatives remain in one aligned question block and no solution block copies an entire题面 or emits a fabricated final answer.
- [x] Step 5: Run parser, answer, and issue checks; inspect the complete diff; commit the source checkpoint with docs(exams): add 2000 national new-science source checkpoint.

### Task 2: 注册来源并生成 LaTeX 工程

**Files:**
- Create temporary ignored input: /private/tmp/gaokao-2000-national-new-science-register.json
- Modify by tools: source-manifest.json, index.json
- Create by tools: 2000_全国新课程卷_理科/{questions.tex,answers.tex,answers_short.tex,试题版.tex,解析版.tex,简答版.tex,印刷版.tex} and seven figure sources

**Interfaces:**
- Consumes: Task 1 Markdown and source ID src-141d138f3d26910518b47759686b06eea4563ba9d9df53742fc363c6f69721b0.
- Produces: paper gk-2000-regular-national-new-science, batch phase2-b77, seven registered figures with two Markdown occurrences each.

- [x] Step 1: Create and dry-run an exact registration spec: project directory 2000_全国新课程卷_理科, title 2000 年·全国新课程卷·理科, track science, count 22, base 2000_national_new_science, pages [1,2], printed pages [74,75], structure 题目 [1,22], and figures f2000_t5_graphs, f2000_t8_area, f2000_t12_cone, f2000_t16_projection, f2000_t18a_tri_prism, f2000_t18b_parallelepiped, f2000_t22_hyperbola sorted by path.
- [x] Step 2: Write the registration and run generate_projects.py, make_short_answers.py, and make_editions.py in write mode; run every corresponding check mode.
- [x] Step 3: Validate seven figure occurrence counts, source manifest, generated answer markers, and both Q18 variant answer sets; commit with chore(exams): generate 2000 national new-science LaTeX source.

### Task 3: provenance、正式构建与清理

**Files:**
- Create by tools: project provenance.json, receipts/build.json, four local PDFs

**Interfaces:**
- Consumes: the registered current source and generated .tex tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [x] Step 1: Initialize the three .work provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Step 2: Run the formal four-edition build; require no compiler errors, missing characters, overfull boxes, or unresolved references; inspect logs before cleanup.
- [x] Step 3: Render all PDFs to /private/tmp, inspect contact sheets and key pages, then remove only exact build intermediates and the ignored batch .work directory.
- [x] Step 4: Commit source/build/provenance artifacts with docs(exams): record 2000 national new-science build; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Files:**
- Create by tool: receipts/review.json, reports/phase2-b77.md
- Modify by tool: source-manifest.json, manifest.csv, missing-issues.md

**Interfaces:**
- Consumes: four current PDFs, build receipt, and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch, and synchronized CSV/report.

- [x] Step 1: Prepare four review work items and fill every page with the eight checks after visual inspection.
- [x] Step 2: Run review_receipts.py finalize-batch, require FINALIZED, inspect the report and issue transitions.
- [x] Step 3: Run targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, A3/page-74–75/22-question facts, Q18甲/乙 structure, and no-answer-page statement are present.
- [x] Q5/Q8/Q12/Q16/Q18甲/Q18乙/Q22 are the only logical image markers and all map to committed .tex figures.
- [x] Q1/Q2/Q8/Q12/Q13/Q17/Q18/Q19/Q21/Q22 calculations and all subpart/variant answer anchors are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

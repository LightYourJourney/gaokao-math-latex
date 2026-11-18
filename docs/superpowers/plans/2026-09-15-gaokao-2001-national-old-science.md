# 2001 年全国旧课程卷理科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox ([ ]/[x]) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 2001 年全国旧课程卷理科数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、四个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID `src-0869d3e56197607fc1bb522c8ff01213fdafc5abd44467f9d231acb76532e05f` 对应的固定源 PDF；公开转录只用于文字定位与交叉检查，不作为答案或解析事实源。题面、答案、独立解析分别落在 `2001/`，由现有工具生成单卷 LaTeX 工程；第 5、11、12、17 题的图形仅以 TikZ/PGFPlots `.tex` 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。


## Global Constraints

- 固定题面 PDF `普通高考/2001/2001全国旧课程理.pdf` 的 SHA-256 必须为 `a17fd2e87b221bffe44d784d631dfd086db68fb7941026c4a30de297f8e99195`，大小 `502018` bytes，PDF 原件不复制进仓库。
- 固定源为 2 页 A3 横向题面，原卷印刷页码为 85–86；题面不含答案或解析页，答案和解析均须独立复算并诚实标注。
- 题面含 22 题：选择题 1–12、填空题 13–16、解答题 17–22；第 17 题含 2 个小问，第 18、19、20、21、22 题的结构须按源 PDF 逐题保留。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 `.tex` 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 `.aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak` 或 `.work`。
- 生成的 `questions.tex`、`answers.tex`、`answers_short.tex`、四个版本壳、`index.json` 与 `manifest.csv` 只能由现有工具写入。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: `2001/2001_数学真题_全国旧课程理_试题.md`
- Create: `2001/2001_数学真题_全国旧课程理_答案要点.md`
- Create: `2001/2001_数学真题_全国旧课程理_解析正文.md`
- Create by tool: `2001/2001_数学真题_全国旧课程理_含解析.md`
- Create: `math-gaokao-latex/2001_全国旧课程卷_理科/figures/{f2001_t5_polar.tex,f2001_t11_roofs.tex,f2001_t12_network.tex,f2001_t17_pyramid.tex}`
- Create by tools: project `.tex` sources, `provenance.json`, `receipts/{build,review}.json`, four local PDFs, `reports/phase2-b78.md`
- Modify by tools: `source-manifest.json`, `manifest.csv`, `missing-issues.md`

### Task 1: 固定题面、答案与独立解析

**Interfaces:**

- Consumes: the fixed two-page A3 PDF and secondary material only for locating text.
- Produces: 22 aligned question blocks, all four choices for Q1–Q12, four fill-ins, six solution blocks, and the four logical image markers.

- [x] Step 1: Verify source facts with `pdfinfo`, `pdftotext -layout`, SHA-256 and visual renders; record page-85/page-86 placement, 22-question structure, and the no-answer-page caveat.
- [x] Step 2: Transcribe Q1–Q22 from the fixed PDF. Preserve the Q5 polar-graph choices, Q11 roof diagrams, Q12 information-network graph, and Q17 pyramid diagram using logical image markers only.
- [x] Step 3: Independently solve every question and recheck the high-risk items: Q3 increasing arithmetic sequence, Q5 polar graph, Q9 prism angle, Q12 max-flow value, Q14 hyperbola distance, Q16 right-triangle count on a circle, Q17 dihedral angle, Q18 complex maximum, Q20 AM–GM inequalities, Q21 geometric-series comparison, and Q22 periodic-function limit.
- [x] Step 4: Use `solution_sources.render_combined()` to generate `_含解析.md` from the three canonical sources, then run `solution_sources.py extract-batch --write` after registration; ensure every solution block has an independent conclusion and no source image is copied.
- [x] Step 5: Run parser, answer, and issue checks; inspect the complete diff; commit the source checkpoint with `docs(exams): add 2001 national old-science source checkpoint`.

### Task 2: 注册来源并生成 LaTeX 工程

**Interfaces:**

- Consumes: Task 1 Markdown and source ID `src-0869d3e56197607fc1bb522c8ff01213fdafc5abd44467f9d231acb76532e05f`.
- Produces: paper `gk-2001-regular-national-old-science`, project `2001_全国旧课程卷_理科`, batch `phase2-b78`, four registered figures with two Markdown occurrences each.

- [x] Step 1: Create and dry-run an exact registration spec: project directory `2001_全国旧课程卷_理科`, title `2001 年·全国旧课程卷·理科`, track science, count 22, base `2001_national_old_science`, pages `[1,2]`, printed pages `[85,86]`, structure `题目 [1,22]`, and figures `f2001_t5_polar`, `f2001_t11_roofs`, `f2001_t12_network`, `f2001_t17_pyramid` sorted by path.
- [x] Step 2: Write the registration and run `generate_projects.py`, `make_short_answers.py`, and `make_editions.py` in write mode; run every corresponding check mode.
- [x] Step 3: Validate four figure occurrence counts, source manifest, generated answer markers, and all Q17 subpart answer anchors; commit with `chore(exams): generate 2001 national old-science LaTeX source`.

### Task 3: provenance、正式构建与清理

**Interfaces:**

- Consumes: the registered current source and generated `.tex` tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [x] Step 1: Initialize the three `.work` provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Step 2: Run the formal four-edition build; require no compiler errors, missing characters, overfull boxes, or unresolved references; inspect logs before cleanup.
- [x] Step 3: Render all PDFs to `/private/tmp`, inspect contact sheets and key pages, then remove only exact build intermediates and the ignored batch `.work` directory.
- [x] Step 4: Commit source/build/provenance artifacts with `docs(exams): record 2001 national old-science build`; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Interfaces:**

- Consumes: four current PDFs, build receipt, and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch, and synchronized CSV/report.

- [x] Step 1: Prepare four review work items and fill every page with the eight checks after visual inspection.
- [x] Step 2: Run `review_receipts.py finalize-batch`, require `FINALIZED`, inspect the report and issue transitions.
- [x] Step 3: Run targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, A3/page-85–86/22-question facts, and no-answer-page statement are present.
- [x] Q5/Q11/Q12/Q17 are the only logical image markers and all map to committed `.tex` figures.
- [x] Q3/Q5/Q9/Q12/Q14/Q16/Q17/Q18/Q20/Q21/Q22 calculations and all subpart answer anchors are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

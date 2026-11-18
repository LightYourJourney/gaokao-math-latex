# 2001 年全国旧课程卷文科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox ([ ]/[x]) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 2001 年全国旧课程卷文科数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、三个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID `src-252f7a32a0058e8d3fb0340da1a06b0c40d364068e006dcd6a7e6db9f4e3c282` 对应的固定源 PDF；公开转录只用于文字定位与交叉检查，不作为答案或解析事实源。题面、答案、独立解析分别落在 `2001/`，由现有工具生成单卷 LaTeX 工程；第 11、12、18 题的图形仅以 TikZ/PGFPlots `.tex` 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。


## Global Constraints

- 固定题面 PDF `普通高考/2001/2001全国旧课程文.pdf` 的 SHA-256 必须为 `8adbfbaa796703ab10cb4b2569e0543ddf5943a4a285bf5cfda4d4ded31c5370`，大小 `506284` bytes，PDF 原件不复制进仓库。
- 固定源为 2 页 A3 横向题面，原卷印刷页码为 87–88；题面不含答案或解析页，答案和解析均须独立复算并诚实标注。
- 题面含 22 题：选择题 1–12、填空题 13–16、解答题 17–22；第 22 题只保留源 PDF 明示的两个小问，不从其他版本补入第三问。
- 二手转录只用于定位；发现其与固定源或独立计算冲突时保留固定源字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 `.tex` 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 `.aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak` 或 `.work`。
- 生成的 `questions.tex`、`answers.tex`、`answers_short.tex`、四个版本壳、`index.json` 与 `manifest.csv` 只能由现有工具写入。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: `2001/2001_数学真题_全国旧课程文_试题.md`
- Create: `2001/2001_数学真题_全国旧课程文_答案要点.md`
- Create: `2001/2001_数学真题_全国旧课程文_解析正文.md`
- Create by tool: `2001/2001_数学真题_全国旧课程文_含解析.md`
- Create: `math-gaokao-latex/2001_全国旧课程卷_文科/figures/{f2001_t11_roofs.tex,f2001_t12_network.tex,f2001_t18_pyramid.tex}`
- Create by tools: project .tex sources, `provenance.json`, `receipts/{build,review}.json`, four local PDFs, `reports/phase2-b79.md`
- Modify by tools: `source-manifest.json`, `manifest.csv`, `missing-issues.md`

### Task 1: 固定题面、答案与独立解析

**Interfaces:**

- Consumes: the fixed two-page A3 PDF and secondary material only for locating text.
- Produces: 22 aligned question blocks, all four choices for Q1–Q12, four fill-ins, six solution blocks, and the three logical image markers.

- [x] Step 1: Verify source facts with `pdfinfo`, `pdftotext -layout`, SHA-256 and visual renders; record page-87/page-88 placement, 22-question structure, and the no-answer-page caveat.
- [x] Step 2: Transcribe Q1–Q22 from the fixed PDF. Preserve the Q11 roof diagrams, Q12 information-network graph, and Q18 pyramid diagram using logical image markers only.
- [x] Step 3: Independently solve every question and recheck the high-risk items: Q1 trigonometric value, Q3 cone surface area, Q5 complex argument, Q6 inverse function domain, Q9 prism angle, Q12 max-flow value, Q13 binomial coefficient, Q14 hyperbola distance, Q15 geometric ratio, Q16 right-triangle count, Q17 series sum, Q18 dihedral angle, Q19 cyclic quadrilateral area, Q20 parabola proof, Q21 poster optimization, and Q22 periodic-function values.
- [x] Step 4: Use `solution_sources.render_combined()` to generate `_含解析.md` from the three canonical sources, then run `solution_sources.py extract-batch --write` after registration; ensure every solution block has an independent conclusion and no source image is copied.
- [x] Step 5: Run parser, answer, and issue checks; inspect the complete diff; commit the source checkpoint with `docs(exams): add 2001 national old-arts source checkpoint`.

### Task 2: 注册来源并生成 LaTeX 工程

**Interfaces:**

- Consumes: Task 1 Markdown and source ID `src-252f7a32a0058e8d3fb0340da1a06b0c40d364068e006dcd6a7e6db9f4e3c282`.
- Produces: paper `gk-2001-regular-national-old-arts`, project `2001_全国旧课程卷_文科`, batch `phase2-b79`, three registered figures with two Markdown occurrences each.

- [x] Step 1: Create and dry-run an exact registration spec: project directory `2001_全国旧课程卷_文科`, title `2001 年·全国旧课程卷·文科`, track arts, count 22, base `2001_national_old_arts`, pages `[1,2]`, printed pages `[87,88]`, structure `题目 [1,22]`, and figures `f2001_t11_roofs`, `f2001_t12_network`, `f2001_t18_pyramid` sorted by path.
- [x] Step 2: Write the registration and run `generate_projects.py`, `make_short_answers.py`, and `make_editions.py` in write mode; run every corresponding check mode.
- [x] Step 3: Validate three figure occurrence counts, source manifest, generated answer markers, and all Q17/Q22 subpart answer anchors; commit with `chore(exams): generate 2001 national old-arts LaTeX source`.

### Task 3: provenance、正式构建与清理

**Interfaces:**

- Consumes: the registered current source and generated `.tex` tree.
- Produces: current three-role provenance, four successful build records, and a build directory containing PDFs only after cleanup.

- [x] Step 1: Initialize the three `.work` provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Step 2: Run the formal four-edition build; require no compiler errors, missing characters, overfull boxes, or unresolved references; inspect logs before cleanup.
- [x] Step 3: Render all PDFs to `/private/tmp`, inspect contact sheets and key pages, then remove only exact build intermediates and the ignored batch `.work` directory.
- [x] Step 4: Commit source/build/provenance artifacts with `docs(exams): record 2001 national old-arts build`; leave PDFs local and ignored per repository policy.

### Task 4: 全页复核、关闭批次与全库验证

**Interfaces:**

- Consumes: four current PDFs, build receipt, and fresh rendered-page evidence.
- Produces: finalized review, complete paper, closed batch, and synchronized CSV/report.

- [x] Step 1: Prepare four review work items and fill every page with the eight checks after visual inspection.
- [x] Step 2: Run `review_receipts.py finalize-batch`, require `FINALIZED`, inspect the report and issue transitions.
- [x] Step 3: Run targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Step 4: Mark this plan checked, commit the final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, A3/page-87–88/22-question facts, and no-answer-page statement are present.
- [x] Q11/Q12/Q18 are the only logical image markers and all map to committed `.tex` figures.
- [x] Q1/Q3/Q5/Q6/Q9/Q12/Q13/Q14/Q15/Q16/Q17/Q18/Q19/Q20/Q21/Q22 calculations and all subpart answer anchors are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

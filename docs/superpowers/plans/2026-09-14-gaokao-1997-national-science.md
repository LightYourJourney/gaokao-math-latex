# 1997 年全国卷理科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 1997 年全国卷理科数学，整理为逐题可追溯的 Markdown 源、四种可编译 LaTeX 版本和已复核 PDF，并接入现有总账。

**Architecture:** 以 `source-manifest.json` 中已经固定的 `src-930ed...` 题面 PDF 为唯一题面事实源，以公开 Daxmate 转录仅作逐题定位和交叉核对；题面、答案要点、独立解析分别落在 `1997/`，由现有生成器投影到单卷 LaTeX 工程。几何图和函数图全部用工程内 TikZ/PGFPlots 重绘，不保存图片；构建回执、来源指纹和复核回执记录可重现性，状态只在事实核对完成后推进。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。

**Spec:** 用户关于继续高考数学转录、清除编译中间产物、仅保留 PDF 与 LaTeX 源文件的要求，以及仓库 `CLAUDE.md` 的来源、复核、图片和提交不变量。

## Global Constraints

- 固定题面 PDF 只从 `普通高考/1997/1997全国理.pdf` 读取；其 SHA-256 必须保持 `51963e62fb3a1df87724af2b08cd7247c84a65e58c601119489a71b655b81ffb`，不把 PDF 原件复制进仓库。
- 公开转录只能作为交叉核对材料，不能替代固定源，也不能把其明显错误的答案或解析照搬进本库。
- 题面异文、缺失或无法从独立证据裁决的内容照录并登记问题，不擅自修订；每题答案必须由题面和独立推导支持。
- 任何图形均为 `.tex` 矢量源；新工程和 `build/` 中不得出现 PNG/JPEG/SVG 或 `aux/log/fls/out/toc/synctex.gz/fdb_latexmk/bcf/run.xml/nav/snm/vrb/idx/ilg/ind/lof/lot/pyc/pyo/swp/swo/bak`。
- `math-gaokao-latex/` 的共享状态只能通过现有工具更新；不手改生成的 `questions.tex`、`answers.tex`、`answers_short.tex`、版本包装文件、`index.json` 或 `manifest.csv`。
- 构建目录最终只保留四个 PDF；构建、来源、复核门禁必须在提交前从干净的最新输入重跑。
- 不修改主工作树，不 push；每个可独立验收的阶段尽早提交。

## File Map

- Create: `1997/1997_数学真题_全国理_试题.md` — 固定源逐题题面和图形说明。
- Create: `1997/1997_数学真题_全国理_答案要点.md` — 25 题答案与答案归属说明。
- Create: `1997/1997_数学真题_全国理_解析正文.md` — 25 题独立推导，含几何、数列、函数和最值证明。
- Create: `1997/1997_数学真题_全国理_含解析.md` — 按仓库约定合并题面和解析的源文档。
- Create: `math-gaokao-latex/1997_全国卷_理科/figures/{f1997_t3_graphs.tex,f1997_t23_cube.tex}` — 固定源实际出现的第 3 题四个函数图象选项和第 23 题正方体示意图。
- Create by tools: `math-gaokao-latex/1997_全国卷_理科/{questions.tex,answers.tex,answers_short.tex,试题版.tex,解析版.tex,简答版.tex,印刷版.tex}` and four PDFs under `build/`.
- Create by tools: `math-gaokao-latex/1997_全国卷_理科/{provenance.json,receipts/build.json,receipts/review.json}` and `reports/phase2-b70.md`.
- Modify by tools: `math-gaokao-latex/{source-manifest.json,index.json,manifest.csv,missing-issues.md}`; only add the new source binding, paper, batch, projection and any evidence-backed issue records.

### Task 1: 固定 1997 题面并建立三份人工源文档

**Files:**
- Create: `1997/1997_数学真题_全国理_试题.md`
- Create: `1997/1997_数学真题_全国理_答案要点.md`
- Create: `1997/1997_数学真题_全国理_解析正文.md`
- Create: `1997/1997_数学真题_全国理_含解析.md`
- Test: `math-gaokao-latex/tools/issues.py` and the Markdown parser exercised by `generate_projects.py --check`

**Interfaces:**
- Consumes: fixed PDF metadata and text from `gaokaomath-src/普通高考/1997/1997全国理.pdf`; secondary locator `gaokao/quanguo1997.tex` from Daxmate/math.
- Produces: four Markdown files with frontmatter, 25 numbered questions, 25 answer entries, 25 independent solution sections, and only `.tex` figure references.

- [x] **Step 1: Record the source facts before transcribing.** Confirm with `pdfinfo`, `pdftotext -layout`, and SHA-256 that the source is a one-page A3 PDF with 25 questions; keep those values in the source note and do not add the binary to Git.
- [x] **Step 2: Transcribe all 25 questions from the fixed source.** Preserve formulas, options, parameter domains, multi-part numbering, and the original `x`/`y`/`n` variables. Represent only the source's Q3 and Q23 diagrams with `![...](images/1997-t3-graphs.png)` and `![...](images/1997-t23-cube.png)` logical markers; the PNG files are deliberately not created. Use the Daxmate file only to locate text or compare a glyph, and mark any disagreement for explicit review.
- [x] **Step 3: Derive all answers independently.** Check the objective answers against direct algebra or geometry, including the circle/arc optimization in Q25, the four-point coplanarity count in Q15, the recurrence limit in Q21, and the cube geometry in Q23; do not copy Daxmate's known malformed prose or fill-in typo without checking the fixed scan.
- [x] **Step 4: Write the solution body and combined source.** State that the PDF has no answer/解析页, identify independent calculation, explain every selected answer, and add figure notes for the two TikZ replacements. Keep the combined file synchronized with the three canonical sources.
- [x] **Step 5: Run source-only mechanical checks.** Run `python3 math-gaokao-latex/tools/issues.py validate --file math-gaokao-latex/missing-issues.md`; run the generator in check mode after a temporary registration spec is prepared, and stop before registration if question counts or answer markers disagree.
- [x] **Step 6: Commit the source checkpoint.** Review `git diff --check` and the complete new Markdown diff, then commit with `docs(exams): add 1997 national science source checkpoint`.

### Task 2: 登记来源和新卷批次，生成 LaTeX 工程

**Files:**
- Create temporary ignored input: `/private/tmp/gaokao-1997-register.json`
- Modify by tool: `math-gaokao-latex/source-manifest.json`
- Modify by tool: `math-gaokao-latex/index.json`
- Create by tool: `math-gaokao-latex/1997_全国卷_理科/`

**Interfaces:**
- Consumes: Task 1 Markdown files and source entry `src-930ed190601053d47a6c2d72d9d2185d4d734e0e92462e66ace578b294dbe9db`.
- Produces: paper `gk-1997-regular-national-science`, project directory `1997_全国卷_理科`, batch `phase2-b70`, and generated source files whose figure occurrence counts agree with registration.

- [x] **Step 1: Create the exact registration spec.** Use `paper_id: gk-1997-regular-national-science`, `project_dir: 1997_全国卷_理科`, `title: 1997 年·全国卷·理科`, `year: 1997`, `track: science`, `question_count: 25`, the four canonical Markdown paths under `1997/`, `source_ids: [src-930ed190601053d47a6c2d72d9d2185d4d734e0e92462e66ace578b294dbe9db]`, and exactly two figure records `1997_全国卷_理科/figures/f1997_t3_graphs.tex` and `1997_全国卷_理科/figures/f1997_t23_cube.tex`, each expected twice; set index metadata to paper `全国卷（理科）`, variant `全国理科`, structure `题目: [1,25]`, pages_q `[1,1]`, pages_s `null`, and base `1997_national_science`.
- [x] **Step 2: Dry-run and write the registration.** Run `python3 math-gaokao-latex/tools/source_manifest.py register-papers --repo . --manifest math-gaokao-latex/source-manifest.json --spec /private/tmp/gaokao-1997-register.json`, inspect the paper and batch output, then rerun with `--write` only after the source files and IDs pass validation.
- [x] **Step 3: Generate all project content.** Run `python3 math-gaokao-latex/tools/generate_projects.py --manifest math-gaokao-latex/source-manifest.json --paper gk-1997-regular-national-science --write` and inspect each generated figure include and answer marker.
- [x] **Step 4: Generate short answers and editions.** Run `python3 math-gaokao-latex/tools/make_short_answers.py --manifest math-gaokao-latex/source-manifest.json --paper gk-1997-regular-national-science --write`; run the edition generator used by this repository to create the four `.tex` wrappers, then run `source_manifest.py validate --manifest ...` and `manifest_csv.py ... --check`.
- [x] **Step 5: Commit the generated source checkpoint.** Include only Markdown, `.tex`, JSON/CSV manifests, and generated vector figure sources; verify no image or compiler intermediate is staged, then commit with `chore(exams): generate 1997 national science LaTeX source`.

### Task 3: 建立 provenance、四版构建和可重现回执

**Files:**
- Modify: `math-gaokao-latex/1997_全国卷_理科/provenance.json`
- Create/modify by tools: `math-gaokao-latex/1997_全国卷_理科/receipts/build.json`
- Create: `math-gaokao-latex/1997_全国卷_理科/build/{试题版,解析版,简答版,印刷版}.pdf`

**Interfaces:**
- Consumes: generated project, fixed source fingerprint, source-manifest paper record, and clean tracked tree from Task 2.
- Produces: provenance role records for questions/answers/solutions/figures, four successful current build receipts, and no residual intermediates.

- [x] **Step 1: Initialize and materialize provenance.** Use `provenance.py` to initialize the `phase2-b70` batch, materialize the three role JSON files (`question-review`/`answer-solve`/`answer-review`), import the project provenance, and verify every role points to the fixed source or an explicit independent derivation.
- [x] **Step 2: Run the formal four-edition build.** Use `build_projects.py` for `gk-1997-regular-national-science` with the repository's standard xelatex engine and current input checks; require four PDFs and capture the exact compiler commands and hashes in `receipts/build.json`.
- [x] **Step 3: Remove compilation intermediates immediately.** Delete only the exact generated `.aux`, `.fls`, `.log`, `.out`, `.toc`, `.synctex.gz`, `.fdb_latexmk`, `.bcf`, `.run.xml`, `.nav`, `.snm`, `.vrb`, `.idx`, `.ilg`, `.ind`, `.lof`, `.lot`, `.pyc`, `.pyo`, `.swp`, `.swo`, and `.bak` files and any `.work` directory; retain four PDFs and all `.tex` source.
- [x] **Step 4: Validate receipts and source freshness.** Run `build_projects.py validate-receipts --manifest ... --paper ... --require-final --require-current-inputs --json`, `provenance.py check-all ...`, and `source_manifest.py validate --manifest ...`; do not proceed if any receipt is stale or any role is missing.
- [x] **Step 5: Commit the build checkpoint.** Inspect the build tree and receipt diff, then commit with `chore(exams): record 1997 national science build`.

### Task 4: 四版视觉复核并关闭批次

**Files:**
- Create by tool: `math-gaokao-latex/1997_全国卷_理科/receipts/review.json`
- Create: `math-gaokao-latex/reports/phase2-b70.md`
- Modify by tool: `math-gaokao-latex/source-manifest.json`, `math-gaokao-latex/manifest.csv`

**Interfaces:**
- Consumes: four current PDFs and build/provenance receipts from Task 3.
- Produces: page-by-page visual review with explicit figure/overflow checks, a `closed` or evidence-backed `closed_with_blockers` batch, and synchronized manifest/report outputs.

- [x] **Step 1: Render PDFs outside the repository.** Render all pages to a fresh `/private/tmp` directory, create contact sheets when useful, and use visual inspection to check text clipping, formula wrapping, page order, all figures, answer markers, and the print version; never add rendered PNGs to Git.
- [x] **Step 2: Repair only source-backed defects.** If a layout defect is found, edit the Markdown or `.tex` figure source, regenerate and rebuild the affected project, remove intermediates, and repeat the receipt freshness check. If a content ambiguity is found, add a new issue with source evidence and leave the literal source unchanged.
- [x] **Step 3: Prepare and finalize review.** Run the repository's review receipt preparation command with four current PDF hashes, inspect the generated per-edition notes, then finalize `phase2-b70` only after every page and edition has a review decision.
- [x] **Step 4: Refresh CSV and report.** Run `manifest_csv.py --manifest ... --output ... --check` after generation, confirm the new paper is `complete` if all questions are resolved, and write the phase2-b70 report with source, build, review and blocker facts.
- [x] **Step 5: Commit the reviewed batch.** Run `git diff --check`, inspect all report and manifest changes, then commit with `docs(exams): finalize 1997 national science review`.

### Task 5: 全局门禁与清理交付

**Files:**
- Verify: `math-gaokao-latex/README.md`, `math-gaokao-latex/source-manifest.json`, `math-gaokao-latex/manifest.csv`, all project `build/` directories
- Modify only if generated by the existing report tool: report/index/CSV outputs

**Interfaces:**
- Consumes: all committed checkpoints from Tasks 1–4.
- Produces: a clean branch whose new batch is current and whose build trees contain PDFs plus source only.

- [x] **Step 1: Run targeted gates.** Validate issues, source manifest, project generation, short answers, provenance, build receipts, review receipts, and `report.py check`; run `git diff --check`.
- [x] **Step 2: Run the full unit suite.** Execute `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s math-gaokao-latex/tests -p 'test_*.py'` and require an `OK` result; do not stage any bytecode created by unrelated commands.
- [x] **Step 3: Assert artifact policy.** Count PDFs and `.tex` files, assert no image suffix occurs under the LaTeX corpus, assert no compiler-intermediate suffix occurs anywhere under project `build/` directories, and assert each build directory has exactly four PDFs.
- [x] **Step 4: Review final Git state and commit.** Confirm the main worktree is untouched, the phase worktree is clean, no source PDF or rendered image is staged, and the branch has not been pushed; record the final commit IDs and unresolved issue count in the handoff.

## Self-Review Checklist

- [x] The source PDF fingerprint, page count, 25-question structure, and no-answer-page caveat are present.
- [x] Every source Markdown file is complete, synchronized, and free of raster image dependencies.
- [x] All independent calculations are checked against the fixed题面; known secondary-source errors are not silently copied.
- [x] The new source is bound exactly once to one paper and one batch.
- [x] Four PDFs compile from current `.tex` sources and survive visual review.
- [x] No compiler intermediates, `.work` directories, or images are in the branch delta.
- [x] Global gates and the full test suite pass before any completion claim.

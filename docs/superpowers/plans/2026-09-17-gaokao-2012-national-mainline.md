# 2012 National Mainline Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** 将 2012 年四套全国主线数学固定源整理为可复用、可打印、带逐题 provenance 与视觉复核证据的 LaTeX 题库项目：大纲卷文/理、新课标卷文/理。

**Architecture:** 沿用 source-manifest.json 驱动的规范 Markdown → 共享 questions.tex/answers.tex/answers_short.tex → 四个入口壳 → 本地 PDF 的单向生成链。四卷的题面、答案和解析写入 2012/，图形只写入各自项目的 TikZ/PGFPlots .tex；公共工具、manifest 结构和既有批次不改写。

**Tech Stack:** Markdown、Python 3 工具链、XeLaTeX、TikZ/PGFPlots、Poppler、Git。


## Global Constraints

- 固定批次使用工具允许的两位编号 phase2-b01；只登记下表四个 source ID，不混入 2012 省市自主命题卷。
- 固定源 PDF 只从本机 gaokaomath-src/普通高考/2012/读取；PDF、渲染 PNG、.work 和编译中间物不入库。
- 题面必须逐页回到固定源核对；固定源不含答案/解析的内容由独立复算产生，禁止凭记忆补题。
- 图形只提交项目内 .tex 矢量源；不得创建或提交 PNG/JPEG/SVG。
- 每卷规范源固定为 _试题.md、_答案要点.md、_解析正文.md、_含解析.md；生成源固定为共享 questions.tex、answers.tex、answers_short.tex 与四个入口。
- build 目录验收后只保留 PDF；所有缺字、未解析引用、真实 Overfull、源/答案冲突都必须修复或进入 issues，不得用状态字段掩盖。
- 所有提交留在本地分支，不 push。

## Fixed Sources

| 试卷 | paper_id | source_id | SHA-256 | 固定源 PDF / 印刷页 | 题数 |
|---|---|---|---|---|---:|
| 全国大纲文 | gk-2012-regular-national-outline-arts | src-5299eb7ef7bee444aa4edbee1bbd1748341b14a6893cd55e8d0c080e1d8c7e67 | 1a88dbed6fd866a13e245da659bb4a548cfa28977cdb481cf6277f1c1c96e3b2 | 2012大纲文(贵州,甘肃,青海,西藏,广西).pdf / 727–728 | 22 |
| 全国大纲理 | gk-2012-regular-national-outline-science | src-7f0b0f1da8f8f1cd330807f110972306ef01c21820e35933f4df5d306d608929 | 977d5ecc3b90904f7b2ba261a69e1a7fea6555ac99c635e360a0f697a3095f9e | 2012大纲理(贵州,甘肃,青海,西藏,广西).pdf / 725–726 | 22 |
| 全国新课标文 | gk-2012-regular-national-new-arts | src-1e893321c125a4047faba9e05f07f1219baeba5560e1bea87da3430b980d387b | 980bad4bf2039fede24830cfc0e5ebd1509b464ac44cfb7630afd96fbcdd4f34 | 2012新课标文(河南,河北,黑龙江,吉林,海南,宁夏,山西,内蒙古,新疆,云南).pdf / 757–758 | 24 |
| 全国新课标理 | gk-2012-regular-national-new-science | src-c50982d6ca581a74ba9bb6fb2d0e0c920874448499d6ce22f90e699c77c8d568 | 040e174f2b685474065fdc6074059a510fe66c5458c86faf8e3b52ac8c1333c2 | 2012新课标理(河南,河北,黑龙江,吉林,海南,宁夏,山西,内蒙古,新疆,云南).pdf / 755–756 | 24 |

## Tasks

### Task 1 — Freeze the source table and register phase2-b01

**Files:**

- Create: docs/superpowers/plans/2026-09-17-gaokao-2012-national-mainline.md
- Create: math-gaokao-latex/.work/phase2-b01/register.json (ignored)
- Modify by tool: math-gaokao-latex/source-manifest.json

- [x] Verify all four source IDs, SHA-256 values, PDF page counts, printed page ranges and raw paths against the fixed-source table above.
- [x] Use project directories 2012_全国大纲卷_文科, 2012_全国大纲卷_理科, 2012_全国卷_文科, 2012_全国卷_理科; use canonical Markdown prefixes 2012_数学真题_全国大纲文, 2012_数学真题_全国大纲理, 2012_数学真题_全国新课标文, 2012_数学真题_全国新课标理.
- [x] Register structures 选择题 1–12 / 填空题 13–16 / 解答题 17–22 for both outline papers and 解答题 17–24 for both new-curriculum papers.
- [x] Freeze these expected vector figure families after source inspection: outline arts q19 pyramid; outline science q18 pyramid; new arts q6 flowchart, q7 grid/three-view, q22 cyclic-geometry diagram; new science q6 flowchart, q7 grid/three-view, q10 graph options, q15 circuit, q19 prism, q22 cyclic-geometry diagram.
- [x] Run source_manifest.py register-papers dry-run, then --write exactly once after all four canonical source triples exist.

### Task 2 — Transcribe the four fixed source question papers

**Files:**

- Create: 2012/2012_数学真题_全国大纲文_试题.md
- Create: 2012/2012_数学真题_全国大纲理_试题.md
- Create: 2012/2012_数学真题_全国新课标文_试题.md
- Create: 2012/2012_数学真题_全国新课标理_试题.md

- [x] Each paper must contain frontmatter with source ID, raw path, printed pages, track, question count and the statement that answers/solutions are independently reconstructed.
- [x] Transcribe every question, option, formula, table, unit and sub-question from the fixed PDF; preserve the source page break facts and use logical image markers only.
- [x] Run solution_sources.parse_question_blocks for counts 22/22/24/24 and independently compare the four texts against rendered source pages.

### Task 3 — Reconcile answers and independent solutions

**Files:**

- Create the four _答案要点.md files under 2012/.
- Create the four _解析正文.md files under 2012/.
- Create the four generated _含解析.md files through solution_sources.py.

- [x] Recompute every answer, including all probability/statistics, sequences, spatial geometry, analytic geometry, calculus and parameter-range parts; preserve multiple valid branches when the equation permits them.
- [x] Keep every answer key and solution block structurally aligned with its question block; run extract-batch --write and check-batch for phase2-b01.
- [x] Any unreadable glyph, source ambiguity or disagreement must receive an issue entry with source/page/question evidence; do not silently normalize it.

### Task 4 — Produce only vector figure sources

**Files:**

- Create only the project-local figures/*.tex files for the frozen figure families in Task 1.

- [x] Redraw each source figure with TikZ/PGFPlots, including source labels, solid/dashed line semantics, axes/grid and option separation where present.
- [x] Check every logical Markdown image marker maps one-to-one to a registered .tex path with expected occurrence count 2 (question and combined source).
- [x] Confirm no image suffix is created under the four 2012 projects.

### Task 5 — Generate shared LaTeX and four shells

**Files:**

- Modify by tools: four 2012 project directories under math-gaokao-latex/.

- [x] Run generate_projects.py --batch phase2-b01 --write, make_short_answers.py --batch phase2-b01 --write, and make_editions.py --batch phase2-b01 --write.
- [x] Run all corresponding --check commands; assert that question counts, answer blocks, figure mappings and shell/template hashes are current.

### Task 6 — Import provenance and compile

**Files:**

- Create by tools: four project provenance.json, four receipts/build.json, ignored .work/phase2-b01/provenance/.

- [x] Initialize question-review, answer-solve and answer-review role files; fill source page/hash and independently recomputed answer hash for every question.
- [x] Dry-run and write provenance.py import-batch, then run check-batch.
- [x] Run formal build for 16 PDFs; require zero build errors, missing glyphs, undefined references and real Overfull diagnostics.

### Task 7 — Review every generated page

**Files:**

- Create by tools: four project receipts/review.json and reports/phase2-b01.md.

- [x] Render all pages outside the repository; visually inspect question, solution, short-answer and print editions for glyphs, heading/option alignment, vector figures, header/footer, pagination, readable size and answer leakage.
- [x] Record any Underfull warning only as a page-specific visual exemption with source file and reason; do not hide a real overflow.
- [x] Run review_receipts.py finalize-batch-checked; require batch status closed or an evidence-backed closed_with_blockers.

### Task 8 — Clean, verify and commit

- [x] Delete .work/phase2-b01, temporary render directories and all build files except PDF.
- [ ] Run source manifest, solution, generation, short-answer, edition, provenance, build, review, CSV and full unit-test gates. The full suite ran 810 tests with 2 environment/fixture cleanup errors; the 7 affected tests reran independently and passed.
- [x] Commit source/generation checkpoint and final receipts/report separately; do not push.

## Acceptance criteria

- phase2-b01 contains exactly the four fixed source IDs above and no provincial paper.
- Four question counts and structures pass parser and manifest gates; all figures are project-local vector .tex.
- Sixteen PDFs compile with current receipts; no missing files, undefined references, missing glyphs or real Overfull warnings.
- Provenance, review receipts, manifest.csv, report and current input hashes are synchronized.
- After cleanup, 2012 build directories contain PDFs only, no raster image is added, and the worktree is clean.

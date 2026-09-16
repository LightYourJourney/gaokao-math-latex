# 2010 National Mainline Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 2010 年六套全国主线数学固定源整理为可复用、可打印、带来源与视觉审查证据的 LaTeX 题库项目。

**Architecture:** 沿用 `source-manifest.json` 驱动的来源链：固定 PDF 已存在于本地上游仓库，题面/答案/解析保存在 `2010/`，生成器输出每卷唯一的 `questions.tex`、`answers.tex` 与四个版本壳。图形只用项目目录下的 TikZ/PGFPlots `.tex` 源，PDF 只作为本地构建产物。

**Tech Stack:** Markdown、Python 3.12 工具链、XeLaTeX、TikZ/PGFPlots、Poppler、Git。

**Spec:** `docs/AGENTS.md`、仓库根 `CLAUDE.md`、总体项目目标及本计划中的固定源表。

## Global Constraints

- 固定批次：`phase2-b99`；本批只处理 2010 大纲卷Ⅰ/Ⅱ文理和 2010 新课标文理六套，不把省市自主命题卷混入本批。
- 固定源目录：`gaokaomath-src/普通高考/2010/`；登记后 manifest 的 `source_id`、SHA-256、PDF 页码是唯一来源身份。
- 题面按固定源转录；答案/解析独立复算。任何源面矛盾、答案缺失或题意不确定必须登记到 `missing-issues.md`，不能凭记忆补写。
- 不向仓库添加 PNG/JPEG 等光栅图；图形使用项目内 `.tex` 矢量源。构建中间物、`.work`、临时渲染目录在验收后删除。
- 每卷保留共享 `questions.tex`、`answers.tex`、`answers_short.tex`、四个入口 `.tex`、`provenance.json`、build/review receipts；`build/` 最终只保留 PDF。
- 批次若仍有开放阻断问题，状态必须为 `closed_with_blockers`；已解决的问题保留历史记录但不得继续阻断完成态。

## Fixed Sources

| 试卷 | paper_id | source_id | SHA-256 | PDF 页数 / 印刷页 | 题数 |
|---|---|---|---|---:|---:|
| 大纲卷Ⅰ文 | `gk-2010-regular-national-1-arts` | `src-56d1ac4b10f7cc5d9455d9e2fd999fc310fdeed852521b697e7f2c9916d03930` | `90f3508d08f6390c13b1a020878ad2343daa590a9ac181fb6012f104662776f8` | 2 / 583–584 | 22 |
| 大纲卷Ⅰ理 | `gk-2010-regular-national-1-science` | `src-64614b86c4539695192493bb574fe06e19a9ec1796bf06cd5c275c2b4b33743f` | `854001f5a5a2dddfdf67fa957fc35f7b1b74e49d2e58686fca3f25695ac2fe42` | 2 / 581–582 | 22 |
| 大纲卷Ⅱ文 | `gk-2010-regular-national-2-arts` | `src-cbfddcaeed484f5bf141e5db16395e77131fae9c246170bf2032cd010e25c20b` | `7fcee1d755e27dd0a8a7984526c0364f4d8aaa7d790d0f4ceb391fee2141121d` | 2 / 587–588 | 22 |
| 大纲卷Ⅱ理 | `gk-2010-regular-national-2-science` | `src-0b4cb75e913f09f221123cdca016be43c92305aa4ca9f9c56c0b373fe175277a` | `b4014087b086d6d5ae6c782e62a4938c325065d759b5965b6505aad29c5cf820` | 2 / 585–586 | 22 |
| 新课标文 | `gk-2010-regular-national-new-arts` | `src-59d0e74e47d730afb1ab9677986b8105df7180a17d0c30498d06ca6c979c54be` | `fd78eb5083bf7eaab7532e196a3fccb97d441e9e2ec2452eee8816557d0db49d` | 2 / 617–618 | 24 |
| 新课标理 | `gk-2010-regular-national-new-science` | `src-c09227c8a0c0c36f290807ae99a86a7ceed0957b62835a6d87717a7f9bb8772e` | `79c5ba2f688ea737ef9298a6b08f3b8b3e29c2bb23983e61328c9c1882a80836` | 2 / 615–616 | 24 |

题面页码映射先按固定源版式登记为第 1–19 题对应 PDF 第 1 页、第 20 题起对应 PDF 第 2 页；新课标卷按其 17/18 题在第 1 页、19 题起在第 2 页的实际排版复核并在 provenance 中逐题记录。

## Tasks

- [ ] **Task 1 — Materialize the six source triples and register `phase2-b99`.**
  - Create six `_试题.md` files, six `_答案要点.md` files, six `_解析正文.md` files and six generated `_含解析.md` files under `2010/`.
  - Use these canonical prefixes: `2010_数学真题_全国1文`、`全国1理`、`全国2文`、`全国2理`、`全国新课标文`、`全国新课标理`.
  - Create one registration spec under `math-gaokao-latex/.work/phase2-b99/register.json`; include exact source IDs, project directories, question counts, structures and figure paths. Run `register-papers --write` once only after every canonical Markdown file exists.

- [ ] **Task 2 — Transcribe and structurally validate all six question papers.**
  - 大纲Ⅰ/Ⅱ文理 use structure `选择题 1–12 / 填空题 13–16 / 解答题 17–22`.
  - 新课标文理 use structure `选择题 1–12 / 填空题 13–16 / 解答题 17–24`.
  - Render both fixed source pages for every PDF, preserve every formula, option, unit, subquestion and figure marker, and run the question parser before registration.

- [ ] **Task 3 — Independently solve and reconcile all answers.**
  - Recompute algebra, probability/statistics, sequences, geometry, calculus and coordinate problems from the transcribed question text.
  - Keep final conclusions in `_解析正文.md` byte-aligned with `_答案要点.md`; record source/answer disagreements in `missing-issues.md` with paper/question/source fingerprints.
  - Run `solution_sources.py extract-batch --write` and `check-batch` for `phase2-b99` before generating LaTeX.

- [ ] **Task 4 — Create only vector figure sources.**
  - Expected figure families are: 大纲Ⅰ文 q20 pyramid; 大纲Ⅰ理 q19 pyramid; 大纲Ⅱ文/理 q19 prism and q20 circuit; 新课标文 q6 motion graph, q8 flowchart, q18 pyramid, q20 ellipse, q22 circle, q23 parametric circle and q24 absolute-value graph; 新课标理 q4 motion graph, q7 flowchart, q18 pyramid, q20 ellipse, q22 circle, q23 parametric circle and q24 absolute-value graph.
  - Name files as `f2010_<paper-key>_t<number>_<short-name>.tex`; validate every Markdown figure marker resolves locally and no PNG/JPEG is created in the project tree.

- [ ] **Task 5 — Generate and check shared LaTeX plus all edition shells.**
  - Run `generate_projects.py`, `make_short_answers.py` and `make_editions.py` for `phase2-b99`, then run their `--check` commands.
  - Confirm each project has one shared question file, one shared answer file, one short-answer file and four shells with no duplicated hand-maintained content.

- [ ] **Task 6 — Import provenance and perform the formal build.**
  - Initialize three roles per paper under `.work/phase2-b99`, attach source IDs/SHA/page evidence and mark unresolved answer/transcription cases with current blocking issues.
  - Dry-run and write `provenance.py import-batch`; build six papers × four editions with `build_projects.py build --formal --json`.

- [ ] **Task 7 — Review every generated page and finalize.**
  - Prepare 24 review work items, render every current PDF page with Poppler, inspect contact sheets and high-risk figure/answer pages, fill all eight checks, and run `finalize-batch-checked`.
  - Preserve `closed_with_blockers` if the issue ledger still contains open blockers; write `reports/phase2-b99.md`.

- [ ] **Task 8 — Clean, verify and commit without pushing.**
  - Delete non-PDF/non-`.tex` files from every 2010 build directory, remove `.work/phase2-b99` and temporary renders, and ensure no new raster files exist.
  - Run source, CSV, solution, generation, short-answer, editions, provenance, build, review and report gates plus the full unittest suite.
  - Commit source checkpoint, final receipts/report and this plan separately; do not push.

## Acceptance Criteria

- `phase2-b99` contains exactly the six fixed source IDs listed above and no provincial paper.
- Six source triples parse with question counts 22/22/22/22/24/24 and the declared structures.
- Every figure marker resolves to a project-local `.tex` source and no new PNG/JPEG is tracked.
- 24 PDFs compile with current receipts, no unresolved references, missing glyphs or unaccepted warnings; every page review passes.
- Provenance, manifest CSV, six global reports and full tests are current; any open issue is visible in `missing-issues.md` and reflected in batch status.
- After cleanup, each 2010 build directory contains PDFs only, `.work/phase2-b99` is absent, and the working tree is clean.

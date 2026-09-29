# 2017 北京、天津卷文理科 Implementation Plan

> **For agentic workers:** 使用 `superpowers:dispatching-parallel-agents` 分派互不重叠的逐卷任务；最多 3 个内容代理同时工作。每卷题面复核者、答案盲核者必须与对应转录者/求解者不同。主代理独占清单登记、规范内容整合、生成、回执和提交。

**Goal:** 将固定上游中的 2017 北京卷、天津卷文理科四套数学试卷整理为可追溯、可编译、可复核的四版本 LaTeX 项目。

**Architecture:** 以 `source-manifest.json` 中固定 `source_id` 为身份根，四套题面的规范 Markdown 放在 `2017/`，生成器产出共享 LaTeX、简答版和四个独立入口。逐卷转录/求解草稿只写隔离工作树内忽略目录；异人盲核后由主代理整合。图稿仅保留 TikZ/PGFPlots `.tex`，来源 PDF、页面渲染图和编译中间件不入库。

**Tech Stack:** Markdown、Python 3 标准库工具、XeLaTeX、TikZ/PGFPlots、Git、Poppler（`pdfinfo` / `pdftotext` / `pdftoppm`）。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库根目录 `CLAUDE.md`。

## Global Constraints

- 固定批次：`phase2-b08`；只处理本计划列出的 2017 北京、天津文理科四套，不改公共生成器、模板、宏或其他批次。
- 上游固定 commit：`34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；`source_id`、SHA-256、blob OID 和路径以本表及当前 `source-manifest.json` 为准。
- 四份源 PDF 均为两页 A3，页面已确认分别覆盖印刷页码表中所列两页；题目共 20 题/卷的预检结果必须在转录时逐题复核，不得为匹配预期补题、改题或忽略非题目说明。
- PDF 未附答案；答案由独立求解与不同角色盲核支持等级 D，无法收敛的题标 U 并列入问题总账，不得伪称官方答案。
- 草稿只写隔离工作树中的 `math-gaokao-latex/.work/phase2-b08/<paper_id>/`。代理开始写入前必须核对 `git rev-parse --show-toplevel` 指向 `仓库根`；严禁将草稿写进主检出 `主工作树/.work/`。
- 题面必须逐页视觉对照 PDF。OCR/文本层只用于初稿；题号、选择顺序、文理差异、限定词、计分说明、原卷编号和印刷页码忠实保留。
- 图稿只用项目 `figures/*.tex` 中的 TikZ/PGFPlots 源；不得将 PDF、页面裁图、PNG/JPEG、截图或 OCR 中间图加入 Git。不要删除主检出或其他会话遗留的 `.work/`、`/tmp` 文件；只清理本计划在当前工作树/独立临时目录中新建且已核实归属的渲染物。
- 四卷各构建试题、解析、简答、印刷四版；忽略的 `build/` 每卷只留四份最终 PDF，编译中间件与本批渲染图清除。
- 不暂存或提交无关更改，不触碰上游目录中的未跟踪文件；本批不 push。

## File Structure and Responsibilities

- 通过项目工具修改：`math-gaokao-latex/source-manifest.json`、`index.json`、`manifest.csv`、`missing-issues.md`。
- 创建四组规范 Markdown：
  - `2017/2017_数学真题_北京文_{试题,答案要点,解析正文}.md`
  - `2017/2017_数学真题_北京理_{试题,答案要点,解析正文}.md`
  - `2017/2017_数学真题_天津文_{试题,答案要点,解析正文}.md`
  - `2017/2017_数学真题_天津理_{试题,答案要点,解析正文}.md`
- 由生成器产生对应四份 `_含解析.md`、四个项目目录中的共享题目/答案/来源文件及四版本入口。
- 项目目录分别为 `2017_北京卷_文科`、`2017_北京卷_理科`、`2017_天津卷_文科`、`2017_天津卷_理科`；只保留来源确认需要的 `figures/*.tex`。
- 创建 `math-gaokao-latex/reports/phase2-b08.md` 并更新本计划完成记录。
- 不修改 `common/`、模板或共享生成器。若发现公共缺陷，记录复现证据并另行立项。

## Fixed Sources

| 试卷 | 拟定 `paper_id` | 项目目录 | `source_id` | SHA-256 | Git blob OID | 上游相对路径 | PDF 页 / 印刷页 |
|---|---|---|---|---|---|---|---|
| 北京卷文科 | `gk-2017-regular-beijing-arts` | `2017_北京卷_文科` | `src-368b4a2cfb95e6a5feab0582f9a69651d69cfee116ee91eda6672e869906542d` | `91a3f2029d2e705d52c435f109f8cd5742d5ffa8ae4b2fdfa5fcff62c8f2d135` | `de7c5b10cd87b7136c64068ad2d3f3cfac926020` | `普通高考/2017/2017北京文.pdf` | 1→1033；2→1034 |
| 北京卷理科 | `gk-2017-regular-beijing-science` | `2017_北京卷_理科` | `src-b12d0ac9ff61fb686257e6f40f4e0f8b48903d715f411f1ef2c5bf5efb88aec2` | `d2fb456023eb068a6e489e62150d6e8b02b8fc1a3ee6c5a64d372045e731ec70` | `001f2fcc11bfe0ae2cf366d8efcf7d04a22ef3db` | `普通高考/2017/2017北京理.pdf` | 1→1031；2→1032 |
| 天津卷文科 | `gk-2017-regular-tianjin-arts` | `2017_天津卷_文科` | `src-af3f095940b31948670126c944affe8cfc461d99f7ee362a36ac314b08ed2ef0` | `65540c5d5dbdc4076cc9d202d2fa4d2a0750d64c2798248813b195ace5edccdb` | `d074a96c4d4541a8b586b991e5097adb39dbb3d3` | `普通高考/2017/2017天津文.pdf` | 1→1057；2→1058 |
| 天津卷理科 | `gk-2017-regular-tianjin-science` | `2017_天津卷_理科` | `src-59000d9a683992059d4ab4804d370738dd2efd09e37ecfa36d726310ff84cfec` | `6d3a6679c32f145316d7316567f220974d102e274cae6a7e93b74543097ee527` | `d43362e88dacda4a49815fa755294f0b64327755` | `普通高考/2017/2017天津理.pdf` | 1→1055；2→1056 |

只读来源预检于 2026-09-29 完成：上游 HEAD 与固定 commit 一致；manifest 校验通过；四条来源均为 `ready` 且尚未绑定；重新计算的 SHA-256/blob OID 与清单相同；四份 PDF 均为两页 A3。页面渲染确认内页标题、地区、文理科及页码映射。2026-09-29 的只读冲突检查还确认四个拟定 `paper_id`、四个项目目录、`phase2-b08` 批次、批次 scratch 路径和报告路径均空闲；四个来源 ID 在总账中各出现一次。正式登记前仍须重新校验源哈希/页数及冲突状态；若来源状态发生变化，停止并更新计划，不得强行登记。

## Review Focus

- 北京卷与天津卷题型、题号或常见题目相似，不可据相似记忆复制题干、数据、选项、图形或解答；每题均按固定来源逐页核对。
- 两页 A3 多栏阅读顺序须从渲染页确认；页码映射覆盖全部题目，跨栏、跨页不得漏题、重复或错序。
- 程序框图、统计图、函数图象、空间几何图中的点名、方向、刻度和虚实线必须由 PDF 证实；看不清则登记问题，不按数学常识补画。
- 上下标、根式范围、分式层级、集合、向量和参数限定易被文本抽取漏掉；复杂公式逐题回看页面渲染。
- 原 PDF 无答案；求解者与盲核者必须分离。无法独立收敛则保留 U/blocked，不以多数网站答案或代理自述替代证据。

## Tasks

### Task 1 — Reconfirm and freeze four source artifacts

**Files:**
- Read: `math-gaokao-latex/source-manifest.json`
- Read: four fixed PDFs under `gaokaomath-src/普通高考/2017/`
- Draft audit, ignored: `math-gaokao-latex/.work/phase2-b08/source-audit.json`

- [x] Validate the source manifest; confirm upstream HEAD is `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`.
- [x] Recompute each PDF SHA-256, page count and Git blob OID; compare with the fixed-source table.
- [x] Render both pages of every PDF; record visible title and page-to-printed-page mapping.
- [x] Recheck four source IDs, proposed paper IDs/directories, and `phase2-b08` are collision-free; preserve all pre-existing ignored files. Repeat the check immediately before registration.

**Expected:** Exactly four matching source artifacts and eight accounted pages; mismatch or ambiguous scan stops registration.

### Task 2 — Transcribe question sets and prepare independent solution drafts

**Files:**
- Draft only: `.work/phase2-b08/<paper_id>/questions.md`, `page-map.md`, `answer-solve.md`, figure inventory.
- Canonical outputs after reconciliation: four `_试题.md` files in `2017/`.

- [x] Assign one paper to each transcription/solver role; work in waves so no more than three content agents are active.
- [x] Transcribe all questions and printed instructions, options, subparts, scoring notes and diagrams; preserve source order and wording.
- [x] Record each question's PDF page, printed page, type, figure reference and uncertain glyph/geometry; visually verify the 20-question preflight count rather than assuming it.
- [x] Derive answers from the transcribed conditions without presenting them as official; preserve derivations and uncertainty in isolated drafts.

**Expected:** Four source-complete drafts with page maps and figure inventories; no question is inferred from another regional/track version.

### Task 3 — Blind-check questions and answers with different roles

**Files:**
- Draft evidence, isolated from producer drafts: `.work/phase2-b08/reviews/<paper_id>/{answers-blind.md,question-review.json,answer-review.json,discrepancy-matrix.md}`.

- [x] Assign separate question-source reviewers and answer-blind reviewers per paper; both must be distinct from the answer solver. The provenance schema requires three pairwise-distinct role identities (`question-review`, `answer-solve`, `answer-review`), so one reviewer cannot fill both review roles for the same paper. Do not expose the first solver's final answer before the answer-blind record is saved and hashed.
- [x] Compare every question with rendered source, including choices, symbols, boundaries, diagrams and printed-page mapping.
- [x] Re-solve disagreements from source conditions; retain unresolved outcomes as U and create issue entries.
- [x] Main agent maintains the cross-paper anchor matrix and accepts/rejects evidence; agent self-reports alone are not acceptance evidence.

**Expected:** Every question has separately assigned transcription/question-review and answer-solve/answer-review roles; discrepancies are evidence-backed or explicitly blocked.

### Task 4 — Integrate canonical Markdown, figures and registration inputs

**Files:**
- Create the four `2017_数学真题_{北京文,北京理,天津文,天津理}_{试题,答案要点,解析正文}.md` canonical sets in `2017/`.
- Generate four `_含解析.md` files from canonical sources.
- Create confirmed vector figure sources under each project's `figures/*.tex`.
- Ignored draft: `.work/phase2-b08/register.json` and provenance role records.

- [x] Reconcile blind-review findings into canonical question files; do not copy between papers on the basis of matching numbers/topics.
- [x] Write aligned answers and detailed solutions; mark independently derived answers D only when distinct blind review supports them, otherwise U.
- [x] Create project-local TikZ/PGFPlots sources only for source-confirmed diagrams; use no raster page images or absolute paths.
- [x] Generate `_含解析.md` with `solution_sources.render_combined()`; verify IDs, titles, tracks, aliases, counts, and source mappings.
- [x] Run registration dry-run and inspect the exact diff; only zero-conflict dry-run permits one `register-papers --write` transaction for `phase2-b08`.

**Expected:** Four canonical question/answer/solution sets, four exact source-to-paper bindings, and consistent generated Markdown/manifest projections.

### Task 5 — Generate projects, build editions and complete visual review

**Files:**
- Generate four project directories, receipts, and `reports/phase2-b08.md`.

- [x] Import question and answer provenance from isolated role evidence; reject stale hashes and incorrect role claims.
- [x] Run project, short-answer and edition generators with `--write --batch phase2-b08`, then rerun with `--check`.
- [x] Check question/answer counts, numbering, figure registration/reference counts, edition input matrix and generator no-drift.
- [x] Build all 16 editions with `python3 tools/build_projects.py build --formal --batch phase2-b08 --json`; require no TeX errors, missing glyphs, unresolved references or unreviewed Overfull warnings.
- [x] Render and visually inspect each required page class for all four papers/editions; prepare page-level receipts against current build hashes.
- [x] Compare short answers with detailed solution conclusions; finalize only states supported by provenance, issues, build and review gates.

**Expected:** Sixteen current build targets and page-level visual decisions; unresolved U issues remain visible and prevent a `complete` state.

### Task 6 — Refresh reports, verify, clean and commit this batch

**Files:**
- Modify through supported project tools: `manifest.csv`, reports and manifest/report projections.
- Create/update: `reports/phase2-b08.md` and this plan's completion record.

- [x] Run source-manifest, CSV, source-generation, solution-consistency, project-generation, short-answer, edition, provenance, build, review and global report checks; finish with `python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md`.
- [x] Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` and `git diff --check`; inspect exact batch-only status and staged diff.
- [x] Clean only this batch's generated temporary renders and build intermediates, retaining four final PDFs per paper in ignored `build/`; leave unrelated main-checkout and pre-existing temp files untouched.
- [x] Commit the verified content stage and final receipts/reports as separate commits when each is complete; stage exact paths, do not use `git add .`, and do not push.

**Expected:** Batch report/global state match machine-derived evidence; no batch scratch outside ignored `.work/`, and commits contain only this batch's approved deliverables.

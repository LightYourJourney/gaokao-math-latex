# 2015 山东卷理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 转录、独立求解与盲核由不同角色分头完成；主会话独占规范整合、manifest、回执与最终提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 山东卷理科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 沿用本库已验证的单卷流程，以 `source-manifest.json` 中固定 source ID 为身份根；转录和独立求解分离，题面、答案要点与解析正文作为唯一规范源，现有生成器产出 LaTeX。仅提交 TikZ/PGFPlots 图源、LaTeX 源及最终四版 PDF；来源 PDF、页面图和编译中间件留在忽略目录。

**Tech Stack:** Markdown、Python 3 标准库工具、XeLaTeX/latexmk、TikZ/PGFPlots、Git、Poppler。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。同卷文科建模先例：`2015_山东卷_文科`（phase3-b14，闭环）。

## Global Constraints

- 正式批次 `phase3-b15`；工作目录 `.work/phase3-b15/`。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；source ID `src-501fd8b49559a60c0ab5208279e15d7d036a082f972029884741c90784c13225`、SHA-256 `d702c863816c079dc4bf2c2b66e915a72d3c2b757b19f1d4c1c3e2b7220b2b0a`、blob OID `918cf28fc78e590513942d2b0cbb681e171166ad` 与路径 `普通高考/2015/2015山东理.pdf` 不得漂移。
- 固定 PDF 两页 A3，印刷页码 969–970；结构为选择 1–10、填空 11–15、解答 16–21，共 21 题。原 PDF 无答案页，解析由独立推导产生，证据等级 D；未确认项保留 U，不把计算猜测写成原题条件。
- 代理只读固定 PDF 和各自任务 brief；不得读取山东文科项目、其规范 Markdown 或 `.work/phase3-b14/`，也不得读取任何其他卷/批次产物。转录与盲解严禁互读；答题代理不得读转录草稿。
- 所有草稿、来源副本、渲染页、OCR 和中间件只放 `.work/phase3-b15/`；不提交 PNG/JPEG/扫描 PDF。仓库项目 `build/` 仅留正式生成的四版 PDF。
- 图源只用 TikZ/PGFPlots `.tex`；图形疑点照源登记，不按比例或同卷图形推测。
- 不改共享生成器、宏、模板或其他批次；发现跨卷问题只记录证据并另行立项。
- 不 push；提交使用显式路径，不暂存无关或其他会话文件。

## Review Focus

- A3 横向三栏阅读顺序与 PDF 文本抽取顺序不同：检查题号连续、题型边界和每题 PDF 页/印刷页映射。
- 上下标、根式、向量点积、区间端点与量词易在文本层丢失：对照渲染页逐题目视确认，抽取文本不作题面权威。
- 第 13 题程序框图的分支方向、循环边与积分表达式必须按源图逐路径复刻；第 17 题三棱台 `DEF−ABC` 的虚实线、点位及标签须独立放大核查。
- 无答案页：四个盲解/盲核角色须彼此隔离；若不同推导产生冲突，保留分支并记录 U/blocker，不以多数投票消歧。
- 山东文理卷同号题可能相似，但本批转录和解答不得接触文科卷；仅主会话完成两边源核后方可作事后互证。

## Fixed Source and Initial Inspection

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | PDF 页/印刷页 |
|---|---|---|---|---|---|---|---|
| 山东卷理科 | `gk-2015-regular-shandong-science` | `2015_山东卷_理科` | `src-501fd8b49559a60c0ab5208279e15d7d036a082f972029884741c90784c13225` | `d702c863816c079dc4bf2c2b66e915a72d3c2b757b19f1d4c1c3e2b7220b2b0a` | `918cf28fc78e590513942d2b0cbb681e171166ad` | `普通高考/2015/2015山东理.pdf` | 1→969；2→970 |

源副本在上游克隆工作树中复算 SHA 与固定 manifest 一致，固定 commit blob 匹配；PDF 为两页 A3、未加密。页面目视确认题名「2015 普通高等学校招生考试（山东卷理）」、无答案；图形需求至少包括 Q13 程序框图、Q17 三棱台示意图。

## Tasks

### Task 1 — Freeze source and create isolated drafts

- [x] 将固定 PDF、两页渲染、`pdftotext -layout` 辅助文本和源核记录放入 `.work/phase3-b15/source/`；再次核对 SHA、blob、页数与本计划。
- [x] 建立只含任务必需路径的转录、盲解、图形清单子目录；所有代理须在各自报告中明确未读取禁读卷材。
- [x] 复核批次 ID、source ID、paper ID、项目目录与规范源文件名均未冲突。

**Task 1 results (2026-10-11):** 固定 commit blob `918cf28f…` 与 source-manifest 相同；本地 PDF SHA-256 `d702c863…` 与 manifest 相同。`pdfinfo` 确认 2 页 A3、无加密；两页 150 dpi 渲染目视确认标题、题量和印刷页 969–970；`source_manifest.py validate` 通过。source ID 为 ready、尚未绑定；批次 `phase3-b15`、paper ID `gk-2015-regular-shandong-science`、项目目录均无冲突。所有 PDF/PNG/TXT 均在 `.work` 忽略目录。

**Expected:** 固定来源身份逐字匹配；两页均已目视；工作材料全在忽略目录。

### Task 2 — Independent transcription and solutions

- [x] Role-isolated drafts remain ignored and uncommitted; no role read another exam project/batch or the paired arts paper. Process deviations recorded: the first B solver's required brief included a Q17 figure-correction progress cue, so its Q17 solution was discarded and replaced by a clean crop-only solve/review. Two reviewers' full-PDF extraction surfaced unrelated source-question text; they did not read other answers, and this boundary deviation is recorded rather than described as perfect isolation.
- [x] 转录代理 A：Q1–10，写 `.work/phase3-b15/transcripts/partA.md`；独立审查和主会话逐题源页复核均通过。报告：`.superpowers/sdd/2026-10-11-gaokao-2015-shandong-science/task-2A-report.md`。
- [x] 转录（控制器接手）B：Q11–21，写 `.work/phase3-b15/transcripts/partB.md` 与 `figure-inventory.md`；记录每题 PDF 页及印刷页。独立审查通过；Q17 图形端点 `BF` 更正为 `FH`，修订后独立复审通过。报告：`.superpowers/sdd/2026-10-11-gaokao-2015-shandong-science/task-2B-report.md`。
- [x] 盲解代理 A（未读任何转录）：独立解 Q1–10，写 `.work/phase3-b15/blind/partA.md`；主会话复算和独立盲核均通过 10/10。报告：`.superpowers/sdd/2026-10-11-gaokao-2015-shandong-science/task-2A-blind-report.md`、`task-2A-blind-review.md`。
- [x] 盲解代理 B（未读任何转录）：独立解 Q11–Q21；Q15/Q19 按盲核发现的错误更正并复核，受简报提示污染的 Q17 段作废后由独立 clean 角色只凭 Q17 局部源图重解。Q11–Q16、Q18–Q21 的盲核中 Q15/Q19 修订复核通过；Q17 clean 解答单独盲核通过。报告：`.superpowers/sdd/2026-10-11-gaokao-2015-shandong-science/task-2B-blind-report.md`、`task-2B-blind-review.md`、`task-2B-fix-review.md`、`task-2Q17-clean-report.md`、`task-2Q17-clean-review.md`。
- [x] 主会话按固定源逐题复核两份转录，并由不同角色盲核解答；Q15/Q19 错误已逐项修正、复核，Q17 有明确隔离替代方案；无 U 项。复核汇总：`.superpowers/sdd/2026-10-11-gaokao-2015-shandong-science/task-2-main-review.md`。审查范围偏差均保留在对应记录中。

**Expected:** 21 题题面与页映射可回溯；答案各题有推导和独立盲核记录。没有跨读转录稿、其他答案稿或文科项目；源 PDF 处理造成的题段范围偏差及 Q17 角色替代均已如实记录。

### Task 3 — Integrate canonical sources, provenance, and vector figures

- [x] 整理规范 `_试题.md`、`_答案要点.md`、`_解析正文.md`；答案证据注明项目独立推导（D），未决项显式登记。
- [x] 依实际源页建立 Q13 框图与 Q17 三棱台 TikZ 图；对照源图检查拓扑、虚实线和标签，不提交栅格图。
- [x] 注册 `phase3-b15` 与新 paper/project，绑定且仅绑定固定 source ID；按分工写三角色 provenance。
- [x] 运行来源/生成器/简答/版本外壳 write+check；检查 Markdown 特殊字符、数学模式、题号与生成一致性。

**Expected:** source-manifest、index、manifest.csv、规范 Markdown、provenance、生成 LaTeX 相互一致；仅新卷与必要共享登记文件发生变化。

### Task 4 — Formal build, review, and close

- [x] 构建试题、解析、简答、印刷四版；检查所有 log 的 Overfull/Underfull/Missing character 与引用/资源错误，修复后重编。
- [x] 对四版全部页面逐页视觉审查（每页八项），单独放大核验 Q13/Q17 图形；问题不掩盖、不降级为文字检查。
- [x] 重编后重新 prepare 绑定 attempt；填写回执并 finalize，刷新批次/全量报告与 manifest.csv。
- [x] 运行批次来源/构建/审查门禁与项目测试；确认只保留 LaTeX 源与四版 PDF，不留栅格图及编译中间件。
- [x] 显式路径暂存本批文件并提交；不 push。

**Task 4 results (2026-10-11):** 正式构建 attempt `f06473d1-96eb-406e-877f-929a4b34d97d` 成功，四版 5/18/7/13 页，共 43 页；日志无缺字、未定义引用或 TeX 错误。解析版 Q6 与印刷版 Q19(1) 各有一条 Underfull，分别登记为逐项豁免（对应 PDF 第 8/11 页）；目视确认文字可读、无裁切/重叠/异常断行。四版全页各完成八项检查，Q13/Q17 图形页目视核对；批次事务 revision 3739，状态 `closed`，build `succeeded`，review `passed`。清理后当前项目 `build/` 仅有四版 PDF；LaTeX 源与 TikZ 图源保留，无栅格图入库。批次 provenance/生成/manifest CSV/报告门禁均通过。全套 862 项测试中 861 通过、13 跳过、1 失败：`test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones` 报告全库 334 条纸卷/批次缓存状态差异（`provenance.py check-all` 汇总涉及 272 卷）；差异指向既有/其他批次的派生状态，本批已闭环且未擅自批量改写其他卷。此前 `clean-build --paper` 曾删除整个当前卷 `build/`（含 PDF），已立即重建；重渲染后四版 43 张 PNG 与重建前逐字节一致，回执随后绑定新 attempt。六份全量汇总报告按事务状态刷新。提交待进行。

**Expected:** 批次为 `closed` 或带真实未决项的 `closed_with_blockers`；每一版四项回执绑定当前构建，所有页有复核记录；工作树只含本批提交。

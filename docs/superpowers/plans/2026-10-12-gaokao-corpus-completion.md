# 高考数学 LaTeX 题库全量收尾实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan batch-by-batch. Each closed manifest batch is one independently verifiable stage.

**Goal:** 按用户目标交付覆盖 1952—2026 年、来源可追溯、四版可编译且经过逐页复核的高考数学 LaTeX 题库，并明确保留未解决项。

**Architecture:** 以 `math-gaokao-latex/source-manifest.json` 为状态权威，以现有 provenance、formal build、review receipt、batch report 和 transactional finalize 工具推进每个批次。按年份顺序关闭批次；每批只改其归属回执/报告及仓库生成的清单投影，不手工伪造派生状态。共享工具、样式和总清单由主会话独占；来源事实不足时保留 pending/blocked 并记入报告。

**Tech Stack:** XeLaTeX、latexmk、TikZ/pgfplots、Python 3 项目工具、Poppler (`pdfinfo`/`pdftoppm`)、Git。

**Spec:** 用户提供的“高考数学真题 LaTeX 题库”完整目标；状态与文件入口见 `math-gaokao-latex/source-manifest.json`、`README.md`、`reports/`。

## Global Constraints

- 只在 `仓库根` 的 `feat/gaokao-phase0` 工作；不改主检出、不 push。
- 不编辑 `.remember/`、`.obsidian/`；共享样式、公共工具和 manifest 仅主会话写入。
- 每批正式构建四版，逐页视觉检查；候选页与警告页高分辨率复核，警告豁免必须逐项匹配当前构建日志。
- 只清理本批 `build/` 中非 PDF 编译中间物，保留 PDF；清理本批 `.work/` 与本次临时 PNG。
- 通过仓库事务/CLI 更新 derived state 和报告；不手工改写 production state、batch status 或 receipt 字段来绕过门禁。
- 阶段成果单独提交，不 push；提交前核对精确 diff 与 `git diff --check`。
- 碰到缺源、内容争议、未完成或视觉失败时如实保留 blocker，不凭记忆补题或答案。

## Review Focus

- 来源/题目/答案哈希变化：必须 provenance 重核，不得只刷新 PDF；由每批 `provenance.py check-batch` 验证。
- 共享生成器或模板变化造成旧产物过期：必须正式重建并重审，不得仅改状态；由 build receipt currency 与状态重算验证。
- 视觉候选之外的页面漏审：每个 work item 页码集合须覆盖完整 PDF；由 `review_receipts.py finalize-batch` 检查。
- TeX 警告误豁免或漏豁免：逐项核对行号、来源文件、类型、页码与当前日志；由 finalize 门禁验证。
- 复核后全量报告/清单投影过期：用 report renderer 更新后再 check；由 `report.py check --all` 验证。

---

### Task 1: 完成已开始的 1956 批次

**Files:**
- Modify: `math-gaokao-latex/1956_全国卷/receipts/build.json`
- Modify: `math-gaokao-latex/1956_全国卷/receipts/review.json`
- Modify: `math-gaokao-latex/reports/phase1-b13.md`
- Modify: `math-gaokao-latex/source-manifest.json` 与 renderer 管理的报告投影
- Update: `math-gaokao-latex/PROGRESS.md`

- [x] 正式重建四版；视觉检查 21 页及候选页；`finalize-batch` 返回 `FINALIZED`。
- [x] 执行来源、build receipt、review receipt、provenance、全量报告与 `git diff --check` 检查。
- [x] 核对仅保留四份 PDF；本批验证已完成，包含进度更新的提交待执行。

### Task 2: 逐批关闭 1957—2006

**Files:** 每批 manifest 指定卷的四个入口、receipt、provenance/来源（仅确有核验或修订需要时）、该批报告、全量生成投影及 `PROGRESS.md`。

- [ ] 每次选择时间顺序中最早且尚未 `closed`/有 blocker 说明的批次；检查已有来源与工作项，避免重复转录/复核。
- [ ] 执行 provenance → 生成/正式构建 → 四版逐页复核 → transactional finalize；内容或视觉 blocker 如实登记。
- [ ] 每批运行 scoped gates、全量报告 check、`git diff --check`，清理中间物并单批提交。

### Task 3: 逐批关闭 2007—2016

**Files:** 同 Task 2；按 manifest 的批次和归属修改，不跨卷改公共工具。

- [ ] 按 Task 2 的批次闭环处理；跨批共用来源、共享模板或生成器问题先由主会话解决并记录影响范围。
- [ ] 对答案、分值、题号与来源存在疑义者保留 needs-review/blocker，不以旧视觉回执代替内容核验。

### Task 4: 逐批关闭 2017—2026

**Files:** 同 Task 2；必须遵守既有年份专属目录与四版本入口结构。

- [ ] 按 Task 2 的批次闭环处理，复用已登记 PDF 来源与 TikZ 矢量图稿；不把 PNG/JPEG 页面渲染入库。
- [ ] 已完成的 Claude Code 转录/核查成果先对照当前 provenance 与来源哈希，确认一致后复用。

### Task 5: 全库整合验收与交付

**Files:** `README.md`、`manifest.csv`、reports、缺源/问题登记、全部项目回执；仅在生成器需要时由主会话修改共享工具。

- [ ] 运行全库 source/provenance/build/review/report validators 与完整测试套件；逐项调查失败，保留真实失败而非放宽门禁。
- [ ] 依据显式目标审计目录、四入口、共享内容复用、TikZ 矢量图、答案一致性与待补标注；校准 README、manifest.csv、缺失清单和构建报告。
- [ ] 复核工作树、最终提交范围与未解决 backlog；不 push。

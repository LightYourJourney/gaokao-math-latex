# 1985 年广东文史类、理工农医类数学 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将固定上游中的 1985 年广东省高考数学文史类与理工农医类两卷整理为有来源证据、逐题可追溯、可编译和可打印的 LaTeX 题库条目。

**Architecture:** 以高考数学题库 `source-manifest.json` 锁定的两份 PDF 为唯一题面依据，转录、答案和解析分别独立核查；主会话统一整合三份 Markdown 源并调用现有工具生成共享 LaTeX、四个版式和正式回执。原卷图只以项目内 TikZ/PGFPlots 重绘，不将扫描页或中间渲染图纳入 Git。

**Tech Stack:** 仓库现有 Python 3 清单/生成/构建工具、XeLaTeX、latexmk、ctex、TikZ/PGFPlots、Git。

**Spec:** 用户提供的“高考数学真题 LaTeX 题库”项目目标；仓库 `AGENTS.md`、`CLAUDE.md` 与题库现行 manifest/schema/生成器。

## Global Constraints

- 批次固定为 `phase2-b09`；仅处理本计划列明的 1985 广东文史类、理工农医类两卷，不 push。
- 题面来源仅为 `普通高考/1985/1985广东文.pdf` 与 `普通高考/1985/1985广东理.pdf`；执行时重新核对上游 HEAD、SHA-256、Git blob OID、PDF 页数和标题。
- 两份 PDF 不复制进题库 Git；不得把扫描页、PNG/JPEG 或其他栅格图稿作为排版素材提交。
- 题面照录固定来源；模糊字形、题号、图线、答案归属有争议时保留原始证据并登记问题，不凭记忆补写或悄悄订正。
- 试题、答案要点、解析正文是唯一人工维护内容；合并 Markdown、LaTeX 源、版本入口、清单投影和回执均按仓库工具生成。
- 文史类与理工农医类不得因题目相似而互相补题；答案独立推导并交由不同角色盲核，未解决项必须保持 U/blocked。
- 四个版本均正式编译并完成视觉复核；构建目录清理编译中间产物，只保留 PDF，源 `.tex` 保留。
- 不修改主检出 `主工作树` 中别的会话数据；所有批次草稿仅写忽略的 `.work/phase2-b09/`。

## 固定来源与映射

| 卷别 | paper ID | 项目目录 | source ID | SHA-256 | Git blob OID | 上游 PDF 页数 |
|---|---|---|---|---|---|---:|
| 文史类 | `gk-1985-regular-guangdong-arts` | `1985_广东卷_文史类` | `src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986` | `08af17407920dfb370335c7e3b52d0195beb4e01bb88c866a565c54e55bcc980` | `9060945c486849e8a0e883bc105ac3280bfc1306` | 16 |
| 理工农医类 | `gk-1985-regular-guangdong-science` | `1985_广东卷_理工农医类` | `src-8dba39a5d57fc6a2b63128db5686a4c8145016f60fe7cde20ec7dc81363d4f08` | `44aeb6e29239e3dc32190c275739979ae8e510de95b64298338182f6d7188206` | `f4398d6de76ab242d20f5ba9e6b7d2836c98480b` | 11 |

上游来源仓库当前 HEAD 预检值：`34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。文史类首页标题为“附录七、一九八五年广东省高考数学（文史类）试题与解答”；理工农医类首页标题为“1985 年广东省高等学校招生统一考试数学（理工农医类）”。上游可见另一个会话未跟踪目录 `普通高考/2016/.work/`，不得读取、修改或清理。

## Review Focus

- 低清扫描中的指数、根号、上下标、希腊字母和不等号是否与 PDF 图像一致；题面复核需逐页并放大疑点。
- 文史卷标题含“试题与解答”，必须分清原卷印刷内容与独立解答，不能把解答文字误并进题面。
- 理工农医卷中手绘坐标图/几何图的轴、刻度、端点、虚实线与遮挡是否逐项保真；源图只以矢量重绘。
- 两卷卷别与题号相似处是否串卷；每个答案均须绑定本卷题面和页码证据。
- 旧卷纸面页码与 PDF 页码是否一致；不确定时逐题记录映射，不按连续页数推算。

## File Map

- Create: `1985/1985_数学真题_广东文史类_{试题,答案要点,解析正文}.md` — 三份人工维护源文件。
- Create by tool: 同目录 `1985_数学真题_广东文史类_含解析.md` — 由规范源生成。
- Create: `1985/1985_数学真题_广东理工农医类_{试题,答案要点,解析正文}.md` — 三份人工维护源文件。
- Create by tool: 同目录 `1985_数学真题_广东理工农医类_含解析.md` — 由规范源生成。
- Create: `math-gaokao-latex/1985_广东卷_文史类/figures/*.tex`、`1985_广东卷_理工农医类/figures/*.tex` — 仅保存经题面确认的 TikZ/PGFPlots 源。
- Create by tool: 两个项目目录内共享 `questions.tex`、`answers.tex`、简答答案、四个独立入口、provenance、build/review 回执及 PDF。
- Modify by tool: `source-manifest.json`、`manifest.csv`、`index.json`、`missing-issues.md`、批次与全局报告；只能由支持工具更新。
- Create: `math-gaokao-latex/reports/phase2-b09.md` — 本批来源、构建、复核和未决项报告。

## Tasks

### Task 1 — 冻结来源并完成逐页转录与盲核

- [ ] 重新校验上游 HEAD、两个文件的 SHA-256/blob OID、PDF 页数、首页标题和全部页面可读性；将逐题 PDF 页/纸面页映射写入隔离草稿。
- [ ] 每卷分配独立转录/求解者、题面复核者、答案盲核者；同一卷三种角色互不相同。代理只写 `.work/phase2-b09/<paper_id>/`。
- [ ] 逐页转录所有题干、选项、小问、分值、图示和印刷说明；疑字、缺损、图形歧义明确标记，不用模型记忆恢复。
- [ ] 独立求解每题并记录推导；盲核代理先保存自己的答案和依据，再对比首解。未能裁定的差异作为 U 和 issue。
- [ ] 图形清单逐图记录源页、标签、几何关系、边线样式与题面引用次数；确认后才转为项目 TikZ/PGFPlots 源。

### Task 2 — 整合规范 Markdown、登记并生成项目源

- [ ] 主会话根据核查证据裁决差异，创建两卷三份规范 Markdown；保留来源无法辨认处，不将未经确认内容写成事实。
- [ ] 通过 `solution_sources.render_combined()` 生成两份 `_含解析.md`；检查题号、答案数、解析数、题面/解析图引用及卷别元数据。
- [ ] 确认 `phase2-b09`、paper ID、目录、source 未被其他会话占用；运行 registration dry-run，审查精确 diff 后仅执行一次 `register-papers --write`。
- [ ] 通过生成器创建共享 LaTeX、简答答案、四个版式入口和 provenance；运行所有相应 `--check` 与 schema 校验，不手改确定性产物。

### Task 3 — 正式构建、视觉复核并分阶段提交

- [ ] 两卷各编译试题、解析、简答、印刷四版；回执记录工具链、输入哈希、页数和日志。修复只限有来源依据的问题。
- [ ] 逐页渲染并复核两卷全部版本的首页、题面页、图形页、解析页、简答页及末页；有条件时复核完整页面，不提交渲染图。
- [ ] 对照详细答案与简答结论；运行来源、manifest、Markdown 题量/解析、生成、provenance、构建、review 和全局报告门禁；保留所有 U/blocker。
- [ ] 删除仅属于 phase2-b09 的临时渲染与编译中间件；`build/` 只留正式 PDF、LaTeX 源保留。精确暂存并分阶段提交，不 push。

## 验收

- `phase2-b09` 仅绑定上表两个 source/paper；来源指纹与当前上游文件一致。
- 两卷题面逐题有 PDF 页/纸面页映射；答案、解析由独立证据支持，模糊内容明确 U/问题化。
- 两卷各四版均有当前构建和视觉回执；生成器、manifest CSV、provenance、批次与全局报告检查通过。
- 不向 Git 加入原卷 PDF、PNG/JPEG、页面截图或编译中间件；主检出和其他批次工作不受影响。

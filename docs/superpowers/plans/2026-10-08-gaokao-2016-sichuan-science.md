# 2016 四川卷理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 四川卷理科（自主命题最后一年）整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** `source-manifest.json` 中的固定来源 ID 是身份根；题面、答案要点和解析正文作为规范 Markdown 保存，含解析稿与 LaTeX 项目由现有工具生成。题面转录和独立求解先写入忽略的批次目录，之后由不同角色盲核；不提交扫描 PDF、页面图或构建中间件。

**Tech Stack:** Markdown、Python 3 标准库工具、XeLaTeX、TikZ/PGFPlots、Git、Poppler。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_北京卷_理科`（b12，closed）与 `2016_北京卷_文科`（b13，closed_with_blockers——第 8 题隐含约定被并行会话复核降级，本卷凡依赖题面外约定的解答一律先标待核）。

## Global Constraints

- 正式批次为 `phase2-b15`（本轮单卷批次）。工作目录 `.work/phase2-b15/`。
- **并行会话警告**：phase2-b14（2016 上海文理）由另一会话进行中（其 index.json/manifest.csv 改动未提交）。本批提交时**必须按显式路径 git add**，不得 `git add -A docs/`，避免混入 b14 会话的未提交文件；开工前先 `git log --oneline -3` 确认批次归属未变。
- 固定上游 commit 为 `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；source ID、SHA-256、Git blob OID 和路径不得漂移（本轮已核定，见下表）。
- 源 PDF 为 2 页 A3（印刷页码 1019–1020），**仅含题面、不含答案**；答案解析一律独立推导，等级 D（非官方答案），必须由不同角色盲核。
- **四川自主命题结构：选择题 1–10（每题不印分值）、填空题 11–15、解答题 16–21，共 21 题**。与全国卷 8+6+6 不同，不得按 20 题模板硬套；原卷未印总分/分值/答题说明，一律不补录。
- OCR/文本抽取仅作辅助，规范题面必须逐页目视核对；不清晰内容保持原样并登记问题。
- 草稿只写 `.work/phase2-b15/<paper_id>/`；只保留 TikZ/PGFPlots 图源，不把 PNG/JPEG/PDF 图像或截图入库。
- 构建每卷试题、解析、简答、印刷四版；`build/` 仅留最终 PDF；不 push、不暂存无关改动。
- **规范源写裸 `%`**（渲染器会二次转义 `\%` 为 `\\%`，b13 踩过）；重编后先重跑 `prepare-batch` 换绑新 attempt 再写工作项。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 四川卷理科 | `gk-2016-regular-sichuan-science` | `2016_四川卷_理科` | `src-e4a937b21bfa9c09390e99ac0b2b2c357297f9b15c2119ffb6f2886984049d1a` | `fbf7accd45a89ee6e17810ccc0724fca27de041d505e8311e0c5e5bb56019c2c` | `85698a66143f8905cf4ad4f51dd26425381efe72` | `普通高考/2016/2016四川理.pdf` | 1019–1020 |

上游本地克隆：`gaokaomath-src`（工作区 HEAD 可漂移，一律以固定 commit 取文件）。SHA-256 已与 manifest 源记录一致、提取副本逐字节复验。

## Review Focus

- A3 三栏阅读顺序与文本抽取顺序可能不同：逐题映射到源页栏位与印刷页，查漏题、重题和错序。
- 无官方答案来源：独立推导与异人盲核必须分开取证；角色不独立则证据记 U，不得写成"盲核通过"。
- **凡依赖题面外约定/常识补充的解答（b13 第 8 题教训）**：本卷重点疑似区为第 16 题(2)「估计全市居民中月均用水量不低于 3 吨的人数，并说明理由」（直方图柱高含未知量 a，第 (1) 问先求 a）；若解答需依赖直方图读数之外的解释性约定，先登记待核再作答，不得无条件写死。
- 图形细节（第 6 题秦九韶程序框图、第 13 题三棱锥正视图、第 16 题频率分布直方图、第 18 题四棱锥 P-ABCD）易误读：逐页放大核验，无法确认则登记 blocker。
- 第 15 题「伴随点/伴随曲线」新定义题与第 21 题含参不等式恒成立（`f(x) > 1/x − e^{1−x}` 在 (1,+∞)）：题面文字逐字核对（定义域、不等号方向、参数范围）。
- 第 10 题向量条件组（|DA|=|DB|=|DC| 与三个点积=−2）几何意义需谨慎转译；第 19 题 e₂=5/3 与 4^n−3^n 通项分式逐字核对。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b15/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-08 晚)：** 固定 commit 下 blob OID `85698a66…`、实算 SHA-256 `fbf7accd…` 与 manifest 源记录（`src-e4a937b2…`，`source_state: ready`、`paper_id: null`）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（四川卷理）」，印刷页 1019–1020，结构 选择 1–10 / 填空 11–15 / 解答 16–21（共 21 题），源不含答案、不印分值。页映射：第 1–16 题在第 1 页（1019），第 17–21 题在第 2 页（1020）。预识别图形需求 4 处：第 6 题程序框图、第 13 题三棱锥正视图、第 16 频率分布直方图（柱高含参数 a）、第 18 题四棱锥。`phase2-b15`、`gk-2016-regular-sichuan-science`、项目目录 `2016_四川卷_理科` 与规范 Markdown 前缀 `2016_数学真题_四川理` 均未被占用。

### Task 2 — Transcribe and solve independently

- [ ] 转录代理只写 `.work/phase2-b15/gk-2016-regular-sichuan-science/questions.md`、`page-map.md`、`figure-inventory.md`。
- [ ] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [ ] 主会话逐题对照源页复核转录稿；不确定字形与图形显式保留为待核。

### Task 3 — Integrate and register

- [ ] 建立规范 Markdown 三件套（试题 / 答案要点 / 解析正文）并派生含解析稿，图形只写 TikZ 图源。
- [ ] 注册 `phase2-b15` 与 paper/项目目录；provenance 按角色分离导入。
- [ ] 生成项目源与四版本外壳，跑对应检查。

### Task 4 — Build, review, and close

- [ ] 正式构建四版本；逐页视觉审查（含图标签"墨迹连通性"量测口径）。
- [ ] 刷新报告与 `manifest.csv`（显式路径提交），全量测试，清理本批中间件（保留 PDF），提交（不 push）。

## 已知口径与坑（b11–b13 沉淀）

- **四版本口径**：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；**印刷版=题目+完整解析的紧凑五号排版**。证明类小题答案框印「见解析版」是生成器既有口径。
- **流水线顺序**：`register-papers --repo <worktree根> --manifest <绝对路径>`（`_含解析.md` 先放占位，注册后 extract-batch 覆盖）→ provenance 三角色文件（role 为 null 必须填，哈希用工具函数现场算）→ generate/short/editions 三连 write+check → build --formal → **重编后先 prepare-batch 换绑 attempt** → 写工作项 → finalize → report render/check --all（带 --manifest --issues 绝对路径）→ manifest_csv --write（**在仓库根跑**）→ unittest。
- **规范源写裸 `%`**；图源 TikZ：框图显式坐标、逐段独立 `draw[->]`、回边 `|-` 且目标点高于源点、坐标轴标题用 `right` 不用 `below left`、`scale` 影响坐标差注释。
- **公共宏是全项目回执依赖闭包**：图环境后齐左、节末留白、「见解析版」均留档不修；单批问题只改规范 Markdown 或图源；孤悬用解析正文 `\Needspace{N\baselineskip}`。
- **审查判据**：留白/齐左类按 b12 实测先例（末页填充 27–42%）判 pass；墨迹连通性判定标签碰线；重编后 150 dpi 像素差分分流，未变页沿用判定。
- **并行会话纪律**：b14（上海）另一会话进行中；本批全程用显式路径提交；收尾前确认 `git log` 中 b14 会话的最新提交，避免误收它的文件。

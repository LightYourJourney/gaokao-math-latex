# 2015 上海文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 上海文卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b23、phase3-b00/b01/b02/b03 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**版式新类型**：源为 **A3 横向（1190.55 × 841.89 pt）双栏书刊合排**——印刷页码 979/980 属**合订本书页体系**（位于页面中缝底部），phase3 批次首次处理；栏序/栏内坐标映射由转录实测建档。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：上海卷 3+1 体制（2017 改革前）结构从源实测核定（2016 上海文理 b14 由另一会话在途，**不依赖其未定稿产物**）。

## Global Constraints

- 正式批次 `phase3-b04`；工作目录 `.work/phase3-b04/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源已核定（下表）。
- 源 2 页 A3 横向，**无答案页**（p1 印 979＝填空 1–14＋选择 15–18＋解答 19/20；p2 印 980＝解答 21–23）→ **答案证据等级 D**（解析全由盲解撰写）。
- **结构（初判，以转录实测为准）**：填空 1–14（4 分×14＝56）＋选择 15–18（5 分×4＝20）＋解答 19–23（74 分）＝23 题 150 分。
- **图形（初判 2 处，以图清单为准）**：第 19 题圆锥（底面直径 AB＋半圆弧中点 C、E 弧 CB 中点；P 顶点、O 圆心；椭圆底＋虚实线——新图元）；第 21 题直角路线图（O-P-Q，含 OP/PQ/OQ 标注）。
- **规范源写裸 `%`（构建前强制 grep 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- 沉淀纪律（b15–b23/phase3 全量 + b03 新增）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学；答案行裸 `*` 用 `\ast`；**规范源反引号内禁裸 `$`（写 `\$`；b03 实证静默丢号）与禁包 LaTeX 命令**；↔ 等 lmroman 无字形符号不裸入正文；图标签 `inner sep=0`、分数型标签按源墨迹定位；**差分同引擎 pdftoppm**；审查代理 ≤8 页；**图自查含线段采样矩阵（每条应有线＋1–2 条空白对照线——连通域查不出「缺一条线」）**；**finalize-batch 先于 check-batch**（回执冻结由 finalize 执行）。
- **答案要点禁「① 答案：」式**（次级序号夹答案硬错误）：同小问多问写「答案：① …；② …」（phase3-b02 新坑）。
- A3 双栏版式：栏序按**阅读序**（左栏→右栏）；印刷页码 979/980 登记于来源说明（合订本页码、非卷内页码）；不印页码时按 b03 口径。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 上海文卷 | `gk-2015-regular-shanghai-arts` | `2015_上海卷_文科` | `src-cc92124505f3372f75db33e14eb583bf18a3e93fc5164f1a67a8e77536b9668f` | `1ad05c305daf172722174bd901b991156c67f78b014e343a974ebe9b5eac17d7` | `b15c5ec48af654ae64aba9275246222b156544df` | `普通高考/2015/2015上海文.pdf` | 2 |

## Review Focus

- A3 双栏书刊版式首次处理：栏序（左栏→右栏）、题号续排、印刷页码 979/980 的记录口径、栏内坐标实测（图形/公式坐标换算按页 pt）。
- 第 19 题圆锥图（椭圆底＋虚实线＋P/O/AB/C/E 标注）按源复刻——新图元类型「圆锥（斜视椭圆底）」。
- 第 21 题直角路线图（O-P-Q 三点、直角在 P）照源。
- 结构核定（23 题、分值印制情况实测）；文理差异对照留待后续 2015 上海理的批次。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the fixed upstream.
- [x] Render and inspect all pages; record visible title, structure and printed-page numbers in `.work/phase3-b04/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 结果（2026-10-10）：** 固定 commit `34c13a6c…` 树内 blob `b15c5ec4…`（`git ls-tree` 核验）与提取副本 SHA-256 `1ad05c30…`（513,487 B）与 manifest 源记录（`src-cc92124505f3372f…`，未绑定）一致。目视：**A3 横向（1190.55 × 841.89 pt）双栏书刊合排**，页脚印 **979（p1）/980（p2）**——合订本书页页码，位于页面中缝底部；标题「2015 普通高等学校招生考试（上海卷文）」；结构＝填空 1–14＋选择 15–18＋解答 19–23（19、20 在 p1，21–23 在 p2），共 23 题；图形 2 处：Q19 圆锥（P 顶、O 心、AB 直径、C 与 E 弧中点）、Q21 直角路线图（O-P-Q）；**全 2 页无答案**（等级 D）。身份（paper_id `gk-2015-regular-shanghai-arts`／项目目录 `2015_上海卷_文科`／批次 `phase3-b04`）双命名空间空闲。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [ ] 转录 A：填空 1–14 + 选择 15–18（p1）+ 全 2 页 page-map（含 A3 双栏栏序/坐标实测）。
- [ ] 转录 B：解答 19–23（p1 尾 + p2）+ 图清单（Q19 圆锥、Q21 路线图）。
- [ ] 盲解 A：本库 1–18（填空+选择）；盲解 B：本库 19–23（解答）。
- [ ] 主会话逐题对照源页复核转录稿；盲解互证。

### Task 3 — Integrate and register

- [ ] 规范三件套 + 含解析派生 + TikZ 图源（圆锥图新图元）。
- [ ] 注册 `phase3-b04`；provenance 三角色导入。
- [ ] 生成项目源与四版本外壳，三连 check。

### Task 4 — Build, review, and close

- [ ] 正式构建 → 审查代理（分波并发 ≤8 页/段）→ 修复轮（如有）→ 重建 → 差分 → 复审。
- [ ] 审查回执填写（逐页×8 项）→ finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

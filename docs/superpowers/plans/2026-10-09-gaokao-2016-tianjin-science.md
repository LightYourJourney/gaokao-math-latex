# 2016 天津卷理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 天津卷理科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15/b16（四川文理）批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_四川卷_理科`（b15）、`2016_四川卷_文科`（b16）。

## Global Constraints

- 正式批次 `phase2-b17`；工作目录 `.work/phase2-b17/`。
- **并行会话**：phase2-b14（上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源三方已核定（下表）。
- 源 PDF 2 页 A3（印刷页 1023–1024），仅含题面；答案解析独立推导（等级 D）+ 异人盲核。
- **天津卷结构：选择 1–8、填空 9–14、解答 15–20，共 20 题**（与四川 10+5+6 不同）；源不印分值，照录不补。
- **规范源写裸 `%`（建批构建前强制 grep `\\%` 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- **解答题小问写法「（N） 内容」（N 后带一个空格）**——b16 首派生失败教训（extract-batch 解析器要求）。
- **Q15 类型长定义式用 `\frac` 非 `\dfrac`**（b15/b16 两次 Overfull 教训）。
- **建后先主会话自查全部新图**，修完再派审查代理。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 天津卷理科 | `gk-2016-regular-tianjin-science` | `2016_天津卷_理科` | `src-b234202a2ba49eaa8c1a881cdd98336816e77c83a73dfc3d2cb077d8f44a4dd6` | `f636ae4f12cc458b39a6a1e4db5de651afe8bd82ccf60e6828fad935a869111b` | `b6c4d6f2050bc9366b0dc7fba4489695b0967acf` | `普通高考/2016/2016天津理.pdf` | 1023–1024 |

## Review Focus

- **津卷结构独立核定**：8+6+6=20 题；填空 9–14 共 6 空。
- 图形 4 处：第 4 题程序框图、第 11 题四棱锥三视图（**三个子图**：正视图+侧视图+俯视图，同 b16）、第 12 题圆（AB 直径、弦 CD 交 AB 于 E）、第 17 题正方形+矩形立体图（**多顶点**：E,F,B,O,A,C,D,G,H）。
- 第 17 题图为本批最复杂图形（正方形 ABCD 中心 O、矩形 OBEF、G 为 AB 中点、H 在 AF 上），转录与重绘须逐顶点核对。
- 文理不得互推（天津文由后续批次做），一律以源页独立核定。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b17/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-09)：** 固定 commit `34c13a6c…` 上 blob `b6c4d6f2…`、SHA-256 `f636ae4f…` 与 manifest 源记录（`src-b234202a…`，ready、未绑定）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（天津卷理）」，印刷页 1023–1024，结构 8+6+6=20 题（选择 1–8、填空 9–14、解答 15–20），源不含答案、不印分值。页映射：Q1–16 → p1（1023）；Q17–20 → p2（1024）。图形 4 处（Q4 框图、Q11 三视图三子图、Q12 圆、Q17 立体图）。**注**：上游 clone HEAD 已非固定 commit（`266afe22`），校验一律显式用固定 commit 对象。

### Task 2 — Transcribe and solve independently

- [ ] 转录代理只写 `.work/phase2-b17/gk-2016-regular-tianjin-science/questions.md`、`page-map.md`、`figure-inventory.md`。
- [ ] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [ ] 主会话逐题对照源页复核转录稿。

### Task 3 — Integrate and register

- [ ] 规范三件套 + 含解析派生 + 4 幅 TikZ 图源。
- [ ] 注册 `phase2-b17`；provenance 三角色导入。
- [ ] 生成项目源与四版本外壳，三连 check。

### Task 4 — Build, review, and close

- [ ] 正式构建（构建前 grep `\\%` 自检）→ **主会话先自查全部图** → 派 4 版审查代理。
- [ ] 修复轮（如有）→ 重建 → 像素差分 → 变化页二轮复审 → 合并（未变页沿用 + 裁定表）。
- [ ] finalize → 报告刷新（带 --manifest/--issues，manifest_csv 在仓库根跑）→ 全量测试 → 清理中间件 → 显式路径提交（不 push）。

## 已知口径与坑（b11–b16 沉淀）

- 四版本口径：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；印刷版=题目+完整解析紧凑排版；「见解析版」为生成器既有口径。
- 规范源写裸 `%`；解答题小问「（N） 内容」（N 后空格，b16 教训）；长定义式 `\frac` 非 `\dfrac`（b15/b16 教训）；TikZ 图源全坐标统一缩放、框图显式坐标逐段独立 draw、回边 `|-` 目标点高于源点、坐标轴标题题用 `right` 锚。
- 孤悬用解析正文 `\Needspace{N\baselineskip}`，N 按实测剩余行数取（须**大于**该处剩余量才触发）；改解析正文后重派生含解析、重编。
- 公共宏/转换器（`common/*`、`md2tex.py`）是全项目回执依赖闭包：齐左、留白、「解析」标签孤悬类均留档不修。
- 留档先例：b12/b13/b15 各批次的裁定表文本在 `.work/phase2-b1{2,3,5}/merge_findings2.py` 可直接复用。
- 在他批在途时刷新报告：`tools/report.py` 已修（缺失回执记 null），直接 `render/check --all` 即可。

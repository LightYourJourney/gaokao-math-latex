# 2016 四川卷文科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 四川卷文科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15（四川理科）批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_四川卷_理科`（b15，同省配对）。

## Global Constraints

- 正式批次 `phase2-b16`；工作目录 `.work/phase2-b16/`。
- **并行会话**：phase2-b14（上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`；收尾前 `git log` 确认批次归属。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源三方已核定（下表）。
- 源 PDF 2 页 A3（印刷页 1021–1022），仅含题面；答案解析独立推导（等级 D）+ 异人盲核。
- **四川自主命题结构：选择 1–10、填空 11–15、解答 16–21，共 21 题**；源不印分值，照录不补。
- **规范源写裸 `%`（建批构建前强制 grep `\\\\%` 自检——b13/b15 两犯）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- **建后先主会话自查全部新图（b15 教训：直方图坐标混用缺陷先派代理后自查、被迫走二轮）**，修完再派审查代理。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 四川卷文科 | `gk-2016-regular-sichuan-arts` | `2016_四川卷_文科` | `src-18b75fe448bbe7811db6e6ba5fc5130b950fc40ba251c916bdbf940647ce5ac4` | `7bdfb3dd1a6547dea9e5e372f2538604a37fe44c5a4342f17367d5d035fff19f` | `1a286990644d01d88ffc1be0a833ac90c45637dc` | `普通高考/2016/2016四川文.pdf` | 1021–1022 |

## Review Focus

- **文理不得互推**：文卷与 b15（理科）同省同年，Q18 解三角形为文理共有题（可交叉参照），其余题（含伴随点命题组、数列、椭圆、导数）内容不同，一律以源页独立核定。
- 图形 4 处：第 8 题秦九韶程序框图、第 12 题三棱锥三视图（**三个子图：正视图+侧视图+俯视图**，比理科多两个子图）、第 16 题频率分布直方图、第 17 题四棱锥 P-ABCD。
- 第 15 题伴随点四条命题与理科卷不同（②单位圆上伴随点仍在单位圆上、④三点共线→伴随点共线），逐字核对。
- 第 20 题椭圆：焦点与短轴**两端点**成直角三角形（与理科"一个端点"不同），P(√3, 1/2) 在椭圆上。
- 第 21 题文卷 g(x) 为显式定义（1/x − e/eˣ）且三小问（理科为不等式恒成立两小问）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b16/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-09)：** blob `1a286990…`、SHA-256 `7bdfb3dd…` 与 manifest 源记录（`src-18b75fe4…`，ready、未绑定）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（四川卷文）」，印刷页 1021–1022，结构 10+5+6=21 题，源不含答案、不印分值。页映射：Q1–16 → p1（1021）；Q17–21 → p2（1022）。图形 4 处（Q8 框图、Q12 三视图三子图、Q16 直方图、Q17 四棱锥）。身份全部空闲。

### Task 2 — Transcribe and solve independently

- [ ] 转录代理只写 `.work/phase2-b16/gk-2016-regular-sichuan-arts/questions.md`、`page-map.md`、`figure-inventory.md`。
- [ ] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [ ] 主会话逐题对照源页复核转录稿。

### Task 3 — Integrate and register

- [ ] 规范三件套 + 含解析派生 + 4 幅 TikZ 图源。
- [ ] 注册 `phase2-b16`；provenance 三角色导入。
- [ ] 生成项目源与四版本外壳，三连 check。

### Task 4 — Build, review, and close

- [ ] 正式构建（构建前 grep `\\\\%` 自检）→ **主会话先自查全部图** → 派 4 版审查代理。
- [ ] 修复轮（如有）→ 重建 → 像素差分 → 变化页二轮复审 → 合并（未变页沿用 + 裁定表）。
- [ ] finalize → 报告刷新（带 --manifest/--issues，manifest_csv 在仓库根跑）→ 全量测试 → 清理中间件 → 显式路径提交（不 push）。

## 已知口径与坑（b11–b15 沉淀）

- 四版本口径：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；印刷版=题目+完整解析紧凑排版；「见解析版」为生成器既有口径。
- 规范源写裸 `%`；TikZ 图源全坐标统一缩放（**勿混用 cm 与单位缩放**——b15 直方图教训）、框图显式坐标逐段独立 draw、回边 `|-` 目标点高于源点、坐标轴标题题用 `right` 锚。
- 孤悬用解析正文 `\Needspace{N\baselineskip}`，N 按实测剩余行数取（须**大于**该处剩余量才触发——b15 Q21 实测 24.7 行、22 不触发、26 生效）；改解析正文后重派生含解析、重编。
- 公共宏/转换器（`common/*`、`md2tex.py`）是全项目回执依赖闭包：齐左、留白、「解析」标签孤悬类均留档不修。
- 留档先例：b12/b13/b15 各批次的裁定表文本在 `.work/phase2-b1{2,3,5}/merge_findings2.py` 可直接复用。

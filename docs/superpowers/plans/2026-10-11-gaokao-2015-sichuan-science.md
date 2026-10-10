# 2015 四川理卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 四川理科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b08 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**与刚完成的 2015 四川文卷（phase3-b08）同书连页**：A3 横向三栏书刊合排（印刷页码 **981/982**，文卷 983/984）、LaTeX（CM 系）重排产物、21 题结构（选择 1–10＋填空 11–15＋解答 16–21）、**无答案页（等级 D）**。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_四川卷_文科`（phase3-b08）。

## Global Constraints

- 正式批次 `phase3-b09`；工作目录 `.work/phase3-b09/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源已核定（下表；sha 与 manifest 逐字一致）。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 981、p2 印 982）→ **答案证据等级 D**（解析全由盲解撰写）。
- **文理对照纪律（照 b05/b08 先例）**：文卷（`2015_四川卷_文科`）已完成并 FINALIZED——**仅作主会话事后互证**；**转录/盲解代理不得读取文卷任何产物**。文理大量同题（理 Q3＝文 Q6 框图同题、理 Q10＝文 Q10 抛物线同题、理 Q13＝文 Q8 保鲜同题、理 Q15＝文 Q15 四命题同题、理 Q18＝文 Q18 展开图同题但**三问不同**（理：FGH 标记＋MN∥平面 BDH＋二面角 A−EG−M；文：FGH 标记＋BEG∥ACH＋DF⊥BEG）；理 Q16＝文 Q16 同题但 **(2) 异问**（理：|Tn−1|<1/1000 的 n 最小值；文：求 Tn））；理独有（Q4 周期奇函数变体、Q5 双曲线、Q6 计数、Q7 向量、Q9 二次函数最值、Q11 二项式、Q12 三角、Q14 面面垂直、Q17 辩论赛概率、Q19 半角公式、Q20 椭圆定点异问（|QA|/|QB|=|PA|/|PB| 求定点 Q）、Q21 异式函数）。
- **图形/表初判 5 处**：Q3 程序框图（7 框「否」右回边，与文卷同构）；Q14 四边形 ABCD 与正方形 ADPQ 面面垂直图（含 EM、AF 线）；Q18 正方体平面展开图＋直观图（两幅一体；理版含 M（BC 中点）、N（GH 中点））；Q19 四边形 ABCD 图（四顶点）；Q20 椭圆图（过 P 动直线、定点 Q 异问）。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- 沉淀纪律（b15–b23/phase3 全量 + b08 新增）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学（用 `\text{}`——**注意显示式内 `\text{CJK␣}` 尾随空格会丢、须写 `\text{CJK}\ `**）；**答案行含 `*` 已由 md2tex 治本**；**规范源反引号内禁裸 `$`（写 `\$`）、禁包 LaTeX 命令、禁空参数命令**；↔ 等 lmroman 无字形符号不裸入正文；图标签 `inner sep=0`、分数型标签按源墨迹定位；**差分同引擎 pdftoppm**；审查代理 ≤8 页、**524 限流时死支不立即重派、分批 ≤4 支补派**；图自查含线段采样矩阵＋**判据灵敏度自证**；**finalize-batch 先于 check-batch**；**not_applicable 必须写理由**；孤儿尾框/Needspace 留白/选项栏漂移/链接色为已接受类。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**的解析须流水式、答案单一答案行。
- 标点与记号照 b08 四川文口径（题号句末全角、正文半角→全角归一、选项标号半角照源、`\leqslant`、向量按源实测定）；**以理卷源页字体实测为准**。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 四川理卷 | `gk-2015-regular-sichuan-science` | `2015_四川卷_理科` | `src-5aca318d1827632415c28e26a7727648d1f31f26b2eccfa9c546e18834fc01e6` | `903a1e91d3eed52d834c8648cd56c8bc94c88e9dd557b0d7506e2858cb1b2e4d` | `1debef009098d6cfce6089585eb1ab132afdfb19` | `普通高考/2015/2015四川理.pdf` | 2 |

## Review Focus

- 21 题结构核定（题号连续、无分值印制）、无答案页（等级 D）。
- 文理对照物（同题五处：Q3/Q10/Q13/Q15/Q18 与异问两处：Q16(2)/Q18 三问——**事后互证**，不干预独立工作）。
- Q14 图（面面垂直正方形＋E/F/M 点）与 Q19 四边形图（新图元）按源复刻；Q18 理版（M/N 点、新三问）与 Q20 椭圆异问（定点 Q）逐题双代理互证。
- 理独有题（Q4–Q7、Q9、Q11、Q12、Q17、Q19、Q20、Q21）逐题双代理互证。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：cp 至 `.work/phase3-b09/source/2015四川理.pdf`，现场 sha256＝`903a1e91…`（与 manifest artifact.sha256 逐字一致）。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，127 行）。
- [x] 版式判读：A3 横向三栏书刊合排；p1＝栏1（标题＋选择 1–7 含 Q3 框图）／栏2（选择 8–10＋填空 11–15＋「三、解答题」头）／栏3（Q14 图＋Q15＋Q16＋Q17）；p2＝18/19/20/21（Q18 双图、Q19 四边形、Q20 椭圆图）。页码 981/982。LaTeX CM 系重排、全矢量、文本层完整。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [ ] 转录 A（Q1–10 选择，含 Q3 框图）：`.work/phase3-b09/transcripts/partA.md`。
- [ ] 转录 B（Q11–21＋图表实测清单）：`.work/phase3-b09/transcripts/partB.md`＋`.work/phase3-b09/figure-inventory.md`。
- [ ] 盲解 A（Q1–10）：`.work/phase3-b09/blind/partA.md`；盲解 B（Q11–21）：`.work/phase3-b09/blind/partB.md`。
- [ ] **所有四代理 prompt 均含：不得读取 `2015_四川卷_文科/` 与 `2015_数学真题_四川文_*` 任何产物。**

### Task 3 — Integrate and register

- [ ] 规范三件套（试题/答案要点/解析正文）+ 含解析占位；四项自检（`%`、空参数、反引号、CJK 入数学）＋（N）空格锚点检查。
- [ ] TikZ 图源 5 处生成 + 探针目检（含源坐标换算回验）。
- [ ] 注册 `phase3-b09`；provenance 三角色导入；extract-batch 派生。
- [ ] generate/short/editions 三连 write+check → build --formal（修复轮 → 重建 → 差分 → 复审）。

### Task 4 — Build, review, and close

- [ ] 审查代理（1 图自查 + 分段并发 ≤8 页/段；524 限流时分批补派）→ 修复轮（如有）→ 重建 → 差分 → 复审。
- [ ] 审查回执填写（逐页×8 项）→ finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

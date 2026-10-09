# 2015 江苏卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 江苏卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b23、phase3-b00/b01 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**结构与 2016 江苏（phase3-b00）同型**（填空 1–14 + 解答 15–20 + 附加题 21–23、21 四选二）——建模与流程直接沿用。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_江苏卷`（phase3-b00）。

## Global Constraints

- 正式批次 `phase3-b02`；工作目录 `.work/phase3-b02/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源三方已核定（下表）。
- 源 2 页 A3（1190.55×841.89pt），印刷页 959–960；**结构**：填空 1–14 + 解答 15–20 + 附加题 21–23（21 四选二【A】–【D】，理科加考）＝ 23 题（参考 2016 江苏；最终以转录核定为准）。
- **图形 6 处（初判，以图清单为准）**：Q4 伪代码流程框（**全库首例「代码框」图元**——若源为带边框文本块，裁定 TikZ 复刻 or 逐字照排）、Q16 三棱柱、Q17 山区公路拟合曲线图（**首例「坐标系+拟合曲线/切线」类**）、Q18 椭圆+准线、Q21【A】圆几何（外接圆+割线）、Q22 四棱锥 P-ABCD。
- **规范源写裸 `%`（构建前强制 grep 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- 沉淀纪律（b15–b23/phase3 全量）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学；答案行裸 `*` 用 `\ast`；**规范源禁反引号包 LaTeX 命令**（\texttt Missing $ 坑）；↔ 等 lmroman 无字形符号不裸入正文；图标签 `inner sep=0`、分数型标签按源墨迹定位；**差分同引擎 pdftoppm**；审查代理 ≤8 页、键名 `"check"`、选项断行/印刷版页眉页脚留档口径。
- **速查表顺序**：选择题表必须置于填空表之前（make_short_answers 拉平机制）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 江苏卷 | `gk-2015-regular-jiangsu` | `2015_江苏卷` | `src-b940baa9dd8774cad81f6437822618e3d9dc33f0bdeef169f41886a07c1ea838` | `1a1870c5cbc0e908308c7573aa0f592087e268bc676f6477bb1d399fc8ba18d4` | `64eaed197a09c19ea01c5fb917df702f7478bfc5` | `普通高考/2015/2015江苏.pdf` | 959–960 |

## Review Focus

- 结构与附加题边界独立核定（对照 2016 江苏先例；21 四选二四子块）。
- Q4 伪代码框图元的复刻方式（全库首例，主会话裁定）。
- 分值印载情况待转录普查（照录不补）。
- 六图逐处对照源实测；新图元类型（伪代码框、拟合曲线图）主会话 600 dpi 连通域自查。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase3-b02/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 结果（2026-10-09）：** 固定 commit `34c13a6c…` 上 blob `64eaed19…` 与 SHA-256 `1a1870c5…`（516,513 B）与 manifest 源记录（`src-b940baa9…`，未绑定、2 页 A3）一致；提取副本逐字节复验。目视：标题「2015 普通高等学校招生考试（江苏卷）」，印刷页 959–960（页脚居中），**结构 = 填空 1–14（p1 左栏）+ 解答 15–20（p1 中/右栏）+ 附加题 21–23（p2；21 四选二【A】–【D】）＝ 23 题**——与 2016 江苏同型。图形初判 6 处（Q4 伪代码框、Q16 三棱柱、Q17 公路拟合曲线图、Q18 椭圆+准线、Q21A 圆几何、Q22 四棱锥）。身份（paper_id `gk-2015-regular-jiangsu`/base `2015_js`/目录 `2015_江苏卷`）空闲；批次号 `phase3-b02` 双命名空间空闲。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [x] 转录 A：填空 1–14 + 全 2 页 page-map + 图清单（Q4/Q16/Q17/Q18）。
- [x] 转录 B：解答 15–20 + 附加 21–23 + 图清单续（Q21A/Q22）。
- [x] 盲解 A：Q1–14；盲解 B：Q15–23（含 21 全四选做）——读源全页（源不附答案，无泄卷约束）。
- [x] 主会话逐题对照源页复核转录稿；盲解互证。

**Task 2 结果（2026-10-09）：** 四代理交付并全读——转录两段（part1 填空+page-map+图清单 F01–F04；part2 解答+附加+图清单续 Q21A/Q22）与盲解两段（1–14 与 15–23 全 23 题零存疑）。主会话修正：part1 frontmatter 的 source ID 笔误（SHA 误作 src ID）、合并稿补 Q21【C】【D】（初版漏）、Q21【B】矩阵行内定界照 2016 先例改 `$...$`。源为 LaTeX（XeLaTeX＋ctex）矢量产物（全库首例「源即 LaTeX」——几何可直接取内容流排版值）。

### Task 3 — Integrate and register

- [x] 规范三件套 + 含解析派生 + TikZ 图源（含首例伪代码框图元）。
- [x] 注册 `phase3-b02`；provenance 三角色导入。
- [x] 生成项目源与四版本外壳，三连 check。

**Task 3 结果（2026-10-09）：** 四份规范源写毕；6 图由 `.work/phase3-b02/make_figures.py` 从图清单实测/排版值程序化生成（内嵌断言：D 中点/E 交点/Q 中点/B-C 镜像全过），探针编译零错、渲染目视通过。register rev 3545、provenance rev 3546；extract-batch 生成含解析与解析正文派生物（check-batch 23 题全过）；三连 check 全过。初次注册后 validate 报「图引用 1≠2」属预期（含解析占位无引用），extract 后归位。**坑**：答案要点第 17 题 (2) 的「① 答案：…；② 答案：…」触发 solution_sources「次级序号夹答案」硬错误——须改为「答案：① …；② …」（答案在前的单块式，照 2016 江苏先例）。

### Task 4 — Build, review, and close

- [x] 正式构建（构建前 grep `\%` 自检）→ 主会话图自查 → 审查代理（≤8 页/代理）。
- [x] 修复轮（两轮）→ 重建（v2/v3）→ 同引擎差分 → 变化页复审 → 收敛。

**Task 4 修复轮编年（2026-10-09）**：
- **v1 审查**：9 段代理（试题版 1、简答版 1、印刷版 3、解析版 4；其中解析版 b 段因中转站 524 中断后重派）。发现 7 处必修（R1 矩阵 `\&` 转义高、R7 Q18 公式越纸高、R2 Q14 sin 值、R3 Q20(2) 舍根、R4 Q12 上下半支、R9「分」字普查 3→5、R11 17/18 图描述矛盾）+ 若干微项。
- **v1→v2**：7 处修复（解析正文 5 处 + 试题.md 2 处）→ extract/generate → build attempt `cb025cf4`（四版 overfull 归零）→ 差分（14 变化页）→ 2 复审代理全 pass。
- **v2→v3**：R15「新形」生造词修复 → build attempt `29326c8c`（全零告警）→ 差分仅 2 页（解析版 p10、印刷版 p8）→ 主会话并排复审通过。
- **接受留档（不修）**：R5 Q17 图跨页（公共生成结构：`questions.tex` 图后 Needspace 对图落页无约束 + `question` 环境 0.15 预留不足；全库同构，b00 未触发）；R14 Q17(2) 小标题孤悬（`\gksubpart` 的 `\Needspace{6\baselineskip}` 只管标题自身，公共宏层）；R6「见解析版」自指（b00 先例）；R8 PUA 大括号（b00 先例 8 处同因）；R12 Q21【B】顶格（b00 三处先例）；R13 Q19 答案框字距微压（正常行适配）。**R10 半角标点=误报撤销**（逐字符复核全角）。
- **测试基线复确认**：861 项 1 失败 = 全库既有项（`test_provenance` 缓存状态，312 条均其它卷、gk-2015 零涉入）。
- [ ] 审查回执填写（4 代理：逐页×8 项）→ finalize → 报告刷新 → 清理中间件 → 显式路径提交（不 push）。
- [ ] 修复轮（如有）→ 重建 → 同引擎差分 → 变化页复审 → 合并。
- [ ] finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

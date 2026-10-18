# 2015 广东理卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 广东理科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b16 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。A3 横向三栏书刊合排（印刷页码 **947/948**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **21 题（选择 1–8＋填空 9–15＋解答 16–21）**。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_广东卷_文科`（phase3-b16）、`2015_山东卷_理科`（phase3-b15）、`2015_安徽卷_理科`（phase3-b13）。

## Global Constraints

- 正式批次 `phase3-b17`；工作目录 `.work/phase3-b17/`。
- **并行会话**：他会话工作线（1977 上海等）在推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；现场核 blob `ec54683e1f030bde8b66ccfe2b1edea4a5a8ea0a` 在 34c13a6 与工作树一致（sha256 `1c3faab5…`）。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 947、p2 印 948）→ **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`–`.work/phase3-b16/`、`2015_广东卷_文科`、`2015_数学真题_广东文*` 等）；同书对照仅主会话事后互证用。**本批与广东文为文理配对**——代理照常零参照，主会话事后互证。
- **说明框预算法（b12 教训，硬纪律）**：gktip 来源说明四段合计行数须 ≤ ~29 行（版心 717pt ÷ 行高 24.5pt）——**写作试题.md 后、建批前先估行数**；超预算即压缩。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`＋孤需参宏 `\\([a-zA-Z]+\)`＋`&` 不在 `$…$`/`\[…\]` 内）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项；**每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character（构建审计三连）**。
- 沉淀纪律（b15–b23/phase3 全量 + b08–b16）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`（`\(...\)` 含 `&` 一律改 `$...$`；`$`/`$$`/`\[` 三者保护）；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；规范源反引号内禁裸 `$`/禁包 LaTeX 命令/禁空参数命令；↔ ∛ △ 等无字形/ToUnicode 缺符号处置照登记先例；**图标签一律绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**、分数型标签按源墨迹定位；**差分同引擎 pdftoppm＋ImageMagick `compare -metric AE`（脚本用 if 防 `&&` 链吞差异页）；跨构建比 md5 无意义（PDF 时间戳）——内容判定一律逐页像素差分**；审查代理 ≤8 页、分波 ≤5 支、524 限流分批 ≤4 支补派；**finalize-batch 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字（题头注记、存疑登记、来源说明）一律不印答案值与选项判定**；**行宽判据双口径（版心右缘：解析版 532.91／印刷版 549.92——是右缘坐标不是宽度；墨迹实测判定）**；**题图后段落齐左（含选项行、小问标号）＝全库同构接受类（记 pass+note，不判 fail）**；作答横线 `\gkblank` 2.2em（12pt 版 26.28pt／五号印刷版 23.16pt）；印刷版页眉盒 34.02bp 差与**页脚居页眉盒中心（左偏 17.1bp）**为全库同构留档；**印刷版 zihao=5：题名 15pt/副题 12pt**；**审查回执键名三变体全兼容**；**tabular 内 `\dfrac` 为临界构造——表内禁 displaystyle 分式（改斜线记法）；不动公共 md2tex**；审查代理中途回报可能为「中途稿级」错误结论（只信落盘 JSON＋主会话亲测）。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**的解析须流水式、答案单一答案行。
- 标点与记号口径以**广东理卷源页字体实测为准**（**本卷 17 字体含 CMMIB10**——向量粗斜体大概率存在，须转录独立判定；LJVORJ+CMMI7 与 NBEQIK+CMMIB10、IYBSXN+CMR5 的 ToUnicode 为 no，文本层可能缺失，像素为准）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 广东理卷 | `gk-2015-regular-guangdong-science` | `2015_广东卷_理科` | 待注册 | `1c3faab50a5d1fb2bdba424104c10910341e7362d222e018fb27e631578daa9a` | `ec54683e1f030bde8b66ccfe2b1edea4a5a8ea0a` | `普通高考/2015/2015广东理.pdf` | 2 |

## Review Focus

- 21 题结构核定（选择 1–8＋填空 9–15＋解答 16–21；题号连续）、无答案页（等级 D）。源内三个节头（一、选择题／二、填空题／三、解答题）；填空 9–12 在栏 1 节头下、13–15 在栏 2 顶部（无重复节头）。
- Q15 圆/切线几何图（AB 直径、AB=4、EC 切于 C、BC=1、过 O 作 BC 平行线交 EC 于 D 交 AC 于 P，标注 A/O/B/C/D/E/P）；Q18 立体图（三角形 PDC 与长方形 ABCD 垂直，PD=PC=4、AB=6、BC=3，E 为 CD 中点，F∈AB、G∈BC，AF=2FB、CG=2GB，标注 P/D/C/A/B/E/F/G）。
- Q16 平面向量 m=(√2/2, −√2/2)、n=(sin x, cos x)——**CMMIB10 粗斜体判定**；Q17 工人年龄表（36 行 4 组「编号/年龄」列＋系统抽样三小问）；Q18 二面角正切／线面角余弦；Q21 数列递推＋`ln n` 不等式（需分级估计）。
- 源为 LaTeX（CM 系）重排：句读为半角西文体系（按全库约定归一全角）；图形为纯矢量，坐标以内容流实测为准。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：cp 至 `.work/phase3-b17/source/2015广东理.pdf`，现场 sha256＝`1c3faab5…`；blob `ec54683e…` 在 34c13a6 实测相同（工作树 blob 同值）。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，119 行）。
- [x] 版式判读：A3 横向三栏书刊合排；p1（页脚 947）＝栏 1（标题「2015 普通高等学校招生考试 (广东卷理)」＋「一、选择题」1–8＋「二、填空题」9–12）／栏 2（填空 13–15 含 Q15 圆图＋「三、解答题」节头＋Q16）／栏 3（Q17 工人年龄表＋三小问）；p2（页脚 948）＝栏 1（Q18 立体图＋Q19）／栏 2（Q20）／栏 3（Q21）。LaTeX CM 系重排、全矢量、17 字体全嵌入、**含 CMMIB10**。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–8 选择）：`.work/phase3-b17/transcripts/partA.md`。
- [ ] 转录 B（Q9–21＋图表实测清单）：原单支挂起（30 分钟无产出，已停止），拆为 B1（Q9–17）＋B2（Q18–21＋精简图清单）：`.work/phase3-b17/transcripts/partB1.md`、`partB2.md`＋`.work/phase3-b17/figure-inventory.md`。
- [x] 盲解 A（Q1–8）：`.work/phase3-b17/blind/partA.md`（1D 2A 3D 4B 5A 6B 7C 8B）；盲解 B（Q9–21）：`.work/phase3-b17/blind/partB.md`（0 存疑；Q20 轨迹弧段、Q21 恒等式已由主会话独立复算）。
- [ ] **所有四代理 prompt 均含：不得读取任何他批/他卷产物（含 `.work/phase3-b12/`–`b16/`、`2015_广东卷_文科`、`2015_数学真题_广东文*` 等）。**

### Task 3 — Integrate and register

- [ ] 规范三件套（试题/答案要点/解析正文）+ 含解析占位；六项自检（`%`、空参数、反引号、CJK 入数学、孤需参宏、`&` 转义）＋（N）空格锚点检查；**说明框行数预算法先行**。
- [ ] TikZ 图源生成 + 探针目检（**绝对字号 10.5pt 定型**；源坐标换算回验与 600 dpi 目检＋判据灵敏度自证）。
- [ ] 注册 `phase3-b17`；provenance 三角色导入；extract-batch 派生。
- [ ] generate/short/editions 三连 write+check → build --formal（构建审计三连 → 修复轮 → 重建 → 差分 → 复审）。

### Task 4 — Build, review, and close

- [ ] 审查代理（1 图自查 + 分段并发 ≤8 页/段、分波 ≤5 支；524 限流时分批补派）→ 修复轮（如有）→ 重建 → 差分 → 复审。
- [ ] 审查回执填写（逐页×8 项）→ finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

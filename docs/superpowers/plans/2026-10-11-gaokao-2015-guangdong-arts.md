# 2015 广东文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 广东文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b15 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。A3 横向三栏书刊合排（印刷页码 **949/950**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **21 题（选择 1–10＋填空 11–15＋解答 16–21）**。

建模先例：`2015_山东卷_文科`（phase3-b14）、`2015_山东卷_理科`（phase3-b15）、`2015_安徽卷_文科`（phase3-b12）。

## Global Constraints

- 正式批次 `phase3-b16`；工作目录 `.work/phase3-b16/`。
- **并行会话**：他会话工作线（1997 上海等）在推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；现场核 blob `92da52358e0e3a279b3d6746dd15096597545544` 在 34c13a6 与本文件一致。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 949、p2 印 950）→ **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`、`.work/phase3-b13/`、`.work/phase3-b14/`、`.work/phase3-b15/`、`2015_安徽卷_*`、`2015_山东卷_*`、`2015_数学真题_安徽*`、`2015_数学真题_山东*` 等）；同书对照仅主会话事后互证用。**本批 广东理未做**——无同书配对在途，代理照常零参照。
- **说明框预算法（b12 教训，硬纪律）**：gktip 来源说明四段合计行数须 ≤ ~29 行（版心 717pt ÷ 行高 24.5pt）——**写作试题.md 后、建批前先估行数**；超预算即压缩。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`＋孤需参宏 `\\([a-zA-Z]+\)`＋`&` 不在 `$…$`/`\[…\]` 内）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项；**每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character（构建审计三连）**。
- 沉淀纪律（b15–b23/phase3 全量 + b08–b13）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`（`\(...\)` 含 `&` 一律改 `$...$`；`$`/`$$`/`\[` 三者保护）；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；规范源反引号内禁裸 `$`/禁包 LaTeX 命令/禁空参数命令；↔ ∛ △ 等无字形/ToUnicode 缺符号处置照登记先例；**图标签一律绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**、分数型标签按源墨迹定位；**差分同引擎 pdftoppm＋ImageMagick `compare -metric AE`（脚本用 if 防 `&&` 链吞差异页）；跨构建比 md5 无意义（PDF 时间戳）——内容判定一律逐页像素差分**；审查代理 ≤8 页、分波 ≤5 支、524 限流分批 ≤4 支补派；**finalize-batch 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字（题头注记、存疑登记、来源说明）一律不印答案值与选项判定**；**行宽判据双口径（版心右缘：解析版 532.91／印刷版 549.92——是右缘坐标不是宽度；墨迹实测判定）**；**题图后段落齐左（含选项行、小问标号）＝全库同构接受类（记 pass+note，不判 fail）**；作答横线 `\gkblank` 2.2em（12pt 版 26.28pt／五号印刷版 23.16pt）；印刷版页眉盒 34.02bp 差与**页脚居页眉盒中心（左偏 17.1bp）**为全库同构留档；**印刷版 zihao=5：题名 15pt/副题 12pt**；**审查回执键名三变体全兼容**；**tabular 内 `\dfrac` 为临界构造——表内禁 displaystyle 分式（改斜线记法）；不动公共 md2tex**；审查代理中途回报可能为「中途稿级」错误结论（只信落盘 JSON＋主会话亲测）。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**的解析须流水式、答案单一答案行。
- 标点与记号口径以**广东文卷源页字体实测为准**（待转录实测；**本卷 14 字体清单已见 pdffonts：无 CMMIB10**——向量记法以 \overrightarrow（TeX-vect10）为主，粗斜体是否存在须转录独立判定）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 广东文卷 | `gk-2015-regular-guangdong-arts` | `2015_广东卷_文科` | `src-a9cfb7624040e639d67a19c89fea581b80a75da4cbfab6255f2a6ccd0da68a84` | `0c27f1a08f837014066c636a3190b8fa7ad7e5a4494f204e60412293aea17e09` | `92da52358e0e3a279b3d6746dd15096597545544` | `普通高考/2015/2015广东文.pdf` | 2 |

## Review Focus

- 21 题结构核定（选择 1–10＋填空 11–15＋解答 16–21；题号连续）、无答案页（等级 D）。**源内仅三个节头（一、选择题／二、填空题／三、解答题），无「必做/选做」分节标注**——600 dpi 已复核栏 2 顶部与 Q13/Q14 交界，structure 按源记 `选择题 1–10／填空题 11–15／解答题 16–21`（照源不补分节）。
- Q15 圆/切线几何图（AB 直径、E 在延长线、CE 切线、AD⊥EC，标注 A/O/B/E/C/D）；Q17 频率分布直方图（组距轴 0.0125/0.011/0.0095/x/0.005/0.0025/0.002＋7 组区间＋三小问）；Q18 立体图（三角形 PDC 与长方形 ABCD 垂直，PD=PC=4、AB=6、BC=3，标注 P/D/C/A/B）。
- Q18(1)「BC∥平面 PDA」的「∥」疑似文本层丢失（渲染可见）——转录须以像素为准并登记。
- Q10 集合计数（card(E)+card(F)，四元组条件）；Q14 极坐标＋参数方程；Q16 三角恒等变换；Q19 数列递推；Q20 圆与轨迹；Q21 含绝对值的分段函数三小问。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：cp 至 `.work/phase3-b16/source/2015广东文.pdf`，现场 sha256＝`0c27f1a0…`（与 manifest artifact 逐字一致）；blob `92da5235…` 在 34c13a6 实测相同。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，114 行）。
- [x] 版式判读：A3 横向三栏书刊合排；p1（页脚 949）＝栏 1（标题「2015 普通高等学校招生考试 (广东卷文)」＋「一、选择题」1–10＋「二、填空题」节头）／栏 2（填空 11–15 含 Q15 圆图＋「三、解答题」节头＋Q16）／栏 3（Q17 频率分布直方图＋三小问）；p2（页脚 950）＝栏 1（Q18 立体图＋Q19）／栏 2（Q20）／栏 3（Q21）。LaTeX CM 系重排、全矢量、14 字体全嵌入、**无 CMMIB10**。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–10 选择）：`.work/phase3-b16/transcripts/partA.md`。
- [x] 转录 B（Q11–21＋图表实测清单）：`.work/phase3-b16/transcripts/partB.md`＋`.work/phase3-b16/figure-inventory.md`。
- [x] 盲解 A（Q1–10）：`.work/phase3-b16/blind/partA.md`；盲解 B（Q11–21）：`.work/phase3-b16/blind/partB.md`。
- [x] **所有四代理 prompt 均含：不得读取任何他批/他卷产物（含 `.work/phase3-b12/`–`b15/`、`2015_安徽卷_*`、`2015_山东卷_*` 等）。**

### Task 3 — Integrate and register

- [x] 规范三件套（试题/答案要点/解析正文）+ 含解析占位；六项自检（`%`、空参数、反引号、CJK 入数学、孤需参宏、`&` 转义）＋（N）空格锚点检查；**说明框行数预算法先行**。
- [x] TikZ 图源生成 + 探针目检（**绝对字号 10.5pt 定型**；源坐标换算回验与 600 dpi 目检＋判据灵敏度自证）。
- [x] 注册 `phase3-b16`；provenance 三角色导入；extract-batch 派生。
- [x] generate/short/editions 三连 write+check → build --formal（构建审计三连 → 修复轮 → 重建 → 差分 → 复审）。

### Task 4 — Build, review, and close

- [x] 审查代理（1 图自查 + 分段并发 ≤8 页/段、分波 ≤5 支；524 限流时分批补派）→ 修复轮（如有）→ 重建 → 差分 → 复审。
- [x] 审查回执填写（逐页×8 项）→ finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

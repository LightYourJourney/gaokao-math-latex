# 2015 山东文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 山东文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b13 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。A3 横向三栏书刊合排（印刷页码 **971/972**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **21 题（选择 1–10＋填空 11–15＋解答 16–21）**。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_安徽卷_文科`（phase3-b12）、`2015_安徽卷_理科`（phase3-b13，同书系列）。

## Global Constraints

- 正式批次 `phase3-b14`；工作目录 `.work/phase3-b14/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`（现场核：HEAD 已前移 266afe2，但 34c13a6 与本文件 2015 目录 diff 为空、blob 一致——冻结以 34c13a6 为准）；sha 与 manifest 逐字一致。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 971、p2 印 972）→ **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`、`.work/phase3-b13/`、`2015_安徽卷_文科/`、`2015_安徽卷_理科/`、`2015_数学真题_安徽文/理_*` 等）；文理对照与同书对照仅主会话事后互证用。**本批 山东理未做**——无同书配对在途，代理照常零参照。
- **说明框预算法（b12 教训，硬纪律）**：gktip 来源说明四段合计行数须 ≤ ~29 行（版心 717pt ÷ 行高 24.5pt）——**写作试题.md 后、建批前先估行数**；超预算即压缩。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`＋孤需参宏 `\\([a-zA-Z]+\)`＋`&` 不在 `$…$`/`\[…\]` 内）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项；**每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character（构建审计三连）**。
- 沉淀纪律（b15–b23/phase3 全量 + b08 + b09 + b10 + b11 + b12 + **b13**）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`（`\(...\)` 含 `&` 一律改 `$...$`；`$`/`$$`/`\[` 三者保护）；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；规范源反引号内禁裸 `$`/禁包 LaTeX 命令/禁空参数命令；↔ ∛ △ 等无字形/ToUnicode 缺符号处置照登记先例；**图标签一律绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**、分数型标签按源墨迹定位；**差分同引擎 pdftoppm＋ImageMagick `compare -metric AE`（脚本用 if 防 `&&` 链吞差异页）；跨构建比 md5 无意义（PDF 时间戳）——内容判定一律逐页像素差分**；审查代理 ≤8 页、分波 ≤5 支、524 限流分批 ≤4 支补派；**finalize-batch 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字（题头注记、存疑登记、来源说明）一律不印答案值与选项判定**；**行宽判据双口径（版心右缘：解析版 532.91／印刷版 549.92——是右缘坐标不是宽度；墨迹实测判定）**；**题图后段落齐左（含选项行、小问标号）＝全库同构接受类（记 pass+note，不判 fail）**；作答横线 `\gkblank` 2.2em（12pt 版 26.28pt／五号印刷版 23.16pt）；印刷版页眉盒 34.02bp 差与**页脚居页眉盒中心（左偏 17.1bp）**为全库同构留档；**印刷版 zihao=5：题名 15pt/副题 12pt**；**审查回执键名三变体全兼容**；**tabular 内 `\dfrac` 为临界构造——表内禁 displaystyle 分式（改斜线记法）；不动公共 md2tex**；审查代理中途回报可能为「中途稿级」错误结论（只信落盘 JSON＋主会话亲测）。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**的解析须流水式、答案单一答案行。
- 标点与记号口径以**山东文卷源页字体实测为准**（待转录实测；**本卷 16 字体清单已见 pdffonts：无 CMMIB10**——粗斜体向量是否存在须由转录独立判定，不得沿用他卷）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 山东文卷 | `gk-2015-regular-shandong-arts` | `2015_山东卷_文科` | `src-894218c6b81612f02ef84a1bba2b0ec1048975042318880eb09b03cd5dc46ac0` | `cc2c1610f06eb6ff1088cf8d24326eff1e87f20f1d16c93f57ce46859571221d` | `cbc352e5585bac7b6f607826df87ee6c7c590846` | `普通高考/2015/2015山东文.pdf` | 2 |

## Review Focus

- 21 题结构核定（选择 1–10＋填空 11–15＋解答 16–21；题号连续）、无答案页（等级 D）。
- Q6 茎叶图（甲乙两组、`9 8 6 | 2 8 9` 与 `1 1 3 | 0 1 2` —— 逐位照录）；Q11 程序框图（开始／输入 x／菱形 x<2／是→x=x+1 回边／否→y=3x²+1／输出 y／结束——与安徽卷框图不同款，逐 path 实测定）；Q16 调查表（2×2 表，格式待判）；Q18 三棱台 DEF-ABC（含虚线与 E/G/H 位置）。
- Q5 逆否命题四选项（长文本选项）；Q10 分段函数嵌套 f(f(5/6))；Q20 三小问（切线/零点存在性/min 函数）；Q21 椭圆两小问含 ①②。
- **本卷无 CMMIB10**（pdffonts 实测）——向量与长箭头记法须照源实测（\overrightarrow 类为 TeX-vect10）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：cp 至 `.work/phase3-b14/source/2015山东文.pdf`，现场 sha256＝`cc2c1610…`（与 manifest 未绑定源逐字一致）；blob `cbc352e5…` 在 34c13a6 实测相同（HEAD 前移但 2015 目录 diff 为空）。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，125 行）。
- [x] 版式判读：A3 横向三栏书刊合排；p1（页脚 971）＝栏 1（标题「2015 普通高等学校招生考试 (山东卷文)」＋「一、选择题」1–7 含 Q6 茎叶图）／栏 2（Q8–10＋「二、填空题」11–15 含 Q11 程序框图＋「三、解答题」节头）／栏 3（Q16 含调查表＋(1)(2)＋Q17）；p2（页脚 972）＝栏 1（Q18 三棱台图＋Q19）／栏 2（Q20）／栏 3（Q21）。LaTeX CM 系重排、全矢量、16 字体全嵌入、**无 CMMIB10**。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [ ] 转录 A（Q1–10 选择，含 Q6 茎叶图、Q11 前判别）：`.work/phase3-b14/transcripts/partA.md`。
- [ ] 转录 B（Q11–21＋图表实测清单）：`.work/phase3-b14/transcripts/partB.md`＋`.work/phase3-b14/figure-inventory.md`。
- [ ] 盲解 A（Q1–10）：`.work/phase3-b14/blind/partA.md`；盲解 B（Q11–21）：`.work/phase3-b14/blind/partB.md`。
- [ ] **所有四代理 prompt 均含：不得读取任何他批/他卷产物（含 `.work/phase3-b12/`、`.work/phase3-b13/`、`2015_安徽卷_文科/`、`2015_安徽卷_理科/` 等）。**

### Task 3 — Integrate and register

- [ ] 规范三件套（试题/答案要点/解析正文）+ 含解析占位；六项自检（`%`、空参数、反引号、CJK 入数学、孤需参宏、`&` 转义）＋（N）空格锚点检查；**说明框行数预算法先行**。
- [ ] TikZ 图源生成 + 探针目检（**绝对字号 10.5pt 定型**；源坐标换算回验与 600 dpi 目检＋判据灵敏度自证）。
- [ ] 注册 `phase3-b14`；provenance 三角色导入；extract-batch 派生。
- [ ] generate/short/editions 三连 write+check → build --formal（构建审计三连 → 修复轮 → 重建 → 差分 → 复审）。

### Task 4 — Build, review, and close

- [ ] 审查代理（1 图自查 + 分段并发 ≤8 页/段、分波 ≤5 支；524 限流时分批补派）→ 修复轮（如有）→ 重建 → 差分 → 复审。
- [ ] 审查回执填写（逐页×8 项）→ finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

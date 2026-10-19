# 2015 湖南文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 湖南文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b21 批次。A3 横向三栏书刊合排（印刷页码 **957/958**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **21 题（选择 1–10＋填空 11–15＋解答 16–21）**。**3 幅 TikZ 图（5 面板）**：Q5 程序框图、Q10 三视图（正视图/侧视图/俯视图）、Q18 三棱柱；另 Q2 茎叶图为竖线分隔的表格（array，非 TikZ）。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_湖北卷_理科`（phase3-b21）、`2015_湖北卷_文科`（phase3-b20）。

## Global Constraints

- 正式批次 `phase3-b22`；工作目录 `.work/phase3-b22/`。
- **并行会话**：他会话工作线在推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；现场核 blob `7994337cfe59dca41ee903bb3b6dd9b0d05e7904`（sha256 `48dc0c67…`）。
- 源 2 页 A3 横向三栏，页脚 **957/958**，**无答案页** → **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`–`.work/phase3-b22/`、各 `2015_*卷_*` 项目目录与 `2015_数学真题_*`）；同书对照仅主会话事后互证。
- **说明框预算法**：gktip 来源说明四段合计 ≤ ~29 行；写作试题.md 后、建批前先估行数。
- **规范源写裸 `%`（仅文本/`\(...\)`；数学 `$...$`/`\[...\]` 内须 `\%`）**；六项自检＋（N）空格锚点；每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character。
- 沉淀纪律：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；反引号内禁裸 `$`/禁包 LaTeX 命令；**图标签绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**；**差分同引擎 pdftoppm＋`compare -metric AE`（用 if 防 `&&` 链）**；审查 ≤8 页/段、≤5 并发、524 分批补派；**finalize 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字禁印答案值与选项判定**；行宽双口径（解析/试题/简答右缘 532.91／印刷 549.92，判溢出用 600dpi 墨迹）；题图后段落齐左＝接受类；`\gkblank` 2.2em；印刷版页眉盒 34.02bp／页脚左偏 17.1bp／zihao=5 题名 15pt 副题 12pt；回执键名三变体全兼容；**tabular 内 displaystyle 分式须用 `\rule{0pt}{1.5em}`＋`\\[0.55em]` 撑行高/行深（b20 定型）**；**cases 行距 `\\[6pt]` 才达源刊 3.7pt（b21 定型）**；只信落盘 JSON＋主会话亲测。
- **答案要点禁「① 答案：」式**；选择答案纯字母；证明类小问写「成立（…）」。
- 标点与记号口径以**湖南文卷源页字体实测为准**：本卷 14 字体含 **TeX-vect10**、**无 CMMIB10**、无 STKaiti；LJVORJ+CMMI7、JBCXHN+TeX-vect10 的 ToUnicode=no。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 湖南文卷 | `gk-2015-regular-hunan-arts` | `2015_湖南卷_文科` | 注册时生成 | `48dc0c6771ccea8291a3ac94336dd89a8b4ff89fa6baceaa76585c349582a074` | `7994337cfe59dca41ee903bb3b6dd9b0d05e7904` | `普通高考/2015/2015湖南文.pdf` | 2 |

## Review Focus

- 21 题结构核定（选择 1–10＋填空 11–15＋解答 16–21）；无答案页（等级 D）。
- **Q2 茎叶图**（竖线分隔的 3 行表格：13/14/15 三行，叶为个位数，共 35 个成绩）；**Q5 程序框图**（开始/输入 n/循环 S=S+1/((2i−1)(2i+1))/i=i+1/判断 i>n?/输出 S/结束）；**Q10 三视图**（正视图、侧视图为等腰三角形 3-3-2，俯视图为圆，含尺寸标注）；**Q18 三棱柱 ABC–A₁B₁C₁**（底面正三角形边长 2，E、F 分别为 BC、CC₁ 中点，实/虚线）。
- Q1 复数、Q4 线性规划、Q6 双曲线渐近线、Q7 最值 \(1/a+2/b=\sqrt{ab}\)、Q9 圆上动点向量最值、Q11 集合、Q12 极坐标、Q13 直线与圆、Q14 零点区间、Q15 三角函数；解答 Q16 概率、Q17 解三角形、Q19 数列、Q20 抛物线与椭圆、Q21 函数极值点与数列不等式。
- 源为 LaTeX（CM 系）重排：句读半角西文体系（归一全角）；图形纯矢量，坐标以内容流实测为准。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：`.work/phase3-b22/source/2015湖南文.pdf`；sha256 `48dc0c67…`、blob `7994337c…` 在 34c13a6 与工作树一致。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，114 行）。
- [x] 版式判读：A3 三栏书刊合排；p1（页脚 957）＝栏 1 标题「一、选择题」1–6（Q2 茎叶图、Q5 程序框图）；栏 2 第 6 题选项续＋7–10（Q10 三视图）＋「二、填空题」11–15；栏 3 第 16 题＋第 17 题（「三、解答题」节头在栏 2 底）；p2（页脚 958）＝栏 1 第 18 题（三棱柱图）＋第 19 题；栏 2 第 20 题；栏 3 第 21 题。LaTeX CM 系重排、全矢量、14 字体嵌入、**含 TeX-vect10、无 CMMIB10**。

### Task 2 — Transcribe (3 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–10）：`.work/phase3-b22/transcripts/partA.md`。
- [x] 转录 B1（Q11–15）：`partB1.md`；转录 B2（Q16–21＋全图清单）：`partB2.md`＋`figure-inventory.md`。
- [x] 盲解 A（Q1–10）、盲解 B（Q11–21）：`.work/phase3-b22/blind/`。
- [x] 所有代理 prompt 含隔离纪律（不得读取他批/他卷产物与本批他人输出）。

### Task 3 — Integrate and register

- [x] 规范三件套＋含解析占位；六项自检＋（N）锚点；说明框预算。
- [x] 3 图 TikZ 图源＋探针（绝对字号 10.5pt；残差 <0.05pt、600dpi 墨迹、灵敏度自证）。
- [x] 注册 `phase3-b22`（rev 4433）；provenance 三角色（rev 4434）；extract-batch 派生。
- [x] generate/short/editions 三连 → build --formal（审计三连→修复轮→重建→差分→复审）。**首建**：6/27/8/19 页、0 警告。

### Task 4 — Build, review, and close

- [x] 审查（图自查＋分段 ≤8 页、≤5 并发）→ 修复轮 → 重建 → 差分 → 复审。
- [x] 回执归集 → finalize → 报告 → 全量测试 → 清理 → 显式路径提交（不 push）。

#### 修复轮记录（phase3-b22）

审查共 9 段（试题 1＋解析 4＋简答 1＋印刷 3，73 页），首轮 **5 处 fail**，全部修复并复审通过。

| # | 版本·页 | 检查项 | 现象（实测） | 处置 |
|---|---|---|---|---|
| 1 | 解析版 p21 | pagination_whitespace | 「解析」＋「(1)」孤悬页底，Q18(1) 正文自 p22 起（页尾余 94.3pt） | 规范源 Q18 解析前加 `\enlargethispage{2\baselineskip}`（先试 8 行 `\Needspace`：修好但页数 27→28、全部下游页码回执作废，弃用） |
| 2 | 印刷版 p1 | option_formula_alignment | 说明框 ③ 分母与「第 10 题」bbox 重叠 0.3pt、⑤ 分母 b 与下行白隙 <0.1pt | 说明框首行 `\setlength{\lineskiplimit}{3pt}\setlength{\lineskip}{4pt}`（仅 `\lineskip{3pt}` 不够：⑤ 所在行自然行距尚 ≥ 阈值，须同时抬 `\lineskiplimit` 才会切到 `\lineskip`） |
| 3 | 印刷版 p2 / 解析版 p5 | option_formula_alignment | 第 1 题题干 \(\dfrac{(1-i)^2}{z}\) 分母 z 悬于选项行 (A) \(1+i\) 的 i 之上（0.85pt，呈上标错觉） | 试题源第 1 题题干末加 `\par\smallskip`（同源一处修好题面版与解析版两处） |
| 4 | 印刷版 p7 | option_formula_alignment | 第 5 题选项 (A) \(\dfrac67\) 分母 7 与「解析」的「解」顶 0.85pt | 试题源第 5 题选项行末加 `\par\smallskip` |

**复审（fix-A/B/C/D，共 22 页重验）**：印刷版 p1–7、解析版 p5–7＋p21–22、试题/简答版 p1–3、四版 p1 —— 全 pass，0 fail。

**终验口径（主会话，1200 dpi 像素行剖面＋分式列窗口）**：③ 分母→下行 = **4.38pt**（试题/解析/简答）／**4.02pt**（印刷）；⑤ 分母 b→下行 = **3.90pt**（前三种）／**4.38pt**（印刷），均 ≥1.5pt 且 bbox 无重叠。全页另有两处 <1.5pt 相邻墨迹带（0.48pt／1.38pt），裁片核验为分式本体内部「分子或分母 ↔ 分数线」的 TeX 度量间隙，非行间碰撞，按既有 0.96pt 低危留档先例处理。

**改动局部性证明（A/B 编译差分）**：以 `\lineskiplimit` 修复前后的两份源分别编译四版，逐页 `compare -metric AE`：仅 **p1** 有差异（差分区域完全落在说明框内），**其余全部页面 AE=0**；四版页数 6／27／8／19 不变，四份 `.log` 的 Overfull／Underfull／Missing character 均为 0。

**工具约束**：本批终验期间 subagent 遭遇中转站日限额 429（`api key 日限额已用完`），四版 p1 终验改由主会话自测完成（`fix-D.json` 注明口径）。


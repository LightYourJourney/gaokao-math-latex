# 2015 浙江文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 浙江文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b17 批次。A3 横向三栏书刊合排（印刷页码 **991/992**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **20 题（选择 1–8＋填空 9–15＋解答 16–20）**。**5 幅图**：Q2 三视图、Q5 四函数图象、Q7 斜线与平面、Q18 三棱柱、Q19 抛物线＋圆。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_广东卷_理科`（phase3-b17）、`2015_山东卷_理科`（phase3-b15）。

## Global Constraints

- 正式批次 `phase3-b18`；工作目录 `.work/phase3-b18/`。
- **并行会话**：他会话工作线在推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；现场核 blob `ee215528ed77f0c70cc5382c708dbb2c6b57ea75`（sha256 `a0e49283…`）。
- 源 2 页 A3 横向三栏，页脚 **991/992**，**无答案页** → **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`–`.work/phase3-b17/`、各 `2015_*卷_*` 项目目录与 `2015_数学真题_*`）；同书对照仅主会话事后互证用。本批**浙江理未做**——无同书配对在途，代理照常零参照。
- **说明框预算法**：gktip 来源说明四段合计 ≤ ~29 行；写作试题.md 后、建批前先估行数。
- **规范源写裸 `%`（仅文本/`\(...\)`；数学 `$...$`/`\[...\]` 内须 `\%`）**；六项自检＋（N）空格锚点；每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character。
- 沉淀纪律：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；反引号内禁裸 `$`/禁包 LaTeX 命令；**图标签绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**；**差分同引擎 pdftoppm＋`compare -metric AE`（用 if 防 `&&` 链）**；审查 ≤8 页/段、≤5 并发、524 分批补派；**finalize 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字禁印答案值与选项判定**；行宽双口径（解析/试题/简答右缘 532.91／印刷 549.92，判溢出用 600dpi 墨迹）；题图后段落齐左＝接受类；`\gkblank` 2.2em；印刷版页眉盒 34.02bp／页脚左偏 17.1bp／zihao=5 题名 15pt 副题 12pt；回执键名三变体全兼容；**tabular 内禁 displaystyle 分式**；只信落盘 JSON＋主会话亲测。
- **答案要点禁「① 答案：」式**；选择答案纯字母；证明类小问写「成立（…）」。
- 标点与记号口径以**浙江文卷源页字体实测为准**：本卷 17 字体含 **CMMIB10** 与 **STKaiti**（后者用途待转录实测）；LJVORJ+CMMI7、NBEQIK+CMMIB10、IYBSXN+CMR5 的 ToUnicode=no。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 浙江文卷 | `gk-2015-regular-zhejiang-arts` | `2015_浙江卷_文科` | `src-eae597f2…`（待注册核） | `a0e49283fb3d086029ec3c96de7e96cc6118365378ea0a24273c6f58285ec977` | `ee215528ed77f0c70cc5382c708dbb2c6b57ea75` | `普通高考/2015/2015浙江文.pdf` | 2 |

## Review Focus

- 20 题结构核定（选择 1–8＋填空 9–15＋解答 16–20）；无答案页（等级 D）。
- **Q2 三视图**（正/侧/俯，尺寸 2/2/2，选项体积 8、12、32/3、40/3）；**Q5 四函数图象选项**（\(f(x)=x-\frac1x\cos x\)，\(-π\leqslant x\leqslant π\) 且 \(x\neq0\)）；**Q7 斜线段与平面 α**（AB 与 α 成 60°，∠PAB=30°，P 轨迹）；**Q18 三棱柱**（∠BAC=90°、AB=AC=2、AA₁=4、A₁ 射影为 BC 中点、D 为 B₁C₁ 中点）；**Q19 抛物线 \(y=\frac14x^2\)＋圆 \(x^2+(y-1)^2=1\)**（过 P(t,0) 的 PA、PB 分别相切）。
- Q12 分段函数（\(x^2\)，\(x\leqslant1\)；\(x+\frac6x-6\)，\(x>1\)）文本层错位，须像素复核；Q15 椭圆离心率；Q20 二次函数零点与范围。
- 源为 LaTeX（CM 系）重排：句读半角西文体系（归一全角）；图形纯矢量，坐标以内容流实测为准。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：`.work/phase3-b18/source/2015浙江文.pdf`；sha256 `a0e49283…`、blob `ee215528…` 在 34c13a6 与工作树一致。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，101 行）。
- [x] 版式判读：A3 三栏书刊合排；p1（页脚 991）＝栏 1「一、选择题」1–8；栏 2 Q5 图象选项/Q6/Q7/Q8＋「二、填空题」9–15；栏 3「三、解答题」16–17；p2（页脚 992）＝栏 1 Q18；栏 2 Q19；栏 3 Q20。LaTeX CM 系重排、全矢量、17 字体嵌入、**含 CMMIB10 与 STKaiti**。

### Task 2 — Transcribe (3 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–8）：`.work/phase3-b18/transcripts/partA.md`。
- [x] 转录 B1（Q9–17）：`partB1.md`；转录 B2（Q18–20＋5 图清单）：`partB2.md`＋`figure-inventory.md`。
- [x] 盲解 A（Q1–8）、盲解 B（Q9–20）：`.work/phase3-b18/blind/`。
- [x] 所有代理 prompt 含隔离纪律（不得读取他批/他卷产物与本批他人输出）。

### Task 3 — Integrate and register

- [x] 规范三件套＋含解析占位；六项自检＋（N）锚点；说明框预算。
- [x] 5 图 TikZ 图源＋探针（绝对字号 10.5pt；残差 <0.05pt、600dpi 墨迹、灵敏度自证）。
- [x] 注册 `phase3-b18`；provenance 三角色；extract-batch 派生。
- [x] generate/short/editions 三连 → build --formal（审计三连→修复轮→重建→差分→复审）。

### Task 4 — Build, review, and close

- [x] 审查（图自查＋分段 ≤8 页、≤5 并发）→ 修复轮 → 重建 → 差分 → 复审。
- [x] 回执归集 → finalize → 报告 → 全量测试 → 清理 → 显式路径提交（不 push）。

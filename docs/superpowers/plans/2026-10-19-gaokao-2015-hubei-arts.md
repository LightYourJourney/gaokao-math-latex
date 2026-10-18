# 2015 湖北文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 湖北文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b19 批次。A3 横向三栏书刊合排（印刷页码 **953/954**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **22 题（选择 1–10＋填空 11–17＋解答 18–22）**。**5 幅图（6 面板）**：Q14 频率分布直方图、Q15 山高示意图、Q16 圆与坐标轴、Q20 阳马、Q22 作图工具（①② 两面板）。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_浙江卷_理科`（phase3-b19）、`2015_浙江卷_文科`（phase3-b18）。

## Global Constraints

- 正式批次 `phase3-b20`；工作目录 `.work/phase3-b20/`。
- **并行会话**：他会话工作线在推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；现场核 blob `a96e1415dc9986206afc24b845f083170fbe020b`（sha256 `801e7333…`）。
- 源 2 页 A3 横向三栏，页脚 **953/954**，**无答案页** → **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`–`.work/phase3-b19/`、各 `2015_*卷_*` 项目目录与 `2015_数学真题_*`）；同书对照仅主会话事后互证用。**本卷同省配对 2015 湖北理未做**——无同书配对在途，代理照常零参照。
- **说明框预算法**：gktip 来源说明四段合计 ≤ ~29 行；写作试题.md 后、建批前先估行数。
- **规范源写裸 `%`（仅文本/`\(...\)`；数学 `$...$`/`\[...\]` 内须 `\%`）**；六项自检＋（N）空格锚点；每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character。
- 沉淀纪律：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；反引号内禁裸 `$`/禁包 LaTeX 命令；**图标签绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**；**差分同引擎 pdftoppm＋`compare -metric AE`（用 if 防 `&&` 链）**；审查 ≤8 页/段、≤5 并发、524 分批补派；**finalize 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字禁印答案值与选项判定**；行宽双口径（解析/试题/简答右缘 532.91／印刷 549.92，判溢出用 600dpi 墨迹）；题图后段落齐左＝接受类；`\gkblank` 2.2em；印刷版页眉盒 34.02bp／页脚左偏 17.1bp／zihao=5 题名 15pt 副题 12pt；回执键名三变体全兼容；**tabular 内禁 displaystyle 分式**；只信落盘 JSON＋主会话亲测。
- **答案要点禁「① 答案：」式**；选择答案纯字母；证明类小问写「成立（…）」。
- 标点与记号口径以**湖北文卷源页字体实测为准**：本卷 15 字体含 **TeX-vect10**（向量箭头，Q11 的 \(\overrightarrow{OA}\) 等）、**STKaiti**、**无 CMMIB10**；JBCXHN+TeX-vect10、LJVORJ+CMMI7 的 ToUnicode=no。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 湖北文卷 | `gk-2015-regular-hubei-arts` | `2015_湖北卷_文科` | `src-460ef6c787e241f6d6d8254b163543595c3608e78ea25d3ff7eabde49035bf2e` | `801e73338b6c4c747cc76b14e167d590a34e0b5a13a47719e5ee6cd4337e4cd2` | `a96e1415dc9986206afc24b845f083170fbe020b` | `普通高考/2015/2015湖北文.pdf` | 2 |

## Review Focus

- 22 题结构核定（选择 1–10＋填空 11–17＋解答 18–22）；无答案页（等级 D）。
- **Q14 频率分布直方图**（组距刻度 a、2.5、2.0、1.5、0.8、0.2；横轴 0–0.9；频率/组距 轴；金额/万元）；**Q15 山高示意图**（D 山顶、C 垂足、B/A 公路点，虚线视线；30°/75°/仰角 30°）；**Q16 圆**（x 轴切于 T(1,0)、y 轴交 A/B、|AB|=2）；**Q20 阳马 P–ABCD**（PD⊥底面、PD=CD、E 为 PC 中点，实/虚线）；**Q22 作图工具**（① 机械连杆 O/N/D/M；② 坐标系中曲线 C）。
- Q1 指数 \(i^{607}\) 的上标须像素复核；Q7 符号函数 cases；Q12 线性约束 cases；Q18 五点法表格（tabular）；Q19 数列；Q21 奇偶函数不等式；Q22 曲线 C 与两定直线。
- 源为 LaTeX（CM 系）重排：句读半角西文体系（归一全角）；图形纯矢量，坐标以内容流实测为准。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：`.work/phase3-b20/source/2015湖北文.pdf`；sha256 `801e7333…`、blob `a96e1415…` 在 34c13a6 与工作树一致。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，139 行）。
- [x] 版式判读：A3 三栏书刊合排；p1（页脚 953）＝栏 1「一、选择题」1–8；栏 2 第 9–10 题＋「二、填空题」11–15（Q14 直方图、Q15 山高图）；栏 3 第 16–17 题＋「三、解答题」18（五点法表）；p2（页脚 954）＝栏 1 第 19 题＋第 20 题（阳马图）；栏 2 第 21 题；栏 3 第 22 题（两面板图）。LaTeX CM 系重排、全矢量、15 字体嵌入、**含 TeX-vect10 与 STKaiti、无 CMMIB10**。

### Task 2 — Transcribe (3 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–10）：`.work/phase3-b20/transcripts/partA.md`。
- [x] 转录 B1（Q11–17，含 Q14/Q15/Q16 图清单）：`partB1.md`；转录 B2（Q18–22＋全 5 图清单）：`partB2.md`＋`figure-inventory.md`。
- [x] 盲解 A（Q1–10）、盲解 B（Q11–22）：`.work/phase3-b20/blind/`。
- [x] 所有代理 prompt 含隔离纪律（不得读取他批/他卷产物与本批他人输出）。

### Task 3 — Integrate and register

- [x] 规范三件套＋含解析占位；六项自检＋（N）锚点；说明框预算。
- [x] 5 图 TikZ 图源＋探针（绝对字号 10.5pt；残差 <0.05pt、600dpi 墨迹、灵敏度自证）。
- [x] 注册 `phase3-b20`；provenance 三角色；extract-batch 派生。
- [x] generate/short/editions 三连 → build --formal（审计三连→修复轮→重建→差分→复审）。

### Task 4 — Build, review, and close

- [x] 审查（图自查＋分段 ≤8 页、≤5 并发）→ 修复轮 → 重建 → 差分 → 复审。
- [x] 回执归集 → finalize → 报告 → 全量测试 → 清理 → 显式路径提交（不 push）。

**修复轮记录**：审查发现 Q18「五点法」表行高不足（分式分母压表线，四版同表共 6 处）。修复：首列 `\rule{0pt}{1.5em}` 抬行高、含分式两行 `\\[0.55em]` 控行深（保留 `\dfrac`，与源表行高一致）。像素差分确定变化页 10 处（试题 p5/p6、解析 p5/p6/p21/p26、简答 p5/p6、印刷 p4/p17）；其中解析 p26 的 24 像素差为回链「题目见第 5 页→第 6 页」的联动更新。定向复审 10/10 pass；四版 0 警告、页数不变（6/28/8/22）。全量测试 1357 项，baseline 同款 1 failure（缓存快照）+1 error（1977 上海卷）。

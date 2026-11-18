# 2015 湖北理卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 湖北理科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b20 批次。A3 横向三栏书刊合排（印刷页码 **951/952**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **22 题（选择 1–10＋填空 11–16＋解答 17–22）**。**6 幅图**：Q4 正态分布密度曲线（两条曲线均为实线；X 峰值更高、Y 更矮更宽）、Q13 山高示意图、Q14 圆与单位圆（切线/割线几何）、Q15 圆切线割线（PA 切、PBC 割、BC=3PB）、Q19 阳马（含 F 与 EF⊥PB）、Q21 作图工具（①② 两面板）。

建模先例：`2015_湖北卷_文科`（phase3-b20）、`2015_浙江卷_理科`（phase3-b19）。

## Global Constraints

- 正式批次 `phase3-b21`；工作目录 `.work/phase3-b21/`。
- **并行会话**：他会话工作线在推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；现场核 blob `03be61cadb179cacb55c63463a661b5ffd4fa16c`（sha256 `66e68220…`）。
- 源 2 页 A3 横向三栏，页脚 **951/952**，**无答案页** → **答案证据等级 D**（解析全由盲解撰写）。
- **隔离纪律**：转录/盲解代理不得读取任何他批/他卷产物（全路径面，含 `.work/phase3-b12/`–`.work/phase3-b21/`、各 `2015_*卷_*` 项目目录与 `2015_数学真题_*`）；**本卷同省配对 2015 湖北文刚收官，严禁代理参照其任何产物**；同书对照仅主会话事后互证。
- **说明框预算法**：gktip 来源说明四段合计 ≤ ~29 行；写作试题.md 后、建批前先估行数。
- **规范源写裸 `%`（仅文本/`\(...\)`；数学 `$...$`/`\[...\]` 内须 `\%`）**；六项自检＋（N）空格锚点；每次 build 后 grep 四版 log 的 Overfull/Underfull/Missing character。
- 沉淀纪律：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学（`\text{}`；显示式 `\text{CJK␣}` 尾随空格写 `\text{CJK}\ `）；反引号内禁裸 `$`/禁包 LaTeX 命令；**图标签绝对字号 `\fontsize{10.5pt}{12.6pt}\selectfont`＋`inner sep=0`**；**差分同引擎 pdftoppm＋`compare -metric AE`（用 if 防 `&&` 链）**；审查 ≤8 页/段、≤5 并发、524 分批补派；**finalize 先于 check-batch**；not_applicable 必写理由；**纯题面版说明文字禁印答案值与选项判定**；行宽双口径（解析/试题/简答右缘 532.91／印刷 549.92，判溢出用 600dpi 墨迹）；题图后段落齐左＝接受类；`\gkblank` 2.2em；印刷版页眉盒 34.02bp／页脚左偏 17.1bp／zihao=5 题名 15pt 副题 12pt；回执键名三变体全兼容；**tabular 内 displaystyle 分式须用 `\rule{0pt}{1.5em}`＋`\\[0.55em]` 撑行高/行深（b20 定型）**；只信落盘 JSON＋主会话亲测。
- **答案要点禁「① 答案：」式**；选择答案纯字母；证明类小问写「成立（…）」。
- 标点与记号口径以**湖北理卷源页字体实测为准**：本卷 17 字体含 **TeX-vect10**（向量箭头）、**STKaiti**、**CMMI5/CMR5**、**无 CMMIB10**；JBCXHN+TeX-vect10、LJVORJ+CMMI7、IYBSXN+CMR5、BJXHNA+CMMI5 的 ToUnicode=no。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 湖北理卷 | `gk-2015-regular-hubei-science` | `2015_湖北卷_理科` | 注册时生成 | `66e6822009bdfd8f9a5a4adf4dd3f7564fc74d8fa09906c271dc6c6a5b31a66f` | `03be61cadb179cacb55c63463a661b5ffd4fa16c` | `普通高考/2015/2015湖北理.pdf` | 2 |

## Review Focus

- 22 题结构核定（选择 1–10＋填空 11–16＋解答 17–22）；无答案页（等级 D）。
- **Q4 正态分布图**（两条钟形曲线 X 实线、Y 虚线，μ/σ 关系，y 轴与 O）；**Q13 山高图**（D 山顶、C 垂足、B/A 公路点，虚线视线；30°/75°/仰角 30°）；**Q14 圆图**（圆 C 切 x 轴于 T(1,0)、交 y 轴于 A/B、|AB|=2；单位圆 O 与 M/N）；**Q15 圆切线割线**（PA 切于 A，PBC 割线，BC=3PB）；**Q19 阳马 P–ABCD**（PD⊥底面、PD=CD、E 为 PC 中点、EF⊥PB 于 F，实/虚线）；**Q21 作图工具**（① 机械连杆 O/N/D/M；② 坐标系中曲线 C）。
- Q1 指数 \(i^{607}\) 的共轭复数；Q5 等比数列充分/必要条件；Q6 符号函数复合；Q10 高斯函数 [t]、[t²]…；Q17 五点法表格（tabular）＋平移对称中心；Q18 数列；Q19 二面角；Q20 线性规划/概率；Q22 数列不等式。
- 源为 LaTeX（CM 系）重排：句读半角西文体系（归一全角）；图形纯矢量，坐标以内容流实测为准。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：`.work/phase3-b21/source/2015湖北理.pdf`；sha256 `66e68220…`、blob `03be61ca…` 在 34c13a6 与工作树一致。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi）；`source-text.txt`（-layout，146 行）。
- [x] 版式判读：A3 三栏书刊合排；p1（页脚 951）＝栏 1「一、选择题」1–6（Q4 正态曲线图）；栏 2 第 7–10 题＋「二、填空题」11–14（Q13 山高图、Q14 圆图）；栏 3 Q14(1)(2) 续＋15–16＋「三、解答题」17（五点法表）；p2（页脚 952）＝栏 1 第 18 题＋第 19 题（阳马图）；栏 2 第 20 题＋第 21 题（两面板图）；栏 3 第 22 题。LaTeX CM 系重排、全矢量、17 字体嵌入、**含 TeX-vect10 与 STKaiti、无 CMMIB10**。

### Task 2 — Transcribe (3 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–10）：`.work/phase3-b21/transcripts/partA.md`。
- [x] 转录 B1（Q11–16，含 Q13/Q14/Q15 图清单）：`partB1.md`；转录 B2（Q17–22＋全 6 图清单）：`partB2.md`＋`figure-inventory.md`。
- [x] 盲解 A（Q1–10）、盲解 B（Q11–22）：`.work/phase3-b21/blind/`。
- [x] 所有代理 prompt 含隔离纪律（不得读取他批/他卷产物与本批他人输出）。

### Task 3 — Integrate and register

- [x] 规范三件套＋含解析占位；六项自检＋（N）锚点；说明框预算。
- [x] 6 图 TikZ 图源＋探针（绝对字号 10.5pt；残差 <0.05pt、600dpi 墨迹、灵敏度自证）。
- [x] 注册 `phase3-b21`（rev 4420）；provenance 三角色（rev 4421）；extract-batch 派生。
- [x] generate/short/editions 三连 → build --formal（审计三连→修复轮→重建→差分→复审）。**生成期修复**：Q20 分布列显示式超宽 94.75pt → 源级拆为两行；Q19 验证段 Underfull → 坐标设置改行间式；重建后四版 0 警告（6/34/8/25 页）。

### Task 4 — Build, review, and close

- [x] 审查（图自查＋分段 ≤8 页、≤5 并发）→ 修复轮 → 重建 → 差分 → 复审。
- [x] 回执归集 → finalize → 报告 → 全量测试 → 清理 → 显式路径提交（不 push）。

**审查与修复轮记录**：11 段（试题 1、解析 5、简答 1、印刷 4）共 73 页回执；唯一硬件 fail＝试题版 p4 Q16 cases 两行分式重叠（分母 t 与次行分子 1，约 2.9pt）。修复：源级 `\\[3pt]` 不足（间隙仅 0.84–1.20pt），按对照实验改 `\\[6pt]`，成品 600 dpi 实测 3.72–4.08pt（源刊 3.7pt）。内容层修复：Q8 解析作差符号写反（a>b 时 m(a−b)>0 → e2>e1）与两处验证值、Q10 验证区间 `[3^{1/3},5^{1/4})`、说明框 ⑦⑧ 计数（4 个空白格、两行四列）。两轮重建均 0 警告、页数 6/34/8/25 不变；差分变化面 13 页，两轮定向复审 6+8+6 页全 pass；finalize 后 report check 全绿，全量单测 1357 项与基线一致（1 既有失败＋1 他会话错误）。

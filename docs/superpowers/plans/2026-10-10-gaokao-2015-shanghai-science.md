# 2015 上海理卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 上海理科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b23、phase3-b00–b04 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**与刚完成的 2015 上海文卷（phase3-b04）同源同系**：A3 横向三栏书刊合排（印刷页码 **977/978**，与文卷 979/980 为同书连页）、LaTeX（CM 系）重排产物、23 题结构（填空 1–14＋选择 15–18＋解答 19–23）。**文理大量同题**（含题号移位，如理 Q1＝文 Q2、理 Q13＝文 Q14）与**三处同题异数**（Q20 路线题数据不同、Q21 椭圆小问不同、Q22 数列小问不同）——文卷产物是**对照物**而非来源：**转录与盲解一律照理卷源页独立工作，不得参考文卷任何产物**。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_上海卷_文科`（phase3-b04）。

## Global Constraints

- 正式批次 `phase3-b05`；工作目录 `.work/phase3-b05/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源已核定（下表）。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 977＝填空 1–14＋选择 15–18＋解答 19/20；p2 印 978＝解答 21–23）→ **答案证据等级 D**（解析全由盲解撰写）。
- **文理对照纪律**：文卷（`2015_上海卷_文科`）已完成并 FINALIZED——**仅作事后互证**（主会话在整合后可做文理答案交叉核对）；转录/盲解代理**不得读取文卷任何产物**。
- **图形（初判 2 处）**：第 19 题长方体 ABCD-A₁B₁C₁D₁（E、F 为棱 AB、BC 中点，A₁C₁FE 共面＋线面角——新图元：长方体含内部虚线）；第 20 题三角形 ABC（AB=5、AC=3、BC=4；A 左下、B 右上、C 顶部——同文卷 Q21 路线题图式但为三角形）。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- 沉淀纪律（b15–b23/phase3 全量 + b03/b04 新增）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学；答案行裸 `*` 用 `\ast`；**规范源反引号内禁裸 `$`（写 `\$`）、禁包 LaTeX 命令、禁空参数命令**；↔ 等 lmroman 无字形符号不裸入正文；图标签 `inner sep=0`、分数型标签按源墨迹定位；**差分同引擎 pdftoppm**；审查代理 ≤8 页；**图自查含线段采样矩阵（按源实测参数！弧类禁按自画参数采样——自证循环）**；**finalize-batch 先于 check-batch**。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**（源内不印 (1)(2)）的解析须流水式、答案单一答案行。
- 标点与记号照文卷口径（题号句末全角、正文逗号全角、正文层括号全角/数学内半角、选项标号半角照源、`\boldsymbol` 向量按源实测定、弧记号 `\overset{\frown}{}`、不等式 `\leqslant`）——**以理卷源页字体实测为准**。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 上海理卷 | `gk-2015-regular-shanghai-science` | `2015_上海卷_理科` | `src-e4d75eddd216e613f2343814eecc664806ea5e3102d860a862fe6f7943601b1d` | `9e847c423a072243674f3f3c8f72d56f3873fad106d93c2f04b68a504fd88d2f` | `7bb6cbbf11ed09b1ea25d0e9b1125dc2c7d2f815` | `普通高考/2015/2015上海理.pdf` | 2 |

## Review Focus

- 文理对照物（同题移位与同题异数三处：Q20 路线题数据、Q21 椭圆小问、Q22 数列小问）——**事后互证**（不干预独立工作）。
- 第 19 题长方体图（新图元）按源复刻；第 20 题三角形图（照源，注意与文卷路线图式区分）。
- 理科独有题（Q6 圆锥侧面积、Q9 轨迹、Q11 三倍展开、Q12 期望、Q14 三角形、Q17 方程判根、Q23 余弦周期函数）逐题双代理互证。
- 结构核定（23 题，题号连续、无分值印制照文卷口径）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the fixed upstream.
- [x] Render and inspect all pages; record visible title, structure and printed-page numbers in `.work/phase3-b05/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 结果（2026-10-10）：** 固定 commit `34c13a6c…` 树内 blob `7bb6cbbf…`（`git ls-tree` 核验）与提取副本 SHA-256 `9e847c42…`（510,249 B）与 manifest 源记录（`src-e4d75eddd216e613…`，未绑定）一致。目视：**A3 横向（1190.55 × 841.89 pt）三栏书刊合排**（同文卷），页脚印 **977（p1）/978（p2）**（与文卷 979/980 为同书连页）；标题「2015 普通高等学校招生考试（上海卷理）」；结构＝填空 1–14＋选择 15–18＋解答 19–23（19/20 在 p1，21–23 在 p2），共 23 题；图形 2 处：Q19 长方体（A₁C₁FE 共面、线面角）、Q20 三角形 ABC（AB=5/AC=3/BC=4，与文卷 Q21 路线题图式相近但为三角形）；**全 2 页无答案**（等级 D）。**文理对照初判**：大量同题（理 Q1=文 Q2、Q2=文 Q3、Q3=文 Q5、Q5=文 Q7、Q7=文 Q8、Q8=文 Q10、Q13=文 Q14、Q16=文 Q17、Q18=文 Q18）；同题异数 3 处（Q20/Q21/Q22 对应文卷 Q21/Q22/Q23）；理独有（Q6、Q9、Q11、Q12、Q14、Q17、Q19、Q23）。身份（paper_id `gk-2015-regular-shanghai-science`／项目目录 `2015_上海卷_理科`／批次 `phase3-b05`）双命名空间空闲。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [ ] 转录 A：填空 1–14 + 选择 15–18（p1）+ 全 2 页 page-map（含三栏栏序/坐标实测与文理对照自建清单）。
- [ ] 转录 B：解答 19–23（p1 中右栏 + p2）+ 图清单（Q19 长方体、Q20 三角形）。
- [ ] 盲解 A：本库 1–18（填空+选择）；盲解 B：本库 19–23（解答）。**禁参考文卷产物**。
- [ ] 主会话逐题对照源页复核转录稿；盲解互证（完成后可做文理交叉核对作事后互证）。

### Task 3 — Integrate and register

- [ ] 规范三件套 + 含解析派生 + TikZ 图源（长方体新图元）。
- [ ] 注册 `phase3-b05`；provenance 三角色导入。
- [ ] 生成项目源与四版本外壳，三连 check。

### Task 4 — Build, review, and close

- [ ] 正式构建 → 审查代理（分波并发 ≤8 页/段）→ 修复轮（如有）→ 重建 → 差分 → 复审。
- [ ] 审查回执填写（逐页×8 项）→ finalize → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

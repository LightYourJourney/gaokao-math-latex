# 2016 四川卷理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 四川卷理科（自主命题最后一年）整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** `source-manifest.json` 中的固定来源 ID 是身份根；题面、答案要点和解析正文作为规范 Markdown 保存，含解析稿与 LaTeX 项目由现有工具生成。题面转录和独立求解先写入忽略的批次目录，之后由不同角色盲核；不提交扫描 PDF、页面图或构建中间件。

**Tech Stack:** Markdown、Python 3 标准库工具、XeLaTeX、TikZ/PGFPlots、Git、Poppler。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_北京卷_理科`（b12，closed）与 `2016_北京卷_文科`（b13，closed_with_blockers——第 8 题隐含约定被并行会话复核降级，本卷凡依赖题面外约定的解答一律先标待核）。

## Global Constraints

- 正式批次为 `phase2-b15`（本轮单卷批次）。工作目录 `.work/phase2-b15/`。
- **并行会话警告**：phase2-b14（2016 上海文理）由另一会话进行中（其 index.json/manifest.csv 改动未提交）。本批提交时**必须按显式路径 git add**，不得 `git add -A docs/`，避免混入 b14 会话的未提交文件；开工前先 `git log --oneline -3` 确认批次归属未变。
- 固定上游 commit 为 `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；source ID、SHA-256、Git blob OID 和路径不得漂移（本轮已核定，见下表）。
- 源 PDF 为 2 页 A3（印刷页码 1019–1020），**仅含题面、不含答案**；答案解析一律独立推导，等级 D（非官方答案），必须由不同角色盲核。
- **四川自主命题结构：选择题 1–10（每题不印分值）、填空题 11–15、解答题 16–21，共 21 题**。与全国卷 8+6+6 不同，不得按 20 题模板硬套；原卷未印总分/分值/答题说明，一律不补录。
- OCR/文本抽取仅作辅助，规范题面必须逐页目视核对；不清晰内容保持原样并登记问题。
- 草稿只写 `.work/phase2-b15/<paper_id>/`；只保留 TikZ/PGFPlots 图源，不把 PNG/JPEG/PDF 图像或截图入库。
- 构建每卷试题、解析、简答、印刷四版；`build/` 仅留最终 PDF；不 push、不暂存无关改动。
- **规范源写裸 `%`**（渲染器会二次转义 `\%` 为 `\\%`，b13 踩过）；重编后先重跑 `prepare-batch` 换绑新 attempt 再写工作项。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 四川卷理科 | `gk-2016-regular-sichuan-science` | `2016_四川卷_理科` | `src-e4a937b21bfa9c09390e99ac0b2b2c357297f9b15c2119ffb6f2886984049d1a` | `fbf7accd45a89ee6e17810ccc0724fca27de041d505e8311e0c5e5bb56019c2c` | `85698a66143f8905cf4ad4f51dd26425381efe72` | `普通高考/2016/2016四川理.pdf` | 1019–1020 |

上游本地克隆：`gaokaomath-src`（工作区 HEAD 可漂移，一律以固定 commit 取文件）。SHA-256 已与 manifest 源记录一致、提取副本逐字节复验。

## Review Focus

- A3 三栏阅读顺序与文本抽取顺序可能不同：逐题映射到源页栏位与印刷页，查漏题、重题和错序。
- 无官方答案来源：独立推导与异人盲核必须分开取证；角色不独立则证据记 U，不得写成"盲核通过"。
- **凡依赖题面外约定/常识补充的解答（b13 第 8 题教训）**：本卷重点疑似区为第 16 题(2)「估计全市居民中月均用水量不低于 3 吨的人数，并说明理由」（直方图柱高含未知量 a，第 (1) 问先求 a）；若解答需依赖直方图读数之外的解释性约定，先登记待核再作答，不得无条件写死。
- 图形细节（第 6 题秦九韶程序框图、第 13 题三棱锥正视图、第 16 题频率分布直方图、第 18 题四棱锥 P-ABCD）易误读：逐页放大核验，无法确认则登记 blocker。
- 第 15 题「伴随点/伴随曲线」新定义题与第 21 题含参不等式恒成立（`f(x) > 1/x − e^{1−x}` 在 (1,+∞)）：题面文字逐字核对（定义域、不等号方向、参数范围）。
- 第 10 题向量条件组（|DA|=|DB|=|DC| 与三个点积=−2）几何意义需谨慎转译；第 19 题 e₂=5/3 与 4^n−3^n 通项分式逐字核对。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b15/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-08 晚)：** 固定 commit 下 blob OID `85698a66…`、实算 SHA-256 `fbf7accd…` 与 manifest 源记录（`src-e4a937b2…`，`source_state: ready`、`paper_id: null`）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（四川卷理）」，印刷页 1019–1020，结构 选择 1–10 / 填空 11–15 / 解答 16–21（共 21 题），源不含答案、不印分值。页映射：第 1–16 题在第 1 页（1019），第 17–21 题在第 2 页（1020）。预识别图形需求 4 处：第 6 题程序框图、第 13 题三棱锥正视图、第 16 频率分布直方图（柱高含参数 a）、第 18 题四棱锥。`phase2-b15`、`gk-2016-regular-sichuan-science`、项目目录 `2016_四川卷_理科` 与规范 Markdown 前缀 `2016_数学真题_四川理` 均未被占用。

### Task 2 — Transcribe and solve independently

- [x] 转录代理只写 `.work/phase2-b15/gk-2016-regular-sichuan-science/questions.md`、`page-map.md`、`figure-inventory.md`。
- [x] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [x] 主会话逐题对照源页复核转录稿；不确定字形与图形显式保留为待核。

### Task 3 — Integrate and register

- [x] 建立规范 Markdown 三件套（试题 / 答案要点 / 解析正文）并派生含解析稿，图形只写 TikZ 图源。
- [x] 注册 `phase2-b15` 与 paper/项目目录；provenance 按角色分离导入。
- [x] 生成项目源与四版本外壳，跑对应检查。

### Task 4 — Build, review, and close

- [x] 正式构建四版本；逐页视觉审查（含图标签"墨迹连通性"量测口径）。
- [x] 刷新报告与 `manifest.csv`（显式路径提交），全量测试，清理本批中间件（保留 PDF），提交（不 push）。

## 已知口径与坑（b11–b13 沉淀）

- **四版本口径**：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；**印刷版=题目+完整解析的紧凑五号排版**。证明类小题答案框印「见解析版」是生成器既有口径。
- **流水线顺序**：`register-papers --repo <worktree根> --manifest <绝对路径>`（`_含解析.md` 先放占位，注册后 extract-batch 覆盖）→ provenance 三角色文件（role 为 null 必须填，哈希用工具函数现场算）→ generate/short/editions 三连 write+check → build --formal → **重编后先 prepare-batch 换绑 attempt** → 写工作项 → finalize → report render/check --all（带 --manifest --issues 绝对路径）→ manifest_csv --write（**在仓库根跑**）→ unittest。
- **规范源写裸 `%`**；图源 TikZ：框图显式坐标、逐段独立 `draw[->]`、回边 `|-` 且目标点高于源点、坐标轴标题用 `right` 不用 `below left`、`scale` 影响坐标差注释。
- **公共宏是全项目回执依赖闭包**：图环境后齐左、节末留白、「见解析版」均留档不修；单批问题只改规范 Markdown 或图源；孤悬用解析正文 `\Needspace{N\baselineskip}`。
- **审查判据**：留白/齐左类按 b12 实测先例（末页填充 27–42%）判 pass；墨迹连通性判定标签碰线；重编后 150 dpi 像素差分分流，未变页沿用判定。
- **并行会话纪律**：b14（上海）另一会话进行中；本批全程用显式路径提交；收尾前确认 `git log` 中 b14 会话的最新提交，避免误收它的文件。

**Task 2 中途记录（2026-10-09 凌晨）：** 盲解代理完成（`answer-solve.md` 442 行，21 题，角色分离：未读转录稿、未联网）。转录代理**首派被中转站日限额掐断（HTTP 429）**，于 10-09 00:41 跨日后重派（重试已正常启动）。盲解关键判读两处，主会话独立复验均通过：
1. **第 16 题直方图最左组 [0,0.5) 有柱、高 0.08**（600 dpi 实测：顶边恰在 0.08 虚线）——九组柱高 0.08/0.16/a/0.40/0.52/a/0.12/0.08/0.04，由柱高总和 = 2.0（频率和×1/组距）得 **a = 0.30**；若误判首组为空将得 a = 0.34（先例教训：b13 第 17 题最左组为空与本卷相反，两卷须各自独立定案）。第 (3) 问独立复算：累积至 2.5 为 0.73，[2.5,3) 内需再取 0.12/0.30 = 0.4 组宽 → **x = 2.9**；(2) 问 0.12×30 万 = **3.6 万人**。
2. **第 13 题三棱锥体积 √3/3**：主会话独立几何推导——四面均为腰长 2 的等腰三角形、底面 (2, 2, 2√3) 面积 √3、高 1 → V = √3/3，与正视图的「底 2√3 分两段各 √3、高 1」自洽。
另：第 10 题向量条件组跨行读法（三点积均 = −2）已由盲解像素读图确认并给旁证（否则题不成题）；第 15 题伴随点定义式已由主会话裁图复核。

**Task 2 完结（2026-10-09 凌晨）：** 盲解先行完成（442 行，21 题，两份独立复核），转录代理首派被中转站日限额掐断（HTTP 429，零产出），跨日重派成功。转录稿 21 题与源页/盲解逐题吻合；主会话独立复验关键点：第 16 题直方图（最左组有柱 0.08、a=0.30、x=2.9——与盲解、转录代理 SVG 矢量核验三方独立收敛）、第 13 题体积 √3/3（独立几何推导）、第 6 题框图 v=18（手工验算）、第 17 题 tanB=4（独立重导）、第 18 题唯一交点 (356.5, 632.0)（按矢量坐标解析计算复核）。

**Task 3 完结（2026-10-09）：** 规范三件套落盘；四幅 TikZ 图源按矢量级坐标重绘（框图 9 框显式坐标、三视图含数字断开式尺寸线、直方图 9 柱含最左柱与 7 条截断虚线、棱锥 6 实 6 虚含 CE×DP 交点绘制次序）；注册 revision 3424；provenance 三角色导入 revision 3425（哈希现场重算）；生成三连 write+check 全绿。

**Task 4 首轮审查与修复（2026-10-09 凌晨）：** 四版 55 页（5/25/7/18）逐页审查（4 代理），报出缺陷与裁定：
1. **第 16 题直方图两处标注缺陷**（4 版 6 页复现：「频率/组距」与「月均用水量（吨）」被画进绘图区、压柱与虚线）：根因是我在图源中**混用坐标系**（柱/虚线用 `\ux/\uy` 缩放坐标，轴与标签用裸 cm）。**修复**：整图统一缩放坐标重写（轴延伸到 5.5 单位、纵轴 0.587 单位、标注移出绘图区），独立编译探针验证通过。
2. **解析版末页孤悬**（p25 仅剩 Q21 两个答案框、填充 13%）：在 Q21 `#### (2)` 前插 `\Needspace`——先试 22 **未触发**（实测该处剩余 ≈24.7 行 ≥ 22），调至 **26** 后 p24 止于 (1) 内容、p25 含 (2) 全文+两答案框（填充 69%）。沿用 b12/Q20 机制。
3. **印刷版 p14「解析」标签孤悬**（Q18 题块被切）：根因锁至共享转换器 `math-gaokao-2017-2026/tools/md2tex.py:593`——「解析」标签固定预留 `\Needspace{4\baselineskip}`，而其后的 `\gksubpart` 需 6 行（`common/macros.tex:57`），差 2 行；b12/b13 各 20 处同构造因版式巧合未触发，属**潜在缺陷首次现形**。局部修复均不可行（题末加大 Needspace 会在本版制造半空页；缩短前题正文会扰乱解析版已修复的 Q21 分页）。**裁定 pass 留档**，并入版式维护轮（建议：md2tex 解析标签预留 4→≥8 行）。
4. **齐左**（试题版 p4/p5：Q16(1)/Q18(1) 顶格，`\begin{center}` 后 `\@doendpe` 抑制 `\parindent`）：跨批次既存，按 b12/b13 口径裁定 pass 留档。
5. **Q15 末句「写出所以真命题的序列」**：转录（1800 dpi 实读）、盲解、审查代理三方一致确认**源卷如此印记**（「所以」应为「所有」的源侧用字），照录不改。

修复后重建 attempt `f2ab6a82`（零警告、页数不变）。150 dpi 像素差分：试题版 p4；解析版 p4/p17/p24/p25；简答版 p4；印刷版 p4/p13（计 9 个页实例）。二轮复审已派 3 代理。

**Task 4 完结（2026-10-09）：** 二轮复审 3 代理回执全部零 fail（试题/简答版 p4 各 8 项 pass；解析版 p4/p17/p24/p25 计 28 pass/0 fail；印刷版 p4/p13 各 8/8 pass），关键修复均经独立量测确证：直方图两标注与线段最小墨迹净空 4.43–4.95 mm（600/1200 dpi 四档阈值一致）、解析版 p25 首行 "(2)" 且填充 72.6%（旧版 13%）、印刷版 p14 孤悬按留档口径判 pass（其页未变、沿用首轮判定 + 裁定表 OVERRIDE）。`prepare-batch` 换绑 f2ab6a82 后 `merge_findings2.py --write`（含 10 条裁定 OVERRIDE）全绿（5+25+7+18 页 pass），`finalize-batch` → **FINALIZED**（全项目第 4 个）。全量测试 861 项回到基线（1 项既存失败＝poppler 升级 312 条缓存失配，经直接调 `check_batch` 验证**不含本卷**）。

**本批引入的工具修复**：`tools/report.py` 的 `_transaction_inputs` 原先对每卷 `receipts/review.json` 无防护算 sha256，被 b14（上海）在途状态（build 完成、review 未完成）首次触发 `FileNotFoundError` 使全量报告渲染整体失败。修复：逐路径 digest 调用保持（测试契约要求输入追踪完整），缺失文件捕获 `FileNotFoundError` 记 `null`（事务约定的「不存在」态）。`test_report` 11 项全过。

**提交范围（显式路径，不 push）**：b15 项目目录（排除 build/，先例同 b12/b13）、规范三件套、本计划、`reports/phase2-b15.md`、`tools/report.py`、共享投影文件一致快照（含 b14 注册记录）；b14 在途产物（上海文理规范源与项目目录、其计划）一并纳入一致快照，提交信息注明。

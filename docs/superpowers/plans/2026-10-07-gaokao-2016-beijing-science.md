# 2016 北京卷理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 北京卷理科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** `source-manifest.json` 中的固定来源 ID 是身份根；题面、答案要点和解析正文作为规范 Markdown 保存，含解析稿与 LaTeX 项目由现有工具生成。题面转录和独立求解先写入忽略的批次目录，之后由不同角色盲核；不提交扫描 PDF、页面图或构建中间件。

**Tech Stack:** Markdown、Python 3 标准库工具、XeLaTeX、TikZ/PGFPlots、Git、Poppler。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2017_北京卷_理科`（同结构 8+6+6，含 `receipts/review.json` 可对照口径）。

## Global Constraints

- 正式批次为 `phase2-b12`（本轮单卷批次；文理成对来源中的文科留待后续批次）。工作目录 `.work/phase2-b12/`。
- 固定上游 commit 为 `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；source ID、SHA-256、Git blob OID 和路径不得漂移（本轮已核定，见下表）。
- 源 PDF 为 2 页 A3（印刷页码 993–994），**仅含题面、不含答案**；答案解析一律独立推导，等级 D（非官方答案），必须由不同角色盲核。
- 题量与页码映射以源 PDF 逐页核验为准，不能为迎合预期补题。结构：选择题 1–8、填空题 9–14、解答题 15–20（共 20 题）。
- OCR/文本抽取仅作辅助，规范题面必须逐页目视核对；不清晰内容保持原样并登记问题。
- 草稿只写 `.work/phase2-b12/<paper_id>/`；只保留 TikZ/PGFPlots 图源，不把 PNG/JPEG/PDF 图像或截图入库。
- 构建每卷试题、解析、简答、印刷四版；`build/` 仅留最终 PDF；不 push、不暂存无关改动。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 北京卷理科 | `gk-2016-regular-beijing-science` | `2016_北京卷_理科` | `src-03d7f3c6d16a4450d2a52c5514e867a9337005032fbdd6dee4d6cf3804ba11c2` | `9be74675257a9c576c925b30d079b06834f2ea7fef941acafdbed8a816cc9aa9` | `6b32801429392903f5eb0b50e5382f98f5050b8e` | `普通高考/2016/2016北京理.pdf` | 993–994 |

上游本地克隆：`gaokaomath-src`（工作区 HEAD 可漂移，一律以固定 commit 取文件）。

## Review Focus

- A3 三栏阅读顺序与文本抽取顺序可能不同：逐题映射到源页栏位与印刷页，查漏题、重题和错序。
- 无官方答案来源：独立推导与异人盲核必须分开取证；角色不独立则证据记 U，不得写成"盲核通过"。
- 图形细节（第 6 题三视图、第 3 题程序框图、第 17 题四棱锥、第 19 题椭圆坐标系）易误读：逐页放大核验，无法确认则登记 blocker。
- 第 20 题"G 时刻"为新定义数列题，题面文字须逐字核对（定义域、下标范围、不等号方向）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b12/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-07):** 固定上游 HEAD 与固定 commit 均可取到该文件；SHA-256 与 Git blob OID 与 manifest 逐字节一致。目视确认标题「2016 普通高等学校招生考试（北京卷理）」，印刷页 993–994，结构 选择 1–8 / 填空 9–14 / 解答 15–20（共 20 题），源不含答案。`phase2-b12`、`gk-2016-regular-beijing-science`、项目目录 `2016_北京卷_理科` 与规范 Markdown 路径均未被占用。

### Task 2 — Transcribe and solve independently

- [x] 转录代理只写 `.work/phase2-b12/gk-2016-regular-beijing-science/questions.md`、`page-map.md`、`figure-inventory.md`。
- [x] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [x] 主会话逐题对照源页复核转录稿；不确定字形与图形显式保留为待核。

### Task 3 — Integrate and register

- [x] 建立规范 Markdown 三件套（试题 / 答案要点 / 解析正文）并派生含解析稿，图形只写 TikZ 图源。
- [x] 注册 `phase2-b12` 与 paper/项目目录；provenance 先落 uncertain + issue，再按角色分离导入。
- [x] 生成项目源与四版本外壳，跑对应检查。

### Task 4 — Build, review, and close

- [ ] 正式构建四版本；逐页视觉审查（含图标签"墨迹连通性"量测口径）。
- [ ] 刷新报告与 `manifest.csv`，全量测试，清理本批中间件（保留 PDF），提交（不 push）。

## 已知口径与坑（沿用 b11 经验）

- 图标签与线段是否"相碰"用**白字差分 + 墨迹连通性**量测（阈值 ≥240 会把浅灰填充计为墨迹产生假象）；有白隙即 pass 并记录量测。
- `finalize-batch` 需要每个版本的 `warning_exemptions` 与 build 回执的警告集合**逐项匹配**（含 Underfull 的 `width_pt: null`）。
- 视觉审查工作项的 `warning_exemptions` 必须在**写工作项时**一并写好（prepare 之后工作项绑定当前 attempt，不能重跑 prepare 覆盖）。
- `clean-build` 会 rmtree 整个 `build/`（连 PDF），只能用非 PDF 中间件手删，否则回执失效。

**Task 2–3 结果（2026-10-07/08 跨零点）：** 转录代理（`a98c34899ff6d507e`）与盲解代理（`a067109e02fd6fd83`）角色分离完成 20 题；主会话独立复算了 Q1–5、Q7、Q9–20 并与盲解逐题对照，20/20 一致（含第 8 题 20000 次模拟、第 16 题枚举 15/40、第 19 题恒等式化简为 4）。规范三件套与三幅 TikZ 图源（第 3 题框图、第 6 题三视图、第 17 题四棱锥）落盘；注册 revision 3377，provenance 三角色导入 revision 3378（无 U 项，production_state `editions_generated`）。

**Task 4 首轮构建（2026-10-08 凌晨）：** 首次正式构建报 2 条 Overfull（解析版 113.7pt / 印刷版 15.2pt，均在第 15 题 (2) 的单行四步推导式）；改规范解析正文为三行 `aligned` 后重生成、刷新 40 条答案哈希、重导入（revision 3381），重建后**四版本 succeeded、警告归零**，无需豁免。

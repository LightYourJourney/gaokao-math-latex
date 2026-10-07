# 2016 全国Ⅲ卷文理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. Each paper has an independent transcription/solver and different blind reviewer; main session owns canonical integration, manifests, receipts, and commits. Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 全国Ⅲ卷文、理科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** `source-manifest.json` 中的固定来源 ID 是身份根；题面、答案要点和解析正文作为规范 Markdown 保存，含解析稿与 LaTeX 项目由现有工具生成。题面转录和独立求解先写入忽略的批次目录，之后由不同角色盲核；不提交扫描 PDF、页面图或构建中间件。

**Tech Stack:** Markdown、Python 3 标准库工具、XeLaTeX、TikZ/PGFPlots、Git、Poppler。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。

## Global Constraints

- 正式批次为 `phase2-b11`（原计划 `phase2-b100` 不符合现有两位序号规则，2026-10-07 登记前核实 `phase2-b11` 空闲并更正）。仅含本计划列出的 2016 全国Ⅲ文理科；原忽略草稿目录 `.work/phase2-b100/` 保留，不修改公共生成器、模板或其他批次。
- 固定上游 commit 为 `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；source ID、SHA-256、Git blob OID 和路径不得漂移。
- PDF 各 2 页 A3；题量与页码映射以源 PDF 逐页核验为准，不能为迎合预期补题。
- OCR/文本抽取仅作辅助，规范题面必须逐页目视核对；不清晰内容保持原样并登记问题。
- 无可靠答案来源时独立推导并由不同角色盲核；没有异人盲核证据则标 U/blocked，不把自我复算写成盲核。
- 草稿只写 `.work/phase2-b100/<paper_id>/`；只保留 TikZ/PGFPlots 图源，不把 PNG/JPEG/PDF 图像或截图入库。
- 构建每卷试题、解析、简答、印刷四版；`build/` 仅留最终 PDF；不 push、不暂存无关改动。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 |
|---|---|---|---|---|---|---|
| 全国Ⅲ卷文科 | `gk-2016-regular-national-3-arts` | `2016_全国Ⅲ卷_文科` | `src-7b7f83ac42bfac1eb17a01ffcbd1dfe8b661bd4e91d6eaa50dbac5c98fe023d0` | `d226bce4eb9076cace566fba1d9facc0a0007e40955b68875802bab1eab98e09` | `43c049f8280afab2279d113102f9997a89ff0ed5` | `普通高考/2016/2016全国3文(云南,广西,贵州).pdf` |
| 全国Ⅲ卷理科 | `gk-2016-regular-national-3-science` | `2016_全国Ⅲ卷_理科` | `src-556d9ea992950bcd4952763e72a15a168bfe8a1928e42bf5d71bd2ddbacd3fe1` | `a86ba3de1a6de798c7370e1b26a278c08d7d33d489184b6e12cf19c9af3dcb75` | `ff0fea076dc760968f4fa17da6bffb91e877ad67` | `普通高考/2016/2016全国3理(云南,广西,贵州).pdf` |

## Review Focus

- A3 双栏阅读顺序与文本抽取顺序可能不同：逐题映射到 PDF 页及印刷页，查漏题、重题和错序。
- 文理卷题号相似但选项、小问或数值可能不同：每卷独立对照来源，不复制近似版本。
- 根式、上下标、集合、向量、选做题条件和图形细节易误读：逐页放大核验，无法确认则登记 blocker。
- 无官方答案来源时必须区分独立推导与盲核：角色不独立则证据记 U。

## Tasks

### Task 1 — Freeze and visually identify sources

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect all four pages; record visible titles and PDF-to-printed-page mapping in ignored `source-audit.json`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-04):** The upstream HEAD, SHA-256 values, Git blob OIDs, and two-page A3 geometry match the fixed source records. Visual inspection confirms National III arts/science; printed-page maps are arts 1009–1010 and science 1007–1008. Both sources remain `ready` and unbound. `phase2-b100`, both paper IDs/project directories, and canonical National III Markdown paths are unused. Source manifest validation passes; see ignored `.work/phase2-b100/source-audit.json`.

### Task 2 — Transcribe and solve independently

- [x] Each paper agent writes only its ignored `questions.md`, `page-map.md`, `figure-inventory.md`, `answer-solve.md`, and audit notes.
- [x] Main session reconciles each transcription directly against source pages; uncertain glyphs and figures remain explicitly unresolved.
- [x] A different reviewer independently checks each question and derives answers without seeing the first solver draft; discrepancies remain U/issues unless resolved from evidence.

### Task 3 — Integrate and register

- [x] Create the two canonical question/answer/solution Markdown trios and derive combined Markdown with the supported renderer.
- [x] Create project-local vector figure sources only where the PDF supports the geometry.
- [x] Run registration dry-run and inspect exact conflicts; only then register `phase2-b11` once and validate all projections.

**Tasks 2–3 results (2026-10-07):** 两卷各 24 题，独立题面核验与异人答案复核已导入 provenance；规范三层源、含解析派生稿及每卷六幅 TikZ 图稿已登记。文科第 12 题、理科第 11 题的退化情形分别保留 U，并登记 ISSUE-0999 / ISSUE-1000，不擅自补条件。各项批次检查通过。

### Task 4 — Build, review, and close

- [x] Generate project sources and four edition entries with supported tools; run corresponding checks.
- [x] Import provenance from separated roles, formally build all eight editions, and visually review every page against current build hashes.
- [x] Refresh reports, run full project tests and manifest/report checks, remove only this batch's intermediates while retaining PDFs, inspect exact diff, and commit scoped changes. Do not push.

**Task 4 checkpoint (2026-10-07):** 八版本正式构建成功，共 106 页；当前待逐页视觉登记。文科试题/简答共 14 页已目视，发现第 19 题 M 标注碰线，待全部复核发现汇总后做局部标签修复。旧卷缓存状态检查因 Poppler 26.09.0 → 26.10.0 工具链变化失败，另有一份旧卷既存构建/复核绑定不一致；不扩大本批范围刷新旧卷。先提交规范源、provenance 与正式构建待复核状态，后续视觉回执及报告单独提交。

**Task 4 第二轮（2026-10-07 21:06）：** Q19 图标签（M/N/A）与 Q21 分段公式、重复小问编号、解析标题孤悬四处修复并重编，见提交 `c5fa68ff`。

**Task 4 第三轮——终局（2026-10-07 深夜）：** 六版本逐页审查（文科两版另行补审）报出候选缺陷，主会话以**白字差分法**独立复核（把标签渲成白色、差分分离字形墨迹、再量测与线的墨迹连通性），裁定：
- **真缺陷三处**：Q4 雷达图「B」标签（字形 4334px → 与折线同块 20572px）、「5℃」刻度的 C（比值 17.9）、Q22 圆图「E」标签（3714px → 20836px）。
- **代理误判两处**：雷达 B 曾被另一代理以阈值 ≥240 的连通域判"相碰"（该阈值把雷达浅灰填充 229 计为墨迹，属方法学假象）；Q19 的 N 标签间隙 0.106mm 但**无墨迹接触**（600 dpi 仍有纯白分隔列、300 dpi 间隙列灰度 227），判 fail 系提示词「完全避开」的字面口径，主会话改为「墨迹是否连通」并据此判 pass。
- 修复：B 改 `below right`、5℃ 刻度下移 0.15、E 改 `below right`；文理两卷图源保持逐字节一致；三处均以独立编译探针（白字差分 + 连通性）验证修复后无连通分量。
- 重编八版本共 106 页、**页数不变**；逐页 150 dpi 像素差分显示仅 24 个页实例变化（包围盒 ≤56px，限于标签位移区）→ 未变页沿用上轮判定并在 note 写入像素一致证据，变化页的 figure_label 换用量测证据。
- `finalize-batch` 结果 **`closed_with_blockers`**：八版本 build `succeeded`、review `passed`、视觉问题 0、警告豁免 4 条；阻塞为既有的 ISSUE-0999（文科 Q12）/ ISSUE-1000（理科 Q11）两个 U 项。六个全量报告目标与 `manifest.csv` 已刷新。
- 全量测试基线（修复前）861 项中 1 项既存失败：`test_the_cached_states_match_the_recomputed_ones`——旧卷回执绑定 poppler 26.09.0 而环境已升至 26.10.0，属本批范围外（见上一段），未扩大处理。

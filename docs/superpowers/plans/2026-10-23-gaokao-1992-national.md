# 1992 全国卷（文/理）Implementation Plan（phase4-b15）

**Goal:** 将 1992 年全国卷文、理两卷从固定来源转录、独立求解、四版本构建、逐页审查并批次收口。

**State at start（2026-10-23）:** 两卷在 manifest 中均为未绑定的 `ready` 来源；1992 年无任何已登记试卷；上游为 XeTeX 重排件。


## Fixed sources

| 试卷 | 上游路径 | SHA-256 | Git blob OID | 页数 | 页脚 |
|---|---|---|---|---|---|
| 1992 全国文 | `普通高考/1992/1992全国文.pdf` | `8bd9671406dfcc344407488d75fa9eba95b62d02492aaeb728f8fd2fe193ffd6` | `f97c1763e911d929744ad4d3da8befba1e16276d` | 1（A3 三栏） | 43 |
| 1992 全国理 | `普通高考/1992/1992全国理.pdf` | `aa3c0a314b5ea0bf990cbc7d768575e3b3931da6ddbfb6c727681a516a7eb7aa` | `aaf960d7713e9864174748679ee16a8cbc603b72` | 1（A3 三栏） | 42 |

**结构（实测）**：两卷均 28 题——选择 1–18、填空 19–23、解答 24–28；无答案页（等级 D，答案/解析须独立推导并标注非官方）。
**图**：文 Q6 幂函数四曲线、Q14 正方体（M、N 中点）、Q26 正方体 A₁–EBFD₁；理 Q6、Q14。
**字体**：LMRoman/CM 系＋STSong/STHeiti＋MSAM10/CMSY10；无 CMMIB10。

## Tasks

### Task 1 — 冻结与判读

- [x] 源冻结：`.work/phase4-b15/source/`；sha256 与 pin 下 blob OID 现场核对。
- [x] 文本层与版式判读：1 页 A3 三栏；页脚 42（理）/43（文）；28 题结构；图表清单骨架。
- [x] 卷面异常登记：文 Q16（`\dfrac{e^x-e^x}{2}`）、Q27（`2-2y+1=0`）与理 Q16、Q26（端点记法歧义）均在 `来源校对.json` 记 `needs-review`，正文保留原文不擅改。

### Task 2 — 转录与盲解

- [x] 转录 文/理（两代理，隔离）：`transcripts/{arts,science}.md`＋`-figures.md`。
- [x] 盲解 文/理（两代理，仅据题面）：`blind/{arts,science}.md`。
- [x] 代理均不得读取其他批次/年份产物。

### Task 3 — 整合与注册

- [x] 规范三件套＋含解析占位；六项自检（`%`、空参、反引号、CJK 入数学、`&`、孤需参宏）＋（N）锚点；说明框预算 ≤29 行。
- [x] TikZ 图源（Q6 幂函数曲线、Q14/Q26 正方体）由内容流逐路径生成＋探针（坐标直录、0 警告、标签避让复核）。
- [x] 注册 phase4-b15（rev 4628）；provenance 三角色（rev 4629/4632/4635/4636）；extract-batch。

### Task 4 — 构建与审查

- [x] generate/short/editions → build --formal → 审计三连（八版 log 0 警告）。
- [x] 审查 14 段（文 7＋理 7，≤5 并发）→ 修复轮 → 重建 → 机械核验 → 回执覆盖。
- [x] collect → finalize（rev 4641，FINALIZED）→ check-batch → validate-receipts OK（2 卷）→ report → 单测 → 显式路径提交（不 push）。

## 修复轮记录

| # | 版本·页 | 检查项 | 现象 | 处置 |
|---|---|---|---|---|
| 1 | 文试题 p2、文简答 p2、文印刷 p2/p6 | option_formula_alignment | 第 6 题选项被空行分成两段，第二段多 24pt 缩进 | 合并四选项为单段（源级） |
| 2 | 文/理 试题 p2、简答 p2、解析对应页 | figure_label | Q6 图中 C₃/C₄ 标签相交、C₄ 下标被 x 轴横穿（10.5pt 字号大于源 9pt） | 标签重定位：C₃ (270,334)、C₄ (252,322.5)（理；文整体 −43.6）；复核 C₃/C₄ 分离 2.1pt、C₄ 距轴 1.1pt |
| 3 | 文试题 p3 | option_formula_alignment | 第 22 题 T/S 分式跨行、行距被撑开 | 源级 `\mbox` 绑定分式 |
| 4 | 文印刷 p2 | pagination_whitespace | 第 12 题「（　）」独占一行 | 「方程是（　）」整体 `\mbox` 绑定 |
| 5 | 文解析 p18 | figure_label | Q26 图 C₁ 下标被斜棱穿过、A 贴虚线 | 标签重定位 C₁ (1119.5,331)、A (1064.5,287) |
| 6 | 文解析 p18 | pagination_whitespace | 「解析」标题孤悬页末 | Q26 解析前 `\Needspace{8\baselineskip}`，整块移至 p19 页首 |
| 7 | 文解析 p19 | pagination_whitespace | 「则」单字成行、「面积」被拆成「其面／积」 | 删「则」并入前句；「面积」用 `\mbox` 绑定 |
| 8 | 文/理 试题 | 构建 | 说明框首段 Underfull（badness 3668） | 精简字体枚举措辞后八版 0 警告 |

**终验**：最终构建文 4/20/6/16、理 4/19/6/16 页，八份日志 0 警告；上述修复点按文本层 bbox 与像素行剖面逐项复核；14 段回执覆盖后四版×两卷顶层全 pass。

## 记录

- **图稿目录**：早期草稿图（`f1992_national_{arts,science}_*`，2026-10-14 入库）迁入各卷 `figures/drafts/`。原因：manifest 图稿登记必须与 `figures/` 目录**逐名一致**，草稿图与正式生成图并处会触发 `figure occurrences` 守卫；`drafts/` 子目录不被 `iterdir` 的 `is_file()` 计入。草稿内容未改，哈希不变；`来源校对.json` 的 `figure_files.path`/`reused_from` 与 `题面转录草稿.md` 的图链同步改为 `figures/drafts/…`，故两份草稿 `draft_sha256` 与文科 `reused_transcription.source_sha256` 相应更新（文 `40a586ea…`，理 `fadcc157…`）。`核源记录.md`（2026-10-14）中引用的旧哈希保留为当时记录。
- **来源测试**：`tests/test_1992_national_{arts,science}_sources.py` 原断言 `source["paper_id"] is None`（登记前状态），现改为断言已绑定的 `gk-1992-regular-national-{arts,science}` 与 `paper_relation=canonical`；`来源校对.json` 本身仍为入库时快照（`paper_id=null`），与其余已完成卷一致。
- **提交**：全量单测（1753 项）通过后按显式路径提交，不 push。

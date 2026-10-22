# 1992 全国卷（文/理）Implementation Plan（phase4-b15）

**Goal:** 将 1992 年全国卷文、理两卷从固定来源转录、独立求解、四版本构建、逐页审查并批次收口。

**State at start（2026-10-23）:** 两卷在 manifest 中均为未绑定的 `ready` 来源；1992 年无任何已登记试卷；上游为 XeTeX 重排件。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md`、`CLAUDE.md`、交接文档。

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
- [ ] 卷面异常登记（随转录回执补全）。

### Task 2 — 转录与盲解

- [ ] 转录 文/理（两代理，隔离）：`transcripts/{arts,science}.md`＋`-figures.md`。
- [ ] 盲解 文/理（两代理，仅据题面）：`blind/{arts,science}.md`。
- [ ] 代理均不得读取其他批次/年份产物。

### Task 3 — 整合与注册

- [ ] 规范三件套＋含解析占位；六项自检（`%`、空参、反引号、CJK 入数学、`&`、孤需参宏）＋（N）锚点；说明框预算 ≤29 行。
- [ ] TikZ 图源（Q6 幂函数曲线、Q14/Q26 正方体）＋探针（残差、600 dpi 墨迹、灵敏度）。
- [ ] 注册 phase4-b15；provenance 三角色；extract-batch。

### Task 4 — 构建与审查

- [ ] generate/short/editions → build --formal → 审计三连（四版 log 0 警告）。
- [ ] 审查分段（≤8 页/段、≤5 并发）→ 修复轮 → 重建 → 差分 → 复审。
- [ ] collect → finalize → check-batch → report → 单测 → 显式路径提交（不 push）。

## 记录

（随阶段补记。）

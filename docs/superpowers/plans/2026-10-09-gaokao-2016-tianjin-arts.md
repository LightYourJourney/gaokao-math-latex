# 2016 天津卷文科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 天津卷文科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b17 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_天津卷_理科`（b17，同省配对）。

## Global Constraints

- 正式批次 `phase2-b18`；工作目录 `.work/phase2-b18/`。
- **并行会话**：phase2-b14（上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源三方已核定（下表）。
- 源 PDF 2 页 A3（印刷页 1025–1026），仅含题面；答案解析独立推导（等级 D）+ 异人盲核。
- **天津卷结构：选择 1–8、填空 9–14、解答 15–20，共 20 题**；源不印分值，照录不补。
- **规范源写裸 `%`（构建前强制 grep 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- **解答题小问「（N） 内容」（N 后空格）**；长定义式用 `\frac` 非 `\dfrac`（b15/b16 教训）。
- **题面分页守卫可局部注入规范源**（b17 手法）：题前独立行 `\Needspace{N\textheight}`，渲染器保留并同入 answers 派生；N 按实测块高且须大于该处剩余。
- **图标签探针必须连通域量测**（b17 教训）：标签用显式坐标（照源矢量中心），400 dpi 隔离探针验证独立分量。
- **审查代理一代理 ≤8 页**（b16 的 524 时长上限教训）。
- **建后先主会话自查全部新图**，修完再派审查代理。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 天津卷文科 | `gk-2016-regular-tianjin-arts` | `2016_天津卷_文科` | `src-3550b3431ddf3fa2c508a3701034b9d01435e13701fd2209a98a43f047b2d841` | `5453505cadbe42aef85a3f8089bb10128f53fa755d5ecc3afdc96bf835cb43a0` | `de8a81c7e41013835fd732f3b69a9957628b327e` | `普通高考/2016/2016天津文.pdf` | 1025–1026 |

## Review Focus

- **文理不得互推**：文 Q11 ≡ 理 Q4（框图同题）、文 Q13 ≡ 理 Q12（圆同题）——两处可交叉参照；**Q19/Q20 形似但独立**（文 Q19 为 ∠MOA=∠MAO 等号求斜率值、理卷为 ≤ 求范围；文 Q20 为 x³−ax−b、求证 x₁+2x₀=0、区间 [−1,1]，理卷为 (x−1)³、x₁+2x₀=3、[0,2]）——一律以源页独立核定。（2026-10-09 修正：本文初稿误写「x₁+x₀=0」，源页文本层为 `x1 + 2x0 = 0`，两代理与主会话三方一致。）
- 图形 4 处：第 3 题三视图选择题（正视图+俯视图+四个侧视图选项）、第 11 题程序框图（同 b17 理卷 Q4，复用其图源并核对）、第 13 题圆（同 b17 理卷 Q12，复用并核对）、第 17 题平行四边形立体图（**文卷特有，新构型**：ABCD 平行四边形、平面 AED⊥ 底面、EF∥AB、G 为 BC 中点，含 F/E/G 顶点）。
- **第 16 题含表格**（甲/乙两种肥料 × A/B/C 三种原料的吨数表，3 列数据）——本卷唯一表格，重绘方式待定（tabular）。
- 文 Q16 为线性规划应用题（A/B/C 原料 200/360/300、利润 2/3 万）——与理卷无对应。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b18/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results (2026-10-09)：** 固定 commit `34c13a6c…` 上 blob `de8a81c7…`、SHA-256 `5453505c…` 与 manifest 源记录（`src-3550b343…`，ready、未绑定）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（天津卷文）」，印刷页 1025–1026，结构 8+6+6=20 题，源不含答案、不印分值。页映射：Q1–16 → p1（1025）；Q17–20 → p2（1026）。图形 4 处（Q3 三视图选择、Q11 框图、Q13 圆、Q17 立体图）+ 表格 1 处（Q16）。身份（paper_id/base `2016_tj_wen`/目录）空闲。

### Task 2 — Transcribe and solve independently

- [x] 转录代理只写 `.work/phase2-b18/gk-2016-regular-tianjin-arts/questions.md`、`page-map.md`、`figure-inventory.md`。
- [x] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [x] 主会话逐题对照源页复核转录稿。

**Task 2 完结（2026-10-09）：** 盲解先行（10 分钟、20 题，全部高/中高置信度，附逐题数值自检与 Q14 六点数值复核）；转录代理交付三文件齐全（questions 135 / page-map 104 / figure-inventory 274 行），图稿以 `pdftocairo -svg` 矢量路径核验（含 F01 四选项虚实排列、F04 平行四边形向量逐分量相等检验、F05 斜线表头坐标）。**主会话终裁核验（文本层 + 独立复算）**：
1. **关键串四点全中**（本会话对源 PDF 文本层直接 grep）：Q3「长方形」（照录待核成立）、Q13 行尾 `BE = 2AE = 2` 的 `= 2` 存在、Q19 为等号且问「求直线 l 的斜率」（单值）、Q20 求证式 `x1 + 2x0 = 0`。
2. **文理独立逐字坐实**（本会话对两卷文本层直接对照）：文 Q20 `x3 − ax − b` / `x1 + 2x0 = 0` / `[−1, 1]` vs 理卷 `(x − 1)…− ax − b` / `x1 + 2x0 = 3` / `[0, 2]`；文 Q19「求直线 l 的斜率」vs 理卷「求直线 l 的斜率的取值范围」。
3. **图稿复用交叉验算**：Q11 框图与理 Q4 为纯平移（转录量得 Δx=+371.68、Δy=−7.15；本会话按「理卷 F01『开始』框 220.92 → 本卷 592.60」复核 371.68 成立）；Q13 圆与理 Q12 同图（圆心横坐标 594.74、半径 40.08 两卷相同）。
4. **主会话独立复算抽验**：Q8 区间边界（六点代入判 0 是否落于开区间）、Q13 相交弦 2√3/3、Q14 单调衔接 a∈[1/3,3/4] 与负根计数 a<2/3 → [1/3,2/3)、Q19(2) ∠MOA=∠MAO⟺|MO|=|MA|、Q20(3) 四点 T(x)=x³−3x/4 反证——全部与盲解吻合。
其余各题转录与盲解逐项一致。源内异常 6 条（Q3「长方形」、Q16 顿号不统一、Q17 示意不按比例、∥ 不在文本层系矢量路径、Q3 作答括号排于选项图之下、全卷不印分值）按纪律照录/记录。**盲解不确定项 7 条**中，Q3 侧视朝向（三重依据判 (B)）、Q13 `=2` 完整性、Q20(3) a>0 冗余三项已由本会话独立复核认同；Q14 链路最长故记为中高置信度之谨慎，其结论已经本会话独立重推确认。

### Task 3 — Integrate and register

- [ ] 规范三件套 + 含解析派生 + 4 幅 TikZ 图源（+ Q16 表格）。
- [ ] 注册 `phase2-b18`；provenance 三角色导入。
- [ ] 生成项目源与四版本外壳，三连 check。

### Task 4 — Build, review, and close

- [ ] 正式构建（构建前 grep `\\%` 自检）→ **主会话先自查全部图** → 派审查代理（≤8 页/代理）。
- [ ] 修复轮（如有）→ 重建 → 像素差分 → 变化页二轮复审 → 合并。
- [ ] finalize → 报告刷新（带 --manifest/--issues，manifest_csv 在仓库根跑）→ 全量测试 → 清理中间件 → 显式路径提交（不 push）。

## 已知口径与坑（b11–b17 沉淀）

- 四版本口径：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；印刷版=题目+完整解析紧凑排版；「见解析版」为生成器既有口径。
- 规范源写裸 `%`；解答题小问「（N） 内容」；长定义式 `\frac`；TikZ 图源全坐标统一缩放、框图显式坐标逐段独立 draw、回边 `|-` 目标点高于源点。
- **分页守卫注入规范源**（b17）：`\Needspace{N\textheight}` 独立行于题前；N 按题块实测高且须大于该处剩余（b15 同坑）；改动经派生同入 answers。
- **图标签独立性的探针量测**（b17）：400 dpi 隔离探针 + 连通域；标签显式坐标；字块尺寸异常=并入线段。
- **留白口径**（b17 澄清）：末页填充先例实为下限参考（≈27%），更满不是缺陷；宏级确定性留白（`\gkpart` 0.6、`\clearpage`、`answer` 环境 0.5）单独判 pass。
- 公共宏/转换器（`common/*`、`md2tex.py`）是全项目回执依赖闭包：齐左、留白、「解析」标签孤悬类均留档不修。
- 印刷版模板共性（页眉横线短、页脚左偏）为全项目缺陷、留档待版式维护轮（b16 裁定）。
- 在他批在途时刷新报告：`tools/report.py` 已修（缺失回执记 null），直接 `render/check --all` 即可。

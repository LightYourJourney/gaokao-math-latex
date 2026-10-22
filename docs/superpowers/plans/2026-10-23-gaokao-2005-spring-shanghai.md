# 2005 春季上海卷 Implementation Plan（phase4-b11）

**Goal:** 把 2005 年春季上海卷（22 题）从既有草稿推进到四版本正式构建、逐页审查与批次收口。

**State at takeover（2026-10-23）:** 题面/答案/解析、四幅 TikZ 图、四版本 tex 均已完成（Codex 前期工作）；卷登记为 `planned`、`source_ids=[]`、无 provenance、无正式构建与审查回执。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md`、`CLAUDE.md`、`docs/superpowers/plans/2026-10-22-gaokao-latex-handoff.md`。

## Fixed source

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 2005 春季上海 | `gk-2005-spring-shanghai` | `2005_上海春季卷` | `src-2cd71e4c…` | `67d4850c…` | `ff0516b9…` | `春季高考/2005/2005春季上海.pdf` | 2（A3 三栏，印刷页 217/218） |

## Constraints

- 无答案页（等级 D）；答案/解析为编者推导、非官方；Q1–22 已分段异人盲核。
- 图：Q19 正三棱锥、Q21 函数示意、Q22 椭圆、Q22(3) 作图构造；仅表达拓扑，不按比例。
- 提交只 stage 本批授权路径；不 push；公共宏不改。

## Tasks

### Task 1 — 来源绑定与 provenance

- [x] 核对上游固定件（pin `34c13a6` 下 blob/sha 与卷标题一致），绑定 `source_ids`（manifest rev 4612）。
- [x] provenance 三角色 22 题填充并导入（rev 4613/4617/4620）。
- [x] 说明：`register-papers` 是 add-only，无重绑入口；绑定走同一 state 事务路径（`.work/phase4-b11/bind_source.py`），三组语义校验通过。

### Task 2 — 生成与正式构建

- [x] `generate_projects` / `make_short_answers` / `make_editions` 三连。
- [x] `build --formal`：4/18/6/14 页，四份日志 Overfull/Underfull/Missing 全 0。

### Task 3 — 审查与修复轮

- [x] 审查分 7 段（试题 1＋解析 3＋简答 1＋印刷 2），≤5 并发。
- [x] 首轮发现并修复：
  - 全四版页眉重复「数学」（登记标题自带「·数学」而模板追加）→ 标题改「2005 年·春季上海卷」（rev 4616）；
  - Q12 `|f(a_n)−2005|` 跨行、闭合竖线落行首 → 源级 `\mbox` 绑定；
  - 解析正文笔误「在 O 处直角」→「在 O 处为直角」；
  - 来源说明/图表清单过期表述（「尚未进入正式构建」「独立盲核尚未完成」）改为与实态一致；
  - 解析侧 `\leqslant` 统一为源件字形 `\le`；
  - Q16③ 题面复述段「值。」孤行 → 源级 `\looseness=-1`。
- [x] 二项式系数行内字形：最小样例与纯 article 对照一致，属 amsmath 默认字形、全库 1046 处同款，按已接受类 pass+note（不在单批改公共层）。
- [x] 印刷版两段回执归集：p1–7 全 pass；p8–14 的 header_footer 位置项按既有 b12/b20 裁定（全库印刷版同构基线：`\headwidth` 未随印刷版壳 `\geometry{margin=1.6cm}` 更新，横线短 35.9pt、页脚左偏 18pt）记 pass+note，与 p1–7 口径统一，留待全局排版维护轮。

### Task 4 — 收口

- [x] prepare-batch（重建后重绑）→ collect → finalize（**rev 4627，FINALIZED**）→ check-batch → `build_projects validate-receipts` 返回 OK（1 卷）。
- [x] `report render/check --all`；单测（1753 项，修复 4 项过期断言后回基线）；显式路径提交（不 push）。

## 修复轮记录

| # | 版本·页 | 检查项 | 现象 | 处置 |
|---|---|---|---|---|
| 1 | 全四版逐页 | header_footer | 页眉「2005 年·春季上海卷·数学 · 数学」重复 | 登记标题改为「2005 年·春季上海卷」（rev 4616）并重生成四壳；重建后 42 页逐页核验只含一次「数学」 |
| 2 | 试题/解析/简答 p2 | option_formula_alignment | Q12 `|f(a_n)−2005|` 跨行、闭合竖线落行首 | 源级 `\mbox` 绑定；重建后文本层为完整一行 |
| 3 | 解析 p12 | pagination_whitespace | Q16③ 题面复述末行「值。」孤行 | 源级 `\looseness=-1`（b19 先例）；重建后整句收束一行 |
| 4 | 解析 p7/p8 | glyph | 行内 `\binom` 上标位于定界符上沿 | 最小样例＋纯 article 对照一致，属 amsmath 默认字形、全库 1046 处同款 → pass+note |
| 5 | 解析 p14 附近 | 文字 | 「△POM 在 O 处直角」缺「为」 | 规范源补字并重生成 |
| 6 | 四版说明框 | 内容一致性 | 来源说明/图表清单的过期表述（「尚未进入正式构建」「独立盲核尚未完成」） | 改为与实态一致（已绑定来源、已进入正式构建、盲核完成） |
| 7 | 解析侧 | 记号一致性 | `\leqslant` 与题面 `\le` 混用 | 统一为源件字形 `\le` |

**终验**：修复后正式构建 4/18/6/14 页、四份日志 0 警告；页眉、Q12、孤行均按文本层逐页机械核验。审查 7 段共 42 页，归集后四版 top-level 全 pass，finalize revision 4623。

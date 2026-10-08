# 2016 山东卷文科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 山东卷文科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b19 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_山东卷_理科`（b19）。

## Global Constraints

- 正式批次 `phase2-b20`；工作目录 `.work/phase2-b20/`。
- **并行会话**：phase2-b14（上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源三方已核定（下表）。
- 源 PDF 2 页 A3（印刷页 1013–1014），仅含题面；答案解析独立推导（等级 D）+ 异人盲核。
- **山东卷结构：选择 1–10、填空 11–15、解答 16–21，共 21 题**；源不印总分与分值，照录不补。
- **文理不得互推**：本卷与 b19 理卷存在若干同题（Q3/Q4/Q5/Q6/Q10/Q14/Q15/Q19 题面近似），**一律以本卷源页独立核定**；转录与盲解代理禁止读取理卷任何文件（防内容污染）。
- **规范源写裸 `%`（构建前强制 grep 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- **解答题小问「（N） 内容」（N 后空格）**；长定义式用 `\frac` 非 `\dfrac`（b15/b16 教训）。
- **含 `&` 的 cases/array 必须行间 `\[ \]`**（b19 教训：行内 `\(\)` 走转义路径）。
- **图标签必须 `inner sep=0`**（b18）且按源字形框中心显式坐标定位；源位拥挤时微调并留档（b19 第三类成因）。
- **图标签探针必须连通域量测**（b17/b18）：400 dpi 隔离探头 + 8-连通域，字母须为独立分量。
- **审查代理一代理 ≤8 页**（b16）；**findings 检查项键名统一用 `"check"`**（b19 实测跨段混用 check/name 的坑，派发 prompt 钉死）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 山东卷文科 | `gk-2016-regular-shandong-arts` | `2016_山东卷_文科` | `src-92fa540a5c2a79fc65e8dae18121e740b7400dffda8fa1f6f4902c1907e533fd` | `a8a11b3efe18d0a484ccd6c8621fddd42d2a5e58b4eeaa6846c91b7224a71e72` | `3efcbea752aca8ba731138c0cfe9b3d04d536a99` | `普通高考/2016/2016山东文.pdf` | 1013–1014 |

## Review Focus

- **山东卷结构独立核定**：10+5+6=21 题；解答题 16–21 共 6 题。
- 图形 **6 处**（预期，须独立核数）：第 3 题频率分布直方图、第 5 题三视图（半球+四棱锥，正（主）/侧（左）/俯三子图）、第 11 题程序框图（**「输入 n」，循环体 S=S+√(i+1)−√i 与 i=i+1**）、**第 16 题转盘（项目首例：指针+四分圆盘 1/2/3/4）**、第 18 题立体几何（E/F/A/B/G/H/C/D 八顶点线框）、第 21 题坐标图（椭圆+定点 M 问题）。
- **与理卷同题须独立复核**（不互推）：Q3 直方图数据/柱高、Q5 三视图形态与选项、Q4 线性约束、Q6 线面逻辑、Q10 T 性质、Q14 双曲线矩形（e=2）、Q15 分段函数、Q19 数列（Tn=3n·2^{n+2}）——本卷逐字或近似以本卷源页为准。
- 第 12 题「观察等式」是数列式规律题（sin 平方倒数和）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b20/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results（2026-10-09）：** 固定 commit `34c13a6c…` 上 blob `3efcbea7…`、SHA-256 `a8a11b3e…` 与 manifest 源记录（`src-92fa540a…`，ready、未绑定）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（山东卷文）」，印刷页 1013–1014（页脚居中），结构 10+5+6=21 题，源不含答案、不印分值。图形预期 6 处（Q3/Q5/Q11/Q16/Q18/Q21，转盘图为项目首例）。身份（paper_id `gk-2016-regular-shandong-arts`/base `2016_sd_wen`/目录 `2016_山东卷_文科`）空闲（index.json、manifest、文件系统三方检索 0 冲突）。

### Task 2 — Transcribe and solve independently

- [x] 转录代理只写 `.work/phase2-b20/gk-2016-regular-shandong-arts/questions.md`、`page-map.md`、`figure-inventory.md`。
- [x] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [x] 主会话逐题对照源页复核转录稿。

**Task 2 完结（2026-10-09）：** 转录代理交付三文件（questions 163 / page-map 228 / figure-inventory 471 行；六图全矢量路径级核验，并纠正任务书一处错误前提——本 PDF 有真实文本层，码位以文本层为真值、几何以 SVG 为真值）；转录代理**未读盲解稿**（防对照污染，做法正确）。盲解代理 21 题全交付（高 18 / 中高 3：5、14、21；速查：1A 2B 3D 4C 5C 6A 7B 8C 9D 10A / 11:1 12:(4/3)n(n+1) 13:−5 14:e=2 15:m>3 / 16 5/16、3/8>5/16；17 [kπ−π/12,kπ+5π/12]、√3；18 证 AC⊥FB、GH∥面ABC；19 bₙ=3n+1、Tₙ=3n·2^{n+2}；20 分类单调、a>1/2；21 x²/4+y²/2=1、k′/k=−3、min=√6/2 于 m=√14/7）。**主会话独立复算抽验 12 项全部吻合**（Q1 补集、Q2 z̄、Q7 a=2→相交、Q8 cosA=sinA→π/4、Q9 周期+奇延拓 f(1)=2、Q11 裂项 S=1、Q12 规律式、Q13 2t+10=0、Q16 枚举 5+6+5、Q17 化 2sin(2x−π/3)+√3−1、Q20(2) f″(1)=1−2a<0、Q21② m=√14/7 时斜率 1.2249=√6/2）。
**一处转录↔盲解冲突裁定**：Q16 转盘数字方位——转录的题图描述「自右上起顺时针 3、4、2、1」与实图不符，400 dpi 亲验为**上 1 / 左 3 / 右 4 / 下 2**（盲解正确），整合时已订正；圆心实心点为转轴记号（源内 U+2022），照录。
**文理同题独立核**：Q3/Q4/Q5/Q6/Q10/Q14/Q15/Q19 与 b19 理卷同题，答案一致但系本卷源页独立转录与独立推导所得（硬禁令有效执行）。

### Task 3 — Integrate and register

- [x] 规范三件套 + 含解析派生 + 6 幅 TikZ 图源。
- [x] 注册 `phase2-b20`；provenance 三角色导入。
- [x] 生成项目源与四版本外壳，三连 check。

**Task 3 完结（2026-10-09）：** 规范三件套（试题/答案要点/解析正文，含 Q18 证明要点与 ①② 并入小问块）；6 幅 TikZ 图源全部按本卷 SVG 清点独立重绘——F01 直方图（**含原点折断符号锯齿**，b20 清点实测 x 4.25–17.00、振幅 ±2.13）、F02 三视图（**半圆平边弦在上、弧下鼓的碗形**，弧底与锥顶点相触——此点后来成为 b19 回查的触发证据）、F03 框图（9 框显式坐标，回接汇入点在 S=0 与处理框之间）、F04 转盘（项目首例；两垂直直径四等分、圆心实心点）、F05 立体几何（五顶点+辅助 D/G/H、虚实测端点照源）、F06 坐标图（椭圆 2 倍线宽 0.8pt、割线两端有意延伸）。含解析派生 + 注册 rev 3489 + provenance rev 3490 + generate/简答/四壳三连 check 全绿。**主会话 400 dpi 连通域探针自查六图全过**（唯一「并入」均为内在结构：圆+直径、根号横线接 CMR「1」字顶（b19 同款先例）、碗底接顶点、CJK 标点字距、虚线端点接线网）。

### Task 4 — Build, review, and close

- [x] 正式构建（构建前 grep `\%` 自检）→ **主会话先自查全部图**（含 400 dpi 连通域）→ 派审查代理（≤8 页/代理）。
- [x] 修复轮（如有）→ 重建 → 像素差分 → 变化页二轮复审 → 合并。
- [x] finalize → 报告刷新（带 --manifest/--issues，manifest_csv 在仓库根跑）→ 全量测试 → 清理中间件 → 显式路径提交（不 push）。

**Task 4 首建（2026-10-09）：** 四版 5/21/7/18=**51 页**、零 Overfull/Underfull、零失败。审查 8 段已派（试题 5、简答 7、解析 21 三段、印刷 18 三段；attempt `c74c878d`，`prepare-batch` 已换绑；prompt 键名钉死 `"check"` 并附 b19 已裁定口径防重复上报）。

**Task 4 审查回报与修复轮（2026-10-09）：** 8 段全回报（51 页）：**1 处真缺陷 + 1 处代理间口径分歧**。
1. **fix-1（真缺陷，跨批新坑）**：解析正文 Q3 句「五组「\(\dfrac{频率}{组距}\)」」——**CJK 裸进数学模式**回落 lmroman 无字形 → 解析版 p7/印刷版 p6 上「频率」「组距」四字**完全未绘出（只剩分数横线）**；解析版代理 800 dpi 实拍抓出（另一代理曾把空横线误读为「源内占位符」——此类缺陷人眼 150 dpi 极难识别）。修复=改文本式「频率／组距」（b19 同句即无数学模式 CJK）；全规范源 CJK-in-math 扫描确认仅此一处（`\text{水杯}` 类经日志零缺字实证安全）。重派生→重编后 **Missing character 四日志全归零**；差分仅 2 页（解析版 p7、印刷版 p6，无分页位移）；修复轮复审 2 页全 pass（逐字墨宽 10.56/9.60pt、U+FFFD 0、无残留横线）。
2. **fix-2（代理间分歧裁定）**：印刷版 p7–12 的 header_footer 被 part2 代理判 fail（并精确定位根因：`common/preamble.tex` 的 `\headwidth` 与壳文件 `\geometry{margin=1.6cm}` 失同步，实测横线短 34.2pt、页脚左偏 17.1pt）——属 **b16 已裁定「印刷版模板共性留档待版式维护轮」**（全项目回执依赖闭包，单批不可修），**降级 pass+note**；p14「解析」标签孤悬（Q18 解析标题孤立页末、页底余 95.6pt）同属 b16 留档类，一并降级。
3. 另记录（均 pass）：Q6 选项折行、Q12 填空横线折行、pdftotext 字身宽假越界、解析端半角 (1) 与题目端全角（1）体例（生成器既有口径、b19 同构）、Q18 图 EF/DB 斜率差 3.5°（源图自身示意不精确、照源复刻，同 b19 圆台先例）。

**Task 4 收尾（2026-10-09）：** 51/51 页 pass 落盘 → **FINALIZED（attempt `9a259456`）**；报告全绿（closed/succeeded/passed，无视觉问题无阻塞）；unittest 861 项仅基线既存 1 项失败（b20 精确 0 条）；清理 build 中间件（仅留 4 PDF）。

## 已知口径与坑（b11–b19 沉淀）

- 四版本口径：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；印刷版=题目+完整解析紧凑排版；「见解析版」为生成器既有口径。
- 规范源写裸 `%`；解答题小问「（N） 内容」；长定义式 `\frac`；TikZ 图源全坐标统一缩放（照源 pt 换算）、框图显式坐标逐段独立 draw、回边 `|-` 目标点注意穿框。
- **图标签 `inner sep=0`**（b18）；**标签并入三成因**：inner sep 移位（b18）/源位拥挤微调（b19）//标签探针必须连通域量测（b17）。
- **分页守卫注入规范源**（b17）：`\Needspace{N\textheight}` 独立行于题前；N 按题块实测高且须大于该处剩余。
- **留白口径**（b17）：末页填充下限参考 ≈27%（更满不是缺陷）；宏级确定性留白单独判 pass。
- 公共宏/转换器（`common/*`、`md2tex.py`）是全项目回执依赖闭包：齐左、留白、「解析」标签孤悬、印刷版页眉横线短/页脚左偏类均留档不修（b16 裁定）。
- **dfrac 选项行→「解析」标题墨迹间隙 ~1pt 为紧凑排版常态**（b19 裁定：无重叠即 pass+note，不改源）。
- **数值抽验行须主会话复算**（b18 fix-1 教训）。
- **审查 findings 键名 check/name 混用**（b19）：merge 脚本双认 + 派发钉死 `"check"`。
- 在他批在途时刷新报告：`tools/report.py` 已修（缺失回执记 null），直接 `render/check --all` 即可。

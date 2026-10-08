# 2016 浙江卷理科 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2016 浙江卷理科整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b20 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2016_山东卷_文科`（b20）。

## Global Constraints

- 正式批次 `phase2-b21`；工作目录 `.work/phase2-b21/`。
- **并行会话**：phase2-b14（上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源三方已核定（下表）。
- 源 PDF 2 页 A3（印刷页 1027–1028），仅含题面；答案解析独立推导（等级 D）+ 异人盲核。
- **浙江卷结构：选择 1–8、填空 9–15、解答 16–20，共 20 题**（与山东 10+5+6 不同；须独立核验题型边界）；源不印总分与分值（待转录代理核实并登记），照录不补。
- **规范源写裸 `%`（构建前强制 grep 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- **解答题小问「（N） 内容」（N 后空格）**；长定义式用 `\frac` 非 `\dfrac`（b15/b16 教训）。
- **含 `&` 的 cases/array 必须行间 `\[ \]`**（b19 教训）。
- **CJK 不得裸进数学模式（b20 教训）**：`\(\text{中文}\)` 或纯文本；build 后必查四日志 `Missing character`。
- **图标签必须 `inner sep=0`**（b18）且按源字形框中心显式坐标定位；源位拥挤时微调并留档（b19）。
- **图标签探针必须连通域量测**（b17/b18）：400 dpi 隔离探头 + 8-连通域，字母须为独立分量。
- **图源↔源保真度由主会话自查**（b19/b20 教训）：形状朝向、非直线要素（折断符号类）逐 path 清点；多卷同图互为对照物。
- **审查代理一代理 ≤8 页**（b16）；**findings 检查项键名统一用 `"check"`**（b19）；印刷版页眉页脚/「解析」孤悬等模板共性已在 prompt 注明为 b16 留档类防重复上报（b20 的代理间分歧教训）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 印刷页 |
|---|---|---|---|---|---|---|---|
| 浙江卷理科 | `gk-2016-regular-zhejiang-science` | `2016_浙江卷_理科` | `src-44a16a20fae82c0cb6461848d1d9d8ed36a2759ca1d748e965bbd5605e9db0a5` | `3f243e53bb72fc5e207e69071d91702d836e12026188fd65c552dd648de37e06` | `a5d27c9ea092897aa485080613dcd4c34db328ed` | `普通高考/2016/2016浙江理.pdf` | 1027–1028 |

## Review Focus

- **浙江卷结构独立核定**：8+7+5=20 题；解答题 16–20 共 5 题。
- 图形 **预期 5 处**（须独立核数）：第 6 题点列图（两射线上点列 Aₙ/Bₙ 与三角形 Sₙ，**项目首例**）、第 11 题三视图（单位 cm，含俯视图）、第 14 题四面体 PBCD 构型图（P 在平面外、D 在 AC 上）、第 17 题三棱台 ABC-DEF 线框（BE=EF=FC=1, BC=2, AC=3）、第 19 题椭圆坐标图（A(0,1) 与过 O 的直线）。
- 浙江卷特点（题号锚定防错位）：Q8 四选项均为长不等式、Q14/Q15 为多空填空、Q18 含 min{p,q} 分段符号、Q19(2)/Q20 为含参数证明题。
- 浙江文由后续批次（b22）做，一律以源页独立核定，文理不得互推。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the manifest and fixed upstream.
- [x] Render and inspect both pages; record visible title, structure and printed-page numbers in `.work/phase2-b21/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 results（2026-10-09）：** 固定 commit `34c13a6c…` 上 blob `a5d27c9e…`、SHA-256 `3f243e53…` 与 manifest 源记录（`src-44a16a20…`，ready、未绑定）三方一致；提取副本逐字节复验。目视确认标题「2016 普通高等学校招生考试（浙江卷理）」，印刷页 1027–1028（页脚居中），结构**选择 1–8 / 填空 9–15 / 解答 16–20 = 20 题**，源不含答案。图形预期 5 处（Q6 点列图、Q11 三视图、Q14 四面体、Q17 三棱台、Q19 椭圆）。页映射：Q1–17 → p1（1027），Q18–20 → p2（1028）。身份（paper_id `gk-2016-regular-zhejiang-science`/base `2016_zj_li`/目录 `2016_浙江卷_理科`）空闲。

### Task 2 — Transcribe and solve independently

- [x] 转录代理只写 `.work/phase2-b21/gk-2016-regular-zhejiang-science/questions.md`、`page-map.md`、`figure-inventory.md`。
- [x] 求解代理（不读转录稿）只写 `answer-solve.md`：逐题独立推导，标注不确定项。
- [x] 主会话逐题对照源页复核转录稿。

**Task 2 完结（2026-10-09）：** 转录代理交付三文件（questions 131 / page-map 306 / figure-inventory 347 行；**5 图以 45 条 SVG 路径逐条枚举**核数，非目测；实测确认含真实文本层、不印分值、不附答案）。**四类文本层缺陷已矢量补出**：Q2 三处 ∥（若只信文本层，「满足 m α」语义反转）、Q20 两条大绝对值竖线（6 个字形象限全无文本）、Q3 花括号落私用区、拉伸定界符坐标失真；另登记 11 处作答横线为 0.42pt 矢量线段。**三处存疑均已处理**：F01-1 两射线有意截断（顶点在图外，端点横差仅 0.40pt 被同竖线切齐）、F02-1 侧视图下半中竖线源内为虚线（照源复刻）、F05-1 x 轴左右不对称延伸（登记）。盲解代理 20 题全交付（高 19 / 中高 1（Q15）；速查：1B 2C 3C 4D 5B 6A 7A 8D / 9:9 10:A=√2,b=1 11:S=72cm²,V=32cm³ 12:a=4,b=2 13:a₁=1,S₅=121 14:1/2 15:1/2；16(2) **A=π/4 或 π/2 双解**（B=π/8、π/4 均已代回验证）；17(2):√3/4；18:①[2,2a] ②m(a)/M(a) 分段；19:(0,√2/2]（后台精细扫描独立复证阈值）；20 证明）。**主会话独立复算抽验 12 项全吻合**（Q1/Q3 投影区间/Q5 周期/Q7/Q9/Q10/Q12/Q13/Q16 双解/Q18 全链/Q15 数值链）。转录格式（半角标点 117 处、`______` 等）由主会话在定稿时统一为项目惯例。

### Task 3 — Integrate and register

- [x] 规范三件套 + 含解析派生 + 5 幅 TikZ 图源。
- [x] 注册 `phase2-b21`；provenance 三角色导入。
- [x] 生成项目源与四版本外壳，三连 check。

**Task 3 完结（2026-10-09）：** 规范三件套（试题/答案要点/解析正文）；5 幅 TikZ 图源按本卷 SVG 清点独立重绘——F01 点列图（两条截断射线、三个 fill-opacity 0.1 灰三角形、16 组下标标签）、F02 三视图（正视图缺左上格/侧视图缺右下格含虚线段/俯视图右列上半、6 条尺寸线+12 实心箭头+9 标签）、F03 四面体（虚 DC）、F04 三棱台（虚 AC、额外 BF 线段）、F05 椭圆（0.8pt 双倍线宽、轴比 5:3 示意）。**两处解析器拦截（工具设计生效）**：① 答案要点 Q18(2) 的 ①② 独立成块（且含行内 & cases）被拒——按 b19 范式改写为单块 ①②；② 解析版两处长式 Overfull（20.4pt/26.7pt）——拆行修复后归零。注册 rev 3497、provenance 3498、extract/generate/三连 check 全绿；探针编译 5 页零告警、五图目视与源一致。

### Task 4 — Build, review, and close

- [x] 正式构建（构建前 grep `\%` 自检）→ **主会话先自查全部图**（含 400 dpi 连通域与源↔成品保真对照）→ 派审查代理（≤8 页/代理）。
- [ ] 修复轮（如有）→ 重建 → 像素差分 → 变化页二轮复审 → 合并。
- [ ] finalize → 报告刷新（带 --manifest/--issues，manifest_csv 在仓库根跑）→ 全量测试 → 清理中间件 → 显式路径提交（不 push）。

**Task 4 首建（2026-10-09）：** 四版 5/19/7/15=**46 页**、零失败；Overfull 修复后归零、四日志零 Missing character。审查 7 段已派（试题 5、简答 7、解析 19 三段、印刷 15 两段；attempt `1a93f4a6`，`prepare-batch` 已换绑；prompt 键名钉死 `"check"`、附 b16 留档口径与 Q16 双解提示防误报）。

## 已知口径与坑（b11–b20 沉淀）

- 四版本口径：试题版=纯题面；解析版=题目+完整解析；简答版=题目+答案速查；印刷版=题目+完整解析紧凑排版；「见解析版」为生成器既有口径。
- 规范源写裸 `%`；解答题小问「（N） 内容」；长定义式 `\frac`；TikZ 图源全坐标统一缩放（照源 pt 换算）、框图显式坐标逐段独立 draw、回边 `|-` 目标点注意穿框。
- **图标签 `inner sep=0`**（b18）；**标签并入三成因**（inner sep 移位／源位拥挤微调）；探针必须 400 dpi 连通域量测。
- **分页守卫注入规范源**（b17）：`\Needspace{N\textheight}` 独立行于题前；N 按题块实测高且须大于该处剩余。
- **留白口径**（b17）：末页填充下限参考 ≈27%；宏级确定性留白单独判 pass。
- **公共宏/转换器（`common/*`、`md2tex.py`）是全项目回执依赖闭包**：齐左、留白、「解析」标签孤悬、印刷版页眉横线短/页脚左偏类均留档不修（b16 裁定；根因见 b20 记录：`\headwidth` 与壳 `\geometry` 失同步）。
- **dfrac 选项行→「解析」标题墨迹间隙 ~1pt 为紧凑排版常态**（b19/b20 裁定：无重叠即 pass+note，不改源）。
- **数值抽验行须主会话复算**（b18 教训）。
- **CJK 入数学模式＝静默缺字**（b20）：用 `\text{}` 或纯文本；build 后必查四日志 `Missing character`。
- **源↔成品图保真由主会话对照**（b19/b20）：轴类非直线要素逐 path 清点；形状朝向逐一核。
- 在他批在途时刷新报告：`tools/report.py` 已修（缺失回执记 null），直接 `render/check --all` 即可。

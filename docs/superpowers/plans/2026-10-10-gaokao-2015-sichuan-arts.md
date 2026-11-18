# 2015 四川文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 四川文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b07 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**与刚完成的 2015 北京文卷（phase3-b07）同构**：A3 横向三栏书刊合排（印刷页码 **983/984**）、LaTeX（CM 系）重排产物、21 题结构（选择 1–10＋填空 11–15＋解答 16–21）、**无答案页（等级 D）**。

建模先例：`2015_北京卷_文科`（phase3-b07）。

## Global Constraints

- 正式批次 `phase3-b08`；工作目录 `.work/phase3-b08/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`（**实证**：该 commit 与上游当前 HEAD 266afe22 之间「普通高考/2015」零差异，四川文 PDF blob 两处逐字相同 c6bb92af…）；固定源已核定（下表）。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 983＝选择 1–10＋填空 11–15＋解答 16–18；p2 印 984＝解答 19–21）→ **答案证据等级 D**（解析全由盲解撰写）。
- **图形/表初判 4 处**：Q6 程序框图（7 框：「否」右回边；开始/结束圆角、k=1、k=k+1、S=sin(kπ/6) 矩形、k>4? 菱形、输出 S 平行四边形）；Q17 座位表（带框线表格＋「乘客/座位号」斜格表头＋P1–P5 列头＋两行示例坐法）；Q18 正方体平面展开图＋直观图（**两幅一体**，字母标记）；Q20 椭圆图（短轴 CD 上 P(0,1)、过 P 动直线、A/B 弦点）。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- 沉淀纪律（b15–b23/phase3 全量）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学；**答案行含 `*` 已由 md2tex 治本（2026-10-10）**；**规范源反引号内禁裸 `$`（写 `\$`）、禁包 LaTeX 命令、禁空参数命令**；↔ 等 lmroman 无字形符号不裸入正文；图标签 `inner sep=0`、分数型标签按源墨迹定位；**差分同引擎 pdftoppm**；审查代理 ≤8 页；**图自查含线段采样矩阵（按源实测参数！弧类禁按自画参数采样——自证循环）＋判据灵敏度自证**；**finalize-batch 先于 check-batch**；孤儿尾框/Needspace 留白/选项栏漂移/链接色为已接受类（b07 裁定）。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**的解析须流水式、答案单一答案行。
- 标点与记号照 b07 北京文口径（题号句末全角、正文逗号全角、正文层括号全角/数学内半角、选项标号半角照源、不等式 `\leqslant`、向量按源实测定）；**以四川文源页字体实测为准**。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 四川文卷 | `gk-2015-regular-sichuan-arts` | `2015_四川卷_文科` | `src-3c4280f311e3b5f3c7bf97218d91b40867297a48e0e475367d6e334b1c9dc915` | `6d10d9ebfea30b5e4af7f6bc3cdeb58284f62c0a61468fa4f1205f60fb48b` | `c6bb92afa84f99282b2ef4d42159b16099fe35ff` | `普通高考/2015/2015四川文.pdf` | 2 |

## Review Focus

- 21 题结构核定（题号连续、无分值印制）、无答案页（等级 D）。
- Q6 框图（7 框、「否」右回边竖排流程）与 Q18 双图（展开图＋直观图，字母标记齐全、虚实口径）按源复刻。
- Q17 座位表（带框线表格的斜格表头与列头排印）照源。
- Q20 椭圆图（P(0,1) 在短轴 CD 上、过 P 动直线弦）按源复刻。
- 四川文理对照物（2015 四川理卷未做，届时互为事后互证——不干预独立工作）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：cp 至 `.work/phase3-b08/source/2015四川文.pdf`，现场 sha256＝`6d10d9eb…`（与 manifest artifact.sha256 逐字一致）；blob OID 两 commit 实证相同。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi，2481×1754）；`source-text.txt`（-layout，106 行）。
- [x] 版式判读：A3 横向三栏书刊合排；p1＝栏1（标题＋选择 1–5＋Q6 框图＋Q7）／栏2（选择 8–10＋填空 11–15＋解答 16 起）／栏3（Q17 座位表＋Q18 双图）；p2＝19/20/21（Q20 椭圆图）。页码 983/984（合订本）。LaTeX CM 系重排、全矢量、文本层完整。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–10 选择）：`.work/phase3-b08/transcripts/partA.md`（零存疑、双向机械核对；字体归属实测：CMMIB10 向量/MSAM10 ⩽/CMEX10 可伸缩括号/LMRoman10 半角标点判定）。
- [x] 转录 B（Q11–21＋图表实测清单）：`.work/phase3-b08/transcripts/partB.md`（含归一替换台账：逗号 75/句号 23/分号 12/小问 13 组等，总账闭合）＋ `.work/phase3-b08/figure-inventory.md`（451 行；**首代理因 API 429 中断于算术自查，续作代理 17 处实测订正全闭合**——含差 1 归属（p1 path 7 分数线）与 §6.3 基准发现（SVG 坐标带 0.999622 等比项，交叉比对须换算））。
- [x] 盲解 A（Q1–10）：`.work/phase3-b08/blind/partA.md`（1A 2B 3C 4A 5B 6D 7D 8C 9A 10D；Q6 逐轮模拟＋回接反证、Q10「垂足＝中点」精确分支逐条验证）。
- [x] 盲解 B（Q11–21）：`.work/phase3-b08/blind/partB.md`（7 个复算脚本；Q17 双口径、Q18 24 旋转枚举（含镜像登记）、Q20 精确分数、Q21 构造性证明）。

### Task 3 — Integrate and register

- [x] 规范三件套＋含解析占位；四项自检（`%`、空参数、反引号、CJK 入数学——5 处 CJK 全在 `\text{}` 保护内、合法）＋（N）空格锚点 13 处修复。
- [x] 解析正文 1010 行（3 改写代理分段 Q1–10/Q11–16/Q17–21 → 合并；改写 A/B 各含对盲解稿的实测订正：Q5 奇偶性、Q8 浮点、Q15④ 残差表述——结论均不变）。
- [x] TikZ 图源 3 处（f2015scw_q06_flowchart／q18_net_cube／q20_ellipse）+ 探针目检（零告警、三图与源结构吻合）。
- [x] 注册 `phase3-b08`（rev 3644）；provenance 三角色导入（rev 3645）；extract-batch 派生。
- [x] generate/short/editions 三连 write+check → build --formal **首轮 COMPILED_PENDING_REVIEW 0 失败**；**生成期修复轮**（解析版 3 Overfull＋1 Underfull → 0）：Q20 两式 aligned 断行（4.3pt/45.4pt）、Q19 化简改行间式（0.23pt）、Q17 验证段数字列表改全角逗号文本串＋拆段（Underfull 2205 → 0）→ 重建后**四版告警全 0**（7/42/9/30 页）。

### Task 4 — Build, review, and close

- [x] prepare-batch 换绑（构建后执行，工作项 7/42/9/30 核验一致）；**14 代理并发**（1 图自查＋13 段审查：试题 1（1–7）＋解析 6（1–7/8–14/15–21/22–28/29–35/36–42）＋简答 2（1–5/6–9）＋印刷 4（1–8/9–16/17–24/25–30））——进行中。
- [ ] 归集脚本预置（`.work/phase3-b08/collect_receipts.py`，EXPECT 7/42/9/30）。
- [ ] 裁定 findings → 修复轮（如有）→ 重建 → 差分 → 复审 → collect_receipts → finalize → check-batch → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push）。

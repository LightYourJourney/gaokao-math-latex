# 2015 北京文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 北京文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 b15–b23、phase3-b00–b06 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**与 b06 北京理卷同书连页**（理卷 935/936 已 FINALIZED，文卷 937/938）；A3 横向三栏书刊合排、LaTeX（CM 系）重排产物。

建模先例：`2015_北京卷_理科`（phase3-b06）。

## Global Constraints

- 正式批次 `phase3-b07`；工作目录 `.work/phase3-b07/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源已核定（下表）。
- 源 2 页 A3 横向三栏，**无答案页**（等级 D）→ 解析全由盲解撰写、两路互证。
- **文理对照纪律（防泄漏）**：b06 理卷（`2015_北京卷_理科`）已完成并 FINALIZED——**转录/盲解代理一律不得读取其任何产物**（文理存在同题，防污染）；**体例模板一律用 b05 上海理卷**（跨省无重叠）。文理互证由主会话在整合后做（文理同题/异数清单届时逐条列）。
- **图形（初判 5 处）**：Q5 程序框图（开始/结束、赋值框、判断菱形——与理卷同型不同内容）；Q7 三视图三联；Q13 线性规划图（坐标轴+三角形区域，含 O/B(1,0)/A(2,1)/C(0,2)）；**Q14 双散点图（新图元：两幅密集散点、甲乙丙标注）**；Q18 三棱锥 V-ABC（M、O 中点，虚线隐藏棱）。
- **规范源写裸 `%`（构建前强制 grep 自检，含空参数命令、反引号、数学内 CJK 自检）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项；`manifest_csv.py --write` 须在仓库根运行。
- 沉淀纪律（b15–b23/phase3 全量 + b05/b06 新增）：解答题小问「（N） 内容」（**「（N） 」后空格＝extract-batch 硬锚点，漏写硬报错**）；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学；答案行裸 `*` 用 `\ast`；**说明框一律写 Unicode 码位不写字面数学字形**（⩽⩾∠ 等 lmroman 缺字形）、图例标记用 `\(\bullet\)` 族；**长内联数学链拆 、组或 aligned**（Overfull 族先例）；反引号内禁裸 `$`、禁包 LaTeX 命令；图标签 `inner sep=0`、分数型标签按源墨迹定位；**图源内元素位移前判包围盒边界成员（是则 overlay）**；**图文清单散文与坐标区间矛盾时一律以坐标区间为准**；**差分同引擎 pdftoppm**；审查代理 ≤8 页；图自查含线段采样矩阵+转变计数+**判据灵敏度自证**；finalize-batch 先于 check-batch。
- 标点口径照全库约定（题号句末全角「．」、正文逗号等全角、数学内半角、选项标号半角照源、`\leqslant`；以北京源页字体实测为准）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 北京文卷 | `gk-2015-regular-beijing-arts` | `2015_北京卷_文科` | `src-d0b941bc2d6452a8ed6284fd56e7bb77fa5344766f53cd0dd4ed76f4cb6625bc` | `69517ac5eb73d4388a2b873c17b34aecd8a1c2e46108c10ba51b6134c0a6ca3b` | `833c3dff1be63bf5c763d46af00b451d73d1fd5e` | `普通高考/2015/2015北京文.pdf` | 2 |

## Review Focus

- Q14 双散点图为**新图元**（两幅、数十散点、甲乙丙标注）——图清单须逐点记录坐标；图自查须逐幅核点数与关键位置。
- Q13 线性规划图（坐标轴+射线三角区域）、Q17 表格（tabular 照源）、Q18 三棱锥（含中点与虚线）。
- 文理互证：整合后主会话列文理同题/异数清单逐条核对（对照物＝b06 理卷，仅主会话可用）。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] Recompute source SHA-256/blob OID and page geometry against the fixed upstream.
- [x] Render and inspect all pages; record visible title, structure and printed-page numbers in `.work/phase3-b07/`.
- [x] Confirm batch/source/paper/project/path identities are collision-free before registration.

**Task 1 结果（2026-10-10）：** 固定 commit `34c13a6c…` 树内 blob `833c3dff…`（`git rev-parse` 核验）与提取副本 SHA-256 `69517ac5…` 与 manifest 源记录（`src-d0b941bc…`，ready 未绑定）一致。目视：**A3 横向（1190.55 × 841.89 pt）三栏书刊合排**（与理卷同书连页：理 935/936→文 **937（p1）/938（p2）**）；标题「2015 普通高等学校招生考试（北京卷文）」；结构＝选择 1–8＋填空 9–14＋解答 15–20（共 20 题；p1＝1–16、p2＝17–20）；图形 5 处（Q5 程序框图、Q7 三视图三联、Q13 线性规划图、Q14 双散点图、Q18 三棱锥 V-ABC）；**全 2 页无答案**（等级 D）。身份（paper_id `gk-2015-regular-beijing-arts`／项目目录 `2015_北京卷_文科`／批次 `phase3-b07`）双命名空间空闲。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [ ] 转录 A：选择 1–8 + 填空 9–14（p1 全栏）+ 全 2 页 page-map（三栏栏序/坐标实测）。
- [ ] 转录 B：解答 15–20（p1 右栏 + p2）+ 图清单（5 处逐要素实测）。
- [ ] 盲解 A：本库 1–14；盲解 B：15–20。**禁读 b06 理卷任何产物**。
- [ ] 主会话逐题对照源页复核转录稿；盲解互证；文理互证（事后）。

**Task 2 结果（2026-10-10）：** 四代理全交付（转录 A 77 行＋page-map 327 行；转录 B 84 行＋图清单 518 行·5 图＋Q17 表框＋存疑 S-1…S-13；盲解 A/B 全覆盖多路校验）。**主会话复核与裁决**：① 标点归一全角（源半角 47 处，按全库约定）；② 题号两稿不一致统一全角「．」；③ Q14 源图与题干不符（左 35 点/右 37 点、未配对、甲乙仅左幅丙仅右幅）——照源复刻＋存疑登记，② 按跨图定位法读出「数学」；④ Q17 表 (217,丁) 格经字形墨迹复核为 √（文本层词盒偏移不可判格——已录 S-13）；⑤ 第 6 题「∥」矢量画、Q6 向量为粗斜体（\boldsymbol）；Q19 e 正体（\mathrm{e}）；⑥ **字面数学符号禁入正文（b06 教训）**：两稿中 √/×/⟺ 等 50+ 处已批量改为 \(\surd\)/\(\times\)/文字（含表格单元格——md2tex 单元格支持行内数学已核）；四张表按本库制表规范以 markdown 表录入（→booktabs）。两待写稿四项自检全过。

### Task 3 — Integrate and register

- [x] 规范三件套（试题/答案要点/解析正文）+ 含解析占位（解析正文 3 改写代理分段→合并 607 行、29 验证段；四项＋字面符自检全过；含 Q10 指数纠错裁定：盲解稿 2^{−1/3} 误读→2^{−3}，四证同向、答案不变；Q17 条件概率口径 600/685≈0.876）。
- [x] TikZ 图源 5 处（f2015bjw_q05_flowchart／q07_three_views／q13_linear／q14_scatter／q18_pyramid）生成 + 探针零告警；q14 右幅散点漏加面板偏移 +176.2461 已修复（图自查伏笔）。
- [x] 注册 `phase3-b07`（rev 3627）；provenance 三角色导入（rev 3628）；extract-batch 派生（含解析.md 以修复后内容重新派生）。
- [x] generate/short/editions 三连 write+check → build --formal：**COMPILED_PENDING_REVIEW，1 待审 0 失败、四版告警全 0、6/31/8/24 页**。构建期两修：`\%` 被渲染器再转义（`\(2.5\%\)`→`\\%`→Missing $、latexmk 12；全库扫 `\%` 修 4 处为裸 %——b13/b15 后第三犯）；说明框反引号内字面 ⩽ 入 lmmono 缺字形 ×4 版（去反引号改述）；解析版 Overfull 54.9pt（Q15 辅助角长链→aligned）、印刷版 Underfull 1314（Q13 验证段改写缩短盒链）。

### Task 4 — Build, review, and close

- [x] 审查代理（1 图自查 + 9 段并发，2026-10-10 全部返回）：图自查＝**30 处实例全 pass**（含判据灵敏度自证 5/5；记录差异：箭头形制 stealth vs 源平底三角 0.8pt、分式横线字体度量差、源清单「21 段」笔误——源与成品实测一致 20 墨段/38 转变）；9 段审查＝**八项全 pass、0 fail**（各段 findings 见裁定记录块）。
- [x] 归集链路预置：`.work/phase3-b07/collect_receipts.py` 已按 b07 口径适配（EXPECT 6/31/8/24）；`prepare-batch` 已跑（4 工作项页数核验一致）。
- [x] **裁定＋值域归一**（11 锚点注入）：印刷版 seg1 p3/p6、seg2 p14 的 3 处 `flag`→`pass`（Needspace 断页留白接受类）；试题版 p1「（见答案）」悬空指针→pass 留档（编辑透明性注释、零泄漏、四版共享源无兼容改法）；解析版 seg2 p11 孤儿尾框→**新接受类留档**（p11→12、p13→14 两例，主会话亲验 p12 顶「答案：B（4）」孤悬于第 6 题标题之上；消除需公共宏粘合→全局轮候选）；选项栏漂移→pass 留档（全库 73 行中 65 单全角空格约定，b05 先例）；解析版 seg2 p9 回链数字链接色→pass 留档（preamble colorlinks，全局轮候选）；Q16 修复注记注入解析版 seg3 p21＋印刷版 seg3 p17。
- [x] 修复轮（Q16 缺框）：根因＝md2tex ANSLINE（转换器级，已修＋回归测试）；`generate/short/editions` 三连 check 全绿（手改 answers.tex 与修后转换器重生成逐字一致）→ `build --formal` 重建 **COMPILED_PENDING_REVIEW 0 失败**。
- [x] 同引擎差分（100dpi AE）：**变化页恰 5 个**——解析版 p21–24（Q16 框出现＋连锁 reflow，p25 起归零）＋印刷版 p17（余量吸收无连锁）；试题版/简答版全零。主会话亲验：解析版 p22 顶部 Q16 两枚绿框齐备归位。定向复审代理覆盖 5 页（进行中）。
- [ ] 复审结果注入 seg 回执 → collect_receipts → finalize（--output-report reports/phase3-b07.md）→ check-batch → 报告刷新 → 全量测试 → 清理中间件 → 显式路径提交（不 push，注明 b14 在途）。

#### Task 4 附：全库同型修复（转换器已修，三卷待走修复轮）

**已完成（2026-10-10）**：`md2tex.py` ANSLINE 修复——`[^*]` 字符类对含星答案值（`\mathbf N^{*}` 类）失配致 `\textbf` 退化；新正则允许内容含单个 `*`（排除成对 `**`）。回归测试入 `tests/test_generate_projects.py::ConversionInterfaceTests::test_answer_line_with_an_asterisk_still_gets_the_answer_box`（35/35 过）。`generate --all --check` 全库爆炸半径＝**恰 3 卷**（其余 250+ 卷零影响）：
1. `2017_北京卷_文科`（answers.tex:535）
2. `2019_全国Ⅰ卷_文科`（answers.tex:798）
3. `2021_新高考Ⅱ卷`（answers.tex 含星答案行）
三卷均四版齐全、rebuild 状态：2017 北京文 production_state=compiled（批 phase2-b08 仍 compiled_pending_review）、2019 全国Ⅰ文 compiled（批 phase0-b02 同前）、2021 新高考Ⅱ卷 **complete（批 phase0-b03 closed——真·已 finalize）**。

**已执行（2026-10-10，当日收官后立即）**：三卷 `generate --write`（全库 `--all --check` 复绿＝**264 套一致**）→ short/editions 三连 check 全绿 → `build --formal` ×3 全成功（0 失败）→ 同引擎 100 dpi AE 差分（对照 `.work/starfix-3vol/prefix-build/<卷>/` 基线）：**变化页恰 6 个、模式整齐**——每卷「解析版 1 页＋印刷版 1 页」：2017 解析 p18(24669)/印刷 p13(1226)、2019 解析 p21(1382)/印刷 p18(1177)、2021 解析 p22(2790)/印刷 p16(2266)；试题版/简答版全卷 AE=0。定向复审代理覆盖 6 页（进行中）。

**收据策略（本次裁定）**：`build.json` 由 build 自动刷新（新 attempt、现行工具链，三卷借此**离开** poppler 失配类）；`review.json` **不擅动**——它是各自批次 finalize 的冻结产品，重开需整批 prepare/collect/finalize（批内尚有未审兄弟卷、超出本修复范围）；三卷 review 回执与最新 attempt 的失配如实随提交注明，待各自批次下一次正规流程（b08 待审、phase0-b02 待审、phase0-b03 已 closed 属维护轮）自然刷新。产物质量由 6 变化页定向复审＋全库 generate/check 复绿背书。

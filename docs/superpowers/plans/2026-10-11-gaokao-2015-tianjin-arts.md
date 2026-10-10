# 2015 天津文卷 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` to implement this plan task-by-task. 卷面转录与独立求解由不同角色分头完成，主会话独占规范整合、manifest、回执与提交。Steps use checkbox (`- [ ]`) syntax.

**Goal:** 将固定上游中的 2015 天津文科卷整理为可追溯、可编译、可逐页复核的四版本 LaTeX 项目。

**Architecture:** 同 phase3-b00–b09 批次：固定来源 ID 是身份根；转录与盲解角色分离；规范三件套 + TikZ 图源由主会话整合；不提交扫描件与构建中间件。**与 2015 四川文/理（b08/b09）同属 2015 合订本族**：A3 横向三栏书刊合排（印刷页码 **987/988**）、LaTeX（CM 系）重排产物、**无答案页（等级 D）**。题量 **20 题（选择 1–8＋填空 9–14＋解答 15–20）**。

**Spec:** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md` 与仓库 `CLAUDE.md`。建模先例：`2015_四川卷_文科`（phase3-b08）、`2015_四川卷_理科`（phase3-b09）。

## Global Constraints

- 正式批次 `phase3-b10`；工作目录 `.work/phase3-b10/`。
- **并行会话**：phase2-b14（2016 上海文理）由另一会话推进；提交全程**显式路径** `git add`，绝不 `-A`、不 push。
- 固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；固定源已核定（下表；sha 与 manifest 逐字一致；**blob 在 34c13a6 与上游 HEAD 266afe2 实证相同**）。
- 源 2 页 A3 横向三栏，**无答案页**（p1 印 987、p2 印 988）→ **答案证据等级 D**（解析全由盲解撰写）。
- **2015 天津理尚未开始**——本批无文理对照物；隔离禁令仍按全路径面写：**转录/盲解代理不得读取任何他批/他卷产物（含 `.work/` 下其它批的全部文件与他卷 md/tex）**（b09 教训：隔离面写窄会被字面绕过）。
- **图形/表初判 4 处（待转录 B 实测确认）**：Q3 程序框图（p1 栏 1，7 框：开始／S=10,i=0／i=i+1／S=S−i／S≤1?／输出 S／结束，「否」支右回折）；Q6 圆图（p1 栏 2 上部，圆 O 上弦 AB、M/N 三等分点、CD 与 CE 过 M/N，标签 A/B/C/D/E/M/N/O）；Q10 三视图（p1 栏 2 中下部，正视图＋侧视图＋俯视图三联、含尺寸箭头与单位 m）；Q17 立体几何图（p2 栏 1，A₁ 顶上、BB₁∥AA₁、E/F 中点）。
- **规范源写裸 `%`（构建前强制 grep 自检，并加扫空参数命令 `\\[a-zA-Z]+{}`＋孤需参宏 `\\([a-zA-Z]+\)`）**；重编后先 `prepare-batch` 换绑 attempt 再写工作项。
- 沉淀纪律（b15–b23/phase3 全量 + b08 + b09 新增）：解答题小问「（N） 内容」；长定义式 `\frac`；含 `&` 的 cases/array 行间 `\[ \]`、答案行用 `$...$`；CJK 不入数学（用 `\text{}`——**注意显示式内 `\text{CJK␣}` 尾随空格会丢、须写 `\text{CJK}\ `**）；**答案行含 `*` 已由 md2tex 治本**；**规范源反引号内禁裸 `$`（写 `\$`）、禁包 LaTeX 命令、禁空参数命令**；↔ 等 lmroman 无字形符号不裸入正文；图标签 `inner sep=0`、分数型标签按源墨迹定位；**差分同引擎 pdftoppm**；审查代理 ≤8 页、**524 限流时分批 ≤4 支补派**；图自查含线段采样矩阵＋**判据灵敏度自证**；**finalize-batch 先于 check-batch**；**not_applicable 必须写理由**；孤儿尾框/Needspace 留白/选项栏漂移/链接色为已接受类；**四项自检扩第 5 项「孤需参宏扫」**——`\(需参宏\)` 无实参（如 `（\(\dfrac\)）`）会让 LaTeX 吞掉 `\)` 致构建失败且四检全漏，凡 `\(...\)` 内只含一个需参宏即违规（b09 实案）；**行宽判据双口径**——`pdftotext -bbox` 的 xMax 含行末全角标点 advance 高估（~9pt 伪影），判溢出前先测全版常态、确证用墨迹像素实测（b09 定型：解析版版心 532.92／印刷版 549.9）；**分数系数以渲染图为准**（pdftotext 文本层可能吞 ½ 类符号——b09 Q9 实案）；**审查代理中途回报可能为「中途稿级」错误结论，只信落盘 JSON＋主会话亲测**（b09 印刷版 seg3 实案）。
- **答案要点禁「① 答案：」式**；主选择组逐题答案**纯字母**（`**答案：A**`）；**单题面题**的解析须流水式、答案单一答案行。
- 标点与记号口径以**天津文卷源页字体实测为准**（题号句末、正文标点半角→全角归一、选项标号、不等号字形、向量记号——四川理卷无 CMMIB10 用 `\overrightarrow` 不加粗、四川文卷有 CMMIB10 加粗，**天津卷以实测定**）。

## Fixed Sources

| 试卷 | paper_id | 项目目录 | source_id | SHA-256 | Git blob OID | 上游路径 | 页数 |
|---|---|---|---|---|---|---|---|
| 天津文卷 | `gk-2015-regular-tianjin-arts` | `2015_天津卷_文科` | `src-2a48e998637ee8209b7b54a1c74fff26ed06b78e3473302e92038b7e064807e9` | `f553ca14c57bb6229bc5fd224afd1c11ccbbfc6761144fe3b17ba2a38eecdb17` | `00ae7ebafc29bb4b6980efb6cb828b2d990f2a29` | `普通高考/2015/2015天津文.pdf` | 2 |

## Review Focus

- 20 题结构核定（选择 1–8＋填空 9–14＋解答 15–20；题号连续）、无答案页（等级 D）。
- Q3 框图（新题面：「S=10,i=0」初值链与 S≤1? 判据——与四川卷框图不同构）按源复刻。
- Q6 圆图（三等分弦 + 两割线，新图元类型）与 Q10 三视图（三联图＋尺寸箭头）按源复刻；Q17 立体图（AA₁⊥平面、BB₁∥AA₁）双代理互证。
- 椭圆 Q19（上顶点/左焦点、λ=|PM|/|MQ| 与 |PM|sin∠BQP 双条件）与函数 Q20（切线与两实根不等式）逐题双代理互证。

## Tasks

### Task 1 — Freeze and visually identify the source

- [x] 源冻结：cp 至 `.work/phase3-b10/source/2015天津文.pdf`，现场 sha256＝`f553ca14…`（与 manifest artifact.sha256 逐字一致）；blob OID `00ae7eba…` 在 34c13a6 与上游 HEAD 266afe2 实证相同。
- [x] 页面图像化：`src-1.png/src-2.png`（150 dpi，2481×1754）；`source-text.txt`（-layout，124 行）。
- [x] 版式判读：A3 横向三栏书刊合排；p1＝栏1（标题＋选择 1–5＋Q6 起）／栏2（Q6 圆图＋选择 7–8＋填空 9–14 含 Q10 三视图）／栏3（三、解答题 15–16）；p2＝栏1（Q17 立体图＋Q18）／栏2（Q19 椭圆）／栏3（Q20）。页码 987/988。LaTeX CM 系重排、全矢量、文本层完整。

### Task 2 — Transcribe (2 agents) and solve independently (2 agents)

- [x] 转录 A（Q1–8 选择，含 Q3 框图与 Q6 圆图的存在性登记）：`transcripts/partA.md`（134 行；`\leqslant` MSAM10 三重闭合、无 CMMIB10、`\complement` U+2201、引号顿号全角/其余半角实测；7 条存疑）。
- [x] 转录 B（Q9–20＋图表实测清单）：`transcripts/partB.md`（143 行）＋`figure-inventory.md`（283 行；pdftocairo 换算因子自行反算 a≈0.999621/+0.1044；栅格 100%/0.170pt；∥ 吞噬两处；4^{1/3} 竖排分式判定；S-1…S-10）。
- [x] 盲解 A（Q1–8）：`blind/partA.md`（B C C A D A B A；Q3「输出 S」矛盾独立发现）；盲解 B（Q9–20）：`blind/partB.md`＋`recheck-B.py`（全断言过；Q19 四尺度三路径、Q20 1998 网格；6 条存疑）。
- [x] **所有四代理 prompt 均含隔离禁令**（全路径面：他批/他卷/`.work/` 其它批；四代理均自证未读）。

### Task 3 — Integrate and register

- [x] 规范三件套＋含解析占位；五项自检全清（三份 md＋合并稿）；小问集合解析↔试题一致 [1,2,3]；`validate_solution_body` 工具校验通过；3 改写代理（176/156/281 行）合并 606 行。**Q3 裁定**：照源复刻（题干问 i、框图印「输出 S」）＋存疑登记；**Q18(2) 错位相减中间行订正**（盲解稿括号漏末项、答案未动）。
- [x] TikZ 图源 4 处（235 行；113 项 tex↔清单残差**全 0.0000pt**；箭尖从 600dpi 墨迹独立重测（提取坐标系 +3.5pt 系统偏移弃用）；灵敏度自证过（唯一坐标注入）；四探针零告警；6 条存疑登记）。
- [x] 注册 `phase3-b10`（rev 3668）；provenance 三角色导入（rev 3669/3672）；extract-batch 派生。
- [x] 三连 write+check；首轮 build 0 失败；**生成期修复轮 2 处**（说明块裸 `∛` 缺字形×4 版 → 去字符；解析版 Q2 验证段长数字原子 Overfull 9.3pt → 改「与 9 的差在 10⁻⁹ 量级」表述）→ 重建**四版告警全 0**（7/31/9/24 页，attempt 3451c579）。

### Task 4 — Build, review, and close

- [x] 审查代理（1 图自查 + 10 段；分波 ≤5 支、零 524）：全部回收。修复轮两轮——① Q8 cases `&` 转义（试题 p4＋解析 p15 fail；改 `$...$` 包裹，b19 族）＋F01 标签越框（解析 p10 fail；图源缺字体设定继承 12pt）→ 重建；② 印刷版（zihao=5）\small=9pt 被判 figure_label fail×4 → 图标签改**绝对 10.5pt**（\fontsize{10.5pt}{12.6pt}，四版一致贴源）＋试题版说明块去答案值「4」＋答案要点 Q20(3) 悬空缩写改「故所证不等式成立」→ 重建。三轮均四版 0 告警；差分全归因；定向复审×2＋终复审×5 全过；33 页逐层替换合并**455 pass/0 fail/105 na**（70 页×8）。
- [x] finalize（final attempt 4b4342b6）→ check-batch → 报告 closed/passed/零问题 → unittest（862 项 1 失败＝既存基线 335 条）→ 清理中间件 → manifest_csv 775 行 → 显式路径提交（不 push）。

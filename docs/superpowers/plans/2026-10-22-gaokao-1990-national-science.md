# 1990 全国卷理科题库录入实施计划

> 本计划只覆盖下一套待录入试卷，不缩小项目 1952—2026 的总目标。主会话独占来源清单、批次与总报告；所有改动仅限 `feat/gaokao-phase0` 工作树，不触碰 Main 检出或用户的 `docs/design/` 改动。

**Goal:** 将经固定来源核对的1990全国理科26题录入共享LaTeX题库，生成可复用四版，并在证据不足处保留待核状态。

**Architecture:** 复用现有规范Markdown、`index.json`、逐题provenance、确定性生成器、来源事务和构建/复核回执；不修改共享模板或工具。原卷没有答案页，因此将推导与答案明确标为编者生成，`official_answer` 保持 `null`。

**Tech Stack:** Markdown、LaTeX、Python `unittest`、TikZ/PGFPlots、XeLaTeX、latexmk。

**Spec:** 当前高考真题 LaTeX 题库持续目标；项目流程见 `math-gaokao-latex/README.md`、`PROGRESS.md` 与 `CLAUDE.md`。

## 全局约束

- 固定输入为 `src-9c2fc92cdbbeac0484bf7355db2d32805c316e1a7be74e3bf175a3891a167a49`，SHA-256 `7801e6dab50ca58eabdc74d074cdaa7012cdee873dcc5304e0df37248986b43a`；不改写或替换来源。
- 页眉原文为“1990 普通高等学校招生考试（全国卷理）”；题面共26题：选择题1–15、填空题16–20、解答题21–26。
- Q5、Q11、Q20、Q23图稿必须为TikZ矢量重绘，不插入原卷截图；示意布局不得添加题设条件。
- Q9保留原图可见的 `\overline M\cap\overline N`；不得仅按 `pdftotext` 丢失上划线的文本层誊写。
- Q20原文没有给两侧体积 `V_1,V_2` 与图形区域的对应，保留源文并将答案方向标为待核，不能猜定顺序。
- 无来源的官方答案、评分标准、出版社或版次均不得补造；数学推导经独立核验后仍标记为生成解答，而非官方答案。

## Review Focus

- 数学上划线/分数/上标在PDF文本层可能缺失；以原页图像为准，并将高风险符号写入回归。
- 三维图的虚实线、点位与中点标签容易错配；按来源拓扑逐图核对。
- Q20的体积比有两个互为倒数的标记方向；测试和答案必须保留未决边界。
- 四版共享同一题面和答案源；生成后校验四入口没有各自维护的内容副本。
- 单页A3原卷缩放成A4后需检查公式、选项和图稿可读性；不能以编译成功代替视觉复核。

---

### Task 1：忠实题面、图稿与来源回归

**Files:**
- Create: `1990/1990_数学真题_全国理_试题.md`
- Create: `math-gaokao-latex/tests/test_1990_national_science_transcription.py`
- Create: `math-gaokao-latex/1990_全国卷_理科/figures/` 下Q5、Q11、Q20、Q23的TikZ源
- Generate: `math-gaokao-latex/1990_全国卷_理科/questions.tex`
- Update: `math-gaokao-latex/PROGRESS.md`

- [x] 先为来源SHA、26个题号/题型范围、Q9上划线、四幅矢量图链接与Q20待核状态写卷级回归测试。
- [x] 运行该测试确认它因目标题稿/图稿缺失而按预期失败。
- [x] 依据固定A3来源页完成逐题题面转录；四图只重绘原图拓扑，图文不补出未给条件。
- [x] 运行新回归及当前题面生成器检查；由独立复核者逐项对照原页，修正后再次运行。
- [x] 更新本进度，列明实际文件、题数、测试、未核点和下一步；仅提交本任务确切路径。

### Task 2：编者答案、解析及独立数学盲核

**Files:**
- Create: `1990/1990_数学真题_全国理_答案要点.md`
- Create: `1990/1990_数学真题_全国理_解析正文.md`
- Create: `math-gaokao-latex/1990_全国卷_理科/answers.tex`、`answers_short.tex`
- Update: `math-gaokao-latex/tests/test_1990_national_science_transcription.py`、`PROGRESS.md`

- [x] 按已核题面逐题推导，简答与详解共用同一份编者答案；没有来源答案的题不标作官方。
- [x] 由互不重叠的独立复核者仅看题面分段盲解；主会话比较差异并给出代数、定义域、几何与量纲检查。
- [x] 将Q20题意导致的 `V_1:V_2` 方向歧义保留为开放问题；不以答案推导消除题面歧义。
- [x] 运行该卷解答、简答一致性及来源状态测试；更新进度并提交精确文件。

### Task 3：规范登记、provenance与四版入口

**Files:**
- Create: `math-gaokao-latex/1990_全国卷_理科/` 下四个版本入口与 `provenance.json`
- Update: `index.json`、`source-manifest.json`、`manifest.csv`、必要的 `missing-issues.md`/批次报告、该卷测试与 `PROGRESS.md`

- [x] 仅在题签/固定来源关系通过既有登记门禁后，以 `gk-1990-regular-national-science` 建立canonical卷记录；出版社/版次仍保持未认证。
- [x] 按当前题面哈希登记逐题来源与验证状态，官方答案为 `null`、独立推导为生成内容；记录Q20阻塞。
- [x] 复用项目生成器产生四个独立编译入口；运行该卷生成、manifest、provenance及四版一致性检查。
- [x] 更新进度并提交本批所有权内文件，不包含构建产物、PNG/JPEG或 `docs/design/`。

### Task 4：正式构建、逐页视觉复核与批次报告

**Files:**
- Create/update: 该卷 `receipts/build.json`、`receipts/review.json` 与所属 `reports/` 批次报告
- Update: `source-manifest.json`、派生报告/CSV、测试与 `PROGRESS.md`

- [x] 通过provenance门禁后用XeLaTeX/latexmk正式编译试题、解析、简答、印刷四版；错误、缺字、引用和溢出按正式门禁处理。
- [x] 渲染并逐页完成八项视觉审查；区分通过、失败、not-applicable与仍待核内容。
- [x] 仅用事务工具登记当前回执；Q20或来源认证未解决时保持`blocked`/`closed_with_blockers`，不得标完成。
- [x] 跑该卷及report/manifest相关测试、`git diff --check`；更新全库投影并提交精确文件，不push。

执行记录见 `math-gaokao-latex/PROGRESS.md` 中的 1990 全国卷理科各阶段回执。最终批次 `phase4-b13` 为 `closed_with_blockers`：Q20 的 `V_1,V_2` 区域对应与来源出版版次/原件身份仍未核实；Task 4 完成不等于整卷解除阻塞。

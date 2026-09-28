# 2023 年全国甲理、乙文、乙理批次实施计划

> **For agentic workers:** 本批次按独立卷并行。每卷转录代理只写忽略的 `.work/phase2-b06/<paper_id>/`；题面复核与答案盲核必须由不同代理完成。主代理独占规范源整合、manifest、provenance、问题总账、回执与报告。

**目标：** 以固定上游 PDF 完成 2023 全国甲卷理科、全国乙卷文科和全国乙卷理科三套真题的逐页转录、独立解答与盲核，生成四版本 LaTeX，并依证据完成登记与批次验收。

**架构：** 沿用高考数学 LaTeX 设计规范与阶段 1/2 的 `source-manifest.json` 单一事实源、三份规范 Markdown 字段源、`provenance.json` 逐题证据及确定性项目生成链。每卷先由独立转录/解题代理建立草稿，再由另一代理盲核；主代理裁决差异后整合，按 `phase2-b06` 一次登记并统一生成、编译、视觉复核。

**技术栈：** Python 3.9 标准库、Bash 3.2、Git、XeLaTeX/TeX Live、latexmk、Poppler、TikZ/PGFPlots。

**依据：** `docs/superpowers/specs/2026-08-04-高考数学真题全量LaTeX工程-design.md`，尤其第 4、6–10 节；仓库根 `CLAUDE.md`；当前 manifest revision 3243。

## Global Constraints

- 上游固定为 `gaokaomath-src` 的 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；三份 PDF 的 source ID、路径、SHA-256 和 Git blob OID 以本计划及当前 manifest 为准。
- 仅从原 PDF 转录题面；PDF 文本抽取、文件名或既有同年其他卷均不能替代逐页视觉复核。题号、选项、公式、限定词、图表、页码和卷别必须与原件一致。
- 本地 2023 来源目录没有独立答案文件。无可靠外部答案材料时，仅在项目独立求解并经另一代理盲核后标答案证据等级 `D`；不得标为官方答案。冲突不能收敛或证据不足时标 `U`、登记问题并阻断该卷完成。
- provenance 的 `question-review`、`answer-solve`、`answer-review` 必须由不同角色承担：原转录/解题代理登记为 `answer-solve`，主代理在未查看答案草稿前独立逐页核对题面并登记为 `question-review`，另一盲核代理登记为 `answer-review`。
- 新图形必须是独立 `figures/*.tex` TikZ/PGFPlots 源；Markdown 用指向本卷登记 `.tex` 图稿的普通链接，禁止新增原卷截图、PNG/JPEG 或源 PDF 到 Git。
- 转录草稿和临时审查材料只写 `.work/phase2-b06/<paper_id>/`；主代理独占 `2023/`、`source-manifest.json`、`manifest.csv`、`index.json`、`provenance.json`、`missing-issues.md`、批次/全局报告、正式回执及生成器/模板。
- 四份 Markdown 字段源齐备、题量和图稿引用通过校验后，才运行 `register-papers` dry-run；dry-run 无冲突后一次性 `--write`。生成的 LaTeX、四版本入口和回执不得手改。
- 只清理本批 `build/` 中的 PDF 以外编译中间件与本批临时渲染；保留 12 个最终 PDF 在各自 `build/`（该目录按仓库规则忽略、不入 Git）。使用 `latexmk -c -outdir=build <edition>.tex` 清理辅助文件；不得使用会移除 PDF 的 `-C` 或 `build_projects.py clean-build --execute`。不碰上游仓库现有未跟踪文件；提交不 push。

## Review Focus

- 上游来源身份：内页标题、科类、地区文件名及纸面页码是否彼此一致；任一冲突须原样保留并记录，不静默纠正。
- 文理科题面差异：选项顺序、参数、条件和小问必须逐卷抄录，不能从对应的另一科或另一卷拷贝。
- 答案证据等级：盲核者不得查看首份答案/解析；每题终结论和推导相符才可记 `D`，否则 `U` 并阻断。
- 图稿忠实性：坐标、点名、虚实线、统计表/程序框图的分支与箭头必须由原 PDF 确认；不可确认时登记问题，不按数学常识补画。
- 交付洁净性：仓库只留可 diff 的 Markdown、LaTeX/TikZ 源及机器回执；源 PDF、渲染截图、PNG/JPEG、`.aux/.log/.fls` 等不得进入提交。

## 固定来源与试卷映射

| 卷别 | `paper_id` | 项目目录 | 规范 Markdown 前缀 | `source_id` | SHA-256 | 上游纸面页码 / PDF 题号映射 | 图示题 |
|---|---|---|---|---|---|---|---|
| 全国甲理 | `gk-2023-regular-national-a-science` | `2023_全国甲卷_理科` | `2023_数学真题_全国甲理` | `src-71b24de88d2093abd56878684c359bd1e361a4c4296f70d0648da7f591875dd0` | `47755f41bac1bf10552f5e22eb21720a6ffbc2414ab3b52b981c757c5cb9a756` | 1181–1182；PDF p.1: 1–19, p.2: 20–23 | 3 程序框图、18 三棱柱 |
| 全国乙文 | `gk-2023-regular-national-b-arts` | `2023_全国乙卷_文科` | `2023_数学真题_全国乙文` | `src-55877a8038ad7eefaf81441e1cb2209519093ff5d06614163386365b1694e5b5` | `6525ebd5c3be25a2cccff54034938963a28542bd2d682a2c352d61d691b2653e` | 1187–1188；PDF p.1: 1–19, p.2: 20–23 | 3 三视图、19 空间几何 |
| 全国乙理 | `gk-2023-regular-national-b-science` | `2023_全国乙卷_理科` | `2023_数学真题_全国乙理` | `src-427a0b0478bbef356f3bbaca4d406757df956bde371599a2c442a04873a193c4` | `04a0fd87993b56dde6189990ec44572ea9da95e93d50b74358e42c86ab9be572` | 1185–1186；PDF p.1: 1–19, p.2: 20–23 | 3 三视图、19 空间几何 |

对应上游路径为：

- `普通高考/2023/2023全国甲理(广西,贵州,西藏,四川).pdf`
- `普通高考/2023/2023全国乙文(河南,江西,陕西,甘肃,青海,内蒙古,宁夏,新疆).pdf`
- `普通高考/2023/2023全国乙理(河南,江西,陕西,甘肃,青海,内蒙古,宁夏,新疆).pdf`

三份来源目前均为 `ready`、PDF 结构检查通过、2 页 A3；甲理 blob OID `8cdd35de4dd2d4a078bd6111395a352b1e01e2c7`，乙文 `e6575dcf65413e7430af2fdf9b282c3ae62f7a78`，乙理 `dcfd4e1a755862422b81ce36b53b496dd9c81536`。每卷题量必须由核对后的 Markdown 计算，预期为 23 题但不允许为匹配预期而补写。

## 工作项

### 1. 冻结来源与批次

- [x] 复核上游 HEAD、三份 PDF 的当前 SHA-256、blob OID、页数与内页标题；确认三个 source 仍未绑定且 paper ID、目录、`phase2-b06` 均未占用。
- [x] 用只读检查冻结题号—PDF 页—印刷页映射、各题型和全部图形位置；保留源文件中任何不确定处作为待核，不预先改写 manifest。

来源预检于 2026-09-28 完成：上游 HEAD 与固定 commit 一致；三个 PDF 均为 A3 两页，内页标题与科类相符；第 1 页为题 1–19、第 2 页为题 20–23。版面大标题为“一、单选题”“二、填空题”“三、解答题”；本项目 2023 同年卷现行结构将 1–12 归为选择题、13–16 填空题、17–21 解答题、22–23 选做题。三个新卷的转录须忠实保留 PDF 上实际印出的分节文字，登记结构时按逐页复核后的题目作答规则确认，不得自行补入原卷未印出的分节说明。三份 SHA-256 与 manifest 的 `artifact.sha256` 一致，source 均 `ready` 且 `paper_id=null`；三个项目目录与批次 ID `phase2-b06` 均空闲；`source_manifest.py validate --require-artifacts 775` 退出码 0。

### 2. 并行转录与解题草稿

- [x] 同时派三名互不重叠的转录/解题代理，一卷一人，各自只写 `.work/phase2-b06/<paper_id>/`：题面 Markdown、答案要点、详细解析、TikZ 图稿、逐题 PDF 页映射、答案推导和疑点报告。
- [ ] 每名代理先视觉检查 PDF 两页，再以文本抽取辅助；逐题核对选择题、填空题、解答题及全部图形。每题答案注明独立推导，不伪称官方材料。
- [ ] 草稿需附题目数、选择/填空/解答题号范围、图形文件及引用次数、各题答案、推导摘要和任何无法确认的原文/图形。

### 3. 独立盲核与主代理裁决

- [ ] 每卷另派一名不同代理；只给该卷原 PDF 与题面草稿，不提供首份答案文件。盲核者逐题重解并独立对照原卷，输出自己的答案、推导及题面差异。
- [ ] 主代理逐题比对盲核与初稿，复算计算题、概率统计和单位；相异答案先回到原题条件求解，无法收敛则保留两方依据、立 `U` 问题，不把该卷设为 complete。
- [ ] 对题面差异建立锚点矩阵（题号、PDF 页、原文、草稿、裁决）；逐页无遗漏后才冻结草稿。

### 4. 整合、登记并生成

- [ ] 主代理将核准内容整合为三卷各自 `_试题.md`、`_答案要点.md`、`_解析正文.md`，答案文件明确说明“由本库独立推导、非官方答案”，并注明独立盲核；`_含解析.md` 由 `solution_sources.render_combined()` 真实生成。
- [ ] 图稿只入相应 `figures/*.tex`；Markdown 链接指向本卷已登记图稿。运行题量、题号、图形引用、生成器无漂移、问题及 schema 检查。
- [ ] 写批次注册规格，dry-run 检查三卷 source/paper/batch 映射、路径与字段；无冲突后一次 `register-papers --write`，随后初始化并导入逐题 provenance，题面核验和答案等级按各自角色准确登记。
- [ ] 使用生成器产出 `questions.tex`、`answers.tex`、`answers_short.tex` 和四个版本入口；更新项目索引投影，不手改生成文件。

### 5. 构建、视觉复核与结项

- [ ] 对 3 卷 × 4 版本统一重编译；检查 XeLaTeX 退出码、Missing character、未解析引用、PDF 页数、输入闭包哈希和 Overfull/Underfull。
- [ ] 每卷检查四版首页、题面密集页、所有图形页、解析起始页、简答页、印刷拥挤页和末页；截图仅临时保存且不提交，正式 review 回执绑定本轮 PDF 与输入哈希。
- [ ] 对照答案要点与详细解析的 23 题结论；执行来源、manifest、provenance、结构、构建、review 和报告门禁。不可解决项保持 `U`/blocked，按实际状态关闭批次。
- [ ] 更新 `manifest.csv`、问题总账、批次报告及全局报告；清理本批 PDF 以外编译产物与临时渲染；`git diff --check`、审阅精确暂存区并提交本批，不 push。

## 验收标准

- `phase2-b06` 仅登记上述三个 source/paper 映射，manifest revision 和 CSV 投影同步。
- 每卷题量、题号、题型、纸面页码、选项、公式及图形均经另一角色对照源 PDF；答案要点和详细解析逐题一致并经过盲核。
- 每卷 `questions.tex`、`answers.tex`、`answers_short.tex` 及四个版本入口可由生成器重建；四个 PDF 本轮构建成功，未解析引用/缺字为零，视觉回执当前。
- 无可靠答案或无法核实的内容如实标 `U` 并阻断完成；没有 PDF、页面截图、PNG/JPEG 或编译中间件进入提交。
- 批次/全局报告与机器清单一致，工作树干净，提交不 push。

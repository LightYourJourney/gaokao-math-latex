# 2006 年 phase1-b69 / phase1-b70 生成投影刷新与结案计划

> **For agentic workers:** 执行各自任务后回报实际改动和门禁结果；子代理不改公共清单、不提交，主代理审查并按阶段提交。

**目标：** 让 phase1-b69 与 phase1-b70 中过期的 2006 年项目 TeX 投影重新与当前生成器一致，对受影响试卷完成构建、逐页视觉审查和批次结案，同时保留所有来源与答案阻塞。

**架构：** 以规范 Markdown、provenance 和当前 manifest 为事实源，只用 `generate_projects.py` 更新 `questions.tex` / `answers.tex`。每批生成改动独立提交；主代理负责正式构建、复核回执、manifest、报告投影和进度/交接记录。

**技术栈：** Python 项目工具、XeLaTeX/latexmk、Poppler；OCR 仅在源页确有需要时使用，本计划不重跑已有转录。

**规格：** `math-gaokao-latex/OCR_WORKFLOW.md`、`math-gaokao-latex/README.md`、`source-manifest.json`、`PROGRESS.md`。

## 全局约束

- 只在 `仓库根` 的 `feat/gaokao-phase0` 工作；不新建 worktree、不改 `main`、不 push。
- 每个批次的生成 TeX 由指定子代理负责互不重叠的卷目录；子代理不改 manifest、issues、receipts、报告或公共文件，也不提交。
- 主代理检查每份实际 diff、所有权范围和 `git diff --cached --check`，再按阶段提交。
- 只刷新生成器投影；不得改写题面、答案、解析、图稿、provenance 或 issue 内容来消除当前 blocker。
- 缺源或存疑保持 `U/PENDING`、`official_answer=null` 和 `blocks_completion`，不得依凭同批其他卷推断。
- 任何批次关闭仅表示相应固定来源副本的批次阶段完成，不表示全库 1952–2026 完成。

## 审查重点

- 生成器输出是否带入规范 Markdown 以外的文字或数学变化；以生成器前后检查和逐文件 diff 核验。
- 同批已有未受影响的卷是否保持当前 build/review 回执；以正式回执 currentness 和 finalizer 检查。
- 页面分页或视觉是否因投影变化；用当前正式 PDF 与有效旧回执/PNG 比较，变化页重新检查。
- 已记录的来源或答案阻塞是否被误清；以 issues、provenance、manifest 现场派生状态核验。
- 报告、CSV 与 manifest 是否一致；以全量 `report.py check --all` 和 CSV 检查证明。

## 任务 1：phase1-b69 中两卷过期 TeX 投影

**文件：**

- `math-gaokao-latex/2006_江苏卷/questions.tex`
- `math-gaokao-latex/2006_江苏卷/answers.tex`
- `math-gaokao-latex/2006_浙江卷_文科/questions.tex`
- `math-gaokao-latex/2006_浙江卷_文科/answers.tex`

**接口：** 输入 `source-manifest.json` 中 `gk-2006-regular-jiangsu` 与 `gk-2006-regular-zhejiang-arts`；输出为对应生成器投影。phase1-b69 中广东、江西文科两卷不在本任务改动范围。

- [ ] 对两卷分别运行 `generate_projects.py --paper <PAPER_ID> --check`，记录预期 stale 文件。
- [ ] 只对上述两卷运行对应 `--write`，再逐卷运行 `--check`。
- [ ] 主代理核对四个目标文件 diff 仅为确定性生成投影，并确认无事实层、manifest 或 receipt 改动。
- [ ] 精确暂存四个目标文件，运行 `git diff --cached --check` 并提交生成阶段。

## 任务 2：phase1-b70 三卷过期 TeX 投影

**文件：**

- `math-gaokao-latex/2006_江西卷_理科/questions.tex` 与 `answers.tex`
- `math-gaokao-latex/2006_浙江卷_理科/questions.tex` 与 `answers.tex`
- `math-gaokao-latex/2006_湖北卷_理科/questions.tex` 与 `answers.tex`

**接口：** 输入 `source-manifest.json` 中 `gk-2006-regular-jiangxi-science`、`gk-2006-regular-zhejiang-science` 与 `gk-2006-regular-hubei-science`；输出为对应生成器投影。

- [ ] 运行 `generate_projects.py --batch phase1-b70 --check`，记录预期 stale 文件。
- [ ] 对该批运行 `--write` 后重新 `--check`。
- [ ] 主代理核对六个目标文件 diff 仅为确定性生成投影，并确认无事实层、manifest 或 receipt 改动。
- [ ] 精确暂存六个目标文件，运行 `git diff --cached --check` 并提交生成阶段。

## 任务 3：正式构建与视觉结案

**文件：** 两个批次受影响卷的 build/review receipts、batch reports、全量报告投影、`source-manifest.json`、`missing-issues.md`、`PROGRESS.md`、本项目交接文档。

- [ ] 对新生成投影的卷进行正式构建；保持未改卷的 current receipts 可复用，不重建无关卷。
- [ ] 对每个新 build attempt 逐页复核；仅当 Poppler 栅格字节完全一致时继承已审页面结论，变化页重新检查。
- [ ] 运行 source/issues、provenance、solution sources、generator、build currentness、review、CSV 和报告门禁；未解决 blocker 保持原状态。
- [ ] 全量测试如实记录实际结果，不因跨卷缓存状态失败而批量改写无关卷。
- [ ] 更新进度及交接记录，核对并精确提交结案路径；结束时确认 feature worktree 干净。

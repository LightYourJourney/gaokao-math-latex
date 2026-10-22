# 高考数学 LaTeX 项目交接

更新时间：2026-10-22（中国标准时间）

## 状态摘要

题库仍在持续建设，1952—2026 全范围目标尚未完成。请在 `feat/gaokao-phase0` 分支和 canonical worktree 继续；不要切到 `main`，不要 push，也不要覆盖既存未提交文件。

### Git 工作位置

- 仓库：`主工作树`
- canonical worktree：`仓库根`
- 分支：`feat/gaokao-phase0`
- 当前 HEAD：`ed8b546bb584d360f3b94b36d7c5a3dfe6cfbdee`（refresh reports after 2006 review close）；当时与 `origin/feat/gaokao-phase0` 同步。
- `main` 是独立 worktree，HEAD `4859ad9b`；本项目不要在 main 继续。
- `main` 已在提交 `9655b6d3` 将排版治理目录从 `docs/design/` 迁到仓库根 `typography/`；当前 main HEAD 为 `4859ad9b` 且工作树干净。`feat/gaokao-phase0` 的历史 HEAD 仍有旧 `docs/design/` 跟踪文件，但已恢复工作树到分支 HEAD，消除了无关删除差异；没有把 typography 迁移提交带入题库分支。
- 主 worktree 此前干净。此交接文档应新增在 canonical worktree。提交前再核对状态与 staging，避免夹带别的工作。

新对话先核对：

```sh
cd 仓库根
git status --short --branch
git log -1 --oneline --decorate
```

## 全库快照

依据 manifest revision **4611** 及生成的 `math-gaokao-latex/reports/baseline.md`（2026-10-22）：

- 775 个来源（734 普通高考、41 春季高考），均为 ready。
- 296 套：complete 242、blocked 50、compiled 3、planned 1。
- 162 批：closed 127、closed_with_blockers 31、compiled_pending_review 3、planned 1。
- 门禁：FINALIZED 158、INVALID_OR_STALE 1、VISUAL_FAILED 3。
- 1180/1180 版本有编译记录；build succeeded 289、compiled_pending_review 6。
- 问题账本 1131 条，unresolved 190，其中 blocks_completion 126。
- baseline 列出的门禁未通过批次：phase0-b02、phase2-b58、phase2-b59、phase4-b11。
- PROGRESS.md 某条较早的同日记录写 295 套，manifest revision 4611 和 baseline 报告均为 296；用状态前请重新对照 manifest 和报告。

这些是登记/批次计数，不代表全卷均逐题人工复核，更不代表全项目完成。

## 最近完成

### 2016 上海文理科，phase2-b14

- `reports/phase2-b14.md`：closed；两卷8版97页全部审查通过。
- 主要提交：最终审核/报告 `e1a7b804`，内容与分页修正 `d2cf43f3`。
- 计划：`docs/superpowers/plans/2026-10-08-gaokao-2016-shanghai.md`。
- 文科Q11、理科Q14的概率模型早期登记 ISSUE-1006/1007；**当前报告和manifest已经结为 closed/complete**。不要照抄历史对话的旧 blocker 状态；如有必要，查当前答案、provenance、issues 再判断。

### 2006 上海春季文科，phase4-b14

- 当前分支最近完成的批次，`reports/phase4-b14.md` 与工作树回执为准，批次 closed。
- 题面/答案阶段、来源判断、四版构建与审查的操作记录在 `math-gaokao-latex/PROGRESS.md` 末尾。

### 1990 全国理科，phase4-b13

- 四版构建和50页视觉审查完成，批次 closed_with_blockers。
- ISSUE-1131：原图未标明 (V_1,V_2) 与两区域的对应，答案保留无序比7:5，不能推测有序比。
- 题面来源无答案页，解析是编者推导且有标注；出版社/版次/原件身份未认证。
- 不重做26题转录、独立盲核或视觉审查；只有取得同版权威证据后再处理阻断。

## 现存失败 / 可能的下一项

- phase0-b02：2020全国Ⅰ文科原卷标记取消的第23题按既定决定仍保留，造成5处 heading_number fail。不要擅自删题或将失败改判通过。
- phase2-b58 / b59：1986广东两卷固定来源缺选项图/字形；未找到可逐页核对同版来源。不可借全国卷或异版图补绘，不可凭推测填补。
- phase4-b11：2005上海春季卷当前仍为 planned；manifest已有部分项目元数据/图稿线索，但不能假定来源登记、内容与验收已完成。若选它，先核查上游固定来源、已有文件、历史记录和题目状态。
- 其他批次如 phase3-b23 也有 blocker。先看报告和 issue，再决定是否具备新增证据，不以清状态数字为目标。
- 最近 PROGRESS 的指导是先复核已有工作，再选择“有可核实来源且未重复完成”的项目。新对话不要盲目开启新批次。

## 权威文件与项目门禁

先读以下内容并用当前文件状态交叉核实：

1. `math-gaokao-latex/PROGRESS.md` 末尾：日期序列操作日志，可能有旧状态。
2. `math-gaokao-latex/source-manifest.json`：来源、卷、批次当前主账。
3. `math-gaokao-latex/reports/baseline.md` 与对应 `phase*-*.md`。
4. `math-gaokao-latex/missing-issues.md`。
5. `math-gaokao-latex/README.md`、根目录 `CLAUDE.md`。
6. 每卷 `provenance.json`、`receipts/build.json`、`receipts/review.json`、题目/答案源及四个入口文件。

守则：来源不明或答案不能证明时标 pending/blocked/U；转录与独立求解分离；编者答案明确注明非官方；图稿须 TikZ/PGFPlots；题面和答案源通过确定性脚本渲染四版本，勿手改派生物。四版编译、逐页八项审查、回执当前性、finalize、报告/CSV刷新都是门禁。公共宏改动可能使全库回执失效。避免 `clean-build`（会删除 build PDF）。主代理独占 manifest/共享文件；subagent 写范围要互不重叠。提交只 stage 本批授权路径；不 push。

## 给新对话的启动提示

> 请从 `仓库根` 的 `feat/gaokao-phase0` 分支继续高考数学 LaTeX 项目。先读 `docs/superpowers/plans/2026-10-22-gaokao-latex-handoff.md`，核对 git status/branch/HEAD；再读 `PROGRESS.md` 末尾、当前 manifest、baseline、相关报告和 issues。`typography/` 的排版治理改动属于 main 分支，勿合并或 stage 到题库分支；不切 main、不 push、不重复已完成工作。选择有固定、可核来源且尚未完成的下一项，按本仓库门禁推进。提交前检查实际 diff 并限定 staging 范围。

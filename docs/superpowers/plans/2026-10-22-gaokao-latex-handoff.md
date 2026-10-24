# 高考数学 LaTeX 项目交接

更新时间：2026-10-22（中国标准时间）


## 2026-10-25 后续（四）：1998 上海理工农医收口

- `phase4-b26`（`gk-1998-regular-shanghai-science`）已提交 `5429317`：22 题（填空 1–11、选择 12–16、解答 17–22）、6 页扫描件附卷内答案（等级 C）、四版 4/16/6/12 页；`FINALIZED`／`closed`／complete。盲解与卷内答案全一致。
- 关键纠错：Q15 源为「且 11∈B」（初稿漏一个 1），修正后 a>6、D 唯一；Q19 图 z 轴改 O–O₁ 虚线＋O₁ 以上实线；Q22 行间公式后孤行句号删除。
- 现况：775 来源、313 卷（complete 258／compiled 3／blocked 52）、174 批，manifest rev 4864。

## 2026-10-25 后续（三）：1997 上海理工农医收口

- `phase4-b25`（`gk-1997-regular-shanghai-science`）已提交 `158432f`：22 题、7 页扫描件附答案要点（等级 C）、四版 6/21/8/15 页；`FINALIZED`／`closed`／complete。独立盲解 22 题与印载答案全一致。
- 生成端两处修复：① 解答题答案必须写成 `**答案（k）：X**` 才会进入答案框与简答版（原 `**（k）**` 会全部退化为「见解析版」）；② 简答版提示语用 `SHORT_ANSWER_NOTICE_OVERRIDES` 按「来源印载答案」改写，已加 1997 上海文/理两卷。
- 现况：775 来源、312 卷（complete 257／compiled 3／blocked 52）、173 批，manifest rev 4846。

## 2026-10-25 后续（二）：1997 上海文史收口

- `phase4-b24`（`gk-1997-regular-shanghai-arts`）已提交 `b0b0af6`：22 题、8 页 A4 扫描件附印载答案与评分（等级 C）、四版 5/20/7/15 页；finalize `FINALIZED`、批次 `closed`、整卷 complete。独立盲解 22 题与印载答案逐题一致。
- 关键纠错：Q21 直线与抛物线交点坐标首稿误作 (5±√17)/2，实为 (5±√13)/2=(0.697,1.303)/(4.303,−2.303)，两份独立审查同时抓出；Q19 三棱柱补 AC′、删幻影 B′C、按源改线型；Unicode 下标 ₁/₂ 缺字改数学模式。
- 现况：775 来源、311 卷（complete 256／compiled 3／blocked 52）、172 批，manifest rev 4824。

## 2026-10-25 后续：2002 北京文科收口

- `phase4-b23`（`gk-2002-regular-beijing-arts`）已提交 `6d10511a`：22 题、2 页 A3 重排件（有文字层、无答案页，等级 D）、四版 5/19/7/17 页；finalize `FINALIZED`，批次 `closed`，整卷 complete。独立盲解 22 题与库内答案逐题一致。
- 修复要点：Q11 零点 0.6→1（原图与选项矛盾）、Q12 虚线仅 f₂/f₃/f₄、Q18 尺寸标注改「标签贴棱外侧、无箭头」、Q4 空选项占位行、Q20 八列表超宽（表头缩写＋题面说明）、Q11 两行选项 24pt 错位。
- 现况：775 来源、310 卷（complete 255／compiled 3／blocked 52）、171 批，manifest rev 4799。

## 2026-10-24 后续：1996 上海文史收口

- `phase4-b22`（`gk-1996-regular-shanghai-arts`）已提交 `72dd5dc3`：24 题、8 页扫描件附印载答案（等级 C）、四版 6/26/8/19 页；finalize `FINALIZED`，批次 `closed_with_blockers`、整卷 blocked（Q15 A1「直线 OA」外分点歧义，ISSUE-1138–1143）。
- 本轮视觉审查代理多次长时间无产出，由主会话接管逐页复核并留证；后续开批建议把审查段拆到 ≤4 页/代理，并预置主会话兜底。
- 当前 775 来源、309 卷（complete 254、blocked 52、compiled 3）、170 批；manifest rev 4773。

## 2026-10-24 阶段提交与1996上海理科接续

本段优先于下方旧快照。用户明确授权“每完成一个阶段就提交”，仍不push。
canonical worktree与分支仍为`phase0-wt` / `feat/gaokao-phase0`。

- 2000春季京皖文理phase4-b20已提交`c4766f2c`；1996上海理科来源/数学/规范登记阶段已提交`be4e95b`。
- 1996上海理科24题/150分、全部选做轨道与7幅TikZ图已登记为`gk-1996-regular-shanghai-science`，source已canonical绑定；不再重复转录或登记。
- phase4-b21最终四版67页（7/28/9/23）视觉通过，finalize返回FINALIZED，manifest revision4752；批次closed_with_blockers、整卷blocked。最终attempt为`75a8a3fe-beda-4e63-bf17-3872c808876d`，见本卷receipts与reports/phase4-b21.md。
- Q15 A1原文“直线OA”按通常无向距离有内外分两解，印载答案只列单解；ISSUE-1136/1137都open并阻碍完成，provenance为U/unresolved。不得按源答案把直线改线段，不得降级冲突以通过门禁。
- 当前775来源、308卷（complete254、blocked51、compiled3）。这只是已登记状态，不是全项目完成。全量1757项测试通过（13跳过，1012.138秒）；详细校验见PROGRESS与1996阶段复核报告；后续先读当前manifest、Git及回执，不用旧截图或旧报告证明新版本合格。

## 2026-10-23 接续校正

本文下方2026-10-22快照已过时。当前仍使用 canonical worktree
`仓库根`、分支 `feat/gaokao-phase0`，
本轮接手HEAD为 `77eeb66c`，未切main、未提交或推送。

- 已接续并收口未提交的2000春季京皖文理两卷（phase4-b20）：48题、八版98页，
  来源视觉/数学复核及全部输出页八项审查完成；修复推导、来源记录与图标注，补答案图。
  当前manifest revision4740，批次closed，check-batch返回FINALIZED。
- 当前全量投影：775来源、307卷（complete254、blocked50、compiled3），
  168批，正式门禁FINALIZED165、VISUAL_FAILED3。此为状态统计，非全项目完成。
- 本轮成果路径：`math-gaokao-latex/reports/phase4-b20.md`、
  `reports/2000-spring-jingwan-review.md`，以及PROGRESS.md末尾。
- 全量测试1753项初跑仅旧来源“未绑定”断言失败，已修为canonical双向绑定校验；
  定向7+2项通过；最终全量1755项通过（13跳过，451.183秒），报告/CSV/最终回执检查均通过。
- 旧PROGRESS把1994上海列为下一套，当前manifest却已将其绑定为phase1-b24、
  blocked/closed_with_blockers；不要重复登记或转录，先核对当前报告和resume_action。
- 可核下一候选为1996上海理科：当前source_id
  `src-544d6951d540a551546ce474b93c3b9bc08e1863472ea0998f971dd4b619de21`
  为ready且未绑定；已有`1996_数学真题_上海理工农医_{试题,答案要点,解析正文,含解析}.md`
  与项目内7幅TikZ图。没有四版入口、provenance或正式回执，需先独立核源/数学复核。
  Q15—18的A1/B1及Q22的A2/B2选做轨道必须保留；Q15 A1直线OA内外分歧义待核。
  固定源印载答案不能当成已认证官方答案。参见PROGRESS旧记录约2540行及
  `tests/test_1996_shanghai_science_sources.py`；此次只读定位，未重验源PDF哈希。
- 保留全部未提交成果；未获授权不Git提交，不push；不用旧PNG或旧QC作为当前验收证据。

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

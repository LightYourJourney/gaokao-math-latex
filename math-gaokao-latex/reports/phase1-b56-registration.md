# 2003 春季北京理科：来源登记与待核问题

批次 `phase1-b56`、paper `gk-2003-spring-beijing-science`。固定副本为 `春季高考/2003/2003春季北京理.pdf`，SHA-256 `4cb807a7fe4989e2b0e0d2ad8aa42438f72861d87a90afe8d8cd003608915b28`；两页题面，印刷页 119–120，未见答案或分值，出版者、版次和官方身份均未核。答案为项目独立推导，非官方标准答案。

已登记 22 题题面、答案要点、解析正文、确定性生成的含解析与 5 幅 TikZ 图；题面经第二人对照。第 18、22 题先前计算错误已复算纠正，详见 `2003-beijing-science-q18-q22-recheck.md`。第 8 题图中 L 与题干 I 不一致，按题干推导可得 B，但正式答案标 U/PENDING；第 14 题表中 140、85 只是满足所列数据的一种规律，亦标 U/PENDING。

登记 revision 5420 中 `ISSUE-1248`、`ISSUE-1249` 对应第 8 题图文标记与条件答案，`ISSUE-1250` 对应第 14 题规律未明；均为开放阻断，paper 为 `blocked`、批次为 `planned`。`solution_sources.py check-batch` 的 22 题、图形登记预检 5 张、manifest 及问题总账结构检查均通过。逐题 provenance、共享 TeX、四版正式构建和逐页视觉审查尚未完成，不能将此卷视为完成。

## 逐题来源导入

22 题逐题来源、独立求解及复核记录已绑定当前题面、答案和固定源哈希；第 8 题题面审查为 uncertain，答案证据 U，关联 `ISSUE-1248`、`ISSUE-1249`；第 14 题答案证据 U，关联 `ISSUE-1250`。第 6、8、18、21、22 题初始解答中出现的误读或运算分歧已复核更正；不能把错误初稿作为一致性证据。`provenance.py check-batch` 通过，manifest revision 5421，CSV 当前。paper 仍为 blocked；四版生成、正式编译和视觉审查尚未完成。

## 共享内容与入口生成

已由规范源生成共享 `questions.tex`、`answers.tex`、`answers_short.tex` 及四个版本入口；共享内容、简答与入口生成器的 `--check` 均通过。简答选择题表第 8 题显示 U，第 14 题显示 U/PENDING 并注明所列值只是可能规律。paper 的三个阻断仍开放；正式编译及 PDF 视觉验收尚未进行。

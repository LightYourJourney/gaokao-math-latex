# 2003 春季北京理科：来源登记与待核问题

批次 `phase1-b56`、paper `gk-2003-spring-beijing-science`。固定副本为 `春季高考/2003/2003春季北京理.pdf`，SHA-256 `4cb807a7fe4989e2b0e0d2ad8aa42438f72861d87a90afe8d8cd003608915b28`；两页题面，印刷页 119–120，未见答案或分值，出版者、版次和官方身份均未核。答案为项目独立推导，非官方标准答案。

已登记 22 题题面、答案要点、解析正文、确定性生成的含解析与 5 幅 TikZ 图；题面经第二人对照。第 18、22 题先前计算错误已复算纠正，详见 `2003-beijing-science-q18-q22-recheck.md`。第 8 题图中 L 与题干 I 不一致，按题干推导可得 B，但正式答案标 U/PENDING；第 14 题表中 140、85 只是满足所列数据的一种规律，亦标 U/PENDING。

登记 revision 5420 中 `ISSUE-1248`、`ISSUE-1249` 对应第 8 题图文标记与条件答案，`ISSUE-1250` 对应第 14 题规律未明；均为开放阻断，paper 为 `blocked`、批次为 `planned`。`solution_sources.py check-batch` 的 22 题、图形登记预检 5 张、manifest 及问题总账结构检查均通过。逐题 provenance、共享 TeX、四版正式构建和逐页视觉审查尚未完成，不能将此卷视为完成。

## 逐题来源导入

22 题逐题来源、独立求解及复核记录已绑定当前题面、答案和固定源哈希；第 8 题题面审查为 uncertain，答案证据 U，关联 `ISSUE-1248`、`ISSUE-1249`；第 14 题答案证据 U，关联 `ISSUE-1250`。第 6、8、18、21、22 题初始解答中出现的误读或运算分歧已复核更正；不能把错误初稿作为一致性证据。`provenance.py check-batch` 通过，manifest revision 5421，CSV 当前。paper 仍为 blocked；四版生成、正式编译和视觉审查尚未完成。

## 共享内容与入口生成

已由规范源生成共享 `questions.tex`、`answers.tex`、`answers_short.tex` 及四个版本入口；共享内容、简答与入口生成器的 `--check` 均通过。简答选择题表第 8 题显示 U，第 14 题显示 U/PENDING 并注明所列值只是可能规律。paper 的三个阻断仍开放；正式编译及 PDF 视觉验收尚未进行。

## 正式构建，待视觉审查

四版正式构建返回 `COMPILED_PENDING_REVIEW`，attempt `4c5d0150-a6ae-400a-a222-b62ee55a6c73`，manifest revision 5423；试题版 5 页、解析版 17 页、简答版 7 页、印刷版 14 页，共 43 页。构建回执检查无 missing、invalid 或 stale，CSV 当前。PDF 仍需逐页目视并生成绑定回执；paper 保持 blocked，三个问题仍开放。

## 第 21 题图形调整及重建

旧 attempt `4c5d0150-a6ae-400a-a222-b62ee55a6c73` 的解析版实际审查发现第 21 题小圆 $O_2$ 标记在第 5、16 页与圆弧、底边相碰。已在隔离目录试排并实际查看两页，将标记移到小圆下方，未改变图形几何；同步更新图形来源哈希。旧 attempt 的解析版逐页观察和审查模板已归档。

正式重建返回 `COMPILED_PENDING_REVIEW`，新 attempt `0a6d7f28-1051-43ff-924d-a4ce9431b7ef`，manifest revision 5426；四版仍为 5、17、7、14 页，共 43 页。构建回执检查无 missing、invalid 或 stale；新构建的四版逐页视觉审查尚未完成，三个问题仍开放。

## 解析工作备注清理及重建

逐页查看 attempt `0a6d7f28-1051-43ff-924d-a4ce9431b7ef` 时，印刷版第 6 页发现第 5 题解析含“须在绘图时再次对照选项图”的内部工作备注。已从解析正文及草稿移除该句，重新生成含解析与共享解析；不改变数学结论。前次主代理实际查看的 28 页及问题记录保存在 `.work/phase1-b56/review-render/`。

正式重建返回 `COMPILED_PENDING_REVIEW`，attempt `8489f534-e58d-4b7f-87a1-adf868b03a3d`、manifest revision 5429；四版页数分别为 5、17、7、14。回执检查无 missing、invalid 或 stale；新构建仍须逐页审查或对实际通过且 PNG 字节相同的旧页继承结论，三个阻断继续开放。

## 第 8 题超宽修正及重建

视觉回执校验曾报告 4 条第 8 题 `Overfull hbox`，涉及试题版、解析版、简答版。日志显示长题干在同一行内无法断开；隔离试排后在题干两个子句间增加换行指令，不更改可见文字，并重新绑定第 8 题题面哈希。正式构建 attempt `2a221356-e120-424d-88eb-da2ce9f4f476` 返回 `COMPILED_PENDING_REVIEW`，revision 5432，四版仍为 5、17、7、14 页；四版日志未见 Overfull hbox。新构建仍须重看变动页并完成视觉回执；原有三个内容问题仍开放。

## 视觉验收及批次收口

当前 attempt `2a221356-e120-424d-88eb-da2ce9f4f476` 四版共 43 页，重排变化的 14 页已实际逐页复看；其余 29 页逐一核验 PNG SHA-256 后，沿用此前实际查看且通过的页面结论，并保留原始 attempt 和页号。四版日志没有 Overfull hbox；正式视觉回执 `FINALIZED`，manifest revision 5433，批次为 `closed_with_blockers`。构建回执当前性、视觉回执、逐题来源、解析正文和三个生成器检查通过。`ISSUE-1248`、`ISSUE-1249`、`ISSUE-1250` 仍开放，第 8、14 题保持 U/PENDING，paper 仍为 `blocked`，不能视为整卷内容完成。

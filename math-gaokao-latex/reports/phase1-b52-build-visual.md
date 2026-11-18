# phase1-b52：2004 北京春季文科四版构建与39页视觉验收

日期：2026-10-28

## 实际构建与修复

来源阶段提交97d5b989后启动正式四版构建。首轮attempt `63411d26-f7ed-468a-ae47-40f40fa8173f`，四版4/16/6/13页：解析版answers.tex第497行Underfull badness10000，简答版answers_short.tex第33–34行Overfull 80.75885pt。主代理实际查看解析第16页与简答第6页，确认Q20长集合让答案框字距失衡，并在简答版越出版心、右侧被裁切；没有豁免。旧build/provenance、pending视觉工作项和两页实际失败观察归档在`.work/phase1-b52/review-history/63411d26-f7ed-468a-ae47-40f40fa8173f/`；其他旧页未检查，不声称通过。

仅将规范答案要点Q20(2)的六对坐标改成六个行内数学坐标逐项列举，让中文顿号处分行。机械比对六对坐标及顺序完全相同，数学结论未改。先同步规范含解析与共享TeX、简答，再更新工作角色证据与Q20答案表示哈希，正式re-import（revision5316→5317）；题面20个哈希和其他19题整条provenance完全不变。Q20答案哈希由db62cecc625bc48ffa74a0305f4c705f511f5c575c050dfef81494b8a9d649c1变为ac73f46099b18288b5fe8796b88042c458c9a8e41071e23203658836b8c019ad。身份角色未改变，证据明确这是盲解后的编辑性等价换行，未伪称重新盲解或源文勘误。

第二轮即最终attempt `7798a4cc-8760-41ba-90e0-6dc870b1ff2b`，输入manifest revision5318；构建结束revision5319。四版日志errors、missing_characters、undefined_references、Overfull、Underfull均0，警告豁免0。无公共样式、字体、页边距或生成器改动。四版均经pdfinfo确认595.28×841.89pt A4，实际PDF SHA与回执一致。

## 当前PDF

| 版本 | 页数 | PDF SHA-256 |
| --- | ---: | --- |
| 试题版 | 4 | `9469384cd715dd5ab346075e72e4f4546738a7e836d79381951b05db97c986fb` |
| 解析版 | 16 | `d6237e024a3777c098a8763eb65910fedab1a61e2d75ccbd17864020789792c0` |
| 简答版 | 6 | `3fc5eb72ef1a1e5f7791c0f7d886a8cf3805e3cb99df9e3704d49ebc88c2775d` |
| 印刷版 | 13 | `ab59788b639d60996cf94ee712b0c9d56c97f0de076670a8806e81d46dbaa24a` |

PDF保存在项目忽略的build目录；Git提交可复用源、provenance和正式回执。

## 实际逐页视觉验收

主代理用view_image实际查看当前attempt全部39张110dpi整页PNG，未继承任何旧attempt结论。八项检查共312项：288pass、24not_applicable、0fail/pending。24项不适用均为该页没有题图/待核表格标注，不把它们记成实看通过。每页PNG SHA、版本/页序、观察及实看状态在`.work/phase1-b52/review-render/7798a4cc-8760-41ba-90e0-6dc870b1ff2b/inspection-summary.json`；绑定PDF/输入/依赖/工具链的视觉工作项在`.work/phase1-b52/review/<edition>/`，已导入正式review回执。

重点实际核验：试题第2页Q11“常实数”修正清楚；试题/简答/解析第3页与印刷第2页Q17/Q18图、解析第13–14页与印刷第10–11页图均无标签遮挡；Q20完整网格与疑脱注记保留。最终简答第6页六个位置自然分两行、解析第16页答案框两行字距正常、印刷第13页完整一行，六个位置无裁切。题面区无答案；速查/解析区按版本出现非官方答案。题号/选项/公式、字号、页眉页脚与分页均逐页检查。

## 正式状态、验证与边界

`finalize-batch`实际返回FINALIZED，当前manifest revision5320，batch closed_with_blockers、paper blocked；build.status=succeeded，review.status=passed，四个edition.result均pass。Q20的ISSUE-1238继续open/blocks_completion。忠实照录“计算公以及”和可推导的数阵公式不等于完整源文已核定；没有补“式”。来源出版者、版次、来源链和官方性仍未知，official_answer=null。

完整回归实际 `Ran 1724 tests in 472.702s` / `OK (skipped=13)`，日志保存在`.work/phase1-b52/verification/full-tests.log`；测试在当前规范源和生成物稳定后运行，期间仅做只读PDF审查及忽略的视觉工作项记录，未改变被测规范源。来源清单/问题总账、provenance、solution_sources、三个生成器、最终build回执当前性、review门禁与报告/CSV在提交前复核。最终自动报告为`reports/phase1-b52.md`。

本阶段闭合本卷构建和版面验收，未消除来源阻断，也不表示1952—2026题库完成。下一批优先推进已有20题转录/独立答案复核的2004北京春季理科，随后可启动固定源带参考答案的2007上海春季卷图像转录；2004上海春季卷Q14/Q18原文歧义须另登记阻断，不能选择性补题。

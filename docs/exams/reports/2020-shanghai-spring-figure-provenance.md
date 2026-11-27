# 2020 上海春季卷：Q17 TikZ 图稿与逐题 provenance

日期：2026-10-28

状态：Q17 矢量图已绘制、登记并纳入确定性 TeX；21 题 provenance 已导入。批次 phase1-b48 为 provenance_verified，paper 仍为 blocked。正式四版构建与整页视觉校样尚未进行。

## 固定来源与图稿

- 固定 PDF：source src-aacbb6140d9e12bc5aca908afe4d613b6ae584f08da89de4fa537d174727f9c2，SHA-256 4cb2e71aa66630c0154487dbb06436236701c22f79f770193436e20b60e9e327，9 页；本次重看第 1 页 Q17。
- 新增图稿：2020_上海春季卷/figures/f2020_shanghai_spring_q17_pyramid.tex。按源图重绘可见拓扑与线型：AD、DC、PD 为虚线；PA、PB、PC、AB、BC 为实线；只标 A/B/C/D/P。没有增加直角符号、长度标记或其他源图没有的信息，坐标仅用于示意投影。
- 题面 Markdown 链接和生成的含解析 Markdown 均已映射图稿；manifest figure_files 登记 expected_occurrences=2，questions.tex 与 answers.tex 各引用一次。生成映射由 manifest 注册与规范 Markdown 链接动态形成，未增加静态生成器例外。
- 使用 standalone TikZ 局部预览编译并渲染 PNG，与固定源页放大图逐项对照。此预览只证明图稿线型、标签和拓扑的局部效果，不是正式试卷版面校样。

## 问题与 provenance

- ISSUE-1226（Q17 缺图）已 resolved：矢量图文件、题面引用、manifest 登记和确定性 TeX 映射齐备。正式 PDF 版面如有图稿排印问题，需据具体问题另行登记。
- ISSUE-1227（Q19 坐标范围未明列）保持 open / blocks_completion，答案仍为 U；不把线段范围补写入原题。
- ISSUE-1228（Q21 源附答案只写“奇数”、项目推导为“正奇数”）保持 open / blocks_completion，provenance conflict_status=unresolved。
- 已导入 Q1–Q21 的三角色 provenance。第二位题面复核者仅查看固定 PDF 第 1–2 页与题面稿，核对文字和页码；复核时 Q17 仍是待重绘占位，因此没有审阅新 TikZ。新图由主会话对照固定页自检，不称第二人审图。独立盲解者只看第 1–2 页，Q1–Q20 与记录结论相符、Q21 差异保留；这不是对后成答案文档的第二人逐字审阅。项目答案作者已接触先前源附答案摘录与盲算汇总，故 answer-solve 记录不称盲解。
- 固定副本的发布者、版次、来源链未核；official_answer=null。Q4 源附解析的 b 符号笔误与项目稿的 b=-1 仍如实并列。

## 生成与验证

- 确定性生成刷新含解析 Markdown、questions.tex、answers.tex、index.json；简答稿和四版入口壳当前，无需重写。
- source_manifest.py validate、issues.py validate、provenance.py check-batch、solution_sources.py check-batch、generate_projects.py --check、make_short_answers.py --check、make_editions.py --check 均通过；项目 21 题与生成结果一致。
- report.py render --all 以一个 content 事务写入并回读六个全量报告目标；report.py check --all 通过，未完成状态仍保留。manifest_csv.py --check 确认 775 行且当前。manifest revision 为 5261。
- 未运行测试套件；没有正式 XeLaTeX 四版构建、build/review receipts 或整页视觉校样。下一阶段是正式构建四版、审查受影响页，并形成绑定构建输入与 PDF 指纹的回执；Q19、Q21 阻断继续存在。
- Token、外部审阅成本和实际工时不可见，记未知。

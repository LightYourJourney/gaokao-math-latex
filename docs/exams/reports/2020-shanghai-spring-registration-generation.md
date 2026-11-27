# 2020 上海春季卷：paper/source 与 blocker 登记、确定性生成

日期：2026-10-28

状态：paper/source 和三条开放阻断已登记；规范源、合并稿、项目 TeX、简答稿与四版入口壳均已确定性生成并通过当前性核验。批次仍为 planned，试卷 blocked；逐题 provenance、正式构建和视觉校样尚未进行。

## 固定来源与登记状态

- 固定来源 src-aacbb6140d9e12bc5aca908afe4d613b6ae584f08da89de4fa537d174727f9c2，PDF SHA-256 4cb2e71aa66630c0154487dbb06436236701c22f79f770193436e20b60e9e327，共9页。第1–2页为题面，第3–9页附载自称“参考答案与试题解析”的材料。
- source 已绑定到 gk-2020-spring-shanghai，绑定含义仅为本库固定副本的内部 canonical 关联，不认证发布者、版次、来源链或官方答案身份；official_answer=null。
- 注册事务将 source manifest 从 revision 5256 更新至 5257，并建立批次 phase1-b48。批次状态 planned；paper 状态 blocked，blocked_from=planned，题量21。
- 本阶段未将扫描件附载答案标为官方，也未裁定其发布身份。

## 规范源与开放问题

- 题面、答案要点、解析正文、源附答案摘录四份文件均登记 paper_id。含解析稿由题面、答案要点和解析正文确定性生成，不作为事实源。
- 新增三条 open / blocks_completion：ISSUE-1226（Q17 缺矢量图）、ISSUE-1227（Q19 未明列 x、t 范围，数值结论仅在线段 OA 解释下成立）、ISSUE-1228（Q21 源附只写 m 为奇数，项目按完整题面独立推导为正奇数）。三项均未结案。
- Q17 占位继续保留；Q19 未把线段范围补写进题面；Q21 保留源附结论与项目推导的差异。Q4 源附计算笔误和 Q19 条件结论详见 2020-shanghai-spring-answer-analysis.md。

## 确定性生成

- 为匹配仓库小问锚点格式，在 Q17–Q21 的12行小问编号后补入 Markdown 分隔空格，没有改动题目文字。解析器现识别21题，小问集合与解析正文一致。
- 在答案要点开头补入 Q13–Q16 速查表 D、A、B、B；四格逐一重复现有答案行，供简答生成器进行第三路核对。
- solution_sources.py extract-batch --write 以一个 content 事务写入解析正文规范化稿和含解析稿，共2个目标。
- generate_projects.py --write 写入 2020_上海春季卷/questions.tex、answers.tex 和 index.json，共3个目标。
- make_short_answers.py --write 写入 answers_short.tex；make_editions.py --write 写入试题版、解析版、简答版、印刷版四个入口壳。
- 全库报告投影经一个 content 事务刷新六个目标；来源清单 CSV 重新生成并核对为775行。

## 校验与下一步

- source_manifest.py validate、issues.py validate、solution_sources.py check-batch、generate_projects.py --check、make_short_answers.py --check、make_editions.py --check 均通过；本卷21题与各生成文件一致。
- manifest_csv.py --check 确认775行 CSV 当前；report.py check --all 确认全量报告与 manifest/issues 一致且保留未完成状态。
- 未运行测试套件，未进行逐题 provenance、XeLaTeX 正式构建、PDF 回执或视觉校样。出版者、版次、来源链及答案材料官方身份仍未核。
- 下一阶段依据固定 PDF 绘制 Q17 矢量图，按图稿登记全链路要求同步更新 manifest、Markdown、生成映射与 provenance；再逐题完成题面、答案和解析 provenance。论文仍不得标为完成。

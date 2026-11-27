# 2007 北京文科候选卷：paper/source 登记与确定性装配

- 日期：2026-11-03。
- Paper：`gk-2007-regular-beijing-arts`；batch：`phase1-b81`；题量20；`track=arts`；项目目录 `2007_北京卷_文科`。
- 固定 source：`src-71817304e261efb7deaf51c2a5f400421a95ac91a90313d8f558bee701a624f9`，上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`，路径 `普通高考/2007/2007北京文.pdf`，2页 A3，印刷页353–354；SHA-256 `e5356797259eb22cc2b4f23019ad7ab044f282bdfc2a65df94dbbdcc502cfff5`，Git blob `3207132ef37ec52e6dfd19ffac856388f4c053f1`。source 的 `source_state=ready`，本库内部 relation 为 `canonical`。这只绑定本库选用的 PDF 字节，不证明发布者、出版者、版次、复制链或官方身份。

## 登记与阻断项

- `source_manifest.py register-papers` dry-run 通过；正式 state transaction ID `d9b970d8-0667-4f16-bbaf-1d3768da7eb8` 将 manifest revision `6014→6015`。Paper 与单卷 batch 登记成功。
- 登记事务创建 `ISSUE-1355`：Q18，类型 `answer-convention-ambiguous`，状态 `open`，影响 `blocks_completion`。固定题面只给每位乘客在10个非起点站的均匀边缘分布，没有声明六人选择联合独立；paper `production_state=blocked`、`blocked_from=planned`，batch `phase1-b81` 状态仍为 `planned`。
- PDF 未见答案、解析或评分页；答案和解析是本库独立推导，`official_answer=null`。Q13、Q17、Q19 的源图仍待矢量重绘；本次 paper record 的 `figure_files=[]`，不把图位占位登记成图稿。

## 确定性装配与验证

- 三份规范源写入 `paper_id=gk-2007-regular-beijing-arts`。通过 `solution_sources.render_combined()` 生成 `_含解析.md`，14,934 bytes，SHA-256 `c57bbb2a4bb4c51312f4e66655cbb1f44a8fbdb8c1646f10cf1ffad1fcedbeff`；随后官方 `solution_sources.py extract-batch --write` 检查为目标已最新、未开启新事务。
- `generate_projects.py --write` 写入3个目标；`make_short_answers.py --write` 写入简答文件；`make_editions.py --write` 写入试题、解析、简答、印刷4个入口壳。三项相应 `--check` 均通过。
- `source_manifest.py validate`、`issues.py validate` 与 `solution_sources.py check-batch` 通过。`report.py render --all` 更新六份全库状态投影；`report.py check --all` 返回“报告输出与全量 manifest 当前一致”。`manifest_csv.py --write` 更新为775行。

本阶段未进行正式 LaTeX PDF 构建或视觉复核；当前没有 build/review receipts。逐题三角色 provenance、图稿同步登记、Q18 问题解除材料、测试套件和最终批次复核均待后续阶段。本登记不认证来源官方身份、不表示整卷完成或长期语料库完成。

# 2006 重庆、陕西文理候选卷：首次正式构建问题修正

- 日期：2026-11-03；批次 `phase1-b80`；承接 `reports/2006-chongqing-shaanxi-build-attempt-01.md` 的首次正式构建诊断。
- 更正文案层的状态事实：四份解析正文不再写 `` `paper_id=null` ``，改为“试卷 ID 已登记，官方答案字段保持空值”，与 frontmatter 中的 paper ID 和 `official_answer: null` 一致，同时避免行内代码下划线引发 XeLaTeX `Missing $ inserted`。
- 数学标点改为生成器可识别的数学界定符，内部文字/公式/选项均未改：重庆理科题面三个含 `、` 的数学片段（Q19、Q22）及陕西文科14个行内、2个行间数学片段（共35处中文标点）。因题面块序列化形式变化，沿用既有 PDF 逐题目视结论，仅将 provenance question hash 绑定到新格式：重庆理 Q19/Q22；陕西文 Q4/Q6/Q7/Q8/Q9/Q11/Q12/Q17/Q19/Q20/Q21。
- 简答输出新增24个本批精确 override，将原答案里的 Unicode 希腊字母、上下标和数学式放回数学模式；不改 `_答案要点.md` 中的答案值，也不触碰四项 U/PENDING。`solution_sources.py extract-batch` 重建四份 `_含解析.md`。
- 验证通过：`python3 -m unittest tests.test_short_answers`（54 tests，OK）；`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`solution_sources.py check-batch`（4×22）、`provenance.py check-batch`（4 卷）、source manifest、issues 与 775 行 manifest CSV 校验。manifest revision 为 6005。
- 此提交前尚未重试正式 PDF 构建。10 个首次构建 compile-error issues（`ISSUE-1345`—`ISSUE-1354`）仍 open，四卷缓存状态为 `blocked`，批次 `provenance_verified`；原四项答案/题意 blocker 同样保留。下一步在独立构建阶段重跑四卷四版并检查所有缺字/溢出版面告警。

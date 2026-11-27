# 2006 重庆、陕西文理候选卷：四版正式构建首次尝试

- 日期：2026-11-03；批次 `phase1-b80`；正式构建 attempt：重庆文 `89a59339-a002-4468-a5ec-85893ab32870`，重庆理 `a8aeed03-e08f-41db-86c8-6354a74b7daa`，陕西文 `95c53884-e74d-4174-a7e3-ee345d10023c`，陕西理 `21eb9806-b898-4da1-8770-58f6075904fa`。四次均基于 manifest revision 6003；完成状态事务 revision 6004。
- 16 个版本中 6 个 XeLaTeX 命令返回成功：四卷试题版及重庆文、陕西文简答版；另 10 个版本 `latexmk` 退出码 12（四卷解析版与印刷版、重庆理/陕西理简答版）。成功返回的版本仍有缺字告警，故均未进入视觉验收。
- 共同编译错误来自解析正文说明中的 `` `paper_id=null` ``：现有行内代码转换生成 `\texttt{paper_id=null}`，下划线在文本模式触发 `Missing $ inserted`。四份解析正文的 frontmatter 显示实际 paper ID 已登记，官方答案字段仍为空；说明文案需校正为真实状态并避免在文本中直接排版带下划线的代码标识。
- 构建日志另检出字形问题：重庆理科题面 Q19 的三处 `、` 进入数学字体；陕西文科题面与派生版共检出 35 处中文逗号缺字；简答版报告的缺字包括 `ω`、`π`、`ξ`、Unicode 上下标及相关符号。需先修正数学标记/版面输入，再做干净的四版 build；当前成功返回的 PDF 也不作为视觉通过。
- 构建器登记 `ISSUE-1345`—`ISSUE-1354` 十个 `formal-build` / `compile-error` blocker，`source-manifest.json` 对应状态置为 `blocked`；原有 `ISSUE-1341`—`ISSUE-1344` 四个答案/题意 blocker 保持 open。`provenance.py check-batch`、source manifest/issues 校验通过，manifest CSV 写回并校验为 775 行；批次仍是 `provenance_verified`。
- 这次尝试未完成正式构建，未做页面检查或 build/review 视觉回执。下一步修正文案和数学排版、重生成共享 TeX，核对 question provenance 的源文本哈希后再重跑 16 个版本。不能把此次构建状态描述为批次完成或长期语料完成。

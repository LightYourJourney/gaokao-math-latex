# 2006 重庆、陕西文理候选卷：最终答案数学模式修正

- 日期：2026-11-03；批次 phase1-b80；承接正式构建 attempt 02。
- 根因：答案源中的最终答案块被解析成粗体文本，Unicode π、ω、ξ、α/β、上下标、≤ 在 Latin Modern 文本字体下缺字；CQ 理 Q18(1) 与陕西理 Q18(2) 还含未置于数学模式的裸幂次，触发 Missing $ inserted。
- 在四份《答案要点》中将22题的最终答案公式改成明确的 LaTeX 数学模式，只改表示方式。与上一版逐题解析结果对照如下，答案事实及未决状态未变：

| 试卷 | 重新绑定的题目 |
|---|---|
| 重庆文科 | Q8、Q18、Q20、Q22 |
| 重庆理科 | Q14、Q17、Q18、Q20、Q21、Q22 |
| 陕西文科 | Q9、Q18、Q19、Q20、Q21 |
| 陕西理科 | Q10、Q17、Q18、Q19、Q20、Q21、Q22 |

- .work/phase1-b80-provenance 中 answer-solve 与 answer-review 的 answer_sha256 仅对以上22题重绑到新序列化值；角色、等级、结论、证据、冲突与 issue 字段均保留。受影响题目之外的 answer hash 不变。执行 provenance.py import-batch 两次：先导入新绑定，再在项目输出重生后同步派生状态；最终 manifest revision 为6011。
- 重生四份含解析稿、四份 answers.tex；新增重庆理 Q20(2) 的 $-6\le b\le2$ 与陕西理 Q21(2) 的 $y=\frac{x^2}{4}$，$-2\le x\le2$ 两条短答 override，SHORT_ANSWER_OVERRIDES 共26条。answers_short.tex 只在这两卷发生新增输出。
- 实证校验：四卷项目、简答与入口模板 --check 通过；含解析来源 4×22、provenance 4卷、source manifest/issues、775行 CSV 校验通过；tests.test_short_answers 54 tests，OK。最终答案输出扫描未见裸 Unicode 数学字符。
- 此次改动令 attempt 02 构建输入树失效；尚未运行新一轮 PDF build，不引用旧 PDF 作为验收证据。ISSUE-1341—1344 对应的未决题意/答案边界保留，official_answer=null、来源身份未认证。本阶段不是正式 PDF 视觉审查或批次闭环。

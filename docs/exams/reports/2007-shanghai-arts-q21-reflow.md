# phase1-b83：2007 上海文科 Q21 印刷版分页修正

日期：2026-11-03

## 发现与修正

- 对正式构建 attempt `9a6f2b2e-45da-4851-a97e-beef2fc9f00b` 的首轮 43 页视觉检查发现：印刷版第 16 页仅剩 Q21(2)、Q21(3) 两条答案框，造成明显尾页留白。该页及其余页面的视觉结论尚未写入正式回执。
- 只压缩权威解析源 `2007/2007_数学真题_上海文_解析正文.md` 的 Q21(3) 论证：保留一般参数域、右半椭圆顶点的分段、左半椭圆候选点比较及与（1）特例的条件边界，去掉重复解释并将比较式改为行内。题面和答案要点未改，Q21 答案哈希保持 `a24aaa4ff650353bdfa7fb13ce9407331ac74d60c869b1a746524a124ca7bd68`；`U/PENDING` 与 `ISSUE-1362` 继续保留。
- 重建确定性 `_含解析.md` 与 `answers.tex`。三角色 provenance 重新导入后 manifest revision 为 6057，batch 从 `compiled_pending_review` 回退至 `provenance_verified`；旧构建回执不再绑定当前输入，必须正式重建。

## 当前验证与下一步

- 已通过：`solution_sources.py check-batch`（21 题）、`provenance.py check-batch`（1 卷）、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、source manifest 校验、issues 校验、`manifest_csv.py --check`（775 行）及 `git diff --check`。
- 未运行测试套件。此次源层修正尚未经过新正式 PDF 的视觉确认；下一阶段重新正式构建四版，并重点检查印刷版 Q21 末页，按新旧 PNG 哈希仅复用未变化页面的实际视觉结论。
- 固定来源没有答案页；发布者、出版者、版次、来源链和官方身份仍未核，`official_answer=null`。本阶段仅修正解析分页，不表示该卷完成或长期语料库完成。

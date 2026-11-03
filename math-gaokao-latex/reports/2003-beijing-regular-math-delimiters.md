# 2003 北京普通文理候选卷：解析显示公式分隔修正

- 日期：2026-11-04；批次：`phase4-b48`。
- 两份规范解析正文均以独占一行的 `\\[` 开始显示公式，但将 `\\]` 接在公式行末。严格转换器只接受同一行成对的标记，或独占一行的结束标记；首次 `generate_projects.py --write` 因此报告未闭合显示数学块，并在原子写入前停止。
- 检查后确认文科解析正文有 19 个、理科有 22 个多行显示公式块，其中 39 个结束标记原来紧跟公式内容。将每个 `\\]` 移至单独一行；原句点在闭合符后的 24 处移到下一行，未增删题目陈述、算式、答案或标点。处理口径与既有同类情况一致，见[2017 上海普通卷题图阶段报告](2017-shanghai-regular-figures.md)。
- 通过把当前格式反向合并为旧格式并逐字比较 HEAD，确认两份规范解析正文只发生公式分隔行布局变化。两份 `_含解析.md` 由 `solution_sources.py extract-batch --write` 重新生成，且分别与 `render_combined` 当前纯函数输出完全相等。

## 文件指纹

| 科类 | 解析正文 SHA-256 | 确定性含解析稿 SHA-256 |
|:--|:--|:--|
| 文科 | `a5eedc70a0915edc1536df2633a34a00c1d065f4280078553cfcffb53690aec2` | `39e816a594f85ea2151c7e0cd250cd2ed3818c6b07008940be402bbc96fdc243` |
| 理科 | `2125c2c5d88c8252b3b80493197fd8a3d847f934574d81217e347f48b0923858` | `6e9a9d3a669f4ace2944e255c8fa40d4d4235bfb598d42b85e8eb9786bb042af` |

## 验证与下一步

- `solution_sources.py check-batch`：两卷各 20 题通过；`provenance.py check-batch`：`OK：2 卷`。
- 两卷 `generate_project` 内存生成与 `validate_project_result` 均通过：试题和解析各 20 题，登记的 8 张图每张正好出现两次，验证问题为空。此处未写入 TeX；下一阶段仍需正式生成 `questions.tex`、`answers.tex`、简答稿及四版入口。
- 未改题面、答案要点、manifest 或 issue ledger；无官方答案或来源身份的新结论。此阶段只修正 LaTeX 生成所需的 Markdown 行界，不表示正式构建或批次验收完成。

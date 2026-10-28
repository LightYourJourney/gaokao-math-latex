# phase1-b51：视觉复核发现后的分页回流修正

日期：2026-10-28

## 发现与修正

- 对首次正式构建的47页四版 PDF 做整页初审及重点页180 dpi复核时，发现解析版第18页页首单独出现第21题（3）答案框，印刷版第16页只含第22题（3）答案框。答案框内容完整、无裁切，但分页造成明显孤立与尾页留白。
- 只改权威解析正文 `2000/2000_数学真题_春季上海_解析正文.md` 的展示组织：第21题将标量三重积等式并入正文行；第22题将导数等式改为行内式。数学运算、推导结论和答案要点均未改变，答案哈希保持原值，`official_answer=null`。
- `generate_projects.py --write` 更新本卷 `answers.tex`；`solution_sources.py extract-batch --write` 同步重建解析正文规范稿及含解析展示稿。首轮生成预检拒绝了跨 Markdown 行的行内公式（未发生写入），收敛公式到单行后生成成功。
- provenance 状态事务 `d8d45fcb-7843-48d9-902e-aa34c22969f1` 将 manifest revision `5297 → 5298`，本卷状态从 `compiled` 回退到 `editions_generated`，批次从 `compiled_pending_review` 回退到 `provenance_verified`；旧构建回执/工作单不再代表当前源版本，需要重新正式构建和逐页审查。

## 门禁与阶段状态

- 通过：source manifest 与 issue 台账校验、`provenance.py check-batch`（1卷/22题）、`solution_sources.py check-batch`、本卷 `generate_projects` / `make_short_answers` / `make_editions --check`、775行 manifest CSV 当前性检查、全量 `report.py check --all`。
- 全量报告与 CSV 已按 revision 5298 刷新。未运行测试套件。
- 本阶段只完成源层分页回流修正；新 PDF 上的排版效果仍待构建验证。出版社、版次、扫描来源链及附录答案官方身份仍未核，`official_answer=null`。本阶段不代表该卷完成或1952–2026长期语料库完成。

下一步：正式重建四版，核对新页数、SHA 和构建警告；重新检查全部页面并重点确认解析版 Q21、印刷版 Q22 的答案框不再孤立。

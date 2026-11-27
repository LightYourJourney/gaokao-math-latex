# 2006 湖南文科候选卷：共享 TeX 与四版入口生成

- 日期：2026-11-02；批次 `phase1-b74`；manifest revision `5942`。
- 生成规范项目文件：`2006_湖南卷_文科/questions.tex`、`answers.tex`、`answers_short.tex`、`试题版.tex`、`解析版.tex`、`简答版.tex`、`印刷版.tex`；共用索引写入项目根 `index.json`。四版入口均通过模板生成并引用共享文件。
- 初次执行被短答生成器拦截：答案要点缺少必需的“答案速查表”。保留门禁并补入与逐题答案一致的 Q1–Q10 字母表 D、C、D、A、A、B、C、B、D、C；不改写逐题推导答案。含解析稿随规范答案同步按 `render_combined()` 重生成，answer-solve / answer-review 工作件的答案摘要重新计算，并重导 provenance 至 revision 5942。

## 验证

- `generate_projects.py --write/--check`、`make_short_answers.py --write/--check`、`make_editions.py --write/--check` 均通过；各生成器检查确认输出与当前规范源一致。
- `provenance.py check-batch --batch phase1-b74`、`source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check`（775 行）均通过。简答表第三路核对与逐题答案一致。
- `index.json` 已列入 paper ID、21 题结构、Q10/Q18 图稿及来源未认证说明；Q17（3）仍为 U/PENDING 并关联 `ISSUE-1338`。

尚未进行 XeLaTeX 四版构建、PDF 页数核对或正式页面视觉审查；本阶段只完成源文件装配，不表示卷级验收或长期语料完成。

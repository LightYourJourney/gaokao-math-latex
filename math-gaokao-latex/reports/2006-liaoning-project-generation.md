# 2006 辽宁文理候选卷：共享 TeX、简答表与四版入口生成

- 日期：2026-11-03；批次 `phase1-b78`；两卷各22题。固定候选来源与题图证据分别见 `reports/2006-liaoning-source-intake.md`、`reports/2006-liaoning-figures.md`。
- 生成两卷的 `questions.tex`、`answers.tex`、`answers_short.tex`、`试题版.tex`、`解析版.tex`、`简答版.tex`、`印刷版.tex`，以及共享 `index.json`；图稿在题面和解析答案相应位置按登记引用。
- 首轮 `make_short_answers.py --write` 按仓库门禁拒绝：答案要点虽列出 Q1–Q12 的十二个字母，但速查区使用区间行，无法与逐题答案做第三路核对。按解析器实际格式，在两份答案要点中增加 Q1–Q12 横向答案行，并将原总览首列改为“题号范围”；字母逐项与下方逐题答案相同，未修改答案结论或推导。随后简答表写入两卷并通过 `--check`。
- 生成后现场状态为文科 `blocked`、理科 `editions_generated`、批次 `provenance_verified`。运行 `provenance.py import-batch --write` 刷新状态缓存；之后核查均通过。manifest revision 从图稿阶段的 `5987` 依次到 `5988`（状态重算）与 `5989`（图稿进度备注修订）。
- 索引投影检查发现旧备注仍称图位待重绘；通过 state transaction 将文理两卷 `index_metadata.note` 更新为图稿已按固定源结构重绘，并重新生成 `index.json`。`manifest.csv` 写入后为775行且 `--check` 当前。
- 验证：`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`solution_sources.py check-batch`、`provenance.py check-batch`、`source_manifest.py validate`、`issues.py validate`、`sync-figure-occurrences` 与 `manifest_csv.py --check` 均通过。
- 当前仍未做正式 XeLaTeX 构建或逐页视觉验收。文科 Q21(2) 的源文 APCD 中 P 未定义，答案维持 U/PENDING 并由 `ISSUE-1340` 阻断；两卷答案均非官方，`official_answer=null`。下一阶段正式构建四版并准备视觉回执；本阶段不表示批次闭环或长期语料库完成。

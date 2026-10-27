# 2004 春季安徽文科卷：共享 TeX 与四版入口生成

日期：2026-10-27

- 使用现行 `source-manifest.json` 生成共享 `questions.tex` / `answers.tex`，更新 `index.json`，生成 `answers_short.tex` 与试题版、解析版、简答版、印刷版入口。
- `generate_projects.py`、`make_short_answers.py`、`make_editions.py` 针对本卷的 `--check` 均通过。
- 全量报告六个投影已由 `report.py render --all` 刷新并回读，`report.py check --all` 通过；`manifest.csv` 当前且775行；manifest、问题总账和 `phase1-b44` 22题合并源验证通过。
- `ISSUE-1211` 仍阻断 Q18 唯一答案确认，paper 保持 `blocked`，`official_answer=null`。逐题 provenance、正式PDF构建和视觉复核尚未完成。

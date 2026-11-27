# 2003 上海普通卷文理科：TeX 项目与四版入口生成

- 日期：2026-11-04；batch `phase4-b47`；manifest revision `6136`。
- 两卷各 22 题。题面、答案要点与解析正文均由规范事实源提供；六张题图通过登记的 Markdown 映射进入 `questions.tex`。`answers.tex` 保留 Q14 的 U/PENDING 与条件性说明，不声明官方答案。

## 答案速查表格式核正

- 首次 `make_short_answers.py --write` 被门禁拒绝。文科速查表使用“题号/结论”的竖向结构，解析器没有识别到速查答案行；理科使用横向表，但 Q14 单元格附有条件说明，因而与逐题解析出的 `U` 不相等。
- 两份 `_答案要点.md` 均改为标准横向答案速查表，Q13–Q16 为 `C / U / D / B`。Q14 的条件性说明仍在表后与逐题答案中保留，结论继续为 U/PENDING；没有把 D 写成确定答案。
- 文科答案要点 SHA-256 更新为 `f46bad5efc183343fc54166a47f5b382f673624d669d43c26f99364fd720433c`；理科更新为 `76e19ab93418d2a22516d82a43278a617ef2a61f19d250ab35dd75c42b8c7804`。登记报告中的对应哈希已同步。

## 生成与校验

- `generate_projects.py --write` 为两卷生成 `questions.tex` 与 `answers.tex` 并更新项目 `index.json`；写入 5 个目标。
- `make_short_answers.py --write` 成功生成两份 `answers_short.tex`；`make_editions.py --write` 成功生成 8 个题目版、解析版、简答版和印刷版入口。
- `solution_sources.py extract-batch --write` 确认确定性 `_含解析.md` 已是最新。随后 `solution_sources check-batch`（文、理各22题）、`provenance.py check-batch`（2卷）、三个生成器 `--check`、`source_manifest.py validate`、`issues.py validate` 及 `manifest_csv.py --check`（775行）均通过。
- 状态查询仍为 paper `blocked`、batch `provenance_verified`；Q14 blockers 保持打开。

## 阶段边界

本阶段只生成并验证 TeX 内容片段与四版入口，尚未进行 XeLaTeX 正式构建、PDF 页数/哈希回执、视觉页面复核或批次关闭。来源身份及官方答案仍未核；下一阶段按登记顺序正式构建四版并检查全部输出页。

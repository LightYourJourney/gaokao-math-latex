# phase1-b49：2003 春季北京文科逐题 provenance 与确定性生成

日期：2026-10-28

## Provenance

- 批次：`phase1-b49`；试卷：`gk-2003-spring-beijing-arts`；固定 source：`src-4ac986eba3d22fd3034252b57e1fed7e2b7b90eaaef7706499eb43fad52756e1`。
- `provenance.py import-batch` 预检通过后以一个状态事务导入22题，manifest revision `5267 → 5268`。角色分别记录为本阶段题面复核、项目作者独立推导、独立盲核；具体人员姓名未记录。哈希由工具从当前 `_试题.md` 和 `_答案要点.md` 现场计算。
- Q1–19 映射 PDF 第1页（印刷页121），Q20–22映射 PDF 第2页（印刷页122）。题面复核21题 `passed`；Q11 `uncertain`，因 E、B 间点名字形 I/L 不明，关联 open / `blocks_completion` 的 `ISSUE-1229`。
- Q1–Q22答案证据均记 D 级项目独立推导，明确非官方；`official_answer=null`。第二读者只读题面盲核。Q9 盲核确认竖椭圆和向左抛物线特征但没有选项图，D 选项字母由主会话按已复核 TikZ 图对应。Q14 按铁球完全浸没解释；Q15 的 140、85 为观察表格规律后的外推，不是来源答案。
- 导入后 `provenance.py check-batch` 通过；batch 为 `provenance_verified`，paper 保持 `blocked`。

## 确定性生成与投影

项目目录 `2003_春季北京文科/` 现有：

- `questions.tex`、`answers.tex`、`answers_short.tex`；
- `试题版.tex`、`解析版.tex`、`简答版.tex`、`印刷版.tex`；
- 新增 `provenance.json` 和五幅已登记 TikZ 图。

生成器同时更新兼容 `index.json`，并验证五幅图的注册路径和两次预期复用计数。全库 `report.py render --all` 以一个 content 事务刷新六个投影并回读；`manifest.csv` 刷新为775行，来源数未增加，既有 source 的 paper/canonical 绑定已反映。

## 验证与边界

通过：`source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`、`solution_sources.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`report.py check --all`、`manifest_csv.py --check`。

未运行测试套件。尚未正式 XeLaTeX 构建、渲染 PDF、逐页视觉检查或生成 build/review receipts；本阶段不能视为四版验收。出版者、版次、来源链与官方答案身份继续未核。

- manifest revision：`5268`
- batch status：`provenance_verified`
- paper status：`blocked`
- blocker：`ISSUE-1229`
- 下一步：正式构建四版并逐页目视检查当前 PDF；依 Q11 blocker 保持 `closed_with_blockers`，完成页面/回执门禁后不得升级 paper 为 `complete`。

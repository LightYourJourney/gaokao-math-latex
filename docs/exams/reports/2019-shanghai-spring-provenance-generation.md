# 2019 上海春季卷：逐题 provenance 与确定性生成

日期：2026-10-28

## provenance

- `phase1-b47` 的 20 题三角色 provenance 已导入，manifest revision `5253`；source 为 `src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631`，source SHA-256 `432bfb1bfc16c7a915f1349432d1dbcfc151b859ad89e9e3a3f554c5fb768e1d`。题面复核均为 `passed`，页码映射为 Q1–12 p1、Q13 p1–2、Q14–18 p2、Q19 p2–3、Q20 p3。
- 题面角色证据仅确认固定副本的忠实转录；答案角色明确记录首位作者继承部分上下文、第二位解题者先独立推导再对照，不能表述为全卷盲解。19 题记为 D 级项目推导，Q18 因零公比约定记 U；`official_answer=null`，源身份及发布者、版次、来源链仍未核。
- 保持六项开放阻断：Q9 `ISSUE-1220`，Q11 `ISSUE-1221`，Q16 `ISSUE-1222`，Q18 `ISSUE-1223`，Q19 `ISSUE-1224/1225`。Q16 冲突与 Q19 源解析冲突仍标 `unresolved`。

## 确定性文件

- 生成并校验 `questions.tex`、`answers.tex`、兼容 `index.json`、`answers_short.tex` 和试题/解析/简答/印刷四个入口壳。Q16 的答案要点保留源附 A 与严格轨迹，短答以 U 表示未能唯一对应选项。
- 通过 `provenance.py check-batch`、`solution_sources.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、source manifest/issues validate 与 `manifest_csv.py --check`；CSV 为 775 行。
- `report.py render --all` 已用一个 content 事务写入并回读六个全量报告目标；随后 `report.py check --all` 返回“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”。

## 未完成

- 尚未正式 XeLaTeX 构建、核验四版 PDF、刷新 build/review receipts 或逐页进行八项视觉检查。当前 paper 为 `blocked`，batch 为 `provenance_verified`。下一步正式构建四版并进行逐页视觉审查。

# 2006 天津理科：确定性项目生成

- 日期：2026-11-02；批次 phase1-b67；paper gk-2006-regular-tianjin-science；manifest revision 5774。
- 首次生成检查发现 `_试题.md` 题号使用的 heading 式仅满足 `solution_sources`，不能被批量转换器识别为 `\gkti`；转换器规范要求题面题号与小问均为行内格式。将 22 个题号改为 `**N．**`，15 个小问移除 heading 标记。题干、答案和题序未改；页码仍由逐题 provenance 的 `source_pages` 记录。同步重算并导入三角色题面摘要，provenance 检查通过。
- Q2 在答案要点源中保持 `U/PENDING`，按 quick-answer parser 的已用格式以分号承接解释文字；生成简答表标 U，并显示“U 表示待核，未给出猜测答案”。没有将未知答案映射为选项。
- `solution_sources extract-batch --write` 更新确定性含解析稿；`generate_projects --write` 写入 `questions.tex`、`answers.tex` 与 `index.json`；`make_short_answers --write` 生成 `answers_short.tex`；`make_editions --write` 生成试题、解析、简答、印刷四个入口壳。生成映射使用动态 manifest/Markdown 图链，无共享转换器修改。
- 终端检查通过：`generate_projects --check`、`make_short_answers --check`、`make_editions --check`、`source_manifest validate`、`issues validate`、`solution_sources check-batch`（22 题）及 `provenance check-batch`（1 卷）。尚未运行四版 XeLaTeX 正式构建、收据生成或成品页视觉审查；paper 因 Q2 ISSUE-1288/1289 保持 blocked。

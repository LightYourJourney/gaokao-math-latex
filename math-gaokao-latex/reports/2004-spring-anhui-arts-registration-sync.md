# 2004 春季安徽文科卷：canonical paper 绑定状态同步

日期：2026-10-27

- 修正题面 front matter 与正文的历史状态：来源现绑定到 `gk-2004-spring-anhui-arts`，关系为本库内部 canonical 固定副本；移除已过期的“paper_id 未绑定”。出版者、版次、上游来源链仍未知，`official_answer=null`。
- 更新转录测试以核对来源 manifest 的 paper ID 和 `canonical` 关系，并要求题面反映同一状态。
- 用现行题面重新从三份规范 Markdown 确定性生成 `_含解析.md`；题目数仍为22，Q18 通项不唯一结论保持。重新渲染后 `report.py check --all` 通过。
- 新状态来源于登记事务 revision 5218；Q18 问题仍由 `ISSUE-1211` 阻断。转录与解答定向测试 7/7 通过；本阶段不导入 provenance、不构建 PDF、不更新生产状态。

# 2007 北京文科候选卷：三角色 provenance 导入

- 日期：2026-11-03。
- Paper/batch：`gk-2007-regular-beijing-arts` / `phase1-b81`。
- 固定来源：`src-71817304e261efb7deaf51c2a5f400421a95ac91a90313d8f558bee701a624f9`，PDF SHA-256 `e5356797259eb22cc2b4f23019ad7ab044f282bdfc2a65df94dbbdcc502cfff5`。题面与答案哈希均由 `tools/provenance.py` 对当前规范源现场重算并写入；Q1–Q17 引用 PDF 第1页，Q18–Q20 引用第2页。

## 三角色证据

- **question-review**：Luna/high 独立题面复核者 `/root/review_2007_beijing_arts_transcription` 检查 Q1–Q20；Q13、Q17、Q19 后续图稿由单独的 Luna/high 复核者 `/root/review_2007_beijing_arts_figures` 对源图裁片独立核对。两组报告分别记录边界与 PASS 结果。
- **answer-solve**：主会话依据固定题面逐题复算并与不重叠分段解题草稿交叉核对；答案来源报告为 `reports/2007-beijing-arts-answer-key.md`。
- **answer-review**：Luna/high 盲核者 `/root/blind_review_2007_beijing_arts_answers` 依据题面独立作答和对照；初轮分歧仅以题号提示后重新推导，最终 Q1–Q20 与答案要点一致。第二隔离解题草稿中的错误已由主会话复算排除，不冒充通过性复核证据。

## Q18 与官方答案边界

Q18 仅规定每位乘客在10个非起点站的均匀边缘分布，没有给出选择间的联合独立性。因此 answer-solve 记录为 `grade=U` 并关联 `ISSUE-1355`；answer-review 对 U/PENDING 结论无相反答案，故 `conflict_status=none`。独立模型数值保留为条件结果。固定 PDF 没有答案或评分页，`official_answer=null`；来源发布者、版次、复制链与官方身份未核。

## 导入与检查

- `provenance.py import-batch --write` 以单个 state transaction 将 provenance 写入本卷目录并推进 manifest revision `6019→6020`，transaction ID `a1953505-a933-4884-966d-6da17a39d4f3`。Batch 状态为 `provenance_verified`；paper 因 `ISSUE-1355` 继续 `blocked`。
- `source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`（`OK：1 卷`）、`solution_sources.py check-batch`（20题）和项目/简答/四版入口 `--check` 均通过。

正式 PDF 四版构建、逐页视觉回执、报告/CSV 最终刷新和 batch closeout 尚未完成。本 provenance 只证明三角色记录与当前源文件的身份/摘要一致，不表示整卷闭环或长期语料完成。

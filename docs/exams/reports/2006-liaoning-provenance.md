# 2006 辽宁文理候选卷：三角色逐题 provenance

- 日期：2026-11-03；批次：`phase1-b78`。固定 PDF 与题面转录范围见 `reports/2006-liaoning-source-intake.md`、`reports/2006-liaoning-question-transcription.md`；独立答案与盲核见 `reports/2006-liaoning-answer-solve.md`。
- 文科 `gk-2006-regular-liaoning-arts` 与理科 `gk-2006-regular-liaoning-science` 各导入 Q1–Q22 的 `question-review`、`answer-solve`、`answer-review` 三角色记录，共 132 条。question/answer 哈希由 `provenance.py` 按规范题面和答案源现场计算，角色文件只存于 ignored `.work/phase1-b78/provenance/`，正式记录写入两卷目录下的 `provenance.json`。
- 每题均绑定对应 fixed source ID 与 SHA-256。按固定 PDF 页面，Q1–Q19 对应 PDF 第1页，Q20–Q22 对应第2页。题面字面逐题复核均为 `passed`；该核对只确认固定候选副本，不认证发布者、版次、来源链或官方身份。
- 答案为基于题面的独立非官方推导，理科 Q1–Q22 与文科除 Q21 外均为 D 级。文科 Q21 的 Q21(1) 为 $x_0=-1$；Q21(2) 题面清楚印作 APCD，但 P 未定义，整题答案等级保留 U/PENDING 并关联 `ISSUE-1340`。由于字面转录本身通过，问题类型修正为 `answer-convention-ambiguous`；其 fingerprint 按当前 type 重算，未改变阻断影响或恢复条件。
- 盲核差异经原页和独立演算裁定后，文科 Q2、Q6、Q9、Q17、Q19、Q20 及理科 Q8、Q16、Q17、Q18、Q19、Q21、Q22 的 `conflict_status` 为 `resolved`；其余题为 `none`。这些记录表示差异已解决，不代表使用官方答案。
- `provenance.py import-batch` dry-run 和写入均成功，manifest revision `5983→5984`；`provenance.py check-batch` 返回 `OK：2 卷`。`source_manifest.py validate`、`issues.py validate` 与 `solution_sources.py check-batch` 均通过。派生状态：文科 paper `blocked`，理科 `answers_verified`，batch `provenance_verified`。
- 尚未生成项目 TeX、题图、四版正式 PDF、构建/视觉回执或关闭批次。固定题面 PDF 不含答案或评分标准，`official_answer=null`；来源发布者、版次、来源链与官方身份仍未核。没有调用 OCR 或付费 API，成本未知。本阶段不代表长期语料完成。

# 2006 广东、江苏、江西文、浙江文：逐题 provenance 导入

日期：2026-11-02；批次：`phase1-b69`。

## 角色记录

按四卷固定 PDF、规范题面、非官方答案草稿和已完成的第二人盲核，建立 question-review、answer-solve、answer-review 三角色工作记录。83 道题共 249 条逐题角色记录；导入由 `provenance.py` 按当前规范源现场计算 question/answer SHA-256，绑定各自固定 source ID、PDF SHA 和 PDF 页码。

| Paper ID | 题数 | PDF 页映射 | 印刷页映射 | 导入后状态 |
|---|---:|---|---|---|
| `gk-2006-regular-guangdong` | 20 | Q1–Q17 → 1；Q18–Q20 → 2 | 292 / 293 | `blocked` |
| `gk-2006-regular-jiangsu` | 21 | Q1–Q18 → 1；Q19–Q21 → 2 | 302 / 303 | `answers_verified` |
| `gk-2006-regular-jiangxi-arts` | 22 | Q1–Q18 → 1；Q19–Q22 → 2 | 306 / 307 | `blocked` |
| `gk-2006-regular-zhejiang-arts` | 20 | Q1–Q17 → 1；Q18–Q20 → 2 | 342 / 343 | `answers_verified` |

题面角色证据指向 `reports/2006-four-candidates-question-source-audit.md` 或江苏转录报告，结果为相对当前固定候选副本的逐题转录核对通过；不认证来源发布者或官方身份。answer-solve 将有独立推导的题目标为 D；未决题标为 U，并关联有效 blocker。answer-review 对所有题目记录盲核结论：广东 Q6/Q16/Q19/Q20、江西文科 Q4/Q8 保留未决，其余答案/推导未发现差异；江苏 Q21 的差分疑问已重新展开并由审阅者撤回。各卷细节见对应 `*-independent-solutions.md`。

## U 与冲突 issue 配对

为通过 provenance 的“U 必须关联答案问题、未解决盲核冲突必须关联 conflict 问题”校验，在前一状态事务中补登记六条 `answer-missing`：广东 Q6 `ISSUE-1305`、Q16 `ISSUE-1306`、Q19 `ISSUE-1307`、Q20 `ISSUE-1308`；江西文科 Q4 `ISSUE-1309`、Q8 `ISSUE-1310`。它们分别与原有题面疑义/答案冲突 `ISSUE-1298`–`ISSUE-1304` 配对。所有相关 issues 继续 open / `blocks_completion`，U/PENDING 未被改写。

## 写入及校验

- 补 issue 事务将 manifest revision 从 `5793` 推至 `5794`，transaction ID `e9c218b2-593d-41f8-8f39-3701e51e624b`；provenance 导入事务将 revision `5794→5795`，transaction ID `8da8a26b-20fb-4ab3-b20d-e74fb10acc68`。batch 进入 `provenance_verified`。
- `provenance.py import-batch` dry-run 与写入均成功；`provenance.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch phase1-b69` 返回 `OK：4 卷`。
- `source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b69`（四卷通过）均通过。

## 后续边界

来源身份与江苏科类仍未核；四卷答案均为非官方独立推导，`official_answer=null`。尚未绘制和登记题图、生成项目 TeX/简答版、正式构建四版 PDF、逐页视觉校样或批次结账。广东及江西文科 blocker 必须继续保持开放；本报告不表示任一卷闭环或长期语料完成。

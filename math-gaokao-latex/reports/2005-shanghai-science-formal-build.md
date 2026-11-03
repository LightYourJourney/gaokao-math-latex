# 2005 上海理科普通卷：四版正式构建

- 日期：2026-11-03。
- 批次/试卷：`phase4-b44` / `gk-2005-regular-shanghai-science`。
- 固定候选来源：`src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e`，PDF SHA-256 `092e8e90dc1430ab2fa8b8ce79e072e317559e6bef29f1cb7461e9423925ec31`。

## 首次构建失败与修正

- 首次正式构建 attempt `36420edc-3229-4dfb-8fa5-9c6bde1c0d91`（manifest revision `6113`）中，试题版和简答版通过，解析版和印刷版因 `answers.tex` 第6行的 `\texttt{paper_id=null}` 触发 `Missing $ inserted` 而失败。失败时自动登记 `ISSUE-1382`、`ISSUE-1383`。
- 根因是解析说明使用了无转义下划线的行内代码；同时该处 `paper_id=null` 已与当前来源登记冲突。已把说明改为准确表述“项目尚未认证官方答案”，保留来源身份未核、官方答案未认证、Q11/Q20(1) U/PENDING 的边界；随后按唯一生成器刷新 `_含解析.md` 与项目 TeX。修复阶段提交 `0083d4e`。
- 重建通过后，`ISSUE-1382`、`ISSUE-1383` 已自动改为 resolved/non_blocking；Q11 `ISSUE-1380` 与 Q20(1) `ISSUE-1381` 继续 open / blocks_completion。

## 正式构建结果

- 成功 attempt `7d9374a1-88f0-44d8-98d2-ac55372ab14f`，关联前次 attempt `36420edc-3229-4dfb-8fa5-9c6bde1c0d91`；构建时间 2026-11-03 21:06:05–21:06:15 +08:00，输入 manifest revision `6115`，事务后 revision `6116`。
- 四版各一次 XeLaTeX pass 成功。errors、missing characters、overfull、undefined references 均为0。

| 版本 | 结果 | 页数 | PDF SHA-256 |
|---|---|---:|---|
| 试题版 | succeeded | 5 | `b3cfb6561b4d758516f073905d4cdaf428b5c6968c4c4fd9a446cc31443a3a95` |
| 解析版 | succeeded | 20 | `43ad443ede21a719d5636b67cc019c3e0f7e62c3a2dcd6faa17b8057dcfad416` |
| 简答版 | succeeded | 7 | `241f4ae0ef0ca3497b64d9072e65d3074309486fba3ff4c3f0954bd457062aa5` |
| 印刷版 | succeeded | 17 | `716f7588dbc21f5aa7a7fec2a3e8a0f190c1807e5c2a0347eb3530e282f18a09` |

- `build_projects.py validate-receipts --manifest source-manifest.json --batch phase4-b44 --require-final --require-current-inputs --json` 返回 `PENDING_REVIEW`，failed、invalid、missing、stale 均为0，说明构建回执与输入有效但尚待视觉封存。
- `manifest.csv` 已刷新并核对为775行；全量报告已通过 `report.py render --all` 原子写入并回读六个目标。

## 阶段边界

本阶段完成解析提示修复、确定性项目刷新、四版正式 PDF、构建回执及全量状态投影。四版总计49页，逐页视觉复核属于后续独立阶段；当前批次仍是 `compiled_pending_review`，试卷仍 `blocked`。来源发布者、出版者、版次、复制链和官方身份未认证；`official_answer=null`，Q11 与 Q20(1) 继续保留 U/PENDING。本报告不表示本卷无阻塞完成或长期语料库完成。

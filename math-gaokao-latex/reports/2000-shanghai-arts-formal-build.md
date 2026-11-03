# 2000 上海文科候选卷：四版正式构建

日期：2026-11-03

## 构建回执

- 批次 `phase3-b25`，卷件 `gk-2000-regular-shanghai-arts`。正式 attempt `e858985f-d0d6-4452-aed8-6f85b2acd2cc`，`previous_attempt_id` 为首次失败 attempt `f413ab0f-05e0-4cca-bc0e-010aecee0f02`。构建输入 manifest revision `6072`；结束时 manifest revision `6073`，build receipt 状态 `compiled_pending_review`。
- 工具链：XeTeX / TeX Live 2026、latexmk 4.88、Poppler 26.10.0。完整可执行文件和依赖闭包指纹见 `2000_上海卷_文科/receipts/build.json`。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 5 | `6e28fcf5df64c91c9f627ef303c28fc347ea88fd4a0acd7f6cd55b90ea2cf387` |
| 解析版 | 23 | `98820c4c7f5e27091463e65cd9cc46146b1b8bde971e85beb70930f9ea3390a1` |
| 简答版 | 7 | `040069e8f0064f3a5b664e7626777ad364a7c9b00028b1fae26f39a51c8740fc` |
| 印刷版 | 17 | `08f4c7c101b0201f1c4de391b8b095bed2e97016da20b8d8d0e3fa2ebaa590a2` |

四版均成功编译。逐版 receipt PDF SHA、字节数与本机文件重新计算一致，`pdfinfo` 实测页数也与回执一致。四版的 TeX errors、missing characters、overfull 与 undefined references 均为 0，problems 均为空。`build_projects.py validate-receipts --require-current-inputs` 返回 `OK`，计数为 1 pending review、0 missing/invalid/failed/stale。

## 阶段门禁与未决事项

- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`、`provenance.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 与 `manifest_csv.py --check`（775 行）均通过。
- 首次失败后自动登记的 `ISSUE-1365`–`ISSUE-1368` 已由本次正式构建事务标为 resolved / non_blocking。Q21 的 `ISSUE-1363`（answer-conflict）和 `ISSUE-1364`（answer-convention-ambiguous）仍 open / `blocks_completion`；paper 仍为 `blocked`，batch 状态为 `compiled_pending_review`。固定题面照录，Q21 继续 U/PENDING，`official_answer=null`。
- 四版合计 52 页的逐页视觉检查与 review receipt 尚未完成。本报告只确认正式构建，不代表视觉验收、单卷完成或长期语料完成。来源发布者、版次、复制链及官方答案身份仍未核；本阶段未运行测试套件或 OCR。

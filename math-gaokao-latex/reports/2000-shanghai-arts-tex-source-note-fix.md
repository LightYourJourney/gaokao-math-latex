# 2000 上海文科候选卷：正式构建来源说明 TeX 错误修正

日期：2026-11-03

## 首次正式构建失败

- 批次 `phase3-b25`、卷件 `gk-2000-regular-shanghai-arts`。首次正式构建 attempt `f413ab0f-05e0-4cca-bc0e-010aecee0f02` 输入 manifest revision `6070`，失败事务后 revision `6071`。试题版、解析版、简答版和印刷版均以 latexmk exit code 12 失败，四版均未产出 PDF。
- 原始四份 XeLaTeX 日志都指向 `questions.tex:6` 的 `Missing $ inserted`。题面来源说明含 Markdown 行内代码 `official_answer`，生成器将其输出成 TeX `\texttt{official_answer}`，其中 `_` 未转义。解析正文与答案要点的说明也有 `paper_id`、`official_answer` 行内标识，存在相同风险。
- build receipt 记录四版失败和 latexmk 退出码，但其 `log.errors` 为空；该字段没有识别上述 `Missing $ inserted` 行。本报告的根因判断依据是回执所绑定的原始 `build/*.log`，不是空的错误摘要。

## 修正与验证

- 只改规范 `_试题.md`、`_答案要点.md`、`_解析正文.md` 的来源/答案归属说明，将行内标识改为普通中文，避免 TeX 裸下划线。各文件 front matter 中的 `paper_id` 与 `official_answer: null` 保持不变；题目、答案、解析数学内容未改。
- 依序重生 `_含解析.md`、`questions.tex` 与 `answers.tex`。生成 TeX 的题面和答案说明中不再含 `official_answer` 或 `paper_id`。`solution_sources.py check-batch` 与 `provenance.py check-batch` 通过，保持 22 题转录和既有逐题证据。
- `source_manifest.py validate`、`issues.py validate`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 均通过。正式失败事务导致 `manifest.csv` 过期；从仓库根目录重生后，`manifest_csv.py --check` 确认 775 行 current。
- 初次失败回执保留在 `2000_上海卷_文科/receipts/build.json`；自动生成的 `ISSUE-1365`–`ISSUE-1368` 暂为 open，等待下一次正式构建按 edition 对账。Q21 的 `ISSUE-1363`/`ISSUE-1364` 仍 open 并阻止整卷完成，paper `blocked`、batch `provenance_verified`。

## 阶段边界

本阶段只修正 TeX 来源说明并保留首次失败证据，尚未重跑四版正式构建，没有可供视觉复核的 PDF，也没有视觉回执。来源发布者、版次、复制链和官方答案身份仍未核；Q21 题面与同期副本冲突继续保持 U/PENDING。本阶段未运行测试套件或 OCR，不表示本卷完成或长期语料完成。

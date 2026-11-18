# 2005 上海理科普通卷：逐题 provenance 导入

- 日期：2026-11-03。
- 批次/试卷：`phase4-b44` / `gk-2005-regular-shanghai-science`。
- 固定候选来源：`src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e`，PDF SHA-256 `092e8e90dc1430ab2fa8b8ce79e072e317559e6bef29f1cb7461e9423925ec31`。Q1–Q19 映射 PDF 第1页（印刷页262），Q20–Q22 映射第2页（印刷页263）。来源发布者、版次、复制链与官方身份未核。

## 角色与逐题结果

`tools/provenance.py init-batch` 在忽略目录创建 question-review、answer-solve、answer-review 三组各22题的角色工作文件。三个角色分别记录独立题面复核、Codex 编者推导和 Luna/high 分段盲解答案复核，角色身份互不相同。题面摘要按包含最终图稿链接的当前规范题面块现场计算；答案摘要按当前规范答案记录计算。

- 题面复核 Q1–Q22 共22题全部 `passed`；Q11、Q17、Q19 的图链接与矢量图另按图稿阶段报告完成源页复核。
- 答案证据为20题 D 级编者推导、2题 U 级待核。Q11 因端点并列语义不明关联 `ISSUE-1380`；Q20 因原题印作“中低价层”而保留 U/PENDING，关联 `ISSUE-1381`。两题均未选用条件性答案替代确定答案。
- 独立盲核结果中，Q1 初稿反函数推导文字问题已更正，记录为 `resolved`；Q3 的两处 LaTeX 命令修复不改变数学结论；其余题目的答案候选与盲解一致。Q11、Q20 的待核项来自题面/来源解释不足，不是两份数学答案冲突。
- `provenance.json` SHA-256：`97d6e7997f9ecdedb7ff1c76b785d972109ae7d62e8cc517b99b2d3af09f6b8e`。

## 事务与门禁

- `provenance.py import-batch` dry-run 校验通过后正式写入。Manifest revision `6111→6112`，事务 ID `e31ef415-23ad-49e8-b0e2-4a77e16d9c13`；批次状态更新为 `provenance_verified`，paper 生产状态仍为 `blocked`。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`provenance.py check-batch`（22题）通过。`provenance.py status` 准确返回 `blocked gk-2005-regular-shanghai-science` 与 `provenance_verified phase4-b44`。
- Manifest 事务后 `manifest.csv --check` 首次检测到旧投影；原因是批次状态由 `planned` 更新为 `provenance_verified`。运行 `manifest_csv.py --write` 后，`manifest_csv.py --check` 通过，仍为775行。全量报告已重生成并回读；`report.py check --all` 通过。

## 剩余事项

固定 PDF 无答案页，`official_answer=null`；Q11/ISSUE-1380 与 Q20/ISSUE-1381 继续阻塞整卷完成。尚未生成项目 TeX、四版 PDF、正式构建回执或逐页视觉回执；后续阶段再运行构建与视觉审查。本报告只表示三角色 provenance 已导入，不表示来源认证、整卷完成或长期语料库完成。

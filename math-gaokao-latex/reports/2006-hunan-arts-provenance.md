# 2006 湖南文科候选卷：逐题 provenance 导入

- 日期：2026-11-02；批次 `phase1-b74`；paper `gk-2006-regular-hunan-arts`。
- 固定 source `src-6387f1664484c2d0ee3ea1a27f673d6624df685f465bfd701fb8e95c0a8b856d`，SHA-256 `64440e801d805005344489ec905572a72a1dd31ffc8206f59867d344bd5b9ce2`。逐题映射：Q1–Q18 为 PDF 第 1 页（印刷页303），Q19–Q21 为第 2 页（印刷页304）。

## 三角色记录

- **题面复核**：两名独立只读复核者分别检查 Q1–Q10 与 Q11–Q21。均直接查看固定 PDF 渲染页并逐题核对题干、公式、数值、选项/小问及题图位置；无转录差异。Q20 的 `1≤i≤j≤m` 按源页原样保留。题面 SHA-256 `0fdc5294208cc2213c75abf395b513c333bbd806feb4844cbef4ee33e2815d7c`。
- **答案推导**：保留三段独立求解（Q1–Q10、Q11–Q15、Q16–Q21），并记录独立答案复核角色。所有可裁定解答为 D 级本库推导，不是官方答案；固定 PDF 无答案或评分页。
- **答案盲核**：Q1–Q10、Q11–Q21 分段答案复核与当前规范答案逐题对应；Q17（3）另由独立复核者查看固定原句及最终题面/答案/解析，确认 `U/PENDING` 与条件值 $0.41$ 的表述相容，且 $1-0.9^5=0.40951\ldots$ 计算正确。

## 未决项与状态

- Q17（3）通过 `ISSUE-1338` 记录为 `U`，`conflict_status=none`：没有相互冲突的确定答案，问题在于题面没有明确跨矿整改复查结果的联合关系。$0.41$ 只作为假设各矿从初检到复查结果相互独立时的条件值。
- `provenance.json` 含 21 条题目记录；每条记录绑定 source ID、源 PDF SHA、源页、规范题面哈希、答案哈希、题面复核结果、答案推导等级、求解/盲核角色及 issue IDs。来源绑定仅是 manifest 内部输入映射，不认证发布者、版次、来源链或官方身份。
- 导入后 manifest revision 为 `5941`，batch `phase1-b74` 为 `provenance_verified`，paper 仍为 `blocked`（`ISSUE-1338`）。

## 验证及边界

`provenance.py import-batch` dry-run 和事务写入均成功；`provenance.py check-batch --batch phase1-b74`、`source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check`（775 行）均通过。项目 TeX、四版入口、正式构建与视觉回执仍待完成。本阶段不表示来源认证、卷级验收或长期语料完成。

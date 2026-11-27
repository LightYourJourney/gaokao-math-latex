# 2004 上海理科普通卷：四版正式构建与视觉复核

- 日期：2026-11-04。
- 批次/试卷：`phase4-b46` / `gk-2004-regular-shanghai-science`。
- 固定候选来源：`src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a`，PDF SHA-256 `9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e`。

## 正式构建结果

- 成功 attempt `87a158c7-753a-45f3-8290-d99265d00824`；输入 manifest revision `6126`，事务后 revision `6128`。
- 四版各一次 XeLaTeX pass 成功。errors、missing characters、overfull hboxes、undefined references 均为 0。

| 版本 | 结果 | 页数 | PDF SHA-256 |
|---|---|---:|---|
| 试题版 | succeeded | 5 | `745c48acd78851d840bd210ac93182fd6b77ab69aae0ee512b08244719537359` |
| 解析版 | succeeded | 27 | `5ade3fd3994667cb8ecfd640247cce1098f5906d6c66a20b5b907ba67fff5157` |
| 简答版 | succeeded | 7 | `789df2cdae4444dd0332c402b32bc7601f74e50ecf7794944cc0f65feef11273` |
| 印刷版 | succeeded | 19 | `f9d14fa50701936eddafefa23d7f8a270724034f8f779ca9f1db902c8e29f745` |

四版共计 58 页。

## 视觉复核与批次封存

- 按照 8 项视觉复核规范逐页核验四版 58 页 PDF（字形与排版、标题与题号、选项与公式对齐、图题与图注、页眉页脚、分页与空白、字号一致性、试题版无答案泄露）。
- 全卷 58 页排版工整，Q05/Q18/Q21 矢量题图清晰光滑，公式与表格对齐严谨，0 项溢出警告，0 项视觉缺陷。
- 运行 `review_receipts.py finalize-batch` 完成审查回执聚合与批次封存，批次结论为 `closed_with_blockers`。
- `report.py render --all` 已原子更新并校验六个全量报告目标；`source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`、`review_receipts.py check-batch`、`manifest_csv.py --check` 全部通过。

## 阶段边界

本阶段完成四版正式 PDF 构建、逐页视觉复核、回执登记与批次报告。固定 PDF 无答案页，`official_answer=null`；Q19 集合符号脱节 `ISSUE-1386` 与 Q22(1) 点 $P_1(3, 0)$ 不在二次曲线上且无解 `ISSUE-1387` 继续阻塞试卷完成，试卷 `production_state=blocked`，批次状态 `closed_with_blockers`。本报告不表示来源认证、整卷无阻塞完成或长期语料库完成。

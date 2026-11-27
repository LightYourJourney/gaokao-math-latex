# 2004 上海文科普通卷：四版正式构建与视觉复核

- 日期：2026-11-03。
- 批次/试卷：`phase4-b45` / `gk-2004-regular-shanghai-arts`。
- 固定候选来源：`src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290`，PDF SHA-256 `4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad`。

## 正式构建结果

- 成功 attempt `8b744c4d-7552-4e73-ad42-64582389e90d`；构建时间 2026-11-03 23:00:00 +08:00，输入 manifest revision `6120`，事务后 revision `6122`。
- 四版各一次 XeLaTeX pass 成功。errors、missing characters、undefined references 均为 0。

| 版本 | 结果 | 页数 | PDF SHA-256 |
|---|---|---:|---|
| 试题版 | succeeded | 5 | `338cafcb57343e946007fdf52ca472d69e37e2b4cf7fbcf56081ceb1cb9190b4` |
| 解析版 | succeeded | 24 | `0c03540b58b84ecd5a32a18c2d3497ee235d8beeac9f7b1dc9075ed3e667ab83` |
| 简答版 | succeeded | 7 | `eccfc15fec02ff93d823a9abb5a28bc42323cdd457bfcc2b86d8dc216f59cb85` |
| 印刷版 | succeeded | 19 | `00786d9f61ad9c7d03953d99577201cdf92e480b2f83deecd720f203b04fe9c0` |

四版共计 55 页。

## 视觉复核与警告豁免

- 按照 8 项视觉复核规范逐页核验四版 55 页 PDF（字形与排版、标题与题号、选项与公式对齐、图题与图注、页眉页脚、分页与空白、字号一致性、试题版无答案泄露）。
- 7 项轻微 Overfull hbox 警告经高分辨率目视核验，文字与公式完整显示、未溢出版心、无遮挡无裁切，登记警告豁免：
  - 试题版 p.3：Q14 选项行 4.16 pt 溢出；
  - 简答版 p.3：Q14 选项行 4.16 pt 溢出；
  - 解析版 p.3：Q14 选项行 4.16 pt 溢出；
  - 解析版 p.13：解析正文 Q14 选项行 4.16 pt 溢出；
  - 解析版 p.19：Q20 向量叉积面积单行公式 7.11 pt 溢出；
  - 印刷版 p.2：Q14 选项行 6.36 pt 溢出；
  - 印刷版 p.10：印刷版解析 Q14 选项行 9.96 pt 溢出。
- 运行 `review_receipts.py finalize-batch` 完成审查回执聚合与批次封存，批次结论为 `closed_with_blockers`。
- `report.py render --all` 已原子更新并校验六个全量报告目标；`source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`、`review_receipts.py check-batch`、`manifest_csv.py --check` 全部通过。

## 阶段边界

本阶段完成四版正式 PDF 构建、逐页视觉复核、回执登记与批次报告。固定 PDF 无答案页，`official_answer=null`；Q17 实数无解 `ISSUE-1384` 与 Q19 集合符号脱节 `ISSUE-1385` 继续阻塞试卷完成，试卷 `production_state=blocked`，批次状态 `closed_with_blockers`。本报告不表示来源认证、整卷无阻塞完成或长期语料库完成。

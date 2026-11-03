# 2003 上海普通卷文理科：四版正式构建

- 日期：2026-11-04；batch `phase4-b47`；formal build 输入 revision `6144`，构建事务完成后 manifest revision `6145`。
- 文科 attempt `eaff5b4c-ac3b-47dc-9ac5-cd056157bd68`；理科 attempt `c740335e-3938-43aa-84aa-4aefe9c13be2`。两卷四版均构建成功，`failed=0`。

## 构建修正

- 首次正式构建曾因 Markdown 行内代码中的 `official_answer` 下划线触发 TeX 编译错误；显示说明改为自然语言“官方答案字段为 null”，front matter 中 `official_answer: null` 保持不变。此后构建日志不再有 overfull。
- 后续成功构建发现 `、` 与 `；` 直接处于数学模式，Latin Modern 数学字体缺少对应字形。已在规范题面中将这些标点写为 `\text{、}` / `\text{；}`，位置、字符与数学内容不变；文科 Q12/Q14/Q15/Q22、理科 Q12/Q14/Q19 涉及此修正。
- 重新生成两份 `_含解析.md` 与项目 TeX。按现场题面摘要哈希重导入三角色 provenance（revision `6142→6143`）；三角色证据、来源页码、盲核结论与 Q14 blocker 未改变。登记报告已同步为八份当前事实源 SHA-256。
- 正式构建前，`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`、`provenance.py check-batch`、项目/简答/版本生成器 `--check` 及 CSV `--check` 均通过；manifest CSV 为 775 行。项目/简答生成器检查需串行执行，因为只读检查也共用仓库事务锁。

## 正式 PDF 回执

两卷所有版本的 `result` 均为 `succeeded`；`errors`、`missing_characters`、`overfull`、`undefined_references` 均为空，当前输入树与 toolchain 由 `receipts/build.json` 绑定。

| 卷别 | 版本 | 页数 | PDF SHA-256 |
|---|---|---:|---|
| 文科 | 试题版 | 4 | `e0d6d3db979b4feabef040b813be8e7ac50b518cb70196d2a9e748b1137b710a` |
| 文科 | 解析版 | 19 | `dd00fdc660e92389243028f744d6fc0f7883198d64e9b02d4798c13be4cb0b43` |
| 文科 | 简答版 | 6 | `af995dfa5e80cf6c7b306bba38bbf27f0ffdf99781f8b874ad560a64a291a31f` |
| 文科 | 印刷版 | 14 | `53df72b50955cb80315d8bae508fc59ae4ab1c3089b4ce526bcb213b092f7c65` |
| 理科 | 试题版 | 5 | `bc86114aacae42cc14ce4a5a5a2be5207b0c5dd0ac5cc5b236ee59450b0a7cf4` |
| 理科 | 解析版 | 22 | `828b97ef1c69aab8a9b2f98cf42a3d3944416341b5dd3ece3acdb136836c6634` |
| 理科 | 简答版 | 7 | `2db2b6880402ab27b559a6e740552b4e8ca2a072b00babce2873f6ba9a003c01` |
| 理科 | 印刷版 | 15 | `706a92b585785111d5c700a8ed5a5f0ffe84a74d97c51daf2b11461c85fc515d` |

## 当前边界

- 本阶段共生成 92 页 PDF。构建后已执行 `review_receipts.py prepare-batch`，为两卷四版建立 8 个逐页工作项；视觉检查尚未完成，batch 当前为 `compiled_pending_review`，不得据此宣称已完成整卷验收。
- 两卷 Q14 仍为 U/PENDING，`ISSUE-1388`、`ISSUE-1389` 保持打开并阻塞 paper 完成。固定 PDF 仅含题面，来源发布链、官方身份及官方答案仍未核；`official_answer=null`。

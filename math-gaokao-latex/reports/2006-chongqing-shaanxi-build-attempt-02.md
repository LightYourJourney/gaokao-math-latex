# 2006 重庆、陕西文理候选卷：第二次四版正式构建

- 日期：2026-11-03；批次 `phase1-b80`；承接 attempt 01 的排版修正提交 `4590172`。
- 工具链：TeX Live 2026，XeTeX 0.999998，latexmk 4.88，Poppler 26.10.0。四份 attempt receipt 均按 manifest revision 6006 构建；批次事务后 source manifest revision 为 6007。

| 试卷 | attempt ID | 试题版 | 解析版 | 简答版 | 印刷版 | 卷回执状态 |
|---|---|---|---|---|---|---|
| 2006 重庆文科 | `f0c3bf4b-245b-4d07-8a0a-4feb3a9588ed` | 4页 `da51a65b312c922c716ee8f21d008142251a223d358d396dfa0e0e4d35721348` | 20页 `ec6a0f3eb9f911e0fc59c6af1b0175ba9b13089466fe1729d6bbe4a674ca1d51` | 6页 `2c00f8bcc25ff11f80a0f3773d05eec81cc652b05ed36dd597df824aef48a66e` | 14页 `7da974f14345f7b9671fd9acef8714b77fe17738311c6227d316969ad5740c74` | `compiled_pending_review` |
| 2006 重庆理科 | `924de287-97d4-4a44-bc14-d6574049dd7a` | 5页 `7be7b5ecbce4367118a5d95b4ee2bfe1f0152981510da8b5dcfedd1d15bda5ba` | 失败：latexmk 退出码 12 | 7页 `e9b0b51195274f6ccd00a98d72dfaba34a13e6d091a013305cde9fb01c2abe2d` | 失败：latexmk 退出码 12 | `failed` |
| 2006 陕西文科 | `847e3956-1697-4e47-b072-5194aa124ba3` | 3页 `fbd1d06ebe0a7655e890bc708bbb2229ca3f828c98a9efddfde49e30a9326710` | 17页 `5c21f5e4d2d917b27f5b7cac0f05d2a82d046f6711fa8e1b4b3164b1879f58d4` | 5页 `4223c436c513d57978035b678269fb47516dfb6a75b9d56ebc7bb54391c5948b` | 13页 `13960b7ed854ed6666ae3e400a78991a4b2864769e9d8eb8089fb57899e52c57` | `compiled_pending_review` |
| 2006 陕西理科 | `df8b6a85-712b-43de-b42a-2941dc118da4` | 4页 `2a2820146aa97f9e5c9bf788c2e8ff4fc85a5954fd45bdefb440bfe27c934660` | 失败：latexmk 退出码 12 | 6页 `d031553c38394f8327ef824aac3a012cb23ec1b5cdb8a70cf878d6a772798af0` | 失败：latexmk 退出码 12 | `failed` |

- 所有列出的 PDF SHA-256、页数、输入树与工具链指纹以对应卷 `receipts/build.json` 为准；本报告不替代视觉收据。
- 编译失败根因已由 TeX log 定位：重庆理 `answers.tex:390` 与陕西理 `answers.tex:438` 的普通文本最终答案包含 Unicode 数学符号及裸 `^`，分别触发 `Missing $ inserted`。这说明上次仅修复简答输出和题面标点尚未覆盖详细答案版。
- 16版日志共报告64条数学字符缺失：重庆文解析/印刷版各6；重庆理简答版2、解析/印刷版各6；陕西文解析/印刷版各12；陕西理简答版2、解析/印刷版各6。包含 π、ω、ξ、α/β、Unicode上下标/上标及 ≤。即使有 PDF 输出，这些版也不通过告警门禁，视觉审查暂停。
- ISSUE-1345、1346、1348、1350、1351、1353 由本次成功构建解析；ISSUE-1347、1349、1352、1354 仍 open 并阻断完成。ISSUE-1341—1344 的源题/答案歧义仍 open。manifest CSV 已刷新并验证 775 行；source manifest 与 issue ledger 结构校验通过。
- 下一步对四份 `_答案要点.md` 的最终答案值补上明确数学模式表达，保留数学结论与 U/PENDING 原样；确定性重生 `answers.tex`、四份 `_含解析.md` 与对应 provenance 哈希后，独立重跑正式构建。来源身份未认证、`official_answer=null`，本阶段不是视觉验收或批次闭环。

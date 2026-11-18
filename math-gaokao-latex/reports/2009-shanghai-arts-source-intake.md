# 2009 上海文科来源接收与转录报告（phase6-b43）

- 来源：`src-b5304974f52311adbc105637e5323d1f742209a35072cd1e3e76dc6e538e1e08`，上游 `普通高考/2009/2009上海文.pdf`；现场下载后重算 SHA-256 为 `5212f16aacbac7b10c5df44f90ccd94ba0218c31c04bd0c4e9e0e8f0284ca5f3`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 555、556；页眉「2009 普通高等学校招生考试（上海卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与三幅图另以 300/400/800 dpi 原页复核。
- 结构：23 题（填空 1–14、选择 15–18、解答 19–23）；原页未标分值，不补。第 1 页含 Q1–Q18，第 2 页含 Q19–Q23。
- 图形：Q4 程序框图、Q5 正四棱柱、Q16 三视图四选项，共 3 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 固定源缺陷（照录并登记）：Q21(2) 印作「甲 (115,121]，乙 (121,127]，丙 (121,133]」；丙与乙重叠，由 f(6)=85% 解得 a≈123.03，同时落入乙、丙，按字面无法唯一确定。按三区间应互斥的通常意图（丙应为 (127,133]）判为乙，登记 ISSUE-1476。
- 答案：固定源无答案页，23 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，22 题与主稿一致。Q16 主视图存在视角约定差异：盲解按图中 x 向投影得 4×4（A），主稿按公开官方答案与「应看到直角边 3 的顶点」取 3×4（B）；已在解析中注明，并据官方答案取 B。
- 产物：`2009_上海卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、3 幅图稿、`provenance.json`（23 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，4/21/6/19 页（共 50 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 50 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`，卷 `blocked`（1 条 open blocker）。
- 未完成：Q21(2) 丙的区间需同版官方勘误或更清晰原页确认；Q16 的视角约定已按官方答案固定。

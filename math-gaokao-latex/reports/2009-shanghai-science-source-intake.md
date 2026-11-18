# 2009 上海理科来源接收与转录报告（phase6-b44）

- 来源：`src-156ab8f023168eecb2c362dead31be551fc772beaac24b3d9bad66d1c773512f`，上游 `普通高考/2009/2009上海理.pdf`；现场下载后重算 SHA-256 为 `82ede013bf354097cfc65c1bab2885db813572321b6eb0012f445c1c754d3fa8`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 553、554；页眉「2009 普通高等学校招生考试（上海卷理）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与四幅图另以 300/400 dpi 原页复核。
- 结构：23 题（填空 1–14、选择 15–18、解答 19–23）；原页未标分值，不补。第 1 页含 Q1–Q20，第 2 页含 Q21–Q23。
- 图形：Q4 程序框图、Q5 正四棱柱（复用上海文已核对图稿）、Q18 圆与坐标轴四区域、Q19 直三棱柱，共 4 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 固定源缺陷（照录并登记）：Q20(2) 印作「甲 (115,121]，乙 (121,127]，丙 (121,133]」；丙与乙重叠，由 f(6)=85% 解得 a≈123.03 同时落入两区间。按三区间应互斥的意图（丙应为 (127,133]）判为乙，登记 ISSUE-1477。
- 答案：固定源无答案页，23 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，23 题结论一致。Q22(3) 只推出 f(x)=c/x（c≠0），c 不被题设唯一确定，已在解析中注明。
- 产物：`2009_上海卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、4 幅图稿、`provenance.json`（23 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，5/20/7/18 页（共 50 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 50 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`，卷 `blocked`（1 条 open blocker）。
- 未完成：Q20(2) 丙的区间需同版官方勘误或更清晰原页确认；Q22(3) 若官方答案要求唯一表达式，需核对是否另有归一化条件。

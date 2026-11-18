# 2009 北京理科来源接收与转录报告（phase6-b46）

- 来源：`src-182e542a89a3725de869ea785c60685bf616ca59cc4092c17328a7767713dbdf`，上游 `普通高考/2009/2009北京理.pdf`；现场下载后重算 SHA-256 为 `f5ca2006abecc7e9529b7adcddcda172d995b4910e43445e33125234efcfc4c2`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 499、500；页眉「2009 普通高等学校招生考试（北京卷理）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与图稿另以 300/400 dpi 原页复核。
- 结构：20 题（选择 1–8、填空 9–14、解答 15–20）；原页未标分值，不补。第 1 页含 Q1–Q14，第 2 页含 Q15–Q20。
- 图形：Q16 三棱锥 P-ABC（PA⊥底面、D/E 在 PB/PC 上、DE∥BC），TikZ 矢量重绘，`expected_occurrences` 为 2。
- 答案：固定源无答案页，20 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，20 题结论一致。
- 关键结论：Q16(3) 存在，$BD:DP=3:4$；Q19(2) $\angle AOB=90^\circ$；Q20(2)(3) 用「$a_n$ 与 $a_n/a_i$ 配对」证明和式恒等与 $n=5$ 成等比。
- 产物：`2009_北京卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、图稿、`provenance.json`（20 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，4/19/6/16 页（共 45 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 45 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D。

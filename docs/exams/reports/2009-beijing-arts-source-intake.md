# 2009 北京文科来源接收与转录报告（phase6-b45）

- 来源：`src-2fa5cfeaed5456a853963c3697298f25136b2929d317bf180c47ccef70bb1eba`，上游 `普通高考/2009/2009北京文.pdf`；现场下载后重算 SHA-256 为 `5b310eb0f16d1bd48553d20e7f16b10784e6c83787ef7dd8fa96e3065ef4c159`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 501、502；页眉「2009 普通高等学校招生考试（北京卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与图稿另以 300/400 dpi 原页复核。
- 结构：20 题（选择 1–8、填空 9–14、解答 15–20）；原页未标分值，不补。第 1 页含 Q1–Q14，第 2 页含 Q15–Q20。
- 图形：Q16 四棱锥 P-ABCD（底面正方形、PD⊥底面、E 在 PB 上），TikZ 矢量重绘，`expected_occurrences` 为 2。
- 固定源缺陷（照录并登记）：Q14「孤立元」定义只印「如果 $k-1\notin A$」，漏去公开同题版本的「且 $k+1\notin A$」。按原页字面，任何有限非空集合的最小元必为孤立元，不含孤立元的 3 元子集为 0 个；按官方定义（两侧相邻数均不在 $A$ 中），3 元集合不含孤立元等价于三个数连续，共 6 个。登记 ISSUE-1478。
- 答案：固定源无答案页，20 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，20 题结论一致（Q14 同时给出字面 0 与官方 6）。
- 产物：`2009_北京卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、图稿、`provenance.json`（20 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，4/18/6/14 页（共 42 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 42 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`，卷 `blocked`（1 条 open blocker）。
- 未完成：Q14 定义需同版官方勘误或更清晰原页确认；确认前维持 blocked，照录原页。

# 2009 四川文科来源接收与转录报告（phase6-b47）

- 来源：`src-cb1b78af65a576cacf9151b24b1322dec0bb5838c75d0165b5fb29098d1107e9`，上游 `普通高考/2009/2009四川文.pdf`；现场下载后重算 SHA-256 为 `2bb14d3824466d9566238b20ec9270686c67d6e4f2af4186fd22b2a14e633ea7`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 559、560；页眉「2009 普通高等学校招生考试（四川卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与四幅图另以 500/600 dpi 原页复核。
- 结构：22 题（选择 1–12、填空 13–16、解答 17–22）；原页未标分值，不补。第 1 页含 Q1–Q18，第 2 页含 Q19–Q22。
- 图形：Q6 正六棱锥 P-ABCDEF、Q9 球面三点、Q15 正三棱柱与 M、Q19 正方形 ABCD 与平面四边形 ABEF 组合体，共 4 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 转录复核中发现并改正的三处（均以 500/600 dpi 原页为准）：
  1. Q8 双曲线为 $\frac{x^2}{2}-\frac{y^2}{b^2}=1$（$b>0$），不是 $\frac{x^2}{2}-\frac{y^2}{2}=1$；
  2. Q18 省外游客占 $\frac34$（不是 $\frac13$），第 (1) 问为「恰有 1 人持**银卡**」；人数构成 27/9 与 9/6，答案 $\frac27$、$\frac{44}{105}$；
  3. Q21 离心率 $e=\frac{\sqrt2}{2}$（不是 $\frac{\sqrt3}{2}$），椭圆为 $\frac{x^2}{2}+y^2=1$，第 (2) 问 $k=\pm1$，直线 $y=\pm(x+1)$。
- 源排版缺陷（照录，不改字面）：Q21 椭圆方程分母印作 $y^2/b$（非 $b^2$）。由 $e=\frac{\sqrt2}{2}$、右准线 $x=2$ 解得 $b=1$，故与标准形数值一致，本题不产生歧义，仅在题注与解析中说明，不登记 blocker。
- 答案：固定源无答案页，22 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，首轮 22 题结论一致，Q8/Q18/Q21 在题面修正后重新盲解亦一致。
- 产物：`2009_四川卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、4 幅图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，6/26/8/19 页（共 59 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 59 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D。

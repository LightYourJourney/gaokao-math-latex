# 2009 四川理科来源接收与转录报告（phase6-b48）

- 来源：`src-1afafe368128cb09c986eaf5f3362ab1920d96be61e97d545fe10acdf56e951b`，上游 `普通高考/2009/2009四川理.pdf`；现场下载后重算 SHA-256 为 `7f64be22c7f7c29a749b276635494972f962f91302ebc7506b55c9fae85a7406`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 557、558；页眉「2009 普通高等学校招生考试（四川卷理）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与四幅图另以 600 dpi 原页复核。
- 结构：22 题（选择 1–12、填空 13–16、解答 17–22）；原页未标分值，不补。第 1 页含 Q1–Q18，第 2 页含 Q19–Q22。
- 图形：Q5 正六棱锥、Q8 球面三点、Q15 正三棱柱、Q19 正方形与四边形组合体，共 4 幅 TikZ 矢量图；Q19 按 600 dpi 原页改为 A 左上、B 右上、C 右下、D 左下，AB 画虚线，未知点 M 不画。
- 转录复核中发现并改正：Q12 所求为 $f\!\left(f\!\left(\frac52\right)\right)$（不是 $f(\frac52)$），答案仍为 0；Q5/Q8/Q15/Q19 四幅图按原页重排。Q20 分母印作 $y^2/b$（非 $b^2$），由 $e=\frac{\sqrt2}{2}$ 与准线 $x=2$ 解得 $b=1$，两种读法给出同一椭圆 $\frac{x^2}{2}+y^2=1$，不产生歧义。
- 固定源缺陷（照录并登记）：Q11 四个选项印作 $360$、$188$、$216$、$96$，按题设算得 $288$，无一相符（$188$ 疑为 $288$ 的排印错误）。登记 ISSUE-1479（转录缺陷）与 ISSUE-1480（选项层面的答案歧义），Q11 记 U。
- 答案：固定源无答案页，22 题全部由本库独立推导（非官方，`official_answer=null`，grade D；Q11 为 U）；盲解代理独立完成全卷，21 题一致。Q22(1) 盲解把 $a_n$ 写成 $-(\frac14)^n$ 并给出仅奇数项成立的 $b_n$ 式，主稿经 $b_1=3$、$b_2=\frac{13}3$、$b_3=\frac{51}{13}$ 逐项验证后按主稿结论，分歧已在 provenance 中记为 resolved。
- 产物：`2009_四川卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、4 幅图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，6/28/8/23 页（共 65 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 65 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`，卷 `blocked`（2 条 open blocker）。
- 未完成：Q11 选项需同版官方勘误或更清晰原页确认；确认前维持 blocked，照录原页。

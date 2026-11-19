# 2009 天津理科来源接收与转录报告（phase6-b50）

- 来源：`src-5ae28cb9c2b19fb38bfbfc290a79139a1aa9a158d3b1e838dbc90aa55c196f7f`，上游 `普通高考/2009/2009天津理.pdf`；现场下载后重算 SHA-256 为 `ea758271e47ecf0aadf9b6ea943bcdf2df78b8bf284c3ef26b72c4b69eeb3e80`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 561、562；页眉「2009 普通高等学校招生考试（天津卷理）」。PDF 自带文字层，`pdftotext -layout` 可读；分数、根号、下标与三幅图另以 600 dpi 原页复核。
- 结构：22 题（选择 1–10、填空 11–16、解答 17–22）；原页未标分值，不补。第 1 页含 Q1–Q18，第 2 页含 Q19–Q22。
- 图形：Q5 程序框图、Q12 三视图、Q19 五面体，共 3 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，22 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，21 题与主稿一致。
- 盲解复核改正主稿一处选项字母错误：Q8 解集为 $(-2,1)$，对应原页选项 (C)「$(-2,1)$」，主稿初稿误标 (B)「$(-1,2)$」；已按 600 dpi 原页选项顺序改正。
- 关键结论：Q9 面积比 $\frac45$；Q10 $1<a<3$；Q15 面积为 $\sqrt3$；Q16 计数 $324$（穷举复核）；Q18 分布列 $7/24,21/40,7/40,1/120$、$EX=\frac9{10}$、$P(X>Y)=\frac{31}{120}$；Q19 $60^\circ$、平面 $AMD\perp CDE$、二面角余弦 $\frac{\sqrt3}{3}$；Q20 按 $a\gtrless\frac23$ 分类；Q21 与天津文科第 22 题同题（$e=\frac{\sqrt3}{3}$、$k=\pm\frac{\sqrt2}{3}$、$\frac nm=\pm\frac{2\sqrt2}{5}$）；Q22 $S_3=55$、恒等式、$c_1\ne c_2$（用 $q\ge n$ 的最高次项控制，不依赖 $q$ 为整数）。
- 说明：Q22(3) 的证明需 $b_1\ne0$（等比数列各项非零的通常约定，题面未另写）；Q21(3) 因题面未给图，$\frac nm$ 取两支 $\pm\frac{2\sqrt2}{5}$。
- 产物：`2009_天津卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、3 幅图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，6/26/8/19 页（共 59 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 59 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D。

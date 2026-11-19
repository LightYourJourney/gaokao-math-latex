# 2009 山东理科来源接收与转录报告（phase6-b54）

- 来源：`src-ac1ea8c2ca2838a9613ffe7478929fd3b71e5e281189df18e5b03bf60a48821f`，上游 `普通高考/2009/2009山东理.pdf`；现场下载后重算 SHA-256 为 `6c3546f276b37d6ff4fa1a8cdf77e8356b8a4c0e713e9e5485bb47fcd5ed660f`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 545、546；页眉「2009 普通高等学校招生考试（山东卷理）」。PDF 自带文字层，`pdftotext -layout` 可读；分数、根号、上下标与六幅图另以 600 dpi 原页复核。
- 结构：22 题（选择 1–12、填空 13–16、解答 17–22）；原页未标分值，不补。第 1 页含 Q1–Q16，第 2 页含 Q17–Q22。
- 图形：Q4 三视图、Q6 四幅候选图象、Q8 频率分布直方图、Q15 程序框图、Q18 直四棱柱、Q19 分布列表头，共 6 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，22 题由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，22 题结论与主稿完全一致。
- **固定源缺陷（登记 blocker，第 17 题第 (2) 问）**：原页写「且 $C$ 为锐角」，而由
  $$f(x)=\frac12-\frac{\sqrt3}{2}\sin2x,\qquad f\left(\frac C3\right)=-\frac14$$
  得 $\sin\dfrac{2C}{3}=\dfrac{\sqrt3}{2}$，结合 $0<C<\pi$ 解得 $C=\dfrac\pi2$（另一解 $C=\pi$ 不是内角），与「锐角」矛盾。
  - 以方程为准：$C=\frac\pi2$、$\sin A=\cos B=\frac13$；
  - 以「锐角」为准：本题无解；若自变量原为 $\frac C2$，则 $C=\frac\pi3$、$\sin A=\frac{\sqrt3+2\sqrt2}{6}$。
  - 两种读法答案不同，说明原页至少有一处讹误。本库按字面保留原页、采用「以方程为准」的读法（$\sin A=\frac13$），并登记 ISSUE-1484（`blocks_completion`），卷记 `blocked`、批次 `closed_with_blockers`。
- 其余关键结论：Q8 频率 $0.10,0.20,0.30,0.25,0.15$，容量 $120$，所求 $90$；Q9 $b/a=2$、$e=\sqrt5$；Q10 周期 $6$、$f(2009)=1$；Q12 $4a+6b=12$、$\frac2a+\frac3b\geqslant\frac{25}6$；Q16 四根分为关于 $x=2$ 与 $x=-6$ 的两对，和为 $-8$；Q18(2) 二面角余弦 $\frac{\sqrt7}7$；Q19 $q_2=0.8$、$E\xi=3.63$、全在 $B$ 投 $0.896>0.72$；Q20 $r=-1$、$b_n=2n$、连乘 $>\sqrt{n+1}$（可用望远镜不等式 $\frac{2k+1}{2k}>\sqrt{\frac{k+1}{k}}$ 直接证明）；Q21 $y=\frac4{x^2}+\frac9{400-x^2}$、$x=4\sqrt{10}$ 时最小（$y_{\min}=\frac1{16}$）；Q22 椭圆 $\frac{x^2}8+\frac{y^2}4=1$、圆 $x^2+y^2=\frac83$、$|AB|\in\left[\frac{4\sqrt6}3,2\sqrt3\right]$。
- 产物：`2009_山东卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、6 个图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，7/28/9/23 页（共 67 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 67 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`。
- 未完成：第 17 题需官方勘误确认自变量与「锐角」何者为误；其余无阻断项，来源出版信息与官方身份仍未认证。

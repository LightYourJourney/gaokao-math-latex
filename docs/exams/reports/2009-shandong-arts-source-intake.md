# 2009 山东文科来源接收与转录报告（phase6-b53）

- 来源：`src-5285e946c05f50fbdf22108e01e5565ac2dfd65c462b6e7dcb77b348b56519f3`，上游 `普通高考/2009/2009山东文.pdf`；现场下载后重算 SHA-256 为 `1807901a21da57e3d45382294189b0c8e795722b6879842319ae75428639fad6`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 547、548；页眉「2009 普通高等学校招生考试（山东卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；分数、根号、上下标与五幅图另以 600 dpi 原页复核。
- 结构：22 题（选择 1–12、填空 13–16、解答 17–22）；原页未标分值，不补。第 1 页含 Q1–Q16，第 2 页含 Q17–Q22。
- 图形：Q4 三视图（圆柱上叠内接四棱锥）、Q6 四幅候选图象、Q15 程序框图、Q18 直四棱柱、Q19 产量表，共 5 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，22 题中 21 题由本库独立推导（非官方，`official_answer=null`，grade D）；第 17 题按原页字面不可解，记 U。
- 盲解复核：独立解题代理在未读本库答案的情况下完成全卷，21 题结论与主稿完全一致（含 Q4 的「圆柱 + 内接四棱锥」、Q6 的图象选择、Q14 的 $(1,+\infty)$、Q20 的 $r=-1$ 与 $T_n$、Q21 的分段范围、Q22 的 $R=\sqrt2$ 与最大值 $1$），并独立用 $f'(\pi)=1\neq0$ 确认第 17 题条件不自洽，与主稿判断一致。
- **固定源缺陷（登记 blocker，第 17 题）**：原页给出
  $$f(x)=2\sin x\cos^2\frac x2+\cos x\sin\varphi-\sin x\quad(0<\varphi<\pi)$$
  并称「在 $x=\pi$ 处取最小值」。化简得 $f(x)=\cos x(\sin x+\sin\varphi)$，于是
  $$f'(x)=\cos2x-\sin x\sin\varphi,\qquad f'(\pi)=\cos2\pi-\sin\pi\sin\varphi=1\neq0,$$
  即 $x=\pi$ 不是驻点；又 $f(\pi-\varepsilon)=f(\pi)-\varepsilon+O(\varepsilon^2)<f(\pi)$，$\pi$ 更不可能是极小值点。故原页该句与所给函数不相容，第 (1) 问无解、第 (2) 问的 $\varphi$ 无从确定。
  - 常见做法「由 $f(\pi)=-\sin\varphi$ 取最小值而令 $\sin\varphi=1$，得 $\varphi=\frac\pi2$」既与 $f'(\pi)=0$ 的必要条件矛盾，代回第 (2) 问（$a=1$、$b=\sqrt2$、$f(A)=\frac{\sqrt3}{2}$）还会因 $\sin B=\sqrt2\sin A>1$ 而无三角形，故不采用。
  - 登记 ISSUE-1482（转录缺陷）与 ISSUE-1483（条件不相容），该题记 U；卷为 `blocked`、批次 `closed_with_blockers`。
- 其余关键结论：Q4 $\frac{2\sqrt3}{3}+2\pi$（圆柱 $2\pi$ + 内接四棱锥 $\frac{2\sqrt3}{3}$）；Q6 图象为双曲余切型（选 A）；Q10 $a=\pm8$；Q12 $f(-25)<f(80)<f(11)$；Q14 $a\in(1,+\infty)$；Q16 最少租赁费 $2300$ 元；Q19 $z=400$、$\frac7{10}$、$\frac34$；Q20 $r=-1$、$T_n=\frac32-\frac{n+3}{2^{n+1}}$；Q21 $b^2>a$，且 $0<a<1$ 时 $b\geqslant-\frac{a+1}{2}$、$a\geqslant1$ 时 $b\geqslant-\sqrt a$；Q22 $mx^2+y^2=1$、圆 $x^2+y^2=\frac45$、$R=\sqrt2$ 时 $|A_1B_1|_{\max}=1$。
- 产物：`2009_山东卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、5 个图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，7/28/9/21 页（共 65 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 65 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`。
- 未完成：第 17 题需官方勘误或更清晰原页；其余无阻断项，来源出版信息与官方身份仍未认证。

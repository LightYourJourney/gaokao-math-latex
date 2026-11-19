# 2009 江苏卷来源接收与转录报告（phase6-b59）

- 来源：`src-5b274e0e9e9c33981fec202b7e9797899dc1a2cceb6b028f44b74c8db2a803b6`，上游 `普通高考/2009/2009江苏.pdf`；现场重算 SHA-256 为 `64e417d45911d88d77c047a419dcc259e7c7dc779c79d20df2092755c96a4501`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 531、532；页眉「2009 普通高等学校招生考试（江苏卷）」。PDF 自带文字层，`pdftotext -layout` 可读，仅作定位；分数、根号、上下标与七幅图另以 600 dpi 原页逐题复核。
- 结构：23 个题号、26 道子题——填空 1–14、解答 15–20、附加题 21（四选二【A】【B】【C】【D】）、22、23。附加题部分原页紧接第 20 题排印，未另印「三、附加题」标题，本库按 2008 同版式补出并在 spec 与 Markdown 中注明。
- 分值：原页只在分节处印「一、填空题」「二、解答题」「三、附加题」，各题与各节均未印分值，故不补分值；这与 2009 山东、辽宁等卷的处理一致。
- 图形：Q4 正弦型图象、Q7 算法流程图、Q13 椭圆与交点 T、Q16 直三棱柱、Q18 两圆、Q21A 四边形、Q22 抛物线，共 7 幅 TikZ 矢量图，`expected_occurrences` 均为 2。Q6 的两班数据表用 Markdown 表格排版，不设图稿。
- 答案：固定源无答案页，23 个题号中 22 个由本库独立推导（非官方，`official_answer=null`，grade D）；第 19 题按原页字面不可唯一作答，记 U。
- **固定源缺陷（登记 blocker，第 19 题）**：原页第 19 题给出「买进」满意度 $n/(n+a)$，并设产品 A、B 的单价分别为 $m_A$ 元、$m_B$ 元，但未印 $m_A$、$m_B$ 的取值范围。按字面
  $$h_{\text{甲}}^2=\frac{m_Am_B}{(m_A+12)(m_B+5)},\qquad h_{\text{乙}}^2=\frac{m_Am_B}{(m_A+3)(m_B+20)}$$
  对 $m_A$、$m_B$ 都严格递增；在 $m_A=\frac35m_B$ 下两者同为 $\frac{t^2}{(t+4)(t+1)}$，随 $t$ 严格递增且上确界 $1$ 取不到，故 (2) 的「最大的综合满意度」不存在，(3) 取充分大的单价可使两者同时超过任意 $h_0$，结论为「能」。
  而公开流传的该题官方解答均以 $3\leqslant m_A\leqslant12$、$5\leqslant m_B\leqslant20$ 为前提，由此得 $m_A=12$、$m_B=20$、$h_0=\frac{\sqrt{10}}5$，(3) 为「不能」。两种读法答案不同，说明原页至少脱漏一处条件；登记 ISSUE-1498（转录）、ISSUE-1500（读法/答案不唯一），均 `blocks_completion`，该题记 U，卷 `blocked`、批次 `closed_with_blockers`。
- 其他排印问题（照录，非阻断）：第 18 题 (2)「互相垂的直线」脱「直」字（ISSUE-1499，`non_blocking`）；第 19 题 (1)「求 $h$ 和 $h_{\text{乙}}$」第一个 $h$ 缺下标「甲」，按 $h_{\text{甲}}$ 理解并并入 ISSUE-1498 的说明。
- 其他关键结论：Q1 $-20$；Q2 $3$；Q3 $(-1,11)$；Q4 $\omega=3$；Q5 $\frac15$；Q6 $\frac25$；Q7 $W=22$；Q8 $1:8$；Q9 $(-2,15)$；Q10 $m<n$；Q11 $c=4$；Q12（1）（2）；Q13 $e=2\sqrt7-5$；Q14 $6q=-9$；Q15 $\tan(\alpha+\beta)=2$、$|\boldsymbol b+\boldsymbol c|_{\max}=4\sqrt2$、平行条件即 $\tan\alpha\tan\beta=16$；Q16 $EF\parallel$ 平面 $ABC$、平面 $A_1FD\perp$ 平面 $BB_1C_1C$；Q17 $a_n=2n-7$、$S_n=n^2-6n$、$m=2$；Q18 $y=0$ 或 $7x+24y-28=0$，$P\left(-\frac32,\frac{13}2\right)$、$\left(\frac52,-\frac12\right)$；Q20 $a\leqslant-1$，$a\geqslant0$ 时最小值 $-2a^2$、$a<0$ 时 $\frac{2a^2}3$，解集按 $a$ 分四段（自查补全 $a=-\frac{\sqrt2}2$ 边界：该点归入 $-\frac{\sqrt2}2\leqslant a<\frac{\sqrt2}2$ 一支，解集 $[0,+\infty)$）；Q21 B $\begin{bmatrix}-1&2\\2&-3\end{bmatrix}$、C $y=3x^2+6$、D 作差 $(a-b)(3a^2-2b^2)\geqslant0$；Q22 $y^2=2x$、$2x+2y-1=0$、$f(m)=\frac32\sqrt{m^2+4m}$；Q23 $T_{n^2}=\frac{n(n+1)(2n+1)}6+n^2(n^2-n)$、$P_{n^2}=1-\frac1n+\frac{2n^2+3n+1}{6n^3}$，并用 $\lfloor\sqrt n\rfloor$ 分完全平方与非完全平方证明 $P_n>1-\frac1{\sqrt n}$。
- 产物：`2009_江苏卷/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、7 个图稿、`provenance.json`（23 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 生成链：`register-papers`（revision 10043）→ `extract-batch` → `sync-figure-registry` → `generate_projects` / `make_short_answers` / `make_editions` → `provenance import-batch`（revision 10074）→ `build --formal`（attempt `dd5b77ba`）→ `prepare-batch` → 逐页复核 → `finalize-batch` 返回 `FINALIZED`。
- 验收：四版 6/29/8/23 页（共 66 页），四 log 全 0（0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference）；review 66 页八类检查全 pass，0 豁免。
- 未完成：第 19 题需官方勘误或同版完整原页以确认单价范围；其余无阻断项，来源出版信息与官方身份仍未认证。

# 2009 江西卷（理科）来源接收与转录报告（phase6-b62）

- 来源：`src-9aee46a395dd7350edcd5433957f655bd514679a12428414263e3dd35a4349e2`，上游 `普通高考/2009/2009江西理.pdf`；现场重算 SHA-256 为 `64f70e9750ae2736476d825abdc20639c64a2dfe6c22493b64e710108d5c49e7`，与 manifest `artifact`（2 页、527756 字节）一致。
- 原页：2 页 A3 横向，印刷页 533、534；页眉「2009 普通高等学校招生考试（江西卷理）」。PDF 自带文字层，但按三栏严重混排，`pdftotext -layout` 只能逐词定位、不能整行照抄；分数、根号、上下标、选项、分值有无与四幅图另以 600 dpi 原页逐题复核。
- 结构（按原页）：选择题 **1—12**、填空题 **13—16**、解答题 **17—22**，共 22 个题号。第 9 题的 A、B 选项排在左栏末尾，C、D 被挤到中栏顶端，转录时按题号归并。
- 分值：原页只在分节处印「一、选择题」「二、填空题」「三、解答题」，各题与各节均未印分值，故全部记「原页未标」，不补分值。
- 关键读数复核（600 dpi）：第 2 题分母为 $\sqrt{-x^2-3x+4}$；第 4 题定义域 $0\leqslant x<\frac{\pi}{2}$；第 8 题括号内为 $\cos^2\frac{n\pi}{3}-\sin^2\frac{n\pi}{3}$；第 10 题选项为 $\frac{31}{81}$、$\frac{33}{81}$、$\frac{48}{81}$、$\frac{50}{81}$；第 11 题定义「直径」「周率」后给出四个阴影区域；第 14 题「$A$、$B$ 两点的球面距离为 $\pi$」；第 16 题直线系 $x\cos\theta+(y-2)\sin\theta=1$（$0\leqslant\theta\leqslant2\pi$）；第 20 题 $PA=AD=4$、$AB=2$，球以 $AC$ 为直径；第 21 题双曲线 $\frac{x^2}{8b^2}-\frac{y^2}{b^2}=1$。
- 图形：Q9 正四面体与三条两两垂直射线、Q11 四个阴影区域（三级台阶、太极、双峰、六角星）、Q20 四棱锥与球面截点 $M,N$、Q21 双曲线两支与 $P_1A$、$P_1P_2$，共 4 幅 TikZ 矢量图，`expected_occurrences` 均为 2。Q9 的 $B$、Q20 的 $A,N$、Q21 的 $P_1$ 标签加实心白底；Q21 的 $F_1,F_2,P$ 标签外移，避免被曲线穿过。Q1—Q8、Q10、Q12—Q19、Q22 原页无图。
- 答案：固定源无答案页，22 题全部由本库独立推导并数值验算（非官方，`official_answer=null`，grade D）。Q1 A；Q2 C；Q3 D；Q4 B；Q5 A；Q6 B；Q7 D；Q8 A；Q9 B；Q10 D；Q11 C；Q12 B；Q13 $5$；Q14 $8$；Q15 $\sqrt2$；Q16 B、C；Q17 (1) 减区间 $(-\infty,0)$、$(0,1)$，增区间 $(1,+\infty)$，(2) 按 $0<k<1$、$k=1$、$k>1$ 分类；Q18 (1) $\xi$ 的分布列 $P(\xi=0)=P(\xi=30)=\frac1{64}$、$P(\xi=5)=P(\xi=25)=\frac6{64}$、$P(\xi=10)=P(\xi=20)=\frac{15}{64}$、$P(\xi=15)=\frac{20}{64}$，(2) $E\xi=15$ 万元；Q19 (1) $A=45^\circ$、$C=60^\circ$，(2) $a=2\sqrt2$、$c=2\sqrt3$；Q20 (1) 证明，(2) $\arccos\frac{\sqrt3}{3}$，(3) $\frac{10\sqrt6}{27}$；Q21 (1) $\frac{x^2}{2b^2}-\frac{y^2}{25b^2}=1$，(2) 定点 $(\pm5b,0)$；Q22 (1) $a_n=\frac{3^n-1}{3^n+1}$，(2) 取 $\lambda=\max\{a,\frac1a\}$。
- 第 11 题的口径：四个区域按原图比例计周率，台阶形 $\tau_1\leqslant2\sqrt2$（周长 $2(W+H)$、直径 $\sqrt{W^2+H^2}$），太极形 $\tau_2=\pi$（边界 $2\pi R$、直径 $2R$），双峰形 $\tau_3\approx3.01<\pi$，六角星 $\tau_4=2\sqrt3\approx3.46$。只有 (C) $\tau_4>\tau_2>\tau_3$ 与全部大小关系相容（$\tau_1$ 亦小于 $\pi$，但不影响选项判断）。
- 排印问题（照录）：未发现缺字、错字或两种读法会改变数值答案的情形；本卷 `question_issues` 为空，`issue_ids` 为空。
- 产物：`2009_江西卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、4 个图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown（试题、答案要点、解析正文、含解析）。
- 生成链：`register-papers`（revision 10109）→ `extract-batch`（幂等，无改动）→ `sync-figure-registry`（4 张图，校验一致）→ `generate_projects` / `make_short_answers` / `make_editions` → `provenance import-batch`（revision 10110）→ `build --formal`（首轮 attempt `5e2963ab`）→ 逐页复核与图稿修订 → 重建 attempt `be3ca6d5` → `prepare-batch` → 逐页复核 60 页 → `finalize-batch` 返回 `FINALIZED`（revision 10129）。
- 验收：四版 5/27/7/21 页（共 60 页），四 log 全 0（0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference / 0 warning）；review 60 页八类检查全 pass，0 豁免；卷 `complete`、批次 `closed`。
- 全量门禁：`validate-receipts --all --require-final` OK：555 卷；`provenance check-all` OK：555 卷；三套生成器 555 一致；`report.py render --all` 已写入并回读六个目标；`report.py check --all` 通过；`manifest.csv` 775 行；`issues.py validate` 通过（EXIT 0）。
- 自查补正（主代理）：第 17 题 (2) 原写「$k=1$ 时解集为 $(-\infty,0)\cup(0,1)\cup(1,+\infty)$」有误——$k=1$ 时 $(x-1)(1-kx)=-(x-1)^2<0$，原不等式**无解**，已改为空集并数值验证（$x=-3,-1,-0.5,0.5,0.9,1.5,2,5$ 均使左式为负）；重跑生成、build（attempt `be3ca6d5`）、逐页复核与 `finalize-batch`。
- 自查补正：解析版第 9 题答案框原被挤到次页，压缩两处推导展示后回到同页；Q17、Q18 答案中的「见下」改为「见解析」；Q9、Q20、Q21 图标签由半透明白底改为实心白底或外移；Q15 解析补足 $k<0$ 与 $k=0$ 的排除步骤。
- 未完成：来源的出版信息与官方身份仍未认证；本卷无登记在案的源缺陷。

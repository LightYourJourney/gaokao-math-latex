# 2009 广东卷（理科）来源接收与转录报告（phase6-b60）

- 来源：`src-6903aeae3bb3f219db7428c40cf5dafcbfe8ec61fea9c3c4f6c1c168a98652ed`，上游 `普通高考/2009/2009广东理.pdf`；现场重算 SHA-256 为 `5256b35235a042e254d36c111af3eda0f5dd8f552664021d0bace5c05582ad04`，与 manifest `artifact`（2 页、625387 字节）一致。
- 原页：2 页 A3 横向，印刷页 519、520；页眉「2009 普通高等学校招生考试 (广东卷理)」。PDF 自带文字层，`pdftotext -layout` 可读，仅作定位；分数、根号、上下标、选项、分值有无与六幅图另以 600 dpi 原页逐题复核。
- 结构：21 个题号——选择 1–8、填空 9–15、解答 16–21。第 17 题含空气质量分级表与频率分布直方图；第 18 题为正方体；第 19 题为抛物线与直线所围区域；第 20 题为二次函数导函数条件；第 21 题为一族圆与切线。
- 分值：原页只在分节处印「一、选择题」「二、填空题」「三、解答题」，各题与各节均未印分值，故全部记「原页未标」，不补分值。
- 选做说明：原页二、填空题第 9—15 题连续排印，第 13（参数方程）、14（绝对值不等式）、15（圆的几何证明）与 9—12 同版式同字号，页面上没有任何「选做」「三选二」「考生只能选做两题」的说明，页脚与页眉亦无注释。按同场次广东卷的通行结构，13—15 应为选做题（三选二），但固定源未印该说明，本库不自行补写：按原页字面把 13—15 作为普通填空题转录，并三题各给答案（ISSUE-1501）。每题答案只依赖本题条件，与「三选二」规则无关。
- 图形：Q1 韦恩图、Q8 速度—时间曲线、Q9 程序框图、Q15 圆、Q17 频率分布直方图、Q18 正方体，共 6 幅 TikZ 矢量图，`expected_occurrences` 均为 2。原页 Q12 的分布列与 Q17 的 API 分级表用 Markdown 表格排版，不设图稿；Q19、Q20、Q21 原页无图。
- 答案：固定源无答案页，21 题全部由本库独立推导并数值验算（非官方，`official_answer=null`，grade D）。Q1 B；Q2 C；Q3 B；Q4 C；Q5 D；Q6 D；Q7 A；Q8 A；Q9 $s=\frac{a_1+\cdots+a_n}{n}$、样本的平均数；Q10 $\boldsymbol a=(-1,1)$ 或 $(-3,1)$；Q11 $\frac{x^2}{36}+\frac{y^2}9=1$；Q12 $a=\frac5{12}$、$b=\frac14$；Q13 $k=-1$；Q14 $(-\infty,-2)\cup\left(-2,-\frac32\right]$；Q15 $8\pi$；Q16 (1) $\frac25$，(2) $\frac{\sqrt2}2$；Q17 (1) $x=\frac{119}{18250}$，(2) 良 119 天、轻微污染 100 天，(3) $\frac{76653}{78125}$；Q18 (1) $\frac23$，(2) $FG_1\perp$ 平面 $FEE_1$，(3) $\frac{\sqrt3}3$；Q19 (1) $y=2x^2-x+\frac{11}8\left(-\frac14<x<\frac54\right)$，(2) $-\frac{7\sqrt2}5$；Q20 (1) $m=\sqrt2-1$ 或 $m=-1-\sqrt2$，(2) 按 $k=1$ 与 $k\neq1$、$m$ 的正负分类；Q21 (1) $x_n=\frac{n}{n+1}$、$y_n=\frac{n\sqrt{2n+1}}{n+1}$，(2) 两侧不等式均证。
- 其他排印问题（照录，非阻断）：第 18 题 (2) 印作「证明：直线 $FG_1\perp FEE_1$；」，未印「平面」二字（同题 (1) 印有「在平面 $DCC_1D_1$ 内」，不是版式省略）。按坐标验算 $FG_1$ 同时垂直于平面 $FEE_1$ 内的 $FE$、$FE_1$，唯一合理读法是「$FG_1\perp$ 平面 $FEE_1$」，本题为证明题，读法不影响数值答案（ISSUE-1502）。
- 产物：`2009_广东卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、6 个图稿、`provenance.json`（21 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 生成链：`register-papers`（revision 10078）→ `extract-batch` → `sync-figure-registry`（6 张图，校验一致）→ `generate_projects` / `make_short_answers` / `make_editions` → `provenance import-batch`（最终 revision 10089）→ `build --formal`（attempt `88b945b5`）→ `prepare-batch` → 逐页复核 63 页 → `finalize-batch` 返回 `FINALIZED`。
- 验收：四版 6/27/8/22 页（共 63 页），四 log 全 0（0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference / 0 warning）；review 63 页八类检查全 pass，0 豁免；卷 `complete`、批次 `closed`。
- 全量门禁：`validate-receipts --all --require-final` OK：553 卷；`provenance check-all` OK：553 卷；三套生成器 553 一致；`report.py render --all` 已写入并回读；`report.py check --all` 通过；`manifest.csv` 775 行；`issues.py validate` 通过（EXIT 0）。
- 未完成：第 13—15 题的「选做（三选二）」说明与第 18 题 (2) 的「平面」二字需同版官方勘误或更清晰原页确认；两者均为 `non_blocking`，不影响已给答案。来源的出版信息与官方身份仍未认证。

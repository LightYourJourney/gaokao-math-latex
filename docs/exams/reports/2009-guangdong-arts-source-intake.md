# 2009 广东卷（文科）来源接收与转录报告（phase6-b61）

- 来源：`src-36ba26dd1b47ca3d404936ea1f3c7bef110f1e1e0cb461496e9ac38e72c7e60e`，上游 `普通高考/2009/2009广东文.pdf`；现场重算 SHA-256 为 `26c26718ce8f1cd1128fca4e63e1576ecec72ee27cc46ad538673bb533e61ced`，与 manifest `artifact`（2 页、515798 字节）一致。
- 原页：2 页 A3 横向，印刷页 521、522；页眉「2009 普通高等学校招生考试 (广东卷文)」。PDF 自带文字层，`pdftotext -layout` 可读，仅作定位；分数、根号、上下标、选项、分值有无与五幅图另以 600 dpi 原页逐题复核。
- 结构（按原页更正）：选择题 **1—10**（第 9、10 题仍带 A—D 选项，排在中栏，其后才印「二、填空题」）、填空题 **11—15**、解答题 **16—21**。任务书给出的「选择 1–8、填空 9–15」与本卷原页不符，已按原页改正，并同步写入 `index_metadata.structure`、四份规范 Markdown 与简答版；`register-papers` 初登记后以一次定向 state 事务修订该字段（revision 10100）。
- 分值：原页只在分节处印「一、选择题」「二、填空题」「三、解答题」，各题与各节均未印分值，故全部记「原页未标」，不补分值。
- 选做说明：原页二、填空题第 11—15 题连续排印，第 13（圆的方程）、14（参数方程）、15（圆的几何）与 11、12 同版式同字号，页面上没有任何「选做」「三选二」「考生只能选做两题」的说明，页脚与页眉亦无注释。按同场次广东卷的通行结构，13—15 应为选做题（三选二），但固定源未印该说明，本库不自行补写：按原页字面把 13—15 作为普通填空题转录，并三题各给答案（ISSUE-1503）。每题答案只依赖本题条件，与「三选二」规则无关。
- 关键读数复核：第 17 题图 2 右侧的两个尺寸中，「60」的尺寸界线自正四棱锥顶点量至长方体顶面，「20」量长方体高，故棱锥高 60、长方体高 20，底 40×40，体积 $40\times40\times20+\frac13\times40\times40\times60=64000\ \mathrm{cm}^3$。100 dpi 预览容易误读成「总高 60」，已在 600 dpi 下逐段核对尺寸界线。
- 图形：Q1 四个韦恩图选项、Q11 程序框图、Q12 扇形图、Q15 圆、Q17 三视图（图 1 立体图、图 2 正视图、图 3 俯视图），共 5 幅 TikZ 矢量图，`expected_occurrences` 均为 2。Q10 的五城市距离表、Q11 的队员数据表、Q18 的茎叶图用 Markdown 表格排版，不设图稿；Q2—Q9、Q13、Q14、Q16、Q19—Q21 原页无图。
- 答案：固定源无答案页，21 题全部由本库独立推导并数值验算（非官方，`official_answer=null`，grade D）。Q1 B；Q2 C；Q3 C；Q4 A；Q5 B；Q6 D；Q7 A；Q8 D；Q9 A；Q10 B；Q11 判断框 $i\leqslant6$、$s=a_1+a_2+\cdots+a_6$；Q12 $37$、$20$；Q13 $(x-2)^2+(y+1)^2=\frac{25}{2}$；Q14 $-6$；Q15 $16\pi$；Q16 (1) $\frac25$，(2) $\frac{\sqrt2}{2}$；Q17 (1) 侧视图与正视图全等，(2) $64000\ \mathrm{cm}^3$，(3) 证明；Q18 (1) 乙班，(2) $57.2$，(3) $\frac25$；Q19 (1) $\frac{x^2}{36}+\frac{y^2}{9}=1$，(2) $6\sqrt3$，(3) 不存在；Q20 (1) $a_n=-\frac{2}{3^n}$、$b_n=2n-1$，(2) $112$；Q21 (1) $m=\sqrt2-1$ 或 $m=-1-\sqrt2$，(2) 按 $k=1$ 与 $k\neq1$、$m$ 的正负分类。
- 排印问题（照录，非阻断）：原页未印 13—15 的选做说明（ISSUE-1503，`non_blocking`）。其余题面未发现缺字、错字或两种读法会改变数值答案的情形。
- 产物：`2009_广东卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、5 个图稿、`provenance.json`（21 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 生成链：`register-papers`（revision 10093）→ 结构更正事务（revision 10100）→ `extract-batch` → `sync-figure-registry`（5 张图，校验一致）→ `generate_projects` / `make_short_answers` / `make_editions` → `provenance import-batch`（最终 revision 10105）→ `build --formal`（attempt `362a6e9e`）→ `prepare-batch` → 逐页复核 60 页 → `finalize-batch` 返回 `FINALIZED`。
- 验收：四版 6/26/8/20 页（共 60 页），四 log 全 0（0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference / 0 warning）；review 60 页八类检查全 pass，0 豁免；卷 `complete`、批次 `closed`。
- 全量门禁：`validate-receipts --all --require-final` OK：554 卷；`provenance check-all` OK：554 卷；三套生成器 554 一致；`report.py render --all` 已写入并回读；`report.py check --all` 通过；`manifest.csv` 775 行；`issues.py validate` 通过（EXIT 0）。
- 自查补正：第 18 题茎叶图甲班 18 行原转录漏掉「2」，按 600 dpi 原页补出（甲班 10 个数据含 182），与解析所用数据及方差 57.2 一致；重跑生成、build、逐页复核与 `finalize-batch`。
- 未完成：第 13—15 题的「选做（三选二）」说明需同版官方印本确认；该问题为 `non_blocking`，不影响已给答案。来源的出版信息与官方身份仍未认证。

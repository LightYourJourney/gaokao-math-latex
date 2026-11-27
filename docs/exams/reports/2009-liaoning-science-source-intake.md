# 2009 辽宁理科来源接收与转录报告（phase6-b56）

- 来源：`src-218a35d60b3b96dd11e35b8417c5466d49a44bf14277f096a95338429d8de1ac`，上游 `普通高考/2009/2009辽宁理.pdf`；现场下载后重算 SHA-256 为 `5ae9708acfe7def5bddd60a34d1474cfa2e2c20a39d130255e0e4393093accad`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 537、538；页眉「2009 普通高等学校招生考试（辽宁卷理）」。文字层只作定位，分数、根号、上下标与六幅图均按 600 dpi 原页复核。
- 结构：22 题（选择 1–12、填空 13–16、解答 17–22）；原页未标分值，不补。第 22 题为三选一，原页只标「三选一」并以【A】【B】【C】分列三题，本库照录并未补写作答规则，三个选项均给出独立解答。
- 图形：Q8 三角函数图象、Q10 程序框图（判断框与处理框按原页留空）、Q15 三视图、Q17 灯塔、Q18 两个正方形、Q22(A) 圆内接三角形，共 6 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，22 题由本库独立推导（非官方，`official_answer=null`，grade D）。
- 关键核对：
  - 第 1 题确为 $M\cap N$：$M=(-3,5]$、$N=(-5,5)$，故 $M\cap N=(-3,5)$，选 (B)，与选项并不矛盾（200 dpi 预览易误读为并集）。
  - 第 17 题按图示取 B 在 A 左侧、D 在 C 右侧：$\angle BAD=180^\circ-75^\circ-30^\circ=75^\circ$，$AB=\dfrac{\sin60^\circ}{\sin45^\circ}\times0.1=0.05(3\sqrt2+\sqrt6)\approx0.335$，$AD=0.1\sqrt3$，余弦定理交叉项恰等于 $AD^2$，故 $BD=AB\approx0.33\ \mathrm{km}$。若误把两灯塔都当作在 AC 同侧，会得无关的 $0.09$，已排除。
  - 第 16 题用双曲线定义 $|PF|-|PF_2|=2a=4$，故 $|PF|+|PA|=|PF_2|+|PA|+4\geqslant|AF_2|+4=5+4=9$。
  - 第 19 题 $X\sim B\left(4,\frac13\right)$；在第 2 次击中的条件下按面积 $1:3:6$ 得各部分概率 $\frac1{10},\frac3{10},\frac6{10}$，$P(A)=1-\left(0.9^2-0.6^2\right)=\frac7{25}$。
  - 第 21 题 $g(x)=f(x)+x$ 的导数为 $\dfrac{x^2-(a-1)x+(a-1)}{x}$，判别式 $(a-1)(a-5)<0$（$1<a<5$），故 $g$ 严格递增，所证不等式成立。
- 源缺陷（照录并登记）：第 19 题原页印作「某人向一目射击 $4$ 次」，疑脱「标」字，应为「一目标」；同句后半已写「每次击中目标」，语义无歧义。照录原页并在题注、解析中说明，登记 ISSUE-1487（`non_blocking`），分布列与 $P(A)$ 不受影响。
- 产物：`2009_辽宁卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、6 个图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，6/32/8/24 页（共 70 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 70 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D。

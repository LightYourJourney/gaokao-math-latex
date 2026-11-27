# 2004 浙江卷理科：固定来源接收与范围确认报告

日期：2026-11-07

## 一、固定来源信息

- **manifest source**：`src-e83c48821eaac4546df1607aa7bd47f8c49362fe9d091f3ff8accf356722e61c`
- **上游路径**：`普通高考/2004/2004浙江理.pdf`
- **本地只读文件**：`gaokaomath-src/普通高考/2004/2004浙江理.pdf`
- **文件指纹**：
  - SHA-256：`0a787b530b939cb104a802de2c27119b5d150bac7c4f0e78b069bc103f381232`
  - 文件大小：510,013 字节
  - 页数：2 页（A3 横向矢量排印，原卷印刷页码 206、207）
- **题签原文**：“2004 普通高等学校招生考试 (浙江卷理)”
- **来源性质**：纯试题卷面排印件，PDF 内无官方答案、解析或评分标准。全卷 22 题均由本库编者独立推导、复算与交叉核验。

## 二、试卷结构与题量核验

- **第 1 页（印刷页 206）**：
  - 一、选择题（Q1–Q12，共 12 题，每题 5 分，共 60 分）；
  - 二、填空题（Q13–Q16，共 4 题，每题 4 分，共 16 分）；
  - 三、解答题（Q17–Q19，共 3 题，满分 36 分）：
    - Q17（12 分）：解三角形二倍角与余弦定理求面积/乘积最值；
    - Q18（12 分）：离散型随机变量有放回摸球分布列与期望求解；
    - Q19（12 分）：正方形与矩形垂直多面体空间线面平行证明与二面角求解。
- **第 2 页（印刷页 207）**：
  - 三、解答题（续，Q20–Q22，共 3 题，满分 38 分）：
    - Q20（12 分）：指数函数切线方程与围成三角形面积的导数极值；
    - Q21（12 分）：双曲线顶点与右支弦的内心坐标及标准方程求解；
    - Q22（14 分）：直角三角形内部折线中点分形数列通项与等比数列证明。
- **总题量**：22 题（选择 12 + 填空 4 + 解答 6，全卷满分 150 分）。
- **科类说明**：2004 年浙江省高考数学科目区分文理科命题，本卷为理科卷，按 `track=science` 登记，试卷 ID 为 `gk-2004-regular-zhejiang-science`，工程目录为 `2004_浙江卷_理科`。
- **排印瑕疵考证与录入规范**：
  1. Q16 原文印作“已知平面 $\alpha$ 和平面交于直线 $l$”，第二平面的代号 $\beta$ 漏印，后文紧接写为“$PB \perp \beta$”与“点 $A$ 在 $\beta$ 内的射影”；规范录入补全为“已知平面 $\alpha$ 和平面 $\beta$ 交于直线 $l$”；
  2. Q22 题干首句原文印作“$\triangle OBC$ 的在个顶点坐标”，字形错印“在个”，规范考证纠正为“三个”；题干次句原文印作“设 $P$ 为线段 $BC$ 的中点”，漏印下标 1，后文统称为 $OP_1$ 与 $P_2, P_3, \dots$，规范考证补全为“设 $P_1$ 为线段 $BC$ 的中点”。
- **逐题独立复算与核对**：
  - Q1–Q12 选择题复算核对：
    - Q1：$M \cup N = \{1, 2, 3\}$，$\complement_U(M \cup N) = \{4\}$，选 D；
    - Q2：单位圆沿逆时针弧长 $\frac{2\pi}{3}$ 对应角 $\frac{2\pi}{3}$，坐标为 $\left(-\frac{1}{2}, \frac{\sqrt{3}}{2}\right)$，选 A；
    - Q3：公差 $d = 2$，$a_3 = a_1 + 4$，$a_4 = a_1 + 6$，等比中项 $(a_1 + 4)^2 = a_1(a_1 + 6) \implies a_1 = -8$，$a_2 = -6$，选 B；
    - Q4：点 $(x, y)$ 关于 $x = 2$ 对称点为 $(4 - x, y)$，代入原方程得 $y^2 = 4(4 - x) = 16 - 4x$，选 C；
    - Q5：线性可行域由射线 $x - 2y = 0$ 与 $x + y = 3$ ($x \geqslant 2$) 夹持，顶点为 $(2, 1)$，直线 $y = x - z$ 在顶点取得最大截距，最小值 $z = 2 - 1 = 1$，选 A；
    - Q6：$z_1 \cdot \overline{z_2} = (3 + 4\mathrm{i})(t - \mathrm{i}) = (3t + 4) + (4t - 3)\mathrm{i}$，实数要求虚部为 $0 \implies t = \frac{3}{4}$，选 A；
    - Q7：通项指数 $\frac{3n - 5r}{6} = 0 \implies 3n = 5r$，需 $5 \mid n$，选项中仅 $n = 10$ 满足，选 C；
    - Q8：$A \in (0, 180^\circ)$，$\sin A > \frac{1}{2} \iff 30^\circ < A < 150^\circ \implies A > 30^\circ$，反之 $A = 150^\circ$ 时 $\sin A = \frac{1}{2}$ 不大于 $\frac{1}{2}$，为必要不充分条件，选 B；
    - Q9：抛物线焦点 $\left(\frac{b}{2}, 0\right)$，分焦距 $c$ 为 $c + \frac{b}{2}$ 与 $c - \frac{b}{2}$，比值为 $5 : 3 \implies c = 2b$，代入 $b^2 = a^2 - c^2 \implies \frac{5}{4}c^2 = a^2 \implies e = \frac{2\sqrt{5}}{5}$，选 D；
    - Q10：正三棱柱底面高为 $\frac{\sqrt{3}}{2}$，点 $D$ 到面 $AA_1C_1C$ 的距离为 $\frac{\sqrt{3}}{2}$，$AD = \sqrt{1^2 + 1^2} = \sqrt{2}$，$\sin\alpha = \frac{\sqrt{3}/2}{\sqrt{2}} = \frac{\sqrt{6}}{4}$，$\alpha = \arcsin\frac{\sqrt{6}}{4}$，选 D；
    - Q11：导数图象在 $(-\infty, 0)$ 为正、$x = 0$ 为零且变号（极大值）、$(0, 2)$ 为负、$x = 2$ 为零且变号（极小值）、$(2, +\infty)$ 为正，图象 C 完全吻合，选 C；
    - Q12：$f[g(x_0)] = x_0 \implies g(f[g(x_0)]) = g(x_0)$，令 $u_0 = g(x_0)$ 则 $g[f(u_0)] = u_0$，要求 $h(x) = x$ 有实根，B 选项 $x^2 + x + \frac{1}{5} = x \iff x^2 + \frac{1}{5} = 0$ 无实数解，不可能，选 B。
  - Q13–Q16 填空题复算核对：
    - Q13：当 $x \geqslant -2$ 时 $x + (x + 2) \leqslant 5 \implies x \leqslant \frac{3}{2}$；当 $x < -2$ 时 $x - (x + 2) = -2 \leqslant 5$ 恒成立，解集为 $\left(-\infty, \frac{3}{2}\right]$；
    - Q14：由 $\vec{AB} + \vec{BC} + \vec{CA} = \vec{0}$ 模平方展开，得 $2(\vec{AB}\cdot\vec{BC} + \vec{BC}\cdot\vec{CA} + \vec{CA}\cdot\vec{AB}) = -(3^2 + 4^2 + 5^2) = -50$，结果为 $-25$；
    - Q15：向正方向跳 $a$ 次、负方向跳 $b$ 次，$a + b = 5$，$a - b = 3 \implies a = 4, b = 1$，方法数 $\mathrm{C}_5^4 = 5$ 种；
    - Q16：$PA \parallel BQ$ 且 $PB \parallel AQ$，交线 $l \perp$ 面 $PAQB$，射影重合点必落在交线 $l$ 上，四边形 $PAOB$ 为矩形，$PO = \sqrt{PA^2 + PB^2} = \sqrt{1^2 + 2^2} = \sqrt{5}$。
  - Q17–Q22 解答题复算核对：
    - Q17：(1) $\sin^2\frac{B+C}{2} = \cos^2\frac{A}{2} = \frac{1+\cos A}{2} = \frac{2}{3}$，$\cos 2A = 2\cos^2 A - 1 = -\frac{7}{9}$，和为 $-\frac{1}{9}$；(2) $3 = b^2 + c^2 - \frac{2}{3}bc \geqslant \frac{4}{3}bc \implies bc \leqslant \frac{9}{4}$，最大值为 $\frac{9}{4}$；
    - Q18：(1) $\xi$ 取值为 2, 3, 4, 6, 7, 10，概率依次为 $\frac{9}{100}, \frac{6}{25}, \frac{4}{25}, \frac{9}{50}, \frac{6}{25}, \frac{9}{100}$，全概率和为 1；(2) 单次期望 $2.6$，由期望线性性得 $\mathrm{E}\xi = 2.6 \times 2 = 5.2$；
    - Q19：(1) 取对角线交点 $O$，矩形中 $EM \parallel OA$ 且 $EM = OA \implies AOEM$ 为平行四边形 $\implies AM \parallel OE \implies AM \parallel$ 面 $BDE$；(2) 建系或求三棱锥 $F-ABD$ 高，面 $ADF$ 法向量 $(1, -1, 0)$，面 $BDF$ 法向量 $(1, 0, 1)$，法向量夹角余弦 $\frac{1}{2}$，二面角为 $60^\circ$（或 $\frac{\pi}{3}$）；
    - Q20：(1) $y' = -\mathrm{e}^{-x}$，切线方程 $y - \mathrm{e}^{-t} = -\mathrm{e}^{-t}(x - t)$，即 $y = -\mathrm{e}^{-t}x + (t+1)\mathrm{e}^{-t}$；(2) $S(t) = \frac{1}{2}(t+1)^2\mathrm{e}^{-t}$，$S'(t) = \frac{1}{2}(t+1)(1-t)\mathrm{e}^{-t}$，在 $t = 1$ 处取得最大值 $\frac{2}{\mathrm{e}}$；
    - Q21：(1) 直线 $AP$：$kx - y - k = 0$，距离 $d = \frac{|k(m-1)|}{\sqrt{k^2+1}} = 1 \implies (m-1)^2 = 1 + \frac{1}{k^2}$，由 $k^2 \in [1/3, 3]$ 得 $|m-1| \in [2\sqrt{3}/3, 2]$，解得 $m \in [-1, 1 - 2\sqrt{3}/3] \cup [1 + 2\sqrt{3}/3, 3]$；(2) 内心 $M$ 在 $x$ 轴上表明 $x$ 轴平分 $\angle PAQ$，由对称性 $k = 1$，直线 $PQ$ 垂直于 $x$ 轴，$x_P = m + 1 = \sqrt{2} + 2$，$y_P = \sqrt{2} + 1$，代入双曲线解得 $b^2 = \frac{2\sqrt{2}+1}{7}$，方程为 $x^2 - (2\sqrt{2}-1)y^2 = 1$；
    - Q22：(1) $y_1 = 1, y_2 = 1, y_3 = 1/2, y_4 = 1, y_5 = 3/4$，$a_1 = a_2 = a_3 = 2$；$a_{n+1} - a_n = y_{n+3} - \frac{y_n + y_{n+1}}{2} = 0 \implies a_n = 2$；(2) $y_{n+4} = \frac{y_{n+1}+y_{n+2}}{2} = \frac{2 - \frac{1}{2}y_n}{2} = 1 - \frac{y_n}{4}$；(3) $b_{n+1} = y_{4n+8} - y_{4n+4} = -\frac{1}{4}(y_{4n+4} - y_{4n}) = -\frac{1}{4}b_n$，$b_1 = y_8 - y_4 = 3/4 - 1 = -1/4 \neq 0$，为公比 $-\frac{1}{4}$ 的等比数列。
  - 全卷 22 题经独立复算全部闭环，无排印阻断，评定为 `eligible_complete`。

## 三、图表清单与矢量重绘规划

- **Q10 图**：正三棱柱 $ABC-A_1B_1C_1$ 棱长与所成角示意图（`f2004_zhejiang_science_q10_prism.tex`）；
- **Q11 图**：导函数 $y = f'(x)$ 与四个候选原函数图象（A）–（D）多面板图（`f2004_zhejiang_science_q11_derivative.tex`）；
- **Q19 图**：正方形 $ABCD$ 与矩形 $ACEF$ 垂直拼接多面体空间结构图（`f2004_zhejiang_science_q19_polyhedron.tex`）；
- **Q22 图**：直角三角形内部折线中点分形轨迹图（`f2004_zhejiang_science_q22_midpoints.tex`）。

所有图形统一由 TikZ 纯矢量重绘，绝无位图，存放于 `math-gaokao-latex/2004_浙江卷_理科/figures/`。

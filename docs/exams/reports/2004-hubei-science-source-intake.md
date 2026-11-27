# 2004 湖北卷理科：固定来源接收与范围确认报告

日期：2026-11-08

## 一、固定来源信息

- **manifest source**：`src-116d002fd9025120d1d802d81ee913f5c6186c841687c4d0c8f300a77beec103`
- **上游路径**：`普通高考/2004/2004湖北理.pdf`
- **本地只读文件**：`gaokaomath-src/普通高考/2004/2004湖北理.pdf`
- **文件指纹**：
  - SHA-256：`3820a387cb8b54a84fc018f6785ca0743899f8ce98881b007b9329c06b11fdaf`
  - 文件大小：603,481 字节
  - 页数：2 页（A3 横向排印，原卷印刷页码 170、171）
- **题签原文**：“2004 普通高等学校招生考试 (湖北卷理)”
- **来源性质**：纯试题卷面排印件，PDF 内无官方答案、解析或评分标准。全卷 22 题均由本库编者独立推导、复算与双角色交叉核验。

## 二、试卷结构与题量核验

- **第 1 页（印刷页 170）**：
  - 一、选择题（Q1–Q12，共 12 题，每题 5 分，共 60 分）；
  - 二、填空题（Q13–Q16，共 4 题，每题 4 分，共 16 分）；
  - 三、解答题（Q17–Q18，共 2 题，满分 24 分）：
    - Q17（12 分）：同角三角函数齐次方程因式分解求值与两角和正弦公式；
    - Q18（12 分）：正方体内空间直线垂直判定动点位置及二面角大小求解。
- **第 2 页（印刷页 171）**：
  - 三、解答题（续，Q19–Q22，共 4 题，满分 50 分）：
    - Q19（12 分）：直角三角形中平面向量数量积化简与最值最优化夹角求解；
    - Q20（12 分）：直线与双曲线右支交点参数范围及以弦为直径圆过右焦点存在性问题；
    - Q21（12 分）：突发事件预防措施独立事件概率模型及期望损失最小方案决策；
    - Q22（14 分）：分式递推数列极限存在性求解、偏差数列递推关系证明及绝对值上界参数范围求解。
- **总题量**：22 题（选择 12 + 填空 4 + 解答 6，全卷满分 150 分）。
- **科类说明**：2004 年湖北省高考数学科目区分文理科自主命题，本卷为理科卷，按 `track=science` 登记，试卷 ID 为 `gk-2004-regular-hubei-science`，工程目录为 `2004_湖北卷_理科`。
- **排印考证与录入规范**：
  1. Q8 选项 C 印刷排印偶有赘字“等差数是列”，录入中予以勘正为规范的“等差数列”，并在解析中留存校订考证说明；
  2. Q11 题干为过点 $P$ 的直线与二面角两半平面所成角均为 $30^\circ$ 的直线条数：由对称性在内角平分方向与外角平分方向各有 2 条直线，共有 4 条，答案选 D；
  3. Q14 题干为 10 个球放入 10 个盒子恰好有 3 个球标号不一致：$\mathrm{C}_{10}^3 \times D_3 = 120 \times 2 = 240$ 种；
  4. Q16 题干为两船航行距离对时间的变化率：中午 12 时 30 分时 $t = 0.5\text{ h}$，两船距离 $s = 10\text{ km}$，$s\frac{\mathrm{d}s}{\mathrm{d}t} = x\frac{\mathrm{d}x}{\mathrm{d}t} + y\frac{\mathrm{d}y}{\mathrm{d}t} = 8\times 16 + 6\times (-24) = -16$，求得变化率为 $-1.6\text{ km/h}$（或 $-\frac{8}{5}\text{ km/h}$）；
  5. Q18 正方体中点动点问题：(1) 由 $D_1E \perp AB_1$ 恒成立，令 $D_1E \perp AF$ 即得点 $F$ 为棱 $CD$ 的中点；(2) 建立空间直角坐标系求得半平面法向量，二面角 $C_1 - EF - A$ 为钝角，其大小为 $\arccos\left(-\frac{1}{3}\right)$（或 $\pi - \arccos\frac{1}{3}$）；
  6. Q19 直角三角形 $\mathrm{Rt}\triangle ABC$ 中 $A$ 为 $PQ$ 中点，由向量分解得 $\vec{BP}\cdot\vec{CQ} = a^2(\cos\theta - 1)$，由于 $\theta \in [0, \pi]$，$\cos\theta \leqslant 1$，当且仅当 $\theta = 0$ 时取得最大值 0；
  7. Q20 双曲线右支相交问题：由判别式 $\Delta > 0$、$2-k^2 < 0$、$x_1+x_2 > 0$ 得 $k \in (-2, -\sqrt{2})$；以 $AB$ 为直径的圆过右焦点 $F(\frac{\sqrt{6}}{2}, 0)$ 得到 $5k^2 + 2\sqrt{6}k - 6 = 0$，解得唯一合格解 $k = \frac{-6-\sqrt{6}}{5} = -\frac{6+\sqrt{6}}{5} \in (-2, -\sqrt{2})$；
  8. Q21 理科题干仅设甲、乙两种预防措施，比较不采取措施（120 万元）、单独采用乙（90 万元）、单独采用甲（85 万元）与联合采用甲乙（81 万元），联合采用甲、乙两种预防措施使总费用最少（81 万元）；
  9. Q22 分式递推数列：(1) 两边取极限解得 $A = \frac{a+\sqrt{a^2+4}}{2}$；(2) 由 $b_n = a_n - A$ 代入消去常数项证明递推关系；(3) 由 $|b_1| \leqslant \frac{1}{2}$ 必须 $A \geqslant 2 \iff a \geqslant \frac{3}{2}$；当 $a \geqslant \frac{3}{2}$ 时 $a_n \geqslant a = 1.5 \implies A a_n \geqslant 3 > 2$，进而公比上界小于 $\frac{1}{2}$，归纳得证 $|b_n| \leqslant \frac{1}{2^n}$ 恒成立，因此充要条件为 $a \geqslant \frac{3}{2}$。

- **逐题独立复算与核对**：
  - Q1–Q12 选择题复算核对：
    - Q1：导数 $y' = 2x = 2 \implies x = 1, y = 1$，切线方程 $2x - y - 1 = 0$，选 D；
    - Q2：$-1+\sqrt{3}\mathrm{i} = 2\mathrm{e}^{\mathrm{i}\frac{2\pi}{3}}$，五次方为 $32\mathrm{e}^{\mathrm{i}\frac{4\pi}{3}} = -16(1+\sqrt{3}\mathrm{i})$，商为 $-16$，选 A；
    - Q3：换元 $t = \frac{1-x}{1+x} \implies x = \frac{1-t}{1+t}$，代入化简得 $f(t) = \frac{2t}{1+t^2}$，选 C；
    - Q4：$\vec{a}\cdot\vec{b} = \vec{a}\cdot\vec{c} \iff \vec{a}\cdot(\vec{b}-\vec{c}) = 0$ 不蕴含 $\vec{b}=\vec{c}$，反之显然，故甲是乙的必要不充分条件，选 B；
    - Q5：$\frac{1}{a} < \frac{1}{b} < 0 \implies 0 > a > b$。① $a+b < 0 < ab$ 正确；② $|a| < |b|$ 错误；③ $a < b$ 错误；④ $\frac{b}{a}+\frac{a}{b} > 2$ 正确。共 2 个正确，选 B；
    - Q6：椭圆 $a=4, b=3, c=\sqrt{7}$。直角在焦点处 $|y| = \frac{b^2}{a} = \frac{9}{4}$；直角在 $P$ 处需要 $|y| = \frac{9\sqrt{7}}{7} \approx 3.4 > b = 3$ 不可能。点到 $x$ 轴距离为 $\frac{9}{4}$，选 D；
    - Q7：单调函数在 $[0, 1]$ 上的最值和为 $f(0)+f(1) = 1 + a + \log_a 2 = a \implies \log_a 2 = -1 \implies a = \frac{1}{2}$，选 B；
    - Q8：$a_n = S_n - S_{n-1} = (-bn + a + b)(\frac{1}{2})^{n-1}$，为等差数列与等比数列的积，选 C；
    - Q9：$f'(x) = 3ax^2 + 1$，有极值需导数有两个相异实根且变号，充要条件为 $a < 0$，选 C；
    - Q10：$P = (-1, 0)$；$mx^2+4mx-4 < 0$ 恒成立需 $m=0$ 或 $m<0$ 且 $\Delta = 16m(m+1)<0 \implies m \in (-1, 0]$，故 $Q = (-1, 0]$。关系为 $P \subsetneqq Q$，选 A；
    - Q11：二面角 $80^\circ$，与两平面所成角均为 $30^\circ$ 的直线在内角平分面方向 2 条、外角平分面方向 2 条，共 4 条，选 D；
    - Q12：周期 $T = 15 - 3 = 12 \implies \omega = \frac{\pi}{6}$，振幅 3，中心线 12，初相 0，函数为 $y = 12 + 3\sin\frac{\pi}{6}t$，选 A。
  - Q13–Q16 填空题复算核对：
    - Q13：分布归一化 $\sum_{k=1}^\infty \frac{a}{5^k} = a \frac{1/5}{4/5} = \frac{a}{4} = 1 \implies a = 4$；
    - Q14：10 个球恰好 3 个错放：$\mathrm{C}_{10}^3 \times D_3 = 120 \times 2 = 240$；
    - Q15：子集定义的逻辑否定为“存在 $x \in A$ 使得 $x \notin B$”，真命题序号为 ④；
    - Q16：$s^2 = (16t)^2 + (18-24t)^2$，在 $t=0.5$ 时 $s=10$，相关变化率 $\frac{\mathrm{d}s}{\mathrm{d}t} = \frac{8(16) + 6(-24)}{10} = -1.6\text{ km/h}$（或 $-\frac{8}{5}\text{ km/h}$）。
  - Q17–Q22 解答题复算核对：
    - Q17：化为 $(2\tan\alpha - 1)(3\tan\alpha + 2) = 0$；由 $\alpha \in [\frac{\pi}{2}, \pi]$ 得 $\tan\alpha = -\frac{2}{3}$；$\sin 2\alpha = -\frac{12}{13}, \cos 2\alpha = \frac{5}{13}$；$\sin(2\alpha + \frac{\pi}{3}) = \frac{5\sqrt{3}-12}{26}$；
    - Q18：(1) 建系得 $\vec{D_1E} = (\frac{1}{2}, 1, -1)$，$\vec{AB_1} = (0, 1, 1) \implies \vec{D_1E}\cdot\vec{AB_1} = 0$；$\vec{AF} = (-1, \lambda, 0) \implies \vec{D_1E}\cdot\vec{AF} = -\frac{1}{2} + \lambda = 0 \implies \lambda = \frac{1}{2}$，即点 $F$ 为棱 $CD$ 的中点；(2) 法向量 $\vec{n}_1 = (0, 0, 1)$，$\vec{n}_2 = (2, -2, 1)$，$|\cos| = \frac{1}{3}$，结合几何位置半平面夹角为钝角，大小为 $\arccos(-\frac{1}{3})$；
    - Q19：向量分解 $\vec{BP}\cdot\vec{CQ} = (\vec{BA} - \frac{1}{2}\vec{PQ})\cdot(\vec{CA} + \frac{1}{2}\vec{PQ}) = \frac{1}{2}\vec{PQ}\cdot\vec{BC} - a^2 = a^2(\cos\theta - 1)$；当 $\theta = 0$ 时取最大值 0；
    - Q20：(1) 联立消元得 $(2-k^2)x^2 - 2kx - 2 = 0$，由交于右支得 $\Delta > 0, 2-k^2 < 0, x_1+x_2 > 0$，求得 $k \in (-2, -\sqrt{2})$；(2) 圆过右焦点 $F(\frac{\sqrt{6}}{2}, 0) \iff \vec{FA}\cdot\vec{FB} = 0$，代入韦达定理化简得 $5k^2 + 2\sqrt{6}k - 6 = 0$，解得唯一合格解 $k = \frac{-6-\sqrt{6}}{5} = -\frac{6+\sqrt{6}}{5} \in (-2, -\sqrt{2})$；
    - Q21：不采取措施总费用 120 万元；单独采用乙 90 万元；单独采用甲 85 万元；联合采用甲乙 $45+30 + 400(0.1\times 0.15) = 75 + 6 = 81$ 万元。联合采用甲、乙两种措施使总费用最少，最少总费用为 81 万元；
    - Q22：(1) 取极限 $A = a + \frac{1}{A} \implies A^2 - aA - 1 = 0 \implies A = \frac{a+\sqrt{a^2+4}}{2}$；(2) $b_{n+1} = a - A + \frac{1}{b_n+A} = -\frac{1}{A} + \frac{1}{b_n+A} = -\frac{b_n}{A(b_n+A)}$；(3) 由 $b_1 = -\frac{1}{A}$ 知 $|b_1| \leqslant \frac{1}{2} \iff A \geqslant 2 \iff a \geqslant \frac{3}{2}$；当 $a \geqslant \frac{3}{2}$ 时，$a_n \geqslant a \implies A a_n \geqslant 3 > 2 \implies |b_{n+1}| \leqslant \frac{1}{3}|b_n| \leqslant \frac{1}{2}|b_n|$，由数学归纳法 $|b_n| \leqslant \frac{1}{2^n}$ 恒成立，因此 $a \geqslant \frac{3}{2}$。
  - 全卷 22 题经双角色独立复算全部闭环，无排印阻断，评定为 `eligible_complete`。

## 三、图表清单与矢量重绘规划

- **Q12 表**：港口水深观测数据表格（LaTeX 内用 `booktabs` 纯文本表格排版）；
- **Q18 图**：正方体 $ABCD - A_1B_1C_1D_1$ 空间立体几何、截面及中点结构图（`f2004_hubei_science_q18_cube.tex`）；
- **Q19 图**：直角三角形 $\mathrm{Rt}\triangle ABC$ 示意图（`f2004_hubei_science_q19_triangle.tex`）；
- **Q20 图**：双曲线 $2x^2 - y^2 = 1$ 右支、割线 $AB$、焦点 $F$ 与外接圆几何示意图（`f2004_hubei_science_q20_hyperbola.tex`）。

所有图形统一由 TikZ 纯矢量重绘，绝无位图，存放于 `math-gaokao-latex/2004_湖北卷_理科/figures/`。

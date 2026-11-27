# 2004 辽宁卷：固定来源接收与范围确认报告

日期：2026-11-07

## 一、固定来源信息

- **manifest source**：`src-2323f00197bbd8d5c8353a847fc0e7ccfc52169ca219272ee58990ae4b6ecba3`
- **上游路径**：`普通高考/2004/2004辽宁.pdf`
- **本地只读文件**：`gaokaomath-src/普通高考/2004/2004辽宁.pdf`
- **文件指纹**：
  - SHA-256：`be2accb36a086126db90ee7c5a217e08e55429053a4167df1ad58bbfb213de46`
  - 文件大小：512,650 字节
  - 页数：2 页（A3 横向矢量排印，原卷印刷页码 180、181）
- **题签原文**：“2004 普通高等学校招生考试 (辽宁卷)”
- **来源性质**：纯试题卷面排印件，PDF 内无官方答案、解析或评分标准。全卷 22 题均由本库编者独立推导、复算与交叉核验。

## 二、试卷结构与题量核验

- **第 1 页（印刷页 180）**：
  - 一、选择题（Q1–Q12，共 12 题，每题 5 分，共 60 分）；
  - 二、填空题（Q13–Q16，共 4 题，每题 4 分，共 16 分）；
  - 三、解答题（Q17，共 1 题，四棱锥底面菱形与二面角平面角余弦值求解，满分 12 分）。
- **第 2 页（印刷页 181）**：
  - 三、解答题（续，Q18–Q22，共 5 题，满分 62 分）：
    - Q18（12 分）：含参绝对值不等式解集与三角函数零点交集元素计数；
    - Q19（12 分）：椭圆旋转弦中点轨迹方程及到定点距离的最值；
    - Q20（12 分）：农场与工厂资源占用索赔的最优化建模与导数极值；
    - Q21（12 分）：二次函数上下界确定系数与非线性递推数列不等式数学归纳法证明；
    - Q22（14 分）：对数指数复合函数反函数、导数及参数绝对值不等式恒成立范围。
- **总题量**：22 题（选择 12 + 填空 4 + 解答 6，全卷满分 150 分）。
- **科类说明**：2004 年辽宁省高考数学科目实行全省统一卷（不分文理科），本库按 `track=none` 登记，试卷 ID 为 `gk-2004-regular-liaoning`，工程目录为 `2004_辽宁卷`。
- **排印质量评估与逐题复算核验**：
  - 卷面排印清晰规范，公式完整，题号、选项、分值完备，无漏印或模糊阻断；
  - Q1–Q12 选择题复算核对：
    - Q1：$\cos\theta > 0, \sin 2\theta = 2\sin\theta\cos\theta < 0 \implies \sin\theta < 0$，角 $\theta$ 为第四象限角，选 D；
    - Q2：$0 < a < 1 \implies 1+a < 1+\frac{1}{a}$，底数 $a\in(0,1)$ 的对数函数与指数函数均单调递减，②与④成立，选 D；
    - Q3：两平行平面内直线必无公共点，反之两直线平行或异面时两平面亦可相交，为必要不充分条件，选 B；
    - Q4：$\frac{1-z}{1+z}=\mathrm{i} \implies z=-\mathrm{i} \implies |1+z|=|1-\mathrm{i}|=\sqrt{2}$，选 C；
    - Q5：独立事件恰有一人解决，概率为 $p_1(1-p_2)+p_2(1-p_1)$，选 B；
    - Q6：$\vec{PA}\cdot\vec{PB}=x^2-x-6+y^2=x^2 \implies y^2=x+6$，轨迹为抛物线，选 D；
    - Q7：$f(x)=-\cos\pi x - 1$，周期 $T=2$，为偶函数，选 B；
    - Q8：全概率和为 1，$\sum_{k=1}^9 \frac{2}{3^k} = 1-\frac{1}{3^9} \implies m = \frac{1}{3^9}$，选 C；
    - Q9：双曲线左支 $x^2-y^2=1$ ($x \leqslant -1$)，纵坐标 $y=\frac{1}{2}$ 时 $x^2=\frac{5}{4}$，到原点距离为 $\sqrt{\frac{5}{4}+\frac{1}{4}}=\frac{\sqrt{6}}{2}$，选 A；
    - Q10：球内接正方形边长 3，小圆半径 $r=\frac{3\sqrt{2}}{2}$，球心距 $d=\frac{1}{2}R \implies \frac{3}{4}R^2=r^2=\frac{9}{2} \implies R=\sqrt{6}$，体积 $V=8\sqrt{6}\pi$，选 A；
    - Q11：$\frac{T}{4}=\pi \implies \omega=\frac{1}{2}$，峰值点 $\frac{1}{2}\cdot\frac{2\pi}{3}+\varphi=\frac{\pi}{2} \implies \varphi=\frac{\pi}{6}$，选 C；
    - Q12：前排中间 3 座不可坐，前排可用 8 座，后排可用 12 座，共 20 座。总排法 $A_{20}^2=380$；前排相邻 6 对，后排相邻 11 对，相邻排法 $(6+11)\times 2=34$ 种。不左右相邻排法 $380-34=346$ 种，选 B。
  - Q13–Q16 填空题复算核对：
    - Q13：圆心 $(-2,1)$，半径 $\sqrt{2}$，点 $P(-1,0)$ 在圆上，切线方程 $x-y+1=0$，$y$ 轴截距为 $1$；
    - Q14：$\lim_{x\to\pi}\frac{(x-\pi)\cos x}{\sqrt{x}-\sqrt{\pi}}=\lim_{x\to\pi}(\sqrt{x}+\sqrt{\pi})\cos x = -2\sqrt{\pi}$；
    - Q15：侧棱 $AA_1$ 平行于截面 $B_1D_1DB$，$A_1$ 在底面正方形投影恰为底面中心 $O$，截面垂直于对角面 $A_1AC$，距离为 $AO\sin 45^\circ = a$；
    - Q16：5 个 0 和 5 个 1 摸 5 球，和小于 2 或大于 3 对应取到 1 的个数为 0, 1, 4, 5，概率 $\frac{\binom{5}{0}\binom{5}{5}+\binom{5}{1}\binom{5}{4}+\binom{5}{4}\binom{5}{1}+\binom{5}{5}\binom{5}{0}}{\binom{10}{5}} = \frac{52}{252} = \frac{13}{63}$。
  - Q17–Q22 解答题复算核对：
    - Q17：菱形底面中 $\triangle DAB$ 为等边三角形，$DE\perp AB$；$PD\perp$ 底面 $\implies AB\perp$ 面 $PED$，故面 $PED\perp$ 面 $PAB$；二面角平面角为 $\angle PEF$，由两角差公式与余弦定理双重验算得 $\cos\angle PEF = \frac{5\sqrt{7}}{14}$；
    - Q18：(1) $a>1$ 解集为 $\mathbf{R}$；$a=1$ 解集为 $\{x\in\mathbf{R}\mid x\neq 1\}$；$a<1$ 解集为 $\{x\mid x<a\text{ 或 }x>2-a\}$。(2) $B=\mathbf{Z}$，$\complement_U A = [a, 2-a]$，含 3 个整数必须恰为 $0, 1, 2 \implies -1 < a \leqslant 0$；
    - Q19：(1) 点差法结合中点坐标得 $4x^2+y(y-1)=0$，即 $4x^2+\left(y-\frac{1}{2}\right)^2=\frac{1}{4}$；(2) 椭圆三角参数化后化为二次函数求极值，最小值为 $\frac{1}{4}$，最大值为 $\frac{\sqrt{21}}{6}$；
    - Q20：(1) $w(t)=2000\sqrt{t}-st$ ($t\geqslant 0$)，求导得最大利润产量 $t=\frac{10^6}{s^2}$ 吨；(2) 甲方净收入 $z(s)=\frac{10^6}{s}-\frac{2\times 10^9}{s^4}$，求导极值点 $s^3=8000 \implies s=20$ 元；
    - Q21：(1) 顶点极值 $\frac{a^2}{6}\leqslant \frac{1}{6}\implies a\leqslant 1$，端点 $f(1/2)=\frac{a}{2}-\frac{3}{8}\geqslant \frac{1}{8}\implies a\geqslant 1$，唯一解 $a=1$；(2) 数学归纳法与单调性结合，以及倒数递推放缩 $\frac{1}{a_{k+1}}-\frac{1}{a_k}>\frac{3}{2}$ 严谨证明 $a_n < \frac{1}{n+1}$；
    - Q22：(1) $f^{-1}(x)=\ln(\mathrm{e}^x-a)$ ($x>\ln a$)，$f'(x)=\frac{\mathrm{e}^x}{\mathrm{e}^x+a}$；(2) 不等式等价于 $\ln\frac{\mathrm{e}^x(\mathrm{e}^x-a)}{\mathrm{e}^x+a} < m < \ln\left(\mathrm{e}^x-\frac{a^2}{\mathrm{e}^x}\right)$，两端函数在 $[\ln(3a), \ln(4a)]$ 均严格单调递增，取最值得 $m\in\left(\ln\left(\frac{12}{5}a\right), \ln\left(\frac{8}{3}a\right)\right)$。
  - 全卷 22 题经独立复算全部闭环，无排印阻断，评定为 `eligible_complete`。

## 三、图表清单与矢量重绘规划

- **Q11 图**：三角函数 $f(x)=\sin(\omega x+\varphi)$ 局部波形图（`f2004_liaoning_q11_sine.tex`）。
- **Q15 图**：底面为正方形的斜四棱柱与对角面截面图（`f2004_liaoning_q15_prism.tex`）。
- **Q17 图**：底面为菱形的四棱锥空间线面垂直与二面角图（`f2004_liaoning_q17_pyramid.tex`）。

所有图形统一由 TikZ 纯矢量重绘，绝无位图，存放于 `math-gaokao-latex/2004_辽宁卷/figures/`。

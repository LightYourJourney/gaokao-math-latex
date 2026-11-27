# 1995 全国卷（文）第 1–26 题 · 独立求解（solverA）

> 依据：`1995_全国卷_文科/题面转录草稿.md` 与 `figures/` 下四幅矢量示意图。来源页未载答案，本稿为独立推导。记法：$\complement_I M$ 表示 $M$ 在全集 $I$ 中的补集。

## 第 1 题

**答案：** B

解析：在全集 $I$ 内取 $M$ 的补集：$\complement_I M=I\setminus M=\{-3,-4\}$；再与 $N=\{0,-3,-4\}$ 取交集，得 $\{-3,-4\}$。

验算：逐元素核对：$0\in M$ 排除；$-1,-2\in M$ 排除；$-3\notin M$ 且 $-3\in N$；$-4\notin M$ 且 $-4\in N$。结果 $\{-3,-4\}$ 与 (B) 一致，其余选项或含 $M$ 中的元素 $\{0\},\{-1,-2\}$，或为空集。

## 第 2 题

**答案：** D

解析：$y=\dfrac{1}{x+1}$ 的定义域为 $x\ne-1$，竖直渐近线 $x=-1$，水平渐近线 $y=0$；且 $x>-1$ 时 $y>0$（右支在 $x$ 轴上方），$x<-1$ 时 $y<0$（左支在 $x$ 轴下方）。逐图核对：(A) 渐近线为 $x=1$；(B) 渐近线为 $x=-1$ 但两支符号与 $y=\dfrac1{x+1}$ 相反（右支在下、左支在上）；(C) 渐近线为 $x=1$ 且两支符号相反；(D) 渐近线 $x=-1$，右支在上、左支在下，与所给函数一致。

验算：取 $x=0$ 得 $y=1>0$，取 $x=-2$ 得 $y=-1<0$，只有 (D) 同时满足"渐近线 $x=-1$"与"左支在下、右支在上"。

## 第 3 题

**答案：** C

解析：$4\sin u+3\cos u=5\sin(u+\varphi)$（$\cos\varphi=\tfrac45,\ \sin\varphi=\tfrac35$）。取 $u=3x+\dfrac\pi4$，则 $y=5\sin\!\left(3x+\dfrac\pi4+\varphi\right)$，其最小正周期为 $\dfrac{2\pi}{3}$。

验算：振幅 $\sqrt{4^2+3^2}=5$；$x$ 增加 $\dfrac{2\pi}{3}$ 时 $3x$ 恰增加 $2\pi$，函数值复原；若周期更小，则 $3x$ 的增量小于 $2\pi$ 而正弦不会对一切 $x$ 复原，故最小正周期为 $\dfrac{2\pi}{3}$，与 (C) 一致。

## 第 4 题

**答案：** B

解析：设正方体棱长为 $s$，全面积 $6s^2=a^2$，故 $s=\dfrac{a}{\sqrt6}$。正方体的体对角线为其外接球直径，长 $s\sqrt3=\dfrac{a}{\sqrt2}$，于是球半径 $R=\dfrac{a}{2\sqrt2}$。球表面积 $S=4\pi R^2=4\pi\cdot\dfrac{a^2}{8}=\dfrac{\pi a^2}{2}$。

验算：取 $a^2=6$（此时 $s=1$），体对角线 $\sqrt3$，球半径 $\dfrac{\sqrt3}{2}$，球表面积 $4\pi\cdot\dfrac34=3\pi$；代入公式 $\dfrac{\pi a^2}{2}=\dfrac{6\pi}{2}=3\pi$，一致。

## 第 5 题

**答案：** D

解析：由图中方位：$l_1$ 自左上向右下倾斜，故 $k_1<0$；$l_2$ 自左下向右上且较陡，$k_2>0$ 且较大；$l_3$ 也上升但较平缓，$k_3>0$ 且 $k_3<k_2$。所以 $k_1<k_3<k_2$，选 (D)。

验算：按重绘图的取样点估算，$k_1\approx-0.68$，$k_3\approx0.49$，$k_2\approx1.61$，满足 $k_1<k_3<k_2$。

源疑点：三条直线与标签 $l_1,l_2,l_3$ 的对应关系及斜率次序只能由示意图给出（重绘说明"仅表达斜率的正负与大小次序，不表示精确坐标"），本解据此判定 (D)；若原页图象次序与重绘不符，结论需重判。

## 第 6 题

**答案：** C

解析：$3x^2-y^2=3$ 化为 $\dfrac{x^2}{1}-\dfrac{y^2}{3}=1$，即 $a=1,\ b=\sqrt3$，渐近线为 $y=\pm\dfrac{b}{a}x=\pm\sqrt3\,x$。

验算：由方程解出 $y^2=3x^2-3$，当 $|x|\to\infty$ 时 $\dfrac{y}{x}\to\pm\sqrt3$；写成 $y=\pm\sqrt3x$ 后代入左边得 $3x^2-3x^2=0$，为低阶差，符合渐近线定义。与 (C) 一致。

## 第 7 题

**答案：** A

解析：$\sin x\le\cos x\iff \cos x-\sin x\ge0\iff \sqrt2\cos\!\left(x+\dfrac\pi4\right)\ge0$，即 $x+\dfrac\pi4\in\left[-\dfrac\pi2+2k\pi,\ \dfrac\pi2+2k\pi\right]$，故 $x\in\left[-\dfrac{3\pi}{4}+2k\pi,\ \dfrac\pi4+2k\pi\right]$。取 $k=0$ 得选项 (A)。

验算：端点处 $\sin x=\cos x$；区间中点 $x=-\dfrac\pi4$ 有 $\sin=-\dfrac{\sqrt2}{2}\le\cos=\dfrac{\sqrt2}{2}$，成立。(B) 含 $x=\dfrac\pi2$（$\sin=1>\cos=0$），(C)、(D) 也含 $x=\dfrac\pi2$，均不成立。

## 第 8 题

**答案：** C

解析：圆 $x^2+y^2-2x=0$ 即 $(x-1)^2+y^2=1$，圆心 $(1,0)$、半径 $1$；圆 $x^2+y^2+4y=0$ 即 $x^2+(y+2)^2=4$，圆心 $(0,-2)$、半径 $2$。圆心距 $d=\sqrt{1^2+2^2}=\sqrt5$，满足 $|2-1|=1<\sqrt5<3=1+2$，故两圆相交。

验算：两式相减得 $-2x-4y=0$，即 $x=-2y$；代入第一圆：$4y^2+y^2+4y=0\Rightarrow y(5y+4)=0$，得交点 $(0,0)$ 与 $\left(\dfrac85,-\dfrac45\right)$，两个不同实交点，确为相交。

## 第 9 题

**答案：** A

解析：$\sin^4\theta+\cos^4\theta=1-2\sin^2\theta\cos^2\theta=1-\dfrac12\sin^22\theta=\dfrac59$，故 $\sin^22\theta=\dfrac89$，$\sin2\theta=\pm\dfrac{2\sqrt2}{3}$。$\theta$ 为第三象限角时 $\sin\theta<0,\ \cos\theta<0$，故 $\sin2\theta=2\sin\theta\cos\theta>0$，取正值 $\dfrac{2\sqrt2}{3}$。

验算：代回 $1-\dfrac12\cdot\dfrac89=1-\dfrac49=\dfrac59$，与题设相符；符号由"第三象限 $\Rightarrow$ 正弦、余弦同号 $\Rightarrow$ 二倍角正弦为正"确定，与 (A) 一致。

## 第 10 题

**答案：** A

解析：设棱长 $1$，取坐标 $A(0,0,0),\ B(1,0,0),\ D(0,1,0),\ A_1(0,0,1),\ B_1(1,0,1),\ D_1(0,1,1),\ C_1(1,1,1)$。由 $B_1E_1=\dfrac{A_1B_1}{4}$ 得 $E_1=\left(\dfrac34,0,1\right)$；由 $D_1F_1=\dfrac{D_1C_1}{4}$ 得 $F_1=\left(\dfrac14,1,1\right)$。于是
$$\overrightarrow{BE_1}=\left(-\dfrac14,0,1\right),\qquad \overrightarrow{DF_1}=\left(\dfrac14,0,1\right).$$
点积 $=-\dfrac1{16}+1=\dfrac{15}{16}$，两向量模均为 $\sqrt{\dfrac1{16}+1}=\dfrac{\sqrt{17}}{4}$，故夹角余弦为 $\dfrac{15/16}{17/16}=\dfrac{15}{17}$。

验算：$|\overrightarrow{BE_1}|=|\overrightarrow{DF_1}|=\dfrac{\sqrt{17}}{4}\approx1.031$，点积 $\approx0.9375$，余弦 $\approx0.882$，即 $\dfrac{15}{17}\approx0.882$，与 (A) 一致。

源疑点：文字只给出 $B_1E_1=D_1F_1=\dfrac{A_1B_1}{4}$，未明写 $E_1\in A_1B_1$、$F_1\in D_1C_1$ 这两条棱；这一归属来自示意图。本解按图取点，若所取棱不同答案会不同。

## 第 11 题

**答案：** B

解析：令 $u=2-x$，它在 $\mathbb R$ 上关于 $x$ 递减。复合函数 $y=\log_a u$ 关于 $x$ 递增，等价于 $\log_a u$ 关于 $u$ 递减，故 $0<a<1$，即 $a\in(0,1)$。

验算：取 $a=\dfrac12$（$a\in(0,1)$）：$x=0$ 得 $y=-1$，$x=1$ 得 $y=0$，递增，合题；取 $a=2$（$a>1$）：$x=0$ 得 $y=1$，$x=1$ 得 $y=0$，递减，不合题。故 (B)。

## 第 12 题

**答案：** D

解析：$(1-x^3)(1+x)^{10}$ 中 $x^5$ 的系数为 $(1+x)^{10}$ 中 $x^5$ 的系数减去 $x^2$ 的系数：
$$\binom{10}{5}-\binom{10}{2}=252-45=207.$$

验算：$1\cdot\binom{10}{5}x^5=252x^5$；$-x^3\cdot\binom{10}{2}x^2=-45x^5$；合并得 $207x^5$，与 (D) 一致。

## 第 13 题

**答案：** D

解析：
- ① $\alpha\parallel\beta$ 且 $l\perp\alpha$ 得 $l\perp\beta$；又 $m\subset\beta$，故 $l\perp m$。正确。
- ② 反例：取 $\alpha$ 为水平面、$l$ 为竖直直线，$\beta$ 为竖直平面，$m$ 为 $\beta$ 内一条水平直线，则 $l\perp m$ 而不平行。错误。
- ③ $l\parallel m$ 且 $l\perp\alpha$ 得 $m\perp\alpha$；又 $m\subset\beta$，故 $\beta\perp\alpha$。正确。
- ④ 反例：$l$ 为竖直直线，$m$ 为 $\beta$ 内一条与 $l$ 垂直的水平直线，此时 $\beta$ 可绕 $m$ 转动而不必与 $\alpha$ 平行。错误。

故正确的为①与③，选 (D)。

验算：用正方体模型逐条检验：①、③在任意摆放的底面/侧面/竖直棱中都成立；②在 $m$ 取 $\beta$ 内水平方向时立即失效；④在 $\beta$ 绕 $m$ 旋转时失效。与 (D) 一致。

## 第 14 题

**答案：** C

解析：等差数列中 $S_{2n-1}=(2n-1)a_n$，$T_{2n-1}=(2n-1)b_n$，故
$$\frac{a_n}{b_n}=\frac{S_{2n-1}}{T_{2n-1}}=\frac{2(2n-1)}{3(2n-1)+1}=\frac{4n-2}{6n-2}\ \longrightarrow\ \frac23\quad(n\to\infty).$$

验算：$n=1$ 时 $\dfrac{a_1}{b_1}=\dfrac24=\dfrac12$，公式给出 $\dfrac{4-2}{6-2}=\dfrac12$，吻合；$n=10$ 时公式值 $\dfrac{38}{58}\approx0.655$，$n=1000$ 时 $\approx0.6666$，单调趋近 $\dfrac23$，与 (C) 一致。

## 第 15 题

**答案：** A

解析：三位数为偶数须个位为 $2$ 或 $4$，共 $2$ 种选法；百位、十位从剩余 $4$ 个数字中任取两个排列，有 $4\times3=12$ 种。故共 $2\times12=24$ 个。

验算：无重复数字的三位数共 $5\times4\times3=60$ 个；五个数字中偶数占 $\dfrac25$，按对称性偶数个数为 $60\times\dfrac25=24$，与 (A) 一致。

## 第 16 题

**答案：** $x=3$

解析：定义域要求 $x+1>0$，即 $x>-1$。此时
$$\log_2(x+1)^2=\log_2\bigl[(x+1)^2\bigr]=2\log_2(x+1),\qquad \log_4(x+1)=\frac12\log_2(x+1).$$
令 $y=\log_2(x+1)$，方程化为 $2y+\dfrac y2=5$，得 $y=2$，于是 $x+1=4$，$x=3$。

验算：$\log_2(4^2)+\log_4 4=\log_2 16+1=4+1=5$，成立。

源疑点：转录 `\log_2(x+1)^2` 未加括号，指数作用范围存在排版歧义。若读作 $\bigl[\log_2(x+1)\bigr]^2$，则方程为 $y^2+\dfrac y2=5$，即 $2y^2+y-10=0$，得 $y=2$ 或 $y=-\dfrac52$，对应 $x=3$ 或 $x=2^{-5/2}-1\approx-0.823$，有两个解。按"指数属于 $(x+1)$"的通行读法解唯一，取 $x=3$。

## 第 17 题

**答案：** $\dfrac{7\sqrt3}{32}$

解析：设球半径为 $R$。下底面所在平面过球心，故下底面圆是大圆，半径 $R$。设上底面半径为 $r$、圆台高为 $h$，则上底面圆在球上：
$$r^2+h^2=R^2.$$
母线与底面所成角为 $\dfrac\pi3$，其水平投影长为 $R-r$，故
$$h=(R-r)\tan\frac\pi3=\sqrt3\,(R-r).$$
联立得 $r^2+3(R-r)^2=R^2$，即 $2r^2-3Rr+R^2=0$，解得 $r=\dfrac R2$（$r=R$ 使 $h=0$，退化舍去），从而 $h=\dfrac{\sqrt3}{2}R$。
圆台体积
$$V_{\text{台}}=\frac{\pi h}{3}(R^2+Rr+r^2)=\frac{\pi}{3}\cdot\frac{\sqrt3 R}{2}\cdot\frac{7R^2}{4}=\frac{7\sqrt3}{24}\pi R^3,$$
球体积 $V_{\text{球}}=\dfrac43\pi R^3$，故体积比为
$$\frac{V_{\text{台}}}{V_{\text{球}}}=\frac{7\sqrt3/24}{4/3}=\frac{7\sqrt3}{32}.$$

验算：取 $R=1$，则 $r=\dfrac12$、$h=\dfrac{\sqrt3}{2}\approx0.866$，$V_{\text{台}}=\dfrac{\pi\cdot0.866}{3}(1+0.5+0.25)\approx1.587$，$V_{\text{球}}\approx4.189$，比值 $\approx0.3789$，而 $\dfrac{7\sqrt3}{32}\approx0.3789$，一致。

## 第 18 题

**答案：** $\sqrt3$

解析：由和差化积
$$\cos x+\cos\left(x+\frac\pi3\right)=2\cos\left(x+\frac\pi6\right)\cos\frac\pi6=\sqrt3\cos\left(x+\frac\pi6\right),$$
故最大值为 $\sqrt3$（当 $x+\dfrac\pi6=2k\pi$ 时取到）。

验算：取 $x=-\dfrac\pi6$，得 $\cos\left(-\dfrac\pi6\right)+\cos\dfrac\pi6=\dfrac{\sqrt3}{2}+\dfrac{\sqrt3}{2}=\sqrt3$；又 $\sqrt3\cos\left(x+\dfrac\pi6\right)\le\sqrt3$，故确为最大值。

## 第 19 题

**答案：** $4$

解析：抛物线 $y^2=4(x+1)$ 的顶点为 $(-1,0)$，由 $y^2=4a(x+1)$ 得 $a=1$，焦点为 $(-1+1,0)=(0,0)$。过焦点且与 $x$ 轴垂直的直线为 $x=0$。代入抛物线：$y^2=4$，即 $y=\pm2$。所截线段端点为 $(0,2),(0,-2)$，长为 $4$。

验算：准线为 $x=-2$；交点 $(0,2)$ 到焦点 $(0,0)$ 的距离为 $2$，到准线的距离也为 $2$，满足抛物线定义，交点位置正确，弦长为 $2-(-2)=4$。

## 第 20 题

**答案：** $144$

解析：恰有一个空盒，先选出空盒，有 $4$ 种；再把 $4$ 个不同的小球放入其余 $3$ 个盒且每盒不空，即把球分成 $2,1,1$ 三组：选 $2$ 球成组有 $\binom42=6$ 种，三组分配到 $3$ 个盒有 $3!=6$ 种。故总数为
$$4\times\binom42\times3!=4\times6\times6=144.$$

验算：用容斥计算"4 球入 3 个指定盒且无空盒"的放法：$3^4-\binom31 2^4+\binom32 1^4=81-48+3=36$，再乘空盒的选择 $4$，得 $144$，一致。

## 第 21 题

**答案：** $x=2$

解析：令 $t=3^x>0$，则 $3^{x+2}=9t$，$3^{2-x}=\dfrac9t$。方程化为
$$9t-\frac9t=80\iff 9t^2-80t-9=0,$$
解得 $t=\dfrac{80\pm\sqrt{6400+324}}{18}=\dfrac{80\pm82}{18}$，即 $t=9$ 或 $t=-\dfrac19$（负值舍去）。由 $3^x=9$ 得 $x=2$。

验算：$3^{2+2}-3^{2-2}=81-1=80$，成立。

## 第 22 题

**答案：** 模为 $-2\cos\dfrac\theta2\left(=2\left|\cos\dfrac\theta2\right|\right)$；辐角主值为 $\dfrac{3\theta}{2}-\pi$，一般辐角为 $\dfrac{3\theta}{2}-\pi+2k\pi\ (k\in\mathbb Z)$。

解析：由和差化积
$$z^2+z=(\cos2\theta+\cos\theta)+i(\sin2\theta+\sin\theta)=2\cos\frac\theta2\left(\cos\frac{3\theta}{2}+i\sin\frac{3\theta}{2}\right).$$
因 $\theta\in(\pi,2\pi)$，有 $\dfrac\theta2\in\left(\dfrac\pi2,\pi\right)$，故 $\cos\dfrac\theta2<0$。于是
$$|z^2+z|=\left|2\cos\frac\theta2\right|=-2\cos\frac\theta2,$$
且 $z^2+z$ 的方向与 $e^{i3\theta/2}$ 相反，故
$$\arg(z^2+z)=\frac{3\theta}{2}+\pi+2k\pi=\frac{3\theta}{2}-\pi+2k\pi\quad(k\in\mathbb Z).$$
又 $\dfrac{3\theta}{2}-\pi\in\left(\dfrac\pi2,2\pi\right)\subset[0,2\pi)$，可作为辐角主值。

验算：取 $\theta=\dfrac{3\pi}{2}$，则 $z=-i$，$z^2+z=-1-i$，模为 $\sqrt2$，辐角为 $\dfrac{5\pi}{4}$。公式给出模 $-2\cos\dfrac{3\pi}{4}=\sqrt2$，辐角 $\dfrac{9\pi}{4}-\pi=\dfrac{5\pi}{4}$，一致。再取 $\theta\to2\pi^-$，模 $\to2$、辐角 $\to2\pi\equiv0$，与 $z^2+z\to2$ 相符。

## 第 23 题

**答案：** 不等式成立（证明见解析）

解析：设 $\{a_n\}$ 首项 $a_1>0$、公比 $q>0$，则各项为正，$S_n>0$。因 $\log_{0.5}$ 在 $(0,+\infty)$ 上递减，原不等式等价于证明
$$S_nS_{n+2}<S_{n+1}^2.$$
计算
$$S_{n+1}^2-S_nS_{n+2}=S_{n+1}^2-S_n(S_{n+1}+a_{n+2})=a_{n+1}S_{n+1}-a_{n+2}S_n.$$
由 $a_{n+2}=qa_{n+1}$，得
$$S_{n+1}^2-S_nS_{n+2}=a_{n+1}(S_{n+1}-qS_n).$$
又 $S_{n+1}=a_1+qS_n$，故 $S_{n+1}-qS_n=a_1$，从而
$$S_{n+1}^2-S_nS_{n+2}=a_1a_{n+1}>0.$$
于是 $S_{n+1}>\sqrt{S_nS_{n+2}}$，由 $\log_{0.5}$ 递减得
$$\log_{0.5}S_{n+1}<\log_{0.5}\sqrt{S_nS_{n+2}}=\frac{\log_{0.5}S_n+\log_{0.5}S_{n+2}}{2}.$$

验算：取 $a_n=2^{n-1}$，则 $S_1=1,S_2=3,S_3=7$，有 $S_2^2-S_1S_3=9-7=2=a_1a_2$，与恒等式一致；再代入数值：$\dfrac{\log_{0.5}1+\log_{0.5}7}{2}\approx-1.404$，$\log_{0.5}3\approx-1.585$，左边大于右边，不等式成立（$q=1$ 的情形 $S_n=na$ 同样由 $a_1a_{n+1}=a^2>0$ 覆盖）。

## 第 24 题

### （1）

**答案：** $AF\perp DB$ 成立

解析：$AB$ 为底面圆直径、$E$ 在底面圆周上，故 $BE\perp AE$（直径所对圆周角为直角）。$AD$ 为母线，垂直于底面，故 $AD\perp BE$。$AE$ 与 $AD$ 是平面 $ADE$ 内两条相交直线，于是 $BE\perp$ 平面 $ADE$；又 $AF\subset$ 平面 $ADE$，故 $BE\perp AF$。题设 $AF\perp DE$，而 $BE$ 与 $DE$ 是平面 $BDE$ 内两条相交直线，故 $AF\perp$ 平面 $BDE$。因 $DB\subset$ 平面 $BDE$，得 $AF\perp DB$。

验算：取底面半径 $1$、高 $2$ 建立坐标：$A(-1,0,0),\ B(1,0,0),\ D(-1,0,2),\ E(\cos\varphi,\sin\varphi,0)$。则 $\overrightarrow{AE}\cdot\overrightarrow{BE}=(\cos\varphi+1)(\cos\varphi-1)+\sin^2\varphi=0$，$\overrightarrow{AD}=(0,0,2)\perp\overrightarrow{BE}$，前提成立。取 $\varphi=\dfrac\pi2$，$\overrightarrow{ED}=(-1,-1,2)$，$\overrightarrow{BE}=(-1,1,0)$，$AF$ 的方向平行于 $\overrightarrow{ED}\times\overrightarrow{BE}=(-2,-2,-2)$，而 $\overrightarrow{DB}=(2,0,-2)$，点积 $-4+0+4=0$，即 $AF\perp DB$，结论成立。

### （2）

**答案：** 点 $E$ 到截面 $ABCD$ 的距离等于圆柱底面半径 $r$（即轴截面边长 $AB$ 的一半，也等于圆柱高的一半）

解析：设底面半径为 $r$，圆柱高为 $h$。轴截面 $ABCD$ 是正方形，其一边 $AB$ 是底面直径 $2r$，另一边 $AD=h$，故 $h=2r$。圆柱体积 $V_{\text{柱}}=\pi r^2h=2\pi r^3$。

设 $E$ 到底面内直径 $AB$ 所在直线的距离为 $d$，则 $S_{\triangle ABE}=\dfrac12\cdot 2r\cdot d=rd$。点 $D$ 在 $A$ 的正上方，到平面 $ABE$（即底面）的距离为 $h=2r$，故三棱锥体积
$$V_{D-ABE}=\frac13\cdot rd\cdot 2r=\frac23r^2d.$$
由题意
$$\frac{V_{\text{柱}}}{V_{D-ABE}}=\frac{2\pi r^3}{\frac23r^2d}=\frac{3\pi r}{d}=3\pi,$$
得 $d=r$。截面 $ABCD$ 垂直于底面且与底面交于直线 $AB$，故 $E$ 到截面 $ABCD$ 的距离等于 $E$ 到直线 $AB$ 的距离 $d$，即距离为 $r$。

验算：取 $r=1,\ h=2,\ d=1$，$V_{\text{柱}}=2\pi$，$V_{D-ABE}=\dfrac13\cdot1\cdot2=\dfrac23$，比值 $\dfrac{2\pi}{2/3}=3\pi$，符合题设。几何上底面圆上点到直径的最大距离恰为 $r$（$E$ 为半圆中点时取到），解 $d=r$ 不越界。

源疑点：题面未另给长度标度，所得距离只能以圆柱自身尺寸（底面半径）表示，无法化为独立数值；这不影响推导与判卷，但若命题意图是数值答案，则转录可能遗漏了条件。

## 第 25 题

### （1）

**答案：** $x=8+\dfrac{2\sqrt{50-t^2}-4t}{5}$，定义域为 $t\in[0,\sqrt{10}]$

解析：由 $P=Q$ 得
$$1000(x+t-8)=500\sqrt{40-(x-8)^2}\iff 2(x+t-8)=\sqrt{40-(x-8)^2}.$$
两边非负，平方不失解。令 $u=x-8\in[0,6]$，得
$$4(u+t)^2=40-u^2\iff 5u^2+8tu+4t^2-40=0,$$
解得
$$u=\frac{-8t\pm\sqrt{64t^2-20(4t^2-40)}}{10}=\frac{-4t\pm2\sqrt{50-t^2}}{5}.$$
因 $u\ge0$，只取加号：$u=\dfrac{2\sqrt{50-t^2}-4t}{5}$。其有意义的条件为 $50-t^2\ge0$ 且 $u\ge0$；后者等价于 $\sqrt{50-t^2}\ge2t\iff 50-t^2\ge4t^2\iff t^2\le10$。综上 $t\in[0,\sqrt{10}]$，且此时 $x=8+u\in[8,\,8+2\sqrt2]\subset[8,14]$。故
$$x=8+\frac{2\sqrt{50-t^2}-4t}{5},\qquad t\in[0,\sqrt{10}].$$

验算：$t=0$ 时 $x=8+2\sqrt2$，代入 $2(x-8)=4\sqrt2=\sqrt{40-8}=\sqrt{32}$，成立；$t=\sqrt{10}$ 时 $x=8$，代入 $2\sqrt{10}=\sqrt{40}$，成立；$t=2$ 时 $x\approx9.113$，$P=1000(x+t-8)\approx3112.9$，$Q=500\sqrt{40-(x-8)^2}\approx3112.9$，$P=Q$ 成立。

### （2）

**答案：** 政府补贴至少为每千克 $1$ 元

解析：由（1），
$$x(t)=8+\frac{2\sqrt{50-t^2}-4t}{5},\qquad x'(t)=\frac25\cdot\frac{-t}{\sqrt{50-t^2}}-\frac45<0,$$
故 $x$ 关于 $t$ 严格递减。令 $x=10$，即 $u=2$：由 $2(2+t)=\sqrt{40-4}=6$ 得 $t=1$。因此市场平衡价格不高于 $10$ 元/千克等价于 $t\ge1$，最小补贴为 $1$ 元/千克。

验算：$t=1$ 时 $x=8+\dfrac{2\sqrt{49}-4}{5}=8+2=10$，此时 $P=1000(10+1-8)=3000$，$Q=500\sqrt{40-4}=3000$，$P=Q$ 且恰为 $10$ 元；取 $t=0.5$，$x=8+\dfrac{\sqrt{199}-2}{5}\approx10.42>10$，不满足要求。故最小值为 $1$。

## 第 26 题

**答案：** 轨迹方程为 $2x^2+3y^2=4x$，即 $\dfrac{(x-1)^2}{1}+\dfrac{y^2}{2/3}=1$，其中 $0<x\le2$；轨迹是椭圆（中心 $(1,0)$，长轴在 $x$ 轴上，长半轴 $1$，短半轴 $\dfrac{\sqrt6}{3}$），去掉原点 $(0,0)$。

解析：设 $P(12,m)$（$m\in\mathbb R$）。射线 $OP$ 上的点可写成 $\lambda(12,m)\ (\lambda\ge0)$。设 $R$ 对应参数 $\lambda$，代入椭圆：
$$\frac{(12\lambda)^2}{24}+\frac{(m\lambda)^2}{16}=1\iff \lambda^2\left(6+\frac{m^2}{16}\right)=1,$$
故 $|OR|^2=\lambda^2|OP|^2$。设 $Q=\mu(12,m)\ (\mu>0)$，由 $|OQ|\cdot|OP|=|OR|^2$ 得
$$\mu|OP|^2=\lambda^2|OP|^2\iff \mu=\lambda^2=\frac{1}{6+m^2/16}=\frac{16}{96+m^2}.$$
（此时 $0<\mu\le\dfrac16<1$，$Q$ 确实在线段 $OP$ 上。）于是
$$x=12\mu=\frac{192}{96+m^2},\qquad y=m\mu=\frac{16m}{96+m^2}.$$
由 $y=\dfrac{mx}{12}$ 得 $m=\dfrac{12y}{x}$；由第一式得 $m^2=\dfrac{192}{x}-96=\dfrac{192-96x}{x}$。代入 $m^2$：
$$\frac{144y^2}{x^2}=\frac{192-96x}{x}\Longrightarrow 144y^2=192x-96x^2\Longrightarrow 2x^2+3y^2=4x.$$
又 $x=\dfrac{192}{96+m^2}\in(0,2]$，原点 $(0,0)$ 对应 $m\to\infty$，取不到。配方得
$$\frac{(x-1)^2}{1}+\frac{y^2}{2/3}=1,$$
即轨迹为椭圆（半长轴 $1$、半短轴 $\dfrac{\sqrt6}{3}$，长轴沿 $x$ 轴），去掉原点。

验算：$m=0$ 时 $P(12,0)$，$Q(2,0)$：$|OQ|\cdot|OP|=2\times12=24$，而 $R=(2\sqrt6,0)$，$|OR|^2=24$，条件成立，且 $(2,0)$ 在椭圆上。$m=4$ 时 $Q=\left(\dfrac{12}{7},\dfrac47\right)$，有 $2\left(\dfrac{12}{7}\right)^2+3\left(\dfrac47\right)^2=\dfrac{288+48}{49}=\dfrac{48}{7}=4\cdot\dfrac{12}{7}$，在轨迹上；$m=-3$ 时 $Q=\left(\dfrac{64}{35},-\dfrac{16}{35}\right)$，代入同样使 $2x^2+3y^2-4x=0$。轨迹方程与点集限制均自洽。

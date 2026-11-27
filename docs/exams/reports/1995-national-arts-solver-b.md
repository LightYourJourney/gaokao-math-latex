# 1995 全国卷文科数学 · 独立求解（求解员 B）

说明：仅依据 `1995_全国卷_文科/题面转录草稿.md` 与 `figures/` 独立求解。来源页未载答案，以下结论待与求解员 A 交叉核对。选择题给字母，填空题给值，解答题给结论；每题末附验算。

## 第 1 题

**答案：** B

解析：$\complement_I M=I\setminus M=\{-3,-4\}$，故 $\complement_I M\cap N=\{-3,-4\}\cap\{0,-3,-4\}=\{-3,-4\}$。

验算：$0\in M$，不在补集；$-3,-4$ 均不属于 $M$ 且属于 $N$；$-1,-2\in M$，不在补集。恰得 $\{-3,-4\}$。

## 第 2 题

**答案：** D

解析：$y=\dfrac1{x+1}$ 的定义域为 $x\ne-1$，有垂直渐近线 $x=-1$、水平渐近线 $y=0$；$x>-1$ 时 $y>0$，$x<-1$ 时 $y<0$。只有 (D) 的图象符合。

验算：取 $x=0$ 得 $y=1$，取 $x=1$ 得 $y=\tfrac12$。(C) 为 $y=-\dfrac1{x-1}$，在 $x=1$ 处无定义，排除；(A)(B) 在 $x=0$ 处 $y=-1$，排除；(D) 同时满足两点。

源疑点：本题四个选项均为图象而非文字，字母与函数式的对应依赖矢量重绘稿；重绘稿标注 (D) 即 $y=1/(x+1)$，其与原页选项排布的一致性仍应以原页图复核。

## 第 3 题

**答案：** C

解析：$4\sin u+3\cos u=5\sin(u+\varphi)$，其中 $u=3x+\dfrac\pi4$，故函数为 $5\sin\left(3x+\dfrac\pi4+\varphi\right)$，最小正周期 $T=\dfrac{2\pi}{3}$。

验算：令 $T=\dfrac{2\pi}{3}$，则 $3(x+T)+\dfrac\pi4=3x+\dfrac\pi4+2\pi$，函数值不变；而 $T=\dfrac\pi3$ 时自变量相位增加 $\pi$，函数值变为相反数，故最小正周期确为 $\dfrac{2\pi}{3}$。

## 第 4 题

**答案：** B

解析：设正方体棱长 $s$，全面积 $6s^2=a^2$，故 $s=\dfrac{a}{\sqrt6}$。正方体外接球直径等于体对角线 $\sqrt3\,s$，故 $R=\dfrac{\sqrt3}{2}s=\dfrac{a}{2\sqrt2}$，球表面积 $4\pi R^2=\dfrac{\pi a^2}{2}$。

验算：取 $a=1$，则 $s=\dfrac1{\sqrt6}$，$R=\dfrac1{2\sqrt2}$，$4\pi R^2=\dfrac{4\pi}{8}=\dfrac\pi2$，与 $\dfrac{\pi a^2}{2}$ 一致。

## 第 5 题

**答案：** D

解析：由图 $l_1$ 下降，$k_1<0$；$l_2,l_3$ 均上升，且 $l_2$ 比 $l_3$ 陡，故 $0<k_3<k_2$。于是 $k_1<k_3<k_2$。

验算：按重绘图形取点估算：$k_1\approx\dfrac{-1.45-1.35}{2.85+1.25}\approx-0.68$，$k_2\approx\dfrac{1.95+1.60}{1.15+1.05}\approx1.61$，$k_3\approx\dfrac{1.25+1.05}{3.05+1.62}\approx0.49$，确得 $k_1<k_3<k_2$。

源疑点：三条直线的具体位置只由矢量重绘图给出，答案依赖重绘图对原图斜率正负与大次序的忠实还原。

## 第 6 题

**答案：** C

解析：$3x^2-y^2=3$ 即 $x^2-\dfrac{y^2}{3}=1$，$a=1$，$b=\sqrt3$，渐近线为 $y=\pm\dfrac ba x=\pm\sqrt3\,x$。

验算：把 $y=\sqrt3 x$ 代入 $x^2-\dfrac{y^2}{3}$ 得 $x^2-x^2=0$，符合渐近线应满足的方程；$y=\pm3x$ 代入得 $-2x^2$，不是常数，排除。

## 第 7 题

**答案：** A

解析：$\sin x\le\cos x\iff\sin x-\cos x\le0\iff\sqrt2\sin\left(x-\dfrac\pi4\right)\le0\iff x-\dfrac\pi4\in[\pi+2k\pi,2\pi+2k\pi]$，即 $x\in\left[\dfrac{5\pi}{4}+2k\pi,\dfrac{9\pi}{4}+2k\pi\right]$。取 $k=-1$ 得 $\left[-\dfrac{3\pi}{4},\dfrac\pi4\right]$，即 (A)。

验算：端点 $x=-\dfrac{3\pi}{4},\dfrac\pi4$ 处 $\sin x=\cos x$；$x=-\dfrac\pi2\in$ (A) 时 $\sin x=-1\le0=\cos x$。(B)(D) 在 $x=\dfrac\pi2$ 处 $\sin=1>0=\cos$；(C) 在 $x=\dfrac{3\pi}{4}$ 处 $\sin=\dfrac{\sqrt2}{2}>-\dfrac{\sqrt2}{2}=\cos$，均不成立。

## 第 8 题

**答案：** C

解析：第一个圆：$(x-1)^2+y^2=1$，圆心 $(1,0)$，半径 $1$；第二个圆：$x^2+(y+2)^2=4$，圆心 $(0,-2)$，半径 $2$。圆心距 $d=\sqrt{1+4}=\sqrt5$，满足 $|2-1|<d<1+2$，故两圆相交。

验算：两方程相减得公共弦所在直线 $x+2y=0$，即 $x=-2y$。代入第一圆：$5y^2+4y=0$，得 $y=0$ 或 $y=-\dfrac45$，对应两个不同交点 $(0,0)$、$\left(\dfrac85,-\dfrac45\right)$，确为相交。

## 第 9 题

**答案：** A

解析：$\sin^4\theta+\cos^4\theta=1-2\sin^2\theta\cos^2\theta=1-\dfrac12\sin^22\theta=\dfrac59$，故 $\sin^22\theta=\dfrac89$。$\theta$ 为第三象限角，$2\theta\in(2\pi+4k\pi,3\pi+4k\pi)$，其终边在第一、二象限，$\sin2\theta>0$，故 $\sin2\theta=\dfrac{2\sqrt2}{3}$。

验算：$\sin2\theta=\dfrac{2\sqrt2}{3}$ 时 $\sin^22\theta=\dfrac89$，回代得 $1-\dfrac12\cdot\dfrac89=\dfrac59$；且第三象限角的两倍角正弦为正，符号一致。

## 第 10 题

**答案：** A

解析：设棱长为 $4$，取 $A(0,0,0)$、$B(4,0,0)$、$D(0,4,0)$、$A_1(0,0,4)$、$B_1(4,0,4)$、$D_1(0,4,4)$。由 $B_1E_1=D_1F_1=\dfrac{A_1B_1}{4}=1$ 得 $E_1(3,0,4)$、$F_1(1,4,4)$。于是
\[
\overrightarrow{BE_1}=(-1,0,4),\qquad \overrightarrow{DF_1}=(1,0,4),
\]
$\overrightarrow{BE_1}\cdot\overrightarrow{DF_1}=-1+16=15$，$|BE_1|=|DF_1|=\sqrt{17}$，故所求余弦值为 $\dfrac{15}{17}$。

验算：$|\overrightarrow{BE_1}|^2=1+16=17=|\overrightarrow{DF_1}|^2$；夹角余弦 $\dfrac{15}{17}\in(0,1)$，与两线所成锐角相符。

源疑点：$E_1,F_1$ 各自所在棱及靠近哪一端，文字只给长度关系，实际由重绘图标明（$E_1\in A_1B_1$ 靠近 $B_1$，$F_1\in D_1C_1$ 靠近 $D_1$）；若方向取反，结果会改变。

## 第 11 题

**答案：** B

解析：由 $2-x>0$ 得定义域 $x<2$。令 $u=2-x$，它在 $x<2$ 上随 $x$ 增大而减小；要使 $y=\log_a u$ 随 $x$ 增大而增大，$\log_a u$ 必须随 $u$ 减小而增大，即 $\log_a$ 为减函数，故 $0<a<1$。

验算：取 $a=\dfrac12$，$x=1$ 时 $y=0$，$x=0$ 时 $y=-1$，$x$ 增大时 $y$ 增大，符合；取 $a=2$，$x=1$ 时 $y=0$，$x=0$ 时 $y=1$，为减函数，不符。故 $0<a<1$。

## 第 12 题

**答案：** D

解析：$x^5$ 项来自 $1\cdot\mathrm C_{10}^5x^5$ 与 $(-x^3)\cdot\mathrm C_{10}^2x^2$，系数为
\[
\mathrm C_{10}^5-\mathrm C_{10}^2=252-45=207.
\]

验算：$(1+x)^{10}=1+10x+45x^2+120x^3+210x^4+252x^5+\cdots$，乘 $(1-x^3)$ 后 $x^5$ 项为 $252x^5-45x^5=207x^5$。

## 第 13 题

**答案：** D

解析：① 若 $\alpha\parallel\beta$，由 $l\perp\alpha$ 得 $l\perp\beta$，而 $m\subset\beta$，故 $l\perp m$，真。② $\alpha\perp\beta$ 时，$l\perp\alpha$ 只推出 $l\parallel\beta$（或 $l\subset\beta$），$m$ 可在 $\beta$ 内任意取向，未必 $l\parallel m$，假。③ 若 $l\parallel m$，由 $l\perp\alpha$ 得 $m\perp\alpha$，而 $m\subset\beta$，故 $\beta\perp\alpha$，真。④ $l\perp m$ 不能推出两平面平行，假。正确的是 ①③。

验算：取 $\alpha:xOy$ 平面，$\beta:yOz$ 平面，$l$ 为 $z$ 轴，$m$ 为 $y$ 轴。此时 $l\perp\alpha$、$m\subset\beta$、$\alpha\perp\beta$、$l\perp m$，但 $l$ 与 $m$ 相交不平行（否定②），且 $\alpha$ 与 $\beta$ 垂直不平行（否定④）。

## 第 14 题

**答案：** C

解析：等差数列中 $S_{2n-1}=(2n-1)a_n$，$T_{2n-1}=(2n-1)b_n$，故
\[
\frac{a_n}{b_n}=\frac{S_{2n-1}}{T_{2n-1}}=\frac{2(2n-1)}{3(2n-1)+1}=\frac{4n-2}{6n-2}\longrightarrow\frac23.
\]

验算：取满足条件的等差序列 $a_n=(2n-1)A$，$b_n=(3n-1)A$（$A\ne0$），则 $S_n=n^2A$，$T_n=\dfrac{n(3n+1)}{2}A$，$\dfrac{S_n}{T_n}=\dfrac{2n}{3n+1}$ 与题设相符，而 $\dfrac{a_n}{b_n}=\dfrac{2n-1}{3n-1}\to\dfrac23$。

## 第 15 题

**答案：** A

解析：三位数为偶数，个位只能取 $2$ 或 $4$，有 $2$ 种；百位从剩余 $4$ 个数字中选，有 $4$ 种；十位从剩余 $3$ 个数字中选，有 $3$ 种。共 $2\times4\times3=24$ 个。

验算：全部无重复数字的三位数共 $5\times4\times3=60$ 个；五个数字中偶数 $2$ 个、奇数 $3$ 个，按个位均匀分布，偶数应占 $\dfrac25$，即 $60\times\dfrac25=24$ 个，一致。

## 第 16 题

**答案：** $x=3$

解析：由 $\log_4(x+1)$ 有意义得 $x>-1$。此时
\[
\log_2(x+1)^2=2\log_2(x+1),\qquad \log_4(x+1)=\frac12\log_2(x+1),
\]
原方程化为 $\dfrac52\log_2(x+1)=5$，故 $\log_2(x+1)=2$，$x+1=4$，$x=3$。

验算：$x=3$ 时 $\log_216+\log_44=4+1=5$，且 $x=3>-1$ 满足定义域；由对数函数单调性，解唯一。

## 第 17 题

**答案：** $\dfrac{7\sqrt3}{32}$（即 $7\sqrt3:32$）

解析：设球半径为 $R$。下底面过球心，故下底面是球的大圆，半径 $R$。设上底面半径为 $r$、圆台高为 $h$。母线与底面成角 $\dfrac\pi3$，其水平投影为 $R-r$，故
\[
h=(R-r)\tan\frac\pi3=\sqrt3\,(R-r).
\]
上底面圆周在球上，球心到下底面所在平面的距离为 $0$、到上底面所在平面的距离为 $h$，故 $r^2+h^2=R^2$。代入得
\[
R^2-r^2=3(R-r)^2\Longrightarrow R+r=3(R-r)\Longrightarrow r=\frac R2,\quad h=\frac{\sqrt3}{2}R.
\]
圆台体积
\[
V_{\text{台}}=\frac{\pi h}{3}(R^2+Rr+r^2)=\frac{\pi}{3}\cdot\frac{\sqrt3R}{2}\cdot\frac{7R^2}{4}=\frac{7\sqrt3\pi R^3}{24},
\]
球体积 $V_{\text{球}}=\dfrac{4\pi R^3}{3}$，故
\[
\frac{V_{\text{台}}}{V_{\text{球}}}=\frac{7\sqrt3\pi R^3/24}{4\pi R^3/3}=\frac{7\sqrt3}{32}.
\]

验算：取 $R=1$，则 $r=\dfrac12$，$h=\dfrac{\sqrt3}{2}$，$r^2+h^2=\dfrac14+\dfrac34=1$ 确在上底球面上；$V_{\text{台}}=\dfrac{\pi}{3}\cdot\dfrac{\sqrt3}{2}\cdot\dfrac74\approx1.587$，$V_{\text{球}}\approx4.189$，比值 $\approx0.3789=\dfrac{7\sqrt3}{32}$。

## 第 18 题

**答案：** $\sqrt3$

解析：由和差化积
\[
\cos x+\cos\left(x+\frac\pi3\right)=2\cos\left(x+\frac\pi6\right)\cos\frac\pi6=\sqrt3\cos\left(x+\frac\pi6\right)\le\sqrt3.
\]

验算：取 $x=-\dfrac\pi6$，得 $\cos\left(-\dfrac\pi6\right)+\cos\left(\dfrac\pi6\right)=\dfrac{\sqrt3}{2}+\dfrac{\sqrt3}{2}=\sqrt3$，最大值确能取到。

## 第 19 题

**答案：** $4$

解析：抛物线 $y^2=4(x+1)$ 的顶点为 $(-1,0)$，$2p=4$，$p=1$，焦点为 $(-1+p,0)=(0,0)$。过焦点且垂直于 $x$ 轴的直线为 $x=0$，代入得 $y^2=4$，$y=\pm2$，故截得线段长为 $4$。

验算：该弦正是过焦点的通径。把抛物线写成 $y^2=4a(x+1)$，得 $a=1$（焦点到顶点距离），过焦点且垂直于对称轴的弦长为 $4a=4$；直接代入 $x=0$ 得交点 $(0,2),(0,-2)$，弦长 $4$，两者一致。

## 第 20 题

**答案：** $144$

解析：恰有一个空盒：先选空盒，有 $4$ 种；再把 $4$ 个不同小球放入其余 $3$ 个盒子且每盒非空。按 $2,1,1$ 分组有 $\mathrm C_4^2=6$ 种，三组分配到 $3$ 个盒子有 $3!=6$ 种，共 $6\times6=36$ 种。总数 $4\times36=144$。

验算：用第二类 Stirling 数，满射数 $3!\,S(4,3)=6\times6=36$，乘以空盒选择 $4$ 得 $144$，两种计数一致。

## 第 21 题

**答案：** $x=2$

解析：令 $t=3^x>0$，则 $3^{x+2}=9t$，$3^{2-x}=\dfrac9t$，原方程化为
\[
9t-\frac9t=80\Longrightarrow 9t^2-80t-9=0.
\]
解得 $t=\dfrac{80\pm\sqrt{6400+324}}{18}=\dfrac{80\pm82}{18}$，即 $t=9$ 或 $t=-\dfrac19$。因 $t>0$，舍去 $t=-\dfrac19$。由 $3^x=9$ 得 $x=2$。

验算：$x=2$ 时 $3^{4}-3^{0}=81-1=80$，成立。

## 第 22 题

**答案：** 模为 $-2\cos\dfrac\theta2$；辐角为 $2k\pi+\dfrac{3\theta}{2}+\pi\ (k\in\mathbb Z)$，辐角主值为 $\dfrac{3\theta}{2}-\pi$。

解析：由 $z=\cos\theta+i\sin\theta=e^{i\theta}$，
\[
z^2+z=z(z+1)=e^{i\theta}(e^{i\theta}+1)=e^{i\theta}\cdot2\cos\frac\theta2\,e^{i\theta/2}=2\cos\frac\theta2\,e^{i3\theta/2}.
\]
因 $\theta\in(\pi,2\pi)$，有 $\dfrac\theta2\in\left(\dfrac\pi2,\pi\right)$，故 $\cos\dfrac\theta2<0$，从而
\[
|z^2+z|=\left|2\cos\frac\theta2\right|=-2\cos\frac\theta2.
\]
又 $2\cos\dfrac\theta2\,e^{i3\theta/2}=(-2\cos\dfrac\theta2)e^{i(3\theta/2+\pi)}$，其中系数 $-2\cos\dfrac\theta2>0$，故辐角为 $\dfrac{3\theta}{2}+\pi+2k\pi$；取主值 $\dfrac{3\theta}{2}-\pi\in\left(\dfrac\pi2,2\pi\right)$。

验算：取 $\theta=\dfrac{3\pi}{2}$，$z=-i$，$z^2+z=-1-i$，模为 $\sqrt2=-2\cos\dfrac{3\pi}{4}$，辐角 $\dfrac{5\pi}{4}=\dfrac{3\theta}{2}-\pi$，与公式一致。

## 第 23 题

**答案：** 不等式对任意正整数 $n$ 成立（证明见解析）。

解析：设首项 $a_1>0$，公比 $q>0$，则 $S_n>0$。由
\[
S_{n+1}=S_n+a_{n+1},\qquad S_{n+2}=S_{n+1}+a_{n+2}=S_{n+1}+q\,a_{n+1},
\]
得
\[
S_{n+1}^2-S_nS_{n+2}
=S_{n+1}^2-S_n(S_{n+1}+a_{n+2})
=S_{n+1}a_{n+1}-S_na_{n+2}
=a_{n+1}(S_{n+1}-qS_n).
\]
而
\[
S_{n+1}-qS_n=(S_n+a_{n+1})-qS_n=a_{n+1}+(1-q)S_n.
\]
由 $S_n=\dfrac{a_1(q^n-1)}{q-1}$（$q\ne1$ 时）可得 $S_{n+1}-qS_n=a_1$；$q=1$ 时 $S_{n+1}-S_n=a_{n+1}=a_1$，同式亦成立。因此
\[
S_{n+1}^2-S_nS_{n+2}=a_1a_{n+1}>0,
\]
即 $S_nS_{n+2}<S_{n+1}^2$。由于 $y=\log_{0.5}x$ 是减函数，故
\[
\log_{0.5}(S_nS_{n+2})>\log_{0.5}S_{n+1}^2,
\]
即 $\dfrac{\log_{0.5}S_n+\log_{0.5}S_{n+2}}{2}>\log_{0.5}S_{n+1}$。

验算：取 $a_1=1$，$q=2$，$n=1$，则 $S_1=1,S_2=3,S_3=7$，
\[
\frac{\log_{0.5}1+\log_{0.5}7}{2}=-\frac{\log_27}{2}\approx-1.404,\qquad
\log_{0.5}3=-\log_23\approx-1.585,
\]
确实 $-1.404>-1.585$。同时 $S_2^2-S_1S_3=9-7=2=a_1a_2$，与恒等式一致。

## 第 24 题

**答案：** （1）证明见解析；（2）点 $E$ 到截面 $ABCD$ 的距离等于圆柱底面半径 $R$（即轴截面正方形边长 $AB$ 的一半）。

解析：（1）依图，$A,B,E$ 在同一底面圆周上，$AB$ 为底面直径，由直径所对圆周角为直角得 $AE\perp BE$。又 $AD$ 为圆柱母线，垂直于底面，故 $AD\perp BE$。于是 $BE$ 垂直于平面 $ADE$ 内的两条相交直线 $AE,AD$，即 $BE\perp$ 平面 $ADE$；而 $AF\subset$ 平面 $ADE$，所以 $BE\perp AF$。题设又给 $AF\perp DE$，且 $BE\cap DE=E$，故 $AF\perp$ 平面 $BDE$。因为 $DB\subset$ 平面 $BDE$，所以 $AF\perp DB$。

（2）设底面半径为 $R$，则轴截面为正方形，高 $h=AB=2R$。设 $E$ 在底面圆上的位置使 $\angle(\overrightarrow{OE},\overrightarrow{AB})=\varphi$，则 $E$ 到直线 $AB$ 的距离为 $R|\sin\varphi|$，故
\[
S_{\triangle ABE}=\frac12\cdot AB\cdot R|\sin\varphi|=R^2|\sin\varphi|.
\]
三棱锥 $D-ABE$ 以 $\triangle ABE$ 为底、$D$ 到该底面的距离为 $h=2R$，故
\[
V_{D-ABE}=\frac13S_{\triangle ABE}\cdot2R=\frac23R^3|\sin\varphi|.
\]
圆柱体积 $V_{\text{柱}}=\pi R^2\cdot2R=2\pi R^3$。由题设
\[
\frac{V_{\text{柱}}}{V_{D-ABE}}=\frac{2\pi R^3}{\frac23R^3|\sin\varphi|}=\frac{3\pi}{|\sin\varphi|}=3\pi,
\]
得 $|\sin\varphi|=1$。截面 $ABCD$ 为过轴的平面，与底面垂直且交线为 $AB$，故 $E$ 到截面 $ABCD$ 的距离等于 $E$ 到直线 $AB$ 的距离，即 $R|\sin\varphi|=R$。

验算：取 $R=1$，此时 $|\sin\varphi|=1$，$V_{\text{柱}}=2\pi$，$V_{D-ABE}=\dfrac23$，比值 $=3\pi$，满足题设；$E$ 到截面距离 $=1=R$。又（1）中用坐标复核：$A(-R,0,0)$、$B(R,0,0)$、$D(-R,0,2R)$、$E(R\cos\varphi,R\sin\varphi,0)$，可算得 $\overrightarrow{AF}\cdot\overrightarrow{DB}=0$，结论一致。

## 第 25 题

**答案：** （1）$x=8+\dfrac{2\sqrt{50-t^2}-4t}{5}$，定义域 $0\le t\le\sqrt{10}$；（2）政府补贴至少为 $1$ 元/千克。

解析：（1）由 $P=Q$ 得
\[
1000(x+t-8)=500\sqrt{40-(x-8)^2},
\]
即 $2(x+t-8)=\sqrt{40-(x-8)^2}$。令 $u=x-8\in[0,6]$，得 $2(u+t)=\sqrt{40-u^2}$，两边平方：
\[
4(u+t)^2=40-u^2\Longrightarrow 5u^2+8tu+4t^2-40=0.
\]
解得
\[
u=\frac{-8t\pm\sqrt{64t^2-20(4t^2-40)}}{10}
=\frac{-4t\pm2\sqrt{50-t^2}}{5}.
\]
因 $u\ge0$，取正号：
\[
u=\frac{2\sqrt{50-t^2}-4t}{5},\qquad x=8+u=8+\frac{2\sqrt{50-t^2}-4t}{5}.
\]
定义域需 $50-t^2\ge0$ 且 $u\ge0$，即 $2\sqrt{50-t^2}\ge4t\iff 50-t^2\ge4t^2\iff t\le\sqrt{10}$；结合 $t\ge0$ 得 $0\le t\le\sqrt{10}$。此时 $u\in[0,2\sqrt2]\subset[0,6]$，$x\in[8,8+2\sqrt2]\subset[8,14]$，满足题设全部限制。

（2）市场平衡价格不高于 $10$ 元，即 $u=x-8\le2$。由 $u(t)=\dfrac{2\sqrt{50-t^2}-4t}{5}$ 在 $[0,\sqrt{10}]$ 上严格递减，只需解 $u(t)=2$：
\[
5\cdot4+8t\cdot2+4t^2-40=0\Longrightarrow 4t^2+16t-20=0\Longrightarrow t^2+4t-5=0,
\]
得 $t=1$（舍负根 $t=-5$）。故 $t\ge1$。

验算：$t=1$ 时 $u=\dfrac{2\sqrt{49}-4}{5}=\dfrac{14-4}{5}=2$，$x=10$，此时 $P=1000(10+1-8)=3000$，$Q=500\sqrt{40-4}=3000$，平衡。$t=0$ 时 $x=8+2\sqrt2\approx10.83$，$P=Q=2000\sqrt2$；$t=\sqrt{10}$ 时 $x=8$，$P=Q=1000\sqrt{10}$，均与公式一致。$t<1$ 时 $u>2$，价格高于 $10$ 元，故至少 $1$ 元/千克。

## 第 26 题

**答案：** 点 $Q$ 的轨迹是椭圆
\[
(x-1)^2+\frac32y^2=1\quad\text{（即 }2x^2-4x+3y^2=0\text{）},
\]
中心为 $(1,0)$，长半轴 $1$ 沿 $x$ 轴、短半轴 $\sqrt{\dfrac23}$ 沿 $y$ 轴；轨迹应除去原点 $(0,0)$（原点只是 $|m|\to\infty$ 的极限点，$|OQ|>0$ 使其不可达）。

解析：设 $P(12,m)$（$m\in\mathbb R$），射线 $OP$ 上的点可写为 $\lambda(12,m)$，$\lambda\ge0$，其中 $P$ 对应 $\lambda=1$。
设 $R=\lambda_R(12,m)$ 在椭圆上，则
\[
\frac{(12\lambda_R)^2}{24}+\frac{(m\lambda_R)^2}{16}=1
\Longrightarrow \lambda_R^2\left(6+\frac{m^2}{16}\right)=1
\Longrightarrow \lambda_R^2=\frac{1}{6+\frac{m^2}{16}}.
\]
设 $Q=\mu(12,m)$，则 $|OP|=\sqrt{144+m^2}$，$|OR|=\lambda_R\sqrt{144+m^2}$，$|OQ|=\mu\sqrt{144+m^2}$。由 $|OQ|\cdot|OP|=|OR|^2$ 得
\[
\mu|OP|^2=\lambda_R^2|OP|^2\Longrightarrow \mu=\lambda_R^2=\frac{1}{6+\frac{m^2}{16}}.
\]
于是
\[
x=\frac{12}{6+\frac{m^2}{16}},\qquad y=\frac{m}{6+\frac{m^2}{16}}.
\]
消去 $m$：由 $y=\dfrac{mx}{12}$ 得 $m=\dfrac{12y}{x}$（$x>0$），又由第一式得 $\dfrac{m^2}{16}=\dfrac{12}{x}-6$，故
\[
\frac{144y^2}{x^2}=\frac{12}{x}-6
\Longrightarrow 144y^2=192x-96x^2
\Longrightarrow 2x^2-4x+3y^2=0,
\]
即 $(x-1)^2+\dfrac32y^2=1$。因 $x=\dfrac{12}{6+m^2/16}\in(0,2]$，轨迹为该椭圆上 $x>0$ 的部分，即整条椭圆除去原点（$x=0$ 只在 $y=0$ 时成立，对应 $|m|\to\infty$，不能取到）。

验算：$m=0$ 时 $P(12,0)$，$R(2\sqrt6,0)$，$|OR|^2=24$，$|OQ|=\dfrac{24}{12}=2$，$Q(2,0)$，满足 $(2-1)^2+0=1$。取 $m=4\sqrt3$ 时 $6+\dfrac{m^2}{16}=9$，$Q\left(\dfrac43,\dfrac{4\sqrt3}{9}\right)$，代入得 $\left(\dfrac13\right)^2+\dfrac32\cdot\dfrac{48}{81}=\dfrac19+\dfrac89=1$，且对应 $\mu=\dfrac19>0$，$Q$ 在射线 $OP$ 上。

源疑点：题面只说“求轨迹方程”，未说明是否剔除方程上的孤立不可达点；按 $|OQ|\cdot|OP|=|OR|^2>0$ 严格理解，原点 $(0,0)$ 不在轨迹上，建议与求解员 A 核对这一细节的表述口径。

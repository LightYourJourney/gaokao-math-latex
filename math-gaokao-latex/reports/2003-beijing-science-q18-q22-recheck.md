# 2003 春季北京理科候选卷第 18、22 题复算

本记录针对固定副本 `春季高考/2003/2003春季北京理.pdf`，SHA-256 `4cb807a7fe4989e2b0e0d2ad8aa42438f72861d87a90afe8d8cd003608915b28`。该卷尚未正式登记；副本无印载答案，以下为项目独立计算，不声明官方身份。两套草稿出现分歧后，主代理对题干及代数重新核算并修正隔离草稿。

## 第 18 题

令 $t=\cos2x$，源题分子 $6\cos^4x+5\sin^2x-4$ 化为 $(3t^2+t)/2$，而非较早草稿中的 $(3t^2-2t)/2$。故在 $t\in[-1,1]\setminus\{0\}$ 上 $f=(3t+1)/2$，值域为 $[-1,1/2)\cup(1/2,2]$；定义域为 $\mathbb R\setminus\{\pi/4+k\pi/2:k\in\mathbb Z\}$，函数为偶函数。随机代入 1000 个非奇点对原式和化简式做数值核验，通过；该数值核验不替代正式逐题审查。

## 第 22 题

抛物线 $y^2=4x$ 与直线 $y=-\sqrt3(x-1)$ 相交时 $3(x-1)^2=4x$，其根为 $x=3$、$1/3$；较早草稿的根 $(5\pm2\sqrt6)/3$ 错误。取 $A=(3,-2\sqrt3)$、$B=(1/3,2\sqrt3/3)$、$C=(-1,t)$，三角形各顶点的对应点积依次为

$$\overrightarrow{AB}\cdot\overrightarrow{AC}=\frac83(10+\sqrt3t),\quad
\overrightarrow{BA}\cdot\overrightarrow{BC}=\frac{16}{9}-\frac{8\sqrt3}{3}t,\quad
\overrightarrow{CA}\cdot\overrightarrow{CB}=\left(t+\frac{2\sqrt3}{3}\right)^2.$$

因此钝角情形为 $t<-10/\sqrt3$ 或 $t>2/(3\sqrt3)$，但须排除共线退化点 $t=2\sqrt3$。两个直角边界也不取。以代表值和边界对三个点积做数值代入核验通过。答案及解析仍需纳入正式逐题审查、来源登记及四版构建流程。

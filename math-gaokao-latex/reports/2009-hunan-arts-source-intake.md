# 2009 湖南卷文科：固定来源接收与文字层路由

- 日期：2026-11-20；canonical worktree：`仓库根`；批次 `phase6-b68`；source manifest revision 10213 后定稿。
- 固定候选 source：`src-8f952daa9c063386e369ff0322811171b3b900a0560749c263440acd3d2ad297`，manifest 相对路径 `普通高考/2009/2009湖南文.pdf`，仓库内副本 `math-gaokao-latex/.work/ocr-local/sources/2009湖南文.pdf`。manifest 状态 `ready`；现场 SHA-256 `db41a34b5d57a8db3f2ee49872e3dbc1e290c2e7390fc96cf4e084b5a679e3eb`，大小 510,869 bytes，与 `artifact` 记录一致。
- PDF 共 2 页，A3 横向（1190.55 × 841.89 pt）。页眉「2009 普通高等学校招生考试（湖南卷文）」，页脚书页码 529、530。无答案页、无解析页、无评分标准页。
- 题面结构（按原页，逐题核对）：一、选择题 1—8；二、填空题 9—15；三、解答题 16—21。原页各题与各节均未印分值，全部记「原页未标」，不补。

## 页面结构与文字层路由

| PDF 页 | 印面 | 可见范围 |
| --- | --- | --- |
| 1 | 529 | 第 1—18 题（第 1 栏 1—7、第 2 栏 8—16、第 3 栏 17—18）、三节标题；第 4 题中位三角形图、第 7 题四幅图象选项、第 15 题三角板拼接图、第 18 题正三棱柱图 |
| 2 | 530 | 第 19—21 题（第 1 栏 19、第 2 栏 20、第 3 栏 21） |

- 两页都有文字层，但按栏错位且**行坐标不可信**：`pdftotext -bbox` 把第 8 题记在页首 $y\approx58\,\mathrm{pt}$（页眉位置），实际印在第 2 栏顶端；第 18 题整段文字被记在页首，实际印在第 3 栏下部（印面 $y\approx585$—$661$）。因此文字层只作题号定位，不作转录依据，也不能把 bbox 换算成裁剪位置；逐块裁剪一律先用 100 dpi 预览目视定位再放大。
- 逐题核对方式：`pdftoppm -r 600 -png -f N -l N -x X -y Y -W W -H H` 逐块放大到 600 dpi；第 6 题「平面六面体」、第 13 题「双曲线线 $C$」、第 14 题「$B=2A$」另按 1200 dpi 逐字确认。第 7 题四个选项本身即图，逐幅核对凹凸与端点；第 15 题的 45°、60° 与两个直角标记按 900—1200 dpi 定位。
- 四幅图均按原页以 TikZ 矢量重绘，登记进 manifest `figure_files`，`expected_occurrences` 均为 2（试题版与含解析各引用一次）。第 7 题按 2009 浙江卷第 8、10 题体例把四个选项合成一幅组合图稿，A—D 次序与原件一致；第 15 题按 $AB=AC$、$ED=BC$、$\angle EBD=90^\circ$、$\angle BED=60^\circ$ 定出 $E$ 为 $BC$ 中点、$BD=\frac{\sqrt6}2 AB$，与原页图按比例吻合；第 18 题取投影 $(x,y,z)\mapsto(x+0.20y,\,z+0.48y)$，$E$ 按 $AE:EC=3:1$ 定位。未使用任何页面截图。

## 结论与边界

- 第 1 题：$\sqrt2=2^{1/2}$，$\log_2\sqrt2=\frac12$，(D)。
- 第 2 题：$2p=8$、$p=4$，开口向左，焦点 $(-2,0)$，(B)。
- 第 3 题：$d=\frac{11-3}4=2$、$a_1=1$，$S_7=7\times1+21\times2=49$，(C)；与 $\frac{7(a_1+a_7)}2=49$ 互验。
- 第 4 题：中点向量代入得 $\overrightarrow{AD}+\overrightarrow{BE}+\overrightarrow{CF}=\boldsymbol 0$，(A)；其余三项分别等于 $\boldsymbol c-\boldsymbol b$、$\boldsymbol b-\boldsymbol a$、$\boldsymbol a-\boldsymbol c$。
- 第 5 题：到会 6 人；含甲企业 $\mathrm C_4^2\times2=12$、不含甲企业 $\mathrm C_4^3\times1=4$，共 $16$，(B)。
- 第 6 题：按「共面＝相交或平行」列出两组，公共棱为 $AA_1$、$BB_1$、$BC$、$CD$、$C_1D_1$ 共 5 条，(C)。
- 第 7 题：$f'$ 递增即曲线下凸、切线斜率递增；只有（A）全程下凸，(A)。
- 第 8 题：$K=\frac12$ 时 $f_K(x)=\frac12$（$|x|<1$）、$2^{-|x|}$（$|x|\geqslant1$），递增区间 $(-\infty,-1]$，对应（C）；$x=-1$ 属递增区间、$x=1$ 不属于，端点单独验算。
- 第 9 题：$15+10-x=22$ 得两项都爱 3 人，只爱篮球 $15-3=12$；四类人数 $12+7+3+8=30$ 回验。
- 第 10 题：$x+\frac2x\geqslant2\sqrt2$，等号 $x=\sqrt2$，最小值 $2\sqrt2$。
- 第 11 题：通项 $\mathrm C_4^k x^{k/2}$，$k=2$ 时系数 $\mathrm C_4^2=6$；展开式回验。
- 第 12 题：分层抽样等概率，$\frac{10}N=\frac1{12}$，$N=120$。
- 第 13 题：$\angle AOF=60^\circ$，$\cos60^\circ=\frac ac=\frac12$，$e=\frac ca=2$；回代 $b^2=3a^2$、$\tan\angle AOF=\sqrt3$。
- 第 14 题：正弦定理给出 $AC=2\cos A$，故 $\frac{AC}{\cos A}=2$；锐角条件 $30^\circ<A<45^\circ$，$AC\in(\sqrt2,\sqrt3)$，两端分别对应 $C=90^\circ$、$B=90^\circ$，不取到。
- 第 15 题：45° 板 △ABC 与 30°—60° 板 △BDE 斜边相等（$ED=BC$），$BE=\frac{\sqrt2}2$、$BD=\frac{\sqrt6}2$，$E$ 为 $BC$ 中点，$D\left(1+\frac{\sqrt3}2,\frac{\sqrt3}2\right)$，$x=1+\frac{\sqrt3}2$、$y=\frac{\sqrt3}2$；用 $|ED|=\sqrt2$ 与 $\cos\angle BED=\frac12$ 回验，并与原页图比例（$BD/AB\approx1.26$、$\angle DAB\approx25^\circ$）核对。
- 第 16 题：$\boldsymbol a\parallel\boldsymbol b$ 得 $4\sin\theta=\cos\theta$，$\tan\theta=\frac14$；$|\boldsymbol a|=|\boldsymbol b|$ 得 $\sin2\theta+\cos2\theta=-1$，$\theta=\frac\pi2$ 或 $\frac{3\pi}4$，两解均回代 $|\boldsymbol a|^2=5$。
- 第 17 题：$3!\times\frac12\times\frac13\times\frac16=\frac16$；$1-\left(\frac23\right)^3=\frac{19}{27}$。
- 第 18 题：以 $D$ 为原点建系，$DE\perp A_1E$ 给出 $16t^2-12t=0$，$t=\frac34$（$t=0$ 即 $E=A$，剔除）；$DE\perp AC$ 且 $DE\perp AA_1$，故平面 $A_1DE\perp$ 平面 $ACC_1A_1$；$\sin\theta=\frac{3\sqrt{21}}{2\sqrt3\times4\sqrt3}=\frac{\sqrt{21}}8$。
- 第 19 题：$f'$ 对称轴 $x=-\frac b3=2$，$b=-6$；极小值点须 $t>2$（$t=2$ 时 $f'=3(x-2)^2\geqslant0$ 无极值），$c=12t-3t^2$，$g(t)=-2t^3+6t^2$ 在 $(2,+\infty)$ 递减，定义域 $(2,+\infty)$、值域 $(-\infty,8)$。
- 第 20 题：正方形对角线相等给出 $b=c$，面积 $2bc=8$ 给出 $b=c=2$、$a^2=8$；左准线 $x=-4$，中点 $\left(-\frac{8k^2}{1+2k^2},\frac{4k}{1+2k^2}\right)$，$|x|+|y|\leqslant2$ 得 $2k^2+2|k|-1\leqslant0$，$|k|\leqslant\frac{\sqrt3-1}2$；$\Delta=32-64k^2>0$ 在该区间内自动满足。
- 第 21 题：(1) 部分和 $3\left(1-2^{-n}\right)<3$，取 $M=3$，是 $B-$数列；(2) 四条条件-结论组合中只有 ②$\Rightarrow$④（等价 ③$\Rightarrow$①）为真——由 $\sum|x_n|$ 收敛推出 $\sum|x_{n+1}-x_n|\leqslant2\sum|x_n|$ 收敛，取逆否即得；其余三条分别以 $x_n=1$、$x_n=2^{1-n}$、$x_n=(-1)^n$ 反例；(3) 由 $|a_n|\leqslant|a_1|+M$ 得 $|a_{n+1}^2-a_n^2|\leqslant2(|a_1|+M)|a_{n+1}-a_n|$，取 $M'=2M(|a_1|+M)$。
- 源缺陷一：第 6 题首句印作「平面六面体 $ABCD-A_1B_1C_1D_1$ 中」，「平面」当为「平行」；「平面六面体」不是数学名词，而题中记号与设问只在平行六面体下确定，按更正语义读法唯一，答案不受影响。照录原页字面，登记 `ISSUE-1509`（`transcription-ambiguous`，`non_blocking`）。
- 源缺陷二：第 13 题末句印作「则双曲线线 $C$ 的离心率为______」，「线」字重复；题首已给出双曲线 $C$ 的方程，末句所指明确，属衍字，不影响答案。照录原页字面，登记 `ISSUE-1510`（`transcription-ambiguous`，`non_blocking`）。
- 两处缺陷均已写入 `index_metadata.note` 与两版解析说明。
- 来源发布者、出版者、版次、原始发布渠道与官方身份均未核实；本报告只证明固定候选 PDF 的指纹、页数、版面与题号范围，以及题面转录、四版构建与视觉审查的完成情况，不表示来源认证或整卷验收。

## 产物与验收

- 四份 Markdown：`2009/2009_数学真题_湖南文_试题.md`、`_答案要点.md`、`_解析正文.md`、`_含解析.md`（后者由 `solution_sources.render_combined()` 生成）。
- 项目：`math-gaokao-latex/2009_湖南卷_文科/`（`questions.tex`、`answers.tex`、`answers_short.tex`、四版壳与 `figures/`）。
- 四版页数：试题版 6、解析版 25、简答版 8、印刷版 19；四份日志均为 0 error / 0 missing character / 0 Overfull / 0 Underfull / 0 undefined reference / 0 warning。
- 视觉审查：58 页八类检查全 pass、0 豁免，`finalize-batch` 返回 `FINALIZED`（`math-gaokao-latex/reports/phase6-b68.md`）；卷 `complete`、批次 `closed`、内容候选 `eligible_complete`。

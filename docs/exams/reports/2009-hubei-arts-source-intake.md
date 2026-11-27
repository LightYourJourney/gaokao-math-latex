# 2009 湖北卷文科：固定来源接收与文字层路由

- 日期：2026-11-20；canonical worktree：`仓库根`；批次 `phase6-b66`；source manifest revision 10193 后定稿。
- 固定候选 source：`src-39055100f5f7ecf067cd24986e10c219a9038df98cb919cc4fab8cecccd33901`，manifest 相对路径 `普通高考/2009/2009湖北文.pdf`，仓库内副本 `math-gaokao-latex/.work/ocr-local/sources/2009湖北文.pdf`。manifest 状态 `ready`；现场 SHA-256 `f60ba7a5a2fef3449fba9474fa973c616aa52a15926b3a97f0dda6b909f4c861`，大小 527,276 bytes，与 `artifact` 记录一致。
- PDF 共 2 页，A3 横向（1190.55 × 841.89 pt）。页眉「2009 普通高等学校招生考试（湖北卷文）」，页脚书页码 525、526。无答案页、无解析页、无评分标准页。
- 题面结构（按原页，逐题核对）：一、选择题 1—10；二、填空题 11—15；三、解答题 16—21。原页各题与各节均未印分值，全部记「原页未标」，不补。

## 页面结构与文字层路由

| PDF 页 | 印面 | 可见范围 |
| --- | --- | --- |
| 1 | 525 | 第 1—17 题全部（第 1 栏 1—8、第 2 栏 9—15、第 3 栏 16—17）、三节标题；第 6 题三棱柱图、第 10 题两幅点阵图、第 15 题频率分布直方图、第 17 题矩形场地图 |
| 2 | 526 | 第 18—21 题；第 18 题四棱锥图、第 20 题抛物线图（第 19 题在第 1 栏下部，第 21 题在第 3 栏） |

- 两页都有文字层，但可读度一般：同一条公式的分子、分母与根号常被拆行，选项的括号与公式分离，第 10 题的点阵与第 15 题的直方图完全不进文字层。文字层只作定位，不作转录依据。
- 逐题核对方式：`pdftoppm -r 600 -png -f N -l N -x X -y Y -W W -H H` 逐块放大到 600 dpi；分数、根号、上下标、选项与图内标注逐项比对；关键疑点（第 6 题侧棱与底面法线的夹角、第 10 题两幅点阵的点数与排列、第 15 题各组矩形高、第 17 题旧墙与进出口位置、第 18 题虚线棱、第 20 题 M/N 与准线位置、第 21 题倒数第二项）再放大复核。
- 六幅图（第 6、10、15、17、18、20 题）均按原页以 TikZ 矢量重绘，登记进 manifest `figure_files`，`expected_occurrences` 均为 2（试题版与含解析各引用一次）。第 10 题点阵按原页 1+2+3+4 与 1×1、2×2、3×3、4×4 逐点绘制，未使用截图。

## 结论与边界

- 第 6 题：设侧棱 $CC_1$ 与底面法线夹角为 $\gamma$，由 $\cos^260^\circ+\cos^245^\circ+\cos^2\gamma=1$ 得 $\cos\gamma=\dfrac12$，高为 $1\times\dfrac12=\dfrac12$，对应 (A)。
- 第 9 题：记 $\varphi=\dfrac{\sqrt5+1}{2}$，由 $\varphi^2=\varphi+1$ 得 $(\varphi-1)\varphi=1$，三数 $\{\varphi\}=\varphi-1$、$[\varphi]=1$、$\varphi$ 成等比（公比 $\varphi$）；两端和 $2\varphi-1=\sqrt5\neq2$，不成等差，(B)。
- 第 10 题：$1225=35^2=\dfrac{49\times50}{2}$ 同时是正方形数与三角形数；$289$、$1024$ 的三角形数判别式 $2313$、$8193$ 非完全平方，$1378=T_{52}$ 但非平方数，(C)。
- 第 14 题：切点弦（极线）$3x+4y=20$，圆心 $(3,4)$ 到弦距离 $1$，半弦 $\sqrt{5-1}=2$，$|PQ|=4$。
- 第 15 题：五组矩形高依次为 $0.02,0.08,0.09,0.03,0.03$，乘组距 $4$ 得 $1$，与总面积归一一致；$[6,10)$ 频数 $0.32\times200=64$，$[2,10)$ 概率 $0.4$。
- 第 18 题 (2)：以 $D$ 为原点建系，平面 $AED$ 法向量 $(0,1,0)$、平面 $CAE$ 法向量 $(\lambda,\lambda,1)$，二面角余弦 $\dfrac{\lambda}{\sqrt{2\lambda^2+1}}=\dfrac12$，得 $\lambda=\dfrac{\sqrt2}{2}\in(0,1]$；$\lambda=\dfrac12$ 时二面角约 $65.9^\circ$，已单独验算排除。
- 第 20 题：焦弦满足 $y_1y_2=-p^2$，故 $\overrightarrow{FM_1}\cdot\overrightarrow{FN_1}=p^2+y_1y_2=0$；又 $\left(x_1+\dfrac p2\right)\left(x_2+\dfrac p2\right)=\dfrac{(y_1-y_2)^2}{4}$，代入得 $S_2^2=4S_1S_3$ 成立。
- 第 21 题 (1)：由 $f'(1)=0$、$f(1)=-\dfrac43$ 得 $b^2=1$。$b=1,c=-1$ 时 $f'(x)=-(x-1)^2\leqslant0$，$x=1$ 两侧均递减，不是极值点，必须剔除；只取 $b=-1,c=3$。(3) 对固定 $b$，$\min_c M$ 等于 $q(x)=x^2-2bx$ 在 $[-1,1]$ 上极差的一半：$|b|\leqslant1$ 时为 $\dfrac{(1+|b|)^2}{2}\geqslant\dfrac12$，$|b|>1$ 时为 $2|b|>2$；$b=0,c=\dfrac12$ 使 $M=\dfrac12$，故 $k$ 最大为 $\dfrac12$。
- 源缺陷：第 10 题原页「摆成各种性状」「这样的数成为正方形数」「下列数中及时三角形数又是正方形数」三处为同音字排印错误（应为「形状」「称为」「既是」）。按更正语义读法唯一，四个选项的判定不受影响；本库照录原页字面，登记 `ISSUE-1506`（`transcription-ambiguous`，`non_blocking`），并写入 `index_metadata.note` 与两版解析说明。
- 来源发布者、出版者、版次、原始发布渠道与官方身份均未核实；本报告只证明固定候选 PDF 的指纹、页数、版面与题号范围，以及题面转录、四版构建与视觉审查的完成情况，不表示来源认证或整卷验收。

## 产物与验收

- 四份 Markdown：`2009/2009_数学真题_湖北文_试题.md`、`_答案要点.md`、`_解析正文.md`、`_含解析.md`（后者由 `solution_sources.render_combined()` 生成）。
- 项目：`math-gaokao-latex/2009_湖北卷_文科/`（`questions.tex`、`answers.tex`、`answers_short.tex`、四版壳与 `figures/`）。
- 四版页数：试题版 6、解析版 29、简答版 8、印刷版 22；四份日志均为 0 error / 0 missing character / 0 Overfull / 0 Underfull / 0 undefined reference。
- 视觉审查：65 页八类检查全 pass、0 豁免，`finalize-batch` 返回 `FINALIZED`（`math-gaokao-latex/reports/phase6-b66.md`）；卷 `complete`、批次 `closed`。

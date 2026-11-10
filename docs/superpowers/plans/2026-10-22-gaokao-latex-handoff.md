# 高考数学全量 LaTeX 工程 · 交接文档

## 2026-11-11 接续：2007 新课标文科（phase5-b12）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 新课标文科（24 题，`gk-2007-newcurriculum-arts`）`phase5-b12` FINALIZED / `closed`，卷 `eligible_complete`，manifest revision 7829，attempt `65e634c0-d4c0-4144-9417-3f09a50a2378`；四版 7/32/9/27 页共 75 页，0 errors、0 overfull、0 underfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b12.md`。
- 六幅 TikZ 图（Q3 正弦简图、Q5 程序框图、Q8 三视图、Q17 塔高测量、Q18 空间四点、Q22 圆与切线割线）均登记 `expected_occurrences=2`；Q3/Q5/Q8/Q17/Q22 与理科版同源，Q18 独立重绘。
- 关键结论：选择 A C A D C B C B C D D B；填空 13=3、14=−1、15=4−4i、16=1/2；Q17 s sinβ tanθ / sin(α+β)；Q18 CD=2 且恒有 AB⊥CD；Q19 三段单调，最大值 ln(7/2)+1/16、最小值 ln2+1/4；Q20 3/4、2/3；Q21 −3/4<k<0 且不存在共线的 k；Q22 90°；Q23 x+y=0；Q24 x<−7 或 x>5/3、最小值 −9/2。
- 图稿修正：Q17 河面灰带下移、C/D 移到近岸带外；Q18 按 D 顶点、A/B 轴端、C 底面点重绘，AB 画虚线。
- 门禁全通过：`review_receipts check-all`（328 批次）、`provenance check-all`（482 卷）、`solution_sources check-all`、`validate-receipts`（482 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（482 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记。
- 下一步：继续 2007 年其余 ready 来源（江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-11 接续：2007 新课标理科（phase5-b11）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 新课标理科（24 题，`gk-2007-newcurriculum-science`）`phase5-b11` FINALIZED / `closed`，卷 `eligible_complete`，manifest revision 7822，attempt `f0db22d3-7d98-43ae-a205-34efb97df995`；四版 7/35/9/28 页共 79 页，0 errors、0 overfull、0 missing characters，4 条 Underfull 已逐条豁免，八类视觉检查逐页 0 fail / 0 pending；报告 `reports/phase5-b11.md`。
- 七幅 TikZ 图（Q3 四幅正弦简图、Q5 程序框图、Q8 三视图、Q17 塔高测量、Q18 三棱锥、Q20 正方形与不规则图形 M、Q22 圆与切线割线）均登记 `expected_occurrences=2`，头注写明来源路径与 SHA-256。
- 关键结论：选择 C D A D C C D B C D B B；填空 13=3、14=−1、15=1+2i、16=240；Q17 AB=s sinβ tanθ / sin(α+β)；Q18(2) √3/3；Q19 k<−√2/2 或 k>√2/2 且不存在共线的 k；Q20 EX=2500、0.9147；Q21 a=3/2 与单调区间、a>√2 且极值之和大于 ln(e/2)；Q22 90°；Q23 两圆与公共弦 x+y=0；Q24 x<−7 或 x>5/3、最小值 −9/2。
- 图稿与版式修正：Q8 的 scope 位移误用 38cm/34cm 造成 674pt 超宽，改为 3.6cm 后归位；Q3 四图放大并省略与曲线重叠的内部零点刻度（保留端点、O、±1）；Q11 三张频数表合并为一张，消除跨页；Q17 河面改为水平灰带、C/D 与 B 分居两岸；Q22 按几何关系重算切点与中点。
- 门禁全通过：`review_receipts check-all`（327 批次）、`provenance check-all`（481 卷）、`solution_sources check-all`、`validate-receipts`（481 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（481 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记。
- 下一步：继续 2007 年其余 ready 来源（新课标文科、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 广东理科（phase5-b10）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 广东理科（21 题，`gk-2007-regular-guangdong-science`）`phase5-b10` FINALIZED / `closed`，卷 `eligible_complete`，manifest revision 7804，attempt `cf4f56a7-dcf6-42c1-a996-9a286fb84706`；四版 7/33/9/25 页共 74 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b10.md`。
- 七幅 TikZ 图（Q4 四联 s–t 图、Q6 条形统计图与算法流程图、Q7 环形分布图、Q12 五棱锥示意、Q15 圆与切线、Q19 折起四棱锥）均登记 `expected_occurrences=2`，头注写明来源路径与 SHA-256。
- 关键结论：选择 C A D B B C B A；填空 9=1/9、10=1/2、11 x=−5/4、12 直线 n(n+1)/2、f(4)=12、f(n)=n(n−1)(n−2)/2、13 (0,2) 与 2√2、14 6 与 [−1,1]、15 30° 与 3；Q16 sinA=2√5/5、c>25/3；Q17 ŷ=0.7x+0.35、降低 19.65 吨；Q18 (x+2)²+(y−2)²=8、Q(4/5,12/5)；Q19 V=3√6x−x³/(6√6)、x=6 时 Vmax=12√6、cos=1/7；Q20 a≤−(3+√7)/2 或 a≥1；Q21 α=(√5−1)/2、β=−(√5+1)/2、Sₙ=2(2ⁿ−1)ln((3+√5)/2)。
- 图稿与版式修正：Q4 (D) 经像素比对确认第二段约 2.75 h 到 140，答案 B；四联图缩小并收紧行距，印刷版第 1 页题干与四图不再分页；Q6 流程图重画返回路径，消除“否”分支压输出框；Q12 隐藏顶点 E 重排并放大；Q15 直角标记改用单位向量作正方形；Q19 D 标签上移。印刷版第 6 题图 1 与图 2 分居第 9/10 页，已按“双图题块成组换页”登记。
- 门禁全通过：`review_receipts check-all`（326 批次）、`provenance check-all`（480 卷）、`solution_sources check-all`、`validate-receipts`（480 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（480 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记。
- 下一步：继续 2007 年其余 ready 来源（新课标文理、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 广东文科（phase5-b09）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 广东文科（21 题，`gk-2007-regular-guangdong-arts`）`phase5-b09` FINALIZED / `closed`，卷 `eligible_complete`，manifest live revision 7791，attempt `fc995812-f170-4a9c-88e2-c8b2f5e290ec`；四版 7/26/9/23 页共 65 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b09.md`。
- 六幅 TikZ 图（Q5 四联 s–t 图、Q7 条形统计图与算法流程图、Q10 维修点环形图、Q15 圆与切线、Q17 俯视图）均登记 `expected_occurrences=2`，头注写明来源路径与 SHA-256。
- 关键结论：选择 C D B B C D B A A C；填空 11 y²=8x、12 (1/e,+∞)、13 aₙ=2n−10 且 k=8、14 2、15 30°；Q16 c=25/3、2√5/5；Q17 V=64、S=40+24√2；Q18 ŷ=0.7x+0.35、降低 19.65 吨；Q19 (x+2)²+(y−2)²=8、Q(4/5,12/5)；Q20 α=(√5−1)/2、β=−(√5+1)/2、Sₙ=2(2ⁿ−1)ln((3+√5)/2)；Q21 a≤−(3+√7)/2 或 a≥1。
- 图稿三处返工：Q5 四联图 `shift` 必须写 `(0cm,-7.2cm)`（y 单位 0.032cm，无单位数值会被缩放导致四图重叠）；Q7 条形图柱区间改 `[i,i+1]` 并与 145–195 的 11 个分界标签对齐；Q7 流程图 `i=i+1` 移到 `s=s+A_i` 上方并回接判断框上方。Q10 环序为 A—D—C—B（与源图一致）。
- 版式修正：试题版 Q8 曾被拆页，源 MD 加 `question-needspace: 0.35` 后整题同页；Q9 四个连续 `\dfrac` 选项改为 `\frac`，行距恢复。两次改动均重跑 provenance（revision 7786、7789）。
- 门禁全通过：`review_receipts check-all`（325 批次）、`provenance check-all`（479 卷）、`solution_sources check-all`、`validate-receipts`（479 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（479 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记。
- 下一步：继续 2007 年其余 ready 来源（广东理、新课标文理、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 山东文科（phase5-b08）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 山东文科（22 题，`gk-2007-regular-shandong-arts`）`phase5-b08` FINALIZED / `closed`，卷 `eligible_complete`，manifest live revision 7778，attempt `44cf07ad-161e-41eb-ad62-27e8a6dd41dc`；四版 5/24/7/18 页共 54 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b08.md`。
- 四幅 TikZ 图（Q3 四个几何体、Q8 频率分布直方图、Q10 程序框图、Q20 直四棱柱）均登记 `expected_occurrences=2`，头注写明来源路径与 SHA-256；Q3/Q8/Q10 复用理科版结构、Q20 按文卷条件独立重绘。
- 关键结论：选择 B B D A C B C A B A B D；填空 13=1/2007、14=4、15=m≤−5、16=(x−2)²+(y−2)²=2；Q17 cosC=1/8、c=6；Q18 aₙ=2ⁿ⁻¹、Tₙ=(3/2)n(n+1)ln2；Q19 甲 100 分钟、乙 200 分钟、最大收益 70 万元；Q20(2) E 为 DC 中点；Q21 ab>0 无极值、ab<0 唯一极值；Q22 x²/4+y²/3=1、定点 (2/7,0)。
- 分页说明：解析版第 8 题题干+直方图在第 11 页、选项在第 12 页页首；简答版答案速查区分组换页（第 6 页选择/填空、第 7 页解答题）；均按模板正常换页登记。
- 门禁全通过：`review_receipts check-all`（324 批次）、`provenance check-all`（478 卷）、`solution_sources check-all`、`validate-receipts`（478 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（478 套）、`manifest_csv`（775 行）。
- 下一步：继续 2007 年其余 ready 来源（广东文理、新课标文理、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 山东理科（phase5-b07）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 山东理科（22 题，`gk-2007-regular-shandong-science`）`phase5-b07` FINALIZED / `closed`，卷 `eligible_complete`，manifest live revision 7773，attempt `d3183365-a84f-47fd-b2c4-85aa91ad9b1d`；四版 6/32/8/26 页共 72 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b07.md`。
- 五幅 TikZ 图（Q3 四个几何体、Q8 频率分布直方图、Q10 程序框图、Q19 直四棱柱、Q20 两船方位图）均登记 `expected_occurrences=2`，头注写明来源路径与 SHA-256。
- 关键结论：选择 D B D A A B C A D D C B；填空 13=√21 p/2、14=4√2、15=(x−2)²+(y−2)²=2、16=8；Q17 aₙ=3⁻ⁿ、Sₙ=(3+(2n−1)3ⁿ⁺¹)/4；Q18 19/36、Eξ=1、7/11；Q19(2) √3/3；Q20 30√2 海里/时；Q21 x²/4+y²/3=1、定点 (2/7,0)；Q22 按 b 四段讨论极值点。
- 版式修正：Q8 用 `question-needspace: 0.5` + 直方图 scale 1.15 回到试题版第 2 页；Q19 图放大到 1.35 并移动 A/B 标签；Q17 判断要点的行内分式改为 `(3+1·9)÷4=3`。
- 源缺陷照录并登记：`ISSUE-1458`（Q9① 印作 m<2，应为 m<−2，non_blocking），按选项设置取 D。
- 门禁全通过：`review_receipts check-all`（323 批次）、`provenance check-all`（477 卷）、`solution_sources check-all`、`validate-receipts`（477 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（477 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记。
- 下一步：继续 2007 年其余 ready 来源（山东文、广东文理、新课标文理、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 安徽文科（phase5-b06）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 安徽文科（21 题，`gk-2007-regular-anhui-arts`）`phase5-b06` FINALIZED / `closed`，卷 `eligible_complete`，manifest live revision 7753，attempt `d51e753b-f41b-45a0-add3-a46b4466779b`；四版 5/25/7/18 页共 55 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b06.md`。
- 两幅 TikZ 图（Q7 折线图象、Q17 六面体）均登记 `expected_occurrences=2`；Q17 与安徽理同源几何，按文科原页重绘。
- 关键结论：选择 D A C D C A B B A C D；填空 12=−256、13=−½a+¾b+¼c、14=3/11、15=①②③；Q16=(0,2/3)；Q17(3)=arccos(−1/5)；Q18 切线 y=±2x−4 且面积最小值 32；Q19 1/28、3/28；Q20 g(t)=4t³−3t+3、极大 4 极小 2；Q21 递推式与等比/等差拆分（初稿第二项求和中间式已修正为 (qⁿ−nq+n−1)/(q−1)²）。
- 源缺陷照录并登记：`ISSUE-1456`（Q13 首项 AB vs OA）、`ISSUE-1457`（Q21「储务金」），均 non_blocking，源疑点写进解析内。
- 门禁全通过：`review_receipts check-all`（322 批次）、`provenance check-all`（476 卷）、`solution_sources check-all`、`validate-receipts`（476 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（476 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记：Q12 选项冲突、Q17 疑字、Q19 条件不足（有反例）、Q21 缺等号，均不得据常见题意修补。
- 下一步：继续 2007 年其余 ready 来源（山东文理、广东文理、新课标文理、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 安徽理科（phase5-b05）封账，卷 complete

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 安徽理科（21 题，`gk-2007-regular-anhui-science`）`phase5-b05` FINALIZED / `closed`，卷 `eligible_complete`，manifest live revision 7746，attempt `b4de5fcc-1707-435f-8bca-7d2871a7a142`；四版 6/27/8/21 页共 62 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b05.md`。
- 四幅 TikZ 图（Q9 双曲线与圆、Q14 抛物线分点、Q17 六面体斜投影、Q19 抛物线 y²=2x 关系图）均登记 `expected_occurrences=2`，头注写明来源路径与 SHA-256。首轮审查发现 Q14 右端 `P_{n-1}` 标签被斜边穿过，把两个右端分点标签移到 x 轴下方后重建并复查改动页。
- 关键裁定：Q2 为充分不必要条件（选 A，solve-b 的 B 属蕴含方向倒置）；Q13 按 300% 放大确认首项为 $\overrightarrow{AB}$，答案 $-\frac12\boldsymbol a+\frac34\boldsymbol b+\frac14\boldsymbol c$；Q16 按「同角」处理得 $2m+4$；Q17(3) 二面角 $\arccos(-1/5)\approx101.54^\circ$。
- 源缺陷按原页照录并登记：`ISSUE-1452`（Q9 印作 r²）、`ISSUE-1453`（Q13 AB vs OA）、`ISSUE-1454`（Q16 拉丁 a 与希腊 α 混用）、`ISSUE-1455`（Q21「储务金」），全部 non_blocking，源疑点写进解析内。
- 门禁全通过：`review_receipts check-all`（321 批次）、`provenance check-all`（475 卷）、`solution_sources check-all`、`validate-receipts`（475 卷）、`report render/check --all`、`generate_projects/make_short_answers/make_editions --all --check`（475 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记：Q12 选项冲突、Q17 疑字、Q19 条件不足（有反例）、Q21 缺等号，均不得据常见题意修补。
- 下一步：继续 2007 年其余 ready 来源（安徽文、山东文理、广东文理、新课标文理、江苏、江西文理、浙江文理、湖北文理、湖南文理、福建文理、辽宁文理、重庆文理、陕西文理等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 四川理科（phase5-b04）封账，卷 blocked

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 四川理科（22 题，`gk-2007-regular-sichuan-science`）`phase5-b04` FINALIZED / `closed_with_blockers`，卷 `eligible_blocked`，manifest revision 7741，attempt `daf060bf-9bcb-42fe-a78a-0ef096602e5e`；四版 7/30/9/22 页共 68 页，0 errors、0 overfull、0 missing characters，八类视觉检查逐页 0 fail / 0 pending / 0 豁免；报告 `reports/phase5-b04.md`。
- 六幅 TikZ 图（Q2 四选项、Q4 正方体、Q6 球面、Q11 三平行线、Q14 正三棱柱、Q19 直角梯形）均登记 `expected_occurrences=2`，头注写明真实来源路径与 SHA-256。
- 阻断项 `ISSUE-1450`：第 11 题四选项无一与独立推导 `2√21/3≈3.055` 相符（(C)≈0.089、(D)≈−0.861 为负或近零，(D) 疑漏根号），速查表记 `U`、不代选；另有「仅凭文字条件不唯一（同侧时 s=2），必须依赖原图」的第二层缺陷，已写入解析内 `【源疑点：…】`。非阻断项 `ISSUE-1449`（Q1 (B)(D) 均印作 1）、`ISSUE-1451`（Q12 (D) 印作 5/25 未约分）按原页照录。
- 其他裁定：Q13 参数为 $u$ 不是 $a$；Q22(3) 题设已限定 $n>1$，故在 $n\ge2$ 上 $a=2$ 存在且唯一，$n=1$ 边界仅在括注说明。
- 门禁全通过：`validate-receipts`、`provenance check-batch`、`solution_sources check-batch`、`report render/check --all`、`generate_projects --all --check`（474 套）、`make_short_answers --all --check`（474 套）、`manifest_csv`（775 行）。
- 2007 四川文科候选仍为 `pending-intake/2007/sichuan-arts`，未登记：Q12 选项冲突、Q17 疑字、Q19 条件不足（有反例）、Q21 缺等号，均不得据常见题意修补。
- 下一步：继续 2007 年其余 ready 来源（2006 尚有 15 套、2003 六套、2000 六套等），逐卷走同一流水线；全库仍未完成。

## 2026-11-10 接续：2007 天津文/理（phase5-b02、b03）封账

- 工作树与分支保持 `phase0-wt` / `feat/gaokao-phase0`，未动 main、未 push。
- 2007 上海理科（21题）`phase5-b01` 已封账（revision 7719，attempt `91828da8-…-66c677f8`，四版 4/15/6/13 页），全量 unittest 修复已提交 `b9e083d3d`。
- 2007 天津理科（22题，`gk-2007-regular-tianjin-science`）`phase5-b02` FINALIZED/closed，revision 7722，attempt `27ddfd9b-d753-421d-8f19-8ff81431194e`；四版 5/25/7/19 页共 56 页 0 fail/pending，解析版 2 条 Overfull 已逐项豁免。
- 2007 天津文科（22题，`gk-2007-regular-tianjin-arts`）`phase5-b03` FINALIZED/closed，revision 7736，attempt `0e644cd1-c933-4206-b40c-bb941eb8060e`；四版 5/26/7/20 页共 58 页 0 fail/pending，解析版 1 条 5.77pt Overfull 已豁免。首轮构建的解析版 Q4 公式超版心 100.44pt 已改为 `aligned` 三行修掉（属真实缺陷，未走豁免）。
- 两卷来源与解答均为「官方身份未核 / 非官方独立推导」边界。读法疑点留证：理卷 Q15 `AB=2AC=1` 读作 AB=1、AC=1/2（−2/3），Q16 按 1×4 长条读作 390；文卷 Q16 题面另要求两端不同色 → 按环 C₄ 得 630（与理卷 390 区分）。文卷另有三处源疑点（Q1、Q11 缺逗号、Q12 裁切）按原页照录。
- 2007 四川文科草稿位于 `pending-intake/2007/sichuan-arts`，未登记；Q12选项冲突、Q17疑字、Q19条件不足（已核原页并构造反例）、Q21方程残缺均不得自行补写。
- 下一步：继续 2007 年尚未绑定来源（四川文、其余省市），逐卷走同一流水线。全库尚未完成，不以单卷替代 1952—2026 目标。


## 当前状态（2026-11-09，2005 年封年后）

- 分支：`feat/gaokao-phase0`（worktree `仓库根`），只在此分支推进，不 push。
- 2005 年：32 套中 29 套 `complete`，3 套 `blocked`（全国1理 ISSUE-0834；上海文 ISSUE-1377/1379；上海理 ISSUE-1380/1381），阻断理由与 `resume_action` 见 `math-gaokao-latex/missing-issues.md`。
- 本阶段封账批次：b94 辽宁、b95 江苏、b96 全国Ⅲ文、b97 全国Ⅲ理、b98 浙江文、b99 浙江理；春季 3 套复核无需重做。
- 全量门禁：`generate_projects --all --check`、`manifest_csv --check`、`report.py render/check --all`、`review_receipts check-all`（`FINALIZED：316 批次`）全部通过；316 批为 2026-11-09 按当前视觉工具指纹重建重审后的结果，其回执证据以构建回执 + `pdftotext` 文本层核对为主，逐页接触印样仅覆盖部分版本。
- 下一步：按年份继续 2006 起的 ready 来源；或为尚无接触印样的版本补渲染审阅（当前 1880 个版本中约 88.9% 仅有文本层核对）。
更新时间：2026-11-09（中国标准时间）

> **当前接续以最新状态小节为准。** 后面的按阶段记录保留当时快照；新会话须读取 live manifest、回执、最新 `PROGRESS.md` 与 Git 状态。

## 2026-11-08 当前状态：phase4-b93 2005 福建理科卷收口，全库 464 套试卷确定性 TeX 投影 100% 一致

### 工作位置与 Git

- 只在规范 worktree `仓库根`、分支 `feat/gaokao-phase0` 继续；phase4-b93 已收口，接续时以 live `git log` 核对提交号。本轮 `git worktree list` 只有既存的 `主工作树`（`main`）和规范 feature worktree，没有新增项。`main` 上用户文件未触碰。不要新建 worktree、切到 `main` 或 push；接续时重新核对实时状态。
- 当前续接目标是继续1952—2026题库，不以单卷结案替代总目标。

### 最近完成：phase4-b93

- `gk-2005-regular-fujian-science`，22 题（选择 1–12、填空 13–16、解答 17–22）；固定来源 `src-a3cf296b65edd3890eb214591c50e36784194dc86d9983c5b04b9c064455548f`，上游 `普通高考/2005/2005福建理.pdf`（两页 A3 横向扫描排印，原卷印刷页码 224、225，印刷题签“2005 普通高等学校招生考试 (福建卷理)”，科类登记 `track=science`）。
- 排印质量与独立复算：PDF 题面第 1 页包含 Q1–Q18，第 2 页包含 Q19–Q22；全卷 22 题题面、选项与结构严谨完备。Q01 复数除法与共轭复数（选 B）；Q02 等差数列通项 $a_{12} = 15$（选 A）；Q03 直角三角形向量垂直求参数 $k = 5$（选 A）；Q04 空间线面平行垂直命题判定 2 个（②③，选 C）；Q05 指数函数图象递减与截距判断参数 $0 < a < 1, b < 0$（选 D）；Q06 正弦波峰与零点确定参数 $\omega = \frac{\pi}{4}, \varphi = \frac{\pi}{4}$（选 C）；Q07 绝对值不等式与二次不等式充要条件判定为充分不必要条件（选 A）；Q08 长方体建立坐标系计算异面直线垂直 $\frac{\pi}{2}$（选 D）；Q09 受限位置排列组合方案数 $240$ 种（选 B）；Q10 正三角形中点双曲线离心率 $e = \sqrt{3} + 1$（选 D）；Q11 柯西不等式求条件最值 $-3$（选 C）；Q12 奇函数周期性求区间零点最小个数 5 个（选 C）；Q13 二项式定理常数项 $240$；Q14 退化可行域目标函数最大值 $0$；Q15 等比数列和式极限 $\frac{1}{b-1}$；Q16 对称变换反函数真命题补充（关于 $y = x$ 对称得 $2^{x-3}$）；Q17 三角同角平方关系化简 $\sin x - \cos x = -\frac{7}{5}$ 与代数式求值 $-\frac{108}{125}$；Q18 离散随机变量数学期望 $\mathbf{E}\xi = \frac{9}{10}$ 与四次投球至少命中一次对立概率 $\frac{91}{100}$；Q19 分式函数切线待定系数解析式 $f(x) = \frac{2x - 6}{x^2 + 3}$ 与单调增减区间；Q20 直二面角性质定理证线面垂直、三垂线逆定理求二面角 $\arccos\frac{\sqrt{3}}{3}$、点面距离 $\frac{2\sqrt{3}}{3}$；Q21 椭圆焦点与对称点求标准方程 $\frac{x^2}{6} + \frac{y^2}{2} = 1$、割线三角形面积转化求直线方程唯一解 $x = -2$；Q22 分式递推数列逆推 $a_4 = 0 \iff a = -\frac{2}{3}$、逆向映射有穷数列证明、正向不变集归纳证明 $a > 0$。全部独立推导闭环，评定为 `eligible_complete`。
- 规范事实层建立：四层 Markdown（`_试题.md`、`_答案要点.md`、`_解析正文.md`、`_含解析.md`），来源接收报告落盘至 `reports/2005-fujian-science-source-intake.md`；重绘并挂接 4 张高保真 TikZ 纯矢量图（`f2005_fujian_science_q05_exp.tex`、`f2005_fujian_science_q06_trig.tex`、`f2005_fujian_science_q08_cuboid.tex`、`f2005_fujian_science_q20_stereometry.tex`）。
- 确定性 TeX 投影与入口生成：通过 `generate_projects.py`、`make_short_answers.py`、`make_editions.py` 生成 `questions.tex`、`answers.tex`、`answers_short.tex` 及四版入口。
- 逐题 Provenance 审计与自动化回归：三角色共 66 条记录确定性导入，22 题全通过，conflict_status=none，issue_ids=[]；新增 `tests/test_2005_fujian_science_solutions.py` 自动化回归套件，全卷 22 题推导与关键数学结论 100% 锁死。
- 正式构建与视觉审查：试题/解析/简答/印刷版分别为 4/31/6/22 页，共 63 页；四版均 `succeeded`，0 errors、0 missing characters、0 overfull、0 undefined references、0 problems。全 63 页共 504 项八类视觉检查全部通过（0 fail、0 pending）。
- 批次封账与报告同步：`review_receipts.py finalize-batch` 返回 `FINALIZED`，批次 `closed`、卷 `eligible_complete`，生成报告 `reports/phase4-b93.md`。`report.py render --all` 更新 6 个全量报告，`report.py check --all` 校验通过，`manifest_csv.py` 生成 775 行并通过 check。全量 464 套试卷 TeX 投影 100% 一致。2005 年福建卷文理双科大圆满收口！
- 下一步推荐推进：推进 2005 年辽宁卷（`2005辽宁.pdf`）或 2005 江苏卷（`2005江苏.pdf`，下一批次 `phase4-b94`）！

### 之前完成：phase4-b92

- `gk-2005-regular-fujian-arts`，22 题；详情参见 `PROGRESS.md`。四版共 62 页，`FINALIZED`，已闭环。全量 463 套试卷 TeX 投影一致。2005 年福建文科卷大圆满收口！

### 之前完成：phase4-b91

- `gk-2005-regular-chongqing-science`，22 题；详情参见 `PROGRESS.md`。四版共 61 页，`FINALIZED`，已闭环。全量 462 套试卷 TeX 投影一致。2005 年重庆卷文理双科大圆满收口！

### 之前完成：phase4-b90

- `gk-2005-regular-chongqing-arts`，22 题；详情参见 `PROGRESS.md`。四版共 55 页，`FINALIZED`，已闭环。全量 461 套试卷 TeX 投影一致。2005 年重庆卷文理双科大圆满收口！

### 之前完成：phase4-b89

- `gk-2005-regular-guangdong`，20 题；详情参见 `PROGRESS.md`。四版共 55 页，`FINALIZED`，已闭环。全量 460 套试卷 TeX 投影一致。2005 年广东卷大圆满收口！

### 之前完成：phase4-b88

- `gk-2005-regular-hunan-science`，21 题；详情参见 `PROGRESS.md`。四版共 65 页，`FINALIZED`，已闭环。全量 459 套试卷 TeX 投影一致。2005 年湖南卷文理双科大圆满收口！

### 之前完成：phase4-b87

- `gk-2005-regular-hunan-arts`，21 题；详情参见 `PROGRESS.md`。四版共 62 页，`FINALIZED`，已闭环。全量 458 套试卷 TeX 投影一致。2005 年湖南卷文理双科大圆满收口！

### 之前完成：phase4-b86

- `gk-2005-regular-hubei-science`，22 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环。全量 457 套试卷 TeX 投影一致。2005 年湖北卷文理双科大圆满收口！

### 之前完成：phase4-b85

- `gk-2005-regular-hubei-arts`，22 题；详情参见 `PROGRESS.md`。四版共 64 页，`FINALIZED`，已闭环。全量 456 套试卷 TeX 投影一致。2005 年湖北卷文理双科大圆满收口！

### 之前完成：phase4-b84

- `gk-2005-regular-jiangxi-science`，22 题；详情参见 `PROGRESS.md`。四版共 70 页，`FINALIZED`，已闭环。全量 455 套试卷 TeX 投影一致。2005 年江西卷文理全科大圆满收口！

### 之前完成：phase4-b83

- `gk-2005-regular-jiangxi-arts`，22 题；详情参见 `PROGRESS.md`。四版共 61 页，`FINALIZED`，已闭环。全量 454 套试卷 TeX 投影一致。

### 之前完成：phase4-b82

- `gk-2005-regular-shandong-science`，22 题；详情参见 `PROGRESS.md`。四版共 61 页，`FINALIZED`，已闭环。全量 453 套试卷 TeX 投影一致。2005 年山东卷文理双科均已大圆满收口！

### 之前完成：phase4-b81

- `gk-2005-regular-shandong-arts`，22 题；详情参见 `PROGRESS.md`。四版共 60 页，`FINALIZED`，已闭环。全量 452 套试卷 TeX 投影一致。2005 年山东卷文理双科均已大圆满收口！

### 之前完成：phase4-b80

- `gk-2005-regular-tianjin-science`，22 题；详情参见 `PROGRESS.md`。四版共 67 页，`FINALIZED`，已闭环。全量 451 套试卷 TeX 投影一致。2005 年天津卷文理双科均已大圆满收口！

### 之前完成：phase4-b79

- `gk-2005-regular-tianjin-arts`，23 题；详情参见 `PROGRESS.md`。四版共 66 页，`FINALIZED`，已闭环。全量 450 套试卷 TeX 投影一致。2005 年天津卷文理双科均已大圆满收口！

### 之前完成：phase4-b78

- `gk-2005-regular-beijing-science`，20 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环。全量 449 套试卷 TeX 投影一致。2005 年北京卷文理双科均已大圆满收口！

### 之前完成：phase4-b77

- `gk-2005-regular-beijing-arts`，20 题；详情参见 `PROGRESS.md`。四版共 58 页，`FINALIZED`，已闭环。全量 448 套试卷 TeX 投影一致。2005 年北京卷文理双科均已大圆满收口！

### 之前完成：phase4-b76

- `gk-2004-regular-chongqing-science`，22 题；详情参见 `PROGRESS.md`。四版共 62 页，`FINALIZED`，已闭环。全量 447 套试卷 TeX 投影一致。2004 年全部自主命题卷 100% 彻底大圆满封账！

### 之前完成：phase4-b75

- `gk-2004-regular-chongqing-arts`，22 题；详情参见 `PROGRESS.md`。四版共 64 页，`FINALIZED`，已闭环。全量 446 套试卷 TeX 投影一致。

### 之前完成：phase4-b74

- `gk-2004-regular-hunan-science`，22 题；详情参见 `PROGRESS.md`。四版共 73 页，`FINALIZED`，已闭环。全量 445 套试卷 TeX 投影一致。

### 之前完成：phase4-b73

- `gk-2004-regular-hunan-arts`，22 题；详情参见 `PROGRESS.md`。四版共 61 页，`FINALIZED`，已闭环。全量 444 套试卷 TeX 投影一致。

### 之前完成：phase4-b72

- `gk-2004-regular-hubei-science`，22 题；详情参见 `PROGRESS.md`。四版共 66 页，`FINALIZED`，已闭环。全量 443 套试卷 TeX 投影一致。

### 之前完成：phase4-b71

- `gk-2004-regular-hubei-arts`，22 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环。全量 442 套试卷 TeX 投影一致。

### 之前完成：phase4-b70

- `gk-2004-regular-fujian-arts`，22 题；详情参见 `PROGRESS.md`。四版共 67 页，`FINALIZED`，已闭环。全量 441 套试卷 TeX 投影一致。

### 之前完成：phase4-b69

- `gk-2004-regular-fujian-science`，22 题；详情参见 `PROGRESS.md`。四版共 66 页，`FINALIZED`，已闭环。全量 440 套试卷 TeX 投影一致。

- `gk-2004-regular-zhejiang-arts`，22 题；详情参见 `PROGRESS.md`。四版共 58 页，`FINALIZED`，已闭环。全量 439 套试卷 TeX 投影一致。

### 之前完成：phase4-b67

- `gk-2004-regular-zhejiang-science`，22 题；详情参见 `PROGRESS.md`。四版共 72 页，`FINALIZED`，已闭环。全量 438 套试卷 TeX 投影一致。

### 之前完成：phase4-b66

- `gk-2004-regular-liaoning`，22 题；详情参见 `PROGRESS.md`。四版共 62 页，`FINALIZED`，已闭环。全量 437 套试卷 TeX 投影一致。

### 之前完成：phase4-b65

- `gk-2004-regular-jiangsu`，22 题；详情参见 `PROGRESS.md`。四版共 54 页，`FINALIZED`，已闭环。全量 436 套试卷 TeX 投影一致。

### 之前完成：phase4-b64

- `gk-2004-regular-guangdong`，22 题；详情参见 `PROGRESS.md`。四版共 56 页，`FINALIZED`，已闭环。全量 435 套试卷 TeX 投影一致。

### 之前完成：phase4-b63

- `gk-2004-regular-tianjin-science`，22 题；详情参见 `PROGRESS.md`。四版共 68 页，`FINALIZED`，已闭环。全量 434 套试卷 TeX 投影一致。

### 之前完成：phase4-b62

- `gk-2004-regular-tianjin-arts`，22 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环。全量 433 套试卷 TeX 投影一致。

### 之前完成：phase4-b61

- `gk-2004-regular-beijing-science`，20 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环。全量 432 套试卷 TeX 投影一致。

### 之前完成：phase4-b60

- `gk-2004-regular-beijing-arts`，20 题；详情参见 `PROGRESS.md`。四版共 60 页，`FINALIZED`，已闭环。全量 431 套试卷 TeX 投影一致。

### 之前完成：phase4-b59

- `gk-2004-regular-national-4-science`，22 题；详情参见 `PROGRESS.md`。四版共 55 页，`FINALIZED`，已闭环。全量 430 套试卷 TeX 投影一致。

### 之前完成：phase4-b58

- `gk-2004-regular-national-4-arts`，22 题；详情参见 `PROGRESS.md`。四版共 52 页，`FINALIZED`，已闭环。

### 之前完成：phase4-b57

- `gk-2004-regular-national-3-science`，22 题；详情参见 `PROGRESS.md`。四版共 50 页，`FINALIZED`，已闭环。

### 之前完成：phase4-b56

- `gk-2004-regular-national-3-arts`，22 题；详情参见 `PROGRESS.md`。四版共 47 页，`FINALIZED`，已闭环。

### 之前完成：phase4-b55

- `gk-2003-regular-liaoning`，22 题；详情参见 `PROGRESS.md`。四版共 58 页，`FINALIZED`，已闭环。1952–2003 年整整 52 年的高考数学真题实现 100% 全量覆盖。

### 之前完成：phase4-b54

- `gk-2003-regular-henan`，22 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环。

### 之前完成：phase4-b53

- `gk-2003-regular-jiangsu`，22 题；详情参见 `PROGRESS.md`。四版共 67 页，`FINALIZED`，已闭环。

### 之前完成：phase4-b52

- `gk-2003-regular-yuegui`，22 题；详情参见 `PROGRESS.md`。四版共 62 页，`FINALIZED`，已闭环（保留 blocker ISSUE-1429）。

### 之前完成：phase4-b51

- `gk-1998-regular-national-arts`，25 题；详情参见 `PROGRESS.md`。四版共 63 页，`FINALIZED`，已闭环（保留 blocker）。1952–2002 年 50 年真题实现 100% 完整覆盖。

### 之前完成：phase0-b08

- `gk-2018-regular-beijing-science`，20题；详情参见 `PROGRESS.md`。四版共45页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase0-b07

- `gk-2018-regular-beijing-arts`，20题；详情参见 `PROGRESS.md`。四版共44页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase4-b41

- `gk-2015-regular-shaanxi-science`，24题；详情参见 `PROGRESS.md`。四版共52页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase1-b53

- `gk-2009-spring-shanghai`，21题；详情参见 `PROGRESS.md`。四版共43页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase1-b50

- `gk-2017-regular-shanghai`，21题；详情参见 `PROGRESS.md`。四版共46页，`FINALIZED`，已闭环。

### 之前完成：phase1-b40

- `gk-2018-spring-shanghai`，21题；详情参见 `PROGRESS.md`。四版共48页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase1-b39

- `gk-2007-regular-beijing-science`，20题；详情参见 `PROGRESS.md`。四版共44页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase4-b12

- `gk-2017-spring-shanghai`，21题；详情参见 `PROGRESS.md`。四版共41页，`FINALIZED`，已闭环（保留 blocker）。

### 之前完成：phase3-b01

- `gk-2016-spring-shanghai`，36题；详情参见 `PROGRESS.md`。四版共64页，`FINALIZED`，已闭环。

### 之前完成：phase2-b22

- `gk-2016-regular-zhejiang-arts`，20题；详情参见 `PROGRESS.md`。四版共42页，`FINALIZED`，已闭环。

### 之前完成：phase2-b21

- `gk-2016-regular-zhejiang-science`，20题；详情参见 `PROGRESS.md`。四版共49页，`FINALIZED`，已闭环。

### 之前完成：phase2-b20 至 phase2-b17

- 均已收口（包含2016山东文科 b20、山东理科 b19、天津文科 b18、天津理科 b17）。各批详情参见 `PROGRESS.md`。

### 之前完成：phase2-b16

- `gk-2016-regular-sichuan-arts`，21题；source `src-18b75fe448bbe7811db6e6ba5fc5130b950fc40ba251c916bdbf940647ce5ac4`，manifest 记录 PDF SHA-256 `7bdfb3dd1a6547dea9e5e372f2538604a37fe44c5a4342f17367d5d035fff19f`、2页。原 PDF 当前不在 worktree/HEAD；本次未声称重新核对原 PDF。答案解析为非官方独立推导，题面疑点照 manifest 注记保留。
- build attempt `6bbc0630-56ae-4720-912f-618874c191e1`，输入 manifest revision 6320，四版页数5/23/7/18，共53页。四版 PDF SHA-256 与逐页检查明细见 `math-gaokao-latex/2016_四川卷_文科/receipts/` 及 `reports/phase2-b16.md`。视觉检查424项：384 pass、40 not_applicable、0 fail；`finalize-batch`=`FINALIZED`，最终 manifest revision 6322、batch `closed`、paper `complete`、无问题。
- batch currentness、provenance、TeX/简答/四版入口生成、21题 solution sources、全量 report render/check、manifest CSV（775行）均通过。完整测试 `Ran 1781 tests in 729.733s`，13 skipped、1 failure：`test_the_cached_states_match_the_recomputed_ones` 报23卷缓存 `production_state` 漂移，首项 phase2-b17 `gk-2016-regular-tianjin-science`（缓存 complete、派生 answers_verified）；尚未修复或批量回写。

### 之前完成：phase2-b13

- `gk-2016-regular-beijing-arts`，20题；source `src-ecf09b64f30a39442d38dc7cc78ae41e3b5138c23a4ddb059f098ac5816543bf`，固定 PDF SHA-256 `f25691253d50ee9aae94243518695e8e7793e32e4b3f22077c9bf6407272d89e`，印刷页995–996。固定源仅含题面，答案/解析为独立编者推导、非官方；Q8 的答案歧义仍标 `U`，ISSUE-1005 阻塞内容完成。
- build attempt `961e27fb-5508-4457-ba18-e88b5dbe66f1`，输入 manifest revision 6312，build 后 6313，finalize 后 6314。试题/解析/简答/印刷版5/21/7/17页，共50页；均 succeeded，TeX errors、missing characters、overfull、undefined references、problems 均为0。PDF SHA-256：`6d2c5692ef44c5f00ccd41dcf0ff9119d1cf7701d84fd809ab6878a3871ef7b7`、`f0a9d823cb6e064cb4fcf58d81a8fafb0a12322868cf02933a33e58da6f617c7`、`564ca6b3777cd708ba5c551f55742dfdcf38e588e137b9a3c258b78f9ca3014e`、`f08fea745376bc49b88f18eb8cf1e62c8ef8e752c6f4c4b444ced3c7002d1bbf`。
- 50页视觉检查400项：338 pass、62 not_applicable、0 fail。复核纠正了解析版的页眉误报、简答版第5页页眉误报，并将试题版总结果设为 pass。`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`；solution sources、provenance、生成器、build receipts、全量报告 render/check 通过。投影提交 `9d0d277`，正式构建提交 `c20f875`；收口回执、报告及进度/交接记录已分阶段提交。

### 当前门禁与接续

- 最近完整测试 `Ran 1781 tests in 729.183s`，13 skipped、1 failure；唯一失败为全库21卷缓存状态与现场 provenance 推导不一致，首项 phase2-b18 `gk-2016-regular-tianjin-arts`（缓存 `complete`、派生 `answers_verified`）。先只读审计状态派生规则，再决定如何修复；不要机械批量覆盖缓存。
- `generate_projects.py --all --check` 当前有26个过期 TeX 投影；下一批为 phase2-b18（2016天津文科）。phase2-b15 至 b17 已收口。不要运行 `--all --write`；先只检查并处理 b18，然后依照“干完一批先停工”停在该批结案。
- 全量报告输出由专用 CLI 刷新并通过 `report.py check --all`，`manifest.csv` 当前775行。b17 批次专项 build/review currentness、provenance、solution sources、source manifest、issues 校验通过；单卷收口不代表1952—2026语料完成。
- 全项目继续按小阶段提交并在阶段间保持工作区干净；不要把单卷或某一批写成1952—2026全库完成。

## 2026-11-05 历史快照：phase1-b46 2006 安徽理科（批次已结案，阻塞保留）

### 工作位置与 Git

- 只使用既有规范 worktree `仓库根` / `feat/gaokao-phase0`；未新建 worktree、未切 `main`、未 push。生成 TeX 阶段提交 `413d6ef1`，复核输入 build 阶段提交 `a773fa4`；本次视觉结案、报告投影、进度及交接记录为后续阶段提交。`主工作树` 是既有 `main` 工作树，本轮仅做过只读核查，没有改动。
- 用户要求本批完成后停工：phase1-b46 收口后不开始下一批。提交后确认 `feat/gaokao-phase0` 工作区干净，并确认 worktree 列表未新增项。

### Live manifest、来源与构建

- manifest revision `6267`；`phase1-b46`=`closed_with_blockers`，`gk-2006-regular-anhui-science`=`blocked`。固定题面 source `src-3aed0bc3d5875c8ce734b5b97f95992307ff56fc580067083caea214e3028675` / SHA-256 `dfdf163d47fa3f279288d7000e2dfb729c7d412c64f4aa3b082d242f6ca2b093`，2页题面、印刷页码276–277，无答案页；题签、发布者、版次、来源链及官方身份未核，`official_answer=null`。
- 本批仅同步确定性 TeX 选项投影，事实层题面、答案、解析、图稿和 provenance 未改。正式 build attempt `336a9737-b4a0-43c9-95d0-7413e37280f7`，输入 revision 6265、finalizer 后 revision 6267。试题/解析/简答/印刷版5/22/7/18页，共52页，均 succeeded。PDF SHA-256：试题 `c1df0cf3686405d832b132601d7e8d508cac5bf092396358345ad384aca3c04b`；解析 `594042a5dd76e165870dd76dc5aa08d360f6e148f20b6c43268a28ec807f2c5d`；简答 `fc5f3d144aedd6ec81ef104b268830a752de528ce4728d2ea8af37ff0587baf5`；印刷 `e63cd809174ddd7605bddb9c7903eaf308027252d095375c02906c1b8b9715c0`。文件级 PDF SHA 与前一 attempt 不同；以 Poppler 26.10.0、150 dpi 比较四版52页 PNG，全部字节相同，因此继承此前针对同图像页面完成的逐页检查结论。
- 当前52页八类视觉检查共416项：315 pass、101 not_applicable、0 fail（28项无题图、47项答案版的“答案泄漏”检查不适用、26项无选择题页面的选项对齐不适用）。四条 Underfull hbox 位于试题p2、解析p2/p12、简答p2，均已视觉检查并豁免；未发现视觉缺陷。`finalize-batch`=`FINALIZED`，review passed，但 batch/paper 因来源问题仍阻塞。

### 问题、校验与停止点

- `ISSUE-1219` 仍 `open / blocks_completion`：Q3 椭圆式在固定副本中缺可见等号及右侧，答案继续 `U/PENDING`。Wayback 可访问 EOL 2006-06-19 第1页图像捕获（HTTP 200，600×744，SHA-256 `4b670066dbb0c0f0b4e7281147f6b6003925df9223d29b7baee5a88be3d8f895`）；仅核对此第1页，未建立与固定两页 PDF 的同版关系或来源链。具体证据见 `reports/2006-anhui-science-q3-source-recheck-2026-11-02.md`。
- source manifest、issues、provenance、22题 solution sources、本批生成器检查、build currentness 和 review `check-batch` 均通过；全量报告 `render --all` / `check --all` 通过，manifest CSV 775行当前。全量测试 `python3 -B -m unittest discover -s tests -q`：`Ran 1780 tests in 584.074s`，`FAILED (failures=1, skipped=13)`。唯一失败 `test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones` 报47项跨卷 paper/batch 缓存与现场派生状态不一致，首项 `gk-2016-regular-national-2-arts`（缓存 `complete`、派生 `answers_verified`）；本批 provenance 检查通过，不批量刷新其他卷缓存。
- 当前结案 commit 后以 live `git status --short --branch`、`git log -1 --oneline` 和 `git worktree list` 为准。此批结束后停止，不继续剩余队列；单卷结案不表示1952—2026全库完成。

## 2026-11-05 历史快照：phase1-b42 2006 上海理科（批次已关闭）

### 工作位置与 Git

- 只使用现有规范 worktree `仓库根` / `feat/gaokao-phase0`；不新建 worktree、不切 `main`、不 push。TeX/构建阶段提交 `7a728be1` 已在分支；本次视觉结案回执、全量报告投影、`PROGRESS.md` 与本交接为结案阶段提交范围。
- `主工作树` 是原有 `main` 工作树，其中用户的 Lab3 文件仍有未提交改动；本任务未触碰。接续时先读 live Git 与 manifest，不凭历史快照切换目录。

### Live manifest、来源与构建

- manifest revision `6257`；`phase1-b42`=`closed`，`gk-2006-regular-shanghai-science`=`complete`，无 issue。固定题面 source `src-7f8706c4a44fd822ba2bb30b55a3f647f1fdf82d7805be1e62d4ee2030ebe4e6` / SHA-256 `0d035a931057065fdef8df4ae2019a97e9e95a04a98a6562df3cd02725e632b5`，2页题面、印刷页码328–329。发布者、版次、扫描链及官方身份未核；无答案页，答案与解析为独立编者推导、非官方。
- 本批只把 Q13/Q15/Q16 的项目 TeX 选项投影同步到现行生成器；事实层 Markdown、图稿与 provenance 未改。正式 build attempt `e5c24644-d7fc-4170-8aea-bb54fc0139bb`，输入 revision 6255、finalizer revision 6257。试题/解析/简答/印刷版4/18/6/14页，共42页；四版均 succeeded，errors、missing characters、overfull、undefined references、problems 均为0。PDF SHA-256：试题 `757e4288a3b876982ebd88b692d735d09c6d3653df3c20c4a8b8a95a93787bbe`；解析 `7e234170d3dfcf6f1c69b2b8736906be87358b7395329ec3d0f201a82a814d98`；简答 `352db78251b0987eee33fde11b5a92234fa840007787325336efe4f9a2d08546`；印刷 `38230c382ac802d304544fcc7d0067dd40b83b8db033f798662085a5013b04e9`。
- 旧 build attempt `70f8a767-2970-451f-b10b-d1dfd9feb86d` 的旧 review SHA-256 为 `884318c180706ab9ffd8f0bd0d817f12c26bc12a39b8290e23b6506ebef46658`。旧 PDF/PNG 没有归档；旧版 TeX/依赖取自提交 `7536c577`，按相同工具链重建作基线，历史 PDF 字节哈希不一致，不能写成旧 PDF 原件比较。150 dpi 下28/42页栅格与重建基线相同并继承旧回执 pass；14个变化页（试题p2；解析p2、p11–18；简答p2；印刷p2、p9–10）全尺寸检查。336项八类检查：332 pass、4 not_applicable、0 fail；警告豁免0。视觉审查报告 `reports/phase1-b42.md` 已结案。

### 校验、全库例外与接续点

- 本批 build currentness、review `check-batch`、provenance、生成器、简答、版本壳、22题 solution sources、manifest、issues 均通过；`manifest.csv` 775行当前。全量报告 `render --all` 与 `check --all` 均通过，报告保留全库未完成状态。
- 全量测试 `python3 -B -m unittest discover -s tests -q` 最终输出 `Ran 1780 tests in 582.123s`、13 skipped、1 failure。唯一失败 `test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones`，49项跨卷缓存状态漂移，首项 `gk-2016-regular-national-2-arts`（缓存 `complete` / 派生 `answers_verified`）；本批单独 provenance 检查通过，不批量刷新其他卷缓存。
- `generate_projects.py --all --check` 仍有67个 TeX 文件、35卷待同步；manifest 顺序中下一批有过期投影的是 `phase1-b45`（2006安徽文科，批次 `closed_with_blockers`）。后续应先核对该批 live 状态并按源题/答案阻塞保留不确定性，只处理实际过期目标，不运行 `--all --write`。
- 当前批结案提交后按“干完一批先停”停止。本批关闭不代表1952—2026总项目完成；下一会话先核对 branch、status、manifest 和此交接。

## 2026-11-05 历史快照：phase4-b14 2006 上海文科（批次已关闭）

### 工作位置与 Git

- 只使用现有 canonical worktree `仓库根` 与 `feat/gaokao-phase0`；不新建 worktree、不切 `main`、不 push。构建阶段提交 `49331ed4` 已在分支；视觉结案、全量投影、进度及本交接为本次待提交阶段。提交后核对分支干净。
- `主工作树` 是既有 `main` 工作树，不是高考任务工作区；其中的用户改动不要触碰。下一会话先核对指定 worktree、branch、status、HEAD 与 live manifest，不根据旧快照切换工作目录。

### Live manifest、内容与构建状态

- live manifest revision `6254`；`phase4-b14` 为 `closed`，paper `gk-2006-regular-shanghai-arts` 为 `complete`，无关联 issue。固定 source `src-99308f47f68d68564b8892365d9d5f2f0634fe95a4a3de74fa5be5fb5fcf9d23`，SHA-256 `1881e13e917febc73882254c59200be192286802042d650c82956f8901c2d174`。考试身份和官方参考答案已核验；原出版者、版次与本地 PDF 数字化来源链仍未知，不能称其为官方原件。
- 本阶段仅将 Q14/Q16 选项投影同步为 `gkopts`：Q14 两列、Q16 四列，题干/选项内容与顺序不变。事实层 Markdown、答案、解析、图稿和 provenance 未修改。旧 build attempt `2f878927-d037-441f-b6ff-0c8b21ab3699` 留在忽略目录 `.work/phase4-b14/baseline/2006_上海卷_文科/`；当前正式 build attempt `934b8b2c-1165-4660-8c0f-2f86b1a7ab87`，输入 revision `6252`，四版共43页（5/18/7/13），均 succeeded。PDF SHA-256：试题版 `73778442001104a50a6ee04e9c4ca26608c14596216033c103fa644fa8793759`；解析版 `d9bdfa4a8597cea92899034b8a11ea5442267c63bf0f3d6d767e1faf1edfb2ef`；简答版 `997af489bf4db40bdf9798d4f054bd50e0144666955f56db76b5cb54f29fbc06`；印刷版 `d980d38ba32175aae4c66a465bc3152db53920ae4bade18b6719d1ad2d71db29`。
- 同 Poppler 26.10.0、150 dpi 逐页比较时43页均出现像素变化；旧 PDF 嵌入 STSong/STHeiti，当前 PDF 嵌入 STSongti-SC Regular/Bold。逐页检查全部当前页面，接触表覆盖43页，重点页面另行全尺寸检查。八项共344项：320 pass、24 not_applicable（无图页）、0 fail。解析版第13页 Q15 的“的（　　）”短续行产生 Underfull hbox，当前源行282–283；已复核无重叠、越界或裁切，作为一条可读短行豁免。`reports/phase4-b14.md` 已更新。

### 校验、全库例外与下一步

- 本批 receipt currentness、provenance、生成器、简答、版本壳、22题 solution sources、source manifest、issues 均通过。`manifest.csv` 775行当前；全量 report render 成功，`report.py check --all` 确认与 manifest 一致。主验证汇总见 `math-gaokao-latex/PROGRESS.md`。
- 全量测试 `python3 -m unittest discover -s tests`：`Ran 1780 tests in 585.216s`，1 failure、13 skipped。唯一失败是 `test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones`：51卷缓存状态与现场派生状态不符，首项 `gk-2016-regular-national-2-arts`（缓存 `complete` / 派生 `answers_verified`）。本批单独 provenance 检查通过；不要批量刷新这些其他卷缓存。
- `generate_projects.py --all --check` 仍有69个生成文件、36卷不同步；按年份下一项为 `phase1-b42` / `gk-2006-regular-shanghai-science`（2006上海理科，卷状态 complete，只有 TeX 投影过期）。用户要求干完这一批先停，因此此处停止；下一次继续前重读 live state，再按独立阶段构建和复核，不运行 `--all --write`。整个题库目标仍是1952—2026，当前批次关闭不表示全库完成。

## 2026-11-05 历史快照：phase4-b20 2000 春季京皖文理选项刷新与视觉结案

### 工作位置与 Git

- 仅在现有 canonical worktree `仓库根`、分支 `feat/gaokao-phase0` 工作；未新建 worktree、未进入 `main`、未 push。结案阶段与此交接、`PROGRESS.md` 同步提交；新会话先用 `git log -1` 和 `git status` 确认实际提交与干净状态。
- 本阶段 `b14889cc` 已提交 build/TeX 阶段；当前变更是 phase4-b20 review/finalize、报告投影与交接文件。提交前仅暂存本批回执、全量报告投影及本交接相关文件，核查 staged diff 与 `git diff --cached --check`。不要顺手改写其他卷的缓存状态。

### Live manifest 与来源边界

- manifest revision `6251`；`phase4-b20` status `closed`，关联 `gk-2000-spring-jingwan-arts` / `gk-2000-spring-jingwan-science`，两卷 `production_state=complete`。正式报告：2卷、8版、102页，构建 succeeded、review passed，视觉问题0、警告豁免0、阻塞0。
- 固定上游 PDF 分别是文科 source `src-6d9f6ee269b4dd80d69001f2f4399956b5d037bfbf1d383a78bfdb281c440e6b` / SHA-256 `b9552b8354735296f6ea1ed051085e094e4af0c14ff97ada2dbd4e579b14287f`，理科 `src-a0269cc0034b8f71793418f0abb911e424058f04f18389e6ff78004045ca1eba` / SHA-256 `37f07244497aa0a21be12d8a31eac78b61490f835f088719a5990463585a35ce`。均为2页题面副本、不含答案页；发布者身份未认证，`official_answer=null`，答案/解析为D级编者推导、非官方。源文疑点照录：文科 Q18③「都有垂直」、Q24两处缺标点；理科 Q18③同词、Q23两处缺标点；未新增或移除 issue。
- 排版仅将行内选择项投影同步为 `gkopts`；题面、选项、顺序及数学内容经两名只读复核确认未变，事实层 Markdown、答案、解析、图稿、provenance 未改。正式 build attempts：文科 `01008f5c-ceb0-453f-86d1-4febd6e4e543`、理科 `3327a32f-9123-4130-8d58-ef9451985bf3`，输入 revision 6249，finalizer revision 6251。页数文科5/19/7/16、理科5/24/7/19。四版 PDF SHA 及阶段细节见 `math-gaokao-latex/PROGRESS.md` 和 `reports/phase4-b20.md`。
- 150 dpi、同一 Poppler 工具链逐页比较并复算 PNG SHA：30页像素一致，72页变化/新增；前者继承旧 review 的240项结论，后者重审576项。总计816项：753 pass、63 not_applicable、0 fail。候选页包含所有变化页，回执理由绑定旧 review/PDF SHA、旧 build attempt 与当前 build attempt。finalizer=`FINALIZED`。

### 校验与已知全库例外

- 本批 receipt currentness：2 succeeded、0 pending/stale/invalid；provenance、生成器、简答、版本壳、48题 solution sources、source manifest、issues 均通过。`manifest.csv` 775行且当前；全量报告 `render --all` 与 `check --all` 均通过。
- 完整测试 `python3 -B -m unittest discover -s tests -q`：`Ran 1780 tests in 583.025s`，13 skipped、1 failure。唯一失败 `test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones` 报53卷 paper/batch 缓存状态漂移，首项 `gk-2016-regular-national-2-arts`；本批 provenance check-batch 单独通过。保持本批范围，不刷新其他卷缓存。
- `generate_projects.py --all --check` 返回非零：仍有71个 TeX 文件、37卷过期；按年份最早下一项为2006上海文科 `phase4-b14`。完成当前批后先停在这里；下一轮接续前仍要检查 canonical worktree、branch、status 与 manifest。总项目仍覆盖1952—2026，本批关闭不表示题库整体完成。

### 结案提交

- TeX/build 阶段提交 `b14889cc`；视觉结案及报告/交接提交 `293d44f2`。结束时 `feat/gaokao-phase0` 工作树干净、ahead 6，未 push。
## 2026-11-05 历史快照：phase4-b36 1999 上海文史类 TeX 刷新与视觉结案（带阻塞）

### 工作位置与 Git

- canonical worktree 是已存在的 `仓库根`，分支 `feat/gaokao-phase0`；本阶段没有新建 worktree、没有进入 `main`、没有 push。`主工作树` 是原有 `main` 工作树。
- TeX 阶段提交 `69bd608a`、共享标点转换与回归测试提交 `cba7ff1` 已在该分支。当前 closeout 需包含本批构建/视觉回执、manifest/issues 与六个报告投影、`PROGRESS.md` 和本交接记录；提交前检查实际 staged diff 与 `git diff --cached --check`，提交后确认工作区干净。

### Live manifest 与本卷

- manifest revision `6248`：775 sources、421 papers、267 batches。paper 状态：blocked 109、compiled 3、complete 309；batch 状态：closed 180、closed_with_blockers 86、compiled_pending_review 1。
- `phase4-b36` / `gk-1999-regular-shanghai-arts` 的 batch 为 `closed_with_blockers`，paper 为 `blocked`。固定 source `src-f45a72cc4b6fca6b3bb48f421c9320f7c17aa8c04d746f7ae368c40ef4875742`，PDF SHA-256 `7a1c81dd9091426a8e524170336a9ba46e58fda3206e658233d6c14f5ea319e5`，10页；来源发布者、版次、答案官方身份未认证。`ISSUE-1188`–`1190` 仍 open / blocks_completion；`ISSUE-1191`–`1194` 已 resolved。
- 生成 TeX 只刷新确定性标点包装：`69bd608a` 处理 Q18 句号，`cba7ff1` 修复 `md2tex.py` 数学模式中文逗号/句号包装并增加回归测试。正式 build attempt `5e0b86a5-8f8d-44af-8627-de1970871cc2`（输入 revision 6246）四版成功，共48页（5/21/7/15）；无 errors、missing characters、overfull、undefined references 或 problems。PDF SHA-256：试题 `cc612b70016676c14a54005765fb21fc11ae2198cf296d3e2c5b8cd31e66312c`；解析 `06e77d437c94e11679b150e3932836f302d1118862312a88b687119cc17ffadf`；简答 `26294b3d703aadc121af475afc59032df9dc233ccf027a2f7aae5cb6a02f9a1b`；印刷 `5d4ca3a843c2f233b82c3759418d6cf98f39d977fc050ffd9c0ea8e18b26fc0e`。
- 视觉比较中36页像素与基线一致并继承已有结论，12个变化页重新目检；384项八类检查全通过（288项继承、96项重审）。`finalize-batch`=`FINALIZED`，review passed，但 batch/paper 仍带阻塞。
- 本批 provenance、build/review receipts、生成器、简答、版本壳、solution sources、manifest/issues/CSV 与 `report.py render --all` / `check --all` 均通过。完整测试运行1780项、13项跳过、1项失败：`test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones` 报告56项跨卷缓存漂移，首项 `gk-2016-regular-national-2-arts`；本批外问题未在此阶段批量改写。

### 下一次接续边界

- `generate_projects.py --all --check` 仍有75个文件、39卷、30批次过期；最早下一批 `phase4-b20`（2000春季京皖文理卷）。本批只完成旧 TeX 的生成器同步、正式构建及视觉回执收口，不表示1952—2026总项目完成。
- 继续只用上述现有 `仓库根` / `feat/gaokao-phase0`，不新建 worktree、不切 `main`、不 push。先核对 Git 状态和 live manifest；来源/答案存疑继续标记，不得补造。

## 2026-11-05 历史快照：phase4-b29 1998 上海文史类排版刷新与视觉结案

### 工作位置与 Git

- canonical worktree 为 `仓库根`，分支 `feat/gaokao-phase0`。本轮只使用该既有 worktree；未新建 worktree、未进入 `main`、未 push。主工作树 `主工作树` 保持原样。
- phase4-b29 的 TeX、四版 PDF 回执、复核回执、全库报告投影、`PROGRESS.md` 与本交接记录纳入本阶段提交；提交号以 live `git log -1 --oneline` 为准，提交后核对工作区干净。
- 本批收口后，最早剩余生成器过期项是 `phase4-b36`（1999 上海文史类）；单卷关闭不等于完成1952—2026总项目。接续时仍须核对 worktree、分支、Git 状态与 live manifest。

### Live manifest 与本卷

- manifest revision `6245`：775 sources、421 papers、267 batches。paper production state：blocked 109、compiled 3、complete 309；batch 状态：closed 180、closed_with_blockers 86、compiled_pending_review 1。
- `phase4-b29` / `gk-1998-regular-shanghai-arts` 当前 batch `closed`、paper `complete`。固定来源 `src-8c86b3e592e594953609fe09d0c182d5252c944006503dfb10e8efa1962aeca7`，PDF SHA-256 `c747bff56863a349aa9432b1616630a249cd7668ead997a5bbe1fefa2616f848`，6页。来源副本不认证发布者、版次或卷内答案的官方身份。
- 本批只按当前生成器重建 Q12/Q13/Q15/Q16 的选项 TeX 排版；题干、选项、答案与解析内容未改。正式 attempt `75a696dc-1dea-46d4-8183-e687cf1c6177`，输入 manifest revision 6243；试题/解析/简答/印刷版分别4/17/6/14页，共41页。PDF SHA-256依次为 `040e61cc02967afa14bec732a13bd35c789b52e9d84f8ec3b1cea916789d7778`、`9fbd22ff749851b36e7ebb9beae43c66797113a674766c2012f6c823342c04fa`、`c1b59ec9d2790b27ae888bdd4774f084a370e8f2f7662d983697626d74cd6286`、`2049f4bb4e66bb3e2971545b688c83cc9ed4798d2b59555d6714e756b1f0ef56`。四版 errors、缺字、Overfull、undefined references、problems 均为空。
- 视觉结论：从提交前 HEAD `73a12c22` 用相同工具链重建基线，41页中26页 PNG 像素相同；15个变化页逐页复看八项，共328项（208项继承、120项重审），274项 pass、54项 not_applicable。`finalize-batch`=`FINALIZED`，review `passed`、batch `closed`、paper `complete`。本批 build/review/provenance、生成器、简答、版本壳、solution sources、source manifest、issues、`manifest.csv`（775行）及全库 `report.py check --all` 均通过。
- 全量测试 `Ran 1779 tests in 686.013s`，13 skipped、1 failure。唯一失败 `test_the_cached_states_match_the_recomputed_ones` 报57项跨卷 paper/batch 缓存状态漂移，首项 `gk-2016-regular-national-2-arts`；本批已由 finalizer 重新派生，不批量改写其他卷缓存。

### 当时的接续边界（已由上方状态覆盖）

- `report.py check --all` 通过，六个全库报告投影与 manifest 一致。`generate_projects.py --all --check` 仍有77个文件、40卷、31批次过期；最早下一项为1999上海文史类 `phase4-b36`。本批关闭不表示1952—2026总项目完成。
- 不得新建 worktree；只用现有 `仓库根` / `feat/gaokao-phase0`。不要切 `main`、不要 push。提交时只 stage 当前阶段授权路径，并检查真实 staged diff、`git diff --cached --check`。
- 全量缓存漂移是跨卷独立问题；需另立阶段按实时来源/derived state核查，不在此批扩大范围。任何来源缺失或答案存疑仍标记，不从模型记忆补造。

## 2026-11-04 历史快照：phase1-b24 1994 上海卷视觉结案，Q25 仍阻塞

### 工作位置与 Git

- canonical worktree：`仓库根`；分支：`feat/gaokao-phase0`。本次继续未进入 `main`、未 push。交接更新提交后先用 live `git status --short --branch` 和 `git log -5 --oneline` 核对工作区与 HEAD。
- 最近阶段提交：`a869a2fc` 更新 1994 上海卷生成 TeX；`de13d706` 完成 phase1-b24 正式构建、视觉回执与全量投影；`1a168350` 同步该卷标点包装回归断言。交接文档的本次提交会位于其后。

### Live manifest 与当前卷

- manifest revision `6193`：775 sources、421 papers、267 batches。生产状态：blocked 109、compiled 3、complete 309；批次状态：closed 180、closed_with_blockers 86、compiled_pending_review 1。全库回执投影当前为 FINALIZED 224、INVALID_OR_STALE 42、VISUAL_FAILED 1。
- `phase1-b24` / `gk-1994-shanghai` 的 batch 为 `closed_with_blockers`，paper 为 `blocked`；source `src-175369213dde711e3bba990974dca1216e7e4ef6ed65cbc9e197dc39d81eba65` 的 PDF SHA-256 为 `2321a1438961a48e8951b83cdb4b71e4afa127e1981420a6ba7d1a9e1eddc22d`。来源出版身份未认证，`official_answer=null`。
- `ISSUE-1071` 仍 `open / blocks_completion`：固定印载 Q25 第二支为 `t≥2`，与项目推导中 `t≥1/2` 不一致，导致 `[1/2,2)` 未被印载分段覆盖。保留原文和区间缺口；项目推导不得标为官方答案。全 26 题局部复核已完成，不要重复盲核。

### phase1-b24 正式构建与视觉复核

- 生成 TeX 阶段提交 `a869a2fc` 只更新 `questions.tex`、`answers.tex` 中 5 处句号包装：由数学模式中的 `\text{。}` 改为 `\mbox{。}`，题面数学内容未改；`generate_projects.py --batch phase1-b24 --check` 通过。
- 正式构建 attempt `4707ef56-8915-42e5-b940-b231a204f530`，输入 manifest revision `6191`；试题版 5 页、解析版 19 页、简答版 7 页、印刷版 16 页，共 47 页。四版均 `succeeded`，errors、missing characters、overfull、undefined references 均为 0。PDF SHA-256 依次为 `61e996a8bd086cb970f665e47a8c7b3aa30cac9cdccfeab9a47637d1361a9708`、`ebffaa45c4d4a74d27e009fd4a9cf020d82e83c0dd7462c786b54beec518b675`、`1b36a7c10ea9dde1f4a9ccb12e0e26b5e1f18371ffb45462aabc23922b4be89e`、`168b95d92e44558a37f5e1391603b2f5d7811ea762e4d38231ece3d806259e20`。
- 旧 review attempt `334e6ca3-0bf1-40dd-aa2e-32f86a108949` 的 47 页均为逐项通过。将旧版 TeX 在临时目录重建后，以同一 Poppler 26.10、120 dpi 栅格和当前 attempt 逐页比对，47/47 页 PNG 字节相同，因此继承旧八项视觉结论；并抽看四版候选锚点页。当前 review 为 `passed`，`finalize-batch` 返回 `FINALIZED / closed_with_blockers`。build、review 回执及页级继承说明见卷目录 `receipts/`；批次报告见[phase1-b24 报告](../../exams/math-gaokao-latex/reports/phase1-b24.md)。
- 局部门禁通过：source manifest、issues、三角色 provenance、26 题 solution sources、TeX/简答/四版入口 currentness、`validate-receipts --require-final --require-current-inputs`、`review_receipts.py check-batch`、`manifest_csv --check`（775 行）、`report.py check --all`。1994 专项 `tests.test_1994_shanghai_sources` 为 16/16 通过。
- 全量测试末次结果：`Ran 1779 tests in 606.387s`，`FAILED (failures=1, skipped=13)`。唯一失败 `test_the_cached_states_match_the_recomputed_ones` 仍报告 79 卷 manifest 缓存 `production_state` 与现场 provenance 推导不一致；首例为 `gk-2012-regular-national-outline-arts`，缓存 `complete`、现场 `answers_verified`。此为跨卷状态缓存问题，不在 phase1-b24 内批量改写。

### 后续接续

- `python3 tools/generate_projects.py --all --check` 当前 exit 1：仍有 105 个生成 TeX 文件、54 卷、41 批次过期。下一项按年份最早的是 `phase1-b36`（1994 上海试验卷文理科）；逐批 `--write`、检查、构建与视觉结案，禁止直接对全库 `--all --write`。
- 不要重复生成、构建或复核 phase1-b24；只有出现可绑定同版来源、答案或勘误证据时才重审 `ISSUE-1071`。全库 79 卷缓存漂移另开阶段处理。
- 并行来源审计没有改变问题状态：2013 全国Ⅰ文科 Q22–Q24 作答规则及 Q21 公切线类型仍缺能绑定固定 PDF 版次的正式证据（`ISSUE-0851`—`0853`、`ISSUE-0879` 保持开放）；2025 全国Ⅰ Q11 的固定源印载 `2 sin C`，公开官方评析未呈现争议公式或勘误（`ISSUE-0048` 保持开放）。审计没有写入仓库文件，不能据此改题面或官方答案字段。

## 2026-11-04 历史快照：phase4-b50 视觉结案，Q18 仍阻塞

### 工作位置与 Git

- canonical worktree：`仓库根`；分支：`feat/gaokao-phase0`。本批最后一次提交后应为干净状态；未切换到 `main`、未 push。新会话先执行 `git status --short` 与 `git log -5 --oneline` 核实实际 HEAD，不以本文件中的提交号代替 live Git 证据。
- 用户要求本批结案后停工，不启动下一卷；任何后续工作仍应只在该 worktree/分支内进行，并按“每阶段提交”执行。

### 当前卷与批次

- live manifest revision `6190`：775 sources、421 papers、267 batches。`phase4-b50` / `gk-2002-regular-suyuyuegui` 的 batch 为 `closed_with_blockers`，paper 为 `blocked`。
- `ISSUE-1417` 仍 `open / blocks_completion`：固定 PDF 第2页 Q18 只称 `{b_n}` 为等比数列，未说明零公比约定。固定 PDF SHA-256 `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91` 不含答案页；官方身份与答案均未核，`official_answer=null`。Q18 保留 U/PENDING 和 q=0、q=±1/√2 两种条件分支，不得擅自补定。
- 早期编译失败生成的 `ISSUE-1418`–`ISSUE-1421` 已由成功正式构建自动标记 `resolved / non_blocking`；不得把它们与仍开放的 `ISSUE-1417` 混淆。

### 项目生成、正式构建与视觉验收

- 项目 TeX、简答源和四版入口已生成；`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 均通过。题面序列化仅对 Q16/Q17 公式断行和句号位置作无语义调整；正文来源说明改为“官方答案未认证”，front matter `official_answer: null` 不变。三角色 provenance 当前 SHA-256：`458ecfb1e2aaba4dab8d3ab7e7e07e77dc62ce6a04bd7ee6ae2767c55993e662`。
- 最终构建 attempt `99457b35-988d-486b-82bf-ee011d6982e2`（输入 manifest revision `6188`）四版成功、45 页；错误、缺字、overfull、未定义引用均为 0。PDF SHA-256：试题版 `a6e46837b6c2035e3d6fc421b32575c5ccc89ef8b65510a393ce20b76d66b5c2`；解析版 `ae19d5e02b766abc59f94f23a0e0fa9170c5c115aeb270c44640bc95e25c0941`；简答版 `60df70de5d930f533142f2cac0c13dfef0d7fba046c40d262af4eeeeced44329`；印刷版 `fcc644253685d16a91b427891b4f0a592f4c0a606389ce6608c5573707a246cb`。
- 四版全部页面完成八项目检，视觉回执 `passed`；Q版第2、4页 PNG SHA 与前次已实际目检图逐字节相同，继承此前结论。`review_receipts.py finalize-batch` 返回 `FINALIZED`、`closed_with_blockers`；批次报告列出唯一阻塞 `ISSUE-1417`。详见[项目生成报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-project-generation-20261104.md)、[正式构建报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-formal-build-20261104.md)与[视觉审查报告](../../exams/math-gaokao-latex/reports/phase4-b50.md)。
- 最新门禁证据：`review_receipts.py check-batch` 无问题；`build_projects.py validate-receipts --require-final` 输出 `OK`（1 succeeded、0 pending、0 stale/invalid/failed）；`manifest_csv --check` 为当前 775 行；`report.py check --all` 报告输出与 manifest 一致。完整测试 `python3 -B -m unittest discover -s tests -q` 实际运行 `1779` 项、13 项跳过、1 项失败（582.882 秒）：`test_the_cached_states_match_the_recomputed_ones` 报告 80 卷的缓存 production_state 与现场推导不符。首例 2012 全国大纲文科在 Git 基线 revision 6181 与当前 revision 6190 中都缓存为 `complete`，现场推导为 `answers_verified`；本卷 `provenance.py check-batch --batch phase4-b50` 通过。完整结果及边界见[正式构建报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-formal-build-20261104.md)。

### 下一位 Agent 的接续边界

- 不要重复生成、编译或复核本卷；`ISSUE-1417` 只有在获得可绑定同版来源的零公比定义、答案或勘误证据时才可重审。在此之前继续保留 blocker 与全部条件分支。
- 全库测试仍报告 80 卷的缓存 production_state 漂移；这是本批外问题，首例在基线 manifest 已存在。若要批量派生刷新，应另开授权阶段，并保留逐批证据。
- 本批完成后本轮已按用户要求停止。新会话先核对 Git/manifest/回执与 `PROGRESS.md`，再从可用清单确认下一批；不据本卷的 `closed_with_blockers` 推断 1952–2026 语料完成。

## 2026-11-04 历史阶段快照：来源接收到 provenance 导入时（revision 6181）

> 以下当时的生成、构建与视觉验收状态已由上方最新小节覆盖；此处细节只用于追溯阶段依据。

### 工作位置与 Git

- canonical worktree：`仓库根`；分支：`feat/gaokao-phase0`。上一阶段登记提交为 `f91a0e33`；本次接续只修改 2002 苏豫粤桂 provenance 阶段文件。阶段提交后以 live Git 状态确认结果；未切换到 `main`、未 push。
- 当前规范源/登记与三角色回执分别见[内部卷登记报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-paper-registration-20261104.md)和[provenance 阶段报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-provenance-20261104.md)。

### Live manifest 概况

- live manifest revision `6181`；source 总数 775、paper 421、batch 267。`phase4-b50` 已导入 provenance，状态 `provenance_verified`。manifest CSV 当前仍为 775 行；全量报告投影最后对应 revision `6180`，本次状态事务后待项目生成刷新共享 `index.json` 时一并重建并重验。本节历史全库快照不代表 1952–2026 目标已完成。
- 当前未关闭批次包括 `phase0-b02`（2019/2020 全国Ⅰ文理四卷，`compiled_pending_review`）和 `phase4-b50`（2002 苏豫粤桂，`provenance_verified`）。保留 2020 文科取消题与五项 `heading_number` 视觉失败，不删除该题或将失败改判通过。
- `phase4-b49`（2026 北京回忆版候选卷）仍为 `closed_with_blockers`；来源身份与官方答案未核，`ISSUE-1408`–`1410`、`1414`–`1416` 继续阻塞，候选版与未认证副本之间的题面/答案差异不得择一消除。`phase4-b50` 的 `gk-2002-regular-suyuyuegui` 为 `blocked`，唯一当前问题是 Q18 的零公比约定 `ISSUE-1417`。

### 最近完成的来源核查

- `phase4-b48`（2003 北京文理卷）已完成原卷忠实转录、构建和视觉封账，当前仍为 `closed_with_blockers`。新查到新浪教育保存的 2003-06-09 精华听课网文理题面/参考答案分页：文科 Q18 扫描图右顶点写 A2、理科 Q17 题面写“底面边长为3”。这些是同期二手材料，不认证为固定 PDF 同版或官方勘误。
- 已更新 `ISSUE-1398`–`1401` 的 `current_evidence` 和[2003 北京来源交叉核查报告](../../exams/math-gaokao-latex/reports/2003-beijing-contemporaneous-source-corroboration-20261104.md)。四项仍 `open` / `blocks_completion`；原题面、答案、provenance、manifest 与回执均未因二手材料改写。定向查找未定位官方扫描/勘误，但这不表示其不存在。
- 先前的 `phase4-b47`（2003 上海文理普通卷）已经完成答案/解析、盲核、图稿、provenance、四版构建及92页视觉复核；批次 `closed_with_blockers`，两卷 Q14 的 `ISSUE-1388`/`1389` 仍为 U/PENDING。原交接快照关于“下一步才开始答案”的文字已过时，细节以 [`PROGRESS.md`](../../exams/math-gaokao-latex/PROGRESS.md) 开头阶段记录及 live manifest 为准。
- 上一轮来源证据更新的确定性校验与 Git 记录详见其阶段提交；本轮注册阶段的命令结果见下方新阶段及报告。

### 2002 苏豫粤桂卷来源接收

- 已目视核对固定 source `src-0daae2fa54742835e68d7f3b2cb647b26cee7c4d302f16958e53100e71e4bab4`：SHA-256 `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91`、Git blob `24ff45c0af6a8707358e31392c08cb4e2c96a32f`、2 页 A3、印刷页 113–114，题签“2002 普通高等学校招生考试（苏豫粤桂）”。PDF 可见 Q1–Q22 及 Q10/Q19/Q21 图；没有答案或评分页。
- 题签未标文理轨道；来源发布身份/复制链未核。仍按单一固定文件处理，不拆成四套；现已登记内部 paper/batch，不据此认证来源身份。完整页图、范围和边界见[来源接收报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-source-intake.md)。
- 后续与全国旧/新课程四卷的题面比对已完成，卷种与分类边界见下一小节及[比对报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-scope-comparison-20261104.md)。

### 2002 苏豫粤桂卷范围比对

- 确认来源卷与全国旧/新课程四卷不是整卷重复，但 Q2、Q3–Q6、Q11–Q14、Q19 等题目在不同题号位置与全国卷题面重合；不得由重合反推组卷关系或官方身份。
- 以一份 22 题固定来源处理，不按文件名列出的四个地区拆卷。拟用内部 ID `gk-2002-regular-suyuyuegui`；未来 paper 记 `track=none` 只表示当前无文/理分类，source `track` 继续 null，`regions` 继续空。来源身份仍未核。
- 两页均是文字层候选；依 `OCR_WORKFLOW.md` 未调用 OCR。180 dpi 页图已用于转录；Q10/Q19/Q21 图需矢量重绘。题面转录状态见下节。

### 2002 苏豫粤桂卷题面转录

- 已完成固定 PDF Q1–Q22 转录草稿，选择12题、填空4题、解答6题；报告与具体源内字形事项见[转录报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-question-transcription-20261104.md)。Q10、Q19、Q21 原页图现已矢量重绘并链接，细节见本节“图稿阶段”。
- 当前题面草稿 SHA-256：`2b90924f6eedf37060b9925f3fa32a93a06d6b13c5ca696c4e97c4e990e0936b`。Q12“十·五”、Q14 指数 7、Q17 共轭横线按原页照录；来源 PDF 文字层只用于定位，未调用 OCR。
- Q1–Q22 独立题面复核已完成，逐题结果见[复核报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-question-review-20261104.md)。Q10(B) 原先误称“竖直坐标轴”，现按原页更正为直线 $x=1/2$；它与圆心重合，对应题目方程。题面稿现已链接独立矢量图。

### 2002 苏豫粤桂卷答案与解析

- 已形成 Q1–Q22 本库独立推导草稿：[答案要点](../../exams/math-gaokao-latex/drafts/2002-suyuyuegui/答案要点.md)、[解析正文](../../exams/math-gaokao-latex/drafts/2002-suyuyuegui/解析正文.md)。当前 SHA-256 分别为 `705c75965d6ff4f8893fd8e3c2fa8f21d86da18e66b57ff12b62a70e3a9efd1e` 与 `2be78cecb67a11310a408eab0c9cf2f588a13d93b4ed3df456c84e6b25d454c3`；逐题复核见[独立答案复核报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-answer-review-20261104.md)。
- 固定 PDF 无答案/评分页；答案均为非官方推导、`official_answer=null`。独立复核未发现实质性数学错误；Q18 保留零公比约定两种口径，Q19 明确采用棱锥两侧面围成的内二面角。Q21 剪线虚线现已绘入独立答案辅助图，图稿不表示剪下后的配对、翻转、剪角平移或成品展开状态，操作由解析正文说明。盲解与主会话在 Q2、Q3、Q10、Q20 四项结论不同，均以重新推导和原页复看结果修正。

### 2002 苏豫粤桂卷题图矢量转录

- 按固定来源 PDF SHA `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91`，重绘 Q10 四选项、Q19 四棱锥、Q21 三张空白题面图和答案剪线图；逐图报告见[题图矢量转录报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-figure-transcription-20261104.md)。
- 四个独立 TikZ 文件位于 `2002_苏豫粤桂卷/figures/`。Q10、Q19、Q21 原题图分别链接在题面草稿；Q21 答案剪线图单独链接在解析草稿。Q10 片段首次审查发现 A/B 圆心误放原点，已按原页改为圆心 $(1/2,0)$、O 为左端点，并重新编译复看；Q21 片段只表示剪线，不能独自说明配对和平移。
- 四图使用 XeLaTeX+CTeX scratch 编译成功并对渲染图做目视检查。scratch PDF/PNG 在忽略目录 `.work/2002-suyuyuegui-figure-review/`，不作为正式版本的构建回执或最终排版验收。
- 已建立规范题面、答案要点、解析正文，并确定性生成 `_含解析.md`。paper `gk-2002-regular-suyuyuegui` 与 batch `phase4-b50` 已登记；source 与 paper 的关系为 `canonical`，source `track=null`、`regions=[]` 保持不变。四图均登记，引用次数为 Q10/Q19/Q21 原图各2、Q21答案剪线图1。
- 登记阶段结束时 `ISSUE-1417` 记录 Q18 零公比约定，状态 `open / blocks_completion`；答案要点保留 U/PENDING 和两个条件分支。paper `blocked`、batch `planned`；身份未认证且 `official_answer=null`。三角色 provenance 随后的阶段状态见本交接下方记录。
- 登记阶段的 source manifest、issues、22 题 solution sources、CSV currentness 和全量报告 currentness 结果见[登记报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-paper-registration-20261104.md)。

### 2002 苏豫粤桂卷三角色 provenance

- 已为 Q1–Q22 导入 question-review、answer-solve、answer-review 三角色 provenance，SHA-256 `63bd83a95aed270e90d475115ca61314148cd5e175b784e6d3a58285188d28ef`。题面复核均 passed，答案 D 21 题、U 1 题；Q18 的 U 与 `ISSUE-1417` 相连，答案复核没有另列计算冲突，未把定义约定误记作两解冲突。证据范围、页码映射及角色来源见[provenance 阶段报告](../../exams/math-gaokao-latex/reports/2002-suyuyuegui-provenance-20261104.md)。
- `provenance.py check-batch` 输出 `OK：1 卷`；source manifest、issues 与 22 题 solution sources 校验通过。revision `6180→6181`，batch `provenance_verified`、paper `blocked`。全量报告仍是 revision 6180 快照，项目生成刷新共享 index 后重新生成/核验。未生成项目 TeX/简答/四版入口，也未构建正式 PDF 或视觉审查。

### 当时的下一阶段计划（已完成）

- 当时计划生成 `questions.tex`、`answers.tex`、简答速查和四版入口，并完成构建与逐页视觉检查；以上工作已完成，当前状态见本文件最上方与 phase4-b50 报告。Q18 仍 U/PENDING，批次以 `closed_with_blockers` 收口。
- 后续年份/来源候选须在新会话重读 live manifest 后确认；1998 全国文科曾列作候选，已有25题转录、独立数学复核及固定 PDF 原页复看，但来源 `ready/unbound`、出版身份未核、Q12/Q13/Q25 原件冲突仍在。旧的定向检索记录不能代替新的来源核验，也不能据未命中推断官方材料不存在。
- 不要因大量未绑定来源、blocked papers 或 open issues 而批量清状态。每阶段核对固定来源、现有草稿、manifest、PROGRESS 与历史，保留来源不确定性，并在每个可审查阶段单独提交；仍不 push。

## 历史快照：2003 上海普通卷文理科题面转录与独立复核完成

### 工作位置与分支

- canonical worktree：`仓库根`；分支：`feat/gaokao-phase0`。本次交接更新前 HEAD 为 `5de51f51`；复核阶段提交后工作区干净，领先 `origin/feat/gaokao-phase0` 6 个提交。交接更新会另加一个本地提交；新会话仍须重新读取 HEAD/status。没有切换到 `main`，没有 push。
- manifest revision `6132`；本批没有写 manifest/issues，也没有注册 `phase4-b47` 或任何 paper。文理来源目前仍是 `ready/unbound`，`official_answer=null`。
- 最新卷级阶段日志在 `math-gaokao-latex/PROGRESS.md` 顶部。当前全库统计读取 `math-gaokao-latex/reports/baseline.md`；以该文件与 live manifest 为准。

### 当前批次：2003 上海普通卷文科与理科

| 科类 | source_id / PDF SHA-256 | 最终题面草稿 SHA-256 | 进度 |
|---|---|---|---|
| 文科 | `src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4` / `ffd59c395a0c675118f6da576e48842549c4afa031d923448f26f33087bc7e85` | `a10f4ad830247154400d028d1e8b0921814266e3200a4dedc132cda37da5a225` | Q1–Q22 转录和独立题面复核通过 |
| 理科 | `src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0` / `88b72fea05d331215504bb89257e375d07c18ba21e830cf9e6288461e88ccf8d` | `be8799e20f184a93be2cea5f201d2487db44c1fc6aa9d72e948b3de0d389b56d` | Q1–Q22 转录和独立题面复核通过 |

- 固定来源都来自 `gaokaomath-src/普通高考/2003/`，与 manifest rev6132 的 PDF SHA、Git blob 及上游 checkout commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d` 相符；发布者、出版者、版次、复制/扫描链和官方身份尚未核实。
- 文科来源接收、草稿和复核记录分别见 `math-gaokao-latex/reports/2003-shanghai-arts-source-intake.md`、`2003/2003_数学真题_上海文_题面转录草稿.md`、`math-gaokao-latex/reports/2003-shanghai-arts-question-review.md`。理科对应记录见 `math-gaokao-latex/reports/2003-shanghai-science-source-intake.md`、`math-gaokao-latex/reports/2003-shanghai-science-question-transcription.md`、`2003/2003_数学真题_上海理_题面转录草稿.md`、`math-gaokao-latex/reports/2003-shanghai-science-question-review.md`。
- 两名未参与各自转录的独立复核者逐题对照可见 PDF 页图；主会话复查并补齐 Q16/Q18/Q20 图注，均无剩余题干、公式、选项或符号差异。转录和复核提交依序为 `976f23b2`（理科来源接收）、`820666b1`（文科转录）、`75938e68`（理科转录）、`5de51f51`（文理题面复核）。
- **理科文字层有明显整题错配：**第2页可见 Q22 是集合 `M` 的函数题；同页文字抽取在 Q22 位置却输出等比数列组合和题，该题可见于第1页 Q19。Q20 的“最小”也被文字层重复为“最最小”，Q13(D)绝对值线及若干平行符号/向量箭头有抽取缺陷；均按可见页面转录，不以文字层替代。
- 本轮没有 OCR、外部 API 或项目测试/构建；token 成本未知。没有生成答案、解析、图形矢量稿或四版 TeX/PDF。本批仍只是题面层工作，不表示 1952–2026 语料完成。

### 当时计划的下一阶段（现已完成；勿按此快照重复开工）

- 从已复核的文理题面开始答案要点与解析草稿；必须标为本库独立推导、非官方答案，并分别完成独立盲解核对。若没有可追溯的同版答案/勘误证据，保留 U/unknown 与 source identity 不确定性。
- 按 Q16/Q18/Q20 原页重绘文理两套题图；图稿、manifest 映射和出处必须一起登记。随后才评估 paper/batch 注册、逐题 provenance、确定性合并、四版构建与逐页视觉验收。
- 任何问题不得因文字层输出或题目看似重复而擅改源稿；尤其理科 Q22 必须以 PDF 可见渲染页为准。每完成一个阶段单独提交；不 push、不切 `main`。

### 先前已登记批次：2004 上海理科普通卷 `phase4-b46`

- `gk-2004-regular-shanghai-science` 已完成构建与视觉审查，终结器返回 `FINALIZED`，批次 `closed_with_blockers`、paper `blocked`。Q19(2) 未定义集合 B 与 Q22(1) 椭圆点位无解分别保留为 `ISSUE-1386` / `ISSUE-1387`，答案维持 U/PENDING；无同版权威证据时不得补条件或解除阻塞。
- 四版共58页，编译错误/缺字/溢出/未定义引用为0，58页八项视觉检查通过。过程、构建与视觉回执见 `math-gaokao-latex/reports/phase4-b46.md`、`math-gaokao-latex/reports/2004-shanghai-science-formal-build.md` 与试卷 `receipts/`。

### 当前全库快照

manifest rev6132 的 baseline 当前记录：775来源；415试卷（complete 309、compiled 3、blocked 103）；263批；正式复核门禁 FINALIZED 219、INVALID_OR_STALE 43、VISUAL_FAILED 1；1660/1660 版本有编译记录；未解决问题293条、其中 blocks_completion 232。baseline 的全部 build/review/issue 计数见 `math-gaokao-latex/reports/baseline.md`。不要沿用此前交接中的 FINALIZED 220 / INVALID_OR_STALE 42 旧投影。



## 2026-10-26 后续（十二）：1995 全国文科接续验收

- 接手HEAD6153e863，保留Claude Code既有未提交成果，继续phase4-b34（gk-1995-regular-national-1-arts）。来源/规范解析阶段已提交4d7c4a3f；四版验收阶段另按用户授权提交，不push。
- 26题、单页A3扫描、无答案/分值，D级双求解员推导。修复Q24/Q25第二问推导漏录、Q24 AE/BE漏线及Q5 O压线；恢复来源json被覆盖丢失的逐题页/栏映射、类型范围和未知分值等字段，旧草稿测试升级为canonical双向绑定校验。
- 最终四版4/20/6/16页，46页八项视觉通过；attempt761a4cb5-bd7b-47f7-b3f5-6f4c1fe91bcf，FINALIZED/closed/complete，rev5086。不得重复转录或使用旧图替代当前回执；完整证据见reports/1995-national-arts-*及reports/phase4-b34.md。
- 当前775来源、321卷（complete265、blocked53、compiled3）、182批。全量1710项测试通过（13跳过，606.114秒），报告/CSV及当前回执检查均通过；详细见本轮交付复核报告；来源非官方、分值未知的边界保留。整个1952—2026目标仍未完成。
- 下一可核候选：1995上海文科，source_id `src-ef7576922eed4ed30b369569c10911cf87356d83988aa0d9bdaf82927061e059`，manifest为ready/unbound；本轮只读确认没有对应项目目录、规范MD或paper记录。固定PDF记录SHA `7a54c35368fb8de8e0842c2da263affa0115f5d1d9afa9798322e3c389a023c0` 尚未本轮重验，不把它说成已核来源；开工先固定字节并逐页核源。

## 2026-10-26 后续（十一）：1995 全国理科（D 级）收口

- `phase4-b33`（`gk-1995-regular-national-1-science`）已提交 `eb4cc57`：26 题、单页 A3 扫描、**来源无答案**；答案/解析为项目独立推导，两名隔离求解员 26 题结论一致；四版 4/23/6/19 页；`FINALIZED`／`closed`／complete。
- 源疑点：Q14 源页选项 (A)(C) 重复；Q23 E 底面按源图取下底面；Q17「过球心」按底面平面过大圆。
- 现况：775 来源、320 卷（complete 264／compiled 3／blocked 53）、181 批，manifest rev 5066。

## 2026-10-26 后续（十）：1993 上海卷收口

- `phase4-b32`（`gk-1993-regular-shanghai`）已提交 `a521e5a`：26 题、7 页扫描件附解答评分、四版 5/28/7/23 页；`FINALIZED`／`closed`／complete。盲解与卷内答案数值一致。
- 修复：Q13(D) 指数 1/3；Q24 的 O（题面 OA/△ADO）与 Q26 椭圆分母作为源疑点照录；Q10/Q24 标签白底、Q11 刻度偏移、Q26 删非源辅助点并移 φ 入角、Q24 PQ 线型；题面解法提示删除。
- 现况：775 来源、319 卷（complete 263／compiled 3／blocked 53）、180 批，manifest rev 5024。

## 2026-10-25 后续（九）：1992 上海卷收口

- `phase4-b31`（`gk-1992-regular-shanghai`）已提交 `01bef09`：26 题、6 页扫描件附解答评分、四版 5/25/7/19 页；`FINALIZED`／`closed`／complete。盲解与卷内答案 26/26 一致。
- 修复：解析 Q20 改 B（P0）、Q12 指数 1/8（P1）、Q22 口径、Q18 定义域、Q16 系数、Q10 向量方向、Q10/Q24/Q26/Q11 图标签。
- 现况：775 来源、318 卷（complete 262／compiled 3／blocked 53）、179 批，manifest rev 5003。

## 2026-10-25 后续（八）：1991 上海卷（blocked）

- `phase4-b30`（`gk-1991-regular-shanghai`）已提交 `4887d04`：27 题、7 页扫描件附解答评分、四版 5/25/7/21 页；批次 `closed_with_blockers`，整卷 **blocked**。
- 阻塞项 `ISSUE-1178`：Q8 题面 `(2x²−1/x)^8` 按指数 8 无常数项，卷内答案 60 只在指数 6 时成立；300 dpi 字形两孔确认 8，盲解与复核独立确认，三说并列保留。
- 现况：775 来源、317 卷（complete 261／compiled 3／blocked 53）、178 批，manifest rev 4977。

## 2026-10-25 后续（七）：1998 上海文史收口

- `phase4-b29`（`gk-1998-regular-shanghai-arts`）已提交 `f617919`：22 题、6 页扫描件附卷内答案（等级 C）、四版 4/17/6/13 页；`FINALIZED`／`closed`／complete。盲解与卷内答案逐项一致。
- 修复：Q22(2) 极限式按卷内原式（P0）；Q20 辅助图从题面版移入解析版并删答案标注；Q19 图 O₁/B 标签与线型。
- 现况：775 来源、316 卷（complete 261／compiled 3／blocked 52）、177 批，manifest rev 4950。

## 2026-10-25 后续（六）：1995 上海理工农医收口

- `phase4-b28`（`gk-1995-regular-shanghai-science`）已提交 `83fa415`：25 题、9 页扫描件附卷内答案（等级 C）、四版 5/19/7/14 页；`FINALIZED`／`closed`／complete。盲解与卷内答案逐项一致。
- 关键纠错：Q9 源式 `(2x-1)/(x+3)>1`、答案 `x<-3 或 x>4`（初稿错作 2x+1 / x>2）；Q24 卷内答案漏 `m=n`，补正 `(2-√3,+∞)`；Q6 选项图恢复 B/D 截距判别信息。
- 现况：775 来源、315 卷（complete 260／compiled 3／blocked 52）、176 批，manifest rev 4933。

## 2026-10-25 后续（五）：1999 上海理工农医收口

- `phase4-b27`（`gk-1999-regular-shanghai-science`）已提交 `8236ab5`：22 题、5 页扫描件附卷内答案（等级 C）、四版 4/19/6/15 页；`FINALIZED`／`closed`／complete。盲解与卷内答案全一致。
- 修复：来源页 4-35—4-39、Q8 多余 `}`、Q9/Q19 结论补全、Q11 断行、Q14 cases、解析前言/草稿状态句清理；Q20 删非源有 B–E、Q21 B 标签移位。
- 现况：775 来源、314 卷（complete 259／compiled 3／blocked 52）、175 批，manifest rev 4895。

## 2026-10-25 后续（四）：1998 上海理工农医收口

- `phase4-b26`（`gk-1998-regular-shanghai-science`）已提交 `5429317`：22 题（填空 1–11、选择 12–16、解答 17–22）、6 页扫描件附卷内答案（等级 C）、四版 4/16/6/12 页；`FINALIZED`／`closed`／complete。盲解与卷内答案全一致。
- 关键纠错：Q15 源为「且 11∈B」（初稿漏一个 1），修正后 a>6、D 唯一；Q19 图 z 轴改 O–O₁ 虚线＋O₁ 以上实线；Q22 行间公式后孤行句号删除。
- 现况：775 来源、313 卷（complete 258／compiled 3／blocked 52）、174 批，manifest rev 4864。

## 2026-10-25 后续（三）：1997 上海理工农医收口

- `phase4-b25`（`gk-1997-regular-shanghai-science`）已提交 `158432f`：22 题、7 页扫描件附答案要点（等级 C）、四版 6/21/8/15 页；`FINALIZED`／`closed`／complete。独立盲解 22 题与印载答案全一致。
- 生成端两处修复：① 解答题答案必须写成 `**答案（k）：X**` 才会进入答案框与简答版（原 `**（k）**` 会全部退化为「见解析版」）；② 简答版提示语用 `SHORT_ANSWER_NOTICE_OVERRIDES` 按「来源印载答案」改写，已加 1997 上海文/理两卷。
- 现况：775 来源、312 卷（complete 257／compiled 3／blocked 52）、173 批，manifest rev 4846。

## 2026-10-25 后续（二）：1997 上海文史收口

- `phase4-b24`（`gk-1997-regular-shanghai-arts`）已提交 `b0b0af6`：22 题、8 页 A4 扫描件附印载答案与评分（等级 C）、四版 5/20/7/15 页；finalize `FINALIZED`、批次 `closed`、整卷 complete。独立盲解 22 题与印载答案逐题一致。
- 关键纠错：Q21 直线与抛物线交点坐标首稿误作 (5±√17)/2，实为 (5±√13)/2=(0.697,1.303)/(4.303,−2.303)，两份独立审查同时抓出；Q19 三棱柱补 AC′、删幻影 B′C、按源改线型；Unicode 下标 ₁/₂ 缺字改数学模式。
- 现况：775 来源、311 卷（complete 256／compiled 3／blocked 52）、172 批，manifest rev 4824。

## 2026-10-25 后续：2002 北京文科收口

- `phase4-b23`（`gk-2002-regular-beijing-arts`）已提交 `6d10511a`：22 题、2 页 A3 重排件（有文字层、无答案页，等级 D）、四版 5/19/7/17 页；finalize `FINALIZED`，批次 `closed`，整卷 complete。独立盲解 22 题与库内答案逐题一致。
- 修复要点：Q11 零点 0.6→1（原图与选项矛盾）、Q12 虚线仅 f₂/f₃/f₄、Q18 尺寸标注改「标签贴棱外侧、无箭头」、Q4 空选项占位行、Q20 八列表超宽（表头缩写＋题面说明）、Q11 两行选项 24pt 错位。
- 现况：775 来源、310 卷（complete 255／compiled 3／blocked 52）、171 批，manifest rev 4799。

## 2026-10-24 后续：1996 上海文史收口

- `phase4-b22`（`gk-1996-regular-shanghai-arts`）已提交 `72dd5dc3`：24 题、8 页扫描件附印载答案（等级 C）、四版 6/26/8/19 页；finalize `FINALIZED`，批次 `closed_with_blockers`、整卷 blocked（Q15 A1「直线 OA」外分点歧义，ISSUE-1138–1143）。
- 本轮视觉审查代理多次长时间无产出，由主会话接管逐页复核并留证；后续开批建议把审查段拆到 ≤4 页/代理，并预置主会话兜底。
- 当前 775 来源、309 卷（complete 254、blocked 52、compiled 3）、170 批；manifest rev 4773。

## 2026-10-24 阶段提交与1996上海理科接续

本段优先于下方旧快照。用户明确授权“每完成一个阶段就提交”，仍不push。
canonical worktree与分支仍为`phase0-wt` / `feat/gaokao-phase0`。

- 2000春季京皖文理phase4-b20已提交`c4766f2c`；1996上海理科来源/数学/规范登记阶段已提交`be4e95b`。
- 1996上海理科24题/150分、全部选做轨道与7幅TikZ图已登记为`gk-1996-regular-shanghai-science`，source已canonical绑定；不再重复转录或登记。
- phase4-b21最终四版67页（7/28/9/23）视觉通过，finalize返回FINALIZED，manifest revision4752；批次closed_with_blockers、整卷blocked。最终attempt为`75a8a3fe-beda-4e63-bf17-3872c808876d`，见本卷receipts与reports/phase4-b21.md。
- Q15 A1原文“直线OA”按通常无向距离有内外分两解，印载答案只列单解；ISSUE-1136/1137都open并阻碍完成，provenance为U/unresolved。不得按源答案把直线改线段，不得降级冲突以通过门禁。
- 当前775来源、308卷（complete254、blocked51、compiled3）。这只是已登记状态，不是全项目完成。全量1757项测试通过（13跳过，1012.138秒）；详细校验见PROGRESS与1996阶段复核报告；后续先读当前manifest、Git及回执，不用旧截图或旧报告证明新版本合格。

## 2026-10-23 接续校正

本文下方2026-10-22快照已过时。当前仍使用 canonical worktree
`仓库根`、分支 `feat/gaokao-phase0`，
本轮接手HEAD为 `77eeb66c`，未切main、未提交或推送。

- 已接续并收口未提交的2000春季京皖文理两卷（phase4-b20）：48题、八版98页，
  来源视觉/数学复核及全部输出页八项审查完成；修复推导、来源记录与图标注，补答案图。
  当前manifest revision4740，批次closed，check-batch返回FINALIZED。
- 当前全量投影：775来源、307卷（complete254、blocked50、compiled3），
  168批，正式门禁FINALIZED165、VISUAL_FAILED3。此为状态统计，非全项目完成。
- 本轮成果路径：`math-gaokao-latex/reports/phase4-b20.md`、
  `reports/2000-spring-jingwan-review.md`，以及PROGRESS.md末尾。
- 全量测试1753项初跑仅旧来源“未绑定”断言失败，已修为canonical双向绑定校验；
  定向7+2项通过；最终全量1755项通过（13跳过，451.183秒），报告/CSV/最终回执检查均通过。
- 旧PROGRESS把1994上海列为下一套，当前manifest却已将其绑定为phase1-b24、
  blocked/closed_with_blockers；不要重复登记或转录，先核对当前报告和resume_action。
- 可核下一候选为1996上海理科：当前source_id
  `src-544d6951d540a551546ce474b93c3b9bc08e1863472ea0998f971dd4b619de21`
  为ready且未绑定；已有`1996_数学真题_上海理工农医_{试题,答案要点,解析正文,含解析}.md`
  与项目内7幅TikZ图。没有四版入口、provenance或正式回执，需先独立核源/数学复核。
  Q15—18的A1/B1及Q22的A2/B2选做轨道必须保留；Q15 A1直线OA内外分歧义待核。
  固定源印载答案不能当成已认证官方答案。参见PROGRESS旧记录约2540行及
  `tests/test_1996_shanghai_science_sources.py`；此次只读定位，未重验源PDF哈希。
- 保留全部未提交成果；未获授权不Git提交，不push；不用旧PNG或旧QC作为当前验收证据。

## 2026-10-22 历史状态摘要（已被文首当前接续取代）

题库仍在持续建设，1952—2026 全范围目标尚未完成。请在 `feat/gaokao-phase0` 分支和 canonical worktree 继续；不要切到 `main`，不要 push，也不要覆盖既存未提交文件。

### Git 工作位置

- 仓库：`主工作树`
- canonical worktree：`仓库根`
- 分支：`feat/gaokao-phase0`
- 当前 HEAD：`ed8b546bb584d360f3b94b36d7c5a3dfe6cfbdee`（refresh reports after 2006 review close）；当时与 `origin/feat/gaokao-phase0` 同步。
- `main` 是独立 worktree，HEAD `4859ad9b`；本项目不要在 main 继续。
- `main` 已在提交 `9655b6d3` 将排版治理目录从 `docs/design/` 迁到仓库根 `typography/`；当前 main HEAD 为 `4859ad9b` 且工作树干净。`feat/gaokao-phase0` 的历史 HEAD 仍有旧 `docs/design/` 跟踪文件，但已恢复工作树到分支 HEAD，消除了无关删除差异；没有把 typography 迁移提交带入题库分支。
- 主 worktree 此前干净。此交接文档应新增在 canonical worktree。提交前再核对状态与 staging，避免夹带别的工作。

新对话先核对：

```sh
cd 仓库根
git status --short --branch
git log -1 --oneline --decorate
```

## 2026-10-22 历史全库快照（统计已被文首与 live baseline 取代）

依据 manifest revision **4611** 及生成的 `math-gaokao-latex/reports/baseline.md`（2026-10-22）：

- 775 个来源（734 普通高考、41 春季高考），均为 ready。
- 296 套：complete 242、blocked 50、compiled 3、planned 1。
- 162 批：closed 127、closed_with_blockers 31、compiled_pending_review 3、planned 1。
- 门禁：FINALIZED 158、INVALID_OR_STALE 1、VISUAL_FAILED 3。
- 1180/1180 版本有编译记录；build succeeded 289、compiled_pending_review 6。
- 问题账本 1131 条，unresolved 190，其中 blocks_completion 126。
- baseline 列出的门禁未通过批次：phase0-b02、phase2-b58、phase2-b59、phase4-b11。
- PROGRESS.md 某条较早的同日记录写 295 套，manifest revision 4611 和 baseline 报告均为 296；用状态前请重新对照 manifest 和报告。

这些是登记/批次计数，不代表全卷均逐题人工复核，更不代表全项目完成。

## 截至 2026-10-28 的历史完成记录

### 2016 上海文理科，phase2-b14

- `reports/phase2-b14.md`：closed；两卷8版97页全部审查通过。
- 主要提交：最终审核/报告 `e1a7b804`，内容与分页修正 `d2cf43f3`。
- 计划：`docs/superpowers/plans/2026-10-08-gaokao-2016-shanghai.md`。
- 文科Q11、理科Q14的概率模型早期登记 ISSUE-1006/1007；**当前报告和manifest已经结为 closed/complete**。不要照抄历史对话的旧 blocker 状态；如有必要，查当前答案、provenance、issues 再判断。

### 2006 上海春季文科，phase4-b14

- 当前分支最近完成的批次，`reports/phase4-b14.md` 与工作树回执为准，批次 closed。
- 题面/答案阶段、来源判断、四版构建与审查的操作记录在 `math-gaokao-latex/PROGRESS.md` 末尾。

### 1990 全国理科，phase4-b13

- 四版构建和50页视觉审查完成，批次 closed_with_blockers。
- ISSUE-1131：原图未标明 (V_1,V_2) 与两区域的对应，答案保留无序比7:5，不能推测有序比。
- 题面来源无答案页，解析是编者推导且有标注；出版社/版次/原件身份未认证。
- 不重做26题转录、独立盲核或视觉审查；只有取得同版权威证据后再处理阻断。

## 2026-10-22 的历史失败项与候选（必须重新核对）

- phase0-b02：2020全国Ⅰ文科原卷标记取消的第23题按既定决定仍保留，造成5处 heading_number fail。不要擅自删题或将失败改判通过。
- phase2-b58 / b59：1986广东两卷固定来源缺选项图/字形；未找到可逐页核对同版来源。不可借全国卷或异版图补绘，不可凭推测填补。
- phase4-b11：2005上海春季卷当前仍为 planned；manifest已有部分项目元数据/图稿线索，但不能假定来源登记、内容与验收已完成。若选它，先核查上游固定来源、已有文件、历史记录和题目状态。
- 其他批次如 phase3-b23 也有 blocker。先看报告和 issue，再决定是否具备新增证据，不以清状态数字为目标。
- 最近 PROGRESS 的指导是先复核已有工作，再选择“有可核实来源且未重复完成”的项目。新对话不要盲目开启新批次。

## 权威文件与项目门禁

先读以下内容并用当前文件状态交叉核实：

1. `math-gaokao-latex/PROGRESS.md` 末尾：日期序列操作日志，可能有旧状态。
2. `math-gaokao-latex/source-manifest.json`：来源、卷、批次当前主账。
3. `math-gaokao-latex/reports/baseline.md` 与对应 `phase*-*.md`。
4. `math-gaokao-latex/missing-issues.md`。
5. `math-gaokao-latex/README.md`、根目录 `CLAUDE.md`。
6. 每卷 `provenance.json`、`receipts/build.json`、`receipts/review.json`、题目/答案源及四个入口文件。

守则：来源不明或答案不能证明时标 pending/blocked/U；转录与独立求解分离；编者答案明确注明非官方；图稿须 TikZ/PGFPlots；题面和答案源通过确定性脚本渲染四版本，勿手改派生物。四版编译、逐页八项审查、回执当前性、finalize、报告/CSV刷新都是门禁。公共宏改动可能使全库回执失效。避免 `clean-build`（会删除 build PDF）。主代理独占 manifest/共享文件；subagent 写范围要互不重叠。提交只 stage 本批授权路径；不 push。

## 2026-10-28 接续：phase4-b37（1990 广东文史类）已 FINALIZED

- Codex 侧把批次推进到 b01–b36（含 b34 1995 全国文 complete）；本会话复核后取未绑定的 1990 广东文新建 phase4-b37。
- 结果：30 条（选择 1–25、第二卷 26–30）、四版 5/25/7/20 页、零告警；Q26(2) 卷内 -10 经独立双解确认正确，原「-4 冲突」为误算已撤销；Q28–30 卷内无结果，另附推导并与 1990 广东理科对应题核对。批次 closed、paper complete，revision 5355。
- 后续可选：1989 广东文（草稿与来源审计已在库，Q9 题面/答案表内部冲突未决）、1998 全国文（源件选项有误）、1997 全国文（Q23 关系缺失）；大量 2003–2025 春季卷尚未绑定，注意与 Codex 春季队列避让。

## 2026-10-28 接续：phase4-b38（2015 重庆文史类）已 FINALIZED

- 21 题 D 级（选 1–10／填 11–15／解 16–21），四版 5/25/7/21 页、零告警，batch closed、paper complete，revision 5369。
- 盲解全一致；Q20(2) 图取 BC=3（另一解 3√3 已在答案披露）；Q8 框图分式改 `rac`，Q20/Q21 图标签已避让。
- 注意：2015 福建文已有另一会话的 22 题草稿（未登记，Q12 选择答案疑为 B，独立核算应为 A，宜复核后再登记）。
- **纠正（2026-11-03）**：见[2015 福建文科预登记复核报告](../../exams/math-gaokao-latex/reports/2015-fujian-arts-preregistration-review.md)。固定原页 Q12 是 $k\sin x\cos x<x$（末项没有平方），令 $P$ 为该命题、$Q$ 为 $k<1$，有 $P\iff k\le1$；$Q\Rightarrow P$ 而 $P\nRightarrow Q$，故答案 B“必要而不充分”。前一行的 A 判断倒置了“P 是 Q 的条件”的蕴含方向，应视为已被本条取代。

## 2026-10-28 接续：phase4-b39（2015 重庆理工农医类）已 FINALIZED

- 22 题 D 级（选 1–10／填 11–16／解 17–22），四版 6/29/8/23 页、零告警，batch closed、paper complete，revision 5395。
- 盲解改判 Q3 中位数为 20（B）；Q14 按题设重定形；Q7 框图分式、Q21 F₂ 标签已修。
- 「解析」标题单独落在页尾：`\enlargethispage` 2 行不够、3 行会把正文压过页脚，最终按模板 Needspace 行为留档；后续若要治本需改公共排版层。

## 2026-10-28 收工点：phase4-b40（2015 陕西文史类）已 FINALIZED

- 24 题 D 级（选 1–12／填 13–16／解 17–24），四版 6/28/8/22 页、零告警，batch closed、paper complete，revision 5406。
- 盲解改判 Q19(2)=7/8、Q24 b=1/最大值 4；Q18 折叠图按真实拓扑重绘（E 为底面顶点）。
- 本会话完成 b37（1990 广东文）、b38（2015 重庆文）、b39（2015 重庆理）、b40（2015 陕西文）四卷，均已提交。

## 给新对话的启动提示

> 请从 `仓库根` 的 `feat/gaokao-phase0` 分支继续高考数学 LaTeX 项目。先读本交接文档最前面的“2026-11-03 当前状态”，核对 Git status/branch/HEAD；再读 `math-gaokao-latex/PROGRESS.md` 最新记录、live manifest、baseline、相关报告和 issues。phase4-b44（2005 上海理科）已 `FINALIZED` / `closed_with_blockers`，不要重做；Q11/Q20(1) blockers 与官方来源身份未认证边界继续保留。本交接没有预选下一批，需依据 live manifest、固定来源和已有文件重新评估。`typography/` 的排版治理改动属于 main 分支，勿合并或 stage 到题库分支；不切 main、不 push、不覆盖未提交成果。每完成一阶段提交前检查实际 diff、限定 staging 范围并运行 `git diff --cached --check`。

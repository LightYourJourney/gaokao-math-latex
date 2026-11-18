# 2009 天津文科来源接收与转录报告（phase6-b49）

- 来源：`src-919044cfbbbcd3b673f66f382aa397eaac8c780cc68fe39a9f460a410e9fc428`，上游 `普通高考/2009/2009天津文.pdf`；现场下载后重算 SHA-256 为 `5d3e0110cc9145311eed3af1cf0f691ee327cbcba3a0d245e88d635fc136203f`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 563、564；页眉「2009 普通高等学校招生考试（天津卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；分数、根号、下标与四幅图另以 600 dpi 原页复核。
- 结构：22 题（选择 1–10、填空 11–16、解答 17–22）；原页未标分值，不补。第 1 页含 Q1–Q18，第 2 页含 Q19–Q22。
- 图形：Q6 程序框图、Q11 两平行线段交叉与 O、Q12 三视图、Q19 四棱锥 P-ABCD，共 4 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，22 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，21 题与主稿一致。
- 盲解复核发现并改正主稿一处实质错误：**Q16**。主稿初稿误把 $a>4$ 当作有界解集，给出 $[49/9,25/4)$；实际上 $a>4$ 时二次项系数 $4-a<0$、解集在两根之外（两条无界射线），含无穷多整数，必须排除。仅在 $0<a<4$ 时解集为有界区间 $(1/(2+\sqrt a),1/(2-\sqrt a))$，恰含 $1,2,3$ 三个整数，得 $a\in(25/9,49/16]$，与盲解一致。端点：$a=25/9$ 时区间上端为 $3$（不含），只有两个整数；$a=49/16$ 时上端为 $4$（不含），恰三个整数。
- Q22(3) 的 $\dfrac nm$ 依赖 $A$ 在 $x$ 轴上/下方的对称选择，题面未给图，故答案记为 $\pm\dfrac{2\sqrt2}{5}$；解析中说明两支来源。Q22(1) 另补 $\overrightarrow{F_1A}=-2\overrightarrow{F_2B}$ 情形的排除（会推出 $a^2=c^2/3$，与 $a>c$ 矛盾）。
- 产物：`2009_天津卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、4 幅图稿、`provenance.json`（22 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，5/29/7/21 页（共 62 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 62 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D。

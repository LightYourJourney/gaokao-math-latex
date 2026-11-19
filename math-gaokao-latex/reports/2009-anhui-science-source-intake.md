# 2009 安徽理科来源接收与转录报告（phase6-b52）

- 来源：`src-b941eebc7523a0bc24b38b4e37800ba8dbf8c78f117be0fc1a8d728fcb880146`，上游 `普通高考/2009/2009安徽理.pdf`；现场下载后重算 SHA-256 为 `e3986483e52654337c383d27cbe67e80ee0bd62eaf64defba6fe8bcc0cdb0c6d`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向，印刷页 495、496；页眉「2009 普通高等学校招生考试（安徽卷理）」。PDF 自带文字层，`pdftotext -layout` 可读；分数、根号、上下标与四幅图另以 600 dpi 原页复核。
- 结构：21 题（选择 1–10、填空 11–15、解答 16–21）；原页未标分值，不补。第 1 页含 Q1–Q17，第 2 页含 Q18–Q21。
- 图形：Q6 四幅候选图象（与同年安徽文科第 8 题同题同图）、Q13 程序框图、Q14 圆弧向量图、Q18 双四棱锥，共 4 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，21 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理独立完成全卷，20 题一致。
- 盲解冲突与解决（第 18 题）：
  - 盲解第 (1) 问给出 $\arccos(-3/7)\approx115.4^\circ$，与主稿 $90^\circ$ 冲突。复核发现盲解取用 $\overrightarrow{AF}=(2,0,1)$，相当于把 $F$ 放在 $(1,0,1)$，与题设 $CF=2$ 矛盾；按题设应为 $F(1,0,2)$、$\overrightarrow{AF}=(2,0,2)$。此时平面 $BAF$ 与 $DAF$ 的法向量 $(\sqrt2,-2,-\sqrt2)$、$(-\sqrt2,-2,\sqrt2)$ 点积为 $0$，二面角确为 $90^\circ$，主稿维持原结论。
  - 盲解第 (2) 问的 $\frac{2\sqrt2}{9}$ 与主稿一致，并给出「公共部分是以 $ABCD$ 为底、顶点 $Q(-\frac13,0,\frac23)$ 的四棱锥」的几何解释；主稿已把该解释作为截面法结果的核对写入解析。
- 其余关键结论：Q7 $k=\frac73$；Q8 增区间 $\left[k\pi-\frac\pi3,k\pi+\frac\pi6\right]$；Q9 切线 $y=2x-1$；Q10 $\frac4{75}$；Q12 $|AB|=\sqrt{14}$；Q14 最大值 $2$；Q16 面积 $3\sqrt2$；Q17 $EX=\frac{11}{6}$；Q21 $a_1\in(0,1)\cup(3,+\infty)$。
- 说明：Q18 的 $E$、$F$ 必须取在底面同侧（题图如此）；若反向，两锥只在底面相交、公共体积为 $0$，故题面隐含同侧。
- 产物：`2009_安徽卷_理科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、4 个图稿、`provenance.json`（21 题三角色）与 `receipts/`；`2009/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，5/26/7/19 页（共 57 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 57 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D。

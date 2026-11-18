# 2008 北京文科来源接收与转录报告（phase6-b42）

- 来源：`src-a24ac8b08aa9604b1cc0ea37ab616d01d66aedaea62913dfa7b4b124fcdb8df4`，上游 `普通高考/2008/2008北京文.pdf`；现场下载后重算 SHA-256 为 `9d725e3f7011f50eddddd9bebd62825365c218b08fa0c920ac23b57228f590f9`，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 427、428；页眉「2008 普通高等学校招生考试（北京卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与三幅图另以 300/400 dpi 原页复核。
- 结构：20 题（选择 1–8、填空 9–14、解答 15–20）；原页未印分值，不补。第 1 页含 Q1–Q14，第 2 页含 Q15–Q20。
- 图形：Q8 正方体与四选项图象、Q13 折线与坐标网格、Q16 三棱锥 P-ABC，共 3 幅 TikZ 矢量图，`expected_occurrences` 均为 2。
- 固定源缺陷（照录并登记）：
  1. Q14 在「条件序号是____」之后混入「$T(a)$ 表示非负实数 $a$ 的整数部分……第 2008 棵树种植点的坐标」一段，但题面没有任何植树递推方案，两个坐标空无法作答；该段与 2008 北京理科第 14 题尾段相同（ISSUE-1474）。可判定部分答 ②。
  2. Q20(1) 印作「求 $\lambda$ 及 $a_1$ 的值」，而题干已给 $a_1=1$；公开同题版本为「求 $\lambda$ 及 $a_3$ 的值」。按字面 $\lambda=3$、$a_1=1$；按同题版本 $a_3=-3$（ISSUE-1475）。
- 答案：固定源无答案页，20 题全部由本库独立推导（非官方，`official_answer=null`，grade D）；盲解代理在未读主稿的情况下独立完成全卷，20 题结论一致。
- 产物：`2008_北京卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、3 幅图稿、`provenance.json`（20 题三角色）与 `receipts/`；`2008/` 下四份规范 Markdown。
- 验收：四版 build `succeeded`，4/22/6/16 页（共 48 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 48 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`，卷 `blocked`（2 条 open blocker）。
- 未完成：Q14、Q20(1) 需同版官方勘误或更清晰原页确认；确认前维持 blocked，不改题面字面。

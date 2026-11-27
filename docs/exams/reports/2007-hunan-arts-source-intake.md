# 2007 湖南文科来源接收与转录报告（phase6-b41）

- 来源：`src-65d03ae2ea8d49e31abcf96e49caaad28a51110d9771abac5da81b26d5f49cba`，上游 `普通高考/2007/2007湖南文.pdf`；现场下载后重算 SHA-256 为 `8e889ae321ffa864b24c505b40e7e96956b301487f5a106264b7fcd9f943e068`，512146 字节，与 manifest `artifact` 一致。
- 原页：2 页 A3 横向（1190.55 × 841.89 pt），印刷页 381、382；页眉「2007 普通高等学校招生考试（湖南卷文）」。PDF 自带文字层，`pdftotext -layout` 可读；公式、上下标、选项与三幅图均另以 300/400 dpi 原页复核。
- 结构：21 题（选择 1–10、填空 11–16、解答 17–21）；原页未印分值，不补。第 1 页含 Q1–Q17，第 2 页含 Q18–Q21，`source_pages` 按此登记。
- 图形：Q6 正四棱柱与 E、F；Q7 水位频率分布直方图（30–51 米，21 组）；Q18 直二面角 α-PQ-β。三幅均以 TikZ 矢量重绘，`expected_occurrences` 均为 2。
- 答案：固定源无答案页，21 题全部由本库独立推导（非官方，`official_answer=null`）；盲解代理在未读主稿的情况下独立完成全卷。比对后发现两处主稿错误并已改正：Q7 由 49 米改为 50 米（应比较「水位不低于阈值」的尾部概率之和：P(X≥49)=1.5%>1%，P(X≥50)=0.5%≤1%）；Q21 由 13、a=−1 改为 16、a=−2（f'(x)=x²+ax+b，a²−4b=(x₂−x₁)²，最大值 16；穿根条件给出 a=−2、b=−1，f=x³/3−x²−x）。其余 19 题结论一致。
- 产物：`2007_湖南卷_文科/` 下 `questions.tex`、`answers.tex`、`answers_short.tex`、四版入口、3 幅图稿、`provenance.json`（21 题三角色）与 `receipts/`；`_试题.md`、`_答案要点.md`、`_解析正文.md`、`_含解析.md` 在 `2007/` 下。
- 验收：四版 build `succeeded`，5/24/7/18 页（共 54 页），0 error / 0 missing char / 0 Overfull / 0 Underfull / 0 undefined reference；review 54 页八类检查全 pass，0 豁免；`finalize-batch` 返回 `FINALIZED`，批次 `closed`，卷 `complete`。
- 未完成：无阻断项；来源出版信息与官方身份仍未认证，答案等级记为 D（非官方独立推导）。

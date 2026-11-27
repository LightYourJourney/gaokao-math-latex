# 2007 北京文科候选卷：Q1–Q20 题面独立复核

- 日期：2026-11-03。
- 固定 PDF：source `src-71817304e261efb7deaf51c2a5f400421a95ac91a90313d8f558bee701a624f9`，SHA-256 `e5356797259eb22cc2b4f23019ad7ab044f282bdfc2a65df94dbbdcc502cfff5`；2 页 A3，印刷页 353–354。
- 复核题面：`2007/2007_数学真题_北京文_试题.md`，更新核校状态后的 SHA-256 `ba1a775fe5aae82b95e260fd68e99b43f3b8c909f67103fdd867f9c3561e63a0`。
- 复核者：`/root/review_2007_beijing_arts_transcription`（Luna/high），没有参与 Q1–Q10 或 Q11–Q20 的分段转录。只读取固定来源 PDF、对应原页渲染图和题面稿；未读取答案或解析，未写入仓库文件。

## 逐题结果

| 题号 | 结果 | 题号 | 结果 |
| --- | --- | --- | --- |
| Q1 | PASS | Q11 | PASS |
| Q2 | PASS | Q12 | PASS |
| Q3 | PASS | Q13 | PASS |
| Q4 | PASS | Q14 | PASS |
| Q5 | PASS | Q15 | PASS |
| Q6 | PASS | Q16 | PASS |
| Q7 | PASS | Q17 | PASS |
| Q8 | PASS | Q18 | PASS |
| Q9 | PASS | Q19 | PASS |
| Q10 | PASS | Q20 | PASS |

未发现题干、公式、指数/下标、关系符号、数值、选项、表格或小问编号差异；无须修订规范题面。重点逐字核对如下：

- Q5：`(C_{26}^{1})^2 A_{10}^{4}`、`A_{26}^{2}A_{10}^{4}`、`(C_{26}^{1})^2 10^4`、`A_{26}^{2}10^4` 四项与原页一致。
- Q7：面面平行关系，以及四个选项里的直线包含、线面平行和异面/平行关系与原页一致。
- Q11：向量坐标 $(2,4)$、$(1,1)$，以及 $\boldsymbol b\perp(\boldsymbol a+\lambda\boldsymbol b)$ 一致。
- Q16：原印递推为 $a_{n+1}=a_n+cn$，不是 $c^n$ 或 $c_n$。
- Q20：$l_1,l_2$ 分别是函数图象在 A、B 两点的切线，M、N 分别是 $l_1,l_2$ 与 $x$ 轴交点；规范题面对应一致。

复核覆盖题面全部 Q1–Q20。该轮确认三处原卷图位对应题面占位，但没有逐笔审查矢量重绘；图稿完成后，独立复核者 `/root/review_2007_beijing_arts_figures`（Luna/high）分别对照源页裁片，Q13、Q17、Q19 全部 PASS，详见 [题图矢量重绘与独立核对](2007-beijing-arts-figure-review.md)。当前题面只将三处占位替换为本地 TikZ 独立段落链接，题干文字未改；当前 full-file SHA-256 为 `428c92e4a0d0f0e1d8d8197e96429734f2425c9e6eea4a368fe86496f36f2500`。题面 frontmatter 的核校状态保持不变。

本地 OCR 与外部 API 均未调用；代理推理费用不可见，人工时间未计量。固定 PDF 仍只是本库候选副本的内部绑定，发布者、出版者、版次、复制链与官方身份未核；原 PDF 没有答案页，`official_answer=null`。本阶段只表示题面独立复核通过，不表示答案/解析完成、卷级验收或长期语料库完成。

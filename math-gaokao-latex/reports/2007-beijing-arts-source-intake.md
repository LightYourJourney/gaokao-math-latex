# 2007 北京文科候选卷：固定来源接收

- 日期：2026-11-03。工作树：`仓库根`，工作分支。
- 固定 source：`src-71817304e261efb7deaf51c2a5f400421a95ac91a90313d8f558bee701a624f9`；路径 `普通高考/2007/2007北京文.pdf`。
- 上游来源库 `gaokaomath-src` 固定 commit：`34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。该 checkout 的 HEAD 与固定 commit 相同，状态为 `main...origin/main` 且没有本地改动。

## 字节与文档核对

| 项目 | 结果 |
| --- | --- |
| Manifest SHA-256 | `e5356797259eb22cc2b4f23019ad7ab044f282bdfc2a65df94dbbdcc502cfff5` |
| 现场 SHA-256 | `e5356797259eb22cc2b4f23019ad7ab044f282bdfc2a65df94dbbdcc502cfff5` |
| Manifest Git blob | `3207132ef37ec52e6dfd19ffac856388f4c053f1` |
| 固定 commit 路径 blob | `3207132ef37ec52e6dfd19ffac856388f4c053f1` |
| 文件大小 / 页数 | 511024 bytes / 2 页 |
| 页面尺寸 | A3 横向，1190.55 × 841.89 pt |
| PDF 检查 | manifest `pdf_check=passed`；`pdfinfo` 成功 |

现场计算与上游固定 commit 的对象指纹一致。该绑定只确认本地候选 PDF 字节及仓库对象，不证明发布者、出版者、版次、来源链或官方身份。

## 原页内容检查

两页均以 220 dpi 渲染并目视查看；`pdftotext -layout` 仅用于辅助定位，题面判断依据为原页。

| PDF 页 | 印刷页 | 可见范围 | 页面内容 |
| --- | --- | --- | --- |
| 1 | 353 | Q1–Q17 | 选择题 Q1–Q8，填空题 Q9–Q16，解答题 Q17 起始；可见 Q13 赵爽弦图和 Q17 立体几何图 |
| 2 | 354 | Q18–Q20 | 三道解答题；Q19 有矩形坐标图，未见答案或解析内容 |

题签可辨为“2007 普通高等学校招生考试（北京卷文）”。可见题量为选择 8 题、填空 8 题、解答 4 题，共 20 题。PDF 是两页题面，不含答案、解析或评分标准。第 1 页有 Q13 弦图、Q17 立体几何图；第 2 页有 Q19 矩形坐标图。Q20 的题干虽提到两函数图象相交，原页未见附图。

`analyze_pdf.py --no-cache --include-text` 的页级结果：

- 第 1 页：`review`，1418 个非空白字符，7 个可疑字符；文字层会压平部分公式位置和关系符号。
- 第 2 页：`text_candidate`，471 个非空白字符，0 个可疑字符。
- 两页均有文字层，`document_classification=mixed_candidates`；本次 `model_calls=0`、`ocr_calls=0`。

因此后续转录须逐题对照固定 PDF 页面，不得仅据提取文字猜补公式、选项关系符号或图示。

## 登记边界与下一阶段

清单中该 source 当前为 `source_state=ready`、`paper_id=null`、`paper_relation=null`。现有项目目录尚无 2007 北京文科 paper/规范题面；本阶段只接收并核验来源，没有更改 manifest、issue ledger 或规范题稿，也没有登记 paper/batch。题面文字、答案及评分材料的官方身份均未核。

下一阶段：转录 Q1–Q20，逐页逐题核对题号、分值、数学符号、选项、题图和小问结构，再独立复核题面。OCR 候选不是规范题面；如现有文字层辅助不足，再按 [本地 OCR 工作规范](../docs/OCR_WORKFLOW.md) 显式路由并保留候选与原页关系。本阶段不表示题面转录完成、paper 完成或长期语料库完成。模型/OCR与外部 API 成本为零；人工时间未计量。

# 2005 上海文科普通卷：固定来源接收

- 日期：2026-11-03；工作树 `仓库根`，工作分支。
- 固定 source `src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846`，路径 `普通高考/2005/2005上海文.pdf`；manifest revision 6100 中状态为 `ready`，当前 `paper_id=null`、`paper_relation=null`、`track=null`。
- 来源库固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场 PDF SHA-256 `952989a262e3f7b34a425ccb6e2132af7e88408a387edae50f59a9505ebe46a1`、Git blob `d3849e9bf2f21c95b4823be90b24669b74ee1685`、512658 bytes、2 页，与清单一致；manifest 标记 `git_oid_verified=true`、`pdf_check=passed`。
- 固定副本位于忽略目录 `.work/ocr-local/sources/2005-shanghai-arts.pdf`。PDF 元数据显示两页 A3 横向；原页渲染位于 `.work/ocr-local/2005-shanghai-arts/`。

## 原页内容与文字层检查

原页题签为“2005 普通高等学校招生考试（上海卷文）”，印刷页码264–265。题面共22题：填空Q1–Q12、选择Q13–Q16、解答Q17–Q22。可见图形题为Q12（两种棱柱拼接示意）、Q17（长方体）和Q21（抛物线）。这两页均为题面，未见答案、解析或评分内容。题签与manifest文件名中的上海文科普通卷候选一致；出版者、版次、复制/扫描链和官方身份未核实，不能据 `ready` 或题签宣称来源已认证。既有2005上海春季卷是不同考试，不与本来源合并。

`analyze_pdf.py --no-cache --include-text` 结果为 `document_classification=mixed_candidates`；两页均有文字层且无嵌入图像对象：

- 第1页：`text_candidate`，1401个非空白字符、0个可疑字符。
- 第2页：`review`，623个非空白字符、7个可疑字符；文字层的栏序和数学符号只作定位候选。
- 两页以150 DPI整页渲染并目视检查；原页题签、页码、题号范围及图示均清晰。第2页进入人工复核路由，逐题转录时继续直接核对原页，不以文字层覆盖原文。
- 本阶段 `model_calls=0`、`ocr_calls=0`、外部 API 调用0。没有对已有文字层页面重复启动OCR；题面仍须逐题以固定原页为准。

## 本阶段状态

仅完成固定来源取件、SHA/Git blob/大小/页数核对、题签/页序/题量/图位与文字层路由；没有修改manifest或issue ledger，没有登记paper/batch、转录题面、推导答案或创建图稿。`official_answer`仍未知；固定PDF没有答案证据。人工耗时未知，模型/API调用为0。

下一阶段转录Q1–Q22并逐题对照两页固定原图，记录无法辨认内容或来源内疑点；之后独立复核题面。本报告不表示来源认证、题面转录完成、答案/解析验证、整卷验收或长期语料库完成。

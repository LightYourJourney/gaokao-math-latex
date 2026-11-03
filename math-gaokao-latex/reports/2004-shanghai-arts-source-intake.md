# 2004 上海文科普通卷：固定来源接收

- 日期：2026-11-03；工作树 `仓库根`，分支 `feat/gaokao-phase0`。
- 固定 source `src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290`，路径 `普通高考/2004/2004上海文.pdf`；manifest revision 6117 中状态为 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`。当前没有对应 paper、项目目录或规范题稿。
- 来源库固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场 PDF SHA-256 `4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad`、Git blob `302ee6023a26b028cf7c89f24359ba818a2a7b3b`、527431 bytes、2 页，与清单一致；manifest 标记 `git_oid_verified=true`、`pdf_check=passed`。
- 固定副本与页图位于忽略目录 `.work/ocr-local/sources/2004-shanghai-arts/`。PDF 为两页 A3 横向；现场 `pdfinfo` 页数、文件大小与来源清单相符。

## 原页内容与文字层检查

原页题签为“2004 普通高等学校招生考试 (上海卷文)”，印刷页码200–201。题面共22题：填空Q1–Q12、选择Q13–Q16、解答Q17–Q22；原页可见图稿位为Q5、Q18、Q20、Q21。两页均为题面，未见答案、解析或评分内容。题签与manifest文件名中的上海文科普通卷候选一致；出版者、版次、复制/扫描链和官方身份未核实，不能据 `ready` 或题签宣称来源已认证。已登记的2004上海春季卷属于另一考试，未与本来源合并。

`analyze_pdf.py --no-cache --include-text` 结果为 `document_classification=mixed_candidates`；两页均有文字层且无嵌入图像对象：

- 第1页：`review`，1444个非空白字符、7个可疑字符；符号与排版须以原页为准。
- 第2页：`text_candidate`，714个非空白字符、0个可疑字符。
- 两页以150 DPI与300 DPI整页渲染并目视检查；题签、印刷页码、题号范围、正文及图稿位可辨。第1页保留人工复核路由，逐题转录继续直接核对原页，不以文字层覆盖原文。
- 本阶段 `model_calls=0`、`ocr_calls=0`、外部 API 调用0。因两页均有原生文字层且 `image_objects=0`，没有启动OCR；文字层候选文字不作为规范题稿或题目正确性证据。

项目门禁：`local_ocr.py doctor` 显示 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 均为 `ready`；`source_manifest.py validate` 通过；`manifest_csv.py --check` 显示当前且775行。

## 本阶段状态

仅完成固定来源取件、SHA/Git blob/大小/页数核对、题签/页序/题量/图位与文字层路由；没有修改manifest或issue ledger，没有登记paper/batch、转录题面、推导答案或创建图稿。`official_answer`未知；固定PDF没有答案证据。人工耗时未知，模型/API调用为0。

下一阶段转录Q1–Q22并逐题对照两页固定原图，记录无法辨认内容或来源内疑点；之后独立复核题面。本报告不表示来源认证、题面转录完成、答案/解析验证、整卷验收或长期语料库完成。

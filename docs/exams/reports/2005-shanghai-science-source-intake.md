# 2005 上海理科普通卷：固定来源接收

- 日期：2026-11-03；工作树 `仓库根`，工作分支。
- 固定 source `src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e`，路径 `普通高考/2005/2005上海理.pdf`；manifest revision 6109 中状态为 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`。当前没有对应 paper、项目目录或规范题稿。
- 来源库固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场 PDF SHA-256 `092e8e90dc1430ab2fa8b8ce79e072e317559e6bef29f1cb7461e9423925ec31`、Git blob `a76d7aa8877b7fa25ac09cb596b440c0545f4fa6`、505945 bytes、2 页，与清单一致；manifest 标记 `git_oid_verified=true`、`pdf_check=passed`。
- 固定副本与页图位于忽略目录 `.work/ocr-local/sources/2005-shanghai-science/`。PDF 为两页 A3 横向；现场 `pdfinfo` 页数、文件大小与来源清单相符。

## 原页内容与文字层检查

原页题签为“2005 普通高等学校招生考试（上海卷理）”，印刷页码262–263。题面共22题：填空Q1–Q12、选择Q13–Q16、解答Q17–Q22；原页可见图稿位为Q11、Q12、Q17、Q19。两页均为题面，未见答案、解析或评分内容。题签与manifest文件名中的上海理科普通卷候选一致；出版者、版次、复制/扫描链和官方身份未核实，不能据 `ready` 或题签宣称来源已认证。已登记的2005上海春季卷属于另一考试，未与本来源合并。

`analyze_pdf.py --no-cache --include-text` 结果为 `document_classification=text_layer_candidate`；两页均有文字层且无嵌入图像对象：

- 第1页：`text_candidate`，1503个非空白字符、0个可疑字符。
- 第2页：`review`，699个非空白字符、7个可疑字符；行列与数学符号须以原页为准。
- 两页以150 DPI整页渲染并目视检查；题签、印刷页码、题号范围、正文及图稿位可辨。第2页保留人工复核路由，逐题转录继续直接核对原页，不以文字层覆盖原文。
- 本阶段 `model_calls=0`、`ocr_calls=0`、外部 API 调用0。因两页均有文字层且 `image_objects=0`，没有启动OCR；候选文字不作为规范题稿或题目正确性证据。

项目门禁：`local_ocr.py doctor` 显示 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 均为 `ready`；`source_manifest.py validate` 通过；`manifest_csv.py --check` 显示当前且775行。

## 本阶段状态

仅完成固定来源取件、SHA/Git blob/大小/页数核对、题签/页序/题量/图位与文字层路由；没有修改manifest或issue ledger，没有登记paper/batch、转录题面、推导答案或创建图稿。`official_answer`未知；固定PDF没有答案证据。人工耗时未知，模型/API调用为0。

下一阶段转录Q1–Q22并逐题对照两页固定原图，记录无法辨认内容或来源内疑点；之后独立复核题面。本报告不表示来源认证、题面转录完成、答案/解析验证、整卷验收或长期语料库完成。

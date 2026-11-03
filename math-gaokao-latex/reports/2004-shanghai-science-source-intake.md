# 2004 上海理科普通卷：固定来源接收

- 日期：2026-11-04；工作树 `仓库根`，分支 `feat/gaokao-phase0`。
- 固定 source `src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a`，路径 `普通高考/2004/2004上海理.pdf`；manifest revision 6122 中状态为 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`。当前没有对应 paper、项目目录或规范题稿。
- 来源库固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场 PDF SHA-256 `9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e`、Git blob `9bfec0f8159c4aac8d9991979f2afd760fb0c11b`、510791 bytes、2 页，与清单一致；manifest 标记 `git_oid_verified=true`、`pdf_check=passed`。
- 固定副本与页图位于忽略目录 `.work/ocr-local/sources/2004-shanghai-science/`。PDF 为两页 A3 横向；现场 `pdfinfo` 页数、文件大小与来源清单相符。

## 原页内容与文字层检查

原页题签为“2004 普通高等学校招生考试 (上海卷理)”，印刷页码 198–199。题面共 22 题：填空 Q1–Q12、选择 Q13–Q16、解答 Q17–Q22；原页可见图稿位为 Q5、Q18、Q21（共 3 幅）。两页均为题面，未见答案、解析或评分内容。题签与 manifest 文件名中的上海理科普通卷候选一致；出版者、版次、复制/扫描链和官方身份未核实，不能据 `ready` 或题签宣称来源已认证。已登记的 2004 上海春季卷属于另一考试，未与本来源合并。

`analyze_pdf.py --no-cache --include-text` 结果为 `document_classification=text_layer_candidate`；两页均有原生文字层且无嵌入图像对象（`image_objects=0`）：

- 第 1 页：`text_candidate`，1475 个非空白字符、0 个可疑字符；版面分 3 栏，包含填空 Q1–Q12、选择 Q13–Q16、解答 Q17–Q19，题图 Q5 与 Q18。
- 第 2 页：`text_candidate`，730 个非空白字符、0 个可疑字符；版面分 3 栏，包含解答 Q20、Q21、Q22，题图 Q21。
- 两页以 150 DPI 与 300 DPI 整页渲染并目视检查；题签、印刷页码、题号范围、正文及图稿位清晰可辨。逐题转录继续直接核对原页高分辨率渲染图，不以文字层盲目覆盖原文。
- 本阶段 `model_calls=0`、`ocr_calls=0`、外部 API 调用 0。因两页均有高质量原生文字层且 `image_objects=0`，未启动外部 OCR；文字层候选文字不直接作为规范题稿或题目正确性证据。

项目门禁：`local_ocr.py doctor` 显示 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 部署资产均为 `ready`；`source_manifest.py validate` 通过；`manifest_csv.py --check` 显示当前且 775 行。

## 本阶段状态

仅完成固定来源取件、SHA/Git blob/大小/页数核对、题签/页序/题量/图位与文字层路由；没有修改 manifest 或 issue ledger，没有登记 paper/batch、转录题面、推导答案或创建图稿。`official_answer` 未知；固定 PDF 没有答案证据。人工耗时未知，模型/API 调用为 0。

下一阶段转录 Q1–Q22 并逐题对照两页固定原图，记录无法辨认内容或来源内疑点；之后独立复核题面。本报告不表示来源认证、题面转录完成、答案/解析验证、整卷验收或长期语料库完成。

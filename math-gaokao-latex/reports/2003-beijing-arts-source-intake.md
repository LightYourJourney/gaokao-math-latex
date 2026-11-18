# 2003 北京文科候选卷：固定来源接收与文字层路由

- 日期：2026-11-04；canonical worktree：`仓库根`；分支：工作分支；source manifest revision：6146。
- 固定候选 source：`src-dcc6a2c21c7b8e7b8f23f5188f34d7f542f94e40f4219b54cfb85a0d7004bc0f`，manifest 相对路径 `普通高考/2003/2003北京文.pdf`。manifest 状态为 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`；本阶段未修改 manifest 或建立 paper/batch 绑定。
- 固定来源 checkout：`gaokaomath-src`，HEAD `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`，工作区干净。PDF 大小 498,873 bytes；现场 SHA-256 `7fc0fd289fc486a0ae1c16a9ab5b4f0561830897df6e8897c50666f03d511913`，Git blob `098d2daa4a08a3ef69b98b656842324f4819ece6`，均与 manifest 相符。
- PDF 为 2 页 A3 横向（1190.55 × 841.89 pt），未加密。页内题签可见“2003 普通高等学校招生考试（北京卷文）”，印刷页码 126–127；该题签只作为页面可见文字记录，不认证出版者、版次、来源链或官方身份。

## 页面结构与文字层路由

| PDF 页 | 印刷页码 | 可见范围 |
| --- | ---: | --- |
| 1 | 126 | Q1–Q17；选择题 Q1–Q10、填空题 Q11–Q14、解答题 Q15–Q17 |
| 2 | 127 | Q18–Q20 |

- `analyze_pdf.py --no-cache --include-text` 判为 `text_layer_candidate`，文档完整；第 1、2 页分别有 1,442、577 个非空白字符，可疑字符均为 0；两页均有文字层、无图像对象。`pdftotext -layout` 的内容仅作为定位候选，跨栏次序及二维公式仍须以原页图为准。
- 两页以 Poppler 26.10.0 的 `pdftoppm` 渲染并逐页查看；页面图和原始分析 JSON 保存在忽略目录 `.work/phase4-b48/intake/main/`。完整可见题号范围为 Q1–Q20；本阶段未发现答案页或解析页。
- 按 `docs/OCR_WORKFLOW.md`，本 PDF 有可用文字层且没有 raster-only 页面；本阶段 `ocr_calls=0`、`model_calls=0`，未调用 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 或外部来源。文字层不替代逐题原图复核。

## 边界

本阶段固定并复核了候选文件字节、PDF 页数/尺寸、题签、印刷页码、题号范围和文字层路由。发布者、出版者、版次、原始发布渠道、复制/扫描链和官方身份均未核实；来源仍是未绑定候选。题面草稿与独立复核已在忽略工作区完成，Q1–Q20 未发现实质转录差异；下一阶段将把题面和复核记录纳入跟踪目录。本报告不认证来源，也不表示题面或整卷已完成。

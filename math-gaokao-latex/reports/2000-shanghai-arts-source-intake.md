# 2000 上海文科候选卷：固定来源接收

- 日期：2026-11-03；工作树 `仓库根`，分支 `feat/gaokao-phase0`。
- 固定 source `src-8d14b1f9f511665ea10dbda45959a3b445a17806415be6b034f816bec663d7f5`，路径 `普通高考/2000/2000上海文.pdf`；清单 revision 6066 中状态为 `ready`，当前 `paper_id=null`、`paper_relation=null`、`track=null`。
- 来源库 `https://github.com/deekur/gaokaomath` 固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场 PDF SHA-256 `35e5d6f6bf052fcd9a2b91a1aa4215766fd4121425cfec7a62cfc4cdc7ab02a1`、Git blob `91ece8675e9cd47367f547bd9b0b6b4979b77d0e`、597723 bytes、2 页，与清单绑定一致；manifest 标记 `git_oid_verified=true`、`pdf_check=passed`。
- 忽略目录 `.work/ocr-local/sources/2000-shanghai-arts.pdf` 保存固定副本；两页 180 DPI 渲染存于 `.work/ocr-local/rendered/2000-shanghai-arts-180dpi/`。分析 JSON 存于 `.work/ocr-local/logs/2000-shanghai-arts-analyze-pdf.json`。

## 原页内容与文字层检查

PDF 两页 A3 横向，印刷页码 72–73。第 1 页题签可见“2000 普通高等学校招生考试（上海卷文）”；第 2 页续题。可见题目共 22 题：填空 Q1–Q12、选择 Q13–Q16、解答 Q17–Q22。原页含 Q8 线段函数图、Q11 线性规划阴影图、Q18 四面体图及 Q20 坐标轴图。PDF 只有题面，未见答案、解析或评分页。现有项目没有 2000 上海普通卷文科的规范题稿；来源名称与原页题签相符，但出版者、版次、复制/扫描链和官方身份未核，不能据 `ready` 或题签宣称来源已认证。

`analyze_pdf.py --no-cache --include-text` 结果为 `document_classification=mixed_candidates`，两页均有文字层、无嵌入图像对象：

- 第 1 页：`review`，1437 个非空白字符、7 个可疑字符；多栏数学内容的提取顺序交错。
- 第 2 页：`text_candidate`，800 个非空白字符、0 个可疑字符。
- 原页渲染逐页目视检查；本阶段 `model_calls=0`、`ocr_calls=0`。文字层仅作定位候选，后续逐题以固定原页核对，不自动用 OCR 或文本抽取覆盖题稿。

## 本阶段状态

仅完成来源固定、题签/页序/题量/题图位置核查和文字层路由；没有修改 manifest 或 issue ledger，没有登记 paper/batch，没有转录题面、求解答案或创建图稿。官方答案状态保持未知；本 PDF 没有答案证据。OCR/外部 API 调用为 0，子代理费用为 0，人工耗时未计量。

下一阶段转录 Q1–Q22 并逐题对照两页固定原图，保留原件疑点和任何无法辨认处；其后另行独立复核题面。本报告不表示来源认证、题面转录完成、整卷验收或长期语料库完成。

# 2006 辽宁文理候选卷：固定来源接收

- 日期：2026-11-03；按 `docs/OCR_WORKFLOW.md` 执行。
- 固定上游仓库：`https://github.com/deekur/gaokaomath`，commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。只读 checkout HEAD 与该 commit 一致，工作树干净。
- 来源物化状态核验：manifest 所列 775 份 PDF 均与固定 Git blob 匹配，0 mismatched、0 missing。

## 来源指纹

| 卷 | source ID | 上游路径 | SHA-256 | Git blob | 字节数 |
|---|---|---|---|---|---:|
| 2006 辽宁文科 | `src-b784613ebc50375b17eb4a91083b447879ebb9ed75bb6a76227bb74345cfbfd3` | `普通高考/2006/2006辽宁文.pdf` | `bbb83af465d4650c594f23a879d82dea43a86f805b6fc8712d25809aac7fda22` | `ec6b1416c0054c34d9f4ea82b922188fbfd76a53` | 508627 |
| 2006 辽宁理科 | `src-db3cbfe3d2c96ec3cbe88c45ad7986cf79f4899fd76a3a73b7c64721f0e67569` | `普通高考/2006/2006辽宁理.pdf` | `f680814a4fc5835d805772711f91c5921f12fb92b1740b9c0e9279fa6def427a` | `130d6a55003fe33977ff2091dfdd2ff26110bb42` | 507180 |

两个 PDF 的现场 SHA-256 与 Git blob 均匹配 manifest 和固定 commit。来源 ID 当前为 `ready`、尚未绑定 paper；文件名和卷内题签支持候选卷名及文理属性，不代表发布者或版本身份已认证。

## 原件检查与 OCR 路由

- 两份 PDF 均为 2 页 A3 横向。文科题签为“2006 普通高等学校招生考试（辽宁卷文）”，印刷页 310–311；理科题签为“2006 普通高等学校招生考试（辽宁卷理）”，印刷页 308–309。每卷 PDF 第 1 页含 Q1–Q19，第 2 页含 Q20–Q22；两卷均为 22 题。原件未见答案、解析或评分标准。
- 200 DPI 渲染的四页均已目视检查。文科 Q15、Q19 有题图，理科 Q18 有题图；题图和公式须在转录时继续逐项对照原页。
- `analyze_pdf.py` 将两份文档判为 `mixed_candidates`，每卷第 1 页为 `review`、第 2 页为 `text_candidate`。四页均有文字层、无页面图像对象；第 1 页分别含 28 个可疑字符（文科 1654、理科 1985 个非空白字符），第 2 页无可疑字符（文科 483、理科 538 个非空白字符）。所有页均要求内容复核。
- OCR doctor 确认 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 三套本机资产为 `ready`。本阶段没有调用模型：原页文字层可用，按工作规范先保留为识别候选，转录与可疑公式/符号由人工对照原图确认；未将模型部署状态误记为本批次推理成功。
- 原始图、分析 JSON 与渲染图保存在忽略目录 `.work/ocr-local/liaoning-2006/`，不提交 PDF 或 PNG。

## 未核实边界与下一步

来源的发布者、出版者、版次、扫描或重排来源链、官方身份均未核实；`official_answer` 不适用且不得据此候选源补写。该阶段仅完成来源固定、文件指纹、页序、题签与题图位置核验，未登记 paper/batch，未绑定 source，未转录题面或编辑 manifest / issues。下一阶段独立转录文理两卷 Q1–Q22，主会话逐题对照原页校核。成本未知；本阶段无外部模型或付费 API 调用。

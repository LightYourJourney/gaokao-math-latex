# 2000 上海理科候选卷：固定来源接收与文字层路由

- 日期：2026-11-03；候选来源 `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`。
- manifest revision：6087。当前 source 记录为 `ready`，`paper_id=null`、`paper_relation=null`，本阶段不登记试卷或批次。
- 固定候选 PDF：上游只读仓库 `gaokaomath-src/普通高考/2000/2000上海理.pdf`，commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`；SHA-256 `b798af61afdac624589769db5bbafe734aa9a0016973bd00b3f5bc8028ab3a40`，Git blob `493b64433fdd83bb4f13a587a8e12a53b2a447e9`，596,831 bytes。与 manifest 元数据一致；上游工作树干净。
- PDF 为 A3 横向两页，印刷页 70–71。原页题签为“2000 普通高等学校招生考试（上海卷理）”，共 Q1–Q22，页面只含试题与题图，不含答案或解析。发布者、版次、复制链与官方身份仍未核验。

## 页面与识别路由

- `pdfinfo`、`pdfimages -list` 与 `analyze_pdf.py --no-cache --include-text` 检查该 PDF；整体分类为 `text_layer_candidate`。PDF 第 1 页有 1,478 个非空白文字字符，第 2 页有 823 个，均为 `text_candidate`、可疑字符 0、图像对象 0；两页仍标记 `requires_content_review=true`，文字层不作为题面正确性的证明。
- 两页均以 Poppler 26.10.0、120 dpi 渲染为 1985×1404 PNG，并逐页目视确认版面、题号范围、图表与印刷页码。第 1 页含 Q8 函数图和 Q18 四面体图，第 2 页含 Q20 坐标示意图；可见内容清晰，无扫描缺页迹象。
- `pdftotext -layout` 的候选文本存在三栏交错及部分公式拆行，保留在忽略目录，仅供定位。随后逐题以固定 PDF 页为准，不直接复制抽取文本。
- 按 OCR 工作规范，此 PDF 有可用文字层且无 raster-only 页面，本阶段不调用 Xiaomi-OCR-0、PaddleOCR-VL-1.6 或 MinerU。`local_ocr.py doctor` 确认三引擎部署资产均为 ready（Xiaomi revision `bbd8cf8d21f256b3644b44cb860f3a7cecb93c30`、Paddle revision `c5630abae1d940eafe0697512a0325494b02ab42`、MinerU revision `358310b4f64b95f9fefc372ad899356e4111f376`）；本来源的识别调用数为 0，未由 OCR 补字或裁定题意。

## 可复核缓存

以下输入、副本、页图和抽取结果留在忽略目录 `.work/ocr-local/sources/2000-shanghai-science/`，不进入 Git：

- `source.pdf` SHA-256 与固定上游 PDF 相同：`b798af61afdac624589769db5bbafe734aa9a0016973bd00b3f5bc8028ab3a40`。
- `triage.json` SHA-256：`614aa6df53614b682b9b66efed89a7c68dc81e52031b7c9afbf791c33db3d37f`。
- `text-layer-layout.txt` SHA-256：`37f4439d019ff1cf0d1a1ebb030012ddcd3a1023746dfb85c80c6f796ef11a6f`。
- `page-1.png`、`page-2.png` 为上述原 PDF 页面渲染；渲染缓存对应原 PDF SHA、原页码和 120 dpi。

本阶段只完成来源接收、完整性核验、页面检查与文字层路由；未创建规范题稿、答案、解析、图稿或 provenance，未登记 paper/batch/issue，未正式构建或做题库测试。下一阶段转录 Q1–Q22，逐题核对原页；任何无法读清处保留 U/待核。

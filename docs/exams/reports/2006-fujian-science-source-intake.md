# 2006 福建理科候选卷：固定来源接收

- 日期：2026-11-03；按 `docs/OCR_WORKFLOW.md` 执行。
- 固定 source：`src-ab0f2729ee4a24495e653b44c14438b4130f8b38b11362bf84251f3595a09d27`。
- 上游：`https://github.com/deekur/gaokaomath`，固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`，路径 `普通高考/2006/2006福建理.pdf`。
- 现场 SHA-256：`50d17546b94af82fb2cee653942752914cd387fe72792d74ffa5f75e7a301d83`；`git hash-object`：`b05111b956dc556d6905036d1d5d0da3d9a9e5b3`；527850 bytes，均匹配 manifest。

## 原件检查

PDF 两页 A3 横向，印刷页288–289，题签为“2006 普通高等学校招生考试（福建卷理）”。本机110 DPI两页均已目视检查，文字层可提取。统一入口的批处理验收已核对该 PDF 的两页采用原生文字候选而未 OCR；不因模型部署完成而重复识别。

共22题：选择Q1–Q12、填空Q13–Q16、解答Q17–Q22。第1页包含Q1–Q19，第2页包含Q20–Q22。题图共三处：Q16逐次连接中点的三角形，Q18四面体，Q20椭圆及割线/垂直平分线；后续按源图矢量重绘。Q7平行符号、Q22指数与乘积式在文字层丢失或压平，转录时必须按原图复核。

固定 PDF 仅见题面，没有答案、解析或评分标准；发布者、出版者、版次、重排/来源链和官方身份未认证。source 为 ready 且未绑定 paper/track，不能把 ready 当来源身份认证。未发现当前分支已有福建理科题稿；已完成的福建文科为另一份卷。

## 本阶段状态

仅完成来源固定、题签、页序、题型与图位清点，不表示题面转录或卷级验收。没有修改 manifest、issues、规范题稿、答案、provenance、TeX 或正式回执。`source_manifest.py validate --manifest source-manifest.json`、`issues.py validate --file missing-issues.md` 退出0。缓存原件、文字与页图位于 ignored `.work/ocr-local/sources/`。

下一步按原图分段转录Q1–Q22，主会话逐题核校后独立提交；再进行独立复核、答案推导、图稿与登记构建。没有新OCR或付费API调用，实际Agent token/费用未提供，记未知。

# 2002 北京理科候选卷：固定来源接收

- 日期：2026-11-03；按 [`docs/OCR_WORKFLOW.md`](../docs/OCR_WORKFLOW.md) 执行。
- 固定 source：`src-6b6e5d61614e04d9b61330de2c085ab84c2f6fddfca9e6f357695a7ba074e690`，当前 manifest 状态为 `ready`，`paper_id=null`、`paper_relation=null`。
- 上游：`https://github.com/deekur/gaokaomath`，固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`，路径 `普通高考/2002/2002北京理.pdf`。本地来源仓库 HEAD 即该 commit，工作区干净。
- PDF SHA-256：`4e19a0d37e74a41655156769e6cb72c2532ec2939cb6fe4d7b18db205123de73`；`git hash-object`：`e6b19791b1fe3ca2e49404428b746bb36c460f12`；620623 bytes，均与 manifest 一致。工作副本和页面渲染位于忽略目录 `.work/ocr-local/sources/`。

## 原件检查

PDF 共两页 A3 横向，印刷页100–101，题签显示“2002 普通高等学校招生考试（北京卷理）”。原件题面覆盖Q1–Q22：选择题Q1–Q12、填空题Q13–Q16、解答题Q17–Q22；第一页含Q1–Q19，第二页含Q20–Q22。图位为Q11函数图、Q12四个函数图和Q18多面体图；Q20含运算表。PDF没有答案、解析或评分页。当前 manifest 已登记2002北京文科 paper，理科 source 尚未绑定；文理是不同卷别。

`analyze_pdf.py --no-cache --include-text` 将两页均判为 `text_candidate`，非空白字符数分别为2002和687，`suspicious_chars=0`，图像对象均为0；本次 `model_calls=0`、`ocr_calls=0`。主会话目视检查两页150 DPI渲染图，并对关键疑点做300 DPI局部复看。文字层只作为转录候选，公式、字形、题图和标点仍以固定原页为准。

发现以下源文疑点，转录时按原页照录并保留复核记录，不做静默修正：

1. Q5 印作“长度单位不便变”，措辞疑似源文误字；尚无可追溯勘误。
2. Q15 第③项和第④项均印作“可能是直角”，原页确有重复，尚无可追溯勘误。
3. Q16 圆方程印作 $x^2+y^2-2x-2y+8=0$。配方为 $(x-1)^2+(y-1)^2=-6$，无实点，题设所称两条切线因此无从定义。转录应保留原式，答案保持待核；后续登记 paper 时为该题建立阻断 issue，除非找到可绑定的同版勘误或更强来源证据。

发布者、出版者、版次、扫描/复制链和官方身份均未认证；不得把 manifest 的 `ready` 状态当成来源认证。候选 PDF 没有答案页，因此任何后续答案须标作独立推导而非官方答案，`official_answer` 应保持 `null`。

## 本阶段状态

仅完成来源固定、原页题签/页序/题量/题图清点及源文疑点登记；没有修改 manifest 或 issue ledger，没有登记 paper/batch，没有写规范题面/答案/解析，也没有调用 OCR。OCR 推理与付费 API 调用均为0；子代理费用不可见，记未知。

下一阶段按固定原页分段转录Q1–Q22，主会话逐题核校，特别保留Q5/Q15字面和Q16无实圆疑点；随后独立复核，并在事务登记阶段建立Q16 blocker。本阶段不表示题面转录、官方来源认证、整卷验收或1952–2026语料完成。

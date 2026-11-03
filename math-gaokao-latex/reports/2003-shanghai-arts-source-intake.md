# 2003 上海普通卷文科：固定来源接收与题面转录

## 固定来源与身份边界

- 固定 `source_id`：`src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4`。
- 固定上游路径：`gaokaomath-src/普通高考/2003/2003上海文.pdf`。
- 来源 checkout：`gaokaomath-src`，HEAD `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。
- 现场 SHA-256：`ffd59c395a0c675118f6da576e48842549c4afa031d923448f26f33087bc7e85`，与 manifest 候选相符。
- Git blob：`19a5b96cd5d9aa9a9a2d74021cd47067e531f51b`。
- 文件大小：592,288 bytes；PDF 页数：2；A3 横向，印刷页码 140–141。
- 题签为“2003 普通高等学校招生考试（上海卷文）”。候选为 `ready/unbound`，尚无该普通卷规范稿、已登记项目、provenance、接收前报告或 batch。身份未认证：发布者、版次、原件/扫描链与官方身份均未核实；不得从题签、manifest `ready` 或本次转录推断已认证。
- PDF Catalog 含 AcroForm，字段数组为空（`qpdf --show-object=73`）；未发现表单字段内容。没有使用表单字段作为题面依据。

## 页签、页题结构与图位

两页均为题面，没有答案、解析或评分页。原页结构如下：

| 原页 | 印刷页码 | 题目 | 分布与原页图位 |
|---|---:|---|---|
| PDF 第 1 页 | 140 | Q1–Q19 | 一、填空题 Q1–Q12；二、选择题 Q13–Q16；三、解答题 Q17–Q19。图位：Q16 函数图、Q18 平行六面体示意图。 |
| PDF 第 2 页 | 141 | Q20–Q22 | 解答题续。图位：Q20 半椭圆隧道截面图。 |

完成草稿：`2003/2003_数学真题_上海文_题面转录草稿.md`，共 Q1–Q22，按原页题序转录，没有答案、分值或外加条件。

## 文字层路由与原图目视核对

- `analyze_pdf.py --no-cache --include-text`：整份文档 `text_layer_candidate`；PDF 第 1 页 `text_candidate`、1,448 个非空白字符、0 个可疑字符；第 2 页 `text_candidate`、553 个非空白字符、0 个可疑字符。`pdfimages -list` 未列出图像对象；题图由 PDF 绘图内容构成。文字层用于定位题号和行序，不作为题面验收结论。
- 按 150 DPI 渲染两页完整预览，并以 300 DPI 渲染、复查 PDF 第 1–2 页；目视检查了完整页、题目密集区及第 13–14 题选项。已逐题将 Q1–Q22 与原页核对；Q16/Q18/Q20 的图位、题签、题号边界和印刷页码均与草稿对应。
- 预览与提取材料仅在忽略目录 `.work/phase4-b47/shanghai-arts/`：`page-1.png`、`page-2.png`（150 DPI），`detail-1.png`、`detail-2.png`（300 DPI），以及 `text-layout.txt`、`analyze_pdf.json`、`image-objects.txt` 和临时局部检查图；不属于交付源文件。
- 文字层路由异常：`pdftotext -layout` 和 `analyze_pdf` 在 Q20 将原图可见的“最小”重复为“最最小”；300 DPI 页图可见为“最小”，草稿按原图转为“最小”。同一文字层还将 Q21 向量箭头抽成分离符号，将 Q14 的平行符号抽取丢失/错位；这些是文字层还原缺陷，不据此改动可见原文。
- 可见原图题面疑点：目前没有确认的印刷错字或数学条件冲突。Q8 的“前 n 项和总小于这个数列的各项和”等原文表达按原样保留，不作语义修补。数学正确性和答案均未审查。

## 调用、核验命令与结果

- PDF 身份与结构：`sha256sum <PDF>` 得到目标 SHA；`wc -c <PDF>` 得到 592288；`pdfinfo <PDF>` 得到 2 页、A3、AcroForm；`git -C gaokaomath-src rev-parse HEAD` 得到指定来源 commit；`git ... rev-parse 'HEAD:普通高考/2003/2003上海文.pdf'` 得到上述 blob。
- 文字层与图像路由：`python3 math-gaokao-latex/tools/analyze_pdf.py --no-cache --include-text <PDF>` 成功；`pdftotext -layout <PDF> .work/phase4-b47/shanghai-arts/text-layout.txt` 成功；`pdfimages -list <PDF>` 仅输出列头，未列出图像对象。
- 原图检查：`pdftoppm -png -r 150 <PDF> .work/phase4-b47/shanghai-arts/page` 与 `pdftoppm -f 1 -l 2 -png -r 300 <PDF> .work/phase4-b47/shanghai-arts/detail` 成功，随后直接查看两整页及检查图。
- 表单核对：`qpdf --show-object=34 <PDF>` 显示 Catalog 的 `/AcroForm 73 0 R`；`qpdf --show-object=73 <PDF>` 显示 `/Fields []`。没有检查或使用任何隐藏答案字段。
- 本地分析流程记录 `model_calls=0`、`ocr_calls=0`；外部 API 调用 0。题面草稿由本会话中的转录代理依据原页完成，主会话已复看原图；未调用 OCR 服务，也未凭模型记忆补题。

## 阶段边界与待做

完成的是固定候选的文件身份复核、两页结构/文字层路由分析、原页目视核对及 Q1–Q22 题面转录草稿。仍待：独立题面复核；来源身份和发布链核查；如要登记项目须由主代理单独处理身份绑定与共享 manifest/issue 变更；答案、解析、图形矢量稿及任何构建/验收均未开始。本报告不表示来源认证、正式规范题稿完成、答案验证、整卷验收或长期语料库完成。

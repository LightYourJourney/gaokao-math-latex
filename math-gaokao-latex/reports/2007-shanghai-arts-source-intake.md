# 2007 上海文科候选卷：固定来源接收

- 日期：2026-11-03；按 [`docs/OCR_WORKFLOW.md`](../docs/OCR_WORKFLOW.md) 执行。
- 固定 source：`src-51aa9840dc7a866be37ded966d4a337c999cacd912ce0118e07b3e6c768c5789`；manifest revision 6047，状态 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`。
- 上游仓库 `gaokaomath-src`，固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场 HEAD 与固定 commit 一致；源仓库工作树干净。

## 来源指纹

| 项目 | 结果 |
| --- | --- |
| 上游路径 | `普通高考/2007/2007上海文.pdf` |
| manifest SHA-256 | `1d43489e28ce9c305faa753519800b9184e40cc40fbd8343f7fd287b4ec70212` |
| 现场 SHA-256 | `1d43489e28ce9c305faa753519800b9184e40cc40fbd8343f7fd287b4ec70212` |
| manifest Git blob | `3d32cf193380f6a892827ef7f9931942839d9ad2` |
| 固定 commit 路径 blob | `3d32cf193380f6a892827ef7f9931942839d9ad2` |
| 字节数 / PDF 页数 | 507465 bytes / 2 页 |
| 页面尺寸 | A3 横向，1190.55 × 841.89 pt |
| PDF 检查 | manifest `pdf_check=passed`；现场 `pdfinfo` 成功 |

本机副本位于 `.work/ocr-local/sources/2007-shanghai-arts.pdf`，现场 SHA 与固定来源一致。原件没有写入 Git。

## 原页内容检查与路由

两页均按 220 DPI 渲染并目视检查。PDF 页码与原件印刷页码分别为1/407、2/408。原页题签为“2007 普通高等学校招生考试（上海卷文）”。题量为21题：填空Q1–Q11、选择Q12–Q15、解答Q16–Q21。可见题图位于Q7、Q11、Q16、Q21；没有答案、解析或评分页。

`analyze_pdf.py --no-cache --include-text` 的页级结果：

| PDF 页 | 印刷页 | 分类 | 非空白字符 | 可疑字符 | 图像对象 | 证据 |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| 1 | 407 | `review` | 1566 | 5 | 0 | `text_layer` |
| 2 | 408 | `text_candidate` | 722 | 0 | 0 | `text_layer` |

文档分类为 `mixed_candidates`。页1文字层中包含需要按原图判读的数学符号；实际转录须以页面为准，不能直接采用提取文本。经原页检查，现阶段以人工核校为主，未调用模型：`model_calls=0`、`ocr_calls=0`。原始 PDF、分析 JSON、文字提取和 PNG 渲染均保存在忽略目录 `.work/ocr-local/`。

## 未核实边界与下一阶段

manifest 仍保持 source `ready` 且未绑定 paper；本阶段没有修改 `source-manifest.json`、`missing-issues.md` 或规范题稿，也没有登记 paper/batch。固定来源字节和卷内题签已核对，但发布者、出版者、版次、复制/扫描来源链及官方身份未认证。由于原 PDF 只有题面，答案及解析仍需独立推导并标注非官方，不能从模型记忆补写。

下一阶段：依据固定 PDF 转录Q1–Q21，逐题核对题号、符号、选项和分节；随后由独立复核者对照原页复核。OCR 候选不替代原页校对。本阶段不表示题面转录完成、来源认证或卷级验收；成本数据未知。

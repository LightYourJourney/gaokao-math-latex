# 2006 广东候选卷：固定来源接收

日期：2026-11-02

## 固定副本

- Manifest source ID：`src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24`；任务提供的状态为未关联 paper/batch。
- 固定路径：`普通高考/2006/2006广东.pdf`；SHA-256 `46542e3594530e351f1f9812d0543cc5cd3c223ee9275d98bdc1dd802d3242aa`。现场重算值与任务提供的 manifest 指纹一致。
- `pdfinfo` 确认 2 页，页面尺寸 1190.55 × 841.89 pt（A3 横向），PDF 1.6，文件大小 511,973 bytes。
- 使用 Poppler `pdftoppm -png -r 120` 渲染两页并逐页目视核对；另对第 1 页以 300 dpi 渲染供公式细节检查。`pdftotext -layout` 只用于定位和交叉检查，不作为视觉核对的替代。

## 原页可见信息

- PDF 第 1 页题签可见为“2006 普通高等学校招生考试（广东卷）”；印刷页码为 292、293。
- 共 20 题：选择题 Q1–Q10、填空题 Q11–Q14、解答题 Q15–Q20。PDF 第 1 页含 Q1–Q17；第 2 页含 Q18–Q20。题面没有印出单题分值，也未见卷面总分或评分办法。
- 可见题图/表：Q4 三角形及中点向量图；Q7 反函数曲线坐标图；Q14 乒乓球三角堆示意；Q16 概率分布表；Q17 两圆平面及空间连线图。Q7 曲线的辅助标记、Q17 关系图及其虚实线需在后续重绘时继续对照固定页；本阶段不生成图稿。
- PDF 可见范围只有题面、选择项、填答空位及解答题，未见答案、解析、评分标准或总分说明。

## 身份与阶段边界

页面题签支持把固定副本作为“2006 广东卷”候选题面处理；这只陈述本地文件上可见的自称，不构成考试机构、发布者、出版者、版次、扫描来源链或官方身份认证。Manifest source ID 与 SHA-256 仅用于固定本次工作输入字节；任务提供的未关联 paper/batch 状态未由本阶段变更。

本阶段仅完成固定文件指纹、页数与可见结构 intake，并形成题面转录稿。未改 manifest、README、PROGRESS、missing-issues、公共工具或其他卷文件；未登记 paper/batch，未录答案、解析、评分或逐题 provenance，未绘图、未构建或生成 PDF。所有不能由页面辨明或页面内部不一致的地方留待核查，不按模型记忆补文。

## 验证命令

```sh
sha256sum gaokaomath-src/普通高考/2006/2006广东.pdf
pdfinfo gaokaomath-src/普通高考/2006/2006广东.pdf | rg 'Pages|Page size|File size|PDF version'
pdftotext -layout gaokaomath-src/普通高考/2006/2006广东.pdf /tmp/2006-guangdong-layout.txt
pdftoppm -png -r 120 gaokaomath-src/普通高考/2006/2006广东.pdf /tmp/2006-guangdong-p
```

后续阶段应先复核规范题面及图稿；Q6 题干对象文字、Q20（1）区间/定义域疑点应在任何答案推导之前维持待核状态。此记录不表示本卷处理完成，更不表示 1952–2026 语料库完成。

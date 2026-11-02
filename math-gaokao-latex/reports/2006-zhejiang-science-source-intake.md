# 2006 浙江卷理：固定源页 intake

日期：2026-11-02

阶段：候选固定来源 intake 与可见题签/页数核验；未登记 paper 或 batch。

## 固定副本核验

- 固定只读文件：`gaokaomath-src/普通高考/2006/2006浙江理.pdf`。
- Source ID：`src-5f9ed6381f35350f76a93adb34b280d596a9d44d2b40366565ac3df18645ab6a`；manifest 中该记录的 `paper_id` 为 `null`，登记文件名为 `2006浙江理.pdf`。
- SHA-256 实测为 `adb6fd06af66efb8cd957004efc3e4278a4df5cb87d4f5e79ad215e548c11cb8`，与任务指定摘要一致；文件大小 547011 bytes，PDF 共 2 页，页面尺寸 1190.55 × 841.89 pt（A3 横向），未加密。
- 两页均以 120 dpi 渲染并逐页目视；对正文公式、小字和图旁标记再以 240 dpi 全页渲染复核。PDF 第 1 页印刷页码 340，含 Q1–Q17；第 2 页印刷页码 341，含 Q18–Q20。
- 首页可见题签为“2006 普通高等学校招生考试（浙江卷理）”。Source ID 与 SHA-256 只绑定本次固定文件字节；题签只支持对页内可见文字的描述。三者均不能认证发布者、版次、来源链或官方原件身份。
- 固定副本没有答案、解析、逐题分值或总分信息；本阶段未推定这些内容。

## 转录范围与图位

- 题面转录文件：`2006/2006_数学真题_浙江理_试题.md`。
- 按源页标题分为选择题 Q1–Q10（10 题）、填空题 Q11–Q14（4 题）、解答题 Q15–Q20（6 题），共 20 题。
- 图位：Q9 球面及大圆弧；Q14 正四面体投影；Q15 函数图象；Q17 四棱锥；Q19 椭圆和直线；Q20 函数曲线、割线及切线。此阶段只在题面用文字占位标记，不重绘图。
- 页面文本抽取仅用于定位和辅助核字；转录以固定 PDF 页面视觉内容为准。未采用答案记忆、其他卷题面或未追溯网页补文。

## 验证命令

```sh
sha256sum gaokaomath-src/普通高考/2006/2006浙江理.pdf
pdfinfo gaokaomath-src/普通高考/2006/2006浙江理.pdf
pdftotext -layout gaokaomath-src/普通高考/2006/2006浙江理.pdf -
pdftoppm -png -r 120 gaokaomath-src/普通高考/2006/2006浙江理.pdf /tmp/gaokao-2006-zhejiang-science-review/page
pdftoppm -png -r 240 -f 1 -l 2 gaokaomath-src/普通高考/2006/2006浙江理.pdf /tmp/gaokao-2006-zhejiang-science-review/high
```

本阶段只新增本报告、题面转录稿及其题面文件；未修改 manifest、README、PROGRESS、missing-issues、公共工具、测试或其他卷文件。未联网认证来源链。

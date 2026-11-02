# 2006 福建文科候选卷：固定来源接收

- 日期：2026-11-02。
- 固定候选 source：`src-88a71372c96b05a58058a4446824a5aa14004ffa91901212088621a6b41d0346`。
- 上游只读 PDF：`gaokaomath-src/普通高考/2006/2006福建文.pdf`。
- 文件 SHA-256：`8984913f8b9b4927361dc042f0d78b4ff9fe6b4b9b7b898d7184c1f4cea05432`；Git blob：`c2b67b68498ac92eb9d864180678ca19725d42e8`；大小 509527 bytes。
- 来源 checkout HEAD：`34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。

## 原件清点

- PDF 为 2 页 A3 横向；印刷页码为 290–291。首页题签显示“2006 普通高等学校招生考试（福建卷文）”。
- 固定页图目视清点为 22 题：第 1 页（印刷页 290）含 Q1–Q19，其中选择 Q1–Q12、填空 Q13–Q16、解答 Q17–Q19；第 2 页（印刷页 291）含解答 Q20–Q22。
- Q19 为四面体图，Q20 为椭圆与直线示意图。两图均需按原件语义重绘为矢量图，不以扫描像素比例推导题设数值。
- 固定 PDF 仅含题面；未见答案、解析或评分标准。发布者、出版者、版次、来源链与官方身份均未核实。

## 状态与下一步

- Manifest 当前把 source 记为 `ready`，但尚未关联 paper，`paper_id=null`、`track=null`。此处“固定候选”仅表示仓库内固定字节输入，不等于认证来源。
- 本 intake 阶段只完成题签、页数、题号范围、题型和图位清点。Q1–Q22 转录及主会话逐题核校见 `reports/2006-fujian-arts-question-transcription.md`；答案/解析独立推导与 paper/batch 登记见 `reports/2006-fujian-arts-independent-solutions.md`。逐题 provenance、图稿、项目 TeX、四版构建与视觉验收仍待后续阶段。
- 本阶段未创建规范题面或答案，不改 manifest、issues、provenance、TeX 或构建回执；未运行测试。耗时和 token 成本未知。本报告不表示题面转录完成、来源认证、卷级验收或长期语料库完成。

# 2015 福建理科候选卷：固定来源接收与 OCR 路由

- 日期：2026-11-03；工作树 `仓库根`，工作分支；source manifest revision **6074**。
- 固定 source `src-c47985c709ff8ae42e6e192879d604223c58a53c4358056d28f78ad5a9736e3c`，路径 `普通高考/2015/2015福建理.pdf`。manifest 状态为 `ready`、`paper_id=null`、`paper_relation=null`、`track=null`，尚无 paper、batch 或 blocker。
- 上游登记指向 `deekur/gaokaomath` commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场固定 PDF SHA-256 `a33455d27abdf2c4b344a5b90395bd71269f6fbefdef350375aba074e47ef700`，Git blob `421cface308a5e99649ed8c316ae0b82322e0a9c`，大小 517,192 bytes，2 页；与 manifest 完全一致。来源库 `HEAD` 的同路径 blob 也相同。文件名及页内题签相符，仍不能据此认证发布者、版次、复制链或官方身份。
- 原 PDF 及 200 dpi 页图保存在忽略目录 `.work/ocr-local/`。固定副本为 `.work/ocr-local/sources/2015-fujian-science.pdf`，哈希与上游 PDF 相同；页图 SHA-256：p.1 `50137b90063254632d3bec2b12cd1fccaecb66dff901190d04721eb7c283b6bf`，p.2 `402f17e4266240a61b2ee36e83881746a9ccc1301fdea3447da15e6587645464`。

## 原页核查

- PDF 为 2 页 A3 横向，印刷页 943–944；题签为“2015 普通高等学校招生考试（福建卷理）”。共 23 题：选择 Q1–Q10、填空 Q11–Q15、解答 Q16–Q23。题面含 Q4 数据表、Q6 程序框图、Q13 函数图、Q17 空间示意图和 Q18 椭圆示意图。未见答案、解析或评分页。
- `analyze_pdf.py --no-cache --include-text`：文档分类 `mixed_candidates`。p.1 为 `review`（1,806 个非空白字符、14 个可疑字符），p.2 为 `text_candidate`（775 个非空白字符、0 个可疑字符）；两页都有文字层、没有图像对象。该文字层的跨栏顺序交错，不作为规范题稿。两页 200 dpi 原页图已逐页目视检查。
- p.1 按人工路由规则明确选页，用本地 OCR 交叉产出独立页级候选：统一运行文件 `.work/ocr-local/runs/2015-fujian-science-page1-crosscheck.json`，SHA-256 `c1e6e33d5120a40bd5c3f1a4d43bc8f9242807eabe3306791aff19b5e88db5ce`。模型输出绑定上述 source ID、PDF SHA、p.1、180 dpi 图像 SHA `c12aace14d206c81e39594cdc9ac8a1e9d083f17ff0c46c231b754be0a1dc84c`，均为 `question_id=null` / `unassigned-page-level` / `recognized_unverified` / `needs-review`，不能直接导入题稿。
  - Xiaomi-OCR-0 revision `bbd8cf8d21f256b3644b44cb860f3a7cecb93c30`，模型树 SHA-256 `a56facd25f7bfcc85db843f7dfca353ff3f0c4095974b7638f9ea23f97058210`；本次 1 次模型调用，MPS，worker 97.137 秒，2,107 tokens，接口报告未截断。输出 SHA-256 `71e7b8100e8767cb48a6c399fafe6b80b3d0e83caa57438a35df721357a224a0`。
  - PaddleOCR-VL-1.6 revision `c5630abae1d940eafe0697512a0325494b02ab42`，模型树 SHA-256 `8060c2c8c26bfdb9e84105951390c5792bdf2208b70749479d3bb9fd30ff6c5e`；本次 1 次模型调用，CPU，worker 258.610 秒。该接口没有暴露停止/截断原因，故截断状态为未知；输出 SHA-256 `c5209e92f59b3ecb3f41d5631f50bf6a76be30bf2b9a2637b8ede7d70e05173a`。
- 两引擎输出字节不一致。核对可见 Q9 中 Xiaomi 候选把 `|AB|=1/t` 识为 `1/l`，Paddle 候选读作 `1/t`；固定原页放大确认是 `1/t`。此处以原页裁定，其余候选仍待人工逐题核对；模型差异不通过投票消解。没有调用外部 OCR/API。

## 本阶段边界与下一步

- 本阶段只完成固定来源指纹、页数/题签/题量/题图位置、文字层分析、页图检查和 p.1 双引擎 OCR 候选。未登记 paper/batch，未修改 `source-manifest.json` 或 issue ledger，未转录题面、求解答案或创建图稿。
- 发布者、出版者、版次、复制链和官方身份均未核；PDF 无答案页，`official_answer` 仍未知。人工耗时和子代理 token/成本数据不可见；本地 OCR worker 时间合计 355.747 秒。
- 下一阶段从固定原页转录 Q1–Q23，并逐题独立对照原图；图表、指数/下标、正负号和 Q9 公式需明确核对。随后另做未读答案的题面复核。本回执不表示题面转录完成、答案验证、来源认证、整卷验收或 1952–2026 语料库完成。

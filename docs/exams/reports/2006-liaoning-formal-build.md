# 2006 辽宁文理四版正式构建（phase1-b78）

## 题面修正

文科卷首轮正式构建暴露缺字 U+3001（顿号）。定位到 Q19、Q22 的题面把中文顿号放在数学模式内部；保持原文字词与符号不变，只把标点移到数学模式外。重新生成规范含解析稿、题目 TeX 与答案 TeX，并重绑文科 Q19、Q22 的题面哈希；没有修改答案或推导。随后确定性生成检查及 provenance 检查通过。

## 正式构建

- 构建输入 manifest revision：5993；构建结果事务后 revision：5994。
- 文科 attempt：`44453959-c03c-402c-bb83-d37dde0b062f`。
- 理科 attempt：`b866e00c-224e-47c1-a8a7-1a7babec1df9`。
- 两卷各四版均 `succeeded`，构建日志 `errors`、`missing_characters`、`overfull`、`undefined_references` 均为空；无 problems。
- 共 91 页：

| 卷别 | 试题版 | 解析版 | 简答版 | 印刷版 | PDF SHA-256（依次对应四版） |
|---|---:|---:|---:|---:|---|
| 文科 | 6 | 20 | 8 | 16 | `c54df9b3ccc005adc9cf66d124e96d02655d359718318d5117a279e1cb702043` · `1f578deadf6b70f6d64087759ef7ffcaa7119290189d5d16b63969de0b43eace` · `39c58270253aefcc384fc5696aa4b30e53cadac32ece09003b9727a618fd7116` · `f831d34c148aead5ef25f1d0664c2c443f106e1632f921a2f07ba0ebc6113a66` |
| 理科 | 4 | 18 | 6 | 13 | `e9c7d82f6674e73fabfb70493f569bd94690dd950a18b899044b6078d544ce27` · `b427ed97563f757a5ac3e4a2dc6a62720ea8bf14816e394b2f1ba8c2323a0555` · `a41aa8c495a66988b91a8da13c53cd0e4b18df33b454e2b897733b38ebb7fadd` · `babcfcdb98c1b2c3dddfc80009d222f4866420c1c85e101580686fff296cea25` |

- `build_projects.py validate-receipts --manifest source-manifest.json --batch phase1-b78 --require-current-inputs --json`：`OK`，2 pending，0 stale/invalid/missing。
- PDF 页面渲染和逐页视觉审查在下一阶段处理；当前 build 状态仍为 `compiled_pending_review`。

## 来源边界

固定 PDF 仅作为题面候选来源，发布者、出版者、版次、扫描/重排来源链和官方身份仍未核实，`official_answer=null`。文科 Q21(2) 原页写“四边形 APCD”且 P 未定义，仍保留 `U/PENDING` 并由 `ISSUE-1340` 阻断；未猜改原文。此阶段不代表本批次验收或长期语料库完成。

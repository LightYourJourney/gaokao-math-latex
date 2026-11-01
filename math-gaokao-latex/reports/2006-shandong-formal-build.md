# 2006 山东文理候选卷：正式四版构建

日期：2026-11-02；批次：`phase1-b68`；工具链：TeX Live 2026 / XeTeX 3.141592653-2.6-0.999998 / latexmk 4.88 / Poppler 26.10.0。

输入 manifest revision：`5789`。完成写回后 revision：`5790`。两个正式 build receipt 均为 `compiled_pending_review`，无前序 attempt。

| 试卷 | Attempt ID | 试题版 | 解析版 | 简答版 | 印刷版 |
|---|---|---|---|---|---|
| 山东文 | `9dde3ace-2511-417f-bb68-e936959ef013` | 5页 · SHA-256 `80571881138271d9ef27747cf6cbe82acdeccec9dd24e55a26e739b8ce841eaf` | 19页 · `a10b0bc581d7bb9e7d2b15acdfa1ab907785ebad4f86362e5a0c1aa5c9247504` | 7页 · `2d072ab2f534e9d9c5de20b6499a2669e3e3e4300665f15d7c40748fd62b41d7` | 14页 · `cdfe7cde3b7a4f9bdbdbdecc26fce3b6153ac811195d5984fba2bd19d6ba2c17` |
| 山东理 | `8a4d85d5-9003-4979-a2b2-f0a100159b2b` | 5页 · `79c9bc26822f4115d8c9b53d195bda8b10f1339225d817c03c2ec00ac862fda0` | 20页 · `10a00fce21de92a7fe4029a8bd84cb882b8988a26bf85209a931faed7e62e3e1` | 7页 · `03eaaa4a0dcc34512cd1fb2d7e6c6109b3412d8c0c639b7a153c4548087c076d` | 16页 · `6c6f5871764de7f7fa817ff3e808d837910b19c9fa2577bea17719b0f8d55c05` |

合计 93 页。八个 edition 均 `succeeded`，没有 TeX errors、missing characters 或 undefined references。文科无 Overfull/Underfull；理科解析版有一项 `Overfull \\hbox (25.69281pt too wide)`，TeX line 333；印刷版有一项 `Underfull \\hbox (badness 1009)`，TeX lines 141–142。后两条在逐页视觉复核前保留为当前回执告警，不先行静默消除。

`build_projects.py validate-receipts --manifest source-manifest.json --batch phase1-b68 --json` 返回 `code=OK`、`failed=0`、`invalid=0`、`missing=0`、`stale=0`；两卷各待视觉复核。回执完整列出四版页数、PDF SHA-256、输入树、工具链与日志诊断。

本阶段未创建 review receipt、未逐页审阅 93 页，也未 finalize 批次。山东理科仍有 Q5/Q10 U blocker，固定候选来源身份与官方答案仍未核。本报告不表示任一卷闭环或长期语料完成。

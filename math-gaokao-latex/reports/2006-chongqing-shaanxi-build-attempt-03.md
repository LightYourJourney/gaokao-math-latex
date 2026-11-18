# 2006 重庆、陕西文理候选卷：第三次四版正式构建

- 日期：2026-11-03；批次 phase1-b80；承接答案数学排版修正提交 aa83abf。
- 命令：tools/build_projects.py build --manifest source-manifest.json --issues missing-issues.md --formal --batch phase1-b80 --json。
- 四个 attempt receipts 的 manifest revision 均为6012；构建事务后 source manifest 为6013。最终 JSON 返回 COMPILED_PENDING_REVIEW，failed=0，pending=4。四卷每版均为 succeeded，且每版错误、缺字、overfull、未定义引用计数全部为0。

| 试卷 | attempt ID | 版次 | 页数 | PDF SHA-256 |
|---|---|---|---:|---|
| 重庆文科 | bc6e981b-b833-4653-9b89-8cdc6700c072 | 试题版 | 4 | 1ed268869e7684e60e647014223f3c0295333d58830b95d64417e3026e9231bc |
| 重庆文科 | bc6e981b-b833-4653-9b89-8cdc6700c072 | 解析版 | 20 | b7b1c5c56475b8c7721906819133ffcdc4853e7df39a47ca26f203d8b5e87a73 |
| 重庆文科 | bc6e981b-b833-4653-9b89-8cdc6700c072 | 简答版 | 6 | 7f2eb010a49c7e69e1d70b131b127a1dff154abc89cb1812ac67c46c4a4b46c9 |
| 重庆文科 | bc6e981b-b833-4653-9b89-8cdc6700c072 | 印刷版 | 14 | de3f041a03c4e3c9ae3bbd7840479556c336a2e494ced47374d6300de8512c4a |
| 重庆理科 | a1f97589-8839-4b94-8c35-59d4e2a15aaa | 试题版 | 5 | 54f5c9db16f1eae39125eaccbcf354ba35b55084b29f77a67853be778ed006e2 |
| 重庆理科 | a1f97589-8839-4b94-8c35-59d4e2a15aaa | 解析版 | 20 | 96fac71b81ba2a6abd7a175b42a5ca02c8a359f4a4e72388efe0537ad5b524ce |
| 重庆理科 | a1f97589-8839-4b94-8c35-59d4e2a15aaa | 简答版 | 7 | 5a0c7f77a3fe8a56f28024bde9f04a66daee095023482bcb43fff4d5a0b138cb |
| 重庆理科 | a1f97589-8839-4b94-8c35-59d4e2a15aaa | 印刷版 | 15 | 5d190da7ef67e140e928f99f06b4dbcca4cac7196b283cc55dca0fc3e08ac16e |
| 陕西文科 | 358fb3ad-e343-498c-8cb9-92ed763948ab | 试题版 | 3 | 683d22e14d57d6cb0bbc0905dc8b418f6e61f98e4bf665d3897676f31f07f015 |
| 陕西文科 | 358fb3ad-e343-498c-8cb9-92ed763948ab | 解析版 | 17 | daa6096deb4ac958da28cf6720df98386413d08cf8f8e5e58cafae7a4d612be2 |
| 陕西文科 | 358fb3ad-e343-498c-8cb9-92ed763948ab | 简答版 | 5 | 677cfa27c5108df512556f768837097d9c33bfcfb544d6e8887152e8510d149c |
| 陕西文科 | 358fb3ad-e343-498c-8cb9-92ed763948ab | 印刷版 | 13 | 1549c77d5ec7fb9c8b25480aa7f81247322cf33dd8c502bf1a3a18a03f09fb7b |
| 陕西理科 | 1b167565-090e-4aa7-9f5b-968d2996076a | 试题版 | 4 | 7a7938c974f6401b55e35fea0a7d8da853d88f0c5919e0e40ddb29f33875e01f |
| 陕西理科 | 1b167565-090e-4aa7-9f5b-968d2996076a | 解析版 | 18 | 3a6c541fc8d76e501f23b7b24a948244e851626348c0e0e3bb527de3cb55f908 |
| 陕西理科 | 1b167565-090e-4aa7-9f5b-968d2996076a | 简答版 | 6 | 3ba2ed88701cac63ac44a4252b6fa3a018008af5c302674a7aafe6fe472e13e4 |
| 陕西理科 | 1b167565-090e-4aa7-9f5b-968d2996076a | 印刷版 | 12 | dd5d2cf79aee12183c522df33a83bb315398375abd7c1330a963e2cab0adeaab |

- `validate-receipts --manifest source-manifest.json --batch phase1-b80 --require-current-inputs --json` 返回 code OK，4卷均 current，stale=0、invalid=0、missing=0。source manifest 与 issue ledger 结构校验通过。
- ISSUE-1345—ISSUE-1354 已 resolved。ISSUE-1341—ISSUE-1344 仍为 blocks_completion；official_answer=null、来源身份未认证。未做视觉审查前，批次只处于 compiled_pending_review。
- 下一阶段逐页渲染并复核以上169页，build/review receipts 绑定本次 attempt、revision、输入树、工具链与 PDF SHA；不以更早 attempt 的视觉判断替代本次页面复核。

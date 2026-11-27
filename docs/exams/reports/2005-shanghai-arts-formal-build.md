# 2005 上海文科普通卷：四版正式构建

- 日期：2026-11-03。
- 批次/试卷：`phase4-b43` / `gk-2005-regular-shanghai-arts`。
- 构建 attempt：`e365d302-3044-43d4-88c8-5bd1d171bac1`；输入 manifest revision `6105`，构建事务后 revision `6106`。
- 构建时间：2026-11-03 18:23:38–18:23:51 +08:00；工具链：TeX Live 2026、XeTeX 3.141592653-2.6-0.999998、Latexmk 4.88、Poppler 26.10.0。

## 构建结果

| 版本 | 结果 | 页数 | PDF SHA-256 |
|---|---|---:|---|
| 试题版 | succeeded | 4 | `6be8f4ce65b99f0f7cfcac7cdac5415a21c3e933fdbcd9101a1979221f0d017d` |
| 解析版 | succeeded | 19 | `967116527b043a0668261353a63c1c75021d406f0b814f7bd51bcd4fb68e4f45` |
| 简答版 | succeeded | 6 | `d6ab10d674cedeb9b08c026a2e3e0058cdf37415a9896eef9287a8ce187f1b6b` |
| 印刷版 | succeeded | 15 | `56947899a67f75cd5afdbd85d9efb5ae70a922ec92072dd123808a695af9052c` |

- 四版均一次编译通过，TeX 日志中的 errors、missing characters、overfull 与 undefined references 均为0。独立 `pdfinfo` 核对页数与回执一致，逐文件 SHA-256 及字节数也与回执一致。
- `build_projects.py validate-receipts --manifest source-manifest.json --batch phase4-b43 --require-current-inputs --json` 返回 `OK`：invalid、missing、stale、failed 均为0；当前状态仍为 `compiled_pending_review`。
- `manifest.csv` 写入检查显示775行且无需改动。全量报告 `render --all` 已写入并回读六个投影目标；随后 `report.py check --all` 通过，`manifest_csv.py --check` 确认当前且775行。全库投影统计412套试卷、260批次；正式复核门禁为216个 `FINALIZED`、43个 `INVALID_OR_STALE`、1个 `VISUAL_FAILED`。这次只刷新事实投影，没有批量修复其他批次状态。

## 阶段边界

本阶段完成四版正式构建及回执有效性、PDF 指纹和全量投影校验，没有进行逐页视觉验收，也没有运行全库测试。视觉复核须以该 build attempt 为输入，随后再决定批次是否关闭。Q12 的并列最小判定与 Q20(1) 原文“中低价层”的解释仍是 U/PENDING；paper 保持 `blocked`，不得据此称本卷无阻塞完成。来源出版者、版次、复制链与官方身份仍未认证，`official_answer=null`。本阶段只覆盖 `phase4-b43`，不代表长期语料完成。

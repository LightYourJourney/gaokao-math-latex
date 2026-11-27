# 2015 福建文科：四版视觉复核与批次收口

日期：2026-11-03

批次：`phase3-b24`；paper：`gk-2015-regular-fujian-arts`

## 复核范围

- 复核固定 build attempt `ab1a008e-7f4c-4c10-9e04-2dd3d06e2ae2` 的试题版、解析版、简答版和印刷版，共 53 页；全部页面以 120 dpi 渲染并逐页目视检查，覆盖题面、解析、答案速查、图表、页眉页脚、分页与留白。
- 四版候选锚点分别为：试题版第 4 页、解析版第 12 页、简答版第 4 页、印刷版第 16 页。锚点用于重点二次检查；本次仍完整检查了全部 53 页。
- 页级八项判据共 424 项：353 pass、71 not_applicable、0 fail、0 pending。not_applicable 仅用于无图表的图形标注项，以及答案版本的答案泄漏项。
- 图稿、表格、公式、字形与题号均清楚可读；页眉页脚和 PDF 页码连续，未见裁切、重叠、缺字、答案误入试题版或不当分页。未发现需返修的版面问题，未新增视觉 issue 或警告豁免。

## 批次结果与边界

- `finalize-batch-checked` 返回 `FINALIZED`，批次 `phase3-b24` 为 `closed`，manifest revision `6066`；paper 状态为 `complete`，review 为 `passed`，无阻塞问题。
- 四版 build receipt 与 review receipt 均绑定上述 attempt 和当前 PDF；`validate-receipts --require-final --require-current-inputs` 返回 OK，failed、invalid、missing、stale 均为 0。
- 固定来源仍是本库使用的候选 PDF：原件 2 页且无答案页；发布者、出版者、版次、复制链与官方身份未核实。未发现官方答案证据；逐题答案证据均为 D 级独立推导，不能标作官方答案。版面闭环不构成来源认证。
- 交付 PDF 为试题版 6 页、解析版 21 页、简答版 8 页、印刷版 18 页。本批只记录 2015 福建文科这一卷，不表示 1952–2026 语料整体完成。

## 收尾校验

- 通过：review `check-batch`、provenance `check-batch`（22 题）、source manifest 与 issues 校验、solution sources（22 题）、项目 TeX／简答／版本壳生成器 `--check`。
- 通过：build receipt currentness、775 行 `manifest.csv` currentness，以及全量报告 `render --all` 后的 `check --all`；全局投影将本批纳入闭合状态。
- 本阶段未调用 OCR，未运行测试套件。

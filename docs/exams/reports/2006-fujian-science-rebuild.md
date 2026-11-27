# 2006 福建理科候选卷：Q10 分页修订后正式重建

日期：2026-11-03
批次：`phase1-b77`
paper：`gk-2006-regular-fujian-science`
构建 attempt：`20ccbb69-b92e-4820-9276-929a9e02e4e7`
输入 manifest revision：`5980`；构建结果事务 revision：`5981`

## 构建结果

| 版本 | 结果 | 页数 | PDF SHA-256 |
|---|---:|---:|---|
| 试题版 | succeeded | 5 | `ee48b310ddeb57ce391f50d9a18ee16dc4eaaddbbde3756785a9f8fa354d3b69` |
| 解析版 | succeeded | 21 | `87dc90351a087971c4c54426d2f5c92d50c4c682a0cfa1c7e4dffc3af08fa5b6` |
| 简答版 | succeeded | 7 | `4e2613bb4908ad334a55601d7823a941c3def49b7c877f0e4e3a3811d431b52b` |
| 印刷版 | succeeded | 18 | `757f74ac30360f0856401e2448708fa8ce4c6e860454407d7f01933dda7176f8` |

共51页、四版构建日志均无 Overfull/Underfull 警告。正式 receipt 位于 `2006_福建卷_理科/receipts/build.json`。`build_projects.py validate-receipts --batch phase1-b77 --json` 返回 `OK`，1 pending、0 failed、0 invalid、0 missing、0 stale、无 problems。

## 视觉复核进度

四个新 PDF 均以 Poppler 110 dpi 重渲染。对照上一 attempt 逐页 PNG SHA-256，试题版5页与简答版7页完全相同；解析版21页中19页相同、印刷版18页中17页相同，共48页继承上一轮对应页面的实际目检结论。变化页为解析版第10、11页及印刷版第9页，均已重新打开检查：解析版第10页的 Q10 推导和答案框现在同页，第11页从 Q11 开始；印刷版第9页的 Q10 答案框仍与推导同页。

四版逐页工作项覆盖51页×8项：377 `pass`、31 个无图页 `figure_label=not_applicable`、0 `fail`、0 `pending`。此时工作项绑定本 attempt，正式 review receipt 尚未聚合；批次仍为 `compiled_pending_review`。变化页检查与 PNG 哈希对照保存在忽略目录 `.work/phase1-b77-rebuild/` 及 `.work/phase1-b77/review/`。

## 来源状态

本阶段只重建 PDF 并复核页面，没有重新 OCR 或推导答案，成本未知。固定 PDF 的发布者、出版者、版次、来源链和官方身份仍未认证，`official_answer=null`；本报告不是批次关闭或长期语料完成证明。

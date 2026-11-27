# 2000 上海春季卷：题面与附录页范围更正

日期：2026-10-28

## 核对结果

- 固定来源 `src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0`，SHA-256 `f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954`。本阶段复用忽略目录 `.work/ocr-cache/<sha>/rendered-195dpi/` 中既有的第1–5页渲染并目视核对，没有重新物化原 PDF。
- Q22 在 PDF 第4页开始，题干、图及小问续至第5页；第5页下半部已经出现“答案要点”附录。因此题面与附录页范围真实重叠：题面总范围 `[1,5]`，附录范围 `[5,9]`。不能把第5页整页都归为答案页。
- 逐题页映射供 provenance 阶段使用：Q1–Q7 → PDF 第1页；Q8 → 第1–2页；Q9–Q14 → 第2页；Q15 → 第2–3页；Q16–Q18 → 第3页；Q19 → 第3–4页；Q20–Q21 → 第4页；Q22 → 第4–5页。印刷页码依次为182–186。

## 更正记录

- 初次登记将 `index_metadata.pages_q` 设为 `[1,4]`，遗漏了 Q22 在第5页的续文；`pages_s=[5,9]` 不变。
- 项目没有修改既有页范围的专用 CLI。本次先经 schema、manifest 语义、来源语义和 paper 语义校验，以 `Transaction` state 事务把 `pages_q` 改为 `[1,5]`，revision `5290→5291`，transaction `c1a62ae9-bd2d-4473-8485-384c5cdaf5f8`；再以第二个 state 事务更正静态 index note，revision `5291→5292`，transaction `b686fa88-e859-47b6-b6fc-297605249632`。
- 随后 `generate_projects.py --paper gk-2000-spring-shanghai --write` 重算本卷 TeX 与共享 `index.json`，使兼容索引记录题面 `[1,5]`、附录 `[5,9]` 并明确页5重叠。题面 Markdown 来源 frontmatter 和原登记阶段报告已同步更正。

## 阶段边界

本阶段只修正来源页范围及其静态索引说明，不改变题面、答案、解析、source 身份或 `official_answer=null`。未导入逐题 provenance、未构建 PDF、未运行测试。下一步按上列逐题页映射准备 provenance，并继续保留固定扫描件出版者、版次、来源链及附录官方身份未核的状态。

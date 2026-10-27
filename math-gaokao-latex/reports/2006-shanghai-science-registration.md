# 2006 上海理科卷：paper/source 登记

日期：2026-10-27

## 登记结果

- 使用唯一事务 `source_manifest.py register-papers` 登记候选 paper `gk-2006-regular-shanghai-science`，批次 `phase1-b42`，manifest revision `5194 → 5195`。
- 目录键 `2006_上海卷_理科`，科类 `science`，题量 22；题面页映射为固定 PDF 第 1–2 页，答案/解析页映射为 `null`（扫描件没有答案页）。
- source `src-7f8706c4a44fd822ba2bb30b55a3f647f1fdf82d7805be1e62d4ee2030ebe4e6` 事务绑定为本卷当前 canonical 题面来源。此关系只界定语料中的来源绑定，不证明 PDF 是官方原件。
- `production_state=planned`；本事务未登记图形、逐题 provenance 或任何答案来源。

## 源稿与派生稿

- 三份规范 Markdown 均存在：`2006_数学真题_上海理_试题.md`、`2006_数学真题_上海理_答案要点.md`、`2006_数学真题_上海理_解析正文.md`。
- 使用 `solution_sources.render_combined()` 对三份规范源确定性生成 `2006_数学真题_上海理_含解析.md`；解析器成功识别 22 题，并核对题号、小问集合与答案块一致。
- 答案与解析由编者独立推导，公开官方答案仍未核，`official_answer=null`。题面 PDF 没有答案页。

## 验证与未完成项

- `register-papers` dry-run 先通过，随后写入 revision 5195。
- `source_manifest.py validate --manifest source-manifest.json` 与 `report.py check --all --manifest source-manifest.json --issues missing-issues.md` 均成功。
- 仍待完成四张矢量图及 figure manifest、逐题 provenance、项目 TeX/四版入口、四版 XeLaTeX 构建、逐页视觉审查及批次收口。本阶段未运行测试套件，未联网核查，未 push。

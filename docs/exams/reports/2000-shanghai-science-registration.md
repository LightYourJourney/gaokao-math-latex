# 2000 上海理科候选卷：paper/source/issue 登记

- 日期：2026-11-03。固定 source `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`，PDF SHA-256 `b798af61afdac624589769db5bbafe734aa9a001697bd00b3f5bc8028ab3a40`。题面两页映射到 PDF 第1–2页；固定副本无答案或解析页。
- `source_manifest.py register-papers` dry-run 通过，正式单一状态事务将 manifest revision `6087→6088`，transaction `1a368a14-9815-44c0-9bd0-34c7eb42c9af`。登记 paper `gk-2000-regular-shanghai-science`、batch `phase4-b42`、目录 `2000_上海卷_理科`，并将该 source 在本库内部绑定为 `canonical`。这仅固定本库采用的候选文件，不认证发布者、版次、复制链或官方身份。
- 同一事务创建两条 open / `blocks_completion` 问题：`ISSUE-1369`（Q12 `transcription-ambiguous`，原页“等此数列”，不可确认数列类型）与 `ISSUE-1370`（Q21 `answer-conflict`，原页指数2导致 $B_n=20^n$ 无最大项）。两题继续保留 U/PENDING。
- 登记后将 `paper_id` 写入规范题面、答案要点、解析正文；调用 `solution_sources.py extract-batch --write --batch phase4-b42` 生成当前 `_含解析.md`，并在解析正文补齐 22 个 `**解析**` 标记。规范答案要点的 Q12、Q21 答案状态仍为 U/PENDING。四个文件 SHA-256：
  - `_试题.md` `31842e97b122f5c1ccf5184e6541ff6bd64f6bc3bdbbd1fab3274d038e79154c`
  - `_答案要点.md` `356bea3e9a50a6d77cf9e1535aaca86d3b3e310ee7840abec2f36f1200716431`
  - `_解析正文.md` `5617ee2dd8a00538234444c8cd2cd87a096d01a7941ad0b073824fb23cef0b7b`
  - `_含解析.md` `3658227faa3c2e8b54f0b0a92d1c7c148e2a713de1cf78da4f9ba746d002f567`
- paper 当前为 `blocked`（`blocked_from=planned`），batch `planned`。`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`manifest_csv.py --check`（775行）通过。CSV 已更新。逐题 provenance、TikZ 图稿登记、共享 TeX、正式构建及视觉验收尚未开始。

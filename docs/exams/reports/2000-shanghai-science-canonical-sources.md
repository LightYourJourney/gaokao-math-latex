# 2000 上海理科候选卷：规范事实源文件建立

- 日期：2026-11-03。由题面、答案要点和解析正文草稿建立规范事实源文件；固定 source 为 `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`，固定 PDF SHA-256 `b798af61afdac624589769db5bbafe734aa9a001697bd00b3f5bc8028ab3a40`。
- 规范文件：
  - `2000/2000_数学真题_上海理_试题.md`，SHA-256 `4cfec39e47a05709a9c8360ebc0262e636af099640f97e48dbd8343f65343880`
  - `2000/2000_数学真题_上海理_答案要点.md`，SHA-256 `f7af91248c8a9afaadb0e29d59da56ec0948c023e668a998c89337273c759caa`
  - `2000/2000_数学真题_上海理_解析正文.md`，SHA-256 `fd66aee6c5b38c4de9d6d4d5bb4df7399165f3f004a9b5aaa157ec8991a78dd9`
- 题面各题正文与已独立复核草稿一致；题首来源说明更新为“本库答案为独立推导”，避免沿用盲核前的过期状态。答案与解析仅调整 front matter、文档标题和泛化来源说明，数学内容与 `U/PENDING` 状态不变。三个文件暂保留 `paper_id: null`、`official_answer: null`，尚未与 manifest 绑定。
- 定向结构检查确认题面正文一致、答案和解析均连续覆盖 Q1–Q22、题号逐题对齐，行间与行内数学定界符成对。`git diff --check` 通过。
- 本阶段未改 `source-manifest.json` 或 `missing-issues.md`，未生成 `_含解析.md`。下一阶段用 `source_manifest.py register-papers` 单一事务登记 paper/batch 及 Q12、Q21 阻断项，再写入 paper ID 并确定性生成合并稿。

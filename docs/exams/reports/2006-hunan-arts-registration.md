# 2006 湖南文科候选卷：paper/source 登记与 Q17 blocker 入账

- 日期：2026-11-02。
- 通过 `source_manifest.py register-papers` 注册 `gk-2006-regular-hunan-arts` 与 `phase1-b74`，将固定候选 source `src-6387f1664484c2d0ee3ea1a27f673d6624df685f465bfd701fb8e95c0a8b856d` 内部绑定为 canonical；登记事务使 manifest revision `5938→5939`，随后图稿登记使 revision `5939→5940`。
- `canonical` 仅表示 manifest 内部绑定固定 PDF 字节为本卷来源输入。文件题签、SHA-256、Git blob 和本地页数不能认证发布者、出版者、版次、来源链或官方身份。`official_answer` 保持 `null`。

## Q17（3）待裁定项

- 注册事务建立 `ISSUE-1338`，类型 `answer-convention-ambiguous`，状态 `open`、影响 `blocks_completion`。题面说明“每家煤矿安检是否合格是相互独立的”，但未明确跨矿整改复查结果的联合关系。
- 答案要点现保留 `U/PENDING`。$0.41$ 只作为假设各家从初检到复查的结果相互独立时的条件计算，并未标作无条件或官方答案。
- 因该 issue，paper 为 `blocked`、`blocked_from=planned`；batch `phase1-b74` 保持 `planned`。

## 登记与验证

- 规范题面、答案要点、解析正文的 `paper_id` 已绑定；含解析稿由 `solution_sources.render_combined()` 确定性重生成。题目和解析中的小问标记按解析器约定添加排版锚点/分隔空格，未改写数学内容。
- 两幅 TikZ 图通过 `sync-figure-registry` 写入 manifest，路径分别为 `2006_湖南卷_文科/figures/f2006hunan_arts_q10_vector_region.tex` 与 `f2006hunan_arts_q18_pyramids.tex`；各自 `expected_occurrences=3`，与规范题面及含解析稿中的引用相符。
- `source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`manifest_csv.py --check`（775 行）及 `solution_sources.py check-batch --batch phase1-b74` 均通过。`register-papers` dry-run 返回 1 卷通过、未落盘，之后正式写入成功。
- 逐题 provenance、项目 TeX、正式四版构建及正式页面视觉审查仍未完成。来源身份未认证；Q17（3）继续阻断本卷完成。本阶段不表示卷级验收或长期语料完成。

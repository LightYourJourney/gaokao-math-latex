# 2004 上海理科普通卷：项目 TeX 生成、简答与四版入口

- 日期：2026-11-04。
- 批次/试卷：`phase4-b46` / `gk-2004-regular-shanghai-science`。
- 固定候选来源：`src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a`，PDF SHA-256 `9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e`。

## 项目生成结果

按 `phase4-b46` 逐卷生成：

| 文件 | SHA-256 |
|---|---|
| `2004_上海卷_理科/questions.tex` | `8053b46e8bbbd44280b9d6bdcb737e2e3f9b74d3f88e63df794b93ff81f7e64f` |
| `2004_上海卷_理科/answers.tex` | `66608d7406156463bd5cdcc8f105b82b578b21b65b4a2fa5de9bbe4ba40adc55` |
| `2004_上海卷_理科/answers_short.tex` | `65a2ca60c1930171b3798617aa9d9eb1a4ae492763538b2edb364972acda3218` |
| `2004_上海卷_理科/试题版.tex` | `e689545e10b8c3612ccb772f5e953bbf65bb3c46780fe5b493ed44f36eb393fb` |
| `2004_上海卷_理科/解析版.tex` | `34c3513ba8fe2a9427690c687368e532208f50a06dedd36a3c94988aac52e3f1` |
| `2004_上海卷_理科/简答版.tex` | `63a1631d66be823fec7464f28167d41d1d9d21c493589fb5bc77e532aae8b133` |
| `2004_上海卷_理科/印刷版.tex` | `ded5cd5c6078b2bca2b3e0666ecb4ac0caec2c82a87f1a2e32a6a276d98b7549` |
| `index.json` | `227759e89e02e3abbff615d5d8deaad6f96e7808ec07438f34beed50cf90f117` |

索引条目登记22题、Q5/Q18/Q21三张图和候选来源说明。生成的 `questions.tex`、`answers.tex` 均包含三张图的 `\input`；简答稿继续保留 Q19、Q22 的 U/PENDING。

## 验证与边界

- 串行执行 `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`；三项均与生成结果一致。
- `solution_sources.py check-batch`（22题）、`provenance.py check-batch`（22题）、`source_manifest.py validate`、`issues.py validate` 均通过。Q19 `ISSUE-1386` 与 Q22 `ISSUE-1387` 继续 open / blocks_completion。
- 本阶段生成项目 TeX、简答与四版入口；尚未编译正式 PDF、写 build/review receipt 或进行整卷逐页视觉验收。固定 PDF 无答案页，`official_answer=null`，paper 仍 blocked。本报告不表示来源认证、整卷完成或长期语料库完成。

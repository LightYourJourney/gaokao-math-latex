# 2003 北京普通文理候选卷：四版正式构建

- 日期：2026-11-04；batch `phase4-b48`；正式构建输入 manifest revision `6155`，完成后 revision `6156`。
- 文科 attempt `c613dd52-166d-4f73-a9f5-913c37f198d5`；理科 attempt `d43c5ef7-3c6f-41b0-ac17-6c2a37a7130d`。两卷四版共 8 份 PDF 全部 `succeeded`，合计 95 页。

## 首次尝试与构建修正

- 首次 attempt：文科 `7c4bc8a2-1801-4d76-b999-f376bc4aca6c`、理科 `607cef33-4290-4608-855c-ff6fb4810dd2`，输入 revision `6152`。文科解析版、印刷版因生成的 `answers.tex` 将 `official_answer=null` 放在 `\texttt{}` 中，触发 `Missing $ inserted`；理科四版因 Q1 的 `(A\cap B)` 未放入数学模式而在 `questions.tex` 第 19 行触发同一 TeX 错误。构建事务登记 `ISSUE-1402`–`ISSUE-1407`。
- 修正只涉及 Markdown 标记：两卷答案要点和解析正文的自然语言说明将行内代码 `official_answer=null` 改为“官方答案字段为 null”，front matter 的 `official_answer: null` 保持不变；理科 Q1 将 `(A\cap B)` 包为 `\((A\cap B)\)`，数学字符和题意不变。重新生成两份 `_含解析.md` 与受影响 TeX，并更新理科 Q1 的题面哈希声明；`provenance.py import-batch` 通过事务将 manifest revision `6153→6154`。原有复核结论、答案证据、`U/PENDING` 与四项题源 blocker 均未改变。
- 正式重跑将 6 个编译问题对账为 `resolved / non_blocking`。第二次尝试全部版本编译成功。

## 正式 PDF 与构建回执

`receipts/build.json` 绑定各卷 attempt、输入树、manifest revision、TeX Live 2026 工具链、PDF SHA-256 和页数。

| 卷别 | 版本 | 页数 | PDF SHA-256 |
|---|---|---:|---|
| 文科 | 试题版 | 5 | `64eb1132a7be2a6d34d16b22b2a845d3ac2e06183c75939270464473eafb4b1e` |
| 文科 | 解析版 | 19 | `6a083dfbdcc1231919284e07993aada2227dc588ffd5f643c1a7c475df8a6a76` |
| 文科 | 简答版 | 7 | `86bd7ca6f92db6de63d5f4eaf6323ff2afd7787f4a6a2fe47544f03ddd8877dd` |
| 文科 | 印刷版 | 13 | `1a2b2c7ec09a9a41c3bd67448f646e0b9170acc74df1f3c1f6669c68d7fc0e5b` |
| 理科 | 试题版 | 6 | `a17a237bf7f82130f9b77fc891bdd97d72f5fba8195bfa75a7615dbb6bb2c9f5` |
| 理科 | 解析版 | 21 | `ef27cefed0b662a675fe86ee6b6485ab57ec1c2b8e0bbacd17c308035b750eab` |
| 理科 | 简答版 | 8 | `c1535b093a082a2ef36ba7be160a22cb04b7af80d7e32b4dd1141945edc20e25` |
| 理科 | 印刷版 | 16 | `ff40b616e4c665f47cf73e1dfc96be6a07f1f6e6262573eacaddbdba915380a8` |

- 8 份回执均无编译错误、缺字或未定义引用；理科解析版在 `answers.tex` 第 450 行记录一处 `0.66212pt` 的 Overfull hbox，视觉审查时检查其所在页是否侵入版心或影响阅读。
- `build_projects.py validate-receipts --manifest source-manifest.json --batch phase4-b48 --require-current-inputs --json` 返回 `code=OK`、`failed=0`、`invalid=0`、`missing=0`、`stale=0`。源账、issues、provenance、逐题答案层和三类生成器检查均通过；`manifest.csv` 当前且 775 行。

## 当前边界

- `review_receipts.py prepare-batch` 已在 `.work/phase4-b48/review` 建立 8 个版本工作项，共 95 页，逐页视觉复核尚未完成；batch 当前为 `compiled_pending_review`。
- 文科 Q18 的 `ISSUE-1398`/`ISSUE-1399` 与理科 Q17 的 `ISSUE-1400`/`ISSUE-1401` 仍 open / `blocks_completion`，两卷 paper 继续 `blocked`。候选 PDF 发布链、官方身份与官方答案未核，`official_answer=null`。本阶段不表示整卷验收或长期语料完成。

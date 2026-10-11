# 高考数学 LaTeX 题库进度

> 本文件是跨会话恢复点。恢复工作时先核对本文件、规范工作树的 `git status`/`git diff` 与 manifest；不要重做已记录且仍有当前证据的步骤。

## 项目阶段

详细验收阶段见 [全量收尾实施计划](../../superpowers/plans/2026-10-12-gaokao-corpus-completion.md)。项目尚未整体完成：当前 manifest 共 272 卷、138 批。

| 阶段 | 范围 | 状态 | 可验证的完成条件 |
|---|---|---|---|
| A | 公共样式、脚手架、manifest、构建与回执工具 | 已有，待最终全库审计 | 检查公共文件、CLI validators、测试及四版构建入口 |
| B | 1952—2006 | 进行中 | 每批 source/provenance、四版构建、全页视觉复核、final receipts/report 通过；未解决项显式登记 |
| C | 2007—2016 | 待推进 | 同阶段 B，覆盖该范围全部 manifest 批次 |
| D | 2017—2026 | 待推进 | 同阶段 B，确认使用已完成转录核查且保持来源哈希一致 |
| E | 全库整合与交付 | 待推进 | 全库 validators/tests、README、manifest.csv、缺失清单及报告完整且状态真实 |

## 已完成阶段

| 批次 | 试卷 | 结果 | 提交 |
|---|---|---|---|
| `phase1-b09` | 1952 全国卷 | 四版 32 页复核；FINALIZED；构建目录仅保留 PDF | `40cde6ac` |
| `phase1-b10` | 1953 全国卷 | 四版 25 页复核；FINALIZED；构建目录仅保留 PDF | `c66dcdbb` |
| `phase1-b11` | 1954 全国卷 | 四版 21 页复核；两条现存警告豁免与当前日志逐项匹配；FINALIZED | `ec61de91` |
| `phase1-b12` | 1955 全国卷 | 四版 14 页复核；FINALIZED；构建目录仅保留 PDF | `219ddd4b` |
| `phase1-b13` | 1956 全国卷 | 四版 21 页复核；FINALIZED；source/build/review/provenance/report gates 通过；构建目录仅保留 PDF | `ec368208` |
| `phase1-b14` | 1957 全国卷 | 旧 build/review 指纹过期后正式重建；四版 24 页复核、4 个候选页高分辨率复核；FINALIZED；门禁通过；构建目录仅保留 PDF | `890d4def` |
| `phase1-b15` | 1959 全国卷 | 历史回执过期后正式重建；四版 22 页复核、4 个候选页高分辨率复核；FINALIZED；门禁通过；构建目录仅保留 PDF | `3188b06f` |
| `phase1-b16` | 1960 全国卷 | 历史回执过期后正式重建；四版 26 页复核、4 个候选页高分辨率复核；FINALIZED；门禁通过；构建目录仅保留 PDF | `f89e260e` |
| `phase1-b17` | 1961 全国卷 | 历史回执过期后正式重建；四版 24 页复核、4 个候选页高分辨率复核；FINALIZED；门禁通过；构建目录仅保留 PDF | `67016eff` |
| `phase1-b18` | 1962 全国卷 | 历史回执过期后正式重建；四版 30 页复核、4 个候选页高分辨率复核；既存 Underfull 精确豁免；FINALIZED；门禁通过；构建目录仅保留 PDF | `c140aa65` |
| `phase1-b19` | 1958 河北卷 | 历史回执过期后正式重建；四版 18 页复核、4 个候选页高分辨率复核；0 警告；FINALIZED；门禁通过；构建目录仅保留 PDF | `67f82cc3` |
| `phase1-b20` | 1963 全国卷 | 历史回执过期后正式重建；四版 32 页复核、4 个候选页高分辨率复核；0 警告；FINALIZED；门禁通过；构建目录仅保留 PDF | `61f3cffe` |
| `phase1-b21` | 1964 全国卷 | 历史回执过期后正式重建；四版 25 页复核、4 个候选页高分辨率复核；0 警告；FINALIZED；门禁通过；构建目录仅保留 PDF | `788ef1b0` |
| `phase1-b22` | 1965 全国卷 | 四版 32 页逐页复核、4 个候选页高分辨率复核；0 警告；FINALIZED；scoped gates 与全量报告检查通过；构建目录仅保留 PDF | `e401d383` |
| `phase2-b23` | 1977 上海卷文理科 | 四版 53 页逐页复核、8 个候选页及 2 个历史问题页高分辨率复核；0 警告；FINALIZED；门禁与全量报告检查通过；两卷构建目录仅保留 PDF | 本阶段待提交 |

上述批次的提交在当前工作树中可由 `git log` 查证；不代表 1952—2006 或整个题库已完成。

## 最近完成阶段

### `phase2-b23` — 1977 上海卷文理科（待提交）

- 既有状态：文、理两卷各有 8 题 provenance；6 条历史 issue 均 resolved。旧 build/review 指纹过期，不重做来源争议核查或转录解题。
- 已完成：formal build 四版成功、0 警告，共 53 页（文科 22、理科 31）；全页接触表检查 53 页，8 个候选页及理科印刷版 p.6、解析版 p.9 两个历史问题页高分辨率复核，无视觉缺陷；`finalize-batch` 返回 `FINALIZED`。
- 已完成：两卷 `build/` 仅保留四份 PDF；清理本批工作项与临时 PNG；source/build/review/provenance scoped gates 通过；全量报告事务更新并通过一致性检查。
- 修改文件：两卷 build/review receipts 与 PDF、`source-manifest.json`、`reports/phase2-b23.md`；renderer 更新的全量报告投影；本进度文件。
- 验证：source manifest `OK`（775 项）；build `OK：2 卷`；review `FINALIZED：phase2-b23`；provenance `OK：2 卷`；`report.py check --all` 输出“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”；构建目录各仅剩四份 PDF。
- 提交状态：本阶段待提交，未 push。

## 当前进行阶段

### `phase2-b23` — 1977 上海卷文理科

- 既有状态：文、理两卷各有 8 题 provenance，原有 build 均四版成功，review receipt 均为 passed；但 review 各自绑定的 build attempt 与当前 build attempt 不同，且 build receipt 因生成输入树和工具链指纹变化而失效。旧页数分别为文科 2/9/3/8、理科 3/14/4/10。
- 问题项：文科 `ISSUE-0125/0126` 与理科 `ISSUE-0916`—`ISSUE-0919` 均为 resolved；不重开来源争议或重复转录/解题。
- 已完成子阶段：核对 manifest、两卷 provenance/receipts 与历史 issue；provenance 检查未报题目证据错误，但指出派生缓存状态不一致（两卷 `compiled` vs `editions_generated`，批次 `compiled_pending_review` vs `provenance_verified`）；build validator 确认两卷需因生成输入树/工具链变化正式重建。
- 已完成子阶段：两卷四版 formal build 成功、0 失败、0 警告；文科 22 页、理科 31 页，共 53 页；8 个 review 工作项已绑定当前 build attempts。候选页：文科 试题 p.1/解析 p.1/简答 p.1/印刷 p.1；理科 试题 p.1/解析 p.4/简答 p.1/印刷 p.8。
- 修改文件：本进度文件；两卷 build receipts 与四版 PDF；忽略目录 `.work/phase2-b23/review/` 下 8 个工作项。
- 已完成子阶段：53 页全页接触表视觉检查无可见缺陷；8 个候选页及 6 条已解决历史 issue 涉及的理科印刷版 p.6、解析版 p.9 均完成高分辨率复核，无裁切、字形或标注问题。
- 已完成子阶段：53 页视觉结果已登记，`finalize-batch` 返回 `FINALIZED：phase2-b23`；6 条历史 issue 均保持 resolved。
- 已完成子阶段：两卷 build 目录仅保留四版 PDF；本批 `.work/` 与临时 PNG 已清理。source manifest、build receipt、review receipt、provenance scoped gates 全通过。
- 待完成：刷新并检查全量报告，审阅最终 diff 后单批提交。
- 修改文件：本进度文件；两卷 build/review receipts、构建 PDF、manifest 与批次报告；全量报告投影待刷新。
- 下一步：执行 `report.py render --all` 和 `check --all`，核对状态后提交；不重做已核实的来源与答案工作。

## 最近一次全库状态快照

来自 1964 全国卷 finalize 后的当前 `source-manifest.json`（每次恢复须刷新）：

- 来源 775；试卷 272；批次 138。
- 批次状态：closed 46、closed_with_blockers 13、compiled_pending_review 77、provenance_verified 2。
- 试卷状态：complete 82、blocked 45、compiled 141、editions_generated 4。
- 这说明仍有大量待复核/阻塞工作；这些数字是进度快照，不是验收目标，也不应伪装成已完成。

## 最近验证与已知问题

- 1956 视觉复核：21 页逐页检查；试题版第 1 页、解析版第 1 页、简答版第 1 页、印刷版第 5 页高分辨率复核。
- 1957 视觉复核：24 页逐页检查；试题版第 1 页、解析版第 7 页、简答版第 1 页、印刷版第 6 页高分辨率复核；四页均无视觉缺陷。
- 1959 视觉复核：22 页逐页检查；试题版第 1 页、解析版第 8 页、简答版第 1 页、印刷版第 6 页高分辨率复核；四页均无视觉缺陷。
- 1960 视觉复核：26 页逐页检查；试题版第 2 页、解析版第 4 页、简答版第 1 页、印刷版第 7 页高分辨率复核；四页均无视觉缺陷。
- 1961 视觉复核：24 页逐页检查；试题版第 1 页、解析版第 1 页、简答版第 2 页、印刷版第 7 页高分辨率复核；四页均无视觉缺陷。
- 1962 视觉复核：30 页逐页检查；试题版第 2 页、解析版第 9 页、简答版第 4 页、印刷版第 8 页高分辨率复核；四页均无视觉缺陷；一条既存 Underfull 警告已逐项豁免。
- 1958 河北卷视觉复核：18 页逐页检查；四版均高分辨率复核第 1 页；未发现视觉缺陷。
- 1963 视觉复核：32 页逐页检查；四版均高分辨率复核第 1 页；未发现视觉缺陷。
- 1964 视觉复核：25 页逐页检查；试题版第 1 页、解析版第 1 页、简答版第 1 页、印刷版第 7 页高分辨率复核；未发现视觉缺陷。
- 本批验证输出：1964 source manifest `OK`（775 项）；build receipt `FINALIZED：phase1-b21`；review receipt `OK：1 卷`；provenance `OK：1 卷`；全量报告与 manifest 当前一致。
- 全套单元测试最近一次（早于 phase1-b13—b21）：862 tests，848 passed、13 skipped、1 failed。唯一失败为 `tests/test_provenance.py::LiveRepositoryTests::test_the_cached_states_match_the_recomputed_ones`，当时全库旧缓存状态与现场派生不一致（报告 297 项）。1956—1964 已按正式批次推进状态；该测试尚未重跑，不能声称全库测试通过。
- 分支不 push；提交前核对 branch/worktree，当前 canonical worktree 是 `仓库根`。

## 下一步

- 1956 阶段已于提交 `ec368208` 完成。
- `phase1-b14` 已于 `890d4def` 提交。
- `phase1-b15` 已于 `3188b06f` 提交；`phase1-b16` 已于 `f89e260e` 提交。
- `phase1-b17`（1961 全国卷）已于 `67016eff` 提交。
- `phase1-b18`（1962 全国卷）已于 `c140aa65` 提交。
- `phase1-b19`（1958 河北卷）已于 `67f82cc3` 提交。
- `phase1-b20`（1963 全国卷）已于 `61f3cffe` 提交。
- `phase1-b21`（1964 全国卷）已于 `788ef1b0` 提交。
- `phase1-b22`（1965 全国卷）已于 `e401d383` 提交。
- `phase2-b23`（1977 上海文理卷）已完成 formal build、53 页视觉复核、finalize、门禁与报告检查；本阶段待提交。
- 下一批为 `phase2-b24`（1977 北京文理卷）；提交 b23 后先检查已有 provenance、问题项与历史回执，再确定刷新范围。
- 继续前刷新 manifest 与 Git 状态；每完成一个批次阶段，更新本文件、运行对应 scoped gates 与全量报告检查，再单批提交。

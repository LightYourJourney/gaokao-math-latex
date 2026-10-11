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
| `phase1-b19` | 1958 河北卷 | 历史回执过期后正式重建；四版 18 页复核、4 个候选页高分辨率复核；0 警告；FINALIZED；门禁通过；构建目录仅保留 PDF | 本阶段待提交 |

上述批次的提交在当前工作树中可由 `git log` 查证；不代表 1952—2006 或整个题库已完成。

## 最近完成阶段

### `phase1-b18` — 1962 全国卷（本阶段待提交）

- 既有状态：源稿与 10 题 provenance 已存在；build receipt 因生成输入树、工具链指纹变化失效，旧 review 绑定失效构建。历史 `ISSUE-0123/0124` 已 resolved；未重做转录或解题。
- 已完成：formal build；四版共 30 页逐页视觉检查；试题版第 2 页、解析版第 9 页、简答版第 4 页、印刷版第 8 页高分辨率复核；未发现视觉缺陷。解析版第 9 页 `answers.tex:349` Underfull 警告与旧 review 登记完全相同，本轮复核确认答案框完整并在版心内，已按当前页码 9 精确豁免；`finalize-batch` 返回 `FINALIZED`。
- 已完成：全量报告事务更新并通过一致性检查；只删除 `1962_全国卷/build/` 中非 PDF 编译产物，保留四份 PDF；清理本批 `.work/` 与本次临时 PNG。
- 修改文件：1962 build/review receipts、`source-manifest.json`、`reports/phase1-b18.md`；renderer 更新的全量 README/报告投影；本进度文件。
- 验证：source manifest `OK：1 卷`；build receipt `FINALIZED：phase1-b18`；review receipt `OK：1 卷`；provenance `OK：1 卷`；`report.py check --all` 输出“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”；`git diff --check` 通过。构建目录核验仅剩四份 PDF。
- 提交状态：已提交 `c140aa65`，未 push。

## 当前进行阶段

### `phase1-b19` — 1958 河北卷（本阶段待提交）

- 既有状态：源稿与 8 题 provenance 已存在，manifest `issue_ids=[]`；formal build receipt 因生成输入树、工具链指纹变化失效，旧 review 绑定旧构建且视觉指纹过期。未重做转录或解题。
- 已完成子阶段：来源/provenance、问题项与历史 build/review receipts 核对；旧 PDF 页数为 1/8/2/7，旧 build 与 review 均不得作为当前证据。formal build 成功、0 失败；新页数为 1/8/2/7，共 18 页，未产生构建警告；四版 review 工作项已准备。
- 已完成子阶段：四版共 18 页全部视觉检查；试题版第 1 页、解析版第 1 页、简答版第 1 页、印刷版第 1 页高分辨率复核，未见缺陷；构建无警告；`finalize-batch` 返回 `FINALIZED`。
- 已完成：清理非 PDF 编译产物与本批临时 PNG；构建目录只保留四版 PDF；scoped gates 与全量报告检查通过。
- 修改文件：1958 河北卷 build/review receipts、`source-manifest.json`、`reports/phase1-b19.md`；renderer 更新的全量 README/报告投影；本进度文件。
- 验证：source manifest `OK`（要求 775 项）；build receipt `FINALIZED：phase1-b19`；review receipt `OK：1 卷`；provenance `OK：1 卷`；全量报告与 manifest 当前一致；`git diff --check` 通过。
- 提交状态：尚未提交；下一步审阅并提交 b19 批次及进度记录，不 push。

## 最近一次全库状态快照

来自 1958 河北卷 finalize 后的当前 `source-manifest.json`（每次恢复须刷新）：

- 来源 775；试卷 272；批次 138。
- 批次状态：closed 42、closed_with_blockers 13、compiled_pending_review 81、provenance_verified 2。
- 试卷状态：complete 77、blocked 45、compiled 146、editions_generated 4。
- 这说明仍有大量待复核/阻塞工作；这些数字是进度快照，不是验收目标，也不应伪装成已完成。

## 最近验证与已知问题

- 1956 视觉复核：21 页逐页检查；试题版第 1 页、解析版第 1 页、简答版第 1 页、印刷版第 5 页高分辨率复核。
- 1957 视觉复核：24 页逐页检查；试题版第 1 页、解析版第 7 页、简答版第 1 页、印刷版第 6 页高分辨率复核；四页均无视觉缺陷。
- 1959 视觉复核：22 页逐页检查；试题版第 1 页、解析版第 8 页、简答版第 1 页、印刷版第 6 页高分辨率复核；四页均无视觉缺陷。
- 1960 视觉复核：26 页逐页检查；试题版第 2 页、解析版第 4 页、简答版第 1 页、印刷版第 7 页高分辨率复核；四页均无视觉缺陷。
- 1961 视觉复核：24 页逐页检查；试题版第 1 页、解析版第 1 页、简答版第 2 页、印刷版第 7 页高分辨率复核；四页均无视觉缺陷。
- 1962 视觉复核：30 页逐页检查；试题版第 2 页、解析版第 9 页、简答版第 4 页、印刷版第 8 页高分辨率复核；四页均无视觉缺陷；一条既存 Underfull 警告已逐项豁免。
- 1958 河北卷视觉复核：18 页逐页检查；四版均高分辨率复核第 1 页；未发现视觉缺陷。
- 本批验证输出：1958 河北卷 source manifest `OK`（775 项）；build receipt `FINALIZED：phase1-b19`；review receipt `OK：1 卷`；provenance `OK：1 卷`；全量报告与 manifest 当前一致。
- 全套单元测试最近一次（早于 phase1-b13—b19）：862 tests，848 passed、13 skipped、1 failed。唯一失败为 `tests/test_provenance.py::LiveRepositoryTests::test_the_cached_states_match_the_recomputed_ones`，当时全库旧缓存状态与现场派生不一致（报告 297 项）。1956—1962 已按正式批次推进状态；该测试尚未重跑，不能声称全库测试通过。
- 分支不 push；提交前核对 branch/worktree，当前 canonical worktree 是 `仓库根`。

## 下一步

- 1956 阶段已于提交 `ec368208` 完成。
- `phase1-b14` 已于 `890d4def` 提交。
- `phase1-b15` 已于 `3188b06f` 提交；`phase1-b16` 已于 `f89e260e` 提交。
- `phase1-b17`（1961 全国卷）已于 `67016eff` 提交。
- `phase1-b18`（1962 全国卷）已于 `c140aa65` 提交。
- `phase1-b19`（1958 河北卷）已完成 formal build、18 页视觉复核及所有 scoped/global 报告门禁；尚待提交。
- 下一批为 `phase1-b20`（1963 全国卷），状态 `compiled_pending_review`；恢复时先查来源/provenance、问题项与历史 receipts，只刷新失效证据，不重复转录。
- 下一步：审阅并提交 b19 阶段，然后接手 `phase1-b20`。
- 继续前刷新 manifest 与 Git 状态；每完成一个批次阶段，更新本文件、运行对应 scoped gates 与全量报告检查，再单批提交。

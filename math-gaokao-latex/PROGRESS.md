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
| `phase2-b23` | 1977 上海卷文理科 | 四版 53 页逐页复核、8 个候选页及 2 个历史问题页高分辨率复核；0 警告；FINALIZED；门禁与全量报告检查通过；两卷构建目录仅保留 PDF | `3477d184` |
| `phase2-b24` | 1977 北京卷文理科 | 四版 39 页逐页复核、8 个候选页高分辨率复核；0 警告；FINALIZED；门禁与全量报告检查通过；两卷构建目录仅保留 PDF | `b59a82f9` |
| `phase2-b25` | 1977 天津卷 | 四版 24 页逐页复核、候选及问题相关页高分辨率复核；0 警告；FINALIZED；四项门禁与全量报告检查通过；构建目录仅保留 PDF | `d0ae344e` |
| `phase2-b26` | 1977 河北卷 | 四版 26 页逐页复核、4 个候选页及首面高分辨率复核；0 警告；FINALIZED；四项门禁与全量报告检查通过；构建目录仅保留 PDF | 本批待提交 |

上述批次的提交在当前工作树中可由 `git log` 查证；不代表 1952—2006 或整个题库已完成。

## 最近完成阶段

### `phase2-b24` — 1977 北京卷文理科（已提交）

- 既有状态：文、理两卷各有 10 题 provenance、`issue_ids=[]`；旧 build/review 指纹过期，不重做转录或解题。
- 已完成：formal build 四版成功、0 警告，共 39 页（文科 16、理科 23）；接触表逐页复核 39 页，8 个候选页均高分辨率复核，无视觉缺陷；`finalize-batch` 返回 `FINALIZED`。
- 已完成：两卷 `build/` 仅保留四份 PDF；本批 `.work/` 与临时 PNG 清理；source/build/review/provenance scoped gates 通过；全量报告事务更新并通过一致性检查。
- 修改文件：两卷 build/review receipts 与 PDF、`source-manifest.json`、`reports/phase2-b24.md`；renderer 更新的全量报告投影；本进度文件。
- 验证：source manifest `OK`（775 项）；build `OK：2 卷`；review `FINALIZED：phase2-b24`；provenance `OK：2 卷`；`report.py check --all` 输出“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”；构建目录各仅剩四份 PDF。
- 提交状态：已提交 `b59a82f9`，未 push。

## 最近完成阶段

### `phase2-b25` — 1977 天津卷（已提交 `d0ae344e`）

- 既有状态：5 题 provenance 已存在；`ISSUE-0127/0128` 均为 resolved。旧 build 四版成功、旧 review passed，但 review 与 build attempt 不匹配；build validator 确认生成输入树和工具链指纹变化导致旧构建回执失效；旧页数为 3/9/4/8，共 24 页。
- 已完成子阶段：核对 manifest、provenance、问题项与 receipts；provenance 检查未报题目证据错误，只指出派生状态缓存不一致（paper `compiled` vs `editions_generated`，batch `compiled_pending_review` vs `provenance_verified`）。不重做题目转录或解题。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 24 页；4 个 review 工作项已绑定当前 build attempt。候选页：试题 p.2、解析 p.5、简答 p.2、印刷 p.6。
- 修改文件：本进度文件（b24 提交号校正及 b25 预检记录）；天津卷 build receipt/PDF；忽略目录 `.work/phase2-b25/review/` 下 4 个工作项。
- 已完成子阶段：24 页接触表逐页检查无可见缺陷；四版第 1 页确认完整题干，解析版 p.4–5 与印刷版 p.3 覆盖两条已解决 issue 的分类解析；4 个候选页（试题 p.2、解析 p.5、简答 p.2、印刷 p.6）及 issue 相关页均高分辨率复核，无视觉缺陷。
- 已完成子阶段：4 个 review 工作项登记全部 24 页及 192 项逐页检查为 pass；`finalize-batch` 返回 `FINALIZED：phase2-b25`，生成 `reports/phase2-b25.md` 并事务性更新回执与 manifest。
- 修改文件：本进度文件；天津卷 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b25.md`；review 工作项（忽略目录）；临时接触表及高分辨率 PNG 位于 `/tmp/gk-phase2-b25-review/`。
- 已完成子阶段：清除天津卷 `build/` 下所有非 PDF 中间物，保留试题、解析、简答、印刷四份 PDF；清理本批 `.work/phase2-b25` 与 `/tmp/gk-phase2-b25-review/`。
- 已完成子阶段：source manifest 校验（`--require-artifacts 775`）、build receipt `OK：1 卷`、review `FINALIZED：phase2-b25`、provenance `OK：1 卷`，全部退出码 0。
- 修改文件：天津卷 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b25.md`；本进度文件；构建目录中间物及本批临时/忽略工作文件已清理。
- 已完成子阶段：`report.py render --all` 通过，以单个 content 事务写入并回读校验六个全量报告目标。
- 复核记录修正：diff 检查发现新 review receipt 虽记录全部 pass，但逐项 note 为空；为避免丢失本次视觉证据说明，将补入与已完成复核相符的统一说明，并经现有 FINALIZED 回执的 report-only 重验证路径重新校验，不重跑构建或视觉审查。
- 已完成：为 review receipt 的 192 项检查补入本次全页及候选/issue 相关高分辨率复核说明；report-only `finalize-batch` 再次返回 `FINALIZED：phase2-b25`。
- 已完成子阶段：`report.py check --all` 通过，报告与全量 manifest 当前一致，未完成状态已在报告中保留；回执说明修正后的 scoped gates 全部通过，全量报告再次经单事务 render 写入并回读校验六个目标。
- 已完成子阶段：最终 `report.py check --all` 再次通过；manifest revision 3824，来源 775、试卷 272、批次 138；批次状态 closed 48、closed_with_blockers 13、compiled_pending_review 75、provenance_verified 2；试卷状态 complete 85、blocked 45、compiled 138、editions_generated 4。
- 最终核对：`git diff --check` 通过；天津卷 build 目录只有四份 PDF；11 个受本批事务影响的 tracked 文件包含天津卷回执、批次/全量报告投影、manifest 与本进度文件，无题目源文件改动。
- 提交状态：已提交 `d0ae344e`，未 push。

## 当前进行阶段

### `phase2-b26` — 1977 河北卷

- 既有状态：单卷、8 题 provenance 已登记，`issue_ids=[]`；不重做转录或解题。manifest 缓存为 `compiled_pending_review`，provenance 检查未发现题目证据问题，仅报告派生缓存状态不一致（paper `compiled` vs `editions_generated`，batch `compiled_pending_review` vs `provenance_verified`）。
- 历史回执：旧 build 四版均成功，页数 3/11/4/8，共 26 页；build 因生成输入树与工具链指纹变化失效。旧 review `passed` 但绑定另一 build attempt，不能复用。
- 已完成子阶段：核对 batch、paper/source 映射、provenance、问题项与历史 receipts；build/review validators 均确认旧证据失效。工作树在 b25 提交后干净。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 26 页；新 attempt `820c4c17-8fe4-4e4c-9f44-fdabc66c25b7`。四个 review 工作项均绑定当前 attempt；候选页待读取工作项后登记。
- 修改文件：本进度文件；河北卷 build receipt/PDF；忽略目录 `.work/phase2-b26/review/` 下四个工作项。未修改题目源文件或 provenance。
- 已完成子阶段：四版接触表逐页复核全部 26 页，无可见缺字、遮挡、裁切或分页异常；试题版、解析版、简答版、印刷版第 1 页及 4 个候选页（试题 p.2、解析 p.11、简答 p.2、印刷 p.6）共 8 页高分辨率复核，无视觉缺陷。
- 已完成子阶段：四个当前 attempt 工作项已登记 26 页、208 项检查全部 pass；`finalize-batch` 返回 `FINALIZED：phase2-b26`，生成批次报告并事务性更新回执与 manifest。
- 修改文件：本进度文件；河北卷 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b26.md`；忽略目录 `.work/phase2-b26/review/` 四个工作项；临时复核图位于 `/tmp/gk-phase2-b26-review.dHJekq/`。
- 已完成子阶段：删除河北卷 `build/` 下所有非 PDF 中间物，保留四版 PDF；清理本批 `.work/phase2-b26` 与临时复核图。
- 已完成子阶段：source manifest 校验（`--require-artifacts 775`）、build receipt `OK：1 卷`、review `FINALIZED：phase2-b26`、provenance `OK：1 卷`，全部退出码 0。
- 已完成子阶段：`report.py render --all` 通过，以单个 content 事务写入并回读校验六个全量报告目标。
- 已完成子阶段：全量报告 `check --all` 通过，确认报告与全量 manifest 当前一致，并保留未完成状态；manifest revision 3827，来源 775、试卷 272、批次 138；批次状态 closed 49、closed_with_blockers 13、compiled_pending_review 74、provenance_verified 2；试卷状态 complete 86、blocked 45、compiled 137、editions_generated 4。
- 最终核对：`git diff --check` 通过；河北卷构建目录仅保留四份 PDF；11 个受本批事务影响的 tracked 文件为卷回执、批次/全量报告投影、manifest 与进度文件，无题目源文件或 provenance 改动。
- 待完成：提交本批；后续按时间顺序进入 `phase2-b27`（1977 内蒙古文科）预检。
- 下一步：提交当前已验收改动，不 push。

## 最近一次全库状态快照

来自 1977 河北卷 finalize 后的当前 `source-manifest.json`（每次恢复须刷新）：

- 来源 775；试卷 272；批次 138。
- 批次状态：closed 49、closed_with_blockers 13、compiled_pending_review 74、provenance_verified 2。
- 试卷状态：complete 86、blocked 45、compiled 137、editions_generated 4。
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
- `phase2-b23`（1977 上海文理卷）已于 `3477d184` 提交。
- `phase2-b24`（1977 北京文理卷）已于 `b59a82f9` 提交。
- `phase2-b25`（1977 天津卷）已于 `d0ae344e` 提交。
- `phase2-b26`（1977 河北卷）已完成 formal build、26 页视觉复核、finalize、scoped gates 和全量报告检查；本批待提交。
- 下一批按时间顺序为 `phase2-b27`（1977 内蒙古文科，1 卷，`compiled_pending_review`）。
- 继续前刷新 manifest 与 Git 状态；每完成一个批次阶段，更新本文件、运行对应 scoped gates 与全量报告检查，再单批提交。

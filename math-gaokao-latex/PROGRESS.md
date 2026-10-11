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

上述批次的提交在当前工作树中可由 `git log` 查证；不代表 1952—2006 或整个题库已完成。

## 最近完成阶段

### `phase1-b13` — 1956 全国卷（待本阶段提交）

- 已完成：formal build；四版共 21 页逐页视觉检查；试题版第 1 页、解析版第 1 页、简答版第 1 页、印刷版第 5 页高分辨率复核；未发现视觉缺陷；`finalize-batch` 返回 `FINALIZED`。
- 已完成：清理 `1956_全国卷/build/` 的非 PDF 编译中间物，仅保留四个 PDF；删除本批 `.work/` 和本次临时 PNG。
- 已完成：全量报告重新渲染（content transaction）。
- 修改文件：1956 build/review receipts、`source-manifest.json`、`reports/phase1-b13.md`；以及 renderer 管理的 `README_数学.md`、`math-gaokao-2017-2026/README.md`、`math-gaokao-latex/README.md`、`reports/baseline.md`、`report.md`、`docs/source-inventory.md`；另含本进度文件和收尾计划。
- 验证：`source_manifest.py validate --require-artifacts 775`、该批 `build_projects.py validate-receipts --require-final`、`review_receipts.py check-batch`、`provenance.py check-batch`、`report.py check --all` 均通过；`git diff --check` 通过。构建目录检查确认仅有四个 PDF，本批 `.work/` 与临时 PNG 路径均已清理。
- 提交状态：尚未提交；下一步先审阅精确 staged diff，再将本批及进度记录作为一个提交，不 push。

## 最近一次全库状态快照

来自 1956 finalize 后的当前 `source-manifest.json`（每次恢复须刷新）：

- 来源 775；试卷 272；批次 138。
- 批次状态：closed 36、closed_with_blockers 13、compiled_pending_review 87、provenance_verified 2。
- 试卷状态：complete 71、blocked 45、compiled 152、editions_generated 4。
- 这说明仍有大量待复核/阻塞工作；这些数字是进度快照，不是验收目标，也不应伪装成已完成。

## 最近验证与已知问题

- 1956 本批次视觉复核：21 页全页接触表检查；试题版第 1 页、解析版第 1 页、简答版第 1 页、印刷版第 5 页高分辨率复核；试卷中的 TikZ 几何图在接触表中可见。
- 本阶段验证输出：source manifest `OK：1 卷`；build receipts `FINALIZED：phase1-b13`；review receipt `OK：1 卷`；provenance `OK：1 卷`；全量报告与 manifest 当前一致。
- 全套单元测试最近一次：862 tests，848 passed、13 skipped、1 failed。唯一失败为 `tests/test_provenance.py::LiveRepositoryTests::test_the_cached_states_match_the_recomputed_ones`，全库旧缓存状态与现场派生不一致（首次报告共 297 项）。未解决前不得声称全库测试通过；按批次正式刷新回执与复核，不手工批量改状态。
- 分支不 push；提交前核对 branch/worktree，当前 canonical worktree 是 `仓库根`。

## 下一步

- 完成本阶段精确 diff 审阅并提交 1956 批次与进度/计划文件。
- 然后按时间顺序接手 `phase1-b14`（1957 全国卷；manifest 当前标记 `compiled_pending_review`）：先检查已有构建、回执和工作项，只执行尚缺的复核/收尾，不重复转录或构建。
- 继续前刷新 manifest 与 Git 状态；每完成一个批次阶段，更新本文件、运行对应 scoped gates 与全量报告检查，再单批提交。

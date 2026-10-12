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
| `phase2-b26` | 1977 河北卷 | 四版 26 页逐页复核、4 个候选页及首面高分辨率复核；0 警告；FINALIZED；四项门禁与全量报告检查通过；构建目录仅保留 PDF | `c42fa4d6` |
| `phase2-b27` | 1977 内蒙古文科 | 四版 20 页逐页复核、13 个首面/候选/问题关联页高分辨率复核；0 警告；FINALIZED；保留两个 open 内容 blocker；四项门禁与全量报告检查通过 | `d2124e2a` |
| `phase2-b28` | 1977 江苏卷 | 四版 23 页逐页复核、16 个首面/候选/问题关联页高分辨率复核；0 警告；FINALIZED；保留两个 open 内容 blocker；四项门禁与全量报告检查通过 | `8867a327` |
| `phase2-b29` | 1977 福建文科 | 四版 28 页逐页复核、11 个高分辨率页面复核；224 项检查通过；FINALIZED with blockers；全量报告检查通过 | `aeacb7cd` |
| `phase2-b30` | 1977 福建理科 | 四版 33 页逐页复核、13 个高分辨率页面复核；264 项检查通过；FINALIZED with blockers；全量报告检查通过 | `984a2bde` |
| `phase2-b31` | 1977 内蒙古理科 | 四版 28 页逐页复核、6 个首页/候选页高分辨率复核；224 项检查通过；FINALIZED；全量报告检查通过 | `315a56e7` |
| `phase2-b32` | 1977 河南卷 | 四版 32 页逐页复核、9 个首页/候选页高分辨率复核；256 项检查通过；FINALIZED；全量报告检查通过 | `1a5c5fd1` |

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

## 最近完成阶段

### `phase2-b26` — 1977 河北卷（已提交 `c42fa4d6`）

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
- 提交状态：已提交 `c42fa4d6`，未 push。

## 最近完成阶段

### `phase2-b27` — 1977 内蒙古文科（已提交 `d2124e2a`）

- 既有状态：单卷、4 题 provenance 已登记；`ISSUE-0129/0130` 是该卷两个尚未解决的答案冲突，涉及第 1 题根式底数与第 2 题圆台面积末值。按既有证据保留题面与源解答，不改写数字或结论；本批应如实以 blocker 关闭。
- 历史回执：旧 build 四版成功，页数 2/9/3/6，共 20 页；因生成输入树和工具链指纹变化而失效。旧 review 已通过但绑定不同 build attempt，不可复用。
- 已完成子阶段：核对 batch、来源映射、provenance、问题项与历史 receipts；provenance 无题目证据错误，仅 batch 派生缓存尚未刷新；build/review validators 确认需重建与重审。manifest 当前显示 production_state `blocked`，issue IDs 均 open。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 20 页；新 attempt `94665937-62be-4355-9042-0d916d2dd275`。四个 review 工作项均绑定该 attempt；候选页为试题 p.2、解析 p.6、简答 p.2、印刷 p.5。
- 修改文件：本进度文件；内蒙古文科 build receipt/PDF；忽略目录 `.work/phase2-b27/review/` 四个工作项。未修改题目源、答案、provenance 或 blocker 内容。
- 已完成子阶段：四版接触表逐页复核全部 20 页，无可见缺字、遮挡、裁切或分页异常；四版首面、4 个候选页（试题 p.2、解析 p.6、简答 p.2、印刷 p.5）及争议关联页共 13 页高分辨率复核。`ISSUE-0129/0130` 的题面、源解答及并列说明呈现完整清楚；未发现视觉问题。
- 修改文件：本进度文件；内蒙古文科 build receipt/PDF；忽略目录 `.work/phase2-b27/review/` 四个工作项；临时复核图位于 `/tmp/gk-phase2-b27-review.oxxPwC/`。
- 已完成子阶段：4 个工作项登记 20 页、160 项检查全部 pass；`finalize-batch` 返回 `FINALIZED：phase2-b27`。`ISSUE-0129/0130` 仍 open，批次按内容 blocker 如实关闭。
- 修改文件：本进度文件；内蒙古文科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b27.md`；忽略目录 `.work/phase2-b27/review/` 四个工作项；临时复核图位于 `/tmp/gk-phase2-b27-review.oxxPwC/`。
- 已完成子阶段：清除内蒙古文科 `build/` 下非 PDF 中间物，保留四版 PDF；清理本批 `.work/phase2-b27` 与临时复核图。
- 已完成子阶段：source manifest 校验（`--require-artifacts 775`）、build receipt `OK：1 卷`、review `FINALIZED：phase2-b27`、provenance `OK：1 卷`，全部退出码 0；两个内容 issue 仍保持 open。
- 已完成子阶段：`report.py render --all` 通过，以单个 content 事务写入并回读校验六个全量报告目标。
- 已完成子阶段：全量报告 `check --all` 通过；manifest revision 3830，来源 775、试卷 272、批次 138；批次状态 closed 49、closed_with_blockers 14、compiled_pending_review 73、provenance_verified 2；试卷状态 complete 86、blocked 45、compiled 137、editions_generated 4。该卷 production_state 保持 blocked，`ISSUE-0129/0130` 未解决。
- 最终核对：`git diff --check` 通过；内蒙古文科 build 目录仅四份 PDF；11 个受本批事务影响的 tracked 文件为回执、批次/全量报告投影、manifest 与进度文件，未更改争议题面、答案或 provenance。
- 提交状态：已提交 `d2124e2a`，未 push。

## 最近完成阶段

### `phase2-b28` — 1977 江苏卷（已提交 `8867a327`）

- 既有状态：单卷、6 题 provenance 已登记；`ISSUE-0131/0132` 为两条仍开放的内容 blocker，分别涉及第 1 题负数负半次幂及附加题极限变量不一致。按现有证据保留原式，不擅改为可计算表达式；最终须保留 blocker。
- 历史回执：旧 build 四版成功，页数 2/10/3/8，共 23 页；生成输入树与工具链指纹变化使其失效。旧 review passed 但绑定另一 build attempt，不可复用。
- 已完成子阶段：核对 batch、来源映射、6 题 provenance、问题项与历史 receipts；provenance 无题目证据错误，仅 batch 派生缓存未刷新；build/review validators 确认需重建重审。当前 production_state `blocked`，两个 issue 均 open。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 23 页；新 attempt `c8df220c-6960-437d-b7d1-52dbe9d458b9`。四个 review 工作项绑定当前 attempt；候选页为试题 p.2、解析 p.7、简答 p.2、印刷 p.7。
- 修改文件：本进度文件；江苏卷 build receipt/PDF；忽略目录 `.work/phase2-b28/review/` 四个工作项。未改题目源、答案、provenance 或 blockers。
- 已完成子阶段：四版接触表逐页复核全部 23 页，无可见缺字、遮挡、裁切或分页异常；四版首面、4 个候选页（试题 p.2、解析 p.7、简答 p.2、印刷 p.7）及 `ISSUE-0131/0132` 关联页共 16 页高分辨率复核，无视觉缺陷。两个疑义均在内容说明中标明待核证，不改原式。
- 修改文件：本进度文件；江苏卷 build receipt/PDF；忽略目录 `.work/phase2-b28/review/` 四个工作项；临时复核图位于 `/tmp/gk-phase2-b28-review.3ArlXA/`。
- 已完成子阶段：4 个工作项登记全部 23 页、184 项检查为 pass；`finalize-batch` 返回 `FINALIZED：phase2-b28`。`ISSUE-0131/0132` 仍 open，批次按 blocker 状态关闭。
- 修改文件：本进度文件；江苏卷 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b28.md`；忽略目录 `.work/phase2-b28/review/` 四个工作项；临时复核图位于 `/tmp/gk-phase2-b28-review.3ArlXA/`。
- 已完成子阶段：清除江苏卷 `build/` 下全部非 PDF 中间物，保留四版 PDF；清理本批 `.work/phase2-b28` 与临时复核图。
- 已完成子阶段：source manifest 校验（`--require-artifacts 775`）、build receipt `OK：1 卷`、review `FINALIZED：phase2-b28`、provenance `OK：1 卷`，全部退出码 0；`ISSUE-0131/0132` 保持 open。
- 已完成子阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`check --all` 确认报告与全量 manifest 当前一致，未完成状态如实保留。
- 已完成子阶段：manifest revision 3833，来源 775、试卷 272、批次 138；批次状态 closed 49、closed_with_blockers 15、compiled_pending_review 72、provenance_verified 2；试卷状态 complete 86、blocked 45、compiled 137、editions_generated 4。江苏卷仍为 blocked，`ISSUE-0131/0132` 未解决。
- 最终核对：`git diff --check` 通过；江苏卷 build 目录仅四份 PDF；11 个受本批事务影响的 tracked 文件为回执、批次/全量报告投影、manifest 与进度文件，未修改争议题面、答案、provenance 或 issue 内容。
- 提交状态：已提交 `8867a327`，未 push。

## 最近完成阶段

### `phase2-b29` — 1977 福建文科（已提交 `aeacb7cd`）

- 既有状态：单卷、6 题 provenance；`ISSUE-0133/0134/0135/0136` 为四条 open 内容 blocker，涉及第 3 题产量条件不足、第 4 题“切线”对象不明、第 5 题参数/角度单位疑义、第 6 题角度与图示矛盾。`ISSUE-0798` 已 resolved（第 2 题根式转录已修正并验证）。
- 历史回执：旧 build 四版成功，页数 3/12/4/9，共 28 页；因生成输入树与工具链指纹变化失效。旧 review passed 但绑定另一 attempt，不可复用。
- 已完成子阶段：核对 batch、来源映射、6 题 provenance、5 条 issue 状态及历史 receipts；provenance 未报题目证据错误，仅 batch 派生缓存未刷新；build/review validators 确认需重建重审。当前 production_state `blocked`。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 28 页；新 attempt `79c9598b-8055-4ba5-a85d-64e8128c21f8`。四个 review 工作项绑定当前 attempt；候选页为试题 p.1、解析 p.12、简答 p.4、印刷 p.8。
- 修改文件：本进度文件；福建文科 build receipt/PDF；忽略目录 `.work/phase2-b29/review/` 四个工作项。未修改题目源、答案、provenance 或 blocker 内容。
- 已完成子阶段：四版接触表逐页检查 28 页；四版首页、4 个自动候选页及 `ISSUE-0133/0134/0135/0136` 关联页共 11 页高分辨率复核，未发现缺字、遮挡、裁切或分页异常。争议页上的源题与待核说明完整可读，四项内容 blocker 保持不变。
- 修改文件：本进度文件；临时复核图位于 `/tmp/gk-phase2-b29-review.77R2vE/`。未改题目源、答案、provenance 或 issue 状态。
- 已完成子阶段：四个当前 attempt work item 已登记 28 页、224 项检查全部 pass，逐项 note 非空；`finalize-batch` 返回 `FINALIZED`，批次状态 `closed_with_blockers`，manifest revision 3836。finalize 前旧 review receipt 因绑定旧 build 被判 stale，事务成功后已刷新。
- 修改文件：本进度文件；福建文科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b29.md`；忽略目录 `.work/phase2-b29/review/` 四个 work item；临时复核图位于 `/tmp/gk-phase2-b29-review.77R2vE/`。
- 已完成子阶段：福建文科 `build/` 清除全部非 PDF 文件，仅保留四版 PDF；本批 `.work/phase2-b29` 与临时复核图清理完毕。
- 已完成子阶段：source manifest（775 项）、build receipt（1 卷 current/final）、review receipt（FINALIZED）、provenance（1 卷）scoped gates 全部退出码 0；`report.py render --all` 与 `check --all` 通过，全量报告确认与 manifest 一致并保留未完成状态；`git diff --check` 通过。
- 修改文件：福建文科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b29.md`；本进度文件；renderer 管理的全量投影 `README_数学.md`、`math-gaokao-2017-2026/README.md`、本项目 `README.md`、`reports/baseline.md`、`report.md`、`docs/source-inventory.md`。未修改题目源、答案、provenance 或四条 issue 内容。
- 验证快照：manifest revision 3836；来源 775、试卷 272、批次 138；批次 closed 49、closed_with_blockers 16、compiled_pending_review 71、provenance_verified 2；试卷 complete 86、blocked 45、compiled 137、editions_generated 4。福建文科仍 blocked，`ISSUE-0133/0134/0135/0136` 均 open。
- 提交状态：已提交 `aeacb7cd`，未 push；提交后工作树干净。

## 最近完成阶段

### `phase2-b30` — 1977 福建理科（已提交 `984a2bde`）

- 预检完成：单卷、7 题 provenance 已登记；`ISSUE-0137/0138/0139` 为 open 内容 blocker，分别涉及第 5 题几何角度与图示不相容、第 6 题参数形式/角度单位疑义、第 7 题数列前 n 项和与三次多项式条件矛盾；`ISSUE-0799` 已 resolved（第 1 题根式已由固定 PDF 与独立版本确认并修正）。
- 历史回执：四版 PDF 仍存在，旧页数为 3/14/4/12，共 33 页；build 因生成输入树和工具链指纹变化而 stale，review 绑定旧 build attempt 也 stale；候选页需从正式新工作项重新确认。
- 已完成子阶段：provenance 检查未发现题目证据错误，仅提示 batch 派生缓存 `compiled_pending_review` 与现场 `provenance_verified` 不一致；build validator 显示 1 卷 stale、0 失败；review validator 显示 build stale。无需重做已有转录/解题，先保留三个 open 内容 blocker。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 33 页；新 attempt `00d2652f-2fcf-4403-8675-7c1393829a39`。四个 review 工作项绑定当前 attempt；候选页为试题 p.3、解析 p.12、简答 p.4、印刷 p.9。
- 修改文件：本进度文件；福建理科 build receipt/PDF；忽略目录 `.work/phase2-b30/review/` 四个工作项。未修改题目源、答案、provenance 或 blocker 内容。
- 已完成子阶段：四版接触表逐页检查 33 页；四版首页、候选页及 `ISSUE-0137/0138/0139` 关联页共 13 个不同页面高分辨率复核，无缺字、遮挡、裁切或分页异常。三项内容疑义在题面与解析中的展示完整清晰，均保持原样。
- 修改文件：本进度文件；临时复核图位于 `/tmp/gk-phase2-b30-review.LQZtf6/`。未改题目源、答案、provenance 或 issue 状态。
- 已完成子阶段：四个当前 attempt work item 登记 33 页、264 项检查全部 pass 且 note 非空；`finalize-batch` 返回 `FINALIZED`，批次 `closed_with_blockers`，manifest revision 3839。finalize 前旧 review receipt 因绑定旧 build 而 stale，事务后已刷新。
- 修改文件：本进度文件；福建理科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b30.md`；忽略目录 `.work/phase2-b30/review/` 四个 work item；临时复核图位于 `/tmp/gk-phase2-b30-review.LQZtf6/`。
- 已完成子阶段：清除福建理科 `build/` 下所有非 PDF 文件，保留四份 PDF；清理本批 `.work/phase2-b30` 与临时复核图。
- 已完成子阶段：source manifest（775 项）、build receipt（1 卷 current/final）、review receipt（FINALIZED）、provenance（1 卷）scoped gates 全部退出码 0；`report.py render --all` 与 `check --all` 通过，报告与 manifest 一致且保留未完成状态；`git diff --check` 通过。
- 修改文件：福建理科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b30.md`；本进度文件；renderer 管理的全量投影 `README_数学.md`、`math-gaokao-2017-2026/README.md`、本项目 `README.md`、`reports/baseline.md`、`report.md`、`docs/source-inventory.md`。未修改题目源、答案、provenance 或三条 open issue 内容。
- 验证快照：manifest revision 3839；来源 775、试卷 272、批次 138；批次 closed 49、closed_with_blockers 17、compiled_pending_review 70、provenance_verified 2；试卷 complete 86、blocked 45、compiled 137、editions_generated 4。福建理科仍 blocked；`ISSUE-0137/0138/0139` open，`ISSUE-0799` resolved。
- 提交状态：已提交 `984a2bde`，未 push；提交后工作树干净。

## 最近完成阶段

### `phase2-b31` — 1977 内蒙古理科（已提交 `315a56e7`）

- 预检完成：单卷、6 题 provenance 已登记，`issue_ids=[]`，无需重做转录或解题。
- 历史回执：四版旧 build 均成功、页数 3/12/4/9，共 28 页；因生成输入树和工具链指纹变化 stale，旧 review 虽 passed 但绑定不同 build attempt，不可复用。旧 PDF 仍在。
- 已完成子阶段：provenance 检查未发现题目证据错误，只提示 paper 派生缓存 `compiled` 与现场 `editions_generated` 不一致、batch `compiled_pending_review` 与 `provenance_verified` 不一致；build validator 显示 1 卷 stale、0 失败；review validator 显示 build stale。
- 修改文件：本进度文件；尚未修改内蒙古理科题目源、答案、provenance 或 issue 内容。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 28 页；新 attempt `1275e3a8-febe-4b1a-9f9a-8b72febd46d3`。四个 review 工作项绑定当前 attempt；候选页为试题 p.1、解析 p.12、简答 p.1、印刷 p.6。
- 修改文件：本进度文件；内蒙古理科 build receipt/PDF；忽略目录 `.work/phase2-b31/review/` 四个工作项。未修改题目源、答案或 provenance。
- 已完成子阶段：四版接触表逐页检查 28 页；四版首页及自动候选页共 6 个不同页面高分辨率复核，无缺字、遮挡、裁切或分页异常。
- 修改文件：本进度文件；临时复核图位于 `/tmp/gk-phase2-b31-review.D32br4/`。未修改题目源、答案、provenance 或 issue 内容。
- 已完成子阶段：四个当前 attempt work item 登记 28 页、224 项检查全部 pass 且 note 非空；`finalize-batch` 返回 `FINALIZED`，批次状态 `closed`，manifest revision 3842。finalize 前历史 review 因绑定旧 build 而 stale，事务后已刷新。
- 修改文件：本进度文件；内蒙古理科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b31.md`；忽略目录 `.work/phase2-b31/review/` 四个 work item；临时复核图位于 `/tmp/gk-phase2-b31-review.D32br4/`。
- 已完成子阶段：清除内蒙古理科 `build/` 下所有非 PDF 文件，保留四份 PDF；清理本批 `.work/phase2-b31` 与临时复核图。
- 已完成子阶段：source manifest（775 项）、build receipt（1 卷 current/final）、review receipt（FINALIZED）、provenance（1 卷）scoped gates 全部退出码 0；`report.py render --all` 与 `check --all` 通过，报告与 manifest 一致且保留未完成状态；`git diff --check` 通过。
- 修改文件：内蒙古理科 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b31.md`；本进度文件；renderer 管理的全量投影 `README_数学.md`、`math-gaokao-2017-2026/README.md`、本项目 `README.md`、`reports/baseline.md`、`report.md`、`docs/source-inventory.md`。未修改题目源、答案或 provenance。
- 验证快照：manifest revision 3842；来源 775、试卷 272、批次 138；批次 closed 50、closed_with_blockers 17、compiled_pending_review 69、provenance_verified 2；试卷 complete 87、blocked 45、compiled 136、editions_generated 4。内蒙古理科无 issue，production state `complete`。
- 提交状态：已提交 `315a56e7`，未 push；提交后工作树干净。

## 最近完成阶段

### `phase2-b32` — 1977 河南卷（已提交 `1a5c5fd1`）

- 预检完成：单卷、10 题 provenance 已登记；`ISSUE-0140` 至 `ISSUE-0149` 全部为 resolved，旧有题目与解答成果可复用。
- 历史回执：四版旧 build 成功，页数 3/14/4/11，共 32 页；因生成输入树和工具链指纹变化 stale。旧 review passed 但绑定不同 build attempt，不可复用；四份旧 PDF 仍在。
- 已完成子阶段：provenance 检查未发现题目证据错误，仅报告 paper/batch 派生缓存状态不一致；build validator 显示 1 卷 stale、0 失败；review validator 显示 build stale。
- 修改文件：本进度文件；尚未修改河南卷题目源、答案、provenance 或 issue 内容。
- 已完成子阶段：formal build 四版成功、0 失败、0 警告，共 32 页；新 attempt `37072bea-5dbb-496f-9f0c-9e2d0342d554`。四个 review 工作项绑定当前 attempt；候选页为试题 p.2、解析 p.12、简答 p.2、印刷 p.9。
- 修改文件：本进度文件；河南卷 build receipt/PDF；忽略目录 `.work/phase2-b32/review/` 四个工作项。未修改题目源、答案或 provenance。
- 已完成子阶段：四版接触表逐页检查 32 页；四版首页与自动候选页共 9 个不同页面高分辨率复核，无缺字、遮挡、裁切或分页异常。既有 `ISSUE-0140`—`ISSUE-0149` 均 resolved，相关页面说明完整。
- 修改文件：本进度文件；临时复核图位于 `/tmp/gk-phase2-b32-review.l26pFP/`。未修改题目源、答案、provenance 或 issue 内容。
- 已完成子阶段：四个当前 attempt work item 登记 32 页、256 项检查全部 pass 且 note 非空；`finalize-batch` 返回 `FINALIZED`，批次状态 `closed`，manifest revision 3845。finalize 前历史 review 因绑定旧 build 而 stale，事务后已刷新。
- 修改文件：本进度文件；河南卷 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b32.md`；忽略目录 `.work/phase2-b32/review/` 四个 work item；临时复核图位于 `/tmp/gk-phase2-b32-review.l26pFP/`。
- 已完成子阶段：清除河南卷 `build/` 下所有非 PDF 文件，保留四份 PDF；清理本批 `.work/phase2-b32` 与临时复核图。
- 已完成子阶段：source manifest（775 项）、build receipt（1 卷 current/final）、review receipt（FINALIZED）、provenance（1 卷）scoped gates 全部退出码 0；`report.py render --all` 与 `check --all` 通过，报告与 manifest 一致且保留未完成状态；`git diff --check` 通过。
- 修改文件：河南卷 build/review receipts 与 PDF；`source-manifest.json`；`reports/phase2-b32.md`；本进度文件；renderer 管理的全量投影 `README_数学.md`、`math-gaokao-2017-2026/README.md`、本项目 `README.md`、`reports/baseline.md`、`report.md`、`docs/source-inventory.md`。未修改题目源、答案、provenance 或 10 条 resolved issue 内容。
- 验证快照：manifest revision 3845；来源 775、试卷 272、批次 138；批次 closed 51、closed_with_blockers 17、compiled_pending_review 68、provenance_verified 2；试卷 complete 88、blocked 45、compiled 135、editions_generated 4。河南卷 production state `complete`，`ISSUE-0140`—`ISSUE-0149` 均 resolved。
- 提交状态：已提交 `1a5c5fd1`，未 push；提交后工作树干净。

## 最近批次进展

### `phase2-b33` — 1977 黑龙江、 西藏、青海、广西百色文科

- 预检完成：4 卷合计 32 题 provenance 已登记；相关 `ISSUE-0150`—`ISSUE-0181` 共 32 条全部 resolved，无 open blocker。
- 历史回执：四卷旧 build 均因生成输入树和工具链指纹变化 stale，旧 review 绑定旧 build attempt，不可复用。历史页数分别为黑龙江 2/11/3/8（24 页）、西藏 2/10/3/7（22 页）、青海 3/13/4/10（30 页）、广西百色文科 2/10/3/6（21 页），合计 97 页。
- 已完成子阶段：provenance 仅提示 paper/batch 派生缓存状态需刷新；build validator 显示 4 卷 stale、0 失败；review validator 显示四卷 build stale。可复用既有转录/解题与已解决 issue 结论。
- 已完成子阶段：formal build 四卷四版均成功、0 失败、0 警告，共 97 页（黑龙江 24、西藏 22、青海 30、广西百色文科 21）；16 个 review 工作项绑定当前 attempts，候选页已更新。四卷四版 97 页接触表和 23 张首页/候选页 120dpi 图像均已视觉检查，未见裁切、重叠、字形缺失或明显版面异常。已逐项登记 97 页 × 8 项共 776 项非空 pass 检查；`finalize-batch` 返回 `FINALIZED`、batch status `closed`，报告生成，manifest revision 3848。
- 修改文件：本进度文件；四卷 build/review receipts 与 PDF；`source-manifest.json` 及生成的报告/清单投影；`reports/phase2-b33.md`；忽略目录 `.work/phase2-b33/review/` 下 16 个工作项。未修改题目源、答案、provenance 或 issue 内容。
- 已完成子阶段：四卷 `build/` 各仅保留 4 份 PDF；已删除本批 `.work/phase2-b33/`（16 份已登记工作项）及 136 张临时 PNG。
- 修改文件：本进度文件；四卷回执/PDF、manifest 与报告投影；批次报告。清理未触及其他批次或源文件。
- 已完成子阶段：source manifest 校验通过（775 artifacts）；build receipts `OK`（4 succeeded、0 stale/invalid/missing/failed）；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：全量 `report.py render --all` 成功，以一个 content 事务写入并回读校验六个全量报告目标；`check --all` 成功，报告与当前 manifest 一致且保留未完成状态。
- 已完成子阶段：`git diff --check` 通过；审阅确认 17 个 tracked 文件均为本批 receipts、manifest 驱动报告/README 投影及进度文件，没有题目源、答案或 provenance 改动。四卷各保留 4 份 PDF。
- 已完成阶段：本批已单批提交 `c80bc829`，进度记录提交为 `272c5187`；未 push。下一步转入 b34 预检。

### `phase2-b34` — 1977 山西、新疆理科、甘肃、浙江

- 预检完成：4 卷共 33 条既有 issue（`ISSUE-0182`—`ISSUE-0214`），逐条确认均 resolved；现有 provenance 与题目源可复用。
- 历史产物：四卷旧 PDF 页数依次为山西 31、新疆理科 24、甘肃 31、浙江 24，合计 110 页。build receipts 因生成输入树和工具链指纹变化 stale，review 绑定旧 build；provenance 的 compiled/批次缓存状态也随旧回执而 stale。
- 已完成子阶段：source manifest 验证通过（775 项）；旧构建 validator 报 4 卷 stale、0 failed，review 报 4 卷 build stale；无来源/答案改动需求。已 formal build 四卷四版，全部 succeeded，manifest revision 3850；新页数为 3/14/4/10、2/10/3/9、3/14/4/10、2/10/3/9，共 110 页。准备 16 个当前 attempt review work items。
- 构建警告：山西解析版 1 条 Overfull（`answers.tex` 第 377 行）；浙江解析版 1 条 Overfull（第 431 行）和 1 条 Underfull（第 442—443 行）。高分辨率检查解析版第 9、10 页后确认三条均无裁切、遮挡或缺字，将逐条登记为精确匹配当前日志的视觉通过豁免。
- 已完成子阶段：四卷四版 110 页接触表均已逐页目视检查，未见明显裁切、重叠或版面断裂；警告均落在解析版末页附近（第 10 页），需高分辨率复查后再判定。
- 修改文件：本进度文件；四卷 build receipts/PDF；`source-manifest.json`；忽略目录 `.work/phase2-b34/review/` 下 16 个工作项。未修改题目源、答案、provenance 或 issue。
- 已完成子阶段：完成 24 张首页/候选/警告页 120dpi 复核，并额外复核山西、浙江解析版第 9 页；未见视觉缺陷，三条日志 warning 均确认不影响可读性和页面边界。
- 已完成子阶段：16 份 work items 已登记 110 页 × 8 项共 880 项非空 pass 检查；三条 warning 均按当前日志 kind/box/width/lines、`answers.tex` 源路径和第 10 页逐项登记，视觉结果均为 pass。`finalize-batch` 返回 `FINALIZED`、状态 `closed`，无问题，报告已生成，manifest revision 3851。
- 修改文件：本进度文件；四卷 build/review receipts 与 PDF；`source-manifest.json` 和生成投影；`reports/phase2-b34.md`；忽略目录 `.work/phase2-b34/review/` 的 16 份 work items。未修改题目源、答案、provenance 或 issue 内容。
- 已完成子阶段：清理四卷 `build/` 内各 24 个非 PDF 编译中间物（每卷仅保留 4 份 PDF）、本批 16 个忽略 work items，以及临时复核目录中的 152 张 PNG；复查四卷各 4 PDF、0 非 PDF，work/temp 目标均已移除。
- 已完成子阶段：scoped gates 全部通过：source manifest 775 artifacts；build receipts 4 succeeded、0 stale/invalid/missing/failed；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与全量 manifest 一致并保留未完成状态。
- 已完成子阶段：`git diff --check` 通过；最终 diff 共 17 个 tracked 文件，仅含四卷 build/review receipts、manifest 驱动的 6 个报告/README 投影、本批报告与进度记录，无题目源、答案或 provenance 改动。
- 验证快照：manifest revision 3851；来源 775、试卷 272、批次 138；批次状态 closed 53、closed_with_blockers 17、compiled_pending_review 66、provenance_verified 2。该快照反映 b34 finalize 后的阶段进度，不代表全库完成。
- 已完成阶段：b34 内容与报告投影已提交为 `751b88d6`；不 push。
- 待完成：预检并继续推进 manifest 顺序中的 b35。
- 下一步：核查 b35 四卷的来源/provenance、issue、旧构建与复核回执，确定可复用内容和需更新门禁。

## 最近一次全库状态快照

来自 b35 finalize 后的当前 `source-manifest.json`，revision 3854（每次恢复须刷新）：

- 来源 775；试卷 272；批次 138。
- 批次状态：closed 54、closed_with_blockers 17、compiled_pending_review 65、provenance_verified 2。
- 试卷状态：complete 100、blocked 45、compiled 123、editions_generated 4。
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
- `phase2-b26`（1977 河北卷）已于 `c42fa4d6` 提交。
- `phase2-b27`（1977 内蒙古文科）已于 `d2124e2a` 提交；两条答案冲突保留为 blocker。
- `phase2-b28`（1977 江苏卷）已于 `8867a327` 提交；两个题面疑义保留为 blocker。
- `phase2-b29`（1977 福建文科）已于 `aeacb7cd` 提交；四个内容 blocker 保持 open。
- `phase2-b30`（1977 福建理科）已于 `984a2bde` 提交；三个内容 blocker 保持 open。
- `phase2-b31`（1977 内蒙古理科）已于 `315a56e7` 提交；该卷无内容 issue。
- `phase2-b32`（1977 河南卷）已于 `1a5c5fd1` 提交；10 条历史 issue 均 resolved。
- `phase2-b33`（1977 黑龙江、西藏、青海、广西百色文科四卷）已于 `c80bc829` 提交；32 条历史 issue 均 resolved，97 页/776 项复核通过。
- `phase2-b34`（1977 山西、新疆理科、甘肃、浙江四卷）已于 `751b88d6` 提交；110 页/880 项复核通过，三条版面 warning 已精确豁免，manifest 状态 `closed`。
- `phase2-b35`（1977 安徽理科、安徽文科、广东、四川四卷）已于 `ac60c0fe` 提交；132 页/1056 项复核通过、0 warning，manifest 状态 `closed`，未 push。
- 下一批按 manifest 顺序为 `phase2-b36`：1977 云南、贵州、广西文科、广西理科四卷，当前状态 `compiled_pending_review`。
- 继续前刷新 manifest 与 Git 状态；每完成一个批次阶段，更新本文件、运行对应 scoped gates 与全量报告检查，再单批提交。

### `phase2-b35` — 1977 安徽理科、安徽文科、广东、四川

- 预检完成：四卷关联 37 条 issue（`ISSUE-0215`—`ISSUE-0245`、`ISSUE-0271`—`ISSUE-0276`）均为 resolved；source manifest 校验通过（775 artifacts）。
- 已有内容：四卷 `provenance.json` 共 31 题，逐题转录复核均 passed、答案证据均 A、无冲突、无未解决 provenance issue；按既有核查成果复用，不重做转录/解题。既有 PDF 页数依次为安徽理科 43、安徽文科 25、广东 30、四川 34 页，共 132 页。
- 旧构建：四卷均有四版 PDF；build receipts 均 stale（生成输入树、工具链指纹变化），review receipts 随 build stale。`provenance.py check-batch` 仅报缓存 production 状态 `compiled` 与现场派生 `editions_generated` 不符（四卷），以及 batch 缓存 `compiled_pending_review` 与现场派生 `provenance_verified` 不符；provenance status 输出四卷 `editions_generated`、批次 `provenance_verified`。无需改来源、题目或答案；正式构建/事务 finalize 后刷新派生缓存。
- 已完成子阶段：formal build 四卷四版成功，manifest revision 3853；页数分别为安徽理科 4/19/5/15（43）、安徽文科 2/11/3/9（25）、广东 3/13/4/10（30）、四川 3/15/4/12（34），共 132 页，四卷均 0 warning。Build attempts：`26b7a80b-4b7b-4953-ab83-67db60a65fe6`、`3341aa58-134d-421f-b714-8de0ecf0dbd3`、`31663c9d-fb2d-4df9-ab0f-f8b356f370ed`、`0a1f1d25-3d40-4c8f-828a-66a83e18e467`。
- 修改文件：本进度文件；四卷 build receipts/PDF；`source-manifest.json`。题目源、答案与 provenance 未改。
- 已完成子阶段：`prepare-batch` 生成 16 个 review work items，覆盖四卷 × 四版，均绑定本轮 build attempts。
- 已完成子阶段：16 个版本接触表覆盖全部 132 页，已逐页检查；未见明显裁切、重叠、缺字或分页断裂。
- 已完成子阶段：按 16 个 work items 登记的候选页完成 120dpi 复核；包括安徽理科印刷版第 14 页、广东印刷版第 9 页、广东解析版第 4 页、四川解析版第 4 页、四川印刷版第 3 页及其余首页，共 16 页，均无可见版面缺陷。
- 已完成子阶段：16 个 work items 已登记 132 页 × 8 项共 1056 个带非空说明的 pass 检查；0 pending、0 non-pass，候选页 16 页全部高分辨率检查通过，工作项绑定 4 个当前 build attempts。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，状态 `closed`，无问题；`reports/phase2-b35.md` 已生成，manifest revision 3854。
- 已完成子阶段：清理四卷 `build/` 内各 24 个非 PDF 文件（每卷保留四份 PDF）、本批 16 个 work items 与临时目录 164 张 PNG；复查四卷各 4 PDF、0 非 PDF，work/temp 目录均已删除。
- 已完成子阶段：scoped gates 全部通过：source manifest 775 artifacts；build receipts 4 succeeded、0 stale/invalid/missing/failed；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标。
- 已完成子阶段：`report.py check --all` 确认报告投影与全量 manifest 一致，未完成状态已保留。
- 已完成子阶段：`git diff --check` 通过；最终 diff 共 17 个 tracked 文件，仅含四卷 build/review receipts、manifest 驱动的 6 个报告/README 投影、`reports/phase2-b35.md`、manifest 与进度记录，无题目源、答案或 provenance 改动。
- 验证快照：manifest revision 3854；来源 775、试卷 272、批次 138；批次 closed 54、closed_with_blockers 17、compiled_pending_review 65、provenance_verified 2；试卷 complete 100、blocked 45、compiled 123、editions_generated 4。此为阶段快照，不代表全库完成。
- 已完成阶段：b35 内容和报告投影已提交为 `ac60c0fe`；不 push。
- 待完成：预检并继续推进 manifest 顺序中的 b36。
- 下一步：核查 b36 四卷的来源/provenance、issue、旧构建与复核回执，确定可复用内容和需更新门禁。

### `phase2-b36` — 1977 云南、贵州、广西文科、广西理科

- 预检完成：四卷关联 25 条 issue（`ISSUE-0246`—`ISSUE-0270`）逐条确认均 resolved；source manifest 校验通过（775 artifacts）。
- 已有内容：四卷 `provenance.json` 共 25 题，逐题转录复核均 passed、答案证据均 A、无冲突、无未解决 provenance issue；复用已完成转录/核查，不重新处理内容。既有 PDF 四版页数分别为云南 10/4/12/3（29）、贵州 10/4/13/3（30）、广西文科 6/3/8/2（19）、广西理科 9/4/12/3（28），合计 106 页。
- 旧构建：四卷 build receipts 均因生成输入树与工具链指纹变化 stale，review receipts 随 build stale；provenance 缓存仍为 `compiled`/`compiled_pending_review`，现场派生为四卷 `editions_generated`、批次 `provenance_verified`。需正式构建并由事务刷新派生状态。
- 已完成子阶段：formal build 四卷四版成功，manifest revision 3856；云南 3/12/4/10（29 页）、贵州 3/13/4/10（30 页）、广西文科 2/8/3/6（19 页）、广西理科 3/12/4/9（28 页），合计 106 页。Build attempts：`dac709ac-f809-45ee-8b2a-0157ed33d58f`、`46ca254d-de9a-4d55-b015-50f914568693`、`3b0ba108-b399-4425-b365-1f2f3edb2900`、`93ccf863-4ed6-48f0-ad29-633051257127`。
- 构建警告：仅贵州卷出现 18 条 missing-character 警告（试题版 2、解析版 7、简答版 2、印刷版 7），字符为 `θ`、`α`、`ⁿ`，来自 `questions.tex`/`answers.tex` 的源注文本；尚未判定视觉影响，不予豁免。
- 修改文件：本进度文件；四卷 build receipts/PDF；`source-manifest.json`。未改题目源、答案或 provenance。
- 已完成子阶段：`prepare-batch` 生成 16 个 work items，覆盖四卷 × 四版并绑定本轮 build attempts。
- 已完成子阶段：16 个版本接触表覆盖全部 106 页并逐页检查；未见明显裁切、重叠或分页异常。贵州卷 18 条 missing-character warning 仍待页面级高分辨率确认。
- 已完成子阶段：16 个候选页与贵州 warning 关联页完成 120dpi 检查（共 20 个不同页码）；确认源注在四版均实际缺字：试题/简答/印刷版源注的 `θ` 消失，解析/印刷版源注的 `ⁿ` 与 `α` 消失。其他候选页无可见布局缺陷。
- 源注修复阶段：权威源 `1977_数学真题_贵州_试题.md`、`1977_数学真题_贵州_解析正文.md` 已将触发缺字的希腊字母、上标与函数记号改为等义 TeX 数学模式，题意、排印误植判断、解答和答案均未改变。正式生成器已同步更新合并解析与贵州卷 `questions.tex`/`answers.tex`；`generate_projects.py --check` 通过。独立盲核确认语义等价；另发现历史源注中 `²`/减号仍为普通字符，但当前构建无对应缺字 warning，故不纳入本次修复。
- 阶段修改文件：权威源 `1977/1977_数学真题_贵州_试题.md`、`1977/1977_数学真题_贵州_解析正文.md`；生成投影 `1977_数学真题_贵州_含解析.md`、贵州卷 `questions.tex`/`answers.tex`；四卷 provenance、`source-manifest.json` 与本进度文件。四卷 b36 旧 build receipts/PDF 仍在工作区，等待修复后正式重建。
- Provenance 子阶段：初次校验确认题面哈希因第 8 题题面块内源注排版变化而 stale（哈希覆盖整题块）；按已授权流程，用现存三角色核验内容重建 12 份忽略 `.work` 角色材料，仅刷新贵州第 8 题当前题面哈希与该题源注复核说明，其余来源/解题/盲核数据沿用已通过记录。`import-batch --write` 事务成功，manifest revision 3857；`check-batch` 返回 `OK：4 卷`，source manifest 校验通过。未绕过门禁。
- 待完成：按修复后的源码正式重建四卷；对最终 106 页重新逐页复核、登记 848 项检查并 finalize；清理非 PDF 构建产物及临时图；完成 scoped/full-report gates、最终 diff 审核并提交。
- formal build 子阶段：修复后正式重建四卷四版成功，manifest revision 3859；云南 29 页、贵州 30 页、广西文科 19 页、广西理科 28 页，共 106 页，四卷均无 missing-character、Overfull 或 Underfull warning。新 build attempts：云南 `0bd4a658-11d6-4856-b9df-0f62084e27d6`、贵州 `9ce3e900-cf42-408b-bb20-f7488230e48b`、广西文科 `ace0fa13-7ba1-4016-a736-1d68512a3fc5`、广西理科 `c14ae01a-5b94-48fb-9542-f1061eb5652d`。`validate-receipts --require-final` 当前返回 `PENDING_REVIEW`，无 failed/invalid/stale/missing receipt，符合待复核状态。
- 已完成子阶段：`prepare-batch` 按四个新 build attempts 重建 16 个 review work items，覆盖四卷 × 四版；旧 work items 已由工具按 attempt 变化安全替换。
- 已完成子阶段：重新生成的 16 张接触表覆盖最终 106 页，全部逐页检查；未见裁切、重叠、缺字或分页异常。
- 已完成子阶段：新构建的 16 个候选页，以及贵州先前 warning 关联页，合计 20 页完成 120dpi 复核；所有源注符号均清晰可读，未见版面缺陷。贵州先前缺字页现已正确显示 `\theta`、`\cos^n x`、`\alpha`。
- 已完成子阶段：16 份当前 attempt 工作项覆盖 106 页 × 8 项，共 848 个带具体说明的 pass 检查；16 个候选页及 4 个额外贵州旧 warning 页均记录 120dpi 复核。`check-batch` 当前仅报告正式 review receipt 仍绑定旧 build（attempt、输入树、工具链和 PDF 变化）；此为 finalize 事务前的预期陈旧状态，work items 已绑定当前 attempts。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，批次 `closed`，无问题；生成 `reports/phase2-b36.md`，manifest revision 3860。
- 已完成子阶段：清除四卷 build 内全部 96 个非 PDF 编译中间物，每卷保留四份 PDF；清除 `.work/phase2-b36/` 下 16 份 review work items 与 12 份 provenance 角色文件；删除本轮临时复核目录中的 142 张 PNG。复核四卷各 4 PDFs、0 非 PDF，临时/工作目录均不存在。
- 已完成子阶段：所有 scoped gates 通过：source manifest 775 项；生成器 `--check` 通过；build receipts 4 succeeded、0 failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。`report.py render --all` 以一个 content 事务写入并回读校验六个目标；`report.py check --all` 通过并保留未完成状态；`git diff --check` 通过。
- 最终 diff 审核：26 个 tracked 文件，仅涉及本批三份规范 Markdown/合并投影、贵州卷生成的 `questions.tex`/`answers.tex`、四卷 provenance/build/review receipts、manifest 驱动的六个报告/README 投影、本批报告、manifest 与进度文件；无无关文件改动。构建目录的 16 份 PDF 均保留。
- 验证快照：manifest revision 3860；来源 775、试卷 272、批次 138；批次 closed 55、provenance_verified 2、compiled_pending_review 64、closed_with_blockers 17；试卷 complete 104、editions_generated 4、compiled 119、blocked 45。仍有大量后续待复核/阻塞卷；该数字只记当前进度，不代表全库完成。
- 已完成阶段：phase2-b36 内容与报告投影已提交 `5cf91e8c`（`docs: 完成1977云贵桂四卷复核`）；不 push。

### `phase2-b37` — 1977 湖北、湖南、湖南株洲、吉林

- 预检完成：四卷关联 33 条 issue（`ISSUE-0277`—`ISSUE-0309`）全部 resolved；source manifest 校验通过（775 artifacts）。
- 已有内容：provenance 共 33 题，逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用既有转录/核查成果，不重新转录或解题。既有 PDF 四版页数分别为湖北 2/11/3/8（24）、湖南 3/15/4/11（33）、湖南株洲 5/21/6/19（51）、吉林 3/14/4/11（32），共 140 页。
- 旧构建：四卷均有四版 PDF；build receipts 均因生成输入树与工具链指纹变化 stale，review receipts 随 build stale。`provenance.py check-batch` 只报缓存状态 compiled/compiled_pending_review 与现场派生 editions_generated/provenance_verified 不符；`provenance.py status` 确认四卷 provenance current、批次 provenance_verified。无题目、答案或来源变化需求。
- 已完成子阶段：formal build 四卷四版成功，manifest revision 3862；湖北 24 页、湖南 33 页、湖南株洲 51 页、吉林 32 页，共 140 页，四卷均无 missing-character、Overfull 或 Underfull warning。新 build attempts：湖北 `84cf156d-c13d-48fa-8664-d80c2763e2e9`、湖南 `18e48179-b0e3-4d4c-9cb8-ad07d185549d`、湖南株洲 `24aee93e-88c4-42bb-af7b-a3145975340f`、吉林 `937d6c9a-0021-4206-b2cd-4795d4392152`。`validate-receipts` 返回 4 succeeded、0 failed/invalid/missing/stale。
- 已完成子阶段：`prepare-batch` 生成 16 个 review work items，覆盖四卷 × 四版并绑定当前 build attempts。
- 已完成子阶段：16 张接触表覆盖最终 140 页并逐页检查；四卷四版均未见裁切、重叠、缺字、异常分页或答案渗入题面。
- 已完成子阶段：16 个候选页均以 120dpi 高分辨率复核通过；包括四卷四版的指定页，图形、公式与标注清晰，无需内容或版式修订。
- 已完成子阶段：16 份当前 attempt 工作项已登记 140 页 × 8 项共 1120 项具体说明的 pass 检查，0 pending、0 non-pass。`check-batch` 仅报告现有正式 review receipts 仍绑定旧 build/PDF；这是 finalize 事务刷新回执前的预期陈旧状态，work items 均绑定当前 attempts。
- 修改文件：16 份 `.work/phase2-b37/review/` 忽略工作项及本进度文件；本阶段未改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，批次状态 `closed`、无问题；生成 `reports/phase2-b37.md`，manifest revision 3863。
- 已完成子阶段：清理四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个；每卷保留四份 PDF。清除 `.work/phase2-b37/` 下 16 份 review work items 和 `/tmp/gk-phase2-b37-review.li2W7Y/` 下 32 张接触表/高分辨率 PNG；复核临时目录均已不存在。
- 已完成子阶段：scoped gates 全部通过：source manifest 校验通过；生成器 `--check` 通过；build receipts 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 当前一致并保留未完成状态；`git diff --check` 通过。
- 最终 diff 审阅：17 个 tracked 文件，限于四卷 build/review receipts、manifest 驱动的六个全量报告/README 投影、本批报告、manifest 与进度文件；没有题目源、答案、provenance 或代码改动。四卷 16 份 PDF 均保留。
- 验证快照：manifest revision 3863；批次 `phase2-b37` 状态 `closed`，140 页、1120 项视觉检查均通过。该批完成不代表全库完成。
- 已完成阶段：b37 内容与报告投影提交 `42556c39`（`docs: 完成1977湘鄂吉四卷复核`）；未 push。
- 下一批：按 manifest 顺序为 `phase2-b38`（1977 江苏南通、江西、辽宁、宁夏四卷），当前状态 `compiled_pending_review`。
- 已完成阶段：b38 内容与报告投影提交 `14bc7f25`（`docs: 完成1977苏赣辽宁四卷复核`）；未 push。

### `phase2-b38` — 1977 江苏南通、江西、辽宁、宁夏

- 预检完成：manifest revision 3863；source manifest 校验通过（775 项）；该批 issue 列表为空。provenance 共 38 题，逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用已完成转录/核查，不重新转录或解题。
- 既有 PDF 四版页数分别为江苏南通 2/10/3/9（24）、江西 2/11/3/9（25）、辽宁 3/16/4/12（35）、宁夏 4/18/5/15（42），共 126 页。
- 旧构建回执四卷均因生成输入树及工具链指纹变化 stale；review receipts 随 build stale。`provenance.py status` 确认现场派生为四卷 `editions_generated`、批次 `provenance_verified`；缓存仍为 `compiled`/`compiled_pending_review`。除该预期缓存差异外，无来源、题目或答案更新需求。
- 修改文件：本进度文件；预检未写 manifest、provenance 或试卷内容。
- 已完成子阶段：formal build 四卷四版完成，manifest revision 3865；江苏南通 24 页、江西 25 页、辽宁 35 页、宁夏 42 页，共 126 页；四卷均 0 warning。Build attempts：江苏南通 `befdbc77-e6f1-403a-9843-c59b435df510`、江西 `77de8114-509b-4e5b-ac58-88f319cc44d4`、辽宁 `3e2f1720-913c-4aa3-8aff-8f6bd5f3b762`、宁夏 `8e9c7670-072d-4602-b6c4-47ce42565e76`。`validate-receipts` 无 failed/invalid/missing/stale；四卷保持 pending review，符合正式复核前状态。
- 已完成子阶段：`prepare-batch` 建立 16 个当前 attempt review work items，覆盖四卷 × 四版。
- 已完成子阶段：16 张接触表覆盖最终 126 页并逐页检查；未见裁切、重叠、缺字、异常分页或答案渗入题面。
- 已完成子阶段：16 个候选页均完成 120dpi 高分辨率复核；公式、图形与文字标注清晰，无需内容或版式修订。
- 已完成子阶段：16 个当前 attempt 工作项已登记 126 页 × 8 项共 1008 项具体说明的 pass 检查，0 pending、0 non-pass。`check-batch` 仅报告正式 review receipts 仍绑定旧 build/PDF；属 finalize 事务刷新正式回执前的预期状态。
- 修改文件：16 份 `.work/phase2-b38/review/` 忽略工作项及本进度文件；未改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，批次状态 `closed`、无问题；生成 `reports/phase2-b38.md`，manifest revision 3866。
- 已完成子阶段：清理四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个；每卷保留四份 PDF。清除 `.work/phase2-b38/` 下 16 份 review work items 与 `/tmp/gk-phase2-b38-review.e6cA2M/` 下 158 张页面/接触表 PNG；复核临时目录均已不存在。
- 已完成子阶段：scoped gates 全部通过：source manifest 校验通过；生成器 `--check` 通过；build receipts 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 当前一致并保留未完成状态；`git diff --check` 通过。
- 最终 diff 初审：17 个 tracked 文件，限于四卷 build/review receipts、manifest 驱动的六个全量报告/README 投影、本批报告、manifest 与进度文件；没有题目源、答案、provenance 或代码改动。四卷 16 份 PDF 均保留。
- 验证快照：manifest revision 3866；批次 `phase2-b38` 状态 `closed`，126 页、1008 项视觉检查均通过。全库统计为批次 closed 57、closed_with_blockers 17、compiled_pending_review 62、provenance_verified 2；试卷 complete 112、compiled 111、blocked 45、editions_generated 4。仅为当前快照，不代表全库完成。
- 已完成阶段：b38 内容与报告投影提交 `14bc7f25`（`docs: 完成1977苏赣辽宁四卷复核`）；未 push。
- 下一批：按 manifest 顺序为 `phase2-b39`（1977 山东 A、山东 B、陕西、新疆文科四卷），当前状态 `compiled_pending_review`。
- 已完成阶段：b38 进度记录提交 `1d5da0aa`；未 push。

### `phase2-b39` — 1977 山东 A、山东 B、陕西、新疆文科

- 预检完成：manifest revision 3866；source manifest 校验通过（775 项）；该批 issue 列表为空。provenance 共 34 题，逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用既有转录/核查，不重新转录或解题。
- 既有 PDF 四版页数分别为山东 A 3/12/4/11（30）、山东 B 3/14/4/12（33）、陕西 3/15/4/12（34）、新疆文科 3/11/4/8（26），共 123 页。
- 旧构建回执四卷均因生成输入树与工具链指纹变化 stale；review receipts 随 build stale。`provenance.py status` 确认四卷 provenance current、现场派生为 `editions_generated`，批次为 `provenance_verified`；缓存仍为 `compiled`/`compiled_pending_review`。
- 修改文件：仅本进度文件；预检未更改来源、manifest、provenance 或试卷内容。
- 已完成子阶段：formal build 四卷四版完成，manifest revision 3868；山东 A 30 页、山东 B 33 页、陕西 34 页、新疆文科 26 页，共 123 页，四卷均 0 warning。Build attempts：山东 A `d85c5494-c89f-4b25-8682-d75faa5aed09`、山东 B `9e1368b2-6215-4285-a173-3daf54dc3c8d`、陕西 `01df8a22-369d-4ba0-87eb-c58d32296b89`、新疆文科 `8b6cc577-1559-4bc1-978d-bef1339e4f3e`。`validate-receipts` 无 failed/invalid/missing/stale；四卷待复核状态符合预期。
- 已完成子阶段：`prepare-batch` 建立 16 个当前 attempt review work items，覆盖四卷 × 四版。
- 已完成子阶段：16 张接触表覆盖最终 123 页并逐页检查；未见裁切、重叠、缺字、异常分页或答案渗入题面。
- 已完成子阶段：16 个候选页均以 120dpi 高分辨率逐张复核，印刷版重点页、三种派生版首页与解答页字形/公式/图稿完整，未发现版式缺陷。
- 修改文件：本阶段未新增受跟踪文件更改；复核图和工作项均为临时/忽略产物。
- 已验证：接触表逐页覆盖 123/123 页；候选页高分辨率复核 16/16 页通过。合计将登记 984 项（123 页 × 8 检查项）。
- 已完成子阶段：16 份当前 attempt 工作项登记 123 页 × 8 项共 984 项具体说明的 pass 检查，0 pending、0 non-pass。`check-batch` 唯一问题为四份正式 review receipts 仍绑定旧 build attempt/输入树/工具链/PDF，属 finalize 刷新回执前的预期陈旧状态。
- 修改文件：16 份 `.work/phase2-b39/review/` 忽略工作项及本进度文件；未改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，批次状态 `closed`、无问题；正式回执与批次投影更新至 manifest revision 3869，并生成 `reports/phase2-b39.md`。
- 已完成子阶段：清除四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个；每卷仅保留四份 PDF。16 份 `.work/phase2-b39/` 工作项与本轮复核图目录 `/tmp/gk-phase2-b39-review.c8hbrL/` 已移入系统废纸篓；四卷各 4 PDFs、0 非 PDF，临时路径均不存在。
- 已完成子阶段：b39 scoped gates 全通过：source manifest 校验、生成器 `--check`、build receipts 4 succeeded/0 pending-failed-invalid-missing-stale、review `FINALIZED`、provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 通过，单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 一致并保留未完成状态。
- 最终 diff 审阅：17 个 tracked 文件，限于四卷 build/review receipts、manifest 驱动的六个报告/README/清单投影、本批报告、manifest 与进度文件；无 `.tex`、答案、provenance 或代码源改动。`git diff --check` 通过；四卷 16 份 PDF 均保留。
- 验证快照：manifest revision 3869；b39 状态 `closed`，123 页、984 项视觉检查通过。全库批次状态为 closed 58、closed_with_blockers 17、compiled_pending_review 61、provenance_verified 2；试卷状态 complete 116、compiled 107、blocked 45、editions_generated 4。仅为当前快照，不代表全库完成。
- 已完成阶段：b39 内容与报告投影提交 `ebf294e2`（`docs: 完成1977鲁陕新四卷复核`）；未 push。
- 下一批：按 manifest 顺序为 `phase2-b40`（1977 广西百色卷理科），当前状态 `compiled_pending_review`。
- 待完成：提交本进度记录中的 b39 提交哈希与下一批状态。
- 下一步：仅提交本进度文件；随后检查 b40 的来源/provenance、issue、构建和复核状态，判断能否复用现有内容。

### `phase2-b40` — 1977 广西百色卷（理科）

- 预检完成：manifest revision 3869；source manifest 校验通过，该批 issue 列表为空。生成器 `--check` 显示 1 卷生成结果一致。
- provenance 共 6 题，逐题 transcription review 均 passed、答案证据均 A、conflict 均 null；复用现有转录/核查，不重新转录或解题。关联 issue `ISSUE-0382`—`ISSUE-0387` 均已 resolved，不属于该批待处理 issue。
- 现有固定源 PDF 为 6 页；四版现有 PDF 页数为试题版 3、解析版 12、简答版 4、印刷版 9，共 28 页。
- 旧 build receipt 因生成输入树与工具链指纹变化 stale；review receipt 随 build stale。`provenance.py status` 确认现场派生卷状态 `editions_generated`、批次状态 `provenance_verified`，manifest 缓存仍为 `compiled`/`compiled_pending_review`。无题目、答案或来源变更需求。
- 修改文件：本进度文件；本阶段只读预检未更改源文件、manifest、provenance 或试卷内容。
- 已完成子阶段：正式构建四版完成，build attempt `cd7fba5f-8b45-474b-b102-6c6342732719`；试题版 3 页、解析版 12 页、简答版 4 页、印刷版 9 页，共 28 页，四版均无 overfull warning。build receipt validation 无 failed/invalid/missing/stale；pending review 为预期状态。
- 已完成子阶段：`prepare-batch` 生成 4 个当前 attempt review work items，覆盖该卷四版。
- 已完成子阶段：四张接触表覆盖四版全部 28 页并逐页检查；未见裁切、缺字、图形遮叠、分页异常或版本内容串漏。4 个候选页以 120dpi 逐张复核，文字/公式/图稿完整。
- 已完成子阶段：4 份当前 attempt 工作项登记 28 页 × 8 项共 224 项具体说明的 pass 检查，0 pending、0 non-pass。`check-batch` 唯一问题为正式 review receipt 仍绑定旧 build attempt/输入树/工具链/PDF，属 finalize 刷新回执前的预期陈旧状态。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b40 状态 `closed`、无问题；正式回执与状态更新至 manifest revision 3872，并生成 `reports/phase2-b40.md`。
- 已完成子阶段：清除该卷 build 内 24 个非 PDF 编译中间物，仅保留四份 PDF；4 个 `.work/phase2-b40/` 工作项与本轮 `/tmp/gk-phase2-b40-review.NGowqI/` 下 36 张 PNG 已移入系统废纸篓。复核项目目录为 4 PDFs、0 非 PDF，临时路径均不存在。
- 已完成子阶段：b40 scoped gates 全通过：source manifest 校验、生成器 `--check`、build receipts 1 succeeded/0 pending-failed-invalid-missing-stale、review `FINALIZED`、provenance `OK：1 卷`。
- 已完成子阶段：`report.py render --all` 通过，单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 一致并保留未完成状态。
- 最终 diff 审阅：11 个 tracked 文件，限于该卷 build/review receipts、manifest 驱动报告/README/清单投影、本批报告、manifest 与进度文件；无 `.tex`、答案、provenance 或代码源改动。`git diff --check` 通过；该卷四份 PDF 均保留。
- 验证快照：manifest revision 3872；b40 状态 `closed`，28 页、224 项视觉检查通过。全库批次状态为 closed 59、closed_with_blockers 17、compiled_pending_review 60、provenance_verified 2；试卷状态 complete 117、compiled 106、blocked 45、editions_generated 4。仅为当前快照，不代表全库完成。
- 已完成阶段：b40 内容与报告投影提交 `347ef48b`（`docs: 完成1977广西百色理科卷复核`）；未 push。
- 下一批：按 manifest 顺序为 `phase2-b41`（1977 江苏农垦、南京、南通地区、南通市四卷），当前状态 `compiled_pending_review`。
- 待完成：提交本进度记录中的 b40 提交哈希与下一批状态。
- 下一步：仅提交本进度文件；随后核查 b41 四卷来源/provenance、issue、构建和复核状态。

### `phase2-b41` — 1977 江苏农垦、南京、南通地区、南通市

- 预检完成：manifest revision 3872；source manifest 校验通过，该批 issue 列表为空。生成器 `--check` 显示四卷生成结果一致。
- provenance 共 40 题，逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用现有转录/核查，不重新转录或解题。关联 issue 共 40 项且均为 resolved，不属于该批待处理 issue。
- 固定源 PDF 页数分别为农垦 2、南京 2、南通地区 1、南通市 3。既有四版 PDF 页数分别为 16、24、16、29 页，共 85 页。
- 旧 build receipts 四卷均因生成输入树与工具链指纹变化 stale；review receipts 随 build stale。`provenance.py status` 确认现场派生四卷均为 `editions_generated`、批次为 `provenance_verified`；manifest 缓存仍为 `compiled`/`compiled_pending_review`。无题目、答案或来源变更需求。
- 修改文件：本进度文件；本阶段只读预检未更改来源、manifest、provenance 或试卷内容。
- 已完成子阶段：formal build 四卷四版完成，manifest revision 3874；农垦 16 页、南京 24 页、南通地区 16 页、南通市 29 页，共 85 页，四卷均无 overfull warning。Build receipts 无 failed/invalid/missing/stale；4 卷 pending review 为预期状态。Build attempts：农垦 `765d292d-422a-49cf-bbd1-d65ca38d3fce`、南京 `878379ae-6032-4f9c-a516-b6d3f06935fa`、南通地区 `5cebf97a-987e-4c5f-b212-191bca28bf20`、南通市 `6d889f37-c762-4814-b680-2549407ce942`。
- 已完成子阶段：`prepare-batch` 生成 16 个当前 attempt review work items，覆盖四卷 × 四版。
- 已完成子阶段：16 张接触表覆盖四卷四版最终 85 页并逐页检查；未见裁切、缺字、图形遮叠、异常分页或答案串版。16 个候选页均以 120dpi 逐张复核，字形、公式和图稿清晰完整。
- 已完成子阶段：16 份当前 attempt 工作项登记 85 页 × 8 项共 680 项具体说明的 pass 检查，0 pending、0 non-pass。`check-batch` 唯一问题为四份正式 review receipts 仍绑定旧 build attempt/输入树/工具链/PDF，属 finalize 刷新回执前的预期陈旧状态。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b41 状态 `closed`、无问题；正式回执与批次状态更新至 manifest revision 3875，并生成 `reports/phase2-b41.md`。
- 已完成子阶段：清除四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个；每卷仅保留四份 PDF。16 份 `.work/phase2-b41/` 工作项与本轮 `/tmp/gk-phase2-b41-review.SXn73v/` 下 117 张页面/接触表/候选 PNG 已移入系统废纸篓。四卷各 4 PDFs、0 非 PDF，临时路径均不存在。
- 已完成子阶段：b41 scoped gates 全通过：source manifest 校验、生成器 `--check`、build receipts 4 succeeded/0 pending-failed-invalid-missing-stale、review `FINALIZED`、provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 通过，单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 一致并保留未完成状态。
- 最终 diff 审阅：17 个 tracked 文件，限于四卷 build/review receipts、manifest 驱动报告/README/清单投影、本批报告、manifest 与进度文件；无 `.tex`、答案、provenance 或代码源改动。`git diff --check` 通过；四卷 16 份 PDF 均保留。
- 验证快照：manifest revision 3875；b41 状态 `closed`，85 页、680 项视觉检查通过。全库批次状态为 closed 60、closed_with_blockers 17、compiled_pending_review 59、provenance_verified 2；试卷状态 complete 121、compiled 102、blocked 45、editions_generated 4。仅为当前快照，不代表全库完成。
- 已完成阶段：b41 内容与报告投影提交 `676783f2`（`docs: 完成1977苏南四卷复核`）；未 push。
- 下一批：按 manifest 顺序为 `phase2-b42`（1977 江苏常州、徐州、扬州、无锡四卷），当前状态 `compiled_pending_review`。
- 待完成：提交本进度记录中的 b41 提交哈希与下一批状态。
- 下一步：仅提交本进度文件；随后核查 b42 四卷来源/provenance、issue、构建和复核状态。

### `phase2-b42` — 1977 江苏常州、徐州、扬州、无锡

- 预检完成：manifest revision 3875；source manifest 校验通过，该批 issue 列表为空。生成器 `--check` 显示四卷生成结果一致。
- provenance 共 42 题，逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用现有转录/核查，不重新转录或解题。关联 issue 共 42 项且均为 resolved，不属于该批待处理 issue。
- 固定源 PDF 页数分别为常州 3、徐州 2、扬州 2、无锡 3。既有四版 PDF 页数分别为常州 34、徐州 30、扬州 22、无锡 29 页，共 115 页。
- 旧 build receipts 四卷均因生成输入树与工具链指纹变化 stale；review receipts 随 build stale。`provenance.py status` 确认现场派生四卷均为 `editions_generated`、批次为 `provenance_verified`；manifest 缓存仍为 `compiled`/`compiled_pending_review`。无题目、答案或来源变更需求。
- 修改文件：本进度文件；本阶段只读预检未更改来源、manifest、provenance 或试卷内容。
- 已完成子阶段：formal build 四卷四版完成，manifest revision 3877；常州 34 页、徐州 30 页、扬州 22 页、无锡 29 页，共 115 页，四卷均无 overfull warning。Build receipts 无 failed/invalid/missing/stale；4 卷 pending review 为预期状态。Build attempts：常州 `5e896c38-34a8-462f-b059-db6e0c59ac61`、徐州 `81e384f9-792b-486e-abd0-786324498577`、扬州 `6134c751-214c-4381-8627-c2dc4c44e0c5`、无锡 `5830b133-ed63-4514-8056-443422fe3a26`。
- 已完成子阶段：`prepare-batch` 生成 16 个当前 attempt review work items，覆盖四卷 × 四版。
- 已完成子阶段：16 张接触表覆盖四卷四版最终 115 页并逐页检查，未见裁切、重叠、缺字、异常分页或答案渗入题面。
- 已完成子阶段：16 个候选页均完成 120dpi 高分辨率复核（常州、扬州、无锡各四版首页；徐州印刷版第 2 页、简答/试题版首页、解析版第 11 页），文字、公式、图稿及边界均清晰完整，未发现需修订的版式缺陷。
- 阶段修改文件：本进度文件；本阶段无内容源、provenance 或生成文件更改。复核 PNG 位于临时目录 `/tmp/gk-phase2-b42-review.2ZzoLM/`。
- 验证结果：接触表逐页覆盖 115/115 页；高分辨率候选复核 16/16 页通过。下一阶段将按 115 页 × 8 检查项登记 920 项视觉检查。
- 已完成子阶段：16 份当前 attempt 工作项登记 115 页 × 8 项共 920 项具体说明的 pass 检查，0 pending、0 non-pass；候选页锚点与已复核的 16 个候选页完全对应。`check-batch` 只报告正式 review receipts 仍绑定旧 build attempt/输入树/工具链/PDF，属于 finalize 刷新正式回执前的预期状态。
- 阶段修改文件：本进度文件及 16 份忽略的 `.work/phase2-b42/review/` 工作项；未改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，批次状态 `closed`、无问题；正式 review receipts 更新并生成 `reports/phase2-b42.md`，manifest revision 3878。
- 阶段修改文件：review receipts、四卷状态/manifest 投影、`reports/phase2-b42.md` 与本进度文件；复核工作项仍为忽略文件。
- 已完成子阶段：四卷各删除 24 个非 PDF 编译中间物，共 96 个；每卷保留四份 PDF、0 个非 PDF 构建文件。16 份 `.work/phase2-b42/` review 工作项及 `/tmp/gk-phase2-b42-review.2ZzoLM/` 下 147 张临时 PNG 已移入系统废纸篓；两处路径均已确认不存在。
- 阶段修改文件：本进度文件、四卷 build/review receipts、manifest 与本批报告；未改 LaTeX 源文件，四卷 PDF 保留。
- 已完成子阶段：scoped gates 全通过：source manifest validate；生成器 `--check` 显示 4 卷一致；build receipts 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认输出与全量 manifest 当前一致，并保留其他未完成状态。
- 最终 diff 审核：`git diff --check` 通过；17 个 tracked 文件，范围仅含四卷 build/review receipts、manifest、全量 README/报告投影、本批报告及进度文件；无题目/答案/provenance/LaTeX 源或代码改动。四卷 16 份 PDF 保留。
- 验证快照：manifest revision 3878；b42 `closed`，115 页、920 项视觉检查通过。全库批次状态：closed 61、closed_with_blockers 17、compiled_pending_review 58、provenance_verified 2；试卷 production state：complete 125、compiled 98、blocked 45、editions_generated 4。该快照只反映当前进度，不代表全库完成。
- 下一批：manifest 顺序为 `phase2-b43`（1977 江苏淮阴、盐城、苏州地区、苏州市四卷），当前 `compiled_pending_review`。
- 已完成阶段：b42 内容与报告投影提交 `f978bcea`（`docs: 完成1977苏常徐扬锡四卷复核`）；未 push。
- 下一步：单独提交本进度记录；随后检查并继续 b43。

### `phase2-b43` — 1977 江苏淮阴、盐城、苏州地区、苏州市

- 预检完成：起始 manifest revision 3878；source manifest validate 通过；批次 issue 列表为空；生成器 `--check` 显示四卷输出一致。
- provenance 共 29 题（淮阴 9、盐城 8、苏州地区 6、苏州市 6），逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用既有转录/解题和盲核结果，不重做内容。
- `provenance.py status` 显示四卷 `editions_generated`、批次 `provenance_verified`；`check-batch` 报告 manifest 缓存状态与现场派生状态不一致，属于此前未 finalize 的缓存状态差异，不是题目 provenance 缺失。四卷旧 build receipts 均因生成输入树和工具链指纹变化 stale，需要重建。
- 现有四版 PDF 页数依次为淮阴 2/9/3/6、盐城 2/10/3/8、苏州地区 2/11/3/8、苏州市 2/12/3/9，共 93 页；每卷现有 build 目录仅有四版 PDF。
- 已完成子阶段：正式构建四卷四版完成，manifest revision 3880；页数与既有 PDF 相同，共 93 页。Build attempts：淮阴 `87f4d274-6472-4dc0-b026-5398ec280020`、盐城 `f27c1389-6a00-443b-830f-8c41b2eaaf4b`、苏州地区 `c5e3d2d8-7646-456d-87a4-4af0bf247a9c`、苏州市 `f1dff174-4434-4251-9fd4-cfb05de943a1`。无 missing-character warning；盐城解析版有一条 4.48792pt Overfull hbox（line 34），其余三卷无 overfull。Build receipt 校验无 failed/invalid/missing/stale，四卷待复核为预期状态。
- 修改文件：本进度文件、四卷 build receipts/PDF；预检与构建未更改题目源、答案或 provenance。
- 已完成子阶段：`prepare-batch` 建立 16 个当前 attempt review work items；生成 16 张接触表，覆盖四卷四版 93/93 页并逐页检查，未见裁切、遮叠、缺字或异常分页。
- 已完成子阶段：16 个候选页完成 120dpi 逐张复核，未见版式缺陷；另对盐城解析版警告页第 3 页完成 120dpi 检查。Overfull 精确指向 `answers.tex` 第 34 行行间公式，宽度 4.48792pt；视觉上公式完整可读、无裁切或遮挡，按既有规则记录精确 warning exemption，保留原题解不改内容。
- 阶段修改文件：本进度文件；接触表、高分辨率图和 work items 位于临时目录/忽略 `.work`，不进入版本控制；本阶段未改题目、答案、provenance 或生成源。
- 验证结果：接触表逐页覆盖 93/93；候选页复核 16/16，另有 warning 关联页 1 页完成高分辨率复核。下一阶段登记 744 项（93 页 × 8 检查项）并登记上述单条 warning 豁免。
- 已完成子阶段：16 份当前 attempt work items 登记 93 页 × 8 项共 744 项具体说明的 pass 检查，0 pending、0 non-pass；盐城解析版单条 Overfull 按当前 build 日志字段精确登记豁免（`answers.tex` 第 34 行、PDF 第 3 页、120dpi 视觉 pass）。`check-batch` 仅报告正式 review receipts 仍绑定旧 build，属 finalize 刷新回执前预期状态。
- 阶段修改文件：本进度文件及忽略的 `.work/phase2-b43/review/` 下 16 份工作项；未改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b43 状态 `closed`、无问题；单条 warning exemption 与 build warning 逐字段匹配，正式 review receipts 更新并生成 `reports/phase2-b43.md`，manifest revision 3881。
- 阶段修改文件：四卷 review receipts、manifest 状态投影、本批报告与本进度文件；忽略工作项和临时 PNG 待清理。
- 已完成子阶段：四卷 build 目录各删除 24 个非 PDF 编译中间物，共 96 个，每卷保留 4 份 PDF、0 个非 PDF；16 份 `.work/phase2-b43/` 工作项与 `/tmp/gk-phase2-b43-review.EfQ1QQ/` 下 126 张 PNG 已移入系统废纸篓，两临时路径确认不存在。
- 已完成子阶段：scoped gates 全通过：source manifest validate；生成器 `--check` 显示 4 卷一致；build receipts 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 一致并保留未完成状态。
- 最终 diff 审核：`git diff --check` 通过；17 个 tracked 文件仅涉及四卷 build/review receipts、manifest、全量 README/报告投影、本批报告与进度；无题目/答案/provenance/LaTeX 源或代码改动。四卷 16 份 PDF 保留；盐城解析版单条 warning 已有视觉豁免证据。
- 验证快照：manifest revision 3881；b43 `closed`，93 页、744 项检查通过，1 条精确 warning exemption。全库批次状态：closed 62、closed_with_blockers 17、compiled_pending_review 57、provenance_verified 2；试卷 production state：complete 129、compiled 94、blocked 45、editions_generated 4。该快照仅代表当前进度，不代表全库完成。
- 下一批：manifest 顺序为 `phase2-b44`（1977 江苏连云港、镇江、黑龙江三卷），当前 `compiled_pending_review`。
- 已完成阶段：b43 内容与报告投影提交 `cc6baf2c`（`docs: 完成1977苏淮盐苏四卷复核`）；未 push。
- 下一步：单独提交本进度记录；随后检查并继续 b44。

### `phase2-b44` — 1977 江苏连云港、镇江、黑龙江

- 预检完成：起始 manifest revision 3881；source manifest validate 通过，批次 issue 列表为空；生成器 `--check` 显示 3 卷生成输出一致。
- provenance 共 29 题（连云港 8、镇江 9、黑龙江 12），逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用既有转录与解题/盲核结果，不重做内容。
- `provenance.py status` 显示三卷 `editions_generated`、批次 `provenance_verified`；旧 build receipts 三卷均因生成输入树和工具链指纹变化 stale，需要正式重建。
- 既有四版 PDF 页数依次为连云港 3/13/4/10、镇江 3/14/4/10、黑龙江 3/11/4/8，共 87 页；未见需修改题目、答案或 provenance 的证据。
- 已完成子阶段：正式构建三卷四版完成，manifest revision 3883；页数与既有 PDF 相同，共 87 页。Build attempts：连云港 `9052ba28-4bf5-48be-bf38-7986e7a530ca`、镇江 `77eb05ee-c50a-4130-b33b-9048c210017c`、黑龙江 `2c3333af-500c-44e8-99e7-a7c5ce4c22cc`。三卷均无 failed/missing-character/Overfull warning；build receipt 校验无 failed/invalid/missing/stale，pending review 为预期状态。
- 修改文件：本进度文件、三卷 build receipts/PDF；未更改题目源、答案或 provenance。
- 已完成子阶段：`prepare-batch` 建立 12 个当前 attempt review work items，覆盖三卷 × 四版。
- 已完成子阶段：12 张接触表逐页覆盖最终 87 页并检查；未见裁切、缺字、图形遮叠、异常分页或答案串版。12 个候选页均以 120dpi 逐张复核通过。
- 阶段修改文件：本进度文件；接触表、候选图和 work items 位于临时目录/忽略 `.work`，不进入版本控制；未改题目源、答案、provenance 或生成源。
- 验证结果：接触表覆盖 87/87 页；高分辨率候选复核 12/12 页通过，构建无 warning。
- 已完成子阶段：12 份当前 attempt 工作项登记 87 页 × 8 项共 696 项具体说明的 pass 检查，0 pending、0 non-pass，无 warning exemption。`check-batch` 仅报告正式 review receipts 仍绑定旧 build，属 finalize 刷新回执前的预期状态。
- 阶段修改文件：本进度文件及忽略的 `.work/phase2-b44/review/` 下 12 份工作项；未改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b44 状态 `closed`、无问题；正式 review receipts 更新并生成 `reports/phase2-b44.md`，manifest revision 3884。
- 阶段修改文件：三卷 review receipts、manifest 状态投影、本批报告与本进度文件；忽略工作项和临时 PNG 待清理。
- 已完成子阶段：三卷 build 目录各删除 24 个非 PDF 编译中间物，共 72 个；每卷保留四份 PDF、0 个非 PDF。12 份 `.work/phase2-b44/` review 工作项与 `/tmp/gk-phase2-b44-review.s51RED/` 下 111 张 PNG 已移入系统废纸篓，两路径确认不存在。
- 已完成子阶段：scoped gates 全通过：source manifest validate；生成器 `--check` 显示 3 卷一致；build receipts 3 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：3 卷`。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认输出与全量 manifest 当前一致，并保留未完成状态。
- 最终 diff 审核：`git diff --check` 通过；15 个 tracked 文件仅涉及三卷 build/review receipts、manifest、全量 README/报告投影、本批报告与进度文件；无题目/答案/provenance/LaTeX 源或代码改动。三卷 12 份 PDF 保留。
- 验证快照：manifest revision 3884；b44 `closed`，87 页、696 项视觉检查通过。全库批次状态：closed 63、closed_with_blockers 17、compiled_pending_review 56、provenance_verified 2；试卷 production state：complete 132、compiled 91、blocked 45、editions_generated 4。该快照仅反映当前进度，不代表全库完成。
- 下一批：manifest 顺序为 `phase2-b45`（1958 北京、云南、四川、江苏四卷），当前 `compiled_pending_review`。
- 已完成阶段：b44 内容与报告投影提交 `99a01770`（`docs: 完成1977连云镇江黑龙江三卷复核`）；未 push。
- 下一步：单独提交本进度记录；随后检查并继续 b45。

### `phase2-b45` — 1958 北京、云南、四川、江苏

- 预检完成：起始 manifest revision 3884；source manifest validate 通过，批次 issue 列表为空；生成器 `--check` 显示四卷输出一致。
- provenance 共 32 题（北京 11、云南 8、四川 8、江苏 5），逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用既有转录与解题/盲核结果，不重做内容。
- `provenance.py status` 显示四卷 `editions_generated`、批次 `provenance_verified`；四卷旧 build receipts 因生成输入树和工具链指纹变化 stale，需要正式重建。
- 既有四版 PDF 页数依次为北京 2/12/3/10、云南 1/10/2/8、四川 1/8/2/6、江苏 1/8/2/6，共 82 页；每卷 build 目录现有四版 PDF，无需改题目、答案或 provenance。
- 已完成子阶段：正式构建四卷四版完成，manifest revision 3886；页数与既有 PDF 相同，共 82 页。Build attempts：北京 `6915f50f-0562-40f9-aebf-a899be72e6cd`、云南 `d6aba18a-7afa-4e19-846c-7871851d2a26`、四川 `791ae4ae-9980-48a4-9a0f-a9a8962f1376`、江苏 `427245e1-9579-4332-af96-bf3b1bb5a270`。四卷均无 failed/missing-character/Overfull warning；build receipt 校验无 failed/invalid/missing/stale，pending review 为预期状态。
- 修改文件：本进度文件、四卷 build receipts/PDF；未更改题目源、答案或 provenance。
- 已完成子阶段：16 张接触表检查覆盖四卷四版全部 82 页；未见裁切、遮叠、缺字、异常分页或答案串版。
- 已完成子阶段：16 个候选页均已 120dpi 高分辨率逐张复核；字形、公式、图稿、页眉页脚和页面边界清晰，无需版式修复或重编。
- 阶段验证：接触表覆盖 82/82 页，候选页复核 16/16 通过；后续已登记 656 项逐页视觉检查（82 页 × 8 项），全部通过。
- 阶段修改文件：仅本进度文件；渲染图和 review work items 位于临时目录/忽略 `.work`，不进入版本控制。
- 已完成子阶段：16 份当前 attempt review work items 登记 82 页 × 8 项共 656 项 pass 检查，0 pending、0 non-pass；逐份核对 paper/edition、build attempt 与 PDF SHA-256 均匹配当前 build receipts。
- 阶段验证：`check-batch` 仅报告正式 review receipts 仍绑定旧 build attempt/输入树/依赖闭包/工具链/PDF；此为 finalize 刷新正式回执前的预期状态。无 warning，无需 warning exemption。
- 阶段修改文件：本进度文件及忽略的 `.work/phase2-b45/review/` 下 16 份工作项；未改题目、答案、provenance 或 LaTeX 源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b45 状态 `closed`、无问题；正式 review receipts 更新并生成 `reports/phase2-b45.md`，manifest revision 3887。
- 阶段修改文件：四卷 review receipts、manifest 状态投影、本批报告与本进度文件；忽略工作项和临时 PNG 待清理。
- 已完成子阶段：清除四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个；每卷保留四份 PDF、0 个非 PDF。`.work/phase2-b45/` 工作项与 `/tmp/gk-phase2-b45-review.bpWipZ/` 临时页面/接触表/候选 PNG 已移入系统废纸篓，两路径确认不存在。
- 阶段验证：四卷 build 目录逐卷核验为 4 PDFs、0 非 PDF；四卷 PDF 均保留。
- 阶段修改文件：本进度文件及四卷 build 目录中的忽略编译产物；未删除源文件或 PDF。
- 已完成子阶段：b45 scoped gates 全通过：source manifest validate；生成器 `--check` 显示 4 卷一致；build receipts 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 阶段验证：五项 scoped gates 均退出码 0，批次维持 `closed`。
- 阶段修改文件：本进度文件；门禁检查未产生额外内容源改动。
- 已完成子阶段：`report.py render --all` 以一个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认投影与全量 manifest 当前一致，并保留未完成状态。
- 阶段验证：全量报告 render/check 均退出码 0。
- 阶段修改文件：全量报告/README 投影、本批报告及本进度文件；尚待最终 diff 审核确认完整范围。
- 已完成子阶段：最终 diff 审核确认 17 个 tracked 文件，范围仅含四卷 build/review receipts、manifest、全量报告/README 投影、本批报告及本进度文件；无题目/答案/provenance/LaTeX 源或代码改动。`git diff --check` 通过，四卷 16 份 PDF 保留。
- 验证快照：manifest revision 3887；b45 `closed`，82 页、656 项视觉检查通过，0 warning exemption。全库批次状态：closed 64、closed_with_blockers 17、compiled_pending_review 55、provenance_verified 2；试卷 production state：complete 136、compiled 87、blocked 45、editions_generated 4。该快照只反映当前进度，不代表全库完成。
- 已完成阶段：b45 内容与报告投影提交 `9e7767b7`（`docs: 完成1958京滇川苏四卷复核`）；未 push。
- 下一批：manifest 顺序为 `phase2-b46`（1958 湖北、湖南、东北、华东四卷），当前 `compiled_pending_review`。
- 下一步：单独提交本进度记录；随后检查并继续 b46。

### `phase2-b46` — 1958 湖北、湖南、东北、华东

- 预检完成：起始 manifest revision 3887；source manifest validate 通过（775 项）；批次 issue 列表为空；生成器 `--check` 显示四卷输出一致。
- provenance 共 28 题（湖北 5、湖南 8、黑龙江吉林辽宁 8、华东 7），逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用既有转录与解题/盲核结果，不重做内容。
- 四份固定来源 PDF 均为 ready、各 1 页；来源路径依次为 `普通高考/1958/1958湖北.pdf`、`普通高考/1958/1958湖南.pdf`、`普通高考/1958/1958黑龙江,吉林,辽宁.pdf`、`普通高考/1958/1958华东(上海,福建).pdf`。
- `provenance.py status` 显示四卷 `editions_generated`、批次 `provenance_verified`；缓存状态仍为 compiled/compiled_pending_review。旧 build receipts 四卷均因生成输入树与工具链指纹变化 stale，review receipts 随 build 失效。
- 四卷现有四版 PDF 页数分别为湖北 1/8/2/7（18）、湖南 1/7/2/5（15）、东北 1/7/2/6（16）、华东 2/10/3/7（22），共 71 页；每卷 build 目录仅含四版 PDF，无编译中间物。无题目、答案或 provenance 变更需求。
- 阶段修改文件：仅本进度文件；预检未更改来源、manifest、provenance 或试卷内容。
- 已完成子阶段：正式构建四卷四版完成，manifest revision 3889；页数与既有 PDF 相同，共 71 页。Build attempts：湖北 `bf8ac118-14d3-496e-a2cc-7ac30dc0c16f`、湖南 `d638bc82-8185-41c1-8b48-a3d3f75601cf`、东北 `fc9177a5-1544-47b2-a762-a3f66f6fe1d6`、华东 `1fbc335b-b101-476d-ac4c-2cf17ab70356`。四卷均无 failed/missing-character/Overfull warning；build receipt 校验无 failed/invalid/missing/stale，pending review 为预期状态。
- 阶段修改文件：本进度文件、四卷 build receipts/PDF；未更改题目源、答案或 provenance。
- 已完成子阶段：`prepare-batch` 建立 16 个当前 attempt review work items，覆盖四卷 × 四版。
- 阶段验证：16 个工作项均与本轮 build attempt 配对，待复核页数共 71 页。
- 阶段修改文件：本进度文件及忽略的 `.work/phase2-b46/review/` 工作项；未改题目、答案、provenance 或生成源。
- 已完成子阶段：将四卷四版 PDF 全部渲染为 71 张页面图，并生成 16 张接触表。初次 montage 因 ImageMagick 未解析字体名失败；确认系统字体存在后改用 `/System/Library/Fonts/Helvetica.ttc`，单张探测和全部接触表生成均成功，没有重跑构建。
- 阶段验证：页面图覆盖 71/71 页，16 张接触表均生成；当前临时渲染目录为 `/tmp/gk-phase2-b46-review.EBlT0A/`。
- 阶段修改文件：仅本进度文件；页面图/接触表为临时 PNG。
- 已完成子阶段：16 张接触表逐页覆盖全部 71 页；16 个候选页均完成 120dpi 高分辨率复核。发现湖北解析版第 6 页末尾仅余“附加题 6”标题、第 7 页才开始对应解析正文；该问题仅涉及分页，其他已检页面未见视觉缺陷。
- 阶段验证：接触表覆盖 71/71 页；候选页复核 16/16，其中 15 页确认通过，湖北解析版候选页记录一项待修版式问题；另将第 7 页以 120dpi 补充核对以确认跨页关系。
- 阶段修改文件：本进度文件；原始页面图、接触表和候选图位于临时目录/忽略 `.work`；尚未修改试卷源。
- 已完成子阶段：定位到 `1958_湖北/answers.tex` 中“附加题 6”标题前的分页保护不足；在标题前增加 `\Needspace{5\baselineskip}`，只约束分页，不改题目、解答文字或结论。
- 阶段修改文件：本进度文件、`1958_湖北/answers.tex`；修复尚待正式重建和视觉复核验证。
- 已完成子阶段：湖北卷四版正式重建，manifest revision 3891；build attempt `53e2fe5c-1d39-4b30-96f3-935aac5bb40f`。四版页数仍为 1/8/2/7，共 18 页，0 warning，构建成功。
- 阶段验证：`validate-receipts` 对湖北卷无 failed/invalid/missing/stale；原题面/答案内容未改，打印版页数不变；分页修复待视觉复核验证。
- 阶段修改文件：`1958_湖北/answers.tex`、湖北 build receipt/PDF、manifest、本进度文件。
- 已完成子阶段：恢复时先核对 Git diff 与本进度记录；旧 b46 review 工作项共 16 份、覆盖 71 页，全部为 pending 模板，无检查结果、批注或候选页覆盖修改。将旧 review 工作项目录移入系统废纸篓（可恢复），按 manifest revision 3891 的当前 attempt 重新 `prepare-batch`，成功生成 16 份工作项、覆盖 71 页。
- 阶段验证：新工作项已绑定湖北重建后的当前 build；未改动湖南、东北、华东 PDF 或源文件。旧模板仅可从系统废纸篓恢复。
- 阶段修改文件：忽略的 `.work/phase2-b46/review/` 工作项及本进度文件；未改题目、答案、provenance 或生成源。
- 已完成子阶段：重渲染湖北四版 18 页并生成 4 张接触表；修复后解析版第 6 页已完整收束附加题 5，第 7 页从附加题 6 开始。不过 120dpi 复核发现第 7 页末尾另有“附加题 8／解析”孤立标题，故不将此次视觉验证判为通过。
- 阶段验证：湖北四版图像共 18 页、4 张接触表；修复目标第 6–7 页实图已核对。初次批量渲染无输出的根因是 zsh 不对未加引号的标量作预期分词，致 edition 与 candidate 页码连成一个路径；改为明确的 edition 循环后渲染成功。
- 阶段修改文件：仅本进度文件；临时图像在 `/tmp/gk-phase2-b46-review.EBlT0A/rebuild/`。
- 已完成子阶段：在“附加题 8”标题前增加 `\Needspace{5\baselineskip}`，只约束分页、不改题目或解答内容；待再次构建及视觉复核。
- 阶段修改文件：`1958_湖北/answers.tex`、本进度文件。
- 已完成子阶段：湖北四版再次正式重建，manifest revision 3893；新 build attempt `7727ac7d-cccc-4667-b4a1-ad7f5ad4a188`，四版均 succeeded、0 warning，页数仍为试题版 1、解析版 8、简答版 2、印刷版 7（18 页）。
- 阶段验证：正式 build 汇总无 failed；修复仅在解析版答案源增加分页保护，其他内容未改。视觉复核尚待完成。
- 阶段修改文件：`1958_湖北/answers.tex`、湖北 build receipt/PDF、manifest、本进度文件。
- 已完成子阶段：当前 attempt 下湖北四版重新渲染 18 页并生成 4 张新版接触表；湖北候选页（印刷版 5、简答版 1、解析版 6、试题版 1）均完成 120dpi 复核，解析版第 7、8 页另做高分辨率复核。第 6 页附加题 5 收束完整，第 7 页附加题 6、7 内容完整，第 8 页附加题 8 正文完整，未见孤立标题、裁切、缺字或答案串版。
- 阶段验证：结合其他三卷未变 PDF 的 12 张既有接触表/候选页复核，覆盖全批 71/71 页与 16/16 候选页；所有页面通过。无警告需要豁免。
- 阶段修改文件：仅本进度文件；更新后的湖北渲染图位于 `/tmp/gk-phase2-b46-review.EBlT0A/rebuild2/`，其他卷复用已检查图像。
- 已完成子阶段：当前 16 份 review work items 全部绑定最终 build attempt、PDF SHA-256 与页数；登记 71 页 × 8 项共 568 条 pass 检查，候选页结论注明 120dpi，其余页面注明接触表逐页复核。
- 阶段验证：工作项核验 16/16，覆盖 71 页；所有页面与检查均 pass，0 pending、0 non-pass，且无 warning exemption。`check-batch` 当前仅报告正式 review receipts 仍绑定旧 build（attempt、输入树、依赖、工具链/视觉工具指纹及 PDF 已变化），这是 finalize 刷新正式回执前的预期状态。
- 阶段修改文件：忽略的 `.work/phase2-b46/review/` 下 16 份工作项及本进度文件；未改题目内容或 provenance。
- 阶段发现与修复：首次 finalize 被 artifact stale 门禁拒绝。根因是生成器规定 `answers.tex` 为派生文件、禁止手改；generator `--check` 发现差异后，已将纯分页指令移入规范源 `1958/1958_湖北_数学真题_解析正文.md` 的附加题 6/8 前，并完成规范重生成、正式重编和最终视觉复核。
- 阶段修改文件：规范解析正文、其派生 `answers.tex` 与本进度文件；派生文件已由生成器更新并通过一致性检查。
- 已完成子阶段：从规范解析正文运行单卷 generator `--write`，原子更新 3 个派生目标；随后单卷 `--check` 通过，b46 全批 generator `--check` 也通过。
- 已完成子阶段：湖北再次正式构建，manifest revision 3895；build attempt `a491993a-e0e1-45c0-b560-45dced498262`，四版 succeeded、共 18 页、0 warning。此 attempt supersedes `7727ac7d-cccc-4667-b4a1-ad7f5ad4a188`。
- 阶段修改文件：规范解析正文、湖北派生 TeX/index、湖北 build receipt/PDF、manifest 与本进度文件。
- 已完成子阶段：针对最终 attempt `a491993a-e0e1-45c0-b560-45dced498262` 重渲染湖北四版 18 页并生成 4 张接触表；全部接触表及湖北 4 个候选页（另复查解析版第 7、8 页）重新目视通过。解析版第 6 页末附加题 5 结束，第 7 页完整呈现附加题 6、7，第 8 页完整呈现附加题 8。
- 阶段验证：全批 71/71 页与 16/16 候选页复核通过；湖北新版无裁切、孤立标题、缺字或异常留白。三卷其余 PDF 未改变，沿用已完成的逐页视觉核查。
- 阶段修改文件：仅本进度文件；当前湖北截图位于 `/tmp/gk-phase2-b46-review.EBlT0A/final/`。
- 已完成子阶段：按最终 build attempt 重新生成 16 份工作项；保存旧工作项备份，恢复三卷未变的 12 份 pass 记录，仅以最终湖北 PDF 重建 4 份工作项并登记 18 页 × 8 项共 144 条 pass。最终核验 16/16 工作项、71 页、568 项均 pass，0 pending/non-pass；build receipt 校验无 failed/invalid/missing/stale。
- 阶段验证：逐项比对当前 attempt、PDF 路径/页数/SHA-256；湖北 4 份绑定 `a491993a-e0e1-45c0-b560-45dced498262`，其余三卷原 12 份仍绑定各自当前 attempt。`check-batch` 仍报告正式 review receipts 旧于当前构建，这是 finalize 应刷新前的预期状态。
- 阶段修改文件：忽略的 `.work/phase2-b46/review/` 当前工作项与 `review-before-a491993a/` 旧记录备份、本进度文件。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b46 状态 `closed`、无问题；四卷正式 review receipts 与当前 build 对齐，并生成 `reports/phase2-b46.md`，manifest revision 3896。
- 阶段修改文件：四卷 review receipts、manifest 状态投影、本批报告与本进度文件；忽略工作项和临时 PNG 在后续清理子阶段已移入废纸篓。
- 已完成子阶段：清理四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个；每卷现仅保留四版 PDF、0 个非 PDF。b46 `.work` 下 32 份工作项/备份及本次临时渲染目录中的 189 张 PNG 均移入系统废纸篓（可恢复），路径确认不存在。
- 阶段验证：逐卷核验 4 PDFs、0 intermediates；PDF 未删除；工作项与临时图像已清理。
- 阶段修改文件：本进度文件及四卷 build 目录内忽略的编译产物；未删除源文件或 PDF。
- 已完成子阶段：五项 b46 scoped gates 全部通过：source manifest validate；generator `--check` 显示四卷一致；build receipts 四卷 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3896，b46 状态 `closed`。
- 阶段修改文件：本进度文件；门禁检查未产生额外内容源改动。
- 已完成子阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认与当前全量 manifest 一致，并保留未完成状态。
- 阶段验证：全量报告 render/check 均成功退出。
- 阶段修改文件：全量 README/报告投影、本批报告与本进度文件；最终审核确认 b46 内容提交共 18 个非进度跟踪文件。
- 已完成阶段：b46 内容、正式回执及报告投影提交 `7ed0318e`（`docs: 完成1958鄂湘东北华东四卷复核`）；未 push。
- 阶段关闭快照：manifest revision 3896；b46 `closed`，四卷 complete、71 页、568 项视觉检查通过，0 warning exemption。16 份 PDF 保留，编译目录仅 PDF；工作项/临时 PNG 已移入系统废纸篓。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段只关闭 b46，不代表全库完成。
- 已完成阶段：b46 独立进度记录提交 `b654c2c3`（`docs: 记录b46完成进度`）；未 push。
- 下一步：检查并预检 manifest 下一批 `phase2-b47`。

### `phase2-b47` — 1958 广东、安徽、不明卷

- 预检完成：起始 manifest revision 3896；批次问题列表为空；source manifest validate 通过；生成器 `--check` 显示三卷生成输出一致；provenance status 显示三卷 `editions_generated`、批次 `provenance_verified`。
- provenance 共 22 题（广东 9、安徽 5、不明卷 8），逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；按既有转录与盲核结果继续，不重做内容。
- 三份固定来源 PDF 均为 ready：广东原卷 6 页、安徽（来源网络、真实性存疑）1 页、不明卷（可能与云南部分同源）7 页。安徽与不明卷身份说明保留，不扩大来源断言。
- 既有四版 PDF 页数依次为广东 3/14/4/11（32）、安徽 1/10/2/8（21）、不明卷 1/10/2/7（20），共 73 页；无新增题目/答案/provenance 修改需求。
- 当前 build receipts 因生成输入树及工具链指纹变化 stale，需正式重建；正式构建、逐页视觉复核、finalize、清理、门禁、报告投影和提交待完成。
- 阶段修改文件：仅本进度文件；预检未更改试卷源、manifest、provenance 或 PDF。
- 已完成子阶段：三卷四版正式构建完成，manifest revision 3898，共 73 页。Build attempts：广东 `1583f07a-fc55-45a3-9207-c365348e8d3f`、安徽 `9e527efd-31a6-4226-bc3e-c611efc18f91`、不明卷 `6d64f1c4-0f4e-439a-94ef-c93ff8146a25`。四版均 succeeded，页数与原 PDF 相同，0 warning。
- 阶段验证：build receipt validator 无 failed/invalid/missing/stale；3 套待视觉复核状态符合预期。
- 阶段修改文件：本进度文件、三卷 build receipts/PDF；未更改题目、答案或 provenance。
- 已完成子阶段：`prepare-batch` 建立 12 个当前 attempt review work items；渲染并检查 12 张接触表覆盖全部 73 页。
- 已完成子阶段：12 个候选页均完成 120dpi 逐张复核；广东、存疑安徽与不明卷的版头/来源说明均如实显示，未见裁切、缺字、图形遮叠、异常分页或串版。
- 阶段验证：接触表覆盖 73/73 页；候选页复核 12/12 通过；三卷构建均无 warning。安徽与不明卷不确定来源标签在题面及解析版页面可见。
- 阶段修改文件：仅本进度文件；接触表、候选图与工作项分别在 `/tmp/gk-phase2-b47-review.sBQahI/` 与忽略的 `.work/phase2-b47/review/`；未改题目、答案、provenance 或生成源。
- 已完成子阶段：核对 12 份 work items 全部绑定当前 attempt、PDF SHA-256 与页数；登记 73 页 × 8 项共 584 条 pass 检查，候选页说明 120dpi 复核，其余说明逐页接触表复核。
- 阶段验证：12/12 工作项、73 页全部绑定正确，584 项 pass、0 pending/non-pass、0 warning exemption。`check-batch` 仅报告正式 review receipts 仍绑定旧 build，为 finalize 刷新前预期状态。
- 阶段修改文件：本进度文件及忽略的 `.work/phase2-b47/review/` 下 12 份工作项；未更改题目、答案、provenance 或生成源。
- 已完成子阶段：`finalize-batch` 返回 `FINALIZED`，b47 `closed`、无问题；三卷正式 review receipts 与当前 build 对齐，并生成 `reports/phase2-b47.md`，manifest revision 3899。
- 阶段修改文件：三卷 review receipts、manifest 状态投影、本批报告与本进度文件；工作项/PNG 已在后续清理子阶段移入废纸篓。
- 已完成子阶段：三卷 build 目录各移除 24 个非 PDF 编译中间物，共 72 个；每卷保留 4 份 PDF、0 个非 PDF。12 份 `.work/phase2-b47/` 工作项与 `/tmp/gk-phase2-b47-review.sBQahI/` 下 97 张 PNG 已移入系统废纸篓（可恢复），路径确认不存在。
- 阶段验证：逐卷核验 4 PDFs、0 intermediates；PDF 保留，临时审查产物已清理。
- 阶段修改文件：本进度文件及三卷 build 目录里的忽略编译产物；未删除源文件或 PDF。
- 已完成子阶段：五项 b47 scoped gates 全部通过：source manifest validate；generator `--check` 显示三卷一致；build receipts 三卷 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：3 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3899，b47 `closed`。
- 阶段修改文件：本进度文件；门禁检查未产生额外内容源改动。
- 已完成子阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认与当前全量 manifest 一致，并保留未完成状态。
- 阶段验证：全量报告 render/check 均成功退出。
- 阶段修改文件：全量 README/报告投影、本批报告与本进度文件；最终审核确认 b47 内容提交共 14 个非进度跟踪文件。
- 已完成阶段：b47 内容、正式回执及报告投影提交 `09c764b0`（`docs: 完成1958粤皖不明卷三卷复核`）；未 push。
- 阶段关闭快照：manifest revision 3899；b47 `closed`，三卷 complete、73 页、584 项视觉检查通过，0 warning exemption。12 份 PDF 保留，编译目录仅 PDF；工作项/临时 PNG 已移入系统废纸篓。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段仅关闭 b47，不代表全库完成。
- 已完成阶段：b47 独立进度记录提交 `29613c7a`（`docs: 记录b47完成进度`）；未 push。
- 下一步：预检 manifest 下一批 `phase2-b48`。

### `phase2-b48` — 1978 全国、1979 全国文理、1980 全国理科

- 预检完成：起始 manifest revision 3899；批次问题列表为空；source manifest validate 通过；生成器 `--check` 显示四卷输出一致；provenance status 显示四卷 `editions_generated`、批次 `provenance_verified`。
- provenance 共 34 题（1978 全国 7、1979 理科 10、1979 文科 8、1980 理科 9），逐题 transcription review 均 passed、答案证据均 A、conflict 均 none；复用已完成的转录与盲核，不重做内容。
- 四份固定来源 PDF 均为 ready、各 1 页；四卷均登记 1 份 TikZ 图稿。
- 既有四版 PDF 页数依次为 1978 全国 2/13/3/9（27）、1979 理科 2/12/3/8（25）、1979 文科 2/11/3/7（23）、1980 理科 2/15/3/10（30），共 105 页；无新增题目/答案/provenance 修改需求。
- 已完成子阶段：四卷四版正式构建完成，manifest revision 3901，共 105 页。Build attempts：1978 全国 `35ea8128-8b40-41c1-9c8a-a9a47883c1bb`、1979 理科 `068dc0fd-988d-41bd-b2ab-7521acec5806`、1979 文科 `b300937a-6147-4172-823d-8abea0979dbd`、1980 理科 `7a893ad1-492b-4077-b0c4-515e0177cd7d`。四卷各版均 succeeded，页数与既有 PDF 相同；总计 6 条 log warning、0 build failure。
- 警告明细：1978 试题/解析/简答版同一处 Underfull hbox（badness 1953，行 10–11，width 未知）；1979 理科解析版 Overfull 33.71384pt（行 457）；1980 理科印刷版 Overfull 23.20967pt（行 69–70、467–468）；1979 文科无 warning。
- 阶段验证：build receipt validator 无 failed/invalid/missing/stale；警告待联系具体 PDF 页做视觉核查后决定精确豁免或纯版式修复。
- 阶段修改文件：本进度文件、四卷 build receipts/PDF；未更改题目、答案、provenance 或图稿。
- 阶段修改文件：仅本进度文件；预检未更改试卷源、manifest、provenance、图稿或 PDF。
- 已完成子阶段：当前 build attempt 下准备 16 份 work items；已渲染 105 页并检查 16 张接触表，逐页覆盖四卷四版全部 105 页；16 个候选页均完成 120dpi 复核。没有发现缺字、裁切、图稿缺失/遮挡、孤立标题、答案串版或妨碍阅读的分页异常。
- 已完成子阶段：6 条构建警告均已精确映射并目视复核。1978 全国三版 Underfull（`answers.tex` 行 10–11）在各版第 1 页，警告段为编注，三页均无异常留白/断行问题；1979 理科解析版 Overfull（`answers.tex` 行 457）为解析版第 12 页特值复算的行间公式，公式未裁切且可读；1980 理科印刷版 Overfull（行 69–70、467–468）为附加题 10 同一参数方程段在题面第 2 页与解析第 8 页的两次呈现，文字/方程均完整、未越出页面或妨碍阅读。均判定无需改源，按精确页面与 warning 指纹记录豁免。
- 阶段验证：16/16 接触表、覆盖 105/105 页；16/16 候选页通过；另对警告关联的 1978 三版第 1 页、1980 印刷版第 2 页和候选图中的解析版第 8 页做高分辨率核查，所有 6 条警告均对应到实际版面且无视觉缺陷。1979 理科解析版第 12 页候选图已核对。
- 阶段修改文件：本进度文件；16 份忽略的 `.work/phase2-b48/review/` 工作项；警告页补充渲染图及既有 105 页渲染图均在 `/tmp/gk-phase2-b48-review.Am8DGu/`；未更改题目、答案、provenance、生成源或 PDF。
- 已完成子阶段：16 份当前 attempt work items 均已登记，覆盖 105 页 × 8 项，共 840 条 pass；候选页记录 120dpi 核验，其余页记录接触表逐页核验。对 6 条警告分别登记精确 warning 指纹、源文件、PDF 页码及目视结论（1978 三条 p1；1979 理科解析 p12；1980 印刷 p2/p8）。
- 阶段验证：工作项结构核验 16/16，105 页及 840 项全部 pass、0 pending/non-pass；6 条 warning exemption 均绑定当前 build warning 的 edition/kind/box/lines/width_pt，无新增题目内容或版式修改。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b48/review/` 下 16 份工作项。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b48 状态 `closed`、无问题；正式 review receipts 与当前四卷 build attempts 对齐，并生成 `reports/phase2-b48.md`，manifest revision 3902。
- 阶段验证：批次 4 卷、105 页、840 项视觉检查全部通过；6 条当前 warning 均有对应页面和视觉证据豁免，无失败项。
- 阶段修改文件：四卷正式 review receipts、manifest 批次状态投影、本批报告与本进度文件；忽略 `.work` 和临时 PNG 尚待清理。
- 已完成子阶段：四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个，均移入系统废纸篓；每卷保留 4 份 PDF、0 个非 PDF。16 份 `.work/phase2-b48/` work items 与本次 142 张临时 PNG 也移入系统废纸篓；对应路径已确认不存在。
- 阶段验证：逐卷核验 4 PDFs、0 intermediates；PDF 未删除，TeX/规范源文件未触动；临时工作项和图像已清理。
- 阶段修改文件：本进度文件及四卷 build 目录的忽略编译产物；删除操作可从系统废纸篓恢复。
- 已完成阶段：五项 b48 scoped gates 全部通过：source manifest validate；generator `--check` 四卷一致；build receipts 为 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3902，b48 `closed`。
- 阶段修改文件：仅本进度文件；门禁检查未产生额外内容源改动。
- 已完成阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，并保留整个语料库的未完成状态。
- 阶段验证：全量报告 render/check 均成功退出；b48 scoped gates 仍全部通过。
- 阶段修改文件：全量 README/报告投影、本批报告、四卷 receipts、manifest 与本进度文件；未更改转录/答案/provenance 内容。
- 已完成阶段：b48 内容、正式回执与全量报告投影提交 `f48d6a1d`（`docs: 完成1978-1980全国四卷复核`）；未 push。
- 已完成阶段：b48 独立进度记录提交 `84450b43`（`docs: 记录b48阶段进度`）；未 push。提交后工作树干净。
- 阶段关闭快照：manifest revision 3902；b48 `closed`，4 卷、105 页、840 项视觉检查通过，6 条 warning 均有精确页面豁免；16 份 PDF 保留、编译目录仅 PDF。仅关闭 b48，不代表全库完成。

### `phase2-b49` — 1980 全国文、1981 全国文理、1982 全国理科

- 预检完成：起始 manifest revision 3902；批次 issues 为空；source manifest validate 通过；generator `--check` 显示四卷一致；provenance status 为四卷 `editions_generated`、批次 `provenance_verified`。
- 本批 34 题（1980 文科 8、1981 理科 9、1981 文科 9、1982 理科 8），沿用已登记的转录/解题与 provenance，不重复录入；四份固定来源 PDF 在 manifest 中均为 `ready`，每份 1 页且 artifact PDF 校验通过。图稿数依次为 1、1、0、3。
- 既有四版 PDF 页数依次为 1980 文科 2/13/3/7（25）、1981 理科 2/15/3/11（31）、1981 文科 2/12/3/9（26）、1982 理科 3/17/4/14（38），共 120 页。
- Build receipt validator 显示四卷均 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；下一步须正式重建四卷四版，再检查警告与复核状态。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 已完成阶段：四卷四版正式构建成功，manifest revision 3904，共 120 页；build attempts：1980 文科 `c71247bf-782f-48ef-bf92-35ab9f9c2e6d`、1981 理科 `c77d396d-7ac4-4945-af2a-68e53b9216e7`、1981 文科 `d28aa96a-f599-450f-a40c-d42b24084645`、1982 理科 `3ad22d09-fd29-45b9-9365-89c3c2d3bc04`。四版页数与原 PDF 完全一致；无 build failure。
- 阶段验证：build receipt validator `OK`，4 套均 succeeded，0 failed/invalid/missing/stale；当前处于 `compiled_pending_review`。共 11 条 Overfull warning：1980 文科解析 1；1981 理科试题 1、解析 6、简答 1；1981 文科解析 2；1982 理科 0。
- 阶段修改文件：本进度文件、四卷 build receipts/PDF；未更改题目、答案、provenance、图稿或生成源。
- 已完成子阶段：为四卷当前 build attempts 生成 16 份 review work items，覆盖 120 页，均为 pending。准备前 `.work/phase2-b49/review/` 已有旧 attempt 工作项；脚本仅允许旧 attempt 工作项被新 attempt 替换，并会拒绝覆盖同 attempt 文件。本次构建已使旧回执失效，故不复用旧 attempt 的视觉结论。
- 阶段验证：16/16 工作项绑定四个当前 attempt 与当前 PDF 页数；旧 attempt 工作项不适用于新 PDF。
- 阶段修改文件：仅本进度文件与忽略的 `.work/phase2-b49/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：当前 attempt 的 120 页已渲染为 16 张接触表，并完成逐页浏览；暂未见明显裁切、缺图、孤立标题、答案串版或异常分页。
- 阶段验证：接触表覆盖 120/120 页；16/16 接触表已检查。警告页和候选页仍待高分辨率复核，当前不提前登记视觉通过。
- 阶段修改文件：本进度文件；16 张接触表和 120 页预览位于临时目录 `/tmp/gk-phase2-b49-review.h4xEYl/`；未更改试卷源或 PDF。
- 已完成子阶段：16 个候选页均完成 120dpi 复核，未见裁切、公式/图稿缺陷、缺字或异常分页。
- 已完成子阶段：按当前 attempt 的 XeLaTeX warning 上下文、源行和 PDF 文本逐项映射 11 条警告：1980 文科解析行 400–402 → p11；1981 理科行 120 → 试题/解析/简答 p2，行 82 → 解析 p4，行 217 → p6，行 244 → p7，行 468 → p10，行 546 → p12；1981 文科解析行 166 → p5、行 358–359 → p8。高分辨率 warning-page 检查待完成。
- 阶段验证：候选页 16/16 通过；warning 页码由构建日志、TeX 源行及 `pdftotext` 页文本相互核对，未沿用旧 review receipt 页码。
- 阶段修改文件：仅本进度文件；高分辨率候选图及接触表位于 `/tmp/gk-phase2-b49-review.h4xEYl/`；未更改试卷源或 PDF。
- 已完成子阶段：高分辨率复核全部 warning 关联版面。1980 文科解析 p11、1981 理科解析 p2/p4/p6/p7/p10/p12、1981 文科解析 p5/p8 均完整可读；另检查 1981 理科试题与简答 p2。公式、答案框、长行与附加题图形均未裁切，没有需改源的视觉问题。
- 阶段验证：warning 关联页面逐一核对通过，11 条 warning 均可按实际页码作视觉豁免；候选页 16/16 和全卷接触表 120/120 的既有检查结论保持有效。
- 阶段修改文件：仅本进度文件；9 张 warning 补充图位于 `/tmp/gk-phase2-b49-review.h4xEYl/`，既有试题/简答 p2 图亦在该临时目录；未更改试卷源或 PDF。
- 已完成子阶段：16 份当前 attempt 工作项登记完成，覆盖 120 页 × 8 项 = 960 项 pass；11 条 warning exemption 均精确绑定当前 warning 指纹、源文件及 PDF 页码，视觉结论均为 pass。
- 阶段验证：工作项汇总为 16/16、120 页、960 pass、0 pending、11 exemptions；`git diff --check` 通过。`check-batch` 在 finalize 前仍指出正式 review receipt 绑定旧 build attempt 等状态，属刷新前预期，待 finalize 写入当前正式回执。
- 阶段修改文件：本进度文件；忽略的 `math-gaokao-latex/.work/phase2-b49/review/` 下 16 份工作项；未修改试卷源、答案、provenance 或 PDF。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b49 状态 `closed`、无问题；正式 review receipts 与四卷当前 build attempts 对齐，报告 `reports/phase2-b49.md` 已写入，manifest revision 3905。
- 阶段验证：4 卷、120 页、960 项视觉检查全部通过，11 条当前 build warning 均有精确页面及视觉豁免；无失败项。
- 阶段修改文件：四卷正式 review receipts、manifest 批次状态投影、本批报告与本进度文件；忽略工作项及临时 PNG 尚待清理。
- 已完成子阶段：四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个，均移入系统废纸篓；每卷保留 4 份 PDF、0 个非 PDF。16 份 `.work/phase2-b49/review/` 工作项与临时审阅目录 `/tmp/gk-phase2-b49-review.h4xEYl/`（共 161 张 PNG）也移入系统废纸篓，路径确认不存在。
- 阶段验证：逐卷核验 4 PDFs、0 intermediates；PDF 保留，LaTeX 源与正式回执未删除；忽略工作项与临时图像已清理，操作可从系统废纸篓恢复。
- 阶段修改文件：本进度文件及四卷 build 目录中的忽略编译产物；未删除源文件或 PDF。
- 已完成阶段：五项 b49 scoped gates 全部通过：source manifest validate；generator `--check` 四卷一致；build receipts 为 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3905，b49 `closed`。
- 阶段修改文件：仅本进度文件；门禁检查未产生额外内容源改动。
- 已完成阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，并保留整个语料库的未完成状态。
- 阶段验证：全量报告 render/check 均成功退出；b49 五项 scoped gates 仍全部通过。
- 阶段修改文件：全量 README/报告投影、本批报告、四卷 build/review receipts、manifest 与本进度文件；未更改试卷转录、答案、provenance 或 LaTeX 源。
- 已完成阶段：b49 内容、正式回执与全量报告投影提交 `4e8e712a`（`docs: 完成1980-1982全国四卷复核`）；未 push。
- 阶段关闭快照：manifest revision 3905；b49 `closed`，4 卷、120 页、960 项视觉检查通过，11 条 warning 均有精确页面豁免；16 份 PDF 保留，编译目录仅 PDF；转录/答案/provenance/LaTeX 源未更改。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段只关闭 b49，不代表全库完成。
- 已完成阶段：b49 独立进度记录提交 `e1783ef8`（`docs: 记录b49阶段进度`）；未 push。提交后工作树干净。

### `phase2-b50` — 1982 全国文、1983 全国文理、1984 全国理科

- 预检完成：起始 manifest revision 3905；批次 issues 为空；source manifest validate 通过；generator `--check` 显示四卷一致；provenance status 为四卷 `editions_generated`、批次 `provenance_verified`。
- 本批 55 题（1982 文科 9、1983 理科 13、1983 文科 13、1984 理科 20），沿用已登记转录/解题与 provenance，不重复录入；四份固定来源 PDF 均为 `ready`，每份 1 页且 PDF artifact 校验通过。四卷 `legacy_ids=[]`。
- 既有四版 PDF 页数依次为 1982 文科 2/15/3/11（31）、1983 理科 3/20/4/14（41）、1983 文科 3/19/4/14（40）、1984 理科 3/19/4/15（41），共 153 页。
- Build receipt validator 显示四卷均 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；manifest 当前批次仍为 `compiled_pending_review`。下一步须正式重建四卷四版，再检查警告与复核状态。
- 阶段修改文件：仅本进度文件；只读预检未更改试卷源、manifest、provenance、图稿或 PDF。
- 已完成阶段：四卷四版正式构建成功，manifest revision 3907，共 153 页；build attempts：1982 文科 `ad6ead08-5ebd-494a-97a3-fb50702babc2`、1983 理科 `58951bd6-388d-480a-9735-54b79b901bcb`、1983 文科 `753e5d37-6c2b-4638-84a8-69bda776d143`、1984 理科 `e8c80b25-f7d6-491b-bdea-c8073456df15`。四版页数与构建前既有 PDF 完全一致；无 build failure。
- 阶段验证：build receipt validator `OK`，四卷均成功、0 failed/invalid/missing/stale，当前为 4 pending review。共 1 条 Overfull warning：1983 理科解析版行 424、45.68964pt；其他三卷及其余版本无 warning。
- 阶段修改文件：本进度文件、四卷 build receipts/PDF；未更改题目、答案、provenance、图稿或生成源。
- 已完成子阶段：`prepare-batch` 为四个当前 build attempts 生成 16 份 review work items，覆盖 153 页；共 1 条待核 warning，所有 1,224 个页面检查项初始为 pending。
- 阶段验证：16/16 工作项均绑定正确 attempt 与当前 PDF SHA-256/页数；每页八项齐全，覆盖 153/153 页。
- 阶段修改文件：本进度文件与忽略的 `math-gaokao-latex/.work/phase2-b50/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：153 页已渲染为 16 张接触表并完成逐页浏览；未见明显缺页、裁切、缺图或串版。唯一 warning 为 1983 理科解析版 `answers.tex` 行 424、Overfull hbox 45.68964pt，经源行和 PDF 文本定位至解析版 p11 的三角恒等式长公式。
- 阶段验证：接触表覆盖 153/153 页，16/16 接触表已检查；warning 对应 p11 的定位已由日志、源行和 PDF 文本交叉确认，尚待高分辨率目视结论。
- 阶段修改文件：仅本进度文件；接触表及 153 页预览位于 `/tmp/gk-phase2-b50-review.nHjJJW/`；未更改试卷源或 PDF。接触表工具初次因 ImageMagick 默认字体未配置而失败，确认原因后显式指定系统 Arial 字体，未重做 PDF 渲染。
- 已完成子阶段：16 个候选页均完成 120dpi 复核；另高分辨率检查 1983 理科解析版 p11 warning 页。各页字形、标题题号、选项公式、图稿标注、页眉页脚、分页留白、字号与答案泄漏均无可见问题；warning 公式完整可读、未裁切且不妨碍阅读，无需改源。
- 阶段验证：候选页 16/16 通过；唯一 warning 的 PDF 页码为 p11，由构建日志、`answers.tex:424` 和页面文本/高分辨率图像相互确认，可作精确视觉豁免。
- 阶段修改文件：仅本进度文件；16 张候选图及 warning 页图位于 `/tmp/gk-phase2-b50-review.nHjJJW/candidates/`；未更改试卷源或 PDF。
- 已完成子阶段：16 份当前 attempt work items 均已登记，覆盖 153 页 × 8 项共 1,224 条 pass；唯一 warning exemption 精确绑定 Overfull/hbox、源行 424、宽度 45.68964pt、`answers.tex` 与 PDF p11，视觉结果 pass。
- 阶段验证：结构汇总 16/16 工作项、153 页、1,224 pass、0 pending、1 exemption；`git diff --check` 通过。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b50/review/` 下 16 份工作项。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b50 状态 `closed`、无问题；正式 review receipts 与四卷当前 build attempts 对齐，并生成 `reports/phase2-b50.md`，manifest revision 3908。
- 阶段验证：4 卷、153 页、1,224 项视觉检查全部通过；唯一当前 build warning 有精确页面及视觉豁免，无失败项。
- 阶段修改文件：四卷正式 review receipts、manifest 批次状态投影、本批报告与本进度文件；忽略工作项及临时 PNG 尚待清理。
- 已完成子阶段：四卷 build 目录各 24 个非 PDF 编译中间物，共 96 个，均移入系统废纸篓；每卷保留 4 份 PDF、0 个非 PDF。16 份 `.work/phase2-b50/review/` 工作项与 `/tmp/gk-phase2-b50-review.nHjJJW/` 临时审阅目录（186 张 PNG）也移入系统废纸篓，路径确认不存在。
- 阶段验证：逐卷核验 4 PDFs、0 intermediates；PDF 保留，LaTeX 源与正式回执未删除；忽略工作项及临时图像已清理，操作可从系统废纸篓恢复。
- 阶段修改文件：本进度文件及四卷 build 目录中的忽略编译产物；未删除源文件或 PDF。
- 已完成阶段：五项 b50 scoped gates 全部通过：source manifest validate；generator `--check` 四卷一致；build receipts 为 4 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：4 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3908，b50 `closed`。
- 阶段修改文件：仅本进度文件；门禁检查未产生额外内容源改动。
- 已完成阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，并保留整个语料库的未完成状态。
- 阶段验证：全量报告 render/check 均成功退出；b50 五项 scoped gates 仍全部通过。
- 阶段修改文件：全量 README/报告投影、本批报告、四卷 build/review receipts、manifest 与本进度文件；未更改试卷转录、答案、provenance 或 LaTeX 源。
- 已完成阶段：b50 内容、正式回执与全量报告投影提交 `5670311f`（`docs: 完成1982-1984全国四卷复核`）；未 push。
- 阶段关闭快照：manifest revision 3908；b50 `closed`，4 卷、153 页、1,224 项视觉检查通过，1 条 warning 有精确页面豁免；16 份 PDF 保留，编译目录仅 PDF；转录/答案/provenance/LaTeX 源未更改。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段只关闭 b50，不代表全库完成。
- 下一步：单独提交本进度记录；随后核对工作树并预检 manifest 下一批 `phase2-b51`。

### `phase2-b51` — 1984 全国文科

- 预检完成：起始 manifest revision 3908；批次仅含 `gk-1984-regular-arts`，issues 为空；source manifest validate 通过；generator `--check` 显示该卷一致；provenance status 为该卷 `editions_generated`、批次 `provenance_verified`。
- 本卷 17 题，固定来源 PDF 为 ready、1 页且 artifact PDF 校验通过，`legacy_ids=[]`。既有四版 PDF 页数为试题 2、解析 20、简答 3、印刷 15，共 40 页；沿用已登记转录/解题与 provenance，不重复录入。
- Build receipt validator 显示该卷 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；manifest 批次仍为 `compiled_pending_review`。下一步须正式重建四版，再检查 warning 与复核状态。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 已完成子阶段：1984 全国文科四版正式构建成功，manifest revision 3910；build attempt `42081829-4c28-4bdc-a6b9-817edddd9c66`。页数仍为 2/20/3/15，共 40 页；零 warning、无 build failure。
- 阶段验证：build receipt validator `OK`，无 failed/invalid/missing/stale；当前 1 卷待视觉复核。
- 阶段修改文件：本进度文件、1984 文科 build receipt/PDF；未改试卷题目、答案、provenance、图稿或生成源。
- 已完成子阶段：为当前 attempt 准备 4 份 review work items，覆盖 40 页；候选页为印刷版 p9、解析版 p20、试题版 p1、简答版 p1。
- 阶段验证：4/4 工作项绑定 attempt `42081829-4c28-4bdc-a6b9-817edddd9c66`，页数及 PDF 哈希一致；每页八项齐全。
- 阶段修改文件：本进度文件与忽略的 `.work/phase2-b51/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：40 页已渲染为 4 张接触表并逐页浏览；4 个候选页均完成 120dpi 复核。未发现缺字、公式/图稿异常、裁切、孤立标题、答案串版或异常分页；本卷构建零 warning。
- 阶段验证：接触表覆盖 40/40 页、4/4 接触表通过；候选页 4/4 通过。
- 阶段修改文件：仅本进度文件；接触表、预览页与候选图位于 `/tmp/gk-phase2-b51-review.eLbJlJ/`；未更改试卷源或 PDF。
- 已完成子阶段：4 份当前 attempt work items 均已登记，覆盖 40 页 × 8 项共 320 条 pass；本卷零构建 warning，故无 warning exemption。
- 阶段验证：工作项汇总 4/4、40 页、320 pass、0 pending、0 exemptions；`git diff --check` 通过。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b51/review/` 下 4 份工作项。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b51 状态 `closed`、无问题；正式 review receipt 与当前 build attempt 对齐，并生成 `reports/phase2-b51.md`，manifest revision 3911。
- 阶段验证：本卷 40 页、320 项视觉检查全部通过，零 warning、无失败项。
- 阶段修改文件：1984 文科正式 review receipt、manifest 批次状态投影、本批报告与本进度文件；忽略工作项及临时 PNG 尚待清理。
- 已完成子阶段：1984 文科 build 目录的 24 个非 PDF 中间物移入系统废纸篓，保留 4 份 PDF、0 个非 PDF；4 份 `.work/phase2-b51/review/` 工作项与临时审阅目录 `/tmp/gk-phase2-b51-review.eLbJlJ/`（48 张 PNG）也移入系统废纸篓，路径确认不存在。
- 阶段验证：build 目录核验为 4 PDFs、0 intermediates；PDF 保留，LaTeX 源和正式回执未删除；忽略工作项及临时图像已清理，操作可从系统废纸篓恢复。
- 阶段修改文件：本进度文件及 build 目录中的忽略编译产物；未删除源文件或 PDF。
- 已完成阶段：五项 b51 scoped gates 全部通过：source manifest validate；generator `--check` 单卷一致；build receipts 为 1 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：1 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3911，b51 `closed`。
- 阶段修改文件：仅本进度文件；门禁检查未产生额外内容源改动。
- 已完成阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，并保留整个语料库的未完成状态。
- 阶段验证：全量报告 render/check 均成功退出；b51 五项 scoped gates 仍全部通过。
- 阶段修改文件：全量 README/报告投影、本批报告、1984 文科 build/review receipts、manifest 与本进度文件；未更改转录、答案、provenance 或 LaTeX 源。
- 已完成阶段：b51 内容、正式回执与全量报告投影提交 `c1ca8068`（`docs: 完成1984全国文科复核`）；未 push。
- 阶段关闭快照：manifest revision 3911；b51 `closed`，1 卷、40 页、320 项视觉检查通过，零 warning；4 份 PDF 保留，build 目录仅 PDF；转录/答案/provenance/LaTeX 源未更改。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段只关闭 b51，不代表全库完成。
- 已完成阶段：b51 独立进度记录提交 `e509d804`（`docs: 记录b51阶段进度`）；未 push。提交后工作树干净。

### `phase2-b52` — 1985 全国卷文科

- 预检完成：起始 manifest revision 3911；批次仅含 `gk-1985-regular-national-arts`，issues 为空；source manifest validate 通过；generator `--check` 显示该卷一致；provenance status 为该卷 `editions_generated`、批次 `provenance_verified`。
- 本卷 17 题，固定来源 PDF 为 ready、1 页且 artifact PDF 校验通过，`legacy_ids=[]`；沿用已登记转录/解题与 provenance，不重复录入。项目目录以 manifest 为准为 `1985_全国卷_文科`。既有四版 PDF 页数为试题 3、解析 15、简答 4、印刷 12，共 34 页。
- Build receipt validator 显示该卷 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；manifest 批次仍为 `compiled_pending_review`。下一步须正式重建四版，再检查 warning 与复核状态。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 已完成子阶段：1985 全国文科四版正式构建成功，manifest revision 3913；build attempt `bf74bc72-5b97-4caa-8778-911fc302b74e`。页数仍为试题 3、解析 15、简答 4、印刷 12，共 34 页；零 warning、无 build failure。
- 阶段验证：build receipt validator `OK`，无 failed/invalid/missing/stale；当前 1 卷待视觉复核。
- 阶段修改文件：本进度文件、1985 文科 build receipt/PDF；未改试卷题目、答案、provenance、图稿或生成源。
- 已完成子阶段：为当前 attempt 准备 4 份 review work items，覆盖 34 页；四版候选页均为 p1。
- 阶段验证：4/4 工作项绑定 attempt `bf74bc72-5b97-4caa-8778-911fc302b74e`，页数及 PDF 哈希一致；每页八项齐全。
- 阶段修改文件：本进度文件与忽略的 `.work/phase2-b52/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：34 页已渲染为 4 张接触表并逐页浏览；四个候选页均完成 120dpi 复核。未发现缺字、公式/图稿异常、裁切、孤立标题、答案串版或异常分页；本卷构建零 warning。
- 阶段验证：接触表覆盖 34/34 页、4/4 接触表通过；候选页 4/4 通过。
- 阶段修改文件：仅本进度文件；接触表、预览页与候选图位于 `/tmp/gk-phase2-b52-review.N9IHEk/`；未更改试卷源或 PDF。
- 已完成子阶段：4 份当前 attempt work items 均已登记，覆盖 34 页 × 8 项共 272 条 pass；本卷零构建 warning，故无 warning exemption。
- 阶段验证：工作项汇总 4/4、34 页、272 pass、0 pending、0 exemptions；`git diff --check` 通过。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b52/review/` 下 4 份工作项。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b52 状态 `closed`、无问题；正式 review receipt 与当前 build attempt 对齐，并生成 `reports/phase2-b52.md`，manifest revision 3914。
- 阶段验证：本卷 34 页、272 项视觉检查全部通过，零 warning、无失败项。
- 阶段修改文件：1985 文科正式 review receipt、manifest 批次状态投影、本批报告与本进度文件；忽略工作项及临时 PNG 尚待清理。
- 已完成子阶段：1985 文科 build 目录的 24 个非 PDF 中间物移入系统废纸篓，保留 4 份 PDF、0 个非 PDF；4 份 `.work/phase2-b52/review/` 工作项与 `/tmp/gk-phase2-b52-review.N9IHEk/` 临时审阅目录（42 张 PNG）也移入系统废纸篓，路径确认不存在。
- 阶段验证：build 目录核验为 4 PDFs、0 intermediates；PDF 保留，LaTeX 源和正式回执未删除；忽略工作项及临时图像已清理，操作可从系统废纸篓恢复。
- 阶段修改文件：本进度文件及 build 目录中的忽略编译产物；未删除源文件或 PDF。
- 已完成阶段：五项 b52 scoped gates 全部通过：source manifest validate；generator `--check` 单卷一致；build receipts 为 1 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance `OK：1 卷`。
- 阶段验证：五项命令均退出码 0；manifest revision 3914，b52 `closed`。
- 阶段修改文件：仅本进度文件；门禁检查未产生额外内容源改动。
- 已完成阶段：`report.py render --all` 以单个 content 事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，并保留整个语料库的未完成状态。
- 阶段验证：全量报告 render/check 均成功退出；b52 五项 scoped gates 仍全部通过。
- 阶段修改文件：全量 README/报告投影、本批报告、1985 文科 build/review receipts、manifest 与本进度文件；未更改转录、答案、provenance 或 LaTeX 源。
- 已完成阶段：b52 内容、正式回执与全量报告投影提交 `3e8c8c34`（`docs: 完成1985全国文科复核`）；未 push。
- 阶段关闭快照：manifest revision 3914；b52 `closed`，1 卷、34 页、272 项视觉检查通过，零 warning；4 份 PDF 保留，build 目录仅 PDF；转录/答案/provenance/LaTeX 源未更改。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段只关闭 b52，不代表全库完成。
- 下一步：单独提交本进度记录；随后核对工作树并预检 manifest 下一批 `phase2-b53`。

### `phase2-b53` — 1985 全国卷理科

- 预检完成：起始 manifest revision 3914；批次仅含 `gk-1985-regular-national-science`，issues 为空；source manifest validate 通过；generator `--check` 显示该卷一致；provenance status 为该卷 `editions_generated`、批次 `provenance_verified`。
- 本卷 18 题，固定来源 `普通高考/1985/1985全国理.pdf` 为 ready；artifact 校验通过，PDF、1 页，SHA-256 `3ed7864978068575dc864cb2db9d2524e0df218bc732c75e08efd65e630ab57d`，`legacy_ids=[]`。沿用已登记转录/解题与 provenance，不重复录入。既有四版 PDF 页数为试题 4、解析 19、简答 5、印刷 16，共 44 页。
- Build receipt validator 显示该卷 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；manifest 批次仍为 `compiled_pending_review`。下一步须正式重建四版，再检查 warning 与复核状态。
- 阶段验证：source manifest validate、generator `--check`、provenance status 均退出码 0；build receipt 检查确认唯一问题为 stale；四份现存 PDF 均可读且页数已记录。预检过程中首次调用 source manifest validator 漏传必需参数、退出码 2；按其 CLI 用法补上 `--manifest` 后验证通过，未产生写入。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 剩余任务：正式构建、逐页视觉复核、登记回执、清理中间产物并完成五项 scoped gates 与全量报告校验。
- 已完成子阶段：1985 全国理科四版正式构建成功，manifest revision 3916；build attempt `45f24548-3eb1-47fc-8e5b-181b34d4a481`。页数仍为试题 4、解析 19、简答 5、印刷 16，共 44 页；零 warning、无 build failure。
- 阶段验证：build receipt validator `OK`，无 failed/invalid/missing/stale；当前 1 卷待视觉复核。
- 阶段修改文件：本进度文件、1985 理科 build receipt/PDF；未改试卷题目、答案、provenance、图稿或生成源。
- 已完成子阶段：为当前 attempt 准备 4 份 review work items，覆盖 44 页；候选页为印刷版 p13、其余三版 p3。
- 阶段验证：4/4 工作项绑定 attempt `45f24548-3eb1-47fc-8e5b-181b34d4a481`，PDF 页数及 SHA-256 与构建回执一致；每页八项齐全，共 352 项初始 pending。
- 阶段修改文件：本进度文件与忽略的 `.work/phase2-b53/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：44 页已渲染为 4 张接触表并逐页浏览；四版候选页均完成 160dpi 高分辨率复核。未发现缺字、公式/图稿异常、裁切、孤立标题、答案串版或异常分页；本卷构建零 warning。
- 阶段验证：接触表覆盖 44/44 页、4/4 接触表通过；候选页 4/4 通过。4 份当前 attempt 工作项登记 44 页 × 8 项共 352 条 pass、0 pending、0 warning exemption；`git diff --check` 通过。`check-batch` 仅报告正式 review receipt 仍绑定旧 build attempt/输入树/依赖/工具链/视觉工具/PDF，属 finalize 刷新前预期。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b53/review/` 下 4 份工作项；接触表、44 页预览与候选图位于 `/tmp/gk-phase2-b53-review.KRGw4u/`；未更改试卷源或 PDF。
- 下一步：提交本阶段进度 checkpoint，运行事务 finalize 更新正式 review receipts 与批次状态。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b53 状态 `closed`、无问题；1985 全国理科正式 review receipt 与当前 build attempt 对齐，并生成 `reports/phase2-b53.md`，manifest revision 3917。
- 阶段验证：`review_receipts.py check-batch` 返回 `FINALIZED`，批次无 problems；44 页、352 项视觉检查全部通过，零 warning、无失败项。
- 阶段修改文件：1985 理科正式 review receipt、manifest 批次状态投影、本批报告；忽略工作项与临时 PNG 尚待清理。
- 已完成子阶段：1985 理科 build 目录的 24 个非 PDF 中间物、4 份 `.work/phase2-b53/review/` 工作项与 `/tmp/gk-phase2-b53-review.KRGw4u/` 临时审阅目录（52 张 PNG）均移入系统废纸篓；路径确认不存在，`.work/phase2-b53/review/` 空目录一并移除。保留四版 PDF，build 目录核验为 4 PDFs、0 个非 PDF。
- 阶段验证：五项 b53 scoped gates 全部通过：source manifest validate；generator `--check` 单卷一致；build receipts 为 1 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance status 显示该卷 complete、批次 closed。`report.py render --all` 单事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，未完成状态保留。
- 阶段修改文件：本进度文件、b53 build/review receipts、manifest、本批报告与六个全量报告目标；构建中间物、忽略工作项和临时图像已清理；未更改题目、答案、provenance、图稿或 LaTeX 源。
- 已完成阶段：b53 内容、正式回执与全量报告投影提交 `b3e28f28`（`docs: 完成1985全国理科复核`）；未 push。b53 关闭快照：manifest revision 3917；1 卷、44 页、352 项视觉检查通过、零 warning；4 份 PDF 保留，build 目录仅 PDF。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段仅关闭 b53，不代表全库完成。
- 下一步：单独提交本进度记录；随后核对工作树并预检 manifest 下一批 `phase2-b54`（1985 上海文科）。

### `phase2-b54` — 1985 上海卷文史类

- 预检完成：起始 manifest revision 3917；批次仅含 `gk-1985-regular-shanghai-arts`，batch issues 为空；source manifest validate 通过；generator `--check` 显示该卷一致；provenance status 为该卷 `editions_generated`、批次 `provenance_verified`。
- 本卷 8 题，固定来源 `普通高考/1985/1985上海文.pdf` 为 ready；artifact 校验通过，PDF、2 页，SHA-256 `c4a114f9e96fb329c34b651a9ad29c7e755b6eab709cbcb8f256af7ecb1035aa`，`legacy_ids=[]`。沿用已登记转录/解题与 provenance，不重复录入。既有四版 PDF 页数为试题 4、解析 17、简答 5、印刷 13，共 39 页。
- Build receipt validator 显示该卷 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；批次仍为 `compiled_pending_review`。paper 已登记两条 open、non-blocking 来源问题 ISSUE-0761/0762：第 5、8 题题干称“如图”，固定扫描未见可独立核验配图；既有源文档明确不得凭空补图，继续沿用原记录。
- 阶段验证：source manifest validate、generator `--check`、provenance status 均退出码 0；build receipt 检查确认唯一问题为 stale；固定来源 artifact 与四份现存 PDF 均已核对，页数记录如上。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 剩余任务：正式构建、逐页视觉复核并记录已登记来源问题的可见影响、登记回执、清理中间产物并完成 scoped gates 与全量报告校验。
- 已完成子阶段：1985 上海文史类四版正式构建成功，manifest revision 3919；build attempt `f7bcfd6c-2b86-4f88-bda9-6b41b4340450`。页数仍为试题 4、解析 17、简答 5、印刷 13，共 39 页；零 warning、无 build failure。
- 阶段验证：build receipt validator `OK`，无 failed/invalid/missing/stale；当前 1 卷待视觉复核。两条预存来源问题 ISSUE-0761/0762 状态保持 open，未更改问题事实或题目源。
- 阶段修改文件：本进度文件、1985 上海文史类 build receipt/PDF；未改试卷题目、答案、provenance、图稿或生成源。
- 已完成子阶段：为当前 attempt 准备 4 份 review work items，覆盖 39 页；候选页为印刷版 p3、其余三版 p2。
- 阶段验证：4/4 工作项绑定 attempt `f7bcfd6c-2b86-4f88-bda9-6b41b4340450`，PDF 页数及 SHA-256 与构建回执一致；每页八项齐全，共 312 项初始 pending。
- 阶段修改文件：本进度文件与忽略的 `.work/phase2-b54/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：39 页已渲染为 4 张接触表并逐页浏览；4 个自动候选页与 ISSUE-0761/0762 涉及题目所在页合计 11 页完成 160dpi 高分辨率复核。固定源未见第 5、8 题“如图”所指图形，页面注记忠实保留该事实，未补绘；没有发现新增缺字、裁切、公式/图稿异常、答案串版或异常分页。
- 阶段验证：接触表覆盖 39/39 页、4/4 接触表通过；候选页及来源问题关联页共 11 页高分辨率复核通过。4 份当前 attempt 工作项登记 39 页 × 8 项共 312 条 pass、0 pending、0 warning exemption；两条来源问题保持 open、non-blocking；`git diff --check` 通过。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b54/review/` 下 4 份工作项；接触表、39 页预览与高分辨率图位于 `/tmp/gk-phase2-b54-review.wtXBr3/`；未更改试卷源或 PDF。
- 下一步：提交本阶段进度 checkpoint，运行事务 finalize 更新正式 review receipts 与批次状态。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b54 状态 `closed`、无问题；1985 上海文史类正式 review receipt 与当前 build attempt 对齐，并生成 `reports/phase2-b54.md`，manifest revision 3920。ISSUE-0761/0762 为既有 open、non-blocking 转录歧义，不阻止批次关闭，未变更其状态或事实。
- 阶段验证：review finalize 报告 `closed`、无 problems；39 页、312 项视觉检查全部通过，零构建 warning。
- 阶段修改文件：1985 上海文史类正式 review receipt、manifest 批次状态投影、本批报告；忽略工作项与临时图像尚待清理。
- 已完成子阶段：1985 上海文史类 build 目录 24 个非 PDF 中间物、4 份 `.work/phase2-b54/review/` 工作项与 `/tmp/gk-phase2-b54-review.wtXBr3/` 临时审阅目录（54 张 PNG）均移入系统废纸篓；路径确认不存在，空 review 目录一并移除。保留四版 PDF，build 目录核验为 4 PDFs、0 个非 PDF。
- 阶段验证：五项 b54 scoped gates 全部通过：source manifest validate；generator `--check` 单卷一致；build receipts 为 1 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance status 显示该卷 complete、批次 closed。`report.py render --all` 单事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，未完成状态保留。ISSUE-0761/0762 仍为 open、non-blocking。
- 阶段修改文件：本进度文件、b54 build/review receipts、manifest、本批报告与六个全量报告目标；构建中间物、忽略工作项和临时图像已清理；未更改题目、答案、provenance 或 LaTeX 源。
- 已完成阶段：b54 内容、正式回执与全量报告投影提交 `a5c33211`（`docs: 完成1985上海文史类复核`）；未 push。b54 关闭快照：manifest revision 3920；1 卷、39 页、312 项视觉检查通过，零 warning；4 份 PDF 保留，build 目录仅 PDF。ISSUE-0761/0762 仍 open，不影响该卷 closed 状态。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段仅关闭 b54，不代表全库完成。
- 下一步：单独提交本进度记录；随后核对工作树并预检 manifest 下一批 `phase2-b55`（1985 上海理科）。

### `phase2-b55` — 1985 上海卷理工农医类

- 预检完成：起始 manifest revision 3920；批次仅含 `gk-1985-regular-shanghai-science`，batch issues 为空；source manifest validate 通过；generator `--check` 显示该卷一致；provenance status 为该卷 `editions_generated`、批次 `provenance_verified`。
- 本卷 10 题，固定来源 `普通高考/1985/1985上海理.pdf` 为 ready；artifact 校验通过，PDF、2 页，SHA-256 `a54787068aa9e04814d9d65eab15a4c8f7e69b04a8c2b59fa7d21212a86ef856`，`legacy_ids=[]`。沿用既有转录/解题与 provenance，不重复录入。既有四版 PDF 页数为试题 4、解析 18、简答 5、印刷 14，共 41 页。
- 已登记 ISSUE-0763/0764/0765 均为 resolved，记录固定扫描将第 2 题第（5）小题印作 `x=x^3`，规范源依现有交叉核定采用 `y=x^3`、答案（D）；本轮保持该既有裁定，不重开来源核查或更改转录。
- Build receipt validator 显示该卷 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；批次仍为 `compiled_pending_review`。
- 阶段验证：source manifest validate、generator `--check`、provenance status 均退出码 0；build receipt 检查确认唯一问题为 stale；固定来源 artifact 与四份现存 PDF 均已核对，页数记录如上。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 剩余任务：正式构建、逐页视觉复核、登记回执、清理中间产物并完成 scoped gates 与全量报告校验。
- 已完成子阶段：1985 上海理工农医类四版正式构建成功，manifest revision 3922；build attempt `139fb324-6cb4-4773-9ed2-5f366658729c`。页数仍为试题 4、解析 18、简答 5、印刷 14，共 41 页；零 warning、无 build failure。
- 阶段验证：build receipt validator `OK`，无 failed/invalid/missing/stale；当前 1 卷待视觉复核。既有 ISSUE-0763/0764/0765 状态均 resolved，本阶段未修改其记录或试卷源。
- 阶段修改文件：本进度文件、1985 上海理工农医类 build receipt/PDF；未改试卷题目、答案、provenance、图稿或生成源。
- 已完成子阶段：为当前 attempt 准备 4 份 review work items，覆盖 41 页；印刷版候选页 p1，其余三版候选页 p2。
- 阶段验证：4/4 工作项绑定 attempt `139fb324-6cb4-4773-9ed2-5f366658729c`，PDF 页数及 SHA-256 与构建回执一致；每页八项齐全，共 328 项初始 pending。
- 阶段修改文件：本进度文件与忽略的 `.work/phase2-b55/review/` 当前工作项；未改试卷内容。
- 已完成子阶段：41 页已渲染为 4 张接触表并逐页浏览；四版自动候选页与各版第 2 题第（5）小题核定说明所在页合计 5 个版页完成 160dpi 高分辨率复核。规范题面 `y=x^3`、选项（D）与既有核定一致，页面保留扫描异文和 ISSUE-0763—0765 指针；未见缺字、裁切、公式/图稿异常、答案串版或异常分页。
- 阶段验证：接触表覆盖 41/41 页、4/4 接触表通过；高分辨率页面 5/5 通过。4 份当前 attempt 工作项登记 41 页 × 8 项共 328 条 pass、0 pending、0 warning exemption；三条既有问题保持 resolved；`git diff --check` 通过。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b55/review/` 下 4 份工作项；接触表、41 页预览及高分辨率图位于 `/tmp/gk-phase2-b55-review.ALrEHV/`；未更改试卷源或 PDF。
- 下一步：提交本阶段进度 checkpoint，运行事务 finalize 更新正式 review receipts 与批次状态。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，b55 状态 `closed`、无问题；1985 上海理工农医类正式 review receipt 与当前 build attempt 对齐，并生成 `reports/phase2-b55.md`，manifest revision 3923。ISSUE-0763/0764/0765 均保持 resolved。
- 阶段验证：review finalize 报告 `closed`、无 problems；41 页、328 项视觉检查全部通过，零构建 warning。
- 阶段修改文件：1985 上海理工农医类正式 review receipt、manifest 批次状态投影、本批报告；忽略工作项与临时图像尚待清理。
- 已完成子阶段：1985 上海理工农医类 build 目录 24 个非 PDF 中间物、4 份 `.work/phase2-b55/review/` 工作项与 `/tmp/gk-phase2-b55-review.ALrEHV/` 临时审阅目录（50 张 PNG）均移入系统废纸篓；路径确认不存在，空 review 目录一并移除。保留四版 PDF，build 目录核验为 4 PDFs、0 个非 PDF。
- 阶段验证：五项 b55 scoped gates 全部通过：source manifest validate；generator `--check` 单卷一致；build receipts 为 1 succeeded、0 pending/failed/invalid/missing/stale；review `FINALIZED`；provenance status 显示该卷 complete、批次 closed。`report.py render --all` 单事务写入并回读校验六个全量报告目标；`report.py check --all` 确认报告与当前全量 manifest 一致，未完成状态保留。ISSUE-0763/0764/0765 均 resolved。
- 阶段修改文件：本进度文件、b55 build/review receipts、manifest、本批报告与六个全量报告目标；构建中间物、忽略工作项和临时图像已清理；未更改题目、答案、provenance 或 LaTeX 源。
- 已完成阶段：b55 内容、正式回执与全量报告投影提交 `ccc4f6ac`（`docs: 完成1985上海理工类复核`）；未 push。b55 关闭快照：manifest revision 3923；1 卷、41 页、328 项视觉检查通过，零 warning；4 份 PDF 保留，build 目录仅 PDF。
- 剩余任务：1952–2026 高考数学语料仍有大量未完成批次；本阶段仅关闭 b55，不代表全库完成。
- 下一步：单独提交本进度记录；随后核对工作树并预检 manifest 下一批 `phase2-b56`（1986 全国文理科两卷）。

### `phase2-b56` — 1986 全国卷文理科

- 预检完成：起始 manifest revision 3923；批次含 `gk-1986-regular-national-arts` 与 `gk-1986-regular-national-science`，batch issues 为空；source manifest validate 通过；generator `--check` 显示 2 卷一致；provenance status 为两卷 `editions_generated`、批次 `provenance_verified`。
- 文科 22 题、理科 24 题，均 `legacy_ids=[]`。固定来源 `普通高考/1986/1986全国文.pdf` 与 `普通高考/1986/1986全国理.pdf` 均为 ready、1 页且 artifact PDF 校验通过；SHA-256 分别为 `3208a80f44c61212cf0cfd6ea35849fa31f12ac21489cf78ddea0c995b316cf9`、`f63a3e838fb7c3fb39228ba4fdf76451965d1518421bd693ba279fe34e48957f`。既有四版页数：文科试题 4、解析 19、简答 5、印刷 16，共 44 页；理科试题 5、解析 21、简答 7、印刷 18，共 51 页；合计 95 页。
- 理科卷已登记 ISSUE-0766/0767/0768 均为 resolved：固定扫描第 20 题 `A∪B` 与独立资料交叉核定的 `A∩B` 有异文，规范题面采用 `A∩B`，答案 1084，原扫描差异保留在 issue 证据中。沿用既有裁定，不重开核查或更改转录。
- Build receipt validator 显示两卷均 stale（生成输入树、工具链指纹变化），无 failed/missing/pending；批次仍为 `compiled_pending_review`。
- 阶段验证：source manifest validate、generator `--check`、provenance status 均退出码 0；build receipt 检查确认 2 卷唯一问题均为 stale；两个来源 artifact 与 8 份现存 PDF 已核对，页数如上。
- 阶段修改文件：仅本进度文件；只读预检未修改试卷源、manifest、provenance、图稿或 PDF。
- 剩余任务：两卷四版正式构建、95 页逐页视觉复核（重点检查理科第 20 题异文说明）、登记回执、清理中间产物并完成 scoped gates 与全量报告校验。
- 已完成子阶段：1986 全国文理科八版正式构建成功，manifest revision 3925；文科 build attempt `d5d91fa1-600f-4ba5-960b-65a6ff822e6d`，理科 `b4121d8a-b708-4609-91c9-a4df5738f765`。页数保持文科 4/19/5/16（44 页）、理科 5/21/7/18（51 页），共 95 页；无 build failure。
- 阶段验证：build receipt validator `OK`，2 卷无 failed/invalid/missing/stale，当前 2 卷待视觉复核。文科及理科四版页数无变化；理科解析版与印刷版各有 2 条缺字日志，均为 Latin Modern Roman 字体缺少中文句号 `。`（U+3002）；其余无 Overfull、build errors 或 missing characters。该 warning 的源行/PDF 页定位与视觉影响待下一子阶段核实。
- 阶段修改文件：本进度文件、两卷 build receipts/PDF；未改题目、答案、provenance、图稿或生成源。
- 已完成子阶段：理科缺字 warning 已由 XeLaTeX 日志映射到规范源 `1986/1986_数学真题_全国理_解析正文.md` 第 357、369 行（生成 TeX `answers.tex` 第 727、743 行）；两个位置都把中文句号置于数学显示环境内。对应理科解析版 p18、印刷版 p16；`pdftotext` 在这两处抽取出替代字符，确认是实际缺字而非无影响日志。两版各 2 条日志分别对应同两处标点。
- 阶段验证：日志上下文、规范源行、生成 TeX 行和 PDF 页文本互相对应；已确认纯标点排版缺陷。理科第 20 题数值与结论未显示其他异常；需要将句号显式放入 CJK 文本标记后重新生成、检查 provenance 与正式构建状态。
- 阶段修改文件：仅本进度文件；诊断未修改源、manifest、provenance、图稿或 PDF。
- 下一步：提交 warning 根因 checkpoint；先以回归检查确认两个数学块内存在未转义句号，再做最小标点标记修复，重跑生成/provenance/构建与页面核验。
- 已完成子阶段：按纯排版边界修复理科解析正文第 357、369 行，将数学环境内句号改为 `\text{。}`；RED 检查曾准确命中两处，修复后 GREEN 检查通过，`git diff --check` 通过。生成器写入理科项目 3 个派生目标，单卷 `--check` 通过；题目数值、论证和答案结论未改。随后两卷八版正式重建，文科 attempt `d5d91fa1-600f-4ba5-960b-65a6ff822e6d`、理科 `b4121d8a-b708-4609-91c9-a4df5738f765`，manifest revision 3925；构建命令无失败。
- 阶段验证：理科补建 attempt `80391215-3b2a-42dc-9ba1-071468d02361` 后，build receipt validator 显示两卷 `OK`，provenance `check-batch` 通过，manifest revision 3927；理科最终四版日志均无 Missing character、Overfull、LaTeX error 或 undefined reference。复核工具已为当前两卷八版准备 8 个 work items，覆盖 95 页，均绑定最新 attempts。
- 阶段修改文件：规范源 `1986/1986_数学真题_全国理_解析正文.md`、生成的理科 LaTeX 目标、两卷正式 build receipts/PDF、source-manifest、本进度文件及忽略的 `.work/phase2-b56/review/` 8 份新工作项；未改题面、数学结论、问题账或 provenance 逐题证据。
- 已完成子阶段：95 页接触表全覆盖浏览；8 个候选首页完成 160dpi 高分辨率复核。理科第 20 题题面与异文说明所在的试题版 p4、解析版 p18、简答版 p6、印刷版 p16 完成 180dpi 高分辨率复核；两处修复句号在解析版 p18、印刷版 p16 均清晰呈现，`A∩B` 异文说明与答案 1084 正确可读。未发现缺页、裁切、图形/公式异常、答案串版或异常分页。
- 阶段验证：8/8 接触表覆盖并检查 95/95 页；高分辨率检查 12/12 页通过。接触表生成初次因 ImageMagick 字体别名 `Arial` 无法解析而打印告警，随后指定系统字体文件重生成；该问题仅影响接触表标注渲染，不影响 PDF 页面图像。新工作项待登记页面级检查结果。
- 阶段修改文件：仅本进度文件与忽略的 `.work/phase2-b56/review/` 工作项；接触表及高分辨率预览位于 `/tmp/gk-phase2-b56-review.T69VtV/`；未更改试卷源或 PDF。
- 已完成子阶段：8 份当前 attempt 工作项已登记 95 页 × 8 项，共 760 条 pass、0 pending、0 warning exemption；文理科各版页数与 attempt 均匹配正式构建回执。`git diff --check` 通过。
- 阶段验证：工作项页覆盖分别为文科 44 页、理科 51 页，检查项合计 760/760 pass；重点页和候选页备注记录了对应检查尺度与结论。
- 阶段修改文件：本进度文件；忽略的 `.work/phase2-b56/review/` 8 份工作项；临时接触表/PNG 位于 `/tmp/gk-phase2-b56-review.T69VtV/`；未更改试卷源或正式 PDF。
- 剩余任务：提交源修复与正式构建检查点；事务 finalize 正式 review/build 回执与批次报告；清理构建中间产物、工作项和临时 PNG；完成五项 scoped gates 与全量报告校验。
- 下一步：先审阅 tracked diff 并提交源修复、生成物、正式构建回执/PDF 及本进度 checkpoint；随后运行事务 finalize。
- 已完成阶段：`finalize-batch` 返回 `FINALIZED`，phase2-b56 已关闭，manifest revision 3928；1986 全国文理两卷 provenance 状态均为 `complete`，正式 build/review receipts 均与当前 attempts 对齐，批次报告 `reports/phase2-b56.md` 已生成。
- 阶段验证：review `check-batch` 返回 `FINALIZED`；build receipt validator `OK：2 卷`；provenance status 显示两卷 `complete`、批次 `closed`。95 页、760 项视觉检查全 pass，构建零 warning。清理与全量报告一致性检查待执行。
- 阶段修改文件：两卷正式 build/review receipts、manifest 批次状态、本批报告及本进度文件；当前 `.work/phase2-b56/review/` 与 build 中间文件/临时 PNG 尚待清理。
- 剩余任务：只保留两卷各四份 PDF 与 LaTeX 源，清理 build 非 PDF 文件、review work items 和本轮临时渲染图；刷新并核验全量报告；完成五项 scoped gates 后提交关闭 checkpoint。
- 下一步：先预览准确清理范围，保留 8 份 PDF，然后将 48 个非 PDF build 产物、8 份本轮 work items 与临时审阅 PNG 移入系统废纸篓；再跑 scoped gates 与 `report.py render/check --all`。
- 已完成阶段：1986 全国文理批次收尾清理完成。两卷 build 目录的 48 个非 PDF 中间产物、8 份本轮 review work items 与 `/tmp/gk-phase2-b56-review.T69VtV/` 临时审阅目录均移入系统废纸篓；各保留试题/解析/简答/印刷 PDF 各一份，核验为每卷 4 PDFs、0 非 PDF。
- 阶段验证：五项 scoped gates 全部通过：source manifest validate；两卷 generator `--check` 一致；build receipts 为 2 succeeded、0 stale/invalid/failed；review `FINALIZED`（95 页、760 项全 pass）；provenance 两卷 complete、批次 closed。`report.py render --all` 单事务更新并回读六个全量报告目标；`report.py check --all` 确认输出与全量 manifest 一致，未完成状态保留；`git diff --check` 通过。
- 阶段修改文件：本进度文件与六个全量报告目标：`README_数学.md`、`math-gaokao-2017-2026/README.md`、`math-gaokao-latex/README.md`、`math-gaokao-latex/reports/baseline.md`、`report.md`、`docs/source-inventory.md`。本批三个提交为 `6734c7fd`（修复/构建）、`05f231a8`（正式复核登记）、`c99d3c84`（全量报告与收尾进度）。
- 剩余任务：phase2-b56 已完整关闭；高考数学语料仍未全部完成。manifest 中下一批 `phase2-b57`（1986 上海文理两卷）当前为 `compiled_pending_review`，需按常规先预检再决定续作。
- 下一步：本次工作树核验位于 `feat/gaokao-phase0`，无未提交更改；不 push。后续从 `phase2-b57` 预检开始，不重复 phase2-b56 操作。

### `phase2-b57` — 1986 上海卷文理科

- 预检完成：批次含 `gk-1986-regular-shanghai-arts`、`gk-1986-regular-shanghai-science`，manifest revision 3928；批次 issues 为空。source manifest validate 与两卷 generator `--check` 均通过；provenance status 为两卷 `editions_generated`、批次 `provenance_verified`。
- 两卷各 7 题、`legacy_ids=[]`。固定来源 `普通高考/1986/1986上海文.pdf`（4 页，SHA-256 `c82132f9b00f53dcfd23f85803baa336737094e3394b63c563062a3171f91958`）与 `普通高考/1986/1986上海理.pdf`（5 页，SHA-256 `d4822a1d879b1f4ce5e9a16cba10a161237362841995220af59a07dd08d7df3f`）均登记 ready 且 PDF artifact 校验通过。四版既有页数：文科 4/18/5/14，共 41 页；理科 5/22/6/17，共 50 页；合计 91 页。
- 既有来源问题保持 open、non-blocking：文科 ISSUE-0769（第 1 题第（9）小题幅角主值约定）、ISSUE-0770（第 7 题折叠几何的 AB=√7 语义）；理科 ISSUE-0771（幅角主值约定）、ISSUE-0772（第 5 题参数 k 定义域）、ISSUE-0773（第 7 题折叠后 AB=√7 语义）。不得擅自补源或更改既有事实裁定。
- Build receipt validator 显示两卷均 stale（生成输入树、工具链指纹变化），非编译失败；manifest 批次状态仍为 `compiled_pending_review`。当前 8 份 review work items 绑定旧 attempts（文科 `8dc23918-5843-44d3-b429-afba1024afa6`、理科 `8d86d75a-5ff3-481a-907c-05d48d34277b`），新构建后需按工具规则刷新，不复用旧视觉结论。
- 阶段验证：source manifest validate、两卷 generator `--check`、provenance status 均通过；build receipt 检查确认两卷需重建；固定来源 artifact 与当前四版 PDF 页数已核对。独立只读内容/来源审计由两名 subagent 分卷并行进行，尚待主会话验收其证据。
- 阶段修改文件：仅本进度文件；预检未修改试卷源、manifest、provenance、issue 或构建产物。ignored `.work/phase2-b57/review/` 中既存工作项保持不动，待新 attempt 后由官方工具刷新。
- 剩余任务：完成独立审计验收；两卷八版正式重建；逐页复核 91 页并重点检查既有五条来源问题所涉页面；登记正式回执并关闭批次；清理中间产物、工作项与临时 PNG；完成 scoped gates 与全量报告校验。
- 下一步：核实分卷只读审计结果与问题记录；若无需要修正的转录/答案事实，再正式重建两卷四版，之后刷新 review work items。
- 已完成子阶段：在两项只读内容审计并行进行期间，完成两卷八版正式重建；文科 attempt `6b44ba20-7ddd-4b0f-8849-b4f5fca44154`，理科 attempt `ff815137-1e49-41e7-94d1-8361cf029bec`，manifest revision 3929。页数保持文科 4/18/5/14（41 页）、理科 5/22/6/17（50 页），总计 91 页。
- 阶段验证：build receipt validator `OK：2 卷`；八版日志均无 Missing character、Overfull、LaTeX error 或 undefined reference。当前 2 卷待视觉复核。provenance 逐题记录未被改动；复核工作项尚绑定旧 attempts，未复用。
- 阶段修改文件：两卷 build receipts/PDF 与 `source-manifest.json`；两名只读 subagent 尚在审计源内容，未写入文件；本进度文件记录本阶段。
- 剩余任务：验收两名独立审计证据；如无事实修正，刷新两卷 review work items 并检查其 attempt/PDF 哈希绑定；逐页复核 91 页并重点查看五条既有非阻塞来源问题涉及页；登记正式回执、清理中间产物与临时图像、完成 scoped gates 和全量报告校验。
- 下一步：取得并核对两名审计者的证据；随后准备当前 attempt 的 review work items，不要在审计未收敛前 finalize。
- 已完成可验证子阶段（固定来源与旧回执核验）：在隔离工作树外的既有来源检出 `gaokaomath-src/普通高考/1986/1986上海文.pdf`、`1986上海理.pdf` 找回固定 PDF；两文件 SHA-256 分别与 manifest 一致（文 `c82132f9b00f53dcfd23f85803baa336737094e3394b63c563062a3171f91958`、理 `d4822a1d879b1f4ce5e9a16cba10a161237362841995220af59a07dd08d7df3f`），页数为 4/5，且两份 book checkout 副本哈希相同。已查看源 PDF 全部 9 页图像，题面页、答案表、解析页与登记的来源页范围相符；五条既有歧义仍保持登记，不据此改动事实。旧 `reports/phase2-b57.md` 记录的是 2026-09-25 attempts（文 `60659bc1-d0b6-4f5f-949e-1c54cca7834f`、理 `4c4d0742-10f1-45d5-b200-71c234642048`），与本次 2026-10-12 新 build 不同，故旧 `closed` 结论和旧视觉回执均不适用于当前 attempt；该生成报告待正式复核后重建。
- 阶段验证：`shasum -a 256` 两个来源位置的四个 PDF 与 manifest 哈希一致；`pdfinfo` 页数 4/5；人工查看源 PDF 9 页扫描图，涵盖两卷题面、答案表和解答页。主工作树在此阶段开始前干净，未改来源或回执。
- 阶段修改文件：仅本 `PROGRESS.md`。
- 剩余任务：为当前 attempts 刷新 8 份 review work items，核对每份绑定当前 attempt 与 PDF 哈希；完成两卷 91 页逐页视觉复核及登记问题页面核查；按正式流程登记回执、清理构建中间产物与临时图像、运行 scoped gates 和全量报告校验。
- 下一步：用 `review_receipts.py prepare-batch` 为 `phase2-b57` 生成当前 attempt 的 8 份工作项，先验证哈希绑定，再进行逐页复核；不沿用旧报告或旧回执。
- 已完成可验证子阶段（当前 attempt 复核工作项准备）：执行 `review_receipts.py prepare-batch --manifest source-manifest.json --batch phase2-b57`，为两卷四版共生成 8 份 ignored work items。逐项核对后，文科全部绑定 attempt `6b44ba20-7ddd-4b0f-8849-b4f5fca44154`、理科全部绑定 `ff815137-1e49-41e7-94d1-8361cf029bec`；PDF 路径、SHA-256、页数与对应 build receipts 一致，页集合精确覆盖各版完整页数，所有审查项仍为 pending。
- 阶段验证：准备命令报告“共 8 个工作项”；对 8 项执行只读 JSON 核验，attempt/PDF hash/page count 均匹配 build receipts；当前 `review_receipts.py check-batch` 按预期报告两卷 `INVALID_OR_STALE`（旧正式回执不匹配新 attempt），尚未尝试 finalize。
- 阶段修改文件：ignored `math-gaokao-latex/.work/phase2-b57/review/{试题版,解析版,简答版,印刷版}/` 下两卷 8 个工作项；tracked 文件无变化。
- 剩余任务：逐页检查文科 41 页、理科 50 页的版面和八项检查标准；对题面/解答的关键图形、易混公式及五条既有 issue 页面做高分辨率复核；完成后在工作项记录真实结果，再运行 checked finalize、清理中间物并完成 scoped gates/全量报告。
- 下一步：继续 91 页视觉审查，先以单页高分辨率图核对候选版面与登记的五条来源歧义页，再逐版完成全页检查并据实登记，不把 contact sheet 粗看当作字形验收。
- 已完成可验证子阶段（视觉首轮与问题页抽核）：浏览两卷四版全部 91 页接触表，并对 8 个版本首页做高分辨率检查；另检查文科 Q1(9)、Q7 与理科 Q1(9)、Q5、Q7 在各相关版本的高分辨率页。已确认两卷试题版首页均有答案泄漏：来源说明框直接写出 Q1(9) 的 `11π/6` 与 `−π/6`，违反“题目版绝不能带答案”的项目不变量。试题版分页的其余已查区域及两卷登记问题页中，暂未见新增缺字、裁切、图形错标；完整 91 页细查仍由独立审查进行。
- 阶段验证：`pdftoppm` 高分辨率页图人工检查；接触表覆盖 41+50=91 页。可复现证据为文、理两卷 `试题版.pdf` 第 1 页；同一答案-bearing 编辑说明也出现在对应解析版首页（解析/答案版允许）。此发现只涉及本库编辑说明，不是固定源题干。
- 阶段修改文件：仅本 `PROGRESS.md`；已生成的 8 个 ignored review work items 保持待填，未写入 pass/fail 或正式回执。
- 剩余任务：等待用户决定对答案泄漏采取最小修订并重建，或保留原文并登记失败；取得两名独立审查者对 91 页逐页结果；随后据实完成其余页回执、清理、scoped gates 与全量报告校验。
- 下一步：继续非冲突的整卷视觉核对；未获用户选择前，不改两卷试题源、不更新 provenance、不重建、不将当前批次标为通过。
- 已完成可验证子阶段（确证失败登记）：在当前 attempt 的文、理 `试题版` 工作项中，仅将第 1 页 `answer_leak` 与该页总结果登记为 `fail`，其余该页检查及所有其余页仍是 pending。证据注释记录首页编辑说明直接呈现 `11π/6` 和 `−π/6`。正式 review receipts/manifest 状态尚未写入；须待全页检查完成且依据用户选择处理后再走 checked finalize。
- 阶段验证：只读回读两份 work items，确认 paper/edition/attempt 与新构建一致，page 1 已 fail，其他页仍 pending；当前没有提交失败回执，也未声称批次通过。
- 阶段修改文件：ignored `.work/phase2-b57/review/试题版/gk-1986-regular-shanghai-arts.json` 与 `.../gk-1986-regular-shanghai-science.json`；tracked 文件尚未包含本子阶段日志。
- 剩余任务：同上，等待用户对修注或保留并登记失败的选择；取得整卷独立视觉审查结论。
- 下一步：根据用户选择处理首页答案泄漏；如果修注，则刷新 provenance/build/work items 并复核受影响输出；如果保留，则继续完成其余页并将失败状态正式登记。
- 已完成可验证子阶段（整卷视觉审查证据收敛）：文史类审查覆盖四版 41/41 页；理工农医类独立审查已覆盖 43/50 页，本会话补查印刷版 p11–17，至此理工农医类四版 50/50 页均完成视觉浏览。印刷版 p11–17 未见新增裁切、缺字或分页问题；已发现的内容/图稿问题除外。
- 阶段发现（依据固定原卷及当前源/PDF复核）：文史类第 7 题当前误录成折叠几何题；固定原卷第 36 页题面与第 37 页解析明确为抛物线 $y^2=px$ 与圆 $(x-2)^2+y^2=3$ 相交、求弦中点条件，解析给出 $p=(7-\sqrt{17})/2$，故 ISSUE-0770 现有描述不适用于原卷。理工农医类第 2 题第（8）小题解析把余切差角分母写成 `cosθ−sinθ`，与其计算结果 7 自相矛盾；固定答案为 7，正确公式分母应为 `sinθ−cosθ`。理工农医类第 6 题图稿把题设圆画成以原点为圆心的半径约 $\sqrt3$ 圆，与方程中心 $(2,0)$ 不符；该图在四版输出中重复出现。理工农医类第 7 题折叠后图稿注记与虚线相交，属于版式缺陷，题意及既有 ISSUE-0773 不变。两卷试题版首页答案泄漏仍待用户选择。
- 阶段验证：固定来源 PDF `src-arts-3.png`、`src-arts-4.png` 与当前输出问题页高分辨率图对照；本会话逐张检查理工农医类印刷版 p11–17。理工农医类剩余 7 页已补齐先前独立审查的 43 页覆盖，当前所有 91 个版页均有视觉审查覆盖；页面级工作项尚未完成登记，正式回执未更新。
- 阶段修改文件：仅本进度文件；来源转录、解答、图稿、manifest、provenance、review work items 和正式 receipts 均未改动。
- 剩余任务：依证据修正文史类第 7 题及图稿/解析、理工农医类第 2 题解答公式、理工农医类第 6 题图稿和第 7 题重叠注记；按官方生命周期处理 ISSUE-0770 并登记新增问题；等待首页答案泄漏选择；随后刷新来源核验、两卷八版重建与仅对变化/未能证明相同的页面复核，登记最终回执并完成批次门禁。
- 下一步：先把本阶段审查范围与发现作为进度 checkpoint 提交；继续只读查明 manifest 图稿登记、问题账和 provenance 更新的事务流程，避免直接改生成状态或覆盖现有记录。
- 已完成可验证子阶段（来源/图稿修正）：按固定原卷第 36—37 页，将文史类第 7 题及答案/解析改回抛物线与圆问题，新增 TikZ 图稿，并移除不再引用的两份文史折叠图；理工农医类第 2(8) 解析修正余切差角分母及代入符号；第 6 题图稿将圆心移至 $(2,0)$ 并按题设抛物线、上半平面交点和中点重绘；第 7 题图稿移除与虚线相交的多余注记。首页答案-bearing 编辑说明未改。
- 阶段修改文件：两卷规范题面/解析/答案源、文史类答案要点、三份规范 TikZ 图稿及两份废弃图稿删除、`source-manifest.json` 文史 Q7 图登记与索引说明、生成的两卷 `questions.tex/answers.tex/index.json`、文史类派生《含解析》、`tests/test_generate_projects.py`、本进度文件。来源清单删除文史折叠图登记并登记新 Q7 图，实际引用数为 2。
- 阶段验证：新增两条真实生成器回归测试均先按预期 RED（错录题目/错误公式），修复后 GREEN；`solution_sources.py extract-batch --write` 提交 4 个派生目标；`generate_projects.py --batch phase2-b57 --write` 写入 5 个目标。其后 `source_manifest.py validate`、两卷 `solution_sources.py check-batch`、生成器 `--check`、两条回归测试与 `git diff --check` 全部通过。XeLaTeX 尚未重建，图稿的最终视觉验收仍待 PDF 阶段。
- 剩余任务：查明并按受支持事务更新 ISSUE-0770 与此次已修复问题的登记策略；为 Q7 转录更正刷新来源/provenance 证据；等待试题版首页答案泄漏处理选择；随后重建两卷八版，按新旧页面哈希复用可证明未变的视觉检查、补查变化页，正式登记回执并完成 scoped gates/全量报告。
- 下一步：检查当前问题账、manifest/provenance 工作项和官方 issue/provenance 写入接口；定妥状态更新路径后继续，不重跑已通过的生成器与来源清单验证，除非后续输入变化使其失效。
- 已完成可验证子阶段（文史类第 7 题解答筛选条件补严）：依据独立解题与盲核意见，明确两个不同上半平面交点对应关于 $x$ 的方程有两个不同实根；又因圆上 $x_i\ge2-\sqrt3>0$，两根皆正，故 $x_1+x_2=4-p>0$、$p<4$；结合判别式 $\Delta=(p-2)(p-6)>0$ 及此前已证 $p>0$，得 $0<p<2$，仅 $p=(7-\sqrt{17})/2$ 合题意。结论未改，仅补全筛根逻辑。
- 阶段修改文件：规范解析源 `1986/1986_数学真题_上海文_解析正文.md`、其派生《含解析》、文史类 `answers.tex` 与本进度文件。
- 阶段验证：`solution_sources.py extract-batch --write` 写入 4 个派生目标；`generate_projects.py --batch phase2-b57 --write` 写入 5 个目标。`source_manifest.py validate`、两卷 `solution_sources.py check-batch`、两卷生成器 `--check`、`test_generate_projects.py` 102 项及 `git diff --check` 均通过。独立求解与盲核均确认结论。全套 unittest 共 864 项：850 通过、13 跳过、1 失败；失败仅为全库 `test_the_cached_states_match_the_recomputed_ones`，发现 156 卷缓存状态漂移，未在本批范围内批量改写。
- 剩余任务：尚未刷新文史类 Q6/Q7 provenance 与问题账，尚未重建本批 PDF；答案泄漏处理选择仍待用户决定；其余构建、页面复核、正式回执、清理与全量报告门禁未完成。
- 下一步：先按官方事务接口只更新受影响的文史类 Q6/Q7 provenance，保留其余题目的角色与证据；审阅并更新 ISSUE-0770 等问题记录；随后处理未决答案泄漏选择，再重建并复核受影响版本。此前已完成的 91 页旧 attempt 视觉浏览不当作新 PDF 的复核结论。
- 已完成可验证子阶段（来源核验与局部更新范围审计）：实时 `provenance.py check-batch` 只报告文史类 Q6 题面哈希过期；Q7 题面与答案摘要均已匹配当前源，故从待更新范围剔除。文科当前派生状态 `blocked`、理科 `editions_generated`、批次 `planned`，manifest 缓存仍记旧 `compiled` / `compiled_pending_review`，须在当前来源状态和后续构建后按事务重算。ISSUE-0770 仍为 `open/non_blocking`，旧折叠题描述与固定源实际题目不符；未检出理科 Q2(8) 专属 issue。
- 阶段发现：官方 `import-batch` 强制覆盖整个 phase2-b57 批次的两卷、三个角色和每题记录；`.work/phase2-b57/provenance/` 当前不存在，不能在未完整重建 14 题角色证据的情况下使用。故保留各题现有角色证据，只刷新确实失配的文科 Q6，问题账与 manifest 必须纳入同一状态事务。
- 阶段修改文件：仅本进度文件；审计命令均为只读，没有改 provenance、问题账、manifest、构建产物或工作项。
- 阶段验证：`provenance.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch phase2-b57` 返回预期 `INVALID：2 卷`，唯一内容级失败为文科第 6 题哈希变化；其余是已记录的缓存状态漂移。此前已确认来源清单、两卷解析抽取与生成器校验通过。
- 剩余任务：实现并验证单题 Q6 provenance 与 ISSUE-0770 的原子更新，同时保持其余 13 题记录字节/语义不变；答案泄漏选择仍未决；之后重建两卷八版并逐页复核新 attempt。
- 下一步：使用共享 state transaction 校验当前 revision、重算文科 Q6 摘要、更新 ISSUE-0770 为有固定源证据支持的 resolved 状态，并只为实际更正创建必要的问题记录；提交前核对事务目标只含文科 provenance、问题账及 manifest 状态投影。
- 更正前条核验范围：`check-batch` 每卷只报告首个过期摘要；逐题重新计算后确认文科 Q7 的题面与答案摘要也已过期。实际 provenance 摘要更新范围为文科 Q6 题面、Q7 题面及答案；理科 7 题均无题面或答案摘要漂移。前条所述“Q7 已匹配”不正确，按本条结果继续；其余逐题证据与角色未见漂移。
- 已完成可验证子阶段（局部 provenance 与问题账原子刷新）：在仓库锁内以 state transaction 更新文科 Q6 题面摘要、Q7 题面与答案摘要；将 ISSUE-0770 依固定源第 3—4 页证据标为 resolved 并关联文科 Q7；为理科 Q2 第（8）小题错误分母建立 resolved 的 ISSUE-1038 并关联该题。保留全部三角色身份与既有证据；其余 11 题的全部 provenance 字段未变。事务同批提交两份 provenance、`missing-issues.md` 与 manifest，revision 3931。
- 阶段修改文件：文史类与理工农医类 `provenance.json`、`missing-issues.md`、`source-manifest.json`、本进度文件。
- 阶段验证：两卷 `provenance.py check-batch` 返回 `OK`；状态派生为文科 `answers_verified`、理科 `editions_generated`、批次 `provenance_verified`；`issues.py validate`、`source_manifest.py validate`、`git diff --check` 均通过。提交前逐字段断言仅涉及文科 Q6/Q7、理科 Q2 的摘要/issue 关联，角色身份与答案/转录证据未被改写。
- 剩余任务：旧 build receipts 与 review work items 不能代表更正后的来源状态；两卷八版需重新正式构建并为当前 attempt 逐页复核。两卷试题版首页编辑说明仍泄漏答案 `11π/6` 与 `−π/6`，尚未获得对“修订说明后重建”或“保留原文并登记视觉失败”的选择。中间产物清理、正式回执 finalize、scoped gates 与全量报告更新尚未完成。
- 下一步：先等待首页答案泄漏处理选择；选定后按该边界生成新 attempt、复核新构建中所有变化页（不复用旧 attempt 页面结论），再登记正式复核与收尾门禁。
- 已完成可验证子阶段（phase2-b57 更正后正式重建）：两卷八版正式构建完成，文科 attempt `634fad00-ca04-4a0a-98b8-919432ff65c3`，理科 attempt `17bd4b56-d2e3-4902-8063-63d05bee5ac6`；页数仍为文科 4/18/5/14（41 页）、理科 5/22/6/17（50 页），总计 91 页。所有版本构建日志均无 LaTeX error、Missing character、Overfull 或 undefined reference，receipt problems 为空。
- 阶段验证：构建器返回 `COMPILED_PENDING_REVIEW：2 待审、0 失败`；`validate-receipts --batch phase2-b57` 报 2 pending、0 stale/invalid/missing/failed，provenance `check-batch` 仍为 `OK：2 卷`，source manifest validate 通过。此状态尚非视觉验收完成，不登记正式成功回执。
- 阶段修改文件：两卷四版 PDF、两份 `receipts/build.json`、`source-manifest.json` 与本进度文件；build 目录内非 PDF 中间产物待完成复核后按清理门禁处理。
- 剩余任务：为两个新 attempt 生成并核对 8 份页面级工作项；逐页复核 91 页并在当前 attempt 中据实登记。试题版首页答案泄漏选择仍未决，最终复核登记须遵守用户选择；随后 finalize、清理中间产物、运行 scoped gates 与全量报告校验。
- 下一步：调用 `review_receipts.py prepare-batch` 生成绑定上述 attempts 的工作项，确认 PDF 哈希与页覆盖后再开始逐页检查；不复用旧 attempt 的页面结果。
- 已完成可验证子阶段（当前 build attempt 复核工作项准备）：`prepare-batch` 为新 attempt 刷新 8 份 ignored 工作项；逐项核对 paper/edition/attempt、PDF 路径、SHA-256、页数与 build receipts 一致，页集合精确覆盖文科 41 页和理科 50 页，共 91 页 × 8 项 = 728 条 pending。旧工作项只绑定旧 attempt，不复用其页面结论；先前发现的首页答案泄漏待在新 PDF 上复核。
- 阶段修改文件：ignored `.work/phase2-b57/review/{试题版,解析版,简答版,印刷版}/` 下两卷 8 个当前 attempt 工作项；tracked 文件仅本进度文件。
- 阶段验证：对 8 份 JSON 与两卷当前 build receipts 做只读逐项比较，所有 attempt 与 PDF path/hash/page_count 匹配；页码序列均为 1…N，全部 728 项状态为 pending。正式 review receipts 仍因 build attempt 及四版 PDF 改变而 stale，尚未 finalize。
- 剩余任务：对当前 91 页完成逐页视觉检查并登记真实结果；首页答案泄漏处理选择未回；随后 checked finalize、清理工作项/中间产物与临时 PNG、跑 scoped gates 和全量报告。
- 下一步：按文理两卷独立分工并行复核四版页面；主会话检查关键页和任何代理发现，之后统一写入当前 work items。
- 已完成可验证子阶段（简答版过期答案根因定位）：`make_short_answers.py --batch phase2-b57 --check` 稳定失败且只点名文科 `answers_short.tex`。规范答案要点和 `answers.tex` 的 Q7 答案均为 $(7-\sqrt{17})/2$，但简答版生成源仍是旧折叠题答案 $\arccos(\sqrt3/3)$；刚构建的简答版 PDF 文本亦确认输出该旧值。已完成的 phase2-b56 同一检查通过，表明本批修改答案源后漏跑独立简答答案生成器；正式构建读取旧派生文件而未拒绝，故本次两卷 build attempt 均不得用于最终复核。
- 阶段修改文件：仅本进度文件；诊断未更改规范答案、派生简答源、PDF、review 工作项或 receipts。此前新 attempt 的 review work items 会随下一次重编失效，不沿用。
- 阶段验证：当前失败命令、旧 PDF 文本与规范答案三方交叉确认 Q7 错答；phase2-b56 参照检查通过。理科简答源与答案核验未发现不一致。
- 剩余任务：用 `make_short_answers.py --write` 同步文科速查答案并 `--check`、定向测试；重建两卷八版获得新 attempts，再刷新工作项和逐页视觉复核。
- 下一步：只生成当前 phase2-b57 简答答案目标，检查 diff 确认为 Q7 单值更新后，重跑生成器检查和简答相关测试，再正式重编。
- 已完成可验证子阶段（简答答案派生修复）：执行 `make_short_answers.py --manifest source-manifest.json --batch phase2-b57 --write`，只将文科 `answers_short.tex` 第 7 题从旧折叠题答案 $\arccos(\sqrt3/3)$ 更新为规范答案 $(7-\sqrt{17})/2$；理科简答源无变化。旧 attempt 的 PDF 与全部旧 attempt review 工作项作废，不得登记为最终结果。
- 阶段修改文件：文科 `1986_上海卷_文史类/answers_short.tex` 与本进度文件。
- 阶段验证：`make_short_answers.py --check` 对 b57 两卷均通过；`tests/test_short_answers.py` 50 项全通过；生成 diff 仅含 Q7 最终答案一行；`git diff --check` 通过。
- 剩余任务：重新正式构建两卷八版并验证新 build receipts/日志；随后重置 8 份 review 工作项绑定新 attempts，再进行 91 页逐页视觉复核。首页答案泄漏用户选择仍未决。
- 下一步：重跑 `build_projects.py build --formal --batch phase2-b57`，确认页数、警告、输出哈希与新的 attempts，再准备新复核工作项。
- 已完成可验证阶段（简答答案修复后重建）：phase2-b57 两卷八版重新正式构建成功。文史 attempt `82cfd59c-7c07-40ea-bb71-438a59b57801`，理工农医 attempt `15a812fe-aba2-4294-a00d-222fb0d66bc3`；页数分别为 4/18/5/14 与 5/22/6/17，总计 91 页。文史简答版 PDF 文本已确认 Q7 输出 $(7-\sqrt{17})/2$，不再是旧折叠题答案。
- 阶段修改文件：两卷 `receipts/build.json`、`source-manifest.json` 与本进度文件；八份 PDF 为 ignored 构建产物。
- 阶段验证：正式 build 返回 `COMPILED_PENDING_REVIEW：2 待审、0 失败`；`validate-receipts`、`provenance check-batch`、`make_short_answers.py --check` 均通过。八版日志逐项为 0 errors、0 missing characters、0 overfull、0 undefined references；页数与既有版式一致。尚未完成视觉验收，不将 pending 描述为正式通过。
- 剩余任务：为新 attempt 刷新并核对 8 份 review work items；完成 91 页当前 PDF 逐页视觉复核并记录结果。试题版首页答案泄漏的处理选择仍未收到，故可记录已知失败但不得擅自改编辑说明或 finalize；随后还需正式登记、清理中间产物、运行 scoped gates 和全量报告。
- 下一步：准备当前 attempt 的复核工作项，核对其 PDF 哈希、attempt 与页覆盖；之后启动新一轮逐页视觉复核，不复用旧 attempt 的页面结论。
- 已完成可验证阶段（当前 attempt 复核工作项刷新）：`review_receipts.py prepare-batch --manifest source-manifest.json --batch phase2-b57` 为文史/理工农医两卷四版生成并刷新 8 份 ignored work items，均绑定本轮 attempt（文史 `82cfd59c-7c07-40ea-bb71-438a59b57801`、理工农医 `15a812fe-aba2-4294-a00d-222fb0d66bc3`）。
- 阶段修改文件：ignored `.work/phase2-b57/review/{试题版,解析版,简答版,印刷版}/` 内 8 个 JSON work items；tracked 仅本进度文件。
- 阶段验证：逐项对照 build receipts，8 项的 attempt、PDF path/SHA-256/page_count 一致；页码连续覆盖 91 页，728 项检查全部 pending。此步骤不复用旧 attempt 的审查结论。
- 剩余任务：对新 attempt 的 91 页完成逐页视觉审查并写入准确结果；首页试题版答案泄漏已知，须保留失败事实，用户此前的处理选择未收到。其后才可 checked finalize、清理中间产物、运行 scoped gates 和全量报告检查。
- 下一步：文史类与理工农医类各由独立审查者检查四版全部页面，主会话复核重点页与代理报告证据，再更新当前工作项；不写正式回执，直到所有页面结论真实且首页失败处置边界明确。
- 已完成可验证子阶段（当前 attempt 首页泄漏复核）：对当前 attempt `82cfd59c…` 与 `15a812fe…` 的两份试题版第 1 页执行高分辨率渲染并目视确认；首页“版式与异文说明”均直接列出第 9 题答案 $11\pi/6$ 与 $-\pi/6$。已在各自当前 work item 将 `answer_leak` 与页面结果登记为 `fail`，其余首页检查仍 pending；未修改试题源或正式回执。
- 阶段修改文件：ignored `.work/phase2-b57/review/试题版/gk-1986-regular-shanghai-{arts,science}.json` 与本进度文件。
- 阶段验证：两份当前 PDF 首页的 PNG 目视图与 `pdftotext -f 1 -l 1` 交叉确认泄漏；工作项仍绑定本轮 attempt/PDF 哈希。`review_receipts.py check-batch` 仍报 `INVALID_OR_STALE`，原因是正式回执尚未刷新至新 attempt（属预期），当前不做 finalize。
- 剩余任务：完成其余 90 页及两首页其他七项检查，复核两名审查者的全页报告；保持已确认失败事实，首页内容改动与否仍待用户决定。未通过前不 finalize。
- 下一步：继续本轮文史与理工农医四版逐页视觉检查，主会话优先抽查文史 Q7、理工农医 Q2/Q6/Q7 当前输出，并与独立报告比对。
- 已完成可验证子阶段（关键问题页当前 attempt 抽核）：主会话高分辨率检查文史解析版 p18、印刷版 p14，Q7 抛物线—圆图、筛根说明与 $(7-\sqrt{17})/2$ 结论均清晰完整；理工农医试题版 p5 的 Q6 圆心标记为 $(2,0)$、抛物线关系与 Q7 两幅折叠图标签清楚；解析版 p20–22 公式与分页连续；印刷版 p12 余切差角分母为 $\sin\theta-\cos\theta$ 且结果为 7，p16–17 的 Q7 图和解析清晰。
- 阶段修改文件：仅本进度文件；复核图像生成于 `/tmp/phase2-b57-current.2cooZS/`，尚未清理。试题版首页失败仍登记在两个 ignored work items。
- 阶段验证：以上页面以当前 attempt PDF 的 135 dpi 页面渲染图逐页目视；与当前生成源和 `pdftotext` 页面定位相符。在本阶段抽查页面中，未见答案泄漏以外的新缺字、裁切、错误标注或严重分页问题；这不替代其余未覆盖页的复核。
- 剩余任务：两名独立审查者仍需提交全部 41/50 页覆盖和 findings；主会话还需确认其报告及覆盖边界，再写完 728 项当前 work items。答案泄漏处置选择未收到，不改题面且不 finalize。
- 下一步：取得并核验两名独立审查者报告；如发现任何其余页面问题，回到对应源修正、重建并重审受影响版本；若仅有已登记首页泄漏，则完成其余检查并保留该失败待用户裁决。
- 已完成可验证阶段（文史类新 attempt 全页视觉复核）：独立审查者逐页渲染检查当前文史类四版 41/41 页（试题 4、解析 18、简答 5、印刷 14），无未确认页。发现试题版 p1 的答案泄漏；另报告试题版 p4 与简答版 p5 留白偏多。主会话复看两页，判定均为卷末题目/短答案版内容稀疏所致，正文完整、无异常分页或裁切，`pagination_whitespace` 可记 pass 并附说明。Q7 当前解析版 p18、印刷版 p14、简答版 p5 结论均为 $(7-\sqrt{17})/2$，图稿和公式清楚。
- 阶段修改文件：仅本进度文件；当前文史试题版 p1 `answer_leak`/页结果 fail 已写入 ignored work item。其余 40 页的八项结果尚待与理工农医类报告合并后统一写入 work items；没有写正式回执。
- 阶段验证：页覆盖由独立审查逐页报告；主会话高分辨率抽查文史 p1、p4、简答 p5、解析 p18、印刷 p14，核实泄漏、留白判定与 Q7 排版。当前 attempt 绑定不变。
- 剩余任务：取得理工农医类完整报告；核对全部页面 findings 后写满两卷 728 项检查，跑 work-item 校验。首页答案泄漏保留 fail、等待用户决定是否修订。
- 下一步：核验理工农医类 50 页审查报告与未决 findings；随后统一登记全部页面结果，并用官方 check 工具验证 work items 后再决定是否 finalize。
- 已完成可验证阶段（理工农医类新 attempt 全页视觉复核）：独立审查者逐页渲染检查当前理工农医类四版 50/50 页（试题 5、解析 22、简答 6、印刷 17），无未确认页。确认试题版 p1 同样泄漏第 9 题幅角主值 `11π/6` 与 `−π/6`；Q2(8) 当前解析版 p15、印刷版 p12 均清楚显示分母 $\sin\theta-\cos\theta$ 且结果为 7；Q7 折叠图标签、虚线与直角标记清楚。
- 阶段发现（需纯版式修复）：Q6 抛物线—圆图的中点标签 M 放在弦 AB 与辅助虚线相交点，文字与图线挤叠。独立审查者指出此图重复出现于试题版 p5、解析版 p5/p20、简答版 p5、印刷版 p4/p15。主会话在 300 dpi 放大试题版 p5 和印刷版 p15 确认 M 字形下部被弦线/虚线穿过；TikZ 源也确认标签锚点与交点完全重合。此项仅为标注位置，不涉及题意/数据。
- 阶段修改文件：仅本进度文件；当前理工农医试题版 p1 `answer_leak`/页结果 fail 已登记于 ignored work item。其余工作项尚未写；当前 attempt 的正式回执未变。
- 阶段验证：独立报告覆盖四版 50 页且未确认页为 0；主会话抽核试题 p1/p5、解析 p20–22、印刷 p12/p15–17 和图稿放大，交叉验证首页泄漏、Q6 标注重叠、Q2(8) 公式与 Q7 图稿。除两卷首页答案泄漏与本条 Q6 M 标签碰线外，未报告其他明显页面问题。
- 剩余任务：在获准的纯版式修复边界内微调理工农医 Q6 图稿 M 标签，单卷重建后复核六个受影响页；其余 91 页审查结论待写入 728 项 work items。两卷首页答案泄漏仍待用户裁决，故不能最终 finalize。
- 下一步：按纯版式范围实施 M 标签偏移，用当前图形源重建理工农医四版，先比较 attempts/页数/日志，再高分辨率复核六个引用页；不改题面、题目数字、答案或结论。
- 已完成可验证阶段（理工农医 Q6 图稿标注修复及复建）：先把 M 改为 `above left` 后的高分辨率视觉检查看到字形仍过近圆弧，故继续仅加 $x=-4$ pt、$y=+4$ pt 偏移；点标记仍在 $(1.281,1.281)$，仅文字移位。最终科学卷正式 attempt 为 `dea4108d-f233-4641-8050-e2fac5986bb0`（上一试编 `e670ea51-5ad9-4219-9d67-8a711457fd4c` 已被替代）；四版页数保持 5/22/6/17，共 50 页。
- 阶段修改文件：理工农医 `figures/f1986_shanghai_science_t6_parabola_circle.tex`、该卷 `receipts/build.json`、`source-manifest.json` 与本进度文件。六份构建 PDF 为 ignored 输出，渲染图在 `/tmp/phase2-b57-current.2cooZS/`。
- 阶段验证：来源清单 validate、两卷生成器 `--check`、两卷 provenance check、简答答案 `--check`、两卷 build receipt validate 均通过；本轮科学卷四版全为 succeeded，零 warning/problem/error/missing-character/overfull/undefined-reference。对试题 p5、解析 p5/p20、简答 p5、印刷 p4/p15 逐页重渲染，且试题 p5 做 300 dpi 局部放大；最终 M 标签与弦/辅助虚线/圆弧分开，点位、图形关系与文字数学内容不变。
- 剩余任务：旧科学卷 review work items 绑定已替代 attempt，须刷新至 `dea4108d…`；在最新 attempt 上复核这六个变化页并维护 50 页审查覆盖。文史 41 页仍绑定 `82cfd59c…`。两卷首页答案泄漏仍待用户裁决，暂不 finalize。
- 下一步：调用官方 `prepare-batch` 刷新 stale work items，核对文史 attempt 保持不变、科学卷绑定 `dea4108d…`，再把两卷审查报告映射到当前 work items；变化的六页以本轮放大图为依据，其余页需保持有明确当前 attempt 覆盖证据。
- 已完成可验证子阶段（新科学 attempt 工作项刷新）：官方 `prepare-batch` 首次因文史四份工作项仍绑定当前 attempt 而按安全机制拒绝覆盖。为保留文史 p1 已登记的 fail，本会话将四份文史工作项临时移入 ignored 备份目录 `.work/phase2-b57-preserve.0eOupU/current-arts/`，调用官方命令刷新八项，再把新生成的文史空白项另存并恢复原文史项；因此文史仍绑定 `82cfd59c…`，科学四项现绑定修复后的 `dea4108d…`。临时备份均保留，未删除工作项。
- 阶段修改文件：ignored `.work/phase2-b57/review/` 内 8 个工作项；当前两卷试题版 p1 `answer_leak` 和页结果各为 fail，其余 726 个检查仍 pending；另有 ignored 的可恢复临时备份目录。
- 阶段验证：8 个工作项总计 91 页、728 检查；逐项核对 build attempt、PDF 路径、SHA-256、page_count 与各卷 receipt 一致，页码覆盖连续且完整。新科学 attempt 首页再次用当前 PDF 高分辨率图确认答案泄漏后才登记 fail。临时文史原件恢复后页1批注仍在。
- 剩余任务：独立审查者需针对最新科学 attempt `dea4108d…` 再次确认全部 50 页（尤其六个重绘图页面）；随后把两卷已审查页面的检查结果完整写入当前 work items、验证 728 项状态。首页答案泄漏选择仍未收到，未 finalize。
- 下一步：取得最新科学 attempt 复查报告，核实修复后 M 标签清晰且无其他变化，再将审查结果登记到当前工作项并复核 JSON/官方回执门禁。
- 已完成可验证子阶段（文史类当前工作项登记）：依据 41/41 页独立审查及主会话重点页复核，将当前文史四版 328 项检查写入对应 ignored work items；327 项 pass，文史试题版 p1 `answer_leak` fail，其余无 pending。p4 与简答版 p5 的留白按主会话复看记为 pass 并注明是正常卷末/短答案版留白。
- 阶段修改文件：文史四版 ignored `.work/phase2-b57/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-shanghai-arts.json`；tracked 仅本进度文件。
- 阶段验证：只读校验确认 41 页页码连续、每页八项齐全、attempt/PDF 绑定当前文史 receipts；全部结论为 327 pass、1 fail、0 pending。未更新正式 `receipts/review.json`，未 finalize。
- 剩余任务：最新科学 attempt `dea4108d…` 的 50 页复查仍在进行；完成后登记当前科学 work items，连同文史组成 91 页/728 项门禁。两卷试题首页答案泄漏仍各一项 fail，正式处置与 finalize 需遵守用户选择。
- 下一步：收取并验收科学卷新 attempt 全页报告，重点确认 Q6 六页标签已充分避开弦、虚线与圆弧，再登记其 400 项结果。
- 已完成可验证阶段（理工农医类当前 attempt 全页复核登记）：依据独立复核者对最新 attempt `dea4108d-f233-4641-8050-e2fac5986bb0` 的 50/50 页检查报告（0 页待确认），将科学卷四版 400 项检查写入当前 work items。Q6 六个图稿页的 M 标注与弦、辅助虚线及圆弧清楚分离；Q2(8) 解析/印刷页分母为 `sinθ−cosθ` 且结果为 7；Q7 折叠图标注清楚。科学卷试题版 p1 `answer_leak` 维持 fail。
- 阶段修改文件：ignored `.work/phase2-b57/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-shanghai-science.json`；tracked 为本 `PROGRESS.md`。未改正式 review receipts、题源、build receipt 或 PDF，也未重编。
- 阶段验证：只读审计 8 份当前 work items，覆盖两卷 91 页、728 项检查，结果为 726 pass、2 fail、0 pending；两项 fail 精确为文史及理工农医试题版 p1 的 `answer_leak`。8/8 项的 attempt、PDF 路径、实际 SHA-256、页数均匹配各自 build receipts；页码连续、每页八项齐全、失败项有说明，官方 `_validate_pages` 校验通过。
- 剩余任务：两卷试题版首页答案泄漏的处置选择尚未收到；因此保留源文和两项失败，不写正式 `receipts/review.json`、不 finalize。之后还需依授权完成正式复核登记、清理明确属于本批的构建中间产物/临时渲染文件，并跑批次门禁及报告校验。
- 下一步：等待并遵循用户对两卷首页泄漏的处置选择；若保留原文，则按失败状态走受支持登记流程；若批准改注，先重跑该卷所需来源核验、构建与受影响页面复核，再更新工作项。未获选择前不 finalize、不清理 PDF 或任何有歧义的文件。

### `phase2-b58` — 1986 广东卷文史类

- 已完成可验证子阶段（批次预检）：当前批次仅含文史卷。现有正式构建 attempt `59421cf0-2381-47e1-b9b0-8920b160fbd7` 的四版 PDF 均存在且与旧 build receipt 哈希一致，共 65 页（试题 7、解析 28、简答 8、印刷 22）；但 receipt validator 判定生成输入树与工具链指纹已过期。4 份旧 work items 全为 pending，绑定旧 attempt `17d0a798-ef8c-4746-ae74-e70cd1331e80`，不复用其审查状态。
- 阶段修改文件：仅本进度记录；题源、provenance、build receipt、PDF 与 review work items 均未改。
- 阶段验证：source manifest、项目生成、简答答案、解析源一致性、四版入口生成器检查均通过。`provenance.py check-batch` 只报告缓存批次状态 `compiled_pending_review` 与现场派生 `provenance_verified` 不符，未报告逐题 provenance 内容错误；`build_projects.py validate-receipts` 报生成树/工具链漂移。首次并行运行只读检查时因共享 `RepoLock` 互斥导致生成器检查失败，改为串行重跑后通过；未删除或绕过锁文件。
- 剩余任务：重建当前 attempt，确认四版构建日志和页数；刷新四个当前 attempt 工作项；逐页复核 65 页并登记结果；按门禁 finalize、清理本批中间产物、运行 scoped gates 和全量报告检查后提交。
- 下一步：串行执行 `phase2-b58` 单卷正式重建；随后用官方 `prepare-batch` 刷新工作项并核对 PDF 哈希绑定，再开始逐页视觉审查。`phase2-b57` 的两项首页答案泄漏失败继续保留，未被本阶段改动。
- 已完成可验证阶段（当前 attempt 正式重建）：单卷正式构建完成，manifest revision 3941；新 attempt 为 `27645bca-21d1-4984-9a5a-28d663584373`。四版页数仍为试题 7、解析 28、简答 8、印刷 22，共 65 页。
- 阶段修改文件：1986 广东文史项目 `receipts/build.json` 与四份 ignored `build/*.pdf`；`source-manifest.json` 状态事务更新；本进度文件。旧 attempt 的四份 review work items 暂未刷新。
- 阶段验证：构建状态 `COMPILED_PENDING_REVIEW`，1 卷待审、0 构建失败；`validate-receipts`、provenance check-batch、source manifest validate 均通过。逐版核对实际 PDF SHA-256 与 receipt 一致；四版均 succeeded，错误、缺字、Overfull、未解析引用数量均为 0。
- 剩余任务：为新 attempt 刷新四份 review work items，核对哈希与完整页集合；完成 65 页逐页视觉审查并登记检查项；之后按门禁 finalize、清理本批中间物、运行 scoped gates 和全量报告检查。
- 下一步：执行官方 `review_receipts.py prepare-batch --manifest source-manifest.json --batch phase2-b58`，确认四份工作项绑定新 attempt `27645bca…` 和当前 PDF 哈希，然后启动四版分工审查。
- 已完成可验证子阶段（当前 attempt 复核工作项准备）：官方 `review_receipts.py prepare-batch` 已为四版创建/刷新 4 份 ignored 工作项，全部绑定 attempt `27645bca-21d1-4984-9a5a-28d663584373`。
- 阶段修改文件：ignored `.work/phase2-b58/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-arts.json` 与本进度文件；未改题源、build receipt 或正式 review receipt。
- 阶段验证：四个工作项的 PDF 路径、SHA-256、页数与当前 build receipts 及实际文件一致；页码连续覆盖 65 页，每页八项齐全，520 项均为 pending。四版候选页均为 p1，当前构建没有 Overfull 警告。
- 剩余任务：对当前 attempt 全部 65 页完成视觉检查，候选首页高分辨率复核，逐项写入 520 个有依据的结论；随后才进入 finalize、清理和完整门禁。
- 下一步：按四个版次并行完成逐页视觉审查，独立审查者各自记录页覆盖和异常；主会话核对全部页数、重点页及 PDF/receipt 绑定后再登记工作项。
- 已完成可验证子阶段（前三版逐页复核及版式根因确认）：试题版 7/7 页、简答版 8/8 页、印刷版 22/22 页已由独立审查覆盖；主会话从当前 attempt 的简答版 p7 以 300dpi 渲染并放大确认，三棱锥图 E 字母被三角形边线穿过，属真实纯版式缺陷。图稿根因是 `figures/f1986_guangdong_arts_t6_pyramid.tex` 中 E 点坐标 `(2.4,0.5)` 使用 `node[right]`，与 C—B 斜边及邻近辅助线发生文字/线条冲突。图稿由 `questions.tex` 和 `answers.tex` 共用，当前 PDF 中对应页为：试题版 p7、解析版 p7 与 p27、简答版 p7、印刷版 p6 与 p21；解析版全页复核报告尚待收齐。
- 阶段修改文件：仅本 `PROGRESS.md`；当前正式源、manifest、build receipt/PDF 和 review work items 均未改。主会话放大图位于 `/tmp/phase2-b58-main.5Ur0mk/`。
- 阶段验证：当前工作树在 `feat/gaokao-phase0`，恢复核对时 tracked diff 与状态均干净；图稿源检索确认只在问题页和答案页两处引用。以 `pdftotext` 对当前四版定位到上述包含三棱锥题面的全部页，简答版 p7 的 300dpi 局部放大直接显示 E 标签被边线穿过；其余两个版次代理未报此缺陷，故后续重建后将对全部六个实际图稿页逐页高分辨率复核，不能沿用旧 attempt 结论。
- 剩余任务：完成解析版 28 页当前 attempt 的独立复核；为 E 标签选取不与边线/辅助线相交的最小位置调整；四版正式重建并刷新 work items；复核 65 页，特别是六个图稿页，登记真实结果，再进入批次 finalize、清理和全量门禁。
- 下一步：收齐解析版审查结果；然后仅调整图稿标签位置（不动点位、线段、题目数字或数学内容），正式重建四版，并核验六处图稿输出。
- 已完成可验证阶段（四版当前 attempt 全页复核与主会话验收）：四名独立审查者共覆盖 65/65 页（试题 7、解析 28、简答 8、印刷 22），均无未确认页。主会话在当前 PDF 以 300dpi 复核图稿，确认 E 标签遮叠见于试题版 p7、解析版 p7/p26、简答版 p7、印刷版 p6/p21；第 26 页是解析版答案区附带题面图，解析版 p27 仅含解答，故更正前条所记页码。解析版 p2、p9 的第（6）小题题首距上一题选项分母较近，但主会话高分辨率检查未见字形相碰、裁切或辨认困难；作为已记录的轻微留白观察，不扩展本次修复范围。
- 阶段发现（内容阻塞，尚未处置）：试题版 p1 来源说明框明确展示解答页数值 `S20=180`，p6 又展示对应判别式结论；主会话 300dpi 页面图和 PDF 文本层均确认可读。此为答案泄漏，不是图稿版式问题；为避免擅改内容/题面，保留现状并标为待处置项，不把它计作视觉通过。第 5 页空白 A—E 图形区及第 6 页原源方框缺字按页面注释属于已披露源缺项，不误报成渲染裁切或字体故障。
- 阶段修改文件：仅本 `PROGRESS.md`；当前源文件、manifest、build receipt/PDF 与 review work items 未改。主会话 300dpi 预览存于 `/tmp/phase2-b58-main.5Ur0mk/`。
- 阶段验证：四份审查报告均声明当前 attempt `27645bca-21d1-4984-9a5a-28d663584373`、PDF 哈希匹配且各版全页覆盖；主会话独立放大了共享图稿在试题版 p7、解析版 p26、简答版 p7、印刷版 p21 的实际输出，逐页确认 E 标签与斜边相交；对解析版 p2/p9、试题版 p1/p6 做高分辨率和文本层交叉检查。题面及答案数字未改，正式 work items 仍待后续按新 attempt 生成/登记。
- 剩余任务：仅修复 E 标签位置并正式重建四版，之后刷新 work items、复查当前批次 65 页和六处图稿页、如实登记检查结果；另需决定如何处置试题版 p1/p6 的答案泄漏后再走 finalize。完成后清理中间产物与临时图像，运行 scoped gates 和全量报告检查。
- 下一步：以当前 p7/p26 等 PDF 作为修复前 RED 证据，只改 TikZ 中 E 的文字锚点/偏移，不动点位和任何题目数据；单卷正式重建后以六页高分辨率输出验证 GREEN，随后刷新并填完当前 attempt 的 520 个复核检查项。
- 已完成可验证子阶段（E 标注首次微调与正式试编）：将 TikZ 的 E 标签从 `right` 改为 `below left`，保持点 E、所有线段及题目/答案不变；正式四版 build attempt `f21ea186-681b-4a33-b05c-b76dbe9425aa` 成功，manifest revision 3942，页数仍为 7/28/8/22。
- 阶段验证：build receipt validator 与 `provenance.py check-batch` 均通过，四版编译日志无错误、缺字、Overfull 或未解析引用。修复后简答版 p7 以 300dpi 检查确认原先 E 字母被 C—B 斜边穿过的问题已消除，但 E 与 D 两个字母靠得过近；该视觉回归仍为 RED，故此 attempt 不接受、不准备当前复核工作项，需再微调标签。
- 阶段修改文件：图稿 `figures/f1986_guangdong_arts_t6_pyramid.tex`、仓库正式生成的广东文史 `receipts/build.json` 与 `source-manifest.json`、本 `PROGRESS.md`；四份新 PDF 为 ignored 构建输出，预览在 `/tmp/phase2-b58-post.wE2rvP/`。试题版 p1/p6 的答案泄漏问题尚未处置。
- 剩余任务：继续只调整 E 字母的排版偏移，避免遮边且与 D 留出清晰间隔；重新正式构建四版并逐页高分辨率检查六处图稿，随后才刷新 review work items。答案泄漏继续保留为未决 blocker。
- 下一步：在 `below left` 基础上给 E 标签增加少量向右和向下偏移；以同一简答版 p7 300dpi 图作回归检查，确认 E 不碰 C—B / D—B 边线且与 D 分离，再重建四版。
- 已完成可验证子阶段（E 标注第二次位置试验；仍未通过）：将 E 标签改为 `below left,xshift=2pt,yshift=-3pt` 并正式四版重建，当前 attempt `cecb27c3-9923-45ab-81d9-8d3aefb0c10c`，manifest revision 3944，页数不变。
- 阶段验证：source manifest validate、provenance check-batch、build receipt validator 均通过；四版均 succeeded，零编译错误/缺字/Overfull/未解析引用。300dpi 复查发现 E 与斜边已分开且 D/E 文字分开，但较大的向下位移使 E 字形与底边 AB 相碰；视觉回归仍 RED，不接受该 attempt，不刷新复核工作项。
- 阶段修改文件：同一图稿、广东文史 `receipts/build.json`、`source-manifest.json` 与本进度文件；4 份 PDF 为 ignored 构建输出，第二次试验页图位于 `/tmp/phase2-b58-final.Mfd03l/`。未更改题面、答案或 provenance 逐题记录。
- 剩余任务：保持 E 标签在点左下方且不改变点位，去掉造成底边相碰的 yshift，仅用小幅横移增加其与 D 的可辨间隔；重新正式构建并复核六个图稿页。试题版 p1/p6 的答案泄漏仍为未决 blocker。
- 下一步：用 `below left,xshift=3pt` 作第三次定向试验（相对第二版不再下移，避免触及 AB；相对第一版向右移开 D），正式重建后放大六页确认。
- 已完成可验证子阶段（第三次位置试验及结构性根因核对；仍未通过）：正式 attempt `70e92843-0d54-4077-a91c-6020502de226` 四版均成功、manifest revision 3946，页数维持 7/28/8/22。E 标签改为 `below left,xshift=3pt` 后，六处输出仍需最终验收；简答版 p7 的 300dpi 2×局部放大确认 E 字母底横与 AB 底边相碰，当前版仍 RED，不刷新/登记 work items，不 finalize。
- 根因证据：固定源 PDF 第 9 页（书页 268）的原始三棱锥图只标 S、A、B、C，没有 D/E 辅助点；项目共用 TikZ 在题面和答案中均加了 D/E，E 标签所在区域同时受 C—B、D—B、D 标签及 AB 底边限制。连续三个只调 E 锚点/偏移的试验均未通过（依次压斜边、挤近 D、触碰 AB），不再盲试第四种偏移。源 PDF 渲染有 JBIG2 解码警告但生成的 p9 页面图可读；不据此推断源文件损坏。
- 阶段修改文件：广东文史三棱锥 TikZ 图稿、正式 build receipt、`source-manifest.json`、本 `PROGRESS.md`；四版 PDF 为 ignored 构建输出，最新放大图在 `/tmp/phase2-b58-verify.zBx5hu/`，来源扫描页图在 `/tmp/phase2-b58-source-p9-09.png`。未改题面正文、辅助点坐标、答案或逐题 provenance。
- 阶段验证：当前 attempt 的 build receipt validator、provenance `check-batch` 与 source manifest validate 均 exit 0；四版编译零错误/缺字/Overfull/未解析引用。主会话高分辨率查看六处当前图稿输出，并 2×放大简答版 p7；E 与 AB 仍相碰，不能登记为版式通过。已向用户请求选择是否拆分题面图/解析图，以及是否概括试题版的答案泄漏说明；等待答复。
- 剩余任务：根据用户对图稿结构和试题版说明的选择继续；之后正式重建、刷新 work items、完成当前 attempt 全页复核并如实处理答案泄漏，再进入批次收尾。未获选择前不再改图稿或泄漏说明。
- 下一步：等待用户答复；按获准方向开展最小改动，并以固定源图、六个含图输出页和最新 attempt 逐项验收。若用户选择保留当前内容，则将相关页记 fail/blocker，不伪报通过。

### `phase2-b58` 恢复续做：来源图稿架构与试题版答案隔离

- 恢复检查：当前规范工作树 `仓库根`、分支 `feat/gaokao-phase0`、HEAD `ce373bc4`；恢复时工作树干净。先读本进度尾部与 SDD 账本，未重跑已完成批次。当前四版 PDF 仍对应 attempt `70e92843-0d54-4077-a91c-6020502de226`。
- Ruling：将原卷题面三棱锥图与解析辅助图拆开，并按固定源修正题面图中 AC 为虚线；固定源 PDF 第 9 页可见原图仅标 S/A/B/C 且 AC 为隐藏线，三次仅调整 E 字标签均未通过。成本若判断错误：需重新制图、重建并复核本卷，但不会改题目数据或结论。
- Ruling：试题源的第 2(9) 题说明改为不披露具体答案/判别式的中性说明；完整冲突证据继续保留在答案要点与解析源中。试题版是无答案卷，当前说明直接暴露 `S20=180` 与负判别式。成本若判断错误：试题卷少了具体编辑背景，但题面照录、来源冲突和解析证据仍保留在答案版。
- 已完成可验证阶段（回归测试 RED）：新增真实生成路径回归测试，要求题面生成只引用来源图，解析生成另引用含 D/E 的辅助图，图登记次数分别为 2/1，试题版生成结果不含 `$S_{20}=180$` 或判别式结论。当前测试按预期失败：生成的题面仍引用旧共享图 `f1986_guangdong_arts_t6_pyramid`。
- 阶段修改文件：`math-gaokao-latex/tests/test_generate_projects.py`（仅新增回归测试）；本 `PROGRESS.md`；SDD 忽略账本同步追加本次裁定。源 Markdown、图稿、manifest、构建回执与 PDF 尚未改。
- 阶段验证：固定源 PDF 第 9 页 150dpi 渲染确认 S/A/B/C 与 AC 虚线；当前简答版 PDF SHA-256 与 build receipt 一致，300dpi 第 7 页复现 E 标签与底边拥挤。`python3 -m unittest discover -s tests -p test_generate_projects.py -k 1986_guangdong_arts_question_figure_is_source_faithful` 返回 1 项失败，失败点是题面仍引用旧共享图，符合预期 RED。
- 剩余任务：按裁定更新规范 Markdown、拆分并修正两份 TikZ、登记第二份图稿并同步引用次数；运行生成器、provenance 与单卷四版正式构建；对变化页复核并以像素一致性证据复用未变化页的既有审查，不重复整批人工审查。批次 finalize、清理、scoped gates、全量报告检查与提交仍未完成。
- 下一步：先以最小改动更新源 Markdown 与图稿，运行同一回归测试至 GREEN，再按受支持入口重生成 `questions.tex`/`answers.tex` 并检查精确 diff；题面哈希变化时重跑该卷 provenance 后才正式构建。

### `phase2-b58` 续做：源稿拆分、登记与生成器验证

- 已完成可验证阶段：按已记录裁定将 1986 广东文史卷题面图与解析辅助图拆开。题面图仅保留固定源中的 S/A/B/C，并将隐藏棱 AC 画为虚线；解析版单独引用含 D/E 的辅助图。试题版第 2(9) 题说明改为中性描述，具体答案及判别式推导不再出现在试题源，解析与答案证据仍保留。新增图稿登记并将引用次数更新为题面图 2 次、解析图 1 次，manifest revision 3948、事务 `c2033700-0a3b-4b48-929a-aceb74093eea`。
- 阶段修改文件：两份规范 Markdown（试题、解析正文）；项目生成文件 `questions.tex`、`answers.tex`、`index.json`；新增题面/解析 TikZ 并删除旧共享图；`source-manifest.json`；`tests/test_generate_projects.py`；本 `PROGRESS.md`。provenance 三角色草稿位于 ignored `.work/phase2-b58/provenance/`，未写正式 provenance。
- 阶段验证：真实生成路径回归测试 `test_1986_guangdong_arts_question_figure_is_source_faithful` 已从预期 RED 转为通过；源清单 validate、图稿引用计数核对、phase2-b58 解析派生源检查、项目生成 `--check` 均通过。正式 provenance 导入 dry-run 校验三角色七题记录通过，但正式 `check-batch` 仍按预期报告旧 provenance 哈希与新源不符，尚未执行写入事务。
- 哈希核对补充：对比当前题面规范源与既有正式记录，变化的是第 2 题（中性化冲突说明）和第 6 题（题面图由旧共享图片改为新登记矢量图），不是只有第 2 题。两题的数学题干/数据未改；第 2 题条件与问法已于固定源 PDF 第 8 页复核，第 6 题图稿依据第 9 页拆分。其余五题的题面哈希、全部答案哈希及既有解题/盲核记录均未变化，角色草稿只更新两题的题面哈希与对应来源核验说明。
- 剩余任务：收取独立来源复核对第 2(9) 题条件及第 6 题原图标注/虚线的确认，再通过官方 `provenance.py import-batch --write` 事务刷新该卷记录与 manifest 状态；随后正式重建四版，复查新旧页面差异、六个图稿输出页与第 2 题说明页。批次页审、登记、清理、scoped gates、全量报告检查和提交均未完成。
- 下一步：先核验独立复核报告；若与主会话对固定源的逐页核对一致，运行 `import-batch` dry-run 与 `--write`，接着 `provenance check-batch`；通过后才正式四版构建并重建当前 attempt 的 review work items。

### `phase2-b58` 来源纠错：第 2(9) 题误读根因

- 已完成可验证调查阶段：独立盲核指出固定源 PDF 第 8 页第（9）小题条件应读为 `a3*a7=-12, a4+a6=-4`，不是规范源中旧有的 `a6+a9=-1`。主会话用 350dpi 原页裁图核实两个条件；同页第（6）题列出完全相同条件。固定源 PDF 第 11 页（书页 270）解答又明确列第（9）题答案 `180`。据此，所谓“题面与答案冲突/负判别式”是旧转录误读及其派生错误解析，不是原卷异文。
- 阶段修改文件：仅本 `PROGRESS.md`。证据图在 `/tmp/gk1986-source-review.CCCLIY/source-p08-q9-full-350dpi.png`、`answer-page-11.png`；正式题面、解析、issue ledger、provenance、build receipt/PDF 均尚未修改。provenance 的 dry-run 工作稿未导入。
- 阶段验证：独立盲核与主会话 350dpi 原扫描分别核对题面条件；来源答案页图像核对 `（9）180`。按 `a_5=(a_4+a_6)/2=-2`、`d>0`、`a_3a_7=4-4d^2=-12` 得 `d=2`、`a_1=-10`、`a_{20}=28`、`S_{20}=180`，与来源答案一致。
- 剩余任务：把试题转录更正为来源条件；删除基于误读的冲突说明并修正解析，复核答案要点；按官方 issue 工具解决由此失效的冲突/转录阻塞，并刷新 q02 当前 provenance 证据与哈希。之后才能单卷正式重建、重审受影响页面并继续 b58 收尾。
- 下一步：先检查 issue ledger 对应 0774–0776、0794–0796 的完整记录和受支持更新命令，确认可以精确结案哪些记录；随后最小更正 q2(9) 题面/解析、运行题源和解答一致性测试。此纠错 supersedes 上一条中关于固定源第 8 页条件及“冲突原因未知”的临时结论；页面布局图稿拆分仍待 provenance/构建/视觉验收。

### `phase2-b58` 来源纠错：题面、答案与解析同步

- 已完成可验证阶段：将第 2 大题第（9）小题条件更正为固定源上的 `a_3a_7=-12, a_4+a_6=-4`，移除错误的异文说明；答案要点改为 `180`；解析改为从 `a_5=-2`、`d=2` 推得 `a_1=-10`、`a_{20}=28`、`S_{20}=180`。解析合并稿和简答版按官方生成器重建。
- 阶段修改文件：规范试题 Markdown、答案要点 Markdown、解析正文 Markdown；官方生成的含解析 Markdown、`questions.tex`、`answers.tex`、`answers_short.tex`；回归测试 `tests/test_generate_projects.py`；本 `PROGRESS.md`。`source-manifest.json` 图稿事务和两份 TikZ 延续前一阶段，本阶段未改 issue ledger 或正式 provenance。
- 阶段验证：新增“（6）与（9）同条件、且解析不再含误读条件/无实解”的断言先以 `1 != 2` 失败，修正源稿后同一回归测试通过。`solution_sources.py check-batch`、`make_short_answers.py --check`、`generate_projects.py --check`、`source_manifest.py validate` 通过；`test_short_answers.py` 50 项、`test_solution_sources.py` 109 项通过。简答生成器在旧 `answers.tex` 下曾安全拒写；先按依赖顺序重生成 TeX 后再生成简答，最终检查一致。独立盲算者从固定源 p8 条件推得 180，并确认 PDF p11 答案表列 180。
- 剩余任务：六条误读派生的阻塞问题（ISSUE-0774/0775/0776/0794/0795/0796）仍在账本中，旧 provenance 仍标 q02 转录不确定、答案未知、冲突未解决；必须以保留历史记录的方式解决这些条目，并用三角色导入事务更新 q02/q06 当前哈希与 q02 证据。其他 q01 缺图问题保持原状态。
- 下一步：用 `issues.upsert_issue` 在暂存副本更新六条记录为 resolved 并附原扫描证据，通过 `build_projects.commit_state` 原子提交 issue ledger 与 manifest；随后重建三角色工作文件（仅刷新 q02 的题面/答案审查状态及 q06 题面哈希）、dry-run/import provenance，再检查 batch 状态仍准确保留 q01 阻塞。

### `phase2-b58` 问题账本与 provenance 纠正

- 已完成可验证阶段：按固定源 p8/p11 与独立盲算，将 ISSUE-0774/0775/0776/0794/0795/0796 标记 resolved，原编号保留并附明确结案证据；使用 `build_projects.commit_state` 原子提交 `missing-issues.md` 与 manifest，revision 3949，事务 `3674bff5-eeec-403c-99d4-e25521561d4d`。随后使用官方 `provenance.py import-batch --write` 导入三角色记录，revision 3950。q02 现为转录 passed、答案 grade A、conflict none；q06 题面哈希绑定当前矢量图稿。q01 的图形选项缺失及其两项阻塞记录原样保留。
- 阶段修改文件：`missing-issues.md`、1986 广东文史 `provenance.json`、`source-manifest.json`、本 `PROGRESS.md`；忽略工作文件 `.work/phase2-b58/{issues-reviewed.md,provenance/}`。规范源与生成 TeX 已在前一阶段登记。
- 阶段验证：provenance import dry-run 与写事务成功；`provenance.py check-batch`、`issues.py validate`、`source_manifest.py validate`、解析派生源检查、简答生成检查和项目生成检查均通过。按导入前的状态预演，结案 q02 六项后仅剩 q01 的 `ISSUE-0777` 与 `ISSUE-0793` 阻塞；没有擅自关闭缺图问题。
- 剩余任务：旧四版 PDF/build receipt 仍因题面、答案、图稿和生成源变化而失效，不能复用旧视觉回执；需要正式重建 4 版、刷新 review work items、逐页检查当前输出并登记。题面版 q01 图形选项缺失继续为待核阻塞；图稿拆分与 E 标注新位置还需输出页视觉验收。之后才可 finalize、清理本批中间产物、跑 scoped/full gates 并提交。
- 下一步：先检查 `build_projects.py build --help` 与当前 receipt 状态，再以正式批次构建重建四版，记录 attempt、页数、日志和 PDF 哈希；通过后按官方流程刷新工作项并复核所有受影响页面。

### `phase2-b58` 纠错后正式重建

- 已完成可验证阶段：1986 广东文史卷四版以正式构建重建成功。当前 attempt `3ca22859-8c6f-426d-b381-19c0df54bf19`，manifest revision 3952，四版页数仍为试题 7、解析 28、简答 8、印刷 22，共 65 页。四版均 `succeeded`，PDF SHA-256 与 receipt 一致；错误、缺字、Overfull、未解析引用均为 0。
- 阶段修改文件：项目 `receipts/build.json`、`source-manifest.json`、本 `PROGRESS.md`；四份 PDF 为 ignored 构建输出。旧 attempt `70e92843…` 的 review 工作项仍在 `.work`，尚未覆盖或刷新。
- 阶段验证：正式构建状态 `COMPILED_PENDING_REVIEW`（1 待审、0 失败）；`build_projects.py validate-receipts --batch phase2-b58` 与 `provenance.py check-batch` 均通过。独立读取 receipt 并现场 SHA-256 比较为四版全匹配，日志的 errors/missing_characters/overfull/undefined_references 全空。
- 剩余任务：为新 attempt 刷新四版 review work items；复核 65 页，重点覆盖试题第 2(9) 页、解析/简答中的纠错推导、题面原图与解析辅助图的全部引用页，以及 E 引线标注；完成真实逐页记录后再判断是否存在新的分页或遮叠问题。q01 缺图 issue 继续保持阻塞。
- 下一步：调用官方 `review_receipts.py prepare-batch` 绑定当前 attempt，检查新工作项的 attempt、PDF 哈希、连续页码与 pending 项数，再启动当前 PDF 的视觉复核。

### `phase2-b58` 当前 attempt 复核工作项准备

- 已完成可验证子阶段：官方 `review_receipts.py prepare-batch` 为新 attempt `3ca22859-8c6f-426d-b381-19c0df54bf19` 创建/刷新四版 review work items。旧 attempt 文件均只含 pending 项；它们已被当前 attempt 的空白工作项替换，未丢失任何已登记页审结论。
- 阶段修改文件：ignored `.work/phase2-b58/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-arts.json` 与本 `PROGRESS.md`；正式 review receipts 未改。
- 阶段验证：四份工作项 attempt 与 build receipt 一致；每份 PDF 路径及 SHA-256 与当前 receipt/实际文件匹配；页数 7/28/8/22，页码连续，共 65 页、520 个检查项，全部 pending。
- 剩余任务：完成当前 attempt 65 页逐页视觉审查并登记真实结果；重点审查 q02(9) 纠错后题面与答案、题面图/解析图及 E 引线的全部使用页；q01 缺图继续保留为唯一当前内容阻塞。
- 下一步：并行检查四版当前 PDF 全页，逐页核实覆盖；主会话单独放大所有变化页并接受独立审查报告，再写回 work items。

### `phase2-b58` 视觉抽核发现解析前言残留旧冲突说明

- 已完成可验证根因修复：当前 attempt 试题版 p1/p6/p7 和解析版 p26/p27 高分辨率抽核显示题面已正确去答案化、q02(9) 条件转录正确、题面图为 S/A/B/C 且 AC 虚线，D/E 解析图已拆分。但解析 PDF p8 仍出现“题面不存在实等差数列/保留冲突”旧前言。追踪 `rg` 定位根因为规范 `1986_数学真题_广东文_解析正文.md` 顶部的过期来源说明（此前只修了 q9 正文段落），不是缓存或生成器缺陷。新增针对过期说明的断言后测试按预期 RED；移除该前言错误并按官方流程重建含解析 Markdown 与 `answers.tex` 后转 GREEN。
- 阶段修改文件：解析正文 Markdown、`tests/test_generate_projects.py`、官方派生含解析 Markdown 与项目 `answers.tex`、本 `PROGRESS.md`。当前 PDF/receipt 仍是 attempt `3ca22859…` 的旧输出，review work items 仍绑定该 attempt；均不得当作新源版本的最终审查证据。
- 阶段验证：定向回归测试通过；`solution_sources.py check-batch`、`generate_projects.py --check`、`git diff --check` 通过；直接检索规范解析、合并稿和 `answers.tex`，旧冲突语句及 `a_6+a_9=-1` 均无残留。
- 剩余任务：因解析前言又有源树变化，attempt `3ca22859…` 与四份 pending review work items 现已 stale；须重新正式四版构建、重新绑定工作项后再开始 65 页复核。上一阶段对当前 PDF 的候选页/图稿观察仅作定位线索，不写入正式工作项。
- 下一步：运行四版正式 build 并验证新 attempt 的 receipt、哈希、页数与日志；随后官方刷新 work items，重新逐页复核受影响页面和其余页面。

### `phase2-b58` 解析前言修正后重建与复核项刷新

- 已完成可验证阶段：在移除解析正文前言中的旧冲突结论后，再次正式四版构建成功。新 attempt `55663131-2dad-4f38-874a-c6367110acd7`，manifest revision 3954；页数 7/28/8/22，共 65 页。解析版 p8 文本层现在只含来源页说明与解析开篇，不再含“不存在实等差数列/保留冲突”旧结论。随后官方 `prepare-batch` 将四份 review work items 绑定到此 attempt。
- 阶段修改文件：项目 `receipts/build.json`、`source-manifest.json`、本 `PROGRESS.md`；ignored 四版 PDF 与 `.work/phase2-b58/review/` 四份工作项。更正后的规范解析源和派生 TeX 记录在上一子阶段。
- 阶段验证：build receipt validator 与 provenance check 均通过；四版均 succeeded，实际 PDF SHA-256 与 receipt 相符，页数正确，errors/missing_characters/overfull/undefined_references 均为空。工作项逐项绑定新 attempt、PDF 哈希和页数；覆盖连续 65 页、520 检查项，全部 pending。
- 剩余任务：对当前 attempt 全部 65 页完成逐页视觉复核，重点检查 q02(9) 题面、简答/解析中的 180 推导、题面图与解析辅助图的全部出现页、E 标注位置及候选页；然后如实写入 work items。q01 图形选项缺失仍是保留的内容阻塞。
- 下一步：四版独立复核与主会话重点页放大并行；接受报告前核对当前 attempt/PDF 哈希，发现源稿或版式问题即停止写入并重建受影响版本。

### `phase2-b58` 中断恢复后定位第 2(6) 转录错误

- 已完成可验证调查阶段：恢复时先检查规范工作树 Git diff 与本进度文件；当前分支为 `feat/gaokao-phase0`、HEAD `ce373bc4`，此前进行中的改动均仍在工作区。续审 5566 attempt 时，试题版审查报告发现第 2(6) 与第 2(9) 条件重复。对照固定源 PDF 第 8 页（书页 267）350dpi 页面图像，源第（6）题为函数 `f(1+1/x)=1/x^2-1`；固定源 PDF 第 11 页（书页 270）答案列第（6）题 `x^2-2x`、第（9）题 `180`。规范试题 Markdown、答案要点、解析正文及派生 TeX 当前把第（9）题数列题和 `180` 错复用于第（6）题，根因是第（6）题转录错位，不是源卷重复题。
- 阶段修改文件：仅本 `PROGRESS.md`；主会话增加一份源 PDF 第 7 页临时高分辨率渲染于 `/tmp/gk1986-source-review.CCCLIY/source-p07-350dpi.png`，未改项目源文件、work item 或正式 review receipt。旧 attempt 的 3 份独立版次报告均只作诊断，不登记；收到内容错误证据后已中断仍在运行的印刷版旧 attempt 复核。
- 阶段验证：原始题面扫描与答案扫描分别直接查看；规范 Markdown 的（6）与（9）及当前生成 `answers.tex` 可复现错配；答案速查把（6）列 `180`，而固定源答案列 `x^2-2x`。旧 attempt `55663131-2dad-4f38-874a-c6367110acd7` 对应错误转录版本，不能作为最终审查或 finalize 依据；四份 work items 仍 pending，正式 review receipt 未写入。
- 剩余任务：先添加并观察 q02(6) 题面、答案和派生解析的回归测试 RED；随后更正规范题源、答案要点、解析正文及生成文件，刷新受影响的 q02 provenance，并重新构建四版。现有视觉报告覆盖的仅是已知错误的旧输出，必须在新 attempt 上重审全 65 页。q01(25) 源图形选项缺失仍保持 open blocker。
- 下一步：新增一个经真实项目生成器执行的 q02(6)/q02(9) 分离回归测试，断言（6）呈现函数题、其答案为 `x^2-2x`，而（9）仍为等差数列题且答案 `180`；先运行至预期失败，再作最小源稿修正。

### `phase2-b58` 第 2(6) 防回归测试 RED

- 已完成可验证子阶段：新增真实项目生成器回归测试，覆盖题面 q02(6) 与 q02(9) 的区分、q02(6) 解答表达式，以及生成答案中 q02(6)=`x^2-2x`、q02(9)=`180`。测试在修改规范源之前按预期失败，失败点是当前生成题面 q02(6) 仍为等差数列条件，证实能捕获本次错位。
- 阶段修改文件：仅 `tests/test_generate_projects.py` 与本 `PROGRESS.md`。源 Markdown、派生 TeX、provenance、receipt 和 work items 尚未修改。
- 阶段验证：`python3 -m unittest discover -s tests -p test_generate_projects.py -k 1986_guangdong_arts_fill_in_6_is_not_item_9` 返回 1 项预期失败，断言找不到固定源中的 `f(1+1/x)=1/x^2-1`；失败不是导入、语法或测试配置错误。
- 剩余任务：更正规范题面第 2(6)、对应答案要点与解析；同步更新此前错误的图稿回归测试中“第（6）与（9）源题条件相同”的断言。随后按依赖顺序生成 TeX/简答并验证测试 GREEN，再刷新 q02 provenance。
- 下一步：只对规范 Markdown 作最小修正：将第（6）题改回函数反求题，答案改为 `x^2-2x`，解析按 (t=1+1/x) 代换推导；（9）题及其答案 `180` 保持不变。之后重跑新测试与相关生成器检查。

### `phase2-b58` 第 2(6) 题源、答案与解析纠正

- 已完成可验证阶段：规范题源第 2(6) 更正为 `f(1+1/x)=1/x^2-1`；答案要点更正为 `x^2-2x`；解析改为令 (t=1+1/x)，推出 (f(t)=(t-1)^2-1=t^2-2t)，并说明题设代换直接确定 (t\ne1) 时的函数值。第 2(9) 题和答案 `180` 保持原样。更新图稿回归测试断言：数列条件只在第（9）题出现。
- 阶段修改文件：规范 `1986/1986_数学真题_广东文_试题.md`、`答案要点.md`、`解析正文.md`；`tests/test_generate_projects.py`；官方派生含解析 Markdown、`questions.tex`、`answers.tex`、`answers_short.tex`；本 `PROGRESS.md`。尚未更新 provenance、build receipt 或 work item。
- 阶段验证：新增生成器回归测试先 RED（第（6）题生成结果仍含数列条件），修正源后 GREEN；图稿/引用回归测试通过。`test_generate_projects.py` 104 项、`test_short_answers.py` 50 项、`test_solution_sources.py` 109 项均通过。`solution_sources.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check` 均通过；测试中的 CLI 用法错误文本来自预期负例，测试套件整体 exit 0。
- 剩余任务：现有三角色 provenance 仍绑定错误的 q02 题面与答案哈希/旧判断，需要按新源重新核对 q02 并以官方 importer 导入；正式 build receipt 仍对应错误转录，5566 四版 PDF 与 work items 不可用，必须在 provenance 通过后重建四版并重新完整复核 65 页。q01(25) 缺少源图形选项仍为 open blocker。
- 下一步：检查三份 `.work/phase2-b58/provenance/{question-review,answer-solve,answer-review}/` 的 q02 记录与官方 hash 计算方式；获得与新题面相符的来源核验/独立求解/盲核证据后，dry-run 再导入 q02 记录，检查 batch provenance 状态及 q01 blocker 保持不变。

### `phase2-b58` q02 provenance 纠正并事务导入

- 已完成可验证阶段：主会话按固定源 PDF 第 8 页（书页267）复核 q02(6)/(9) 转录；两位隔离盲核只看题面独立推导 q02(6)，均得 (f(x)=x^2-2x)（仅对 (x\ne1) 可由关系确定，(f(1)) 未定）。答案页第 11 页（书页270）第（6）列 (x^2-2x)、第（9）列 180，与独立推导相符。三角色 `.work` 仅修正 q02 证据/摘要；清理 q01/q03–q06 角色证据中的过时“第2(9)冲突”描述，q01 缺图不变。
- 阶段修改文件：三份 ignored `.work/phase2-b58/provenance/{question-review,answer-solve,answer-review}/gk-1986-regular-guangdong-arts.json`；官方导入的 `1986_广东卷_文史类/provenance.json`、`source-manifest.json` revision 3955；本 `PROGRESS.md`。题面、答案、解析和派生 TeX 在上一阶段已更正。
- 阶段验证：`provenance.py import-batch` dry-run 通过；`--write` 事务提交 revision 3955；`provenance.py check-batch`、issues 校验、source manifest validate、项目生成 `--check`、简答 `--check`、解析源 `check-batch` 与 `git diff --check` 均通过。固定源答案与两份独立盲算一致；q01 的 ISSUE-0777/0793 仍 open。
- 剩余任务：当前 build receipt / PDF / work items 均对应更正前的 attempt `55663131-2dad-4f38-874a-c6367110acd7`，全部作废；需正式四版重建、核对编译日志与哈希、刷新 work items，再对新 attempt 的 65 页完成全页复核和登记。尚未 finalize、清理本批临时渲染、运行全量报告检查或提交。
- 下一步：检查正式构建命令与当前 receipt，再运行 `phase2-b58` 单卷四版 build；记录新 attempt、revision、页数、PDF 哈希和编译警告后，刷新 review work items。

### `phase2-b58` q02 纠正后四版正式重建

- 已完成可验证阶段：正式构建新 attempt `7b8a4633-49c8-441b-999a-fe1ba67ac98e`，manifest revision 3957，四版均 succeeded；页数为试题 7、解析 27、简答 8、印刷 22，共 64 页（解析版较旧 attempt 少 1 页）。
- 阶段修改文件：1986 广东文史项目 `receipts/build.json`、`source-manifest.json`、本 `PROGRESS.md`；四份 PDF 为 ignored build 输出。旧 attempt `55663131-2dad-4f38-874a-c6367110acd7` 不再作为依据。
- 阶段验证：`build_projects.py validate-receipts --batch phase2-b58` 与 provenance `check-batch` 通过；四份实际 PDF SHA-256 均与 receipt 相符；四版 log 的 errors、missing_characters、overfull、undefined_references 全为空。
- 剩余任务：新 attempt 的 review work items 尚未刷新；需要将四版 64 页、512 个检查项绑定新 attempt/哈希并确认全部 pending，然后完成全页视觉复核。q01(25) 源图形选项缺失继续保持 open blocker。
- 下一步：运行官方 `review_receipts.py prepare-batch` 刷新四份 work items，逐项核对 attempt、实际 PDF 哈希和页码连续性，再开始审查。

### `phase2-b58` 新 attempt 复核工作项准备

- 已完成可验证阶段：官方 `review_receipts.py prepare-batch` 为 attempt `7b8a4633-49c8-441b-999a-fe1ba67ac98e` 刷新四版 work items；旧 attempt 工作项此前全为 pending，没有已登记页审结论需要迁移。
- 阶段修改文件：ignored `.work/phase2-b58/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-arts.json`；本 `PROGRESS.md`。正式 review receipt 未写入。
- 阶段验证：四份工作项均与新 build attempt、项目 PDF 路径/receipt SHA/实际 SHA 匹配；页码连续覆盖 7/27/8/22 页，共 64 页和 512 检查项，全部 pending；每版候选页为 p1。
- 剩余任务：对当前 attempt 的 64 页逐页视觉审查并登记；特别重看试题/解析/简答/印刷中 q02(6) 函数题及答案、q02(9) 数列题，以及解析和印刷中拆分后的三棱锥辅助图。尚未 finalize、清理临时渲染、跑全量报告检查或提交。
- 下一步：隔离分派四版只读复核，主会话同时检查当前 attempt 的变化页和候选页；只依据这次 attempt 的 PDF 哈希和图像，全部页完成且问题如实处理后再写 work items。

### `phase2-b58` 主审发现解析辅助图构造点位置错误

- 已完成可验证调查阶段：对当前正式 attempt `7b8a4633-49c8-441b-999a-fe1ba67ac98e` 的解析版第 26 页进行高分辨率检查。正文定义 D 为 AC 中点、E 为从 S 向 BC 作垂线的垂足，但登记图稿坐标为 A=(0,0)、B=(3.6,0)、C=(1.25,1.35)、D=(1.8,0.68)、E=(2.4,0.5)：D 不在 AC 上且不是其中点，E 也不在 BC 上。PDF 图像与源坐标一致，属于辅助图几何关系错误，不是标签遮叠或截图观感问题。
- 阶段修改文件：仅本 `PROGRESS.md`。未改图稿、生成源、build receipt、review work items 或正式 review receipt；当前 64 页审查仍不可登记。
- 阶段验证：主会话已查看当前 attempt 的试题版 p6/p7、解析版 p8/p20/p21/p25/p26/p27、简答版 p7/p8；当前 PDF 图像确认 p26 的 D/E 坐标错误，TikZ 源文件给出一致的数值坐标。解析版其它已抽页未见裁切、遮叠或答案泄漏；这些抽页结论不替代全页复核。
- 剩余任务：先增加几何回归断言并观察预期失败，再把解析辅助图 D 放到 AC 中点、E 放到 BC 线上；重生成并检查相关页面，随后四版重新正式构建、刷新 work items，并从新 attempt 开始完成全 64 页审查。q01(25) 图形选项缺失仍为已登记的内容阻塞。
- 下一步：扩展 `test_1986_guangdong_arts_question_figure_is_source_faithful`，从解析 TikZ 中读取 A/B/C/D/E 坐标并机械验证 D 是 AC 中点、E 在 BC 线段上；先运行到预期 RED，再修图稿并按官方生成/构建流程重建。

### `phase2-b58` 解析辅助图几何断言 RED

- 已完成可验证子阶段：将图稿回归测试扩展为解析 A/B/C/D/E 的 TikZ 数值坐标，并断言 D 等于 AC 中点、E 落在线段 BC 上。测试在修复图稿之前按预期失败，首个失败为 D 的 x 坐标 `1.8 != 0.625`，与视觉检查发现相符。
- 阶段修改文件：`tests/test_generate_projects.py`；本 `PROGRESS.md`。图稿与 build/work-item 文件未改。
- 阶段验证：`python3 -m unittest discover -s tests -p test_generate_projects.py -k 1986_guangdong_arts_question_figure_is_source_faithful` 运行 1 项并以预期 AssertionError 失败；测试正常执行到几何断言，无导入或语法错误。
- 剩余任务：修正解析辅助图的 D/E 坐标，使 D 真为 AC 中点、E 真在线段 BC 上；同一测试应转绿，再渲染确认标签及线段清楚。当前正式 PDF/64 页 work items 仍绑定旧图稿 attempt，后续须重建四版并从新 attempt 重审。
- 下一步：只改 `f1986_guangdong_arts_t6_solution.tex` 的 D/E 坐标，运行上述定向测试至 GREEN，并编译单卷确认 PDF 图形位置；随后再按正式流程四版重建及刷新审查工作项。

### `phase2-b58` 解析辅助图几何修复与预览验证

- 已完成可验证阶段：将解析辅助图 D 移至 AC 中点 `(0.625,0.675)`，E 移至 BC 中点 `(2.425,0.675)`；题面源图、题目文字、答案和结论未改。扩展后的几何回归断言从预期 RED 转为 GREEN。
- 阶段修改文件：`1986_广东卷_文史类/figures/f1986_guangdong_arts_t6_solution.tex`、`tests/test_generate_projects.py`、本 `PROGRESS.md`。旧 attempt 的 build receipt、正式 review receipt 与 work items 尚未改。
- 阶段验证：定向 `test_1986_guangdong_arts_question_figure_is_source_faithful` 通过；`generate_projects.py --batch phase2-b58 --check` 通过。使用仓库相同 latexmk/XeLaTeX 参数，将解析版预览输出隔离到 `/tmp/phase2-b58-figure-preview.KPOYKu/`；27 页编译成功，350dpi 检查第 26 页，D 落在 AC、E 落在 BC，D/E 标签及 SD、SE、DE 线条可辨且无碰撞。正式 PDF 与 receipt 未被预览构建覆盖。
- 剩余任务：图稿变更使 attempt `7b8a4633-49c8-441b-999a-fe1ba67ac98e` 的 build 回执和四版 64 页 work items 失效；旧 attempt 的四个独立审查进程已停止，不会将旧 PDF 结果登记。需正式重建四版、核验新哈希和日志、刷新 work items，再从新 attempt 完成全部 64 页审查。q01(25) 缺少源图形选项仍为 open blocker。
- 下一步：按官方流程运行 `phase2-b58` 四版正式构建，记录新 attempt、页数、PDF 哈希及编译日志；验证成功后通过 `review_receipts.py prepare-batch` 绑定新工作项，再启动全页复核。

### `phase2-b58` 几何修复后四版正式重建

- 已完成可验证阶段：官方四版正式构建生成新 attempt `35994390-fc54-4784-b6ae-b98628958908`，manifest revision 3958；四版均 succeeded，页数 7/27/8/22，共 64 页。新 build input tree 已包含修正后的解析辅助图。
- 阶段修改文件：`1986_广东卷_文史类/receipts/build.json`、`source-manifest.json`、本 `PROGRESS.md`；四版 PDF 与 `.log/.aux/.fls/.xdv` 为 ignored 构建输出。旧 attempt `7b8a4633…` 不再作为最终审查依据。
- 阶段验证：官方 `build_projects.py validate-receipts --manifest source-manifest.json --batch phase2-b58` 与 `provenance.py check-batch --manifest source-manifest.json --batch phase2-b58` 均通过；source manifest validate 通过。现场 SHA-256 与 receipt 一致：试题版 `d14b1181…`、解析版 `38b42c76…`、简答版 `12d0ca03…`、印刷版 `1bd45c04…`；各版问题列表为空。解析版预览的第 26 页已按前一阶段完成 350dpi 视觉确认。
- 剩余任务：尚未为新 attempt 刷新正式 review work items，也未做当前版本 64 页完整复核；新图中 D/E 几何关系已确认，但须复核含该图的正式新 PDF。q01(25) 源选项图缺失继续是已知内容阻塞。尚未 finalize、清理临时中间产物、执行最终 gates 或提交。
- 下一步：调用 `review_receipts.py prepare-batch` 绑定新 attempt，逐项确认 PDF 路径、receipt/实际哈希、页码覆盖及 pending 数，再从这 64 页新 PDF 开始四版全页复核。

### `phase2-b58` 新 attempt 复核工作项刷新

- 已完成可验证子阶段：官方 `review_receipts.py prepare-batch` 将四份复核工作项重新绑定至 attempt `35994390-fc54-4784-b6ae-b98628958908`。
- 阶段修改文件：ignored `.work/phase2-b58/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-arts.json` 与本 `PROGRESS.md`；正式页级 review receipts 尚未写入。
- 阶段验证：四份工作项的 attempt、PDF 路径、页数和 SHA-256 均匹配当前 build receipt；本地实际 PDF SHA 与 receipt 相符。连续覆盖试题/解析/简答/印刷版 7/27/8/22 页，共 64 页、512 检查项，全部 pending。
- 剩余任务：对当前 attempt 全部 64 页进行逐页视觉复核并记录八类检查；不能复用旧 attempt 的复核结果。q01(25) 缺少固定源图形选项仍为已知内容 blocker，须在复核中保留并如实表述；页审后还需 finalize、清理临时中间产物、最终 gates 与提交。
- 下一步：重新启动四个隔离的只读版次复核，各自覆盖一个当前 PDF 的全部页面；主会话复核关键变化页及候选页。登记前再次核对所有报告所指的 attempt 和 PDF SHA。

### `phase2-b58` 新 attempt 主会话重点页抽核

- 已完成可验证子阶段：主会话直接渲染并检查当前正式 PDF 的候选首页及关键变化页：试题版 p1/p6/p7，解析版 p1/p8/p26，简答版 p1/p8，印刷版 p1/p21/p22。第 6 题题面图、解析辅助图及相邻分页均可辨；p26 的 D 位于 AC 中点、E 位于 BC，标签未遮叠；q02(6) 与 q02(9) 区分清楚，试题版未泄露具体答案；q02(2) 的来源方框缺字及 q01(25) 缺图说明均保持显式标注。
- 阶段修改文件：仅本 `PROGRESS.md`。当前 PDF 与 review work items 未改。
- 阶段验证：上述图像均由 attempt `35994390-fc54-4784-b6ae-b98628958908` 的 PDF 直接以 300/350dpi 渲染；复核项 PDF 哈希与正式 receipt 一致。抽核页未发现新视觉失败。此项是重点页复核，不替代独立审查者对全部 64 页的逐页覆盖。
- 剩余任务：四名独立只读审查者分别检查当前四版全部 64 页并返回逐页覆盖及例外；之后主会话核验报告与 SHA，并将真实检查结果写入工作项。q01(25) 缺图仍为内容 blocker，尚未 finalize、清理中间文件、执行最后 gates 或提交。
- 下一步：接收并核查四份独立报告；若任一报告指向版式/内容问题，先处理并重新构建受影响版本，不能先登记通过。若全页通过，则按 64 页逐项登记八类检查，再运行 review receipts 验证及批次 finalize。

### `phase2-b58` 独立逐页复核完成一半

- 已完成可验证子阶段：试题版 7 页和简答版 8 页分别由隔离复核者逐页检查完毕；每版均覆盖八类检查，所报 attempt `35994390-fc54-4784-b6ae-b98628958908`、PDF SHA 与页数匹配当前 receipt。两份报告均未发现版式失败，且只把第 1(25) 选项图缺失、第 2(2) 源乘号缺字方框作为已登记的 source limitations。
- 阶段修改文件：仅本 `PROGRESS.md`。两份对应 ignored work items 仍保持 pending，尚未把复核报告折入检查项，也未写正式 review receipt。
- 阶段验证：复核者分别报告试题版 SHA `d14b1181…`、7 页及简答版 SHA `12d0ca03…`、8 页；主会话已直接核对 receipt/实际 SHA，且查看当前试题版 p1/p6/p7、简答版 p1/p8。全页范围为连续页码 1..7 与 1..8，八类检查均全覆盖。
- 剩余任务：解析版 27 页、印刷版 22 页仍在隔离复核中；收齐后需再次核对报告 attempt/SHA，再更新四份 work items 并用 `review_receipts.py` 验证/最终登记。q01(25) 图形缺源仍保持 open blocker。
- 下一步：继续对解析版和印刷版当前 PDF 完成全页审查；收到报告后只登记有当前 PDF 证据的逐页结果，必要时保留来源限制的详细 note。

### `phase2-b58` 当前 attempt 全版次复核揭示分页缺陷

- 已完成可验证阶段：当前 attempt `35994390-fc54-4784-b6ae-b98628958908` 的四版独立逐页复核均已完成，覆盖试题版 7 页、解析版 27 页、简答版 8 页、印刷版 22 页，共 64 页。试题版与简答版通过；解析版发现 p14 仅留下第（12）小题标题、正文移至 p15；印刷版发现 p2/p3 把第（15）题条件句拆开（p3 页首孤立“且”）、p16 页末孤立“解析”标题、p17 页末孤立第（7）小题标题而正文到 p18。
- 阶段修改文件：仅本 `PROGRESS.md`。正式页级 review receipt 与四个 work item 暂未登记通过或失败；当前构建和工作项仍绑定 attempt `35994390…`。
- 阶段验证：独立报告的 attempt、PDF SHA 与当前 build receipt 一致；主会话直接检查印刷版 p3、p16–p18 和解析版 p14–p15 的当前 PDF 高分辨率页面，确认上述缺陷真实存在；印刷版 p2 的断句亦由当前页图与 p3 对照确认。另 60 页报告无新增分页异常，已知来源限制仍为 q01(25) 缺选项图与 q02(2) 乘号缺字方框。
- 剩余任务：定位并用回归测试覆盖四处纯分页问题，最小化修正规范源稿/本卷分页；随后重新生成并正式四版构建。新 attempt 将使全部 64 页需重新复核。未解决的来源限制继续保留，不能由排版修复代替内容核验。
- 下一步：检查本卷源稿到 TeX 的转换路径、现有换页控制宏及可用源级分页指令；先补能复现目标分页约束的回归测试并观察预期失败，再实施局部版式修复。

### `phase2-b58` 四处分页约束回归测试 RED

- 已完成可验证阶段：新增本卷生成级回归测试，检查第（15）题题面、第（12）小问、第 2 题“解析”标题、第（7）小问前均有 `\Needspace{12\baselineskip}` 源级预留。检查对象是 `generate_project()` 返回的实际 `questions.tex` / `answers.tex` 内容，不是只检查源 Markdown 字符串。
- 阶段修改文件：`tests/test_generate_projects.py`、本 `PROGRESS.md`；规范源稿、派生 TeX、build receipt 与 review work items 未改。
- 阶段验证：执行 `python3 -m unittest discover -s tests -p test_generate_projects.py -k 1986_guangdong_arts_reviewed_page_blocks_reserve_space`，测试运行 1 项、四个子检查均按预期失败；失败点分别确认四处源级预留缺失。测试已使用局部上下文断言，避免在失败时输出整份生成 TeX。
- 剩余任务：在规范源稿四处加入纯分页指令；通过生成器刷新派生文件，目标回归测试转绿后进行单卷预览编译与页图核验。题目、答案与解析数学内容不得变更。
- 下一步：只改 1986 广东文史试题 Markdown 的第（15）题前和解析正文中对应标题/小问前的 `\Needspace`，按生成器 `--write` 重建规范派生物，再跑定向测试及 `--check`。

### `phase2-b58` 四处源级分页修复与派生物刷新

- 已完成可验证阶段：在本卷试题第（15）题、解析正文第（12）小问、第 2 题 `**解析**` 标题及第（7）小问前加入 `\Needspace{12\baselineskip}`，未改题干、答案或数学推导。通过官方事务流程刷新含解析派生稿及 `questions.tex`、`answers.tex` / index 投影。
- 阶段修改文件：规范 `1986_数学真题_广东文_试题.md`、`1986_数学真题_广东文_解析正文.md`；派生 `1986_数学真题_广东文_含解析.md`、项目 `questions.tex`、`answers.tex` / `index.json`；`tests/test_generate_projects.py` 与本 `PROGRESS.md`。正式 PDF、build receipt、review receipt 和 review work items 未覆盖。
- 阶段验证：新分页生成级回归测试通过；`python3 -m unittest discover -s tests -p test_generate_projects.py` 通过 105 项；`generate_projects.py --batch phase2-b58 --check`、`solution_sources.py check-batch`、`source_manifest.py validate --manifest source-manifest.json` 及 `git diff --check` 均通过。逐段检查生成 TeX，四处预留均处于目标标题之前。
- 剩余任务：源/TeX 已更新，正式 attempt `35994390…` 与其 64 页 work items 均已过期；尚未确认 PDF 中的真实分页效果。之后须重新正式四版构建并从新 attempt 重新复核全部 64 页。
- 下一步：在临时隔离目录用仓库相同 XeLaTeX/latexmk 配置预览解析版与印刷版，检查印刷版原 p2/p3、p16/p17/p18 对应处及解析版原 p14/p15 对应处；修复未达标时继续限定在源稿分页指令内。

### `phase2-b58` 隔离预览确认分页修复

- 已完成可验证阶段：在隔离目录 `/tmp/phase2-b58-layout-preview.4lhmTG/` 用与正式构建相同的 latexmk/XeLaTeX 参数编译解析版和印刷版。印刷版仍为 22 页、解析版 27 页；原印刷 p2/p3 的第（15）题现完整从 p3 开始，p16 不再孤立“解析”，p17 解析标题与第（1）至（6）题同页，p18 第（7）题标题与正文同页；解析版 p14 结束于第（11）题，p15 第（12）题标题与推导同页。
- 阶段修改文件：仓库无新改动；临时预览 PDF、日志及 350dpi 页面图均位于上述 `/tmp` 目录。规范源、生成 TeX、正式 PDF/receipt 与 work items 未被预览构建覆盖。
- 阶段验证：两版 latexmk 均退出 0；`pdfinfo` 页数为 27/22；逐页目视检查印刷版 p2、p3、p16–p18 与解析版 p14–p15（350dpi）确认分页达到预期，题目/结论未改变。两份日志检索不到 Overfull、Missing character、LaTeX Warning 或错误记录；`git diff --check` 通过。
- 剩余任务：正式 attempt `35994390…` 仍绑定旧输入且不可作为修复版凭证；尚未正式重建四版，也未刷新新 attempt 的 64 页工作项或重新全页复核。q01(25) 缺选项图与 q02(2) 源乘号缺字方框仍为登记中的来源限制。
- 下一步：正式四版重建 `phase2-b58`；核对新 attempt、四版页数、PDF SHA/receipt 与编译日志，再用官方 `prepare-batch` 刷新 64 页工作项。之后全部页面从新 PDF 重新复核，不能挪用本次预览或旧 attempt 的页级结论。

### `phase2-b58` 正式重建前 provenance 门禁发现 q1 哈希变化

- 已完成可验证诊断阶段：四处布局指令中，只有放入试题 Markdown 的 q1 第（15）题前标记改变了 provenance 所记录的 q1 题面哈希；数学内容和题干未变。批次状态从旧回执的 `compiled_pending_review` 显示为现场 `planned`，是源文件变更使旧 attempt 失效的预期状态，不属于额外题目事实错误。
- 阶段修改文件：仅本 `PROGRESS.md`；provenance、正式构建回执及复核工作项未改。
- 阶段验证：`provenance.py check-batch --manifest source-manifest.json --batch phase2-b58` 如实失败，报告 q1 题面哈希变化及旧构建状态与现场派生状态不一致；其余卷项未报来源核验问题。
- 剩余任务：按已授权的版式变更边界，通过仓库支持的事务方式刷新 q1 受影响哈希，不重跑或改写题目事实；随后 provenance 与各源门禁通过后正式四版重建。批次状态差异需由新正式构建解决。
- 下一步：检查 `provenance.py` 支持的 q1 事务更新接口和当前 provenance 记录，确认只更新受影响的 q1 题面哈希，再重跑 `check-batch`。

### `phase2-b58` q1 版式哈希经事务刷新

- 已完成可验证阶段：去除题面唯一新增的分页标记后重算 q1 digest，与旧哈希完全一致；仅更新 ignored `question-review` 工作项的 q1 `question_text_sha256` 声明，原三角色证据文本、身份、审查结果、来源页和答案哈希均保留。官方 `provenance.py import-batch --write` 事务成功，manifest revision 更新为 3960，现场批次状态回到 `planned`。
- 阶段修改文件：ignored `.work/phase2-b58/provenance/question-review/gk-1986-regular-guangdong-arts.json`；正式 `1986_广东卷_文史类/provenance.json` 与 `source-manifest.json` revision；本 `PROGRESS.md`。题目事实、答案与问题总账内容未改。
- 阶段验证：`import-batch` dry-run 校验通过后才写事务；`provenance.py check-batch`、`source_manifest.py validate`、`issues.py validate`、`generate_projects.py --check` 和 `solution_sources.py check-batch` 均通过。
- 剩余任务：旧 build receipt / PDF 与 64 页 work items 仍绑定 attempt `35994390…`，不可用于修复版。尚未四版正式重建、刷新 review work items、重审、finalize、清理仓库中间产物或提交。
- 下一步：运行 `phase2-b58` 四版正式构建，随后核对 attempt、输入 revision、各 PDF 页数/hash、日志 findings 与 receipt；通过后刷新工作项并重新审查完整 64 页。

### `phase2-b58` 修复后四版正式构建

- 已完成可验证阶段：正式四版构建生成 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069`。试题/解析/简答/印刷版页数依次为 7/27/8/22，共 64 页；build receipt 绑定输入 manifest revision 3961，构建状态为 `compiled_pending_review`。
- 阶段修改文件：1986 广东文史 `receipts/build.json`、`source-manifest.json` 状态 revision、本 `PROGRESS.md`；四版 PDF 与 `.log/.aux/.fls/.xdv` 为 ignored 构建输出。旧 attempt `35994390…` 不再作为新版本证据。
- 阶段验证：`build_projects.py validate-receipts --require-current-inputs`、`provenance.py check-batch`、`source_manifest.py validate`、`git diff --check` 均通过。现场 SHA 与 receipt 完全一致：试题版 `73921e89…`、解析版 `eb9a827c…`、简答版 `54895780…`、印刷版 `7dae1e00…`；四版 errors、missing_characters、overfull、undefined_references 和 problems 全空。
- 剩余任务：官方 review work items 仍绑定旧 attempt；新正式 PDF 尚未完成 64 页全页复核。已知 q01(25) 缺选项图、q02(2) 源乘号方框继续作为来源限制保留。尚未 finalize、清理仓库编译中间产物或提交。
- 下一步：官方 `review_receipts.py prepare-batch` 将四份工作项绑定到 attempt `53d535ef…`，核实实际 PDF 路径、哈希、连续页码与 512 个检查项全部 pending，再开始全页复核。

### `phase2-b58` 修复后 attempt 复核工作项刷新

- 已完成可验证阶段：官方 `review_receipts.py prepare-batch` 将四份版次 work item 绑定至 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069`。
- 阶段修改文件：ignored `.work/phase2-b58/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-arts.json` 与本 `PROGRESS.md`；正式 review receipt 未写入。
- 阶段验证：逐项比对 work item 与 build receipt 及实际 PDF：attempt、PDF 路径、SHA、页数全匹配；连续覆盖 7/27/8/22 页，共 64 页、512 项（每页八类检查），全部 pending。
- 剩余任务：修复版 PDF 尚未完成全页视觉审查或写入正式页级回执；q01(25) 缺选项图与 q02(2) 缺字方框仍需作为已知来源限制准确记录。
- 下一步：对当前 attempt 的四版 PDF 重新完成 64 页全页复核；重点复核本次分页修复页及 q02 图稿页，同时主会话抽查关键页面。完成报告后先核实 attempt/SHA，再写入 work items。

### `phase2-b58` 试题版与简答版当前 attempt 全页视觉复核

- 已完成可验证子阶段：直接从 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069` 的正式 PDF 渲染并检查试题版 7 页、简答版 8 页，共 15 页；逐页覆盖 glyph、heading_number、option_formula_alignment、figure_label、header_footer、pagination_whitespace、font_size、answer_leak 八类检查。未发现新增答案泄漏、裁切、公式/选项错位、图标不清或页眉页码问题。q01(25) 来源选项图缺失与 q02(2) 来源乘号方框均保留显式说明，不作为新排版失败。
- 阶段修改文件：仅本 `PROGRESS.md`；实际复核图片生成在 `/tmp/pdfs/phase2-b58-review.PEltpf/`，尚待全部复核完成后清理。
- 阶段验证：复核前核对当前 PDF 页数与 SHA：试题版 7 页 `73921e8929be2e65a171e63dc8d943c0505d65abd8c9896790c27d8bdf247cfd`，简答版 8 页 `5489578029a873e3fe1b54cdd9dd8a866bb2621d34cc8c7626bf5cad17e30361`；全部页面以 150dpi 渲染并逐页检查。试题版第 3 页第 1(15) 题的“且”在页内单独成行，未再跨页；该行观感将与独立复核报告交叉确认，暂不登记为失败。
- 剩余任务：解析版 27 页、印刷版 22 页须由独立审查者对当前 attempt 全页核验；主会话收到报告后检查 attempt/SHA 与逐页覆盖。全部 64 页确认后再写入 512 项工作项并执行官方复核/登记门禁；之后清理构建中间文件、运行最终验证并提交。尚未推送。
- 下一步：取得解析版和印刷版当前 attempt 的独立逐页报告；若报告确认分页修复有效且没有新的严重问题，则审定试题版第 3 页“且”单行的版面性质，再登记逐页检查结果。

### `phase2-b58` 当前 attempt 关键修复页高分辨率复核

- 已完成可验证子阶段：主会话从当前正式 PDF 以 300dpi 检查印刷版 p2–3、p16–18，解析版 p14–15 及解析版 p26 辅助图。旧分页异常均已消失：印刷版 p3 的题 1(15) 完整同页，p16 无孤置“解析”，p17 的解析标题及(1)–(6) 正文在同页，p18 的(7)标题与正文同页；解析版 p14 结束于(11)，p15 的(12)标题与解答同页。p26 的 D/E 构造点和图中文字清楚，未见遮叠或裁切。
- 阶段修改文件：仅本 `PROGRESS.md`；300dpi 栅格图仍在 `/tmp/pdfs/phase2-b58-review.PEltpf/`。
- 阶段验证：四个正式 PDF SHA 与 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069` 的记录一致；目视核对上述 8 页渲染图。印刷版 p3 的连接词“且”仍为页内独立一行，但题干已完整落在同一页；等待独立复核报告对其作为行内断句或分页失败的分类。解析版 p26 中 D 位于 AC 中点、E 位于 BC 上，辅助图与推导关系一致。
- 剩余任务：解析版及印刷版独立复核仍在进行，尚未全部确认 64 页、尚未写入 512 个检查结果或正式视觉回执。后续还需完成 finalization、精确清理构建中间文件、全部最终门禁和提交。
- 下一步：收到独立报告后对照当前 attempt/SHA、核实连续页码与八类覆盖；对印刷版 p3“且”单独成行作出一致判定后，才登记页级工作项。

### `phase2-b58` 印刷版当前 attempt 独立全页复核

- 已完成可验证阶段：独立审查者对 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069` 的印刷版连续复核 p1–p22，22/22 页覆盖八类检查；未发现新分页、标注、字号、页眉页脚、公式选项或答案泄漏问题。之前识别的 p2/p3、p16–p18 分页问题已由当前 attempt 修复。p3 的“且”属于同页题干中的短连接行，不是跨页孤行，独立报告判为通过。
- 阶段修改文件：仅本 `PROGRESS.md`；独立审查者未修改 work items 或正式回执，临时渲染图留在 `/tmp` 并待统一清理。
- 阶段验证：审查者现场确认 SHA `7dae1e0020c8b9c995955a409748d60e9992a9103256e367343efb7574f4d09a`、22 页和当前 attempt 与 build receipt/预期一致；以 180dpi 全页渲染逐页检查，另有主会话 300dpi 复核修复关键页 p2–3、p16–18。八类每项均 22/22 通过。q01(25) 来源图形选项缺失及 q02(2) 来源乘号方框为已登记限制，未猜补内容，未计为版面失败。
- 剩余任务：解析版 27 页仍待独立复核完成；之后合并核对四版 64 页覆盖、attempt/SHA 与已知限制，再填写 512 个页级检查并运行复核回执门禁。
- 下一步：收取解析版当前 attempt 的全页报告；确认报告页数、SHA 和每页八类检查后，再进入 work item 登记阶段。

### `phase2-b58` 四版全页复核揭示两处余留行级版式问题

- 已完成可验证诊断阶段：当前正式 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069` 的四版全页复核已覆盖试题/解析/简答/印刷版 7/27/8/22 页，共 64 页。旧的四处分页缺陷均已修复；复核者另发现：试题版与简答版 p3 的题 1(15) 连接词“且”单独占行，形成明显行级孤置；解析版 p16 页首“有”单字承接 p15 题 1(16) 的句子，形成跨页孤字。两处均为版式问题，不涉及题目事实或答案。印刷版审查及另一份解析版说明将“且”判为通过，主会话图像亦确认它在页内单独成行；该点需统一按版式标准处理。
- 阶段修改文件：仅本 `PROGRESS.md`；所有四份 ignored review work items 仍保持 pending，正式 review receipt 未写入。
- 阶段验证：四份报告的 attempt、PDF SHA 与页数均匹配当前 build receipt，页码连续无漏页；试题版主审 7 页、简答版独立审查 8 页、解析版独立审查 27 页、印刷版独立审查 22 页均逐页检查八类项目。关键修复页另经主会话 300dpi 复看。q01(25) 来源选项图缺失、q02(2) 来源乘号方框仍是既有来源限制，所有报告均未建议猜补。
- 剩余任务：先定位“且”与“有”两处的规范 Markdown 到生成 TeX 排版来源；依据最小生成级回归测试修正行级断裂及跨页孤字，再重生成、正式重建四版并对新 attempt 的 64 页全部重审。当前 attempt 的 512 个复核项不得登记通过。
- 下一步：检查题 1(15) 与题 1(16) 的源稿、转换后 TeX 和现有分页指令；先补覆盖两类可观察排版结果的回归测试并看到预期失败，再作局部纯版式修正。

### `phase2-b58` 两处余留版式问题根因确认

- 已完成可验证诊断阶段：题 1(15) 的规范题面 Markdown 把“且”作为独立段落放在两组展示公式之间，生成器原样输出独立正文行，因此所有包含该题的版次都会出现页内孤立连接词；题 1(16) 解析稿把“利用半角公式”及第一组恒等式与后续“有”及第二组推导分成独立段落，但该小问前没有空间预留，故第二组前的单字“有”可被分页到下一页页首。根因在源稿结构/局部分页约束，不是 PDF 渲染或字体问题。
- 阶段修改文件：仅本 `PROGRESS.md`；源稿、派生 TeX、构建回执及 review work items 未改。
- 阶段验证：对照规范 Markdown 行 162–176 与生成 `questions.tex` 的对应输出，确认独立“且”段落被保留；对照 `解析正文.md` q1(16) 行 205–222 与生成 `answers.tex`，确认“有”位于两个展示公式块之间且无 `\Needspace` 局部预留。重现页面分别为当前试题版/简答版 p3、解析版 p16。
- 剩余任务：为生成结果添加回归断言：题 1(15) 的连接词并入第二组公式而不再是独立段落，题 1(16) 小问前有足够的分页预留；先确认新增断言对当前源稿按预期失败，再只调整版式源标记并重新验证。
- 下一步：检查现有 `1986_guangdong_arts` 生成级测试的组织方式，新增两项最小 RED 断言并运行定向测试。

### `phase2-b58` 印刷版独立复核补充发现辅助图标签干扰

- 已完成可验证诊断阶段：另一名独立审查者复核当前印刷版全部 22 页，在 p3 与解析 p8 再次指出 q1(15) 的“且”各自独占一行；并发现印刷版 p21 q6 解析辅助图中的 `C` 标签与虚线相交/紧贴，辨识受干扰。来源已知限制仍仅为 q01(25) 缺来源选项图与 q02(2) 乘号缺字方框。当前实际正式 PDF 直接渲染 p21（300dpi）已确认 `C` 标签问题可见。
- 阶段修改文件：本 `PROGRESS.md`；生成级回归测试 `tests/test_generate_projects.py` 已开始添加 q1(15) 和解析 q1(16) 的两项断言，但尚未运行验证；源稿与图稿未改，work items 仍 pending。
- 阶段验证：复核者确认印刷版 SHA `7dae1e0020c8b9c995955a409748d60e9992a9103256e367343efb7574f4d09a`、22 页、attempt `53d535ef-8274-4f4d-b200-a7cfbe106069` 与当前 receipt 一致；150dpi 全页及关键页 300dpi 复核。主会话也在当前 PDF 高分辨率 p21 确认标注相交/贴线。四版 64 页已全覆盖，但这三类余留缺陷使 512 项不得登记通过。
- 剩余任务：完成 q1(15) 及 q1(16) 生成级回归测试的 RED/GREEN；为辅助图 C 标签添加针对标签与线段间距的回归保护后仅移动标签、不改几何坐标。之后生成新四版正式 attempt，并重审全部 64 页，检查修复不引入新问题。
- 下一步：先运行新增生成级测试，确认 q1(15) 连接词结构及 q1(16) 空间预留断言都按预期 RED；随后检查解析辅助图 TikZ 标签锚点并设计最小图稿断言。

### `phase2-b58` 三处余留版式回归测试 RED

- 已完成可验证阶段：为生成 TeX 增加断言，要求题 1(15) 的“且”不再独立成段并并入第二组展示公式、解析 q1(16) 标题前预留空间；为 q6 解析图增加 C 标签采用 `above left` 锚点的图稿保护，防止标签继续压住 AC 虚线。当前实现下三项均按预期失败。
- 阶段修改文件：`tests/test_generate_projects.py`、本 `PROGRESS.md`；规范试题/解析 Markdown、辅助图和派生 TeX 未改，正式 PDF/receipt/work items 未改。
- 阶段验证：分别运行两个定向 unittest。分页回归测试以两个 AssertionError 失败（q1(16) 前缺少 12-baseline 预留；q1(15) 生成 TeX 仍有独立“且”段落）；图稿回归测试以一个 AssertionError 失败（现有 C 标签仍用 `node[left]`）。无测试运行错误。
- 剩余任务：只调整三处版式源：把“且”放入 tg 条件展示式、在解析 q1(16) 前加入足够的 `\Needspace`、将解析图 C 标签移至 `above left`；题目数值、推导、几何坐标不改。GREEN 后须预览相关页，更新因版式标记变化而受影响的 provenance，再四版正式重建并重审 64 页。
- 下一步：实施最小源级版式调整后，重生成派生 TeX并运行上述两个定向测试至 GREEN；再单卷隔离编译，确认孤行与标签问题实际消失。

### `phase2-b58` 三处纯版式修复与定向回归测试 GREEN

- 已完成可验证阶段：题 1(15) 将“且”并入第二组 tg 条件展示公式；解析正文 q1(16) 标题前增加 `\Needspace{12\baselineskip}`；辅助图 C 标签从 `left` 移到 `above left`。没有改题目数字、结论、推导或图中 A/B/C/D/E 坐标。CJK 数学文本交由转换器包装为 `\text{且}`，避免源稿显式 `\text{}` 造成双层包装。
- 阶段修改文件：`1986/1986_数学真题_广东文_试题.md`、`1986/1986_数学真题_广东文_解析正文.md`、`1986_广东卷_文史类/figures/f1986_guangdong_arts_t6_solution.tex`、`tests/test_generate_projects.py`、本 `PROGRESS.md`。派生稿/TeX、provenance、build receipt、正式 PDF 与 review work items 尚未刷新。
- 阶段验证：针对生成级分页测试和图稿来源性测试均 GREEN；其中新增断言确认转换结果中的“且”不再单独成段、q1(16) 前有空间预留、C 标签锚点改为 above-left。实现前均观察到对应的预期 RED。
- 剩余任务：需通过官方事务刷新含解析派生稿及 TeX/index 投影；复跑整个 `test_generate_projects.py` 和源/生成器门禁。再在隔离目录编译四版预览，目视确认题 1(15) 连接词、q1(16) 跨页及解析图 C 标注确已改善。之后刷新受影响 provenance，四版正式重建并从新 attempt 重新复核 64 页。
- 下一步：按批次 `phase2-b58` 的官方 `solution_sources.py` 与 `generate_projects.py --write` 流程更新派生文件，再跑全文件测试和门禁。

### `phase2-b58` 派生稿刷新与测试/来源门禁阶段

- 已完成可验证阶段：按批次事务重新生成来源派生稿与该卷 TeX 投影；生成器检查、来源抽取检查、manifest 校验、`test_generate_projects.py` 全文件 105 项测试及 `git diff --check` 均通过。未重复运行这些已通过检查。
- 阶段修改文件：该卷派生 Markdown/TeX、相关生成索引与现有事务回执，以及本 `PROGRESS.md`；具体文件以当前 Git diff 为准。原始三处版式修复与新增回归测试仍在工作树中。
- 阶段验证：`solution_sources.py check-batch`、`generate_projects.py --check`、`source_manifest.py validate` 均通过；105 tests OK；diff whitespace 检查通过。随后运行 provenance 检查发现第 1 题题面哈希变化，批次现场状态仍为 `compiled_pending_review` 而派生状态为 `planned`，因此来源门禁暂未通过；这是当前源稿结构重排后的待处理证据，不代表校验通过。
- 剩余任务：按既有正式来源事务核验该哈希变化是否仅为等价版式重排，再决定是否只更新对应 question-review 摘要；完成 provenance 门禁后隔离预编译，验证三项版式修复的实际 PDF 效果。新源稿尚未正式编译，旧 attempt 的页面复核不可复用。
- 下一步：定向检查 provenance 哈希计算与 `phase2-b58` question-review 工作项，只触及第 1 题相关证据；不得直接绕过 import/check 门禁或改答案证据。

### `phase2-b58` q01 版式摘要核验与来源事务刷新

- 已完成可验证阶段：确认 provenance 对规范题面块逐字计算摘要；本次 q01 摘要变化来自仅调整“且”的段落/公式位置，连接词与两个条件的数学含义未变。固定来源仍为已逐页核对的同一份 PDF，既有 q01 transcription review 结论和已登记缺图 issue 保持不变。
- 阶段修改文件：忽略目录 `.work/phase2-b58/provenance/question-review/gk-1986-regular-guangdong-arts.json` 仅更新 q01 的 `question_text_sha256`（旧值 `74deae…158a8`，新值 `061dba…e384a`）；正式 provenance 与 manifest 由官方导入事务更新；本 `PROGRESS.md`。
- 阶段验证：`provenance.py import-batch` dry-run 通过且未落盘；随后官方 `--write` 事务提交 revision 3963；`provenance.py check-batch --batch phase2-b58` 返回 `OK：1 卷`。答案摘要、其余题目摘要、来源引用与审核结论未手工改动。
- 剩余任务：隔离编译当前四版并检查“且”行内呈现、解析 q1(16) 分页及解析图 C 标签；预览确认后才正式构建新 attempt。旧 attempt 的 64 页审核仍不可复用。
- 下一步：根据构建脚本的受支持参数，在独立临时目录编译预览版；只检查受影响页及编译日志，不覆盖正式 PDF/receipt。

### `phase2-b58` 四版隔离预编译与关键页复核

- 已完成可验证阶段：以 latexmk 相同 XeLaTeX 参数将四版输出到 `/tmp/pdfs/phase2-b58-preview.K5OYg6/`，未覆盖正式 `build/` PDF 或 receipt。四版均成功，页数分别为试题 7、解析 28、简答 8、印刷 22。
- 阶段修改文件：仅本 `PROGRESS.md`；预览 PDF 与 180/300dpi 检查图均在上述临时目录。
- 阶段验证：目视复核试题/简答 p3、印刷 p3/p8，题 1(15) 的“且”已与第二组条件同一行；解析 p15–16，题 1(16) 从 p16 小问标题起完整排版，未再以“有”单字开页；解析新增 p28 含完整第 7 题，不是空白页。印刷版解析辅助图位于 p20；300dpi 检查发现 C 标签仍与 S–D 虚线相交，故该项修复尚未通过。其他预览版页未经全面复核，预览不作为正式回执。
- 剩余任务：先把图稿 C 标签从 `above left` 移至右侧空白区，并更新回归断言；再重编受图稿影响的解析版、印刷版预览及高分辨率检查标签间距。之后正式四版构建并对新 attempt 的 64 页逐页复核。
- 下一步：把图稿回归断言改为要求 C 标签置于点的右侧，先运行观察到预期 RED，再最小调整锚点并验证 GREEN。

### `phase2-b58` C 标签版式修正与预览复核

- 已完成可验证阶段：高分辨率复核确认 `above left` 仍与 S–D 虚线相交；将图稿 C 标签改到点右侧空白区，未移动任何几何坐标。对应图稿测试先按新锚点断言 RED，再在修复后 GREEN。
- 阶段修改文件：`1986_广东卷_文史类/figures/f1986_guangdong_arts_t6_solution.tex`、`tests/test_generate_projects.py`、本 `PROGRESS.md`。
- 阶段验证：两个定向生成器测试（图稿来源/标签断言、三处版式回归）通过；解析版和印刷版在隔离目录成功重编。解析版 p27 与印刷版 p20 的 300dpi 图像确认 C 标签现位于右侧且不与虚线/边线相交；页面数仍为 28/22。四个预览 log 未发现 Overfull、LaTeX Warning、undefined、Error 或 Missing character 匹配项。解析版 p28 的第 7 题布局清楚。
- 剩余任务：更新图稿后尚未正式构建新 attempt；旧 64 页视觉复核报告不可复用。需进行正式四版构建、按当前 PDF SHA 和页数重建 review work items、逐页复核 64 页，再完成 receipt/finalization 门禁。
- 下一步：运行正式四版批次构建与构建回执验证；确认构建 SHA、页数、日志和 attempt 后，才启动新的页级复核。

### `phase2-b58` 四版正式构建 attempt `4f48ddc0-7717-45a0-a040-d69b1602dfa8`

- 已完成可验证阶段：该卷正式四版均编译成功，状态为 `compiled_pending_review`；当前 attempt 替代旧 attempt `53d535ef-8274-4f4d-b200-a7cfbe106069`。
- 阶段修改文件：该卷 `receipts/build.json`、批次 manifest 状态及正式 `build/` 下四份 PDF/编译产物；具体跟踪状态见 Git diff 与忽略构建目录。
- 阶段验证：`build_projects.py validate-receipts --paper gk-1986-regular-guangdong-arts` 返回 `OK`、无 failed/invalid/missing/stale。页数与 SHA：试题版 7 页 `e2f5ccad…b6c889c`；解析版 28 页 `aab14a0f…b1c01c05`；简答版 8 页 `40479a96…b700687`；印刷版 22 页 `711b8189…a71144f`。四版 log 的 error、missing character、undefined reference、overfull 列表均为空。
- 剩余任务：为新 attempt 准备四份新的 pending 页级 work item（合计 65 页、520 个八类检查），不得复用旧 attempt 的视觉结果；完成全部页面复核和必要的来源限制标注后再写回执。
- 下一步：查看 `review_receipts.py` 支持的初始化/刷新事务，按新 attempt、页数和 SHA 重置该卷工作项，再启动逐页视觉复核。

### `phase2-b58` 新 attempt 视觉工作项准备完成

- 已完成可验证阶段：按 attempt `4f48ddc0-7717-45a0-a040-d69b1602dfa8` 为四版准备全新工作项，覆盖试题 7 页、解析 28 页、简答 8 页、印刷 22 页，共 65 页 / 520 项检查；四个工作项全部是 `pending`，绑定 SHA 与正式 build receipt 一致。旧 attempt 结果未迁移。
- 阶段修改文件：忽略目录 `.work/phase2-b58/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-arts.json`；本 `PROGRESS.md`。review receipt 尚未登记。
- 阶段验证：`review_receipts.py prepare-batch` 创建 4 项；逐项核对 attempt、SHA、页数、检查总数。生成器检查、solution source 检查、manifest/provenance 检查和 `git diff --check` 均通过。完整单测套件正在运行；四版只读逐页盲核已并行派发。
- 剩余任务：收齐并核验四份独立报告，核对 SHA/页数/连续覆盖及八类结果，再把真实结论登记入工作项；已知来源限制须注明，不能计作版式通过或臆补内容。
- 下一步：等待完整测试与四版复核结果；若发现新缺陷，按批准范围修复并重建新 attempt，否则进入回执检查与事务 finalization。

### `phase2-b58` 新 attempt 四版全页盲核与结果录入

- 已完成可验证阶段：四名独立审查者均核验 attempt `4f48ddc0-7717-45a0-a040-d69b1602dfa8`、各自 PDF SHA 与连续页数，并实际渲染逐页覆盖全部 65 页。520 个检查项中 508 项通过、12 项失败；失败全部是既知来源限制，无新发现版式问题。q01(25) 来源选项图空白在六处出现，统一登记为 `figure_label`；一份审查报告原标为 `option_formula_alignment`，根据仓库 rubric“图形与标注”及其余三版一致结果归一。q02(2) 乘号缺字方框在六处统一登记为 `glyph`。
- 阶段修改文件：四份忽略的 `.work/phase2-b58/review/<edition>/gk-1986-regular-guangdong-arts.json` 已逐页登记 pass/fail 和失败说明；本 `PROGRESS.md`。12 项来源限制均保留原样并在 note 中注明；review receipt 尚未事务写入。
- 阶段验证：工作项均绑定当前 SHA/attempt，页覆盖 7/28/8/22，失败数按版为 2/4/2/4；唯一发现差异的分类按 `CHECK_CODES` rubric 统一为缺失图稿 `figure_label`。只读 `review_receipts.py check-batch` 因正式 review receipt 仍绑定旧 attempt 而报 stale；这是 finalization 前状态，工作项自身已按新 attempt 登记。`test_generate_projects.py` 的 105 项测试此前全通过，图稿锚点修订后两个相关回归测试仍通过；另一次宽泛 `unittest discover -s tests` 运行约 9 分钟后因额度优化中断（退出 130），不记为通过或失败。
- 剩余任务：用官方事务把失败结论与对应 visual issues 写入正式回执，验证批次报告/状态并按项目流程提交该已核验阶段；随后精确清理编译中间产物但保留四份 PDF 与 LaTeX 源文件，复跑最终门禁并核对 Git diff/status。
- 下一步：运行 `review_receipts.py finalize-batch` 的批次事务；预期状态为 `VISUAL_FAILED`，因为来源限制必须如实保留，不能伪报全部通过。

### `phase2-b58` 全页审查结论正式登记

- 已完成可验证阶段：官方 `review_receipts.py finalize-batch` 以单一事务写入新 attempt 的 review 失败回执、视觉问题与批次派生状态，revision 3966。结果为 `VISUAL_FAILED`，12 个失败检查均对应既知来源限制（六处 q01(25) 缺来源选项图、六处 q02(2) 乘号方框），未发现新视觉缺陷；因此未生成成功报告，build 保持 `compiled_pending_review`。
- 阶段修改文件：该卷 `receipts/review.json`、`missing-issues.md`、`source-manifest.json`、本 `PROGRESS.md`；正式四版 PDF 与 build receipt 均绑定当前 attempt。忽略目录中的 4 份 work item 已登记全部 520 项结论。
- 阶段验证：`review_receipts.py check-batch` 返回预期 `VISUAL_FAILED`；`build_projects.py validate-receipts` 返回 `OK`（pending 1、stale 0）；`provenance.py check-batch` 返回 `OK：1 卷`。视觉失败并非校验异常，而是来源缺陷需保留并阻止错误标成 passed。
- 剩余任务：按 `clean-build --dry-run` 精确确认可清理的 LaTeX 中间产物，执行后保留四份 PDF 与所有 `.tex` 源稿；核对 tracked diff 和 staged scope，提交本阶段已完成的内容，不 push。宽泛全量 `unittest discover` 已中断，退出 130，不视作测试通过；相关完整 105 项生成器测试此前通过，新增两项定向回归通过。
- 下一步：先对本卷运行构建清理 dry-run，审定删除清单只含中间产物后再执行；之后检查四 PDF、源 TeX、receipt 仍存在并核对 Git diff/status。

### `phase2-b58` 编译中间产物清理与 PDF 保留验证

- 已完成可验证阶段：`build_projects.py clean-build --dry-run` 确认其会删除整个 build 目录（包含 PDF），因此未执行该命令；先在隔离预览目录实测 `latexmk -c -outdir=...` 会清理辅助文件并保留 PDF，再对四版正式构建目录逐版执行相同清理。
- 阶段修改文件：仅本 `PROGRESS.md`；删除了该卷 `build/` 中四版 `.aux/.fdb_latexmk/.fls/.log/.out/.xdv` 等编译中间产物。PDF、项目 `.tex` 源稿、构建/复核回执均保留。清理了本次确切临时目录 `/tmp/pdfs/phase2-b58-preview.K5OYg6/` 和此前保留的 `/tmp/pdfs/phase2-b58-review.PEltpf/`。
- 阶段验证：正式 `build/` 现在仅含四份 PDF；SHA 仍与 build receipt 一致：试题 `e2f5ccad…b6c889c`、解析 `aab14a0f…b1c01c05`、简答 `40479a96…b700687`、印刷 `711b8189…a71144f`。四版 `.tex` 壳和题面/解析/图稿 `.tex` 均存在；`validate-receipts` 仍 `OK`、stale 0；复核状态仍如实为 `VISUAL_FAILED`。
- 剩余任务：最终审阅 tracked diff 与索引范围，提交已完成的来源、生成、正式构建、失败复核记录及进度；不 push。`unittest discover -s tests` 曾因耗时退出 130，不能称全量测试通过。
- 下一步：核对 `git status`、staged diff、完整 diff 摘要与 `git diff --check`；确认只包含本卷任务后，按现有提交规范提交。

### `phase2-b58` 提交前最终验收

- 已完成可验证阶段：最终复核确认 12 个 visual-review issues 全部绑定当前 attempt，均为 `open / blocks_completion`；四版 PDF、TeX 源稿和回执仍在，build 目录仅保留四份 PDF。
- 阶段修改文件：仅本 `PROGRESS.md`；提交候选范围为当前 Git status 中 1986 广东文史卷源稿、生成投影、图稿、测试、manifest/index/issues、build/review receipts 与本进度文件；没有 staged 变更。
- 阶段验证：本轮最新定向测试 2/2 通过；生成器、来源投影、manifest、provenance 与 build receipt 均通过；review check 返回预期 `VISUAL_FAILED`；`git diff --check` 通过。完整 `unittest discover -s tests` 因耗时退出 130，不宣称通过。最终检查报告了 12 项既知来源限制，未伪装成全绿。
- 剩余任务：当前卷仍被 ISSUE-0777/ISSUE-0793 的 q01(25) 来源图缺失及 q02(2) 乘号缺字限制阻塞；需未来取得更清晰同版来源后再核验/重建。其他语料和批次任务仍未完成。
- 下一步：仅暂存以上本卷任务路径并创建本地提交；不 push。

### `phase2-b57` 1986 上海文理四版全页复核正式登记

- 已完成可验证阶段：对当前文史 attempt `82cfd59c-7c07-40ea-bb71-438a59b57801` 和理工农医 attempt `dea4108d-f233-4641-8050-e2fac5986bb0` 的 8 份工作项完成提交前哈希核验；attempt、PDF SHA-256、页数均与 build receipt 和磁盘 PDF 一致。官方 `review_receipts.py finalize-batch` 事务 revision 3967 登记 91 页/728 项复核结果：726 pass、2 fail、0 pending。两项失败均为两卷试题版第 1 页 `answer_leak`；批次保持 `compiled_pending_review`，审查结果 `VISUAL_FAILED`，finalizer 未生成成功报告。
- 阶段修改文件：两卷 `receipts/review.json`、`missing-issues.md` 与 `source-manifest.json` 的事务派生状态；本 `PROGRESS.md`。未改题面、答案、LaTeX 源或正式 PDF。
- 阶段验证：8/8 工作项的 SHA/attempt/page-count 与正式 build receipt 及实存 PDF 匹配；逐版覆盖完整 91 页，检查项总数和状态为 726/2/0。finalizer 明确列出两处首页泄漏并以退出码 4 报 `VISUAL_FAILED`，不是校验执行错误。
- Ruling：保留两卷原有首页异文说明并按事实登记 `answer_leak` 失败，不擅自删改题面内容；这是遵循全量目标中“内容不足或有疑义时保留 blocker”的最小处理。若该边界判断错误，代价是两项视觉失败会继续阻塞批次完成，待取得单独内容处置授权后重开。
- 剩余任务：批次报告因视觉失败未生成；仍需按受支持报告工具生成反映 `VISUAL_FAILED` 的批次/全库投影，执行 scoped gates，并清理本批 build 中间产物（保留 8 份 PDF）。
- 下一步：先核对本事务实际 diff 与 report 工具命令，再更新批次报告/全库报告；随后做本批门禁、精确清理和本地提交，不 push。
- 已完成可验证阶段（报告投影与 scoped gates）：官方 `report.py render --all` 以单个 content 事务写入并回读验证六个全量报告目标；报告 check 确认投影与当前 manifest 一致，并保留未完成状态。
- 阶段修改文件：两卷 review receipts、`missing-issues.md`、`source-manifest.json`、renderer 管理的 `README_数学.md`、2017–2026 README、本项目 README、baseline、`report.md`、`docs/source-inventory.md` 与本进度文件。未修改共享模板/生成器或题目源。
- 阶段验证：source manifest（775 artifacts）、两卷 solution-source extraction、project/short-answer/edition generator checks、provenance、build receipt validation 均通过；review check 返回预期 `VISUAL_FAILED`；`report.py check --all` 与 `git diff --check` 通过。未运行全量单测，因为本阶段仅刷新回执/报告，项目最终审计再执行全套测试。
- 剩余任务：build 目录尚待确认和清除非 PDF 中间物；之后复验四版 PDF 与 receipt 哈希、运行相关 review/report 测试并核对精确 diff，再提交本阶段。
- 下一步：先列出两卷当前 build 目录文件，确保 PDF 清单与路径无歧义，再仅以 `latexmk -c -outdir=build` 清除各版辅助文件。
- 已完成可验证阶段（build 中间物清理与 PDF 保留核对）：对本批两项目四入口逐一执行 `latexmk -c -outdir=build`；两卷 `build/` 现在各仅保留试题、解析、简答、印刷四份正式 PDF。
- 阶段修改文件：本 `PROGRESS.md`；仅清理两卷 ignored build 中的 `.aux/.fdb_latexmk/.fls/.log/.out/.xdv`，未触及任何 PDF、LaTeX/TikZ 源或其他批次文件。
- 阶段验证：8 份保留 PDF 的 SHA-256、页数与正式 build receipts 全部一致（文史 4/18/5/14 页，理工农医 5/22/6/17 页）；目录无非 PDF 文件。
- 剩余任务：对 review/report 事务执行相关回归测试，复核最终 diff/status；随后提交本批回执、问题与报告投影更新，不 push。
- 下一步：定位并运行 `review_receipts.py` 与 `report.py` 对应的定向测试，再重跑 `report.py check --all` 和最终 `git diff --check`。
- 已完成可验证阶段（相关回归测试）：运行 `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_review_receipts.py -v` 与 `... -p test_report.py -v`，共 77 项通过、0 失败。
- 阶段修改文件：仅本 `PROGRESS.md`；测试未改写正式报告或事务状态。
- 阶段验证：review receipts 66/66、report 11/11；前置全库报告检查、manifest/provenance/build 与生成器门禁均已通过，视觉检查仍按预期 `VISUAL_FAILED`。
- 剩余任务：复跑最终报告一致性与 whitespace 检查，审阅本批精确 diff 和路径范围，并提交该阶段；不 push。
- 下一步：执行 `report.py check --all`、`git diff --check`、`git status --short` 与 diff 摘要，确认无测试副作用后，仅暂存本批与全库生成投影的明确路径并本地提交。

### `phase2-b58` 已完成内容本地提交

- 已完成可验证阶段：1986 广东文史卷本阶段已本地提交，提交信息为 `docs: 登记1986广东文史全页复核结果`；未 push。提交包含该卷来源转录与 LaTeX 投影、图稿、回执、复核问题、回归测试及本进度记录。
- 阶段修改文件：本提交覆盖 17 个受跟踪文件；详细范围以该提交记录为准。此次提交后仅追加本阶段状态记录。
- 阶段验证：提交前 `git diff --cached --check` 通过且无未暂存 diff；提交成功，提交后工作树干净。沿用前一阶段已记录的定向测试与来源/生成/回执门禁结果；未重复运行。
- 剩余任务：该卷仍有 12 项来源限制复核失败，分别涉及 q01(25) 缺失的来源选项图和 q02(2) 乘号缺字，阻止将该卷标为视觉完成。更大范围待核清单不属于本次提交范围。
- 下一步：取得适用的更清晰同版来源后，定向核验上述来源限制；在此之前保留当前 `VISUAL_FAILED` 结论，不扩展处理范围。

### `phase2-b57` 1986 上海文理复核阶段本地提交

- 已完成可验证阶段：两卷 91 页的视觉复核回执、两项 `answer_leak` blocker、批次状态与全库报告投影已本地提交，提交信息为 `docs(exams): 登记1986上海文理全页复核结果`；未 push。
- 阶段修改文件：该阶段提交覆盖 11 个受跟踪文件，包含两卷 review receipts、`missing-issues.md`、`source-manifest.json`、六个报告投影与本进度记录。
- 阶段验证：提交前 staged diff 精确覆盖上述 11 个路径且 `git diff --cached --check` 通过；review/report 定向测试 77/77 通过；`report.py check --all` 通过并保留 `VISUAL_FAILED` 状态；提交后工作树干净。
- 剩余任务：phase2-b57 两卷仍因试题版首页答案泄漏保持 `VISUAL_FAILED` / `compiled_pending_review`，题源未擅改；1952—2026 全语料目标仍在推进中。
- 下一步：按全量收尾计划继续处理最早尚未完成的批次；不重做 b57 已完成的来源、构建或页级复核。

### `phase2-b59` 1986 广东理工农医卷续作预检

- 已完成可验证子阶段：确认 b59 仅含 `gk-1986-regular-guangdong-science`，正式 build receipt 为 attempt `4178bc96-691e-4c97-b5b4-580cab0eb76c`、四版均 succeeded；既存四份 ignored review work items 仍全 pending，但绑定旧 attempt `3cba4219-937f-47bf-97cf-eda56e3440c4`。官方 `prepare-batch` 因生成输入树与工具链指纹变化拒绝复用/刷新旧构建。
- 阶段修改文件：未修改 tracked 文件；CLI 帮助及受支持工具均只读。一次带不支持 `--json` 参数的 prepare 命令以 usage 错误退出，未写入状态；无效 receipt 后，正确 prepare 调用也安全拒绝。
- 阶段验证：source manifest、solution-source、project、short-answer、edition checks 均通过；provenance 检查未通过，唯一已报告差异为缓存批次状态 `compiled_pending_review` 与现场派生 `provenance_verified` 不符。未覆盖状态，也未开始复核 stale PDF。
- 进一步核验：官方 `provenance.py status --batch phase2-b59` 显示试卷维持 `blocked`、批次 provenance 派生状态为 `provenance_verified`；没有题面/答案内容哈希失配。故不在缺少新角色证据时重导 provenance，选择通过正式构建事务刷新 stale build 与派生批次状态。
- 剩余任务：正式 build receipt 刷新至 current 后，才能准备当前 attempt 工作项并复核 60 页。现有来源 blocker ISSUE-0778/ISSUE-0797 必须保留。
- 下一步：执行 `build_projects.py build --formal --batch phase2-b59` 更新正式四版 attempt；验证页数、警告、SHA、receipt 和 provenance 派生状态，再刷新工作项。
- 已完成可验证阶段（stale build 正式重建）：官方 formal build 事务 revision 3969 完成四版并创建新 attempt `d185c2df-20ab-4f8b-ad88-91cddb6f3568`，替代 stale attempt `4178bc96-691e-4c97-b5b4-580cab0eb76c`。页数保持 7/26/8/19，共 60 页；四版均 succeeded。
- 阶段修改文件：该卷 `receipts/build.json`、`source-manifest.json` 事务状态及 ignored `build/*.pdf`；本 `PROGRESS.md`。
- 阶段验证：`validate-receipts` 返回 `OK`（1 pending、0 stale/invalid/missing/failed）；`provenance check-batch` 返回 `OK：1 卷`。四版 logs 的 errors、missing characters、overfull、undefined references 和 problems 均为空。
- 剩余任务：四份工作项仍绑定旧 attempt，须刷新后再做 60 页/480 检查；两项既有来源问题继续阻断完成。
- 下一步：运行官方 `review_receipts.py prepare-batch --batch phase2-b59`，逐项确认新 attempt、PDF SHA 和页数后分派视觉复核。
- 已完成可验证阶段（当前 attempt 工作项刷新）：官方 `prepare-batch` 为 b59 刷新 4 份 ignored review work items，均绑定新 attempt `d185c2df-20ab-4f8b-ad88-91cddb6f3568`。
- 阶段修改文件：仅 `.work/phase2-b59/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-science.json` 四个 ignored 工作项；tracked 内容未变。
- 阶段验证：4/4 项的 attempt、PDF 路径/SHA-256、页数均与新 build receipt 和实存 PDF 相同；覆盖 60 页，480 项全为 pending。
- 剩余任务：对当前 attempt 的 60 页完成逐页视觉复核，记录真实的来源限制与任何新排版发现；之后正式 finalize、更新报告、清理中间物、复跑门禁并提交。
- 下一步：独立并行复核试题+简答、解析、印刷三个版本组；主会话核验页覆盖与 fail 依据后再登记正式回执。
- 已完成可验证阶段（当前 b59 attempt 四版视觉复核）：三组独立审查者覆盖全部 60 页/480 项；结果为 451 pass、29 fail、0 pending。每项 work item 绑定 attempt `d185c2df-20ab-4f8b-ad88-91cddb6f3568` 与各版当前 PDF SHA/页数；临时审查图已由各审查者清理。尚未写正式 review receipt。
- 阶段修改文件：仅四份 ignored `.work/phase2-b59/review/*/gk-1986-regular-guangdong-science.json` 与本 `PROGRESS.md`；正式题源和 review receipt 未改。
- 阶段发现：已知 q01(25) A—E 图形缺失、q01(12)/(15) 重复 D 标记继续保留；另见试题选项跨页、印刷版解析标题孤置、三棱锥 E 标签碰线、解析题号错配。主会话对照固定源 PDF（SHA-256 `ad1042cc…cda24`）目视确认：源 PDF 第 5 页“第二卷·二”为直线/平面关系题，并非当前源稿和图稿中的三棱锥题；“辐角主值”题为第一卷第 5 小题，而非第 9 小题。当前解析正文多个第一卷小题编号与题意不对应，不能以现 attempt 通过构建作为内容正确证据。
- Ruling：暂停 b59 正式 review finalize；先按固定源纠正明确的题面/解析错配并独立复算受影响答案，再更新 provenance、正式重建和受影响页面复核。若源页结构理解有误，代价是需返工题源和后续 build；本决定以已核验的固定 PDF 页图、页码和逐字文本为依据。
- 剩余任务：完整复算第一卷 25 道选择题的详细解析与答案要点对应关系；按 PDF 转录第二卷第二题及两幅平面关系图，并从固定解答页核对证明/数值；修正首页题号说明、版式跨页/孤置与图稿；保留无法核对的 q01(25) 图形 blocker。
- 下一步：并行委派互不重叠的 q01(1–12) 与 q01(13–25) 独立盲解/题解映射；主会话对照固定源第 5、7–11 页完成 q4 及解答源核查，随后整合并按官方事务刷新 provenance、生成、build 和 review。
- 已完成可验证阶段（第二卷第二题源稿错配核实）：重新目视检查固定 PDF 第 5 页并以 `pdftotext -layout` 对照第 5、7–11 页，确认第二卷第二题为两小题的直线—平面关系题，原题干与图均不是三棱锥；固定解答给出第（1）题证明链与第（2）题角度结果 `arcsin(sqrt(4b^2+a^2)/(2a))`。原题文档、答案要点和详细解析仍未修改；未经逐题独立核对，不沿用现稿中不匹配的三棱锥答案。
- 阶段修改文件：仅本 `PROGRESS.md`；题源稿、答案和图稿未改。尝试恢复上一轮三项盲审时，subagent 服务返回 `agent thread limit reached`，未生成新代理或报告；避免重复提交同样无效的调用，继续在主会话直接核查。
- 阶段验证：固定 PDF SHA-256 与上段记录的来源清单值一致；第 5 页图像可辨识题干及两幅图；文本提取与官方解答内容一致。尚未运行生成器或构建，因为源稿尚未修改。
- 剩余任务：替换第二卷第二题题面与错误图稿、答案及解析；独立核验第一卷 25 小题解析和答案映射；处理已确认的题号说明和纯版式缺陷，同时保留 q01(25) 缺图 blocker。
- 下一步：先完成第二卷第二题的受控源文修订和对应 TikZ 图稿，加入精确题面/数值回归检查，再更新 provenance 并走正式生成、构建与复核事务。
- 已完成可验证阶段（第二卷第二题题面、解析和图稿纠正）：按固定 PDF 第 5 页把错录的三棱锥题替换为直线—平面两问；题面恢复源符号 $\alpha$ 和分值 14，答案要点及解析改为平面垂直证明与角度公式 $\arcsin(\sqrt{4b^2+\alpha^2}/(2\alpha))$。两幅矢量示意图替换错误三棱锥图；解析不把原图标记 E 的交叠误读为空间交点。同步更正第 5 题辐角说明，并把第 8、9、20、25 题的源限制明示为待核/歧义，不凭空补符号或选项图。
- 阶段修改文件：`1986/1986_数学真题_广东理_{试题,答案要点,解析正文,含解析}.md`；本卷 `questions.tex`、`answers.tex`、TikZ 图稿（删除旧 pyramid，新增 planes）、`index.json`、`source-manifest.json`；本 `PROGRESS.md`。`questions.tex`、`answers.tex`、`index.json` 与含解析文档均由官方确定性生成器/解析正文抽取器刷新。
- 阶段验证：固定源 PDF 第 5 页已目视核对；`source_manifest.py validate --manifest source-manifest.json` 通过；本卷 `generate_projects.py --check` 通过；`solution_sources.py check-batch --batch phase2-b59` 通过；`test_generate_projects.py` 105 项通过；`git diff --check` 通过。第一次门禁发现试题小问标记后缺分隔空格、又发现含解析投影残留旧 PNG 记号；经证实分别是解析器锚点格式与未刷新的派生投影问题，已按源稿排版补空格并用受支持抽取器重生成后复验通过。
- 剩余任务：第一卷 25 题的既存解析正文仍有题号/题意错配，需逐题按固定源改写并对照独立盲解；之后重新登记 provenance、正式四版构建及视觉复核。q8/q9 缺字、q20 语义歧义、q25 缺图继续作为明确限制。
- 下一步：依据 `.work/phase2-b59/answer-audit/q01-01-12.md` 与 `q01-13-25.md` 逐题映射当前第一卷解析，先处理 1–12 题并记录仍不能确定的选项，再继续 13–25 题；不复做来源 PDF 比对。
- 已完成可验证阶段（第一卷选择题 1–12 解析重映射与复算）：将解析正文前 12 个锚点逐项按原题更正，覆盖直线斜率、三角差角、正三棱锥二面角、参数椭圆、复数辐角、复数幂、复平面轨迹、医生组选法、节目排序、指数和最值、余切条件三角式、根式化简。第 8、9 题保留可复算数值 2156/7200，但答案要点不再把 E/C 写成无条件答案；因扫描连接符是不可辨方框，仅记录“若为乘号则对应 E/C”，字母待核。
- 阶段修改文件：1986 广东理科 `_解析正文.md` 与 `_答案要点.md`；官方抽取器生成的 `_含解析.md`、本卷 `answers.tex` 及 `index.json`（题面投影未变化）；本 `PROGRESS.md`。
- 阶段验证：两份独立盲解审计报告 `.work/phase2-b59/answer-audit/q01-01-12.md` 和 `q01-13-25.md` 已逐项作为答案依据；`solution_sources.py check-batch --batch phase2-b59`、本卷 `generate_projects.py --check`、`source_manifest.py validate` 均通过；`test_solution_sources.py` 109 项通过；`git diff --check` 通过。
- 剩余任务：第一卷选择题 13–25 的解析锚点仍与原题错配，尚需重写并核验答案要点，尤其 q20 语义歧义、q25 选项图缺失；q8/q9 的源字形 blocker 也尚未写入独立问题记录。构建 receipt 仍需待全部源内容稳定后经正式事务刷新。
- 下一步：依 `q01-13-25.md` 的独立推导重写第一卷 13–25 解析；只对 q20 保留语义条件结论，对 q25 只记可确定的函数图形性质、不映射缺失字母。
- 已完成可验证阶段（第一卷选择题 13–25 解析重映射与歧义保留）：按独立盲解报告替换错配推导，覆盖最大值、反正切、交点数、动圆轨迹、焦点圆、单调区间、对数值域、空间命题、四棱锥判定、奇偶性、函数图象辨析、抛物线距离和、反函数图象。q20 明示“边”为线段/支撑直线两种含义导致的结论差异；q25 只登记 $f(x)=-\sqrt{2x-x^2}$、定义域和弧段性质，并说明原答案表 E 因选项图空白而无法核验。
- 阶段修改文件：1986 广东理科 `_解析正文.md` 与 `_答案要点.md`；官方抽取器生成的 `_含解析.md`、本卷 `answers.tex`、`index.json`；本 `PROGRESS.md`。
- 阶段验证：按 `.work/phase2-b59/answer-audit/q01-13-25.md` 逐题复算；`solution_sources.py check-batch --batch phase2-b59`、本卷 `generate_projects.py --check`、`source_manifest.py validate` 通过；`test_solution_sources.py` 109 项通过；`git diff --check` 通过。
- 剩余任务：需要核查并按规范登记 q8/q9 缺字、q20 几何语义与 q25 缺图问题；核验全部 25 项答案要点、详细解析与固定答案表之间的对应；之后更新 provenance、正式四版重建、全页复核及版式问题处置。
- 下一步：定向检查本卷 `missing-issues.md` 与 manifest issue_ids，补齐三类已有证据支持的 blocker（不引入推测）；随后做解析/答案全卷交叉核查及四版正式重建。
- 已完成可验证阶段（第一卷选择题 13–25 解析及答案边界核验）：按独立题面报告重写 13–25 推导；q20 对“边”按线段解释给出 E、按支撑直线解释指出五项均非普遍成立，不擅改原文；q25 将反函数写为 $f(x)=-\sqrt{2x-x^2}$（$0\le x\le1$），保留答案表 E 作为来源记录并明确图形选项缺失、字母不可核验。
- 阶段修改文件：1986 广东理科 `_解析正文.md`、`_答案要点.md`；官方抽取器生成的 `_含解析.md`、本卷 `answers.tex`、`index.json`；本 `PROGRESS.md`。
- 阶段验证：对照 `.work/phase2-b59/answer-audit/q01-13-25.md` 的独立逐题推导；`solution_sources.py check-batch --batch phase2-b59`、本卷 `generate_projects.py --check`、`source_manifest.py validate` 通过；`test_solution_sources.py` 109 项通过。抽取器报告投影已最新；`git diff --check` 将与问题登记阶段一并复核。
- 剩余任务：q8/q9 运算符缺字与 q20 语义歧义尚未各自登记到问题总账；q25 虽已有 ISSUE-0778/0797，但须确认其文字涵盖本轮限定源核查结论。答案表、解析与源答案页还需全卷交叉核对，之后再刷新 provenance/build/review。
- 下一步：仅在 `missing-issues.md` 追加有固定源证据的 q8、q9、q20 问题记录；遵循 issue fingerprint 与 manifest 派生规则，验证登记后本卷 blocker id 完整。
- 已完成可验证阶段（题源限制登记）：在问题总账末尾新增 ISSUE-1053/1054/1055，分别记录 q01(8) 连接符缺字、q01(9) 连接符缺字及 q01(20)“边”的语义分歧；全部关联固定 PDF source_id，列明可复算结果、条件选项与解除条件。现存 ISSUE-0778/0797 继续保留 q01(25) 原图缺失。
- 阶段修改文件：`math-gaokao-latex/missing-issues.md` 与本 `PROGRESS.md`；尚未刷新 manifest 派生 issue_ids 或 provenance。
- 阶段验证：`issues.py validate --file missing-issues.md`、source manifest 校验、solution-source batch check、本卷生成检查及 `git diff --check` 均通过；新增 fingerprint 由项目 `issue_fingerprint()` 对规范身份计算并通过总账校验。
- 剩余任务：manifest 当前卷的 `issue_ids` 仍只有旧记录，需由受支持 provenance 事务从问题总账重算；然后重跑 provenance、正式四版构建与视觉回执，核对既有 29 个版面/内容失败是否仍适用。
- 下一步：查看 provenance CLI 的当前支持操作，按已授权范围重核本卷来源与答案证据，更新问题绑定后再执行正式构建；不手工改派生 issue_ids 或 build receipt。
- 继续核验：`provenance.py status --batch phase2-b59` 当前报告卷为 `blocked`、批次为 `planned`；旧 provenance 与本轮改稿哈希不一致，不能直接复用。`init-batch` 已创建三角色、6 大题骨架，忽略文件位于 `.work/phase2-b59/provenance/phase2-b59/provenance/{question-review,answer-solve,answer-review}/gk-1986-regular-guangdong-science.json`；CLI 的 `--work-dir` 是 `.work` 基目录，本次传入了更深的合法 ignored 子目录，故文件额外嵌套一层，尚未填充或导入，正式 provenance 未变。
- 当前实际修改：除前述题源、图稿、派生投影、问题总账及本进度外，未编辑 provenance 或构建回执；未正式重建 PDF。
- 下一步：审读该卷现有 provenance 和三份角色骨架，复用未变题的有效证据，仅为本次更改的题面/答案重算哈希并补足独立复核；待 `provenance check-batch` 通过后，走正式 build 事务并重新准备四版页审工作项。
- 已完成可验证阶段（b59 provenance 刷新）：三角色工作项基于固定 PDF 与独立审计证据填写；官方 `provenance.py import-batch --write` 事务 revision 3970 写入当前题面/答案哈希并从问题总账推导 issue_ids。更新涵盖 q01 25 小题的未决项、q03 题面分值修订、q04 题面/答案重写；其余答案哈希与既有记录一致。
- 阶段修改文件：1986 广东理科 `provenance.json`、`source-manifest.json` 事务 revision/issue_ids、`missing-issues.md` 新增整题组 blocker ISSUE-1056；ignored 三角色工作项；本 `PROGRESS.md`。
- 阶段验证：官方 `provenance.py import-batch` 只读预检通过后以 `--write` 提交；`provenance.py check-batch --batch phase2-b59` 返回 `OK：1 卷`；status 为试卷 `blocked`、批次 `provenance_verified`，与 q01 未决 blocker 一致。manifest 当前卷登记 ISSUE-0778/0797/1053/1054/1055/1056。
- 剩余任务：正式 PDF 仍对应旧输入；需先正式构建四版，核对页数、PDF 哈希、工具链和 warning，再为新 attempt 刷新工作项并重新逐页审查。不得沿用旧 451/480 视觉结论。
- 下一步：运行官方 `build_projects.py build --formal --batch phase2-b59`；构建后验证四版 receipt 与生成输入当前性，再启动新 attempt 的页级复核。
- 已完成可验证阶段（1986 广东理科四版正式重建）：官方 `build_projects.py build --formal --batch phase2-b59 --json` 事务 revision 3972 创建 attempt `5167c87d-c1a7-4e96-bcc1-d1125298bb7f`，四版 succeeded。
- 阶段修改文件：该卷 `receipts/build.json`、`source-manifest.json` 事务派生状态及四份 ignored `build/*.pdf`；本 `PROGRESS.md`。
- 阶段验证：页数为试题 7、解析 26、简答 8、印刷 19，共 60 页；四版 errors、missing characters、overfull、undefined references、problems 均为 0；`build_projects.py validate-receipts --batch phase2-b59 --json` 返回 `OK`（failed/invalid/missing/stale/running 均 0）；provenance batch check 与本卷生成一致性检查均通过。卷状态仍是 compiled_pending_review，不因构建成功而标为完成。
- 剩余任务：60 页的新 attempt 尚无当前 review 工作项；旧 attempt 的 451/480 结果不能复用。仍需全页视觉审查、登记真实失败、报告投影/门禁、清理编译中间物及提交。
- 下一步：官方 `review_receipts.py prepare-batch --batch phase2-b59` 刷新四版工作项；校验 attempt、PDF SHA 和页数后，重新覆盖全部 60 页。
- 中断恢复核验：先检查了规范工作树 `phase0-wt`、分支 `feat/gaokao-phase0`、当前 Git diff 与本进度文件。b59 当前正式 build attempt 仍为 `5167c87d-c1a7-4e96-bcc1-d1125298bb7f`；但 `.work/phase2-b59/review/` 及其页审工作项在本次恢复时不存在，因此不能把先前准备状态或旧 attempt 的 451/480 结论当作当前证据。tracked diff 仍仅涉及 1986 广东理科题源/派生文件、问题总账、manifest 和本进度记录。
- 本次优化执行约束：复用已通过的解析、provenance 与正式构建门禁，不重跑全库；只重建当前 attempt 的四版 review work items，按 PDF 版次并行核查相互独立页组，完成后运行 review/report 相关门禁并更新本记录。
- 恢复状态更正：工作项实际位于项目内 `math-gaokao-latex/.work/phase2-b59/review/`（而非仓库根 `.work/`）。四份文件均已存在并绑定 attempt `5167c87d-c1a7-4e96-bcc1-d1125298bb7f`，分别覆盖试题 7 页、解析 26 页、简答 8 页、印刷 19 页，共 60 页/480 项，当前全为 pending。误用根目录路径检查及一次安全拒绝覆盖的 `prepare-batch` 调用均未改写工作项；不再重复准备命令。此前“工作项目录不存在”的表述系路径检查错误，以本条实测为准。
- 并行工具状态：尝试并行分派四版审查，但平台因 agent thread limit 拒绝启动，未创建子任务；不重复尝试，改由主会话本地完成全页视觉核查。临时渲染只存于 `/tmp/gk1986-b59-pages.9OVfAJ/`，尚未写入 review 结果。
- 本轮审查结论暂不登记：四版 60 页完成目视检查后，finalizer 因 artifact stale 安全拒绝；构建回执本身 current（build validate pending 1、stale 0）。定向生成器检查确认唯一 stale 投影为 `answers_short.tex`；只读差异发现该投影保留了修订前的 q01(8)/(9)/(20)/(25) 结论及旧 q04 三棱锥答案，与当前规范源不符。当前 attempt 的 480 项审查已作废，不写入正式 receipts；须官方刷新简答投影后正式重编，再审新 attempt。
- 已完成可验证阶段（简答答案投影同步）：通过官方 `make_short_answers.py --write --paper gk-1986-regular-guangdong-science` 从当前题面、答案和解析生成 `answers_short.tex`；投影现覆盖 q01(8)/(9) 条件选项待核、q01(20) 语义歧义、q01(25) 函数信息/选项图缺失及 q04 新答案，不再保留旧结论。
- 阶段修改文件：仅该卷 `answers_short.tex` 与本 `PROGRESS.md`；未手改生成文件。
- 阶段验证：本卷 `make_short_answers.py --check`、`generate_projects.py --check`、`make_editions.py --check` 全通过。旧 PDF/构建回执及 480 项视觉工作项都不再与当前简答投影闭合，尚未正式重编或登记复核。
- 下一步：仅对 phase2-b59 执行正式四版构建，验证新 attempt 的四份 PDF、页数/哈希/警告与构建 receipt；再准备并核验新 attempt 工作项，不能复用本次已作废结论。
- 已完成可验证阶段（同步简答投影后的正式重建）：官方 `build_projects.py build --formal --batch phase2-b59 --json` 事务 revision 3974 创建新 attempt `4282128a-6c7e-4b68-ab5d-6ac670b3a70c`；四版全部 succeeded，卷状态仍为 `compiled_pending_review`。
- 阶段修改文件：该卷 `receipts/build.json`、`source-manifest.json` 派生状态、四份 ignored build PDF 与本 `PROGRESS.md`；新 attempt 替代之前因简答投影陈旧而失效的 `5167c87d…`。
- 阶段验证：页数仍为 7/26/8/19，共 60 页；errors、missing characters、overfull、undefined references、problems 合计 0；四 PDF 新 SHA 已记入 build receipt。`build_projects.py validate-receipts` 返回 OK（stale 0），provenance batch check 与题面/答案/简答生成一致性检查通过。
- 剩余任务：新 attempt 尚无视觉工作项；此前 480 项结论绑定旧 attempt，必须全部重审。复核仅登记来源缺陷 q8/q9 运算符、q25 图形选项缺失等真实项目，不复核已通过的来源解题过程。
- 下一步：对新 attempt 执行官方 `review_receipts.py prepare-batch`；核对四版 hash、页数与 60 页覆盖后，使用低开销联系表核查并放大疑点页。
- 已完成可验证子阶段（新 attempt 复核工作项）：官方 `review_receipts.py prepare-batch --batch phase2-b59` 为四版创建 4 份工作项，均绑定 attempt `4282128a-6c7e-4b68-ab5d-6ac670b3a70c`；页数 7/26/8/19，合计 60 页/480 checks，全部 pending。
- 阶段修改文件：仅 ignored `.work/phase2-b59/review/{试题版,解析版,简答版,印刷版}/gk-1986-regular-guangdong-science.json` 与本 `PROGRESS.md`。旧 attempt 工作项因输入投影陈旧而由官方工具刷新；其结论不视为当前 attempt 回执。
- 阶段验证：4/4 工作项的 attempt、PDF 路径、SHA-256、页数及连续页码与新 build receipt 相符；未复用旧页级状态。
- 剩余任务：新 attempt 的全页审查；此前旧 attempt 已经做过目视检查，但不能直接依旧 attempt 登记。为避免重复劳动，下一步将逐页对比两次同工具渲染图像，仅像素完全一致的页面沿用已有视觉观察，变化页重新放大检查，再登记新 attempt 结论。
- 下一步：以相同 `pdftoppm` 版本/参数重新渲染当前四版，按页和旧 `/tmp/gk1986-b59-pages.9OVfAJ/` 图像做像素差；所有变化页定向复核。
- 已完成可验证阶段（新 attempt 四版视觉复核）：attempt `4282128a-6c7e-4b68-ab5d-6ac670b3a70c` 的 60 页全部有当前结论。旧 attempt 与新 attempt 以相同渲染器/参数逐页比较，59 页 PNG 字节完全一致；唯一变化为简答版 p8，已放大复核 q8/q9/q20/q25 限定答案和 q4 新答案，排版清晰。其余页面复用已完成的逐页视觉观察，仅在像素完全相同后迁移观察结论，不沿用旧 attempt 的工作项状态。
- 阶段修改文件：4 份 ignored 新 attempt review work items 与本 `PROGRESS.md`；review receipt 尚未正式写入。
- 阶段验证：60 页 × 8 checks 全覆盖，无 pending、无空 note；合计 472 pass、8 fail。每版各 2 项 fail：p2 `glyph`（q8/q9 源运算符不可辨，ISSUE-1053/1054）及 q25 所在页 `figure_label`（选项图缺失，ISSUE-0778/0797）；印刷版页码分别为 p2/p3，其余版本 p2/p4。四份 work items 的 attempt、PDF SHA 和页数均与新 build receipt 一致。
- 剩余任务：把 8 项真实来源限制正式登记为 review receipt/visual issues，并验证批次状态与报告；随后运行 review/report 定向测试与相关门禁、清理编译中间产物、复核 diff 并提交。不 push。
- 下一步：官方 `review_receipts.py finalize-batch` 执行单批事务；预期结果 `VISUAL_FAILED`，保留 blocked 状态，不把来源缺陷伪报为版式通过。
- 已完成可验证阶段（新 attempt review 正式登记）：`review_receipts.py finalize-batch` revision 3975 原子登记当前 attempt 的 60 页/480 项结果、视觉问题及派生状态；472 pass、8 fail、0 pending。失败为四版各一项 q8/q9 源运算符未决 `glyph` 与一项 q25 来源选项图缺失 `figure_label`，未发现新的排版缺陷。
- 阶段修改文件：该卷 `receipts/review.json`、`missing-issues.md` 新增当前 attempt 视觉问题、`source-manifest.json` 事务派生状态与本 `PROGRESS.md`；正式构建仍绑定 attempt `4282128a-6c7e-4b68-ab5d-6ac670b3a70c`。
- 阶段验证：finalizer 返回预期 `VISUAL_FAILED`，批次保持 `compiled_pending_review` 且未生成成功报告；review check、build receipt validation、provenance check 和本卷三个生成器一致性检查通过。一次 `report.py check --all` 因漏传必需的 `--manifest/--issues` 参数仅显示 usage，未写入状态，现将按帮助补齐参数重跑。
- 剩余任务：跑 review/report 定向回归测试、正确参数的全库报告一致性只读检查及 whitespace/diff 检查；确认视觉问题和报告状态，清理该卷构建中间产物但保留 PDF/TeX，然后按用户要求提交已完成阶段，不 push。
- 下一步：以支持的参数运行 `report.py check --all --manifest source-manifest.json --issues missing-issues.md`，并运行 `test_review_receipts.py`、`test_report.py`。
- 已完成可验证子阶段（review/report 定向测试与报告投影诊断）：`test_review_receipts.py` 66/66、`test_report.py` 11/11 通过。带齐参数的 `report.py check --all` 发现 6 个由本事务变更导致的全库报告投影 stale（source inventory、exams report/README、LaTeX 项目 README、2017–2026 README、baseline），没有修改这些文件。
- 阶段修改文件：仅本 `PROGRESS.md`；测试和只读报告检查未落盘。
- 剩余任务：用官方 `report.py render --all` 刷新这 6 个派生投影，再 `check --all` 确认一致；之后清理中间产物、跑最终门禁、审阅并提交。
- 下一步：运行 `report.py render --all --manifest source-manifest.json --issues missing-issues.md`，随后再次检查报告投影。
- 已完成可验证阶段（报告投影与中间物清理）：官方 `report.py render --all` 事务更新并回读校验 6 个报告投影；`report.py check --all` 随后通过，报告与 manifest 一致且保留 blocked/未完成状态。对该卷四个入口分别执行 `latexmk -c -outdir=build`。
- 阶段修改文件：六个全库派生报告、本卷四版 build 中间物删除及本 `PROGRESS.md`。build 目录仅保留四份 PDF；题面/解析/图稿 TeX、PDF、build/review receipts 均保留。
- 阶段验证：build 目录精确列出四份 PDF；SHA 为试题 `30c259aa…fb7a64`、解析 `57e78223…7d3406`、简答 `b61e2b89…1c4046d`、印刷 `3e8c4ddf…664e50a`，与当前 build receipt 一致；build validator OK（stale 0）；source manifest/provenance/generator checks、review/report 定向测试（66+11）及 `git diff --check` 均通过。review check 仍按预期为 `VISUAL_FAILED`（8 项来源限制），批次保持 `compiled_pending_review`。
- 剩余任务：核对完整 tracked diff、索引/报告范围和暂存路径，创建本地提交；不 push。全语料完整测试未运行，因为本阶段是单卷内容、回执与派生报告事务，review/report 定向测试和 scope gates 已覆盖变更面。
- 下一步：执行最终 Git 状态与 diff 审阅，确认仅本卷、全量派生报告和本进度记录，然后本地提交。
- 已完成阶段（`phase2-b59` 本地提交）：经核对暂存范围仅包含1986广东理科源稿/投影/回执、相关报告投影及本进度，`git diff --cached --check` 通过；已提交为 `5aa9b9ad`（`docs(exams): 修订1986广东理科并登记四版复核`），未 push。
- 阶段修改文件：本提交的 22 个 tracked 文件；ignored review 工作项与 build PDF 未入库，build 中间产物已清理。
- 阶段验证：提交后工作树干净；四版 build 及当前 review 回执仍绑定 attempt `4282128a-6c7e-4b68-ab5d-6ac670b3a70c`。视觉状态如实为 `VISUAL_FAILED`，不能在缺少更清晰同版来源时关闭 ISSUE-0778/0797/1053/1054；q20 语义歧义 ISSUE-1055 与整题组 ISSUE-1056 也仍 open。
- 剩余任务：获取足以核验缺失图形/运算符/题意的固定版本来源，解除来源 blockers 后再更新 provenance、重建和全页复核；1952—2026 全语料目标继续未完成。
- 下一步：按全语料计划选择下一个已准备批次；不重做 b59 已通过的题面/答案审计、正式构建、视觉核验及定向测试。

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
- 待完成：提交 b40 内容与报告投影，再单独提交本进度记录中的提交哈希和下一批状态。
- 下一步：提交已核验的 b40 变更（不 push）；提交后记录哈希并检查下一批 `phase2-b41`（1977 江苏农垦、南京、南通地区、南通市四卷）。

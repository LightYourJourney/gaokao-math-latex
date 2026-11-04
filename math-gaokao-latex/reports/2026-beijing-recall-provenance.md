# 2026 北京回忆版候选卷：逐题三角色 provenance 导入

- 日期：2026-11-04。
- worktree：`仓库根`；分支：`feat/gaokao-phase0`。
- paper/batch：`gk-2026-regular-beijing-recall` / `phase4-b49`。
- 固定来源：`src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee`；PDF SHA-256 `7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9`；Git blob `cf49aa3671ff4143e5c665c7bc53b5f08ab38fca`；5 页。来源首页自称回忆版，发布者、版次、复制链和官方身份未核，`official_answer=null`。
- 当前 provenance 文件：`2026_北京卷_回忆版/provenance.json`；SHA-256 `b46fef9e0dcbbe9aeef8259ad1b1e3ed419bba3f3799b52615178a66515f166b`。初次导入文件的 SHA-256 为 `a9f4bc1505ec5756de513695596653625deb821236a07df9ed4803035a810de5`，后续 Q13 答案排版修正与重新绑定见[简答与四版入口阶段报告](2026-beijing-recall-short-answers-editions.md)。

## 导入内容与边界

- 为 Q1–Q21 导入独立的题面复核、盲解汇总、主会话复算/交叉核对记录。逐题题面复核均为 `passed`，含义仅为规范题面忠实于上述固定候选 PDF 字节，不认证正式卷身份。题号对应 PDF 页码为：Q1–Q9 第1页；Q10 第1–2页；Q11–Q16 第2页；Q17–Q18 第3页；Q19–Q20 第4页；Q21 第5页。
- 盲解与主会话复核记录均指向既有[独立答案推导与交叉复核报告](2026-beijing-recall-independent-solve-review.md)；角色分别记为“两路独立盲解角色（汇总记录）”及“主会话独立复算与交叉核对”，没有虚构模型、姓名或未记录的独立产物。题面角色依据[题面转录复核报告](2026-beijing-recall-question-transcription-review.md)和固定原页核验记录。
- Q10 固定候选字面下推导区间 `[5/16,73/80]`、对应候选版 B；第三方未认证副本将其列为 A。数学推导等级记 D，但跨来源最终选项保留 U/PENDING、`conflict_status=unresolved`，由 `ISSUE-1408`、`ISSUE-1415` 阻断。
- Q13 固定候选的非严格上界给 `[700,4900]`，第三方未认证副本的严格上界给 `[700,4900)`。条件推导等级记 D，但最终端点保留 U/PENDING、`conflict_status=unresolved`，由 `ISSUE-1409`、`ISSUE-1416` 阻断。
- Q15 两份来源仅将陈述②③交换编号；复核记录四项均成立，因此答案集合不受交换影响，但题面版本异文 `ISSUE-1410` 仍 open。
- Q18(2) 的①②条件均可得夹角余弦 `2/3`；③对所有非退化 P 均成立，不能唯一确定，答案等级为 U，由 `ISSUE-1414` 阻断。其余题目的 D 级记录表示本库独立数学推导，不表示官方答案。
- `ISSUE-1411`–`ISSUE-1413` 缺图问题此前随题图阶段解决；Q10/Q13/Q15 来源异文、Q18 条件歧义及 Q10/Q13 答案映射冲突仍未解决。没有把固定候选或第三方副本认定为官方版本。

## 状态与检查

- provenance 首次导入前 dry-run 通过，manifest revision `6161→6162`；随后因 Q13 答案源的多余数学闭合符号修正并刷新答案摘要，重新导入至 revision `6163`。当前 batch 为 `provenance_verified`；paper 仍为 `blocked`、`blocked_from=planned`；来源仍为 `ready`，不是来源认证或试卷验收。
- 以下确定性/currentness 检查通过：`provenance.py check-batch`（1卷）；`source_manifest.py validate`；`issues.py validate`；`solution_sources.py check-batch`（21题）；`generate_projects.py --check`（1卷）；`manifest_csv.py --check`（775行）。CSV 检查从仓库根目录执行。
- 已更新来源清单 CSV，并登记 `ISSUE-1415`、`ISSUE-1416` 两项阻断性答案冲突。报告投影需在本报告和进度日志落盘后重新渲染并校验。
- 未运行测试套件或 OCR；未生成简答/四版入口，未构建正式 PDF，也没有正式 build/review receipt。本阶段只完成逐题 provenance 登记，不表示候选卷完成或长期语料完成。

## 下一步

继续按工作流生成并核对简答和四版入口，再进行正式构建及逐页视觉复核。来源身份、Q10/Q13/Q15 异文和 Q18 条件③问题仍是阻断项；除非取得有可验证来源链的权威原卷或勘误，否则维持未决标记。

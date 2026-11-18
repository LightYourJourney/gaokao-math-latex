# 2026 北京回忆版候选卷：四版正式构建与视觉复核

- 日期：2026-11-04。
- worktree：`仓库根`；分支：`feat/gaokao-phase0`。
- paper/batch：`gk-2026-regular-beijing-recall` / `phase4-b49`。
- 固定来源：`src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee`；PDF SHA-256 `7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9`。该来源仍是身份未认证的回忆版候选，`official_answer=null`；绑定只标识本库固定字节，不认证正式卷。

## 当前正式构建

- 命令：`python3 tools/build_projects.py build --manifest source-manifest.json --issues missing-issues.md --batch phase4-b49 --formal --json`。
- 当前 attempt：`312cdaea-4916-49de-aedd-0d683c00949f`；开始 `2026-11-04T11:59:05+08:00`，结束 `2026-11-04T11:59:12+08:00`；build 输入绑定 manifest revision `6176`。
- 当前 build receipt SHA-256：`3d963028e7b359a92fa2446a1317fd194c3337bbafeccab9ec07429e7bc1f60d`；review receipt SHA-256：`b78cc1b2f25acc99b4a3eaf97dce5352c378f763e1706461676521789f42e473`。

| 版本 | 结果 | 页数 | PDF SHA-256 | 缺字 | 版面 warning |
|---|---|---:|---|---:|---|
| 试题版 | succeeded | 6 | `0093e62d71a2a28526df8563a1a566413fbbd965dfb3b0f6cf3163129ab4f9f5` | 0 | 0 |
| 解析版 | succeeded | 22 | `1cdacfd46c1770ee4667c9c1092ceeee34b354b435c9fd509e4ecf75d8b185c9` | 0 | 1 Underfull |
| 简答版 | succeeded | 8 | `9911692881a822df4bc289f1a0663f42187047c2223f23c216db142339ffa85b` | 0 | 0 |
| 印刷版 | succeeded | 20 | `326265fa8758fa579b85122afb053f458716db3a394f44f26c27b9890a9243a0` | 0 | 1 Overfull |

四版均无 TeX error、缺字或 undefined reference。解析版第17页的 Underfull `\\hbox`（badness 6842）和印刷版第16页的 Overfull `\\hbox`（15.48851pt）均对应 `answers.tex` 第501–503行；视觉复核确认内容无裁切、遮挡且可读，已在 review receipt 中逐字段记录并通过豁免。

## 视觉审查与批次状态

- 四版全部56页、448项检查完成：408项通过，40项图形标注检查因该页无图而标记 `not_applicable`；未发现视觉问题。最终 attempt 的全部页面渲染均与上一轮已审页面逐字节相同，图形检查已核正：解析版第12页 Q10 与第18页 Q18 含图并通过；其余无图页标为 `not_applicable`。
- 曾用 attempt `6cf10a91-a876-4dd5-b001-068521eb80c8` 的 review 工作项把解析版第12、18页误标为无图。发现后以新 attempt 重新构建、准备四版工作项并通过事务终结器重新封账；旧 attempt 与旧 review receipt 均不作为当前依据。
- `review_receipts.py finalize-batch` 返回 `FINALIZED`，批次状态 `closed_with_blockers`，manifest revision `6178`。当前批次回执见[phase4-b49 批次回执](phase4-b49.md)。
- `validate-receipts --require-final --require-current-inputs` 返回 `OK`；`review_receipts.py check-batch` 返回 `FINALIZED`。source manifest、issues、provenance、21题 solution sources、题面/简答/版本生成检查通过；CSV 与全量报告投影已刷新。

## 未解决事项与边界

- 阻塞问题：`ISSUE-1408`、`ISSUE-1409`、`ISSUE-1410`、`ISSUE-1414`、`ISSUE-1415`、`ISSUE-1416`。分别涉及 Q10 选项异文、Q13 端点异文、Q15 ②③编号异文、Q18 条件③不能唯一确定，以及 Q10/Q13 最终答案映射或端点冲突。没有来源链可验证的正式原卷或勘误前，继续保留 `U/PENDING`，不择版、不补造官方答案。
- Paper `blocked`，batch `closed_with_blockers`。视觉与构建阶段已闭合，不代表来源认证、整卷完成或长期语料完成。
- 未运行测试套件或 OCR。

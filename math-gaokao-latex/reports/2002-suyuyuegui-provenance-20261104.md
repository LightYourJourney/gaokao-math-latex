# 2002 苏豫粤桂卷：Q1–Q22 三角色 provenance 导入

- 日期：2026-11-04；paper `gk-2002-regular-suyuyuegui`；batch `phase4-b50`。
- 固定来源为 source `src-0daae2fa54742835e68d7f3b2cb647b26cee7c4d302f16958e53100e71e4bab4`，PDF SHA-256 `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91`。官方发布身份未认证，固定 PDF 不含答案/评分页，`official_answer=null`。

## 三角色证据

- **question-review**：独立题面复核者依据固定 PDF 可见页逐题核对 Q1–Q22；报告逐题列出核对点与结果。PDF 第 1 页含 Q1–Q19，第 2 页含 Q20–Q22。规范化期间仅改机器可读题号格式、加入已经逐图核对的原图链接，没有更改题干、公式、选项或小问事实；题面摘要由导入器对当前规范题面现场重算。Q10/Q19/Q21 的原题图另外按[题图报告](2002-suyuyuegui-figure-transcription-20261104.md)对照来源复核。
- **answer-solve**：主会话只据固定题面独立推导 Q1–Q22，记录见[答案初稿报告](2002-suyuyuegui-answer-draft-20261104.md)和规范解析正文。固定 PDF 没有答案页，因此 Q1–Q17、Q19–Q22 记为 D 级本库独立推导；Q18 的零公比定义未定，保留两组条件结果并记 U。
- **answer-review**：一名独立复核者不参考首轮盲解表，依据题面独立重算 Q1–Q22；主会话逐题检查复核返回，详见[答案复核报告](2002-suyuyuegui-answer-review-20261104.md)。Q2、Q3、Q10、Q20 的初稿分歧按复算及原页复看结果处理。独立答案复核与当前答案源无未解决的答案冲突；Q18 的定义边界仍由 ISSUE-1417 阻断，而非将条件结论改成确定答案。

题号—源页映射为 Q1–Q19 → PDF 第 1 页、Q20–Q22 → PDF 第 2 页。所有 `question_text_sha256`、`answer_sha256` 与 source SHA 均由 `provenance.py` 按当前规范源和 manifest 现场校验。

## 导入结果与状态

- 三角色记录写在忽略目录 `.work/provenance/phase4-b50/`；首次导入时正式 `provenance.json` SHA-256 为 `63bd83a95aed270e90d475115ca61314148cd5e175b784e6d3a58285188d28ef`。后续只因 Q16/Q17 题面显示公式的序列化调整而刷新相应角色哈希，当前正式文件 SHA-256 为 `458ecfb1e2aaba4dab8d3ab7e7e07e77dc62ce6a04bd7ee6ae2767c55993e662`。
- Q1–Q22 的题面复核均为 `passed`；答案证据为 D 21 题、U 1 题（Q18）；所有 `conflict_status=none`。Q18 的 answer-solve 与 answer-review 记录均关联 `ISSUE-1417`。
- 首次 `import-batch --write` 将 manifest revision `6180→6181`；batch 从 `planned` 到 `provenance_verified`，paper 保持 `blocked`。当前复核时 `provenance.py check-batch` 输出 `OK：1 卷`；`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch` 与 `manifest_csv.py --check` 均通过，后者确认 22 题。项目生成、正式构建及视觉审查后，live manifest 为 revision `6190`，batch `closed_with_blockers`、paper 仍 `blocked`；来源、Q18 blocker 和官方身份边界均未改变。
- provenance 导入后，Q16/Q17 display math 改为单行序列化，并将句号置于 `\text{。}` 内，避免公式后出现孤立标点；可见题意与数学事实不变，相应 question-review 摘要已刷新。两处正文来源说明也改为自然语言“官方答案未认证”，front matter 的 `official_answer: null` 未变。项目生成、正式构建与视觉复核结果见[项目生成报告](2002-suyuyuegui-project-generation-20261104.md)、[正式构建报告](2002-suyuyuegui-formal-build-20261104.md)和[批次视觉审查报告](phase4-b50.md)。
- 全量报告与回执须以 live manifest revision `6190` 重验；revision `6180` 的全库计数只是历史快照，不代表当前门禁状态。未调用 OCR。

## 下一阶段

本卷项目生成、四版构建与 45 页视觉审查现已完成，批次以 `closed_with_blockers` 收口。只有取得可绑定至同版来源的零公比约定证据后，才继续裁定 Q18 / `ISSUE-1417`；证据到位前保留 U/PENDING 与两种条件分支，不将 paper 改标完成。

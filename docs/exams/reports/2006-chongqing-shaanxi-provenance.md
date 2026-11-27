# 2006 重庆、陕西文理候选卷：三角色逐题 provenance

- 日期：2026-11-03；批次：`phase1-b80`；本阶段将 manifest revision 从 `6000` 推进至 `6001`。四卷固定来源 ID、PDF SHA、转录页码及逐题复核记录见 `reports/2006-chongqing-shaanxi-question-review.md`。
- 四卷各导入 Q1–Q22 的 `question-review`、`answer-solve`、`answer-review` 三角色记录，共 88 题、264 条角色记录。正式 `provenance.json` 写入四卷项目目录；三个原始角色工作件保存在 ignored `.work/phase1-b80-provenance/`。question/answer 哈希均由 `provenance.py` 按当前规范题面与答案现场重算，不接受手填值。
- 题面复核角色分别为四位独立只读原页复核者，逐题记录固定 source ID、PDF SHA、PDF 页码和当前题面块哈希。四卷 Q1–Q22 均为 `transcription_review.result=passed`；每卷 22 题的渲染与页码映射详见逐题复核报告。此结果只证明当前候选 PDF 的可见字面对应，未确认发布者、出版者、版次、来源链或官方身份。
- 解题角色以 D 级登记 84 道有确定推导的题，均为依据候选题面形成的非官方答案；重庆理 Q20、陕西文 Q3/Q15、陕西理 Q16 共 4 题登记为 U 级，答案仍是 U/PENDING。固定候选 PDF 只有题面页，没有答案或评分材料，四卷 `official_answer=null`。
- 两名独立盲核者作为一个 cohort role 核验了四卷全部题目和小问。复核前记录过的答案/证明差异均已修订并标为 `conflict_status=resolved`：重庆文 Q17/Q20、重庆理 Q22、陕西文 Q9/Q22、陕西理 Q20 共 6 题；其他题为 `none`。四个 U 项的盲核者一致认可在当前源文下不能唯一作答，故 `conflict_status=none`，阻断由 U 级答案证据与 open issue 表示，并未制造盲核分歧。
- 为匹配 issue/provenance 类型门禁及实际问题性质，本阶段将 `ISSUE-1341` 至 `ISSUE-1344` 的分类统一从答案冲突/转录歧义调整为 `answer-convention-ambiguous`，稳定 issue ID、问题范围、恢复条件与 open/blocking 状态保持不变，按新类型重算 fingerprint。原文转录均准确；未决点在于题面条件、参数或语义不能唯一支持答案，而不是字形无法辨认或盲核答案相互冲突。

## 导入与验证

- `provenance.py import-batch` dry-run 与写入均成功；`provenance.py check-batch --batch phase1-b80` 返回 `OK：4 卷`。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（4 卷各 22 题）通过；导入后运行 `manifest_csv.py --write` 并由 `--check` 确认 775 行且当前；`git diff --check` 通过。
- 派生状态为重庆文科 `answers_verified`，重庆理、陕西文、陕西理三卷 `blocked`；批次 `provenance_verified`。四个既有 blocker 与 U/PENDING 均开放。仍未生成 TeX 项目、正式构建 PDF、建立构建/视觉回执或逐页验收；下一阶段为四卷项目生成与确定性核对。
- 本阶段没有调用 OCR 模型；既有固定 PDF 文字层可读，按 `OCR_WORKFLOW.md` 不重跑 OCR，判断依据仍是逐页渲染原图。成本数据未知。本阶段不表示候选来源已认证、四卷已完成或 1952–2026 长期语料已完成。

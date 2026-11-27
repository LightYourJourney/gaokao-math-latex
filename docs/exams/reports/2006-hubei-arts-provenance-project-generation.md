# 2006 湖北文科：Q16 修正、provenance 与项目生成

- 日期：2026-11-02；paper `gk-2006-regular-hubei-arts`；batch `phase1-b73`。
- 两名独立源页审阅者分段复核 Q1–Q10、Q11–Q21。第二段初审发现 Q16（2）原页第1页（印刷页296）末尾为“取值集”，规范题面多录“合”；主流程对照 200 dpi 原页图后删除该字并重生成含解析稿，原审阅者再次对照确认。该轮其余题面差异未见。Q18 图稿的点名、实/虚线和可见拓扑经第二段审阅者对照通过。
- provenance 输入使用的独立角色为 `phase1-b73-independent-candidate-source-reviewers-q1-10-and-q11-21`、`phase1-b73-independent-blind-solver-cohort-q1-10-and-q11-21`、`phase1-b73-independent-answer-reviewer`。写入的21题记录逐题绑定固定 source ID、source SHA-256 与 PDF 页码：Q1–Q18 → 第1页，Q19–Q21 → 第2页。答案证据为 D 级本库独立推导且非官方；Q12 记 U/PENDING 并关联 `ISSUE-1333`，因题面只给边缘发热概率而未说明五人的联合模型。Q12 的 0.94 只在独立假设下成立，不作为题面确定答案。
- `provenance.py import-batch --write` 写入 manifest revision 5933；batch 派生状态为 `provenance_verified`，paper 仍受 Q12 blocker 阻断。生成 `questions.tex`、`answers.tex`、`answers_short.tex`、`index.json` 及试题版/解析版/简答版/印刷版四个入口。答案要点的答案速查表按生成器约定记录 Q1–Q10 十个单选字母，并与逐题答案行进行第三路比较。
- 验证：`provenance.py check-batch` 为 1 卷 OK；`solution_sources.py check-batch` 为21题通过；`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 均通过；`source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check`（775行）通过。
- 尚未进行本卷正式四版 XeLaTeX 构建、构建收据或页面视觉验收；Q12 blocker 与固定来源身份未认证状态保持。此报告不表示卷级或长期语料库完成。

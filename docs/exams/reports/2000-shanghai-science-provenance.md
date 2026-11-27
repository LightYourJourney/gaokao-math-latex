# 2000 上海理科候选卷：逐题 provenance 导入

- 日期：2026-11-03。固定 source `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`，PDF SHA-256 `b798af61afdac624589769db5bbafe734aa9a0016973bd00b3f5bc8028ab3a40`。Q1–Q19 绑定 PDF 第1页，Q20–Q22 绑定第2页。
- 通过 `provenance.py init-batch` 在 ignored `math-gaokao-latex/.work/phase4-b42/provenance/` 建立三角色文件。题面复核角色为 `/root/2000_shanghai_science_transcription_audit`（Luna/high）：全卷转录与固定 PDF 逐页比对，之后只对改动过的 Q6、Q7、Q12 标点作定向复查；没有声称在标点修订后重新逐字复查全部22题。规范事实源沿用经核题目正文，变化仅包括规范化和图稿链接。
- 两名分段 blind solver 为 `/root/2000_shanghai_science_answer_q1_q12`（Luna/high，Q1–Q12，仅使用题面转录草稿）与 `/root/2000_shanghai_science_answer_q13_q22`（Luna/high，Q13–Q22，使用固定 PDF 与题面草稿）。主会话按盲解报告对照规范答案并复算关键结果；Q18 初算差异（$d^2=6$）更正为 $d^2=16$、体积 $8/3$；Q20 的最快截点为 $(7,0)$、第二指令为 $(5.00,-98.13^\circ)$；Q22 参数轨迹也经代回更正。各项过程见[答案独立盲解复核](2000-shanghai-science-answer-review.md)。

## 逐题证据与未决项

- provenance 当前题面摘要哈希、答案摘要哈希、source ID/SHA 和 PDF 页码均由导入器从规范源现场重算。Q1–Q22 `transcription_review.result=passed` 只表示按固定候选 PDF 忠实转录，不表示来源身份认证，也不解除内容 blocker。
- 22题中 20 题的答案证据为 D 级本库独立推导；Q12、Q21 为 U 级。固定 PDF 不含答案、解析或评分页，所有答案均非官方，`official_answer=null`。
- Q12 原字仍为“等此数列”，数列类型无法判定；答案级别 U、`conflict_status=none`（没有相互矛盾的答案来源），关联 `ISSUE-1369`（转录字面异常）与 `ISSUE-1371`（答案约定不明），均 open / `blocks_completion`。
- Q21 指数按原页保留为2；按字面 `B_n=20^n` 无最大项。答案级别 U、`conflict_status=unresolved`，关联 `ISSUE-1370`（设问与字面推导冲突）与 `ISSUE-1372`（同版答案/约定未核），均 open / `blocks_completion`。

## 导入和校验

- `provenance.py import-batch` dry-run 通过；正式单一 state transaction `ea8a5f52-121e-4985-b334-da4ffabde061` 将22题 provenance 写入本卷 `provenance.json` 并更新 manifest revision `6091→6092`。批次 `phase4-b42` 状态 `provenance_verified`；paper 仍 `blocked`。
- `provenance.py check-batch`：`OK`，1卷；`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）均通过。`manifest_csv.py --write` 更新为775行后，`--check` 确认为 current。

项目 TeX、简答、四版入口尚未生成；正式 PDF 构建、逐页视觉审查及回执尚未开始。Q12/Q21 blocker 继续阻止本卷完成。本阶段不表示来源认证、整卷闭环或长期语料完成。

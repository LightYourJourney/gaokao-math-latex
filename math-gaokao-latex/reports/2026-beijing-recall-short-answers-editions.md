# 2026 北京回忆版候选卷：简答速查与四版入口生成

- 日期：2026-11-04。
- worktree：`仓库根`；分支：`feat/gaokao-phase0`。
- paper/batch：`gk-2026-regular-beijing-recall` / `phase4-b49`。
- 固定来源：`src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee`；PDF SHA-256 `7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9`；Git blob `cf49aa3671ff4143e5c665c7bc53b5f08ab38fca`。来源首页自称回忆版，发布者、版次、复制链和官方身份仍未核，官方答案仍为 null。

## 生成与源层修正

- 由 `answers.tex` 生成 `2026_北京卷_回忆版/answers_short.tex`；由既有模板生成试题版、解析版、简答版和印刷版入口壳。
- 简答速查抽查发现 Q13 答案要点中的第三方严格区间写成 `\([700,4900)\)\)`，重复了一个数学模式闭合符。已在规范 `_答案要点.md` 的答案表和逐题答案正文各删去一个多余的 `\)`，数学区间、U/PENDING 和来源异文判断均未更改。随后刷新 `_含解析.md`、`answers.tex` 与 `answers_short.tex`；四版入口壳无需改动。
- 由于 provenance 的答案摘要基于解析后的标准化答案记录，Q13 的摘要随符号修正改变。将 ignored `.work/phase4-b49/provenance/answer-solve/` 和 `answer-review/` 输入中的 Q13 `answer_sha256` 绑定更新为 `c8b0ef625112c95e4fbf3b191c9895fde379b2480d768e030fc9e156b77e1e11`，不改独立推导、答案等级、冲突状态或证据；dry-run 通过后重新导入，manifest revision `6162→6163`。`provenance.json` 最终 SHA-256：`b46fef9e0dcbbe9aeef8259ad1b1e3ed419bba3f3799b52615178a66515f166b`。

## 当前判定与检查

- 简答速查保留 Q10 `U`、Q13 `U/PENDING` 并列两种端点、Q18(2) `U/PENDING`；Q15 顺序异文说明继续保留。答案仍是编者独立推导，不是官方答案。
- `make_short_answers.py --check`：通过；`make_editions.py --check`：4 个入口壳与模板一致；`generate_projects.py --check`：1 卷一致；`solution_sources.py check-batch`：21题通过；`provenance.py check-batch`：1卷通过；`source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check`（775行）均通过。仓库事务按序执行。
- paper 仍为 `blocked` / `blocked_from=planned`，batch 为 `provenance_verified`。尚未构建四版正式 PDF、未生成 build/review receipt、未进行逐页视觉验收；没有运行测试套件或 OCR。

本阶段完成简答与四版入口生成及 Q13 答案源排版修正，不表示来源认证、候选卷完成或长期语料完成。下一阶段按批次构建和回执流程继续；现存来源与答案 blocker 不作裁定。

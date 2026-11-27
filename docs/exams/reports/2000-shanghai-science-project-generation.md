# 2000 上海理科候选卷：TeX、简答与四版入口生成

- 日期：2026-11-03。按 `phase4-b42` 和 `gk-2000-regular-shanghai-science` 单卷生成项目产物；规范来源仍为固定候选 PDF，答案非官方。
- 简答生成器先后揭示答案源格式的两项不符合项：Q13–Q16 的选择题值原写为带括号的“（C）”等，而选择题摘要要求字母开头；另缺“答案速查表”，无法进行第三路逐题答案核对。参照相邻上海文科答案规范，将逐题答案首字母改为 C/A/A/D，将解释移至括号中，并在答案要点加入由这四个逐题答案汇总的速查表。答案选择与数学含义不变。
- `solution_sources.py extract-batch --write` 刷新 `_含解析.md`；随后速查表本身不参与合并题解，故再运行时判定目标已最新。`generate_projects.py --write` 生成/核对本卷 `questions.tex`、`answers.tex`、总 `index.json`（3个目标）；`make_short_answers.py --write` 生成 `answers_short.tex`；`make_editions.py --write` 生成试题版、解析版、简答版、印刷版4个入口壳。
- Q13–Q16 答案字面规范化后，provenance 答案摘要哈希相应变化。更新忽略区三角色声明后，`provenance.py import-batch --write` 单事务更新 revision `6092→6093`，transaction `64167f83-3b41-4160-a734-a8bba08e964d`；逐题答案证据、等级、冲突状态与 issues 未变。manifest CSV 仍为775行，无需变更。

## 本阶段校验

- `generate_projects.py --check`：1套与生成结果一致。
- `make_short_answers.py --check`：1套简答与答案要点一致。
- `make_editions.py --check`：1套四版入口与模板一致。
- `provenance.py check-batch`、`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`manifest_csv.py --check` 均通过；CSV current、775行。生成器涉及仓库全局事务锁，currentness 检查顺序执行。

paper 仍 `blocked`，batch 仍 `provenance_verified`；Q12/Q21 的四条 blocker 继续 open / `blocks_completion`，答案 U/PENDING，`official_answer=null`。正式 PDF 构建、四版逐页视觉检查及回执尚未开始；本阶段不表示整卷完成或长期语料完成。

# 1989 广东文科候选卷：项目 TeX 装配

日期：2026-10-30

## 答案索引与生成

- `make_short_answers.py` 首次拒绝生成：规范答案稿只有固定扫描答案表，没有与逐题项目答案对应的速查行，第三路交叉核对无法执行。沿用仓库已有简答版约定，在答案要点中新增独立的“项目独立答案速查表”；按逐题答案自动折算25项，其中Q9、Q16、Q21均为`U`。扫描所载答案表仍单独保留，未用扫描字母覆盖未决项目答案。
- `generate_projects.py --write` 为本批生成 `index.json`、`questions.tex`、`answers.tex`；`make_short_answers.py --write` 生成 `answers_short.tex`；`make_editions.py --write` 生成试题版、解析版、简答版、印刷版四个 TeX 壳。
- 三个生成器的`--check`均通过；`solution_sources check-batch`、`provenance check-batch`、source manifest validate 与 issues validate 通过。来源校对 sidecar 已更新规范答案稿哈希。未改变 manifest revision（仍为5474），逐题答案内容及provenance绑定未变。

## 保留的状态

批次`phase1-b59`仍为`provenance_verified`，paper仍为`blocked`；Q9答案冲突、Q16定义边界、Q21选项不匹配及相应答案待核问题仍开放。固定PDF身份未认证，`official_answer=null`。Q29（2）的固定扫描未见最终解集，Q30解答未见于扫描页8—9。

本阶段只装配TeX输入，尚未运行XeLaTeX、生成四版PDF或建立build/review receipts；未运行测试套件。后续构建若因阻断继续，必须如实保留`closed_with_blockers`，不得标为完整。

# 1999 广东卷 paper 登记与确定性项目生成（phase1-b72）

## 登记结果

- Paper：`gk-1999-regular-guangdong`；项目目录：`1999_广东卷`；固定 source：`src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019`。
- Manifest revision `5898→5899`。source 反向绑定为 `canonical`，paper 与 batch `phase1-b72` 登记成功。题面卷种原件未标文理，paper track 记为 `none` / index track“原卷未标注”。固定副本包含 13 页，题面物理页 1–6、答案/解析材料物理页 6–13。
- 登记同时建立六条 open / `blocks_completion` 问题：Q10 题面歧义与答案未决，Q13 F/F1 及重复语句与条件答案，Q21 函数记号/列式异常及条件答案。编号为 `ISSUE-1323`–`ISSUE-1328`。paper 状态为 `blocked`（`blocked_from=planned`），batch 保持 `planned`。
- 官方性边界：候选固定副本的来源身份、出版者/版次和复制链未认证；印刷答案栏只是扫描件内“A 型卷答案”。B 型答案与 A/B 卷对应关系未核；`official_answer` 保持 `null`。

## 生成与门禁

- 更新三份规范 Markdown 的 `paper_id`，并由 `solution_sources.render_combined` 生成 `_含解析.md`。
- `generate_projects.py --write` 生成 `questions.tex`、`answers.tex` 与 index 投影；`make_short_answers.py --write` 生成 `answers_short.tex`；`make_editions.py --write` 生成试题版、解析版、简答版、印刷版四个独立入口。
- 五幅图登记在 manifest，题面与含解析稿各引用一次。选择题 Q10 的 U/PENDING 进入简答表；Q16 两个可成立命题均纳入简答；Q21 条件答案中包含分段式和定义域。
- 当前成功验证：`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --batch phase1-b72`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`。三个 Markdown 源解析器及合成稿均识别 22 题。
- 期间发现并修复两个输入兼容问题：选择题待核答案须写成 parser 支持的 `U/PENDING`；Q16 最终结论须包含在答案块内，避免简答版只提取到“可写出两种命题”的引导语。修复后写入与 `--check` 全部通过。

## 未完成门禁

尚未导入逐题 question-review / answer-solve / answer-review provenance，未正式构建四版 PDF，未检查全页视觉、字体及版面，也未生成 build/review receipt。六条来源歧义问题继续阻塞卷级完成；本登记和生成阶段不认证来源/官方答案，也不表示卷件验收或长期题库完成。

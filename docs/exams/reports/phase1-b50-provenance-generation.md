# phase1-b50：2017 上海普通卷逐题 provenance 与确定性生成

日期：2026-10-28

## Provenance

- 批次：`phase1-b50`；试卷：`gk-2017-regular-shanghai`；固定 source：`src-213fecea206481434c7eb8f292fa39ffff3d28572e6080db2429c327529b2bac`。
- 以 `provenance.py import-batch` 三角色事务导入 21 题。题面复核页映射为 Q1–Q18 → PDF 第1页、Q19–Q21 → PDF 第2页。question/answer 哈希由工具从当前规范源现场计算；原卷题号为 1–21。
- 题面记录引用 `reports/2017-shanghai-regular-transcription.md` 的固定 PDF 逐页和放大核对记录；报告没有记录校对者姓名，也未证明校对为独立盲核。
- 答案证据均为 D 级项目推导。固定 PDF 只有题面页，无答案、解析或评分；所有答案非官方，`official_answer=null`。答案记录引用 `reports/2017-shanghai-regular-answer-analysis.md`；答案要点 frontmatter 明确标记 `solution_status: draft-independently-reviewed`，阶段报告记录逐题复算并更正 Q19 首算错误。来源记录没有复核者姓名或详细方法，也没有盲核记录；provenance 保留“来源记录称已独立复核”，不补写人员身份或将其说成独立盲核。
- provenance 的 reviewer role 字段记录答案稿来源标注的独立复核、以及复核者身份与方法未记录；conflict 状态为 none（现存报告中的 Q19 错误已有更正记录，未报告仍未解决的答案冲突）。

## 确定性生成

- 既有 `questions.tex`、`answers.tex`、兼容 `index.json` 经 `generate_projects.py --check` 确认当前，无需改写。
- 首次 `make_short_answers.py --write` 报告 Q13–Q16 的速查值与逐题答案行不一致。根因是答案要点把填空速查表放在选择题速查表之前，而提取器把所有 `| 答案` 行的单元格合并后取前四格。将填空表行名改为 `填空答案` 后，答案数据不变，提取器只读选择题 `答案` 行；同时重算 `来源校对.json` 中直接绑定答案要点原始字节的 SHA-256。
- `solution_sources extract-batch` 确认含解析稿已是当前结果；随后简答版成功生成，四版入口成功生成。
- 新增项目文件：`provenance.json`、`answers_short.tex`、`试题版.tex`、`解析版.tex`、`简答版.tex`、`印刷版.tex`。规范答案表格行名变更后，`canonical_answer_sha256` 为 `8954c9e577ac60ecb4bb1c5810b32e6f0387d9f83f5fc863fac2de80ad952860`。

## 验证与边界

通过：`source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`provenance.py check-batch --batch phase1-b50`、`solution_sources.py check-batch --batch phase1-b50`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`git diff --check`。正式当前状态来自 manifest revision `5279`：paper `editions_generated`，batch `provenance_verified`。

尚未正式构建四版 PDF，未生成 build/review 回执，未逐页目视检查。来源发布者、出版物、版次、原始来源链及官方身份仍未核。未运行测试套件；模型 Token、费用与工时不可见，记未知。

下一步：正式构建试题版、解析版、简答版、印刷版 PDF，记录构建与工具链身份，渲染并逐页完成八项视觉检查后再收尾批次。该阶段不代表该卷验收完成，也不代表 1952–2026 长期语料库完成。

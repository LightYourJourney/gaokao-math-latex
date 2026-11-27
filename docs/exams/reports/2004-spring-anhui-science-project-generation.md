# 2004 春季安徽理科卷：项目产物生成与阶段状态对齐

日期：2026-10-27

## 阶段结果

- `generate_projects.py --paper gk-2004-spring-anhui-science --write` 生成共享 `questions.tex`、`answers.tex` 并更新全局 `index.json`；`make_short_answers.py --write` 生成简答源；`make_editions.py --write` 生成试题、解析、简答、印刷四版入口。
- 生成后以 `provenance.py import-batch --write` 的官方 state transaction 重算并写入逐题 provenance 与 manifest，revision `5211 → 5212`。paper 当前为 `editions_generated`，batch 仍为 `provenance_verified`；没有手工编辑状态字段。
- 全局 index 纳入新卷后，既有 build 回执 currentness 恢复：全库 333 卷中 326 份成功、6 份待处理、0 stale；唯一缺少 build 回执的是本阶段尚未正式构建的 2004 安徽理科卷。
- 报告生成器以 content transaction 刷新并回读校验六个全量报告目标。

## 验证记录

- `generate_projects.py --check`：1 套试卷与生成结果一致。
- `make_short_answers.py --check`：1 套简答与生成结果一致。
- `make_editions.py --check`：1 套四版壳与模板渲染一致。
- `provenance.py check-batch`：1 卷 OK；`solution_sources.py check-batch`：22 题全部通过。
- `source_manifest.py validate` 成功；`report.py check --all` 报告投影与当前 manifest 一致，未完成状态保留。
- `build_projects.py validate-receipts --all --require-current-inputs --json` 返回 INVALID，精确原因只有当前卷缺 build 回执：326 succeeded、6 pending、1 missing、0 stale。
- `review_receipts.py check-all` 返回 `INVALID_OR_STALE：192 批次`。输出包含历史未关闭/视觉失败批次，以及当前卷缺 build 回执；本阶段未重写或重审这些其他批次。

## 边界与下一步

- 本阶段没有运行测试套件、正式 XeLaTeX 构建或视觉检查；四版入口生成不等于 PDF 交付或视觉验收。
- 来源 PDF SHA-256 `51038ba6ecdfbb8c5c7edc417f871eda5a5a5c03cc5af510da08131ec0dbb151`；来源出版者、版次及原始来源链仍未知，`official_answer=null`。答案是 D 级独立推导，不能表述为官方答案。
- 下一阶段为正式构建本卷四版 PDF，随后对所有页面进行视觉审查并生成有效回执；历史回执全库检查中的既存问题继续按其原记录处理。

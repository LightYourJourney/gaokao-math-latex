# 2004 春季安徽理科卷：四版正式构建

日期：2026-10-27

## 构建结果

- 首次正式构建 attempt `94c39d0f-32f2-4c5e-ae07-fc918deba873` 四版均在 `questions.tex` 第 10 行失败。XeLaTeX 将正文裸写的 `official_answer` 中 `_` 解释为数学下标并报 `Missing $ inserted`。同一源行被四版共享，故四版出现相同根因。
- 仅修订题面与解析正文中的说明语句为“官方答案字段保持为空（null）”，不改数学题意、答案或来源身份；经 `solution_sources.py extract-batch --write`、`generate_projects.py --write` 刷新确定性派生稿。
- 第二次正式构建 attempt `3f3fe168-903c-4008-8086-4347ee96c501` 成功，paper 状态 `compiled_pending_review`，manifest revision `5215`，构建输入树 SHA-256 `9126632c8da0076eb063ec2001af80cd87677be69c24aac58e86d8110c67f18d`。

## 四版产物

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 4 | `90b7bb536b420db6bebfa258a63008847520e72b67b6b7565cf60e1c389f3ce2` |
| 解析版 | 17 | `764b951ecc6572ed3c098a78c4f1499c945913252b649f4badedb73f65f054fc` |
| 简答版 | 6 | `9428a8eb181f142f9eae148272d6f99e9f58d627c035bd3b72c1cfaad1106a58` |
| 印刷版 | 11 | `58f993bc6f52b7758e348afa5cf71268ff7201b88dea5fe536e329126cd8cdbb` |

四版共 38 页。最终回执四版均 `succeeded`、每版 latexmk 退出码 0；错误、缺字、overfull、未解析引用和构建 problems 均为空。首次失败登记的 `ISSUE-1207` 至 `ISSUE-1210` 均由后续成功构建解决。

## 验证与边界

- `build_projects.py validate-receipts --paper gk-2004-spring-anhui-science --require-current-inputs --json`：OK，0 invalid/missing/stale，1 pending review。
- `source_manifest.py validate`、`provenance.py check-batch`、`solution_sources.py check-batch`、三个项目生成器 `--check` 均通过。
- 本阶段未运行测试套件或视觉检查。PDF 构建通过不等于页面视觉验收；下一阶段需对四版全部 38 页逐页检查并生成视觉回执。
- 来源出版者、版次、原始来源链继续未知，`official_answer=null`；答案为 D 级独立推导。

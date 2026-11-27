# phase1-b58：2005 春季北京文/理卷共享 TeX 与正式构建

日期：2026-10-30

工作树：`仓库根`

分支：工作分支

## 当前阶段

文科、理科两卷的共享题面与解析 TeX、简答源及四版入口已由仓库生成器产出。最终正式 XeLaTeX 构建成功，8 份 PDF 共 95 页。当前 manifest revision `5454`，两卷 paper 状态为 `compiled`，批次 `phase1-b58` 为 `compiled_pending_review`。

本报告只记录正式构建，不代表逐页视觉验收或本批关闭。

## 生成与修正

- `generate_projects.py --batch phase1-b58 --write` 生成两卷 `questions.tex`、`answers.tex` 与项目索引；`make_short_answers.py` 生成两份 `answers_short.tex`；`make_editions.py` 生成两卷试题版、解析版、简答版和印刷版入口。
- 简答生成器要求答案要点内有选择题速查表，以便与逐题答案块作第三路交叉核对。两份答案要点各补一张 Q1–Q8 表，答案为 `D, A, C, A, B, C, B, A`；这与逐题答案、解析及既有盲核一致，未改答案内容或 official answer 状态。
- 理科题面图形说明最初直接显示清单文件名中的 `_`，转换器将其作为普通文字写入 `questions.tex`，导致四版在同一行报 `Missing $ inserted`。源 Markdown 改为“图表清单”链接显示标签后重生成，问题定位在源文格式而非题目内容。首轮四个正式编译错误登记为 ISSUE-1255–1258，均已在后续成功构建中解决并标为 `resolved/non_blocking`。

## 最终 build attempt

输入 manifest revision：`5453`。首轮失败/前序 attempt 由当前 build receipt 的 `previous_attempt_id` 关联；以下为最终 attempt。

| 卷别 | Attempt ID | 试题版 | 解析版 | 简答版 | 印刷版 |
|---|---|---|---|---|---|
| 文科 | `534500d2-d387-4022-9580-975fccd07596` | 5 页 · `7d3eef855124a130077ca9835bc9cb3ce88387ba1b04e6142e52a139027f67a8` | 20 页 · `9da14a3192a0db5559ff1572ae7cf141c803dda293e65fbf2e7f0c1a4f0c896a` | 7 页 · `5c2fc03843e210f5aa78ea8803ccf8b50456fb43020a31085439180a04ed64d3` | 15 页 · `14ea302ea37d78d690acb94f9590c71ad96cb1aaf3f891310421b2f1c4febbac` |
| 理科 | `cf7c2253-6447-49c0-8da3-f08ad0d30515` | 5 页 · `6fb49d5e46984702229b11d9912f3601bbb8edff2cc6e62798e325480fe0886d` | 20 页 · `e107c09bc87e3f72a8740ae18520ba1e4f16261effcd6c4dcebc5155239d791b` | 7 页 · `9bab615acb9be927167a917e5991dd9b17f2aa040cf30013c89230ad78af7cb5` | 16 页 · `ad22969a3b41fc75cdfb39144413060863f92a2eb27462912b95f951cba0431d` |

最终构建日志中错误、缺字、未解析引用与 Overfull 项均为 0。PDF 共95页。

## 已执行验证与未完成项

- 三个生成器的 `--check` 均通过；`source_manifest.py validate` 通过。
- `solution_sources.py check-batch` 两卷各20题通过；`provenance.py check-batch` 返回 `OK：2 卷`。
- `build_projects.py validate-receipts --require-current-inputs` 返回 `OK：2 卷`。
- 未运行测试套件。尚未建立视觉 review receipt，95页尚未逐页查看；不能把 PDF 编译通过等同为排版合格。
- 固定 source 仅绑定本库采用的字节；发布者、版次与来源链未知。PDF 仅有题面，答案仍为 D 级项目推导，`official_answer: null`。
- 下一步使用 `.work/phase1-b58/review`，核查最终 attempts 的全部 PDF 页面并写入视觉检查记录，再执行 batch finalize。未关闭本批，也不代表长期语料库完成。

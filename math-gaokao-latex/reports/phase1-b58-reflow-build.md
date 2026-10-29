# phase1-b58：视觉问题修正与正式重编

日期：2026-10-30

工作树：`仓库根`

分支：`feat/gaokao-phase0`

## 修正范围

- 首轮 PDF 校样发现理科题面源中的 17 个字面 `<br>` 被逐字印出。对照固定原卷 PDF 第 1–2 页后，将 12 个小问/命题位置的标签改成 TeX 断行；5 个选择项组位置移除标签，由题项网格负责排版。题干、数学符号、选项与问句内容未改，综合版 Markdown 和 TeX 均由确定性工具同步。
- 文科 Q20 仅有（1）–（3），与理科版多出的（4）不同。将文科逐项分类的不等式证明改为对 `1≤n≤4` 统一成立的短证明；不改题目范围、答案或 D 级结论。文科解析版从20页回流到19页，原末页仅剩一条 `n=4` 不等式与三个答案框的问题消失。
- provenance 工作记录更新理科 Q3–8、Q15–20 共12题的规范题面哈希及源页复核说明。仅覆盖格式变更涉及的题号；其他题的逐题来源记录未改。

## 当前正式构建

provenance 写入后 manifest revision 为 `5455`。以下构建以 revision `5456` 为输入，正式回执完成后当前 manifest 为 `5457`。两卷状态均为 `compiled_pending_review`。

| 卷别 | Attempt ID | 试题版 | 解析版 | 简答版 | 印刷版 |
|---|---|---|---|---|---|
| 文科 | `193e94e8-824d-4f89-9c2f-74f512e6b115` | 5页 · `a82fc378e81e4a11a709944c2d847f5b6b9368661c5d12f378c13bfc5808d236` | 19页 · `4899e6cc5101beb78575f78b5482d7f4bf86979d40d3195e4d157de981c99aab` | 7页 · `303a53f6c44aba2ce403f118cb966eb62dc6f38556e1df3a280597108fc3a476` | 15页 · `0980e72a76b91ca379e5003a23b50c728beb07fcae20119cd3d40f771ddf344c` |
| 理科 | `b9499a8d-8b63-4ece-bd64-bef760b25e78` | 5页 · `8f63326f276afd10eafa58f5a11619afacff1907d2c15f60a60e7f8e54dba2b9` | 20页 · `24c0fa61c6641b287730ac669b9e31269e4d75d6cb24040f80a83371bc47d8c5` | 7页 · `930cdfbfb36961d7e1684438f007a96d53c86f35e56c1c44ffa990ec788b8339` | 17页 · `ea574a63c8cdd6f8e3d9f912c587992252af1e57dc9a5842a07ed99cff2c9727` |

8份 PDF 共95页；所有构建日志的错误、缺字、未解析引用、Overfull 项均为0。新 attempt 分别由文科 `534500d2-d387-4022-9580-975fccd07596`、理科 `cf7c2253-6447-49c0-8da3-f08ad0d30515` 重建。

## 验证与后续

- `solution_sources.py check-batch`：两卷各20题通过；`provenance.py check-batch`：`OK：2 卷`；来源清单验证通过。
- `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 全部通过；`build_projects.py validate-receipts --require-current-inputs`：`OK：2 卷`。
- 未运行测试套件。当前构建尚未完成 PDF 页视觉复核，未生成最终视觉回执；两卷不能标为 `complete`。下一步比较并复核这8份最新 PDF 的逐页图像后完成视觉阶段。
- 固定来源只绑定本库采用的字节，不认证发布者、版次或来源链；原卷不含答案页，答案仍为 D 级项目推导，`official_answer=null`。本批工作不表示长期语料库完成。

# phase1-b58：视觉问题修正与正式重编

日期：2026-10-30

工作树：`仓库根`

分支：工作分支

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


## Q20（4）重复尾式回流与正式重编（2026-10-30）

- 首轮逐页检查发现理科印刷版第17页只剩 Q20（3）、（4）答案框，属于本次换行回流产生的孤页。理科解析源的面积推导已得到分母为 $5T$ 的表达式，后续展开 $T=a_1+\cdots+a_5$ 与答案框重复；删去重复展示，保留完整推导，规范答案和题目内容不变。含解析稿与 `answers.tex` 已按确定性工具同步。
- 新正式 build attempt：文科 `69f4326e-64de-40bb-9b2a-588accf02649`，理科 `4b0dff21-7f61-4aba-94ad-54c046263f6d`；两者以 manifest revision `5458` 为输入，当前 revision `5459`。文科页数仍为 5/19/7/15（46页）；理科为 5/20/7/16（48页），合计94页。理科印刷版由17页回流到16页，孤页已并回末页；需以本次实际逐页审查确认视觉结果。
- 8份构建日志的错误、缺字、未解析引用与 Overfull 均为0。`source_manifest validate`、`solution_sources check-batch`、`provenance check-batch`、`generate_projects --check`、`make_short_answers --check`、`make_editions --check` 及 `validate-receipts --require-current-inputs` 均通过。未运行测试。
- 最新构建仍为 `compiled_pending_review`；本批94页的最终视觉回执尚未完成，不能标为完成。旧版中逐页实看且 PNG SHA 完全相同的页面才可继承既有结论；理科印刷版新末页及其他未审页面需实看。

## Q18 解析标题分页修正与最新正式重编（2026-10-30）

- 文科解析版第16页原先在 Q18 题干和图后仅余“解析”标题。规范解析源增加 `\Needspace{8\baselineskip}`，含解析稿与 `answers.tex` 由确定性生成器同步；最新解析版第16页保留题目与图，第17页从“解析”标题和完整解答开始。数学内容未改。
- 最新 attempt：文科 `2fcce5e3-2d52-49e5-9e00-8d0f362d1a1e`、理科 `ff3c1b03-8924-4d7f-bd78-c92712772754`，build 输入 manifest revision `5460`（review finalize 后当前 `5462`）。页数文科 5/19/7/15，理科 5/20/7/16，共94页。文科四版 PDF SHA-256：试题 `eb75013ac9e929d175385e401497f94e0f4ab302252c808d092208b5824bbe56`、解析 `a3c52dff0dda49e7fa0c4821ed225150e91052c162f025346b5b5bed5c852b6e`、简答 `7efaec4327a9be213d10d6b6c3887e02ceeb23f871a89288d27cead15e80005e`、印刷 `7eab5442a02c5f9ed89b89b236001b8c513780f470bdb467a6e04022ba529cc7`；理科：试题 `3b4d170899b9355d7b5dbdf80e8b508878594af1bfac705a9c01800194b6bf31`、解析 `1c5030d570cf5558602691f161b5ecc830d1ab116dbec5b3dcba8e9fe4e96d77`、简答 `6cf55caed868e317e4d1273d2f812fec1699c7cf1855256c4251c6df1576be27`、印刷 `b97af5efee4abdef9b0e1ecdcaa605ee3836a9671a1b7ea9512f7fa04478fefa`。
- 与已检查的 build-5458 逐页栅格 SHA 比较，94页中91页完全相同；变化仅文科解析版第16、17页和印刷版第13页，三页在 build-5460 全页图上实看。最终94页八项视觉核查共752项：701 pass、51 not_applicable、0 fail；两卷 review receipt 均绑定当前 build attempt、PDF SHA 和工具链。`review_receipts check-batch` 及 `build_projects validate-receipts --require-final --require-current-inputs` 均通过。
- `phase1-b58` finalize 结果为 `closed`，manifest revision `5462`，文/理两卷 production state 均 `complete`；正式总结见 `reports/phase1-b58.md`。两卷的固定题面发布者、版次和来源链仍未知，来源 PDF 没有答案页，答案/解析为D级项目独立推导且 `official_answer=null`。未运行测试；这只表示本批两套卷在本库内部生产流程收口，不表示1952–2026语料库完成。

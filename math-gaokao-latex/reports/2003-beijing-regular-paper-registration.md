# 2003 北京普通文理候选卷：规范事实源与内部卷登记

- 日期：2026-11-04；工作树 `仓库根`；分支 `feat/gaokao-phase0`。
- 本报告记录规范题面、答案/解析事实源与 `phase4-b48` 内部登记，不认证来源身份或官方答案。

## 固定来源与题面边界

- 文科 source `src-dcc6a2c21c7b8e7b8f23f5188f34d7f542f94e40f4219b54cfb85a0d7004bc0f`，PDF SHA-256 `7fc0fd289fc486a0ae1c16a9ab5b4f0561830897df6e8897c50666f03d511913`，Git blob `098d2daa4a08a3ef69b98b656842324f4819ece6`；固定两页题面，印刷页126–127，可见 Q1–Q20。
- 理科 source `src-120ea104f8cb373f5731039fa9d36469df457869849f27420831962ef1ad2306`，PDF SHA-256 `d0081500bd56d03199ddcf232fe8e870f2ecd7e9c41ba849417af9af79fbb702`，Git blob `1f3cde756f4b417da80d0bb4b7cf2501e1ffad37`；固定两页题面，印刷页124–125，可见 Q1–Q20。
- 两份固定 PDF 均无答案或解析页。发布者、出版者、版次、复制/扫描链和官方身份未认证；两卷 `official_answer=null`，答案与解析是本库独立推导。

## 规范源与派生稿指纹

Q1–Q20 题面由已复核草稿规范化。答案与解析保持上游已复核内容；只把 `paper_id` 绑定到登记卷，并由 `extract-batch --write` 补齐解析块标记。`_含解析.md` 由三份规范源确定性生成。

| 文件 | SHA-256 |
|---|---|
| 文科 `_试题.md` | `d3f322321d096520e5f0eabddfefe42ba2eabbffc508d72d566050133ac8b17b` |
| 文科 `_答案要点.md` | `ba2eb09ff74acc97b885246234779afd5272fb7cdd5c36557f9dee24d5cc2b07` |
| 文科 `_解析正文.md` | `83862d86c874566059857de879113fe34570f5399d679ce073afa176abef080c` |
| 文科 `_含解析.md` | `637f61cc8d84b4c136c0de6bd0cea8b77834dbab90245c87eeb9ecb2f135ec6b` |
| 理科 `_试题.md` | `2d2b571f9a7f57df773927bc259c6806029542053d35d6356e8515c81123d376` |
| 理科 `_答案要点.md` | `c40a648dacbe231d1bbd292cf9ef73cc0c124ae2e73ba4407b6acc0c09368655` |
| 理科 `_解析正文.md` | `c16df257c7af7676d26e587c33969a39175ac78b8d7b9d17d58eb4806e601bf2` |
| 理科 `_含解析.md` | `f3d759dcfe94e33cea4b44400bfbef0dc6a68fc0224b7a015c5e5369460321b8` |

## 登记与 blockers

- `source_manifest.py register-papers` dry-run 通过；单一状态事务建立 batch `phase4-b48`、两套 paper，并将两个候选 source 绑定为 `canonical`。登记事务 `64dcd398-3bfb-4f1b-a521-ade459556c4f` 将 manifest revision 从 `6146` 推进到 `6147`；随后按原页更正 ISSUE-1400 的证据引文，事务 `07dc5eb5-d429-43ec-925a-40df590146cd` 将 revision 推进到 `6148`。
- 文科 `gk-2003-regular-beijing-arts`：`ISSUE-1398`（Q18 `transcription-ambiguous`，固定原页题干/图示顶点字母冲突）与 `ISSUE-1399`（Q18 `answer-convention-ambiguous`，几何构造端点无法由题面唯一确定）。
- 理科 `gk-2003-regular-beijing-science`：`ISSUE-1400`（Q17 `transcription-ambiguous`，原页可见“底面边长的 3”，没有“为”）与 `ISSUE-1401`（Q17 `answer-convention-ambiguous`，底面边长未定）。四项均为 `open / blocks_completion`；paper 为 `blocked`，batch 仍为 `planned`。
- 文科 Q18 与理科 Q17 均忠实保留源字并标 U/PENDING；条件性推导没有提升为确定答案。其余文科 Q1–Q20、理科 Q1–Q20 的答案复核结果按前序报告保留。

## 登记后检查与下一步

- `solution_sources.py extract-batch --write` 为本批提交4个规范/派生目标；`check-batch` 通过，两卷各识别20题，答案块和解析小问锚点对齐。
- `source_manifest.py validate`、`issues.py validate` 均以退出码0完成；`manifest.csv` 写入并检查为当前投影，共775行。全量报告投影 currentness 检查通过，结果为“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”。
- 尚未登记题图、导入逐题 provenance、生成 TeX/四版入口、正式构建或视觉审查。下一阶段按固定 PDF 重绘题图，并将 Markdown、manifest 图登记、生成器映射与 provenance 同步更新。

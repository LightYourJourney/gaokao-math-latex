# 2006 湖南理科候选卷：paper/source 登记与 Q17 blocker

- 日期：2026-11-02；batch：`phase1-b75`；paper：`gk-2006-regular-hunan-science`。
- 固定候选 source：`src-74bd6a8b302120c812e3aa287309cf3d3a0cf6217761cc4637696bf4d12817cb`；SHA-256 `ae341d81af084449fe66f2f737553001cf04fd1781ad5f47f1a4f5b5da1bbb09`；Git blob `0e7fdec5b934366efe430a192955195c9a82bad4`。
- `source_manifest.py register-papers` 将该 source 在 manifest 内绑定为 canonical，并创建 paper 与 batch；revision `5951→5952`。canonical 仅表示本库固定输入关系，题签、文件指纹与页数不认证发布者、版次、来源链或官方身份。`official_answer` 保持 `null`。

## Q17（3）待核项

- 建立 `ISSUE-1339`，类型 `answer-convention-ambiguous`，状态 `open`，影响 `blocks_completion`。原题给出初检/整改后复查的边际合格概率，并称“每家煤矿安检是否合格是相互独立的”，但没有明确不同煤矿复查结果与初检、复查之间的联合独立范围。
- 在各矿最终关闭事件独立的额外假设下，至少关闭一家为 $1-0.9^5=0.40951\ldots\approx0.41$；规范答案要点保留 `U/PENDING`，不把该条件值伪装成题面唯一确定答案。
- paper 状态为 `blocked`、`blocked_from=planned`；batch `phase1-b75` 保持 `planned`。

## 当前边界与验证

- 题面、独立答案要点、解析正文与确定性生成的含解析 Markdown 均关联此 paper ID；源文件 `official_answer` 均为 `null`。候选来源身份仍未核实。
- `generate_projects.py` 已为新卷生成 `questions.tex`、`answers.tex`，并更新全库静态 `index.json`；`make_short_answers.py` 已生成 `answers_short.tex`，`make_editions.py` 已生成试题/解析/简答/印刷四个入口壳文件。以上只是确定性源装配，未进行 XeLaTeX 构建。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --batch phase1-b75` 均通过；解析器识别题面、解析、答案各 21 题，编号连续 1–21。
- Q9、Q15、Q16、Q18 原图尚未矢量重绘或登记；逐题 provenance、四版 XeLaTeX 构建及逐页视觉审查尚未完成。此登记不表示来源认证或卷级验收。

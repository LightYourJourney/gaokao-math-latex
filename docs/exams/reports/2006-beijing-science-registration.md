# 2006 北京理科候选卷：登记、题面复核与答案交叉复算

日期：2026-10-30

## 固定输入与内部登记

- `paper_id`：`gk-2006-regular-beijing-science`；批次：`phase1-b61`；题量20；`track=science`；项目目录：`2006_北京卷_理科`。
- 固定候选 source：`src-49f52e7c83c2b20d33f62d6dbc57b1610f96cf9de81c5743d41612834cb318de`，路径 `普通高考/2006/2006北京理.pdf`，SHA-256 `878cd3b020d41450cb9876ad9263ec384840bb4c00597e720069a12f89d2016c`，Git blob `4368ce3dfefce75019107dde3a836a975dc19c6c`。`pdfinfo` 确认为2页A3横向，题面在 PDF 第1—2页、印刷页280—281。
- 注册 dry-run 返回 `OK`；事务 `22dc3a72-e04e-4d49-93d2-de9854700b63` 将 paper/batch 写入 revision `5491`。source 双向绑定为 `paper_relation=canonical`；其含义仅为本库选定固定字节输入，不证明发布者、版次、来源链或官方身份。描述元数据后经事务 `40da0027-045a-4a9a-b582-20dcdfef65e5` 更新至 revision `5492`。paper 与 batch 保持 `planned`。

## 题面复核与订正

- 另一复核者将 PDF 与题面稿逐页比对，发现唯一内容差异是 Q18（1）漏“时”；题面已订正为“用方案一和方案二时考试通过的概率”。Q1—Q17、Q19—Q20 的题干、公式、选项和小问未发现其他差异。半角/全角题号、选项括号差异为格式统一，题号、内容、顺序不变。
- 复核者先前读过进度摘要中的 Q8、Q17 答案结论，但没有打开本卷题面、答案或解析稿；本轮比较的目标是题面字节/图位对应。视觉渲染与局部图像检查详见 `2006-beijing-science-transcription-review.md`。

## 答案交叉复算

- 第二解题者没有查看本卷答案/解析文件后作答，独立复算全部20题，结论与答案草稿一致。其此前读过进度摘要中的 Q8、Q17 答案结论，因此仅将这两题标为非盲复核。关键答案与数学检查点见 `2006-beijing-science-answer-review.md`。
- 固定 PDF 未见答案、解析或评分页；所有答案仍属本库非官方推导，`official_answer=null`。来源身份不确定性继续保留。

## 确定性装配与校验

- Q15—Q20 小问标号按原页间隔补入解析器要求的分隔空格，解析正文小问改为规范 `#### (k)` 锚点。含解析 Markdown 按三份规范源重生成，当前16,419 bytes；共享 `questions.tex`、`answers.tex`、`answers_short.tex` 与试题版、解析版、简答版、印刷版四个入口已生成。
- `solution_sources.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 均通过；source manifest 775项、missing issues、schema 校验通过。CSV 775行；六个全库报告投影刷新并经 `report.py check --all` 确认当前一致。
- 全局登记投影为357卷、215批；状态 `complete=279`、`blocked=74`、`compiled=3`、`planned=1`。计数不意味着其余来源已绑定或题库长期目标完成。

## 阶段边界

Q8/Q16/Q17 仍待矢量重绘；尚无逐题 provenance、正式四版构建、build/review receipt 或视觉排版验收；本阶段未运行测试。固定候选 PDF 身份未认证，题目答案非官方。本阶段只完成内部绑定、题面纠正/复核、答案交叉复算和确定性 Markdown/TeX 装配，不表示本卷或1952—2026题库完成。

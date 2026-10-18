# 批次 phase1-b24 视觉审查诊断

- 当前结论：`VISUAL_FAILED`
- 批次闭环：未完成；本诊断不得作为 `closed` 或 `closed_with_blockers` 报告
- 试卷数：1
- 审查页数：45
- 失败检查数：17

## gk-1994-shanghai

- 标题：1994 年·上海卷·数学
- 项目目录：`1994_上海卷`
- 构建状态：`compiled_pending_review`；attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`
- 复核状态：`failed`；时间 2026-10-18T18:46:35+08:00
- 试题版：5 页；PDF SHA-256 `ccab37f4975d751ab09d5d71309c2c0a070662c771851d82b18ba3f7f6023d6b`
- 解析版：19 页；PDF SHA-256 `a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633`
- 简答版：7 页；PDF SHA-256 `1387c998560128ae2f7f913b0bbcd6429e25da28045b163472721110e6da8894`
- 印刷版：14 页；PDF SHA-256 `be6a861df5007dfbbd0c57412c03691601047caf53222bc3449facc5c2fe7561`

## 失败检查

- gk-1994-shanghai｜试题版 第 2 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q11(A)原点O被递增曲线穿过；300dpi局部复核确认，须调整标号位置。
- gk-1994-shanghai｜试题版 第 4 页｜`heading_number`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜原卷Q24前第四节（54分、3题）标题与说明缺失，当前第三节36分共3题却连续列Q21—26。
- gk-1994-shanghai｜试题版 第 4 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q23题面图A标号被PB边线穿过；300dpi局部复核确认，须调整标号位置。
- gk-1994-shanghai｜解析版 第 2 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q11左上(A)图的原点标签O放在y轴右侧、x轴下方，递增对数曲线直接穿过O字形（约x=435—454,y=482—505，坐标基于整页1241×1754 PNG）；该处文字与曲线遮叠。其余B/C/D、x/y及1可辨。
- gk-1994-shanghai｜解析版 第 4 页｜`heading_number`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜本attempt已实际查看150dpi的page-04.png，并定向对照根目录.work/source-pdf-cache/1994-shanghai-page2.png：固定扫描第2页右栏在Q23结束、Q24之前明确有“四、（本大题满分54分）本大题共有3题。解答下列各题必须写出必要的步骤。”当前解析版首次承载Q24的第4页却由Q23两小问直接进入Q24，整段第四大题标题/分值/题数/作答说明缺失，只有页首“三、解答题，36分共3题”，导致21—26题连续挂在第三大题下；heading_number=fail。后续第17页Q24解析入口也未显示该第四大题结构。仅记录本attempt源章节完整性缺陷，未修改题面、解析或LaTeX，未重做来源盲核。
- gk-1994-shanghai｜解析版 第 4 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q23题图中A字母与左侧PB实线相交（约x=540—559,y=664—688）；A实际顶点位于其右侧、AD虚线左端，标签现落在线段上，影响标签辨识。P/B/C/D可辨，图整体未裁切。
- gk-1994-shanghai｜解析版 第 10 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q11重复题图的左上(A)图仍有对数曲线穿过原点标签O（约x=435—454,y=430—452，整页PNG坐标）；B/C/D及坐标轴字母完整。
- gk-1994-shanghai｜解析版 第 16 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q23上方题面重复图的A标签被PB边线穿过（约x=540—559,y=999—1025，整页1241×1754 PNG坐标），figure_label=fail；此处对应第4页题面图，并以同attempt的试题版/q23-crop.png局部证据再次确认。页底解析辅助图与上方题面图区分，P/A/B/C/D/E/H标签可辨，本次不将该已修辅助图列为失败对象。
- gk-1994-shanghai｜解析版 第 17 页｜`heading_number`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜已实际查看本attempt的150dpi page-17.png：页首接续Q23的(1)(2)解答及两答案框后，直接出现“第24题”和“题目见第4页”，未见第四大题标题、54分/共3题或该章作答说明。定向查看根目录.work/source-pdf-cache/1994-shanghai-page2.png可见原扫描在Q24前有完整“四、（本大题满分54分）本大题共有3题。解答下列各题必须写出必要的步骤。”；第4页首次Q24题面亦缺该段，后续答案结构未呈现这一章界，故heading_number=fail。这是与第4页关联的章节遗漏，不是第17页长答案框的分页问题；内容留待主会话修复。
- gk-1994-shanghai｜简答版 第 2 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q11(A)原点O被递增曲线穿过；300dpi局部复核确认，须调整标号位置。
- gk-1994-shanghai｜简答版 第 4 页｜`heading_number`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜原卷Q24前第四节（54分、3题）标题与说明缺失，当前第三节36分共3题却连续列Q21—26。
- gk-1994-shanghai｜简答版 第 4 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q23题面图A标号被PB边线穿过；300dpi局部复核确认，须调整标号位置。
- gk-1994-shanghai｜印刷版 第 2 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q11四选项图左上(A)中，原点字母O位于y轴右下方并被对数曲线穿过，标签与曲线实际遮叠（约页面宽35.7%、高23.0%处）；B/C/D的轴名及选项字母可辨。需调整O标签位置后复看；本次不修图。
- gk-1994-shanghai｜印刷版 第 3 页｜`heading_number`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜已实际查看固定扫描第2页（.work/source-pdf-cache/1994-shanghai-page2.png）及本attempt印刷版page-03.png：扫描右栏Q23结束、Q24之前明确有“四、（本大题满分54分）本大题共有3题，解答下列各题必须写出必要的步骤”。印刷版第3页首次Q24前整段章节标题及说明缺失，Q23(2)后直接进入Q24；页上仅保留“三、解答题／本大题满分36分，共有3题”的说明，后续却连列Q21–26，章节归属与题数范围不完整。此为源章节完整性缺陷，heading_number判fail；保留当前attempt诊断，交主会话集中修复，本次不改内容。
- gk-1994-shanghai｜印刷版 第 3 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q23题面几何图中，A标签放在顶点A左侧，与左侧斜线PB相交，字母笔画被线穿过（约页面宽44.5%、高37.6%处）。P/B/C/D标签可辨。需移开题图A标签后复看；本次不修图。
- gk-1994-shanghai｜印刷版 第 7 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q11四选项图左上(A)中，原点字母O位于y轴右下方并被对数曲线穿过，标签与曲线实际遮叠（约页面宽35.7%、高60.3%处）；B/C/D的轴名及选项字母可辨。需调整O标签位置后复看；本次不修图。
- gk-1994-shanghai｜印刷版 第 11 页｜`figure_label`｜attempt `4713a95a-06b4-4399-9bab-c58f428d8b8c`｜Q23题面几何图中，A标签放在顶点A左侧，与左侧斜线PB相交，字母笔画被线穿过（约页面宽44.5%、高66.1%处）。P/B/C/D标签可辨。页下方解析辅助图的P/A/B/C/D/E/H标签均可辨且图未裁切。需移开题图A标签后复看；本次不修图。

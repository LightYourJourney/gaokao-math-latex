# phase1-b52：2004 春季北京文科共享内容与四版入口生成

日期：2026-10-28

## 触发与固定输入

上一批运行 provenance/short_answers 针对性测试时，全库答案一致性测试因已登记的 `2004_春季北京文科/answers.tex` 尚未生成而报 FileNotFoundError。本批实际生成缺失内容，保留全库检查覆盖所有登记卷的原要求。

本批为 `gk-2004-spring-beijing-arts` / `phase1-b52`，20题；固定source `src-417d865aa928e69f32b3fcbc80abe4fa227259b79ababcce8765ea981117119b`，SHA-256 `4670b402354afd088d6993fbc473490158f27e232b1c54730e5989b64a21ec26`，2页（印刷页155–156）。来源是XeTeX排印副本，只有题面，无来源答案；内部canonical仅绑定工作流固定字节，不认证发布者、出版物、版次、来源链或官方身份，`official_answer=null`。

## 生成物与阻断边界

- 依据已登记的题面、答案要点和解析正文生成 `questions.tex`、`answers.tex`、`answers_short.tex` 及试题/解析/简答/印刷四个入口。四版复用共享内容，没有另写一份题面或答案。稳定index此前已由上一批按完整manifest生成，本批index字节未变。
- 复用项目目录中已登记的Q17四棱锥、Q18椭圆轨道TikZ图；题面与解析各引用一次。图稿内容与数学答案均未修改。
- Q20仍照录“计算公以及”并保留疑脱“式”的显式注记；没有据答案反补题面。`ISSUE-1238`保持open/blocks_completion，paper仍blocked，batch仍planned。本阶段没有导入provenance或伪装成已完成。

## 登记与图稿测试修正

既有转录测试仍断言来源paper_id为空、题面含“paper_id未绑定”，与此前已提交的登记阶段冲突。本批改为检查实际paper_id、canonical关系、source_ids反向绑定、blocked状态、ISSUE-1238以及official_answer仍为空；原有20题连续题号、题型、关键公式/文本和缺字标记检查保留。

既有图稿测试读取 `2004/figures/` 的旧副本。本批改为直接测试 `2004_春季北京文科/figures/` 内正式登记的图稿。题面链接以年度目录为基准、图表清单以LaTeX项目根为基准，分别验证相对路径。两处旧目录图稿与项目图稿SHA相同；引用检查发现Q17旧路径仍被2004北京理科题面与清单复用，因此保留旧图稿，未破坏其他卷引用。

首次专项测试的临时XeLaTeX包装器因本会话沙箱不能写该worktree的.work而报权限错误；在已授权的worktree写环境重跑。图稿测试实际编译/渲染的是当前项目图稿；Q20数阵同样编译为单页。此类局部临时PDF不等于正式四版PDF或逐页视觉验收。

## 验证记录

- `generate_projects.py --batch phase1-b52 --check`、`make_short_answers.py --batch phase1-b52 --check`、`make_editions.py --batch phase1-b52 --check`通过。
- `solution_sources.py check-batch`为20题全部通过；source_manifest validate通过，manifest CSV当前且775行。
- 北京文科专项：`python3 -m unittest discover -s math-gaokao-latex/tests -p 'test_2004_beijing_spring_arts*.py'`，现场 `Ran 9 tests in 2.021s` / `OK`，包含两幅项目图稿与数阵的临时编译/渲染检查。

- 最终完整相关检查：provenance、short_answers（含全库逐卷答案一致性）及本卷transcription/solutions/figures，现场 `Ran 172 tests in 146.571s` / `OK`。先前缺少2004卷answers.tex的错误已消除；最终日志见 `.work/phase1-b52/verification/generation-tests.log`。
- 全量 `report.py check --all`确认输出与manifest当前一致，775行CSV当前；`git diff --check`通过。

## 报告与下一步

本批不改manifest业务状态或revision（仍5306），不改来源、答案、图稿或既有正式回执。全量报告细表按当前Git事实刷新ownership：前批验证时的validated成为committed，尚缺正式回执的两批为unavailable；这是Git持久化事实，不是新的视觉结论。

下一步补齐本卷题面独立复核与逐题provenance，再推进正式四版构建和全部页面视觉审查；2009春季上海卷已具备provenance与四版入口，待正式构建。未运行全量测试套件，未生成本卷正式build/review回执，本阶段不表示单卷或1952—2026题库完成。token/费用/总工时未知。

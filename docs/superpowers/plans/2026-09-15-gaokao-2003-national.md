# 2003 年全国卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** 将固定源对应的 2003 年全国新课程文、理两卷与全国旧课程文、理两卷整理为可追溯 Markdown、四种可编译 LaTeX 版本、矢量图源和通过全页复核的 PDF。

**Architecture:** 四卷各自拥有唯一题面 Markdown、答案要点 Markdown 和解析正文 Markdown；\`solution_sources.py\` 确定性生成含解析稿，\`generate_projects.py\` 生成共享 \`questions.tex/answers.tex\`，\`make_short_answers.py\` 与 \`make_editions.py\` 生成其余源文件。固定源 PDF 只用于核对，不进入仓库；原卷图形全部用 TikZ/PGFPlots 重绘为项目内 \`.tex\` 图源。

**Tech Stack:** Markdown、Python 3 工具链、XeLaTeX/PGFPlots/TikZ、Poppler (\`pdfinfo\`/\`pdftoppm\`/\`pdftotext\`)、仓库 manifest/provenance/review receipts。

**Spec:** \`math-gaokao-latex/README.md\` 与高考数学 LaTeX 题库目标。

## Global Constraints

- 新课程文固定源：\`普通高考/2003/2003全国新课程文(天津,山西,江西,山东,安徽,黑龙江,青海).pdf\`，source id \`src-3ddeacd5e7af3ae7ea5e8d57361f03cb101441d1d16e2e0fb8745b9abb1f0ee1\`，SHA-256 \`818528bc51de1b64f955b805d73ae94c2e618fffc2b64d85a87f8566f7b3785a\`，502579 bytes，2 页 A3，原卷印刷页码 144–145。
- 新课程理固定源：\`普通高考/2003/2003全国新课程理(天津,山西,江西,山东,安徽,黑龙江,青海).pdf\`，source id \`src-cb1fea4cc700f8010560816b4eea32e118db965a0a186d64692cb293d2e90da2\`，SHA-256 \`1f2e03804b1957f9521812172895a1aceb6baf3f702a101ff7c6d809661f0a00\`，504619 bytes，2 页 A3，原卷印刷页码 142–143。
- 旧课程文固定源：\`普通高考/2003/2003全国旧课程文.pdf\`，source id \`src-8029e29df29623f528ee2fa4af275a49872530b12c47faf25df544e38a5d0764\`，SHA-256 \`4c27f10550cec0e9322b2302d1acb0396e2aaaa34477d74c26d3f4512f695a81\`，501572 bytes，2 页 A3，原卷印刷页码 136–137。
- 旧课程理固定源：\`普通高考/2003/2003全国旧课程理.pdf\`，source id \`src-9474496def11d3c2b490c481bfebf0f952588afa06395dc1129ca3c37d8bc4a7\`，SHA-256 \`e8644b5b0263e92d5d27243373e5f54c0b2fdf63f6992c70504a8895f7eee9b8\`，503803 bytes，2 页 A3，原卷印刷页码 134–135。
- 四卷均须以固定源为事实边界；固定源 PDF 不进入仓库，图形只提交 TikZ/PGFPlots \`.tex\`，禁止提交原卷截图、PNG/JPEG 或其他栅格媒体。
- 每卷题面、答案要点、解析正文和含解析稿须保持唯一来源关系；每卷预计 22 题，必须保留全部选项、图表、几何图形、开放式小问和分问。
- 四卷各生成 4 个 PDF；每个 \`build/\` 最终只保留 \`试题版.pdf\`、\`解析版.pdf\`、\`简答版.pdf\`、\`印刷版.pdf\`，清除 \`.aux/.log/.out/.fls/.xdv/.synctex.gz\` 与 \`.work/\`。
- 不修改主 worktree，不 push；manifest、index、CSV、provenance、build/review receipts 和批次报告必须与当前字节一致后分提交。

## File Map

- Create: \`2003/2003_数学真题_全国新课程文_{试题,答案要点,解析正文,含解析}.md\`
- Create: \`2003/2003_数学真题_全国新课程理_{试题,答案要点,解析正文,含解析}.md\`
- Create: \`2003/2003_数学真题_全国旧课程文_{试题,答案要点,解析正文,含解析}.md\`
- Create: \`2003/2003_数学真题_全国旧课程理_{试题,答案要点,解析正文,含解析}.md\`
- Create by tools: \`math-gaokao-latex/2003_全国新课程卷_文科/*\`
- Create by tools: \`math-gaokao-latex/2003_全国新课程卷_理科/*\`
- Create by tools: \`math-gaokao-latex/2003_全国旧课程卷_文科/*\`
- Create by tools: \`math-gaokao-latex/2003_全国旧课程卷_理科/*\`
- Modify by registration/finalization tools: \`source-manifest.json\`、\`index.json\`、\`manifest.csv\`、四卷 provenance/build/review receipts、\`reports/phase2-b92.md\`、必要的问题总账条目。

## Tasks

- [x] **Task 1: Verify fixed sources.** 已用 \`pdfinfo\`、SHA-256、\`pdftotext\` 和 A3 渲染确认四份固定源及原卷印刷页码；源页图和文本只保存在临时目录，不进入仓库。
- [ ] **Task 2: Transcribe the four papers.** 建立四卷各四份规范 Markdown，逐题保留题面、选项、表格、图形位置、所有小问和题面页脚事实；图片标记使用确定性的 ASCII 图名。
- [ ] **Task 3: Solve and blind-review.** 独立复算四卷答案，分别核对选择/填空、解析几何、立体几何、数列、函数和应用题；对开放题、题面缺字或答案歧义保留源字面并登记问题。
- [ ] **Task 4: Register and generate.** 注册 \`phase2-b92\` 与四个 paper，生成四卷含解析稿、共享 TeX、简答版和四种入口壳文件，并校验题号、答案块、图形引用集合及复用次数。
- [ ] **Task 5: Record provenance.** 为四卷建立三角色核查工作稿，导入固定 source id、页码、题面/答案哈希和角色证据，生成 provenance。
- [ ] **Task 6: Build and review.** 正式编译 16 个版本；用 Poppler 渲染逐页视觉检查字形、题号、公式/选项、图形标签、页眉页脚、分页留白、字号和答案边界；修复真实排版问题后重新编译并 finalize review。
- [ ] **Task 7: Global gates and cleanup.** 更新 CSV 与批次报告，运行 b92 及全局 manifest/solution/generation/build/provenance/review/report 门禁和完整测试，清除编译中间物、\`.work/\` 与其他本地缓存，提交并关闭本计划。

## Self-Review Checklist

- [ ] 四个 source id、SHA、A3 页数和印刷页码已出现在 manifest/provenance。
- [ ] 每个 Markdown 图片标记都对应项目内已提交的矢量 \`.tex\`，分支没有新增栅格媒体。
- [ ] 四卷题面、选项、图形、开放式小问和答案均已独立核对。
- [ ] 16 个 PDF 编译成功并逐页视觉通过，\`build/\` 不留编译中间物。
- [ ] b92 与全局报告、回执、测试通过；历史无关漂移单独报告，不伪装成 b92 结果。

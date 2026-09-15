# 2002 年全国旧课程卷数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** 将固定源对应的 2002 年全国旧课程文、理两卷整理为可追溯 Markdown 源、四种可编译 LaTeX 版本、矢量图源和通过全页复核的 PDF。

**Architecture:** 文科与理科各自拥有唯一题面 Markdown、答案要点 Markdown 和解析正文 Markdown；\`solution_sources.py\` 确定性生成含解析稿，\`generate_projects.py\` 生成共享 \`questions.tex/answers.tex\`，\`make_short_answers.py\` 与 \`make_editions.py\` 生成其余源文件。固定源 PDF 只用于核对，不进入仓库；原卷图形分别用 TikZ/PGFPlots 重绘为项目内 \`.tex\` 图源。

**Tech Stack:** Markdown、Python 3 工具链、XeLaTeX/PGFPlots/TikZ、Poppler (\`pdfinfo\`/\`pdftoppm\`/\`pdftotext\`)、仓库 manifest/provenance/review receipts。

**Spec:** \`math-gaokao-latex/README.md\` 与当前高考数学 LaTeX 题库目标。

## Global Constraints

- 文科固定源：\`普通高考/2002/2002全国旧课程文.pdf\`，source id \`src-e94a11b05b4ad42845d528bcbff857ece76994b862f8d048695238d53dc7598f\`，SHA-256 \`49bfdc7bbdd039343607fc8dca4ba21ff9fa325a295aa275a3cf83eaee9c4773\`，500667 bytes，2 页 A3，印刷页码 106–107。
- 理科固定源：\`普通高考/2002/2002全国旧课程理.pdf\`，source id \`src-318d665806619e51ad75d72ca59d2819e49112e6f8ce48c6d1b3a0a360f58ec0\`，SHA-256 \`fd94463dc6b89e964464a75e3fc973139d27457e5b1e09da5ccaab8d203e8aa9\`，500656 bytes，2 页 A3，印刷页码 104–105。
- 两卷均为 22 题：选择题 1–12、填空题 13–16、解答题 17–22；必须保留全部选项、图形、开放式剪拼要求和小问。
- 所有原卷图形只提交 TikZ/PGFPlots \`.tex\` 源，禁止提交原卷截图、PNG/JPEG 或其他栅格图。
- 每卷 \`build/\` 最终只保留 4 个 PDF；\`.aux/.log/.out/.fls/.xdv/.synctex.gz\` 和 \`.work/\` 必须清除。
- 不修改主 worktree，不 push；源、生成、构建/复核和计划关闭按独立提交完成。

## File Map

- Create: \`2002/2002_数学真题_全国旧课程文_{试题,答案要点,解析正文,含解析}.md\`
- Create: \`2002/2002_数学真题_全国旧课程理_{试题,答案要点,解析正文,含解析}.md\`
- Create by tools: \`math-gaokao-latex/2002_全国旧课程卷_文科/*\`
- Create by tools: \`math-gaokao-latex/2002_全国旧课程卷_理科/*\`
- Create vector figures: 文科第 13/17/19/22 题图形，理科第 10/18 题图形。
- Modify by registration/finalization tools: \`source-manifest.json\`、\`index.json\`、\`manifest.csv\`、对应 provenance/build/review receipts、\`reports/phase2-b91.md\`、必要的问题总账条目。

## Tasks

- [x] **Task 1: Verify fixed sources.** 已用 \`pdfinfo\`、SHA-256、\`pdftotext\` 和 A3 渲染核对两份固定源及印刷页码；四张源页图保存在临时目录，不进入仓库。
- [x] **Task 2: Transcribe the two papers.** 建立两卷四份规范 Markdown，逐题保留题面、选项、表格、图形位置、开放式剪拼题与所有小问；文科第 13/17/19/22 题、理科第 10/18 题的图片标记使用确定性的 ASCII 图名。
- [x] **Task 3: Solve and blind-review.** 独立复算两卷答案；重点核对文科温度函数、运动相遇、四棱锥二面角、距离比轨迹和剪拼体积，理科二次曲线离心率、正方形垂直几何、汽车递推、绝对值函数和非负参数递推。若题面措辞有多解或条件缺失，保留源字面并登记问题。
- [x] **Task 4: Register and generate.** 注册 \`phase2-b91\` 与两个 paper，生成含解析稿、共享 TeX、简答版、四种入口壳文件，并校验题号、答案块、图形引用集合和复用次数。
- [x] **Task 5: Record provenance.** 为两卷建立三角色核查工作稿，导入固定 source id、页码、题面/答案哈希和角色证据，生成 provenance。
- [x] **Task 6: Build and review.** 正式编译 8 个版本；用 Poppler 渲染逐页视觉检查字形、题号、公式/选项、图形标签、页眉页脚、分页留白、字号和答案边界；修复真实排版问题后重新编译并 finalize review。
- [x] **Task 7: Global gates and cleanup.** 更新 CSV 与批次报告，运行 b91 及全局 manifest/solution/generation/build/provenance/review/report 门禁和完整 816 项测试，清除编译中间物、\`.work/\` 与其他本地缓存，提交并关闭本计划。

## Self-Review Checklist

- [x] 两个 source id、SHA、A3 页数和印刷页码已出现在 manifest/provenance。
- [x] 每个 Markdown 图片标记都对应项目内已提交的矢量 \`.tex\`，分支没有新增栅格媒体。
- [x] 两卷 22 题、选项、开放式图形题和小问均已独立核对。
- [x] 8 个 PDF 编译成功并逐页视觉通过，\`build/\` 不留编译中间物。
- [x] b91 与全局报告、回执、测试通过；历史无关漂移单独报告，不伪装成 b91 结果。

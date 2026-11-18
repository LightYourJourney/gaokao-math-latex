# 2001 年全国新课程卷文史财经类数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or \`superpowers:executing-plans\` to implement this plan task-by-task. Steps use checkbox ([ ]/[x]) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 2001 年全国新课程卷文史财经类数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、五个矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID \`src-cd2fb5a40dd3158755f6b2df6cbef2f85f6df70d42dc36d05ad965d8707df3d4\` 对应的固定源 PDF；第 1–3 页是题面，第 4–7 页是同一文件附带的参考答案与评分标准。公开转录和附带解答只用于文字定位、答案交叉核验与独立推导复核，不替代题面事实。题面、答案、独立解析分别落在 \`2001/\`，由现有工具生成单卷 LaTeX 工程；第 11、12、19、20 甲、20 乙题的图形仅以 TikZ/PGFPlots \`.tex\` 永久保存。

**Tech Stack:** Python 3 标准库工具链、XeLaTeX、ctex、TikZ/PGFPlots、Git。


## Global Constraints

- 固定 PDF \`普通高考/2001/2001全国新课程文(天津,山西,江西).pdf\` 的 SHA-256 必须为 \`48d73376f3c7b2b524dd6e75974a0b1ffff3ef0ceb75e7e0d6da92dd717186e3\`，大小 \`3905154\` bytes，PDF 原件不复制进仓库。
- 固定源为 7 页 A4 扫描件，题面位于文件第 1–3 页、印刷页码 343–345；第 4–7 页为附带参考答案与评分标准、印刷页码 346–349。答案与解析须另行独立复算并诚实标注。
- 题面含 22 题：选择题 1–12、填空题 13–16、解答题 17–22；第 20 题保留原卷甲/乙二选一结构，甲题答案是 \`cos\angle BED=-1/3\`，乙题答案含二面角正切 \`\\sqrt2/2\`。
- 二手转录与固定 PDF 附带解答只用于定位和交叉核对；发现其与题面或独立计算冲突时保留固定题面字面并显式修正解析，不能静默改题。
- 题面图形全部重绘为 \`.tex\` 矢量源；逻辑 PNG 标记可留在 Markdown 以驱动映射，但 PNG/JPEG/SVG 文件不得创建或提交。
- 构建目录最终只保留四个 PDF；不得留下 \`.aux/.fls/.log/.out/.toc/.synctex.gz/.fdb_latexmk/.bcf/.run.xml/.nav/.snm/.vrb/.idx/.ilg/.ind/.lof/.lot/.pyc/.pyo/.swp/.swo/.bak\` 或 \`.work\`。
- 生成的 \`questions.tex\`、\`answers.tex\`、\`answers_short.tex\`、四个版本壳、\`index.json\` 与 \`manifest.csv\` 只能由现有工具写入。
- 不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: \`2001/2001_数学真题_全国新课程文_试题.md\`
- Create: \`2001/2001_数学真题_全国新课程文_答案要点.md\`
- Create: \`2001/2001_数学真题_全国新课程文_解析正文.md\`
- Create by tool: \`2001/2001_数学真题_全国新课程文_含解析.md\`
- Create: \`math-gaokao-latex/2001_全国新课程卷_文科/figures/{f2001_t11_roofs.tex,f2001_t12_network.tex,f2001_t19_systems.tex,f2001_t20a_square_pyramid.tex,f2001_t20b_trapezoid_pyramid.tex}\`
- Create by tools: project \`.tex\` sources, \`provenance.json\`, \`receipts/{build,review}.json\`, four local PDFs, \`reports/phase2-b81.md\`
- Modify by tools: \`source-manifest.json\`, \`manifest.csv\`, \`missing-issues.md\`

## Task 1: 固定题面、答案与独立解析

- [x] Verify source facts with \`pdfinfo\`, SHA-256 and visual renders; use OCR only as a locating aid, record question pages 1–3 / printed pages 343–345 and attached answer pages 4–7 / printed pages 346–349.
- [x] Transcribe Q1–Q22 from the first three fixed-source pages. Preserve Q11 roof diagrams, Q12 network graph, Q19 circuit systems, both Q20 variant diagrams using logical image markers only.
- [x] Independently solve every question and recheck Q1 set intersection, Q5 vector coordinates, Q8 ellipse eccentricity, Q10 parabola dot product, Q14 stratified sampling, Q15 converse logic, Q16 ratio, Q17 sequence limit, Q18 optimization, Q19 system probabilities, Q20甲/乙 geometry, Q21 cubic extrema, and Q22 intersection angle/radius range.
- [x] Use \`solution_sources.render_combined()\` through \`extract-batch --write\` to generate \`_含解析.md\`; keep Q20甲/乙 in one aligned question block and ensure each solution block matches its own question.
- [x] Run parser, answer, and issue checks; inspect the complete diff; commit the source checkpoint.

## Task 2: 注册来源并生成 LaTeX 工程

- [x] Create and dry-run an exact registration spec for paper \`gk-2001-regular-national-new-arts\`, project \`2001_全国新课程卷_文科\`, title \`2001 年·全国新课程卷·文科\`, track arts, count 22, base \`2001_national_new_arts\`, pages \`[1,3]\`, printed pages \`[343,345]\`, solution pages \`[4,7]\`, structure \`题目 [1,22]\`, and the five registered figures.
- [x] Write the registration and run \`generate_projects.py\`, \`make_short_answers.py\`, and \`make_editions.py\` in write mode; run every corresponding check mode.
- [x] Validate figure counts, generated answer markers, both Q20 variant answer sets, and source-page metadata; commit the generated LaTeX source.

## Task 3: provenance、正式构建与清理

- [x] Initialize the three provenance roles, fill current question/answer hashes, import them, and verify provenance current.
- [x] Run the formal four-edition build; require no compiler errors, missing characters, overfull boxes, or unresolved references; inspect logs before cleanup.
- [x] Render all PDFs to \`/private/tmp\`, inspect contact sheets and key pages, then remove exact build intermediates and the ignored batch \`.work\` directory.
- [x] Commit source/build/provenance artifacts and leave PDFs local and ignored.

## Task 4: 全页复核与全库验证

- [x] Prepare four review work items and fill every page with the eight checks after visual inspection.
- [x] Finalize the batch review, require \`FINALIZED\`, inspect the report and issue transitions.
- [x] Run targeted gates, the full unit-test suite, and artifact assertions; confirm every build directory has exactly four PDFs and no intermediate/image/work files.
- [x] Mark this plan checked, commit final metadata/report diff, and report remaining unregistered years and unresolved issues honestly.

## Self-Review Checklist

- [x] Fixed source fingerprint, question pages 1–3 / printed pages 343–345, attached answer pages 4–7 / printed pages 346–349, and Q20甲/乙 structure are present.
- [x] Q11/Q12/Q19/Q20甲/Q20乙 are the only logical image markers and all map to committed \`.tex\` figures.
- [x] All high-risk calculations and every Q20 variant/subpart answer anchor are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with any preexisting unrelated source drifts explicitly reported.

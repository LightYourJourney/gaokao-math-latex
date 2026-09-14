# 2001 年上海卷文科数学资产 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or \`superpowers:executing-plans\` to implement this plan task-by-task. Steps use checkbox ([ ]/[x]) syntax for tracking.

**Goal:** 将固定源 PDF 对应的 2001 年上海卷文科数学整理为 22 题的可追溯 Markdown 源、四种可编译 LaTeX 版本、三份矢量图源和通过全页复核的 PDF。

**Architecture:** 题面唯一依据 source ID \`src-e3874efedf21e835ec81144259ce64bfe239ca02be1100474179b0afb3015d9c\` 对应的固定源 PDF；文件为 2 页 A3 题面，印刷页码 92–93，不附答案。题面、答案、独立解析分别落在 \`2001/\`，由现有工具生成单卷 LaTeX 工程；第 12、19、22 题的图形仅以 TikZ/PGFPlots \`.tex\` 永久保存。

## Global Constraints

- 固定 PDF \`普通高考/2001/2001上海文.pdf\` 的 SHA-256 为 \`53d8d6243e1309c2dde8da4a1722241f0f70c10d5e761aac02c97fc0496f3664\`，大小 \`501317\` bytes，PDF 原件不复制进仓库。
- 固定源为 2 页 A3 扫描/文本混合题面，印刷页码 92–93；PDF 不含答案，答案和解析均为本库独立复算。
- 题面含 22 题：填空题 1–12、选择题 13–16、解答题 17–22；Q20–Q22 均保留原题三问结构。
- Q12 保留左侧荒漠化总面积折线与右侧待绘网格；Q19 保留立方体；Q22 保留数列发生器流程图。图形使用矢量源，不提交截图。
- 构建目录最终只保留四个 PDF；不得留下 LaTeX 中间物、媒体文件或 \`.work\`。
- 不修改主工作树，不 push；源、生成、构建、复核各阶段分别提交。

## File Map

- Create: \`2001/2001_数学真题_上海文_试题.md\`
- Create: \`2001/2001_数学真题_上海文_答案要点.md\`
- Create: \`2001/2001_数学真题_上海文_解析正文.md\`
- Create by tool: \`2001/2001_数学真题_上海文_含解析.md\`
- Create: \`math-gaokao-latex/2001_上海卷_文科/figures/{f2001_t12_desertification.tex,f2001_t19_cube.tex,f2001_t22_generator.tex}\`

## Tasks

- [x] Verify source facts with \`pdfinfo\`, SHA-256 and visual renders; record pages 1–2 / printed pages 92–93.
- [x] Transcribe Q1–Q22, including the Q10 table and Q12 blank plotting grid, with only Q12/Q19/Q22 logical image markers.
- [x] Independently solve all answers, especially Q4 logarithmic set, Q8 constant term, Q11 radical-axis generalization, Q12 chart, Q16 \`lg x/x\`, Q18 ellipse right triangle, Q19 dihedral angle, Q20 complex powers, Q21 washing model, and Q22 iteration.
- [x] Generate \`_含解析.md\`, register b82, generate/check LaTeX, provenance and receipts.
- [x] Compile, visually review all pages, finalize review, run full gates and tests, clean all intermediates, and close this plan.

## Self-Review Checklist

- [x] Fixed source fingerprint and two-page A3 range are present.
- [x] Q12/Q19/Q22 are the only logical image markers and all map to committed \`.tex\` figures.
- [x] All 22 answers and subparts are independently checked.
- [x] Four PDF versions compile, are visually reviewed, and have no compiler intermediates left.
- [x] No raster image enters the branch; PDFs remain ignored local build artifacts.
- [x] Full tests and global receipt/report gates pass, with preexisting unrelated source drifts reported.

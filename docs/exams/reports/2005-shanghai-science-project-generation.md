# 2005 上海理科普通卷：解析转义修复与项目 TeX 生成

- 日期：2026-11-03。
- 批次/试卷：`phase4-b44` / `gk-2005-regular-shanghai-science`。
- 固定候选来源：`src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e`，PDF SHA-256 `092e8e90dc1430ab2fa8b8ce79e072e317559e6bef29f1cb7461e9423925ec31`。

## 解析源修复

首次运行 `generate_projects.py --write` 时，严格 Markdown-to-TeX 转换器在 Q4、Q5 报“未配对的 `$`”。逐字节检查确定 `2005/2005_数学真题_上海理_解析正文.md` 中有1个退格字符和5个换页符，分别替代了 LaTeX 命令 `\binom`、`\frac` 的反斜杠。已根据上下文及答案要点恢复为 `\binom{10}{3}`、`\frac18`、`\frac12`、双曲线标准式中的两处 `\frac` 和渐近线 `\frac ba=3`；算式与答案数值不变。题面和答案要点无控制字符。修复后解析正文 SHA-256 为 `ac03931501a9f7944a58bb4595e75061d2c34f89e459ef2c7992a4cd38ecb837`。

随后运行 `solution_sources.py extract-batch --write` 刷新含解析稿；22题解析块与规范题面/答案要点再次通过批次一致性检查。含解析稿 SHA-256 为 `9d0ecc1d29e5fa745933acce0cb48dc4074326b753367a7e61ca36e5c4862d55`。

## 项目生成结果

按 `phase4-b44` 逐卷生成：

| 文件 | SHA-256 |
|---|---|
| `2005_上海卷_理科/questions.tex` | `fc7adbeda57f9ced2ac8f4bacca28a62950ac58e2dece295e1f9c61623d83b7d` |
| `2005_上海卷_理科/answers.tex` | `81be5fd4a2831057846db6d5c0d5162d17fa56340148faff04a54110284d1c32` |
| `2005_上海卷_理科/answers_short.tex` | `8bb924c6cec4242f6912c52a74fd67c62155758782730403852ff70ab9058e21` |
| `2005_上海卷_理科/试题版.tex` | `06222ae93b4725812fa8242e1e6345b9a2a3e93c434c99d3350e073ef54c4267` |
| `2005_上海卷_理科/解析版.tex` | `6b3e83bbd24d7951cf6273768c4031f666da7076fe101e11f20ad0b70e38e1f3` |
| `2005_上海卷_理科/简答版.tex` | `5ebf451f750d3176026b9ceaf292bf1f1538c39f8195745ba7fdcd41d117e226` |
| `2005_上海卷_理科/印刷版.tex` | `a8d3e22dabcc5d3490ed4a219ab8aa4e0f218968bce356cb2d19f48e82e3dbdc` |
| `index.json` | `8a78672256e355ad8d534ab6d6af0d2e0bed92f845ad84b708b1f0e13c50922e` |

索引条目登记22题、Q11/Q17/Q19三张图和候选来源说明。生成的 `questions.tex`、`answers.tex` 均包含三张图的 `\input`；简答稿继续保留 Q11、Q20 的 U/PENDING。

## 验证与边界

- 串行执行 `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`；三项均与生成结果一致。并行检查时遇到共享 RepoLock 竞争，改为串行后通过。
- `solution_sources.py check-batch`（22题）、`provenance.py check-batch`（22题）、`source_manifest.py validate`、`issues.py validate` 均通过。provenance 摘要不因这次解析排版转义修复改变；Q11 `ISSUE-1380` 与 Q20 `ISSUE-1381` 继续 open / blocks_completion。
- 本阶段只修复解析源并生成项目 TeX、简答与四版入口；没有编译正式 PDF、写 build/review receipt 或进行整卷逐页视觉验收。固定 PDF 无答案页，`official_answer=null`，paper 仍 blocked。本报告不表示来源认证、整卷完成或长期语料库完成。

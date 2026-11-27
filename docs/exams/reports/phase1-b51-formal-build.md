# phase1-b51：2000 上海春季卷四版正式构建

日期：2026-10-28

## 构建与修正

- 首次正式 attempt `b941a8a9-c34c-4f43-b7f1-fdc58560e0e8` 在四版均以 latexmk exit code 12 失败。原始 XeLaTeX 日志定位到 `questions.tex:8`：说明文字中的行内代码 `official_answer` 被转换成含裸下划线的 `\texttt{official_answer}`，触发 `Missing $ inserted`。首轮没有产出 PDF，manifest revision 从构建输入5294更新至5295，并生成 ISSUE-1234–1237。
- 只把规范题面来源说明改为“本库官方答案状态仍为 null”，保留固定副本无版权页/完整书目、出版者/版次/来源链和官方身份未核的边界；未改题目内容、答案或解析。按 `generate_projects.py --write` 刷新项目 TeX；逐题题面哈希与 provenance 原有22条逐一相同，`provenance.py import-batch` dry-run 与 `check-batch` 均通过。
- 成功 attempt `36aee468-9d50-403d-b997-7b62eca90d07` supersedes 上述失败 attempt，receipt 输入 manifest revision 5296，完成后 manifest revision 5297。TeX Live 2026；XeTeX 3.141592653-2.6-0.999998、latexmk 4.88、Poppler 26.10.0。四版 latexmk exit code 均为0；receipt 中 errors、missing characters、overfull、undefined references 和 problems 均为空；前次四条 compile-error issue 均由构建事务标记 resolved / non_blocking。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 5 | `53fbd1faaa33408aa87ed86893fb4a6bce8f85f2384045073bdc7f8eeb608ee7` |
| 解析版 | 19 | `dcd12b216d937d94163404f7446546a7c51cea90928e8daca29faa4e36a37bc3` |
| 简答版 | 7 | `d8d577d3945a0138f0229774e331a3d18259f21ebf5f02f4d0546f4599ce94e3` |
| 印刷版 | 16 | `0206c9bf3dcfd2e43fcb3e446765cf48daa5905305315f4fa2a9f3c7a7962e1c` |

实测 SHA-256 与页数已用本机 PDF 文件和 `pdfinfo` 对照 receipt 一致。正式输出共47页。receipt 当前性检查为0 invalid / stale / missing，1 pending review；该结果表示构建等待视觉审查，不表示最终验收。

## 阶段边界

paper 当前为 `compiled`，batch `compiled_pending_review`；尚未生成最终 review 回执，47页仍须逐页完成八项视觉审查。来源发布者、出版物、版次、扫描来源链及附录答案官方身份未核，`official_answer=null`。本阶段不代表该卷完成或1952–2026语料库完成。

阶段报告：本文件。未运行测试套件。

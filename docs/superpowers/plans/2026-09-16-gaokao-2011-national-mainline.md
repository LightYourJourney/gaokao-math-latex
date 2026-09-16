# 2011 National Mainline Corpus Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` for this plan. Keep source verification, answer reconciliation and visual review separate.

## Goal

将 2011 年四套全国主线数学固定源整理为可复用、可打印、带 provenance 与视觉审查证据的 LaTeX 题库项目：大纲卷文/理、新课标卷文/理。省市自主命题卷不混入本批。

## Fixed sources

| 试卷 | paper_id | source_id | SHA-256 | PDF 页数 / 印刷页 | 题数 |
|---|---|---|---|---:|---:|
| 全国大纲文 | `gk-2011-regular-national-outline-arts` | `src-35cf2a952171a9a5ed841b65fe64f4db79736b9691f1ec11ab01010d498f7e66` | `d3d4ea37feaea5912a7944bc55c59a7276553353df7343b490a041b85aaa6640` | 2 / 待逐页确认 | 22 |
| 全国大纲理 | `gk-2011-regular-national-outline-science` | `src-97272800598ffb89a3d1fd20879ebfc173927660c59c8b865e6370deca0cdbd9` | `99df7de63b91e3c467edba49a64aca1e6f99df19df3f6d8c7ca771960cd56ecb` | 2 / 待逐页确认 | 22 |
| 全国新课标文 | `gk-2011-regular-national-new-arts` | `src-fbcfbffda78ab6ba823b9eec98ba0cc35f776b0485e0691789956e5b5984fabe` | `0a51cfc47db01607c02454f6c5f1b703a3677738846bb7c34bd850b1dc802687` | 2 / 待逐页确认 | 24 |
| 全国新课标理 | `gk-2011-regular-national-new-science` | `src-d721501484d5ca7f344cd8e1c5a148445befecbb2d1d72109ca8c1581c300617` | `416f534b60c91bfb6db95f0b83c4f7701b244d84ba01124af92ce28bda403eed` | 2 / 待逐页确认 | 24 |

固定源 PDF 位于外部本地上游仓库 `gaokaomath-src/普通高考/2011/`，登记后以 manifest 的 source ID、artifact SHA 和逐题页码为唯一来源身份。固定源不附答案与解析，答案由独立复算，任何矛盾进入 `missing-issues.md`。

## Structure

- 大纲文/理：选择题 1–12、填空题 13–16、解答题 17–22。
- 新课标文/理：选择题 1–12、填空题 13–16、解答题 17–24。
- 页码先按 PDF 高分辨率渲染和 `pdftotext -f/-l` 双重定位，不能从相邻年份推断。

## Tasks

- [ ] **Task 1 — Freeze source table and register `phase2-b00`（工具契约中的两位批次编号，对应第 100 批）。**
  - 逐一确认四个 source artifact、纸面页码和题量，创建 registration spec；全部规范 Markdown 齐全后再执行一次 `register-papers --write`。
- [ ] **Task 2 — Transcribe and structurally validate four papers.**
  - 题面逐题转录，保留选项、公式、单位、小问和原卷图形标记；每卷先过 question parser。
- [ ] **Task 3 — Independently solve and reconcile answers.**
  - 独立复算代数、概率统计、数列、几何、解析几何和微积分；答案/解析确定性对齐，疑点写问题总账。
- [ ] **Task 4 — Create vector figure sources only.**
  - 所有实际 Markdown 图形标记映射为项目内 TikZ/PGFPlots `.tex`；不将 PNG/JPEG 放入仓库。
- [ ] **Task 5 — Generate shared LaTeX and four shells.**
  - 生成 `questions.tex`、`answers.tex`、`answers_short.tex` 和四种入口，运行对应 `--check` 门禁。
- [ ] **Task 6 — Import provenance and build.**
  - 三角色逐题来源回执写入 provenance，四卷四版本正式编译，build 目录最终只保留 PDF。
- [ ] **Task 7 — Review every page and finalize.**
  - 渲染全部 PDF 页面，检查字形、题号/选项、图形、页眉页脚、分页、字号和答案泄漏，生成批次报告。
- [ ] **Task 8 — Clean, verify and commit without pushing.**
  - 删除 `.work`、临时渲染和编译中间物；运行全套门禁与单元测试；提交本批，不 push。

## Acceptance criteria

- `phase2-b00` 恰好包含上述四个固定 source ID，不包含省市自主命题卷；工具的 `batch_id` 只接受两位 `bNN` 编码。
- 四卷题号、结构、答案、解析和图形引用均通过工具门禁；每卷 4 个入口编译成功且无缺字、未解析引用和 overfull。
- provenance、build/review receipts、manifest CSV、批次报告与当前输入一致；开放问题明确反映在批次状态。
- 清理后 2011 `build/` 只含 PDF，仓库无新栅格图，工作树干净。

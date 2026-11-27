# 2003 北京普通文理候选卷：项目 TeX 与四版入口生成

- 日期：2026-11-04；batch `phase4-b48`；输入 manifest revision `6151`。
- 文科 `gk-2003-regular-beijing-arts` 与理科 `gk-2003-regular-beijing-science` 各生成项目题目、完整答案、简答答案，以及试题版、解析版、简答版、印刷版四个入口；共 14 个 TeX 文件，并将两卷加入 `index.json`。

## 生成与核对

- `python3 tools/generate_projects.py --manifest source-manifest.json --batch phase4-b48 --write`：成功，2 卷写入 5 个目标。
- 同脚本 `--check`：2 卷项目内容与生成结果一致。
- `python3 tools/make_short_answers.py --manifest source-manifest.json --batch phase4-b48 --write`：成功，2 卷写入简答稿；`--check`：两卷简答与生成结果一致。
- `python3 tools/make_editions.py --manifest source-manifest.json --batch phase4-b48 --write`：成功，生成 8 个版本入口；`--check`：两卷版本壳与模板渲染结果一致。
- 产物为 `2003_北京卷_文科/`、`2003_北京卷_理科/` 下各 7 个 TeX 文件，以及 `index.json` 中对应的两条记录。生成内容包含逐题 U/PENDING，不把条件性答案写成确定答案。

## 当前边界

- 两卷仍处于 `blocked`，batch 为 `provenance_verified`。文科 Q18 的 `ISSUE-1398`、`ISSUE-1399` 与理科 Q17 的 `ISSUE-1400`、`ISSUE-1401` 仍 open / `blocks_completion`；候选 PDF 发布链、官方身份与官方答案均未核。
- 本阶段没有运行正式 XeLaTeX 四版构建、生成正式 PDF / build receipts、逐页视觉复核、批次封存或全量测试。下一阶段执行正式构建并建立当前构建回执后，逐页检查所有 PDF 页面。本阶段不表示整卷验收或长期语料完成。

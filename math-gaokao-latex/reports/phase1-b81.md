# 批次 phase1-b81 视觉审查报告

- 批次结论：`closed_with_blockers`
- 试卷数：1
- 版本数：4
- 审查页数：39

## gk-2007-regular-beijing-arts

- 标题：2007 年·北京卷·文科
- 项目目录：`2007_北京卷_文科`
- 构建：`succeeded`（attempt `6b6ea9af-ae99-4a10-9d45-6910e2ef7fae`）
- 审查：`passed`（2026-11-03T07:57:50+08:00）
- 内容候选：`eligible_blocked`
- 页数：试题版 4；解析版 16；简答版 6；印刷版 13
- 警告豁免：0
- 视觉问题：无
- 阻塞问题：ISSUE-1355

## 收口门禁

- `manifest.csv` 已刷新并通过 currentness 校验（775 个来源）；`report.py check --all` 通过，确认报告投影与全量 manifest 一致且保留未完成状态。
- 全库 `python3 -B -m unittest discover -s tests -q` 实际结束于 `Ran 1769 tests in 541.255s`，结果 `FAILED (failures=2, skipped=13)`。两个失败均为既有跨卷门禁漂移：
  1. `test_task25_updates_exactly_eight_existing_keys_with_layout_only_diffs`：2017 全国Ⅰ理科 `answers.tex` 的漂移账本 SHA 为 `9318dce3313b0575c1382eb225301dfec145683d59b54367fa13a81f3f0b3a30`，当前文件 SHA 为 `8ea128d4aba0a2bed8897d4719a8df3d99c119c7bc3a15b98ee8c6f5d797f233`。本阶段未修改该卷或漂移账本；同一 SHA 漂移已记于 `reports/2006-fujian-arts-q11-correction.md`。
  2. `test_the_cached_states_match_the_recomputed_ones`：全库发现79套旧卷缓存状态与现场派生状态不一致，例如 `gk-2012-regular-national-outline-arts` 缓存为 `complete`、现场为 `answers_verified`。本批 `provenance.py check-batch --batch phase1-b81` 通过；未改动全库其他卷的缓存状态。
- 因全库测试仍有上述两项失败，本批记录为全库门禁未全通过；不把跨卷漂移归入本批，也不据此改写其他试卷状态。phase1-b81 的正式构建、视觉复核和报告/CSV 投影均已通过，批次仍为 `closed_with_blockers`，Q18 `ISSUE-1355` 保持 open / `blocks_completion`。

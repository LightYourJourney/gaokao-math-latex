# 2005 上海文科 Q22 版面修正与视觉收口

- 日期：2026-11-03
- 批次：`phase4-b43`
- 试卷：`gk-2005-regular-shanghai-arts`
- 来源：`src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846`
- 来源 PDF SHA-256：`952989a262e3f7b34a425ccb6e2132af7e88408a387edae50f59a9505ebe46a1`

## 修正原因与范围

首次正式构建 attempt `e365d302-3044-43d4-88c8-5bd1d171bac1` 的解析版共19页。逐页视觉检查发现第19页只排了 Q22 的两个答案框，形成内容稀少的尾页。

修正仅涉及 Q22 解析的排版：将（1）中的乘积等式和（3）中的三角恒等式并入文字行，保留（1）的分段函数独立展示。没有修改题意、数学步骤、结论或答案。确定性生成器据此更新 `_含解析.md` 与项目 `answers.tex`。

## 修正后构建

正式构建 attempt `0a9ae90f-d1bc-4768-8bc9-d6a0fde10c67` 使用 manifest revision 6107，结束后由视觉收口推进至 revision 6109。四版结果如下：

| 版本 | 页数 | PDF SHA-256 |
| --- | ---: | --- |
| 试题版 | 4 | `726e5af21f41aa1f1de65cf29102d2a0a5454ad582b7e4a7fcff38d2b5f91662` |
| 解析版 | 18 | `b1dc87c86503026a226af8e861426614f7dc49eadd2b19d45de78522303d64ce` |
| 简答版 | 6 | `7ed88d8abca369eaae41433ae72d9a26937cea0679b21192fb864ad97756fe9b` |
| 印刷版 | 15 | `5bf59296d975f983e3911f896087b9d83cbdc3a91ffc2afc71aa71220af62b7f` |

四版均构建成功；TeX errors、missing characters、overfull 和 undefined references 均为0。`build_projects.py validate-receipts --require-current-inputs` 通过。

## 视觉及工作流核验

- 四版43页逐页复核完成，每页8项，共344项检查，全部通过。
- 41页与已实际检查的前次渲染图像完全一致，沿用原有逐页视觉结论。
- 解析版第18页和印刷版第15页受分页紧凑影响；两页均以120 dpi单页检查并通过。原解析版第19页已消失。
- `review_receipts.py check-batch` 返回 `FINALIZED`；正式批次结论为 `closed_with_blockers`。
- `provenance.py check-batch` 通过；`solution_sources.py check-batch` 覆盖22题并通过。项目 TeX、简答稿、四版入口及全局报告投影的确定性检查均通过。
- 全库来源 CSV 为775行；报告投影 currentness 检查通过。全库快照为412套试卷、260个批次，门禁状态217 `FINALIZED` / 42 `INVALID_OR_STALE` / 1 `VISUAL_FAILED`。这些是本次投影读数，不表示其他批次在本阶段获得重新验收。

## 全量测试结果

执行 `python3 -B -m unittest discover -s tests -q`：`Ran 1769 tests in 565.093s`，`FAILED (failures=3, skipped=13)`。失败项如下：

1. `test_2015_fujian_arts_transcription.FujianArtsTranscriptionTests.test_source_identity_and_transcription_hash`：测试期待审查记录 `paper_id` 为 `None`，实际为 `gk-2015-regular-fujian-arts`。相关2015福建文科来源记录和测试不在本批改动路径中。
2. `test_baseline.AdjudicatedDriftLedgerTests.test_task25_updates_exactly_eight_existing_keys_with_layout_only_diffs`：测试期待 `2017_全国Ⅰ卷_理科/answers.tex` SHA-256 为 `9318dce3313b0575c1382eb225301dfec145683d59b54367fa13a81f3f0b3a30`，当前值为 `8ea128d4aba0a2bed8897d4719a8df3d99c119c7bc3a15b98ee8c6f5d797f233`。该卷和 drift ledger 不在本批改动路径中。
3. `test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones`：全库有79条缓存状态与现场重算不一致。此项是全库一致性失败；本批 `phase4-b43` 自身的 provenance 检查通过。

因此，全量 unittest 没有通过；本报告只记录各项定向批次核验通过，不掩盖上述全库失败。

## 未解除的阻塞

- Q12 `ISSUE-1377`：表面积端点是否允许并列最小，来源没有说明，答案继续保持 U/PENDING。
- Q20(1) `ISSUE-1379`：原件印作“中低价层”，与上下文疑似冲突，继续保留原文与 U/PENDING，不自行改字或裁定。
- `ISSUE-1378` 已按前序来源核验结案，不再阻塞。
- Paper `gk-2005-regular-shanghai-arts` 仍为 `blocked`；`phase4-b43` 为 `closed_with_blockers`。本报告不表示整卷无阻塞完成，也不表示1952–2026长期语料完成。

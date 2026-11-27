# 2002 苏豫粤桂卷：四版正式构建

- 日期：2026-11-04。
- 批次/试卷：`phase4-b50` / `gk-2002-regular-suyuyuegui`。
- 最终正式构建 attempt：`99457b35-988d-486b-82bf-ee011d6982e2`；上一构建 attempt：`b4702eff-141d-4dbb-9bf6-e50bf669efe0`。
- 最终构建输入 manifest revision：`6188`；build receipt 状态 `succeeded`。视觉复核结案后 live manifest revision 为 `6190`。

## 构建修复

- 首次正式 attempt `b8ffbcde-258a-4c92-af28-acf40cbae8a7` 因来源说明中的行内代码 `official_answer` 被转换成含未转义下划线的 `\texttt{official_answer}` 而编译失败。正文改为自然语言“官方答案未认证”，front matter 中的 `official_answer: null` 未改；失败构建产生的 `ISSUE-1418`–`ISSUE-1421` 在成功重建后自动标为 resolved / non_blocking。
- attempt `b4702eff-141d-4dbb-9bf6-e50bf669efe0` 成功后，初次目检发现 Q16/Q17 行间公式句号落在公式外。规范题面将 display math 改为单行序列化，并把句号放入 `\text{。}`；随后生成最终 attempt `99457b35-988d-486b-82bf-ee011d6982e2`。

## 最终 PDF 回执

工具链为 TeX Live 2026 / XeTeX、latexmk 4.88 与 Poppler 26.10.0。四版均成功编译，`errors`、`missing_characters`、`overfull`、`undefined_references` 均为空：

| 版本 | 页数 | 字节 | PDF SHA-256 |
|---|---:|---:|---|
| 试题版 | 4 | 110375 | `a6e46837b6c2035e3d6fc421b32575c5ccc89ef8b65510a393ce20b76d66b5c2` |
| 解析版 | 19 | 207293 | `ae19d5e02b766abc59f94f23a0e0fa9170c5c115aeb270c44640bc95e25c0941` |
| 简答版 | 6 | 127181 | `60df70de5d930f533142f2cac0c13dfef0d7fba046c40d262af4eeeeced44329` |
| 印刷版 | 16 | 207360 | `fcc644253685d16a91b427891b4f0a592f4c0a606389ce6608c5573707a246cb` |

四版共 45 页。`build_projects.py validate-receipts --manifest ... --batch phase4-b50 --require-final --json` 返回 `OK`，1 卷成功、0 pending、0 stale、0 invalid、0 failed。逐页视觉复核八项全部通过；详见[批次视觉审查报告](phase4-b50.md)。

## 当前边界

Q18 的零公比约定仍未由同版来源裁定；`ISSUE-1417` 保持 `open / blocks_completion`，Q18 仍 U/PENDING，paper 为 `blocked`，batch 为 `closed_with_blockers`。固定来源发布者、版次、复制链及官方身份仍未认证，`official_answer=null`。本报告只记录这一卷的构建结果，不表示整卷事实问题已解决或 1952–2026 语料已完成。

## 全库测试结果

- 按规范执行 `python3 -B -m unittest discover -s tests -q`：`Ran 1779 tests in 582.882s`，`FAILED (failures=1, skipped=13)`。
- 唯一失败为 `test_provenance.LiveRepositoryTests.test_the_cached_states_match_the_recomputed_ones`：现场发现 80 卷的缓存 `production_state` 与 provenance 重算状态不一致，首例为 2012 全国大纲文科（缓存 `complete`、重算 `answers_verified`）。对照本批修改前 HEAD revision `6181` 与当前 revision `6190`，该卷的缓存值均为 `complete`；source manifest 的本批差异只涉及 2002 苏豫粤桂的批次/试卷字段，因此这是进入本批前已存在的全库状态漂移。
- 本卷定向 `provenance.py check-batch --batch phase4-b50`、source manifest、issues、solution sources、build/review receipt 及报告/CSV 检查均通过。完整测试套件目前仍有上述一项失败，不能记作全通过；应由后续全库状态治理单独处理。

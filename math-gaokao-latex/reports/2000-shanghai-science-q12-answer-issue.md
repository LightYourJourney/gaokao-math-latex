# 2000 上海理科候选卷：Q12 答案约定 blocker 补充登记

- 日期：2026-11-03。来源仍为 `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`，PDF SHA-256 `b798af61afdac624589769db5bbafe734aa9a0016973bd00b3f5bc8028ab3a40`。
- provenance 导入预检指出：U 级答案必须关联当前、仍阻断的答案类或约定类问题。Q12 已有 `ISSUE-1369`（`transcription-ambiguous`）记录原页字面“等此数列”及忠实照录，但该类型不能单独表达“数列类型不明导致确定答案未知”。
- 使用 `issues.question_issue()` / `issues.upsert_issue()` 构造与校验问题块，并通过 `build_projects.commit_state()` 的 state transaction 同时写入问题总账与重算后的 manifest；未手工编辑问题 Markdown 或 manifest。新增 `ISSUE-1371`（`answer-convention-ambiguous`，open / `blocks_completion`），fingerprint `eac81cb1071c79f3385d531f1ad7763b7973531daca8cb6824439c2a4022ee70`。transaction `3a875335-c3c7-452c-bca9-35ee3a4b02d2`，manifest revision `6089→6090`。
- `ISSUE-1369` 保持原状态和原证据；`ISSUE-1370`（Q21 `answer-conflict`）未变。Q12 仍逐字照录“等此数列”，答案仍为 U/PENDING，不以条件性等比推导替代确定答案；paper `blocked`、batch `planned`、`official_answer=null`。
- 事务后 `source_manifest.py validate --manifest math-gaokao-latex/source-manifest.json` 与 `issues.py validate --file math-gaokao-latex/missing-issues.md` 均通过。本登记不解决 Q12 内容，也不构成来源认证。

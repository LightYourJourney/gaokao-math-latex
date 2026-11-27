# 2000 上海理科候选卷：Q21 答案约定 blocker 补充登记

- 日期：2026-11-03。固定来源 `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`，PDF SHA-256 `b798af61afdac624589769db5bbafe734aa9a0016973bd00b3f5bc8028ab3a40`。
- provenance 导入预检要求 U 级答案和未解决答案冲突分别挂接当前 blocker。Q21 已有 `ISSUE-1370`（`answer-conflict`）表达按原页指数2推导后，与“最大项”设问不相容；该类型满足 conflict 守卫，但不满足 U 级答案的 answer/convention 守卫。
- 使用 `issues.question_issue()` / `issues.upsert_issue()` 构造并验证问题，再通过 `build_projects.commit_state()` 的 state transaction 同时写入问题总账和重算后的 manifest。新增 `ISSUE-1372`（`answer-convention-ambiguous`，open / `blocks_completion`），fingerprint `d7ce4a294bc7e8c9ab36c9b1efa7204479109793845b97ecb993caf36cd9a086`。transaction `d5f8ce73-0fd3-4a99-8770-27de1ab77942`，manifest revision `6090→6091`。
- `ISSUE-1370` 保持不变；新增问题记录未核定原卷意图或版本差异。Q21 仍照录指数2，按字面结论“无最大项”，整题答案继续 U/PENDING；paper `blocked`、batch `planned`、`official_answer=null`。
- 事务后 source manifest 与 issue ledger 校验通过。本登记不把指数2改成 $n$，也不解除 Q21 blocker。

# 2006 湖北文科候选卷：paper/source 登记与 Q12 blocker 入账

- 日期：2026-11-02。
- 通过 `source_manifest.py register-papers` 登记 paper `gk-2006-regular-hubei-arts` 与批次 `phase1-b73`，绑定固定 source `src-af4cc84c7c2f6c2c1ed0bef598d5a51f57d65a1b25926d7a02631cc6c5387d75`；manifest revision `5930→5931`。
- `canonical` 只表示 manifest 内部将这组固定 PDF 字节绑定为本卷来源输入；SHA-256、Git blob、题签与本地页数不认证发布者、出版者、版次、来源链或官方身份。`official_answer` 保持 `null`。

## Q12 问题记录

- 注册事务同时建立 `ISSUE-1333`，类型 `answer-missing`，状态 `open`、影响 `blocks_completion`。固定题面只给每人的边缘发热概率0.80，没有给出五人的联合模型。
- 五人完全同动且边缘概率均为0.80时，至少3人发热的概率为0.80；假设反应相互独立时为0.94208，按题目要求精确到0.01为0.94。结果不唯一，因此规范答案保留 U/PENDING，0.94 仅作独立性假设下的条件值。issue 的恢复动作是取得明确独立性条件、可裁定答案/勘误或其他同版材料。
- 该 blocker 使 paper `production_state=blocked`、`blocked_from=planned`；batch `phase1-b73` 保持 `planned`。本次未以条件计算消除 issue。

## 事务与针对性验证

题面、答案要点、解析正文的 frontmatter 已绑定新的 paper ID，含解析稿由 `solution_sources.render_combined` 重新生成。`source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`manifest_csv.py --check` 和 `solution_sources.py check-batch --batch phase1-b73` 均通过；CSV 投影为775行。

登记后已完成 Q18 TikZ 图稿阶段，见 `2006-hubei-arts-q18-figure.md`；逐题三角色 provenance、项目 TeX、正式构建与视觉验收仍未完成。Q12 blocker 继续阻断卷级完成。本阶段不表示来源认证、卷级验收或长期语料库完成。

# 2006 江西、浙江、湖北理科候选卷：逐题 provenance

日期：2026-11-02；批次：`phase1-b70`。

## 角色记录

为江西 22 题、浙江 20 题、湖北 21 题建立 `question-review`、`answer-solve`、`answer-review` 共 189 条角色记录。question-review 将每题对应到固定 Source ID、PDF SHA-256 和所在页，并指向各卷逐页转录报告；结论仅证明规范题面与本次固定副本可见文字相符，不认证副本身份。answer-solve 以独立推导报告为依据，答案为非官方项目推导；answer-review 记录独立盲解核对角色。规范题面及答案哈希由导入器从当前文件现场计算。

| Paper ID | 题数 | PDF 页映射 | provenance 后状态 |
|---|---:|---|---|
| `gk-2006-regular-jiangxi-science` | 22 | Q1–Q18 → 1；Q19–Q22 → 2 | `answers_verified` |
| `gk-2006-regular-zhejiang-science` | 20 | Q1–Q17 → 1；Q18–Q20 → 2 | `answers_verified` |
| `gk-2006-regular-hubei-science` | 21 | Q1–Q17 → 1；Q18–Q21 → 2 | `blocked` |

答案推导与争议更正见 `reports/2006-three-science-answer-solve.md`。江西 Q7/Q19、湖北 Q16/Q20 等独立解题中发现的问题已按复核后结论修正；湖北 Q17（2）仍为未解决冲突。

## 未决项与状态

湖北 Q17（2）答案证据等级为 U，盲核状态为 unresolved，关联仍开放且阻断的 `ISSUE-1319`（题面约束冲突）与 `ISSUE-1320`（答案缺失/冲突）。原题照录，答案保持 U/PENDING，不猜测勘误。江西、浙江当前角色记录没有未决答案冲突；`answers_verified` 描述的是项目独立推导和盲核状态，不代表官方答案认证。

导入事务将 manifest revision 从 5879 推进至 5881（首次导入后修正一处转录报告路径引用并重导入）。批次当前 `provenance_verified`；该状态不代表项目 TeX 已生成或 PDF 已构建。

## 验证与边界

- `provenance.py import-batch` dry-run 和写入成功；`provenance.py check-batch --batch phase1-b70` 返回 `OK：3 卷`。
- `source_manifest.py validate`、`issues.py validate --file missing-issues.md` 通过；`solution_sources.py check-batch --batch phase1-b70` 三卷全部通过。
- 固定 PDF 未提供官方答案或评分材料，所有 `official_answer` 继续为 null。三卷图稿尚未制作、登记；未生成项目 TeX/简答版、未正式构建 PDF、未做视觉检查。湖北 Q17 blocker 继续阻断完成。本记录不表示来源认证、批次闭环或长期语料完成。

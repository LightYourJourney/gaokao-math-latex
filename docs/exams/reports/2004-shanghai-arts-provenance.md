# 2004 上海文科普通卷：逐题 provenance 导入

- 日期：2026-11-03。
- 批次/试卷：`phase4-b45` / `gk-2004-regular-shanghai-arts`。
- 固定候选来源：`src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290`，PDF SHA-256 `4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad`。Q1–Q19 映射 PDF 第1页（印刷页200），Q20–Q22 映射第2页（印刷页201）。来源发布者、版次、复制链与官方身份未核。

## 角色与逐题结果

`tools/provenance.py init-batch` 在忽略目录创建 question-review、answer-solve、answer-review 三组各22题的角色工作文件。三个角色分别记录独立题面复核、Codex 编者推导和 gpt-6-luna/high 分段盲解答案复核，角色身份互不相同。题面摘要按包含最终图稿链接的当前规范题面块现场计算；答案摘要按当前规范答案记录计算。

- 题面复核 Q1–Q22 共22题全部 `passed`；Q5、Q18、Q20、Q21 的图链接与矢量图按图稿阶段报告完成源页复核。
- 答案证据为20题 D 级编者推导、2题 U 级待核。Q17 因实数范围内条件无解关联 `ISSUE-1384`；Q19 因第 (2) 问集合符号脱节未定义集合 B 而保留 U/PENDING，关联 `ISSUE-1385`。两题均未选用条件性答案替代确定答案。
- 独立盲核结果中，全部22题冲突状态均为 `none`，答案候选与盲解一致。Q17、Q19 的待核项来自原卷字面无解与集合符号脱节，不是两份数学答案冲突。
- `provenance.json` SHA-256：`da62a06388e15b285c1e07e4ee30cb818cc5d03892a499318627577d01979b17`。

## 事务与门禁

- `provenance.py import-batch` dry-run 校验通过后正式写入。Manifest revision `6119→6120`，事务 ID `b3d294ea-a025-4180-baa9-57240d95b581`；批次状态更新为 `provenance_verified`，paper 生产状态仍为 `blocked`。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`provenance.py check-batch`（22题）通过。`provenance.py status --batch phase4-b45` 准确返回 `blocked gk-2004-regular-shanghai-arts` 与 `provenance_verified phase4-b45`。
- Manifest 事务后 `manifest.csv --check` 首次检测到旧投影；原因是批次状态由 `planned` 更新为 `provenance_verified`。运行 `manifest_csv.py --write` 后，`manifest_csv.py --check` 通过，仍为775行。

## 剩余事项

固定 PDF 无答案页，`official_answer=null`；Q17/ISSUE-1384 与 Q19/ISSUE-1385 继续阻塞整卷完成。尚未生成项目 TeX、四版 PDF、正式构建回执或逐页视觉回执；后续阶段再运行项目 TeX 生成、四版构建与视觉审查。本报告只表示三角色 provenance 已导入，不表示来源认证、整卷完成或长期语料库完成。

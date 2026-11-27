# 2004 上海理科普通卷：逐题 provenance 导入

- 日期：2026-11-04。
- 批次/试卷：`phase4-b46` / `gk-2004-regular-shanghai-science`。
- 固定候选来源：`src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a`，PDF SHA-256 `9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e`。Q1–Q19 映射 PDF 第1页（印刷页198），Q20–Q22 映射第2页（印刷页199）。来源发布者、版次、复制链与官方身份未核。

## 角色与逐题结果

`tools/provenance.py init-batch` 在忽略目录创建 question-review、answer-solve、answer-review 三组各22题的角色工作文件。三个角色分别记录独立题面复核、Codex 编者推导和 gpt-6-luna/high 分段盲解答案复核，角色身份互不相同。题面摘要按包含最终图稿链接的当前规范题面块现场计算；答案摘要按当前规范答案记录计算。

- 题面复核 Q1–Q22 共22题全部 `passed`；Q5、Q18、Q21 的图链接与矢量图按图稿阶段报告完成源页复核。
- 答案证据为20题 D 级编者推导、2题 U 级待核。Q19 因第 (2) 问集合符号脱节未定义集合 B 而保留 U/PENDING，关联 `ISSUE-1386`；Q22 因第 (1) 问点 $P_1(3, 0)$ 不在椭圆上且无实数解而保留 U/PENDING，关联 `ISSUE-1387`。两题均未选用条件性答案替代确定答案。
- 独立盲核结果中，全部22题冲突状态均为 `none`，答案候选与盲解一致。Q19、Q22 的待核项来自原卷字面无解与集合符号脱节，不是两份数学答案冲突。
- `provenance.json` SHA-256：`2f76275bacd8d9bf49212cd026efe62662ee2d06709cff50836a177a5a35c5a8`。

## 事务与门禁

- `provenance.py import-batch` dry-run 校验通过后正式写入。Manifest revision `6125→6126`，事务 ID `c1a0ad36-cd67-420a-9e6d-7a54551c96f8`；批次状态更新为 `provenance_verified`，paper 生产状态仍为 `blocked`。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`provenance.py check-batch`（22题）通过。`provenance.py status --batch phase4-b46` 准确返回 `blocked gk-2004-regular-shanghai-science` 与 `provenance_verified phase4-b46`。
- Manifest 事务后 `manifest.csv --check` 检测到旧投影（批次状态由 `planned` 更新为 `provenance_verified`）；运行 `manifest_csv.py --write` 后，`manifest_csv.py --check` 通过，保持775行。

## 剩余事项

固定 PDF 无答案页，`official_answer=null`；Q19/ISSUE-1386 与 Q22/ISSUE-1387 继续阻塞整卷完成。尚未生成项目 TeX、四版 PDF、正式构建回执或逐页视觉回执；后续阶段再运行项目 TeX 生成、四版构建与视觉审查。本报告只表示三角色 provenance 已导入，不表示来源认证、整卷完成或长期语料库完成。

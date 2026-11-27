# 2004 春季安徽理科卷：Q20 图稿登记与逐题 provenance

日期：2026-10-27

## 记录结果

- `source_manifest.py sync-figure-registry` 登记 Q20 TikZ 图 `gaokao_2004_anhui_spring_science_q20_prism.tex`，规范题面与合并稿各引用 1 次，manifest revision `5209 → 5210`。
- `provenance.py import-batch` 导入 `phase1-b43` 共 22 题三角色证据，manifest revision `5210 → 5211`；批次进入 `provenance_verified`，paper 为 `answers_verified`。
- Q1–Q19 来源页映射固定 PDF 第 1 页，Q20–Q22 映射第 2 页。source SHA-256 `51038ba6ecdfbb8c5c7edc417f871eda5a5a5c03cc5af510da08131ec0dbb151`，题面和答案哈希由导入器现场计算。
- 三个角色以职责标签登记。历史进度记录没有保存核查者姓名，故不补造姓名；答案为 D 级编者独立推导，独立盲解结果一致，22 题冲突状态均为 `none`。固定 PDF 无答案页，`official_answer=null`。

## 验证与边界

- 图稿登记预检/写入通过，实际引用闭合为 1 图、2 处。
- `provenance.py import-batch` dry-run 与写入成功；`provenance.py check-batch --batch phase1-b43` 返回 `OK：1 卷`。
- `source_manifest.py validate` 与 `solution_sources.py check-batch --batch phase1-b43` 通过；全量 CSV 已刷新为 775 行，六份报告已事务写入并回读校验。
- `index.json` 尚未由 `generate_projects.py` 纳入新卷，因此旧卷生成物 currentness 仍暂报 stale；此阶段没有重审旧批次或声称旧回执有效。
- 本阶段未运行测试套件、正式 XeLaTeX 构建、视觉审查或外部书目核查。来源链/出版者/版次和官方身份继续保持未知。
- 后续生成本卷共享 TeX、简答版、四版入口和全局 index，再进行正式构建与逐页视觉校样；完成这些门禁前不得称整卷完成。

# 1989 广东文科候选卷：四版正式视觉审查

日期：2026-10-30

## 验收绑定

- 批次 `phase1-b59`，卷件 `gk-1989-regular-guangdong-arts`，构建 attempt `06a36244-5d74-4489-a485-35f38b76391a`。
- 四版视觉收据绑定同一构建 attempt、PDF SHA-256 与工具链指纹；逐版文件指纹见 `1989-guangdong-arts-formal-build.md` 和 `1989_广东卷_文科/receipts/review.json`。
- 题面版、解析版、简答版、印刷版分别 6、24、8、19 页，共 57 页。审查记录时间 `2026-10-30T08:02:50+08:00`。

## 逐页检查结果

每页按八项检查，共 456 项：410 pass、46 not_applicable、0 fail。46 项 not_applicable 全部是无独立图形或图表标注的页面，其余项目均通过。

| 版本 | 页数 | pass | not_applicable | fail |
| --- | ---: | ---: | ---: | ---: |
| 试题版 | 6 | 44 | 4 | 0 |
| 解析版 | 24 | 172 | 20 | 0 |
| 简答版 | 8 | 57 | 7 | 0 |
| 印刷版 | 19 | 137 | 15 | 0 |
| 合计 | 57 | 410 | 46 | 0 |

Q12 函数图像标签、坐标轴和关键位置清楚；Q28 几何图中的点名及平面标记可辨。Q9、Q16、Q21 的 U/PENDING 与来源问题在相应页面可读。个别页面题目较少、留白较多，题目和分页完整，无裁切、错序或内容遗漏；未发现视觉缺陷。

## 结论与未决事项

- `review_receipts.py finalize-batch-checked` 返回 `FINALIZED`，batch `closed_with_blockers`；review receipt 的顶层状态为 `passed`，四版结果均通过。manifest revision 从 5478 更新至 5479。
- 本次只确认当前四版输出的视觉与分页质量，不改变来源或答案判断。固定扫描题签只见“文史类”，年份、地区归属、出版者、版次及官方身份仍未核实，`official_answer=null`。
- `ISSUE-1259` 至 `ISSUE-1263` 继续开放并阻断整卷完成，涉及 Q9 印载 C 与题干推导 B 冲突、Q16 异面直线垂直约定、Q21 印载选项与推导范围不匹配及关联答案问题。固定扫描未见 Q29（2）最终解集和 Q30 解答。
- `source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`（1 卷）、三种生成器 `--check`、`solution_sources.py check-batch`（30 题）、`review_receipts.py check-batch` 与 `build_projects.py validate-receipts --require-final --require-current-inputs` 均通过。全库报告/CSV 投影另行刷新；本阶段未运行测试套件。

本记录只关闭 `phase1-b59` 的构建与视觉审查门禁，不表示该卷内容已无阻断，也不表示 1952–2026 语料库完成。

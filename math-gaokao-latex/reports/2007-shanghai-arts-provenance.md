# 2007 上海文科候选卷：逐题 provenance 登记

- 日期：2026-11-03。
- Paper：`gk-2007-regular-shanghai-arts`；batch：`phase1-b83`。
- 固定 source：`src-51aa9840dc7a866be37ded966d4a337c999cacd912ce0118e07b3e6c768c5789`；PDF SHA-256：`1d43489e28ce9c305faa753519800b9184e40cc40fbd8343f7fd287b4ec70212`。固定 PDF 两页为印刷页 407–408，且只含题面。

## 导入记录

从忽略目录 `.work/phase1-b83/provenance/` 的三角色逐题记录运行 `provenance.py import-batch --write`。事务 `e3e50387-4d28-4680-a61c-af95ca124639` 将 manifest revision 从 6048 更新为 6049，并写入跟踪文件 `2007_上海卷_文科/provenance.json`，当前 SHA-256 为 `89a8d1d2c1b412e3876151162ef4ac1093b3f7387f7a618a95dd0da8748d61e8`。

- **question-review**：Q1–Q21 全部 `passed`；Q1–Q18 来源页为 PDF 第1页（印刷页407），Q19–Q21 为第2页（印刷页408）。角色报告 `reports/2007-shanghai-arts-question-review.md`。
- **answer-solve**：Q1–Q20 为 D 级编者独立推导；Q21 保持 U/PENDING。答案推导和差异记录见 `reports/2007-shanghai-arts-answer-key.md`、`reports/2007-shanghai-arts-answer-review.md`、`reports/2007-shanghai-arts-solution-review.md`。
- **answer-review**：Q1–Q20 复核一致；Q21 的一般果圆解释与承接第（1）问等边焦点特例会产生不同结果，故 Q21 仍 U/PENDING 并关联 `ISSUE-1362`。固定 PDF 没有答案、解析或勘误页，无法裁定该参数范围。

本次 provenance 校验绑定了 source PDF SHA、原页映射、现行规范题面摘要与答案摘要。该绑定只表示本库采用的固定输入与逐题记录一致，不认证来源发布者、出版版次、扫描复制链或官方身份。`official_answer` 仍为 null；paper 的 `production_state` 保持 `blocked`，batch 状态更新为 `provenance_verified`。

## 同步修订与验证

首次 `solution_sources.py check-batch` 发现解析正文 Q18–Q21 缺少与确定性合成输出一致的 `**解析**` 标记。已在四个题目标题后补齐结构标记并重新生成 `_含解析.md`；题面、答案、数学结论没有变化。解析正文当前 SHA-256 为 `0f8d354c77c764bc8d45682b1896cb9f25dfedccf3cf47209d896677f43b8554`，合成稿 SHA-256 仍为 `b39454ec05d5617277372a64a041bd9af92cf6324e6de2f7b3d5d89b3ca4bc06`。

最终通过以下定向门禁：

- `provenance.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch phase1-b83`：`OK：1 卷`。
- `solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b83`：21题通过。
- `source_manifest.py validate --manifest source-manifest.json`。
- `issues.py validate --file missing-issues.md`。
- `manifest_csv.py --manifest source-manifest.json --output manifest.csv --check`：775行且 current。
- `git diff --check`。

本阶段只完成逐题 provenance 导入和解析正文结构标记同步。Q7、Q11、Q16、Q21 图稿重绘、TeX 项目生成、四版正式构建、构建/视觉回执与逐页目视检查尚未进行；下一阶段继续图稿与项目生成。当前阻断项 `ISSUE-1362` 未解除。本报告不表示本卷闭环、来源认证或长期语料完成。

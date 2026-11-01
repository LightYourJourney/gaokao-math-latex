# 2006 天津理科：source 与题卷登记

- 日期：2026-11-02；批次 phase1-b67；paper gk-2006-regular-tianjin-science。
- 绑定固定候选 source src-634ea48d3fc77ee048d2cf8418a3afb0d6b18c347365c36d8a8e15b53796d307，SHA-256 b38a31042aaadb71d602486419cd5f999ff607dfd5ae3f01eb95f5fd8c253039。绑定只固定本库输入字节；发布者、版次、来源链及官方身份仍未核。
- register-papers dry-run 通过后写入，manifest revision 5767。Q2 作为 ISSUE-1288（answer-conflict，open / blocks_completion）登记；两条渐近线交于原点而选项无 0，固定材料没有答案或勘误。paper 保持 blocked。
- 规范题面、答案要点、解析正文均指向同一 source 和 paper；含解析稿通过 solution_sources 确定性生成。为兼容项目解析器，将题号与小问标题规范为既有 heading 格式，不改题干文字。
- 已通过 source_manifest validate、issues validate、solution_sources check-batch（22 题）。当前未登记题图文件；题图重绘、三角色 provenance、项目 TeX/简答与版本入口、正式构建和逐页视觉审查仍待完成。

本阶段仅完成来源/题卷登记与确定性含解析源；Q2 阻断保持打开，不代表整卷验收或 1952–2026 语料完成。

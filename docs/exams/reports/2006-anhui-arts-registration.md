# 2006 安徽文科：paper/source 与阻断项登记

日期：2026-10-27

- 候选卷 `gk-2006-regular-anhui-arts` 登记入批次 `phase1-b45`；事务将 manifest revision 从 5226 推进到 5227。固定 source `src-c8cc6985576733188a535d25ee781c6c6b1b8de19855999d38d24a0e053810a7` 与本卷作 canonical 内部绑定，仅表明本库选用该固定副本，不认证其官方身份。
- 固定 PDF SHA-256 `631bacb1145ada877f0a40867668cd12bda3caf399cdcacec6543c2829ac32fa`；两页题面、印刷页码278–279，未见答案或分值。出版者、版次、来源链和官方身份未核，答案与解析为非官方项目推导，`official_answer=null`。
- 三幅经独立源图对照的 Q9/Q19/Q22 TikZ 源登记于 `2006_安徽卷_文科/figures/`；题面和含解析稿各引用一次，`figure_files` 对每图记录两次引用。
- 问题事务创建三条 `blocks_completion`：`ISSUE-1216` 为 Q2 的无匹配选项；`ISSUE-1217` 为 Q5 缺少可见方程右侧；`ISSUE-1218` 为 Q5 答案无法确定。三条均 open；paper `production_state=blocked`、`blocked_from=planned`，批次为 `planned`。
- Q1–Q22 题面已独立对照，答案已由第二位解题者逐题复算；Q19/Q22 复算前已知部分结论，不称盲解。正式逐题 provenance 尚未导入，共享 TeX、四版入口、构建及视觉审查尚未完成；`index.json` 尚未包含新卷，当前全库报告有191个批次 `INVALID_OR_STALE`，`phase1-b44` build receipt 单独检查仍 current 但批次 review 门禁暂报状态失配。须先由项目生成器更新索引再重查，不能把登记视为整卷完成或把旧门禁假称当前通过。

# 2003 春季北京文科：固定题源内部绑定与 Q11 阻断登记

日期：2026-10-28

## 来源判定

固定输入为 source `src-4ac986eba3d22fd3034252b57e1fed7e2b7b90eaaef7706499eb43fad52756e1`，SHA-256 `fbb6d54c9af88a7fc594be969b8e61c24bb37d98c05061cceaaf5d1be999c5c6`，Git blob `9f741f6a30aa11e69c466fc5e94257f80a4cb805`，PDF 共2页，印刷页121–122，卷题签为“2003 普通高等学校春季招生考试（北京卷文）”。该文件是 XeTeX 排印副本，不是原卷扫描。

2026-10-21 的公开资料追溯未找到能把这两页与可核实出版社、版次或考试机构原件关联起来的证据。该历史核查结论保持有效。本次区分“本库选择哪一个固定输入”和“该输入是否官方/出版来源可认证”：依据题签及固定字节将它登记为本库内部 `canonical` 输入，以便继续建立本卷工作流；不据此认证发布者、版次、复制来源链或官方身份。与后续同分支 2006 安徽及 2019/2020 春季卷的登记口径一致。若日后出现更可靠同版来源，可按新证据更正绑定并重核所有受影响输出。

## 登记结果

- `source_manifest.py register-papers` dry-run 通过；写入以单一状态事务完成，manifest revision `5266 → 5267`。
- paper：`gk-2003-spring-beijing-arts`；batch：`phase1-b49`；题量22；`track=arts`；题面页 `[1,2]`；无来源答案页，`pages_s=null`。
- 五幅已有 TikZ 图登记到 `figure_files`，每项预期题面版与印刷版共引用2次。五幅 TikZ 源已迁入 canonical 项目 `2003_春季北京文科/figures/`，题面与图表清单改用项目路径；每图的题面/印刷版预期引用数登记为2。
- 事务新增 `ISSUE-1229`。Q11 图中字形 I/L 无法定读，题干文字写 I；open / `blocks_completion`。paper 当前 `blocked`、`blocked_from=planned`，batch 当前 `planned`。
- `official_answer=null`；答案与解析为已形成、经异人复核的独立推导，明确非官方。Q15的数值为依题面表格规律外推，非源附答案。

## 同步修订

题面、答案要点、解析正文及来源校对 sidecar 已更新为内部绑定状态，同时继续明示出版者、版次、来源链和官方身份未核。sidecar 的答案/解析路径与题面 SHA `723fe65b05fdeb082d2fb8b086ede756c29d45920d4be5d51fbc96dd2d8ec50e` 已同步。修正 Q13 解析中把题面 `\sin 2x+1` 写成 `\sin(2x+1)` 的笔误；确定性生成器随后重建 `_含解析.md`。

## 阶段边界

`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch` 和 `git diff --check` 均通过。本阶段没有导入逐题三角色 provenance，没有生成共享 TeX、简答/四版入口或兼容 `index.json`，没有正式 XeLaTeX 构建、整页视觉检查或 build/review receipts。尚不能据登记状态声称整卷完成。未运行测试套件。

## 可复核状态

- batch：`phase1-b49`
- paper：`gk-2003-spring-beijing-arts`
- blocking issue：`ISSUE-1229`
- manifest revision：`5267`
- 下一步：按本卷既有题面、答案和解析审查记录导入逐题 provenance，核对已登记图稿映射，生成共享内容、兼容索引与四版入口，再运行当前性校验并决定是否继续正式构建。

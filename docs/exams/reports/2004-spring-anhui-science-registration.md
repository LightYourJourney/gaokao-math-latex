# 2004 春季安徽理科卷：规范源合并与 paper/source 登记

日期：2026-10-27

## 登记结果

- 使用 `source_manifest.py register-papers` 登记候选卷 `gk-2004-spring-anhui-science`，批次 `phase1-b43`；manifest revision `5208 → 5209`。
- 卷目录键 `2004_安徽春季卷_理科`，科类 `science`，题量 22；题面映射固定 PDF 第 1–2 页，答案/解析页为 `null`。
- source `src-7c00191d50c17971e6f514bf6066e92693aa2b71f0ff05a054e2abe22acb5075` 的固定 PDF SHA-256 为 `51038ba6ecdfbb8c5c7edc417f871eda5a5a5c03cc5af510da08131ec0dbb151`。PDF 页眉及印刷页码对应 2004 年普通高等学校春季招生考试安徽卷理科，2 页 A3，印刷页码 149–150；该文件是 XeTeX 生成件而非原始扫描。
- canonical 仅表示本库将该固定副本绑定为本卷题面来源。上游出版者、版次、扫描来源链未核；不称其为官方原件。固定 PDF 没有答案页，答案/解析为本项目独立推导并经独立盲解交叉核对，`official_answer=null`。
- 当前 `production_state=planned`、批次 `planned`。本阶段未登记逐题 provenance、图形清单或构建/视觉回执。
- 登记后全局 `index.json` 尚未由项目生成器加入本卷；旧卷生成物 currentness 因 index 投影不含新 paper 而暂报 stale。该项留待下一项目生成阶段以正式生成器更新；当前不声称历史 build/review 回执有效。

## 规范源与派生稿

- 保留原 22 题题面、非官方答案和解析结论。为兼容确定性解析器，仅规范化 Q13–Q22 的最终答案块格式；Q19、Q20、Q22 答案按原题小问拆分，解析源新增对应小问锚点。数学内容未作更改。
- 将每题解析正文经 `solution_sources.extract_solution_blocks()` 规范化为含 `**解析**` 标记的 canonical 结构；再由 `solution_sources.render_combined()` 确定性生成 22 题 `_含解析.md`。
- 更新题面/答案/解析中的来源状态文案，明确 canonical 是本库绑定关系、来源官方身份未知；更新原转录测试中已过期的 source 未绑定断言。

## 验证与未完成项

- `register-papers` dry-run 成功（1 卷，仅校验），事务写入 revision 5209。
- `solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b43`：1/1 通过。
- `source_manifest.py validate` 与 `report.py check --all --manifest source-manifest.json --issues missing-issues.md` 通过；`manifest.csv` 已刷新为 775 行；六份全量报告由事务写入并回读校验。
- `git diff --check` 通过。本阶段未运行测试套件、未做外部书目核查、未进行正式四版构建或视觉检查，未 push。
- 后续阶段继续登记图稿/provenance、生成项目 TeX 与四版入口、正式构建并逐页目视审查；未完成这些门禁前不得标记整卷完成。

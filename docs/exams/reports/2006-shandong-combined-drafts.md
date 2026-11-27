# 2006 山东文理候选卷：登记前确定性含解析稿

日期：2026-11-02

- 为满足 `source_manifest.py register-papers` 对规范 `_含解析.md` 路径的存在性前置条件，调用 `solution_sources.render_combined`，以两卷现存题面、答案要点及解析正文生成派生稿。
- 输出为 `2006/2006_数学真题_山东文_含解析.md`（508行）和 `2006/2006_数学真题_山东理_含解析.md`（530行）。未手工修改派生内容。
- 再次从三份规范源调用相同渲染函数与磁盘字节逐卷比较相等；`parse_question_blocks` 对两份派生稿均识别22题；`git diff --check` 通过。
- 该预备输出不建立或绑定 paper/source/batch，也不是单独的完成事实源。完成登记后仍将使用正式批次命令重新提取并检查生成物 currentness；之后再导入逐题 provenance。
- 山东理 Q5、Q10 的 U/PENDING 保留在答案要点及解析正文；固定候选 PDF 的发布者、版次、来源链与官方身份仍未核实。

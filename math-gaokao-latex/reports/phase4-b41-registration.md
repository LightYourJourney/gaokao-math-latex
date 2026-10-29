# 2015 陕西理科：来源登记与待核问题

批次 `phase4-b41`、paper `gk-2015-regular-shaanxi-science`；固定源为 `普通高考/2015/2015陕西理.pdf`，SHA-256 `5cf0ce45b952db59d103b5ff4c3d73d31f8bbcd0dd2ec0fe6fc40b7d9403409c`，两页 A3，印刷页 973–974，未见答案、分值或选做说明。发布者、版次及官方身份未核。本库解答为非官方独立求解；不将固定副本视为官方答案。

已登记 24 题规范题面、答案要点、解析正文、确定性生成的含解析，以及 8 幅 TikZ 图的路径和来源校对记录。题面经第二人对照；独立计算曾在第 20 题出现系数分歧，经复算更正为椭圆 $x^2/12+y^2/3=1$。第 19 题第（2）问无条件答案保留未定，独立同分布下的 0.91 是有条件的计算。

登记事务 revision 5411 为第 11、16、19 题分别创建 `ISSUE-1245`、`ISSUE-1246`、`ISSUE-1247`，当前 paper 状态 `blocked`、batch 状态 `planned`。三项分别涉及圆盘均匀概率模型、流量与截面积的水力假设、以及往返联合分布未明。不得把有条件结果视为无条件官方答案；详见 `2015-shaanxi-science-q19-source-gap.md`。

`solution_sources.py check-batch` 检查 24 题通过；题图登记预检 8 张通过，`source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check` 通过。逐题 provenance 仅创建工作模板，尚未导入；共享 TeX、四个入口、正式编译、字体检查和当前 PDF 的逐页视觉验收均未完成。本阶段不声明试卷完成。

## 逐题来源导入

已将 24 题来源审查、项目求解和独立盲解记录导入 `provenance.json`，与当前题面、答案及固定源哈希绑定；第 11、16、19 题的答案证据为 U 级，分别关联 `ISSUE-1245`、`ISSUE-1246`、`ISSUE-1247`，当前卷仍为 `blocked`。`provenance.py check-batch` 通过，manifest revision 5412，CSV 已按新状态刷新。第 20 题独立初解曾误算，复核后已更正，不能把初始结果当作有效证据。四版生成及编译和视觉验收仍未完成。

## 共享内容与入口生成

已从规范源生成 `questions.tex`、`answers.tex`、`answers_short.tex` 和试题版、解析版、简答版、印刷版四个入口；生成器及简答、入口的 `--check`、24 题来源层检查和 provenance 检查通过。第 11 题答案改为 `U/PENDING`，简答速查表显示 U，解析保留均匀模型下 D 的条件结论；第 16 题和第 19 题继续保留条件与未定说明。逐题哈希重新绑定后 manifest revision 5413；三条阻断仍开放。尚未正式编译或验收 PDF。

## 正式构建，待视觉验收

四个版本正式构建返回 `COMPILED_PENDING_REVIEW`，attempt `1131f12e-55f9-460d-881b-56048c8374db`、manifest revision 5415：试题版 7 页、解析版 22 页、简答版 9 页、印刷版 17 页，共 55 页。回执检查无 missing、invalid 或 stale，状态为 compiled_pending_review；CSV 当前。三项源/模型问题仍开放，paper 保持 blocked，不能将构建成功称为试卷完成。当前 PDF 尚未逐页目视，视觉审查和绑定回执仍待完成。

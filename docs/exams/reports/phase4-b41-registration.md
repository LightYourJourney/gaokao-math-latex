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

## 分页调整及新构建

旧 attempt `1131f12e-55f9-460d-881b-56048c8374db` 的逐页查看发现第 8 题流程图与选项跨页、题目区最后一页仅有第 24 题。隔离试排后缩小第 8、20、22 题图的绘制尺度，并对第 24 题设置局部保留空间；题面逐题内容哈希不变，来源校对的题面及图形文件哈希已更新。试排实际查看相关页：第 8 题图与选项同页，第 24 题与前题同页。旧 attempt 的实际查看记录及审查模板归档于 `.work/phase4-b41/review-history/`。

正式重建返回 `COMPILED_PENDING_REVIEW`，新 attempt `4e311e00-942f-4ac7-be9c-8c0879e12b1e`、manifest revision 5418；四版分别 6、21、8、17 页，共 52 页。当前回执检查无 missing、invalid 或 stale，但新 attempt 尚未逐页验收；仍须重渲染并实际查看变化页。第 11、16、19 题的三个阻断继续开放。

## 当前构建视觉验收

对 attempt `4e311e00-942f-4ac7-be9c-8c0879e12b1e` 的 52 页进行验收：其中 32 页由审查员按 110 dpi 整页实际查看，另外 20 页的 PNG 哈希与上一 attempt 实际查看并通过的页面字节一致，继承其结论。第 8 题流程图及选项同页、第 24 题并入前页，简答第 11 题显示 U、第 19 题第（2）问显示未定及独立同分布条件。第 6、12 题个别选项续行顶格，未见裁切重叠。逐页审查记录和图片哈希保存在 `.work/phase4-b41/review-render/`，正式回执绑定当前构建和 PDF。

`finalize-batch` 返回 `FINALIZED`、`closed_with_blockers`，revision 5419；最终构建与视觉回执、provenance、规范源、共享内容、简答、入口和 CSV 检查通过。paper 保持 `blocked`，`ISSUE-1245`、`ISSUE-1246`、`ISSUE-1247` 仍开放；视觉通过不消除这些内容问题。

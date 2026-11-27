# 2006 北京文科候选卷：题图与逐题 provenance

日期：2026-10-30

## 固定源与图稿

- 依据固定候选 PDF 普通高考/2006/2006北京文.pdf（source ID src-48c4e852d76caf4118f9d92691883137983f1f132326a07ee8d5da7707668347，SHA-256 476c44dd673847bcf6b5a3f940cdf464720fcf89d4a7096d8c531b27327813ec）第1页（印刷页282）放大核对并重绘三幅 TikZ 图。
- Q8 保留路口 A、B、C 与路段变量 x1、x2、x3，环岛方向为 A→B→C→A；外部流量按源图箭头标为 A 流入50/流出55、B 流入30/流出20、C 流入30/流出35。
- Q16 重绘坐标轴、向上开口曲线及 x=1、x=2 两个横轴交点。曲线只表达源图中的示意特征，不作为精确函数曲线。
- Q17 重绘正四棱柱 ABCD-A1B1C1D1、隐藏棱、题图所示底面对角线与线段 BC1；透视比例为示意，不表达长度条件。
- 新增 2006_北京卷_文科/figures/f2006_beijing_arts_q08_traffic_island.tex、f2006_beijing_arts_q16_derivative_graph.tex、f2006_beijing_arts_q17_square_prism.tex。规范题面以独立 Markdown 本地 .tex 链接指向本卷 figures/；项目生成器据该链接动态映射，无需修改共享 FIGMAP。manifest 登记每图 expected_occurrences=2，分别对应题面与确定性含解析稿。
- sync-figure-registry 将三图登记到 manifest，revision 5480→5481；确定性含解析稿已由 solution_sources extract-batch 重建。

## 逐题 provenance 与状态

- provenance.py import-batch 将 Q1—Q20 三角色记录导入本卷 provenance.json。每题绑定固定 source ID、SHA-256 和页码；Q1—Q17 映射 PDF 第1页，Q18—Q20 映射第2页。答案证据标为 D 级本库独立推导，盲解结论一致，非官方；official_answer=null。
- 角色按可追溯工作职责命名为 phase1-b60-second-transcription-reader、phase1-b60-primary-solution-author、phase1-b60-independent-blind-solver-cohort；姓名未记录，不从历史描述推断人员身份。Q8/Q16/Q17 的新 TikZ 图稿由主流程对照固定源页绘制，尚无第二读者对这三份新图稿的专项复核，后续正式页面校样仍须检查。
- provenance 导入及生成状态对齐后，manifest revision 为5484；paper 为 editions_generated，batch 为 provenance_verified。index 说明已同步标出三图与20题 provenance 已登记，但正式构建和视觉校样未完成。

## 验证边界与后续

- provenance、solution-source 20题对齐、generate_projects --check、make_short_answers --check、make_editions --check 均通过。manifest CSV 曾因 revision 更新短暂过期，已从 manifest 重新生成775行；全库报告投影已刷新。
- 本阶段未生成正式 PDF、build/review receipt 或逐页视觉结论；未运行测试套件。固定 PDF 的发布者、出版者、版次、来源链与官方身份仍未核实。
- 下一步按 phase1-b60 运行四版正式构建，再对所有变更页做视觉检查并建立当前 build/review 回执。本阶段仅完成题图、provenance 与确定性装配，不代表本卷验收，更不代表1952—2026长期语料库完成。

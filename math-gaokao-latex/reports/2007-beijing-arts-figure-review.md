# 2007 北京文科候选卷：Q13/Q17/Q19 题图矢量重绘与独立核对

- 日期：2026-11-03。
- 固定 source：`src-71817304e261efb7deaf51c2a5f400421a95ac91a90313d8f558bee701a624f9`，PDF SHA-256 `e5356797259eb22cc2b4f23019ad7ab044f282bdfc2a65df94dbbdcc502cfff5`。图稿依据 PDF 第1页 Q13/Q17 和第2页 Q19。
- 题图为项目本地 TikZ 源，分别链接到规范题面 Q13、Q17、Q19；确定性 `_含解析.md` 随后重生。manifest 登记三张图各 `expected_occurrences=2`，对应事实题面和合并稿各一处；生成的 `questions.tex`、`answers.tex` 均引用这三张图。

## 源图对照

- **Q13 PASS**：原页显示外正方形、旋转的中心小正方形，以及从外方形四角连到中心方形四顶点的八条斜边。TikZ 用四条折线划分为四个全等直角三角形并闭合中心方形。原图无角标、点名或其他文字标记，图稿未增加。
- **Q17 PASS**：原页外轮廓为 `A-C-B-A`；`D` 在 `AB` 上，`CD` 为实线；`AO`、`OB`、`OC`、`OD` 为虚线，`O` 处有直角小方框。图稿逐项保留，点名与题干的旋转/直二面角构型相符，没有多余几何标记。
- **Q19 PASS**：原页显示倾斜矩形 `ABCD`，`M` 在正 `x` 轴、`N` 在负 `x` 轴，`T` 位于 `AD` 延长线上，`O` 为原点；两坐标轴带箭头并标 `x/y`。图稿保留矩形、`AD` 延长线、坐标轴和点标，且与题设 `M(2,0)`、`N(-2,0)`、`T(-1,1)` 的相对位置一致。

独立复核者 `/root/review_2007_beijing_arts_figures`（Luna/high）只读取固定源图裁片、题面 Q13/Q17/Q19 与三个 TikZ 文件，未读取答案要点、解析正文或含解析稿，也未修改文件；逐图 PASS 结论及原图细节均由其独立核对。

## 登记与验证

- 三张图的单独段落链接位于 `_试题.md`；生成 `_含解析.md` 后，`source_manifest.py sync-figure-registry --write` 将三图各登记为两处引用。首次同步早于合并稿刷新，`generate_projects` 因清单计数 1、实际计数 2 正确拒绝；合并稿更新后重跑同步，计数对齐。这一顺序约束已补入 [OCR 工作流](../docs/OCR_WORKFLOW.md)。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check` 均通过；生成器确认题目和答案 TeX 使用本卷三张本地图。
- 当前规范题面 full-file SHA-256 为 `428c92e4a0d0f0e1d8d8197e96429734f2425c9e6eea4a368fe86496f36f2500`；其余文字题干未改，只把三个图位替换为明确的本地图稿链接。

本阶段只完成题图源图对照、矢量图稿与映射/生成器/manifest 同步。正式 LaTeX 四版构建、输出 PDF 页面视觉复核、provenance 导入与批次闭环仍待完成；Q18 `ISSUE-1355` 继续阻断整卷完成，来源官方身份未认证。

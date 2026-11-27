# 2006 天津理科：题图重绘与来源核对

- 日期：2026-11-02；批次 phase1-b67；paper gk-2006-regular-tianjin-science。
- 固定 PDF 位于 `gaokaomath-src/普通高考/2006/2006天津理.pdf`，SHA-256 `b38a31042aaadb71d602486419cd5f999ff607dfd5ae3f01eb95f5fd8c253039`，与 manifest artifact 一致。逐页渲染检查第 1 页 Q9/Q13/Q17、第 2 页 Q19/Q22；五图均按源图可见结构重绘。
- 登记图稿及 SHA-256：Q9 `2006_天津卷_理科/figures/q09.tikz.tex` `a9cbef6135643bacfcccbdc33b29bb070b94dd8981d9b6aff64fd4d96215c625`；Q13 `.../q13.tikz.tex` `8970e0387837fd002020a4ab1a865dc56f053b579c1451e1499421ea0349f287`；Q17 `.../q17.tikz.tex` `432961afeaac40e86be112ee7a44d34ceed6f0d5415f5774ea97394137b38678`；Q19 `.../q19.tikz.tex` `153d544645d0595e70db36122b050c98385d7c72e27c5755f5ab22ce9059fff1`；Q22 `.../q22.tikz.tex` `bed467b0c32a49e75ce7c1e281df669ea1f7a2fab4c233f99c32e9d131926a38`。
- Q9 保留定义域端点空心、虚线投影、三次穿轴及 O 处相切；Q13 保留正三棱柱可见/隐藏棱及 AC、AC1 虚线；Q17 仅示意三角形顶点拓扑；Q19 保留源图虚实关系与 O。Q19 的 FO、EO、FD 按图面虚线照录，原页无法仅凭线型判定其是否为棱或辅助线。Q22 参数取 a=1、b=(sqrt(5)-1)/2、c=sqrt(b)，满足 c²=ab；A、B 在 OA 上且分别位于大、小圆，BF 为小圆在 B 处切线。P、Q 使用直线 BF 与椭圆的数值交点 (0.326993, 0.584059)、(0.945027, -0.202093)，仅为便于绘图的近似坐标。
- 规范题面、生成的含解析稿均映射这五份 TikZ；`figure_files` 每图登记两次引用，`sync-figure-occurrences` 对齐。question-review 的五个题面摘要因新增图链而更新，题面内容及答案未改；三角色 provenance 重新导入后 manifest revision 5772，`provenance check-batch` 通过。
- 本报告记录源图对照与图稿身份，不代替 TikZ/四版编译和成品页视觉审查。答案来源仍非官方；Q2 的 ISSUE-1288/1289 与 U 保持不变，paper blocked。

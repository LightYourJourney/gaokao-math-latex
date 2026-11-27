# 2006 湖南理科候选卷：题图重绘、逐题 provenance 与项目同步

- 日期：2026-11-02；paper `gk-2006-regular-hunan-science`；batch `phase1-b75`。
- 固定候选 source `src-74bd6a8b302120c812e3aa287309cf3d3a0cf6217761cc4637696bf4d12817cb`；PDF SHA-256 `ae341d81af084449fe66f2f737553001cf04fd1781ad5f47f1a4f5b5da1bbb09`；Git blob `0e7fdec5b934366efe430a192955195c9a82bad4`。以下核对仅绑定本库固定副本，不认证发布者、版次、扫描来源链或官方身份。

## 题图与引用

- Q9：`2006_湖南卷_理科/figures/f2006hunan_science_q9_section.tex`，按固定原页重绘截面圆和三角形。其几何解释为底边取正四面体一条棱、顶点取对棱中点；图稿只表达截面关系，不标尺寸。
- Q15：`2006_湖南卷_理科/figures/f2006hunan_science_q15_vector.tex`。保留 O、A、B、P、M 与射线/边界线型；原图没有独立平行刻痕，`OM∥AB` 取自题干文字。未添加长度或角度数值。
- Q16：`2006_湖南卷_理科/figures/f2006hunan_science_q16_triangle.tex`。保留直角三角形 ABC、斜边点 D、AD、直角符号及 α、β 的位置；绘图不表达精确比例。
- Q18：`2006_湖南卷_理科/figures/f2006hunan_science_q18_pyramids.tex`。保留两个共底正四棱锥、原页的顶点命名及可见/隐藏棱；P、Q 位于底面两侧按固定原页图示绘出。坐标和高度不按比例。
- 四图均仅为 TikZ 矢量线稿，没有嵌入扫描截图。规范题面和解析正文分别链接每幅 `.tex` 图稿，`solution_sources.py extract-batch --write` 重建含解析稿。manifest `figure_files` 登记四图，每图 `expected_occurrences=3`，与试题版一次、解析版两次的生成引用核对一致；`generate_projects.py` 按规范 Markdown 本地链接动态解析，无共享转换器例外。
- 每幅图均由独立 smoke wrapper 经 XeLaTeX 编译为 1 页 PDF，再渲染 PNG 目视检查标签、线型和边界；检查未见裁切或标签重叠。Smoke PDF 仅用于图稿核对，不是正式版本构建或卷级视觉验收。

## 逐题来源与答案证据

- `provenance.py import-batch --write` 导入 Q1–Q21 的三角色记录，manifest revision `5953→5955`。题面复核角色逐题绑定固定 source ID、SHA-256 与原页号：Q1–Q18 对应 PDF 第 1 页，Q19–Q21 对应第 2 页。答案证据记为本库独立推导（D），独立分段盲核记录于 `reports/2006-hunan-science-answer-derivation.md`。
- Q17 整题答案证据记 U，挂接 `ISSUE-1339`；Q17（3）的约 0.41 仍只在额外假设跨矿复查结果联合独立时成立，题面未明确该条件。不得把条件值写成无条件或官方答案。`official_answer` 保持 null，paper 仍 blocked；batch 派生状态为 `provenance_verified`。

## 验证与未完成项

- 通过：`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --batch phase1-b75`（21 题）、`provenance.py check-batch --batch phase1-b75`（1 卷 OK）、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`。
- 尚未正式 XeLaTeX 构建试题版、解析版、简答版、印刷版；没有正式 build/review receipts，也未作全卷逐页视觉审阅或运行全量测试。上述 smoke 检查不替代这些门禁；本报告不表示本卷验收或 1952–2026 题库完成。

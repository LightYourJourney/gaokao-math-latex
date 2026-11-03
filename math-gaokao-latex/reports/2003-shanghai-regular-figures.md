# 2003 上海普通卷文理科：Q16/Q18/Q20 题图矢量重绘

- 日期：2026-11-04。
- 文科固定来源：`src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4`，PDF SHA-256 `ffd59c395a0c675118f6da576e48842549c4afa031d923448f26f33087bc7e85`；图稿对应 PDF 第 1 页（印刷页 140，Q16/Q18）和第 2 页（印刷页 141，Q20）。
- 理科固定来源：`src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0`，PDF SHA-256 `88b72fea05d331215504bb89257e375d07c18ba21e830cf9e6288461e88ccf8d`；图稿对应 PDF 第 1 页（印刷页 138，Q16/Q18）和第 2 页（印刷页 139，Q20）。

## 产物与指纹

| 科类 | 题号 | 图稿 | SHA-256 |
|---|---:|---|---|
| 文科 | 16 | `2003_上海卷_文科/figures/f2003_shanghai_arts_q16_function_graph.tex` | `71b280f2d6ac5013e7e3ebf5a38e75a78f62cea6025e55b01ed5832e7993a8e8` |
| 文科 | 18 | `2003_上海卷_文科/figures/f2003_shanghai_arts_q18_parallelepiped.tex` | `bae8a36500c4d374eba7f2c4e4c01ce128f4a492f239f4e2fc913c5ca22454cb` |
| 文科 | 20 | `2003_上海卷_文科/figures/f2003_shanghai_arts_q20_tunnel_cross_section.tex` | `e5c1540de79139df57fbe74a0bc2593af8a2843afdd28fcdb62b7d6733f530d6` |
| 理科 | 16 | `2003_上海卷_理科/figures/f2003_shanghai_science_q16_function_graph.tex` | `86bc2bbe54ff6c2c7b68c8fa85507c43716c96273db6c3d40060f8a8608d61e2` |
| 理科 | 18 | `2003_上海卷_理科/figures/f2003_shanghai_science_q18_parallelepiped.tex` | `92542c5a428eb356fe463c725f08c1d97f8262013df36e93d4265a6489775a69` |
| 理科 | 20 | `2003_上海卷_理科/figures/f2003_shanghai_science_q20_tunnel_cross_section.tex` | `26da0c4cfed5be993c4f6f4121c23e8a49b4b7dfc76416c48962a20bdf4223c6` |

六个文件均记录 Generator、source ID、源 PDF SHA-256、PDF 页码/印刷页码和题号。图稿保留源图的可见拓扑、标签及尺寸线；坐标、曲线具体形状、车道虚线间距和图形比例仅作示意，不代表题设给出的精确坐标或长度比例。

## 编译与视觉复核

- 六个 TikZ 片段均用 XeLaTeX 独立编译成功；以 `ctexart`、`ctex`、TikZ 建立预览 harness，CJK 单位标记“单位：米”可见。编译器为 XeTeX 3.141592653-2.6-0.999998（TeX Live 2026）。
- 主会话逐图将预览与固定 PDF 原页/裁图对照：Q16 的零点在 `(-c,-2)`、`(0,0)`、`(2,c)`，极值水平为 `y=±2`，且端点 `x=±c` 与竖虚线对应；Q18 的八顶点标签、实棱、隐藏虚棱和 `B_1D` 虚线均对应原图；Q20 的半椭圆、坐标轴、单位、`4.5` 水平虚线/尺寸、`22`、`l`、`h`、车道虚线和 `h` 顶部引线均可见。
- 初版 Q16 曾把 `x=±2` 误画成零点。按源图复核后已于提交 `06ec53ca` 修正为零点位于 `(-c,-2)` 与 `(2,c)`；答案 B 不变。Q20 初版漏掉 `h` 顶部水平引线，现已补齐，并用 CJK harness 检查了单位字样。
- 本阶段未调用 OCR、联网或模型；未运行测试套件。编译预览与源图视觉比对记录保存在忽略目录 `.work/phase4-b47/figure-review/root-final-ctex/`。

## 尚未完成

- 图稿尚未链接进规范 `_试题.md`，manifest `figure_files`、生成器登记及逐题 provenance 还未更新；目前来源仍为未认证候选，`official_answer=null`。
- 两卷 Q14 仍为 U/PENDING。下一阶段将把复核后的题面规范化为 `_试题.md`，链接六张图，完成内部 paper/batch/issues 登记和 `_含解析.md` 派生；随后登记 figure occurrences、逐题 provenance、构建及视觉回执。

本报告只记录六张题图的源码与预览，不表示来源认证、答案官方性或整卷验收完成。

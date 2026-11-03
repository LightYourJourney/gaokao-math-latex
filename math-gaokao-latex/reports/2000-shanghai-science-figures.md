# 2000 上海理科候选卷：Q8/Q18/Q20 题图矢量重绘

- 日期：2026-11-03。固定 source `src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8`，PDF SHA-256 `b798af61afdac624589769db5bbafe734aa9a0016973bd00b3f5bc8028ab3a40`，Git blob `493b64433fdd83bb4f13a587a8e12a53b2a447e9`。Q8、Q18 在 PDF 第1页（印刷页70），Q20 在 PDF 第2页（印刷页71）。该绑定只固定本库采用的候选文件，不认证发布者、版次、复制链或官方身份。
- 按题图工作流完成三份手工 TikZ 矢量源；每份文件头记录 generator、source ID、PDF SHA、PDF 页和题号：`2000_上海卷_理科/figures/f2000_shanghai_science_q08_graph.tex`、`f2000_shanghai_science_q18_tetrahedron.tex`、`f2000_shanghai_science_q20_robot_axes.tex`。

## 原页可见信息与重绘边界

| 题号 | 固定原页可见信息 | 不补入的内容 |
|---|---|---|
| Q8 | 坐标轴 $O,x,y$、横纵轴刻度1和2、线段 $A(0,2)B(1,1)$ 及端点标签。 | 不向线段区间外延伸函数图，不补点标记。 |
| Q18 | 四面体 $ABCD$ 与 $E\in AC$；实线 $CA,CD,DA$，虚线 $CB,BA,BD,BE$。 | 透视图只表示拓扑，不据此推断长度、角度或垂直关系；题设中的垂直与长度仍以文字为准。 |
| Q20 | 坐标轴 $O,x,y$；$x=4$、$x=17$、$y=4$ 三处刻度。 | 不加机器人、小球、起点、轨迹、运动方向或路径。 |

## 规范源、登记和视觉核对

- 在规范 `_试题.md` 中将三张 `.tex` 文件各以独立 Markdown 段落链接到对应题目，并将原先的待重绘说明更新为完成说明。运行 `solution_sources.py extract-batch --manifest math-gaokao-latex/source-manifest.json --batch phase4-b42 --write`，确定性刷新 `_含解析.md`。
- 运行 `source_manifest.py sync-figure-registry --manifest math-gaokao-latex/source-manifest.json --paper gk-2000-regular-shanghai-science --write`，manifest revision `6088→6089`。三个 `figure_files` 均由 Markdown 链接及目录内容派生，`expected_occurrences=2`（规范题面与当前合并稿各一次）；没有手填引用计数。`manifest.csv` 无需变更，仍为775行。
- 以 XeLaTeX 编译三张单图预览，合并为三页 PDF，再以 Poppler 180 dpi 渲染；逐页与固定 PDF 两页目视对照。线段端点和标签、四面体虚实线、坐标刻度均与原页一致，无新增图面事实或裁切。忽略目录预览为 `.work/phase4-b42/figures/figure-preview.pdf`，3页，SHA-256 `22b7f52881e23d236b0deadce16cb3b2fc8df593232803af75eac5540427de96`；它仅用于核图，不是正式试卷 PDF 或构建回执。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）及 `manifest_csv.py --check` 均通过；CSV 为775行。固定 PDF 有可读文字层，本阶段未运行 OCR 模型。

## 未完成项

本阶段只完成三张题图、规范题面映射、合并稿刷新和 manifest 图稿登记。逐题 provenance 尚未导入；项目 TeX、简答、四版入口、正式 PDF 构建及逐页视觉回执尚未完成。Q12“等此数列”和 Q21 指数2疑点仍各由 `ISSUE-1369`、`ISSUE-1370` 阻断，答案保持 U/PENDING，`official_answer=null`，paper 仍为 blocked。本阶段不表示来源认证、整卷闭环或长期语料完成。

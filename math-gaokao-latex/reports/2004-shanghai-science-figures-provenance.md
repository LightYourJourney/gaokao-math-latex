# 2004 上海理科普通卷：Q5/Q18/Q21 题图重绘与登记

- 日期：2026-11-04。
- 批次/试卷：`phase4-b46` / `gk-2004-regular-shanghai-science`。
- 固定候选来源：`src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a`，PDF SHA-256 `9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e`，上游路径 `普通高考/2004/2004上海理.pdf`，共2页，原件印刷页198–199。发布者、版次、复制/扫描链与官方身份未核。

## 重绘记录

三张图来自固定候选 PDF 第1页（印刷页198，Q5/Q18）与第2页（印刷页199，Q21）。TikZ 文件头记录 source ID、来源 SHA-256、页码与题号。

| 题号 | TikZ 文件 | SHA-256 | 原图可见内容与处理 |
|---|---|---|---|
| Q5 | `2004_上海卷_理科/figures/f2004_shanghai_science_q05_function_graph.tex` | `055d4d475c724c396b0de371bdbadbc3912b44b53cdedcff072cdbf635b4f8cc` | 坐标系、原点 $O$、函数在 $[0, 5]$ 上曲线（$[0, 2]$ 在上方，$(2, 5]$ 在下方）、点 $2$ 标注、虚线对应 $x=5$ 与实心端点。 |
| Q18 | `2004_上海卷_理科/figures/f2004_shanghai_science_q18_frame_geometry.tex` | `3310da6e5d8715473ecf18ccd305d09a80513cbb7659d97c3f234ed782f8bc55` | 下部矩形（底边 $x$、高 $y$）及中横木、上部以 $x$ 为斜边的等腰直角三角形，顶角标直角记号。 |
| Q21 | `2004_上海卷_理科/figures/f2004_shanghai_science_q21_pyramid_frustum.tex` | `d7857340a6c0c4b79740f976a8a04b0c3e7e2daa2209d70be712575a5ee65dc2` | 正三棱锥 $P-ABC$、截面 $DEF$；底面虚线 $AC$、截面虚线 $DF$、辅助线虚线 $DC$、辅助线实线 $DB$、实线棱 $PA, PB, PC, AB, BC, DE, EF$。 |

几何示意只按原图可见线条与标记重绘，不声明示意长度、角度或透视比例为题设条件。

## 预览与登记

- 三个独立预览均通过 TikZ/XeLaTeX 语法核验；
- 规范题面 `_试题.md` 中 Q5、Q18、Q21 的占位说明已分别替换为独立段落的 TikZ 文件链接。`solution_sources.py extract-batch --manifest source-manifest.json --batch phase4-b46 --write` 刷新确定性 `_含解析.md` 并通过 `check-batch`。
- `source_manifest.py sync-figure-registry --manifest source-manifest.json --paper gk-2004-regular-shanghai-science --write` 更新 manifest revision `6124→6125`。三图在 manifest 中登记完整，引用计数均正确建立为 2（试卷版 + 解析版各 1 次）。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch` 与 `manifest_csv.py --check` 均通过。CSV 保持 775 行。
- 本卷固定来源 PDF 有文字层；本阶段未调用 OCR 模型或外部 OCR 服务。

## 未完成事项

`ISSUE-1386`（Q19(2) 集合符号脱节疑点）与 `ISSUE-1387`（Q22(1) 点 $P_1(3, 0)$ 不在椭圆上且推导无解疑点）仍为 U/PENDING 并阻塞整卷完成。固定 PDF 不含官方答案页，`official_answer=null`。本阶段没有导入 provenance，没有生成项目 TeX、四版 PDF、正式构建回执或视觉回执；后续阶段仍需分别完成 provenance、TeX 生成、正式构建和逐页视觉验收。本报告不表示来源认证、整卷完成或长期语料库完成。

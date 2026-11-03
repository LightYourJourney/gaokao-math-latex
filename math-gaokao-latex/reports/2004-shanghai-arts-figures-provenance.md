# 2004 上海文科普通卷：Q5/Q18/Q20/Q21 题图重绘与登记

- 日期：2026-11-03。
- 批次/试卷：`phase4-b45` / `gk-2004-regular-shanghai-arts`。
- 固定候选来源：`src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290`，PDF SHA-256 `4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad`，上游路径 `普通高考/2004/2004上海文.pdf`，共2页，原件印刷页200–201。发布者、版次、复制/扫描链与官方身份未核。

## 重绘记录

四张图来自固定候选 PDF 第1页（印刷页200，Q5/Q18）与第2页（印刷页201，Q20/Q21）。TikZ 文件头记录 source ID、来源 SHA-256、页码与题号。

| 题号 | TikZ 文件 | SHA-256 | 原图可见内容与处理 |
|---|---|---|---|
| Q5 | `2004_上海卷_文科/figures/f2004_shanghai_arts_q05_function_graph.tex` | `2517fdebec6048cca898d7ee1b9c54a49e2727040cd25a6df340f2214ff41a98` | 坐标系、原点 $O$、函数在 $[0, 5]$ 上曲线（$[0, 2]$ 在上方，$(2, 5]$ 在下方）、点 $2$ 标注、虚线对应 $x=5$ 与实心点。 |
| Q18 | `2004_上海卷_文科/figures/f2004_shanghai_arts_q18_frame_geometry.tex` | `e4954761a2c30dc2a40f552a22c0b95a985e53e30fb8076152b93a0b50edb33b` | 下部矩形（底边 $x$、高 $y$）及中横木、上部以 $x$ 为斜边的等腰直角三角形。 |
| Q20 | `2004_上海卷_文科/figures/f2004_shanghai_arts_q20_parabola_geometry.tex` | `7119d5819693a011c1794aa573760a5dcef829d23ef34bc7767c9e8deca6f3bb` | 坐标系、原点 $O$、抛物线 $y=\frac{1}{8}x^2-4$、直线 $y=\frac{1}{2}x$、交点 $A, B$、直线 $y=-5$、垂直平分线交点 $Q$。 |
| Q21 | `2004_上海卷_文科/figures/f2004_shanghai_arts_q21_pyramid_frustum.tex` | `06a607d751412ac6fb4538eb5609a94295a5e12252df27eded59c7163eb4e031` | 正三棱锥 $P-ABC$、截面 $DEF$；底面虚线 $AC$、截面虚线 $DF$、实线可见棱 $PA, PB, PC, AB, BC, DE, EF$。 |

几何示意只按原图可见线条与标记重绘，不声明示意长度、角度或透视比例为题设条件。

## 预览与登记

- 四个独立预览均由 XeLaTeX 编译为单页 PDF，输出在忽略目录 `.work/ocr-local/2004-shanghai-arts/figure-preview/`；随后以 `pdftoppm -png -r 180 -singlefile` 导出 PNG，并逐幅与固定来源原页裁片目视比对，全部一次性编译成功，几何结构与标签完全吻合。
- 规范题面 `_试题.md` 中 Q5、Q18、Q20、Q21 的占位说明已分别替换为独立段落的 TikZ 文件链接。`solution_sources.py extract-batch --write --manifest source-manifest.json --batch phase4-b45` 刷新确定性 `_含解析.md` 并通过 `check-batch`。
- `source_manifest.py sync-figure-registry --manifest source-manifest.json --paper gk-2004-regular-shanghai-arts --write` 更新 manifest revision `6118→6119`。四图在 manifest 中登记完整，引用计数均正确建立。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch` 与 `manifest_csv.py --check` 均通过。CSV 保持 775 行。
- 本卷固定来源 PDF 有文字层；本阶段未调用 OCR 模型或外部 OCR 服务。

## 未完成事项

`ISSUE-1384`（Q17 实数无解疑点）与 `ISSUE-1385`（Q19(2) 集合符号脱节疑点）仍为 U/PENDING 并阻塞整卷完成。固定 PDF 不含答案页，`official_answer=null`。本阶段没有导入 provenance，没有生成项目 TeX、四版 PDF、正式构建回执或视觉回执；后续阶段仍需分别完成 provenance、TeX 生成、正式构建和逐页视觉验收。本报告不表示来源认证、整卷完成或长期语料库完成。

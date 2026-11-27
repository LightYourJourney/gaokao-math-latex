# 2005 上海理科普通卷：Q11/Q17/Q19 题图重绘与登记

- 日期：2026-11-03。
- 批次/试卷：`phase4-b44` / `gk-2005-regular-shanghai-science`。
- 固定候选来源：`src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e`，PDF SHA-256 `092e8e90dc1430ab2fa8b8ce79e072e317559e6bef29f1cb7461e9423925ec31`，上游路径 `普通高考/2005/2005上海理.pdf`，共2页，原件印刷页262–263。发布者、版次、复制/扫描链与官方身份未核。

## 重绘记录

三张图均来自固定候选 PDF 第1页（印刷页262）。TikZ 文件头记录 source ID、来源 SHA-256、页码与题号。

| 题号 | TikZ 文件 | SHA-256 | 原图可见内容与处理 |
|---|---|---|---|
| Q11 | `2005_上海卷_理科/figures/f2005_shanghai_science_q11_prism_assemblies.tex` | `7cbc28fea21027458f42b10e019eeb901013a3029cda4d2f4b34f0ecde402d41` | 保留并排的两幅相同棱柱线图、标注 `3a,4a,5a,2/a` 和虚线隐藏棱；不把两图解释为不同拼合拓扑。 |
| Q17 | `2005_上海卷_理科/figures/f2005_shanghai_science_q17_trapezoidal_prism.tex` | `5afe0fe52ea0b2027f8088e45827443a4cb546da0f19062c940f19fe393f640c` | 保留直四棱柱的顶点标记、隐藏棱，以及原图中的虚线对角线 `BC_1`。 |
| Q19 | `2005_上海卷_理科/figures/f2005_shanghai_science_q19_ellipse_geometry.tex` | `23ccf0d64ba0f59e7348844c7e942d5e246995dec1b596f5b5b26000cbe55892` | 绘出椭圆、坐标轴、`A,B,O,M,F,P` 标记及线段 `AP,PF`。 |

几何示意只按原图可见线条与标记重绘，不声明示意长度、角度或透视比例为题设条件。

## 预览与登记

- 三个独立预览均由 XeLaTeX 编译为单页 PDF，输出在忽略目录 `.work/ocr-local/2005-shanghai-science/figure-preview/`；随后以 `pdftoppm -png -r 180 -singlefile` 导出 PNG，并逐幅与固定来源原页裁片目视比较。
- Q11 预览的第一轮独立编译发现标准 `article` math 环境没有 `\dfrac` 命令；图稿改用基础 `\frac` 后，最终三张预览均成功编译。该过程不涉及正式项目 TeX 或正式 PDF 构建。
- 规范题面 `_试题.md` 中 Q11、Q17、Q19 的占位说明已分别换成独立段落的 TikZ 文件链接。`solution_sources.py extract-batch --write --manifest source-manifest.json --batch phase4-b44` 刷新确定性 `_含解析.md` 并通过 `check-batch`。
- `source_manifest.py sync-figure-registry --manifest source-manifest.json --paper gk-2005-regular-shanghai-science --write` 更新 manifest revision `6110→6111`。三图 `expected_occurrences` 均为2，分别对应规范题面与合并稿。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`、`manifest_csv.py --check` 与 `report.py check --all` 均通过。CSV 仍为775行；六个全库报告已按当前 manifest 重生成并回读校验。
- 本卷固定来源 PDF 有可用文字层；本阶段未调用 OCR 模型或外部 OCR 服务。

## 未完成事项

Q11 并列端点问题 `ISSUE-1380`、Q20(1) 原文“中低价层”疑点 `ISSUE-1381` 仍为 U/PENDING，并继续阻塞整卷完成。固定 PDF 不含答案页，`official_answer=null`。本阶段没有导入 provenance，没有生成项目 TeX、四版 PDF、正式构建回执或视觉回执；后续阶段仍需分别完成答案/解析来源核查、provenance、正式构建和逐页视觉验收。本报告不表示来源认证、整卷完成或长期语料库完成。

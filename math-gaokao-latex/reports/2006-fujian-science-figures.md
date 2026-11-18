# 2006 福建理科候选卷：Q16/Q18/Q20 矢量图阶段

- 日期与批次：2026-11-03，phase1-b77。
- 工作树：工作分支；paper：gk-2006-regular-fujian-science。
- 固定题面：source ID src-ab0f2729ee4a24495e653b44c14438b4130f8b38b11362bf84251f3595a09d27，SHA-256 50d17546b94af82fb2cee653942752914cd387fe72792d74ffa5f75e7a301d83。

## 图稿

- Q16：2006_福建卷_理科/figures/f2006fujian_science_q16_midpoint_triangles.tex，展示题面坐标三角形及两层中点三角形。
- Q18：2006_福建卷_理科/figures/f2006fujian_science_q18_tetrahedron.tex，展示四面体、隐藏棱及 O、E 中点标注。
- Q20：2006_福建卷_理科/figures/f2006fujian_science_q20_ellipse_chord.tex，展示椭圆、焦点/坐标轴、弦与垂直平分线；示意弦方向仅用于布局，不作为题设条件。

每个 TikZ 源文件都注明固定 PDF 的 source ID、SHA、页码和题号。三张独立预览均由 XeLaTeX 编译，使用 Poppler 渲染 PNG，并目视确认标签及线型可辨、示意没有引入额外条件。预览产物位于 ignored .work/ocr-local/next-paper/figure-preview/，不进入提交。

## 来源链接与登记

题面和解析正文各为每图保留一条 Markdown 链接；solution_sources.py extract-batch --write 从解析事实源生成含解析稿后，合并稿中每图在题面、解析各出现一次。sync-figure-registry --write 从规范 Markdown 链接计算清单，manifest revision 5972→5973；三张图的 expected_occurrences 均为 3。试题与解析事实层均未由合并稿反向覆盖。

## 验证

- python3 tools/source_manifest.py validate --manifest source-manifest.json：退出0。
- python3 tools/solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b77：1卷、22题通过。
- python3 tools/issues.py validate --file math-gaokao-latex/missing-issues.md：退出0。
- python3 math-gaokao-latex/tools/manifest_csv.py --check（从仓库根运行）：当前，775行。
- 成本：本阶段未触发 OCR 或外部模型调用；本地绘图成本未单独计量。

## 未完成门禁

本报告只覆盖三张矢量图及其引用登记。逐题 provenance、TeX 项目生成、四种版本正式构建、全部改动页视觉审查、正式 receipt 和卷级最终状态仍待后续阶段。固定候选 PDF 的发布者、出版者、版次、来源链及官方身份未核；没有答案页，official_answer=null。

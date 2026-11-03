# 2003 北京普通文理卷：题图矢量重绘

- 日期：2026-11-04；批次：`phase4-b48`。
- 文科固定候选 source `src-dcc6a2c21c7b8e7b8f23f5188f34d7f542f94e40f4219b54cfb85a0d7004bc0f`，PDF SHA-256 `7fc0fd289fc486a0ae1c16a9ab5b4f0561830897df6e8897c50666f03d511913`；PDF 页 1/2 对应印刷页 126/127。
- 理科固定候选 source `src-120ea104f8cb373f5731039fa9d36469df457869849f27420831962ef1ad2306`，PDF SHA-256 `d0081500bd56d03199ddcf232fe8e870f2ecd7e9c41ba849417af9af79fbb702`；PDF 页 1/2 对应印刷页 124/125。
- 本次实测两份来源 PDF SHA-256 与 manifest 绑定值一致，各两页 A3 横向。此处的 canonical 固定输入不认证发布者、版次、复制/扫描链或官方身份。

## 图稿与指纹

| 科类 | 题号 | 固定来源页 | TikZ 文件 | SHA-256 |
|:--|--:|:--|:--|:--|
| 文科 | 5 | PDF 1 / 印刷 126 | `2003_北京卷_文科/figures/f2003_beijing_arts_q05_ellipse_focus.tex` | `d63e0b7f022f7840df0662d39071128b559778b0be6e07ed75500a33f578b329` |
| 文科 | 17 | PDF 1 / 印刷 126 | `2003_北京卷_文科/figures/f2003_beijing_arts_q17_triangular_prism.tex` | `0108ce9ebdde86e91a50a80ef40a457c8df5d0c60b138ce4e79ded9aba231eba` |
| 文科 | 18 | PDF 2 / 印刷 127 | `2003_北京卷_文科/figures/f2003_beijing_arts_q18_ellipse_notation.tex` | `8250092e554e9a7b3089f3777d8c9a86d07b45ea796bbc38d7054e5afb45fd29` |
| 文科 | 19 | PDF 2 / 印刷 127 | `2003_北京卷_文科/figures/f2003_beijing_arts_q19_city_triangle.tex` | `997d9996a53df7aa84f81e3c3c6475d610954f320bbce2364650cb48bd2a69e2` |
| 理科 | 13 | PDF 1 / 印刷 124 | `2003_北京卷_理科/figures/f2003_beijing_science_q13_oblique_cylinder.tex` | `8511c56ab73ab64a560cd16a581d5c09ad91f1a5007109ff82bedcf4a1808c77` |
| 理科 | 17 | PDF 1 / 印刷 124 | `2003_北京卷_理科/figures/f2003_beijing_science_q17_triangular_prism.tex` | `8ef4b8ad1044fa9b584ded4a345c16b35795476db87c1068261bd0e6f2eba27a` |
| 理科 | 18 | PDF 2 / 印刷 125 | `2003_北京卷_理科/figures/f2003_beijing_science_q18_shifted_ellipse_chords.tex` | `bf99d13da7a4f784a409a23bb6cbe860c3111f3e6fe6624621f20691b44597be` |
| 理科 | 19 | PDF 2 / 印刷 125 | `2003_北京卷_理科/figures/f2003_beijing_science_q19_city_triangle.tex` | `60546a39487a9fb4f41bc0369662da1be0e35abdffd8bf7f944a8e45f3615165` |

八个源文件均记录 Generator、source ID、PDF SHA-256、PDF 页/印刷页与题号。坐标、曲线具体形状和三维投影比例只用于重现原图关系，不表示题设未提供的数值。

## 原页核对与预览

- 两名独立复核者分别对照文理两份固定 PDF 的完整页与题图裁片，检查了可见顶点、坐标标签、实虚线及线段连接；未发现既有题面转录复核中的具体标记错误。本次使用现有 300 dpi 页图和题图裁片，没有再次运行 OCR。
- 文科 Q5 保留横椭圆、坐标轴、`F_1`、`O`、上端点 `B` 和穿过 `F_1/B` 的实线；Q17 的 `BC` 与 `C_1D`、`DA_1` 为虚线，`C_1A` 为实线，`D` 不加源图没有的中点刻痕；Q18 保留坐标轴、焦点处刻线及原图 `A_1(-5,0)`/`A(5,0)` 标签，不补画 `A_2`；Q19 保留实线三角形、`P` 位于 `OA` 上和坐标轴关系。
- 理科 Q13 保留下底后半弧与直径 `2r` 的虚线、前半弧实线、左 `b`/右 `a` 母线和斜截口；Q17 保留 `C-B-D` 共线、源图的实/虚线端点组合，且不从图猜补“底面边长的 3”；Q18 保留 `M(0,r)` 的平移椭圆、`A_1/A_2/B_1/B_2`、`O` 与交于 `O` 的两条实弦；Q19 保留 `A/P/O` 的纵向位置、`B(-b,0)`、`C(b,0)` 与实线三角形。
- 八个片段由 XeTeX 3.141592653-2.6-0.999998（TeX Live 2026）编入一个 8 页 `standalone` 预览，编译成功；以 Poppler `pdftoppm -r 160` 渲染后逐图目视检查，无溢出、标签截断或线型缺失。预览 PDF SHA-256：`23908b1b6f0596e68aeec8c4d849087e70c2da1d62b1f4309e6653cd91268678`，保存在忽略目录 `.work/phase4-b48/figure-review/tex-preview/all-figures.pdf`。该图稿预览不是正式四版试卷构建或视觉回执。

## 同步登记与检查

- 文理规范题面中的 8 个占位分别替换为对应 TikZ 文件链接；通过 `solution_sources.py extract-batch --manifest source-manifest.json --batch phase4-b48 --write` 刷新两份 `_含解析.md`。
- 两次 `source_manifest.py sync-figure-registry --write` 分别登记每卷 4 张图；每个 `figure_files` 记录的 `expected_occurrences=2`，对应规范题面与确定性生成的含解析稿。manifest revision `6148→6150`。
- `source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`solution_sources.py check-batch`（两卷各 20 题）、`manifest_csv.py --check`（775 行）及全量报告 currentness 检查均通过。CSV 无需改写，报告投影已按 revision 6150 刷新。
- `provenance.json` 尚未导入；逐题 question-review、answer-solve、answer-review provenance、TeX 项目/四版、正式构建、逐页校样及批次收口均待后续阶段。

## 未决边界

- 文科 Q18 原页首句 `A_1,A_2` 与后文/图示 `A` 不一致；题面和图稿保留差异，答案继续 U/PENDING，关联 `ISSUE-1398`、`ISSUE-1399`。
- 理科 Q17 原页可见“底面边长的 3”，未增补“为”；答案继续 U/PENDING，关联 `ISSUE-1400`、`ISSUE-1401`。
- 四个问题仍为 open / `blocks_completion`；paper 仍 blocked，batch 未关闭。题图重绘不认证来源或答案，不表示单卷、批次或长期语料已完成。

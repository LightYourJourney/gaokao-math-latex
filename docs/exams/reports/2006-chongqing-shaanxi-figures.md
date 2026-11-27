# 2006 重庆、陕西文理候选卷：10 幅题图矢量重绘与登记

- 日期：2026-11-03。
- 范围：`phase1-b80` 四卷共 10 幅题图。四份固定候选 PDF 的现场 SHA-256 与 manifest 绑定值再次一致；来源为仓库内部 canonical 输入绑定，不代表发布者、版次、扫描链或官方身份已认证。四卷 `official_answer=null`。

## 来源与图稿绑定

| 卷别 / 题号 | Source ID | 源 PDF SHA-256 | PDF 页 / 印刷页 | TikZ 源（即矢量图生成源） | 图稿 SHA-256 |
|---|---|---|---|---|---|
| 重庆文 Q20 | `src-bfaf1f0ca2f3b8edd4a2455d39b464722513d2bb05efe36769938f1f187729e5` | `fca2f5abda4a5e4982176417bf2f33b6b248847bffb0dcd09ae089c4f6a85b6e` | p.2 / 287 | `2006_重庆卷_文科/figures/f2006_chongqing_arts_q20_square_prism.tex` | `d8733109b2555c3098c212371cc445178606c4d8c3634a005ae30798edcd9506` |
| 重庆文 Q22 | 同上 | 同上 | p.2 / 287 | `2006_重庆卷_文科/figures/f2006_chongqing_arts_q22_parabola_focus_chords.tex` | `785acfa73e34b00636a5c69b9f21a1fdb00bbefc9593c81f02d3ce9d4d079087` |
| 重庆理 Q6 | `src-5abd831561d7d4fa968c5bf0deb634e0d666376fd8cc90967cf30d301e77a351` | `211d79b8676187c7e4a98c71d7eae5eadd28b2e5aaf9237fefd55a791241faa3` | p.1 / 284 | `2006_重庆卷_理科/figures/f2006_chongqing_science_q06_histogram.tex` | `1e2e73a453bdaf3aaf5970df1db1eb2dc7e2bb676b40355163f2d2718c3a6caf` |
| 重庆理 Q9 | 同上 | 同上 | p.1 / 284 | `2006_重庆卷_理科/figures/f2006_chongqing_science_q09_circle_segment_options.tex` | `02aadea617f11276b616b0d8dcfe38759b84ba6b38f725a00277413319472a28` |
| 重庆理 Q19 | 同上 | 同上 | p.2 / 285 | `2006_重庆卷_理科/figures/f2006_chongqing_science_q19_pyramid.tex` | `8a46a9e60b6ec8018a1e64df5c681ba228dd4cfbcc79087b088e0c057e056391` |
| 重庆理 Q22 | 同上 | 同上 | p.2 / 285 | `2006_重庆卷_理科/figures/f2006_chongqing_science_q22_ellipse_directrix.tex` | `dbf814e27de6b3aa3f76f74b46afc82b2e0e448218b0aa61771d5bf670f393f4` |
| 陕西文 Q19 | `src-d3bb569fc2c589e075c748b1494aaadeaae67bbe0e3926306e123e08de2a5fec` | `ef53636f75f8cef48067ff22478f699a5ac7d3dee4a42f06e01e640bc906d221` | p.1 / 326 | `2006_陕西卷_文科/figures/f2006_shaanxi_arts_q19_two_planes.tex` | `c5558bdd4454b7ea1aff620780dc84e2742443a37d0747c3d4c6c9792af2f3f1` |
| 陕西文 Q21 | 同上 | 同上 | p.2 / 327 | `2006_陕西卷_文科/figures/f2006_shaanxi_arts_q21_locus_graph.tex` | `3ce4573bbc51e5575eb805947199ad424e4c08d54c5cca034b9b8b9b7c7e3c4f` |
| 陕西理 Q19 | `src-6914e1c400640e0c3ef3785cb187876891213e18557a04ba0e97c2f4dae5a999` | `32093147448a616af26055d81831b7028e661e5138d8546f803a6c6a1a42bc43` | p.1 / 324 | `2006_陕西卷_理科/figures/f2006_shaanxi_science_q19_two_planes.tex` | `737605b95d6f816050d4e7e7c9786f7f193dfb5b4fa89bf28458869e49b95167` |
| 陕西理 Q21 | 同上 | 同上 | p.2 / 325 | `2006_陕西卷_理科/figures/f2006_shaanxi_science_q21_locus_graph.tex` | `4a5dd8726a4423ddbfdef2144374e805c10cfaa42fc20880f2ee6960308b2505` |

每份 `.tex` 首部均记录对应 source ID、完整源 PDF SHA-256、PDF 页码和题号；这些 TikZ 文件是正式装配所用的图稿生成源。四卷规范题面分别在对应题图占位处加入独立 Markdown 链接，确定性 `_含解析.md` 已由 `solution_sources.py extract-batch --write` 重生成。`sync-figure-registry` 干跑分别确认 2/4/2/2 张图；随后四次 state transaction 将每图登记为 `expected_occurrences=2`（题面版与确定性合并版），manifest revision `5996→6000`。`manifest.csv` 保持 775 行且投影当前。

## 源图对照与示意边界

- 重庆文 Q20 保留正四棱柱顶/底面、E 在 BB₁、F 在 DD₁、平面迹 A–E–C₁–F；G 位于 A₁D₁ 延长线上，C₁G 单独绘出。E–C₁ 按原页可见实线绘制，遮挡线用虚线。透视不表达长度/角度；原扫描中 Q20 若干隐藏棱虚实较淡，报告保留该不确定性。
- 重庆文 Q22 按题干关系精确构造示意几何：抛物线 $x^2=4y$，焦点 $F=(0,1)$，每组点取 $x_Ax_B=-4$ 使弦过焦点；Aₙ、Bₙ 处切线按斜率 $x/2$ 绘制并交于 Cₙ。锚点只用于清楚显示拓扑，不声称对应具体 $n$ 值。
- 重庆理 Q6 保留 0 与体重刻度之间的断轴、54.5–76.5 的 2 kg 组界及从 [54.5,56.5) 开始的 11 个柱。高度依据 400 dpi 原页目测近似，没有按像素测量或从柱高推导人数。Q9 保留单位圆弓形及 A–D 四个选项，B/C/D 的 $y=x$ 虚线均在；选项曲线为拓扑/走势示意。Q19 将 E、F 分别放在 PC、CD 的投影中点；三维投影与线段虚实按原页辨读。Q22 仅表达椭圆、右准线、Pₙ、Fₙ/Gₙ 与到准线的水平距离 $d_n$，椭圆参数不表示题设给定值。
- 陕西文、理 Q19 分别对照各自 PDF 重绘相交平面 α、β、交线 l、A/B 与其在 l 上的射影 A₁/B₁；两份图稿保留不同 source ID/SHA。Q21 分别依据两份 PDF 绘制带坐标轴、A/B/C/D/E/M 的折线图。为了呈现三条同参数关系，草图以 $t=0.4$ 作为示例放置 D、E、M；此数值仅为图稿布局示例，不是题目另加条件，也不作为精确比例。

每份 TikZ 片段均使用独立 standalone wrapper 编译预览：重庆文两图用 `pdflatex -interaction=nonstopmode -halt-on-error`；其余八图用 XeLaTeX 同等 halt-on-error 参数；PDF 均由 Poppler 栅格化并目视检查边界、标签、线型和关系。主流程重新打开全部 10 张最终 scratch 预览，并检查对应原页；草稿验证未替代正式卷版构建、正式 PDF 视觉回执或另一读者专项审图。

## 验证与后续

- `source_manifest.py validate`：通过；`issues.py validate`：通过；`solution_sources.py check-batch --batch phase1-b80`：四卷各 22 题通过；`manifest_csv.py --check`：775 行且当前；`git diff --check`：通过。
- 保留 `ISSUE-1341` 至 `ISSUE-1344` 与对应 U/PENDING；无官方答案或候选来源身份结论。production state 未推进为 completed。
- 下一阶段：导入完整三角色逐题 provenance，生成/校验四卷 TeX 项目，执行正式构建与逐页视觉复核，形成当前回执；再根据 blocker 规则决定可否闭合。此阶段不代表四卷验收或 1952–2026 长期语料完成。成本数据未知。

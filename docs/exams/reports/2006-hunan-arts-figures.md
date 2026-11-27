# 2006 湖南文科候选卷：Q10、Q18 矢量图稿

- 日期：2026-11-02。
- 固定候选 source：`src-6387f1664484c2d0ee3ea1a27f673d6624df685f465bfd701fb8e95c0a8b856d`；PDF SHA-256 `64440e801d805005344489ec905572a72a1dd31ffc8206f59867d344bd5b9ce2`；Git blob `c031a5e9f5d5cd83eaa2278036de1e8a3e19bce9`。
- 图稿位于 `math-gaokao-latex/2006_湖南卷_文科/figures/`：Q10 `f2006hunan_arts_q10_vector_region.tex`，SHA-256 `8978b10b9f0b46a16e9679c03ab77ff92d83feb48fde695b3a538b47f05c0318`；Q18 `f2006hunan_arts_q18_pyramids.tex`，SHA-256 `b0ca159cb565109ddd07b342736172da4953399597fe1beed7242c62c61c3ec4`。

## 图稿与源图对照

- Q10 重绘 $O,A,B,M$、向量箭头 $\overrightarrow{OA}$ 与 $\overrightarrow{OB}$、$OM\parallel AB$ 的虚线关系，以及源图灰色区域。额外的未标记角点只用于闭合灰区，不添加题目标签或新数学条件。坐标只复现示意形状，不作为长度比例；选项判断按固定源页灰色区域读取。
- Q18 重绘共底正四棱锥 $P-ABCD$ 与 $Q-ABCD$，保留可见棱、隐藏后棱及 $P,Q,A,B,C,D$ 标注。源图显示两锥顶分处底面两侧；该图示支持解析草稿的相对位置设定，不从图形像素推导边长或高。
- 题面稿与解析稿均已使用本卷内的普通本地 TikZ 链接引用对应图稿；没有把原卷截图插入题库。

## 编译与边界

- 两幅 TikZ 图合入临时 smoke 文档，XeLaTeX 编译成功；生成 2 页 A4 PDF，220 dpi 渲染后逐页目视核对线型、标签、阴影方向和裁切。渲染图与固定 PDF 第 1 页对应的结构一致。临时 PDF 位于 `/tmp/2006-hunan-figure-smoke.pdf`，不是交付产物。
- source 尚未绑定 paper/batch，图稿尚未通过 `source_manifest.py sync-figure-registry` 登记 `figure_files` 与 `expected_occurrences`；尚未生成正式项目 TeX 或四版 PDF，正式页面视觉验收待办。
- 固定文件发布者、版次、扫描传播链及官方身份未核；本阶段只完成题图矢量源稿与隔离编译核对，不表示本卷闭环或长期题库完成。

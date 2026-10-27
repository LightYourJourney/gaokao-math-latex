# 2019 上海春季卷 Q10/Q17 题图矢量初稿

日期：2026-10-27

## 固定来源与重绘

- 来源为 `src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631` 的固定 PDF；本机文件 SHA-256 `432bfb1bfc16c7a915f1349432d1dbcfc151b859ad89e9e3a3f554c5fb768e1d`，与来源清单一致。按 180 dpi 渲染并查看题面 PDF 第 1、2 页的 Q10、Q17 原图；来源出版者、版次与官方身份仍未核。
- Q10 `2019_shanghai_spring_q10_curves.tex`：保留坐标轴、正方形 $OABC$、两条函数曲线、交点 $P,Q$ 与源图各字母。为明确作图取 $a=2>1$，用 $P=(\sqrt{2/3},2)$、$Q=(2,1/\sqrt2)$ 与两条题设函数计算曲线和交点；此参数仅为示意，非答案。图稿 SHA-256 `5374b17383c77b12cdd3ba5a60f88d27cfd773bd15b63cd354e260f33c4148b3`。
- Q17 `2019_shanghai_spring_q17_pyramid.tex`：按源图保留三棱锥 $P-ABC$ 的可见边、虚线底边 $AC$、$PB$ 中点 $M$、$BC$ 中点 $N$ 与线段 $MN$。投影坐标用于示意，两个中点由投影坐标的平均值计算；不把示意图长度当作题设度量。图稿 SHA-256 `dc729cd4d7612810377c6e8b30b17e35647e19cf77e97eb8a1939ce98ad73995`。
- 两图都是 TikZ 路径和文本；题面 Q10/Q17 已以普通 Markdown 链接各引用一次。没有把原卷扫描图片作为题图。

## 局部检查与未完成事项

- 使用 `latexmk -xelatex -halt-on-error -interaction=nonstopmode` 将两图装入临时两页文档，退出码 0；`pdfinfo` 显示 2 页。用 `pdftoppm -r 150` 逐页渲染并目视，图线、虚实关系和标签清楚，无裁切或重叠；`pdfimages -list` 未列出图像对象。临时 PDF、日志和 PNG 存在 `/private/tmp/gaokao2019draw/`，不作为正式交付或收据。
- 主会话另行查看源 PDF 第 1、2 页与两张图稿渲染：Q10 的坐标轴、正方形、两条曲线和 $P,Q$ 对应关系，以及 Q17 的六条棱、$AC$ 虚线、两处中点和 $MN$ 均与源图所示一致；标签可辨。重新从临时 PDF 以 150 dpi 渲染，两页 PNG SHA-256 与受检图逐字节一致；当前两份 TikZ 源 SHA-256 与上列记录一致。
- 来源图注/映射与 manifest `figure_files` 的正式登记、四版生成、正式构建及逐页视觉审查均未完成。题面来源仍未绑定 paper，Q16 轨迹和 Q19（3）源解析的疑点仍待核；不能以此次局部图稿核对代替全卷验收。

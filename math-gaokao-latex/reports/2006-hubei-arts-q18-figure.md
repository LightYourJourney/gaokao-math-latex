# 2006 湖北文科 Q18：题图矢量重绘

- 日期：2026-11-02；paper `gk-2006-regular-hubei-arts`；batch `phase1-b73`。
- 固定来源为 `src-af4cc84c7c2f6c2c1ed0bef598d5a51f57d65a1b25926d7a02631cc6c5387d75`，PDF SHA-256 `b7de4b974a9d512908f6104f3acfdd3785328cd6a1a7ca7ea4578e2fa0d37379`。据 PDF 第1页 Q18 图绘制 TikZ 源 `2006_湖北卷_文科/figures/f2006hubei_arts_q18_prism.tex`，SHA-256 `2a3bcf11868faba17ed0e6d3d74c5628cf476123d4c2db05d702959efe4b64b8`。
- 对照源图可见的实线为棱 BC、BB1、B1C1、CC1、B1A1、A1C1，以及辅助线 B1M、MN；虚线为 BA、AC、AA1、B1C、AM。顶点及 M、N 标注均已录入。坐标为非比例投影示意；没有从图形像素推导题目数据。
- 规范题面以相对 Markdown 链接指向本卷图稿；`solution_sources.py extract-batch --write` 刷新含解析稿后，`source_manifest.py sync-figure-registry` 登记 1 张图、expected_occurrences=2，manifest revision `5931→5932`。登记器要求普通本地链接；Markdown 图片嵌入不会被它计数，故使用项目既有的 `[图稿：…](…tex)` 约定。
- 使用 XeLaTeX 将该图稿单独编译为一页临时 PDF，240 dpi 渲染后目视核对标签、棱线与虚实线；渲染结构与固定源图相符，图中文字清晰，无裁切或相互遮挡。该检查不替代正式版面中的成图检查。
- 本报告确认的是源图结构对照、文件登记、Markdown 映射及隔离图稿编译/目视检查。四版项目装配、正式 PDF 构建与页面验收仍未完成。固定来源身份仍未认证；Q12 的 `ISSUE-1333` 保持开放并阻断卷级完成。

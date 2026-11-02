# 2006 辽宁文理候选卷：题图矢量重绘与登记

- 日期：2026-11-03；批次：`phase1-b78`。只依据固定候选 PDF 重绘题图；来源身份仍未认证。
- 文科固定来源 `src-b784613ebc50375b17eb4a91083b447879ebb9ed75bb6a76227bb74345cfbfd3`，PDF SHA-256 `bbb83af465d4650c594f23a879d82dea43a86f805b6fc8712d25809aac7fda22`：第1页（印刷页310）Q15、Q19。理科固定来源 `src-db3cbfe3d2c96ec3cbe88c45ad7986cf79f4899fd76a3a73b7c64721f0e67569`，PDF SHA-256 `f680814a4fc5835d805772711f91c5921f12fb92b1740b9c0e9279fa6def427a`：第1页（印刷页308）Q18。
- 新增三个手绘 TikZ 图稿：文科 `f2006_liaoning_arts_q15_hemisphere_hexagon.tex`（半球、赤道椭圆、内接正六边形、锥棱与中心点），文科 `f2006_liaoning_arts_q19_folded_square.tex` 和理科 `f2006_liaoning_science_q18_folded_square.tex`（折叠前正方形及折叠后空间示意）。折叠图保留 E/F 中点、固定平面 BCDE、沿 DE 折起的三角形 ADE、题面所涉 AC，以及原图的虚实线关系。三图均标明坐标不按比例。
- 依据原 PDF 页图逐项核对题图标签、边线和虚实线；三个单图预览均以 XeLaTeX 编译为一页 PDF 并渲染 PNG，目检通过。预览和编译日志位于 ignored `.work/ocr-local/liaoning-2006/figure-review/`，不是正式交付 PDF，也没有生成正式构建或视觉回执。
- 图稿链接已写入规范题面和解析源；两份 `_含解析.md` 由 `solution_sources.py extract-batch --write` 派生。文科两图、理科一图均在 `figure_files` 登记，各图 `expected_occurrences=3`；`sync-figure-occurrences` 返回 `already-aligned`。
- 三处图稿映射改变了文科 Q15/Q19、理科 Q18 的规范题面哈希。已重新对照原页与当前图稿目检，并仅更新三条 ignored `question-review` 角色记录的哈希和图稿复核说明；另外 41 题的声明哈希未变。`provenance.py import-batch` 写入 revision `5986→5987`。
- 验证：`provenance.py check-batch --batch phase1-b78` 返回 `OK：2 卷`；`solution_sources.py check-batch` 两卷各22题通过；`source_manifest.py validate`、`issues.py validate`、`sync-figure-occurrences` 均通过。当前文科卷仍被 Q21(2) 源文 APCD 中未定义的 P 阻断，理科答案为非官方 D 级推导；`official_answer=null`。
- 下一阶段：生成项目 TeX、简答表和四版入口，之后正式构建、逐页视觉审查并办理批次回执。本阶段不代表批次闭环或长期语料库完成。

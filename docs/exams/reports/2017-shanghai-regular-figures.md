# 2017 上海普通高考卷：三幅源图重绘与图稿登记

日期：2026-10-28

## 来源复核与图数更正

固定输入为来源清单中的两页 PDF，SHA-256 为 44501ab771be2e0a625a47e1feb7afc6529e4038f363d238da73362d897c3675，Git blob 为 a187b22997bfe066cc488bb954333a31dfb51fd6。重看第 1 页 180 dpi 全页渲染及第 2 页 Q20 区域 300 dpi 裁图后，确认只有 Q7、Q12、Q17 含源图。此前接收、转录及答案阶段记录的“四处图形题”是初检误记；Q20 题干后是空白区，没有椭圆图，已从题面移除图位，没有制作 Q20 图稿。

发布者、出版物、版次、原始来源链和官方身份仍未核；固定输入的本库内部绑定不构成来源认证。固定 PDF 不含答案、解析或评分材料，official_answer 继续为 null。

## 矢量图稿与源对应

| 题号 | 源页 | 图稿 | 源图结构 |
|---|---:|---|---|
| Q7 | 1 | figures/f2017_shanghai_regular_q07_cuboid_axes.tex | D 为原点；DA、DC、DD1 为 x/y/z 正向轴，DB1 虚线表示题干向量；其余长方体边按源图实线绘制。投影只示结构，不表示长度。 |
| Q12 | 1 | figures/f2017_shanghai_regular_q12_grid_points.tex | 7 列×5 行单位方格；P1=(0,4)、P2=(3,2)、P3=(4,2)、P4=(6,5)；四个 ▲ 位于 (1,0)、(0,3)、(4,4)、(7,1)。 |
| Q17 | 1 | figures/f2017_shanghai_regular_q17_triangular_prism.tex | 直三棱柱 ABC-A1B1C1；仅底边 BC 按源图画为虚线，其余棱为实线。不添加长度、角标或从投影推出的条件。 |

三份图稿各在规范题面与含解析稿引用一次，manifest 登记 expected_occurrences=2。图稿哈希、source page 与 source-faithful-schematic-redraw 分类记录在本目录的来源校对 JSON。

## 生成与检查

- source_manifest 图稿同步 dry-run 识别 3 张图；图稿与 index_metadata.note 经状态事务写入，manifest revision 5274→5276。
- solution_sources 确定性重生成含解析稿，含 3 条图稿映射。
- generate_projects 写入本卷 questions.tex、answers.tex 和 index.json；随后 --check 报告 1 套试卷与生成结果一致。
- source_manifest validate 与 solution_sources check-batch --batch phase1-b50 均退出码 0；后者核对 21 题。
- 三幅图以 standalone TikZ 预览编译成 3 页 XeLaTeX PDF，180 dpi 渲染并逐幅查看。首轮发现 Q7 的 A/x、C/y 与 Q17 的 A1/C1 标签靠近，调整标签后重渲染；最终预览无标签相碰或裁切。
- 首次项目生成发现规范题面原有三处公式闭合符后紧接中文句读（\]。 / \]，），转换器因此报告未闭合。该现象在本阶段改动前的 HEAD 也可复现。只把句读移到下一源行，让 \] 独占一行；题目字词未改，确定性生成随后成功。

## 尚未完成

本阶段只完成源图更正、三幅 TikZ 重绘、manifest/Markdown 映射、来源侧记及共享 TeX/index 生成。未构建试题/解析/简答/印刷正式 PDF，未做整页版面视觉审查，未生成 build/review receipt，也未运行测试套件。paper gk-2017-regular-shanghai 与 batch phase1-b50 仍为 planned；官方来源身份和答案身份未核。本阶段不表示该卷完成，也不表示长期语料库完成。

成本：使用本地固定 PDF、TikZ 与项目生成器；未使用 OCR、外部 API 或付费服务。模型 token、工时与金额不可见，记未知。

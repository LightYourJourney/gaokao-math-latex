# 2006 山东文理候选卷：题图登记与项目 TeX 生成

日期：2026-11-02；批次：`phase1-b68`；工作树：工作分支。

## 固定图像来源与实现

所有图均依据已登记的固定候选题面 PDF 重绘为 self-contained TikZ 文件；文件注释记录 source 所示 PDF 页和题号。图稿只复现可见结构，不补充原卷未给出的数值条件，也不认证 PDF 发布者、版次、来源链或官方身份。

| 试卷 | 题号 | 文件 | 固定 PDF 页 | 目检关注点 |
|---|---:|---|---:|---|
| 山东文 | 3 | `2006_山东卷_文科/figures/f2006_shandong_arts_q03_inverse_choices.tex` | 1（印刷页322） | 四个选项分别保留坐标轴、刻度、竖直渐近线及增减方向；A 过 `(2,0)` 且在 `x=1` 有渐近线 |
| 山东文 | 16 | `2006_山东卷_文科/figures/f2006_shandong_arts_q16_prism.tex` | 1（印刷页322） | 正三棱柱顶点和隐藏棱线型，保留 `C_1A_1` 斜边 |
| 山东文 | 20 | `2006_山东卷_文科/figures/f2006_shandong_arts_q20_pyramid.tex` | 2（印刷页323） | 四棱锥 `P-ABCD`、等腰梯形底面、`AC` 与 `BD` 交于 `O`、虚线高 `PO` |
| 山东理 | 2 | `2006_山东卷_理科/figures/f2006_shandong_science_q02_inverse_choices.tex` | 1（印刷页320） | 与文科 Q3 同源函数的四个选项图形，保持选项各自的截距、渐近线和单调性 |
| 山东理 | 12 | `2006_山东卷_理科/figures/f2006_shandong_science_q12_trapezoid_fold.tex` | 1（印刷页320） | `AB=2`、`DC=1`、`∠DAB=60°` 的等腰梯形；`E` 为 `AB` 中点，显示 `ED`、`EC` 折叠线 |
| 山东理 | 15 | `2006_山东卷_理科/figures/f2006_shandong_science_q15_prism.tex` | 1（印刷页320） | 正三棱柱标签和实虚棱，`D` 位于 `A_1C_1` 中点，显示 `AD` |
| 山东理 | 16 | `2006_山东卷_理科/figures/f2006_shandong_science_q16_cube.tex` | 1（印刷页320） | 正方体八顶点标签和源图隐藏棱 |
| 山东理 | 19 | `2006_山东卷_理科/figures/f2006_shandong_science_q19_pyramid.tex` | 2（印刷页321） | 三棱锥 `V-ABC` 及与底面平行的截面 `A_1B_1C_1`，按源图区分实线与虚线 |

规范题面中的八个独立 Markdown 图稿链接与 manifest `figure_files` 一一对应；确定性含解析稿由规范题面、答案和解析正文刷新后，每幅图在题面和合并稿中各出现一次，manifest 的 `expected_occurrences` 均为 `2`。

## 编译与门禁

- 8 个 standalone 图稿分别使用 XeLaTeX 成功编译；输出渲染为 PNG 后逐幅目视检查。首轮发现四选项图条件分支没有正确按选项切换，修正为数值分支并重编。复核中按原题条件修正山东理 Q12 梯形尺寸比例与山东文 Q20 对角线交点 `O`。
- `solution_sources.py extract-batch --manifest source-manifest.json --batch phase1-b68 --write` 刷新4个派生目标。`generate_projects.py` 写入两卷共享 TeX，`make_short_answers.py` 写入2份简答源，`make_editions.py` 写入8个四版入口。
- 三个生成器各自 `--check` 均通过。`solution_sources.py check-batch` 两卷22题均通过，`provenance.py check-batch` 返回 `OK：2 卷`，`source_manifest.py validate` 与 `issues.py validate` 退出码为0。
- manifest revision 从 `5783` 经题图登记、摘要刷新、引用计数同步和状态重算到 `5788`。文科状态 `editions_generated`；理科仍 `blocked`，Q5/Q10 的 U 与四条 open / `blocks_completion` issue 保持。批次状态为 `provenance_verified`。

## 尚未完成

尚未构建正式试题、解析、简答和印刷四版本 PDF，未生成正式 build/review receipt，也未检查正式 PDF 的全部页面。standalone 预览只验证图稿可编译与局部结构，不能替代正式版面校样。固定 source 的身份疑点及山东理 Q5/Q10 blocker 继续保留。本报告不表示任一卷闭环或长期语料完成。

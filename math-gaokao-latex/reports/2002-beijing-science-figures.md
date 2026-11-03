# 2002 北京理科候选卷：题图重绘与生成面同步

- 日期：2026-11-03。
- 固定 source `src-6b6e5d61614e04d9b61330de2c085ab84c2f6fddfca9e6f357695a7ba074e690`，PDF SHA-256 `4e19a0d37e74a41655156769e6cb72c2532ec2939cb6fe4d7b18db205123de73`。Q11、Q12、Q18 均位于 PDF 第 1 页（印刷页 100）。
- 图稿依据固定 PDF 高分辨率原页图重绘；曲线与空间比例仅作示意。来源发布者、版次、扫描复制链和官方身份未核，固定 PDF 不附答案。

## 图稿与源图特征

| 题号 | 图稿 | TikZ SHA-256 | 保留的源图结构 |
|---|---|---|---|
| Q11 | `2002_北京卷_理科/figures/2002_beijing_science_q11_sign_graph.tex` | `d2c099aef2e4b7d9b6a94319496d709ee793a49ca24c72c4087fbd93e9f123de` | 定义在正半轴分支的曲线由 $x=0$ 处开端点起，穿过 $x=1$，先升后降，并在 $x=3$ 处以开端点结束。坐标刻度和曲线高度按示意绘制。 |
| Q12 | `2002_北京卷_理科/figures/2002_beijing_science_q12_convexity_graphs.tex` | `0e0f106268d7a646bf3b365059d96b8b0f053a2ac93f832f139ce946cb855f3b` | 四面板分别保留 $f_1$ 先降后升、$f_2$ 凹向下、$f_3$ 线段、$f_4$ S 形；$x=1$ 虚线仅出现在 $f_2,f_3,f_4$。 |
| Q18 | `2002_北京卷_理科/figures/2002_beijing_science_q18_polyhedron.tex` | `b0398a12b2abdf4da3bad9572285d7eff9d7ef474376d1ead142b6c4ba36ba88` | 保留上下矩形、顶点标签、E/F 侧棱延长交点、源图实线/虚线棱关系与 $a,b,c,d$ 标签；不添加原图没有的 $h$ 或尺寸箭头。 |

三份图稿均在忽略目录中以独立 XeLaTeX 文档编译并目视检查；Q18 的 $A_1,D_1,C_1$ 与 $d$ 初版标签有重叠，调整后复编检查，当前预览中标签分离。预览文件仅位于 `.work/phase1-b82/figure-review/build/`，不作为正式试卷 PDF 或正式视觉回执。

## 同步与验证

- 规范题面 `2002/2002_数学真题_北京理_试题.md` 中三处占位替换为独立段落 Markdown 图链；原题文字和公式不作改写。
- 运行 `solution_sources.py extract-batch --batch phase1-b82 --write` 刷新确定性 `_含解析.md`，再运行 `source_manifest.py sync-figure-registry --paper gk-2002-regular-beijing-science --write`。全部同步后 manifest revision 为 6041，三项 `figure_files` 各登记 2 次引用（规范题面与合成稿）。
- 更新 manifest 的项目索引注记，并生成 `questions.tex`、`answers.tex`、`index.json`、简答稿及四版入口。题面与合成稿中的 `\input` 映射均指向三份项目内 TikZ 文件。
- 22 题 question-review、answer-solve、answer-review provenance 已事务导入；固定 PDF SHA、原页映射、现行题面/答案哈希均由工具校验。Q11/Q12/Q18 的 answer evidence 绑定相应图稿哈希和本报告。Q16 为 U/PENDING，关联 ISSUE-1360；Q19 原文 `{a_n}`/`x_n` 差异照录，关联 ISSUE-1361。
- 下列定向门禁通过：`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`provenance.py check-batch`（1卷）、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`manifest_csv.py --check`（775行且 current）。

## 阶段边界

本阶段完成三张源图矢量重绘、题面和合成稿映射、manifest/provenance 注册及项目生成。paper 仍因 Q16 与 Q19 两条 open / `blocks_completion` issue 保持 `blocked`，batch 当前为 `provenance_verified`；`official_answer=null`。尚未构建正式四版 PDF、生成构建/视觉回执、逐页检查或关闭批次。下一阶段执行正式四版构建和全页视觉验收；此报告不代表本卷闭环或长期语料完成。

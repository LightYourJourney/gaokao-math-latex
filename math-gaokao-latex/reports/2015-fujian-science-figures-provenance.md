# 2015 福建理科候选卷：四幅题图与逐题来源记录

- 日期：2026-11-03；工作树 `仓库根`，分支 `feat/gaokao-phase0`。
- 固定来源：source `src-c47985c709ff8ae42e6e192879d604223c58a53c4358056d28f78ad5a9736e3c`，PDF SHA-256 `a33455d27abdf2c4b344a5b90395bd71269f6fbefdef350375aba074e47ef700`，Git blob `421cface308a5e99649ed8c316ae0b82322e0a9c`。本图稿仅复刻固定候选副本的图形，不认证发布者、版次、复制链或官方身份。

## 题图

| 题号 / 原页 | 图稿 | 原页结构记录 |
|---|---|---|
| Q6 / PDF p.1（印刷页 943） | `2015_福建卷_理科/figures/q06-flowchart.tex` | 开始、`i=1`、`S=0`、累加 `cos(iπ/2)`、`i=i+1`、判断 `i>5?`；“否”回到累加入口，“是”输出 `S`。 |
| Q13 / PDF p.1（印刷页 943） | `2015_福建卷_理科/figures/q13-parabola-shaded-region.tex` | 坐标点 A(1,0)、C(2,4)，曲线 `y=x²`；阴影是矩形内曲线上方、`y=4` 下方的区域。 |
| Q17 / PDF p.1（印刷页 943） | `2015_福建卷_理科/figures/q17-solid-geometry.tex` | 保留 ABCD 矩形投影、E 点、G/F 中点与原图实虚线关系。该图为题面示意图，不据视觉投影推断未给出的度量。 |
| Q18 / PDF p.2（印刷页 944） | `2015_福建卷_理科/figures/q18-ellipse-chord.tex` | 保留椭圆、坐标轴、割线 l、交点 A/B 与横轴上的点 G；直线斜率只按原图示意，不作数值测量。 |

四处原页图位均以 350 dpi 页渲染局部对照。规范题面以单独 Markdown 链接映射四个 `.tex` 文件；`solution_sources.py extract-batch` 同步更新 `_含解析.md`，`generate_projects.py` 确定性生成题目版与解析版 TeX。`sync-figure-registry` 登记 4 张图，每张在规范题面和含解析稿中各出现 1 次（`expected_occurrences=2`），manifest revision `6075→6076`。

## 逐题 provenance

- `provenance.py init-batch` 为 `phase3-b26` 创建 question-review、answer-solve、answer-review 三个隔离工作文件；按当前规范题面和答案要点计算 23 个题面哈希与 23 个答案哈希。
- 导入时逐题绑定固定 source ID、PDF SHA 和页码（Q1–Q17 为 PDF p.1，Q18–Q23 为 PDF p.2）。题面复核均为 passed；答案证据基于项目推导并经 Q1–Q23 独立盲核；冲突状态均为 none、ISSUE 数为 0。
- 题面复核证据见 [题面复核报告](2015-fujian-science-question-review.md)；答案推导及核对见 [答案要点报告](2015-fujian-science-answer-key.md) 与 [答案盲核报告](2015-fujian-science-answer-review.md)；Q1–Q15、Q16–Q23 解析分别见 [解析正文盲审报告](2015-fujian-science-solution-review.md)。`official_answer=null`，没有答案页或官方答案来源。
- `provenance.py import-batch --write` 将正式逐题记录写入本卷 `provenance.json`，manifest revision `6076→6077`；批次派生状态为 `provenance_verified`。

## 检查与阶段边界

- 通过：`source_manifest.py validate --manifest source-manifest.json`；`issues.py validate --file missing-issues.md`；`provenance.py check-batch`（23 题）；`solution_sources.py check-batch`（23 题）；`generate_projects.py --batch phase3-b26 --check`；`manifest_csv.py --check`（775 行）；图稿注册只读复核（4 张）。
- 当前图稿按源页完成结构复刻；正式生成 PDF 中的尺寸、分页、可读性与图文布局复核尚未完成。简答版、四版入口、正式构建与视觉回执仍待后续阶段。本报告不表示来源认证、官方答案确认或整卷验收。

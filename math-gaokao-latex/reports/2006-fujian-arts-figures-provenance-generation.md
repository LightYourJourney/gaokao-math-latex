# 2006 福建文科候选卷：盲核校正、题图、provenance 与共享 TeX

- 日期：2026-11-02；batch `phase1-b76`；paper `gk-2006-regular-fujian-arts`。
- 固定候选 source `src-88a71372c96b05a58058a4446824a5aa14004ffa91901212088621a6b41d0346`；PDF SHA-256 `8984913f8b9b4927361dc042f0d78b4ff9fe6b4b9b7b898d7184c1f4cea05432`。固定 PDF 仅有题面，来源发布者、出版者、版次、来源链及官方身份仍未核。

## 盲核与答案订正

- 独立盲核者仅读取规范题面并推导 Q1–Q22。Q10 经复核确认：按直线与平面平行的严格定义（无公共点），A 可令 `m` 为 `α` 的法线、`n` 为 `α` 内经过垂足且垂直于 `m` 的直线，从而前件成立而 `n∥α` 不成立；C 则由 `m,n` 共面、`m⊂α`、`n∩α=∅` 得 `m∩n=∅`，所以只有 C 为真。
- Q17 初稿相位符号有误。恒等式为 `f(x)=3/2+(√3/2)sin 2x+(1/2)cos 2x=3/2+sin(2x+π/6)`；由导数符号，递增区间为 `[-π/3+kπ,π/6+kπ]`，$k\in\mathbb Z$。图象由 $y=\sin2x$ 左移 `π/12`、再上移 `3/2` 得到。答案要点、解析正文、含解析稿及生成的 LaTeX 已同步更新。
- Q1–Q16、Q18–Q22 盲核与最终答案一致；Q19、Q20 可仅用题面文字条件推导，不依赖图上比例。完整推导见独立答案报告；固定 PDF 中没有可据以确认官方答案的页面，`official_answer=null`。

## 图稿、provenance 与生成文件

- Q19 图重绘 `figures/f2006fujian_arts_q19_tetrahedron.tex`：实线 AB、BC、CA；虚线 AD、BD、DC、AO；标出 B、C、D、A、BD 中点 O 及 BC 中点 E。Q20 图重绘 `figures/f2006fujian_arts_q20_ellipse.tex`：椭圆、坐标轴正方向、左焦点刻线及 F 标记、原点 O、左准线 `l`。坐标仅重现示意拓扑，不作为题目数据。
- 两张图分别由 `latexmk -xelatex` 编译为单页测试图并渲染 PNG；主会话逐张查看，标签清楚、实虚线与原图对应，未见裁切。题面、解析和确定性含解析稿各保留相应本地图稿引用。`sync-figure-registry` 登记两图，`expected_occurrences=3`。
- `provenance.py import-batch --write` 写入 22 题 provenance，分别记录题面原页核对、分段独立推导和全卷独立盲核；source page 为 Q1–Q19 第1页、Q20–Q22 第2页。Q10、Q17 的推导冲突状态标记 resolved；最终均无 U 级答案及未解决逐题 issue。manifest revision `5960→5961`。
- `generate_projects.py` 生成共享 `questions.tex`、`answers.tex` 与索引；`make_short_answers.py` 生成 `answers_short.tex`；`make_editions.py` 生成试题版、解析版、简答版、印刷版入口。paper 状态为 `editions_generated`，batch 仍是 `planned`。

## 验证与剩余工作

- 通过：`source_manifest.py validate`、`sync-figure-occurrences`（already-aligned）、`solution_sources.py check-batch`、`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`provenance.py check-batch`、`issues.py validate`、`manifest_csv.py --check`（775 行）、`git diff --check`。
- 本阶段只编译独立图稿，没有正式构建四个版本 PDF；构建回执、逐版逐页视觉审查和完整测试套件仍未完成。本报告不表示来源认证、本卷验收或 1952–2026 题库完成。

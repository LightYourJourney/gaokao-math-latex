# 试卷目录说明与索引

本仓库的高考数学试卷按「年份_卷别」独立成目录，**目录根为 `docs/exams/`**，例如
`docs/exams/2020_全国Ⅰ卷_理科/`。这与任务书示例 `docs/exams/<年份>_<卷别>/` 一致。

为保住 2017—2026 各卷已产生的 2800+ 份构建/复核回执（其中含人工逐页视觉审查记录），
仓库根保留了一个兼容符号链接：

```
math-gaokao-latex -> docs/exams
```

因此旧回执里的 `math-gaokao-latex/<卷>/...` 路径仍可解析；**项目实体只在
`docs/exams/` 下**，符号链接仅为历史证据与旧命令的兼容别名，不复制任何内容。

## 单卷目录内容

```
<年份>_<卷别>/
  questions.tex        共享题面（由规范 Markdown 生成，勿手改）
  answers.tex          共享答案与解析（由规范 Markdown 生成，勿手改）
  answers_short.tex    共享简答速查（由答案要点生成，勿手改）
  试题版.tex            仅题面，独立编译
  解析版.tex            题面 + 详细解析，独立编译
  简答版.tex            题面 + 答案速查，独立编译
  印刷版.tex            五号字紧凑版，独立编译
  figures/*.tex        TikZ/pgfplots 矢量图
  provenance.json      逐题来源、题面/答案哈希与三角色复核记录
  receipts/build.json  正式构建回执（XeLaTeX + latexmk）
  receipts/review.json 逐页八类视觉审查回执
```

四个入口只引用共享内容文件，题面、答案与解析不重复维护。规范 Markdown 源在仓库根的
`<年份>/` 下：`_试题.md`、`_答案要点.md`、`_解析正文.md`，`_含解析.md` 由生成器确定性
合成。

## 全量索引

- `docs/exams/index.json`：逐卷静态身份（paper_id、目录、题数、结构、图稿）。
- `docs/exams/manifest.csv`：来源级清单，每个上游 PDF 一行，含绑定卷、状态与问题号。
- `report.md`、`README_数学.md`、`docs/exams/reports/baseline.md`：当前总量、批次与门禁统计。
- `docs/exams/missing-issues.md`：缺源、源缺陷、答案冲突与待核事项总账。

## 构建与校验

```bash
# 单卷四版正式构建（以 2009 重庆卷文科为例）
python3 docs/exams/tools/build_projects.py build \
  --manifest docs/exams/source-manifest.json \
  --issues docs/exams/missing-issues.md \
  --paper gk-2009-chongqing-arts --formal

# 全量回执与报告一致性
python3 docs/exams/tools/build_projects.py validate-receipts \
  --manifest docs/exams/source-manifest.json --all --require-final
python3 docs/exams/tools/report.py check --all \
  --manifest docs/exams/source-manifest.json \
  --issues docs/exams/missing-issues.md
```

未完成或存疑的卷不会伪装为完成：`blocked` 卷在 manifest 中带 `issue_ids` 与
`resume_action`，逐题答案可为 `U/PENDING`；只有四版构建、逐页审查与门禁全部通过的卷
才标为 `complete`。

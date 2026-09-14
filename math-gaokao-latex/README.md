# 高考数学真题 LaTeX 题库

本目录保存可编译、可复用、可直接打印的高考数学题库项目。题面以清单中登记的固定来源为准；无法由来源唯一确认的内容保留原样，并在缺失清单中标记为 `pending` 或 `blocked`，不按模型记忆补写。

## 当前规模

截至 2026-09-14，来源级清单覆盖 1952—2026 年，共 775 条上游 PDF 来源：普通高考 734 条、春季高考 41 条。

- 试卷项目：137 套，其中 `complete` 126 套、`blocked` 11 套
- 批次：69 批，其中 58 批正常关闭、11 批带内容阻塞关闭
- 每套试卷：4 个独立入口，共 548 个已编译 PDF
- LaTeX 源文件：1279 个 `.tex`
- 题库项目内图片：0 个；图形以 `TikZ/pgfplots` 等矢量源维护
- 编译中间产物：0 个；`.work` 临时目录不存在
- 未解决的阻塞问题：29 条，涉及 11 套试卷，见 [missing-issues.md](missing-issues.md)

`blocked` 表示题面、答案或来源身份仍有不可唯一裁决之处；对应项目的四个版本仍须通过构建门禁，但不会因此把存疑结论伪装成已核定事实。

## 项目结构

每套项目位于一个“年份_卷别”目录中，包含：

- `questions.tex`：共享题面内容
- `answers.tex`：共享答案与解析内容
- `试题版.tex`：只含题面
- `解析版.tex`：题面、答案和完整解析
- `简答版.tex`：题面与简答
- `印刷版.tex`：适合 A4 打印的完整版本
- `figures/*.tex`：需要的矢量图源
- `build/*.pdf`：四个入口对应的 PDF 产物
- `provenance.json`、`receipts/`：来源、构建和复核回执

共享内容由生成脚本维护，入口文件不重复保存题目正文。原始 Markdown 题面、来源清单和审计记录位于仓库的 `<year>/` 与本目录中，用于追溯和重生成，不是编译缓存。

## 清单与校验

`source-manifest.json` 是主清单，`manifest.csv` 是来源级投影，每个上游 PDF 占一行。常用校验命令（从本目录的父仓库根目录执行）：

```bash
python3 math-gaokao-latex/tools/issues.py validate \
  --file math-gaokao-latex/missing-issues.md

python3 math-gaokao-latex/tools/generate_projects.py \
  --manifest math-gaokao-latex/source-manifest.json \
  --all --check

python3 math-gaokao-latex/tools/make_short_answers.py \
  --manifest math-gaokao-latex/source-manifest.json \
  --all --check

python3 math-gaokao-latex/tools/manifest_csv.py \
  --manifest math-gaokao-latex/source-manifest.json \
  --output math-gaokao-latex/manifest.csv --check

python3 math-gaokao-latex/tools/provenance.py check-all \
  --manifest math-gaokao-latex/source-manifest.json \
  --issues math-gaokao-latex/missing-issues.md

python3 math-gaokao-latex/tools/build_projects.py validate-receipts \
  --manifest math-gaokao-latex/source-manifest.json \
  --all --require-final --require-current-inputs --json

python3 math-gaokao-latex/tools/review_receipts.py check-all \
  --manifest math-gaokao-latex/source-manifest.json \
  --issues math-gaokao-latex/missing-issues.md \
  --require-current-build --json

python3 math-gaokao-latex/tools/report.py check --all \
  --manifest math-gaokao-latex/source-manifest.json \
  --issues math-gaokao-latex/missing-issues.md
```

编译环境为 XeLaTeX/latexmk；每个 `build/` 目录只保留四个 PDF，必须删除 `.aux`、`.fls`、`.log`、`.out`、`.toc`、`.synctex.gz`、`.fdb_latexmk`、`.bcf`、`run.xml` 等编译中间产物。项目级 provenance、回执和清单文件用于审计，图片不得作为题库项目文件提交。

## 回归测试

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s math-gaokao-latex/tests -p 'test_*.py'
```

最近一次完整测试结果为 `Ran 816 tests`、`OK (skipped=13)`；正式构建与复核回执均已通过当前清单门禁。

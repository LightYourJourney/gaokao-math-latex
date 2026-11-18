# 高考数学真题 LaTeX 题库

1952–2026 年高考数学真题的转录与排版工程：每卷有规范 Markdown 源（题面、答案要点、解析正文），由工具生成 LaTeX，再编译出试题版、解析版、简答版、印刷版四个版本；题图全部用 TikZ/PGFPlots 重绘。

当前规模与状态见 [README_数学.md](README_数学.md)（由工具生成，勿手改），完整构建与复核报告见 [report.md](report.md)。

## 目录

| 路径 | 内容 |
|---|---|
| `<年份>/` | 各卷的规范 Markdown 源与题图草稿 |
| `math-gaokao-latex/` | LaTeX 工程：每卷一个目录，另有 `tools/`、`tests/`、`reports/` 与来源总账 `source-manifest.json`。说明见 [其 README](math-gaokao-latex/README.md) |
| `math-gaokao-2017-2026/` | 早期的 2017–2026 全国卷工程与 Markdown → LaTeX 转换器 |
| `docs/` | 实施计划、流程审计与迁移记录 |

## 使用

需要 TeX Live（XeLaTeX、latexmk）、Python 3 与 poppler。命令都在仓库根目录运行：

```bash
# 只读核对全部构建与复核回执
./math-gaokao-latex/compile.sh validate-receipts --manifest math-gaokao-latex/source-manifest.json --all --require-final
# 跑测试
python3 -m unittest discover -s math-gaokao-latex/tests -t math-gaokao-latex
```

PDF 等编译产物不入库，可由源文件重建。

## 来源与许可

- 真题原件来自 [deekur/gaokaomath](https://github.com/deekur/gaokaomath)（CC BY 4.0）。试题版权归命题方或出版方所有。
- 本仓库的转录、解析、LaTeX 源、TikZ 图与工具采用 [CC BY 4.0](LICENSE) 许可：转载或改编须署名并注明修改。

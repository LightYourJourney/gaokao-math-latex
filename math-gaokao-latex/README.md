# 高考数学 LaTeX 项目

## 阶段 0 机器报告

- 来源守恒：**775 = 734 + 41**（普通高考 734，春季高考 41；2004 `.txt` 不计入 PDF 来源）
- 历史口径：21 套、84 个版本；legacy baseline 的 Overfull 为 **1**
- 当前口径：complete 13，blocked 8，in_progress 0
- 当前构建：84/84 succeeded
- 当前警告重算：Overfull 0，Underfull 13，警告豁免 13
- 上游题面不含答案的说法仅有三份抽样证据，不外推为 775 份全部无答案。

| 批次 | 重算终态 | 回执门禁 | ownership |
|---|---|---|---|
| phase0-b01 | closed_with_blockers | FINALIZED | committed |
| phase0-b02 | closed_with_blockers | FINALIZED | committed |
| phase0-b03 | closed | FINALIZED | committed |
| phase0-b04 | closed | FINALIZED | committed |
| phase0-b05 | closed_with_blockers | FINALIZED | committed |
| phase0-b06 | closed_with_blockers | FINALIZED | committed |

来源清单：`manifest.csv` 是 `source-manifest.json` 的来源级清单投影，每个上游 PDF 一行。重建命令：

```bash
python3 tools/manifest_csv.py \
  --manifest source-manifest.json \
  --output manifest.csv \
  --write
```

运行 `python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md` 校验。

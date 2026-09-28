# 高考数学 LaTeX 项目

## 全量状态

- 来源总数：**775**（普通高考 734，春季高考 41）。
- 来源状态：ready 775
- 试卷总数：**228**；生产状态：blocked 31，compiled 3，complete 194
- 批次总数：**106**；manifest 状态：closed 87，closed_with_blockers 18，compiled_pending_review 1
- 正式复核门禁：FINALIZED 105，VISUAL_FAILED 1
- 已编译版本：912/912；构建回执状态：compiled_pending_review 4，succeeded 224
- review 回执状态：failed 1，passed 227
- 问题总账：951 条，未解决问题：135，阻塞完成 69。
- 回执日志警告汇总（包含待复核回执）：Overfull 23，Underfull 38，豁免记录 61。
- 回执完整性：build 缺失 0 / 无效 0；review 缺失 0 / 无效 0。
- 门禁未通过批次：phase0-b02。

## 交付物与校验

来源清单：`manifest.csv` 是 `source-manifest.json` 的来源级清单投影，每个上游 PDF 一行。

```bash
python3 tools/manifest_csv.py --manifest source-manifest.json --output manifest.csv --write
python3 tools/report.py render --all --manifest source-manifest.json --issues missing-issues.md
python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md
```

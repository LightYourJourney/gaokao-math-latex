# 高考数学 LaTeX 项目

## 全量状态

- 来源总数：**775**（普通高考 734，春季高考 41）。
- 来源状态：ready 775
- 试卷总数：**272**；生产状态：blocked 45，compiled 58，complete 165，editions_generated 4
- 批次总数：**138**；manifest 状态：closed 77，closed_with_blockers 18，compiled_pending_review 41，provenance_verified 2
- 正式复核门禁：FINALIZED 71，INVALID_OR_STALE 65，VISUAL_FAILED 2
- 已编译版本：1088/1088；构建回执状态：compiled_pending_review 70，succeeded 202
- review 回执状态：failed 6，passed 266
- 问题总账：1069 条，未解决问题：186，阻塞完成 121。
- 回执日志警告汇总（包含待复核回执）：Overfull 23，Underfull 45，豁免记录 68。
- 回执完整性：build 缺失 0 / 无效 0；review 缺失 0 / 无效 0。
- 门禁未通过批次：phase0-b01、phase0-b02、phase0-b03、phase0-b04、phase0-b05、phase0-b06、phase1-b07、phase1-b08、phase2-b58、phase2-b59、phase2-b62、phase2-b63、phase2-b64、phase2-b65、phase2-b66、phase2-b67、phase2-b68、phase2-b69、phase2-b70、phase2-b71、phase2-b72、phase2-b73、phase2-b74、phase2-b75、phase2-b76、phase2-b77、phase2-b78、phase2-b79、phase2-b80、phase2-b81、phase2-b82、phase2-b83、phase2-b84、phase2-b85、phase2-b86、phase2-b87、phase2-b88、phase2-b89、phase2-b90、phase2-b91、phase2-b92、phase2-b93、phase2-b94、phase2-b95、phase2-b05、phase2-b06、phase2-b07、phase2-b09、phase2-b10、phase2-b11、phase2-b12、phase2-b13、phase2-b15、phase2-b16、phase2-b17、phase2-b18、phase2-b19、phase2-b20、phase2-b21、phase2-b22、phase3-b00、phase3-b01、phase3-b02、phase3-b03、phase3-b04、phase3-b05、phase3-b06。

## 交付物与校验

来源清单：`manifest.csv` 是 `source-manifest.json` 的来源级清单投影，每个上游 PDF 一行。

```bash
python3 tools/manifest_csv.py --manifest source-manifest.json --output manifest.csv --write
python3 tools/report.py render --all --manifest source-manifest.json --issues missing-issues.md
python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md
```

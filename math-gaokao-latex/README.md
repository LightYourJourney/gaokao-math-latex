# 高考数学 LaTeX 项目

## 全量状态

- 来源总数：**775**（普通高考 734，春季高考 41）。
- 来源状态：ready 775
- 试卷总数：**295**；生产状态：blocked 50，compiled 3，complete 241，planned 1
- 批次总数：**161**；manifest 状态：closed 126，closed_with_blockers 31，compiled_pending_review 3，planned 1
- 正式复核门禁：FINALIZED 157，INVALID_OR_STALE 1，VISUAL_FAILED 3
- 已编译版本：1176/1176；构建回执状态：compiled_pending_review 6，succeeded 288
- review 回执状态：failed 3，passed 291
- 问题总账：1131 条，未解决问题：190，阻塞完成 126。
- 回执日志警告汇总（包含待复核回执）：Overfull 19，Underfull 51，豁免记录 70。
- 回执完整性：build 缺失 1 / 无效 0；review 缺失 1 / 无效 0。
- 门禁未通过批次：phase0-b02、phase2-b58、phase2-b59、phase4-b11。

## 交付物与校验

来源清单：`manifest.csv` 是 `source-manifest.json` 的来源级清单投影，每个上游 PDF 一行。

```bash
python3 tools/manifest_csv.py --manifest source-manifest.json --output manifest.csv --write
python3 tools/report.py render --all --manifest source-manifest.json --issues missing-issues.md
python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md
```

### 题目级 IR 导出（增量能力）

可从已登记的规范 Markdown 题面与逐题 `provenance.json` 生成确定性 JSON，不重新 OCR 或重录题面：

```bash
python3 tools/export_question_ir.py gk-2017-regular-national-1-science --output /tmp/2017-national-1-science.ir.json
```

导出前会核对 `paper_id`、唯一 canonical 来源绑定、manifest 与逐题 provenance 中登记的来源 PDF SHA-256、题数、逐题 ID、source ID 和题面哈希；它不重新打开/哈希 PDF 原件。任一记录不一致即失败。题面以 `body_markdown` 保留解析题块，当前没有结构化证据的 `options`、`equations`、`tables` 与 `source_bbox` 保持 null；图像 Markdown 引用独立列出。项目答案材料只作为 `answer_evidence`，`official_answer` 固定为 null。该工具目前只覆盖已登记规范 Markdown 的导出，不代表 OCR→IR 自动接入或整卷验收。

OCR 整页结果使用独立候选格式，不能自动分配给题号；例如把已登记 JSONL 第 2 条 MinerU 结果绑定到 manifest 来源：

```bash
python3 tools/ocr_candidate_ir.py benchmarks/ocr-runs.jsonl --line 2 --output /tmp/2008-page05-ocr-candidate.json
```

只有在 source ID、PDF SHA、页码与引擎字段匹配时才导出；结果始终 `recognized_unverified` / `needs-review`，并保留页级原文、区域坐标（如有）及已有耗时/缓存/资源记录。`question_id` 为空；人工按原图切分、核对并确认前，不得导入规范题面。

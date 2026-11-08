# 高考数学 LaTeX 项目

## 全量状态

- 来源总数：**775**（普通高考 734，春季高考 41）。
- 来源状态：ready 775
- 试卷总数：**470**；生产状态：blocked 111，compiled 3，complete 356
- 批次总数：**316**；manifest 状态：closed 227，closed_with_blockers 88，compiled_pending_review 1
- 正式复核门禁：FINALIZED 40，INVALID_OR_STALE 276
- 已编译版本：1880/1880；构建回执状态：compiled_pending_review 4，succeeded 466
- review 回执状态：failed 1，passed 469
- 问题总账：1448 条，未解决问题：312，阻塞完成 249。
- 回执日志警告汇总（包含待复核回执）：Overfull 45，Underfull 147，豁免记录 192。
- 回执完整性：build 缺失 0 / 无效 0；review 缺失 0 / 无效 0。
- 门禁未通过批次：phase0-b01、phase0-b02、phase0-b03、phase0-b04、phase0-b05、phase0-b06、phase1-b07、phase1-b08、phase1-b09、phase1-b10、phase1-b11、phase1-b12、phase1-b13、phase1-b14、phase1-b15、phase1-b16、phase1-b17、phase1-b18、phase1-b19、phase1-b20、phase1-b21、phase1-b22、phase2-b23、phase2-b24、phase2-b25、phase2-b26、phase2-b27、phase2-b28、phase2-b29、phase2-b30、phase2-b31、phase2-b32、phase2-b33、phase2-b34、phase2-b35、phase2-b36、phase2-b37、phase2-b38、phase2-b39、phase2-b40、phase2-b41、phase2-b42、phase2-b43、phase2-b44、phase2-b45、phase2-b46、phase2-b47、phase2-b48、phase2-b49、phase2-b50、phase2-b51、phase2-b52、phase2-b53、phase2-b54、phase2-b55、phase2-b56、phase2-b57、phase2-b58、phase2-b59、phase2-b60、phase2-b61、phase2-b62、phase2-b63、phase2-b64、phase2-b65、phase2-b66、phase2-b67、phase2-b68、phase2-b69、phase2-b70、phase2-b71、phase2-b72、phase2-b73、phase2-b74、phase2-b75、phase2-b76、phase2-b77、phase2-b78、phase2-b79、phase2-b80、phase2-b81、phase2-b82、phase2-b83、phase2-b84、phase2-b85、phase2-b86、phase2-b87、phase2-b88、phase2-b89、phase2-b90、phase2-b91、phase2-b92、phase2-b93、phase2-b95、phase2-b96、phase2-b97、phase2-b98、phase2-b99、phase2-b00、phase2-b01、phase2-b02、phase2-b03、phase2-b04、phase2-b05、phase2-b06、phase2-b07、phase2-b08、phase2-b09、phase2-b10、phase2-b11、phase2-b12、phase2-b13、phase2-b14、phase2-b15、phase2-b16、phase2-b17、phase2-b18、phase2-b19、phase2-b20、phase2-b21、phase2-b22、phase3-b00、phase3-b01、phase3-b02、phase3-b03、phase3-b04、phase3-b05、phase3-b06、phase3-b07、phase3-b08、phase3-b09、phase3-b10、phase3-b11、phase3-b12、phase3-b13、phase3-b14、phase3-b15、phase4-b01、phase4-b02、phase4-b03、phase4-b04、phase4-b05、phase4-b06、phase4-b07、phase1-b23、phase1-b24、phase3-b16、phase3-b17、phase3-b18、phase3-b19、phase3-b20、phase3-b21、phase3-b22、phase3-b23、phase4-b08、phase4-b09、phase4-b10、phase4-b12、phase4-b13、phase4-b14、phase4-b15、phase4-b16、phase4-b17、phase4-b18、phase4-b19、phase4-b20、phase4-b21、phase4-b22、phase4-b23、phase4-b24、phase4-b25、phase4-b26、phase4-b27、phase4-b28、phase4-b29、phase4-b30、phase4-b31、phase4-b32、phase4-b33、phase4-b34、phase4-b35、phase1-b36、phase1-b37、phase4-b36、phase1-b38、phase1-b39、phase1-b40、phase1-b41、phase1-b42、phase1-b43、phase1-b44、phase1-b45、phase1-b46、phase1-b47、phase1-b48、phase1-b49、phase1-b50、phase1-b51、phase1-b52、phase1-b53、phase1-b54、phase1-b55、phase4-b37、phase4-b38、phase4-b39、phase4-b40、phase4-b41、phase1-b56、phase1-b57、phase1-b59、phase1-b60、phase1-b61、phase1-b62、phase0-b07、phase0-b08、phase0-b09、phase0-b10、phase0-b11、phase0-b12、phase0-b13、phase0-b14、phase0-b15、phase0-b16、phase0-b17、phase0-b18、phase0-b19、phase0-b20、phase0-b21、phase0-b22、phase0-b23、phase0-b24、phase0-b25、phase1-b63、phase1-b64、phase1-b65、phase1-b66、phase1-b67、phase1-b68、phase1-b69、phase1-b70、phase1-b71、phase1-b72、phase1-b73、phase1-b74、phase1-b75、phase1-b76、phase1-b77、phase1-b78、phase1-b80、phase1-b81、phase1-b82、phase1-b83、phase3-b24、phase3-b25、phase3-b26、phase4-b42、phase4-b45、phase4-b46、phase4-b47、phase4-b48、phase4-b49、phase4-b50、phase4-b51、phase4-b52、phase4-b53、phase4-b54、phase4-b55、phase4-b56、phase4-b57、phase4-b58、phase4-b59、phase4-b60、phase4-b61、phase4-b62、phase4-b63、phase4-b64。

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

### 本地 OCR 与转录规范

部署、模型下载、路由、交叉核对、人工校对和阶段提交统一遵循 [OCR_WORKFLOW.md](docs/OCR_WORKFLOW.md)。首选 Xiaomi-OCR-0，复杂文档与公式用 PaddleOCR-VL-1.6 交叉验证，批量 PDF 使用 MinerU。统一入口为 `python3 tools/local_ocr.py --help`；模型与依赖固定记录在 `tools/ocr-local-models.json`，运行资产放在忽略目录 `.work/ocr-local/`。

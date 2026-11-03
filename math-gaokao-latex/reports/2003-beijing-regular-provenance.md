# 2003 北京普通文理候选卷：三角色逐题 provenance 导入

- 日期：2026-11-04；批次：`phase4-b48`。
- 文科内部卷 `gk-2003-regular-beijing-arts` 绑定固定候选 source `src-dcc6a2c21c7b8e7b8f23f5188f34d7f542f94e40f4219b54cfb85a0d7004bc0f`，PDF SHA-256 `7fc0fd289fc486a0ae1c16a9ab5b4f0561830897df6e8897c50666f03d511913`；理科 `gk-2003-regular-beijing-science` 绑定 source `src-120ea104f8cb373f5731039fa9d36469df457869849f27420831962ef1ad2306`，PDF SHA-256 `d0081500bd56d03199ddcf232fe8e870f2ecd7e9c41ba849417af9af79fbb702`。两份固定 PDF 均为 2 页；绑定只表示内部 canonical 来源关系，不认证发布者、版次、复制/扫描链或官方身份。

## 逐题映射与状态

| 卷别 | PDF 页映射 | 题面复核 | 答案证据 | 未决项 |
|:--|:--|:--|:--|:--|
| 文科 | Q1–Q17 → PDF 第 1 页（印刷页 126）；Q18–Q20 → PDF 第 2 页（印刷页 127） | Q1–Q17、Q19–Q20 `passed`；Q18 `uncertain` | Q1–Q17、Q19–Q20 为编者推导 D 级；Q18 为 U/PENDING | Q18 关联 `ISSUE-1398`、`ISSUE-1399`，均 open / `blocks_completion` |
| 理科 | Q1–Q17 → PDF 第 1 页（印刷页 124）；Q18–Q20 → PDF 第 2 页（印刷页 125） | Q1–Q16、Q18–Q20 `passed`；Q17 `uncertain` | Q1–Q16、Q18–Q20 为编者推导 D 级；Q17 为 U/PENDING | Q17 关联 `ISSUE-1400`、`ISSUE-1401`，均 open / `blocks_completion` |

- 文科 Q18 的文字确实照录原页，但原件首句 A1/A2 与后文及图示 A1/A 不统一；理科 Q17 原页可见“底面边长的 3”，未见“为”。按项目既有口径，原字照录不能消除源内容歧义，因此对应题面复核记录为 `uncertain`。两题答案保持 U/PENDING，不把条件性推导升级为确定答案。
- 其余 38 题的题面复核均为 `passed`。两卷所有题目的 `conflict_status` 均为 `none`：复核材料未记录解题者与盲核者之间的答案分歧；来源歧义由各自 transcription / answer issue 表达。
- PDF 均无答案、解析或评分页；答案要点和解析正文为本库独立推导，`official_answer=null`。角色字段使用任务角色标签；原始忽略区 `.work/phase4-b48` 已不存在，故不推断具体代理名、模型身份或不可复查的原始工作记录。

## 事务与验证

- `provenance.py init-batch` 在项目忽略目录重新建立三角色工作文件；结合当前规范题面、答案要点、固定 source 元数据及跟踪的逐题复核报告填入 120 条角色记录。question / answer 哈希由 `provenance.py` 从当前规范源现场计算。
- `provenance.py import-batch` dry-run 通过；write 以事务 `a8b24b50-c43e-45cc-9f10-a83d47ee736c` 将两卷 `provenance.json` 与 manifest revision `6150→6151` 原子写入。批次推进为 `provenance_verified`，两 paper 继续 `blocked`。
- `provenance.py check-batch` 返回 `OK：2 卷`；`source_manifest.py validate`、`issues.py validate --file missing-issues.md` 及 `solution_sources.py check-batch`（两卷各 20 题）通过。
- 本阶段未生成项目 TeX、四版入口或 PDF；未运行正式构建、逐页视觉审查、批次封存或全量测试。下一阶段按流程生成并核对 TeX 项目，再进行正式构建与视觉回执。本报告不表示来源认证、整卷验收或长期语料完成。

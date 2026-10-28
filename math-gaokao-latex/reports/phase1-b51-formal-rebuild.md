# phase1-b51：分页回流后的四版正式重建

日期：2026-10-28

## 构建结果

- 本卷 `gk-2000-spring-shanghai` 正式构建 attempt：`8fd91441-c7fc-4c19-9846-989f14559e84`，supersedes 分页回流前 attempt `36aee468-9d50-403d-b997-7b62eca90d07`。构建输入对应 manifest revision 5298；构建状态事务将记录推进到 revision 5300。固定来源 ID 为 `src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0`，来源 SHA-256 `f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954`。
- 四版均构建成功，无 `errors`、`missing_characters`、`overfull`、`undefined_references` 或 receipt `problems`。TeX Live 2026、XeTeX 3.141592653-2.6-0.999998、latexmk 4.88、Poppler 26.10.0。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 5 | `d764d9cefb715cac3c28ee2d69d8a7c6261309f6156db402cf019d5411e29de7` |
| 解析版 | 19 | `e5f9f7d646d064492d526f06031ee17ca8f990d22dd3ff0d3885c9f1b3241003` |
| 简答版 | 7 | `dac7d9a025a7454b71eac83502a8a74e0e87bc0f7ab151cc4657216177033422` |
| 印刷版 | 15 | `d832a911a7fd9ac459183c69e3b4853599bd3ca3e94a1d094e03a7a86491edc6` |

四版共46页；印刷版从16页降为15页，解析版 Q21 答案框不再单独落在页首。build receipt 的独立当前性验证为0 failed、0 invalid、0 missing、0 stale、1 pending review；PDF 页数及 SHA-256 与本机文件及 receipt 一致。

## 当前状态与门禁

- paper 状态为 `compiled`，batch 状态为 `compiled_pending_review`。新构建已替代旧 attempt；下一阶段完成当前 attempt 绑定的逐页视觉审查并生成最终 review receipt。
- 通过：`source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`（1卷/22题）、`solution_sources.py check-batch`（22题）、本卷 `generate_projects` / `make_short_answers` / `make_editions --check`、manifest CSV 当前性（775行）和 `report.py check --all`。全量报告已按当前 manifest content transaction 刷新并回读校验。
- 未运行测试套件。出版者、出版物、版次、扫描来源链及附录答案官方身份仍未核实，`official_answer=null`；本阶段不声称来源认证、整卷验收或1952–2026语料库完成。

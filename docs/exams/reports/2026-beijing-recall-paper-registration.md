# 2026 北京高考数学回忆版候选卷：规范源与内部卷登记

- 日期：2026-11-04。
- 固定候选 source `src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee`，仓库内文件 `普通高考/2026/2026北京.pdf`；PDF SHA-256 `7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9`，Git blob `cf49aa3671ff4143e5c665c7bc53b5f08ab38fca`，共 5 页。首页自称“回忆版”；发布者、版次、复制链及官方身份未核，`official_answer=null`。绑定只确认本库使用的固定字节，不认证正式卷身份。
- 已将 Q1–Q21 固化为规范题面、非官方答案要点、解析正文，并按 `solution_sources.py` 确定性生成含解析稿。PDF 仅有题面，无答案页。题面保留 Q10、Q13、Q15 版本异文；Q10/Q14/Q18 原图位置仍为待绘占位。

## 规范文件指纹

| 文件 | SHA-256 |
|---|---|
| [试题](../../2026/2026_数学真题_北京回忆版_试题.md) | `e13022ce512ac97842618ed9bf225535d1117203638baaf2aff0b7eb3140ca96` |
| [答案要点](../../2026/2026_数学真题_北京回忆版_答案要点.md) | `b9a9e0bd8c136fb60de8cdca517095e4d2069c7a0ddab495d47900189465e366` |
| [解析正文](../../2026/2026_数学真题_北京回忆版_解析正文.md) | `9649f8a30ec225714138a95cb4bfafb3e7bd4325b03ba2e7bda25d27c4f39db0` |
| [确定性含解析稿](../../2026/2026_数学真题_北京回忆版_含解析.md) | `0bcc0199a207ee2886c1ca57c0eb9054172f293d65e2ad46c58b5d68c7372e33` |

## 登记与阻塞

- `register-papers --write` 将 `gk-2026-regular-beijing-recall` 登记到 `phase4-b49`，manifest revision `6159→6160`。paper 为 `blocked`（`blocked_from=planned`），batch 为 `planned`；source relation 为 `canonical` 仅表示固定字节内部绑定。
- 七项 open / `blocks_completion`：`ISSUE-1408`（Q10 选项异文）、`ISSUE-1409`（Q13 上限端点异文）、`ISSUE-1410`（Q15 ②③次序异文）、`ISSUE-1411`（Q10 图缺失）、`ISSUE-1412`（Q14 图缺失）、`ISSUE-1413`（Q18 图缺失）、`ISSUE-1414`（Q18(2) 条件③不能唯一确定点）。不裁定异文，不把条件性答案提升为确定答案；Q10、Q13、Q18(2) 保留 U/PENDING。

## 校验与当前边界

- `solution_sources.py extract-batch --write` 后 `check-batch` 通过，识别 21 题；题面、答案、解析题号和小问锚点对齐。
- `source_manifest.py validate`、`issues.py validate`、`manifest_csv.py --check`（775 行）通过；六个全量报告投影经 `report.py check --all` 检查为当前，未完成状态已保留。
- 当前全局报告显示正式复核门禁 `INVALID_OR_STALE 265`、`VISUAL_FAILED 1`。核查 `phase4-b48` 后确认其 build/review 回执仍可读、输入与工具链绑定未变；状态降级来自 manifest 增加本卷后，全局生成投影 `index.json` 尚未重生成，`provenance.default_artifacts_state` 因而把生成物标为 stale。报告检查通过只表示报告投影与现有 manifest/回执状态一致，不表示 265 个批次都已最终验收。下一次按流程生成本卷 TeX 时会一并刷新全局 index，再重算相关门禁；本登记没有修改旧卷回执。
- 尚未导入本卷逐题 provenance，未登记图稿 / `figure_files` / 图稿 provenance，未生成 TeX/PDF，未执行正式构建、review receipt 或视觉检查。该阶段没有额外调用 OCR 或模型；模型 token 与费用不可见，记未知。

下一步先按固定 PDF 第 2、3 页重绘 Q10/Q14/Q18 图并目视核验，再同步题面图链、生成器、manifest `figure_files` 和图稿 provenance；随后导入逐题三角色 provenance、生成项目并验证全局 index。来源身份、Q10/Q13/Q15 异文及 Q18(2) 答案约定继续保持未决。本登记不表示来源认证、整卷验收或长期语料库完成。

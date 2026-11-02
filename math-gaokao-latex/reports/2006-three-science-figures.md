---
title: 2006 江西、浙江、湖北理科候选卷题图、正式构建与视觉收口记录
date: 2026-11-02
batch_id: phase1-b70
manifest_revision_at_finalization: 5897
status: closed_with_blockers
---

# 2006 江西、浙江、湖北理科：题图与四版正式构建

## 范围与来源边界

本阶段覆盖绑定到 `phase1-b70` 的 3 份固定候选 PDF。Source SHA-256 仅绑定副本字节，不认证发布者、版次、扫描链或官方身份。三卷均无可见官方答案/评分页，`official_answer` 继续为 null；答案为独立推导草稿。湖北 Q17（2）维持 U/PENDING，ISSUE-1319 与 ISSUE-1320 仍 open 且阻断该卷完成。

## 题图登记与修订

- 江西：Q11 四面体、Q12 气温与选项图、Q15 直三棱柱、Q19 三角形截面、Q20 三棱锥、Q21 椭圆弦。
- 浙江：Q9 球面大圆弧、Q14 正四面体投影、Q15 正弦曲线、Q17 四棱锥、Q19 椭圆切线、Q20 曲线和切线。
- 湖北：Q15 莱布尼茨三角形示例、Q18 正方体。Q18 源图未标 P，图稿不补点。

14 个 TikZ 文件、题面 Markdown 映射及 manifest `figure_files` 已同步。首轮视觉复核发现浙江 Q14 的 B、Q19 的 F₂ 与 M、Q20 的横轴标签在个别版次间距不足；调整三个标签并重建四版。最新 attempt `a82bc906-c4d2-4546-83cc-a34b9ba0ddb3` 中，Q14 B 与投影边线分开，Q19 焦点标注清楚，Q20 的 O 与 x_{n+1} 已分开。

## 答案速查更正

简答表检查发现江西 Q6 误录为“②④”，按题面重算得最小参数 $a=-5/2$，应选 C；江西 Q3 字母由 A 改为 D，与原逐题答案及解析一致。哈希已同步到 provenance。

## 正式构建

三卷使用 TeX Live 2026、XeLaTeX 与 latexmk 4.88；正式 build 状态均为 `succeeded`。页数合计 139。各版 PDF SHA-256 与 attempt 绑定在对应 `receipts/build.json`。

| 卷别 | Build attempt | 页数（试题/解析/简答/印刷） | PDF SHA-256（同序） |
|---|---|---:|---|
| 江西理科 | `1a75c317-6e62-4f58-bce3-dd38a50c5b61` | 6 / 21 / 8 / 16 | `db9f78a881d6c0ecb0e881c5b4e54fe3960e7196a72c5e50dc4e87e138f129a4` / `0b43e5a6eae917af0e8b28fd5ed545176459931491da7a778d2b9fb472da2a52` / `6fbd27913a0cfbc53650cc24d18fcbfb9ec14ec23f1f276d61680780966171a1` / `dff47315baa235db1b10468a9ff26f06f02a9d0789b36ea76185b0f7d8ca6c09` |
| 浙江理科 | `a82bc906-c4d2-4546-83cc-a34b9ba0ddb3` | 5 / 18 / 7 / 13 | `db3af58630cc74d038a06a0677876cae4aab9bbf317b8246012c484483104716` / `654d651bd4fcab8c4331a090eba89869911ed52b1b9e9cb85d4b9de6d9733fc3` / `51ece13a0a4968eb20aff9e3db58a208db0e38e0f0b2b7748ef68f30e073dafc` / `7219fb310f22b07e4ce978f14f7724d92d9b6262cc0ed4ee152b3698cd4ad61c` |
| 湖北理科 | `cb4a5749-2126-4d27-bd4e-c004284d1476` | 5 / 19 / 7 / 14 | `8cf726750a31da196a365128d95939a4bb687d93c16d26b3ad9533b2cec158cd` / `ff2eb8c93961063abf688fee1a3a55fea98bb8a31e926f0c11283014534774a0` / `91d5c683e0a8461e901368f54771dd3df370627b4445821d87c1167c0bd36478` / `face5138969b10c47af63ee89dd7eb4c7b0a42d5d0937a42907274aacecdb0f4` |

江西印刷版有 1 条 Underfull，湖北四版共 5 条 Underfull；均已定位到对应页面复核，未见可读性或版心损害并登记警告豁免。无编译错误、缺字、Overfull 或未定义引用。

## 视觉复核与批次状态

三卷 139 页均按当前 PDF 重新渲染并逐页检查八项，共 1112 项：1038 pass、74 not_applicable、0 fail、0 pending。最终 receipt 与各 build attempt、PDF SHA、页数和工具链相符；`validate-receipts --require-final --require-current-inputs` 与 `review_receipts check-batch` 均通过。

`finalize-batch-checked` 将 `phase1-b70` finalize 为 `closed_with_blockers`，manifest revision 5897。江西、浙江转为 `complete`；湖北仍为 `blocked`，阻塞项为 ISSUE-1319 与 ISSUE-1320。全量报告和 775 行 `manifest.csv` 已刷新且通过 currentness 检查。

完整 unittest 结果：`Ran 1752 tests in 562.100s`，`FAILED (failures=1, skipped=13)`。唯一失败 `test_the_cached_states_match_the_recomputed_ones` 涉及 16 个既有缓存状态差异，不含 phase1-b70：6 卷的缓存 `complete` 与现场派生 `answers_verified`/`compiled` 不符，另有 10 个批次缓存 `closed_with_blockers`、现场派生 `provenance_verified` 不符。未批量改写这些历史状态。

本阶段完成 3 卷候选材料的构建与视觉收口，不认证来源发布者或版次、不将独立答案标记为官方，也不表示长期语料完成。

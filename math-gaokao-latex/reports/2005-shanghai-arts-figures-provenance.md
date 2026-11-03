# 2005 上海文科普通卷：题图重绘与三角色 provenance

- 日期：2026-11-03。
- 批次/试卷：`phase4-b43` / `gk-2005-regular-shanghai-arts`。
- 固定来源：`src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846`，PDF SHA-256 `952989a262e3f7b34a425ccb6e2132af7e88408a387edae50f59a9505ebe46a1`，Git blob `d3849e9bf2f21c95b4823be90b24669b74ee1685`，512658 bytes，2页。

## 题图重绘与登记

按固定 PDF 原页可见信息重绘三张本地 TikZ 图。图稿只表达原图可见关系，不按示意透视推断额外的长度、角度或垂直条件。

| 题号 | 固定 PDF 页（印刷页） | TikZ 文件 | SHA-256 |
|---|---|---|---|
| Q12 | 1（264） | `2005_上海卷_文科/figures/f2005_shanghai_arts_q12_prism_assemblies.tex` | `c9e30ac764e8f9de8da4972992ff0d78b7dd939c63ad01e30649c760d6cda654` |
| Q17 | 1（264） | `2005_上海卷_文科/figures/f2005_shanghai_arts_q17_rectangular_prism.tex` | `95d99d02cbdb729d7fb8ff0ae3c4f02ab74460923dd044966c56847edcb011df` |
| Q21 | 2（265） | `2005_上海卷_文科/figures/f2005_shanghai_arts_q21_parabola_geometry.tex` | `cbef94fc5fb05e9e680b521fc86ea52c6494309179fa5b0c23f9df57435b13e7` |

Q12 原页的两幅棱柱图线形相同，重绘保留两幅相同图样，没有将它们分别解释为不同拼合拓扑。Q17 保留长方体棱线、虚线 `B₁D` 及 `M/N` 中点位置。Q21 按原图绘出抛物线、`O/F/A/B/M/N`、`AB`、`FA` 延长线和 `MN` 垂线；图形不用于裁定题目未给出的度量条件。

三份图稿分别以 XeLaTeX 编译为一页本地预览 PDF，均成功生成；转成 PNG 后逐幅与固定原页局部目视对照。预览 PDF 留在忽略目录 `.work/ocr-local/2005-shanghai-arts/figure-preview/`，不是正式试卷版 PDF，也不构成版面回执。

规范题面中的三条 TikZ 链接独立成段；注册后将 `paper_id` 补入三份规范事实源，并在答案/解析稿中显式绑定 `source_id` 和 `source_sha256`。再次运行 `solution_sources.py extract-batch --manifest source-manifest.json --batch phase4-b43 --write` 后，确定性 `_含解析.md` 当前 SHA-256 为 `7e520a56499aa8e0decc8256d51f75908f3f1d1604a585e0dbcfbbddd1320d5e`。随后 `sync-figure-registry --manifest source-manifest.json --paper gk-2005-regular-shanghai-arts --write` 将三图写入 manifest revision `6102`，每图期望引用数为2，分别对应规范题面与合并稿。题面与答案摘要由 provenance 工具按内容结构计算，补充 frontmatter 后 `provenance.py check-batch` 仍通过。

## 逐题 provenance 与问题状态

`provenance.py init-batch` 为 22 道题建立 question-review、answer-solve、answer-review 三个角色文件。使用 `tools/provenance.py` 的题面和答案摘要函数按当前规范源重算 22 组摘要；三角色共66条记录通过 `import-batch` dry-run，随后以单一 state transaction 导入，manifest revision `6103→6104`。题面复核 Q1–Q22 均为 `passed`；来源页映射为 Q1–Q19 对 PDF 第1页、Q20–Q22 对第2页。固定 PDF 无答案或解析页，所有确定答案均标为 D 级编者推导，`official_answer=null`。

Q12 与 Q20 继续为 U/PENDING：

- Q12 关联 `ISSUE-1377`。四棱柱表面积严格小于三棱柱时 `0<a<sqrt(5/3)`；端点两者并列，原题未说明“最小”是否允许并列。
- Q20 关联 `ISSUE-1379`。固定原页清楚印作“中低价层”，规范题面忠实照录；按“中低价房”解释时才得到2013年底，不能把条件结果写成确定答案。

登记初期的 `ISSUE-1378` 原列为转录歧义。复核确认字面本身清楚后，该项已以 resolved 状态保留历史记录；对答案解释的未决另由 `ISSUE-1379` 阻断。paper 保持 `production_state=blocked`、`blocked_from=planned`。这一分类调整不认证来源的出版者、版次、复制链或官方身份。

## 全库投影

登记后刷新 `manifest.csv`（775行）；`manifest_csv.py --check` 通过。运行 `report.py render --all` 并检查全量输出，`report.py check --all` 返回“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”。最新全库投影含412套试卷、260个批次；复核门禁显示259个 `INVALID_OR_STALE`、1个 `VISUAL_FAILED`，其中本批因尚无 build/review 回执处于无效待建状态。抽查既有 `phase4-b41` 的 `review_receipts.py check-batch`，当前事实指出其 manifest 批次状态与当前事实不一致。本阶段只刷新全库投影，没有改动或修复其他卷的状态。本卷自身尚无 build/review 回执，后续阶段再建立。

## 阶段边界

本阶段完成 source ID 更正、Q12/Q17/Q21 题图与 manifest 登记、确定性合并稿刷新、问题分类澄清及三角色 provenance 导入。没有调用 OCR；图稿子任务的模型 token/费用不可见。项目 TeX、简答表、四版入口、正式试卷 PDF、逐页视觉回执和批次报告尚未生成；本卷仍被 Q12、Q20 两项未决问题阻断。本报告只记录本卷阶段进度，不表示来源认证、整卷无阻塞完成或 1952–2026 语料完成。

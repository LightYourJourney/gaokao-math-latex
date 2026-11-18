# 2006 广东、江苏、江西文、浙江文候选卷：题图登记与项目生成

日期：2026-11-02
批次：`phase1-b69`
固定工作树：`仓库根`，工作分支

## 范围与来源边界

本阶段为四份固定候选 PDF 重绘并登记 17 幅 TikZ 图，更新题面链接、manifest、逐题 provenance 与确定性派生稿。固定副本 SHA-256：

| 卷件 | source-relative 页码及印刷页 | 固定源 SHA-256 | 图题 |
|---|---|---|---|
| 广东 | PDF 第1页，印刷页292 | `46542e3594530e351f1f9812d0543cc5cd3c223ee9275d98bdc1dd802d3242aa` | Q4、Q7、Q14、Q17 |
| 江苏（文理变体未知） | PDF第1页/第2页，印刷页302/303 | `a2eb12dcb9ef4ea50908436bf15619674a7e263b8455569163ab183cf2a0cfa0` | Q9、Q10、Q18、Q19 |
| 江西文科候选卷 | PDF第1页/第2页，印刷页306/307 | `2550b886dff3865452708e5e163681924784ec9b7289ff650bedb910a29e51fe` | Q12、Q15、Q20、Q21 |
| 浙江文科候选卷 | PDF第1页/第2页，印刷页342/343 | `b53d9923107e7030a296fcace329efc61c6af454014c3ea94464acaf5a46b5c4` | Q8、Q14、Q16、Q17、Q19 |

固定字节与当前 source artifact 一致。该一致性不认证 PDF 发布者、版次、来源链或官方身份；四卷 `official_answer` 继续为 `null`。江苏题签未标科类，variant 仍未知。

## 图稿与核对

- 广东：`2006_广东卷/figures/` 新增 Q4 中点三角形、Q7 反函数图、Q14 三角球堆、Q17 双圆空间图。
- 江苏：`2006_江苏卷/figures/` 新增 Q9 双棱锥/正方体、Q10 信号源与接收器、Q18 帐篷、Q19 折叠前后图。图稿为供生成器 `\input` 的 TikZ 片段，不含文档级 wrapper。
- 江西文科：`2006_江西卷_文科/figures/` 新增 Q12 温度曲线与 A–D 候选图、Q15 三棱柱绕行、Q20 三棱锥、Q21 椭圆弦图。Q15 源 PDF 的细绕行线部分端点与棱线重合；稿件将路线标作示意，端点不宣称精确转录。
- 浙江文科：`2006_浙江卷_文科/figures/` 新增 Q8 三棱柱、Q14 正四面体投影、Q16 正弦曲线、Q17 四棱锥、Q19 椭圆切线图；Q14 保留原图可辨的 `B′`，Q16 保留 `y=1`、峰点 `P` 及其两侧相邻零点 `M/N`。
- 各卷规范题面将原图位替换为本卷相对 TikZ 源链接；代理分别对照固定 PDF 两页及 intake/transcription 报告。主会话对四份 PDF 图位复核，并用临时 standalone wrapper 对全部17幅执行 XeLaTeX 编译与 PNG 渲染，逐幅/联系页检查无编译错误、缺字或图框裁切。

## 清单、provenance 与派生物

- `sync-figure-registry` 将四卷图稿写入 `figure_files`，17 项的 `expected_occurrences` 均为2（试题源和解析正文中的图链）；随后 `sync-figure-occurrences` 全局对齐实际引用计数。
- 图链改变了广东 Q4/Q7/Q14/Q17、江苏 Q9/Q10/Q18/Q19、江西文 Q12/Q15/Q20/Q21、浙江文 Q8/Q14/Q16/Q17/Q19 的规范题面哈希。按 `provenance.question_text_digests` 刷新对应的 `question-review` 记录后重新导入三角色 provenance。
- 为通过简答生成器的速查表一致性门禁，广东 Q6 与江西文 Q4/Q8 的答案速查表格将字面 `U/PENDING` 规范为 `U`；逐题详细答案仍保留 `U/PENDING` 及原说明，答案判断和 blocker 均未变化。
- `solution_sources.extract-batch --write` 重生成四份 `_解析正文.md` 投影及四份 `_含解析.md`。`generate_projects.py` 写入9个项目目标；`make_short_answers.py` 生成4份简答；`make_editions.py` 生成16个四版壳。manifest 最终 revision `5805`，批次状态 `provenance_verified`。

## 验证与未完成事项

以下确定性门禁通过：

- `source_manifest.py validate`：4卷通过。
- `issues.py validate`：通过；未决 blocker 保持原状态。
- `provenance.py check-batch --batch phase1-b69`：4卷有效。
- `generate_projects.py --batch phase1-b69 --check`：4卷一致。
- `make_short_answers.py --batch phase1-b69 --check`：4卷一致。
- `make_editions.py --batch phase1-b69 --check`：4卷一致。
- `solution_sources.py check-batch --batch phase1-b69`：4卷全部通过。
- `manifest_csv.py --check`：775行投影当前；`git diff --check`：通过。
- 临时 figure review：17/17 XeLaTeX 成功并生成 PNG；不是正式卷件构建或 review receipt。

当前广东、江西文科仍因既有 U/PENDING 题面/答案问题为 `blocked`；江苏、浙江为 `editions_generated`。本阶段没有正式构建四版 PDF、页面级视觉审查、build/review receipt 或批次 finalize；不表示来源认证、单卷闭环或长期语料完成。

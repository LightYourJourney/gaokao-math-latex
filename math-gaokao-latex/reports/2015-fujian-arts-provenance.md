# 2015 福建文科候选卷：三角色逐题 provenance 与答案盲核

日期：2026-11-03

批次：phase3-b24；paper：gk-2015-regular-fujian-arts

## 来源与题面复核

- 固定输入 source ID `src-1a7c18ef934f5ef3b6afbb819418e905cbfa4bf8a6b9d7a784c676fd3ad7132f`，PDF SHA-256 `4ca0fbac9967c9a73bdb0bc00eceb3d0181c57285ee72fc260a02c9c24172383`。原 PDF 两页，印刷页 945–946；Q1–Q18 在 PDF 第1页，Q19–Q22 在第2页。
- 独立题面复核者逐题对照题干、公式、选项/小问、题号和图表引用，22/22 通过，未报告转录差异。Q21 的行内写法与原页数学内容相同。
- PDF 不含答案页；发布者、出版者、版次、复制链及官方身份仍未核实。manifest 的来源关系 canonical 仅表示本库固定使用这些字节，不构成来源认证；`official_answer=null`。

## 三角色 provenance

- 按 `provenance.py init-batch` 在 ignored `.work/phase3-b24/provenance/` 建立三条独占角色路径。角色分别为独立题面复核、独立答案求解、独立盲态答案复核；三角色 ID 两两不同。
- 两名独立求解角色均只使用题面与固定原卷（图形题需要时），没有读取答案要点或解析正文。最终答案与当前规范答案逐题一致；答案证据均为 D 级项目推导，不是官方答案。
- `provenance.py import-batch` dry-run 通过，随后写入 22 题 provenance，source 页面、题面/答案摘要均由工具按当前规范源重算。manifest revision 升至 6063；无未解决逐题冲突或新增 issue。Q5、Q6、Q9、Q11、Q12、Q14、Q17、Q19、Q20、Q22 的首轮选项/计算/端点差异，经复算后记为 `resolved`；其余题为 `none`。

## 最终交叉核验答案

| 题号 | 核验结论 |
|---:|---|
| 1–4 | A、D、D、C |
| 5–8 | C、D、A、B |
| 9–12 | B、C、A、B |
| 13–16 | 25、√2、1、9 |
| 17 | `a_n=n+2`；`Σb_n=2101` |
| 18 | (1) 9/10；(2) 121/20 |
| 19 | `y²=4x`，`m=±2√2`；两条切线到 F 距离相等 |
| 20 | (1) 证明成立；(2) 最大体积 1/3；(3) 最小值 `(1+√3)/√2` |
| 21 | 最小正周期 `2π`；`g(x)=10sin x−8`；存在无穷多个所需正整数 |
| 22 | 严格递增区间 `(0,(1+√5)/2]`；参数范围 `k<1` |

## 盲核差异及裁定

- 答案求解角色首轮在 Q5 选项映射、Q12 必要/充分方向、Q14 数值化简和 Q20(3) 最值上出错；按自身推导复算后分别改为 C、B、√2 和 `(1+√3)/√2`。
- 盲态复核角色首轮在 Q5 选项映射、Q6 正切商、Q9 棱柱表面积、Q11 点到直线距离系数、Q12 参数阈值/条件方向、Q17 等比求和、Q19 的 m 值、Q20(3) 最小值和 Q22 右端点上出现差异。逐项只依题面及原图复算后，最终答案与答案层一致。
- 关键裁定：Q12 的全称不等式恰等价于 `k≤1`，而 `Q:k<1` 蕴含 `P`、`P` 不蕴含 `Q`，所以 `P` 是 `Q` 的必要不充分条件，选 B。Q11 中 M 到 `3x−4y=0` 的距离是 `4b/5`，故 `b≥1`、`e∈(0,√3/2]`，选 A。Q22 的导数仅在 `(0,φ)` 为正，但函数在端点 `φ=(1+√5)/2` 仍严格递增，最大递增区间包含该端点。
- 首轮差异均有独立复算依据并已解决；provenance 中没有 `unresolved`，missing-issues 未新增事项，不以未解决 blocker 掩盖任何答案分歧。

## 校验与阶段边界

- 通过：`provenance.py import-batch` dry-run、`provenance.py check-batch`（1 卷/22题）、`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`generate_projects.py --check`。
- 导入后 `manifest.csv` 曾因 revision 6063 变旧；已重新生成并通过 775 行 currentness check。manifest revision 6063 的六个全量报告投影已重新生成并通过 `report.py check --all`，返回与 manifest 一致且保留未完成状态。
- 本阶段 OCR 调用 0；使用三名独立 Luna high 角色进行题面复核、答案求解及盲复核，实际 token/费用未知。未运行测试套件、未生成简答版、未建立四版入口，尚无正式 XeLaTeX 构建、逐页视觉回执或 build/review receipts。
- 当前 paper 状态为 `answers_verified`，batch 状态为 `provenance_verified`。下一阶段生成简答版和四版入口，再做正式构建及页面验收；本阶段不表示来源认证、整卷闭环或长期语料完成。

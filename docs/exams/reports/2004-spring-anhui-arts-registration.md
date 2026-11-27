# 2004 春季安徽文科卷：paper/source 与 Q18 阻断项登记

日期：2026-10-27

## 登记结果

- 候选 paper：`gk-2004-spring-anhui-arts`；批次：`phase1-b44`；manifest revision：`5217 → 5218`。
- 题量 22，科类 `arts`；卷目录 `2004_安徽春季卷_文科`；题面映射 PDF 第 1–2 页，答案页为 `null`。
- source `src-9c46c959fc97e9d53c91e510403e97f1810d192e5049962539d9d4b54331c35d` 绑定为本库 canonical 题面来源。canonical 只表示该固定副本与本卷的内部绑定，不表示来源为官方原件。
- Q20 TikZ 图登记进 `figure_files`，在题面及确定性含解析稿中各有一次引用。

## 来源与答案边界

- 固定 PDF SHA-256：`17f32ff6f385dfd59d80f5bccfa548dd9b7f8d20e697ce4a66b4de185b95d7a8`；2页A3，原卷印刷页码151–152。文件题签自称“2004年普通高等学校春季招生考试（安徽卷文）”。
- 固定副本本身为可复现来源；其上游发布者、出版者、版次及扫描链未核，不能据题签或文件名推断这些属性。PDF 没有答案页，答案/解析为本项目独立推导，`official_answer=null`。
- Q18 仅给首项与前 n 项和关系。关系化简为每步 `b_n=b_{n-1}+2` 或 `b_n=-b_{n-1}`；`2n-1` 和 `(-1)^(n-1)` 两组序列均满足，因此不能给出唯一通项。

## 阻断状态与验证

- 注册事务在 `missing-issues.md` 创建 `ISSUE-1211`：`answer-missing`、`blocks_completion`，明确要求取得可追溯的同版勘误或独立同期材料。paper 维持 `blocked`，`blocked_from=planned`；批次当前仍为 `planned`。
- `source_manifest.py validate` 通过；`issues.py validate` 通过；全量 report 投影检查通过；`manifest.csv` 检查为 current、775行；`solution_sources.py check-batch --batch phase1-b44` 通过，22题全部对齐。
- 本阶段未运行测试套件、未生成 TeX/PDF、未做视觉检查，未 push。

## 后续

下一阶段导入逐题 provenance 并生成共享 TeX 与四版入口，同时确保 Q18 保持 `U`/未解决状态；四版构建及全页视觉复核完成前，不升级生产状态。

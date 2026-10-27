# 2006 上海春季招生数学试卷：候选卷与固定来源登记

日期：2026-10-27

## 登记结果

- 通过 `source_manifest.py register-papers` 事务将 `gk-2006-spring-shanghai` 登记为候选 paper，批次 `phase1-b41`，manifest revision `5183 → 5184`。
- 纸卷名为“2006 年·上海春季招生数学试卷”，目录键 `2006_上海春季卷`，22 题，`track=none`，`production_state=planned`。source `src-788a65aef8319a4a0abebc5ded42d68216d14d78d55583936dba4ab5d90a7a3b` 绑定为本库当前固定副本的 canonical 题面来源。
- 页码映射：题面 Q1–Q16 在 PDF 第1页、Q17–Q22 在第2页，故 `pages_q=[1,2]`；扫描副本第2–4页含源载答案与解答，故 `pages_s=[2,4]`。
- 登记时无逐题问题项，`issue_ids=[]`，来源未因本次登记改状态；figure 列表暂空，后续图稿阶段单独登记。

## 来源身份边界

- `canonical` 仅说明本库将已固定的这份 PDF 作为该候选卷当前绑定来源，不证明扫描件就是官方原件。
- 扫描页内题签、杂志栏头及页码可见；杂志出版资料、扫描来源链、题面发布身份，以及印载“参考答案”的发布者、版本和官方身份均未核。源载答案身份保持未核，`official_answer=null`。
- 登记为 `planned` 不表示题目或批次完成，也不表示1952–2026语料库完成。

## 验证记录

- 注册事务 dry-run 通过后，以唯一入口原子写入 paper、batch 和 source 反向绑定；manifest revision 为 5184。
- `source_manifest.py validate`、`issues.py validate`、`report.py check --all`均成功。报告/CSV 投影经 `report.py render --all`刷新后检查 current；此轮无其它投影差异。
- 未运行测试套件。注册规格留在仓库忽略的 `.work/phase1-b41/`，与既有项目工作文件策略一致。

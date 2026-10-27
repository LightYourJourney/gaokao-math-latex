# 2006 上海春季招生数学试卷：题图与逐题 provenance

日期：2026-10-27

## 题图

- 固定 PDF 第 2 页已核对 Q17 长方体及题干指定线段、Q20 椭圆/抛物线轨迹与点位、Q21 题面空白坐标网格。
- 新增三份 TikZ 矢量源：f2006_spring_q17_cuboid.tex、f2006_spring_q20_trajectory.tex、f2006_spring_q21_grid.tex；在规范题面中建立对应 Markdown 映射，并重新生成 _含解析.md 派生稿。
- Q20 图按题设曲线方程作图，并按源图将 C 至 D 的抛物线运行弧段画为实线、其余辅助曲线画为虚线；示意比例不作为题设条件。Q21 只采用第 2 页题面网格，没有把第 4 页解答函数图放进题面。
- sync-figure-registry 将三图登记至 manifest，revision 5184 → 5185；manifest 检查确认题面和含解析稿中的图引用计数与登记相符。

## 逐题 provenance

- 以 phase1-b41 初始化并填充题面复核、独立求解、答案盲核三角色工作记录，逐题关联固定 source、SHA-256、题面页码、规范题面哈希和答案哈希。
- 题面复核覆盖固定 PDF 第 1–2 页共 22 题；分段独立解答及第二读者复核沿用已提交的独立推导记录。导入前 dry-run 通过；正式事务写入 provenance 并推进 manifest revision 5185 → 5186。
- 固定副本内题签、页眉和页码可见；杂志出版资料、扫描来源链、题面及源载参考答案的发布者/版本/官方身份仍未核。official_answer 仍为 null；没有登记未发现的数学冲突。

## 验证与范围

- source_manifest.py validate、provenance.py check-batch、solution_sources.py check-batch 均通过；覆盖 1 卷、22 题。
- 更新来源清单 CSV 投影，共 775 行；manifest、题面和含解析稿中的三图引用已登记一致。
- 未运行测试套件，也未生成项目 TeX 或 PDF。本阶段只完成题图与来源证据登记，不表示该卷交付完成或全语料完成。

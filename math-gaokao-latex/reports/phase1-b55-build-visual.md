# phase1-b55：2007 上海春季卷四版54页验收

日期：2026-10-29

本批为`gk-2007-spring-shanghai`，21题150分120分钟，7幅源图实现为6份TikZ，1张原生LaTeX表格。题面、答案、解析三源分开维护，含解析稿确定性派生，四入口共享questions/answers/answers_short。源文归档已提交0c0767d3，三角色/来源与生成记录见[本批报告](phase1-b55-provenance-generation.md)。本卷完成不代表1952—2026全集完成。

## 当前构建与视觉证据

最终attempt `a83e512c-b211-4991-99f1-86439ba1d6a8`，构建输入manifest revision5339；本次接手后以当前manifest revision5407执行finalize，实际返回FINALIZED，batch closed、paper complete、build succeeded、review passed。构建输入与PDF当前性检查实际OK，无stale/missing/invalid/pending。四版为A4，日志没有错误、缺字、未解析引用或Overfull。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 6 | `50eda8d6c4002a14e60a15b87eb6c85d6a1bc611fdac9bcd260d213d925b1e7c` |
| 解析版 | 23 | `503e78f22445d14bcac8c289db4383a11ef27c5292923c33110b0277ff17ca4b` |
| 简答版 | 8 | `9392cb782b30de9ae82f7dddc309b5c4ef1494da26e2268653b587b591d3060a` |
| 印刷版 | 17 | `c1240fe049843302412344bdfac504387266497bd5374c1135400a44b6a9912c` |

本attempt全部54页重新实际查看，无继承旧结论：主代理查看试题6页、简答8页、印刷17页；独立复核者`/root/final_b55_solution_visual`逐页view_image解析23页，逐页PNG SHA和八项观察保存在`.work/phase1-b55/verification/current-solution-visual.json`。统一视觉工作项及inspection-summary绑定本attempt和当前PDF/PNG。共432项检查410pass、22not_applicable、0fail/pending。解析15页通用“解析”标签落在页尾，正文续16页，按现有模板行为pass+note保留事实；无公式截切、图标签遮挡或孤立答案末页。题面区无答案，速查与解析区明示非官方推导。

## 修复历史与来源边界

首轮63910eef四版因来源说明裸下划线official_answer报Missing $ inserted；已从Markdown改为中文并重生成，失败日志/回执保存在build-history，ISSUE-1241–1244均resolved/non_blocking。4325af60轮7/25/9/19页，实看印刷Q16答案跨页后精简公式排布。500edb8b轮全部59页实看，印刷末页仅两个Q21答案框，实际记pagination fail；进一步精简Q19/Q21推导后8943a775轮58页通过，9页变化重看、49张完全相同PNG继承此前实际结论，旧证据保留review-history。

提交前diff --check发现独立题号段使生成TeX行尾留空格；改源Markdown将题号与正文合段、移除EOF空白。21个解析题块和题面哈希逐项保持相同，不手改生成物。最终重新生成、正式构建并对本attempt全部54页实看，页数降为6/23/8/17，不沿用58页旧回执。题图及数学答案均未变；未改公共样式、字体或生成器。

Q19保留四块相同砖旋转、公共边接点和中央恰成四边形共同推出CE=CF的推理；材料完成平方与最优位置完整。Q20完整存在性分类、第三边±根式及等边/直角边界在简答版未丢失；Q17开放逆向构造与印载示例可不同；Q21(3)只选①，保留前三项正向检验和c4反证。独立复核报告保存了对这些数学步骤及历史印刷15/18页的实际专项检查，最终本attempt页序以本报告为准。

固定源SHA为26bee86f9e4572a70a1b847a702b49b812f92d598f7794fc490e9c295232cb2a，6页扫描副本，题面1–3、未认证印载参考答案4–6。内部canonical只绑定字节；出版者、版次、传播链及官方身份仍未认证，official_answer=null。21题为D级独立推导、conflict_status=none。印载Q20 cos(a+B)小写笔误在原文归档保留，独立解析注明正确角式；Q21两处c2均3/2，无伪冲突。

## 接手核验与回归

Claude Code最新提交2151bd7b等新增phase4-b37至b40四卷，主代理已分别运行check-batch，均FINALIZED/problems=[]，保留其全部提交。接手时manifest5406、349卷208批；本批关闭后为276 complete、70 blocked、3 compiled，全集仍有未完成工作。

以包含Claude最新代码和四卷的当前工作树完整运行：`Ran 1747 tests in 1426.797s` / `OK (skipped=13)`，日志`.work/phase1-b55/verification/after-claude-full-tests.log`。三个生成器、provenance、solution_sources及最终回执当前性已现场通过；全量报告/CSV及暂存差异在提交前复核。此前1724项结果仅作历史记录，不冒充接手后的测试。

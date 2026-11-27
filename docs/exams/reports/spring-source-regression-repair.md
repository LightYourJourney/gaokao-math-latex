# 春季卷来源、图稿与回归测试修复

日期：2026-10-28

## 完整回归发现

首轮完整运行 `python3 -m unittest discover -s math-gaokao-latex/tests` 得到 `Ran 1724 tests in 464.014s`，`FAILED (failures=6, errors=10, skipped=13)`。失败集中在2000上海春季、2003北京春季文科的历史转录/图稿测试。两名工作者分别独占对应测试文件，主代理独占来源元数据、规范源、总清单及公共报告；没有以跳过或删除检查缩小覆盖。

## 2000 上海春季卷

三图早已迁入 `2000_春季上海卷/figures/`，来源已canonical登记；题面范围也已更正为PDF第1–5页、附录第5–9页，第5页包含Q22续题和附录起始。旧测试仍用年度旧目录、未绑定断言与第1–4页范围。

本轮修正两测试的路径与登记断言，检查source↔paper↔Markdown双向绑定、固定来源SHA/9页、页范围，以及Markdown与manifest各自基准下的图稿路径和每图两次引用。原题号、数学、图形拓扑、无栅格、编译渲染与官方性未知检查保留。工作者 `/root/repair_2000_shanghai_stale_tests` 定向两模块 `Ran 10 tests in 1.112s` / `OK`。

## 2003 北京春季文科卷

旧测试仍断言未绑定，并从年度旧目录读取Q11/Q19/Q22图稿。本轮改核当前canonical绑定、五图完整集合、规范源/清单链接解析及项目内图稿；保留来源指纹、22题与图形拓扑、矢量及官方答案为空检查。

严格题面文件SHA比较又揭示sidecar漂移：提交 `ad346dfa` 只改题面答案说明一行，却未同步校对元数据。主代理核实旧sidecar SHA恰等于该提交父版本题面SHA，并比较前后22个题面块哈希完全相同，只更新 `2003_春季北京文科_来源校对.json` 的 `transcription.sha256`，不补写或更改复核结论。工作者 `/root/repair_2003_beijing_stale_tests` 复跑 `Ran 9 tests in 2.336s` / `OK`。

两卷 `validate-receipts --require-final --require-current-inputs` 均返回code=OK、succeeded=1，failed/invalid/missing/stale均0；既有正式回执没有改写。

## 2004 北京春季文科卷独立源页复核与图形修正

固定source `src-417d865aa928e69f32b3fcbc80abe4fa227259b79ababcce8765ea981117119b`，PDF SHA-256 `4670b402354afd088d6993fbc473490158f27e232b1c54730e5989b64a21ec26`，2页，印刷页155–156。只表示固定输入，不认证发布者、出版物、版次、来源链或官方身份。

两名只读审阅者分别从已核指纹的PDF独立重新渲染并目视对照：`/root/source_review_2004_beijing_arts_p1` 负责第1页Q1–Q17，`/root/source_review_2004_beijing_arts_p2` 负责第2页Q18–Q20。未查看答案或解析。20题文字、数学式、选项、小问与Q20数阵均忠实，无跨页题；源页未列各题分值，项目未虚加。Q9组合数C记号规范化为等义的binom。Q20尾问仍按源照录“计算公以及”，ISSUE-1238继续open/blocks_completion，未据语义补“式”。

Q18源图的F1与O都在以F2为心的地球圆内，O标签在原点右上。原正式图稿两焦点相距1.2，地球圆半径1.05，把F1画在圆外。新增真实几何回归断言先得到 `1.2 not less than 1.05` 的预期失败；随后调整示意焦点为±0.5、圆半径1.3，短刻度同步，O标签改右上。数值只用于示意排版，不当作题目条件或精确比例。

主代理对比源图放大裁片，并在独立临时包装器编译当前项目TikZ、以180dpi查看PNG。F1/O均在圆内，圆仍在椭圆内，焦点短刻度及A/B/x/y/O/F1/F2标签可辨无碰撞。第一次几何候选虽通过内含关系，但F1文字靠近圆线，已进一步留出标注空间。最终图稿SHA为 `8805936cb41ee89e53be937992a27230bf917a77a605e9f445bff02611af0c9c`；PDF/PNG指纹与渲染路径保存在 `.work/phase1-b52/figure-review-current.json`。

同步图表清单和规范源中的复核状态；保留原有真实的首轮复核历史，再追加本轮记录。答案与解析的“题面文字复核未完成”旧说明已按当前事实修正，并确定性同步含解析稿和answers.tex。最终2004卷专项 `Ran 9 tests in 1.901s` / `OK`；来源仍未认证、official_answer=null，尚无该卷逐题正式provenance与四版build/review回执，不称整卷完成。

## 最终验证与范围

- 最终完整回归：`Ran 1724 tests in 457.839s`，`OK (skipped=13)`；未新增跳过。此前一次基于过渡元数据启动的运行已主动中断（exit130），不用于验收。
- 2004卷生成器/解析源检查、manifest与issues校验通过；既有2000/2003正式回执当前性通过。
- 完整日志保存在 `.work/phase1-b53/verification/full-tests-stable.log`；初次失败与主动中断日志分别保留，定向测试日志同目录存档。
- 本批不变更source manifest的业务状态，不认证官方来源，不消除既有Q11/Q20等来源阻断；2009卷的构建/排版与最终视觉回执作为另一阶段提交。本批不表示1952—2026题库完成。

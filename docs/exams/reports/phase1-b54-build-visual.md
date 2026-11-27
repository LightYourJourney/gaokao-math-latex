# phase1-b54：2004 北京春季理科四版40页构建与视觉验收

日期：2026-10-28

## 实际构建与校样修复

来源、20题三角色provenance与四版生成阶段已提交0a254ed8。第一轮正式attempt `b4ad5c68-b39d-44d8-aca2-5f818414c61c`，四版4/18/6/13页，共41页，日志无错误/缺字/未解析引用/Overfull/Underfull。日志通过没有代替视觉验收：主代理实际查看解析第13–18页，发现Q20第18页只余两个答案框；Q18的C标签被抛物线延长线穿过，A标签与y轴过近。又实际渲染第14页220dpi局部，确认两个标签问题。首轮build、pending视觉工作项、6页实际观察（其余页未声称检查）及放大图保存在`.work/phase1-b54/review-history/b4ad5c68-b39d-44d8-aca2-5f818414c61c/`。

修复仅涉及：Q18正式项目图稿的A节点在above left基础上xshift=5pt、C节点改below left；全部坐标、曲线、三角形及中线连接不变。当前图稿SHA `56ae647fe6ed07e7255515710d1970977d63c51624359d72ff98e39855cd246c`；旧年度图稿未覆盖，其余卷不受影响。Q20保留完整必要/充分性，以前两列通项直接求行公差，并把奇因子到正整数索引的双向构造写成连续段落，减少显示公式造成的分页占用。数学步骤未删，未改变题面或最终答案，全部逐题provenance及其哈希与0a254ed8相同。

第二轮即最终attempt `27c3e3c9-d9e7-4778-877a-6a37b5dea0f6`，构建输入manifest revision5325、构建后revision5326。四版日志errors/missing_characters/undefined_references/Overfull/Underfull均0，警告豁免0；没有公共样式、字体、页边距或生成器改动。pdfinfo现场确认四版均595.28×841.89pt A4，实际PDF SHA与build/review回执一致。

## 当前四版

| 版本 | 页数 | PDF SHA-256 |
| --- | ---: | --- |
| 试题版 | 4 | `8ed44693a030ad919cad8ccd01135ba4cc7b8105049c908f7546a7a9537c30d4` |
| 解析版 | 17 | `d8e857925cf8e5cc61869bb2308cd4f29eed0c230874f391f8e96a20c91e394f` |
| 简答版 | 6 | `abb926631fe7b95192eb478148354214cfa73685afec2d3e377224a9826ee689` |
| 印刷版 | 13 | `c378d81a910699d3c0c3f8616892de18c87f9404949c46b21ec0177d0adbb3c9` |

可打印PDF保存在项目忽略的build目录，Git提交可复用源、正式回执与报告。

## 实际逐页视觉检查

主代理实际用view_image查看当前attempt全部40张110dpi整页PNG，另查看Q18修正版220dpi局部；没有继承旧attempt的任何视觉结论。八项检查共320项：295pass、25not_applicable、0fail/pending；不适用项均因该页无题图/待核表格标注。页序、PNG SHA、观察、actually_viewed和inherited字段保存在`.work/phase1-b54/review-render/27c3e3c9-d9e7-4778-877a-6a37b5dea0f6/inspection-summary.json`，正式review保存逐页八项记录。

实际检查重点：四版Q17/Q18图线型与标签完整，A/C均避开轴与曲线，Q18长图未碰页脚；Q20完整7×8数阵和全部三个小问保留，解析第17页三个答案框与证明同页，不再存在孤立末页。简答第6页Q19含完整三段函数、正整数定义域、500/1000个对应的6000/11000元利润；解析及印刷版结论一致。题面区无答案，解析/速查区明确非官方独立推导。题号、选项、上下标、公式、页眉页脚和字号逐页检查通过。

## 独立复核、正式状态与验证

只读提交前审阅者`/root/review_2004_science_closeout`检查当前diff及0a254ed8主要登记/答案拆分，独立核算75个输入/PDF/PNG SHA并核对attempt、依赖树、生成输入树、投影和工具链绑定；确认Q20双向证明完整、Q18仅标签锚点改变，未发现实质问题。其不冒充重新实看全部页面，也不代替正式finalize。

`finalize-batch`实际返回FINALIZED，当前manifest revision5327，batch closed、paper complete，build.status=succeeded、review.status=passed，四版edition.result均pass。这里的complete表示本库固定来源题面、独立数学答案和四版构建/视觉门禁已闭合；固定PDF依然是排印副本，出版物、出版者、版次、来源链及官方身份未认证，official_answer=null。没有把本库推导认证为官方答案。

完整回归实际 `Ran 1724 tests in 449.325s` / `OK (skipped=13)`，日志保存在`.work/phase1-b54/verification/full-tests.log`。测试在最终规范源/图稿/生成物稳定后运行，期间仅只读PDF检查和忽略的视觉工作项记录。来源清单/问题总账、provenance、solution_sources、三个生成器、最终build回执当前性、review门禁、报告及775行CSV在提交前复核。

本批完成一套2004北京春季理科卷，不表示1952—2026全集完成。后续可推进2007上海春季卷的固定图像来源转录；2004上海春季卷的Q14包含关系与Q18变量歧义仍需保持待核，不能据预期答案补题。

# phase1-b53：解析回流、四版43页视觉验收与阻断闭合

日期：2026-10-28

## 首轮校样到最终构建

| attempt | 页数（试题/解析/简答/印刷） | 实际发现与处理 |
| --- | --- | --- |
| 422df2e5-ccf1-4e71-9f56-bfedb978280a | 5/18/7/14 | 解析第15页Q18的cos E在等号处分行，Underfull badness1838；规范源分段后重建，未豁免。 |
| 0754a253-fe2a-474d-9bd7-916ec8338ea3 | 5/18/7/14 | 四版零警告，但完整校样发现解析第17页的Q19答案框脱离推导、第18页只有Q20(3)答案框；实际失败记录已归档。 |
| bf351298-4607-4e0e-9a60-7b4b0c49beb3 | 5/17/7/14 | Q19/Q20解析源重排并重建，分页问题消除，当前43页视觉全部通过。 |

Q19保留坐标来源及全部结论，改用行内坐标与逐项系数比较，并补明a=2d的充分性：x=d(m+2)²/2、y=d(m+2)/2，故y²=(d/2)x，取p=d/4>0。历史初稿误算说明仍在答案要点和独立答案阶段报告保留；不作为重复数学正文。Q20(2)恒等变形仅从显示式改为行内。题面、最终答案及其provenance哈希均未改变；无字体、公共样式、页边距或生成器改动。

源稿回流使旧build回执失效，期间provenance检查曾按现场状态拒绝缓存的compiled_pending_review；正式重建事务完成后已恢复一致。最终build回执输入revision5311，当前manifest revision5313；previous_attempt_id为0754a253-fe2a-474d-9bd7-916ec8338ea3。回执绑定输入投影、生成输入树、最终.fls依赖树和工具链。

## 当前四版

| 版本 | 页数 | PDF SHA-256 |
| --- | ---: | --- |
| 试题版 | 5 | `a23351b8c6e62d86e506ae4d8abf3da5f8e51cab31a8357698f182e0d8b225ad` |
| 解析版 | 17 | `d1b553b51dd5dd62b404e92057cbdaacf16a4739fe1162a372f248537f1e54b0` |
| 简答版 | 7 | `819bddfb0161cdd26325cc51da8cfc4977b20d744f79d61b2a553ff8fb90d708` |
| 印刷版 | 14 | `e0cb67281eea38aabd6d55dac121a92573ef6ad0c7bdc402bc157d6c56837688` |

四版errors、missing_characters、undefined_references、Overfull及Underfull均0，现场PDF SHA与回执逐一一致；没有警告豁免。PDF留在忽略的build目录，Git仅提交可复用源和回执。

## 逐页视觉证据

主代理实际查看四版所有页，按八项检查填写当前工作项。最终共43页、344项：325 pass、19 not_applicable、0 fail、0 pending。无题图页的figure_label项均明确写明不适用。

新attempt的解析第16–17页、印刷第13–14页以110dpi重新逐页查看，题干、推导与对应答案框在同页完整，Q20没有孤立末页。其余39页的PNG SHA与已实际检查通过的0754a253逐页完全相同，才继承既有结论；0754a253中尚未看过的页曾全部实看，且没有继承它的失败页。更早422df2e5的继承也仅限实看且PNG字节相同的页。旧review工作项、build及逐页观察保存在`.work/phase1-b53/review-history/<attempt>/`，当前渲染清单和检查摘要在`.work/phase1-b53/review-render/bf351298-4607-4e0e-9a60-7b4b0c49beb3/`。

Q16题面角值缺项与U答案框均清晰保留。试题区没有答案内容；解析/简答区只按版本出现相应答案。图稿、选项、公式、题号、页眉页脚及字号已逐页检查，未发现裁切或标记相碰。

## 最终门禁与边界

`review_receipts.py finalize-batch`已实际返回FINALIZED；review.status为passed，各edition.result为pass，build.status为succeeded。batch为closed_with_blockers，paper仍blocked；ISSUE-1239、ISSUE-1240及Q16的U/未解决冲突继续保留。没有把印载48补成当前题面的确定答案。

完整回归 `Ran 1724 tests in 457.839s` / `OK (skipped=13)`，来源/图稿回归修复详见`reports/spring-source-regression-repair.md`。source manifest、issues、provenance、solution sources、三个生成器、最终构建回执当前性、review门及报告/CSV当前性在提交前核对。

本卷的构建/排版阶段已闭合，来源出版者、版次、来源链与官方身份仍未核，official_answer=null。Q16仍阻断整卷完成；本批不是1952—2026题库完成。

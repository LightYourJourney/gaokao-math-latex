# phase4-b21 1996上海理科 source/math阶段独立提交前终审

2026-10-24；只读复核仓库 仓库根，未修改仓库、未提交、未联网。

## 结论

未发现阻碍本次source/math转录阶段提交的新缺陷，可提交本阶段成果。此结论不等于整卷完成：Q15 A1来源冲突继续未决，整卷production_state必须维持blocked；ISSUE-1136、ISSUE-1137继续open且blocks_completion，Q15须维持U/unresolved，不能以补列两个数学解或补全转录为由关闭。

## 实际复验与证据

1. 本轮最新四份规范MD、来源校对.json、七份TikZ及source/math最终报告的范围一致。题面开头现已明确主要在p1—4、Q24末尾续p5；JSON Q24 question_continues_on:[5]以及page_map p5/p7角色已补，前次source-final报告所提页范围收尾已实际完成。旧报告“本次读取时”段落是历史时间点记录，不能当成现存未修复项。
2. Q17 A1两类书各自相邻条件、A1/A2非试点与B1/B2试点、混选只计A组、选择/填空计分规则、小问分值保持与全9页源核结论一致。
3. Q19—24累计评分节点与原source-final结论一致；解析的“来源评分说明摘要”明确题末集中列出节点、不是小问分值、逐步位置以固定源为准。Q1—18编者推导均区分为非来源原载。
4. Q8 C/D根相对±1的关系、Q7四O、Q20去新增投影线/开圈、Q21 MN与中点构造及两平面标签、Q23实线渐近线均仍保留。图源码几何结构与源核报告一致；不把代码阅读代替最终PDF压线/裁切验收。
5. 现场实算来源校对.json draft_sha256与当前题面MD一致；七份figure_files的sha256全与磁盘文件相符。固定源SHA-256继续为3c0c6b1da5ad37389f6cccf555c72188500787510e60b9902af8d51c97bb1f18。official_answer仍null，source_authenticity仍publisher-unverified。
6. 现场读取source-manifest对应paper记录：production_state=blocked，issue_ids同时含ISSUE-1136与ISSUE-1137；missing-issues两条均status=open、impact=blocks_completion，1137恢复动作明确“保持U级与unresolved，不得标完成”。题面仍原样“直线OA”，答案/解析未冒充已消除冲突。
7. 现场读取本卷provenance.json中的Q15逐题记录，answer_evidence.grade="U"、conflict_status="unresolved"、issue_ids同时含ISSUE-1136/1137；题号15及固定源SHA-256归属正确。转录核验passed仅表示忠实记录来源，不升级答案证据等级。
8. 现场运行 python3 -m unittest discover -s math-gaokao-latex/tests -p test_1996_shanghai_science_sources.py：8 tests，全部OK。

## 验收界限

本报告终审的是source/math转录阶段。正式build正在主代理处进行；本代理已亲查provenance.json的Q15 U/unresolved与两个issue IDs，未改写状态。四版PDF视觉及最终回执有效性由接续阶段验证，不能据本报告设置整卷complete。

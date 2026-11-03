# 2005 上海理科普通卷：规范事实源与内部卷登记

- 日期：2026-11-03。
- 固定候选来源：src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e，PDF SHA-256 092e8e90dc1430ab2fa8b8ce79e072e317559e6bef29f1cb7461e9423925ec31，Git blob a76d7aa8877b7fa25ac09cb596b440c0545f4fa6，2页A3、印刷页262–263。
- 新规范题面 2005/2005_数学真题_上海理_试题.md SHA-256：2af066bb79bf8296a8aea3710d656bf5ee91020fe00941d55d6a97651aaf27c5。
- 绑定内部 paper ID 并经规范生成后，答案要点 SHA-256：169d5cd8efa2e7621c8e48507b5f7c0f574da701148e5fa905543ba291726c68；解析正文 SHA-256：98a79fefe99423146eacc36995d4ec3b0bdf612db438d4d096a35d9ce18e2eb0。
- 当前含解析派生稿 SHA-256：bec50e1a667010b52792cc579be058d39c4cd5c4649c4dd54b0fe274a84f41a8；包含22题，加入图链后须按规范重新生成。

## 登记结果

- 通过 source_manifest.py register-papers --write 建立 gk-2005-regular-shanghai-science，批次 phase4-b44，manifest revision 6109→6110。固定 PDF 与内部卷的关系登记为 canonical，仅表示本项目将该候选 PDF 用作这套内部转录的来源绑定，不表示已认证发布者、版次、复制链或官方身份。
- 题卷状态为 blocked；批次状态 planned。自动建立两条完成阻塞问题：ISSUE-1380（Q11“最小”是否要求唯一最小）和 ISSUE-1381（Q20(1)原文“中低价层”与上下文“中低价房”冲突）。题面继续照录原字，两个条件结论均保留 U/PENDING。
- 登记后的规范事实源路径为 _试题.md、_答案要点.md、_解析正文.md；_含解析.md 是展示派生物，不作为事实源。来源页仅题面，official_answer=null。

## 校验与剩余

- source_manifest.py validate --manifest source-manifest.json 通过；issues.py validate --file missing-issues.md 通过；solution_sources.extract-batch --write 后 check-batch 通过（22题）；manifest_csv.py --write 后 --check 通过，当前775行。
- 本阶段未生成 Q11/Q17/Q19 图稿，manifest figure_files 暂空；尚未建立逐题 provenance、TeX/简答/四版入口、正式构建或视觉回执。下一阶段依据固定原图重绘三张题图、在规范题面插入图链，再通过 solution_sources.py extract-batch --write 和 source_manifest.py sync-figure-registry --write 更新派生稿与登记图引用次数。
- 本阶段 OCR 与外部 API 调用为0，人工耗时未知。来源发布身份与官方答案均未核。本登记不代表来源认证、整卷闭环或长期语料完成。

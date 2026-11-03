# 2004 上海理科普通卷：规范事实源与内部卷登记

- 日期：2026-11-04。
- 固定候选来源：`src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a`，PDF SHA-256 `9f6c7f71c18bcdc3dd863fc846636661eacc03b4d3837feeaafcd36258c2be5e`，Git blob `9bfec0f8159c4aac8d9991979f2afd760fb0c11b`，2页A3、印刷页198–199。
- 规范题面 `2004/2004_数学真题_上海理_试题.md` SHA-256：`1238628877a236c72f70d4a5b9ccdfbff45d39dfa501a584d3bc04ad9136b2cb`。
- 绑定内部 paper ID 后，答案要点 SHA-256：`4325b1a3193de2075d6fc26fea9fbd566a5217e1c6c465c63d0eb1a327c686d6`；解析正文 SHA-256：`aff77054a2fccffdc1fe231e6335a18e7369372877f9fbaf50acceca30b39726`。
- 当前含解析派生稿 SHA-256：`aab6475202e5ff82de8a652be7836ff9e18f6c2770de74c69dd4592a07cee90d`；包含22题，加入图链后须按规范重新生成。

## 登记结果

- 通过 `source_manifest.py register-papers --write` 建立 `gk-2004-regular-shanghai-science`，批次 `phase4-b46`，manifest revision 6123→6124。固定 PDF 与内部卷的关系登记为 canonical，仅表示本项目将该候选 PDF 用作这套内部转录的来源绑定，不表示已认证发布者、版次、复制链或官方身份。
- 题卷状态为 `blocked`；批次状态 `planned`。自动建立两条完成阻塞问题：`ISSUE-1386`（Q19(2) 题面印作“若 B ⊆ A”但未定义集合 B 疑点）和 `ISSUE-1387`（Q22(1) 点 $P_1(3, 0)$ 不在椭圆上且 $S_3 = 255$ 在实数范围内无对应曲线上的点 $P_3$ 疑点）。题面继续照录原字，两题存疑结论均保留 U/PENDING。
- 登记后的规范事实源路径为 `_试题.md`、`_答案要点.md`、`_解析正文.md`；`_含解析.md` 是展示派生物，不作为事实源。来源页仅题面，`official_answer=null`。

## 校验与剩余

- `source_manifest.py validate --manifest source-manifest.json` 通过；`issues.py validate --file missing-issues.md` 通过；`solution_sources.py check-batch --manifest source-manifest.json --batch phase4-b46` 通过（22题）；`manifest_csv.py --write` 后 `--check` 通过，当前775行。
- 本阶段未生成 Q5/Q18/Q21 图稿，manifest `figure_files` 暂空；尚未建立逐题 provenance、TeX/简答/四版入口、正式构建或视觉回执。下一阶段依据固定原图重绘三张题图、在规范题面插入图链，再通过 `solution_sources.py extract-batch --write` 和 `source_manifest.py sync-figure-registry --write` 更新派生稿与登记图引用次数。
- 本阶段 OCR 与外部 API 调用为0，人工耗时未知。来源发布身份与官方答案均未核。本登记不代表来源认证、整卷闭环或长期语料完成。

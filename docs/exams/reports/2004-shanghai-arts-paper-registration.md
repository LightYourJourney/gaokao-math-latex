# 2004 上海文科普通卷：规范事实源与内部卷登记

- 日期：2026-11-03。
- 固定候选来源：`src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290`，PDF SHA-256 `4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad`，Git blob `302ee6023a26b028cf7c89f24359ba818a2a7b3b`，2页A3、印刷页200–201。
- 规范题面 `2004/2004_数学真题_上海文_试题.md` SHA-256：`752a56c8eb0a6b91d24282686f682dd3f3084dffdaa8daaa4fbb1bc063094d4b`。
- 绑定内部 paper ID 后，答案要点 SHA-256：`6b2938f6841a70b3eea3775713fbe8a2914fa3d65dfd6a52b30d5a91b94aaad2`；解析正文 SHA-256：`61ec23b36e7d8e8d5ba051f35a28c015d73309f0cdd6fb42150b7a05eca25ac5`。
- 当前含解析派生稿 SHA-256：`3129a581881e143a9273dea0658a0cbc11099ccd3eb26b20d93debfaf0092d74`；包含22题，加入图链后须按规范重新生成。

## 登记结果

- 通过 `source_manifest.py register-papers --write` 建立 `gk-2004-regular-shanghai-arts`，批次 `phase4-b45`，manifest revision 6117→6118。固定 PDF 与内部卷的关系登记为 canonical，仅表示本项目将该候选 PDF 用作这套内部转录的来源绑定，不表示已认证发布者、版次、复制链或官方身份。
- 题卷状态为 `blocked`；批次状态 `planned`。自动建立两条完成阻塞问题：`ISSUE-1384`（Q17 实数范围内无解疑点）和 `ISSUE-1385`（Q19(2) 题面印作“若 B ⊆ A”但未定义集合 B 疑点）。题面继续照录原字，两题存疑结论均保留 U/PENDING。
- 登记后的规范事实源路径为 `_试题.md`、`_答案要点.md`、`_解析正文.md`；`_含解析.md` 是展示派生物，不作为事实源。来源页仅题面，`official_answer=null`。

## 校验与剩余

- `source_manifest.py validate --manifest source-manifest.json` 通过；`issues.py validate --file missing-issues.md` 通过；`solution_sources.extract-batch --write` 后 `check-batch` 通过（22题）；`manifest_csv.py --write` 后 `--check` 通过，当前775行。
- 本阶段未生成 Q5/Q18/Q20/Q21 图稿，manifest `figure_files` 暂空；尚未建立逐题 provenance、TeX/简答/四版入口、正式构建或视觉回执。下一阶段依据固定原图重绘四张题图、在规范题面插入图链，再通过 `solution_sources.py extract-batch --write` 和 `source_manifest.py sync-figure-registry --write` 更新派生稿与登记图引用次数。
- 本阶段 OCR 与外部 API 调用为0，人工耗时未知。来源发布身份与官方答案均未核。本登记不代表来源认证、整卷闭环或长期语料完成。

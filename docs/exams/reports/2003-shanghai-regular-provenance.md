# 2003 上海普通卷文理科：逐题 provenance 导入

- 日期：2026-11-04；batch `phase4-b47`；manifest revision `6135→6136`。
- 文科 paper `gk-2003-regular-shanghai-arts` 绑定 source `src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4`，PDF SHA-256 `ffd59c395a0c675118f6da576e48842549c4afa031d923448f26f33087bc7e85`。
- 理科 paper `gk-2003-regular-shanghai-science` 绑定 source `src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0`，PDF SHA-256 `88b72fea05d331215504bb89257e375d07c18ba21e830cf9e6288461e88ccf8d`。

## 逐题记录

- 每卷 Q1–Q22 均有 question-review、answer-solve、answer-review 三角色记录；来源页码按固定 PDF 第1页 Q1–Q19、第2页 Q20–Q22登记。题面与答案哈希由 `provenance.py` 按规范源现场重算，随后正式写入文理项目 `provenance.json`。
- 独立题面复核者未参与转录；主会话另对最终题面与图注改动复看固定原页。`transcription_review.result=passed` 仅表示与固定页图相符，不认证候选来源身份、发布者、版次或复制链。理科 Q22 的 PDF 文字层错配依可见页图判读，详见题面复核报告。
- 答案来源为独立盲解及主会话逐题复核，固定 PDF 均不含答案页，因此 42 题记录为本库推导 `D`，不是官方答案。两卷 Q14 均记录 `grade=U`、`conflict_status=none`：问题属于题面未说明平面是否互异造成的约定歧义，并无两个答案来源互相冲突。
- 文科 Q14 关联 `ISSUE-1388`，理科 Q14 关联 `ISSUE-1389`；两项保持 open / blocks_completion。答案记录仍为 U/PENDING；默认两平面互异时 D 仅是条件性预期答案。

## 校验与阶段边界

- `provenance.py import-batch` dry-run 与 `--write` 均成功；`provenance.py check-batch` 输出 `OK：2 卷`。`source_manifest.py validate`、`issues.py validate` 成功；`manifest_csv.py --check` 输出 `manifest.csv 当前且 775 行`。
- 当前推导状态：两 paper `blocked`，batch `provenance_verified`。来源身份与官方答案仍未核。
- 本阶段未调用 OCR、联网或模型，未生成项目 TeX、四版 PDF、formal build receipt、视觉 review receipt 或 batch closeout receipt。下一步运行三类生成器的确定性检查，再生成、构建并逐页检查正式输出；未决 Q14 blockers 不得清除。

本报告仅记录逐题来源与答案证据，不表示官方身份认证、单卷完整或长期语料库完成。

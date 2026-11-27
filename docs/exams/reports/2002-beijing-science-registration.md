# 2002 北京理科候选卷：paper/source 登记

- 日期：2026-11-03。
- 固定 source `src-6b6e5d61614e04d9b61330de2c085ab84c2f6fddfca9e6f357695a7ba074e690`，SHA-256 `4e19a0d37e74a41655156769e6cb72c2532ec2939cb6fe4d7b18db205123de73`，Git blob `e6b19791b1fe3ca2e49404428b746bb36c460f12`。上游路径 `普通高考/2002/2002北京理.pdf`，固定上游 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。manifest 中的 `canonical` 只表示本库选择此固定输入，不认证发布者、出版者、版次、来源链或官方身份。
- `register-papers` dry-run 通过后，以单一状态事务登记 paper `gk-2002-regular-beijing-science` 与 batch `phase1-b82`，绑定 source `canonical`；manifest revision `6034→6035`，transaction `ef5f6a92-8d8c-4716-ad87-61dc3a240310`。题量 22，track 为 `science`，题面 PDF 页 `[1,2]`，来源答案页 `pages_s=null`。

## 未决问题

- `ISSUE-1360`（Q16，`answer-missing`，open / `blocks_completion`）：固定式配方后为 `(x-1)^2+(y-1)^2=-6`，没有实圆，切点与面积无定义。题面保持原式，答案为 U/PENDING，不猜系数或答案。
- `ISSUE-1361`（Q19，`answer-missing`，open / `blocks_completion`）：原件开头与第（3）问称 `{a_n}`，递推及所问极限使用 `x_n`。原字照录；本项目只对明确递推的 `x_n` 推得极限 `√a`，不把它改成 `{a_n}`。该问题按既有变量不一致先例入账，待同版勘误或权威同版说明。
- 两条 issue 均使 paper `production_state=blocked`、`blocked_from=planned`；batch 当前为 `planned`。`official_answer=null`。

## 同步和验证

题面、答案要点与解析正文的 `paper_id` 已绑定新 paper；题面状态说明改为内部 canonical 输入；答案/解析 frontmatter 指向独立答案盲核报告。`_含解析.md` 由 `solution_sources.py extract-batch --batch phase1-b82 --write` 重建。登记时 `figure_files=[]`，Q11、Q12、Q18 图稿仍待完成。

已执行并通过：

- `source_manifest.py register-papers` dry-run 与事务写入。
- `source_manifest.py validate --manifest source-manifest.json`。
- `issues.py validate --file missing-issues.md`。
- `solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b82`：1 卷、22 题通过。
- `manifest_csv.py --write`：更新为 775 行；提交前再运行 `--check`。

## 阶段边界

本阶段未导入逐题 provenance，未绘制 Q11/Q12/Q18 图稿，未生成共享 TeX、简答及四版入口，未做正式构建、页面视觉审查或生成回执。OCR 部署的 Xiaomi、Paddle 与 MinerU doctor 状态均为 ready；固定 PDF 两页均为完整文字层，本卷未调用 OCR。下一阶段先完成三幅图并同步题面映射、manifest、生成与 provenance，再继续确定性项目生成和正式收口。本报告只记录一卷内部 source/paper 绑定，不表示来源认证、题目无阻断或长期语料完成。

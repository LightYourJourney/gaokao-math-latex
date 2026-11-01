# 2006 山东文理候选卷：paper/source 登记

日期：2026-11-02；批次：`phase1-b68`。

## 登记结果

- `gk-2006-regular-shandong-arts`：track `arts`，22题，绑定候选 source `src-a957620ac8adeec8abc02ef4bf8beb3bb89a7288cc7f086069fac46ed7dd63f2`，SHA-256 `dfa18cc6724fb66fe5f8f2fbc84e309d2ea709b3c91e6675acea06c2be05cf42`。当前 `production_state=planned`，没有逐题 blocker。
- `gk-2006-regular-shandong-science`：track `science`，22题，绑定候选 source `src-58e17c4f7678bc58e38a926d939e980fac0868d781ca9da87efeeed6bf6c6947`，SHA-256 `8cd7733727ed4ff238dedc4a1c7cb42773260de88f1d516f0416cbaa3976393b`。当前 `production_state=blocked`。
- `source_manifest.py register-papers` dry-run 返回 `OK`，计划批次为 `phase1-b68`，2卷；新增问题编号 `ISSUE-1294`–`ISSUE-1297`。正式事务写入后 manifest revision 从5781升至5782，并在两个 source 记录中回写本库 canonical paper 绑定。
- 固定来源仍仅称题签所示的本地候选题面副本。此登记固定本库工作输入，不认证出版者、版次、来源链或考试机构官方身份。答案层均保留 `official_answer: null`。

## 未决问题

- `ISSUE-1294`：理科 Q5 的向量闭合结果为 $(-2,-12)$，四个选项均不匹配（`answer-conflict`）。
- `ISSUE-1295`：理科 Q5 固定题面副本没有答案、解析、评分材料或勘误，且现有结果无法成为可核答案来源（`answer-missing`）。
- `ISSUE-1296`：理科 Q10 由系数比得 $n=10$，但常数项需要 $k=60/7$，题面按此没有常数项（`answer-conflict`）。
- `ISSUE-1297`：理科 Q10 固定题面副本没有答案、解析、评分材料或勘误，不能确定预期表达式或答案（`answer-missing`）。

四项均为 `open` / `blocks_completion`。题面照录、答案保持 U/PENDING；未推测应修改的文字、选项或“官方答案”。

## 登记后验证

- 登记前已有两卷规范题面、答案要点、解析正文及以 `solution_sources.render_combined` 生成的初始 `_含解析.md`。
- 登记后将 `paper_id` 写入两卷三层规范源，并运行 `solution_sources.py extract-batch --manifest source-manifest.json --batch phase1-b68 --write`，实际提交4个派生目标。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b68` 和 `git diff --check` 均通过。
- 尚未导入逐题 provenance，未登记题图文件，未生成 TeX/简答/印刷项目，未构建正式 PDF 或生成构建/视觉回执。下一步初始化 `phase1-b68` 三角色 provenance，随后办理图稿与项目生成。

本阶段不表示来源认证、两卷完成或 1952–2026 长期语料完成。

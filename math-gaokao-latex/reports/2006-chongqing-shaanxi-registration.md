# 2006 重庆、陕西文理候选卷：paper/source 登记与确定性合并稿

- 日期：2026-11-03。
- 范围：一次事务登记重庆文、重庆理、陕西文、陕西理四卷及批次 `phase1-b80`。登记前 `register-papers` dry-run 校验四卷规格通过；正式事务将 `source-manifest.json` revision 从 5995 推进到 5996。
- Paper IDs：`gk-2006-regular-chongqing-arts`、`gk-2006-regular-chongqing-science`、`gk-2006-regular-shaanxi-arts`、`gk-2006-regular-shaanxi-science`。批次登记状态为 `planned`。
- 四个候选 source 由未绑定改为仓库内部 `canonical` 对应关系；该关系仅固定本库此次使用的 PDF 字节，不认证发布者、出版者、版次、来源链或官方身份。四份 PDF 均为两页题面，没有答案、解析或评分材料；所有规范源仍为 `official_answer: null`。

## 规范源与合并输出

四卷 `_试题.md`、`_答案要点.md`、`_解析正文.md` 的 frontmatter 均已绑定对应 paper ID；运行 `python3 math-gaokao-latex/tools/solution_sources.py extract-batch --manifest math-gaokao-latex/source-manifest.json --batch phase1-b80 --write` 生成四份 `_含解析.md`。

| 卷别 | 含解析稿 SHA-256 |
|---|---|
| 重庆文科 | `a9febb717aba5b5b3eb43d6785be600aca66491a76746d9539407e67fd8c8429` |
| 重庆理科 | `9384e4a74c59099da946d94a17c9f0c380ebc81e05277f7f6de2ae3bc28f466b` |
| 陕西文科 | `a1fa616290806fc8b36daf1b4fb5976874d3c1196288ad5824127a321dd1e1a8` |
| 陕西理科 | `9db7a12b45f1b8686ffeaac9856e32ecfb2d9ddd99aa5a20f80f59f69253c015` |

四份合并稿分别以相同规范题面、解析正文和答案要点重新调用 `render_combined` 后逐字一致；每份均解析出连续 Q1–Q22。来源题签、印刷页和 PDF SHA-256 见 `reports/2006-chongqing-shaanxi-question-transcription.md`。

## 已登记的逐题阻断

- `ISSUE-1341`：重庆理 Q20(1) 原印条件使用函数定义中没有的字母 \(a\)；题面照录，答案与解析保留 U/PENDING，不推测修成 \(c\)。
- `ISSUE-1342`：陕西文 Q3 仅给 \(a_1+a_8=8\)，满足条件的正项数列可分别得到 \(S_9=36\) 与 \(81/2\)；保留 U/PENDING，不从选项反推缺失条件。
- `ISSUE-1343`：陕西文 Q15 的可读原句“甲和乙不同去”不能唯一确定选派关系；保留原字和 U/PENDING。
- `ISSUE-1344`：陕西理 Q16 同有“甲和乙不同去”语义未决；保留原字和 U/PENDING。

因此重庆文科 paper 保持 `planned` 且无 issue；其余三卷按登记规则为 `blocked`，`blocked_from=planned`。paper 记录中没有伪造来源认证或官方答案结论。

## 验证与剩余阶段

- `source_manifest.py validate`：退出 0。
- `issues.py validate --file math-gaokao-latex/missing-issues.md`：退出 0。
- `solution_sources.py check-batch --batch phase1-b80`：四卷全部通过，每卷 22 题。
- `manifest_csv.py --write` 后 `--check`：当前，775 行。
- 四份含解析稿与内存 `render_combined` 逐字节一致；`git diff --check` 通过。
- 尚未登记三角色逐题 provenance，尚有 10 个题图占位待按固定原页重绘和登记；未生成 TeX 项目、正式构建 PDF、建立构建/视觉回执或逐页验收。成本数据未知。本阶段不表示四卷完成或长期语料完成。

# 2006 江西、浙江、湖北理科候选卷：paper/source 登记

日期：2026-11-02。

## 登记范围

批次 `phase1-b70` 登记三套题面已转录、独立答案与解析草稿已形成的候选卷。`register-papers` dry-run 后通过同一事务写入 manifest revision 5879（从 5878 推进）：

| Paper ID | 固定 Source ID | 题数 | 当前状态 |
|---|---|---:|---|
| `gk-2006-regular-jiangxi-science` | `src-087e91818b6473a217dd7dda423b4d033dad9f20e1e6f77e162d3dce4d896817` | 22 | `planned` |
| `gk-2006-regular-zhejiang-science` | `src-5f9ed6381f35350f76a93adb34b280d596a9d44d2b40366565ac3df18645ab6a` | 20 | `planned` |
| `gk-2006-regular-hubei-science` | `src-3e4d37728fe026360081acff678b849c40c747cd67ac478230a0040ead794c42` | 21 | `blocked` |

三个 Source ID 均绑定固定候选 PDF，manifest 中记录的 SHA-256 与 intake 报告一致。绑定只标识本库采用的固定副本，不认证发布者、出版者、版次、扫描来源链或官方原件身份。三份 PDF 仅含题面，没有答案、解析或评分页；所有 `official_answer` 字段继续为 null。

## 问题与状态

湖北 Q17（2）由题面给出 `a₁=1`、`a₂=7`，所以 `T₁=m/7`；而题设要求所有正整数 n 均有 `Tₙ<m/20`，n=1 即导致矛盾。原题和 U/PENDING 状态未改写。登记新增：

- `ISSUE-1319`：Q17 题面与约束冲突，等待同版可靠复本、正式勘误或其他可追溯裁决材料。
- `ISSUE-1320`：Q17 答案材料缺失且现有题面矛盾，答案继续 U/PENDING，不推定官方答案。

问题均为 open / `blocks_completion`。因此湖北 paper 为 `blocked`（`blocked_from=planned`）；该批次仍为 `planned`。

## 规范文件与检查

三卷题面、答案要点及解析正文 frontmatter 已写入对应 `paper_id`。三份 `_含解析.md` 由 `solution_sources.render_combined` 从规范题面、解析正文和答案要点确定性生成。登记索引记录的题数结构为江西 12/4/6、浙江 10/4/6、湖北 10/6/5（选择/填空/解答）。题图文件尚未制作或登记：江西 Q12；浙江 Q9、Q14、Q15、Q17、Q19、Q20；湖北 Q15 示例与 Q18。

验证：`register-papers` dry-run 与写入成功；`source_manifest.py validate`、`issues.py validate` 通过；`solution_sources.py check-batch --batch phase1-b70` 显示三卷全部通过，分别识别 22、20、21 题。

## 后续边界

尚未建立逐题 question-review / answer-solve / answer-review provenance，未制作图稿，未生成项目 TeX/简答版，未正式构建 PDF 或完成视觉检查。本登记阶段不表示来源认证、答案官方认证、批次闭环或长期语料完成。

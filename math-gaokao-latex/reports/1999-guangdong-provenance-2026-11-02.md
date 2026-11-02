# 1999 广东卷逐题 provenance 导入（phase1-b72）

## 三角色记录

- 批次 `phase1-b72` 为 Q1–Q22 分别导入 `question-review`、`answer-solve`、`answer-review` 三角色，共 66 条逐题记录。题面复核绑定固定 source ID、PDF SHA-256 与物理页码；题面文本哈希及答案哈希由工具按当前规范源现场计算。
- `question-review` 依据固定扫描副本逐栏核验题目、公式、选项、小问和图位。Q10（“面 AC”指称）、Q13（F/F1 与重复尾句）、Q21（函数记号及列式）虽按可见字样忠实转录，其语义仍未决；对应记录标为 `uncertain` 并挂接题面问题。
- `answer-solve` 依据题面独立求解；`answer-review` 复核答案层与解析结论。Q10、Q13、Q21 的答案证据等级为 U，分别关联既有答案 blocker；Q14 的 12 以“至少空出 6 垄”解释并与固定副本 A 型答案栏一致，记为 B 级。其余题按解析与独立核算证据记录。角色名两两不同。

## 状态与验证

- 导入事务将 manifest revision `5899→5900`；paper 因 `ISSUE-1323`–`ISSUE-1328` 仍为 `blocked`，batch 进入 `provenance_verified`。此状态只表示三角色 provenance 结构与当前源哈希校验通过，不表示题意 blocker 解除。
- `provenance.py import-batch` 只读预检与写入均通过；`provenance.py check-batch --batch phase1-b72` 返回 `OK：1 卷`。逐题 source 页面、来源 SHA、question-text 哈希、answer 哈希、角色身份及 issue 关联均由工具校验。
- provenance 不认证来源发布者、出版者、版次、复制链或官方答案。`official_answer` 仍为 null，A/B 卷型关系仍未知。

## 后续门禁

尚未正式编译四版 PDF，未逐页审查最终版面、生成构建/视觉收据或收口批次。六条未决问题保持 open / `blocks_completion`；下一阶段执行四版正式构建并按页复核。本记录不表示试卷完成或长期题库完成。

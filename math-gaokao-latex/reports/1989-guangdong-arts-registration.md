# 1989 广东文科候选卷：内部登记与阻断项

日期：2026-10-30

## 内部候选绑定

- 登记批次 `phase1-b59`、卷件 `gk-1989-regular-guangdong-arts`，题量30，`track=arts`；登记事务将 manifest revision 从 `5470` 推进到 `5471`；随后图引用计数窄事务推进至 `5472`。
- 固定来源 `src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766`，文件 `普通高考/1989/1989广东文.pdf`，SHA-256 `e0b112f4d4576e791844332f7ffb465c65f3a3ba6516467a7888f9333ca7169f`，9页。PDF题签仅见“文史类”；年份、广东地区、出版者、版次及官方身份未核。manifest 的 `canonical` 只表示本库选用这份固定字节，不构成来源认证；`source_authenticity=unverified`、`official_answer=null`。
- 题面原卷第二卷“一”至“五”对应内部第26—30题，映射由 `printed-label` 保留。3幅 TikZ 图按规范 Markdown 实际引用数登记：Q12选项图2处、Q28题面图2处、Q28来源解答图1处。

## 阻断项

| Issue | 题目 | 类型 | 当前状态 |
|---|---:|---|---|
| ISSUE-1259 | Q9 | `answer-conflict` | open / blocks_completion：题面推得B，扫描答案表印C |
| ISSUE-1260 | Q16 | `answer-convention-ambiguous` | open / blocks_completion：方向垂直与共同公垂线解释不同 |
| ISSUE-1261 | Q21 | `answer-conflict` | open / blocks_completion：A项原文为a≤3，题面条件推得a≤−3，四项无完全匹配 |

三条均保留 U/PENDING；paper 状态为 `blocked`，批次为 `planned`。来源校对 sidecar 保留 `canonical_question_source_ready=false`：现有数学复核以转录文本为对象，不等同于整份 PDF 题面逐字独立校勘。

## 阶段边界与下一步

- 注册前只读预检通过；注册事务原子写入 manifest、source 反向绑定和 `missing-issues.md`。图数复核后通过 `sync-figure-occurrences` 窄事务只更新 Q28 来源解答图的登记值（2→1）。
- `solution_sources` 确定性生成检查确认题面、答案、解析各30题对齐；三条问题答案均为 U/PENDING。
- 尚未导入逐题三角色 provenance，未生成项目 TeX / 四版入口，未构建或视觉验收 PDF；本阶段未运行测试套件。
- 下一步依据已存在的题面复核、独立答案和扫描来源记录建立逐题 provenance，保持来源真实性未认证与三项阻断。

# phase1-b58：2005 春季北京文/理卷登记与逐题核验

日期：2026-10-30

工作树：`仓库根`

分支：`feat/gaokao-phase0`

## 当前阶段

两卷各 20 题的题面、答案要点与解析正文已规范化；固定题面 source、8 幅 TikZ 图稿及 40 题 provenance 已登记。source manifest revision `5448 → 5449` 完成纸卷登记，`5449 → 5450` 完成 provenance 导入。当前 manifest 状态：两个 paper 均为 `answers_verified`，批次 `phase1-b58` 为 `provenance_verified`。

这不是 PDF 生产或视觉验收完成，也不表示语料库完成。

## 固定来源与边界

| 卷别 | Source ID / SHA-256 | 页码 | 题面范围 |
|---|---|---|---|
| 春季北京文科 | `src-62dbddff15a86738e785c92afc5ba358ecaaf0b339911e508a4581333007a7e5` / `698a85348a8a0f96bfc3fec8be3113f19b646d20215bb9c4d9b520cfadee42ae` | PDF 2 页；印刷页 215–216 | Q1–17 在 PDF 第 1 页，Q18–20 在第 2 页 |
| 春季北京理科 | `src-786c297176584bdd68013a9c78428a46275919a77cb2f2ba2af059eb5e019901` / `d9ca7414ddbc1043ee487b49523694ef20db7e41511d5a44d0b78fe20870e5fe` | PDF 2 页；页脚 213–214 | Q1–17 在 PDF 第 1 页，Q18–20 在第 2 页 |

登记只把固定字节绑定为本库 canonical 输入，不认证发布者、版次或来源链。两份固定 PDF 均只有题面页，没有官方答案页；全部答案是 D 级项目独立推导，`official_answer: null`。

## 完成内容

- 文、理卷题面统一为解析器支持的题号格式，并在小问标记后补齐分隔空格；理科题号原有 PDF 页信息改存 HTML 注释，逐题 PDF 页映射另记于 provenance。
- 重建逐题答案块，使题号、答案和解答题小问锚点与题面一致；解析正文只保留推导，不复述独立最终答案。仓库确定性工具生成两份 `_含解析.md`。
- 每卷 Q2、Q12、Q16、Q18 共 8 幅 TikZ 图稿移入项目目录；题面 Markdown、图表清单和 manifest `figure_files` 已同步，每幅图预期在题面及含解析稿各引用一次。8 个 standalone XeLaTeX 预览已编译并目视检查，覆盖本地构图与标注；尚无正式四版 PDF。
- 盲核者只读取各自题面 Markdown 与直接链接的 TikZ 图稿，独立计算 Q1–Q20。两卷共 40 题均与规范答案块相符。文科盲核初始结果表 Q1 的虚部符号和其自身推导矛盾，盲核者复查后确认应为 `-2-i`；规范答案原已正确，无源文件改动。两份盲核均指出 Q12 原题未画拼接后的形态；按标准整侧面贴合并排除立方体后，不改变答案，保留为非阻断的解释边界。理科 Q19 照录“汽车站的平均速度”原词，按同题变量 `v` 解释，未改题面。
- 正式 provenance 写入 40 条记录，记录源页、题面哈希、答案哈希、D 级解题角色及独立盲核角色。没有登记缺失官方答案或来源冲突问题；发布者、版次和来源链仍未知。

## 已执行的验证

- `source_manifest.py register-papers` dry-run 与写入通过。
- `source_manifest.py validate --manifest ...` 退出码 0。
- `solution_sources.py check-batch --batch phase1-b58`：两卷各 20 题通过。
- `provenance.py import-batch` dry-run 通过；写入 revision 5450 后 `provenance.py check-batch` 返回 `OK：2 卷`。
- 两次 `sync-figure-registry` 校验均确认每卷 4 张图、每图 2 次引用；登记规格中的引用数已准确，无需再改 manifest。
- 未运行单元测试或完整测试套件。未生成四版 TeX/PDF，也未创建正式 build/review receipt 或进行正式逐页 PDF 校样。

## 文件与后续

本阶段修改集中于 `2005/` 的两套规范 Markdown、`math-gaokao-latex/` 的 source manifest、两套项目图稿、provenance、报告与进度登记。构建、PDF、视觉回执及最终 batch closeout 留待下一阶段。OCR/API、人工耗时、token 与费用均未知。

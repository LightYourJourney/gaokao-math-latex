# 2021 上海春季卷：Q17 图稿、正式登记与逐题 provenance

日期：2026-10-29

状态：paper/source 已登记；21 题 provenance 已导入，批次 `phase1-b57` 为 `provenance_verified`。试卷因 Q9、Q12 两条开放问题保持 `blocked`。规范源与四个 TeX 入口已确定性生成；正式 XeLaTeX 构建、四版 PDF 视觉复核与回执尚未进行。

## 固定来源与题面复核

- 固定输入 `春季高考/2021/2021春季上海.pdf`：source `src-7ae0174ccd32fd350e3842a1514ae63a3d1bf1bfb082340400feec85431fc1b1`，SHA-256 `fab47237bfe016b5290c753ef2fb0155c72624d16e9a81523ad45f5e87663e1e`，12 页。PDF 首页称“网络收集版”；出版者、版次、复制来源链及附载参考答案的官方身份未核。manifest canonical 绑定只表示本库固定副本与该 paper 的内部对应关系，`official_answer=null`。
- 题面 Q1–14 位于 PDF 第 1 页，Q15–20 位于第 2 页，Q21 跨第 2–3 页。主会话于本阶段重新目视三页并逐题对照题号、文字、公式、选项、小问和页码；这是主会话复核，**没有独立第二位转录者**。Q9、Q12 的原字样照录。
- Q17 图按 PDF 第 2 页重绘为 `2021_春季上海卷/figures/f2021_shanghai_spring_q17_pyramid.tex`。保留 P、A–F 顶点与可见线段拓扑/虚实线；不增加直角符号和长度标记，坐标仅作示意投影。题面 Markdown 独立段落链接与 manifest 的 `figure_files` 均已登记，预期引用 2 次；生成映射由现有工具从 manifest 与 Markdown 链接动态读取，没有改公共生成器。TikZ standalone 预览以 XeLaTeX 编译成功并与源页目视对照；这不是正式试卷版面校样。

## 独立推导与未决项

- 三段只读求解分别覆盖 Q1–7、Q8–14、Q15–21；主会话复核答案和推导，全部标为本库非官方独立答案。主会话逐页核题并非盲转录，答案复核也不声称独立盲评。
- Q9：若递推定义允许公比 `q=0`，范围为 `(-4,4)`；若命题约定排除 `q=0`，范围为 `(-4,0)∪(0,4)`。没有本卷定义证据，答案保持 U/PENDING，新增 `ISSUE-1251`（convention，blocks_completion）。
- Q12：照录的 `∀n∈N*，∃φ∈R` 量词下，对每个 `θ>0` 可取 `φ=π−nθ`，因而没有最小正值；固定副本参考答 `2π/5` 与题面不相容。未调换量词，新增 `ISSUE-1252`（conflict，blocks_completion）。
- Q16：复核发现 `E` 是 `AD` 中点，故 `CE=(3u+v)/4`。已将先前错误的 `(2u+v)/4` 和相应证明修正；①仍成立，②不成立，答案 B。
- Q19：独立联立得 `x²=14400/47`、`y²=2975/47`，距离为 `sqrt(17375/47)` km，按题面取整 19,227 m，位置为北偏东 66°。复核把早先误判的西北象限改为第一象限；固定副本只写约 19 km，精度差异保留。

## 登记、provenance 与确定性生成

- `register-papers` dry-run 成功后以唯一事务登记 `gk-2021-spring-shanghai` / `phase1-b57`，manifest revision `5433→5434`，绑定固定 source。paper `blocked`，问题总账新增 `ISSUE-1251/1252`。
- `provenance.py import-batch` 通过只读预检并以单一 state transaction 导入 21 题记录，revision `5434→5435`。逐题答案哈希、题面哈希、来源页、角色和 issue 关联现场校验；Q9 为 U，Q12 `conflict_status=unresolved`。本阶段把主会话复核身份如实写入，不标成异人审阅。
- `solution_sources.py extract-batch --write` 规范化解析正文并生成 `_含解析.md`；`generate_projects.py --write` 同步 `questions.tex`、`answers.tex`、`index.json`；随后生成 `answers_short.tex` 与四个版式入口壳。Q17 图在题面源与合并稿中各引用一次，对应 `questions.tex` / `answers.tex`；简答速查内容不重复插图。
- 通过：`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`、`provenance.py check-batch`，以及 `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`。全量报告投影已用单一 content transaction 刷新并回读；`manifest.csv` 已重生成 775 行。未运行测试套件，未进行正式 XeLaTeX 构建或 PDF 页面视觉验收。

## 下一阶段

完成 report/CSV 投影只读核对后，正式构建四版并逐页检查改动页，创建与 manifest revision、输入哈希、工具链、PDF SHA 和页数绑定的 build/review 回执。Q9、Q12 继续阻断 paper 完成；来源发布身份和官方答案均不作推断。

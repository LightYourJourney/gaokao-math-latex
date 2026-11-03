# 2000 上海文科候选卷：规范事实层、登记与确定性装配

- 日期：2026-11-03；工作树 `仓库根`，分支 `feat/gaokao-phase0`。
- 固定题面 source `src-8d14b1f9f511665ea10dbda45959a3b445a17806415be6b034f816bec663d7f5`，PDF SHA-256 `35e5d6f6bf052fcd9a2b91a1aa4215766fd4121425cfec7a62cfc4cdc7ab02a1`，来源路径 `普通高考/2000/2000上海文.pdf`。来源固定字节与本库 paper 的绑定只作内部 canonical 输入；发布者、出版物、版次、复制链及官方身份未核。固定 PDF 无答案页，`official_answer=null`。
- 本阶段重验本地 OCR 部署：`deploy_local_ocr.py --verify-only` 与 `local_ocr.py doctor` 均通过。Xiaomi、Paddle、MinerU 安装均为 verified，模型树 SHA-256 分别为 `a56facd25f7bfcc85db843f7dfca353ff3f0c4095974b7638f9ea23f97058210`、`8060c2c8c26bfdb9e84105951390c5792bdf2208b70749479d3bb9fd30ff6c5e`、`9c8592fda806b08b4789d83cf3d92bcba06bef5057fc71e29e91c9b7ee3630aa`。本阶段没有调用 OCR 推理；沿用已完成的原页逐题核对及盲核证据。

## 规范事实层

- 新增规范 `_试题.md`、`_答案要点.md`、`_解析正文.md`，覆盖 Q1–Q22。三份源层题号一致；Q19/Q20/Q21/Q22 小问分别为 1–2、1–2、1–3、1–3。`solution_sources` 识别 22 道题，答案、题面与解析的小问集合对齐。
- 题面沿用 22/22 最终独立核对稿；答案层将独立推导结论规范成解析器可读答案块，并补入单选速查表 C/A/A/D。解析层沿用已通过逐题独立盲审的 Q1–Q22 内容；小问标题只做结构规范化，未改数学推导。
- Q21 固定页仍照录 `y=2000(a/10)^2`。本地字面条件结论与同期答案副本按指数 `x` 的推导仍冲突，故答案三小问保持 `U/PENDING`，不推测修订原题、不认证副本为官方或同版。问题记入 `ISSUE-1363`，类型 `answer-conflict`，状态 `open` / `blocks_completion`。
- 源层 SHA-256：试题 `fdcf2d36670336fb522954c0c728ba9993270ee721dc4e06cf5c6955e7cf32a1`；答案要点 `f34399bac01e6e99d94f015bd55fd6f4d1df384b3bc1cdbc4a82c65b52906714`；解析正文 `1f57bb614ef38c2eaa4091505a43bbc336fddad8859b8159eae3d172fc1992c8`；确定性含解析 `358ec237bb25f983cdb5d2b6a202362d3ee37823981392ebaaffc12aa6435f76`。

## 登记与生成

- `register-papers` 以单一 state transaction 登记 `gk-2000-regular-shanghai-arts` / `phase3-b25`，manifest revision `6066→6067`，并将固定来源反向绑定到该 paper。paper 为 `blocked`、`blocked_from=planned`；batch 仍为 `planned`。这是本库内部输入绑定，不表示来源认证。
- 已生成全局 `index.json`、本卷 `questions.tex` / `answers.tex`、`answers_short.tex` 及试题版、解析版、简答版、印刷版四个入口壳。含解析正文由确定性生成器维护。
- 定向检查通过：`solution_sources.py check-batch`（22题）；`generate_projects.py --check`；`make_short_answers.py --check`；`make_editions.py --check`；`source_manifest.py validate`；`issues.py validate`。检查范围仅本卷及对应状态文件；未运行单元测试或正式 PDF 构建。

## 尚未完成

- Q8、Q11、Q18、Q20 的 TikZ 图稿尚未建立；题面目前仍保留图位说明。接下来需按固定 PDF 重绘，并在同一图稿阶段同步题面 Markdown 映射、确定性含解析稿、manifest `figure_files` 与 provenance。
- 三角色 provenance 尚待图稿与题面事实层冻结后导入；四版正式 PDF 构建、逐页视觉审查、build/review receipts、报告/CSV 投影与最终批次结论均未完成。
- 来源发布身份、版次、复制链及官方答案未核；`ISSUE-1363` 保持阻断。成本/人工时长未知。本阶段不表示该卷验收或长期语料库完成。

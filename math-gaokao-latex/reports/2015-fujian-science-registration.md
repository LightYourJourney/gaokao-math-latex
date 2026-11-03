# 2015 福建理科候选卷：固定来源与规范事实层登记

- 日期：2026-11-03；工作树 仓库根，分支 feat/gaokao-phase0。
- 固定来源 source src-c47985c709ff8ae42e6e192879d604223c58a53c4358056d28f78ad5a9736e3c，PDF SHA-256 a33455d27abdf2c4b344a5b90395bd71269f6fbefdef350375aba074e47ef700，Git blob 421cface308a5e99649ed8c316ae0b82322e0a9c；与 manifest 固定资产一致。

## 登记事务

- register-papers dry-run 通过后，将 paper gk-2015-regular-fujian-science 与单卷 batch phase3-b26 写入 source-manifest.json，revision 6074→6075，transaction_id 5a11cade-a7ba-4b00-828b-00bbdf2dd670。source 保持 source_state=ready，内部绑定关系为 canonical；这一关系只表示本库采用的固定字节，不认证发布者、出版者、版次、复制链或官方身份。
- 题量 23：选择题 Q1–Q10、填空题 Q11–Q15、解答题 Q16–Q23；题面来源 PDF 页码为 [1,2]，答案页为空。paper 与 batch 均为 planned，ISSUE 数为 0。
- 新建规范事实层：试题、答案要点、解析正文。解析正文规范稿对 Q16 增加与题面一致的两个小问标题，以符合解析器结构要求；数学正文与已盲核稿一致。由 solution_sources.py extract-batch 确定性生成含解析稿，再由 generate_projects.py 生成 questions.tex、answers.tex 与 index.json。

## 文件与当前状态

- 试题 SHA-256 a055165fc84d91a6e8fb80184d294dcc0f083f9dc0f01dd3b49bd409fbfbcb8c。
- 答案要点 SHA-256 365f5199d65429db438d86d606804d6cbcf8edee75b16ba43bdbba4b1aa4157a。
- 解析正文 SHA-256 a2218288af157d757018667a3fec92959548d6024e7bea2ffba533fa67d6ae29。
- 含解析 SHA-256 e2151d21992778551b4f6d0ae78c5c9a0a75aad670c59a9e33b2ecd95ddcaeb1。
- manifest.csv 经 manifest_csv.py --write 更新为 775 行。

## 检查与阶段边界

- 通过：source_manifest.py validate；issues.py validate；solution_sources.py check-batch（23 题）；generate_projects.py --check。
- 本阶段没有登记 provenance、ISSUE 或图稿；题图仍为纯文字待重绘标记。没有生成简答版或四版入口，没有正式 XeLaTeX 构建、回执或逐页视觉检查；未运行测试套件或 OCR。
- official_answer=null。下一阶段绘制并目视核对 Q6、Q13、Q17、Q18 四幅矢量图，随后同步 Markdown 图链、manifest figure_files、生成产物与逐题 provenance。本报告不表示来源认证、单卷验收或长期语料完成。

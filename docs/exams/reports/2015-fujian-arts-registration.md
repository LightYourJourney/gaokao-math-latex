# 2015 福建文科候选卷：paper/source 登记与基础生成

日期：2026-11-03

## 登记结果

- 固定来源 `src-1a7c18ef934f5ef3b6afbb819418e905cbfa4bf8a6b9d7a784c676fd3ad7132f`，PDF SHA-256 `4ca0fbac9967c9a73bdb0bc00eceb3d0181c57285ee72fc260a02c9c24172383`，Git blob `b91e92a997699d6fdb3cb9785f11222badf9b1e2`；上游固定 commit `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。来源题签为 2015 福建卷文科，PDF 2 页 A3 横向、印刷页 945–946、不含答案页。
- `source_manifest.py register-papers` dry-run 校验通过后，事务 `49e1da0e-44eb-4046-8269-a2a87d8d631c` 将 `gk-2015-regular-fujian-arts` 与 batch `phase3-b24` 写入 manifest，revision `6060→6061`。固定来源由未绑定改为本库内部 `canonical` 关系；这只标识本库采用的固定字节，不认证发布者、出版者、版次、复制链或官方身份。
- 题量 22：选择题 1–12、填空题 13–16、解答题 17–22；题面映射 PDF `[1,2]`，来源答案页为空。当前 paper 与 batch 均为 `planned`，没有逐题 blocker；`official_answer=null`，答案和解析继续为项目独立推导、非官方。
- `sync-figure-registry` dry-run 检出 5 幅 TikZ 图；事务将 5 项登记入 `figure_files`，每项预期在题面及合成稿出现 2 次，manifest revision `6061→6062`。Q18 频数表是题面 Markdown 表，不计为 TikZ 图。图稿仍待正式项目版面验收。

## 规范源同步与生成

- 题面、答案要点、解析正文 frontmatter 已绑定新 `paper_id`；来源校对 JSON 同步 `paper_id` 与题面 SHA。`solution_sources.py extract-batch --batch phase3-b24 --write` 重建确定性 `_含解析.md`。
- 首次 `generate_projects --write` 发现 Q21 公式的 `\]。` 结束行不符合转换器要求的独立闭合行。原固定 PDF 该公式本来就在句内；将规范题面改为行内数学符号，表达式、题目文字及答案均不变，之后重新生成成功。
- `generate_projects.py --batch phase3-b24 --write` 写入 3 个目标：`questions.tex`、`answers.tex` 和共享 `index.json`。登记后必须先刷新共享索引；索引未更新时历史批次会被算作 artifacts stale。生成后 `phase1-b83` 和 `phase3-b23` 的 `review_receipts.py check-batch` 均恢复为 `FINALIZED`，确认历史回执仍 current。
- 以下检查通过：`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22 题）、`generate_projects.py --check`、`manifest_csv.py --check`（775 行）。

## 阶段边界

本阶段未调用 OCR（`ocr_calls=0`、`model_calls=0`），未运行测试套件；没有登记逐题 provenance/issues，没有生成简答版与四版入口，未进行正式 XeLaTeX 构建或逐页视觉检查，也未产生 build/review 回执。来源真实性与 `official_answer` 仍未核/为空。下一阶段导入 22 题三角色 provenance，并推进简答、四版入口、构建和页面复核；本阶段不表示来源认证、单卷闭环或长期语料完成。

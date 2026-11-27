# 2009 春季上海卷：固定题源内部登记与 Q16 阻断

日期：2026-10-28

## 来源与登记

固定输入为 source `src-306adbf685e57e000a68f29eb9e85f4c3e0846f2c5b1f2b9e28d23d3635b629f`，SHA-256 `7012664a55336f327de730b2d7709256ca07e6c373110efa1a4d79ecedb64de2`，Git blob `5928da1aeae41277da97b7b7d08ed3649705e6f4`，9页、707,794字节。PDF 第1–4页是题面；第5–9页为该固定副本自称“参考答案及评分标准”的内容。

本阶段依据已固定的文件指纹，将该 PDF 绑定为本库内部 `canonical` 输入，仅表示本库工作流选用的字节；没有认证发布者、出版物、版次、扫描来源链或官方身份。卷内答案页同样未认证，`official_answer=null`；答案与解析仍标为非官方。

`source_manifest.py register-papers` dry-run 通过。单一状态事务登记 `gk-2009-spring-shanghai` / `phase1-b53`，manifest revision `5302 → 5303`，事务 ID `10aca2eb-4803-41c1-af75-f436ad35f09d`。题量20，题面页 `[1,4]`，副本所载答案/解析页 `[5,9]`；结构为填空1–11、选择12–15、解答16–20。paper 因开放问题处于 `blocked`（`blocked_from=planned`），batch 为 `planned`。

## Q16 阻断

事务新增 `ISSUE-1239`（`answer-conflict`，open / `blocks_completion`）。固定 PDF 第3页在 `∠A₁AC =` 后未见数值；第5–6页印载解答假设 `△AA₁C` 为直角三角形并据此得体积48。两组满足其余可见条件的构造给出不同体积，因此现存题面不能唯一决定答案。题面缺项照录，答案记为 U；恢复动作要求取得可追溯的同版清晰页或可靠正式勘误，再重新求解并盲核。

## 内容同步与验证

- 将五幅 TikZ 图从 `2009/figures/` 迁入 `2009_春季上海卷/figures/`；Git 检查为内容不变的重命名。题面和图表清单映射到项目目录；manifest 对每图登记预期引用2次。
- 题面、答案要点和解析正文关联 `paper_id: gk-2009-spring-shanghai`；来源说明区分内部固定输入与来源认证。答案保持 `official_answer: null`。
- 为 `solution_sources` 补齐分题答案锚点、解析小问锚点及题面小问分隔空格；这些修改用于满足确定性解析器契约，不改变题目或数学结论。含解析稿由唯一生成器生成。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --batch phase1-b53`、`report.py check --all`、`manifest_csv.py --check` 与 `git diff --check` 均通过；本卷解析检查为20题对齐，manifest CSV 为775行且当前。全量报告检查确认输出与 manifest 当前一致，并在报告中保留尚未完成状态。

## 阶段边界

本阶段只完成来源内部绑定、Q16 blocker 登记、图稿归档与确定性 Markdown 同步。尚未导入逐题 provenance，尚未生成共享 TeX、简答稿和四个编译入口，尚未正式构建 PDF 或逐页视觉审查，因此没有本卷 build/review receipts。未运行测试套件。下一阶段按现存题面、盲解和复核证据导入逐题 provenance，再生成共享内容及四版入口；Q16 继续阻断整卷完成。该阶段状态不代表1952—2026语料库完成。

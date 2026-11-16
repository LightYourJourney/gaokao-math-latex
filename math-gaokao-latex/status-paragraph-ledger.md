# 状态段（needs-review）清理台账

- 更新：2026-11-16；扫描 `*/*_试题.md`，仍含「状态：needs-review」首段的 **1 卷**：**0 卷为 complete**，1 卷为 blocked（随其终局结论一并处理）。基线 37 卷，已清理 **36 卷**。
- 已清理 36 卷（2008 天津文/理、上海文/理、安徽文/理、北京理、山东文/理；2007 上海理、浙江文/理、陕西文/理、福建文/理、辽宁文/理、山东文/理、江苏、广东文/理、天津文/理、重庆文/理、安徽文/理、湖南理、江西文/理、湖北文/理、新课标文/理），均重封账。
- 该段**印在 PDF 里**，必须「删段 → 重生成三件套 → 重建 → 逐页重审 → 重封账」；只改 Markdown 会让三套生成器 `--all --check` 立即不一致。

## 五步规程（每卷一轮）

1. 删 `_试题.md` 标题下「状态：needs-review；…」整段（其余题面一字不动）；
2. `solution_sources.py extract-batch --batch <batch> --write` 重生成 `_解析正文.md`、`_含解析.md`；
3. 若第 2 步改动过 `_解析正文.md`，先跑该批次 `gen_prov.py` + `provenance import-batch`（否则 `build --formal` 报 stale）；
4. `generate_projects.py` / `make_short_answers.py` / `make_editions.py` 加 `--batch <batch> --write`；
5. `build_projects.py build --formal --batch <batch>`，确认四版 log 全为 0；出现 Overfull/Underfull 先改解析正文/题面分段再重建；
6. `review_receipts.py prepare-batch` → 逐页审查（图页 350dpi）→ `finalize-batch` → 全量门禁 → 限定路径提交。

**已知坑**：① `prepare-batch` 必须在重建之后，否则 `finalize-batch` 报 `INVALID_OR_STALE`；② 长串拉丁字符/数字（如「×××××××0000」）或整段短数学原子（坐标列表）会造成 Underfull，应在自然句读处拆句/分段（题面不改字，解析可改措辞）；③ 改 md 后 `provenance` 转 stale，须按第 3 步处理；④ 重建后若曾 `prepare-batch`，须重跑一次再填表；⑤ 图稿也要按 300~350dpi 回源核对（已发现椭圆圆心偏位、标注压边两类缺陷）；⑥ 不可断的行内公式（如区间 `(-0.03,0.03)`）可在逗号处加 `\allowbreak` 消除 Underfull，比「句中分段」安全（后者会挤出孤页）。

## 一、待清理队列（complete 卷）

**空。**37 卷状态段清理队列中的 complete 卷已全部重封账。


## 二、随 blocked 卷终局处理（1 卷，不列入本轮清理队列）

这些卷 `production_state = blocked`，题面存疑点（重复选项、答案与印面冲突等）须由外部证据裁定；其状态段在其终局结论确定时一并处理，见 `blocked-ledger.md`。

| 年份 | 卷 | paper_id | 项目目录 | 立项理由 |
| --- | --- | --- | --- | --- |
| 2007 | 四川理 | `gk-2007-regular-sichuan-science` | `2007_四川卷_理科` | ISSUE-1449, ISSUE-1450, ISSUE-1451 |

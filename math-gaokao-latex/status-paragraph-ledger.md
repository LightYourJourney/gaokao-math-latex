# 状态段（needs-review）清理台账

- 更新：2026-11-16（本轮再清 2007 辽宁文、辽宁理）；扫描 `*/*_试题.md`，仍含「状态：needs-review」首段的 **23 卷**。
- 已清理 **14 卷**：2008 天津文/理、上海文/理、安徽文/理（`phase6-b15`/`b16`/`b17`），2008 北京理（`phase6-b04`）、2007 上海理（`phase5-b01`）、浙江文（`b16`）、陕西文（`b19`）、陕西理（`b20`）、福建理（`b26`）、辽宁文（`b21`）、辽宁理（`b22`），均重封账。
- 该段**印在 PDF 里**（例如 `2007_安徽卷_理科/build/试题版.pdf` 第 1 页可 grep 到），所以必须「删段 → 重生成三件套 → 重建 → 逐页重审 → 重封账」；只改 Markdown 会让三套生成器 `--all --check` 立即不一致。

## 五步规程（每卷一轮）

1. 删 `_试题.md` 标题下「状态：needs-review；…」整段（其余题面一字不动）；
2. `solution_sources.py extract-batch --batch <batch> --write` 重生成 `_解析正文.md`、`_含解析.md`；
3. `generate_projects.py` / `make_short_answers.py` / `make_editions.py` 加 `--batch <batch> --write`；
4. `build_projects.py build --formal --batch <batch>`，确认四版 log 的 errors/overfull/underfull/missing characters 全为 0；
5. `review_receipts.py prepare-batch` → 逐页审查（图页 350dpi）→ `finalize-batch` → 全量门禁 → 限定路径提交。

**顺序要点**：`prepare-batch` 必须放在重建之后；否则工作项与 build 不匹配，`finalize-batch` 会报 `INVALID_OR_STALE`（须重跑 `prepare-batch` 再填表）。

## 待清理清单（按四版总页数升序，便于排期）

| 年份 | 卷 | paper_id | 项目目录 | 试题/解析/简答/印刷 | 合计 |
| --- | --- | --- | --- | --- | --- |
| 2007 | 浙江理 | `gk-2007-zhejiang-science` | `2007_浙江卷_理科` | 6/22/8/17 | 53 |
| 2007 | 山东文 | `gk-2007-regular-shandong-arts` | `2007_山东卷_文科` | 5/24/7/18 | 54 |
| 2007 | 江苏 | `gk-2007-jiangsu` | `2007_江苏卷` | 4/25/6/19 | 54 |
| 2007 | 重庆理 | `gk-2007-chongqing-science` | `2007_重庆卷_理科` | 5/23/7/19 | 54 |
| 2007 | 安徽文 | `gk-2007-regular-anhui-arts` | `2007_安徽卷_文科` | 5/25/7/18 | 55 |
| 2007 | 湖南理 | `gk-2007-hunan-science` | `2007_湖南卷_理科` | 5/24/7/19 | 55 |
| 2007 | 福建文 | `gk-2007-fujian-arts` | `2007_福建卷_文科` | 6/22/8/19 | 55 |
| 2007 | 重庆文 | `gk-2007-chongqing-arts` | `2007_重庆卷_文科` | 5/25/7/18 | 55 |
| 2007 | 天津理 | `gk-2007-regular-tianjin-science` | `2007_天津卷_理科` | 5/25/7/19 | 56 |
| 2007 | 江西理 | `gk-2007-jiangxi-science` | `2007_江西卷_理科` | 6/24/8/19 | 57 |
| 2007 | 湖北理 | `gk-2007-hubei-science` | `2007_湖北卷_理科` | 5/25/7/20 | 57 |
| 2007 | 天津文 | `gk-2007-regular-tianjin-arts` | `2007_天津卷_文科` | 5/26/7/20 | 58 |
| 2008 | 山东文 | `gk-2008-shandong-arts` | `2008_山东卷_文科` | 6/25/8/19 | 58 |
| 2007 | 湖北文 | `gk-2007-hubei-arts` | `2007_湖北卷_文科` | 6/24/8/21 | 59 |
| 2007 | 江西文 | `gk-2007-jiangxi-arts` | `2007_江西卷_文科` | 6/27/8/20 | 61 |
| 2007 | 安徽理 | `gk-2007-regular-anhui-science` | `2007_安徽卷_理科` | 6/27/8/21 | 62 |
| 2008 | 山东理 | `gk-2008-shandong-science` | `2008_山东卷_理科` | 6/25/8/23 | 62 |
| 2007 | 广东文 | `gk-2007-regular-guangdong-arts` | `2007_广东卷_文科` | 7/26/9/23 | 65 |
| 2007 | 四川理 | `gk-2007-regular-sichuan-science` | `2007_四川卷_理科` | 7/30/9/22 | 68 |
| 2007 | 山东理 | `gk-2007-regular-shandong-science` | `2007_山东卷_理科` | 6/32/8/26 | 72 |
| 2007 | 广东理 | `gk-2007-regular-guangdong-science` | `2007_广东卷_理科` | 7/33/9/25 | 74 |
| 2007 | 新课标文 | `gk-2007-newcurriculum-arts` | `2007_新课标卷_文科` | 7/32/9/27 | 75 |
| 2007 | 新课标理 | `gk-2007-newcurriculum-science` | `2007_新课标卷_理科` | 7/35/9/28 | 79 |

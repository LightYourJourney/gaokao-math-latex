# 状态段（needs-review）清理台账

- 盘点：2026-11-16 扫描 `*/*_试题.md`，仍含「状态：needs-review」首段 **31 个文件**。
- 已清理 6 卷（2008 天津文理、上海文理、安徽文理，见 `phase6-b15/b16/b17`）。
- 该段**印在 PDF 里**（如 `2007_安徽卷_理科/build/试题版.pdf` 第 1 页），故必须「删段 → 重生成三件套 → 重建 → 重审 → 重封账」，只改 Markdown 会使三套生成器 `--all --check` 立即不一致。

## 清理规程

1. 删 `_试题.md` 标题下「状态：needs-review；…」整段，其余题面不动；
2. `solution_sources.build_paper_targets` 重生成 `_解析正文.md`、`_含解析.md`；
3. `generate_projects.py` / `make_short_answers.py` / `make_editions.py` 加 `--batch <batch> --write`；
4. `build_projects.py build --formal --batch <batch>`，四版 log 归零；
5. `prepare-batch` → 逐页审查（图页 350dpi）→ `finalize-batch` → 全量门禁 → 限定路径提交。

## 待清理清单（含当前四版页数，供排期）

| 年份 | 卷 | paper_id | 状态 | 项目目录 | 试题/解析/简答/印刷 |
| --- | --- | --- | --- | --- | --- |
| 2007 | 上海理 | `gk-2007-regular-shanghai-science` | complete | `2007_上海卷_理科` | 4/15/6/13 |
| 2007 | 四川理 | `gk-2007-regular-sichuan-science` | blocked | `2007_四川卷_理科` | 7/30/9/22 |
| 2007 | 天津文 | `gk-2007-regular-tianjin-arts` | complete | `2007_天津卷_文科` | 5/26/7/20 |
| 2007 | 天津理 | `gk-2007-regular-tianjin-science` | complete | `2007_天津卷_理科` | 5/25/7/19 |
| 2007 | 安徽文 | `gk-2007-regular-anhui-arts` | complete | `2007_安徽卷_文科` | 5/25/7/18 |
| 2007 | 安徽理 | `gk-2007-regular-anhui-science` | complete | `2007_安徽卷_理科` | 6/27/8/21 |
| 2007 | 山东文 | `gk-2007-regular-shandong-arts` | complete | `2007_山东卷_文科` | 5/24/7/18 |
| 2007 | 山东理 | `gk-2007-regular-shandong-science` | complete | `2007_山东卷_理科` | 6/32/8/26 |
| 2007 | 广东文 | `gk-2007-regular-guangdong-arts` | complete | `2007_广东卷_文科` | 7/26/9/23 |
| 2007 | 广东理 | `gk-2007-regular-guangdong-science` | complete | `2007_广东卷_理科` | 7/33/9/25 |
| 2007 | 新课标文 | `gk-2007-newcurriculum-arts` | complete | `2007_新课标卷_文科` | 7/32/9/27 |
| 2007 | 新课标理 | `gk-2007-newcurriculum-science` | complete | `2007_新课标卷_理科` | 7/35/9/28 |
| 2007 | 江苏 | `gk-2007-jiangsu` | complete | `2007_江苏卷` | 4/25/6/19 |
| 2007 | 江西文 | `gk-2007-jiangxi-arts` | complete | `2007_江西卷_文科` | 6/27/8/20 |
| 2007 | 江西理 | `gk-2007-jiangxi-science` | complete | `2007_江西卷_理科` | 6/24/8/19 |
| 2007 | 浙江文 | `gk-2007-zhejiang-arts` | complete | `2007_浙江卷_文科` | 4/20/6/16 |
| 2007 | 浙江理 | `gk-2007-zhejiang-science` | complete | `2007_浙江卷_理科` | 6/22/8/17 |
| 2007 | 湖北文 | `gk-2007-hubei-arts` | complete | `2007_湖北卷_文科` | 6/24/8/21 |
| 2007 | 湖北理 | `gk-2007-hubei-science` | complete | `2007_湖北卷_理科` | 5/25/7/20 |
| 2007 | 湖南理 | `gk-2007-hunan-science` | complete | `2007_湖南卷_理科` | 5/24/7/19 |
| 2007 | 福建文 | `gk-2007-fujian-arts` | complete | `2007_福建卷_文科` | 6/22/8/19 |
| 2007 | 福建理 | `gk-2007-fujian-science` | complete | `2007_福建卷_理科` | 5/22/7/17 |
| 2007 | 辽宁文 | `gk-2007-liaoning-arts` | complete | `2007_辽宁卷_文科` | 5/21/7/18 |
| 2007 | 辽宁理 | `gk-2007-liaoning-science` | complete | `2007_辽宁卷_理科` | 5/22/7/17 |
| 2007 | 重庆文 | `gk-2007-chongqing-arts` | complete | `2007_重庆卷_文科` | 5/25/7/18 |
| 2007 | 重庆理 | `gk-2007-chongqing-science` | complete | `2007_重庆卷_理科` | 5/23/7/19 |
| 2007 | 陕西文 | `gk-2007-shaanxi-arts` | complete | `2007_陕西卷_文科` | 5/20/7/16 |
| 2007 | 陕西理 | `gk-2007-shaanxi-science` | complete | `2007_陕西卷_理科` | 5/20/7/17 |
| 2008 | 北京理 | `gk-2008-beijing-science` | complete | `2008_北京卷_理科` | 5/20/7/15 |
| 2008 | 山东文 | `gk-2008-shandong-arts` | complete | `2008_山东卷_文科` | 6/25/8/19 |
| 2008 | 山东理 | `gk-2008-shandong-science` | complete | `2008_山东卷_理科` | 6/25/8/23 |

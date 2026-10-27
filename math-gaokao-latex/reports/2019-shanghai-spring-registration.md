# 2019 上海春季卷：paper/source 与待核项登记

日期：2026-10-28

## 登记

- 通过唯一事务 `source_manifest.py register-papers` 将 `gk-2019-spring-shanghai` 登记到 `phase1-b47`；manifest revision `5248 → 5249`。项目目录 `2019_上海春季卷`，题量 20，`track=none`；题面映射固定 PDF 第 1–3 页，卷内附答案/解析第 4–15 页。
- 固定 source `src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631` 的 PDF SHA-256 `432bfb1bfc16c7a915f1349432d1dbcfc151b859ad89e9e3a3f554c5fb768e1d`、Git blob `2eb483bb17e1267fe30f99a85af7321441c92cf8`、15 页与清单一致。内部 `canonical` 绑定只表示本库选用该固定副本；出版者、版次、来源链及官方身份仍未核，卷内答案不标为官方，`official_answer=null`。
- Q10、Q17 两幅 TikZ 图登记到 `figure_files`，各自期望在题面和含解析稿出现 2 次；图稿 SHA 分别为 `5374b17383c77b12cdd3ba5a60f88d27cfd773bd15b63cd354e260f33c4148b3` 与 `dc729cd4d7612810377c6e8b30b17e35647e19cf77e97eb8a1939ce98ad73995`。

## 开放阻断项

- `ISSUE-1220`（Q9）：是否要求五天每日有人参加未明；24/500 两种计数条件均保留。
- `ISSUE-1221`（Q11）：`F_1,F_2` 未显式定义；答案只在按椭圆焦点解释时成立。
- `ISSUE-1222`（Q16）：源附答案选 A 并称整条直线，严格轨迹另须满足坐标范围，当前选项无精确匹配。
- `ISSUE-1223`（Q18）：等比数列定义对零公比的约定未明，`q=0` 条件分支保留。
- `ISSUE-1224`（Q19(3)）：题面未说明三点互异，该条件会改变严格结论。
- `ISSUE-1225`（Q19）：源解析“点睛”把中线不等式方向写反，与严格三角形不等式冲突。

六项均为 `open / blocks_completion`。纸卷 `production_state=blocked`、`blocked_from=planned`，批次目前为 `planned`。

## 验证与后续

- 注册规格 dry-run 与写入均通过；`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --batch phase1-b47`、`manifest_csv.py --check` 通过；CSV 为 775 行。`report.py render --all` 与 `report.py check --all` 均确认六个全量报告投影当前。
- 本阶段未运行测试套件；尚未导入逐题 provenance、生成共享 TeX/四版入口、正式构建或进行整卷视觉审查。下一步按当前题面/答案/解析和六条阻断导入 provenance，生成共享内容与四版，再正式构建和逐页复核。

## 稳定题号补正

- 导入 provenance 前对照 `provenance.question_id()` 发现 `ISSUE-1220` 使用 `gk-2019-spring-shanghai-q9`，应为规范内部题序 `gk-2019-spring-shanghai-q09`。保留 issue 编号 `ISSUE-1220`，重算 fingerprint，并用状态事务同步 manifest；最终 revision 为 `5251`。
- 补正仅统一稳定标识，不改变题面、答案分支或待核判断；问题总账仍为 1225 条，纸卷仍 `blocked`、批次仍 `planned`。

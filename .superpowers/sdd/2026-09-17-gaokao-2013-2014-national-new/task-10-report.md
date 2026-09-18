# Task 10 总装配执行报告（closed_with_blockers；视觉与形式 gates PASS，内容仍阻塞）

工作树：`仓库根`；分支 `feat/gaokao-phase0`；计划起始 HEAD `e7b8290901eecda05b5696616dacad037cadb94b`，本次恢复前工具修复后的 HEAD `1c8fb53933d3b68a72cf4da24c47b39a14b83a38`，视觉回执 checkpoint `a69e60fa`。未改主工作区工作文件；未派生 subagent/reviewer；未 push；未改公共 tools。采用 executing-plans、隔离工作树、PDF 和 verification-before-completion 技能；以实际 gate 证据为准，不以编译退出 0 代替最终视觉验收。

## 当前结论

成功登记固定八卷，生成八组 combined/shared TeX/四版本壳与 provenance；正式 XeLaTeX 构建输出 32 个当前 PDF。工具上限修复提交 `1c8fb539` 后，`prepare-batch` 实际生成 32 个工作项；最终在仓库外重新渲染并逐页检查 441 页，32 个 work item 的 8 项检查全部签署，1 条 Underfull 做了页级豁免。`finalize-batch-checked` 与 `check-batch` 均退出 0，正式 review 全部 `passed`，build 8/8 `succeeded`；批次结论按真实内容问题为 `closed_with_blockers`，不是 PASS。

用户 ruling：首次注册 `--write` 在 spec figure 路径 schema 校验时、事务写入前退出 1；manifest 未变，没有副作用。按用户裁定它是失败演练，不计成功注册。修正 spec dry-run PASS 后立即执行一次成功 `--write`，退出 0、revision 2731。此前暂停说明仅是历史记录，不再代表当前权限状态。

## 实际命令与退出码

所有相对命令 cwd 为指定工作树。下表为实际调用记录，包括失败；“相同命令再次调用”并不隐去前次失败。

| 命令 | 退出码 | 摘要 |
| --- | ---: | --- |
| `python3 math-gaokao-latex/tools/source_manifest.py register-papers --repo . --manifest math-gaokao-latex/source-manifest.json --spec math-gaokao-latex/.work/phase2-b02/register.json --write` | 0 | phase2-b02：8 卷，已提交 revision 2731 |
| `python3 math-gaokao-latex/tools/solution_sources.py extract-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --write` | 0 | phase2-b02 的目标已是最新，未开启事务 |
| `python3 math-gaokao-latex/tools/solution_sources.py check-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02` | 0 | 8 套全部通过 |
| `python3 /private/tmp/task10_run.py generate --write` | 0 | ✓ 8 套试卷，已写入 17 个目标 |
| `python3 /private/tmp/task10_run.py generate --check` | 0 | ✓ 8 套试卷与生成结果一致 |
| `python3 math-gaokao-latex/tools/make_short_answers.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --write` | 0 | ✓ 8 套试卷，已写入 8 份简答 |
| `python3 math-gaokao-latex/tools/make_short_answers.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | ✓ 8 套试卷的简答与生成结果一致 |
| `python3 math-gaokao-latex/tools/make_editions.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --write` | 0 | ✓ 8 套试卷，已写入 32 个壳 |
| `python3 math-gaokao-latex/tools/make_editions.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | ✓ 8 套试卷的壳与模板渲染结果一致 |
| `python3 math-gaokao-latex/tools/provenance.py import-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --work-dir math-gaokao-latex/.work` | 0 | ✓ phase2-b02：8 卷，仅校验，未落盘 |
| `python3 math-gaokao-latex/tools/provenance.py import-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --work-dir math-gaokao-latex/.work --write` | 0 | ✓ phase2-b02：8 卷，已提交 revision 2732 |
| `python3 math-gaokao-latex/tools/provenance.py check-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02` | 0 | OK：8 卷 |
| `python3 math-gaokao-latex/tools/build_projects.py build --formal --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --json` | 5 | {"batches": {"phase2-b02": "provenance_verified"}, "code": "BUILD_FAILED", "failed": 1, "failed_papers": ["gk-2014-regular-national-2-science"], "papers": ["gk-2013-regular-national-1-arts", "gk-2013-regular-national-1-science", "gk-2013-regular-national-2-arts", "gk-2013-regular-national-2-science", "gk-2014-regular-national-1-arts", "gk-2014-regular-national-1-science", "gk-2014-regular-national-2-arts", "gk-2014-regular-national-2-science"], "pending": 7, "revision": 2734} |
| `python3 -m unittest discover -s math-gaokao-latex/tests` | 1 | FAILED (failures=1, errors=1, skipped=13) |
| `python3 math-gaokao-latex/tools/solution_sources.py extract-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --write` | 0 | 已提交 16 个目标：phase2-b02 |
| `python3 /private/tmp/task10_run.py generate --write` | 0 | ✓ 8 套试卷，已写入 17 个目标 |
| `python3 math-gaokao-latex/tools/provenance.py import-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --work-dir math-gaokao-latex/.work --write` | 0 | ✓ phase2-b02：8 卷，已提交 revision 2735 |
| `python3 math-gaokao-latex/tools/source_manifest.py validate --manifest math-gaokao-latex/source-manifest.json` | 0 |  |
| `python3 math-gaokao-latex/tools/solution_sources.py check-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02` | 0 | 8 套全部通过 |
| `python3 /private/tmp/task10_run.py generate --check` | 0 | ✓ 8 套试卷与生成结果一致 |
| `python3 math-gaokao-latex/tools/make_short_answers.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | ✓ 8 套试卷的简答与生成结果一致 |
| `python3 math-gaokao-latex/tools/make_editions.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | ✓ 8 套试卷的壳与模板渲染结果一致 |
| `python3 math-gaokao-latex/tools/provenance.py check-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02` | 0 | OK：8 卷 |
| `python3 math-gaokao-latex/tools/build_projects.py validate-receipts --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --require-current-inputs --json` | 0 | {"code": "OK", "failed": 0, "invalid": 0, "missing": 0, "papers": 8, "pending": 8, "problems": [], "running": 0, "stale": 0, "succeeded": 0} |
| `python3 math-gaokao-latex/tools/build_projects.py validate-receipts --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --require-final --require-current-inputs --json` | 3 | {"code": "PENDING_REVIEW", "failed": 0, "invalid": 0, "missing": 0, "papers": 8, "pending": 8, "problems": [], "running": 0, "stale": 0, "succeeded": 0} |
| `python3 math-gaokao-latex/tools/review_receipts.py check-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --json` | 6 | {"batch_id": "phase2-b02", "code": "INVALID_OR_STALE", "papers": ["gk-2013-regular-national-1-arts", "gk-2013-regular-national-1-science", "gk-2013-regular-national-2-arts", "gk-2013-regular-national-2-science", "gk-2014-regular-national-1-arts", "gk-2014-regular-national-1-science", "gk-2014-regular-national-2-arts", "gk-2014-regular-national-2-science"], "problems": ["gk-2013-regular-national-1-arts: 缺 review 回执", "gk-2013-regular-national-1-science: 缺 review 回执", "gk-2013-regular-national-2-a |
| `python3 math-gaokao-latex/tools/manifest_csv.py --manifest math-gaokao-latex/source-manifest.json --output math-gaokao-latex/manifest.csv --write` | 0 | manifest.csv：已写入，775 行 |
| `python3 math-gaokao-latex/tools/manifest_csv.py --manifest math-gaokao-latex/source-manifest.json --output math-gaokao-latex/manifest.csv --check` | 0 | manifest.csv 当前且 775 行 |
| `python3 math-gaokao-latex/tools/issues.py validate --file math-gaokao-latex/missing-issues.md` | 0 |  |
| `python3 math-gaokao-latex/tools/build_projects.py clean-build --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --dry-run` | 0 | 共 8 个目标，0 个已删除 |

补充实际调用：

| 命令 | 退出码 | 摘要 |
| --- | ---: | --- |
| `python3 /private/tmp/task10_run.py build-setup` | 0 | 首次外部目录 /private/tmp/task10-5xy2490j；八 build 临时 symlink 指向仓库外 |
| `python3 /private/tmp/task10_run.py source-render /private/tmp/task10-5xy2490j` | 0 | pdftoppm 150dpi，八固定 PDF 的 16 页全部实际查看 |
| `python3 /private/tmp/task10_run.py render /private/tmp/task10-5xy2490j`（首次） | 1 | magick montage 字体错误：unable to read font ''; 图像输出在外部 |
| 同上，显式 `-font /System/Library/Fonts/Supplemental/Arial.ttf` 后 | 0 | pdftoppm 130dpi；32 PDF、441 页、120 张四页拼图；不等于已完成人工视觉检查 |
| `python3 /private/tmp/task10_run.py conflicts` | 0 | 既有 issues.upsert_issue 接口登记 ISSUE-0879/0880，24 角色输入按问题身份挂接 |
| `provenance.py import-batch --manifest ... --issues ... --batch phase2-b02 --write`（实际漏写 work-dir） | 2 | argparse：缺少 --work-dir；未写入 |
| `python3 math-gaokao-latex/tools/provenance.py import-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --work-dir math-gaokao-latex/.work --write`（构建持锁期间） | 4 | Errno 35 仓库已有写事务 主工作树/.git/gaokao-latex.lock；停止重试，不删锁 |
| 同上，当前构建退出释放锁后 | 0 | revision 2740，新增冲突 provenance 生效 |
| `python3 math-gaokao-latex/tools/review_receipts.py prepare-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02` | 6 | 必须包含 1–4 套试卷，实际 8 套；未产生视觉工作回执 |
| `python3 /private/tmp/task10_run.py build-retain /private/tmp/task10-5xy2490j` | 0 | 八 symlink 转为普通目录，只复制 32 PDF |
| `python3 /private/tmp/task10_run.py cleanup /private/tmp/task10-5xy2490j` | 0 | 删除 737 个外部文件、25 个 .work 批次临时文件；两目录不存在 |
| `python3 math-gaokao-latex/tools/build_projects.py clean-build --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --execute` | 0 | 操作失误：既有工具删除整个八个 build 目录，32 PDF 被删除，并非只删除中间物 |
| `python3 /private/tmp/task10_run.py inventory`（误删后） | 1 | FileNotFoundError: build/试题版.pdf；随后重新构建恢复，不以旧清单冒充最终清单 |
| `python3 /private/tmp/task10_run.py build-setup`（恢复） | 0 | /private/tmp/task10-eysf9rcz，编译中间物再次只在仓库外 |
| `git diff --check` | 0 | 无 whitespace 错误 |
| `git diff e7b8290901eecda05b5696616dacad037cadb94b --name-only -- math-gaokao-latex/tools` | 0 | 无输出，公共 tools 未变 |

正式 build 全部使用实际命令：
`python3 math-gaokao-latex/tools/build_projects.py build --formal --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --json`。首次退出 5（2014 II science 下划线 missing $），第二轮退出 0 但仍有一个真实 Overfull，第三轮退出 0（revision 2739），恢复构建结果见下文。工具每 PDF 执行两轮 XeLaTeX。真实 Overfull 和缺字只在 canonical 源修复，不修改 tools：
2014 II science 空白下划线转 TeX 安全转义；2013 II science 展示公式中文句号用 text；2014 II arts 茎叶数据仅缩减间距；2014 I science /2013 II science 不可断行数字列表拆为独立数学片段；期望式用 aligned 分行。数学数值和题意未改。

`generate` 包装器只调用既有 `generate_projects.main([...], figure_map=...)`；映射来自每卷逻辑图形文件名与既有 project/figures 源的 stem。所有固定 PDF SHA 与 manifest 现场重算相符，44 figures，192 题均 1–24，结构 12/4/8。init-batch 实际退出 0 创建 24 角色文件；初始 import dry-run/write/check 均 0。前序 Task2–9 独立复审证据与报告 SHA 被引用，不声称本轮派生了 reviewer；答案 B 级独立复算，不是官方答案。2014 I science q18 明确为固定 PDF 第2页（印刷900），不能套其它卷映射。

## 视觉审查与 Underfull

最终视觉证据来自当前正式 build receipts 绑定的 32 个 PDF，而不是旧构建渲染：在仓库外目录 `/private/tmp/task10-final-nMP3Rk` 以 `pdftoppm -r 130 -png` 重新生成全部页面，再生成 120 张四页 contact sheet；实际逐张查看 120 张 contact sheet，覆盖 8 卷 × 4 版本 × 441 页。逐页填写 8 项 `glyph`、`heading_number`、`option_formula_alignment`、`figure_label`、`header_footer`、`pagination_whitespace`、`font_size`、`answer_leak`，32/32 work items、441/441 页均为 `pass`，未见裁切、缺字、图形/标签错位、页眉页脚冲突、分页碰撞或意外答案泄漏。

唯一构建警告为 `2014_全国Ⅱ卷_文科/解析版` 的 `Underfull \\hbox (badness 1577)`，`answers.tex` lines `516--517`。已在正式 work item 中写入页级豁免：`source_file=answers.tex`、`pdf_page=18`、`visual_result=pass`、`width_pt=null`；新渲染第 18 页复核确认段落及后续 display 均在版心内，无裁切或碰撞。其余版本无 Underfull/Overfull 豁免。

## 未解决 issues

24 条源作答规则缺失 blocking transcription-ambiguous（八卷各 q22–24），来自固定 PDF 第2页与四研究报告；保留24题但不猜必答或选答。
新增 ISSUE-0879：2013 I arts q21 单值答案只给2sqrt3，固定题面未限定公切线类型；与 science 同型题既有多分支解析不一致。
新增 ISSUE-0880：2013 I science q20 同一未限定切线类型问题。两题 conflict_status=unresolved 且身份一致 blocking answer-conflict。没有擅自选答案。
工具/计划冲突：视觉 prepare 接口 1–4 卷上限与固定八卷批次要求冲突，需另行明确修改接口的授权或更正计划；本轮无此授权，停止该流程。review/final build gate 失败不能掩盖。
首次完整 unit gate 实际 810 tests /257.031s，1 failure、1 error、13 skipped，退出1；运行与装配变动重叠，错误为历史 batch ownership 尚未提交和 cached state 不符。不能作为通过证据。

## checkpoint 与最终交付边界

`a088f59d0c1d86088bd6aade4019d6882f56476c`：八 combined。
`5837ec6352d05a07261eff370a6130328127d799`：首次阻塞报告。
`f7b088fa08ea52e89d7b46b6d3080aeef1b26a3d`：成功登记/生成/provenance checkpoint。该 checkpoint 意外暂存八个临时 build symlink；最终提交删除这些 tracked symlink，保留本地普通 PDF-only build 目录，不重写历史。
最终提交是 blocked build receipts/report 交付，不是成功视觉回执提交。无伪造 finalization 或 closed 状态。已有不相关 untracked research 和 plan 不纳入提交。

## 恢复构建与最终清理实测

同一完整 formal build 命令恢复轮退出 0，revision2742，8 pending、0failed；最终日志扫描 `rg -n 'Underfull|Overfull|Missing character|undefined' /private/tmp/task10-eysf9rcz -g '*.log'` 退出0，唯一匹配为上述 Underfull。0 missing characters、0undefined references、0 realOverfull。
`python3 /private/tmp/task10_run.py build-retain /private/tmp/task10-eysf9rcz` 退出0；随后 `python3 /private/tmp/task10_run.py cleanup /private/tmp/task10-eysf9rcz` 退出0，删除160个外部编译文件，两个外部目录及批次work均不存在。
`python3 /private/tmp/task10_run.py inventory` 恢复后退出0，逐个读取PDF重算SHA并断言匹配当前build receipt：{"pdf":32,"figures":44,"project_tex":56,"provenance":8,"build_receipts":8,"review_receipts":0,"raster":0}。八个build全部普通目录、每个恰好4PDF，无其它文件；canonical三源和combined共32文件保留，100个项目/figure TeX保留。临时symlink最终不保留。PDF可从保留源重建，误删已恢复；被删除的外部渲染和中间物可重新生成，未删除固定源、Markdown/LaTeX、provenance、receipts或report。

## 最终 32 PDF 页数与 SHA256（共441页）

| paper_id | 版本 | 页数 | SHA256 |
| --- | --- | ---: | --- |
| gk-2013-regular-national-1-arts | 试题版 | 6 | `379abb279fb5c7d135f5fd11051faafa6f0a40eaa5b51097f8d2c55c0303254c` |
| gk-2013-regular-national-1-arts | 解析版 | 23 | `9593efd0c33336d2b72011c2be3a674afd2a806044d802a8ea04adadc85785a0` |
| gk-2013-regular-national-1-arts | 简答版 | 8 | `ff65018bb967faa5ae24a1223e5b67c58b6ad3c3b8692c2c4fa0c5751591e86c` |
| gk-2013-regular-national-1-arts | 印刷版 | 17 | `429678af3ff0bb4eca0bfc0ce8fd6f534184dcc4a20eb6f1a03836cf265f7850` |
| gk-2013-regular-national-1-science | 试题版 | 6 | `f1f19dcd2a6b1b188a372458ed3cae7b19bbc4e1c12b0cbc7fd9ecaa3e23891d` |
| gk-2013-regular-national-1-science | 解析版 | 24 | `c7aa8ef41bf567a9a8dbcaa8a8ad784981b544eac9c2d2008c474f80d350c44e` |
| gk-2013-regular-national-1-science | 简答版 | 8 | `6d6ecc4fdd201bc6abba1f033be1f3eb3a521988912079670b597fba68049cf5` |
| gk-2013-regular-national-1-science | 印刷版 | 19 | `8c93142962cba50d26ceda7837b8c6394411119af4181465d677d3199f54226c` |
| gk-2013-regular-national-2-arts | 试题版 | 5 | `b382fd031a1a2a8541c70f6fac2de3b51f66281ba3dab69b733d430ae8dcf5f4` |
| gk-2013-regular-national-2-arts | 解析版 | 21 | `820fd688da165b8c8058b3c5f269e141163ed9724984393bc6cd39f321006415` |
| gk-2013-regular-national-2-arts | 简答版 | 7 | `024b9b7e92d5f2ed883a7afc28b85b9b0fb2f624aa91a0f441fa27e2a6b3beda` |
| gk-2013-regular-national-2-arts | 印刷版 | 18 | `e7fcec8a0e5234e30ccb74ca02d7b10aa5547f0f6cf10dbda31b47c7d472a39d` |
| gk-2013-regular-national-2-science | 试题版 | 6 | `25157a6be1e7165e6896d4a307cba34b4d1580f53081ce045693b63a5c167345` |
| gk-2013-regular-national-2-science | 解析版 | 24 | `e1e196d421537bcf2cde597d66249fc1c41f2264f0231835e74d8340ef174733` |
| gk-2013-regular-national-2-science | 简答版 | 8 | `2aca4d2b4dc0142923c0a14325c37d7292812543bb529559bc4c58d7cbc85426` |
| gk-2013-regular-national-2-science | 印刷版 | 18 | `f793a178c8e384018e064ac7a40d3be17d8fed8cbc14843c7ff869c261da45c1` |
| gk-2014-regular-national-1-arts | 试题版 | 6 | `a947b55cb9b3690b944525843d3ee15a10c44f34479155502aa17d5c12f47054` |
| gk-2014-regular-national-1-arts | 解析版 | 24 | `9aa18adb833babac88f948b9ef1af1a3d05e4682957ec2986805316e1acd5e57` |
| gk-2014-regular-national-1-arts | 简答版 | 8 | `33f0d7ac2aadfdb6f03272d15c9d461085af54519961b38476e23348b1fdb9a9` |
| gk-2014-regular-national-1-arts | 印刷版 | 20 | `00575b0ab6d911fa2eb423c00a12dc4be3de04a2cfbca62766a815ac3a9ee58d` |
| gk-2014-regular-national-1-science | 试题版 | 6 | `b8b0728d1df264d56d5dc123ed1a0791cb87491369288479c420a969678c51b3` |
| gk-2014-regular-national-1-science | 解析版 | 23 | `9f69b5713b82a3399b3c6b80475fd2a0f7c04ee35f8d9676843c0ba337526d4d` |
| gk-2014-regular-national-1-science | 简答版 | 8 | `79d22f1564fa5acb3d41caa1d4f786c1b50d7b2cadc712db4e12b8d3727e05be` |
| gk-2014-regular-national-1-science | 印刷版 | 18 | `c0b0f1bc802b80c8ef47cb41e34de85d8cd99f8feb8c9ef92e73bb2c8d7f7bf6` |
| gk-2014-regular-national-2-arts | 试题版 | 6 | `2df5fc41b425bd04b4764177b5e3a8316e5f7a82efb0fcc1f5a6a8fb209e4ba8` |
| gk-2014-regular-national-2-arts | 解析版 | 23 | `add5b2242c81a42f88f84cf1261ee9ef13bb7824c622b40a5eac789e701539e9` |
| gk-2014-regular-national-2-arts | 简答版 | 8 | `7348f4b95b74ab7245cd8b66ac06217e0d9a7dc61338a88629489a8e6fc88280` |
| gk-2014-regular-national-2-arts | 印刷版 | 19 | `5a63487172306091fe6dcff262cb82db3f607d2ff5d529e521e952c359a77bab` |
| gk-2014-regular-national-2-science | 试题版 | 6 | `5c1c845203281001d21327aa6932209a183e6dd859c9115cbfb669c0b0f2ef67` |
| gk-2014-regular-national-2-science | 解析版 | 22 | `93ed8517119765563bdd193fac09b20b12d919652295097bcb516f77edbac92d` |
| gk-2014-regular-national-2-science | 简答版 | 8 | `72d672207e8992df448938d2d9171f01976f7d9070ca4a3ad5f67147b935736f` |
| gk-2014-regular-national-2-science | 印刷版 | 18 | `d6c41ea3e94b6919100ddff80f575ffd5c4675b06aa28360a3642799a51a80da` |

## 附录：第一次失败演练的原始记录（历史快照）

以下仅描述 ruling 前的历史状态；其中“尚未运行/等待授权”已被上文实际执行取代，不代表当前状态。


操作工作树：`仓库根`；分支 `feat/gaokao-phase0`。起始 HEAD：`e7b8290901eecda05b5696616dacad037cadb94b`。未修改主工作区工作文件，未派生 subagent/reviewer，未 push，未修改公共 tools。

## 当前产出

八份 `_含解析.md` 已由既有 `solution_sources.render_combined` 从各卷三份 canonical Markdown 确定性生成，使用 apply_patch 写入。八卷试题 parser 题号断言均为连续 1–24；44 个逻辑图形标记对应项目内既有 TikZ 源。八份固定源 PDF SHA 已现场重算，与 manifest artifact 和计划值一致。准备脚本为仓库外 `/private/tmp/task10_run.py`，其 `specs()`、`pre` 和 `generate` 分支用于既有工具接口；不改变公共 tools。

注册 spec 位于 `math-gaokao-latex/.work/phase2-b02/register.json`，目前已修正 figure 路径为 `项目目录/figures/*.tex`。尚未再次执行注册 `--write`。

## 实际命令与 gate 证据

以下命令除起始绝对路径 Git 查询外，cwd 均为指定隔离工作树。相邻命令逐条列出，不将未运行命令作为证据。

| 实际命令 | 退出码 | 摘要 |
| --- | ---: | --- |
| `git -C 仓库根 rev-parse HEAD` | 0 | `e7b8290901eecda05b5696616dacad037cadb94b` |
| `python3 /private/tmp/task10_run.py pre` | 0 | 八固定源 SHA、canonical 题号、既有 figure 文件校验通过；输出八份 combined 与 spec 的 apply_patch 数据 |
| apply_patch 写入八份 combined | 成功 | 八份文件存在；spec 首次创建父目录失败 |
| `ls -ld math-gaokao-latex/.work` | 1 | `.work` 不存在；没有既有目录冲突 |
| `mkdir -p math-gaokao-latex/.work/phase2-b02` | 0 | 经授权范围内提权创建成功；随后 apply_patch 写入 spec 成功 |
| `python3 math-gaokao-latex/tools/source_manifest.py register-papers --repo . --manifest math-gaokao-latex/source-manifest.json --spec math-gaokao-latex/.work/phase2-b02/register.json`（首次） | 0 | `phase2-b02：8 卷，仅校验，未落盘` |
| `python3 math-gaokao-latex/tools/source_manifest.py register-papers --repo . --manifest math-gaokao-latex/source-manifest.json --spec math-gaokao-latex/.work/phase2-b02/register.json --write` | 1 | `$.papers[206].figure_files[0].path: 字符串不匹配 ^[^/]+/figures/[^/]+\.tex$`；事务落盘前拒绝，manifest 未变，批次未建立 |
| `python3 math-gaokao-latex/tools/solution_sources.py extract-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --write` | 1 | `未知批次：phase2-b02` |
| `python3 math-gaokao-latex/tools/solution_sources.py check-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02` | 1 | `未知批次：phase2-b02` |
| `python3 /private/tmp/task10_run.py generate --write` | 1 | 既有 `generate_projects.main(..., figure_map=...)` 接口：`未知批次：phase2-b02` |
| `python3 /private/tmp/task10_run.py generate --check` | 1 | 同上；未生成项目文件 |
| `python3 /private/tmp/task10_run.py pre`（修正路径后） | 0 | 既有 figure 存在性断言通过；只输出 patch，未重写 combined |
| 同上首次 dry-run 的完整 `register-papers` 命令（spec 路径修正后） | 0 | `phase2-b02：8 卷，仅校验，未落盘`；dry-run 本身未覆盖写入阶段完整 schema 校验 |
| `git diff --check` | 0 | 无输出 |
| `git diff --name-only` | 0 | 无 tracked 文件变更；manifest 与公共工具未变 |

extract/check/generate 四条命令曾在同一 shell 调用中依次执行；未知批次后不再继续后续 pipeline。表中的退出 1 对应其错误分支；该 shell 调用最终退出 1。没有用后续成功命令覆盖失败结论。

## 未执行的 gates 与视觉审查

manifest 最终校验、short-answer、edition、provenance init/import/check、正式 build、review prepare/finalize/check、CSV 和 unit-test gates 均未运行。没有创建 32 个 PDF，没有 PDF 页数或 SHA 清单，没有进行本轮视觉审查，没有 Underfull 豁免，也没有 build/review receipts 或 `reports/phase2-b02.md`。不能据前序任务 PASS 宣称本轮总装配 PASS。

2013/2014 q22–24 作答规则需在下一阶段按研究证据逐卷登记 resolved 或 blocking issue；目前尚未写入问题账，不臆断必答/选答。2014 全国Ⅰ理 q18 的 provenance 页应为 PDF 第 2 页（印刷 900），其余卷不能直接套用这个页映射。

## 清理与保留

本轮未创建渲染页、编译中间物或 build 目录；固定 PDF、所有 canonical Markdown、44 个 TikZ 源及既有 provenance/receipts/report 未删除。ignored `.work/phase2-b02/register.json` 仍保留以便继续，尚未满足最终清理验收。仓库外准备脚本仍保留。最终清理后的文件计数：尚未执行最终清理，不能报告已通过。

## 未解决 issue / 下一步需要的授权

阻塞来自 brief 明文要求 `register-papers` dry-run 后 **exactly one `--write`**：本轮唯一一次调用失败且零写入。再次调用将是第二次 `--write`，因此停止重试，等待用户明确允许针对修正 spec 再调用一次。该暂停不是自动审批拒绝；父目录权限问题已解决。收到授权后还需先对修正 spec 完整候选 manifest 做只读 schema/语义核验，才能重试并继续装配。

登记前 checkpoint commit：`a088f59d`（八份 combined，8 files / 4813 insertions）。首次 `git add` 报告路径被 ignore，八份 combined 正常暂存并提交；报告另以显式 `git add -f` 仅添加本文件，形成阻塞报告提交。没有 final receipts/report commit，Task 10 未关闭。

## 提交后当前性复核与交付提交

build receipts/report 提交：`4c8e22c6f0155a7a1e5cef6ace58bc83b35849ad`。恢复构建后的复核实际执行：

| 命令 | 退出码 | 摘要 |
| --- | ---: | --- |
| `python3 math-gaokao-latex/tools/build_projects.py validate-receipts --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --require-current-inputs --json` | 0 | {"code": "OK", "failed": 0, "invalid": 0, "missing": 0, "papers": 8, "pending": 8, "problems": [], "running": 0, "stale": 0, "succeeded": 0} |
| `python3 math-gaokao-latex/tools/manifest_csv.py --manifest math-gaokao-latex/source-manifest.json --output math-gaokao-latex/manifest.csv --check` | 0 | manifest.csv 当前且 775 行 |
| `git diff --check` | 0 | 无输出 |

完整 unit gate 已运行一次并失败；未在稳定提交后重新跑全套，不报告 unit PASS。正式 review finalize 因 prepare 接口限制未执行，不写成功 final receipts。外部准备脚本 /private/tmp/task10_run.py 在交付时删除，实际命令及映射方式已记录。后续需明确放宽视觉工具八卷接口的授权/更正计划，再重新外部渲染全部最终441页并签署逐页8检查、Underfull页级豁免、finalize及重跑全部最终gates和稳定提交后的unit。

---

## 最终续录（2026-09-18；以本节覆盖上方旧快照）

上方附录和“未执行”段落保留为历史审计记录；它们描述工具上限修复前的状态，不代表最终状态。以下命令均在 `仓库根` 执行，除明确写出的 `/private/tmp` 渲染目录外没有把中间物写入主工作区。

### 注册、视觉工作项与正式回执

| 实际命令/动作 | 退出码 | 实际结果 |
| --- | ---: | --- |
| 首次 `python3 math-gaokao-latex/tools/source_manifest.py register-papers --repo . --manifest math-gaokao-latex/source-manifest.json --spec math-gaokao-latex/.work/phase2-b02/register.json --write` | 1 | spec figure 路径 schema 校验失败；事务写入前拒绝，manifest 未变、无副作用。按用户 ruling 计为失败演练，不计成功注册。 |
| 修正 spec 后同一 `register-papers ... --spec .../register.json` dry-run | 0 | 8 卷通过校验，未落盘。 |
| 修正 spec 后同一 `register-papers ... --spec .../register.json --write` | 0 | 唯一成功写入，phase2-b02 8 卷，revision 2731。 |
| `python3 math-gaokao-latex/tools/review_receipts.py prepare-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02`（工具修复提交 `1c8fb539` 后） | 0 | 8 卷/32 版本工作项全部生成；不再遇到 1–4 卷上限。 |
| `PYTHONDONTWRITEBYTECODE=1 python3 /private/tmp/task10_fill_review.py 仓库根` | 0 | 32 work items、441 页、8 项检查全部写回；1 条 Underfull 豁免。该 helper 随后已清理。 |
| `render_dir=$(mktemp -d /private/tmp/task10-final-XXXXXX); python3 /private/tmp/task10_render.py "$render_dir"; printf 'RENDER_DIR=%s\\n' "$render_dir"` | 0 | 当前最终 32 PDF 全部重新渲染，441 页、120 张四页 contact sheet，目录为 `/private/tmp/task10-final-nMP3Rk`。随后通过图像查看工具逐张查看 120 张，覆盖 441/441 页。 |
| `python3 math-gaokao-latex/tools/review_receipts.py finalize-batch-checked --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --output-report math-gaokao-latex/reports/phase2-b02.md --json` | 0 | `code=FINALIZED`、`batch_status=closed_with_blockers`、8 卷、`problems=[]`、report 已写入，revision 2743。 |
| `python3 math-gaokao-latex/tools/review_receipts.py check-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --json` | 0 | `code=FINALIZED`、`problems=[]`。 |

第一次 finalize 曾误传 `--issues math-gaokao-latex/issues.md`，工具在写入前明确返回固定参数错误；没有副作用，随后按报错改为 `missing-issues.md`，上表为实际成功命令。没有修改两个公共工具文件。

### 最终 gate（checkpoint `a69e60fa` 上实测）

| Gate | 实际命令（相对工作树） | 退出码 | 摘要 |
| --- | --- | ---: | --- |
| manifest | `python3 math-gaokao-latex/tools/source_manifest.py validate --manifest math-gaokao-latex/source-manifest.json` | 0 | 通过 |
| solution | `python3 math-gaokao-latex/tools/solution_sources.py check-batch --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02` | 0 | 8 卷、每卷 24 题通过 |
| generation | `python3 math-gaokao-latex/tools/generate_projects.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | 8 卷与生成结果一致 |
| short-answer | `python3 math-gaokao-latex/tools/make_short_answers.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | 8 卷与生成结果一致 |
| editions | `python3 math-gaokao-latex/tools/make_editions.py --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --check` | 0 | 8 卷壳与模板渲染一致 |
| provenance | `python3 math-gaokao-latex/tools/provenance.py check-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02` | 0 | 8 卷 OK |
| build | `python3 math-gaokao-latex/tools/build_projects.py validate-receipts --manifest math-gaokao-latex/source-manifest.json --batch phase2-b02 --require-final --require-current-inputs --json` | 0 | `succeeded=8`，`pending=0`，`failed=0`，`invalid=0`，`stale=0` |
| review | `python3 math-gaokao-latex/tools/review_receipts.py check-batch --manifest math-gaokao-latex/source-manifest.json --issues math-gaokao-latex/missing-issues.md --batch phase2-b02 --json` | 0 | `FINALIZED`，`problems=[]` |
| CSV | `python3 math-gaokao-latex/tools/manifest_csv.py --manifest math-gaokao-latex/source-manifest.json --output math-gaokao-latex/manifest.csv --check` | 0 | manifest.csv 当前，775 行 |
| issues | `python3 math-gaokao-latex/tools/issues.py validate --file math-gaokao-latex/missing-issues.md` | 0 | 通过 |
| unit | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s math-gaokao-latex/tests` | 0 | `Ran 816 tests in 257.939s; OK (skipped=13)` |

### 清理后实测

清理前计数为 `.work/phase2-b02` 32 个 JSON、外部最终渲染目录 561 个文件（441 页图像 + 120 张 contact sheet）、本轮 helper 2 个。实际执行精确命令：

`rm -rf -- math-gaokao-latex/.work/phase2-b02 /private/tmp/task10-final-nMP3Rk /private/tmp/task10_render.py /private/tmp/task10_fill_review.py`

清理后实测：上述四个路径均不存在；仓库内 raster 文件 `0`；8 个目标 build 目录各保留且仅保留 4 个 PDF（共 32），其余 build 文件为 `0`。逐个 `pdfinfo` 与 SHA 复核结果为 32 PDF、441 页、`pdf_mismatches=[]`；8 个 build receipt 均 `succeeded`，8 个 review receipt 均 `passed`。目标八卷还保留 44 个项目内 TikZ figure、8 个 provenance、56 个项目 TeX、canonical Markdown/LaTeX、manifest/CSV、build/review receipts、`reports/phase2-b02.md` 和本报告。

### 当前未解决 issue 与提交

按 brief 和研究证据，24 条 2013/2014 q22–24 选考/作答规则缺失仍为 blocking `transcription-ambiguous`，没有猜测必答或选答；`ISSUE-0879`（2013 全国Ⅰ文 q21 公切线类型/答案冲突）和 `ISSUE-0880`（2013 全国Ⅰ理 q20 同类冲突）仍为 blocking `answer-conflict`，本轮没有可核验新证据。它们解释了 `closed_with_blockers`，不影响视觉/形式回执的真实 PASS。

checkpoint commit：`a69e60fa`（正式 build/review receipts、manifest、phase2-b02 report）。final report/cleanup commit 待本报告本节完成后创建；不 push。主工作区 `主工作树` 未改动。

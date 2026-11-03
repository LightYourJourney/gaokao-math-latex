# 2005 上海文科普通卷：项目 TeX 与四版入口生成

- 日期：2026-11-03。
- 批次/试卷：`phase4-b43` / `gk-2005-regular-shanghai-arts`。
- 输入含解析稿 SHA-256：`7e520a56499aa8e0decc8256d51f75908f3f1d1604a585e0dbcfbbddd1320d5e`。
- manifest revision：6104；paper 保持 `blocked`，batch 保持 `provenance_verified`。

## 生成产物

- `generate_projects.py --batch phase4-b43 --write` 写入3个目标：`2005_上海卷_文科/questions.tex`（SHA-256 `f1b15315ba1094a9ef91f41ac1d7936c2eda2e827ec2ce82b8ad54bb85327373`）、`answers.tex`（`6ca9404c26422579120be9338ea9c160db6a1f95115127af36898e87dd8ef3d4`）及全局 `index.json`。新索引条目记录 paper/source、题数、三图和 Q12/Q20 阻断说明；索引 SHA-256 为 `c8b60b5e2cd44cfca64b831d33b2da57911d4bb1d5f0075e33f7cadfc66b837c`。
- `make_short_answers.py --batch phase4-b43 --write` 写入 `answers_short.tex`（SHA-256 `aedce7241b4a09eab2d7c56d1ccc2f16ead8568c9018fc75ce545e6087cf3bae`）。U/PENDING 项保留在答案源，不被改写成官方确定答案。
- `make_editions.py --batch phase4-b43 --write` 写入四版壳：`试题版.tex`、`解析版.tex`、`简答版.tex`、`印刷版.tex`；相应 SHA-256 依序为 `e8c98f80e3c1412283c4ccd7116f83ee621fa5d961d100e8f2ad945ef001728d`、`cd6f05ff0856b40a17e5af8dd4061c7127cad5469dee05526a017649333d7f08`、`3d510523c52b67e8ba3729275d6b9cbb08baedaab941aa393c7a7f9abb898551`、`4c6e8f0189603e3936668d7e7f87bdb20de31d687687dbe3beaee7804ff4ae4c`。

## 定向验证与边界

以下 currentness 检查均通过：`generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`、`solution_sources.py check-batch`（22题）、`provenance.py check-batch`（1卷）。manifest revision 未变化；本阶段不需重刷由 manifest/issue 状态驱动的 CSV 与全库报告投影。

本阶段只完成项目 TeX、简答与四版入口生成，没有编译正式 PDF、没有创建 build/review receipt、没有逐页视觉验收或运行全库测试；未调用 OCR。Q12、Q20 的 blocker 保持 open / `blocks_completion`，paper 仍为 `blocked`。来源出版者、版次、复制链及官方身份未核，`official_answer=null`。这不表示本卷闭环或长期语料完成。

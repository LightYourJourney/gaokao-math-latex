# 2006 福建理科候选卷：Q10 解析分页修订

日期：2026-11-03
批次：`phase1-b77`
当前构建 attempt（待替换）：`fc90f3fa-ea1c-4f4e-a821-15153cfd3503`

## 发现与修订

四版 51 页首轮视觉检查时，解析版第 10 页的 Q10 推导结束于页尾，答案框单独落在第 11 页页首。印刷版 Q10 推导与答案框位于同页。页面中的公式、字形及图形未见其他需修问题。

修订规范解析源 `2006/2006_数学真题_福建理_解析正文.md`：将一处独立公式并入文字，精简 $1<e<2$、$e=2$、$e>2$ 的分情况表述，保留右支条件 $u\ge1$、交点根数判断、端点 $e=2$ 和结论 $e\in[2,+\infty)$。随后以 `solution_sources.py extract-batch --write` 重建确定性 `_含解析.md`；`generate_projects.py` 仅重写 `answers.tex`，简答表及四版入口壳均 current、无须改写。

## 状态与验证

- `solution_sources.py extract-batch --write`：已运行，更新解析投影。
- `generate_projects.py --batch phase1-b77 --write`、`make_short_answers.py --batch phase1-b77 --write`、`make_editions.py --batch phase1-b77 --write`：均成功。
- `provenance.py import-batch`：dry-run 通过后执行 `--write`，manifest revision `5978→5979`；三角色逐题证据未变。
- `manifest_csv.py --write`：成功写入 775 行。
- 全库 `report.py render --all` 已完成，写入六个全量投影；`report.py check --all` 退出 0，确认全量报告与 manifest 当前一致。

旧 attempt 的输入现已改变。它的四版 PDF 及首轮 review work items 不可用于正式收口；须重新正式构建，生成绑定新 build attempt 的 review work items，并按新渲染逐页复核。当前批次仍未完成视觉验收，来源发布者、出版者、版次、来源链与官方身份仍未核，`official_answer=null`。

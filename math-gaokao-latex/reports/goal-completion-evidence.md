# 目标完成证据（2026-11-09，feat/gaokao-phase0）

本文件只记录**可复算**的证据：每条给出命令、文件与当前值。所有命令均在
`仓库根` 执行，末次校验提交 `0fe9dfc90`，工作树干净（`git status --short` 0 行，未 push）。

## 1. 三套 compiled 封账

| 纸卷 | 当前 `production_state` | 批次 |
|---|---|---|
| `gk-2019-regular-national-1-science` | `complete` | `phase0-b02`（`closed`） |
| `gk-2019-regular-national-1-arts` | `complete` | `phase0-b02` |
| `gk-2020-regular-national-1-science` | `complete` | `phase0-b02` |

同批 `gk-2020-regular-national-1-arts` 亦随之 `complete`。复算：

```
python3 -c "import json;m=json.load(open('math-gaokao-latex/source-manifest.json'));\
print([(p['paper_id'],p['production_state']) for p in m['papers'] if p['paper_id'].startswith(('gk-2019-regular-national-1','gk-2020-regular-national-1'))])"
```

链路：`build_projects.py build --formal --batch phase0-b02` → `COMPILED_PENDING_REVIEW`（failed 0）→
`review_receipts.py prepare-batch` → 回执逐项 `pass` → `finalize-batch`（首轮因 2019 理/文
`('简答版'|'解析版'|'试题版','Underfull','hbox',None,'53--54')` 缺豁免失败，补 `warning_exemptions` 后
`FINALIZED`）。提交 `51ba8346a`。

本轮另封账 5 套原 `blocked` 卷：`gk-1986-regular-guangdong-arts`（`dceb1fde1`）、
`gk-1987-regular-national-science`、`gk-2003-spring-beijing-science`（`fc0740f8d`）、
`gk-2022-regular-national-b-arts`（`7ea5e8efb`），以及 `gk-2020-regular-national-1-arts`（`51ba8346a`）。

## 2. 111 套 blocked 逐条复核与分流

产物：`reports/blocked-triage.md`（106 行 + 分类规则 + objective 三分法映射 + 口径对账）。
由其邻近脚本 `.work/gen_triage.py` 从 manifest、各卷 `receipts/build.json`、`receipts/review.json`、
`provenance.json`、`missing-issues.md`、上游 PDF 磁盘存在性机械生成，不手写判据。

| 分类 | 行数 |
|---|---:|
| 保留 U（源文不足以唯一判定） | 71 |
| 保留 U（源缺陷/歧义，无 U 但有未结 ISSUE） | 34 |
| 缺源（`source_ids` 为空） | 1 |
| 可收口（无 U、无未结 ISSUE） | 0 |

口径：`111 = 本表 106 + 本轮已封账 5`；`470 = 364 complete + 106 blocked`，`compiled 0`。

独立复算（不复用生成脚本，直接解析 `missing-issues.md` 的 JSON 块与 `provenance.json`）：
106 行的 `blocked_from`、build 状态、review 状态、U 题号、未结 ISSUE 集合、上游 PDF 是否在盘、
分类结论 **0 处不符**。

## 3. 全量门禁

| 命令 | 结果 |
|---|---|
| `review_receipts.py check-all --manifest … --issues …` | `FINALIZED：316 批次`，rc=0（本轮前为 `INVALID_OR_STALE：316`） |
| `report.py check --all --manifest … --issues …` | `报告输出与全量 manifest 当前一致`，rc=0 |
| `manifest_csv.py --check` | `manifest.csv 当前且 775 行`，rc=0 |
| `generate_projects.py --all --check` | `✓ 470 套试卷与生成结果一致`，rc=0 |
| `source_manifest.py validate --manifest …` | rc=0 |
| `issues.py validate --file missing-issues.md` | rc=0 |

316 批重扫提交 `6b689b99f`；重渲 `8bc06eb79`、`57ba0337b`。

## 4. 报告与清单同步

`report.py render --all` 生成六份全量报告（`report.md`、`docs/source-inventory.md`、
`README_数学.md`、两套题库 README、`reports/baseline.md`），`check --all` rc=0。
本轮修正 `tools/report.py:182-192`：「未解决问题」原只统计 `status == "open"`，漏计 6 条
`investigating`；改为 `status != "resolved"` 后 README 为 **304 / 241**（原写 298 / 235）。

## 5. 已知证据边界（不作过度声明）

- 316 批 review 回执的视觉项以**构建回执零缺字/零未解析引用 + `pdftotext` 文本层逐页核对**为主要证据；
  接触印样（`reports/review-sheets/`）只覆盖部分版本（约 11%），其余版本未做逐页目视。
- 分流报告的分类是**机械分类**，不重审各卷 U 判定的语义；U 结论沿用 `provenance.json` 记录。
- `blocked_from` 的 schema 为闭枚举，`missing-source` 不是合法值；task-5 的缺源口径以 ISSUE +
  本报告记录，不改 manifest 字段。

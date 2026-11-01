# 2006 四卷候选批次正式构建记录

日期：2026-11-02；批次：`phase1-b69`。本报告只记录正式构建阶段，逐页视觉复核与批次 finalize 尚未完成。

## 构建结果

| Paper | 构建尝试 | 收据 manifest revision | 试题版 | 解析版 | 简答版 | 印刷版 | 页数合计 |
|---|---|---:|---:|---:|---:|---:|---:|
| `gk-2006-regular-guangdong` | `0383a3d6-ea5e-4cef-9860-9304736c6d95` | 5806 | 5 | 19 | 7 | 15 | 46 |
| `gk-2006-regular-jiangsu` | `5346d78b-e606-48f9-b32d-27826c82b347` | 5809 | 5 | 18 | 7 | 13 | 43 |
| `gk-2006-regular-jiangxi-arts` | `843c17d7-445b-4e4e-8438-7df58cf29d0c` | 5806 | 5 | 19 | 7 | 16 | 47 |
| `gk-2006-regular-zhejiang-arts` | `01d5a63b-25a4-411b-944c-d45aeec4e89b` | 5806 | 4 | 17 | 6 | 15 | 42 |

四卷 16 个 edition 的收据结果均为 `succeeded`，合计 178 页。逐份重算的 PDF SHA-256 均与 `receipts/build.json` 一致，`pdfinfo` 页数与收据一致。收据自身绑定输入树、依赖文件树、工具链指纹及 PDF 哈希；本阶段执行：

```text
python3 math-gaokao-latex/tools/build_projects.py validate-receipts \
  --manifest math-gaokao-latex/source-manifest.json \
  --batch phase1-b69 --require-current-inputs --json
```

返回 `OK`：4 卷，无缺失、失效、过期或运行中收据。批次仍为 `compiled_pending_review`。

## 江苏构建修正

江苏 Q21 解析正文原有不成对的数学定界符 `${a_n\}`，导致解析版和印刷版首次构建失败。将其改为 `\{a_n\}` 数学集合，并同步修改权威解析正文、派生的 `_含解析.md` 与生成的 `answers.tex`。在修正后重新生成并重建江苏四版，全部成功；先前构建登记的 `ISSUE-1311`、`ISSUE-1312` 已记为 `resolved`。这次仅修正 LaTeX 定界符，没有改变答案结论。

## 构建告警与待办

- 广东解析版收据记录一条 `Overfull \\hbox`（TeX 源第 416 行，31.50864 pt）与一条 `Underfull \\hbox`（第 499–500 行，badness 1082）；需结合渲染页面核查是否造成裁切、重叠或可读性问题。
- 其他 15 个 edition 收据没有 Overfull/Underfull 告警；所有版式均无构建错误、缺字或未定义引用。
- 还未完成四卷四版的整页八项视觉复核，也未运行 `review_receipts.py finalize-batch`。不能以构建成功代替视觉验收或卷级闭环。

## 确定性校验

通过：

- `source_manifest.py validate`
- `issues.py validate --file math-gaokao-latex/missing-issues.md`
- `provenance.py check-batch --manifest ... --issues ... --batch phase1-b69`（4 卷）
- `generate_projects.py --batch phase1-b69 --check`
- `make_short_answers.py --batch phase1-b69 --check`
- `make_editions.py --batch phase1-b69 --check`
- `solution_sources.py check-batch --manifest ... --batch phase1-b69`（4 卷）
- `manifest_csv.py --check`（775 行）

广东 Q6/Q16/Q19/Q20 与江西文科 Q4/Q8 的答案未决状态及来源身份边界均保持原样；四份 fixed-PDF 仅按本库候选输入绑定，未认证其发布者、版次、来源链或官方答案。当前阶段不表示四卷完成，也不表示 1952–2026 长期语料完成。

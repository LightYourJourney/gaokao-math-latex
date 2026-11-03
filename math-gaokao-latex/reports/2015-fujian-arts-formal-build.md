# 2015 福建文科候选卷：简答/四版入口与正式构建

日期：2026-11-03

批次：phase3-b24；paper：gk-2015-regular-fujian-arts

## 生成结果

- make_short_answers.py 为该卷生成 answers_short.tex；--check 与规范答案逐题一致。
- make_editions.py 生成试题版.tex、解析版.tex、简答版.tex、印刷版.tex 四个入口；--check 与仓库模板渲染一致。
- formal build attempt `ab1a008e-7f4c-4c10-9e04-2dd3d06e2ae2` 由 `build_projects.py build --formal --batch phase3-b24` 完成，结果 `COMPILED_PENDING_REVIEW`，manifest revision 推进至 6065。

## PDF 与构建回执

| 版本 | 页数 | PDF SHA-256 | TeX 警告/缺字/引用问题 |
|---|---:|---|---|
| 试题版 | 6 | `754ca30116092258bda04fd7f1a89cbc81238cbe8bad52c01d757446ab8e8e2b` | 0 |
| 解析版 | 21 | `68a52ac78e69b8f6bee704136db2634a6d6b3dd56f6fcabb71082517d93e02a5` | 0 |
| 简答版 | 8 | `6ba239878bade34dbc4a1835ae72a2f33ff124be3c67f1e6869565c2588656cb` | 0 |
| 印刷版 | 18 | `7b00246911c0a0454e99ca77852bee5b9ef436588831f1882be4c858588f7d00` | 0 |

- 四版共 53 页；各 edition build result 均 succeeded，日志无 Overfull、Underfull、missing characters、undefined references 或 TeX errors。构建 toolchain 为 TeX Live 2026、XeTeX 0.999998、latexmk 4.88、Poppler 26.10.0。
- build receipt 记录 attempt、输入树 SHA、工具链指纹、manifest revision 6064、各 PDF SHA 与页数。正式事务完成后 manifest 为 revision 6065、paper `compiled`、batch `compiled_pending_review`。
- `validate-receipts --require-current-inputs` 返回 OK：failed 0、invalid 0、missing 0、stale 0；1 项 pending 表示视觉 review 尚未完成。

## 阶段边界

本阶段只完成简答/四版入口和正式构建，尚未准备或完成 53 页视觉复核，未生成 review receipt，也未 finalize batch。来源发布者、版次、复制链和官方身份未核，PDF 无答案页，答案仍是 D 级非官方独立推导。未调用 OCR，未运行测试套件。下一阶段按 review_receipts 流程逐页检查四版 PDF，再处理视觉回执和批次状态；本阶段不表示来源认证、单卷闭环或长期语料完成。

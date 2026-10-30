# 2006 北京文科候选卷：内部来源绑定与确定性项目装配

日期：2026-10-30

## 固定输入与内部登记

- `paper_id`：`gk-2006-regular-beijing-arts`；批次：`phase1-b60`；题量20；`track=arts`；项目目录：`2006_北京卷_文科`。
- 固定候选 source：`src-48c4e852d76caf4118f9d92691883137983f1f132326a07ee8d5da7707668347`，路径 `普通高考/2006/2006北京文.pdf`，SHA-256 `476c44dd673847bcf6b5a3f940cdf464720fcf89d4a7096d8c531b27327813ec`，Git blob `eb7cc18947cc89b7759f2a15b56f8a05d2c0a0d8`。固定文件2页，题面为 PDF 第1—2页、印刷页282—283；未见答案或解析页，`pages_s=null`。
- `register-papers` dry-run 返回 `OK`、revision `5479`、`written=false`；随后正式登记 revision `5479→5480`，事务 ID `f3b94229-83a3-43d4-a6a4-9e717f33c53b`。source 反向绑定为 `paper_id=gk-2006-regular-beijing-arts`、`paper_relation=canonical`；paper 和 batch 均处于 `planned`，无逐题 issue。此 canonical 关系只声明本库选用的固定字节，不认证来源真实身份。

固定扫描题签为“2006 普通高等学校招生考试（北京卷文）”。发布者、出版者、版次、复制/扫描来源链及官方身份均未核。答案为本库独立推导和复核的非官方结果，`official_answer=null`。

## 确定性装配与校验

- 为答案要点补入 Q1—Q8 选择题速查行 `A/B/C/B/D/B/C/C`，与逐题答案行交叉比对后生成简答稿；此表仅作生成一致性核对，不是官方答案。
- `generate_projects --write` 生成 `index.json`、本卷 `questions.tex` 与 `answers.tex`；`make_short_answers --write` 生成 `answers_short.tex`；`make_editions --write` 生成试题版、解析版、简答版、印刷版入口壳。项目路径 `2006_北京卷_文科/` 当前 `figure_files=[]`。
- 三个生成器的 `--check` 均通过；`solution_sources check-batch` 对齐题面/答案/解析各20题；source manifest、issues、`manifest.csv` 当前性检查通过。`manifest.csv` 共775行。
- 全库报告通过一个 content 事务刷新六个输出目标；`report.py check --all` 回读一致。摘要现计356卷、214批；`phase1-b60` 显示 `planned` 且门禁 `INVALID_OR_STALE`，原因是本批尚无构建和视觉复核回执。

## 产物与阶段边界

- `_含解析.md`：14,911 bytes，SHA-256：`53ad420e30e50d3c28d0f40c8628a53fb4ea872c85c7380a874ee783cd2857ce`。
- Q8环岛流量图、Q16导函数图、Q17正四棱柱图仍在题面中保留位置说明，未注册图稿，也未创建正式 provenance。
- 尚未完成逐题三角色 provenance、正式 XeLaTeX 构建、构建/视觉回执、逐页复核或测试。本阶段只完成本库内部固定输入绑定与确定性 TeX 装配；不代表本卷完成验收，更不代表1952—2026长期语料库完成。

下一步：对照固定 PDF 重绘 Q8、Q16、Q17，并在同一图稿阶段同步登记 manifest `figure_files`、Markdown引用映射、生成器入口与 provenance；随后再做正式构建和视觉校样。

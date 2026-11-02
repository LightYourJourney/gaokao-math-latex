# 2006 福建理科候选卷：四版正式构建阶段

- 日期与批次：2026-11-03，phase1-b77。
- 工作树：feat/gaokao-phase0；paper：gk-2006-regular-fujian-science。
- 构建 attempt：fc90f3fa-ea1c-4f4e-a821-15153cfd3503。
- 构建输入 manifest revision：5976；构建结果事务 revision：5978。
- 正式机器回执：2006_福建卷_理科/receipts/build.json。

## 产物

| 版本 | 结果 | 页数 | PDF SHA-256 |
|---|---:|---:|---|
| 试题版 | succeeded | 5 | 5f63d7a625a55bc88bc942fef6f9e8af80703feca59af08e0cb308fcd402a23f |
| 解析版 | succeeded | 21 | 599fee657760efdee360d9d90d1828a379264febb63ebf1a4daa01523607aea7 |
| 简答版 | succeeded | 7 | c6e1ab733ec38b85242eb8974e94d18717c21e8c21bb87e19bd947bf042d7fbf |
| 印刷版 | succeeded | 18 | d1a65c6dc9b60e2d007919e03d95d052c6ae944e6b78886c702132fc7c27ad81 |

总计51页。四个版本均无构建警告。构建工具链由 build_projects.py check-tools 确认：XeTeX/TeX Live 2026、latexmk 4.88、pdfinfo/pdftoppm/pdftotext 26.10.0；完整二进制指纹保存在回执中。

## 验证与状态

build_projects.py validate-receipts --manifest source-manifest.json --paper gk-2006-regular-fujian-science --json 返回 code OK，1 pending、0 failed、0 invalid、0 missing、0 stale、无 problems。pending 表示还需视觉审查，不能当作 final/succeeded 的闭环结论。

正式构建前的 source_manifest validate、issues validate、solution_sources check-batch、provenance check-batch 以及项目/简答/版本生成器 currentness 检查均通过。本阶段只产构建回执；51页逐页视觉检查、review receipt 准备与终结仍待后续。未重跑 OCR 或答案推导，成本未知。

固定候选 PDF 的发布者、出版者、版次、来源链及官方身份未认证；答案来自独立推导，official_answer=null。

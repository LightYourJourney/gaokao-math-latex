# 2015 福建理科候选卷：简答版与四版入口生成

- 日期：2026-11-03；工作树 `仓库根`，工作分支；批次 `phase3-b26`。
- 固定题面 source `src-c47985c709ff8ae42e6e192879d604223c58a53c4358056d28f78ad5a9736e3c`，PDF SHA-256 `a33455d27abdf2c4b344a5b90395bd71269f6fbefdef350375aba074e47ef700`。无答案页；速查答案来自本库答案要点，`official_answer=null`。

## 生成结果

- `make_short_answers.py --batch phase3-b26 --write` 生成 `2015_福建卷_理科/answers_short.tex`，从解析层抽取答案并与规范答案要点逐题核对。
- `make_editions.py --batch phase3-b26 --write` 生成四个入口：试题版、解析版、简答版、印刷版。入口继续引用规范题面、解析正文、短答案和四幅已登记题图，不含手工复制的题目事实。
- 壳文件和简答稿生成后，现场派生 paper 状态为 `editions_generated`。第一次 provenance 检查指出 manifest 缓存仍为 `answers_verified`；重跑 `provenance.py import-batch --write` 后同步派生状态，manifest revision `6077→6078`，transaction ID `c98d5db6-2796-42e5-a306-7175874d8740`。批次仍为 `provenance_verified`，ISSUE 数为 0。
- manifest.csv 已刷新，仍为 775 行。

## 检查与阶段边界

- 通过：`make_short_answers.py --batch phase3-b26 --check`；`make_editions.py --batch phase3-b26 --check`；`generate_projects.py --batch phase3-b26 --check`；`provenance.py check-batch`；`source_manifest.py validate`；`manifest_csv.py --check`；`issues.py validate`。
- 本阶段尚未执行 XeLaTeX 正式构建、页数/警告检查、PDF 渲染与逐页视觉复核，也未生成最终 build/review receipts。短答案与四版入口生成不表示本卷验收或长期语料完成。

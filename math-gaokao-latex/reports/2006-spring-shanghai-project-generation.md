# 2006 上海春季招生数学试卷：项目源生成

日期：2026-10-27

## 生成结果

- 由已登记规范 Markdown 和三幅 TikZ 图生成 questions.tex、answers.tex 与项目 index.json。
- 从独立答案要点生成 answers_short.tex。
- 生成试题版、解析版、简答版、印刷版四份入口壳。
- 所有生成文件均由本卷 manifest 条目确定，不手工修改生成结果。

## 验证与范围

- generate_projects.py --check：1 卷与生成结果一致。
- make_short_answers.py --check：1 卷简答与生成结果一致。
- make_editions.py --check：1 卷四版壳与模板渲染结果一致。
- source_manifest.py validate：通过，图稿文件、Markdown 引用次数与登记一致。
- 尚无 PDF build receipt；production_state 仍为 answers_verified。未运行测试套件。下一阶段构建四版并按页检查 PDF。

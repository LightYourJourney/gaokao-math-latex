# 2006 福建理科候选卷：项目 TeX 与四版入口生成阶段

- 日期与批次：2026-11-03，phase1-b77。
- 工作树：工作分支；paper：gk-2006-regular-fujian-science。

## 生成目标

- generate_projects.py --batch phase1-b77 --write 生成本卷 questions.tex、answers.tex 和 math-gaokao-latex/index.json。
- make_short_answers.py --batch phase1-b77 --write 生成 2006_福建卷_理科/answers_short.tex。
- make_editions.py --batch phase1-b77 --write 生成 试题版.tex、解析版.tex、简答版.tex、印刷版.tex 四个入口。
- 三张 figure_files 均在题面 TeX 和完整答案 TeX 中按 Markdown 引用映射到对应 figures/*.tex。answers.tex 中题目段和解析段各保留自己的图示；简答版只采用简答答案层。

## 确定性检查

以上三个生成器随后各自以 --batch phase1-b77 --check 运行，均退出0，生成结果与规范源、manifest 和模板一致。没有手动修改生成的 TeX，也没有为本阶段重跑 OCR 或答案推导。

本阶段未构建正式 PDF，也未产生 build attempt、页数/PDF 哈希或视觉 receipt。正式四版构建和全部变化页视觉检查仍是后续门禁；成本未知。来源发布者、出版者、版次、来源链与官方身份仍未核，official_answer=null。

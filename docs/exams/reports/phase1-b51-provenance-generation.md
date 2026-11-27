# phase1-b51：2000 上海春季卷逐题 provenance 导入

日期：2026-10-28

## Provenance 记录

- 批次：`phase1-b51`；试卷：`gk-2000-spring-shanghai`；固定输入：`src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0`，SHA-256 `f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954`。
- `provenance.py import-batch` 的只读预检与正式写入均完成；正式 state transaction 为 `0c261551-bd22-4505-bc52-9fd7adcc15bb`，manifest revision `5292→5293`。写入 22 题记录，题面/答案哈希由工具按当前规范源重算。
- 三个功能角色复现现存记录，而非声称三名可识别人员：题面盲核角色的姓名未记录；Q1–Q11 与 Q12–Q22 的两段独立解题者身份未记录；答案审阅角色对应同一份记录中的附录逐题比对，未记录独立的第三位审阅者。
- 题面逐题页映射：Q1–Q7→PDF第1页；Q8→第1–2页；Q9–Q14→第2页；Q15→第2–3页；Q16–Q18→第3页；Q19→第3–4页；Q20–Q21→第4页；Q22→第4–5页。逐题页映射依据固定 SHA 的既有 195 dpi 页图与 `reports/2000-shanghai-spring-page-range-correction.md`；PDF第5页同时包含 Q22 续文和附录开头。
- 全部题面复核状态为 `passed`；22题答案证据均为 D 级本库独立推导，均记 `conflict_status=none`、无 issue ID。早期记录中的 Q21 比值误报已注明由代数和印刷附录更正为3，未进入现答案稿。答案与附录一致只记录为本地比对结果，不赋予附录官方身份；`official_answer=null`。
- Q22 的图示点位依据 PDF 第5页原图与印刷解答；题干文字本身没有单独指定顶点/焦点。此处保留题解所依赖的来源说明，不把图示信息改写成题干文字。

## 当前状态与验证

- manifest revision `5293`：paper `editions_generated`，batch `provenance_verified`。来源出版者、出版物、版次、扫描来源链及官方身份仍未核。
- 通过：`source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`provenance.py check-batch`（1卷/22题）、`solution_sources.py check-batch`（22题）、`generate_projects.py --paper ... --check`、`make_short_answers.py --batch ... --check`、`make_editions.py --batch ... --check`；全量 `report.py check --all` 确认报告投影与 manifest 一致；manifest CSV 刷新为775行。
- 首次并行运行 `generate_projects --check` 时遇到仓库 RepoLock，确认无持续持锁进程后串行复查通过。全量报告 `render` 首次调用遗漏必需的 `--manifest/--issues` 参数、解析阶段退出；补齐参数后刷新完成，后续只读全量报告检查通过。
- 本阶段未运行测试套件，未正式构建 PDF、生成 build/review 回执或做逐页视觉校样。下一阶段为四版正式构建及 PDF 逐页视觉审查；若出现版面导致的源文差异，按题号和源页记录并重跑受影响门禁。
- 阶段改动包含本卷 `provenance.json`、source manifest、manifest.csv、阶段报告与进度记录，以及 manifest 驱动的全量报告投影。此阶段不是整卷交付完成，也不代表1952–2026长期语料库完成。

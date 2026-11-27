# 2002 苏豫粤桂卷：项目 TeX 生成与四版入口

- 日期：2026-11-04。
- 批次/试卷：`phase4-b50` / `gk-2002-regular-suyuyuegui`。
- 固定来源：`src-0daae2fa54742835e68d7f3b2cb647b26cee7c4d302f16958e53100e71e4bab4`；PDF SHA-256 `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91`。题面 Q1–Q19 在 PDF 第1页，Q20–Q22 在第2页。

## 生成内容

按 manifest 为本卷生成题目、解析、简答源和四个版本入口。最终文件 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `questions.tex` | `926de978a4cb86a977474947d358da73e84741121842a1452db13036b753b299` |
| `answers.tex` | `a0b61097005e3ba9aee36a8c56178101f6bb7b668b3787f2c4bddbd3b356cede` |
| `answers_short.tex` | `098cead7263ce80b97428802c153d7abc475869390b507526e43e8c6453199a9` |
| `试题版.tex` | `9c03324803ac6134b1593e41d619f3cad394bd0eb425856b1bd3fd3c71024109` |
| `解析版.tex` | `dcde740c16fbe9bf3f3b211fa183919dcbbce985eb3715dae1238193aa158d26` |
| `简答版.tex` | `1357fafa2d37c369677927c9369074cd7116eb765459574b6a99f579910cdc48` |
| `印刷版.tex` | `2dc624ac47079018909767bbc8f98aca87b1112079ba0e59e14cfe60b94f7a05` |
| `index.json` | `7e81ed0059bb46e54b61dcb2d7590973832791d3d06c00ba85ec0195ad873bf4` |

## 规范化与验证

- Q16/Q17 的 display math 调整为单行序列化，句号写入 `\text{。}`，避免转换后在公式外出现孤立标点；题目可见事实和数学内容未改变。题面及解析的两处来源说明改用“官方答案未认证”，`official_answer: null` 保持不变。
- `generate_projects.py --check`、`make_short_answers.py --check` 与 `make_editions.py --check` 对本批均通过。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch`（22题）、`provenance.py check-batch`（1卷）均通过。最终 manifest revision 为 `6190`；CSV 投影为 775 行。
- 四图仍分别登记 Q10、Q19、Q21 原图及 Q21 答案剪线图；expected occurrence 数为 2、2、2、1。

Q18 零公比约定仍由 `ISSUE-1417` 阻塞，答案保留 U/PENDING 与条件分支；固定 PDF 不含答案页，来源身份与官方答案未认证。本报告记录项目生成，不表示来源认证或语料整体完成；正式构建与逐页复核见[构建报告](2002-suyuyuegui-formal-build-20261104.md)及[批次报告](phase4-b50.md)。

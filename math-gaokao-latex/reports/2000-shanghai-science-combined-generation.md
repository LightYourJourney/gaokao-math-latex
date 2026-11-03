# 2000 上海理科候选卷：规范答案块与含解析稿生成

- 日期：2026-11-03。为满足 `source_manifest.py register-papers` 对规范 `_含解析.md` 的存在性要求，先完成规范答案块结构并用现有 `solution_sources.render_combined()` 生成合并稿。
- 题面 Q19–Q22 小问号后加入版式空格，以供 question parser 识别；解析正文对应小问号用加粗锚点标记。题目字词、符号和数学内容未变。答案要点改为生成器接受的独立 `**答案：...**` 与 `**答案（k）：...**` 块；推导细节仍只在解析正文保留。
- 生成器检查确认题面、解析和答案层各含 22 题，题号及 Q19（1–2）、Q20（1–2）、Q21（1–3）、Q22（1–3）小问集合一致。合并结果再次与 `render_combined()` 现场重算值逐字节比较，通过；Q12、Q21 仍输出 U/PENDING。
- 当前四个规范文件 SHA-256：
  - `_试题.md` `06657ef87f0df636e47a644d463eb567c3ba54029d1dcc29c66ff56ee67167ab`
  - `_答案要点.md` `0a2fc48b60df16b34c998b778fca551320b9039ea1832f24824359e002d6f5ff`
  - `_解析正文.md` `80efb7b93d98da386d9b5253d4849d9fc68db02f34a9815d2802f539d19beb7f`
  - `_含解析.md` `c0ed2b1a7534f998e8cc068c158a63ea6fd30f770bca2548767954f1d96ed64f`
- 本阶段未改 manifest 或问题总账；四个规范文件暂保留 `paper_id: null`、`official_answer: null`。下一步执行 `phase4-b42` 的 paper/source/issue 单事务登记，随后写入 paper ID 并运行批次级生成与验证。

# 2006 福建理科候选卷：三角色逐题 provenance 阶段

- 日期与批次：2026-11-03，phase1-b77。
- 工作树：工作分支；paper：gk-2006-regular-fujian-science。
- 正式输出：2006_福建卷_理科/provenance.json（22题）。
- 固定来源：source ID src-ab0f2729ee4a24495e653b44c14438b4130f8b38b11362bf84251f3595a09d27；PDF SHA-256 50d17546b94af82fb2cee653942752914cd387fe72792d74ffa5f75e7a301d83。

## 三角色证据

- Question review：独立题面复核者按 PDF 第1–2页逐题核对文字、公式、选项与小问，22题均通过；逐题表见 reports/2006-fujian-science-question-review.md。该复核发生时 Q16/Q18/Q20 的图仍是图位，因此本记录没有把它算作图稿检查；这三题的后续图链、图源和渲染结果另见 reports/2006-fujian-science-figures.md。
- Answer solve：主会话据已核题面独立推导 Q1–Q22，指纹由 provenance.py 依据当前规范答案要点重算；固定 PDF 无答案页或评分标准，故所有题的 answer evidence grade 为 D，且均为非官方推导。答案记录见 reports/2006-fujian-science-answer-key.md。
- Answer review：两名独立盲核者分别覆盖 Q1–Q11、Q12–Q22，未读取答案稿；主会话逐题复算，最终均与答案要点一致。Q1 选项字母、Q17 单调区间端点表达、Q20 弦中点代数有过初稿差异，复核后标记 resolved；其他19题标记 none。详情见 reports/2006-fujian-science-answer-review.md。

三个角色标识两两不同。Q1–Q19 provenance 指向 PDF 第1页，Q20–Q22 指向第2页；每条记录绑定同一固定来源 ID、PDF SHA、当前题面块哈希与当前答案记录哈希。Q16/Q18/Q20 的题面块哈希包含图链，但题面文字/数学条件未因图稿阶段改写。

## 事务与验证

三份角色工作文档先由 init-batch 在 ignored .work/ocr-local/next-paper/phase1-b77/provenance/ 下创建；填入22题记录后，import-batch 无写入检查通过，再以一个状态事务写正式 provenance 与 manifest，revision 5973→5975。manifest CSV 随后由生成器同步到当前。

- provenance.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch phase1-b77：退出0，1卷通过。
- source_manifest.py validate --manifest source-manifest.json：退出0。
- manifest_csv.py --check：退出0，775行且 current。
- 派生状态：paper answers_verified，batch provenance_verified。正式 TeX、PDF 构建、receipt 和视觉复核尚未进行。

本阶段未触发 OCR 或外部模型调用；成本未知。source 身份仍只是本库候选 PDF 与卷的内部关系，发布者、出版者、版次、来源链和官方身份均未认证；official_answer=null。

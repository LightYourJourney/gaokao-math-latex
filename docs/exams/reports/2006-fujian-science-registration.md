# 2006 福建理科候选卷：paper/source 登记与规范源绑定

- 登记 paper `gk-2006-regular-fujian-science` 与批次 `phase1-b77`。`register-papers` 先以无写入模式核对成功，再以事务写入 manifest revision `5970→5971`；题量 22，卷种为理科，题面页为固定候选 PDF 第 1–2 页，答案页为空。
- 绑定 source `src-ab0f2729ee4a24495e653b44c14438b4130f8b38b11362bf84251f3595a09d27`，固定 PDF SHA-256 `50d17546b94af82fb2cee653942752914cd387fe72792d74ffa5f75e7a301d83`，Git blob `b05111b956dc556d6905036d1d5d0da3d9a9e5b3`。原 PDF 题签为“2006 普通高等学校招生考试（福建卷理）”，两页 A3 横向、印刷页 288–289。`canonical` 只记录本库中候选文件与该卷的对应关系，不代表发布者、出版者、版次、来源链或官方身份已经认证。
- 将三个事实源层 frontmatter 的 `paper_id` 统一绑定至新 ID，并用 `solution_sources.py extract-batch --write` 重新生成 `_含解析.md`。答案和解析仍明确为独立推导；`official_answer=null`。未发现需新增的逐题 blocker；paper 当前为 `planned`，batch 为 `planned`。
- 验证：`source_manifest.py validate` 退出 0；`issues.py validate --file missing-issues.md` 退出 0；`solution_sources.py check-batch --batch phase1-b77` 返回 1 卷、22 题全部通过；`manifest_csv.py --check` 确认投影 current、775 行。OCR `doctor` 现场显示 Xiaomi、Paddle、MinerU 均为 `ready`；本阶段没有重复推理。
- 本阶段未运行全库测试或构建。成本数据未知。尚待 Q16/Q18/Q20 题图、三角色逐题 provenance、项目 TeX、四版正式构建、视觉审查和批次回执；来源发布身份及答案官方性继续未核。

# 2004 春季北京文科：固定题源内部绑定与 Q20 阻断登记

日期：2026-10-28

## 来源判定

固定输入为 source `src-417d865aa928e69f32b3fcbc80abe4fa227259b79ababcce8765ea981117119b`，SHA-256 `4670b402354afd088d6993fbc473490158f27e232b1c54730e5989b64a21ec26`，Git blob `d402a6935a3251aa8f5a6f918f5c3144728e064f`，PDF 共2页，印刷页155–156，题签为“2004 年普通高等学校春季招生考试（北京卷文）”。该文件是 XeTeX 排印副本，不是原卷扫描。

本阶段将该固定副本绑定为本库内部 `canonical` 输入，表示本卷工作流选用这些固定字节；这不认证上游发布者、出版物、版次、来源链或官方身份。来源 PDF 不含答案页；答案与解析为本库独立推导、明确非官方，`official_answer=null`。

## 登记结果

- `source_manifest.py register-papers` dry-run 通过；单一事务写入后 manifest revision 为 `5302`（`5301 → 5302`）。
- paper：`gk-2004-spring-beijing-arts`；batch：`phase1-b52`；题量20；paper `blocked`，`blocked_from=planned`；batch `planned`。
- 题面页为 `[1,2]`，来源答案页为 `null`；题型结构登记为单选1–10、填空11–14、解答15–20。
- 两幅已有 TikZ 图迁入 `2004_春季北京文科/figures/` 并登记，各自在题面及含解析稿预期引用2次。规范含解析稿由题面、答案要点、解析正文确定性生成。
- 事务新增 `ISSUE-1238`，Q20：固定 PDF 第2页（印刷页156）尾问原文可辨为“计算公以及”。虽疑脱“式”，当前无可追溯勘误或同版异本可裁定；题面保持原文并注记疑点。issue 为 open / `blocks_completion`，整卷维持 blocked。

## 同步修订

题面、答案要点和解析正文 frontmatter 均关联 `paper_id: gk-2004-spring-beijing-arts`。题面来源说明区分本库内部固定输入绑定与来源认证；答案/解析继续说明为非官方独立推导。题面和图表清单更新为项目目录内图稿路径，图稿原内容未改。现有定向测试中关于“未绑定 paper_id”的断言更新为登记后的状态；按当前工作指令未运行测试套件。

## 阶段边界与验证

本阶段仅完成固定来源登记与 Q20 blocker 登记。尚未导入逐题 provenance、生成共享 TeX/简答与四版入口、正式 XeLaTeX 构建、渲染或逐页视觉验收；没有 build/review receipt。来源出版者、版次、来源链和官方答案身份继续未核。

登记 dry-run 与写入通过。`source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch --batch phase1-b52`、`report.py check --all` 和 `manifest_csv.py --check` 均通过；六个全量报告投影已刷新并回读，manifest CSV 为775行且当前。生成含解析稿时，首轮直接渲染未规范化解析锚点，被确定性检查发现；之后使用已登记批次的 `solution_sources.py extract-batch --write` 正常完成解析正文与含解析稿规范化，两份派生文件检查通过。

全量投影当前列出198个 `INVALID_OR_STALE` 复核门禁和3个 `VISUAL_FAILED`；build 与 review 各缺1份，缺项对应本次新登记、尚未编译的卷。本阶段没有重建或重新视觉审查其他纸卷 PDF，因此这些状态只反映当前 manifest/receipt 核验结果，不能解释为新的页面审查结论。

未运行测试套件、未调用 OCR 或外部 API。具体人工工时、Codex Token 与费用不可见，记未知。

## 可复核状态

- paper：`gk-2004-spring-beijing-arts`
- batch：`phase1-b52`
- blocker：`ISSUE-1238`
- manifest revision：`5302`
- 下一阶段：依据已有审题和盲解证据导入逐题 provenance，检查题面与答案哈希、source page 映射和图稿引用；随后生成共享 TeX、简答及四个独立入口。正式构建前继续保留 Q20 阻断。

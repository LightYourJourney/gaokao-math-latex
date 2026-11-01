# 2006 天津文科候选卷：规范源、paper/source 绑定与 Q14 问题登记

日期：2026-11-02。

## 状态变更

- 以固定 source `src-14a9fbe59a503a78a1e7f2d2cdf99e546574bda3fe11f37a5f17eaee39a4af70` 为本库 canonical 候选输入；SHA-256 `5500d9997d4710817516ad6d73104b93f1ac657dcf5a06a8d6b5717566dd98fa`。绑定仅指向固定字节，不认证题签以外的出版者、版次、来源链或官方身份。
- `source_manifest.py register-papers` 对 `gk-2006-regular-tianjin-arts` / `phase1-b66` 只读预检通过；写入 manifest revision `5758→5759`，source 反向绑定 `canonical`。卷含22题，题面页 PDF 1—2（印刷页338—339），答案页 `pages_s=null`。Q14 作为 `ISSUE-1287`（`answer-convention-ambiguous`、open / blocks_completion）原子登记，paper 进入 blocked。
- 规范源落地于 `2006/2006_数学真题_天津文_{试题,答案要点,解析正文,含解析}.md`。题面、答案与解析均声明非官方；`official_answer: null`。Q14答案保留 U；没有据单一题面推断、补写第二个圆方程。
- 三幅工作稿复制至 canonical `figures/` 目录，题面已映射 Q13、Q19、Q22，登记的 `expected_occurrences=2` 对应题面和确定性含解析稿各一处：
- `math-gaokao-latex/2006_天津卷_文科/figures/q13.tikz.tex`：SHA-256 `df90edb6e89b4bb503f687997098b542b0811f2caa880391ef9f99f18a327cda`。
- `math-gaokao-latex/2006_天津卷_文科/figures/q19.tikz.tex`：SHA-256 `7f3ad89d133916f9d79d3432b3251d422c6f556fca8458e0891945dea4a225e3`。
- `math-gaokao-latex/2006_天津卷_文科/figures/q22.tikz.tex`：SHA-256 `b8fde58703afdde71d4ede796d7f6532718ed0e93c3c14a6cfff8d9ebebbb008`。
- `solution_sources.py extract-batch --write` 已为 `phase1-b66` 写出两项派生目标；该阶段生成前曾按解析器错误提示去掉题目块外的重复尾注、补齐小问锚点并确保题面小问标号后有空格，未改变题目原意。

## 阶段边界与下一步

本阶段完成规范 Markdown、图稿映射与内部 paper/source/issue 登记。批次仍为 `planned`；三角色逐题 provenance、`index.json` / TeX、简答及版本入口壳、正式 PDF 构建、构建/视觉回执和页面复核尚未完成。Q14 blocker 保持打开。本阶段不表示本卷正式验收或全语料完成。

下一步：核对源文档解析结果，生成项目 TeX、简答和版本入口壳；随后完成三角色 provenance，再依据当前 manifest 输入构建和逐页视觉审查。

# 1989 广东文科候选卷：四版正式构建

日期：2026-10-30

## 构建结果

- 批次 `phase1-b59`，试卷 `gk-1989-regular-guangdong-arts`；正式构建 attempt `06a36244-5d74-4489-a485-35f38b76391a`，开始于 `2026-10-30T07:49:04+08:00`，结束于 `2026-10-30T07:49:14+08:00`。构建输入 manifest revision `5477`，当前 manifest revision `5478`。
- 构建工具链为 XeTeX / TeX Live 2026、latexmk 4.88、Poppler 26.10.0；完整指纹、输入树及 PDF SHA-256 由 `1989_广东卷_文科/receipts/build.json` 绑定记录。

- 试题版：6 页，SHA-256 `f5d741566bea5bb33afb3833a45a70e84ea7105edc9458bb0152bf1f5a87cf30`。
- 解析版：24 页，SHA-256 `e277929eb42fe65191a4cadf934bde72c52804aefd989060f0fa285b1b836a6b`。
- 简答版：8 页，SHA-256 `5cd46777b1d94bc217477716ed83c7a9193ccbb17c63879b8fa199805067b886`。
- 印刷版：19 页，SHA-256 `9021c717c74bd21bc7199a9b029b717cc2c37ad0aa01dbddcb37152cf40adbf7`。

- 四版均编译成功；错误、缺字、未解析引用和当前构建警告（Overfull）均为 0。`source_manifest.py validate`、`issues.py validate`、`provenance.py check-batch`（1卷）、三种生成器 `--check`、`solution_sources.py check-batch`（30题）、`manifest_csv.py --check`（775行）均通过。`validate-receipts --require-current-inputs` 返回 `OK`，缺失/无效/过期均为 0，尚有 1 个 review pending。
- 首次构建 attempt `df5e22a8-bc23-4187-976e-21675d0eb76a` 的简答版25列答案表出现 131.5708pt Overfull。已在 `make_short_answers.py` 为本卷登记13列拆表规则并重新生成 `answers_short.tex`；当前 PDF 显示为13+12两表，第二次构建无 Overfull。首轮 attempt 保留在 build receipt 的历史链中。

## 阶段边界

- 此记录只确认 TeX 四版正式构建成功。构建完成时的页面视觉审查尚未 finalize；后续阶段以同一 attempt、manifest/输入指纹、工具链指纹和 PDF SHA 为依据逐页审查，并生成 review receipt。
- 本候选卷的固定扫描 PDF 题签仅见“文史类”，年份、地区归属、出版者、版次和来源链仍未认证；`official_answer=null`。Q9 答案冲突、Q16 垂直约定及 Q21 源面无匹配选项仍阻断整卷完成；Q29（2）固定扫描未见最终解集，Q30解答未见于该扫描。
- 本阶段未运行测试套件；总耗时/成本未知。正式构建记录约10秒运行时间。

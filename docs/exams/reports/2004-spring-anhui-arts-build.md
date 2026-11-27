# 2004 春季安徽文科卷：TeX 文本修复与四版正式构建

日期：2026-10-27

- 根因是试题说明 prose 中行内代码 `paper_id` / `official_answer` 被 Markdown 转换器原样放入 `\texttt{}`，下划线触发 XeLaTeX `Missing $ inserted`。正文改为不带机器字段下划线的自然语言，front matter 字段保持不变；新增正文 inline-code 下划线回归断言。
- 定向转录与解答测试7/7通过，项目/简答/入口生成检查通过。
- 最新正式构建四版均 succeeded，页数为4/17/6/12；逐版 PDF SHA 与输入/工具链指纹记录在 build receipt。
- ISSUE-1212–1215 是失败构建自动登记且已由成功构建清除的非阻断项。ISSUE-1211 仍 open，Q18 欠定，paper 仍 blocked。后续视觉校样与批次收口待完成。

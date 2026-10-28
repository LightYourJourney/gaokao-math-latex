# phase1-b53：2009 春季上海卷四版正式构建

日期：2026-10-28

## 构建与输入绑定

- paper：`gk-2009-spring-shanghai`；batch：`phase1-b53`。
- 构建 attempt：`422df2e5-ccf1-4e71-9f56-bfedb978280a`；无前一正式attempt。起始manifest revision5306，running事务后回执记录输入revision5307，结果事务后revision5308。
- build receipt状态为`compiled_pending_review`；四版latexmk/XeLaTeX均succeeded。receipt绑定稳定manifest投影、generation input tree、最终.fls依赖树、工具链指纹与每份PDF SHA。输入投影：`df63394301890f07068f4c49ce126897a307b8944ed5e4a3a2df6cc3055f9e55`。
- PDF位于本卷`build/`，共44页。现场逐一重算SHA与回执一致；二进制PDF按既有规则留在忽略构建目录，不提交到Git。

| 版本 | 页数 | PDF SHA-256 |
| --- | ---: | --- |
| 试题版 | 5 | `0aed5b19750c98d0b910ec21f28d3af299f5976ef7ebb15d62d6b8c2282a44f3` |
| 解析版 | 18 | `14c98197d1931236fdc57e35db5ba497397ebab3001dbcd77e97d715920cbad4` |
| 简答版 | 7 | `2546408cffbc7cdd0dbec1184da4e982dea313e386d42d52b6f94a00c8d30577` |
| 印刷版 | 14 | `5ae8bf8bec0ea049125dea969f778e038511ec6896648a93f992836f0fa73343` |

## 日志与门禁

四版均无errors、missing_characters、undefined_references及Overfull。解析版有一条Underfull hbox（badness1838，answers.tex第396–397行），位于Q18第一次经过参数点的解释段；其余版无排版警告。首轮校样已定位解析版第15页：cos E的等号处分行，上一行字距偏松。警告未豁免；后续调整规范解析稿的段落后重建，再审查当前新attempt全部变化页。

构建前 `provenance check-batch`（20题）、`solution_sources check-batch`（20题）与三个生成器只读检查通过。正式构建后 `validate-receipts --require-current-inputs --json` 返回code=OK，failed/invalid/missing/running/stale均0，pending=1，problems为空；这只证明当前构建回执有效，尚未达到require-final视觉门。

## 当前边界

paper继续blocked，Q16的U级答案、未解决冲突与ISSUE-1239/ISSUE-1240仍保留；batch为compiled_pending_review。已准备绑定当前attempt的44页视觉工作骨架，尚未最终化视觉回执。

本阶段不改题面、答案、解析或图稿。来源出版者、版次、来源链及官方身份仍未核，official_answer=null。此前172项相关测试已通过，本次未重复运行测试套件。下一阶段逐页检查四版全部页面及八项视觉项目，定位Underfull，合格后办理review回执；Q16仍阻断整卷完成。本阶段不表示1952—2026题库完成。

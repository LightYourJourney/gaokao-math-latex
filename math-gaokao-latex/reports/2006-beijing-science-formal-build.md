# 2006 北京理科候选卷：四版正式构建

日期：2026-10-30

## 当前正式构建

- 当前 build attempt：c7eb4a45-455a-49ac-b4e4-02678eb9bf4b；前序 attempt：0e5ec32a-7461-4aa8-b116-e125ff89aa96。receipt 输入 manifest revision 为5501，构建完成后总账 revision 为5502；构建时间约8秒。
- 工具链为 TeX Live 2026、XeLaTeX、latexmk 与 Poppler。四版页数分别为：试题版5页、解析版19页、简答版7页、印刷版15页，共46页。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 5 | 4b06c459fadf3e6c6ba1cd99c6ebdcc2d918ceebfe9590720612a2bf0d1f9449 |
| 解析版 | 19 | 6a48f36bb455cd1519a0b53277b56584e3ed4d7ac4081be243e7eecc0a122989 |
| 简答版 | 7 | 295f86bfc73c5b11bff5abbb9926a9674e928b0c009ee8ab5e1a83ccb64c7dd8 |
| 印刷版 | 15 | 8672f5cfca9ed7a855b1f66984ad9a0e97253bcb6b64f99e299db2e1e173e945 |

- 四版构建结果均为 succeeded；errors、missing characters、overfull 与 undefined references 均为0。validate-receipts --require-current-inputs 返回 OK，当前 receipt 状态是 compiled_pending_review。
- 第一次正式构建 attempt ee722b21-675c-436a-9687-e98e714f367b 的解析版与印刷版各有30条缺字告警。逐项计数与解析正文显示公式内30个全角标点一一对应（13个逗号、17个句号）。已在规范解析源中删除这些公式行尾标点，重新生成后最终构建告警为0。中间 attempt 0e5ec32a-7461-4aa8-b116-e125ff89aa96 已由当前 attempt 取代；第一次警告构建不再是当前输出。

## 阶段边界

本阶段只完成四版正式构建与当前 build receipt，不表示视觉验收或整卷完成。试题、解析、简答、印刷四版全部46页及Q8/Q16/Q17图稿仍需逐页目视检查，并创建与本 attempt、输入 manifest revision、PDF 指纹及页数绑定的 review receipt。固定 PDF 的发布者、版次、来源链及官方身份仍未核；答案为本库非官方推导，official_answer=null。

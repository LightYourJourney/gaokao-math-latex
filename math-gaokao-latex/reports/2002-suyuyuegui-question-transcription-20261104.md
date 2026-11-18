# 2002 苏豫粤桂卷：Q1–Q22 题面转录

日期：2026-11-04

## 固定来源与路由

- 来源候选 `src-0daae2fa54742835e68d7f3b2cb647b26cee7c4d302f16958e53100e71e4bab4`，SHA-256 `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91`；两页 A3，印刷页 113–114，题签“2002 普通高等学校招生考试（苏豫粤桂）”。来源身份/发布链仍未核。
- `analyze_pdf.py --no-cache` 的两页结果均为 `text_candidate`、可疑字符数 0，文档级为 `text_layer_candidate`。按 `OCR_WORKFLOW.md`，此类已有文字层来源不自动重跑 OCR；本阶段 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 调用均为 0。文字层仅作定位。
- `local_ocr.py doctor` 显示 Xiaomi、Paddle、MinerU 三引擎部署资产均为 `ready`；该状态只确认资产可用，本阶段没有实际推理调用。Agent token/费用不可见，记未知。
- 对两页 180 dpi 整页图重新目视，并局部放大 Q10、Q12、Q17、Q19。图像结果保存在被忽略的 `.work/ocr-local/sources/2002-suyuyuegui/` 下，不入库。

## 转录内容与核查记录

- 转录阶段提交 `d7e68e0e` 时，题面草稿 SHA-256 为 `cc1fd8f2cf4fc703eeb93316f5ace88596ac782a3c1cffd01010c6bd36782730`；共覆盖选择 Q1–Q12、填空 Q13–Q16、解答 Q17–Q22。独立复核发现并补充了 Q10 选项图位置说明；修订后指纹与逐题结果见[独立复核报告](2002-suyuyuegui-question-review-20261104.md)。
- Q10 四个图形选项的圆、直线、坐标轴位置已在独立复核后分项补记；Q19 四棱锥示意图及 Q21 三个剪拼图记录原页图位和可见结构，均未代替矢量图稿；后续应以 PDF 原页重绘。
- Q12 原页可见引号内写作“十·五”，忠实照录；不根据上下文改成常见词形。Q14 指数确认是 7，不是 3。Q17 原页第二项为 $2b\overline z$，PDF 的文字层漏掉共轭横线；按局部放大原图录入。
- 首次转录阶段结束时，独立题面复核尚未进行；后续复核确认并修订 Q10 图位文字，最终题稿指纹见独立复核报告。未做数学求解或答案核验；没有答案/解析/评分页。来源仍 `ready/unbound`，`official_answer` 未认证。

## 本阶段边界

- 本稿是转录草稿，不代表独立题面复核、来源认证、答案验证或整卷完成；题图重绘、答案与解析、issues/provenance、paper/batch 登记、项目生成、正式构建和视觉回执均待后续。
- 未运行测试、OCR或构建。本阶段仅新增题面草稿与本报告，并更新 `PROGRESS.md` 和交接文档；未修改 source manifest 或问题总账。

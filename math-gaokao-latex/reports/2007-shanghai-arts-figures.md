# 2007 上海文科候选卷：题图重绘、provenance 与项目生成

- 日期：2026-11-03。
- Paper：`gk-2007-regular-shanghai-arts`；batch：`phase1-b83`。
- 固定输入：source `src-51aa9840dc7a866be37ded966d4a337c999cacd912ce0118e07b3e6c768c5789`，PDF SHA-256 `1d43489e28ce9c305faa753519800b9184e40cc40fbd8343f7fd287b4ec70212`。PDF 仅含题面；Q1–Q18 在 PDF 第 1 页（印刷页407），Q19–Q21 在第 2 页（印刷页408）。来源发布者、版次、复制链和官方身份未核。

## 图稿

四份 TikZ 文件均按固定 PDF 的对应题图重绘。SHA-256：

| 题号 | 文件 | SHA-256 | 图形记录 |
|---|---|---|---|
| Q7 | `2007_上海卷_文科/figures/f2007_shanghai_arts_q07_triangular_prism.tex` | `a431258ef8b17578901253792f049fbae643f300714e8585ed5836c42a25c2db` | 保留直三棱柱顶点、斜线 $A_1B$、$C$ 处直角符号；隐藏底棱和后侧棱用虚线，直角符号用实线。 |
| Q11 | `2007_上海卷_文科/figures/f2007_shanghai_arts_q11_equal_tangent_circles.tex` | `b8dce3521445df726df60312f9c844f2884dd52494cef447f832c71f1988ad8c` | 保留直线 $l$、切点 $A,B$ 和在 $C$ 相接的对称弧形。曲线按源图作示意，不用于测量半径。 |
| Q16 | `2007_上海卷_文科/figures/f2007_shanghai_arts_q16_square_pyramid.tex` | `1e2f81450b8c4414831677583e7b1652f3714fe4c46f220dd2a9f21c9b99c0a4` | 保留正四棱锥顶点及底面关系；不可见底棱和棱 $PD$ 用虚线，$D$ 标签与棱线分开。 |
| Q21 | `2007_上海卷_文科/figures/f2007_shanghai_arts_q21_pear_curve.tex` | `5eab7ed07d2953179ce3cb8c4c6b59de40620016c70f6ad09dc5c8d6679217c4` | 用两段半椭圆表示果圆，标示坐标轴、$A_1,A_2,B_1,B_2,O,M,F_0,F_1,F_2$；示意参数不代表题设数值。 |

原页渲染与图形裁片保存在忽略目录 `.work/ocr-local/2007-shanghai-arts/` 和 `.work/phase1-b83/figure-review/source-crops/`。四份独立预览在 `.work/phase1-b83/figure-review/build/` 使用 XeLaTeX 编译成功，各输出 1 页；转为 180 dpi PNG 后逐张目视检查，Q7 另以 600 dpi 检查直角符号。检查发现并修正了 Q11 初版弧线的小环、Q21 的 $A_1/A_2$ 轴线间距、Q16 的 $D$ 标签间距，以及 Q7 直角符号的线型。最终预览 PNG SHA-256 依次为 `de5abed1146d0fd63562918160457e0a66edde1194ac95793a3830bd2325d47c`、`b33eb727a5aed4c9dd71e45442aaea61eb94db01c6c6e4f067844d3a3a2b428a`、`2bd2f024a70d4c28f09e85d8838558f946f6b4efbb56ccad3b2cbab3ad3cadf4`、`9fbbf617485510930b69e06401cffbfbb664123e887166d5eafb6cd95eb38196`。

## 映射、provenance 与生成

- 规范题面中的四处占位替换为独立段落 TikZ 链接；解析正文和答案事实未因图稿而改写。运行 `solution_sources.py extract-batch --manifest source-manifest.json --batch phase1-b83 --write` 重建确定性 `_含解析.md`。`source_manifest.py sync-figure-registry --paper gk-2007-regular-shanghai-arts --write` 登记四张图，每张在规范题面与合成稿中各出现 2 次。
- 更新 manifest 索引注记，说明图稿已重绘、正式版构建和视觉回执仍待完成。答案要点的标题规范为「答案速查表」，并补上 Q12–Q15 的独立字母行 A、C、B、D；逐题答案与答案值未变。此表用于 `make_short_answers.py` 的第三路一致性校验。
- 更新 Q7、Q11、Q16、Q21 的题面哈希及图稿证据。answer-solve 证据记录对应 TikZ 路径和 SHA；Q21 仍保留 U/PENDING 与 ISSUE-1362，不用示意图裁定参数作用域。
- 最终 provenance 事务 `f5b20be7-5ff4-4d5b-ba81-5edbc30473f2` 将 manifest revision 更新至 `6054`，当前 provenance SHA-256 为 `7e67dfa387ea06fbded3ec71addfa8f1aa53b1040595965265c136c7fe9b70d5`。paper 仍为 `blocked`，batch 为 `provenance_verified`，`official_answer=null`。
- 已生成并核对项目 `questions.tex`、`answers.tex`、`answers_short.tex` 与四版入口。以下定向检查通过：`solution_sources.py check-batch`（21题）、`provenance.py check-batch`（1卷）、`source_manifest.py validate`、`issues.py validate`、三类项目生成器的 `--check`、`manifest_csv.py --check`（775行且 current）及 `git diff --check`。未运行测试套件。

## 阶段边界

当前视觉证据只覆盖四张独立图稿预览，不覆盖题面/解析版式中的图文分页、图中文字大小或整页布局；尚未运行正式四版 PDF 构建，也没有 build/review receipt。下一阶段执行正式构建并逐页视觉检查。Q21(3) 的参数作用域问题 `ISSUE-1362` 仍 open / `blocks_completion`；来源身份未核，官方答案仍为 null。本阶段不表示本卷闭环或长期语料完成。

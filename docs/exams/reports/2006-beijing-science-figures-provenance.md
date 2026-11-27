# 2006 北京理科候选卷：Q8/Q16/Q17 图稿与逐题 provenance

日期：2026-10-30

## 图稿来源与映射

- 固定输入为 `src-49f52e7c83c2b20d33f62d6dbc57b1610f96cf9de81c5743d41612834cb318de`，SHA-256 `878cd3b020d41450cb9876ad9263ec384840bb4c00597e720069a12f89d2016c`。本次目视查看 PDF 第1页（印刷页280）原图；PDF为2页A3横向。该固定副本的发布者、版次、来源链和官方身份仍未认证。
- Q8 按源图重绘三岔路口环岛，保留 A/B/C、x1/x2/x3、50/55/20/30/30/35 六处外部流量及箭头方向。题图外部流量与2006北京文科卷图相同，文件单独归档在理科项目目录并绑定理科 source 页码。
- Q16 按源图重绘坐标轴、原点、根1/2及向上开口曲线；曲线仅表达形状与根，不标作按比例图。
- Q17 新绘 P-ABCD 四棱锥、PD 中点E、题图底面隐藏边/对角线、PA及辅助线EC/EA，按原图保留虚实线；明确声明非比例图。图中没有补入源图未标示的长度或角度标记。
- 三个 TikZ 文件分别位于 `2006_北京卷_理科/figures/`。规范题面以独立本地 `.tex` 链接引用；确定性生成器根据这些链接将图稿映射到 `questions.tex` 和 `answers.tex`。`sync-figure-registry` 按实际源文件/派生 Markdown 引用登记每图 `expected_occurrences=2`，不是手填次数。

## 逐题 provenance 与状态

- `provenance.py import-batch` 导入20题三角色记录：独立题面复核、主解题推导、第二解题者复算。题面 Q18（1）漏“时”已按固定 PDF订正；其他题未发现文字/公式/选项差异。所有答案证据为本库 D 级非官方推导，`official_answer=null`。
- 第二解题者此前读过进度摘要中的 Q8、Q17答案结论，因此这两题记录为非盲复核；其余题未从本卷答案稿获知结论。矢量图本身目前只有源页定位对照，尚无独立第二读者专项图稿审查。
- figure registry 在 manifest revision `5492→5493` 登记三图；provenance 导入使 revision `5493→5494`，当前 paper=`editions_generated`、batch=`provenance_verified`；随后 index note 事务 `b4d36cbe-a658-4688-b340-73382f1a6680` 将 revision `5494→5495`。

## 校验与阶段边界

图稿链接、manifest 登记、三角色 provenance 和 TeX 输出已同步。三份 TikZ 源分别经临时 XeLaTeX wrapper 编译为单图预览，并检查可读性、标签和图形关系；这不代表正式版面验收。本阶段未构建试题版、解析版、简答版或印刷版 PDF，未创建 build/review receipt，也未运行测试。下一阶段需构建四版、检查每页版面与三幅图形，并保存当前输入对应的回执；来源身份不确定性继续保留。

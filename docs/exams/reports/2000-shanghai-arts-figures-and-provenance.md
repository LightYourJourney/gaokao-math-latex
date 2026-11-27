# 2000 上海文科候选卷：四幅题图矢量重绘与 provenance

- 日期：2026-11-03。固定来源 `src-8d14b1f9f511665ea10dbda45959a3b445a17806415be6b034f816bec663d7f5`，PDF SHA-256 `35e5d6f6bf052fcd9a2b91a1aa4215766fd4121425cfec7a62cfc4cdc7ab02a1`；Q8、Q11、Q18 在 PDF 第1页（印刷页72），Q20 在 PDF 第2页（印刷页73）。
- 新增四个 TikZ 矢量源：Q8 `f2000_shanghai_arts_q08_graph.tex`；Q11 `f2000_shanghai_arts_q11_linear_programming.tex`；Q18 `f2000_shanghai_arts_q18_tetrahedron.tex`；Q20 `f2000_shanghai_arts_q20_robot_axes.tex`。文件头均记录 source ID、PDF SHA、PDF 页与印刷页。

## 原页对照与矢量范围

| 题号 | 按固定原页保留的事实 | 未加入的图面信息 |
|---|---|---|
| Q8 | 坐标轴 O、x、y；刻度 1、2；线段 A(0,2)–B(1,1) 与端点标签。 | 不外推线段区间外的函数图像，不添加点标记。 |
| Q11 | 两条下降边界线、第一象限阴影四边形及标签 (1,4)；可行域顶点为 (0,0)、(0,5)、(1,4)、(3,0)。 | 不添加原图没有的顶点标签或点标记；(1,4) 标签不代表目标函数最大点。 |
| Q18 | 四面体 A、B、C、D，E 位于 AC；实线为 CA、CD、DA，虚线为 CB、BA、BD、BE。 | 不依据示意图透视推断长度、角度或垂直关系；不添加点标记。 |
| Q20 | 坐标轴 O、x、y 与 x=4、x=17、y=4 三处刻度。 | 不添加机器人、小球、起点、路径或运动方向。 |

Q11 原图核查报告的首稿曾把可行域误称为三角形。本阶段按原图阴影、两条约束直线和第一象限边界更正为四边形；题目文字及不等式未改。源图边界细节见[原图核查报告](2000-shanghai-arts-figure-source-review.md)。

四幅图先以单独预览 wrapper 使用 XeLaTeX 编译为 4 页 PDF，再以 Poppler 180 dpi 渲染并逐页与固定原页及局部图像目视对照。四页均编译成功；端点、边界、虚实线、坐标刻度、标记文字均与上述源事实一致，未见标签重叠或裁切。最终复核重渲染与先前逐页检查图像字节一致。忽略目录预览文件为 `.work/ocr-local/2000-shanghai-arts-figure-preview.pdf`，SHA-256 `74e39e822c96fe746e3b261903cd24fa00ec4434823d5a400af27586c8f82038`；它只用于核图，不是正式试卷 PDF 或构建回执。

## 规范源、登记与逐题 provenance

- 在规范题面中用独立段落链接到四个 `.tex`；`solution_sources.py extract-batch --write` 重建 `_含解析.md`。四幅图各在题面与合并稿出现一次。
- `sync-figure-registry --write` 将四项登记到 manifest，expected occurrences 均为 2，revision `6067→6068`。`generate_projects.py --write` 同步题面 TeX、答案 TeX 与 `index.json`；简答及四版入口校验无内容变化。随后三角色 provenance dry-run 和导入通过，revision `6068→6069`；`manifest.csv` 按新 manifest 投影为 current（775 行）。
- `phase3-b25` 的 Q1–Q22 provenance 已导入：题面复核 22/22 passed；答案证据为 D 级 21 题、U 级 1 题。Q21 三问仍为 U/PENDING，冲突状态 unresolved；`ISSUE-1363`（answer-conflict）与 `ISSUE-1364`（answer-convention-ambiguous）均保持 open / blocks_completion。后者记录固定印式与同期未认证、未证同版副本造成的指数变量及预期答案约定不明。`official_answer=null`，paper 仍为 blocked，batch 状态为 provenance_verified。
- Q1–Q20、Q22 的答案和解析仍是本库独立推导、非官方内容；固定 PDF 只含题面，出版者、版本、复制链和官方身份未核。

## 本阶段验证

- XeLaTeX 4 页图稿预览构建成功，Poppler 180 dpi 页面全部目视检查。
- `solution_sources.py check-batch --manifest source-manifest.json --batch phase3-b25`：22 题通过。
- `source_manifest.py validate --manifest source-manifest.json`、`issues.py validate --file missing-issues.md`、`provenance.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch phase3-b25`：通过。
- `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`：本卷生成结果均与规范源/模板一致。
- `manifest_csv.py --check`：775 行 current。
- 本阶段未运行 OCR 推理、测试套件、四版正式试卷构建或视觉回执。OCR/API 调用为 0；耗时与费用未测。

## 未完成项

Q21 的来源/答案约定冲突仍阻止本卷完成；需取得能绑定到本卷版本的原始出版页、正式答案或勘误后再裁定。四版正式 PDF 构建、逐页视觉检查和正式回执仍待后续阶段。本报告仅记录 2000 上海文科候选卷本阶段图稿与 provenance，不表示该卷整体闭环或 1952–2026 语料完成。

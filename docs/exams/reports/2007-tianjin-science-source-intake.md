# 2007 年天津卷理科数学来源接收报告

状态：`pending`。本报告只固定来源字节与版式，不代表题面、解答、图稿或四版验收完成。

## 1. 固定来源

| 项 | 值 |
|---|---|
| source_id | `src-48d8d69d7573bbc8e32736c808a5f8830a7e9e1d4ebe39b164da68c578e5e3a1` |
| 上游路径 | `普通高考/2007/2007天津理.pdf` |
| SHA-256 | `292db7ce8ca498293125ba6cdb90e0b2c4e41626fe2027f675c7c52b364944df` |
| 字节数 | 512,499 |
| Git blob OID | `4322387bdf7ae7338f8825d909b06508bfb0548d`（manifest 记录与本机 `git hash-object` 实测一致） |
| 页数 / 版面 | 2 页，1190.55 × 841.89 pt（A3 横向排印） |
| 印刷页码 | 413、414 |
| 题签 | 「2007 普通高等学校招生考试（天津卷理）」 |
| 来源状态 | `ready`，`paper_id=null`（尚未登记） |
| 考试类型 / 科类 | `regular` / `track=null`（上游文件名标“理”，登记时按理科绑定） |

上游 checkout HEAD 实测 `657e35f015766b0da12a281a0c99969626e1797b`；manifest 的 `artifact.page_count=2`、`size_bytes=512499` 与本机 `pdfinfo` 一致。发布者、出版者、版次、扫描/重排链与官方身份均未核。

## 2. 卷面结构与页映射

- 全卷 22 题：选择题 1–10，填空题 11–16，解答题 17–22。原件**不印各题分值，也没有答案、解析或评分标准**；不补分值。
- 第 1 页：Q1–Q8（左栏）、Q9–Q17（中栏，含填空 Q11–16 与解答 Q17）、Q18–Q19（右栏，含 Q19 四棱锥图）。
- 第 2 页：Q20–Q22（三栏各一题）。

## 3. 图形清单（需 TikZ 矢量重绘）

| 题号 | 内容 | 目标文件 |
|---|---|---|
| Q15 | △ABC，D 在 BC 上且 DC=2BD，连 AD | `figures/f2007_tianjin_science_q15_triangle.tex` |
| Q16 | 横向 4 格涂色条 | `figures/f2007_tianjin_science_q16_grid.tex` |
| Q19 | 四棱锥 P–ABCD，E 为 PC 中点 | `figures/f2007_tianjin_science_q19_pyramid.tex` |

原页无函数图象、无立体三视图、无程序框图。Q4/Q9 的曲线只以文字描述，不需要图。

## 4. 文字层质量

`pdftotext -layout` 可抽出正文，但阅读顺序按排版框乱序（如 Q9 的公式被拆到三栏顶部），且上下标、根号、向量箭头有抽取缺陷；转录以 180/300 dpi 页面渲染图为准，文字层仅用于定位。

## 5. 后续门禁（未完成）

1. 逐题题面转录与主代理逐题核对（候选稿在 `.work/phase5-b02/2007-tianjin-science/`）。
2. 独立求解 + 答案复核；原卷无答案，全部标非官方独立推导，`official_answer=null`。
3. 三幅 TikZ 图重绘并编译目检。
4. 登记 source→paper（`gk-2007-regular-tianjin-science`）与 batch，三角色 provenance。
5. 生成 `questions.tex`/`answers.tex`/`answers_short.tex` 与四版入口，正式构建、逐页视觉审查、回执当前性验证、finalize。
6. 全量报告与 `manifest.csv` 刷新后才可把本卷状态从 `pending`/`blocked` 改为 `complete`。

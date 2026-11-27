# 2006 安徽卷理：题图登记、paper/source 与逐题 provenance

日期：2026-10-28

## 内部登记与来源边界

- 候选卷 `gk-2006-regular-anhui-science` 登记入 `phase1-b46`。固定来源 `src-3aed0bc3d5875c8ce734b5b97f95992307ff56fc580067083caea214e3028675` 的 PDF SHA-256 为 `dfdf163d47fa3f279288d7000e2dfb729c7d412c64f4aa3b082d242f6ca2b093`，Git blob 为 `5a7adad2311c8cb9af246aee962060f0f8785e53`；source manifest revision `5235 → 5239`。
- 内部 canonical 绑定只说明本库选用该固定副本，不认证发布者、版次、来源链或官方原件。固定 PDF 两页，题签自称“2006 普通高等学校招生考试（安徽卷理）”，页码276–277；没有答案或解析页，`official_answer=null`。
- Q3 原印只见 `x^2/6 + y^2/2`，无等号及右侧，照录且不补写。创建并保持开放阻断 `ISSUE-1219`（答案缺失），答案要点与 provenance 均为 `U/PENDING`。paper 当前 `blocked`，batch 当前 `provenance_verified`。
- 注册器初建问题记录时采用 `q3`，而 provenance 规范 ID 为 `q03`。在导入前通过 state transaction 将 ISSUE-1219 的 question_id 校正为 `q03` 并重算 fingerprint，保留 issue ID、证据和开放状态；相关事务后 manifest revision 为5238。

## 四幅矢量题图

题面与确定性含解析稿都用普通 Markdown 链接映射到本卷 TikZ 源。manifest `figure_files` 每图记录 `expected_occurrences=2`：

| 题号 / 源页 | TikZ 源 | SHA-256 |
|---|---|---|
| Q6 / PDF第1页 | `2006_安徽卷_理科/figures/f2006_anhui_science_q06_sine.tex` | `ba3ff3c339a6fe43415f18729602d67e69e919b1c40dcf71c35484cf648f97ae` |
| Q16 / PDF第1页 | `2006_安徽卷_理科/figures/f2006_anhui_science_q16_cube_plane.tex` | `ef4b016a95956039f3f50f7d265c9a30949566ff78bb9c876524ececbc21bd55` |
| Q19 / PDF第2页 | `2006_安徽卷_理科/figures/f2006_anhui_science_q19_hexagon.tex` | `1e6a556edc7749f84e6a96ac1df3322d955e59e8869c135c22c37bf84f4ec911` |
| Q22 / PDF第2页 | `2006_安徽卷_理科/figures/f2006_anhui_science_q22_hyperbola.tex` | `259c2ba232268a4f62b4923043080d79db5640140f77dae17ec0293274f448c4` |

四个 TikZ 源均已单独编译到 `/private/tmp/gaokao-2006-anhui-science-figures/main.pdf`，4页；`pdfimages -list` 无图像对象，确认预览 PDF 不嵌入栅格图。四页临时图稿预览已逐张目视检查并与固定 PDF 对应题图复核；这不是正式四版页面验收。Q16 的透视位置及 Q19 的仿射投影按示意绘制，没有题设尺寸标记；Q22 的坐标取满足所述关系的示意构型，未把参数值印入题图。

## 规范源、生成器与逐题来源核验

- 用项目 `solution_sources.render_combined()` 从题面、答案要点、解析正文确定性生成含解析稿；`solution_sources check-batch` 确认22题及小问集合逐题对齐。Q3答案解析为显式 `U/PENDING`。
- `sync-figure-registry` 干跑确认四条链接和目录闭合后，以项目 state transaction 登记四图。`generate_projects.py --write` 更新共享 `questions.tex`、`answers.tex` 与全卷 `index.json`；随后 `--check` 返回1套试卷与生成结果一致。
- 导入22题三角色 provenance：题面复核均为 `passed`，Q1–Q18来源页为1，Q19–Q22来源页为2；21题答案证据为项目独立推导D级并经第二位盲算者逐题核对，Q3为U级，关联 ISSUE-1219。Q19按包含A、D的两个半平面给出推导，同时保留取两平面较小角时为补角的约定说明。
- `source_manifest.py validate`、`issues.py validate`、`solution_sources.py check-batch` 与 `provenance.py check-batch` 均通过；provenance 检查返回 `OK：1 卷`。本阶段没有运行测试套件。

## 尚未完成

四版入口、正式四版构建回执及逐页视觉审查均未生成。本批尚未完成；Q3 的原印缺式和答案阻断继续开放。固定副本身份仍未经认证，任何独立解答都不是官方答案。本报告不代表1952–2026题库完成。下一步按当前 manifest 与项目工具生成四版入口，再构建、复核并记录回执；Q3 继续标为 `U/PENDING`。

# 2026 北京回忆版候选卷：Q10/Q14/Q18 题图重绘与登记

- 日期：2026-11-04。
- worktree：`仓库根`；分支：工作分支。
- paper/batch：`gk-2026-regular-beijing-recall` / `phase4-b49`。
- 固定只读来源：`src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee`；PDF SHA-256 `7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9`；Git blob `cf49aa3671ff4143e5c665c7bc53b5f08ab38fca`；365585 字节、5 页。首页自称回忆版；发布者、版次、复制链与官方身份仍未核，`official_answer=null`。

## 图稿与原页核对

| 题号 | 固定 PDF 页 | 图稿 | 图稿 SHA-256 |
|---|---:|---|---|
| Q10 | 2 | `2026_北京卷_回忆版/figures/f2026_beijing_recall_q10_fourbar_linkage.tex` | `a036339debed625516b8140161b76614bf77f1f0040f440fa030954c303652eb` |
| Q14 | 2 | `2026_北京卷_回忆版/figures/f2026_beijing_recall_q14_tetrahedron.tex` | `b1b5e6036587fb61a25785485f812e94e403e1930970628485bd3e0a615cf866` |
| Q18 | 3 | `2026_北京卷_回忆版/figures/f2026_beijing_recall_q18_triangular_prism.tex` | `b863e9faa26365491a467880d031fbc24e7a615506ae64343e1c205e9771b622` |

- 三份 TikZ 文件都记录 generator、source ID、固定 PDF SHA、页码与题号。Q10 保留 `A-D-C-B-A` 四杆轮廓和以 A 为视觉中心的完整圆，不把圆标成完整可达轨迹；Q14 仅 DC 为虚线；Q18 按来源画出三棱柱的可见/隐藏棱及 EP、ED、PD 辅助线。所有投影比例仅作示意；没有从图形补入长度、角度或垂直事实。
- 固定源 PDF 只读检查并以 300 DPI 渲染第2、3页；图稿通过 XeLaTeX 生成 3 页局部预览，逐图与源页目视对照。预览 PDF SHA-256 为 `4cd4ea62fba5dfdacebdc8e17be78ca38c4ceeaaa4bf0a666c1ee99176bbce1a`，连同源页 PNG 和编译日志保存在忽略目录 `.work/ocr-local/2026-beijing-recall/figure-preview/`。预览仅核对图稿局部线型、标签与拓扑，不是正式卷版面校样。

## 确定性接入与问题状态

- 规范题面 `_试题.md` 中三个占位均改为独立段落的 TikZ 文件链接；运行 `solution_sources.py extract-batch --manifest source-manifest.json --batch phase4-b49 --write` 刷新含解析稿。
- `source_manifest.py sync-figure-registry --manifest source-manifest.json --paper gk-2026-regular-beijing-recall --write` 登记三图，manifest revision `6160→6161`，每图 `expected_occurrences=2`。随后 `generate_projects.py --manifest source-manifest.json --batch phase4-b49 --write` 更新 `questions.tex`、`answers.tex` 与共享 `index.json`；每张图在题目和答案 TeX 中各出现一次。未新增静态生成器例外，映射由规范 Markdown 图链和 `figure_files` 派生。
- `ISSUE-1411`、`ISSUE-1412`、`ISSUE-1413` 已保留记录并改为 resolved。Q10 选项异文 `ISSUE-1408`、Q13 端点异文 `ISSUE-1409`、Q15 陈述顺序异文 `ISSUE-1410`、Q18(2) 条件③不唯一 `ISSUE-1414` 继续 open / `blocks_completion`；对应答案和来源判断不变。
- paper 仍为 `blocked`（`blocked_from=planned`），batch 仍为 `planned`。下一阶段导入逐题三角色 provenance；之后再生成简答和四版入口、正式构建及逐页视觉检查。来源身份和官方答案状态未改变。

## 检查记录

- `source_manifest.py validate --manifest source-manifest.json`：通过。
- `issues.py validate --file missing-issues.md`：通过。
- `solution_sources.py check-batch --manifest source-manifest.json --batch phase4-b49`：21 题通过。
- `generate_projects.py --manifest source-manifest.json --batch phase4-b49 --check`：1 卷生成结果一致。
- `manifest_csv.py --check`（从仓库根目录运行）：通过，775 行。
- `git diff --cached --check` 仅提示新生成 `questions.tex` 的21个 `\gkti{N}` 页码标题行有行末空格。源 Markdown 行无尾随空格；固定 Markdown 转换器在 `md2tex.py` 第681行于加粗页码标签后明确输出分隔空格。为保持生成物与当前转换器一致，没有手改 TeX 或扩大到全库的转换器重写。其余暂存内容无空白问题。
- 未运行测试套件或 OCR；未构建正式卷 PDF，未建立 build/review receipt。

本阶段只完成题图矢量重绘、源页目视核对和确定性登记，不表示候选卷完成、来源认证或长期语料库完成。

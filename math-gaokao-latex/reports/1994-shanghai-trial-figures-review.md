# 1994 上海试点教材文理卷：TikZ 图稿及 provenance 阶段复核（2026-10-26）

## 范围与结果

`phase1-b36` 两卷各补齐 Q11、Q23、Q24 三幅 TikZ 图。题面 Markdown 对各图均有明确相对路径映射；source manifest 的 `figure_files` 各登记三项、每项 `expected_occurrences=2`。`generate_projects.py` 已为两卷生成题面/答案 TeX、项目索引、简答稿和四版壳。

固定来源仍为文科 PDF SHA-256 `86d8bc7b9f5eb467d29f09bf1963eba0075fccc0ba4359e714549fed6f69c488`（Q11 第1页、Q23 第3页、Q24 第3页），理科 PDF SHA-256 `b7582351e09479e49306f4b59ee118955ad716fdde093f49f1f9ac3de8ee6234`（Q11 第1页、Q23/Q24 第2页）。来源没有 PDF 文字层，未使用 OCR。图稿重绘遵循原图拓扑和选项排列：文科 Q11 横向四图，理科 Q11 二乘二；Q23保留棱柱/棱锥相对位置和虚实线；Q24绘制原题双抛物线、切点和切线。图稿不补充题目未给出的尺寸或结论。

## 文件校验与视觉检查

六个 TikZ 源文件 SHA-256：

- 文科 Q11 `f1994_shanghai_trial_arts_q11_graph_options.tex`：`0c9ed5f5ca3581bc36e969da4e6ce35fc87b12d7157641e638364d59158c3bb9`
- 文科 Q23 `f1994_shanghai_trial_arts_q23_trapezoid_pyramid.tex`：`13a3719cb81789384458af2ac0ead210dcfa08a7dd180a570f8ce19ba795b413`
- 文科 Q24 `f1994_shanghai_trial_arts_q24_parabolas.tex`：`328826af51165fe1fe071abeae0c119b835cc09fb045f967de7863d9cc62c550`
- 理科 Q11 `f1994_shanghai_trial_science_q11_graph_options.tex`：`3503b8dd5b77e0a1dd2a32d2c83cfea51da78b2c6c60c466170af4d9817cc418`
- 理科 Q23 `f1994_shanghai_trial_science_q23_trapezoid_pyramid.tex`：`4394cd642ebe1828373d3b48fe9ce18c9747d3f1bd8c65f6e4f773889caf61ec`
- 理科 Q24 `f1994_shanghai_trial_science_q24_parabolas.tex`：`328826af51165fe1fe071abeae0c119b835cc09fb045f967de7863d9cc62c550`

XeLaTeX smoke 文件 `.work/phase1-b36/figures-smoke.pdf` 共6页，SHA-256 `d737ef639c4af283532bfb582172f9c4445b6ab6715e70ee33e42e119d53bf86`。六页逐张目视：文理 Q11、Q23、Q24 均无裁切、标签遮挡或线型丢失，页面上的图形关系清晰。该 PDF 只验证 TikZ 图稿可编译并供本轮图形检查，不是正式试题版/解析版/简答版/印刷版的 build receipt，也不代替后续四版校样。

## provenance 与盲核差异

两卷三角色、每卷26题 provenance 于 manifest revision 5099 导入，`provenance.py check-batch` 返回 `OK：2 卷`。逐题记录固定来源 SHA、页码、题面块/答案哈希和证据。答案等级 C 仅指固定副本卷内答案，出版者、版次、官方性仍未核实。

- 文科 Q11：旧盲核因题稿缺图未判字母；补图后主会话依据固定源图复核为 B。
- 文科 Q14：盲核称 A/D 也可能成立，反例分析不成立；唯一必真项 C。
- 文科 Q23：盲核建议点位不在 BC；结合源图与条件得 `C=(a,0)`。源图题干为 `PA=a`，见 `1994-shanghai-trial-arts-math-review.md`。
- 理科 Q11：旧盲核因缺图未判字母；补图后主会话依据固定源图复核为 B。
- 理科 Q22：盲核点积漏一次项；根审复算 `2k^2+k-10=0`，得 `k=-5/2,2`，与卷内答案相符。

## 阶段门禁

- `solution_sources.py extract-batch --write` 规范化两份解析正文并重建含解析；随后 `check-batch`：2卷、26题/卷全部通过。
- `provenance.py check-batch`：2卷通过。
- `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`：均2卷通过。
- `source_manifest.py validate`、`git diff --check`：退出码0。
- 本阶段完成图稿、引用、索引、provenance 与确定性入口生成；尚未做四版正式构建、正式回执、整卷逐页八项视觉审阅或批次 finalize。

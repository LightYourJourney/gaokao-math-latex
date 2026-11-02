---
title: 2006 江西、浙江、湖北理科候选卷题图与正式构建阶段记录
date: 2026-11-02
batch_id: phase1-b70
manifest_revision_at_build: 5889
manifest_revision_current: 5890
status: compiled_pending_visual_review
---

# 2006 江西、浙江、湖北理科：题图与四版正式构建

## 范围与来源边界

本阶段覆盖三份绑定到 `phase1-b70` 的固定候选 PDF。固定 PDF 的 SHA-256 与 source manifest 登记相符，但指纹只绑定这些副本字节，不认证发布者、版次、扫描链或官方身份。三卷均无可见官方答案/评分页，`official_answer` 继续为 null；答案是独立推导草稿。湖北 Q17（2）保持 U/PENDING，ISSUE-1319 与 ISSUE-1320 继续 open 且阻断完成。

## 题图登记

- 江西：Q11 四面体、Q12 气温与选项图、Q15 直三棱柱、Q19 三角形截面、Q20 三棱锥、Q21 椭圆弦。
- 浙江：Q9 球面大圆弧、Q14 正四面体投影、Q15 正弦曲线、Q17 四棱锥、Q19 椭圆切线、Q20 曲线和切线。
- 湖北：Q15 莱布尼茨三角形示例、Q18 正方体。Q18 源图未标 P，图稿不补点。

14 个 TikZ 文件、题面 Markdown 映射及 manifest `figure_files` 已一起更新。未标尺寸的空间关系和曲线仅作示意。

## 答案速查更正

生成简答表时检查器发现江西 Q6 速查项误抄为 `②④`，与逐题答案冲突。复核题面 $x^2+ax+1\\ge 0$ 对所有 $x\\in(0,1/2]$ 成立；因 $x>0$ 等价于 $a\\ge -x-1/x$，右端在该区间最大值为 $-5/2$，故最小 $a=-5/2$，选项 C。原逐题推导已是 C，仅速查表误录。江西 Q3 速查字母也由 A 改为 D，与逐题答案和解析一致。更改后的哈希已同步到 provenance。

## 确定性检查

以下定向检查通过：provenance batch、题面/答案投影、简答表、四版入口壳、规范解析源（22/20/21 题）、source manifest 与 issues ledger。三卷 question-review、answer-solve、answer-review provenance 重新导入后检查通过。

## 正式构建回执

最新构建输入 manifest revision 为 5889，当前 manifest revision 为 5890；前一次 attempt 因文档输入修改而被 supersede，现用 attempt 重新构建并重新准备 review JSON。三卷均使用 TeX Live 2026、XeLaTeX 和 latexmk 4.88。回执状态 `compiled_pending_review`。PDF SHA、输入树、依赖树、工具指纹和完整日志均绑定在各项目 `receipts/build.json`。

| 卷别 | Build attempt | 页数（试题/解析/简答/印刷） | PDF SHA-256（同序） |
|---|---|---:|---|
| 江西理科 | `1a75c317-6e62-4f58-bce3-dd38a50c5b61` | 6 / 21 / 8 / 16 | `db9f78a881d6c0ecb0e881c5b4e54fe3960e7196a72c5e50dc4e87e138f129a4` / `0b43e5a6eae917af0e8b28fd5ed545176459931491da7a778d2b9fb472da2a52` / `6fbd27913a0cfbc53650cc24d18fcbfb9ec14ec23f1f276d61680780966171a1` / `dff47315baa235db1b10468a9ff26f06f02a9d0789b36ea76185b0f7d8ca6c09` |
| 浙江理科 | `ad74a82a-5c3d-467c-bec2-c673ec07e561` | 5 / 18 / 7 / 13 | `832f88a29c8ee9400286ba557f8d54f1b417c57011533c22876e3e2c34d57824` / `94aeba2c8648a54cb11fcc8df8d03b767a2c323951f27da7fcc9d9488cf355e8` / `352f2e8301deb109445f251ff9a6eb1e01edb9e76fc87e5a1373abdbea9842f1` / `b62c9f3f19deb1a2ded2d9927af84a50408c0344394b7ba0aa4e22e1720d5cce` |
| 湖北理科 | `cb4a5749-2126-4d27-bd4e-c004284d1476` | 5 / 19 / 7 / 14 | `8cf726750a31da196a365128d95939a4bb687d93c16d26b3ad9533b2cec158cd` / `ff2eb8c93961063abf688fee1a3a55fea98bb8a31e926f0c11283014534774a0` / `91d5c683e0a8461e901368f54771dd3df370627b4445821d87c1167c0bd36478` / `face5138969b10c47af63ee89dd7eb4c7b0a42d5d0937a42907274aacecdb0f4` |

12 个版本均无编译错误、缺字、Overfull 或未定义引用。日志中有 5 条 Underfull `\\hbox`：江西印刷版 1 条（lines 455–456，badness 1087）；湖北试题、解析、简答版各 1 条（lines 6–7，badness 10000）；湖北印刷版 2 条（lines 6–7，badness 10000 与 3219），须结合相关页面判断。

## 视觉审查现状

已建立 12 份 review JSON，覆盖 139 页、每页 8 项。页面已渲染；已抽查江西若干试题、答案速查、解析与印刷版页面，所见图稿和版面清楚。抽查不能代替全页检查，尚未完成 139 页逐页审查；未写 pass 结论，未 finalize。`build_projects.py validate-receipts --manifest source-manifest.json --batch phase1-b70 --json` 返回 `pending: 3`，failed/invalid/missing/stale/running 均为 0。全库单元测试未运行。

## 后续步骤

1. 完成 139 页的逐页八项视觉检查，优先检查所有新图页面及 5 条 Underfull 警告所在页面。
2. 仅对实际检查过的页面更新 review JSON；全部完成后运行 review/check/finalize 门禁。
3. 湖北 Q17（2）继续保留原题面和阻断 issue，除非有可核的一手来源证据消除冲突。
4. 批次关闭后更新全量报告投影与 CSV，并按项目流程评估完整测试；此批收口不表示长期语料完成。

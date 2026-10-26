# 2000 广东卷：固定来源身份与结构审计（2026-10-27）

## 结论

固定来源 `src-c603aac0b64fcc89e162bd2b5358ce3c9a5c1ce8e5949a7f787f906fa25393a6` 的两页 PDF 自题“2000 普通高等学校招生考试（广东卷）”，可作为**自题为2000年广东卷的固定题面副本**继续转录。它没有答案或解析页，未标文/理轨道，也不能单独证明原始发布机构、出版者、版次或官方性。

## 文件与来源绑定

- manifest 固定 upstream：`普通高考/2000/2000广东.pdf`
- upstream 仓库：`deekur/gaokaomath`；manifest 固定 commit：`34c13a6cf632c0b69c95f89b9b923bbc4a08924d`
- Git blob：`6be3ae05418e54f487cb869c561b3338bf10df64`；从该 commit 读取的文件 blob SHA 与 manifest 一致
- PDF SHA-256：`0169a9a1f44f8cfab377f1c49423c5875147961d1965ee17cb8a3a84d38aedcb`，与 manifest 一致
- 大小：620,036 字节；2页；A3横向，约1190.55 × 841.89 pt；PDF 1.6
- 来源经 GitHub 固定 commit 读取，随后由 `source_manifest.materialize_source` 校验 Git blob、PDF SHA 与 PDF 元数据，并将本地审计副本放入被忽略的 `.work/2000-guangdong/source.pdf`；未改 manifest 或登记关系

## 卷首、题号与图形

两页整页以140 dpi渲染并目视核看，PDF文字层可提取；没有使用OCR。首面题签为“2000 普通高等学校招生考试（广东卷）”，页脚为印刷页64、65。题号连续1–22：选择题1–12、填空题13–16、解答题17–22。可见图形题包括Q5函数图、Q12圆锥、Q16正方体截面、Q19平行六面体、Q21种植成本图、Q22双曲线图。未见答案、答案表或解析内容。

该固定副本只覆盖题面；题目原字形和图形仍需逐题核读，文字层抽取结果只用作定位辅助，不替代页面核对。题签没有表明文/理科别或总分，manifest 的 `track=null`、`regions=[]`、`paper_id=null` 保持不变。

## 下一步门槛

先独立逐题转录并对照两页原图，保留字形疑点；图形需TikZ重绘并与Markdown引用、manifest和provenance同步。答案与解析必须另找可核验来源或明确标记缺失；不得从模型记忆补写。来源出版/官方身份尚未核实前，本报告不建立canonical paper绑定，也不启动四版构建。

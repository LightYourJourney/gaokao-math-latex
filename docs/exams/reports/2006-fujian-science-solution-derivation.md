# 2006 福建理科候选卷：Q1–Q22 解析正文独立推导

## 来源和范围

- 固定 source：`src-ab0f2729ee4a24495e653b44c14438b4130f8b38b11362bf84251f3595a09d27`；PDF SHA-256 `50d17546b94af82fb2cee653942752914cd387fe72792d74ffa5f75e7a301d83`。题面 SHA-256 `c67e39d29dff29b6e76426821694841504141f73feb3e336b637976f880ab03f`。
- 规范解答写入 `2006/2006_数学真题_福建理_解析正文.md`，覆盖 Q1–Q22；答案小问与题面 2/3/2/2/2/3 完全对应。以下均为非官方独立推导。
- 固定 PDF 只有题面，发布者、出版者、版次、来源链及官方身份未核；`paper_id=null`、`official_answer=null`。Q16、Q18、Q20 尚无矢量图；解析不依未完成图形补入题目条件。

## 复核结论

解析正文 SHA-256：`dc4e1cea6390b4bedc7cc782714c2f712f1c423ef880097056cf0201fdbda1bf`。两名 Luna/high 独立审稿者分段审读 Q1–Q11 和 Q12–Q22，均逐题标记 PASS。审查记录保存在 ignored `.work/ocr-local/next-paper/solution-proof-review/q01-q11.md`、`q12-q22.md`；主会话核对记录及关键推导。

重点复核包括：

- Q7：按直线平行平面即无公共点的严格定义，A 可被“$n$ 落在 $\alpha$ 内”的反例排除；C 利用两条直线共面且不相交成立。
- Q10：联立式判别式为 $16(e^2-1)^2$；右支判据 $u\ge1$；$1<e<2$ 时右支两个交点，$e=2$ 线性退化所得唯一右支交点 $u=5/4$，$e>2$ 时恰有一个右支交点，故区间为 $[2,+\infty)$。
- Q16：中点三角形重心不变、直径逐次减半，极限点为原三角形重心 $(5/3,2/3)$。
- Q18：空间坐标推导得到 $AO\perp$ 平面 $BCD$，异面角为 $\arccos(\sqrt2/4)$，点 $E$ 到平面 $ACD$ 距离为 $\sqrt{21}/7$。
- Q20：弦中点 $u=-2k^2/(1+2k^2)$、$v=k/(1+2k^2)$，从而 $x_G=-k^2/(1+2k^2)$；$k\ne0$ 使值域端点均不取，范围 $(-1/2,0)$。
- Q21：水平线与 $H(x)=-x^2+8x-6\ln x$ 有三个不同交点当且仅当 $7<m<15-6\ln3$；等号时只有两个不同交点。Q22 未补造 $b_2$，推得 $b_n=2+(n-1)(b_2-2)$，自由公差保留。

## 确定性合并

- 解析器读取题面、答案点、解析正文各22题，小问集合逐题相符。
- `solution_sources.check_paper` 对本卷三份源文本返回 `ok=True`、`question_count=22`、`problems=[]`。
- `solution_sources.render_combined()` 生成的 `2006/2006_数学真题_福建理_含解析.md` 为14,210字符，和当前文件逐字节相同；`extract_solution_blocks()` 提取出的解析正文也与规范解析源相同。
- 合并稿 SHA-256：`2b160ad4aed06c1cad5043fa293576d3e7b3362d5c86f5d60f04ddb0480d2fcb`。

## 全库检查及未完事项

全库 `python3 tools/solution_sources.py check-all --manifest source-manifest.json` 退出码1，报告15/397套旧合并输出与确定性重建结果不一致。失败 paper ID 为：`gk-2026-regular-national-1-recall`、`gk-1958-regular-hubei`、`gk-1986-regular-national-science`、`gk-1986-regular-guangdong-science`、`gk-1987-regular-national-arts`、`gk-1987-regular-national-science`、`gk-1987-regular-shanghai-math`、`gk-2005-regular-national-1-science`、`gk-2016-regular-national-1-arts`、`gk-2016-regular-national-1-science`、`gk-2015-regular-hubei-arts`、`gk-1990-regular-national-arts`、`gk-2015-regular-chongqing-arts`、`gk-2018-regular-zhejiang`、`gk-2018-regular-jiangsu`。以上均非本卷，本卷尚未登记进该 manifest 集合，因此专卷检查以直接三源重建比较为准，未将全库结果描述为通过。

本阶段仅完成解析正文和确定性含解析输出。题图重绘、逐题 provenance、paper/batch 登记、生成 TeX、正式四版构建和逐页视觉回执尚未完成；本卷及长期语料均未验收完成。

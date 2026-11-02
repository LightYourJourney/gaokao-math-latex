# 2006 福建文科候选卷：Q11 双曲线解析纠错

## 范围与来源

- 目标：`gk-2006-regular-fujian-arts`，批次 `phase1-b76`，仅修订 Q11 详细解析并更新受影响的确定性输出、构建与视觉回执。
- 固定题源：source `src-88a71372c96b05a58058a4446824a5aa14004ffa91901212088621a6b41d0346`，PDF SHA-256 `8984913f8b9b4927361dc042f0d78b4ff9fe6b4b9b7b898d7184c1f4cea05432`。
- PDF 仅固定本库收到的候选题面字节；发布者、版次、来源链和官方身份均未认证，`official_answer=null`。以下答案是本库独立推导，不宣称为官方答案。

## 纠错与独立复核

旧解析将右焦点 $F=(c,0)$ 作为一个双曲线交点，但 $F$ 代入双曲线左端为 $c^2/a^2=e^2>1$，所以并不在曲线上。原答案 C 及区间 $e\in[2,+\infty)$ 不变；证明已改为直接对直线与双曲线联立，并检查两个交点分别位于左支还是右支。

令 $e=c/a>1$、$r=b^2/a^2>0$、$u=x/a$。由直线 $y=\sqrt3(x-c)$ 与 $e^2=1+r$，得到

$$
u^2-\frac3r(u-e)^2=1,
\qquad
(r-3)u^2+6eu-(3e^2+r)=0.
$$

判别式为 $16r^2>0$。当 $r\ne3$，两根为

$$
u_+=\frac{-3e+2r}{r-3},\qquad u_-=\frac{-3e-2r}{r-3}.
$$

右支满足 $u\ge1$，左支满足 $u\le-1$。若 $0<r<3$，则 $r+3-3e<0$，从而 $u_+-1=(r+3-3e)/(r-3)>0$；并且 $u_--1=3(1-e-r)/(r-3)>0$，两交点都在右支。若 $r>3$，则 $r+3-3e>0$，故 $u_+>1$；且 $u_-+1=(-3e-r-3)/(r-3)<0$，另一个交点在左支。临界情形 $r=3$ 时方程退化为 $12u-15=0$，唯一交点 $u=5/4>1$。所以恰有一个右支交点等价于 $r\ge3$，即 $e^2=1+r\ge4$、$e\ge2$，答案仍选 C。

独立盲核者先按固定题面独立重推，指出旧证明的焦点错误而确认答案 C 不变；随后逐项复核新证明的无量纲方程、判别式 $16r^2$、根式分类及 $r=3$ 的线性情形，确认论证成立。记录见 ignored `.work/ocr-local/next-paper/arts-q11-blind-review.md` 与 `arts-q11-proof-review.md`。

## 变更与构建

- 修订 `2006/2006_数学真题_福建文_解析正文.md`；解析正文 SHA-256：`d30478671d1e413eed8167fc8ab7cc8b11167982c14bd9ecebe31b0436d7415a`。
- 确定性更新 `2006/2006_数学真题_福建文_含解析.md` 与 `math-gaokao-latex/2006_福建卷_文科/answers.tex`；简答表和四版壳无需改动。
- 正式构建 attempt `1f4445a4-552e-48da-8e7f-4485c3d64dbd` 成功，构建时 manifest revision 5968。页数为试题版4、解析版18、简答版6、印刷版13，共41页。
- PDF SHA-256：
  - 试题版：`5c5a9d42bc5edada9dbc7c4595fdde0a0f2b8bcfa471b764af9a7795743b8e11`
  - 解析版：`7baacf65e48342ccc8a1dce979e3e6961c2fd2d7517295a22990c010f79a3b72`
  - 简答版：`17b9de3e84637eab1ed8206f29990094ef3490888e8dc71e3f359544be56f2ab`
  - 印刷版：`2c1803994dde7ab6bfe061fb43f83fd4ce9d204ae9337f52470e30e699b8708e`
- 旧/新页渲染逐页 SHA 对照后，试题版4页、简答版6页、解析版前9页及印刷版前6页共25页图像字节相同，继承此前同页视觉结论；解析版10–18页及印刷版7–13页共16页重新检查。八项视觉检查合计272 pass、56 not_applicable、0 fail。解析 Q18 有一条 Underfull 行宽警告，已目视确认页面完整并登记豁免。
- `review_receipts.finalize-batch` 成功，phase1-b76 状态 `closed`、review receipt `FINALIZED`，manifest revision 5970；`source_manifest.py validate`、`issues.py validate`、本批 `provenance.py check-batch`、`solution_sources.py check-batch`、四版 receipt currentness、review receipt、CSV projection 与 `report.py check --all` 均通过。

## 全量测试结果

`python3 -B -m unittest discover -s tests -q` 结束于 `Ran 1767 tests`，结果 `FAILED (failures=2, skipped=13)`。失败为：

1. `test_task25_updates_exactly_eight_existing_keys_with_layout_only_diffs`：2017 全国Ⅰ理科 `answers.tex` 当前 SHA 为 `8ea128d4aba0a2bed8897d4719a8df3d99c119c7bc3a15b98ee8c6f5d797f233`，漂移账本记录 SHA 为 `9318dce3313b0575c1382eb225301dfec145683d59b54367fa13a81f3f0b3a30`。该文件当前工作树字节与本分支 HEAD 一致；本阶段没有修改该卷或其漂移账本。
2. `test_the_cached_states_match_the_recomputed_ones`：全库 provenance 检查发现79项缓存状态与现场派生状态不一致；失败示例含 `gk-2012-regular-national-outline-arts` 的缓存 `complete` 与现场 `answers_verified` 不符。本批福建文科 `provenance.py check-batch` 通过，manifest 内容仅因本批事务更新了 revision 和 transaction ID。

上述全量测试问题未在本阶段改动；因此记录为现有全库门禁失败，不能将本阶段描述为全量测试通过。本卷 Q11 纠错、四版构建和视觉回执完成，不表示来源认证、官方答案验证、整卷无阻塞验收或1952–2026语料完成。

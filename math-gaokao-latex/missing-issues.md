# 高考数学 LaTeX 缺失与问题总账

每个问题块使用稳定编号和可重算 fingerprint；已解决问题保留记录。

## ISSUE-0001

```json
{
  "affected_paper_ids": [],
  "conflict_code": "recall-vs-official",
  "current_evidence": "b06 题面核对角色的核心发现：上游对照件「普通高考/2026/2026全国1(山东,广东,湖南,湖北,河北,江苏,福建,浙江,河南,江西,安徽).pdf」（manifest source_id src-a6848f53cf4932dc654a47dc89f3ce68bcd68c88c1e90e1bfeb7fb504fb59536，现场 shasum -a 256 得 f6f8ed7cdab86bedd7b3d261b7066c97a9fe24e3ad71538d1d01e6ce03f3fcb1，与 manifest artifact.sha256 相同，实测 5 页与登记一致）第 1 页页眉逐字印「2026 年全国 1 卷高考数学真题(回忆版)」——即上游件自身即标注为回忆版，上游根本不存在 2026 全国 1 的正式卷，可比对、可绑定的正式源不存在。19 题逐题四分类比对结果：逐字一致 9 题、实质一致但表述有出入 10 题、实质不一致 0 题、正式卷有而回忆版无对应 0 题（对照件 19 题分布于 p1-p4，p5 整页空白，不存在第 20 题及以后内容）。这一比对只证明规范源 2026/2026_数学真题_试题.md 忠实转录了该回忆版 PDF，不证明、也无法证明它与官方正式卷一致——比对的两端都是回忆版。10 处「表述有出入」中 9 处为标点/记号/分值补注类，唯一一处非标点实词改动是第 17 题（md 删去「投中 1 次时」的「时」字，见另条题锚定登记）。本卷 source_ids 保持为空、只用 legacy_source_files 的本地路径引用（2026/2026_数学真题_试题.md，sha256 9a7b161d42029833ebd0c38c4c6add67576ecfd390a1c52f3f428d12bd0bb5e1），provenance 亦按本地路径导入，未绑定任何上游 source。",
  "fingerprint": "838b91797a3403c21eee95a996aa19fccfa8bf0d9e78955f16c9ba97811b9f20",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-national-1-recall",
  "resume_action": "需从上游之外获得教育部考试院发布的 2026 全国 1 卷官方正式卷，方可解除本身份问题；上游件页眉自陈回忆版（对照件 sha256 f6f8ed7cdab86bedd7b3d261b7066c97a9fe24e3ad71538d1d01e6ce03f3fcb1），绑定通道关闭——在取得官方正式卷之前，不得将本卷与任何上游 source 绑定，也不得据「与回忆版逐题一致」推断与正式卷一致",
  "status": "open",
  "type": "identity-ambiguous"
}
```

## ISSUE-0840

```json
{
  "affected_paper_ids": [
    "gk-2009-regular-national-1-arts"
  ],
  "conflict_code": "duplicate-choice-item-12-13",
  "current_evidence": "固定源 PDF（source_id src-867f441324b4d2d957468f27b46ef4193ad0fd6e8755a90e64ad242a8dc2b3cf，印刷页 509）中的第 12、13 题题干、椭圆方程、向量条件和 A-D 选项逐字重复。题面按固定源原样保留，不能据此判断其中一题是否应为其他题。",
  "fingerprint": "51bcb9560599f9ba5144455fd50788f274103ee6a273f31eef055c747d2272bd",
  "impact": "blocks_completion",
  "paper_id": null,
  "resume_action": "取得同版官方勘误或其他可靠版本，确认第 12、13 题是否确为重复题；在此之前保留固定源字面与两个相同的独立计算结果。",
  "source_id": "src-867f441324b4d2d957468f27b46ef4193ad0fd6e8755a90e64ad242a8dc2b3cf",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0841

```json
{
  "affected_paper_ids": [],
  "evidence": "复核确认 `lg` 为常用对数而非自然对数。令 t=lg e，由 2<e<3<√10 得 0<t<1/2，故 a=t>c=t/2>b=t^2，正确选项为 B；原阻断来自误读，不是固定源题面缺陷。",
  "fingerprint": "59423def55ea3b936c954b0491ba5c72fffad7d113848609bfb2b6924228afaa",
  "impact": "blocks_completion",
  "paper_id": "gk-2009-regular-national-2-arts",
  "question_id": "gk-2009-regular-national-2-arts-q07",
  "resume_action": "已完成复核：按常用对数重新计算并将答案修正为 B；不再需要外部勘误。",
  "source_id": "src-0edea5107f19ab7a372cdf45d0f6d80b04d55899bf82531626bf29483732d902",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-0839

```json
{
  "affected_paper_ids": [],
  "evidence": "固定源 PDF 第 2 页第 18 题的题干仅给出等差数列 a_4=10 且 a_3、a_6、a_10 成等比数列。设公差为 d，可得 (10+2d)^2=(10-d)(10+6d)，即 d(d-1)=0；d=0 与 d=1 均满足题面，分别给出 S_20=200 与 S_20=330。题面未写出‘非零公差’或‘非等差常数列’限制。",
  "fingerprint": "b808c216ae80a79fa37a237b01f97370313f693ad1f9a2057e748894e10a1952",
  "impact": "blocks_completion",
  "paper_id": "gk-2008-regular-national-2-arts",
  "question_id": "gk-2008-regular-national-2-arts-q18",
  "resume_action": "取得同版官方答案或清晰勘误，确认是否隐含排除公差为零；在此之前保留两个合法值，并在解析中说明分支。",
  "source_id": "src-f95822698595457bf8e1dd66e1257dafb395f0c106977e34f771837d14c654aa",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0834

```json
{
  "affected_paper_ids": [],
  "evidence": "固定源 PDF 第 1 页第 4 题的题干为圆弧 y=1-√(1-x²) 与过 (-2,0) 的直线求两交点斜率；按题干字面实算为 0<k≤1/3，但固定源选项 C 印成 (√2/4,√2/4)，为空区间，现有选项无法独立核对。题面忠实保留该印刷字面，答案仅保留源位置 C 并标注待核。",
  "fingerprint": "aa992be00e11e7e6d066279086b27b289c7fdf4e509358e45740c6c730314ee8",
  "impact": "blocks_completion",
  "paper_id": "gk-2005-regular-national-1-science",
  "question_id": "gk-2005-regular-national-1-science-q04",
  "resume_action": "取得清晰勘误或同版源确认第 4 题选项 C；在此之前保留固定源字面与独立计算结论。",
  "source_id": "src-c734f943945ff01fe268ce680901faefaf71cecd77971ead7cebdf4d982ee4b3",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-0002

```json
{
  "affected_paper_ids": [
    "gk-2017-regular-national-1-arts",
    "gk-2017-regular-national-1-science"
  ],
  "conflict_code": "regions-vs-upstream-path",
  "fingerprint": "49d8a4ab4466a6bc24f65d97624aafa328e40cd139ad2572455d0e1ba5497286",
  "impact": "blocks_completion",
  "paper_id": null,
  "resolution": "逐卷内容核验完成：2017 年山东有独立卷（与全国 1 卷第 1 题内容互异，已实证），上游固定路径 普通高考/2017/2017全国1理·文(河南,河北,山西,江西,湖北,湖南,广东,安徽,福建).pdf 的卷种身份与本库 2017 全国 I 卷理/文两卷一致，身份歧义消解，据此确认来源绑定；规范源 frontmatter 的适用省份记载有误（多列山东）、上游文件名正确，frontmatter 错误不属身份歧义，由 ISSUE-0006 跟踪。",
  "resume_action": "逐卷核验规范源地区与固定上游全国 1 路径，不按地区字符串自动绑定",
  "status": "resolved",
  "type": "identity-ambiguous"
}
```
## ISSUE-0003

```json
{
  "affected_paper_ids": [],
  "current_evidence": "公开版 PDF 第 2 页下方完整显示正视图、左视图和俯视图的等腰直角三角形；当前 LaTeX TikZ 图形已完整覆盖，原裁切 PNG 不作为最终图形来源。 核验资料：https://file.xdf.cn/uploads/171031/1017_171031111038bRXHLd0C5GaKSdRr.pdf",
  "fingerprint": "42aeaff5fe35ed88f5e4960e7c46d0f935b4c91442b8bfdf040f2fb02ed0c0cd",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-1-science",
  "question_id": "gk-2017-regular-national-1-science-q07",
  "resume_action": "已用独立公开版核验三视图完整性，保留 LaTeX TikZ 矢量重绘，不提交 PNG；重跑题面、生成、编译与视觉复核。",
  "source_id": "src-51eb5c18a0e4ad056c80a78acd915bc5d94193d7bb4506dd2fd2d078157b8d40",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0004

```json
{
  "affected_paper_ids": [],
  "current_evidence": "公开版 PDF 第 3 页完整显示第 8 题 A、B、C、D 四幅图及下降分支；当前 LaTeX TikZ 图形已完整覆盖，原裁切 PNG 不作为最终图形来源。 核验资料：https://cdn.gaokzx.com/zixunzhan/202403/546f482e-f82b-42c6-9afc-a17bfc28c12f.pdf",
  "fingerprint": "78c8e8465c7357d3f9e820e8944ff1aea9509fd28092c4eb4bef7fc400f05f83",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-1-arts",
  "question_id": "gk-2017-regular-national-1-arts-q08",
  "resume_action": "已用独立公开版核验四个候选图及 A—D 标签完整性，保留 LaTeX TikZ 矢量重绘，不提交 PNG；重跑题面、生成、编译与视觉复核。",
  "source_id": "src-f4cc1ec8f7a5385f215c3ccec22f7942eadf5c1caa6a30fa88862df589f91c55",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0005

```json
{
  "affected_paper_ids": [
    "gk-2017-regular-national-1-arts",
    "gk-2017-regular-national-1-science",
    "gk-2018-regular-national-1-arts",
    "gk-2018-regular-national-1-science"
  ],
  "conflict_code": "official-answer-key-unavailable",
  "current_evidence": "b01 求解角色 92 题全 A、盲核 92 题全 none，但比对基准是库内 `_答案要点.md`（其本身系库内独立推导），官方发布版未获取，与官方的一致性未核。",
  "fingerprint": "acdfb52f53f4d5da8a00158490eef3dfa4784fa1b4bd5ec40c4b13f4c9293ef0",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "取得官方发布的标准答案后，逐题比对 b01 四卷 `_答案要点.md`；在此之前答案要点只能声明为库内独立推导的结论，不得表述为官方答案",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0006

```json
{
  "affected_paper_ids": [
    "gk-2017-regular-national-1-arts",
    "gk-2017-regular-national-1-science"
  ],
  "conflict_code": "frontmatter-regions-vs-upstream",
  "current_evidence": "ISSUE-0002 收口时逐卷核验：2017 年山东有独立卷（与全国 1 卷第 1 题内容互异实证），上游文件名 `2017全国1理/文(河南,河北,山西,江西,湖北,湖南,广东,安徽,福建).pdf` 正确、不含山东，而两卷 frontmatter 的适用省份多列了「山东」（2018 上游文件名才含山东）。现已按该证据修正两卷规范源，并核对生成结果未受题面内容影响。",
  "fingerprint": "f5d0925b92f2e0cf2b1741332467f6b80726c8b958a6326a9d728369a880d802",
  "impact": "non_blocking",
  "paper_id": null,
  "resolution": "已修正 2017 理/文两卷 `_试题.md` frontmatter，以及理科卷正文卷种提示处的同一串，适用省份改为 河南、河北、山西、江西、湖北、湖南、广东、安徽、福建（不含山东）；两卷生成结果校验通过。",
  "resume_action": "已完成修正；若上游卷种身份再次变更，重新按上游文件名与逐卷内容核验",
  "status": "resolved",
  "type": "source-mismatch"
}
```

## ISSUE-0007

```json
{
  "affected_paper_ids": [
    "gk-2017-regular-national-1-arts",
    "gk-2017-regular-national-1-science",
    "gk-2018-regular-national-1-arts",
    "gk-2018-regular-national-1-science"
  ],
  "conflict_code": "footer-raw-pdf-dangling",
  "current_evidence": "四卷 `_试题.md` 文末页脚均写 `> **原卷影印件**：[`../_raw/<年>_数学_<科>.pdf`](...)`，而 `_raw/` 目录在库内不存在，四条链接均为死链。",
  "fingerprint": "b35bde5a325214aac4289a124350891db6252198efbc823a8d09709aca381e8b",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "改写四卷 `_试题.md` 文末页脚的原卷影印件链接（PDF 二进制不入库，宜改为指向 source-manifest 的 source_id / upstream_path），或另行说明获取方式",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0008

```json
{
  "affected_paper_ids": [
    "gk-2017-regular-national-1-science",
    "gk-2018-regular-national-1-science"
  ],
  "conflict_code": "answer-key-argument-gaps",
  "current_evidence": "2017 理 Q12、2018 理 Q19(2) 与 Q22(2) 的原论证缺口已补齐；2017/2018 理科四版当前构建与逐页视觉复核均通过，phase0-b01 已正式关闭。",
  "fingerprint": "48c04c30c3aea79e39d6c78bc09fdcd7dfa0f0e82ae4ae5068361602e6fa53b4",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "已完成：2017 理 Q12 补足唯一性与整数范围论证；2018 理 Q19(2) 补入垂直线情形；2018 理 Q22(2) 补足斜率符号与位置分类。",
  "resolution": "2017 理 Q12 补足由 N>100 推出 k≥13、比较相邻整数幂并唯一确定 k+3=2^m 的过程；2018 理 Q19(2) 补入垂直弦 l:x=1 的对称情形，并在斜率存在时用韦达定理完成斜率和为零的证明；2018 理 Q22(2) 补足 k>0、-4/3<k<0、k<-4/3 的交点数分类及相切位置验证。两卷四版当前构建与视觉审查收据均通过，phase0-b01 正式关闭。",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-0009

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面文字与图形均已核实：公开扫描页 https://www.gaokao.com/e/20190609/5cfc879c086fb_2.shtml 的第 2 页逐字显示「爻分为阳爻“——”和阴爻“— —”，如图就是一重卦」，并显示六爻图形（从上到下为阴、阴、阴、阳、阳、阴）；规范源文字已补回，图形已按该扫描用 TikZ 矢量重绘为 f2019_t6_hexagram.tex，题试版与解析版均引用同一源，未提交扫描图。",
  "fingerprint": "e52460575976f006ce1b6600a8b8753f6a3aab17c097b90444a55a0315cd4710",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-regular-national-1-science",
  "question_id": "gk-2019-regular-national-1-science-q06",
  "resolution": "已取得独立可核验扫描页并完成 TikZ 矢量重绘；已接入规范题面、manifest 和生成器映射，待本批 provenance、XeLaTeX 构建与视觉回执完成后闭环。",
  "resume_action": "已完成矢量图接入；重跑本批题面核对、生成、编译与视觉复核",
  "source_id": "src-7052c2bd0093946c481076d7dfc16a8eaaec17214ab251fa4f0d43660f94e002",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0010

```json
{
  "affected_paper_ids": [],
  "current_evidence": "原始理科源图左缘被切（内容包围盒 x 起自 0）：待填空白框左边框被切除、「k=k+1」被切成「= k + 1」、循环回边不完整；下缘越界混入第 9、10 题正文与被切成残片的选项行（(A) 项不可读）。同一框图在文科固定源 `2019文-t9-程序框图.png` 中完整；最终 LaTeX 不把裁切 PNG 当线稿，而由既有 `2019_全国Ⅰ卷_理科/figures/f2019_flow.tex` 矢量重绘，完整包含空白框左边框、`k=k+1` 和回流箭头。phase0-b02 四版本构建与视觉回执已通过。",
  "fingerprint": "ef53e85a85a78cede3c8d180b1ad96eb90af09ab1861111996a2c8341c271128",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-regular-national-1-science",
  "question_id": "gk-2019-regular-national-1-science-q08",
  "resolution": "保留裁切理科 PNG 作为来源缺陷记录；沿图形标准不新增或提交 PNG，采用同题完整文科源交叉核对，并使用 `f2019_flow.tex` 矢量重绘。四个版本的生成、XeLaTeX 构建和视觉复核均通过。",
  "resume_action": "已完成矢量修复；不提交原卷截图或 PNG",
  "source_id": "src-7052c2bd0093946c481076d7dfc16a8eaaec17214ab251fa4f0d43660f94e002",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0011

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立公开版 PDF 第 2 页给出完整横轴 0/10/20/30/40、温度/°C 标签和散点云；当前 LaTeX pgfplots 矢量图已覆盖这些要素，未使用截图作为线稿。 核验资料：https://cdn.zizzs.com/zixunzhan/202310/c15dec3e-666b-4c24-a7fb-7d66a2f1d1f1.pdf",
  "fingerprint": "aac74a79333bf972f0dad1ff2038fbe915c52199d42398f3593db1d5ede09833",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q05",
  "resume_action": "已用独立公开版核验散点图完整性，重跑题面、生成、编译与视觉复核；不提交 PNG。",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0012

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立公开版 PDF 第 2 页给出 [−π,π] 上两个完整波谷及 −π、−4π/9、O、π 标注；当前 LaTeX pgfplots 矢量图已完整重绘。 核验资料：https://cdn.zizzs.com/zixunzhan/202310/c15dec3e-666b-4c24-a7fb-7d66a2f1d1f1.pdf",
  "fingerprint": "1d16e3a6bed0798f589bc86973f74165eff09da0fa926445e3f9d4a1f47d990f",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q07",
  "resume_action": "已用独立公开版核验函数图完整性，重跑题面、生成、编译与视觉复核；不提交 PNG。",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0013

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立公开版 PDF 第 3 页给出标注 D(P)、A、B、C、E(P)、F(P) 的完整三棱锥平面展开图；当前 LaTeX TikZ 矢量图已按该构型重绘并编译通过。 核验资料：https://cdn.zizzs.com/zixunzhan/202310/c15dec3e-666b-4c24-a7fb-7d66a2f1d1f1.pdf",
  "fingerprint": "d13a5e11a755fd220001718a56bc6fc9132c5bdb253ccda80cd6dc38a6a79984",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q16",
  "resume_action": "已用独立公开版核验展开图标注，重跑题面、生成、编译与视觉复核；不提交 PNG。",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0014

```json
{
  "affected_paper_ids": [],
  "current_evidence": "实验数据句子已补回；独立公开版 PDF 第 2 页确认复用散点图完整，当前 LaTeX pgfplots 矢量图已完整重绘，未将 PNG 作为线稿。 核验资料：https://cdn.zizzs.com/zixunzhan/202310/c15dec3e-666b-4c24-a7fb-7d66a2f1d1f1.pdf",
  "fingerprint": "53d1a4270c45205732fc2720759b8238bf72ac67fa6831fa6665bdf7ac9644dc",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-arts",
  "question_id": "gk-2020-regular-national-1-arts-q05",
  "resume_action": "已补回实验数据句子，并用独立公开版核验复用散点图；重跑题面、生成、编译与视觉复核，不提交 PNG。",
  "source_id": "src-922b361942c8607abdfaba4bb5d504e18b644f5cfb744d7ae848a477192919bf",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0015

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立公开版 PDF 第 2 页确认复用函数图完整包含两个波谷和横轴标注，当前 LaTeX pgfplots 矢量图已完整重绘。 核验资料：https://cdn.zizzs.com/zixunzhan/202310/c15dec3e-666b-4c24-a7fb-7d66a2f1d1f1.pdf",
  "fingerprint": "eed5d5c350a48802bdb98c890787a6803fdb0b6590cc0b689d7ecbe108fc38bb",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-arts",
  "question_id": "gk-2020-regular-national-1-arts-q07",
  "resume_action": "已用独立公开版核验复用函数图，并重跑题面、生成、编译与视觉复核，不提交 PNG。",
  "source_id": "src-922b361942c8607abdfaba4bb5d504e18b644f5cfb744d7ae848a477192919bf",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0016

```json
{
  "affected_paper_ids": [],
  "current_evidence": "已将答案要点、解析和含解析中的余弦值统一更正为 +2√5/5；四法复核及当前生成物一致。",
  "fingerprint": "c953859e9024b1898ccd56fd010e5aa7df3a34a7c1c7cccca541a93328bd79bb",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q18",
  "resume_action": "已更正第 18(2) 题答案为 +2√5/5，并以垂直于 PC 的截面投影法重跑计算与答案核验。",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "resolved",
  "type": "answer-missing"
}
```
## ISSUE-0017

```json
{
  "affected_paper_ids": [],
  "current_evidence": "当前答案要点与独立复核均为 +2√5/5，二面角按指定两半平面的截面方向为锐角，冲突已消除。",
  "fingerprint": "87894b0360c60bb0b5ad40ea7e7c43b2dab282e881847d4ce6d3e9c8f5abcdfd",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q18",
  "resume_action": "已更正答案符号并重跑答案核查、生成、编译与盲核；原有答案冲突已消除。",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "resolved",
  "type": "answer-conflict"
}
```
## ISSUE-0018

```json
{
  "affected_paper_ids": [],
  "current_evidence": "已将答案要点改为“由奇偶性排除 A；f(π/2)>1（峰值）排除 B；(0,π) 上函数值为正排除 C”。答案 D 与独立复核及解析一致，冲突已消除。",
  "fingerprint": "e72c14acf6c00916b001b22d329162d9dc7b01e2fdcf91b404ff3bff52648fe7",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-regular-national-1-arts",
  "question_id": "gk-2019-regular-national-1-arts-q05",
  "resume_action": "已更正第 5 题答案要点的排除依据，并重跑题面、答案、生成、编译与盲核；答案 D 保持不变。",
  "source_id": "src-67200538ccc7c8c92b28b4ee9180beac26c60144b9fc409ccf93ce5db5ebc37c",
  "status": "resolved",
  "type": "answer-conflict"
}
```
## ISSUE-0019

```json
{
  "affected_paper_ids": [
    "gk-2020-regular-national-1-arts",
    "gk-2020-regular-national-1-science"
  ],
  "conflict_code": "cross-paper-figure-reuse",
  "current_evidence": "2020 文科卷 `_试题.md` 第 46 行引用 `images/2020理-t5-散点图.png`、第 58 行引用 `images/2020理-t7-图象.png`，即文卷第 5、7 题直接复用理科卷的图片资产。这条隐式跨卷依赖没有任何登记，理科卷资产一旦改名或移动，文卷会静默断链。",
  "fingerprint": "0b751a7f2f44b47b516cc3b056bce6f5a8c3ff1a212847b99729c0e63b421417",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "为 2020 文科卷第 5、7 题建立本卷自有图片资产（或在两卷图片清单里显式登记这条跨卷依赖），避免理科卷资产改名/移动时文卷静默断链",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0020

```json
{
  "affected_paper_ids": [
    "gk-2019-regular-national-1-arts",
    "gk-2019-regular-national-1-science",
    "gk-2020-regular-national-1-arts",
    "gk-2020-regular-national-1-science"
  ],
  "conflict_code": "figure-trim-artifacts",
  "current_evidence": "b02 题面核对在 7 道 passed 题的证据里逐条记录了配图越界毛边：内容完整、不涉实质损失，故判 passed；集中登记以便批量重导。",
  "fingerprint": "8a3ea2c30431a6ae2c74f9f8f0aa4e1d4a927a1c345e2488623961509f2da3c6",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "批量重导以下 7 张图，去掉越界毛边（题面核对均判 passed，仅观感问题，不阻断）：2019理-t5-四图（图内重复题干 + 图下贯穿全幅的黑色条带伪影）、2019理-t18-棱柱（左上角相邻文字）、2019文-t5-四图（右缘「=」字符）、2019文-t9-程序框图（下缘选项行上半截）、2020文-t9-程序框图（上缘上一行残片 + 下缘混入 (B)(C)(D) 选项与第 10 题首行）、2020文-t19-圆锥（右上角「(1) 求／(2) 证明」文字）、2020理-t18-圆锥（左上角一点毛边）",
  "status": "open",
  "type": "layout-warning"
}
```

## ISSUE-0021

```json
{
  "affected_paper_ids": [
    "gk-2019-regular-national-1-arts",
    "gk-2019-regular-national-1-science",
    "gk-2020-regular-national-1-arts"
  ],
  "conflict_code": "answer-key-argument-gaps",
  "current_evidence": "前四处由 b02 答案独立求解角色在 A 级判定的比对说明中记录；第五处（Q21 标号）由导入方直接核对 `2019/2019_数学真题_理_答案要点.md` 第 241–260 行确认。五处均不影响答案正确性。",
  "fingerprint": "e7d23153add8c16b3c1e5832bb92ca5909f90bb8ea9b143144fbb2a575479d59",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "补齐/更正五处（结论均正确，缺的是论证或表述）：2019 文 Q4 要点写「身高=1.618×(头顶至肚脐)×…」，正确系数应为 1+1/λ≈2.618 且省略号未补全，所给区间 [170,178] 是精确区间 [169.89,178.21] 的取整版；2019 理 Q4 直接取等算出 h≈178.3 后以「四个选项中最接近 175」收尾，未建立区间上下界；2019 理 Q20(2) 列出三段单调性后径称 (0,π) 上「先升后降」，未显式补出 [π/2,π] 段的 f'<0；2020 文 Q19(2) 未校验 P 确在线段 DO 上（PO=√2/2 ≤ DO=√2）；2019 理要点 Q21 小问标号笔误——(2) 之下的第二小问被再次标为「(2) 答案：p₄=…」，应为「②」（其上一条已标「① 证明要点」）",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0022

```json
{
  "affected_paper_ids": [
    "gk-2019-regular-national-1-arts",
    "gk-2019-regular-national-1-science",
    "gk-2020-regular-national-1-arts",
    "gk-2020-regular-national-1-science"
  ],
  "conflict_code": "official-answer-key-unavailable",
  "current_evidence": "与 b01 的 ISSUE-0005 同类、同 conflict_code，因 affected_paper_ids 进 fingerprint 身份，故按批次另立同类新条而非改写既有条目。b02 求解角色的比对基准同样是库内 `_答案要点.md`（其本身系库内独立推导），官方发布版未获取。",
  "fingerprint": "f2aacbf58b1196e1b1193605c9b414aad90b0d485450d5bc492463ed0c0f9c81",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "取得官方发布的标准答案后，逐题比对 b02 四卷 `_答案要点.md`；在此之前答案要点只能声明为库内独立推导的结论，不得表述为官方答案",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0023

```json
{
  "affected_paper_ids": [
    "gk-2019-regular-national-1-arts",
    "gk-2019-regular-national-1-science",
    "gk-2020-regular-national-1-arts",
    "gk-2020-regular-national-1-science"
  ],
  "conflict_code": "footer-raw-pdf-dangling",
  "current_evidence": "与 b01 的 ISSUE-0007 同类、同 conflict_code，按批次另立同类新条（affected 进身份）。已核对：四卷 `_试题.md` 末行分别写 `../_raw/2019_数学_理.pdf`、`../_raw/2019_数学_文.pdf`、`../_raw/2020_数学_理.pdf`、`../_raw/2020_数学_文.pdf`，而 `_raw/` 目录在库内不存在。",
  "fingerprint": "18a9ba16633cb36a733dddfc5a2973592ac7d2b507e3419ecfcc063378a0897e",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "改写 b02 四卷 `_试题.md` 文末页脚的原卷影印件链接（PDF 二进制不入库，宜改为指向 source-manifest 的 source_id / upstream_path），或另行说明获取方式",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0024

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed（标注 Q/A/B/C/D 五点齐全、无裁切、几何构型与 PDF 相同、棱与面的连接关系未变），但虚实线约定有一处偏差：PDF 中可见棱 QD 为实线，转录件画成虚线。该图中 QA 本就是虚线，两条虚线并存会暗示存在两个被遮挡的顶点，与实际构型不符，属会误导读图的呈现错误，故按中等严重度单独登记。",
  "fingerprint": "83922b837c67137cfbb0c09a919b6057de221378cfb5dc1ef17f2963df4f176d",
  "impact": "non_blocking",
  "paper_id": "gk-2021-regular-new-gaokao-2",
  "question_id": "gk-2021-regular-new-gaokao-2-q19",
  "resume_action": "重绘 images/2021-Ⅱ-t19-四棱锥.png：可见棱 QD 应为实线（PDF 原图如此），现画成虚线；其余 QA、AB、AD、BD 的虚线与 PDF 一致，勿一并改动",
  "source_id": "src-20c5bf5c6684f32611f1bb38d0907bd8800fb03780f0b52c603fb222695aa505",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0025

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed：题干（球心 O、纬度定义、水平面定义、晷面与赤道平面平行、北纬 40°）与选项 20°／40°／50°／90° 均与 PDF p1 一致。非实质差异仅一处：PDF 在选项上方印有一张日晷实物照片，规范源未转录。该照片无任何标注、题干未出现「如图」、不承载解题信息，属装饰性插图缺省。",
  "fingerprint": "a00911746019d123d217a56355e0d43731013fff2a207e7c3f36f6a9a00f172e",
  "impact": "non_blocking",
  "paper_id": "gk-2020-regular-new-gaokao-2",
  "question_id": "gk-2020-regular-new-gaokao-2-q04",
  "resume_action": "如需与 PDF 完全对齐可补转录第 4 题选项上方的日晷实物照片；该照片无标注、题干未出现「如图」、不承载解题信息，补与不补均不影响作答，优先级低",
  "source_id": "src-48131c790a20ff5ba4bce9416b0422dd2f2a9b23fd269fa657eb7581877a5b4e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0026

```json
{
  "affected_paper_ids": [
    "gk-2020-regular-new-gaokao-2",
    "gk-2021-regular-new-gaokao-1",
    "gk-2021-regular-new-gaokao-2"
  ],
  "conflict_code": "scoring-notes-not-in-source",
  "current_evidence": "三卷 `_试题.md` 各有四条段首说明行（单选「本题共 8 小题，每小题 5 分，共 40 分…」、多选「本题共 4 小题，每小题 5 分，共 20 分。全部选对得 5 分，部分选对得 2 分，有选错得 0 分。」、填空、解答），三卷逐字相同，已由导入方直接核对三份规范源确认存在。题面核对角色报告：这四条说明行在本批三份上游 PDF 中完全无对应，即无本批来源可为其背书。事实核查协议记录：2020 与 2021 两年份的多选题部分分值是否相同，本批证据不足以判定，结论为「未能核实」——未能核实不等于不存在，不得据此断言该行错误，也不得据参数记忆补全。",
  "fingerprint": "0d5d8e8c79be600ec8b50837f3fd9846372951e0438922dea1246a7f67345237",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "对三卷四条段首分值说明行做定向核查后决定去留：或找到权威来源（官方试卷扉页说明/考试院文件）为其背书并注明出处，或改写为不声称分值的中性提示，或整体删除。特别注意：2020 与 2021 两个年份的多选题部分分值规则是否相同尚未核实，禁止用参数记忆补全，须联网定向核查后再动",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0027

```json
{
  "affected_paper_ids": [
    "gk-2021-regular-new-gaokao-1"
  ],
  "conflict_code": "frontmatter-reform-claim-unverified",
  "current_evidence": "2021 新高考Ⅰ卷 `_试题.md` 第 16 行写「历史意义：这是湖南首次使用新高考 I 卷的年份（2021 年湖南实施「3+1+2」新高考改革）」，已由导入方直接核对规范源确认原文。该句是现实世界事实陈述，本批来源（上游数学试卷 PDF）不含任何可核验它的内容。事实核查协议记录：结论为「未能核实」，既不能据此判其为错，也不能据参数记忆为其背书。",
  "fingerprint": "fb7d9f24269f2e1baf29548a0ad9b388aeac84ce7fd68f7bc926041105301c28",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "对该括注做外部定向核查（湖南 2021 年是否首次使用新高考 I 卷、是否实施「3+1+2」模式）；核实前不得据参数记忆改写，核实后或补出处或删去括注",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0028

```json
{
  "affected_paper_ids": [
    "gk-2021-regular-new-gaokao-1"
  ],
  "conflict_code": "footer-raw-pdf-dangling",
  "current_evidence": "沿 b01 的 ISSUE-0007、b02 的 ISSUE-0023 约定，同 type 同 conflict_code 另立新条（affected_paper_ids 进 fingerprint 身份，无法原地扩展）。已核对：2021 新高考Ⅰ卷 `_试题.md` 末行写 `../_raw/2021_数学.pdf`，而 `_raw/` 目录在库内不存在。本批仅此一卷有该缺陷——2020 新高考Ⅱ与2021 新高考Ⅱ的末行是「试题来源：deekur/gaokaomath（commit 34c13a6…）」说明，不含 _raw 链接。",
  "fingerprint": "88856f28486cd888f0472a16bf3cdc5e9c0368d6415b7825e478d97297c31b37",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "改写 2021 新高考Ⅰ卷 `_试题.md` 文末页脚的原卷影印件链接（PDF 二进制不入库，宜改为指向 source-manifest 的 source_id / upstream_path，或沿用本批另两卷的「试题来源：deekur/gaokaomath（commit …）之「…」PDF」写法）",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0029

```json
{
  "affected_paper_ids": [
    "gk-2021-regular-new-gaokao-1"
  ],
  "conflict_code": "metadata-conventions-drift",
  "current_evidence": "已由导入方直接核对三份规范源：2021 新高考Ⅰ卷 frontmatter 的来源行写「deekur/gaokaomath（CC BY 4.0）」不带 commit 号，且全文零处 commit 号（其文末是 _raw 链接而非来源说明）；同批 2021 新高考Ⅱ卷 frontmatter 与 2020 新高考Ⅱ卷文末均记有 commit 34c13a6。另，2021 新高考Ⅰ卷的 title 与「卷种」字段写「新高考 I 卷」，用的是 ASCII 大写 I，而同批另两卷及库内其余各卷用罗马数字 Ⅰ／Ⅱ。两者都不影响题面与答案，属元数据一致性问题。",
  "fingerprint": "4d2e27a465142d4dbcd47973b333906c244c5d80704e101718b4cfc3f07f118b",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "统一 2021 新高考Ⅰ卷的元数据写法：一是补上上游 commit 号（另两卷均为 34c13a6，2021Ⅱ 记在 frontmatter 的来源行、2020Ⅱ 记在文末来源行），二是把 title 与「卷种」里的 ASCII 字母 I 改为罗马数字 Ⅰ，与全库其余各卷一致",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0030

```json
{
  "affected_paper_ids": [
    "gk-2020-regular-new-gaokao-2",
    "gk-2021-regular-new-gaokao-1",
    "gk-2021-regular-new-gaokao-2"
  ],
  "conflict_code": "official-answer-key-unavailable",
  "current_evidence": "沿 b01 的 ISSUE-0005、b02 的 ISSUE-0022 约定，同 type 同 conflict_code 另立新条。b03 求解角色 66 题全 A、盲核 66 题全 none，但比对基准是库内 `_答案要点.md`（其本身系库内独立推导），官方发布版未获取，与官方的一致性未核。b03 的证据文本自始使用「库内答案要点」措辞，未出现「官方」误称。",
  "fingerprint": "6a86f1159a96e56831d54722797ec092f8764259f2b9a1f5a3b2b238bb57eaa7",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "取得官方发布的标准答案后，逐题比对 b03 三卷 `_答案要点.md`；在此之前答案要点只能声明为库内独立推导的结论，不得表述为官方答案",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0031

```json
{
  "affected_paper_ids": [
    "gk-2020-regular-new-gaokao-2",
    "gk-2021-regular-new-gaokao-1",
    "gk-2021-regular-new-gaokao-2"
  ],
  "conflict_code": "answer-key-argument-gaps",
  "current_evidence": "证据来源分两组，逐条标明以免混淆。甲组（可在本批 .work 落盘证据里逐字核对，共四处）：2021Ⅰ 第 21 题的「内部」措辞、以及三处「见解析版」，均见于答案独立求解角色的 A 级比对说明。乙组（由角色在回报中提出，未落入 .work，共三处）：2021Ⅱ 第 21(2) 题 c∈[0,1) 区间偏松、一处选择题排除理由不完备、2020Ⅱ 第 1 题干扰项点评含糊。乙组之所以不在 .work 里，是因为盲核角色的记录 schema 只有 answer_sha256／conflict_status／issue_ids 三个字段、没有 evidence 字段，其观察无处落盘；第六处的具体题号亦因此缺失，改写前需回盲核角色回报确认题号。",
  "fingerprint": "0e329a573cbafa61e935f84ed6e703d6fe3be8fe44ffa327e194db7860b6254e",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "逐处复核并改写（七处均不影响答案正确性）：一、2021Ⅰ 第 21 题要点称「T 在双曲线内部」，而 T(1/2,t) 实际位于两支之间的中心区域而非某一支的凹侧，真正起作用的判据是 x₁x₂>0 ⇒ k²>16、与 T 的具体位置无关，建议改写措辞；二至四、三处小问标「见解析版」但要点正文其实已自包含完整内容——2020Ⅱ 第 19(2) 题（已给出完整列联表）、2021Ⅰ 第 18(1) 题（已给出完整分布列）、2021Ⅱ 第 22(1) 题（已给出完整分类表），建议去掉误导性的「见解析版」；五、2021Ⅱ 第 21(2) 题要点给的 c∈[0,1) 区间偏松（双盲同见）；六、一处选择题的排除理由不完备；七、2020Ⅱ 第 1 题对干扰项的点评含糊。",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0032

```json
{
  "affected_paper_ids": [
    "gk-2020-regular-new-gaokao-2"
  ],
  "conflict_code": "figure-trim-artifacts",
  "current_evidence": "沿 b02 的 ISSUE-0020 约定，同 type 同 conflict_code 另立新条。本批 7 张图全为重绘件、零裁切缺陷，题面核对全判 passed；两处差异均已与 PDF 原图逐点比对确认不改变读图信息：t9 图的两组 11 天数据走势、第 2 天复工降至 78%、第 9 天两线交叉、第 11 天复产略高于复工、82%／80%／78% 三条虚线与轴标均相符，仅图例文字为编辑性扩写；t11 图的 y 轴、刻度 1、O、π/6、2π/3 标注齐全，相位与零点位置一致，仅两端截止位置略有出入。",
  "fingerprint": "1d85f36605c679782104602cbc5d9ee6c443068b2468530fa741f2c6db6bce08",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "重绘时对齐两处细节：images/2020-Ⅱ-t9-复工复产折线图.png 的图例文字由 PDF 的「复产／复工」被扩写为「复产指数／复工指数」；images/2020-Ⅱ-t11-正弦图象.png 曲线左右两端的截止位置与 PDF 不同（重绘件收于 x 轴、PDF 收于半坡）",
  "status": "open",
  "type": "layout-warning"
}
```

## ISSUE-0033

```json
{
  "affected_paper_ids": [],
  "current_evidence": "双盲同见（本工程第二例）：答案独立求解角色与答案盲核角色在互不知情下对同一处给出同一诊断——要点把 |t|=√2/2 一支写成「（或 1/√2，对称）」，而该值恰为双曲线 x²/2−y²=1 的渐近线斜率，代入后二次项系数为零、方程退化，AP 与曲线只有一个公共点，必须舍去，并非对称解。求解角色另做 numpy 复核（两点均在双曲线上、k_PQ=−1、tan∠PAQ=2.828427、面积 2.5141574=16√2/9），确认结论不受影响。本条同时承接盲核角色对本题给出的 conflict_status=resolved：分歧已判明为要点叙述缺陷而非答案错误，按 T18 口径为 resolved 状态留一条可追溯的指针。",
  "fingerprint": "2b321d8816d5ba7dd877d87f5940867d427bf067797ca7f560cc2d3bbeab3c21",
  "impact": "non_blocking",
  "paper_id": "gk-2022-regular-new-gaokao-1",
  "question_id": "gk-2022-regular-new-gaokao-1-q21",
  "resume_action": "改写 2022 新高考Ⅰ卷 `_答案要点.md` 第 21(2) 题的舍值理由：|t|=√2/2（即 1/√2）不是「对称支」，而是与渐近线平行的无效支——该斜率下二次项系数为零、方程退化、AP 与 C 只有一个公共点，应以此为由排除；答案 16√2/9 无需改动",
  "source_id": "src-abb272e6926b56eec2f33b23b5a36bf48cf890620787bec47c5dfd69d3fcaf73",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0034

```json
{
  "affected_paper_ids": [],
  "current_evidence": "控制器裁定维持 passed（判例同 b03 的 ISSUE-0024 QD 虚实线）：F 由题干向量式 EF⃗=DA⃗ 完全代数确定，图仅起辅助作用，缺该虚线不影响解题。500 dpi 比对确认两处辅助虚线差异：转录件多一条 A—E 竖直虚线、缺 PDF 原图的 E—F 虚线。六个标注（D/B/A/C/E/F）齐全、实线 DA/DB/AB/AF/FB 一致、无裁切。题面核对角色评为「四卷中最值得登记的图片问题」。",
  "fingerprint": "6321c77996290c1179e8de1fbbc93cb22dd17448d67f156112efd11a1b1426b2",
  "impact": "non_blocking",
  "paper_id": "gk-2023-regular-new-gaokao-2",
  "question_id": "gk-2023-regular-new-gaokao-2-q20",
  "resume_action": "重绘 images/2023-Ⅱ-t20-三棱锥.png：补上 PDF 原图中的 E—F 虚线（原图以虚线 D—E—F 折线表示 F 的位置），并去掉转录件多画的 A—E 竖直虚线",
  "source_id": "src-6d630ab56ae1e00ba708253221026ea6afd0bb2e506f8e949ca761a54de6d641",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0035

```json
{
  "affected_paper_ids": [],
  "current_evidence": "控制器裁定维持 passed：图 1 不承载解题信息，解题信息全在题干与图 2，而图 2（images/2022-Ⅱ-t3-屋顶截面.png）与 PDF 原图逐点相符——y 轴、O、D₁、D、C₁、C、B₁、B、A₁、A、x 轴共 11 个标注齐全、折线与虚线辅助线一致、无裁切。图 1 的问题是与源图不同源：PDF 为古建屋架透视版画（九个标注），转录件改画为山面桁架剖面示意（八个标注，缺 O）。",
  "fingerprint": "6189c733a07b7ac2d48e82c1cc95e34f5b6dca1d4973bb27c1bd29287cff8dda",
  "impact": "non_blocking",
  "paper_id": "gk-2022-regular-new-gaokao-2",
  "question_id": "gk-2022-regular-new-gaokao-2-q03",
  "resume_action": "由内容任务定夺 images/2022-Ⅱ-t3-举架结构.png（图 1）的处置：或忠实重绘源图（古建屋架透视版画，含 A′/B′/C′/D′、A/B/C/D 与 O 共九个标注），或保留现有示意图但明确标注为编者示意并补回缺失的 O 标注",
  "source_id": "src-8a9765e7b1dd41ff5435b28d8edee31aa19573a01960a903650ad6ae3cd25fd6",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0036

```json
{
  "affected_paper_ids": [],
  "evidence": "固定 source_id `src-7fdec764fe31e143cd6daf81734e2df4d142dc09b0a3ad696d522aacbefa7f63` 的 PDF 第 1 页文字层及页面渲染均印作“学生需从这 8 门课中选修 2 门或 3 门课”；规范题面现已补回末尾“课”，与固定源一致，答案 64 不变。",
  "fingerprint": "91a1212be76d82c368ff795020cee10c2a1a48e38d2c170342806d8457fc4f66",
  "impact": "non_blocking",
  "paper_id": "gk-2023-regular-new-gaokao-1",
  "question_id": "gk-2023-regular-new-gaokao-1-q13",
  "resume_action": "已按固定源 PDF 第 1 页补回漏字，并同步更新规范题面、派生稿、provenance 与四版；无需后续核查。",
  "source_id": "src-7fdec764fe31e143cd6daf81734e2df4d142dc09b0a3ad696d522aacbefa7f63",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0037

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed（300 dpi 渲染复核）：题干与四选项 1/6／1/3／1/2／2/3 一致，唯一差异是单字近义替换，取数范围与答案不变。本题无配图。与「源 PDF 有缺陷、按正确版转录」那一类不同——此处源无缺陷，是转录方无理由改字。",
  "fingerprint": "1d44e128c9ba24f6333c727cb04a30e5a2d4c856a7aee6d1e4b4ed8448222adf",
  "impact": "non_blocking",
  "paper_id": "gk-2022-regular-new-gaokao-1",
  "question_id": "gk-2022-regular-new-gaokao-1-q05",
  "resume_action": "回改近义替换：PDF 作「从 2 至 8 的 7 个整数」，规范源作「从 2 到 8 的 7 个整数」，「至」被无理由换成「到」；按忠实转录纪律回改为「至」",
  "source_id": "src-abb272e6926b56eec2f33b23b5a36bf48cf890620787bec47c5dfd69d3fcaf73",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0038

```json
{
  "affected_paper_ids": [],
  "current_evidence": "由答案盲核角色在回报中提出（其记录 schema 只有 answer_sha256／conflict_status／issue_ids，无 evidence 字段，故未落入 .work）。可与求解角色的落盘证据相互印证：求解角色用代换 u=√3x−y、v=√3x+y 把三命题归结为 λ=2 即 M 为 AB 中点，在 ②③⇒① 一支里显式处理了「u₂=v₁ 会导致 x₁=x₂ 与 x₁>x₂ 矛盾」，并有数值复核（M=(3.84615,4.61538) 恰为 AB 中点、|MA|=|MB|=7.174906964）；要点缺的是与之对称的u₂=−v₁ 一句。",
  "fingerprint": "a12895e4ad73287ed2ffd610abb51e3434fd9ae9b0d573d75b7fdbb07584241f",
  "impact": "non_blocking",
  "paper_id": "gk-2022-regular-new-gaokao-2",
  "question_id": "gk-2022-regular-new-gaokao-2-q21",
  "resume_action": "在 2022 新高考Ⅱ卷 `_答案要点.md` 第 21(2) 题补一句 u₂=−v₁ 情形的排除说明（现有分类只处理了 u₂=v₁）；结论与主线论证不受影响",
  "source_id": "src-8a9765e7b1dd41ff5435b28d8edee31aa19573a01960a903650ad6ae3cd25fd6",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0039

```json
{
  "affected_paper_ids": [],
  "current_evidence": "由答案独立求解角色在 A 级比对中发现（答案 C={−2} 双方一致，仅注解有瑕）：x²−x−6≥0 ⇔ x≤−2 或 x≥3，M 中仅 −2 满足且恰取等号；若漏掉等号则解集为空，不会得到选项 D。该注解自相矛盾，不影响答案。",
  "fingerprint": "1144e7e729ddc91a4c0886e9bf0d298fd5284ef61f6c9728cd3ecbebe2edfac0",
  "impact": "non_blocking",
  "paper_id": "gk-2023-regular-new-gaokao-1",
  "question_id": "gk-2023-regular-new-gaokao-1-q01",
  "resume_action": "更正 2023 新高考Ⅰ卷 `_答案要点.md` 第 1 题的「易错」注解：现写「漏掉等号导致误选 D」不成立——漏掉等号得到的是空集，四个选项中没有对应项；应改写为真实的易错成因或删去该注解",
  "source_id": "src-7fdec764fe31e143cd6daf81734e2df4d142dc09b0a3ad696d522aacbefa7f63",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0040

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed：C/P/A/B/E/O 六个标注齐全，实线 CP/CA/AB/AP/PE/EB/AE 与 PO 虚线一致、无裁切，600 dpi 比对仅见辅助虚线的条数与起点差异，不丢标注、不改变棱面连接关系。注：本题第 (2) 问 PDF 源缺「的」字（「求二面角 C−AE−B 正弦值」），规范源照录未改，属 report.md「批次 1 勘误」第 2 条既有裁决，不在本条范围内。",
  "fingerprint": "6a08acc049e530c267af2623082bd33fca3d000c039dc2420066e168c0dd11ad",
  "impact": "non_blocking",
  "paper_id": "gk-2022-regular-new-gaokao-2",
  "question_id": "gk-2022-regular-new-gaokao-2-q20",
  "resume_action": "重绘 images/2022-Ⅱ-t20-三棱锥.png 的辅助虚线：现自 C 引出三条虚线（含一条 C—O），PDF 原图自 C 只引出两条（至 E、至 B），另有一条自 O 出发的虚线",
  "source_id": "src-8a9765e7b1dd41ff5435b28d8edee31aa19573a01960a903650ad6ae3cd25fd6",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0041

```json
{
  "affected_paper_ids": [
    "gk-2022-regular-new-gaokao-1",
    "gk-2023-regular-new-gaokao-1"
  ],
  "conflict_code": "source-pdf-errata-corrected",
  "current_evidence": "三处均由题面核对角色在 150–300 dpi 渲染复核中逐字核对，判非实质、维持 passed，处理方式与 report.md「批次 1 勘误」第 1 条（2024 Q19 源 PDF 衍文按语法正确版转录）同类。其中 2022Ⅰ 第 20 题的两处讹字是本批新发现、此前未登记；2022Ⅰ 第 8 题与 2023Ⅰ 第 19 题两处亦未登记。登记为卷级批量单而非逐题条目，是因为一条 issue 的身份只能带一个 question_id，跨三题两卷无法逐题锚定；代价是这三处在 provenance 的逐题 issue_ids 里不可见。",
  "fingerprint": "d3a821aab11b07556759ac59724e31a2f7de88f1fe5baf081cba8509a6dc057c",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "把三处「源 PDF 缺陷、规范源按正确版转录」补登进 report.md 的勘误清单（现清单只有 2024 Q19 衍文与 2022Ⅱ T20(2) 缺「的」两条）：一、2022Ⅰ 第 20(1) 问，PDF 作「认为该疾病群体与末患该疾病群体」，「认为」后缺「患」字、「未患」误作「末患」，规范源按语义正确版写作「认为患该疾病群体与未患该疾病群体」（另 PDF「調査」用「査」异体字形，规范源作「查」，属字形归一）；二、2022Ⅰ 第 8 题，PDF 设问作「则该四棱锥体积的取值范围是」，规范源补一「正」字作「该正四棱锥」（题干首句已声明正四棱锥）；三、2023Ⅰ 第 19(2) 问，PDF 作「(2) 证明: 当 a>0 时, 求证: f(x)>2lna+3/2.」，「证明:」与「求证:」重复，规范源删去重复的「求证:」。另见 ISSUE-0047（2023 新高考Ⅱ 第 19(2) 问缺「时」字，属「源错照录不改」类，补登勘误册时勿遗漏这第四处）",
  "status": "open",
  "type": "source-mismatch"
}
```
## ISSUE-0042

```json
{
  "affected_paper_ids": [
    "gk-2022-regular-new-gaokao-1",
    "gk-2023-regular-new-gaokao-1"
  ],
  "conflict_code": "punctuation-normalized",
  "current_evidence": "三处均由题面核对角色记录、判非实质并维持 passed：只涉标点形态，题意、数据与答案均不变。三题均无配图。",
  "fingerprint": "ba5373ad38e576aa7ea944adf76c905940ed315550e8126f5a639f6529338e16",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "三处标点与 PDF 不一致，按忠实转录纪律决定是否回改：2022Ⅰ 第 6 题「最小正周期为 T, 若」的逗号在规范源作句号；2023Ⅰ 第 10 题「距离燃油汽车, 混合动力汽车, 电动汽车」的逗号在规范源作顿号；2023Ⅰ 第 15 题「在区间 [0,2π], 有且仅有」的逗号在规范源被省略",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0043

```json
{
  "affected_paper_ids": [
    "gk-2022-regular-new-gaokao-1",
    "gk-2023-regular-new-gaokao-1"
  ],
  "conflict_code": "footer-raw-pdf-dangling",
  "current_evidence": "沿 ISSUE-0007（b01）、ISSUE-0023（b02）、ISSUE-0028（b03 的 2021Ⅰ）同 type 同 conflict_code 另立新条（affected_paper_ids 进 fingerprint 身份，无法原地扩展）。已核对：2022Ⅰ 末行写 `../_raw/2022_数学.pdf`、2023Ⅰ 末行写 `../_raw/2023_数学.pdf`，而 `_raw/` 目录在库内不存在。同批两个Ⅱ卷末行是「试题来源」说明、不含 _raw 链接。这已是该缺陷第四次出现，且四次全部落在Ⅰ卷/全国卷一侧，疑为同一批转录作业的固定习惯。",
  "fingerprint": "6fb01e0aff8b2cc49924d9a41eb3f11368599ee0ed96079e787c57c072cbe36f",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "改写 2022、2023 两个新高考Ⅰ卷 `_试题.md` 文末页脚的原卷影印件链接（PDF 二进制不入库，宜改为指向 source-manifest 的 source_id / upstream_path，或沿用同批两个Ⅱ卷的「试题来源：deekur/gaokaomath（commit `34c13a6`…）」写法）",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0044

```json
{
  "affected_paper_ids": [
    "gk-2022-regular-new-gaokao-1",
    "gk-2023-regular-new-gaokao-1"
  ],
  "conflict_code": "metadata-conventions-drift",
  "current_evidence": "沿 ISSUE-0029（b03 的 2021Ⅰ）同 type 同 conflict_code 另立新条。已由导入方直接核对四份规范源：2022Ⅰ 与 2023Ⅰ 的来源行均无 commit 号与 PDF 名，而 2022Ⅱ、2023Ⅱ 均有；2022Ⅰ、2023Ⅰ 的 title 与「卷种」写「新高考 I 卷」（ASCII I）。ASCII I 现已在 2021Ⅰ、2022Ⅰ、2023Ⅰ 三卷连续出现，不是一次性笔误而是Ⅰ卷侧的系统性写法漂移，建议连同 ISSUE-0029 一次性归一。另观察到Ⅱ卷内部亦不齐（2022Ⅱ 作「新高考Ⅱ卷」无空格、2023Ⅱ 作「新高考 Ⅱ 卷」有空格），一并归一为宜。",
  "fingerprint": "23cda00ead69153f0ed9f3ce142f1bea00cd3943435fd4626393b7a668462e58",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "统一 2022、2023 两个新高考Ⅰ卷的元数据：一是来源行补上 commit 号与源 PDF 名（现仅「deekur/gaokaomath（CC BY 4.0）」，同批两个Ⅱ卷均为「deekur/gaokaomath（commit 34c13a6，CC BY 4.0）之 <PDF 名>」）；二是把 title 与「卷种」里的 ASCII 字母 I 改为罗马数字 Ⅰ",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0045

```json
{
  "affected_paper_ids": [
    "gk-2022-regular-new-gaokao-1",
    "gk-2022-regular-new-gaokao-2",
    "gk-2023-regular-new-gaokao-1",
    "gk-2023-regular-new-gaokao-2"
  ],
  "conflict_code": "frontmatter-regions-unverified",
  "current_evidence": "事实核查协议记录。四卷省份串已由导入方与 manifest 的上游文件名逐项比对，结论是内部自洽：2022Ⅰ「山东、广东、湖南、湖北、河北、江苏、福建」、2022Ⅱ「海南、辽宁、重庆」、2023Ⅰ「山东、广东、湖南、湖北、河北、江苏、福建、浙江」、2023Ⅱ「辽宁、重庆、海南、安徽、吉林、黑龙江、山西、云南」，与各自upstream_path 文件名括号内的省份串一致。但「与上游文件名一致」只证明转录忠实，不证明该串符合现实——上游文件名本身未经核查。结论为「未能核实」：未能核实不等于有错，既不据此判其为误，也不为其背书；属涉现实、随年份变化的时变事实，按协议不采信参数记忆。b01 的 ISSUE-0006（2017 两卷多列山东）证明这类串确实可能出错。",
  "fingerprint": "4d8b6687b656ebdb092116ef7642c8a4b6dc1ab33eee4512949050ccf0e27ac3",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "对四卷 frontmatter 的「适用省份」串做外部定向核查（各年各卷种的实际使用省份以考试院/教育部公告为准）；核查前不得据参数记忆增删省份，核查后补出处或更正",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0046

```json
{
  "affected_paper_ids": [
    "gk-2022-regular-new-gaokao-1",
    "gk-2022-regular-new-gaokao-2",
    "gk-2023-regular-new-gaokao-1",
    "gk-2023-regular-new-gaokao-2"
  ],
  "conflict_code": "official-answer-key-unavailable",
  "current_evidence": "沿 ISSUE-0005（b01）、ISSUE-0022（b02）、ISSUE-0030（b03）约定另立新条。b04 求解角色 88 题全 A、盲核 87 none + 1 resolved，但比对基准是库内 `_答案要点.md`（其本身系库内独立推导），官方发布版未获取。本批证据文本统一使用「库内答案要点」措辞，未出现「官方」误称。",
  "fingerprint": "66837db19c6a595107f9fef67786ecffb3efcf790840a16a4e3fcb2f1c87f5fc",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "取得官方发布的标准答案后，逐题比对 b04 四卷 `_答案要点.md`；在此之前答案要点只能声明为库内独立推导的结论，不得表述为官方答案",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0047

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed，其证据末段记录：PDF 原文第 (2) 问作「当 c∈[95,105], 求 f(c) 的解析式」，「[95,105]」之后缺一「时」字；规范源 2023/2023_数学真题_新高考Ⅱ_试题.md 第 131 行照录为「当 $c\\in[95,105]$，求 $f(c)$ 的解析式，并求 $f(c)$ 在区间 $[95,105]$ 的最小值。」，同样无「时」字，行号已由导入方用 grep -n 机械定位复核（对照同题第 (1) 问第 129 行「当漏诊率 $p(c)=0.5\\%$ 时，求…」，「时」字在该处是有的，可见缺字仅在第 (2) 问）。本处与 ISSUE-0041 的三处方向相反：0041 是「源错、规范源按正确版改对」，本处是「源错、规范源照录不改」，两类的后续处置不同，故分条登记。",
  "fingerprint": "7e7f2d002694ec2f1671e4f73e0b1979ed67bd61b6736acc8a8df7baa930434e",
  "impact": "non_blocking",
  "paper_id": "gk-2023-regular-new-gaokao-2",
  "question_id": "gk-2023-regular-new-gaokao-2-q19",
  "resume_action": "把本处补登进 report.md 的勘误清单，与该清单第 2 条（2022 新高考Ⅱ T20(2) 缺「的」）同列为「源 PDF 有缺陷、按不改字纪律照录」类。规范源不需改动——照录本身是正确的忠实转录行为，登记只为让这处源缺陷进入勘误册、不至于只存活在一条逐题证据里。",
  "source_id": "src-6d630ab56ae1e00ba708253221026ea6afd0bb2e506f8e949ca761a54de6d641",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0048

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 failed（本批唯一）。上游源 PDF p1 600 dpi 视读为「cos 2A + cos 2B + 2 sin C = 2」，sin C 无平方上标，PDF 文本层同样抽出「2 sin C = 2」；同题选项 (A) 的「sin²A + sin²B」两处上标在同一渲染与同一文本层中均清晰可见，据此排除字体或文本抽取丢失上标的可能。规范题面第 74 行作 $2\\sin^2 C$，是增加了一个数学上标、改变了条件方程本身，不属标点或排印差异，故判 failed 而非编辑性勘误——从源印文本无法机械推出该上标，需要数学论证，不满足「唯一可复原」判据。旁证（不构成对官方原卷的认定）：按 2sin²C 读，条件化为 sin²C=sin²A+sin²B ⇒ C=π/2，配合面积 1/4 与 cosAcosBsinC=1/4 可解出 ab=1/2、外接圆 R=1/√2，四选项非退化；按源印的 2sinC 读，(A) 恰为条件的同义改写而 (B)(C) 无法定出，题目退化。但官方原卷该处究竟为 sin C 抑或 sin²C 未能核实——本次只比对了上游 PDF 与规范题面，未取得官方文本作正面核查，按不对称证据标准不下断言。四个选项与源逐字一致。",
  "fingerprint": "a359896e775cdf0387b2bfddabecb46983157ced3430b9acafb65f33a1c42831",
  "external_evidence": "中国教育在线 2025-06-07 试题页（https://gaokao.eol.cn/shiti/sx/202506/t20250607_2673303_1.shtml）所嵌第 2 页原题图（https://img.eol.cn/e_images/gk/2025/st/qg1/sx02.png）也清晰印作「2sinC」，未见平方上标；该页面不是教育考试院直发文件，因此只作为独立旁证，不改变当前阻断结论。",
  "impact": "blocks_completion",
  "paper_id": "gk-2025-regular-national-1",
  "question_id": "gk-2025-regular-national-1-q11",
  "resume_action": "对官方原卷该处做正面定向核查后二选一：若官方为 sin²C，则补一条与 2024 新高考Ⅱ Q19 同规格的勘误裁决（来源页 + 旧/新题面 SHA-256 + 删改理由），本题转 passed；若官方与上游源印同为 sin C，则规范源 2025/2025_数学真题_试题.md 第 74 行须改回源印字面。在官方层面核实之前，两个方向都不得径自执行",
  "source_id": "src-52c0a1ccacd7d0f6a8ba555e22474325194ac4aba7daa75012cc39626bc32ac3",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0049

```json
{
  "affected_paper_ids": [],
  "current_evidence": "盲核角色判 conflict_status=resolved，本条为该状态的承接指针（沿 b04 ISSUE-0033 口径：resolved 也要留一条可追溯条目，否则「这里曾有分歧、结论是什么」在 provenance 里只剩一个状态词）。已修正规范答案源与解析正文：z>y 的临界值为 (5 ln 5−3 ln 3)/(ln 5−ln 3)≈9.301320，x>z 的临界值为 (5 ln 5−2 ln 2)/(ln 5−ln 2)≈7.269412；k=8 时 (x,y,z)=(64,243,125)，确为 y>z>x（D）。B 要求 k 同时大于 9.301320 且小于 7.269412，仍不可能；答案 B 未变。独立算式用标准库对数重算，针对性测试覆盖阈值顺序、A/C/D 见证及答案源/解析正文一致。",
  "fingerprint": "3ba8cd72d53c8b630da71b4aa1eed378f729e2b9ee02641b4ad3344dcbd65a5c",
  "impact": "non_blocking",
  "paper_id": "gk-2025-regular-national-1",
  "question_id": "gk-2025-regular-national-1-q08",
  "resume_action": "已修正第 8 题两份规范答案材料中的临界值与 D 项见证；最终答案 B 保持不变。",
  "source_id": "src-52c0a1ccacd7d0f6a8ba555e22474325194ac4aba7daa75012cc39626bc32ac3",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-0050

```json
{
  "affected_paper_ids": [],
  "current_evidence": "同一道题的两处非实质差异，因逐题问题的身份是 (type, paper_id, question_id, source_id)、同题同类无法分立两条，故合并登记。图片：500 dpi 视读确认图 1 表值（2 轻风 1.6~3.3、3 微风 3.4~5.4、4 和风 5.5~7.9、5 劲风 8.0~10.7）与图 2 的「视风风速」箭头指向 (0,2)、「船速」箭头指向 (3,3)、虚线网格与 O/1/2/3/x 标注均与源一致；缺陷是仓库图顶边被裁、纵轴「y」轴名与箭头缺失，纵轴刻度与向量坐标仍可读，故记为图注完整性缺陷而非题意改变。用字：源印「之和」，规范题面作「的和」，同义虚词替换，未改题意。两处均判 passed。",
  "fingerprint": "4da7d4771447e2f6607a5d9875ea0a7dbc23e98abce4f779ddb34d1ee352cba0",
  "impact": "non_blocking",
  "paper_id": "gk-2025-regular-national-1",
  "question_id": "gk-2025-regular-national-1-q06",
  "resume_action": "两处一并处理：一、重导 images/2025-t6-风速.png——现顶边被裁（顶行 7 个墨点触边）且源图 2 纵轴顶端的「y」轴名与箭头整体缺失，重导时须含完整纵轴标注（处置规格参照 2017 两卷图片重导先例）；二、把题干「真风风速对应的向量与船行风风速对应的向量的和」回改为源印的「之和」",
  "source_id": "src-52c0a1ccacd7d0f6a8ba555e22474325194ac4aba7daa75012cc39626bc32ac3",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0051

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed。源 PDF p1（页眉「2024 普通高等学校招生考试 (新高考 I)」、页脚 1207）印作「已知集合 ＝ {x | −5 < x³ < 5}, B = {−3, −1, 0, 2, 3}, 则 A ∩ B =」，集合名「A」在源中整体缺失——900 dpi 视读确认为真缺字而非缺字框，文本层同样无「A」。规范题面补入「A=」；后文「则 A∩B」已经指名该集合，故补入是唯一可复原的，属编辑性勘误。四选项 {−1,0}／{2,3}／{−3,−1,0}／{−1,0,2} 逐字一致。本题无配图。",
  "fingerprint": "f93726a6d65e8b040832501f82acf7cf9b46c260887c5e660e2865d1d7d90d94",
  "impact": "non_blocking",
  "paper_id": "gk-2024-regular-new-gaokao-1",
  "question_id": "gk-2024-regular-new-gaokao-1-q01",
  "resume_action": "本条是编辑性勘误的裁决备案，规范题面不需回改：源印整体缺失集合名「A」，而后文「则 A∩B」使补入唯一可复原。补登进 report.md 的勘误清单，与 2024 新高考Ⅱ Q19 衍文裁决同规格记载",
  "source_id": "src-c914711690e239f541141b43c6da9a999570c6e6ca481633494cab4d80fcb01e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0052

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed。删除源衍文·勘误裁决四要素：① 来源页码：源 PDF 第 2 页（页脚 1210，第三栏）；来源 src-47e5b559bef050d8a1bc792cfc8708d11c2477b98a2a926d00bdc165dd18f11c，源文件 SHA-256 0c36577fb1b30822ae1108ae56fa6ff37edc368d62441bf36d857e458b9a9e1c。② 衍文原文：源印「过点 P_{n−1} 作斜率为 k 的直线与 C 的左支点交于点 Q_{n−1}」，衍字为「左支」之后的「点」；600 dpi 渲染视读与 PDF 文本层双证一致，排除 pdftotext 伪影。③ 删除理由三点：C 为双曲线 x²−y²=m，「左支」是曲线分支而非点，「左支点」在本题中不是已定义对象；「与…左支点交于点 Q_{n−1}」既不成搭配，也与 (2)(3) 对 Q_{n−1}、P_n 的用法冲突；删去该「点」后「与 C 的左支交于点 Q_{n−1}」为唯一可解读版本，故按语法正确版转录，沿用工程早期批次 1 的既有裁决。④ 旧/新题面 SHA-256（对两段纯文本各自取 UTF-8 哈希，与本题 question_text_sha256 字段无关）：含衍文源题面 = c9f06572c1dea84c2adc8551c2102bdbf20bd4420aa996444cf9f6545f7aca28（194 字符）；规范源题面 = d8deef4984c3a7fade9a23e2cfd8b783e5b20493f088e4ec2a40211800a211d0（193 字符）；两串仅差一个「点」字。旁证：求解角色核对规范源现文为「与 C 的左支交于点」，无残留冗余。",
  "fingerprint": "cf57e662aa8f9d7562561b4f7066374e02ae67799eabf42260db3860ef813280",
  "impact": "non_blocking",
  "paper_id": "gk-2024-regular-new-gaokao-2",
  "question_id": "gk-2024-regular-new-gaokao-2-q19",
  "resume_action": "本条是删除源衍文的勘误裁决书面载体，规范题面不需回改。本条的裁决结论已在 report.md 第 50 行「批次 1 勘误与保留意见」第 1 条（「2024 Q19 源 PDF 衍文：原文『与 C 的左支点交于点 Q_{n-1}』多一「点」字…按语法正确版转录」）——勿重复新增条目；如需补强，只应把本 issue evidence 里的四要素（来源页/源文件 SHA-256/衍字双证/旧新题面 SHA-256）补进该既有条目",
  "source_id": "src-47e5b559bef050d8a1bc792cfc8708d11c2477b98a2a926d00bdc165dd18f11c",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0053

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed。源 PDF p1 第 (1) 问印作「求 C 的率心率」，900 dpi 视读确认、文本层同为「率心率」；「率心率」在数学上不是任何已定义量，而椭圆 C 的语境下「离心率」是唯一可解读版本，故改正唯一可复原。A(0,3)、P(3,3/2) 与第 (2) 问（过 P 的直线 l 交 C 于另一点 B、△ABP 面积为 9 求 l 的方程）逐字一致。本题无配图。",
  "fingerprint": "3a06b69a48128524b179519f8f482cfcafc5ff842cdca25c1cf2d1c66dabc352",
  "impact": "non_blocking",
  "paper_id": "gk-2024-regular-new-gaokao-1",
  "question_id": "gk-2024-regular-new-gaokao-1-q16",
  "resume_action": "本条是编辑性勘误的裁决备案，规范题面不需回改：源方块字笔误「率心率」，规范题面作「离心率」，改正唯一可复原。补登进 report.md 勘误清单",
  "source_id": "src-c914711690e239f541141b43c6da9a999570c6e6ca481633494cab4d80fcb01e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0054

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed。题干与四选项（a=−2／(2√2,0) 在 C 上／第一象限纵坐标最大值为 1／y₀⩽4/(x₀+2)）逐字一致；配图 images/2024-t11-曲线.png 结构与标注齐备（F 标签在环内位置与源略有高低差，非内容性）。差异仅一处：源在「其造型」与「可以看作」之间排有一个非文字的丝带形矢量小图标（文本层此处为空白，pdffonts 无对应字符），规范题面未复现，属装饰性省略。",
  "fingerprint": "df1f68c8a162d93a854f33a2fa3efe76dfe3dd752fc14a6bf10b4de64759f69a",
  "impact": "non_blocking",
  "paper_id": "gk-2024-regular-new-gaokao-1",
  "question_id": "gk-2024-regular-new-gaokao-1-q11",
  "resume_action": "如需与源完全对齐，可在题干「其造型」与「可以看作」之间补回丝带形矢量小图标；该图标为装饰性、不承载解题信息，补与不补均不影响作答，优先级低",
  "source_id": "src-c914711690e239f541141b43c6da9a999570c6e6ca481633494cab4d80fcb01e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0055

```json
{
  "affected_paper_ids": [
    "gk-2024-regular-new-gaokao-1"
  ],
  "conflict_code": "figure-trim-artifacts",
  "current_evidence": "沿 b02 的 ISSUE-0020、b03 的 ISSUE-0032 同 type 同 conflict_code 另立新条（图片毛边批量单家族）。题面核对判 passed：该 PNG 顶点与虚实线约定与源一致，毛边不涉内容缺失。毛边实测（导入方复核）：碎片位于 images/2024-t17-四棱锥.png（400×310）顶部，横跨列 120–122（宽 2–3 px）、纵向 5 行（第 0–4 行；其中第 4 行为抗锯齿灰阶，按严格阈值 <128 计则为 4 行），碎片来源是上一行文字「√42/7」中「7」的竖尾。b05 四卷共有 6 道含图题：2024 新高考Ⅰ q11（2024-t11-曲线.png）、q17（本条）、2024 新高考Ⅱ q17（2024-Ⅱ-t17-翻折.png）、2025 全国 1 q06（2025-t6-风速.png）、q17（2025-t17-四棱锥.png）、2025 全国 2 q17（2025-2-t17-翻折四边形.png）。除本条外，其中 5 道经视读确认四边无墨迹触边、无裁切；唯一例外是 2025 全国 1 q06——该图顶边被裁且源图 2 纵轴「y」轴名与箭头整体缺失，属内容完整性缺陷、不属本毛边批量单，已单独登记为 ISSUE-0050。（登记订正记录：本条初版写「顶边残留 2 像素」，把宽度当成了高度，且称「其余含图题（3 道）均无墨迹触边、无裁切」——含图题实为 6 道且 2025 全国 1 q06 恰是反例，两处均已改正。）",
  "fingerprint": "c4442baf0205b8f078983d2a687e41ef02671d2a0a5df10cfa43670e1c85dfbe",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "重导 images/2024-t17-四棱锥.png，去掉顶边残留的 2 像素上一行文字笔画碎片",
  "status": "open",
  "type": "layout-warning"
}
```
## ISSUE-0056

```json
{
  "affected_paper_ids": [
    "gk-2024-regular-new-gaokao-1",
    "gk-2025-regular-national-1"
  ],
  "conflict_code": "footer-raw-pdf-dangling",
  "current_evidence": "沿 ISSUE-0007（b01）、0023（b02）、0028（b03）、0043（b04）同 type 同 conflict_code 另立新条。已由导入方直接核对：`_raw/` 与 `原卷PDF/` 两个目录在库内均不存在，故两条链接都是悬空的。两者形态有别，值得区分：`_raw/` 写在 .gitignore 第 45 行，属「按策略排除、链接注定悬空」；`原卷PDF/` 不在 .gitignore 中，即它既不存在、也不受排除策略覆盖，是纯粹的指向失效。这已是该缺陷第五次出现，且五次全部落在Ⅰ卷/全国 1 卷一侧。",
  "fingerprint": "d886cf68acb3913545789c24a6af48fc1803429f3b0586d5a48e7f55eeda82e1",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "改写两卷 `_试题.md` 文末页脚的原卷指向（PDF 二进制不入库，宜改为指向 source-manifest 的 source_id / upstream_path，或沿用同批两个Ⅱ卷的「试题来源：deekur/gaokaomath（commit `34c13a6`…）」写法）：2024 新高考Ⅰ卷指向 `../_raw/2024_数学.pdf`；2025 全国 1 卷指向 `../原卷PDF/` 目录下的 `2025全国1(...).pdf`",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0057

```json
{
  "affected_paper_ids": [
    "gk-2024-regular-new-gaokao-1",
    "gk-2025-regular-national-1"
  ],
  "conflict_code": "metadata-conventions-drift",
  "current_evidence": "沿 ISSUE-0029（b03 的 2021Ⅰ）、0044（b04 的 2022Ⅰ/2023Ⅰ）同 type 同 conflict_code 另立新条。已由导入方直接核对四份规范源：2024Ⅰ 与 2025 全国 1 的来源行均无 commit 号与 PDF 名，而 2024Ⅱ、2025 全国 2 均有；2024Ⅰ「卷种」写「新高考 I 卷」、2025 全国 1 写「全国 1 卷 / 新高考 I 卷」，均为 ASCII 大写 I。至此 ASCII I 已在 2021Ⅰ、2022Ⅰ、2023Ⅰ、2024Ⅰ、2025 全国 1 连续五卷出现（2025 全国 2 另写「新高考 II 卷」，同为 ASCII），系Ⅰ卷侧的系统性写法漂移而非个别笔误，建议连同 0029、0044 一次性归一。",
  "fingerprint": "a3adf46c291b14fd54d9d711ef22aa0ede1d156aecedec450a82c7ccaec83ecc",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "统一 2024 新高考Ⅰ卷与 2025 全国 1 卷的元数据：一是来源行补上 commit 号与源 PDF 名（现仅「deekur/gaokaomath（CC BY 4.0）」，同批两个Ⅱ卷均为「deekur/gaokaomath（commit 34c13a6，CC BY 4.0）之 <PDF 名>」）；二是把「卷种」里的 ASCII 字母 I 改为罗马数字 Ⅰ",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0058

```json
{
  "affected_paper_ids": [
    "gk-2024-regular-new-gaokao-1",
    "gk-2024-regular-new-gaokao-2",
    "gk-2025-regular-national-1",
    "gk-2025-regular-national-2"
  ],
  "conflict_code": "official-answer-key-unavailable",
  "current_evidence": "沿 ISSUE-0005（b01）、0022（b02）、0030（b03）、0046（b04）约定另立新条。b05 求解角色 76 题全 A、盲核 75 none + 1 resolved，但比对基准是库内 `_答案要点.md`（其本身系库内独立推导），官方发布版未获取。本批证据文本统一使用「库内答案要点」措辞，未出现「官方」误称。注意本批的 2025 全国 1 q08 （ISSUE 见题锚定条）正是库内要点佐证出错的实例，说明这条披露不是形式主义。",
  "fingerprint": "fd4a47439f94c383f632a1ad0fbe2115df09973def9f5f6ff824124cb1cf08fd",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "取得官方发布的标准答案后，逐题比对 b05 四卷 `_答案要点.md`；在此之前答案要点只能声明为库内独立推导的结论，不得表述为官方答案",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0059

```json
{
  "affected_paper_ids": [
    "gk-2024-regular-new-gaokao-1",
    "gk-2024-regular-new-gaokao-2",
    "gk-2025-regular-national-1",
    "gk-2025-regular-national-2"
  ],
  "conflict_code": "frontmatter-regions-unverified",
  "current_evidence": "事实核查协议记录，沿 b04 的 ISSUE-0045 同 type 同 conflict_code 另立新条。本条不在角色提交的清单内，是导入方按 §13.7 交叉核对时按批次一致性补登的——若不登记，读者会误以为 b05 四卷的省份串已核。已由导入方比对四份规范源与 manifest 的 upstream_path：四串与各自上游文件名括号内的省份逐项一致（2024Ⅰ 与 2025 全国 1 均为 11 省、2024Ⅱ 11 省、2025 全国 2 17 省）。但「与上游文件名一致」只证明转录忠实，不证明该串符合现实——上游文件名本身未经核查。结论为未能核实：既不判其为误，也不为其背书；属涉现实、随年份变化的时变事实，不采信参数记忆。b01 的 ISSUE-0006（2017 两卷多列山东）是此类串确会出错的实证。",
  "fingerprint": "e0c192b387ca7181fad48849cac260ba48fd845644b6e6603e6845aa7ada2d6f",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "对四卷 frontmatter 的「适用省份」串做外部定向核查（各年各卷种实际使用省份以考试院/教育部公告为准）；核查前不得据参数记忆增删省份，核查后补出处或更正",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0060

```json
{
  "affected_paper_ids": [],
  "current_evidence": "双盲同见（本工程第三例）。答案独立求解角色 b06-answer-solver-opus 与答案盲核角色 b06-answer-blind-reviewer-opus 在互不知情下对同一处给出同一诊断——两路均指出库内答案要点 C 项的介值论证实质错误：其称「b 从 √3−1 变到 1 时和从 ≈4.72 连续降到 ≈1.36，必过 3」，而 b→(√3−1)⁺ 时 d₃→1（圆 C₃ 相切）故 s₃→0，和的极限是 4√(2√3−3)=2.7250 而非 4.72；且和非单调，先升至 b≈0.797 处的极大 ≈3.1249 再降至 b→1⁻ 的 1.3627，两端均小于 3，介值论证整体失效。两路各自给出的修正论证一致：和在族内两次穿过 3（盲核二分求得两根 b₁=0.746458、b₂=0.866025=√3/2，两处和均为 3.000000000；求解角色独立算得 b≈0.7475 与 b=√3/2），后者恰为 B 项的等弦线，再由 120° 旋转对称性推出无穷多条。答案 BCD 经两路独立验证正确，故盲核记 conflict_status=resolved；本条即该 resolved 状态的承接指针（沿 b04 ISSUE-0033、b05 ISSUE-0049 口径）。",
  "fingerprint": "7be2ba980fba3826b065870e660dc8be1d467fb289f1fe33adad05fa45141c32",
  "impact": "non_blocking",
  "paper_id": "gk-2026-regular-national-1-recall",
  "question_id": "gk-2026-regular-national-1-recall-q11",
  "resume_action": "改写 2026 全国 1 卷（回忆版）`_答案要点.md` 第 11 题 C 项的论证：现用的介值论证（「和从 ≈4.72 单调降到 ≈1.36，必过 3」）两处失效——端点值应为 2.7250 而非 4.72（4.72≈2.725+2，系把 s₃ 相切时的 0 误当成过心弦的直径 2），且该族的和非单调（内部极大 ≈3.125 于 b≈0.797-0.80）、两端 2.725 与 1.3625 均小于 3；应改用「和在族内先升过 3 再降回」的双穿越论证（两根 b≈0.7465 与 b=√3/2，后者恰为 B 项的等弦线），再由构型绕中心 120° 的三重对称性得无穷多条。另 A 项叙述只点名 k=√3/3、未提对称的 −√3/3（对判 A 为假已够，属叙述不全）。答案 BCD 本身正确，只需改佐证",
  "source_id": "legacy:docs/exams/2026/2026_数学真题_试题.md",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0061

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed：几何信息本身无损——八个标注 C₁/A₁/B₁/E/C/A/D/B 齐全，实线（A₁B₁、A₁C₁、B₁C₁ 上沿与 A₁A、B₁B 侧棱、AB 底边）与虚线（C₁—C、C₁—A、A—C、C—B、E 所在的 A—C₁ 段）走向与 PDF 原图一致，A₁ 被切的笔画放大后仍可辨认。缺陷是越界毛边加边缘微裁：墨迹包围盒 rows 18-349 / cols 0-319（画布 320x350）。判据与既有 ISSUE-0020/0032/0055 的图片毛边家族同类，但本批每卷只有一张问题图、无需批量单，故按 T19「题锚定一律回填」口径登记为逐题条目而非卷级批量单。",
  "fingerprint": "e980dd4d68d234f5b864e6aa5262d63a2769cb3bd186e74b8a6f040cefcbd7f6",
  "impact": "non_blocking",
  "paper_id": "gk-2026-regular-national-1-recall",
  "question_id": "gk-2026-regular-national-1-recall-q15",
  "resume_action": "重做 images/2026-t15-棱柱.png：现件不是重绘件而是 PDF p2 的页面截图裁剪，图内上方混入题干残行「5．如图，在直三棱柱 ABC−A₁B」、下方混入其后正文行「(1)证明：」的顶部像素，且末行 31 px、左列 16 px、右列 9 px 触及画布边缘，A₁ 标注中 A 字左侧笔画被左缘切去一小截。宜按其余各卷的做法改为 TikZ 重绘",
  "source_id": "legacy:docs/exams/2026/2026_数学真题_试题.md",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0062

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed，本卷 19 题中唯一一处非标点性的实词改动（其余 9 处表述出入均为标点/记号/分值补注类）。600 dpi 渲染视读确认 PDF 中该「时」字确实存在，非文本层伪影；「…时或…时」为并列结构，删去前一「时」后语义不变、不改作答方式，故判非实质。",
  "fingerprint": "644acf8a87a89bf2b33e7ab3eeb71ef77d7211227034975995d598419ebfb3b4",
  "impact": "non_blocking",
  "paper_id": "gk-2026-regular-national-1-recall",
  "question_id": "gk-2026-regular-national-1-recall-q17",
  "resume_action": "本条是编辑性裁决备案，需内容任务定夺：规范源第 17 题删去了 PDF 有的一个「时」字（PDF「当且仅当投中 1 次时或 N 次均未投中时」→ md「当且仅当投中 1 次或 N 次均未投中时」）。按忠实转录纪律宜补回；若维持删字，须补登进 report.md 的勘误清单并说明理由。注意本处与 ISSUE-0047 方向相反：0047 是「源缺字、md 照录不改」，本处是「源有字、md 删字」",
  "source_id": "legacy:docs/exams/2026/2026_数学真题_试题.md",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0063

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面核对判 passed。重绘件整体质量良好：四边无触墨（墨迹包围盒 rows 23-541 / cols 23-873，首末三行三列均零墨，无裁切、无邻栏文字混入）；与 PDF 原图 600 dpi 逐格比对，纵轴刻度 0.005/0.01/0.015/0.02/0.025、横轴刻度 345…425、轴标「频率/组距」与「时间/天」、原点 O 与折断号均齐备且数值相同，各组高度 0.005/0.01/0.02/0.025/0.015/0.015/0.005/0.005 与原图逐格相同，八组频率合计 1.000 自洽。缺失的两条分隔线是等高相邻柱的内部边界，不改变任何一段的 频率/组距 值与横轴分点；三处设问所依赖的区间（365-375、375-385、345-365）全部不在受影响区段，题目可按原样作答。像素级核验：重绘件在 x≈523、x≈665 两列无竖直墨线，而 x≈169/240/310/381/452/594/736 各列有。",
  "fingerprint": "4b0d47b3c720f558bf3870f7a3a1901d738cf85fada7a82022cdb8e0f761de93",
  "impact": "non_blocking",
  "paper_id": "gk-2026-regular-national-2",
  "question_id": "gk-2026-regular-national-2-q15",
  "resume_action": "重绘 images/2026-2-t15-直方图.png 时补回两条竖直分隔线：PDF 原图把 385-395 与 395-405 画成两个独立矩形（395 处有分隔线）、405-415 与 415-425 亦然（415 处有分隔线），重绘件省略了这两条等高相邻柱之间的分隔线，画成 385-405、405-425 两段连续水平线",
  "source_id": "src-f7b5dfbecde104bf273ee89c47131e86300dd9f8f25846d23992ce12fc89a609",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0064

```json
{
  "affected_paper_ids": [
    "gk-2026-regular-national-1-recall",
    "gk-2026-regular-national-2"
  ],
  "conflict_code": "footer-raw-pdf-dangling",
  "current_evidence": "沿 ISSUE-0007（b01）、0023（b02）、0028（b03）、0043（b04）、0056（b05）同 type 同 conflict_code 另立新条。已由导入方直接核对两份规范源末行与目录存在性。与 b05 的 2025 全国 1 卷同为 `../原卷PDF/` 形态（该目录不在 .gitignore 中，即既不存在、也不受 PDF 排除策略覆盖，属纯粹指向失效），区别于 `_raw/` 那一支的「按策略排除、注定悬空」。该缺陷至此已第六次出现。",
  "fingerprint": "87032cd6e63d1e4428336b4d1492a505313f9512a12b07728f41820e71e0f566",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "改写两卷 `_试题.md` 文末页脚的原卷影印件链接（PDF 二进制不入库，宜改为指向 source-manifest 的 source_id / upstream_path）：卷 1 指向 `../原卷PDF/2026全国1(...).pdf`、卷 2 指向 `../原卷PDF/2026全国2(...).pdf`，而 `原卷PDF/` 目录在库内不存在",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0065

```json
{
  "affected_paper_ids": [
    "gk-2026-regular-national-1-recall",
    "gk-2026-regular-national-2"
  ],
  "conflict_code": "scoring-notes-not-in-source",
  "current_evidence": "沿 b03 的 ISSUE-0026 同 type 同 conflict_code 另立新条。事实核查协议记录：两卷上游 PDF 全卷无任何分值标记（题面核对角色对两卷逐页视读确认），而两份规范源均补有段首说明行与逐题分值补注。内部自洽性已核：解答题 13+15+15+17+17=77 与段首「共 77 分」相符，加单选 8×5=40、多选 3×6=18、填空 3×5=15 合计 150，无加法矛盾。但全部分值信息在本批来源中无对应，官方赋分规则【未能核实】——未能核实不等于错误，不得据此断言，也不得据参数记忆补全。",
  "fingerprint": "61d2e5abceeb95f6600d84205fd59f85cb97a89b24689b85f21dc10464b30f33",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "对两卷的分值信息做定向核查后决定去留：或找到权威来源（官方试卷扉页说明/考试院文件）为其背书并注明出处，或改写为不声称分值的中性提示，或整体删除。涉及各段段首说明行（如「本题共 5 小题，共 77 分」）与五道解答题的「（13/15/15/17/17 分）」补注。禁止据参数记忆补全",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0066

```json
{
  "affected_paper_ids": [
    "gk-2026-regular-national-1-recall",
    "gk-2026-regular-national-2"
  ],
  "conflict_code": "official-answer-key-unavailable",
  "current_evidence": "沿 ISSUE-0005（b01）、0022（b02）、0030（b03）、0046（b04）、0058（b05）约定另立新条。两卷 `_答案要点.md` 均自述「非官方标准答案」，盲核角色据此把一切官方口径的断言标为【未能核实】。b06 求解角色 38 题全 A、盲核 37 none + 1 resolved，比对基准均为库内要点。卷 2 采纳件是否为官方发布版同样【未能核实】。两路证据文本统一使用「库内答案要点」措辞，未出现「官方」误称。",
  "fingerprint": "5184cb997cbf7cd3b8bcddce653f72c1c8311dcc55bc332d0bd549469e613068",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "取得官方发布的标准答案后，逐题比对两卷 `_答案要点.md`；在此之前答案要点只能声明为库内独立推导的结论，不得表述为官方答案。卷 1 为回忆版，官方答案的可得性还受 ISSUE-0001 制约",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0067

```json
{
  "affected_paper_ids": [
    "gk-2026-regular-national-1-recall",
    "gk-2026-regular-national-2"
  ],
  "conflict_code": "frontmatter-regions-unverified",
  "current_evidence": "沿 b04 的 ISSUE-0045、b05 的 0059 同 type 同 conflict_code 另立新条。事实核查协议记录：题面核对角色确认两卷 PDF 正文均不含任何省份信息，省份串只见于上游文件名与规范源自述（frontmatter 与正文引用块两处）。「与上游文件名一致」只证明转录忠实，不证明符合现实；官方原卷的适用范围【未能核实】。b01 的 ISSUE-0006（2017 两卷多列山东）是此类串确会出错的实证。",
  "fingerprint": "38fe7464c834741feb642cdb2ba6413287dd9c5891868e6f436d384de846284c",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "对两卷 frontmatter 与正文的「适用省份」串做外部定向核查；核查前不得据参数记忆增删省份，核查后补出处或更正",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0068

```json
{
  "affected_paper_ids": [
    "gk-2026-regular-national-1-recall",
    "gk-2026-regular-national-2"
  ],
  "conflict_code": "metadata-conventions-drift",
  "current_evidence": "沿 ISSUE-0029（b03）、0044（b04）、0057（b05）同 type 同 conflict_code 另立新条。⚠️ 本条不在角色提交的清单内，是导入方按 §13.7 与上一批卷级 issue 家族逐个对表时补登的——b05 家族五条（0055 毛边/0056 悬空链接/0057 frontmatter/0058 非官方/0059 省份串）中，唯独 frontmatter 一条在本批清单里整类缺席。已由导入方直接核对两份规范源确认缺陷存在。至此 ASCII 罗马数字写法漂移已在 2021Ⅰ、2022Ⅰ、2023Ⅰ、2024Ⅰ、2025 全国 1、2026 全国 1/2 连续出现，建议连同 0029/0044/0057 一次性归一，勿逐卷修。",
  "fingerprint": "c6ed8122bf27e705b38a247792011e6576daaae32990966b474c439760263a9e",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "统一两卷元数据：一、卷 1 的来源行补上 commit 号与源 PDF 名（现仅「deekur/gaokaomath（CC BY 4.0）」，卷 2 已有 commit 34c13a6 但同样缺 PDF 名）；二、把「卷种」里的 ASCII 字母 I / II 改为罗马数字 Ⅰ / Ⅱ（现作「全国 1 卷（新课标 I 卷）」「全国 2 卷（新课标 II 卷）」）",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0069

```json
{
  "affected_paper_ids": [
    "gk-2026-regular-national-1-recall",
    "gk-2026-regular-national-2"
  ],
  "conflict_code": "answer-key-argument-gaps",
  "current_evidence": "沿 b03 的 ISSUE-0031 同 type 同 conflict_code 另立新条。六处中前五处出自答案独立求解角色 b06-answer-solver-opus 的 A 级比对说明，第六处（λ 命名复用）出自答案盲核角色 b06-answer-blind-reviewer-opus 在卷 2 第 18 题记录里的【低级观察】，两者均可在本批 .work 中逐字核对；第六处的底层缺陷另经导入方在 tracked 文件独立复核确认——2026/2026_数学真题_全国2_答案要点.md 第 278 行的 λ=t₀/(x₀+t₀)（AO 上的比例参数）与第 282 行的 λ=(t₀²−2)/2（x² 项系数）确系同一小问中的两个不同对象。卷 1 第 11 题的要点硬伤不并入本条，已单独登记为题锚定条目 ISSUE-0060（双盲同见）。（登记订正记录：本条初版称「答案盲核角色除第 11 题外未另提要点缺陷」，该句不实，已删除；漏检根因是检索面只覆盖了 schema 承载的 answer-solve evidence，而盲核 evidence 系角色自加的非 schema 字段——见本批报告 §8 记录的机制债。）",
  "fingerprint": "c323cd2a8d11909b0513c66d71eeeac4824ccfaff9bbab8bbd2444f42d6d19a8",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "逐处复核并改写（五处均不影响答案正确性）：一、卷 1 第 17(1) 题要点标「答案：见解析版」，但紧接着就在同一处给出了完整分布列，标注与内容不符；二、卷 1 第 18 题由 1+k₁k₂=1/4>0 只能断定两直线夹角为锐角，而 ∠PQR 是射线 QP 与 QR 的夹角，严格说还需说明二者同为锐角；三、卷 1 第 19 题未点明「x₁<0<x₂ 与 f(x₁)≤f(x₂) 相斥」即直接分三种情形，属叙述省略；四、卷 2 第 18 题「A²/B²=2t₀²/(t₀²−2)>2>1」只在 |t₀|>√2 分支成立，却写在分支讨论之前（0<|t₀|<√2 时该比值为负），属排版顺序问题；五、卷 2 第 18 题称被去掉的两点是「A 取椭圆左右顶点时的像」略不准确——y₀=0 时 B 与 O 重合、直线 GB 与 AO 重合，P 根本不存在，那两点是 y₀→0 的极限位置而非像；六、卷 2 第 18 题在同一小问中用符号 λ 先后指代两个不同对象——要点第 278 行的 λ=t₀/(x₀+t₀) 是 AO 上的比例参数，第 282 行的 λ=(t₀²−2)/2 是 x² 项系数，属命名复用，宜为其一改名（如 x² 项系数改记为 A）",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0070

```json
{
  "affected_paper_ids": [],
  "current_evidence": "既有三路证据确认题源 PDF 的 C—B 为虚线而旧 TikZ 源误画为实线。现 canonical 项目图源 math-gaokao-latex/2025_全国2卷/figures/f2025g2_t17_fold.tex 与共享图源 math-gaokao-2017-2026/figures/f2025g2_t17_fold.tex 均已改为 \\draw[dashed] (C) -- (B);。phase0-b05 当前正式构建的试题版第3页、印刷版第3/17页、解析版第23页以120dpi复核，C—B均显示为虚线，标注完整且未见裁切。原 Markdown 引用的 images/2025-2-t17-翻折四边形.png 当前不在 Git 树中（此前已移除）；本次修正并验证的是 canonical TikZ 源及 PDF 输出，不声称该 PNG 已重建。",
  "fingerprint": "4b1782752dd28caa4cc8c219a32b2f94a82f051b3811a6b7667961fce19fe84b",
  "impact": "non_blocking",
  "paper_id": "gk-2025-regular-national-2",
  "question_id": "gk-2025-regular-national-2-q17",
  "resume_action": "已修正两份共享 TikZ 源并在当前正式 PDF 中复核 C—B 虚线；历史 Markdown PNG 不在仓库中，未在本阶段重建。",
  "source_id": "src-63d8cf8aeded86d1dc644b80483c817de4f9ba7d312f117942a408b916bcc94d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0071

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "5ed9e3048bca6625ae9c480e9e7493718b1084faa2dba677ee1156701d0723c0",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "ab3129a0a3724df5c112fc2282dc6d1cbf1ed8147a19bcd018262d6cb0e3bec7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0072

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "86dc97900ab666d76a9da726182bfc8ccf4464ba596b7ede12fe376a1dcb1a57",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "ab3129a0a3724df5c112fc2282dc6d1cbf1ed8147a19bcd018262d6cb0e3bec7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0073

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "54d0c786e13a5af3c46ae9e7dee3e2d2f80ba007bb23945c97da444ee6b87aee",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "ab3129a0a3724df5c112fc2282dc6d1cbf1ed8147a19bcd018262d6cb0e3bec7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0074

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "4898b1105f8176c8e91c81144eb88c0e8d4c05fab8212528fef448eb40a97f3b",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "ab3129a0a3724df5c112fc2282dc6d1cbf1ed8147a19bcd018262d6cb0e3bec7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0075

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "option_formula_alignment",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "3d29d4458f4240738b94050d0d8afbfe97dde2402e44608b40783bc7f2186d63",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 24,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "ab3129a0a3724df5c112fc2282dc6d1cbf1ed8147a19bcd018262d6cb0e3bec7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0076

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "b7fa73c528ec19513b817fff9902272be4a9fa83e6c3be85018f20c13f715f26",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 26,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "ab3129a0a3724df5c112fc2282dc6d1cbf1ed8147a19bcd018262d6cb0e3bec7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0077

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2d915330-13bc-4410-9986-ad8a7c9686b2",
  "check_code": "option_formula_alignment",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "c63c6c5146c01c26010f3d5156d6e8baa56b9c35847203a4114e88d377d29120",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 32,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "4bc445c6d6245ad4a7eae4675e661ad87faa878df37ae653b42cf0f7ad36d4e8",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0078

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "32fdc8f5c572610e2c7b770df063c4489b6eaf7768ee7620f2df21b2bbe90831",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "ff50ccf7aedf04f55322a9854b6be616e650f624742fc0d07e7af81cd0ecbfca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0079

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "a87ef0fb58c8976910c6c6a06393f0897c887bffc1d68f588ee136081d08a42e",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "ff50ccf7aedf04f55322a9854b6be616e650f624742fc0d07e7af81cd0ecbfca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0080

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "2b3d28a9f05d406976fce53ae3dc4257d504f421b1cd68fadf3d5601a9e114bb",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "ff50ccf7aedf04f55322a9854b6be616e650f624742fc0d07e7af81cd0ecbfca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0081

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "0167ae2992b31dec7a1e2e992d243fc68c5291975507f6b1c32b130350e5a7a0",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "ff50ccf7aedf04f55322a9854b6be616e650f624742fc0d07e7af81cd0ecbfca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0082

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "option_formula_alignment",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "18234334141ce660d77aa36d30b60ad5b327737e14f85918815626d4be3c240f",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 24,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "ff50ccf7aedf04f55322a9854b6be616e650f624742fc0d07e7af81cd0ecbfca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0083

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "6c667039cbc2402d59ec45a49de279d9a903a1ef25be45b57b0fb3b3887a8100",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 27,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "ff50ccf7aedf04f55322a9854b6be616e650f624742fc0d07e7af81cd0ecbfca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0084

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "31e746a4-2629-42d8-9c86-92314a63e71a",
  "check_code": "option_formula_alignment",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "ab945cd9b317f7d3cca08815ad1583377bf2033741c00becc99008d8fa7e76b0",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 33,
  "paper_id": "gk-2017-regular-national-1-science",
  "pdf_sha256": "c6034dc4abd26b022a7d853fa30d46e5546f0fb3feaf152f1ebc507fc169cb42",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0085

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "571bf210-f867-44af-a4ac-f4a2442ed6ee",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "4c3a6bae1cfda56bd131bd0c5e214b96d83469f2f4fb293552c84851153ec277",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 20,
  "paper_id": "gk-2018-regular-national-1-arts",
  "pdf_sha256": "36cc3d6c8995706e128a88a831a1cad00a66038ca8b89c2f33aa4f7e562ad8c8",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0086

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "60371fd7-bc04-468a-8607-dcb9f8bf328e",
  "check_code": "option_formula_alignment",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "e02456fd7eca082fd39145f5ac7873700d1a82d74677c1667bb5c69c40beb2ec",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 21,
  "paper_id": "gk-2018-regular-national-1-science",
  "pdf_sha256": "3306ca55d47701bb3d9ed0fe4bdc06cffbb7a5f057d27596bc70c0cf9f7426b9",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0087

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "60371fd7-bc04-468a-8607-dcb9f8bf328e",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "e33c25f5cd7c7a263209c5910fec84e82d2c7751b15faf2147a1d69252e27385",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 23,
  "paper_id": "gk-2018-regular-national-1-science",
  "pdf_sha256": "3306ca55d47701bb3d9ed0fe4bdc06cffbb7a5f057d27596bc70c0cf9f7426b9",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0088

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "60371fd7-bc04-468a-8607-dcb9f8bf328e",
  "check_code": "option_formula_alignment",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "4affbf2de1c5337b49f074b2040ca803a2212efaae320e8af8e026ca5708516c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 28,
  "paper_id": "gk-2018-regular-national-1-science",
  "pdf_sha256": "f2a5ebf8d3facfe40201207b322f2dc816ba9c46c52e5954a818256f5ec1bce4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0089

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "8fcb38d3e90c08ae9c7146cd696060dadb7666e0f80763b0e60792fae4688ea2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0090

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "b66b6932e5ab1c3a1562dd7c52abb77e11c2d29206a4c40f182da1f7aebd7160",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0091

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "004094877aa58825daf54a949828d0b2b0b043c4ad54f292437f34d0e2d5761e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0092

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "b33bf6c48975bb5a38d2109932ba74214ff7136dfcccbe85bfb129ad51116995",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0093

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "9b4049cba29a3f78d0d1dc12ea4e94824bb335752bbd637166597028c372bd11",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0094

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "0f1fae6c4cb8dd217b8740f5e825ab8c2b4d39a2f85b6db2fc983ae03663e09c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0095

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8b6a7e88d8b56479ffd3461d79772eb79d40ab9f8060977424f329443bcbd23c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0096

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "faf852d6ce4682eb58d83ec6eade1c40fe6cbe27cb358a0484b363ed47354ec7",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0097

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "5d33da07b8a5891b37bda1e6a3219fca34f55ae6005429280ca4982a34dcf3ce",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0098

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "1e6699aa8aeba16d7556e94431155d9f051686e59971471ad84492e79c998612",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0099

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "58565dcdd3e63e9b3d871f8547389ba642fdcd61350fbd055d11c20ecb00cd54",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0100

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "4401ebc430b7971244637bb82995cb737736bbcf6a237e1cc52243f4fc863173",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0101

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "ac40bfd5bd3bc1bb68da707b242686f7361a7566a2254fb73801f359eb27a721",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0102

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "f87859c9bf812694375447dd080042878434cbe963dd713ce42e0a248fc9472d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0103

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "1ad7a52c6be8f9d87fe32fbcf6b9bb8c16624a169a5852430aa5e295fe410b70",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0104

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "b07bf7bd152f5504e5214c1fa2a11a938f65c31ab620c2cb2ca1d174a855171d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0105

```json
{
  "affected_paper_ids": [],
  "conflict_code": "pdf-header-national-ii-vs-national-a",
  "current_evidence": "上游 PDF 页眉逐字为“2021 普通高等学校招生考试（全国卷 II 文）”，而 source-manifest 与规范源按上游文件名及既有目录身份登记为“2021 全国甲卷文科”；当前尚无独立权威证据解释该卷别标签冲突。",
  "fingerprint": "d75a42e62638e243e074663febd437611be4aa6d600583446ed5f961244003e6",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-a-arts",
  "resolved_evidence": "固定上游 PDF 第2题“农户家庭年收入”和第6题“青少年视力”与人民网转载的教育部考试中心 2021 高考数学命题评析逐题对应，后者明确分别为全国甲卷文、理第2题及甲卷文科第6题；该 PDF 同时具有 A3 横排、汇编页码 1147/1148 和非官方简化题签，故页眉“全国卷 II 文”记为非官方重排汇编标签。未能核实其为模板编号或防伪编号，不作该断言。来源：http://edu.people.com.cn/n1/2021/0608/c1006-32125641.html",
  "resume_action": "无需动作；卷种按题目内容与教育部考试中心逐题评析认定，汇编页眉不作为卷种字段",
  "source_id": "src-0e4e7506220e2969389efd998364e538cea0fb7e552b9f06b1479647e9634629",
  "status": "resolved",
  "type": "identity-ambiguous"
}
```
## ISSUE-0106

```json
{
  "affected_paper_ids": [],
  "current_evidence": "上游 PDF 第 2 页第 23 题作图网格在 y 轴两侧大致对称；规范题面引用的 images/2021甲文-t23-网格.png 右侧仅约 4 格、左侧约 9 格，右半网格明显被裁掉，属于实质图形转录缺陷。",
  "fingerprint": "214be4bb191cc78e44d8353962842664c8cc37281697613b96008a1f75077dc4",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-a-arts",
  "question_id": "gk-2021-regular-national-a-arts-q23",
  "resolved_evidence": "已逐页对照固定上游 PDF 第 2 页，并将正式 TikZ 网格修正为左右、上下各 8 格；规范题面继续使用稳定图名，由生成器映射到 f2021jw_t23_grid.tex。",
  "resume_action": "无需动作；图形已按固定上游 PDF 重新核验并矢量重绘",
  "source_id": "src-0e4e7506220e2969389efd998364e538cea0fb7e552b9f06b1479647e9634629",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0107

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "e0ab8426ae2b98a6065b1cfa571c50991659d20b11e26976a69f3cc6101f3ff1",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1956-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0108

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "de71579e5626c696685b1324d6d54fec720a60462a154704d9caf1a816cb4825",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1956-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0109

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "e1b9317e27cd6eab3484780e3076a4e1789b92a5d28cd5822d33953920c1f119",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1956-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0110

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "68ea9c4668185e694f9896b82e5745ad3c2d0f3385de90f822728e61955b981a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1956-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0111

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "db7d5217054f9d6763aa7ae2677ecd222f8a518b7a3c05e464cb909e04304773",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1961-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0112

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "893d32e9fa5ff725700f7a85e4cb466f05a2993d62b01058f1c521451d5995e6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1961-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0113

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0122c92a-ed18-4a1f-99e4-f16c7b454509",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "76e2921aca58988db5a05302efd647ced0cf155b9a99eb2958371602c423baec",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 14,
  "paper_id": "gk-2021-regular-national-a-arts",
  "pdf_sha256": "438ea03525b9e3d3dbd9a45d77f5ac37183f8da197c54e920dba0e61f660b159",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0114

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0122c92a-ed18-4a1f-99e4-f16c7b454509",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "fbcabf1b441f777bd9a003b4d5d9a952c5d6d14e060619f15f7ae0344b15097f",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 16,
  "paper_id": "gk-2021-regular-national-a-arts",
  "pdf_sha256": "438ea03525b9e3d3dbd9a45d77f5ac37183f8da197c54e920dba0e61f660b159",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0115

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "990228735e9940b9151128d4cad0e39ad8988c08cae9f5d8b35e161d27837ed2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-a-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0116

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "dbb9526d0cf9cc90db9ddab705437d9efde2cc38fe2533e75937329a94788982",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-a-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0117

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "45bf0881eb26de5aebf73e882580c41996c4a73182a06f811847df0e17d167ef",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1965-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0118

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "d6876df76706882540d0a2ecaaf0abaae53feb8b0b67bd69a1892ef68d269b48",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1965-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0119

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "2abc569ae32b7f2ddba78efeeccbf50f471f70044fd1ade348853d1bc8ce556c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1957-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0120

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "9370a3badcccbc5d04dcd393728ca1d2b60a794afded403ff362b7d61497a29c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1957-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0121

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "6dc19ed42a5afedb7ed2d5894417fe48892be205dd73b71c6af1d922157fe848",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1959-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0122

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "863eb381e2c1736d2196c6fc88ea82b7d1d80650ad99dcfa2fdfd73abb7bf291",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1959-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0123

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "3667421b2d1a58752fb15ccaa51f3fca9dbadfab08a324dd5bb106078e3aa275",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1962-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0124

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "cff4822a9dda03b006e40a6dd7f913748876e2db404714dcaf809eac192a6e3e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1962-regular-national",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0125

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页高分辨率复核仍确认题干印作“过 D 作 BC 的平分线交 AC 于 E”，而图中 D-E 线段与 BC 同向平行；同年上海理科固定源的同题印作“过 D 作 BC 的平行线”，公开同题转录也作“平行线”。规范源据此采用“平行线”，固定扫描异文保留。",
  "external_evidence": "直接核查同年上海理科固定源对应题面：该卷固定源规范转录第 2 题作“过 D 作 BC 的平行线”；另核查公开 Daxmate/math 仓库的 1977 上海理科转录（https://github.com/daxmate/math/blob/main/1977shanghai/shanghai1977.tex），其第 2 题同样明确作“平行线”。该公开转录不是官方原件，但与文科固定扫描图示 DE∥BC、以及独立几何可解性一致；文科公开题面页（https://www.doc88.com/p-4149997998535.html）只作为同卷种身份的辅助线索，未将其受限预览当作唯一证据。",
  "fingerprint": "38050afbb46610362059f5e3637d8955596a041b9d53d371b29ec2725dcb2f3d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanghai-arts",
  "question_id": "gk-1977-regular-shanghai-arts-q02",
  "resolution": "固定扫描异文保留为“平分线”；同年上海理科固定源的同题与公开 Daxmate 转录均为“平行线”，且文科图示为 DE∥BC，规范题面已按交叉核定采用“平行线”。",
  "resume_action": "已完成交叉核定；规范题面采用“平行线”，固定扫描异文已留档，并完成答案、解析、生成、构建与视觉复核。",
  "source_id": "src-21ede2f4d2feea45ce0c013e43c589d4c6268b39e22ee860d9939b045f6a197c",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0126

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描第 2 题字面为“BC 的平分线”，与图示 DE∥BC 不一致；同年上海理科固定源与公开同题转录均作“BC 的平行线”。按该交叉核定读法，DE=ab/(a+b) 的独立推导与题面相容。",
  "external_evidence": "直接核查同年上海理科固定源对应题面：第 2 题作“过 D 作 BC 的平行线”；公开 Daxmate/math 转录（https://github.com/daxmate/math/blob/main/1977shanghai/shanghai1977.tex）同样作“平行线”。另核查公开同构题的完整题解（https://www.1010jiajiao.com/czsx/shiti_id_1da1f97104c4e5b74a707b76c0a5b992），其按 CD 为角平分线、DE∥BC 推出 DE=ab/(a+b)；该页不是 1977 原卷，只用于独立核对答案公式，不作为历史题面身份依据。",
  "fingerprint": "002076828588d3eec0048a3aa120fdb89846810732603f2fedfe41163b2729e4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanghai-arts",
  "question_id": "gk-1977-regular-shanghai-arts-q02",
  "resolution": "按同年上海理科固定源、公开同题转录与文科图示交叉核定，规范构造为 DE∥BC；独立由角平分线定理和相似三角形复算 DE=ab/(a+b)，答案要点与解析已同步更新。",
  "resume_action": "已完成构造核定、独立答案复算，并完成答案、解析、生成、构建与三角色核验记录。",
  "source_id": "src-21ede2f4d2feea45ce0c013e43c589d4c6268b39e22ee860d9939b045f6a197c",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-0127

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1977天津.pdf》（manifest source_id src-fe8066472767be7a1d3a8466092df82bc08c125c6b5317f8d5334c617119ff24，SHA-256 db7a8e6ccf1d9ab5a673062ad0f15b1e1db3136eeb26f2ef05c3a521e9736d3d）第 1 页高清渲染显示完整设问“在什么条件下，y/(2x)”并列出四项“是正数、是负数、等于零、没有意义”，并非缺页或残缺。21 世纪教育网的 1977—2021 数学汇编也复现同一完整题面（https://zy.21cnjy.com/13497153）；公开独立 LaTeX 整理件的天津卷源文件亦逐字写作同一设问（https://raw.githubusercontent.com/daxmate/math/main/gaokao/tianjing1977.tex）。原问题将“条件”误判为缺失。",
  "fingerprint": "bf1c895f6d8c21e4bbba57cd71d93051b4418f34ebabe521bef76dc5afa88ffb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tianjin",
  "question_id": "gk-1977-regular-tianjin-q01",
  "resolution": "已确认题面四项分类设问完整，无需补写题干；已按分母 2x 的符号规则修正解析并完成独立答案推导。",
  "resume_action": "已确认设问完整并修正题面判定记录，无需继续动作。",
  "source_id": "src-fe8066472767be7a1d3a8466092df82bc08c125c6b5317f8d5334c617119ff24",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0128

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1977天津.pdf》（manifest source_id src-fe8066472767be7a1d3a8466092df82bc08c125c6b5317f8d5334c617119ff24，SHA-256 db7a8e6ccf1d9ab5a673062ad0f15b1e1db3136eeb26f2ef05c3a521e9736d3d）第 1 页高清渲染显示完整设问“在什么条件下，y/(2x)”及四类结果；21 世纪教育网汇编复现同一题面（https://zy.21cnjy.com/13497153）。公开独立 LaTeX 整理件 https://raw.githubusercontent.com/daxmate/math/main/gaokao/tianjing1977.tex 给出对应分类答案：xy>0、xy<0、y=0 且 x≠0、x=0。该答案也可直接由当前完整题面独立推导。",
  "fingerprint": "e009d5c9f80a8158077909d5e32eb705b8fc4e8c54f5edbc9c9dbe5ad1de9393",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tianjin",
  "question_id": "gk-1977-regular-tianjin-q01",
  "resolution": "已将第 1(1) 的答案要点改为四类条件，并补入分类解析；已重跑答案生成、provenance、正式构建与视觉复核。",
  "resume_action": "已补入四类条件并完成盲核与 provenance 更新，无需继续动作。",
  "source_id": "src-fe8066472767be7a1d3a8466092df82bc08c125c6b5317f8d5334c617119ff24",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-0129

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页高清局部复核确认第 1(3) 根式印作 sqrt((-1/16)^(-1/2))；第 2 页源解答却将同一处按 sqrt((1/16)^(-1/2)) 计算并给出 -72。严格按实数题面原式没有实数意义，源解答与题面不一致。",
  "external_evidence": "本轮直接核查了中国教育在线的 1977 年试题汇总页（https://gaokao.eol.cn/shiti/moniti/201506/t20150603_1266777.shtml），页面明确只列部分省市，未提供内蒙古数学卷；另核查了公开预览的《1977 年全国各地普通高等学校招生考试数学试题及答案》（https://max.book118.com/html/2023/0404/8006003067005053.shtm），可见预览从北京市文科卷开始，剩余页面需付费，未出现可核对该题根式底数的内蒙古原卷或勘误。搜索摘要与视频页未提供可核对的同版题面，因此没有足够外部证据授权把 -1/16 改成 1/16。",
  "fingerprint": "838fbcd5e4987ef501a156e0fe14815380193099406e3a46d0b0334a800f567c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-inner-mongolia-arts",
  "question_id": "gk-1977-regular-inner-mongolia-arts-q01",
  "resume_action": "取得更清晰源卷或权威勘误，确认第 1(3) 根式的底数是否应为 1/16；确认后重做答案、盲核与 provenance，在确认前保留题面原式和源解答 -72 两种证据。",
  "source_id": "src-1b8b3b5dc1b32466b26aa70873f050666dfa6eaf27c32d708f030c58535f823b",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0130

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 3 页高清复核确认圆台全面积的源解答在公式 pi(36+144+180) 后印作约 113 cm^2；按源卷给出的半径 6、12、母线 10 与 pi=3.14 独立复算为 360pi=1130.4 cm^2，源解答末值漏写一个数量级。",
  "external_evidence": "本轮直接核查了中国教育在线的 1977 年试题汇总页（https://gaokao.eol.cn/shiti/moniti/201506/t20150603_1266777.shtml），页面明确只列部分省市，未提供内蒙古数学卷；另核查了公开预览的《1977 年全国各地普通高等学校招生考试数学试题及答案》（https://max.book118.com/html/2023/0404/8006003067005053.shtm），可见预览从北京市文科卷开始，剩余页面需付费，未出现可核对该题全面积末值的内蒙古原卷或勘误。搜索摘要与视频页未提供可核对的同版题面，因此只能保留源印刷值 113 与独立复核值 1130.4 并列，不能据此改写源解答。",
  "fingerprint": "9a62a0716585318205d8bfdf630aeaacd355e29b0a361489151787e3504405a2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-inner-mongolia-arts",
  "question_id": "gk-1977-regular-inner-mongolia-arts-q02",
  "resume_action": "取得更清晰源卷或权威勘误，确认第 2(2) 全面积末值是否应为 1130.4 cm^2；确认后重做答案、盲核与 provenance，在确认前并列保留源印刷值 113 与独立复核值 1130.4。",
  "source_id": "src-1b8b3b5dc1b32466b26aa70873f050666dfa6eaf27c32d708f030c58535f823b",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0131

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1977 江苏卷》（manifest source_id src-d9a8910d628c7c1fa11a8b0f3184baa39d3a78411a2ebeea69a7461c52754608，SHA-256 ce3d55b0f282697ce3407bcfac4c542956de3e619c2f1ce71332b1fab20e75e8）单页高清复核确认第 1(1) 末项印作 (-27/8)^(-1/2)，负数的负半次幂在实数范围内无实数定义。独立 Daxmate LaTeX 整理件（https://raw.githubusercontent.com/daxmate/math/main/gaokao/jiangsu1977.tex）改写为 (-27/8)^(1/3) 并算得 99；百度文库公开页面（https://wenku.baidu.com/view/920e92afe418964bcf84b9d528ea81c759f52e9e.html）可见题面仍显示 -1/2，但其解答区将该项改写为立方根并给出 99。公开资料支持“疑似排印误写”，但没有官方勘误或同版标准答案，尚不足以授权改题。",
  "fingerprint": "a29d7a800f89618e7ce06a40568f58d0612eaf758c2cd184617879b2a6850724",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu",
  "question_id": "gk-1977-regular-jiangsu-q01",
  "resume_action": "取得更清晰源卷或权威勘误，确认第 1(1) 负数半次幂是否为排印误写；确认前保留题面原式，并不得擅自改成可计算表达式。",
  "source_id": "src-d9a8910d628c7c1fa11a8b0f3184baa39d3a78411a2ebeea69a7461c52754608",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0132

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1977 江苏卷》（manifest source_id src-d9a8910d628c7c1fa11a8b0f3184baa39d3a78411a2ebeea69a7461c52754608，SHA-256 ce3d55b0f282697ce3407bcfac4c542956de3e619c2f1ce71332b1fab20e75e8）单页高清复核确认附加题 7 写作 lim(n→∞) sqrt(x)(sqrt(x+1)-sqrt(x))，表达式只含 x 且未定义 x 与 n 的关系。独立 Daxmate LaTeX 整理件（https://raw.githubusercontent.com/daxmate/math/main/gaokao/jiangsu1977.tex）仍复现 n→∞/x 的不一致但按有理化算得 1/2；百度教育公开题解（https://easylearn.baidu.com/edu-page/tiangong/questiondetail?id=1739882210836506778&fr=search）则将同题写作 x→∞ 并给出 1/2。资料支持“极限指标疑似应为 x”，但未取得官方勘误，当前仍不能擅改源式。",
  "fingerprint": "e82c2c27808e45bf974fb65827b9062576a86a87cdef9cf822c4bd3a4617b2e8",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu",
  "question_id": "gk-1977-regular-jiangsu-q06",
  "resume_action": "取得更清晰源卷或权威勘误，确认附加题 7 的被开方变量是否应为 n；确认前保留源式，并将 1/2 仅标为假设下候选值。",
  "source_id": "src-d9a8910d628c7c1fa11a8b0f3184baa39d3a78411a2ebeea69a7461c52754608",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0133

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1977 福建文科数学》单页第 3 题只给出十月份产量 1000 台、一月至十月完成原任务及年底前再生产 2310 台，未给出一月至十月各月产量或变化规律。第 3(1) 可在补充‘十一、十二月从十月按同一增长率递增’的假设下得 10%，但第 3(2) 的原计划年产量仍无法由当前源面唯一确定。",
  "fingerprint": "6d37f3dded3be808f9db7104478aacd6cb2bd6337e69544421a5c3cf0a86b20f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-arts",
  "question_id": "gk-1977-regular-fujian-arts-q03",
  "resume_action": "取得更清晰源卷或独立权威版本，确认第 3 题是否遗漏一月至十月产量规律；确认前保留第 3(1) 的条件式 10% 与第 3(2) 的不可唯一确定结论。",
  "source_id": "src-695012a4c4b226accca28c241571eab14a51c31f47f7ddec60950425b6c6e926",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0134

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 4 题单页文字要求求抛物线 y^2=9x 和圆 x^2+y^2=36 在第一象限交点处的‘切线方程’。两曲线在交点 (3,3√3) 的切线分别为 y-3√3=(√3/2)(x-3) 与 x+√3y-12=0，彼此不同；源面未说明求哪一条。",
  "fingerprint": "a5fece9152dd5d91558d903171d110f8b7e18bba4adfea9652d1bbd68d9a0a36",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-arts",
  "question_id": "gk-1977-regular-fujian-arts-q04",
  "resume_action": "取得权威题面或答案，确认第 4 题是要求抛物线切线、圆切线，还是两条切线；确认前并列保留两条按字面可得的切线。",
  "source_id": "src-695012a4c4b226accca28c241571eab14a51c31f47f7ddec60950425b6c6e926",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0135

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 5 题高清局部确认双曲线分母印作 24α、16cotα，且仅说明 α 为锐角。将 A=(4√3,4) 代入得到 2/α-tanα=1；这要求明确 α 的数值单位，并产生约 51.1361° 的非典型数值根，缺少答案页无法确认公式是否存在排印误写。",
  "fingerprint": "5fc9d7705fb943df764f5b48ef52efffd12cfa58ff5bf18b6927e6caca5734d4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-arts",
  "question_id": "gk-1977-regular-fujian-arts-q05",
  "resume_action": "取得更清晰源卷或权威答案，确认 24α 的参数形式及 α 的单位；确认前保留按字面推导的隐式方程和候选数值，不视作标准答案。",
  "source_id": "src-695012a4c4b226accca28c241571eab14a51c31f47f7ddec60950425b6c6e926",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0136

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 6 题高清整页与图示复核确认 AB=AC=50、∠BAC=60°、∠ABP=120°、∠ACP=135°。前三项使 ABC 为等边三角形；在普通平面角定义下，从 B、C 按两角作出的射线没有共同交点 P，与源图示不相容。",
  "fingerprint": "cd6f30bbe284e4b7f50ed10c7c636172166e9cbf2c5ba1fe084aaf27d65fb383",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-arts",
  "question_id": "gk-1977-regular-fujian-arts-q06",
  "resume_action": "取得更清晰源卷或权威答案，确认第 6 题一个角度、点位或图示是否存在排印错误；确认前不得补造 AP 距离。",
  "source_id": "src-695012a4c4b226accca28c241571eab14a51c31f47f7ddec60950425b6c6e926",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0137

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1977 福建卷理科》第 5 题高清复核确认 AB=AC=50、∠BAC=60°、∠ABP=120°、∠ACP=135°。前三项使 ABC 为等边三角形；按普通平面角定义，从 B、C 按后两角作出的射线没有共同交点 P，与源图示不相容。",
  "fingerprint": "1e5373a75b924bd0ef0301b88f6ab271bc2d4c226d87f47aa8f033c2a08facb9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-science",
  "question_id": "gk-1977-regular-fujian-science-q05",
  "resume_action": "取得更清晰源卷或权威答案，确认第 5 题一个角度、点位或图示是否存在排印错误；确认前不得补造 AP 距离。",
  "source_id": "src-169ec552629b39cd748da5afa1bce33d6aae2be96064ce7c9e5505c51312d359",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0138

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 6 题高清局部确认双曲线分母印作 24α、16cotα，且仅说明 α 为锐角。将 A=(4√3,4) 代入得到 2/α-tanα=1；公式参数形式与角度单位异常，缺少答案页无法确认是否为排印误写。",
  "fingerprint": "e93d49a202502825928a852edbf60be769aa115e4f57ef105938b725d3e353a6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-science",
  "question_id": "gk-1977-regular-fujian-science-q06",
  "resume_action": "取得更清晰源卷或权威答案，确认 24α 的参数形式及 α 的单位；确认前保留按字面推导的隐式方程和候选数值。",
  "source_id": "src-169ec552629b39cd748da5afa1bce33d6aae2be96064ce7c9e5505c51312d359",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0139

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 7 题单页高清复核确认数列写作 1、2、4、…，同时断言其前 n 项和为三次多项式 a+bn+cn^2+dn^3。实际几何级数前 n 项和为 2^n-1，不可能对所有 n 等于三次多项式；按前四项拟合还会在 S_4 处矛盾。",
  "fingerprint": "1cb946c6451b18f90fc71003ab0520fb0f060bade9d70a1af67e0adec0ac7e52",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-fujian-science",
  "question_id": "gk-1977-regular-fujian-science-q07",
  "resume_action": "取得更清晰源卷或权威答案，确认第 7 题的数列或 S_n 表达式是否存在排印错误；确认前保留矛盾证明，不补造 a、b、c、d。",
  "source_id": "src-169ec552629b39cd748da5afa1bce33d6aae2be96064ce7c9e5505c51312d359",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0140

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8219fc4025d627166c7b07c21dce8fda6f2e42a0c52f1dae03a5f16192464b93",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q01",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0141

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3478019ad4ca74436bc782f647689e173e4c5ef0e50a35be87b0f59f3564635a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q02",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0142

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0e4adbabde37fcb0c301a4f0b7667c89e4a13cb6dc350a49a0441aa7bed1ddbb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q03",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0143

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2bb75832f9eae493eb6bc3665887a58f23915dcec79775faa9b301f6df258362",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q04",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0144

```json
{
  "affected_paper_ids": [],
  "fingerprint": "93f400b4d5924dfea3a35726a49992134fd7ff8a57113606972f41586a73a979",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q05",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0145

```json
{
  "affected_paper_ids": [],
  "fingerprint": "47aed3e61278d44e9c362b1cd337202114da974bc3872cc7db87617187caf012",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q06",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0146

```json
{
  "affected_paper_ids": [],
  "fingerprint": "02e1f24fe071e5fc4050c4bd7c5efabd9f06c1b9fb06b4be2b4f039993d92183",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q07",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0147

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bd6b72a30cb71b61c5191815f43c9b6390bca474aef936bef2a863b47feddfd5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q08",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0148

```json
{
  "affected_paper_ids": [],
  "fingerprint": "758b5c137a0bc9dccbc6d488f40ac04b21d71e097498327fc687f8c471a1ec99",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q09",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0149

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0635736d447c8e2f13a3f78060f4739479eaf6c20546a39bd50f95801dd75cc1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-henan",
  "question_id": "gk-1977-regular-henan-q10",
  "resume_action": "已完成：主会话逐页视觉核对（p1—p6 书页83—87）确认题面转录一致；两处源卷特征（第九题小问跳号、第十题解答方程漏零）已在题面/解析留注。",
  "source_id": "src-be5fe5b27d4e762a3216a92b1836d799b7f78e554f4e322d34d61b3f123fe96a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0150

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d8087ce1bc536fce5dbd282d3cb4ccd42a75ae58ee9024d6e0d11d0c04c16e4d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0151

```json
{
  "affected_paper_ids": [],
  "fingerprint": "333015fa28536fba9fe454ec83693281cccaf6c753a2041984e358d8f89ff765",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0152

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c56fd9e415afc69eed8ff50292ac00732d91950c702b8d069ce1f0da7e2bd313",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0153

```json
{
  "affected_paper_ids": [],
  "fingerprint": "29747ea18974ff7b1ef2d832c94eaf0d3fb24f22f5771091d3b4381b04f665c2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0154

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3159c14da27c485f9c09d35a897591a9a160d3f26c77a278476ae036b665f4bb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0155

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cfb342b4d491cb584daadcd302886061c50d11fb62e381ad6035c3aff3b4f55c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0156

```json
{
  "affected_paper_ids": [],
  "fingerprint": "42ac2521363c48aabc8d3180a148dca652d007562fde3dba2f1aa53da7936aaa",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q07",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0157

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cbabb9e660b057fd6b86939dbca12f215bc4fa48dcbbf06161616fe3fbdd4b37",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-heilongjiang",
  "question_id": "gk-1977-regular-heilongjiang-q08",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-469f2117370979519f106c34083c61490a9c7ebdaba7a06dbe87633b8a5f4c7e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0158

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9f1027a2ee310b2e7a98f1f8a3fc3befe0b12e29cba5dd78be44c6adf0749168",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0159

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f87f610ee278a2849df68b33d26abd0b561772a83f5688b86c6a18886e59a1ee",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0160

```json
{
  "affected_paper_ids": [],
  "fingerprint": "025b3b4d26049d92638c93ad2f641f02bf63b112a3b2fc7a49f176d34ed6fae2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0161

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bb17c0ea3af086d068a8e1a4b6e59013c174da442af5853da6e3c38dad4f2c69",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0162

```json
{
  "affected_paper_ids": [],
  "fingerprint": "309a3fd1ea53ba8ca8ffaa2523ee219b932a0eea059481186dd2c97265584ea4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0163

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8340609dc87a3bed4646a5650311797c0c9f73277e06990aa2c84a82415d7e92",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0164

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5e7349f6fc569700ef943037e4d7299754cfcd1712947a3f656b5267add84a66",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q07",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0165

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7182709767f42fb9ebedb739480c89765f47b8a91d2a49c3ce2bcceadaf78c8a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tibet",
  "question_id": "gk-1977-regular-tibet-q08",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-ed97867a87ffc89b1d90329dd0f45e564ac2fa00d2d0b3d53f70555edfa714a6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0166

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7ed9b59ba08ae02e5c191454750b22a930bdd0bdcdbc772d00c54b88926499cf",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0167

```json
{
  "affected_paper_ids": [],
  "fingerprint": "434fb577979c08a6ac0e9703f161f451ae16ce89ea8e126a0c9c03a73b80ce17",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0168

```json
{
  "affected_paper_ids": [],
  "fingerprint": "66c5702cbf46fa967427f3758d380dc45df0255f4b4c238889217257f3b253b4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0169

```json
{
  "affected_paper_ids": [],
  "fingerprint": "618bf7365486fe1891378a2c88fe1233976076dfc9c4298a6d8951695543b4d4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0170

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f47c3e19dd7a086cd1730b790592944580370c26c5ec2bdffa4a175e342e46d2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0171

```json
{
  "affected_paper_ids": [],
  "fingerprint": "310585575fe3c68ce1b7bb7e87e4c6bccc72b0e317de8a867ed4ecce4c405da3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0172

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c07b48e96022f61b875ad8bbda9a13ec6b3a19fee7b879e65668ed4ff48d456c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q07",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0173

```json
{
  "affected_paper_ids": [],
  "fingerprint": "efb0f53b83549b898c5185fbf1703a62030a4387b3de920aec5de33388c3fa69",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q08",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0174

```json
{
  "affected_paper_ids": [],
  "fingerprint": "eb588fd52a705e215c1fec648ccf952b9aa2ad7be44888fb773b4a43c3bd6583",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q09",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0175

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b3571a7e18c71316ad050204cf80efa8f40a0996a5e5d4301a8f91a47f8a6f2d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-qinghai",
  "question_id": "gk-1977-regular-qinghai-q10",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-e332957caaf461ca62ecd4111dcb7a1bf7004dc8df74125b2191ab68ac05b3ec",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0176

```json
{
  "affected_paper_ids": [],
  "fingerprint": "108dc6d6bde2df335df55f7f28436b2ca463c53f19e3d2dd76965c748f2f5b65",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-arts",
  "question_id": "gk-1977-regular-guangxi-baise-arts-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-04ec742258d5003ce6db366a3e5195248321da77d66cbb0cb74a25872007035e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0177

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a043071e39ff702e28b8d788472ead89992bf7e7da65d93a253922ce019f96bc",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-arts",
  "question_id": "gk-1977-regular-guangxi-baise-arts-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-04ec742258d5003ce6db366a3e5195248321da77d66cbb0cb74a25872007035e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0178

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fd1baf395d312f70a3fd3ff5b61c60059e417f95c71eca7c8779ffc49472533a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-arts",
  "question_id": "gk-1977-regular-guangxi-baise-arts-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-04ec742258d5003ce6db366a3e5195248321da77d66cbb0cb74a25872007035e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0179

```json
{
  "affected_paper_ids": [],
  "fingerprint": "32e932d7e269999ac74754cecc0cf9330ece9ffce36d801c1b40f6090ea62ced",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-arts",
  "question_id": "gk-1977-regular-guangxi-baise-arts-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-04ec742258d5003ce6db366a3e5195248321da77d66cbb0cb74a25872007035e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0180

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9032996be4b4269fb364618ba6ea8bd67cdbf1f66a22cc9ad7ac8c82e1078c49",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-arts",
  "question_id": "gk-1977-regular-guangxi-baise-arts-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-04ec742258d5003ce6db366a3e5195248321da77d66cbb0cb74a25872007035e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0181

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2185e7ace043be47ed55eaddafe3a836e801cabfa54883eeba3060df17263395",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-arts",
  "question_id": "gk-1977-regular-guangxi-baise-arts-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-04ec742258d5003ce6db366a3e5195248321da77d66cbb0cb74a25872007035e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0182

```json
{
  "affected_paper_ids": [],
  "fingerprint": "81e223a0e5d48b61c2ec01dcc801dfca0400adfee1047a162800dfbe4f596f6b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0183

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1da67baa04776c5512a541ef7aeeb98005159b2b39325c87026443ae0c749f1b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0184

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f896e6d8a4e7ed508e01c17dc337658f1aa8237e64a417444beb2332a7db9fc3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0185

```json
{
  "affected_paper_ids": [],
  "fingerprint": "12f9428f5a9d6d1aaca2bbc00d6591df125e59e03ada294aeb8748307682e1e5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0186

```json
{
  "affected_paper_ids": [],
  "fingerprint": "79beadfd3a4650e345f0e5342ab992b27fe5f51b035bdb0c79687c8eaa4cae23",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0187

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ac8d531b5591d7ef6b1def4b2907daaeb7500e1cb6e85c8035d32c20a5b9ec6e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0188

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4918188b276c80e32138e8378d42dc4149a253b7ccd6f98a5abf0c84b2c0896f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q07",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0189

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1fbd109e9c75535bc3a94bb47b52aa09f7c7552dbdbd5b60442361f6a9b20473",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanxi",
  "question_id": "gk-1977-regular-shanxi-q08",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-194a0e44a866d4b52517fc813e2b48ea6553017687214e496a89fb295f73b173",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0190

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5c5c0bcdd7b3e054d74eb33bdecdf3d752fad020a9d40354165c0c746d918585",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-science",
  "question_id": "gk-1977-regular-xinjiang-science-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-605e4cd51a110ede8ab4edb9fc5aea099d44b1dd9cb8b9462a2ee3105110a734",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0191

```json
{
  "affected_paper_ids": [],
  "fingerprint": "06b7ab68bfd4418065107d03b1e7ebe0621f7019e707566a92ec69fe6511321c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-science",
  "question_id": "gk-1977-regular-xinjiang-science-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-605e4cd51a110ede8ab4edb9fc5aea099d44b1dd9cb8b9462a2ee3105110a734",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0192

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c35a1c2196173263ac812ce2e7d339f826e91d57d8a54046c55c5974a9605824",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-science",
  "question_id": "gk-1977-regular-xinjiang-science-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-605e4cd51a110ede8ab4edb9fc5aea099d44b1dd9cb8b9462a2ee3105110a734",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0193

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5c40971404ebbe93e23a6c5c1d6c30cd189639cb0c9a620cd88d81cd35c90d54",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-science",
  "question_id": "gk-1977-regular-xinjiang-science-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-605e4cd51a110ede8ab4edb9fc5aea099d44b1dd9cb8b9462a2ee3105110a734",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0194

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ebb0a7cddddf9066a59d089571296555f2d967383ad5cdab37630b129ca1aca5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-science",
  "question_id": "gk-1977-regular-xinjiang-science-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-605e4cd51a110ede8ab4edb9fc5aea099d44b1dd9cb8b9462a2ee3105110a734",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0195

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d73866bb5cf50b5a2bbc3459c993f187bd6458329344a07ab8b4f3592a18793c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-science",
  "question_id": "gk-1977-regular-xinjiang-science-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-605e4cd51a110ede8ab4edb9fc5aea099d44b1dd9cb8b9462a2ee3105110a734",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0196

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b2135e776e640dee80d6bfd95f1daa54c3e00f0218c328af4b4042450cdd0e74",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0197

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4dbff1f82bfc886c2129853ea7b1de023c38b7396cce8c5a40d67b22be734090",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0198

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7edc2202a8652e53b28531339a61ae615b19f47f65e2a80c33fdbe191fb451cf",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0199

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7a6ad13d34349944a65e2b1ee6ead719d4b48625e8f918aaefb848af3647af6a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0200

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3c70772150ea87e041380737ed6cb5d1a02523d6d53d4d144ba05cfbae20f617",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0201

```json
{
  "affected_paper_ids": [],
  "fingerprint": "da9608083f19f5875d26914ca4a96accaef05366fc67dede1c3f4cf5f87c52c2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0202

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2793de098c4a972b90fb28b67251b266361161433a2e0e9b93ed283f04219d88",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-zhejiang",
  "question_id": "gk-1977-regular-zhejiang-q07",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-26f527d9d16bec362778b445057c4658198692a71ea78f2d43cf068bf401ea0a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0203

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0919e1904b99168d06597e9394446a51fe8e1c9470d65e1e897a89b813b58de5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q01",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0204

```json
{
  "affected_paper_ids": [],
  "fingerprint": "df1b76f504ef3435fc5b8df84dfc72af3337983329ba981661c0ad93ada61f65",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q02",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0205

```json
{
  "affected_paper_ids": [],
  "fingerprint": "95785b8e13871f4f99ab75c89a439ae60e578111fa814b2ff3c42e455fd82deb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q03",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0206

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f8167a20043d05d756c222d3b45d9c2ab0ab5facda87b76c7e7eaf0fc8f193dc",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q04",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0207

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4450468159a14f4753200bb3b5cf4bc942b0a36b05fc46ac495e127f15049b32",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q05",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0208

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b4599449ba46234ad49259ffa092c53e43e6a6e218752ea037a3432208e11ea9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q06",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0209

```json
{
  "affected_paper_ids": [],
  "fingerprint": "54dcc3f95ac93ce5cce906da506ed0d01c4b31cf90732cd1116a079ba9c46749",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q07",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0210

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ba450659396f723fdaaaad218ac0e62387a7fbd067eed0e56620466a2b859f28",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-gansu",
  "question_id": "gk-1977-regular-gansu-q08",
  "resume_action": "已完成：批级视觉审查逐页对照原卷复核题面通过（b33/b34 finalized），问题闭环留档。",
  "source_id": "src-00b522e7172a65b52de24f640b6aa653ebee4f358e86ac4631422e242f57362f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0211

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "2a65acf3e18882b6a280331f5f7bf1586c3a59dcabaa62a070bfb4abdf23b027",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-shanxi",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0212

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "27734fedb8c1e8f859ef445ba06fd8c43a95b0719d67292309f41ce039761639",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-shanxi",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0213

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "beea83f0c142ea50ed7b384b048ae21263da6b1725a4d08ff3c8b9039e82bd7a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-shanxi",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0214

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "6d854dbf02319b99b6c5261bcf0de64c97403cc438d808cab71f072d46e1c7d2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-shanxi",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0215

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e6ed3fd3ab509d6df1815d9e9d3d5e981ab28e6dc20070f68aca875ce5250c49",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0216

```json
{
  "affected_paper_ids": [],
  "fingerprint": "afd0b1ab01f333b555349b3a913f9ff0beea85741843e31c27a8db49cb5bd8b6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0217

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a5831dc5eb46ef597a4055a55e880609fceec32566606073599ac34dfd924f49",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0218

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8613a6bfe8b095ed7d4fdc644e39725448bb530cd365e6ec6e67ec74617a2a25",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0219

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e5c6bca337b9e856a9b33e3f8d001a0cb799f8511643ca671c6f3a7fde1a5781",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0220

```json
{
  "affected_paper_ids": [],
  "fingerprint": "376bdee6e4dda08ddc0d9b173ca9cd4436abfb7a9796a318117eb31cc5d22547",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0221

```json
{
  "affected_paper_ids": [],
  "fingerprint": "71ac7a7f4cba1bd8899672430c2f6b88e8503d397549ac472a1c2e8c6a5882d8",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0222

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d7384f12855aff98ac4a40b437e19231546225a2e4fce49327cfe019474a262c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-science",
  "question_id": "gk-1977-regular-anhui-science-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0223

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3a6d5c7c58488198dde20ebca0387a399129dce448224cc80c881e3b6a9a7af1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0224

```json
{
  "affected_paper_ids": [],
  "fingerprint": "dac6dcd5558427a59495acd534a5d8e4f6bb690c9240992a48889bf210584d0d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0225

```json
{
  "affected_paper_ids": [],
  "fingerprint": "91e51c015f1e1ff8b685c5da08b021c9f63962442400777f03819ff7530997ba",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0226

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d78debe6556205f6f7e277dc017ae90f4e58a95460092f1817fa3c32d7b3f378",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0227

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c0488d3a442216453a55df1e1139221a80415c398db48653ed50049837649d24",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0228

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4233f6564725e48592a3d63b79d72108110d6ea0b37a54673a61208a877aad57",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0229

```json
{
  "affected_paper_ids": [],
  "fingerprint": "02a7db7c16120d6135b058eb25f27cdb9b06157c9233b876fca499409b6797da",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0230

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f4522e60d3745258bc5f7950f1bdfd64d9d679c9060716ca0de9e7af58d60ade",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0231

```json
{
  "affected_paper_ids": [],
  "fingerprint": "56cb2f001a8bbd1ad7c75753444685ecee83551c8b821767f733dc5d9fa3ace9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q09",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0232

```json
{
  "affected_paper_ids": [],
  "fingerprint": "557fd6ccf5ac36b5180b405b0c4a28fec7dd15e2bfc3e6397ca16ae196471a1a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-anhui-arts",
  "question_id": "gk-1977-regular-anhui-arts-q10",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0233

```json
{
  "affected_paper_ids": [],
  "fingerprint": "17840b1041004bf99cf091c36c8bc6074c458cc3d39746bd553808973f3b6855",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0234

```json
{
  "affected_paper_ids": [],
  "fingerprint": "33abaee01c0911bb64de18cd4a50c4ec5523ddc3775ec2e380d349c4edc4143b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0235

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d00d270a3a635e76f38b6f2c19bc5fcd75ca31e96c8cbdf108edbaf339aaa63b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0236

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4023bcf992e510e44bc70876be028d200bc0e53f23d251dbe7a5f24fb58203c2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0237

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5c7ea15f71dbc754b7ba5eb4f6b88844fb8798207929876583e4114ea6cc7aaa",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0238

```json
{
  "affected_paper_ids": [],
  "fingerprint": "915f6b831f953c2dd7f497a68ee74052ca12533122a4ef042e26156dd11b5784",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0239

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a88915c3e23cf5180c1d584b0bb51a78c3397268a29371ab52abc1154d942cb4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangdong",
  "question_id": "gk-1977-regular-guangdong-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0240

```json
{
  "affected_paper_ids": [],
  "fingerprint": "509fb9ebd958d9494c67240500f325a7135a1da3ba8fc88de0f6ba78845b6837",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-sichuan",
  "question_id": "gk-1977-regular-sichuan-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0241

```json
{
  "affected_paper_ids": [],
  "fingerprint": "82f68b4a0acbcb93b3918de2aca61b190e0f9de28f2f28938d5f7cb90d0d95f7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-sichuan",
  "question_id": "gk-1977-regular-sichuan-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0242

```json
{
  "affected_paper_ids": [],
  "fingerprint": "26ae2ff44083b9b5db63f6542d1fa4f0c72c2723db78caa8094a7236913c18dd",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-sichuan",
  "question_id": "gk-1977-regular-sichuan-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0243

```json
{
  "affected_paper_ids": [],
  "fingerprint": "35f5d30897ad6f99e4a56e905df332601d909f93c75c2002bb3c3af6dc627540",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-sichuan",
  "question_id": "gk-1977-regular-sichuan-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0244

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4fb15350cde96d25ab8fc99901f2b0ac9a01b4f9b1b4d24164dc4eab0eadbbec",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-sichuan",
  "question_id": "gk-1977-regular-sichuan-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0245

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7052bf9e3e99ee497cd3adeaf8fb7ef1b39ef39bde447160684192014d8c274b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-sichuan",
  "question_id": "gk-1977-regular-sichuan-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0246

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a4c237677a9a6d715ed5133cb108809482b7c4230328f95f3c367656115e204c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0247

```json
{
  "affected_paper_ids": [],
  "fingerprint": "315eeaa200baf1c262682899af071d1c7b4c491ff8a4ec33e7f8fcdd3f743632",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0248

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c242bb5e8ed9dcbdeb06bb52262c8d4d06b1f835dff54e85df9842e6f57c8ba8",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0249

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8cca3c035ea3b39b1960e3253c58374020cc023a03498f2f294a619a4b1a3ecb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0250

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6bbd8f8865f32d242dcaa319b144ce8636ac30965af16ca7a13823f991957d4c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0251

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6be8334b00095908d9d4be48a18fcf665c536192d34712b8752b6134f7aec48c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0252

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e0ff10bcbd14fc7d1ba080942be405bb059b339a8bcc67e5809dbf75ee91833c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-yunnan",
  "question_id": "gk-1977-regular-yunnan-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0253

```json
{
  "affected_paper_ids": [],
  "fingerprint": "67a1e51be7068aa28f1558228041577a9f4bf0f3826ed84e23301cbe4137f257",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0254

```json
{
  "affected_paper_ids": [],
  "fingerprint": "22d35bdba2671eefb4a8d2019d927306551d7ffb2cfd74dabf599b82f154124a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0255

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c27d3beb48e43f68280f15222fff10f0287b2059fd3d9d69fbe6a3aa5cedf1ae",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0256

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4254daaddb11a11750f45dffa190da363abc0786efd7e08c6ad6f033454cd95c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0257

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7db6c8e4258cc9ca96c44acb93bff6a46fa46a675ce29868da9da85ecccfe46a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0258

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4a32215c34df4a762da4dcd95c7fdc2df38feca8f99b53e89172a71b648a048a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0259

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1a34a2ff51e7881747212f03c370adc2b9faa054b5ab48d7c82ae023b4accdc9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0260

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f8acbe442e9bb184adebda9744b0e41850da99ba7c80a8e0418e5777edbb2b1f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guizhou",
  "question_id": "gk-1977-regular-guizhou-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0261

```json
{
  "affected_paper_ids": [],
  "fingerprint": "acaf83201d0e42bfde9765765f1d5ab680255d2d27f5b58641da3ec3917e6083",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-arts",
  "question_id": "gk-1977-regular-guangxi-arts-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0262

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5f2b0105c14b0cd0daa72dae49acde00fff555028ac0b0b9755dd5caaed6d182",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-arts",
  "question_id": "gk-1977-regular-guangxi-arts-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0263

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cafe7c5583cec73153d589c97b61b5b8eb21c8007aa172b1adba9fe2039eab93",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-arts",
  "question_id": "gk-1977-regular-guangxi-arts-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0264

```json
{
  "affected_paper_ids": [],
  "fingerprint": "092b345169fa171c3d57b969b09c6c979d0e06cf60b1dde8d9b896ff62fc13f7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-arts",
  "question_id": "gk-1977-regular-guangxi-arts-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0265

```json
{
  "affected_paper_ids": [],
  "fingerprint": "76b8726d0a1c49f29acf46fad4525c6812f8db686df2f7b87b4c1e8e2d476e17",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-arts",
  "question_id": "gk-1977-regular-guangxi-arts-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0266

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c1a519a2192e429cb64069d558cc31a8913504e42e2587cc8f0632c535f99529",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-science",
  "question_id": "gk-1977-regular-guangxi-science-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0267

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bacf8c58cd312f781efdaafc982ba2a0fddd4652007f9ff541bc784d8cd32f32",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-science",
  "question_id": "gk-1977-regular-guangxi-science-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0268

```json
{
  "affected_paper_ids": [],
  "fingerprint": "208753c4e322670ef048117c29790e397e8264a0df8c2a599653a70da0be383e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-science",
  "question_id": "gk-1977-regular-guangxi-science-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0269

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0bf18eb0900ddb9dbe916698c9ef3e388ae294edd062f6d260244a82612cd2ef",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-science",
  "question_id": "gk-1977-regular-guangxi-science-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0270

```json
{
  "affected_paper_ids": [],
  "fingerprint": "40323070fc8aa35b2e354bd6cf9744349a1b4fc64df15b91633b9ec72f10ad27",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-science",
  "question_id": "gk-1977-regular-guangxi-science-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b35/b36 finalized），问题闭环留档。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0271

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "f9b3c5d22fa1b4c4a6d00c8653c409bbbb1dbbb38b97cfedb789828f2c257561",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-guangdong",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0272

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "48642ed41cdd81c187285d01dd32a125d76e1688c7c10ae45bbe565bbd92ae89",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-guangdong",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0273

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "abc26abb1af7cc0bb08a0e824dd746f0bad489b012a94a82e83e7d163531c22c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-sichuan",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0274

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "581899c601cc1bcf88e6241ddca30a3e055fe79f43781354264a31d7af7e1b6a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-sichuan",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0275

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "9cc1e7e5ee8cfa92df05eb2afaec69bffac218293c2cd6e2f71b5761d865ea80",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-sichuan",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0276

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "880e46950123f67a21ee64c402748c6a3320efa4685c32d6a9b20568230d8bf2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1977-regular-sichuan",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0277

```json
{
  "affected_paper_ids": [],
  "fingerprint": "23472d220f562b249f1ec44279ad5f0cd1517650cd926c4896796266b1da3ba3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hubei",
  "question_id": "gk-1977-regular-hubei-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-dd9ccba4e381fd5340e9f078a68e4023bf62fb6c12c5d87952daa84f6ce00ef6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0278

```json
{
  "affected_paper_ids": [],
  "fingerprint": "baa3dca3d494e84ac1dc79122202a624058f777074f2971ca8d1d116b2c30648",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hubei",
  "question_id": "gk-1977-regular-hubei-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-dd9ccba4e381fd5340e9f078a68e4023bf62fb6c12c5d87952daa84f6ce00ef6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0279

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d29621b47e6650d10063651b9936e6de2953a00d8d2e1bc2be9549c9a85b4794",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hubei",
  "question_id": "gk-1977-regular-hubei-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-dd9ccba4e381fd5340e9f078a68e4023bf62fb6c12c5d87952daa84f6ce00ef6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0280

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7c3767516fa93e3f99ab9b9c67f5ff9c07cffd944289ba4889029cb27f1c7725",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hubei",
  "question_id": "gk-1977-regular-hubei-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-dd9ccba4e381fd5340e9f078a68e4023bf62fb6c12c5d87952daa84f6ce00ef6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0281

```json
{
  "affected_paper_ids": [],
  "fingerprint": "36a8039dc3a593afb20037e1e2dd81f5560203f82193a1fc4be3d25dd00541a1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hubei",
  "question_id": "gk-1977-regular-hubei-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-dd9ccba4e381fd5340e9f078a68e4023bf62fb6c12c5d87952daa84f6ce00ef6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0282

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7ff1f78b614984333ee1341690f4798c71d5d894e257a2c04eb1346c2a1bffd1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q01",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0283

```json
{
  "affected_paper_ids": [],
  "fingerprint": "38f1d22a0faf9faa64ed8418470e8e8bb1da9410132b8afacc8059fc0ef58c18",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q02",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0284

```json
{
  "affected_paper_ids": [],
  "fingerprint": "769fe8e8332f8d49164a23ff93c238ead0d30bf8ad9a8ed500a4fbe6ab8223e3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q03",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0285

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6ce81635b17985ec280089a24af3f9a3c0d5b6f9d16d4104e7e763e83069d53f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q04",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0286

```json
{
  "affected_paper_ids": [],
  "fingerprint": "43b4c253848c291ae96afe6d60864ee54cec11cb6c35be76eed31bc6dd89aaf8",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q05",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0287

```json
{
  "affected_paper_ids": [],
  "fingerprint": "39016f813ab2d6475f7d8641f0af186cc710f6f01673121dcd3d3d55545d1735",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q06",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0288

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c73a188f80cecefc49593c30e48a165b3c488ef783297ac4fa01c5d192e13f83",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan",
  "question_id": "gk-1977-regular-hunan-q07",
  "resume_action": "源卷为无题面的答案与评分标准册，题面反推+逐题源注已是可达的最诚实形态；第 1 题（2）（3）（4）原始式子的不可确认性已留档。如取得原卷题面可再行比对。",
  "source_id": "src-7dfa7c98af01b5dd89262583976b40226b41e5107a5d0e14bcccb0178124782d",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0289

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4d0977d9fbc6df485c2fd48802a0b4b8c6c818e30d638d738b6c3274e631c23c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0290

```json
{
  "affected_paper_ids": [],
  "fingerprint": "04388f557ec6625c98842ff996ccade6db4f164c1763098cdaad7b03cfd35e62",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0291

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ef96d0106edd0dc27b59bdac0b1efcb7a15d08dafc8d313d1fbd9d8b4da41c76",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0292

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1c541ad802e06485967cafe01f7035b9f590d75bf41fac66e02ee8c77cc3ef36",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0293

```json
{
  "affected_paper_ids": [],
  "fingerprint": "eabe23d21f35387b84b9441b484a968641b09e81eceb2bb799354f00e1d380ca",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0294

```json
{
  "affected_paper_ids": [],
  "fingerprint": "41fab200ff6eb2f9b599e0d08e8ada5ea831ba2953a5e571827ec2f84366bde3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0295

```json
{
  "affected_paper_ids": [],
  "fingerprint": "caa57adad048bd7794d5b36c4774d4973945c75414e84825a8f8c07a841e1719",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0296

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d1febc356085e12852798a041f557863db317c4dfe38cd916434091502d0d40b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0297

```json
{
  "affected_paper_ids": [],
  "fingerprint": "00541600b7e5b83540ddce2343ae73f09a7306041fd1e57247c090e34f3fa5a3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q09",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0298

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ec8ce255287d4010efce970d62910fc905f6c3df846494b8dd45a65bbf111ac7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q10",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0299

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9c88b0182379564b98d26a9ab30d0ea50d08cd940f36acfb44231c6e52f10892",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q11",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0300

```json
{
  "affected_paper_ids": [],
  "fingerprint": "80baca1a2b18e2e8fe14fe258fc0d413cf66a883b6c17df9c635e0d823570be6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q12",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0301

```json
{
  "affected_paper_ids": [],
  "fingerprint": "506d84cfd932357baed382c285f2a92651332fe7eaab954b1bd3a4f184f2f58d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q13",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0302

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bdec3dda3f3630a7b32681ba26df7fa70184d671a34185f35d54874b364a84f6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q14",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0303

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c5ca89ff9346e74ea8241f1972edd736068e08e8a5d401972f3e080cb65107b7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-hunan-zhuzhou",
  "question_id": "gk-1977-regular-hunan-zhuzhou-q15",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-32ff9e25e49ce9f87720ae7e05f2ff9bdc8dc9475034f1d0e658a768db02f3ea",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0304

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9d08fea1cfff11201bf6132a5ba03c42634bbd71a7f73533fbcc584453bada15",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jilin",
  "question_id": "gk-1977-regular-jilin-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-839c81f43061fcafd6499921a8792ffbf2c99a5ee54829de60ba7ae6d8734346",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0305

```json
{
  "affected_paper_ids": [],
  "fingerprint": "105ad04c63caf632f878b74bcc912b75ae47166c8625befe3358d6f4b87828a4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jilin",
  "question_id": "gk-1977-regular-jilin-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-839c81f43061fcafd6499921a8792ffbf2c99a5ee54829de60ba7ae6d8734346",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0306

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a3186d5d3e5665de62fad9b59f82426aa252ac406ba58fd9882aee655279da2c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jilin",
  "question_id": "gk-1977-regular-jilin-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-839c81f43061fcafd6499921a8792ffbf2c99a5ee54829de60ba7ae6d8734346",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0307

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ede8ab9433e1762ee296a9e14df58e4e37a696aa87fe2b622207dbfed89daafa",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jilin",
  "question_id": "gk-1977-regular-jilin-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-839c81f43061fcafd6499921a8792ffbf2c99a5ee54829de60ba7ae6d8734346",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0308

```json
{
  "affected_paper_ids": [],
  "fingerprint": "43290bc0172fa3364ce68231b7ce2e5f3bb83f0cd956ef2a21a7152874659df6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jilin",
  "question_id": "gk-1977-regular-jilin-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-839c81f43061fcafd6499921a8792ffbf2c99a5ee54829de60ba7ae6d8734346",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0309

```json
{
  "affected_paper_ids": [],
  "fingerprint": "745896d7e0eb9b58dfb73bae48ad91af023bd72f0b17370d7ee38fa8b507e537",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jilin",
  "question_id": "gk-1977-regular-jilin-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-839c81f43061fcafd6499921a8792ffbf2c99a5ee54829de60ba7ae6d8734346",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0310

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4ed111398841ba3d2378ec946a74871eb831f41e36e5a637540b6296af43c20d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0311

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1b2dfcf61e1f1894f299410f83fcddd2c37b8f8408defda76ae4cc1e4a36e5b1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0312

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c59eef8472072b010492add8dda25de1da27f66f76ea746000d46127908b543f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0313

```json
{
  "affected_paper_ids": [],
  "fingerprint": "af01a8644227b78b080d7ccb55e15d982b8404105e91b21f0eb6ecc60c81002f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0314

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0538e0b8458c0a566d3cc58d0e9b106864ca90bb56de65d64af9728acb9dcc1c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0315

```json
{
  "affected_paper_ids": [],
  "fingerprint": "912b75b166dda7f217fd5b172b2863ad4dccf3f49ba0bc79a2723885e933fbcf",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0316

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ced1cf84946b37f047523542d9d6a3164eadd70168466aa841e3d914ec02bf12",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0317

```json
{
  "affected_paper_ids": [],
  "fingerprint": "01c527cd31e39a3bfe138e9251c0d2d91bdab2d793525ec84306c6396908b176",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0318

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ba7261d5891e6cf7c8f71aed023b193ddf625df0f8ab5a06ab2b797279060813",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q09",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0319

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e83f7e0b503506c36a8e92ea6812e2f538e92f4b8567b8430997a3298dbd68d7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangsu-nantong",
  "question_id": "gk-1977-regular-jiangsu-nantong-q10",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-ef8797067b66d45c6d11cc72ae7d854f0265cffecce16eeb945f46bf553391ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0320

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3967053964b2cd76e09b065abe79ef90c1f6eaf3af4383ab809687b4791fe60d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangxi",
  "question_id": "gk-1977-regular-jiangxi-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-8cba381093818508a66781ef8274406609a93629b8ffea3f92b1cbf71e2d53b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0321

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f1e177b7201966b9d76dfd425e0a9c3d2578b270e2a57434f7c5e18e104d723c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangxi",
  "question_id": "gk-1977-regular-jiangxi-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-8cba381093818508a66781ef8274406609a93629b8ffea3f92b1cbf71e2d53b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0322

```json
{
  "affected_paper_ids": [],
  "fingerprint": "dfbe2df93d45af4a66c4ed62427afe17b8c4260ba91b9d19358f27389992f272",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangxi",
  "question_id": "gk-1977-regular-jiangxi-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-8cba381093818508a66781ef8274406609a93629b8ffea3f92b1cbf71e2d53b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0323

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e6c337b5055c8b92e1748713789855311be529ededbffe149f0c4c1db9f6f636",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangxi",
  "question_id": "gk-1977-regular-jiangxi-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-8cba381093818508a66781ef8274406609a93629b8ffea3f92b1cbf71e2d53b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0324

```json
{
  "affected_paper_ids": [],
  "fingerprint": "05397c68ed0f27a4743a809aa83caf23385a9f90797a3ad6dc25ce4b15a22a80",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangxi",
  "question_id": "gk-1977-regular-jiangxi-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-8cba381093818508a66781ef8274406609a93629b8ffea3f92b1cbf71e2d53b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0325

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9617020c1f557d512cab4bd85ef6a2754dad6a14b2b458f40c7a481ed7ad3313",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-jiangxi",
  "question_id": "gk-1977-regular-jiangxi-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-8cba381093818508a66781ef8274406609a93629b8ffea3f92b1cbf71e2d53b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0326

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c79da31ea5a1529f0e332a82ec417760517890117d15755501a53e4e613c83ee",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0327

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cfa771424c6b41c73a78986e7202f3f9288087c7dce76474fdcc948517c9a5b2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0328

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6b129e779e21c74eae8624a6786c99278f8362fe63cf7dd0caacc21eb1946461",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0329

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a8ab0cfcbeb1cd23f5cb200668fc965783b7b54e0755c295fdc2ec2f137f7255",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0330

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f4b97df5808a5fc6eb086fcbfc32d464a638a423511782c7bbd38c8381f2ea66",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0331

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e6333b4e3fcf36f86c04fbfb72604abcd96b2eb974d33443fefdd9f03dfc5b85",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0332

```json
{
  "affected_paper_ids": [],
  "fingerprint": "40b46d2a31b27431cbd52b44c4021162cc6f5161a5c31a95a9af1be8b349ddde",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-liaoning",
  "question_id": "gk-1977-regular-liaoning-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-7d7b10b2fef891c7ab5bbe3155f2df772bebfa95a7c1771d82722fa2169271aa",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0333

```json
{
  "affected_paper_ids": [],
  "fingerprint": "aaea39bbbd9071d5b6eee41c00f42fd367674aaedd1b988cc4edebf42c808ee9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0334

```json
{
  "affected_paper_ids": [],
  "fingerprint": "84eb0ee915025fc6366a383e56123a8af7c6a75267a216f77cbb3df3a4201217",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0335

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6af4287be36482b4b801ca6de3cfe83be5be481ab35ffae77810546735a55508",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0336

```json
{
  "affected_paper_ids": [],
  "fingerprint": "41fa5a9d2e58dbc6ae29316846944f7a3f702400e16da2b0fa71373b295adac6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0337

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0212b89ff69379b006bdb16193bf2a1d03dab88bd92b0b8d10a4e8b84f5b387e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0338

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8a3ebbdb3c59755dc4eef86d16aaedb83b02259c9a06442daf676a234caa9085",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0339

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2603dd2149e5397862595d3c29e595d2542d9d9a87d2868d1686bcd9276e4e24",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0340

```json
{
  "affected_paper_ids": [],
  "fingerprint": "21be058c6337136fb610c16636920610cdb393eff5ea483955a4bc5d4e6d80cc",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0341

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a7f5cd5fd38a4cafb02aaa448a5c90e345d50434a8a570ab20612a142006aaae",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q09",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0342

```json
{
  "affected_paper_ids": [],
  "fingerprint": "73f2c6a3cd38661e4f1d382593116e3c4e8fbecddb1e85ed2ef7adf51f7bfbc4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q10",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0343

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b90c46311b0c41b0cd7a87264a33d83305f8d9ef7cbe474d48018523a0fdcbba",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q11",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0344

```json
{
  "affected_paper_ids": [],
  "fingerprint": "505f0123abb675845855980a35b37b18b5961c4d1750f8b77961dec01aefd090",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q12",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0345

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f293cf0c75c06a33f93c2ee336c7b398dda157a6e9cae5cf288c6a15386ae8cc",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q13",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0346

```json
{
  "affected_paper_ids": [],
  "fingerprint": "185e20e69388e43fa13654739afd2e4de3096eff869fcb3233246ed9998c17fe",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q14",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0347

```json
{
  "affected_paper_ids": [],
  "fingerprint": "af1c8502a619a9da96d45e08444c3a0a2bd61a550c949e9909eae6a57c692817",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-ningxia",
  "question_id": "gk-1977-regular-ningxia-q15",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-a28e694ae4d23dcae2294ae347c8e2911ea6253dac4f07b20405f9ca104f03e1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0348

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e84b75ffbc841d61888665069051277aa83236858f882713fc5b131d8a6e38ce",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-a",
  "question_id": "gk-1977-regular-shandong-a-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-efbab9ec63911f956ef3f988691d7ad7fd070ac714122987ba18cfd5d26496b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0349

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0768abd9e030f79fd1de046f0795d20c12fad5246b6b11e829e15e565973930f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-a",
  "question_id": "gk-1977-regular-shandong-a-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-efbab9ec63911f956ef3f988691d7ad7fd070ac714122987ba18cfd5d26496b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0350

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0d89dc653fa41c56a57b1beaf51e9b63a00872c931742966f77bf970dc1f7be0",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-a",
  "question_id": "gk-1977-regular-shandong-a-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-efbab9ec63911f956ef3f988691d7ad7fd070ac714122987ba18cfd5d26496b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0351

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ab1e11f294e7c74550816beb909d85939a0a6c4054036beef7a6034a70084958",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-a",
  "question_id": "gk-1977-regular-shandong-a-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-efbab9ec63911f956ef3f988691d7ad7fd070ac714122987ba18cfd5d26496b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0352

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c67f1bb070b35c3579eb292d5a47e0cae8424175d86be4b26f5018fc76100c74",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-a",
  "question_id": "gk-1977-regular-shandong-a-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-efbab9ec63911f956ef3f988691d7ad7fd070ac714122987ba18cfd5d26496b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0353

```json
{
  "affected_paper_ids": [],
  "fingerprint": "df46f9732bc23c5b8aedef9b62416a6022c6037c7d3660b137d511ec77edc23f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-a",
  "question_id": "gk-1977-regular-shandong-a-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-efbab9ec63911f956ef3f988691d7ad7fd070ac714122987ba18cfd5d26496b6",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0354

```json
{
  "affected_paper_ids": [],
  "fingerprint": "49c17065fad52ec8553c3e766e2446770b7b3d945f28d1d7009ba1209953a71d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0355

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8b1505c1c5f096af3d17d485b9aaceebab181f70e44de2ed61253858432aa87f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0356

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f93698d0d34957bd55ee1c35f71e338be0b7ffdaafb5c3efeaf56fed6e22f658",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0357

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b2994e9bc49dca7c9b82a8f9bff8486faef3c7c50501871b862aa704c3f0b96b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0358

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b3daf323cf5a08f0d45ff4b59fb0585648117ab8751de1cdb64092fb29f8cd9b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0359

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8c5cb09b873dbac645ba9697ee3b0c62481fb2178b29d3f239d3227f31b5a22b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0360

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fcb560c346997caf6a47bdea59ca9170e7709a3334847ec6c126044ff921d5d6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0361

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6b9493e3f7c7e29c7fe1399762ec2671b4576b36dca7ad8b465679c8832b69f1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0362

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c284987850434cb42e480339ebc407f38691cda85c8942d6b30980c34234012e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q09",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0363

```json
{
  "affected_paper_ids": [],
  "fingerprint": "093f4dd69e23d9d14946c81bcc8c77113cce576929847fe97d97650abc36e52e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q10",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0364

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d2d10e4c0922773f9ad37121b49f84d7db2a2cbeeb97bde8ac8478024d09f775",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shandong-b",
  "question_id": "gk-1977-regular-shandong-b-q11",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-36d98ff635ea1b544cc43f0b78be419d472dba39e0befcb8ce9e75c1b9afb158",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0365

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c3f74026d84fca3178d97c937ba31e34e9eda7497727210d6d033a6e8e8dc514",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0366

```json
{
  "affected_paper_ids": [],
  "fingerprint": "82b19561429e0abdcacbb5532e65a699ad32ff14ef4a23169fecd8d31b073f4a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0367

```json
{
  "affected_paper_ids": [],
  "fingerprint": "75b810c9975012e1dc6defafffc63ea22a47e4ee1fc10c5a47c7914305ccdf13",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0368

```json
{
  "affected_paper_ids": [],
  "fingerprint": "dec5c52f3aed143bafab1921f35346c4210a70042c3c4fe36365e6bd9c30c741",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0369

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b9fccc6faa14c65c617df12842cd2a6f12e9de5e375addcac2185d7c642885fa",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0370

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9dcfd33b95d3178424830716665f24edafe9997230baf102ee5053e014f50f09",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0371

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c237e6d9c0ede1850cb5b41f25b14071283b72ceb18692275ef01c763f5b3016",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0372

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2b3158c4247c5fc38ee128d0798429a70b1f867178fafe8066739b253225fc52",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q08",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0373

```json
{
  "affected_paper_ids": [],
  "fingerprint": "edef1a4d57ef23583037802c8c0787728c33e69d44c7f4a522daaa89675ba888",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q09",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0374

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7ef8416c835142e0269dfad7044a1a304bae165f14481502c18531588d6e0972",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shaanxi",
  "question_id": "gk-1977-regular-shaanxi-q10",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-5e7e33aa2bc4a4f0ac630726cd948661c2c1d95f5f98b827f981b467a51e3db4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0375

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fdecfee4d4745062b6a9ea9434c317fe7eadf1c97d7a070b9d149aff92eb4d49",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0376

```json
{
  "affected_paper_ids": [],
  "fingerprint": "88684612f31d59963532f80fa965d6bc48618873073bf58aeca4dd39ba5cfc2f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0377

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c8268d44a0ffd8fcbc51613b5b587be0d7c0dc8d0aa791a99349580b487bf057",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0378

```json
{
  "affected_paper_ids": [],
  "fingerprint": "47b90f06c9372aff297cb0f005e3125cc643e6e666cd4b9dd67dd8dbcf797eca",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0379

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7ceda7b0e639008c60f43283b50776f2edb2a669d0581adc903a69daa3ff3a5c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0380

```json
{
  "affected_paper_ids": [],
  "fingerprint": "02b2b6a69a05f456172c09b4053bfd2182e4ea40d00ab1a927f9fb2903e1d08e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0381

```json
{
  "affected_paper_ids": [],
  "fingerprint": "419af07db994bd9323eb6b86502c18285c94ff6d91e29dccbeab5f950f36cf66",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-xinjiang-arts",
  "question_id": "gk-1977-regular-xinjiang-arts-q07",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-800c7953893d1b748f44ab64fd270c28074d8b3291ecc9f9fda200eb1d2db9db",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0382

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9001ec0c5c31044394765db9ecb4af656ddffb2ccc0cbdd73a3bfbc62533b8b9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-science",
  "question_id": "gk-1977-regular-guangxi-baise-science-q01",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-137c42f4705802889d5bcbfa9cb558a8af4ac5940b95ad39f8e0c01c215c6081",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0383

```json
{
  "affected_paper_ids": [],
  "fingerprint": "914613462726b2d0511536aaf0b31f3e98d7dc285b1d596b50cd4e99199da412",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-science",
  "question_id": "gk-1977-regular-guangxi-baise-science-q02",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-137c42f4705802889d5bcbfa9cb558a8af4ac5940b95ad39f8e0c01c215c6081",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0384

```json
{
  "affected_paper_ids": [],
  "fingerprint": "710481610f82f68b8e76ee274aeb4225b6bc9dfe71915b16560944f703cfa9c0",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-science",
  "question_id": "gk-1977-regular-guangxi-baise-science-q03",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-137c42f4705802889d5bcbfa9cb558a8af4ac5940b95ad39f8e0c01c215c6081",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0385

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3b3cef95b5601e877c8cb8e41c23f8805c606792e47f1f3e39dc61931ede1d3f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-science",
  "question_id": "gk-1977-regular-guangxi-baise-science-q04",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-137c42f4705802889d5bcbfa9cb558a8af4ac5940b95ad39f8e0c01c215c6081",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0386

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e7b67d7abd4e842f9b5ec54e8897a6bd3f5d16a32a240f8ac875ff30d51510b7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-science",
  "question_id": "gk-1977-regular-guangxi-baise-science-q05",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-137c42f4705802889d5bcbfa9cb558a8af4ac5940b95ad39f8e0c01c215c6081",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0387

```json
{
  "affected_paper_ids": [],
  "fingerprint": "77855aa5e898919f986b3741defb04cbaa3e378fec4ca8acc6c80bff7c52b336",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-guangxi-baise-science",
  "question_id": "gk-1977-regular-guangxi-baise-science-q06",
  "resume_action": "已完成：批级视觉审查复核题面通过（b37-b40 finalized），问题闭环留档。",
  "source_id": "src-137c42f4705802889d5bcbfa9cb558a8af4ac5940b95ad39f8e0c01c215c6081",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0388

```json
{
  "affected_paper_ids": [],
  "fingerprint": "00274ca7f81a168862228634949bf0d0fd3d990265cd0a0e32233241b93f11fe",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0389

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c9494613a1fc1df591ee72b9b31d07af9b4ffa7fb34037985a47358397d624ea",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0390

```json
{
  "affected_paper_ids": [],
  "fingerprint": "629018aa7dfdb8e90a33a461ebdd1a7f62a4e3b73792a948ed738e98c02eb370",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0391

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0170eafbf31bd9a2859d5970a9cfc0fc2064c4040a4fbe71e8f95878d0b2b6da",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0392

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d259ff300126c3ebcc3fac3ba18d35e1b9bb936a7d88c2a67b520e2cb0b76756",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0393

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2bc0afb77a56faa450def512059dd81bfe8fb9cadb9ef8bf1fdfca145ab775f4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0394

```json
{
  "affected_paper_ids": [],
  "fingerprint": "414a1f334ca79b39da2eb9ff3d8d5e149253e98d81ffc199ccc9ac7efc405690",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0395

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d46be2be8dd835d8ab94103dec9e0dceb6b1dbcb382c7006a93ceb50eb77a49f",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nongken",
  "question_id": "gk-1977-chushi-js-nongken-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f4a7d2f8fad786cd39014fc551f6c0cb79d4c7982ec66dc7641dd7350f664008",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0396

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e74d03c34024c8d0f7374279d75e21f5e20230c1f1775981053ae6fe72165ce9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0397

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c32f7723d1cdb81bfbc467f4ce3d1e142cc453e339108d52a19c3d27126a1a3d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0398

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7b9ace3b51f0105700f2809fcc7257e3133621fb326f93c57ab445dba15271b5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0399

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2ac645f40552d024012970b2308f21511f8459aa41a1bdca0869e7e076658e93",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0400

```json
{
  "affected_paper_ids": [],
  "fingerprint": "dd1df7391c9afa21e3095ff2f456c98d978e09a96e344fd2b64d9c05800acdb1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0401

```json
{
  "affected_paper_ids": [],
  "fingerprint": "347f3a3f7d269ec3defb9dea88548c88fc49a0d2883d82e098da5419bb5e226a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0402

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8c0891b4de29a57447b4729a067ef5c707604bd832682e7ac755e6ededeab2f3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0403

```json
{
  "affected_paper_ids": [],
  "fingerprint": "eb72fd4bb1c6ed82b063c0bef88641cc7aa9a00e1d8867cd31f985470aafd8df",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0404

```json
{
  "affected_paper_ids": [],
  "fingerprint": "96ce04f53e9221248b10d97910ba499e19f9e58b5f6cd390a640e005ae12dab3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0405

```json
{
  "affected_paper_ids": [],
  "fingerprint": "deb1c6314f8fd94c1296381aba205cdec447f1f8d0c512db17a183715ab72a41",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nanjing",
  "question_id": "gk-1977-chushi-js-nanjing-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(2)题答案方向错误，已改正（cos40°>sin40°）并重编译。",
  "source_id": "src-9c79436644ee99fdecaaca9ed70178c17f782e9fb7fbf296322451737bc54284",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0406

```json
{
  "affected_paper_ids": [],
  "fingerprint": "944fecfa8b00c9fc81f507f30f3d080f76b5a1b83a0206ef1028cb423649636d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0407

```json
{
  "affected_paper_ids": [],
  "fingerprint": "188ec834f0fe3b8a76fdd37410331cf087ee5bfadd27e2bb7c8f3515eb9de249",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0408

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e4717eff5085e02f4e739c11c5516e5d4f7e293b10d80af36e910076f1d848ef",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0409

```json
{
  "affected_paper_ids": [],
  "fingerprint": "34d32954dcf97403596fdd1b382bf5246b056f3b1c6d4231dfb2211bb1b146d9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0410

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8f4466e3bf5db48a8bf354c75aaa55b95f59e5c6992560f58f54a616c6dcf10e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0411

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b69fb6022ffdab3d857f187b817cc6237b901d2411f0af16721a3b6ea9ca87ca",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0412

```json
{
  "affected_paper_ids": [],
  "fingerprint": "57d8c76d9ccfd47a7a4ccbad40711a54fecb4aa92008716b5647afb0ffafed03",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0413

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9c0cc680ca274a646110d8d523b069f7f4e11d514b54279268e651ac737a88fb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0414

```json
{
  "affected_paper_ids": [],
  "fingerprint": "082faaa75265a46c1433472ff2d2615b54a6ee1c3462e593cd015c600964dd12",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0415

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b47cf42a8639e40ef2e02a8553d9ec3d93d50330c03834d44894a93cd88c2f4e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-diqu",
  "question_id": "gk-1977-chushi-js-nantong-diqu-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f7078988752596ebc9a30b5c09c072ccefc69cbc7f09a7b460247f482e7a2327",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0416

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3d082fa4cd1b3ee392effd2c2b0806eba9ba437c7d03bd0ad710cb2bd22c3f4b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0417

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e997e9a915c947b2f8021defcd47264ff3e5ff25456905e4fa3d73c2035e525d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0418

```json
{
  "affected_paper_ids": [],
  "fingerprint": "77bcb776c6cafa674e2a46355896c9947a5955d26984b2e8df4d1817911585b6",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0419

```json
{
  "affected_paper_ids": [],
  "fingerprint": "356615d2d7bad08300f974a6be6b0f096698f882e47708ab05761ebd4de0c3ec",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0420

```json
{
  "affected_paper_ids": [],
  "fingerprint": "03d56ef49b8e7e9cc7814ca295338da240e0c3340a61e38d312152b7a81dd22e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0421

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7ef13b215c6335d979ef4f449e74bd7f3838d3b330ae6c879c0c21ccc0a61ec3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0422

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e23aed0e6fdf2d0aa8f7ef327f466384b7f0c7c712915cf0c680d563d67fdea1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0423

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a46d3f5f10cc4dbf70040e1d9e09d5e5aac00e4f85e677de45780813f23398d9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0424

```json
{
  "affected_paper_ids": [],
  "fingerprint": "95504542d2f46a719025c35af37664a6e3f92645638b395aafcd6a969c5d6ba7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0425

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9563e500ee577949db5c8b7471af41109c91f4f092ff1de99bfdafd4b47c0ada",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0426

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7e1783404316bc992312ebf88bba90eefb9924df7d6aed82d0eb1a6ce8ffb4f9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0427

```json
{
  "affected_paper_ids": [],
  "fingerprint": "06355b3304c9be5e179da3728fa26ab24ef07ddca4b0188d5b2fdf47404c8c61",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-nantong-shi",
  "question_id": "gk-1977-chushi-js-nantong-shi-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-291fc57797d8a978bb9f42288912b9d711a7840dfc6879c65d8fb440ecdebc06",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0428

```json
{
  "affected_paper_ids": [],
  "fingerprint": "902dca58cb215c5c978b58000fdef400f727336d5cb42999ce4f2379529120e5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0429

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d9110fcb6c0af0cc00a61cacd0e3b3116b4c43820a95ab340d253d29be1c9bc9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0430

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1dab5726f408c5587bc2da79df6ce5ba88969c3c8474444e573eb27431ffab03",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0431

```json
{
  "affected_paper_ids": [],
  "fingerprint": "135ac2ebf92b1b86c65e151eb58c96eeafc825f015b61cafaf11c605d57c1d31",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0432

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6e8dca728fdf28dbcc97a8cb94b11a48ae42e61e4185685aaaf986bceda9bcaf",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0433

```json
{
  "affected_paper_ids": [],
  "fingerprint": "364fe9cecc1646bdce679d562bc1c43812a42aadb6006edfd3c7388df8f9629b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0434

```json
{
  "affected_paper_ids": [],
  "fingerprint": "662350fee18ae79c149c6a756501a9652d6e72512280915ac0cc03881ebf3c8a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0435

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b4a54cce1f8ddc1848bf2805f3904886865dfea7fff897fb514f4577aeb4b02c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0436

```json
{
  "affected_paper_ids": [],
  "fingerprint": "05f50a23b8f16ba5aa642da3920dcc87f296bff06e9744b4cdc15bfe1a40aadb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0437

```json
{
  "affected_paper_ids": [],
  "fingerprint": "64fe30c525c6c00fbf931c215a11b4ea6edcd3039565457ddf73a7cb0f7d587c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0438

```json
{
  "affected_paper_ids": [],
  "fingerprint": "951a28859eb4fdddfd06bb1f8952bea0a5513dbd8a01b109f529865b337fea52",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0439

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fc533b5cffbbc8ab15aca2705615a7840165d2a68a4bac6bdd0070e72b3cd2a1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0440

```json
{
  "affected_paper_ids": [],
  "fingerprint": "117972ee7381dc24de8cb6e6906af5ed2ca1928de3589d22cce09b7653ae52ca",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-changzhou",
  "question_id": "gk-1977-chushi-js-changzhou-q13",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6457e830fac3765fc09b5595e1d36d1403fa11874026027fe904e60aec1d5f49",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0441

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bf1200dbf8fcf24d2b0401515abde4e770ff7a6800af5552ee09b4462af9d203",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0442

```json
{
  "affected_paper_ids": [],
  "fingerprint": "21435d875c823decf8aff77086ff21514ac5ae9ec91192ffc4bb8361c431754a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0443

```json
{
  "affected_paper_ids": [],
  "fingerprint": "973d13351c585190dd199f7dd58819f891522f1fe3390969b76dd86b790ff7bd",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0444

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1b6e04d82ae93ac725904d8d06264047d28e5c004826383f8f53bbd76f731322",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0445

```json
{
  "affected_paper_ids": [],
  "fingerprint": "537a09624bf586c36d792db8f19f14e278a5256e346e26da156c0eeeb0c37a7b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0446

```json
{
  "affected_paper_ids": [],
  "fingerprint": "43a1b4336bf29ee8c99e7afd1589beb8e31328fd1a8d189fe54f1dd45f68771c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0447

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d13024bcf3438c31e527edf2e5aa2b4e24fab437a43c88c66bad6794c73dd98c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0448

```json
{
  "affected_paper_ids": [],
  "fingerprint": "211a00e8665ee1aa7b9a6c0c4b55699eeb324c5ef1a552ba852149b50eeb5d85",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0449

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a782e4e1f8226cb8c9d3d16d61a704c618db030dac450b26156d623073e74fbb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0450

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f8a9dbeca4920c8ae56d25ae0725553097efdbce2e4ce0059788393529894d86",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-xuzhou",
  "question_id": "gk-1977-chushi-js-xuzhou-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析中间步与来源说明分值分布错误，已改正。",
  "source_id": "src-00c3e553b11512701cd6d349c599a770513dda541a7acbb4d3ec0b2ed5ba8557",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0451

```json
{
  "affected_paper_ids": [],
  "fingerprint": "350cb9aa34c22146ab00a08f246dd69c502f8a3ebee85baa3c4132b80e981fb9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0452

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8bf858307e844eff8004ab72467695cfb25a04f589613a80ac93ffc2e6d2cbc9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0453

```json
{
  "affected_paper_ids": [],
  "fingerprint": "65940c9952d78e9f94925d35813e7be75c0f8f9e726171310a2c7b098ae1f633",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0454

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1457fef08eb582e3da0e3b6275e459fc60bc45c51ebfbbc15f1a50219b93cedd",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0455

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d2619a636631449596e3faa00c1359a4d05c5f0c6d28e98762cc2d9cc173e452",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0456

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1985d881547937875f5a592aa441cffe07aa65e77c8f2cb9cb5809e6b5213b33",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0457

```json
{
  "affected_paper_ids": [],
  "fingerprint": "99dd07b6afe7ff726de59e5bf8ad5320f95fed4a6e5ff10117ef08bfc5fa049e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0458

```json
{
  "affected_paper_ids": [],
  "fingerprint": "78edaa85c806f525a3a007b188b3aa19b91c3952b2ce6600db848e472a7d37cc",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0459

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4e593c16bf19ae678d200d33afbaf918b3639dc1a91a74b14b2f944bcfd61782",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0460

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8eecc2f91ac16cbb13ea5c593f448301217f132d7e1ae75f0c3d71b9c5af4306",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yangzhou",
  "question_id": "gk-1977-chushi-js-yangzhou-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-ab38c726bbf259d4ee5f02f0b5bd03d88c502550e82a36a5595b705818faa930",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0461

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5aaee0e0b7c91193fc0ef5e64d9db8ea8558fa33440b7706a3839d342417c8f3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0462

```json
{
  "affected_paper_ids": [],
  "fingerprint": "821f6cf4be6c591b69263dd62b67cc30bc14aab9d1ee99ea0d0200127ee6db5a",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0463

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2de3ab87f31fdfbf11549474f4eaf5fcad465c5d672c486d7bdfb1b31034d024",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0464

```json
{
  "affected_paper_ids": [],
  "fingerprint": "77db49906182121faba26405a6c87b5ae94285977501f6c90cdd1e5406b6204b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0465

```json
{
  "affected_paper_ids": [],
  "fingerprint": "432b10d8da32d107caa9544f9556e3f2eac9e10fc1535861eb143c0bc488b380",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0466

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7cd5ec74d42ed0f88b82a9770ab7d0a058ed5f91bdc74e6a0e4bddb1eff29f55",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0467

```json
{
  "affected_paper_ids": [],
  "fingerprint": "06b6a42a5c04f1689c0e071356a4fdcc2061e674d7f799d83fa9644e01854420",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0468

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7602c46d35a9fa24e023b4ea669401b3e13355fcdb771dca950f51b5f75224da",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0469

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9bfe431d575c22ea947d5f6b565102f68601d46d1273aa9377a2f09267d22d71",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-wuxi",
  "question_id": "gk-1977-chushi-js-wuxi-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(1)题第三空 x 误作 1/3，按字形拓扑证据改正为 1/8。",
  "source_id": "src-1f6fe97938b8859a847ae91a239a3aab88461e76dc143ff6c9984af7b772e00a",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0470

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a708dc861d3ff60548b76f472f2810bae39c55d4a5fadc0954e7dfb3669cb61d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0471

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ce1b92c461758265ff76a9ef6055371d554c6ed484678a047cc73df26879ef02",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0472

```json
{
  "affected_paper_ids": [],
  "fingerprint": "007492057cbb6248f3c3f9c8cc8be8a6b41493e4ac9b1a198c173d769e451699",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0473

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4ea26700c5cfc93216a2b561b261c42332fefe711d070cc2ca58bf7f288a9bc3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0474

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7f893502c86a13edb0f869debfc8885113279d1300ee9afeaff89e63cbf41006",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0475

```json
{
  "affected_paper_ids": [],
  "fingerprint": "be98c33703053e740f7d8e85e4bc9406a67055c68d63a60aca03a4d7f0aa153c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0476

```json
{
  "affected_paper_ids": [],
  "fingerprint": "01fdf24c2d01cf1f3fd984b27bcbbb99485715c3d9bd8b82752cb3dbdeb5ca8e",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0477

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3d35608cc7eca0f195008eb536b83e509d1892137936ad86d799560100b490e8",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0478

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d21f9a9f59cc39bb80884b260ea4c06278e1f81e8a5238d7b340b4f9db58516d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-huaiyin",
  "question_id": "gk-1977-chushi-js-huaiyin-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bdee7399437d102d22cc6c98a434f0e813796b714736294830d50aa18b5397f9",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0479

```json
{
  "affected_paper_ids": [],
  "fingerprint": "808edd4d696897c1f070e6b8cd31d1e0243a6709ed20fd91253e3e24c8e3ed95",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0480

```json
{
  "affected_paper_ids": [],
  "fingerprint": "255cae1642e83db16de2ebcfe8f19d49d9867fac4e451a9df2b719ac68520dca",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0481

```json
{
  "affected_paper_ids": [],
  "fingerprint": "70d054857348a284f25696d893f5aff80fa16b1e2ebca761bf074bef6a57cf26",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0482

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6363f3bada0713f1498c65c7f3172b6a8cd49435b427d4358f21b352c9f2b8e3",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0483

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4ecafa28e6ef2d45c59b64ff6607984906ceffbe9c39989024c92ba470233510",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0484

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b7c70b77167e2c576610b8fb639e755f87912d9cb6b9bc467c8d0a63dac93043",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0485

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ed31672802689d484056da1d7d6e212add93dfafc4e9d9a5b359a1badfb11041",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0486

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e5a2bfb85c21ea634c0e9df1c7d316a68a972c4e9dd4b725161d95d507e6dbc2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-yancheng",
  "question_id": "gk-1977-chushi-js-yancheng-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题两行公式超版心，已 aligned 拆行。",
  "source_id": "src-27455a047401a5371889e71b79e909aea7d8ffd5adee64cd9601e052eca65b82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0487

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7e4180bc1d59ed797cef9f82c200b4cb5fe4b9b4c9f44b3e122026c6b06c98a7",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-diqu",
  "question_id": "gk-1977-chushi-js-suzhou-diqu-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-55844654209df25f211ea632854cf55d8e13c8a1951184b7141d4d051cc36297",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0488

```json
{
  "affected_paper_ids": [],
  "fingerprint": "36638c7eb69f27fa2491ec5ba08e545b51b76ca9c251ee141068c2d2fbbb51dd",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-diqu",
  "question_id": "gk-1977-chushi-js-suzhou-diqu-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-55844654209df25f211ea632854cf55d8e13c8a1951184b7141d4d051cc36297",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0489

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f794c3b100b8752bec2853f2307a7a351d644f76ccbab7a1f907769b79f8e126",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-diqu",
  "question_id": "gk-1977-chushi-js-suzhou-diqu-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-55844654209df25f211ea632854cf55d8e13c8a1951184b7141d4d051cc36297",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0490

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b69bcd1576112e92459baf727008fe9acade62b462a0bd5e6bb8f31b1683fe36",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-diqu",
  "question_id": "gk-1977-chushi-js-suzhou-diqu-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-55844654209df25f211ea632854cf55d8e13c8a1951184b7141d4d051cc36297",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0491

```json
{
  "affected_paper_ids": [],
  "fingerprint": "362f409f0bca096536e942b100533142911c776e79636385d64c3c39f01687c9",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-diqu",
  "question_id": "gk-1977-chushi-js-suzhou-diqu-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-55844654209df25f211ea632854cf55d8e13c8a1951184b7141d4d051cc36297",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0492

```json
{
  "affected_paper_ids": [],
  "fingerprint": "da1ff361a8793d2b97613c86f818d2d374389d3f3b767c72cc7144faf17f7045",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-diqu",
  "question_id": "gk-1977-chushi-js-suzhou-diqu-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-55844654209df25f211ea632854cf55d8e13c8a1951184b7141d4d051cc36297",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0493

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6f5a08048770a01979af06b863914db3b45f89df2529991b4f7c3221b8e02727",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-shi",
  "question_id": "gk-1977-chushi-js-suzhou-shi-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-53fb3671367861e803496b755ea5411e7cf570b35f32223f2ee2b2cd8c454b6e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0494

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9f13afe1ea6aad58cb234471b86d11e21420ae22a2878a0f55af9e8a1d6d428b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-shi",
  "question_id": "gk-1977-chushi-js-suzhou-shi-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-53fb3671367861e803496b755ea5411e7cf570b35f32223f2ee2b2cd8c454b6e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0495

```json
{
  "affected_paper_ids": [],
  "fingerprint": "52ad4db9b76885d958b44328a59132b2b65613c98a6f548b44bd9c4670a76efc",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-shi",
  "question_id": "gk-1977-chushi-js-suzhou-shi-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-53fb3671367861e803496b755ea5411e7cf570b35f32223f2ee2b2cd8c454b6e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0496

```json
{
  "affected_paper_ids": [],
  "fingerprint": "503d19fe8e892d59f7a475bea3abf1a77f6a3387882d58734dedeb61ba31c22c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-shi",
  "question_id": "gk-1977-chushi-js-suzhou-shi-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-53fb3671367861e803496b755ea5411e7cf570b35f32223f2ee2b2cd8c454b6e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0497

```json
{
  "affected_paper_ids": [],
  "fingerprint": "17ac891fd792047ec629d7798ece6882abd05b1d80ae66a72db2011c079ca328",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-shi",
  "question_id": "gk-1977-chushi-js-suzhou-shi-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-53fb3671367861e803496b755ea5411e7cf570b35f32223f2ee2b2cd8c454b6e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0498

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a6be57c824af944320cb52ba55da389353ed67ee66f5357b74a533cfc0c48c32",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-suzhou-shi",
  "question_id": "gk-1977-chushi-js-suzhou-shi-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-53fb3671367861e803496b755ea5411e7cf570b35f32223f2ee2b2cd8c454b6e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0499

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d80f908f35c5a1d9e399b8a8d4bb29ef283370d6ec53ac94ac7c142127dbd947",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0500

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2341ad15936fa568b1ff8327c66f1278f22b25020a1b720556f45521e0b0f03c",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0501

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9b09b7c584a317fe0ea5665cd9b21a520e4477bf6bae79224c1664a1b4f8a0cf",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0502

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9986366c03c97a16523104f6677446909ffef7a588d2031ce981296ada89c640",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0503

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a01ef3bf6bd852e37748adbd34b4decd632a87f4e7a5cc8a90ebcbff2abff468",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0504

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cd5ccdfd37c648a4c414503510d1bb7162563fa45fedcfbb8470ae40d97d49b4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0505

```json
{
  "affected_paper_ids": [],
  "fingerprint": "af5ed1cd46d9745ed29905ea6d9f948f733938a1ff064361774c577b0effc2d5",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0506

```json
{
  "affected_paper_ids": [],
  "fingerprint": "29e124dd55d773b6d1672fa49445a53141b260b7f91e1960871c470f85f0be77",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-lianyungang",
  "question_id": "gk-1977-chushi-js-lianyungang-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第2(3)题分母根指数误读（五次根号→三次根号），推导与答案全链改正。",
  "source_id": "src-b041ff9e546e0469e647b183163556a695bc9e4b7f57ddb7447daed97c8f3dde",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0507

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c794dc91faf44da7cacec8fb57de7c14c682b67f4eb81a36be8ea36b6a50637b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0508

```json
{
  "affected_paper_ids": [],
  "fingerprint": "21e550507022c3a41fe48d55d573c9d69e1c252cd99be0e055ad3d6f69362469",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0509

```json
{
  "affected_paper_ids": [],
  "fingerprint": "80246b934d49c7fe2bb8e049e1e60f95871e3ad9478d87a653ce2140a123dbdd",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0510

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5a8c5b1ca1164b464397a7841c1c60430ad1e52591ca3b46327d156068c29baa",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0511

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e603010c94c726cafe56ee5cf45f8145f4d6e48d7c968bab7d1c46b081d211e4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0512

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a31a68c1e35e20221a57991a2c1551e63ba7cbfdd27f8657d8dcbdf1a80708d2",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0513

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9b7fea89f2e5d186718f7f5739b5a119114686e55a223b47cb20adb04b6ef695",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0514

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a9b9ce1592fa96f1c077781f4c1bcf2aee0d0a5b8b8ac131f1442f72099a46ba",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0515

```json
{
  "affected_paper_ids": [],
  "fingerprint": "05e02dfc809a752846318903fc7d0a5b2a09f66e42abe74e7fd59fbf4930de2b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-js-zhenjiang",
  "question_id": "gk-1977-chushi-js-zhenjiang-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第9题漏抄全角冒号，已补。",
  "source_id": "src-41e12e57af2ab22740d3d68b95daaa3d31b67c1de01b944ebf1e02d4067bb3ca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0516

```json
{
  "affected_paper_ids": [],
  "fingerprint": "98b736223d8330b43ea816a7071991f7aeeee22247b627ec335b1f3d0eb6634d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0517

```json
{
  "affected_paper_ids": [],
  "fingerprint": "926ff1777e4d2618ac930f3cf57660888ce75df62b8cdf1c41e3df96a4e385e4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0518

```json
{
  "affected_paper_ids": [],
  "fingerprint": "12246314d5788f7353b79d2ef71d5218763cdb5176344a77374b1a231a41aaf8",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0519

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f2c03b91b7cf07625b537f74ed8e83f3f7cb63f3347a485e6ff366a446e07648",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0520

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9c6496175a67441dbe9aab317382b47d6e6eb5430b00af50d8b056126073fb1b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0521

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bda4e14318cfcfcfbe844c267d8a4f530a5efd526da667aa2506ac9cdc3ec485",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0522

```json
{
  "affected_paper_ids": [],
  "fingerprint": "602ce4b59aefc894c559f477955dab44f6b50869ecbe7c023d18f5cb867b965b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0523

```json
{
  "affected_paper_ids": [],
  "fingerprint": "afef48ecddab6d0ec9dc6b9ddd57788e6ce717c717a4e703f5e56afda3466feb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0524

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1512ddb1664715241359c9ecd0a7eb2e14d9bc6aa11f9edd0a9773b22dc48b88",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0525

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c3b510927dcb5a14a00cfb1b0002d8670e33465c974596a501e11b1b747c0f81",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0526

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8c8c263575a8407623f07cbc160513c146ea2389d38aecd220ad3b24834cfab1",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0527

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8c4b78f849edde0cc463f8284d54c05e5e7cb5b2fa701accb8f8b5a0e64f4a9b",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-chushi-hlj",
  "question_id": "gk-1977-chushi-hlj-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-81d53f406529461dd00450bb31358ae154275388b8fb3f8b0e6accb77b77e340",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0528

```json
{
  "affected_paper_ids": [],
  "fingerprint": "df88c30c1f8ca42d93053cd755c2b8cf062fff0454aaf6d9baa0229c32db08e7",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0529

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0e6c482bc912eae726ddea978b4049bbb9c1d8cf71c16c4fb79f51f4c16a2570",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0530

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7d0e8abf601cab03064cdd8bf98297b06dbe273512f0cd81d02658f17324fda0",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0531

```json
{
  "affected_paper_ids": [],
  "fingerprint": "01700876888228cc8020448f80c380c202636307fb80ff923955d750c5160941",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0532

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d810f75b0d698d55f24f460eb80714fb3033ae8e876fe4b82119541ec79c088e",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0533

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1e383a27c40ad839fc0816e7b75d4b0249e630e50c0f54123a583fa20391bbdf",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0534

```json
{
  "affected_paper_ids": [],
  "fingerprint": "051663f9501e225404f72239fd0fa90dfaafbd46386e3b42f2d581acd95c7c55",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0535

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cad231a7c2c02cf82fd2e6930fbaa9e7db73a1598d19fcefda8a90b25f22d1a8",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0536

```json
{
  "affected_paper_ids": [],
  "fingerprint": "37d9b8108ac20aec3e3402ec6e16c39f9ba780ee309461bb512a6ac5e5407bf5",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0537

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cbc7abcdc4c4bf2e047288647b0c3e26e7d79475b79dc5f240f9eb72fb1058f9",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0538

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a1542d00b183ae15519ff34fc6cfbf4bf379aadaf31a87140bba70c4e7e096a3",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-beijing",
  "question_id": "gk-1958-regular-beijing-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-0a220bc0c47e25e6425ec061b7fbdb404fdd9130d3997645aad139c89adfbae4",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0539

```json
{
  "affected_paper_ids": [],
  "fingerprint": "01f293f668636e38772a8483f96e9d7add259a2eebaafe4463f252b61a7c8822",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0540

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9c66762aa4dc3fe8a9e3627a03921509200285137b137203553b87d4b1b53e59",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0541

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4ed5ab599ee5cafa24d596171c133656a12b80471827c6c4620ed3ef37e35c18",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0542

```json
{
  "affected_paper_ids": [],
  "fingerprint": "71442f9350da2545e89bc1c7f68ff5151658937d59ca156bac828c9f18c4493f",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0543

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4577dd9b3b7feb09d9e89d2a8265c494fb263cfb9ec03c57ccd1e149dc9808e6",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0544

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8df71e72d661c3a4863a47a0afbbcbf717afe840d084fb8f675f485ed0899360",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0545

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4c738964eaba789e6f518451a3ccb3bbda6cbb601f2a3a79fa9786fe7bfa0d6e",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0546

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e5d44d0e3d41ff1bd596d369535646121da68fe963b86c81e4fd9b50011ff4bb",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-yunnan",
  "question_id": "gk-1958-regular-yunnan-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6e2b6e5284b79bd5a6a5cc1693e013554c9caa596ee63bd629533c5e71f43d62",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0547

```json
{
  "affected_paper_ids": [],
  "fingerprint": "504f84cd0dfe9b67e900e355ed9ef64d6d8dd99bd2f8b54df80b0e3ca16d8d9c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0548

```json
{
  "affected_paper_ids": [],
  "fingerprint": "76cabf59c6b89b1f058f1772dc41e8a1097f0f073e0cb97171d8d974c2a3ada2",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0549

```json
{
  "affected_paper_ids": [],
  "fingerprint": "92171fcb77f59fb90c2a4cfa51b1978b95721e764788d34b65ae76092bcc9f1d",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0550

```json
{
  "affected_paper_ids": [],
  "fingerprint": "de859b61c0c802127e22499fee89c359445cffce07ca052838988dfa88f0523e",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0551

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6e93bd7598d308da4ebe543b01a8aa1ae7637ad04cf63174bd18d8b8a5449390",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0552

```json
{
  "affected_paper_ids": [],
  "fingerprint": "23682013b0991983b742c1003d12df87fca831dbb54d8b493cee1d94bd56289f",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0553

```json
{
  "affected_paper_ids": [],
  "fingerprint": "64bb9145d2b89c83b085583b00ca289ddc89b3b9dacf03915854bbee2971b627",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0554

```json
{
  "affected_paper_ids": [],
  "fingerprint": "024fc03458754897522516425d8299526e9f5a6d693cc8d14dad22c4d4fae33a",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-sichuan",
  "question_id": "gk-1958-regular-sichuan-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第6题 x=1/3 自相矛盾，改正为 x=1。",
  "source_id": "src-ea1482a1ad738f07e6662725892efaa52dc53530d273cc305c78d169058ccc43",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0555

```json
{
  "affected_paper_ids": [],
  "fingerprint": "443edfe489eaf7dd3cfdb85cd213f84484dd7e8acad8fe85bff463468be78ca2",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-jiangsu",
  "question_id": "gk-1958-regular-jiangsu-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-608b96d22ae47061173180665494408e8314181d2b954c8ab2fd2bbb4accb80f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0556

```json
{
  "affected_paper_ids": [],
  "fingerprint": "80206bc3ff2ff063d1784d62f74792e5d997261fcb213d6dc59240758bb3dd0f",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-jiangsu",
  "question_id": "gk-1958-regular-jiangsu-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-608b96d22ae47061173180665494408e8314181d2b954c8ab2fd2bbb4accb80f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0557

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3cfb97e6f2a09c72739a817dd860a7f4770f084f1e756cf967388c7db6e54ae7",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-jiangsu",
  "question_id": "gk-1958-regular-jiangsu-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-608b96d22ae47061173180665494408e8314181d2b954c8ab2fd2bbb4accb80f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0558

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0c6f73249640eb48fe373f5adaa7fcaf8b12004967674c71a5e5efeec1268281",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-jiangsu",
  "question_id": "gk-1958-regular-jiangsu-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-608b96d22ae47061173180665494408e8314181d2b954c8ab2fd2bbb4accb80f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0559

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b9691bf367b3c6659e4a514b3a2de81c35f7b78e8a01bf303fcdfd68b8311bba",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-jiangsu",
  "question_id": "gk-1958-regular-jiangsu-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-608b96d22ae47061173180665494408e8314181d2b954c8ab2fd2bbb4accb80f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0560

```json
{
  "affected_paper_ids": [],
  "fingerprint": "952ddec511bdf6b7ea1130a3dd314711a75559fc479ab94932256daf77f35d46",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hubei",
  "question_id": "gk-1958-regular-hubei-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9040ed276c30bd1a6b34b15c925e788b47e94be0d7455e8aaba400a3da97d00c",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0561

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4590b285cec0572b3e4a73ae47ebef120f80b206c73d5f0b3238190740dd0506",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hubei",
  "question_id": "gk-1958-regular-hubei-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9040ed276c30bd1a6b34b15c925e788b47e94be0d7455e8aaba400a3da97d00c",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0562

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4dd4e7abf2d53975fd505ed4b0d9444825e03ba6a41fe4041866ea39d4407ea3",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hubei",
  "question_id": "gk-1958-regular-hubei-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9040ed276c30bd1a6b34b15c925e788b47e94be0d7455e8aaba400a3da97d00c",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0563

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2d3d975b9c009d74a5bb80cc78ae46dc9d243e5ecec16725a427db6b59444d4c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hubei",
  "question_id": "gk-1958-regular-hubei-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9040ed276c30bd1a6b34b15c925e788b47e94be0d7455e8aaba400a3da97d00c",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0564

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ed4cb84ae7febb1509c62fdcd5d52f2e1009ed0aa8309cf77341128d1722a062",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hubei",
  "question_id": "gk-1958-regular-hubei-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9040ed276c30bd1a6b34b15c925e788b47e94be0d7455e8aaba400a3da97d00c",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0565

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fb9f8c8becdc6795f50bf46801c3435bd55ebde7bf79948b5bd9af4583be20fd",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0566

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e3af23a7d7fdba8570d926ed0ccefa5115bd41b87b09f509bf309c95d7c54fa5",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0567

```json
{
  "affected_paper_ids": [],
  "fingerprint": "afec533408a33fdef9889de42af06d3c04c5ae28556f472e4e22572acb95d343",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0568

```json
{
  "affected_paper_ids": [],
  "fingerprint": "dddb1094cedd548ed90a38bb246389de4681adcb35f2eea8cf3d2bda551dbb83",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0569

```json
{
  "affected_paper_ids": [],
  "fingerprint": "36f4c50526daee3c59cf76a7b2cc7ef502cef3ec50a556ace7437b360c7a181c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0570

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6d111e3d296048b993fba21f49ae925aaaf2ad0c4e502f9cb32a06390e55dfc6",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0571

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7d4f54d251d8e94f0539ebcd6aabf039d8def8254c9cbb99ac66168150559413",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0572

```json
{
  "affected_paper_ids": [],
  "fingerprint": "30d9a67bc0ff5975ac685ecd5d6e7a73fe6b7648f05167e566667277fed86c7c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-hunan",
  "question_id": "gk-1958-regular-hunan-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-1a4d35af9cd4f4f9a8581f9694e54af955e3a8f8ab9435e10032e3f48d96cbf5",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0573

```json
{
  "affected_paper_ids": [],
  "fingerprint": "d6061dfe9ad296193f48a18b354d45b144607dff5c4c12f396f68732a357475c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0574

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fbd26a0970906c059aff5aa79f7171a2047c5a60400bb9e1260719d11807a015",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0575

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c2c874a441cd64a0ea56f567e9176836d21ef9ff0402a22b170649c1cfc98404",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0576

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b9cec6b45d9e6543894a886b10656e2ef5156810a81545478fd168d7f227338c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0577

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f029763ab1830fc9a44f5aca031bad4022ea0207ace55bf3e6ef31372409a49b",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0578

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8b45dfe5aa654aa28c762fbfea442467a6e13c7c947931af8ce231ae85d5679f",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0579

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ca256d33bb847cc132cb8c631b4fde8edff837126a540a7fe62e9e3fd44ca345",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0580

```json
{
  "affected_paper_ids": [],
  "fingerprint": "94ccb81b48a513300831308cdee650644105bbbcd24a80ad4df2dcafbf5fbb62",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-dongbei",
  "question_id": "gk-1958-regular-dongbei-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1题解析公式溢出 21.2pt，已 aligned 拆行。",
  "source_id": "src-f68456b6b95f99585c1c9d307b6d6427e16ad3ffd755c5536129168b478d106e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0581

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f3a2aec5d7a6d702a4a1340e2d0e321e4b628710af9310713ddf7bfb26cb8efe",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0582

```json
{
  "affected_paper_ids": [],
  "fingerprint": "81293b08ba72e81b27df9a6735b8026f61fc2a926e814474f64c5c1fb2d19858",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0583

```json
{
  "affected_paper_ids": [],
  "fingerprint": "099dd0fa4768e6b806f8aec2e82f52148592e607bf41ae24063ca8b87380a2f5",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0584

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e1ffde4986d08787f8749ada9d0a4737d024d1139abaaa5f35879cbe7b80e597",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0585

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4122c1ca1994658f326f4cccbbe8b21a79d83c3148164f17154e5d36f97afc7a",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0586

```json
{
  "affected_paper_ids": [],
  "fingerprint": "aa2abc5ede19909592141235be303408991f26788f18a93a0161909835f96e89",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0587

```json
{
  "affected_paper_ids": [],
  "fingerprint": "47a4f2ea7d93cb28dc879f49516154d40d4a5d8f7de5014a25fa8db0efac0052",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-huadong",
  "question_id": "gk-1958-regular-huadong-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-f69565036fe83184140e7d1ee23869c1fad1dda027201326db20e04699235610",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0588

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3f0d6c12c6166dd50c89df2a1a8e35b68e64828c7f6b8463d89db2f3d76b94a2",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0589

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6ec76ba256964b7a890e506e07a2ac56bbe5efccdaac1ed8eacbb0acded6eee5",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0590

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e60839645857062e975ee9d63543619b5a88195b0d1ff867f6192ef8151975a0",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0591

```json
{
  "affected_paper_ids": [],
  "fingerprint": "aa0e0a3261fcd6dc9e3bda8893972dee4ffc04c0d013a995ad9a8f2502113c9f",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0592

```json
{
  "affected_paper_ids": [],
  "fingerprint": "22448cc8dc5846e88e1872953d66c691639d84d5281f26336edc6d00aac552ac",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0593

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2f4fd52b8587d77e43013f487425a5baaf37009b869ebd295fcf0b4e149fd39b",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0594

```json
{
  "affected_paper_ids": [],
  "fingerprint": "08a026493220c4c58bbdb4adf37940acc52dd4eaf0ef908d2c53a3ab345aa9a9",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0595

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0a4c3f25f2400a77ea0f5119ecd13e5a3f8bed492969016f5a44b2a810bd4001",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0596

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ff2c1d2e017927548c9c4f6b8fe3058e8a4dde194056e92b141a7f4b2d658577",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-guangdong",
  "question_id": "gk-1958-regular-guangdong-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题图缺 OE/A′D 线段、第9题图标签重叠、第3题图缺 ∠1/∠2 角标，均已修复。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0597

```json
{
  "affected_paper_ids": [],
  "fingerprint": "09adcd995f57fd7b86afac4376f16d3fffd98331e1de1c3d41cb1beb76b89ab0",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-anhui",
  "question_id": "gk-1958-regular-anhui-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-17b184d6dc2e3231605a9d571594435f2dafeac4a6501593b8131baf1658299f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0598

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0b215db743c8ceddf34a9bd44e44f20ac1cb4bc8913dcc907064e0e22ba0f07a",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-anhui",
  "question_id": "gk-1958-regular-anhui-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-17b184d6dc2e3231605a9d571594435f2dafeac4a6501593b8131baf1658299f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0599

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1954fc1f24be6018d466d96b65574127689206e8492edc51092833411f228caa",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-anhui",
  "question_id": "gk-1958-regular-anhui-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-17b184d6dc2e3231605a9d571594435f2dafeac4a6501593b8131baf1658299f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0600

```json
{
  "affected_paper_ids": [],
  "fingerprint": "006a2c4154bf3a1dcf54035e354ec316fddc56710071402d025b16732592bbea",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-anhui",
  "question_id": "gk-1958-regular-anhui-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-17b184d6dc2e3231605a9d571594435f2dafeac4a6501593b8131baf1658299f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0601

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3b749c2cd3a7380c786a22172f02a9f33a5730e92c1f1fc35b8c9fb3b0622c58",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-anhui",
  "question_id": "gk-1958-regular-anhui-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-17b184d6dc2e3231605a9d571594435f2dafeac4a6501593b8131baf1658299f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0602

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a950c1e2e38c2232f320932cb2ea521d4dedc36b4d64fbda33114ee268863df0",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0603

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2e007bae361ae8bd6bbc32da1be403058afd8dc305012de2274f446fa6197ba7",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0604

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0e322dd5fb8f50647ddab164730a869e9dacae9d45b7bbcdf49162f73dadd2db",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0605

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7e4299a9ead9903bc3d7613e7d3e25d1b84edfaede2d6675ba20104690a572b6",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0606

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ccabce8b97ee8536c7a13b144fe283bb5e1ba3dc7768521de4751c919567b33b",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0607

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a33bd3cc5e24584653c8aa562f08a78c70d1e4d5fe1b8dc314b73697edf64036",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0608

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b23f2615f4a790ea3deef622b80dc094960013dc024f9c06750248dec4757c85",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0609

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c2ce548be5c8e4fbd19f33055729a8a4034e49cd14dd2f2a5f9b101b96db530c",
  "impact": "blocks_completion",
  "paper_id": "gk-1958-regular-unknown",
  "question_id": "gk-1958-regular-unknown-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0610

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "67ff33b961da8b56b3c0e51d292e17a834096100080257e11979f4461a8da660",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1958-regular-guangdong",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0611

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "3acace3b20efe1da00a3f8370009fe98f0c0f291c1193fc8cd12678594d0e65f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1958-regular-guangdong",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0612

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "36f47ea44353d4bae608f7a5d1122daa84aadc3bc741c6b521a06f2039ab362b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1958-regular-guangdong",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0613

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "a5c097df1a09f05e92a1dfe8797560fca006aca564d798b22eeaeb940f478a4f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1958-regular-guangdong",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0614

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0d6fe2992de746cc90f0547ecd8494e27bc70fb301899dc630325a498a17f877",
  "impact": "non_blocking",
  "paper_id": "gk-1958-regular-guangdong",
  "resolution": "固定源（登记版 6 页，SHA256 7f9e7576…）第 1 页标题下方嵌有一行现代黑体文字「存在其他版本为(1+2x)的5次方,答案为80」，字体与渲染方式同周围 1958 年印刷体明显不同，经主会话视觉复核判定为后期插入。该行给出的「80」对应 (1+2x)^5 展开式 x³ 系数，而原卷印刷体题面为 (3+2x)^5（系数 C(5,3)·3²·2³=720），属数学自洽但对应错误题目的诱导性注入。转录已弃用该行、采信印刷体原文并以独立复算验证 720。已抽查同批 1958 不明卷、华东卷首页，未见同类插入，判定为孤立个案。",
  "resume_action": "已处理完毕：图像证据显示为后期插入、非原卷印刷内容，无需后续动作。",
  "source_id": "src-01afd96d355e65819d9d78d9636cf1b6d3995ff70a150c69b0752caf86bc90df",
  "status": "resolved",
  "type": "source-mismatch"
}
```

## ISSUE-0615

```json
{
  "affected_paper_ids": [],
  "fingerprint": "dbf59743533b2db80b340e660df1d52531bc5e2dec6602e7fc5555cd87430d57",
  "impact": "non_blocking",
  "paper_id": "gk-1958-regular-anhui",
  "resume_action": "待人工核验该卷真实性：若能取得可核验的原始出处（1958 年安徽卷官方或权威汇编），据以替换固定源并重新转录。",
  "source_id": "src-17b184d6dc2e3231605a9d571594435f2dafeac4a6501593b8131baf1658299f",
  "status": "open",
  "type": "source-unavailable"
}
```

## ISSUE-0616

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bd63ccadbd016ff54f4dae112c160e30661842087cccda62b838a5d01fe789ff",
  "impact": "non_blocking",
  "paper_id": "gk-1958-regular-unknown",
  "resume_action": "待人工判定该卷与已收录 1958 云南卷的关系：若确认同源变体，在总目录注明二者关系；若确为独立卷，补充卷别署名。",
  "source_id": "src-d74a85da81acae2d6c5208fda43394e5cb7f90a57c69db22a05d65283fbb909f",
  "status": "open",
  "type": "identity-ambiguous"
}
```

## ISSUE-0617

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c64e0be3ea342c320a94126feaa973004d9a9b223a83afbf981a9bb40d35a3ce",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0618

```json
{
  "affected_paper_ids": [],
  "fingerprint": "65b4e1d25c44cec7f8c868f8ffff42654ad8fb5b17f4a404702c0c8ef44dedcd",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0619

```json
{
  "affected_paper_ids": [],
  "fingerprint": "43ff4c9722b3e2f4bd82746566abb408e054b7e5ee4ce7188ace1a95d7c64c97",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0620

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0f45beb0210f44b8de1831723da2106bb9bee66a9f4fe195a71030d7157a47ed",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0621

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fba2207f55cb29e3c26cd58e788f55529f25d32085061394af120d9f5642ce4e",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0622

```json
{
  "affected_paper_ids": [],
  "fingerprint": "533e3245d8a6b36ed8de9f1b04e5b504f3b7e377ee61025aa37940e8dea0c55e",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0623

```json
{
  "affected_paper_ids": [],
  "fingerprint": "92ef3567f04325fe2b6905eb6a32af4f9c33086f12270a54224dd6c560c75ba9",
  "impact": "blocks_completion",
  "paper_id": "gk-1978-regular-national",
  "question_id": "gk-1978-regular-national-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第1(5)题解析复核句分数笔误，已改正；两处标点按原卷修复。",
  "source_id": "src-d57213ed7fe1f3230f088f4e49a791a732ceec813314d9fba5ed6e8aa63e4fcb",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0624

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9eb57097c7bf617d1bc6b73737575b0fb32c3e97817d51f4417cdb32819c665a",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0625

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bfc7220dbaad7b7d73ce7562a97e4472e0e68b58b3e626c5bf220c82a57ca93e",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0626

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6363fa13dde19e889d4e308de7996e96241e12f7dc46146cf9f8719b9cdfbc3e",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0627

```json
{
  "affected_paper_ids": [],
  "fingerprint": "446d130a36d8d35a3b8a8f2f25d75aa98f024d534164d51f419455148ee9b635",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0628

```json
{
  "affected_paper_ids": [],
  "fingerprint": "512b7e0122eed7df6f6e29a90f37bdfc55f16afad7515a0484fac8ca87f5871c",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0629

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6cf7b4cb1b8f8fac9e7456688af9a91dafb2c53c28aa143393e2e0029cd451e6",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0630

```json
{
  "affected_paper_ids": [],
  "fingerprint": "95ecaf019b3fc0d73db724136f71d5f37b0936b3644de53edc82205dd027ba6e",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0631

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b5fa34017b3485875a1ff5171ff4eb3577666726fcd1988ca66764afaea1bb49",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0632

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0fa3aae530d98d59ab32ad012f97308781709af4a0cf6e12559d50b90003d5c3",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0633

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b59066a737254338c90c8e56525f932a3cf691cfa92b2860445a738e62a680f8",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-science",
  "question_id": "gk-1979-regular-science-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75c48ad9a18a9198ece10dee7050086a9a5896d5bd0cac030efa73f90921a7a7",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0634

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cec5c024dd1f62f882d67929be095ed8ca1a69a50e15649c22b33d9f49a0ad84",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0635

```json
{
  "affected_paper_ids": [],
  "fingerprint": "89ef78f4a4bfea50b711354f767628515381845d15f2a1e0db748a9d34eb4a6c",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0636

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a3e4f5eb2dcf744233a312e501670bed590cbf908f2e836d1af6172745996b27",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0637

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bcedc8461cfea335e41a76eccf50df6cfd78a9808d3de45f99d532584fa9ff64",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0638

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a6bb03713dffc0aee7827e581faebe704d765bfe32f4ff6b34b9352f5a3bdab4",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0639

```json
{
  "affected_paper_ids": [],
  "fingerprint": "740299813f0ddfd0e566af526ec16c7c1ca003dcb2bb59a7994040af599c8fd6",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0640

```json
{
  "affected_paper_ids": [],
  "fingerprint": "53c870242901a94a9cdd9b64d1063f76722df2cd391e494087a21c6872078328",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0641

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a4a0d5188b2a6dea14b07c794f4e1704110eb1e8338b36fb4056a737f54322c9",
  "impact": "blocks_completion",
  "paper_id": "gk-1979-regular-arts",
  "question_id": "gk-1979-regular-arts-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第3题答案行截断（生成器不抽展示公式块），公式已并入答案行。",
  "source_id": "src-957ba5d59c707802462cc45f4e292549e0df575a79070f259af9546d0f9d25ba",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0642

```json
{
  "affected_paper_ids": [],
  "fingerprint": "951dde720e98d48a34219f496dd63392e92f4b510d668ded15046c884e7fcaca",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0643

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a4f55ff8b8876750829868a9ce522ead9fe41a65d540c894aa9dbea8cff45deb",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0644

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ae84aca6f287ded1e92fd15ec4fc9cafbeebce366cca9947d450917890e903c6",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0645

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f923e6b9bad0b5ed856c1ca23f955d17217d126fc02e56e457559dd765e9c5e7",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0646

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b5ae495c884ab83b7081264b6521cda17170840ad5f8be58dece8a3bf00a9978",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0647

```json
{
  "affected_paper_ids": [],
  "fingerprint": "91188ecdeb29f412fa2b6155aa8d050e5ab710c5c488c36122a7f049f71e2482",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0648

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a3d3aa68019326945b4e15bf270a55fd19011962d8514611422dda692d904c03",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0649

```json
{
  "affected_paper_ids": [],
  "fingerprint": "867e5fb2769b2bdaa884f291fe95cf8b52257d17c3e756e6e093c35786c4eedc",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0650

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7f9a02c3752992b95c742f1b35906ef6804a30fc69a84980a3a7f1e4638f59de",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-science",
  "question_id": "gk-1980-regular-science-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第5题图缺 PB 视线、第8题公式链溢出 174.99pt，均已修复。",
  "source_id": "src-17ee115a6c2cbd90785528de060ec9ff1955035fa68282c4c2f4103e79a3b902",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0651

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8ad967b99d1e60a5610938ac3b1689ac5b140496ac283423fbcd1df2dd8c2439",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0652

```json
{
  "affected_paper_ids": [],
  "fingerprint": "523172f42931886f0952ed6212d320d80ce3710b179c416922ff032cfba7a636",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0653

```json
{
  "affected_paper_ids": [],
  "fingerprint": "19705d1f0cf711fa5ffdd5ef7797d7651d05cbbc1b78d9b0231606d62779c8f0",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0654

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ae6a00a59b6a30f690ed14b41fd57a650e3e00b87667d86b5bb8b94c0be212f3",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0655

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fb66e4b7f396e41e81cfa80a787e5aa3634c51bfc5514d2389e98eab2be1e88a",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0656

```json
{
  "affected_paper_ids": [],
  "fingerprint": "52a78edaab9a9c1097171076d6f2f79f404f48ab6403b49cb580015e816a65c8",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0657

```json
{
  "affected_paper_ids": [],
  "fingerprint": "98f978358e1e1571861d3ccf9b3e7e02d6d75d846c2d4872ba4cf2598dd6c7a3",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0658

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1bfece6d8fc048077a86d0fb2bc70163a700d64b6d86e5d8b209193cf6636a2c",
  "impact": "blocks_completion",
  "paper_id": "gk-1980-regular-arts",
  "question_id": "gk-1980-regular-arts-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第7题长方体图缺 Cp-Dp 可见棱，已补。",
  "source_id": "src-79ee79ac09788d04e2fd4fe86728d3da0119f15cd57b7dd347042b61f3a8165b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0659

```json
{
  "affected_paper_ids": [],
  "fingerprint": "911f10e26e8f6f73cf179509cd35142fddaf68f5121b6b6b68777224ef4b2c0c",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0660

```json
{
  "affected_paper_ids": [],
  "fingerprint": "20750bbaf04dab4f738724327adb1a33a46e611d3edd8627abe97fdef9f33533",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0661

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3b0e959eb14743e312d3080ef5f789782102eb7dfcfbb016e82535c115204b50",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0662

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0f5dc330c3ef586dd2f1a8e101ddc5fd00c3accbbb4aeed52eb0da11ba55d4c7",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0663

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7dbefcad06aeb637d79b9613cf41ded80a84b60eb6181d19e3a81b1e9daa7c13",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0664

```json
{
  "affected_paper_ids": [],
  "fingerprint": "279f5f8e34bdf93433fd743eec965157531c8e13f5f1a8b2eda3a4d52cb02d12",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0665

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fa13ccc82d117a2db3db6a170b1ea133d3292a4018632c097b38738c12cf195d",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0666

```json
{
  "affected_paper_ids": [],
  "fingerprint": "23f95f159dff8ca698c8ab7fe53ed829c453ae813708d561b3fc0ecbb8265710",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0667

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1cddc02af6e40fbe0c8853b6f8ad386a7119dad00fd7477f7f2c1dd892bae584",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-science",
  "question_id": "gk-1981-regular-science-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-3508b5246c3c9910d0786f42f4bb64b6c9165c144a642dd3e0e6726f375ec392",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0668

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0b7e5a287a3b3439575827f7d6db0f7641b73d7ad5e73d12ef09703a53f3a77a",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0669

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4fc1b306d8ba7de6f63dfd3ac353058054933464c9c16ead452b7fc7c864a9c4",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0670

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e7ed8148c5d9a854f0167a1159ace25bd58379ace4d025f35525564894eb12e1",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0671

```json
{
  "affected_paper_ids": [],
  "fingerprint": "345dbc19c8e00fb077ce38899aaff9e7ca9a5c8c5fdbb5bb60d4a53b6534cb13",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0672

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1f0dd1a2e77a3a449bbad9aa79c750f6fe753480061672fef9f9de69c090a94b",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0673

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6b5dfb847dfbe8ed7374befea98d4818cefc10792fbc77e7801e5d4cebf0b2e3",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0674

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0f8ffe0424088494aa1b9caed75895add659dac61ee3d79ad7d412ab22b2ebab",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0675

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0cfddfd338cd4a6cd9cbee9d0fa98472ab0c00ee252096fb6db1afa8380cc290",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0676

```json
{
  "affected_paper_ids": [],
  "fingerprint": "921669d93757110bc74eda778ffea99dec88688600863d80db4b05caedacde6e",
  "impact": "blocks_completion",
  "paper_id": "gk-1981-regular-arts",
  "question_id": "gk-1981-regular-arts-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9d1618487cfaab255fb5f0103aced007158f2caf5ff2fde404916a814d781d3b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0677

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e3ab00a14997477d27d64d7856ec6780d1532f37a26e987aa831b12f2ba8d789",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0678

```json
{
  "affected_paper_ids": [],
  "fingerprint": "4d688a979b35cb019681f7bdc26bc474377e4e38bd8bc8616e0b5601ba2c2b58",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0679

```json
{
  "affected_paper_ids": [],
  "fingerprint": "73c507b2cae78e8e4b6dad6323a3948f89dff5e08d2981ec0d3b67c777771f46",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0680

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f0a6b76576c1df7cfe233dae0ab7bfceec2ba49b7cc32eb96657fdbc402c1a62",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0681

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fef9cc611b4204d73ac0b64dc9fdfddfbc603d6b6c174261dc63f8899195c1c0",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0682

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7f07420e9efae905a58ee04f3872124a1fbe8b1aae483b90380f66b0ea452328",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0683

```json
{
  "affected_paper_ids": [],
  "fingerprint": "ddc7a04ef0ee6aa4e9e68ce422e3919f81d9180b84491f9c0858cfd09c7c63b6",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0684

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3b407469ffa12579b6ae2e0f4fb23869a9a9d45ad9ff075a659cbf3ca3824983",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-science",
  "question_id": "gk-1982-regular-science-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6072baf1788c1fec5fee024289d04a4e7690a42211edfef62cad0a1b3e012dca",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0685

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bec5c5db7b4ed3279d5e594aee05199bb2d97390d7f58fa5d8a3d5543f903712",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0686

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bebb002293f18ca0ac68ca16b162b0f0a6a5edd735b04ed9fc3bc3f2845d1c29",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0687

```json
{
  "affected_paper_ids": [],
  "fingerprint": "59a53237d6505b48496fabc37395f313ce8caac328dcda306d7a60b2ea801946",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0688

```json
{
  "affected_paper_ids": [],
  "fingerprint": "65dc959a6a2017fb91dc01d1043a91464e54c2adf8ca45f343a26ff7ff24eff4",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0689

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2d8fbff70ae5d1baeea88f0de9f4bacce0d30a6b3775e86838f3c5d018a43efd",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0690

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b16592a15c322f2f5c8aa40a091eac51e032d431bf4fed0f5ad266ebf7bde608",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0691

```json
{
  "affected_paper_ids": [],
  "fingerprint": "261c2bcb8edb29d7130354376bc92104d380249ebfb42ce167ce193d19b1a6b3",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0692

```json
{
  "affected_paper_ids": [],
  "fingerprint": "95862c93df6f8a6e19162fa303600c83911fc27c6b86bb7e3c9c63c34e797cf9",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0693

```json
{
  "affected_paper_ids": [],
  "fingerprint": "56a975fec6aa450895145d77be938a1442ea23ce1f9713137485e09b7e856e27",
  "impact": "blocks_completion",
  "paper_id": "gk-1982-regular-arts",
  "question_id": "gk-1982-regular-arts-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-bd78960a20b182413246af6c4d3785f72f5d328c664c7170ad6f176225889f60",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0694

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c4cb6481836fc1c7935c8dd6e16205183aa48f29df10cd826def13056fe1388f",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0695

```json
{
  "affected_paper_ids": [],
  "fingerprint": "db8017ede8016264b7cd79590adfdddac7aef58f42129b232bd53bfb5f2e6fbd",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0696

```json
{
  "affected_paper_ids": [],
  "fingerprint": "febfd7799f4e66766fb93b93efca92580206a30f46986869adbe1bff638562a0",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0697

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0bbb2b46c9d452df62af9cc85d90c64c8559087cc234bc36bd572c500331ff53",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0698

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7be09d71063ea0e76ad23ac705a9842a79cd893bf1f5854361b1faf316b24aab",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0699

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1ae9eb77a7287315bcf9c6bbef482f2ec952b7bd42a12331e8dcdb01a5cfbc35",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0700

```json
{
  "affected_paper_ids": [],
  "fingerprint": "424acdc7269c8ab5d9d1f6e35e912529d82cb903f4545d445c513989a6a182d4",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0701

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3944acb1d4fc851646eee483e6d648a22fdcb47bf6612c5a6713caf99acb40f4",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0702

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fae01a6a96a1601dfd61931c4537bfce8d3cd329eec7548e213351d5376788fa",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0703

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1903e44c32bf63479a2ef3182e3f1d3fa4c578b919151ec5ba3e98c92b5bac51",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0704

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0641a635246bd5d6bd2ee92f2799fe9a9d5d8a921d290626ddf94227f9fe1006",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0705

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9383e5612a42c92c446a7c62717d84d1094a1e400432efd3b536c32053527c5a",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0706

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a33498d02ecb0c2b6cb9cfa9974d0cf01877f08552e50d6a263938c308256ea6",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-science",
  "question_id": "gk-1983-regular-science-q13",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。 审查发现第13题解析两处数值错误，已按 Python 验算改正。",
  "source_id": "src-c15d4741d61c527497f974ce4f31a92d47b0c86a3095eca91b9bf40067d1c900",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0707

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cb66b4ff276fe6b52722360fd1df3ae4f52caa832fc17e718a64f44aa7b7fc72",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0708

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9a6f1e560ce3581cdc1d915568a9044bfdc8656591399b80a53b52349cbaddaa",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0709

```json
{
  "affected_paper_ids": [],
  "fingerprint": "43d727948b033b3fbfce3077cdc5f17b181169e1c24452496c7fab9238fe98d9",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0710

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9980d75f80b0c5b37fab292da030f76f82748e0f0a355feb489d4efc8e8302d6",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0711

```json
{
  "affected_paper_ids": [],
  "fingerprint": "868dffc2428a85be4d21272c61c44869227ab6b45e6e91fe78e3af7a8de96df1",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0712

```json
{
  "affected_paper_ids": [],
  "fingerprint": "70aa15a3a1e197cb27bfc81e05f77780b8404fe47689d623f68de45d6ff899ef",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0713

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fd06017e63958d5f4f4a0b29ca28b295f440fc678e68af38326816a8dc86c2cc",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0714

```json
{
  "affected_paper_ids": [],
  "fingerprint": "66ab042f11d04c58e82dcfb8e9ece413b78f6cadf28efb4d78ad58b725e6f052",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0715

```json
{
  "affected_paper_ids": [],
  "fingerprint": "136e6560c9c599f8157fe6c6eade573eabafd304fc4e8ba44b30df90cc36e421",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0716

```json
{
  "affected_paper_ids": [],
  "fingerprint": "fdf944ef798b0f0890262c5192981cc6dd1ab38f8251ad181a5f35c1b7f710be",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0717

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cad1741156e07075d146b2d60d7acad45dc542d0aa904ba28abdab3840b6a979",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0718

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a8a488f9dc622d57160cee3b0f0d6cc01d0eeb58085e0926cc7074680c03342d",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0719

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e3820a584ba21f430e0a2665b6450890ac62bdc9732975eb3fa55b4ec1ae99f3",
  "impact": "blocks_completion",
  "paper_id": "gk-1983-regular-arts",
  "question_id": "gk-1983-regular-arts-q13",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-9ecc03064ba3a1dd27920ebd5cb9fa9822dd778caca1466ebc14f93482ee9d9b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0720

```json
{
  "affected_paper_ids": [],
  "fingerprint": "cb16ab317c95fe45b66fc2edb027efa5394abd7a9dcce2e2c8a764a6c23400d0",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0721

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2f325b7a28c276004b5a58a345c42699db58b99ed6e5be552d7ef16e329c274c",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0722

```json
{
  "affected_paper_ids": [],
  "fingerprint": "570239431d23d68adc2374a30071c679fc902437d44dbe11a454d59e9aa23f8d",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0723

```json
{
  "affected_paper_ids": [],
  "fingerprint": "3b7746732a5725264389c9b6f94f840340427b3e438b51f7b21ad74ec14c51ef",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0724

```json
{
  "affected_paper_ids": [],
  "fingerprint": "19d47574c5d23b8b74b31228ba1034fe1f0420886d0c50bc868ca5e8bcd3e3a1",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0725

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0706204dde3cd5281228e93b8bafffb44ca6129bc5a119f0efc6c9028d5a4f7f",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0726

```json
{
  "affected_paper_ids": [],
  "fingerprint": "86643d354be602359792f7d55e4f52861b76e4fdf2bcab2094a3486bd033340f",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0727

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a4b383b46ba9a34aaa9d4d35c608c9969118421b44531a292e8795f668d8cfa7",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0728

```json
{
  "affected_paper_ids": [],
  "fingerprint": "99f546e28fe43d100754a1d9c4fb3d7e44e5bfac76b97c64ec18b3645e725727",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0729

```json
{
  "affected_paper_ids": [],
  "fingerprint": "67946d3c3e3cb3c5431e94dc43c6b1ea60458bd5a910d07968cdaf05b282eb87",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0730

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5fca16a550f2e90dc9c4c17a8cf0dce7c2724e2b5b1671eb5ba72222c0c3de85",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0731

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e4cc7995d6955ea1a0f73cca6d1bcfe4b63892d716540f08f3b8196603f7ef36",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0732

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e619140aa6133ce00b93083f2c88068693068810d06d62295bee8ba3587e07ec",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q13",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0733

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1dde5d73d0d86690cfe1038e911c912556080c25282fefba97bd96cef0e2e37d",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q14",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0734

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7ad4ce4a3f3e2e14ff6facbe0c11fc83e12f44dc6ecacb1bb19f646aaaa37611",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q15",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0735

```json
{
  "affected_paper_ids": [],
  "fingerprint": "849f42c7abbf43ef567172391708f91fa2a3d540033b3f27db1d99c78b9b6d9d",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q16",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0736

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b703087c0a163b9493163a209c9ea38f4054c2119106e2dd1bf6167ffc718722",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q17",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0737

```json
{
  "affected_paper_ids": [],
  "fingerprint": "8e71e1f4f302efb87ba0d1c04559c67ad45c7875572af0076155f0a58cd33c4e",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q18",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0738

```json
{
  "affected_paper_ids": [],
  "fingerprint": "abaea1f4b12e32aae86bf6f0c81ffdcb53913bc98bcafce96d6d5a372db6151d",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q19",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0739

```json
{
  "affected_paper_ids": [],
  "fingerprint": "886bd70d6f1c9912d12d01263d458ea228a034307707eefd52691a7f599535b9",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-science",
  "question_id": "gk-1984-regular-science-q20",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-6b42e1aab74990c2bcb728592ac86d488768aaaec74058a2d08f07d782a2d09e",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0740

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e5ceb942aa79b3dfef2c4f79eb5b167d4d3c6c86081567e47a88d42059409e09",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q01",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0741

```json
{
  "affected_paper_ids": [],
  "fingerprint": "5c4b80cbc126c96335a7cbacde49b5837b76b63f09743baeba7651e684aaa396",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q02",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0742

```json
{
  "affected_paper_ids": [],
  "fingerprint": "795e71efe7c22b9f109d864dfb601b3aaa1cdef1d01a08d87047aad7cdbbf62b",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q03",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0743

```json
{
  "affected_paper_ids": [],
  "fingerprint": "db451406b93c639b0836975f68eef8c1c7cff50960f61df21c60225154155489",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q04",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0744

```json
{
  "affected_paper_ids": [],
  "fingerprint": "aa563c3f5c36c3e911feccf33e1762c26b7e400b1ddbaa3f7dab0495ddbeb767",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q05",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0745

```json
{
  "affected_paper_ids": [],
  "fingerprint": "32c42015e56b56779b8f0f862cf91ba1d57536430ca1c68ed1329e974859f2d4",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q06",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0746

```json
{
  "affected_paper_ids": [],
  "fingerprint": "2c4e2afc762a30f148c1b5db2d870adc927b15c517c6ec0a469c6c9518b787d0",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q07",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0747

```json
{
  "affected_paper_ids": [],
  "fingerprint": "bfe74485fea629771d019892eca745059102373c717fd84944cf2daf963b0bc0",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q08",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0748

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9d68715f10df1a592890cfbc0027379fd730938a7ad21b8861bcc3ac2f651a3f",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q09",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0749

```json
{
  "affected_paper_ids": [],
  "fingerprint": "9ef423ea6ee895a18742b7233f27846fece84d8e9a04ad7d448d1dac8766fbfe",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q10",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0750

```json
{
  "affected_paper_ids": [],
  "fingerprint": "68eb498fb871c354e43280fdbc3ae9c264d6f4c836ca473be8661c8aad189a14",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q11",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0751

```json
{
  "affected_paper_ids": [],
  "fingerprint": "f8728f346bd5518ce1572f0f1d6d099bbbb8f614658f733be9e10f7ed5d74d51",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q12",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0752

```json
{
  "affected_paper_ids": [],
  "fingerprint": "b9d079a38f2568260e658b9c282320fc053de81f0d5cb23a974efbf44f40414b",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q13",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0753

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0f25013c6901849e0f73f74769687efd171829fc73b267efa0b6b4970958d8de",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q14",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0754

```json
{
  "affected_paper_ids": [],
  "fingerprint": "a54878b82ff001f627531e97a3a9d4e3212a65e746528ed257024344cde59505",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q15",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0755

```json
{
  "affected_paper_ids": [],
  "fingerprint": "48ec45de2214d5e81b91142d03be8d2947df175320bc92354f9843ff31c74d37",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q16",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0756

```json
{
  "affected_paper_ids": [],
  "fingerprint": "315a243b5642944dfa2bf9ac76e116bffa2e5d269beff55aece4ee28a1dc5cfc",
  "impact": "blocks_completion",
  "paper_id": "gk-1984-regular-arts",
  "question_id": "gk-1984-regular-arts-q17",
  "resume_action": "已完成：批级视觉审查通过（对照固定源逐页核对+答案独立复算）。",
  "source_id": "src-75d1cff1c8e4861b3f53ce7df14df0b60b2e7650265948a8e792b0836548fa82",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0757

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "84f1637106265449fe87661e22a8aac16024f24de3947ba860189f4c815707ef",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1984-regular-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0758

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "21eb67d1d1e0dc1ee720fd4b0073c5d8a906fe06a16dd12194f157af20f3c507",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1984-regular-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0759

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "216f3158c3cdf805ddf8aac59ed06d61b5ee1231aef2007f77dcd64e31fe27c9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1984-regular-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0760

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "9f97eb29b90fe4b03f42569ff39f11e786d71ecb59582f3d5c7f8513b7d27178",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1984-regular-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0761

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1985 年上海市普通高等学校招生统一考试题目·数学（文史类）》第 2 页第 5 题题干写有“如图”，但该两页扫描中未见可独立辨认的对应图形。题干中的平行线、垂线和交点关系均清晰可见，证明可仅依据文字完成；本文没有凭模型补画源图。",
  "fingerprint": "c8c585fa6a2c7960b8e245512ef9ce078969ecb9a689da9f418f408771db6e89",
  "impact": "non_blocking",
  "paper_id": "gk-1985-regular-shanghai-arts",
  "question_id": "gk-1985-regular-shanghai-arts-q05",
  "resume_action": "取得同版更清晰排印件或独立权威扫描，补核第 5 题“如图”所指图形；在确认前保留题面可见文字，禁止凭空补画源图。",
  "source_id": "src-b568da2ee95d48c563e206a1f333102de6d206287202709d56be9678e91687e5",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0762

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1985 年上海市普通高等学校招生统一考试题目·数学（文史类）》第 2 页第 8 题题干写有“如图”，但该两页扫描中未见可独立辨认的对应图形。抛物线、垂线、垂足和定比分点等文字及公式条件均清晰可见，本文仅据这些可见条件推导，不补写不可核验的图形信息。",
  "fingerprint": "54d6b149230de708f231202be2abbfc086fb08ee093b65fac3b193c98ff85e17",
  "impact": "non_blocking",
  "paper_id": "gk-1985-regular-shanghai-arts",
  "question_id": "gk-1985-regular-shanghai-arts-q08",
  "resume_action": "取得同版更清晰排印件或独立权威扫描，补核第 8 题“如图”所指图形；在确认前保留题面可见文字，禁止凭空补画源图。",
  "source_id": "src-b568da2ee95d48c563e206a1f333102de6d206287202709d56be9678e91687e5",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0763

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF《1985 年上海市普通高等学校招生统一考试题目·数学（理工农医类）》第 1 页第 2 题第（5）小题高清复核仍确认扫描字面为“原坐标系中的曲线 x=x^3”；但 A—D 四个选项均为 y=x^3 平移到新坐标系后的形式。两个公开答案资料均把本卷第 2 题第五小题列为（D），因此规范源按交叉核定结果采用 y=x^3，并保留固定扫描异文。",
  "external_evidence": "直接核查了《DA1985年上海市数学(理工类)》百度文库页（https://wenku.baidu.com/view/5965463832b765ce0508763231126edb6f1a76e4.html）：公开页面的内嵌答案文字明确列出二、1—5小题答案 C、C、D、B、D；另核查公开整理页《1985年全国统一高考数学试卷及解答（上海理工类），满分120分》（https://baijiahao.baidu.com/s?id=1816949649413178087&wfr=spider&for=pc），该页同样列出上海理工类选择题答案 C、C、D、B、D。两者均为二手公开资料而非考试院原件，但与四个选项的平移换元一致：按 x=x^3 字面无法得到任何选项，按 y=x^3 得 y'-1=(x'+2)^3，即（D）。",
  "fingerprint": "949a9ab74011e0744bcf96f88c07f326908dda53f4162f16352b7d4edb5501c5",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-shanghai-science",
  "question_id": "gk-1985-regular-shanghai-science-q02",
  "resolution": "固定扫描保留 x=x^3 异文；两个公开答案资料均给出第五小题为（D），且平移换元只与 y=x^3 相容，规范源已将题面核定为 y=x^3，并保留上游差异记录。",
  "resume_action": "已完成交叉核定；规范题面采用 y=x^3，答案为（D），并完成答案、解析、生成、构建与视觉复核。",
  "source_id": "src-49bdf04407d48da1a3265cea8e079a2bbf0b72f553b9d529fb30b326f95aff71",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0764

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描第 2(5) 小题字面为 x=x^3，与全部选项不一致；两个公开答案资料均把本卷第五小题列为（D），且只有将曲线核定为 y=x^3 才能由平移换元得到该选项。",
  "external_evidence": "直接核查了《DA1985年上海市数学(理工类)》百度文库页（https://wenku.baidu.com/view/5965463832b765ce0508763231126edb6f1a76e4.html）：公开页面的内嵌答案文字明确列出二、1—5小题答案 C、C、D、B、D；另核查公开整理页《1985年全国统一高考数学试卷及解答（上海理工类），满分120分》（https://baijiahao.baidu.com/s?id=1816949649413178087&wfr=spider&for=pc），该页同样列出上海理工类选择题答案 C、C、D、B、D。两者均为二手公开资料而非考试院原件，但与四个选项的平移换元一致。",
  "fingerprint": "5781a035d53d1179ac6b5ce69afcf75d4f05d09bc44c9994c726cde1ce807ed4",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-shanghai-science",
  "question_id": "gk-1985-regular-shanghai-science-q02",
  "resolution": "按两个公开答案资料及平移换元交叉核定，规范题面采用 y=x^3，可靠答案为（D）；答案要点与解析已同步更新。",
  "resume_action": "已按核定题面确定（D），并完成答案要点、解析、生成、构建与三角色核验记录。",
  "source_id": "src-49bdf04407d48da1a3265cea8e079a2bbf0b72f553b9d529fb30b326f95aff71",
  "status": "resolved",
  "type": "answer-missing"
}
```
## ISSUE-0765

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描第 2(5) 小题的字面 x=x^3 与 A—D 选项不相容；两个公开答案资料均给出该卷第五小题为（D），而 y=x^3 的平移换元恰好得到 D。固定扫描异文与规范修订依据已留档。",
  "external_evidence": "直接核查了《DA1985年上海市数学(理工类)》百度文库页（https://wenku.baidu.com/view/5965463832b765ce0508763231126edb6f1a76e4.html）：公开页面的内嵌答案文字明确列出二、1—5小题答案 C、C、D、B、D；另核查公开整理页《1985年全国统一高考数学试卷及解答（上海理工类），满分120分》（https://baijiahao.baidu.com/s?id=1816949649413178087&wfr=spider&for=pc），该页同样列出上海理工类选择题答案 C、C、D、B、D。两者均为二手公开资料而非考试院原件；按 y=x^3 换元才与 D 相容，故不再把题面级冲突留给盲核。",
  "fingerprint": "217fd3c78bf6144906814dbcc1bc238cbdb137e4a80c1c116a0b708e9a219f8c",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-shanghai-science",
  "question_id": "gk-1985-regular-shanghai-science-q02",
  "resolution": "固定扫描异文与两个公开答案资料的（D）记录完成交叉核定；规范题面采用 y=x^3，盲核按 y'-1=(x'+2)^3 复算并确认（D）。",
  "resume_action": "已完成独立资料交叉核验、答案复算和盲核。",
  "source_id": "src-49bdf04407d48da1a3265cea8e079a2bbf0b72f553b9d529fb30b326f95aff71",
  "status": "resolved",
  "type": "answer-conflict"
}
```
## ISSUE-0766

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 20 题印为“集合 A 和集合 B 各含有 12 个元素，A∪B 含有 4 个元素”；已通过浏览器下载并渲染公开上游同版 `deekur/gaokaomath` 的 `普通高考/1986/1986全国理.pdf` 复核：文件 SHA-256 为 `f63a3e838fb7c3fb39228ba4fdf76451965d1518421bd693ba279fe34e48957f`、488796 字节、1 页，与 manifest artifact 完全一致，原页第 20 题的运算符确为 `A∪B`。但两个独立公开资料均将同一题记为 `A∩B` 并给出 1084：精英家教网题目页（https://www.1010jiajiao.com/gzsx/shiti_id_e722ee7da6d5ded181a6fc5912129fe7）在题源处标为“1986年全国统一高考数学试卷（理科）”，页面答案为 1084；《高中数学第一章-集合》公开 PDF（https://dfiles.jiajiaoban.com/ohr/2020/07/07/155223_5f0429b76d23f.pdf）第 100 页含完整题面和 1084 的分类解，SHA-256 为 `1d5119f0477c2efcc2f958eb0d4912a862cb6c294b8bf9b9d41831f273388396`、9318964 字节、169 页；另一份公开教材 PDF（https://cdn.zizzs.com/1723774967581%E9%AB%98%E8%80%83%E6%95%B0%E5%AD%A6%E7%9F%A5%E8%AF%86%E7%82%B9%E6%B1%87%E7%BC%96%E5%8F%8A%E9%AB%98%E4%B8%AD%E6%95%B0%E5%AD%A6%E8%A7%A3%E9%A2%98%E5%9F%BA%E6%9C%AC%E6%96%B9%E6%B3%95.pdf）第 123 页同样给出 `A∩B` 与 1084，SHA-256 为 `f48fa15f04a40317123718d377270e751d9bbbe6db376f18c235b32597a89edf`、4340252 字节、163 页。",
  "fingerprint": "cd2505d9d0a18bf8ba361cba2433e61bcdc96e4d234f141ea5846b19bf5feae3",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-national-science",
  "question_id": "gk-1986-regular-national-science-q20",
  "resolution": "固定上游扫描的 `A∪B` 与两个独立公开题源/解析资料的 `A∩B`、答案 1084 相冲突；考虑题面可解性、两份独立资料的一致性及精确题源索引，规范转录采用 `A∩B`，并在本条证据中保留固定源的原始差异，不修改或提交上游 PDF。",
  "resume_action": "已完成交叉核定；规范转录采用 A∩B，保留固定源 A∪B 差异记录，并重跑题面、答案、解析、provenance、构建和视觉复核。",
  "source_id": "src-dcbe01c963fb151595722561942650d49d97c55287ec155c8566716b0e13327b",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0767

```json
{
  "affected_paper_ids": [],
  "current_evidence": "规范题面已依据 ISSUE-0766 登记的两份独立公开资料核定为 |A|=|B|=12、|A∩B|=4；两份资料均给出集合 C 的个数为 1084，且该值可由 C(20,3)-C(8,3) 独立复算。固定源的 A∪B 差异与核定结果并列保留在 ISSUE-0766。",
  "fingerprint": "4dc1f1c6408f05cd610714b39e1f7342cf52ef66ee97b2f5b03487eb37586051",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-national-science",
  "question_id": "gk-1986-regular-national-science-q20",
  "resolution": "按 ISSUE-0766 的交叉核定结果更新规范题面、答案要点和解析正文为 1084，并以容斥计数复算：|A∪B|=20，C(20,3)-C(8,3)=1084。",
  "resume_action": "已按确认的交集题面确定集合 C 的数量 1084，并完成答案、解析和三角色核验记录。",
  "source_id": "src-dcbe01c963fb151595722561942650d49d97c55287ec155c8566716b0e13327b",
  "status": "resolved",
  "type": "answer-missing"
}
```
## ISSUE-0768

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源的 A∪B 基数前提与 |A|=|B|=12 不相容；独立公开题源与解析资料一致采用 A∩B 并给出 1084，且该答案经容斥公式独立复算。该冲突的来源差异、URL、页码和文件 SHA-256 已在 ISSUE-0766 留档。",
  "fingerprint": "8dd531e4828dbec5587ca478e868dc5fbc16e371f3f665e5a03b16c3f260c1f1",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-national-science",
  "question_id": "gk-1986-regular-national-science-q20",
  "resolution": "盲核按交叉核定后的规范题面复算并确认 1084；解析版与简答版结论一致，固定源的运算符差异不再阻断本卷完成。",
  "resume_action": "已完成独立题源交叉核验、答案复算和盲核。",
  "source_id": "src-dcbe01c963fb151595722561942650d49d97c55287ec155c8566716b0e13327b",
  "status": "resolved",
  "type": "answer-conflict"
}
```
## ISSUE-0769

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源把复数√3−i的幅角主值列为正角 11π/6，但没有明示主值区间；按现代 (-π,π] 约定应写成 −π/6，按固定源选项和答案表只能沿用 [0,2π) 约定。",
  "fingerprint": "c13f2935683c17ca2e9cb4c89a4b0f7fcd3a607f4b1c9259aff3f0cd93f72a57",
  "impact": "non_blocking",
  "paper_id": "gk-1986-regular-shanghai-arts",
  "question_id": "gk-1986-regular-shanghai-arts-q01-(9)",
  "resume_action": "取得同版更清晰排印或教材定义，确认该卷幅角主值区间；确认前保留源选项、答案表和约定说明。",
  "source_id": "src-d2fb778ac710a05ac590cdbb3594ceac90133b3d15047ae12b1dbb725f991d10",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0770

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 3 页（原卷第 36 页）题面与第 4 页（原卷第 37 页）解答均为抛物线 y^2=px 与圆 (x-2)^2+y^2=3 相交问题；本库第 7 题已按固定源更正。旧登记的折叠题及 AB=√7 语义不属于本卷第 7 题，原歧义据此关闭。",
  "fingerprint": "ed9ad51f816ff0bad0c56146d5e30333d14c1d790936fa9065da8c6cfc129a5a",
  "impact": "non_blocking",
  "paper_id": "gk-1986-regular-shanghai-arts",
  "question_id": "gk-1986-regular-shanghai-arts-q07",
  "resume_action": "已按固定源第 3—4 页恢复本题；若发现新的同版来源异文，另立可核验问题。",
  "source_id": "src-d2fb778ac710a05ac590cdbb3594ceac90133b3d15047ae12b1dbb725f991d10",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0771

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源把复数√3−i的幅角主值列为正角 11π/6，但没有明示主值区间；按现代 (-π,π] 约定应写成 −π/6，按固定源选项和答案表只能沿用 [0,2π) 约定。",
  "fingerprint": "a3a18aa998e46a486fff48ee651962425ba069930197f8693b78c16db1b3c162",
  "impact": "non_blocking",
  "paper_id": "gk-1986-regular-shanghai-science",
  "question_id": "gk-1986-regular-shanghai-science-q01-(9)",
  "resume_action": "取得同版更清晰排印或教材定义，确认该卷幅角主值区间；确认前保留源选项、答案表和约定说明。",
  "source_id": "src-194e8e0291756d4efe602fdad56cd93f41da514be669a940d5510dedcc6bc2f4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0772

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源未单列 k∈R，且解答把纯虚数按非零纯虚数处理；若允许 0 或把 k 取复数，参数条件会改变。",
  "fingerprint": "3c0146071627733ee84015616921ff7f0e8143f90988b1b4f53b6e9a2f54cf32",
  "impact": "non_blocking",
  "paper_id": "gk-1986-regular-shanghai-science",
  "question_id": "gk-1986-regular-shanghai-science-q05",
  "resume_action": "取得同版教材或清晰题面，确认 k 的取值域以及纯虚数是否排除 0；确认前保留固定源解答口径。",
  "source_id": "src-194e8e0291756d4efe602fdad56cd93f41da514be669a940d5510dedcc6bc2f4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0773

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源在折叠前给出 AC=2、BC=3，折叠后条件写 AB=√7；本库按源解答将其解释为折叠后的空间距离。",
  "fingerprint": "5ca779cf476e084df61bd7d02a874639e1de5ff92656bd73ac3acbda35b800cf",
  "impact": "non_blocking",
  "paper_id": "gk-1986-regular-shanghai-science",
  "question_id": "gk-1986-regular-shanghai-science-q07",
  "resume_action": "取得同版更清晰题面，确认 AB=√7 的语义；确认前保留该解释依赖说明。",
  "source_id": "src-194e8e0291756d4efe602fdad56cd93f41da514be669a940d5510dedcc6bc2f4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0774

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "external_evidence": "先前记录的外部题库页面与本次固定源复核结果相符，但不用于确认本卷身份或替代固定源证据。",
  "fingerprint": "e72707f8c2ff9a9066fdea6dfc6178c36dc43724c4930231d51af848a1f4edb1",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q02-(9)",
  "resolved_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "resume_action": "已按固定源更正第2(9)题转录、答案与解析，并复核答案180；不再需要外部勘误或继续阻断。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0775

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "external_evidence": "先前记录的外部题库页面与本次固定源复核结果相符，但不用于确认本卷身份或替代固定源证据。",
  "fingerprint": "00ba3aac44086883e6d7d849b0f114fc2fe393d8605c7b4bf997df435b00d988",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q02-(9)",
  "resolved_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "resume_action": "已按固定源更正第2(9)题转录、答案与解析，并复核答案180；不再需要外部勘误或继续阻断。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "answer-missing"
}
```
## ISSUE-0776

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "external_evidence": "先前记录的外部题库页面与本次固定源复核结果相符，但不用于确认本卷身份或替代固定源证据。",
  "fingerprint": "1028f700367d9148ae99bb21ecc275b18af0eaa6a30138034ee24f3e3a2c8b24",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q02-(9)",
  "resolved_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "resume_action": "已按固定源更正第2(9)题转录、答案与解析，并复核答案180；不再需要外部勘误或继续阻断。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "answer-conflict"
}
```
## ISSUE-0777

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立核源（2026-11-09，.work/verify/1986-guangdong-arts-q1-25.md）：1986 广东文史类第 1(25) 题为纯文字命题题，固定源全卷无图形；原「图形选项缺失」实为理工类卷内容错位继承。已按源文改写第 24、25 题与解析，答案 24=A、25=C，与固定源答案表（书页 269）一致。",
  "external_evidence": "百度题库公开页（https://easylearn.baidu.com/edu-page/tiangong/questiondetail?id=1714381465704937476&fr=search）展示了完全相同的函数及定义域，并由解析得到反函数图形为 (x−1)^2+y^2=1 在 0≤x≤1、−1≤y≤0 的弧段；该页为四选项练习题，答案标为 C，未标识为 1986 年广东卷，不能映射固定源五选项中的 E，也不能补回 A—E 原图。",
  "fingerprint": "037ee492d77a54546001612bafa94aa7f7765fd3ede8c09cc772453c69986422",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q01-(25)",
  "resume_action": "已按固定源订正；理工类第 25 题图形区空白另案保留。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0778

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 1(25) 题的 A—E 图形选项区域整段空白；题干和答案表 E 可见，但无法核对 E 对应的具体图形。独立推导的反函数图形为 (x−1)^2+y^2=1 的左下四分之一弧。",
  "external_evidence": "百度题库公开页（https://easylearn.baidu.com/edu-page/tiangong/questiondetail?id=1714381465704937476&fr=search）展示了完全相同的函数及定义域，并由解析得到反函数图形为 (x−1)^2+y^2=1 在 0≤x≤1、−1≤y≤0 的弧段；该页为四选项练习题，答案标为 C，未标识为 1986 年广东卷，不能映射固定源五选项中的 E，也不能补回 A—E 原图。",
  "fingerprint": "afa2a86288e765aee2005d66d6436127ad3de5712ca174683e9ab3e4d054d0fc",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q01-(25)",
  "resume_action": "取得含有第 1(25) 题 A—E 图形的同版清晰源；确认前保留题干和答案表，禁止补画为源图。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0779

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立核源（2026-11-09，.work/verify/1987-national-science.md）：600dpi 放大判读下标为 n→∞、底数与指数均为 x，文本层同；源卷自身指标与变量不一致，按字面该式不是确定的数。题库三处照录 x 并标注疑点，未擅自改写为 n，处置正确。",
  "external_evidence": "另直接核查公开整理页《1987年全国统一高考数学试卷及解答（理工农医类），满分120》（https://www.toutiao.com/article/7415485199338766883/）：其附加题图片仍显示题面为 lim(n→∞)(1−1/(2x))^x，但紧接的解答图片将求解步骤写成 lim(x→∞)(1−1/(2x))^x=e^(−1/2)，即把 x 视为极限变量。该页为二手整理而非官方原件，能支持“通常意图为 x→∞”，但单独不足以替代官方勘误，因此本条仍保持 open。",
  "fingerprint": "3076fd80ee19a575e9903091e424a6c13720b649e3d08c08eb17e1c25892ecc4",
  "impact": "blocks_completion",
  "paper_id": "gk-1987-regular-national-science",
  "question_id": "gk-1987-regular-national-science-q22",
  "resume_action": "保持按字面转录与疑点标注；若取得官方勘误页再更新题面与答案。",
  "source_id": "src-1027abd4ab36c6d3535d5370b4fa98af66ccd38c7dbd2cc91c43a06b1154cff0",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0780

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第三大题的解答页只写有“解答见印刷页 286”，而当前 PDF 截止印刷页 280；本库已提供独立几何推导，但缺少固定源原解答页。",
  "fingerprint": "8f2bb70097b7209cfe40b0e4c84461ff1fb5e4b161c3006cc05927be2e43a8a1",
  "impact": "non_blocking",
  "paper_id": "gk-1987-regular-guangdong-arts",
  "question_id": "gk-1987-regular-guangdong-arts-q04",
  "resume_action": "取得包含印刷页 286 的同版广东文科解答源，将固定源答案与本库独立推导逐项比对；在此之前保留独立结果并标注来源缺页。",
  "source_id": "src-11b2f166621b2cea6a14d5390e97f3428d3511ca4dc67f7d3dab516a4abc7b0f",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-0781

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 1(2) 题的文本层使用私有字形显示乘号，视觉上读作 2×4^x−5×2^x+2=0；当前转录用标准 LaTeX 乘法点表示，需更清晰源确认字形。",
  "fingerprint": "05f38f56f9a0bd484b16fa045167c77afc21a91520f5549fae15fbab3f63e8a6",
  "impact": "non_blocking",
  "paper_id": "gk-1987-regular-guangdong-science",
  "question_id": "gk-1987-regular-guangdong-science-q01-(2)",
  "resume_action": "取得同版更清晰排印或矢量源，确认第 1(2) 题两个私有字形均为乘号；确认前保留视觉读取和标准 LaTeX 乘法点。",
  "source_id": "src-c52f9f57d337fda6a30bd1d35897dfb8c0b5a6d96726d513af1bf889cef355fa",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0782

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 1(17) 题可见 C 条件为 l⊥α、m∥β、l∥m，但固定源答案表记为 C；取水平面与相交的竖直平面即可构成反例，题面条件不能推出 α∥β。",
  "fingerprint": "947de71e0535790f03227b976e520f50f3140abe87613c3af8fc2072921088f3",
  "impact": "blocks_completion",
  "paper_id": "gk-1987-regular-guangdong-science",
  "question_id": "gk-1987-regular-guangdong-science-q01-(17)",
  "resume_action": "取得同版更清晰题面或权威勘误，确认第 1(17) 题 C 选项是否漏印“m⊥β”或其他条件；确认前保留固定源文字与答案表冲突，禁止擅改题面。",
  "source_id": "src-c52f9f57d337fda6a30bd1d35897dfb8c0b5a6d96726d513af1bf889cef355fa",
  "status": "open",
  "type": "answer-conflict"
}
```
## ISSUE-0783

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 1(21) 题选项 D 只写“有两个侧面都垂直于底面”，未显式限定相邻侧面；不同教材对该省略条件的解释可能不同，当前按固定答案 D 记录。",
  "fingerprint": "ac2f1f1c9cc62b8c5473b23d711cef2f2d21164d06765a1db6453e07420d874f",
  "impact": "non_blocking",
  "paper_id": "gk-1987-regular-guangdong-science",
  "question_id": "gk-1987-regular-guangdong-science-q01-(21)",
  "resume_action": "取得同版教材或更清晰排印，确认“两个侧面”是否有相邻限定；确认前保留源句并标注解答口径。",
  "source_id": "src-c52f9f57d337fda6a30bd1d35897dfb8c0b5a6d96726d513af1bf889cef355fa",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0784

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 1(22) 题题干可读，但其后的 A—D 轨迹图形选项整段缺失；答案表记为 C，无法据当前源把独立推导的两条射线对应到字母。",
  "fingerprint": "ef9b960b0dfb6926f8797d0426a4653c9fbee6dfcf37c953ac30cfef17f35908",
  "impact": "blocks_completion",
  "paper_id": "gk-1987-regular-guangdong-science",
  "question_id": "gk-1987-regular-guangdong-science-q01-(22)",
  "resume_action": "取得含有第 1(22) 题 A—D 图形选项的同版清晰源；确认前保留题干、独立轨迹和答案表，禁止补画为源选项。",
  "source_id": "src-c52f9f57d337fda6a30bd1d35897dfb8c0b5a6d96726d513af1bf889cef355fa",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0785

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1—4 页题面明确写“已知 y=f(x) 的图象如右图”，但逐页视觉检查和 PDF 资源列表均未发现该图；第 23 小题四个文字选项可辨，图形本身缺失。",
  "fingerprint": "d49bf04f0350744567b6eda768689168e28a367fff204d44e87d897e408e27aa",
  "impact": "blocks_completion",
  "paper_id": "gk-1988-regular-guangdong-science",
  "question_id": "gk-1988-regular-guangdong-science-q01",
  "resume_action": "取得包含第 23 小题右图的更完整固定源或独立可核验扫描页；在补齐前保留题面文字和固定源答案 A，不凭空补图。",
  "source_id": "src-9047cf57fbda6f984bbcfc55e4fe8db14b99ddbb1d756b65d3dcc9ea0d01926a",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0786

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "1800a0e74166b7e0bb24fe80826b0361fcc1742c53dea3ad28f79ab679bdc21e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1988-regular-guangdong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0787

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "428d3d0bb1107a6c2621be105f22f678b50a7037565f61ee498fa56dc6c540bf",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1988-regular-guangdong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0788

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "5166830f39912a0d514346f716a373be244579480a154c342611eed0f3e6d5d5",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1988-regular-guangdong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0789

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "649219f70165d849a9b7e87d0fe23874aef0ba93efdc830620c5b85247f1f7a0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1988-regular-guangdong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0790

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 2 页第 6 小题可见“若 sin α=5/13，α 为第二象限角，则 tg(α/2) 的值为”题干，但当前扫描在题干后未见 A、B、C、D 四个选项；第 3 页答案表仍记录该小题代号 B。已通过浏览器下载并渲染公开上游同版 `deekur/gaokaomath` 的 `普通高考/1988/1988上海.pdf` 复核：文件 SHA-256 为 `eba069161024fb508a36ecb51e8707afb1114c8e873548a9aff5c187635aa51a`、162789 字节、6 页，与 manifest artifact 完全一致；第 2 页视觉上同样缺少 A—D 选项。中国知网目录确认同题发表于《中学数学教学》1988 年第 5 期（https://mall.cnki.net/magazine/Article/ZSJX198805016.htm）；百度文库公开的同题名 5 页扫描（https://wenku.baidu.com/view/aa1a1695daef5ef7ba0d3cea.html）第 2 页直接显示 A=1/5、B=5、C=-5、D=-1/5，且 B 与题干独立复算值 5 对应。因此已用独立同题扫描补足缺失选项，缺失不是本库漏页或导入损坏。",
  "fingerprint": "8f9048419fee231e5f125695780b613826952b36341451ecc8e5e74d84fae8de",
  "impact": "blocks_completion",
  "paper_id": "gk-1988-regular-shanghai",
  "question_id": "gk-1988-regular-shanghai-q02",
  "resolution": "已取得独立同题公开扫描并视觉核对四个选项；已补入规范题面、答案和解析，并将 B 与独立计算值 5 对齐。",
  "resume_action": "已补足选项并完成题面、答案、生成、编译与视觉复核，无需继续动作。",
  "source_id": "src-4a65e135bdb52f81bc99a0783fd42dc77e118ca220546d84412fdcae8197c424",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0791

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 1 题第（17）小题可见条件与固定答案表 C 不相容，第（22）小题题干可读但 A—D 轨迹图形选项整段缺失；细项分别由既有 ISSUE-0782、ISSUE-0784 跟踪，本条作为题面级阻塞汇总。",
  "fingerprint": "2fadfb7ccb2e84edd8b639b053728857f46cbe3b9b388cd65f9a2c8ae4f5a48a",
  "impact": "blocks_completion",
  "paper_id": "gk-1987-regular-guangdong-science",
  "question_id": "gk-1987-regular-guangdong-science-q01",
  "resume_action": "取得第 1 题第（17）、（22）小题的完整题面/答案对应源，解决答案冲突并补齐缺失图形选项后，重跑逐题核查、生成、编译和复核。",
  "source_id": "src-c52f9f57d337fda6a30bd1d35897dfb8c0b5a6d96726d513af1bf889cef355fa",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0792

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 1 题第（17）小题的固定答案表记为 C，但按当前可见题面条件不能推出该结论；细项由 ISSUE-0782 跟踪，本条作为题面级答案冲突汇总。",
  "fingerprint": "1c2d1bc91d6b7d2f4792e1cc2eb0b6fffe65afda63db157178b22c86968145d9",
  "impact": "blocks_completion",
  "paper_id": "gk-1987-regular-guangdong-science",
  "question_id": "gk-1987-regular-guangdong-science-q01",
  "resume_action": "取得第 1 题第（17）小题的完整题面/权威勘误，解决可见条件与固定答案表的冲突后，重跑答案核查、生成、编译和复核。",
  "source_id": "src-c52f9f57d337fda6a30bd1d35897dfb8c0b5a6d96726d513af1bf889cef355fa",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0793

```json
{
  "affected_paper_ids": [],
  "current_evidence": "同上：文史类第 25 题为空间命题判断（文字选项），答案 C；库内先前的反函数图象题与答案 E 属理工类内容，已替换为固定源原文。",
  "external_evidence": "百度题库公开页（https://easylearn.baidu.com/edu-page/tiangong/questiondetail?id=1714381465704937476&fr=search）展示了完全相同的函数及定义域，并由解析得到反函数图形为 (x−1)^2+y^2=1 在 0≤x≤1、−1≤y≤0 的弧段；该页为四选项练习题，答案标为 C，未标识为 1986 年广东卷，不能映射固定源五选项中的 E，也不能补回 A—E 原图。",
  "fingerprint": "499eb3d8a813d12ff1d9285777fb442ee800e62dc5fb0b04baee39c9881eef55",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q01",
  "resume_action": "已按固定源订正。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0794

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "external_evidence": "先前记录的外部题库页面与本次固定源复核结果相符，但不用于确认本卷身份或替代固定源证据。",
  "fingerprint": "f37fc85f7b4489265ed34284aaecc711eb0c476bb50542077772c96f21639598",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q02",
  "resolved_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "resume_action": "已按固定源更正第2(9)题转录、答案与解析，并复核答案180；不再需要外部勘误或继续阻断。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0795

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "external_evidence": "先前记录的外部题库页面与本次固定源复核结果相符，但不用于确认本卷身份或替代固定源证据。",
  "fingerprint": "19c213f540ab41126f054a59c822558aa489334dcb1464cc4b06e62519ab933d",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q02",
  "resolved_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "resume_action": "已按固定源更正第2(9)题转录、答案与解析，并复核答案180；不再需要外部勘误或继续阻断。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "answer-missing"
}
```
## ISSUE-0796

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "external_evidence": "先前记录的外部题库页面与本次固定源复核结果相符，但不用于确认本卷身份或替代固定源证据。",
  "fingerprint": "4b9aae5b64c90c7fc998570cc483e6748069c1e828e75ff21e7d74ddf78f75ce",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-arts",
  "question_id": "gk-1986-regular-guangdong-arts-q02",
  "resolved_evidence": "固定源 PDF 第 8 页（书页267）350dpi复核第2大题第（9）题为 a3a7=-12、a4+a6=-4、公差为正；固定源 PDF 第11页（书页270）答案表第（9）项列180。独立盲算同得：a5=-2，d=2，a1=-10，a20=28，S20=180。旧的 a6+a9=-1、负判别式与冲突记录源于转录误读；规范试题、答案要点与解析已纠正。此前外部题库页面不作为本次结案依据。",
  "resume_action": "已按固定源更正第2(9)题转录、答案与解析，并复核答案180；不再需要外部勘误或继续阻断。",
  "source_id": "src-e473c445909eeafaf4432caa72be993d8ea68e9c79b5e236da41eb6ca67e3350",
  "status": "resolved",
  "type": "answer-conflict"
}
```
## ISSUE-0797

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e58aaae6a5734e320bbb8414e686209805fe7be840e42b5511c41d40622b320e",
  "external_evidence": "百度题库公开页（https://easylearn.baidu.com/edu-page/tiangong/questiondetail?id=1714381465704937476&fr=search）展示了完全相同的函数及定义域，并由解析得到反函数图形为 (x−1)^2+y^2=1 在 0≤x≤1、−1≤y≤0 的弧段；该页为四选项练习题，答案标为 C，未标识为 1986 年广东卷，不能映射固定源五选项中的 E，也不能补回 A—E 原图。",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q01",
  "resume_action": "取得含有第 1(25) 题 A—E 图形的同版清晰源；确认前保留题干和答案表，禁止补画为源图。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0798

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定上游 PDF《1977福建文.pdf》（deekur/gaokaomath 固定版本，SHA-256 ee125e8b70f6a6d90818fc256aa1884fc19a0137313fc7716ceb8c20773d3cd0，A3 单页）第 2 大题第（1）题高清渲染明确印作 y=lg(2−x)/√(x−1)；PDF 文本层同样提取为 x−1。独立公开页面《1977年福建高考数学真题》（https://mdnice.com/writing/e2ab33f129de4a8ba4f9b96750417574）也将同题写作 √(x−1)，与固定源相互印证。原库转录误写为 √x−1。",
  "fingerprint": "2d1f1782ab6936b2c3f9dec9e9cbc927ad40f77300fedd05a0923bd25aa550f7",
  "impact": "non_blocking",
  "paper_id": "gk-1977-regular-fujian-arts",
  "question_id": "gk-1977-regular-fujian-arts-q02",
  "resolution": "已将题面与解析统一修正为 √(x−1)，并将定义域由 [0,1)∪(1,2) 修正为 (1,2)；共享 questions.tex/answers.tex 与 answers_short.tex 已重生成。",
  "resume_action": "已修正并重跑生成检查，无需继续动作。",
  "source_id": "src-695012a4c4b226accca28c241571eab14a51c31f47f7ddec60950425b6c6e926",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0799

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定上游 PDF《1977福建理.pdf》（deekur/gaokaomath 固定版本，SHA-256 41cfadf1b11caf1028eca522072a83b4adce7c398491c247cd455b17ec1b3e47，A3 单页）第 1 题第（3）小题高清渲染明确印作 y=lg(2−x)/√(x−1)；PDF 文本层同样提取为 x−1。独立公开页面《1977年福建高考数学真题》（https://mdnice.com/writing/e2ab33f129de4a8ba4f9b96750417574）也将同题写作 √(x−1)，与固定源相互印证。原库转录误写为 √x−1。",
  "fingerprint": "8bc637e2d03428956279f663d694e3bfb4ce8c80d911478b37ccbc02c6e33c1e",
  "impact": "non_blocking",
  "paper_id": "gk-1977-regular-fujian-science",
  "question_id": "gk-1977-regular-fujian-science-q01",
  "resolution": "已将题面与解析统一修正为 √(x−1)，并将定义域由 [0,1)∪(1,2) 修正为 (1,2)；共享 questions.tex/answers.tex 与 answers_short.tex 已重生成。",
  "resume_action": "已修正并重跑生成检查，无需继续动作。",
  "source_id": "src-169ec552629b39cd748da5afa1bce33d6aae2be96064ce7c9e5505c51312d359",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0800

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "8264e7d5e14766d3e1d9d928ced24968442ff7bad62fce6905110012a791e41b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0801

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "4d75d84d1d300a26fc27097846605bd53ab0c31578da0f35726d2a3c5de86c3b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0802

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "0ee73d1c7b095db568bd00670497e100da7e07417ca09bc44b1d2ae89d41684e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0803

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "f83a2f3b3e2dfdd4267a02b71c084df078d84fdc04245209d6b95fdb5319eb6c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0804

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "11b1afcc9338c8d407a6764e1b0dead79f5613d41a6ffbda1e43f12b94cd58e3",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2001-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0805

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "8db307a921d661beee7053f131e9f61fd115ff1cc3cfca9449bb87fc48d883ca",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2001-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0806

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "824344c1d251afd57974084553b8e6585061619c4a7ac469bc007c757f471905",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2001-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0807

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "0bac8d114b20efadde26a8835cf36fec9e594bdd491c75eaf6cbb982a0b94dd2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2001-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0808

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "1e4f0fe83b46a686095508f97397180fe4f4a0769db11fb21e4d08fa959f3a3d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-spring-jingmengwan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0809

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "661d949574cab6fd1a764648ba58511274cddc74588ccfca1310465bcfecb1ac",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-spring-jingmengwan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0810

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "34c46a51656c29a41a19638664b37790d9c1ec3b2c85145afaeb0dd2cd377e42",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-spring-jingmengwan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0811

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "623835e98c8a364586c387f58262c4d3d4b076f7bf643e772d9d977f72b27092",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-spring-jingmengwan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0812

```json
{
  "affected_paper_ids": [],
  "current_evidence": "由切线截距 x_2=2x_1/3+a/(3x_1^2) 及 x_2-x_1=(a-x_1^3)/(3x_1^2) 独立复算，确认题面缺少 x_1>√[3]{a} 条件。",
  "fingerprint": "c49c5a19826ba132b821559889b47c19d83315332a16fdaa5ea46c12c5ba2261",
  "impact": "blocks_completion",
  "paper_id": "gk-2002-regular-national-new-arts",
  "question_id": "gk-2002-regular-national-new-arts-q21",
  "resolution": "固定源第②问写为“若 x_2>√[3]{a}，则 √[3]{a}<x_2<x_1”，但 a=1、x_1=1/2 时 x_2=3/2，直接构成反例。规范解析保留原题，给出反例，并明确说明补充 x_1>√[3]{a} 后结论才成立；未擅自改写题面。",
  "resume_action": "固定源已按字面保留；若取得正式勘误资料，核对第 21 题第②问是否应补充 x_1>√[3]{a}，再更新规范记录。",
  "source_id": "src-2cfc2db9c0f09cde88a57c79780a0b5946a263027611e86cc07ee0763b66d4c8",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-0813

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "346e142b5a9c5317a7e647f4fba4d93f6dbfddc4ec71602d98c970c796949c44",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0814

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "e384c0ec7f878e40cc1aff8b11a3df7df75d3b91c09137201a626ea133eeb063",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0815

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "2ecf2904737cd8a83a6bcb6c13336a8b5f2979d0c28e63c660e5c80f8c431d1d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0816

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "4bdc07e101da5f28d8fbe21aa63fc205c0fb91c4977abaefa1df6db00c16498b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0817

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 1 题印刷为 sqrt(4x-x^2)<x，选项 C 印为 (2,4)；定义域和平方运算给出的严格解集为 (2,4]。",
  "fingerprint": "388a26d1a08208db51d41944d05df2781134069a99b3240ad034c6d7d99f2850",
  "impact": "non_blocking",
  "paper_id": "gk-2003-regular-national-new-arts",
  "question_id": "gk-2003-regular-national-new-arts-q01",
  "resolution": "题面按固定源逐字保留；答案与解析明确给出 (2,4]，并仍将对应选项记为 C。该矛盾不影响后续题面、生成和编译，但保留为来源问题。",
  "resume_action": "取得正式勘误或另一份清晰题面后复核第 1 题选项 C 的右端点；在此之前保留固定源字面与独立计算结果。",
  "source_id": "src-3ddeacd5e7af3ae7ea5e8d57361f03cb101441d1d16e2e0fb8745b9abb1f0ee1",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0818

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "2cc06daadd0a3c187869162c171917e1f0c87c9e529558a262322c6031fd8d28",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0819

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "db972284c6e50e314e8069e1ffd4520397d7e990c8836a98484603f827d6d0bb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0820

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "bd0cb85d3867435b1927dca267e5dfeee2f1ff8b3d6136e30ac9b916e2e18bfe",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0821

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "bff14bd42289d05d1083644a4ae64f5ac141fc9780d86025960ec74c477dd77a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0822

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "b56d09dd0938bea993959efa2a5862e227a57e3965167700b1c78936fe809d1c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0823

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "32124092157e5d509db0bec3124e40d231a30d88977dc25f8df835237a16c5f0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0824

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "cd12f23e438f411f65f51ebe4013ee09585ec26e125cf2c06ef060b7c4dadc77",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0825

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "5f451d7d1f7bf6c751df7a9564323505e5dff815cc2d4f77f5b46646a913ee7f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-1-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0826

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "672298816cf88b44b1a0f68ef474ba3d0f8fb66c382e2cae00dfa803d7c472a1",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0827

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "8f2d5f732e25c779ae1aae77186752942cf870d164cb95174499d8df845a48f2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0828

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "648678627533e40b0032e101be8f7b8564cb989174976b4d076daaa837446a4c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0829

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "1f6ec7f60d00824395b62f1de0f5cc99e41b6d02028bc8a283fcba564ee44941",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0830

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "05136cdd138ce31fa9ebef8a9e515d8817465acddab68f90e7e21f6c4cd69a51",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0831

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "3592b0b34c849e32a273a1782c898ca3ef5a4f5cc44b0a340b68c31c4e97ef3f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0832

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "05e79b1888d0ccb34b8192bc16f63ecb073db9ab7d8532bd55df389ffdcb843a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0833

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "3a525dff004cd450aad95bfd7378674aeb0efa422d5741a8edb0f90a3aad42cb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0835

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "24bd35eeaffce064f28a4bbc4f05edd2f4a4500043733fbeb02913606012914e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0836

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "447804d142fa1ec781e5d55322cd6bd4e8989500a8514b59061bd1aa1b69eef7",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0837

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "21be60d3ccb2ee85d30ac5844b4a74745abc5760f53fd695803a6d0fdfb79167",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0838

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "2c083fb899a769a625078a3e8d74a5fc17b7320e94b70c61c0404e6d40e0fdd6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0842

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "9aa462ec00473bf2517d85dd6570ae7ce778fa4b55895707711bec4aeb261035",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0843

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "4c83d6be516a0fa6ff760c3441dc40372faa83cfb3e5663ca4afe9b36e53cfcd",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0844

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "865a2810af73b98a26098744d684c9574cf670fdef21882ea1cdbc44bb96ecdb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0845

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "93fba392b0a78bd007f8220bbab8b9d82c6ee8b91f008c8d4b24647b723a80bb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0846

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "97d1d404267ccca98f78300b2904bf54c12d51f8869cdad6c427e5cfa4492ca0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0847

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "063c6735daa3d03c08f55ac856032c7303c23ebbb8bbbca498b4e885e1794827",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0848

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8354fbb6f1e0d53540491309c65ea079b8930558f3fc8a8868c26bf3d2c32e13",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0849

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "3b88812dc4d7e54ca921ceff0fb1b89c40792cd94433fabd7a212f4f5a249982",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2010-regular-national-new-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0850

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 印刷页 725 第 2 题题面为 A={1,3,√m}、B={1,m}、A∪B=A。按试题列举项互异的通常约定，采用 m=0 或 m=3（选 B）；但严格集合语义下 m=1 时 A={1,3}、B={1} 也满足 A∪B=A。解析正文已保留该歧义与处理方式，未静默改写固定源题面。",
  "fingerprint": "8bd931c77dff955268f4dc7be78143a2769f882228d30347f40dab94b944a697",
  "impact": "non_blocking",
  "paper_id": "gk-2012-regular-national-outline-science",
  "question_id": "gk-2012-regular-national-outline-science-q02",
  "resume_action": "题面集合列举语义已在解析正文登记；若需官方勘误，按同版源复核。",
  "source_id": "src-7f0b0f1da8f8f1cd330807f110972306ef01c21820e35933f4df5d306d608929",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0851

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标1文(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；SHA f726a1784cfa2eff4ebf812ea5e5a89f753bbcfd152c18066242a7bd22093f42。中国教育在线 2013-06-08 页面（https://gaokao.eol.cn/shiti/zhenti/201306/t20130608_957718.shtml）DOM 关联的第1页影像标为全国统考文科数学试题 A；同目录第5页影像（https://img.eol.cn/html/g/2013gkst/xkb/sxwa5.jpg）显示 22–24 三题任选一题，题目内容与固定源相符。此为第三方同期转载影像，未确认考试机构发布链或与固定源的版本关系，故规则旁证尚不足以关闭本问题。",
  "fingerprint": "e019ad164bd21d8c4dbe41f7fbb02ff3ae334e3f1cd8c6715c9204fe6aee1902",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-1-arts",
  "question_id": "gk-2013-regular-national-1-arts-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-47bd80f9a5d3b732a472e5fa228cf17ca1277abb11e832db0e9cded072589a92",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0852

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标1文(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；SHA f726a1784cfa2eff4ebf812ea5e5a89f753bbcfd152c18066242a7bd22093f42。中国教育在线 2013-06-08 页面（https://gaokao.eol.cn/shiti/zhenti/201306/t20130608_957718.shtml）DOM 关联的第1页影像标为全国统考文科数学试题 A；同目录第5页影像（https://img.eol.cn/html/g/2013gkst/xkb/sxwa5.jpg）显示 22–24 三题任选一题，题目内容与固定源相符。此为第三方同期转载影像，未确认考试机构发布链或与固定源的版本关系，故规则旁证尚不足以关闭本问题。",
  "fingerprint": "9ebc77bec64e16bdc610f4f259d8f8a0cf16da885f7fcf576dbfe461bf798bf7",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-1-arts",
  "question_id": "gk-2013-regular-national-1-arts-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-47bd80f9a5d3b732a472e5fa228cf17ca1277abb11e832db0e9cded072589a92",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0853

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标1文(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；SHA f726a1784cfa2eff4ebf812ea5e5a89f753bbcfd152c18066242a7bd22093f42。中国教育在线 2013-06-08 页面（https://gaokao.eol.cn/shiti/zhenti/201306/t20130608_957718.shtml）DOM 关联的第1页影像标为全国统考文科数学试题 A；同目录第5页影像（https://img.eol.cn/html/g/2013gkst/xkb/sxwa5.jpg）显示 22–24 三题任选一题，题目内容与固定源相符。此为第三方同期转载影像，未确认考试机构发布链或与固定源的版本关系，故规则旁证尚不足以关闭本问题。",
  "fingerprint": "4b057749012b897bffdf2c345aac0b56b322a79592b35d466bfee98bcf068f7b",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-1-arts",
  "question_id": "gk-2013-regular-national-1-arts-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-47bd80f9a5d3b732a472e5fa228cf17ca1277abb11e832db0e9cded072589a92",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0854

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标1理(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 3源核验记录；SHA a5a0e74db921b11074270f0e152023f81d73ec17d1a6b64377ecd9bcb106764c",
  "fingerprint": "04287df2ed7b45cff96f12b47c42b7958b1c1cb0d38b42edfd41b9e7f7e5f9f7",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-1-science",
  "question_id": "gk-2013-regular-national-1-science-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-993d110a9edd0c0bd5b892d64d897778e547bcce2efff6aab9f98668ef5ef2cb",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0855

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标1理(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 3源核验记录；SHA a5a0e74db921b11074270f0e152023f81d73ec17d1a6b64377ecd9bcb106764c",
  "fingerprint": "e985f6ea08e1eb7905b26889a1e60699f597a9aad1f7c2bebf7bb9efabb9eee7",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-1-science",
  "question_id": "gk-2013-regular-national-1-science-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-993d110a9edd0c0bd5b892d64d897778e547bcce2efff6aab9f98668ef5ef2cb",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0856

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标1理(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 3源核验记录；SHA a5a0e74db921b11074270f0e152023f81d73ec17d1a6b64377ecd9bcb106764c",
  "fingerprint": "636c18228ed54534bff292aa3f358a0aa7d76f1b029e05f75ecfb0c44b5d8423",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-1-science",
  "question_id": "gk-2013-regular-national-1-science-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-993d110a9edd0c0bd5b892d64d897778e547bcce2efff6aab9f98668ef5ef2cb",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0857

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 4源核验记录；SHA 7bc58472b3f68d708305e5123228aa513e88d4b76c64c541b08591f02fc167a6",
  "fingerprint": "cb656422e13ffd222170a73122867d6a80ccc16a1058c587f9575b3b6941aae7",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-2-arts",
  "question_id": "gk-2013-regular-national-2-arts-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-e970bf564d89917b7b671f6416394e3fddec287db66077465f40876add86de25",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0858

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 4源核验记录；SHA 7bc58472b3f68d708305e5123228aa513e88d4b76c64c541b08591f02fc167a6",
  "fingerprint": "9cd5f148bd58f183a2bbea5c492ee31c70c9a5e5aaa507e2908a5acede791711",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-2-arts",
  "question_id": "gk-2013-regular-national-2-arts-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-e970bf564d89917b7b671f6416394e3fddec287db66077465f40876add86de25",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0859

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 4源核验记录；SHA 7bc58472b3f68d708305e5123228aa513e88d4b76c64c541b08591f02fc167a6",
  "fingerprint": "abfb88504c46f186b865d3cd5973c0757dafc28d4321c2f433bb793540f57383",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-2-arts",
  "question_id": "gk-2013-regular-national-2-arts-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-e970bf564d89917b7b671f6416394e3fddec287db66077465f40876add86de25",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0860

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 5源核验记录；SHA 6e1b230072a3dfc55f6533d9afa35851ea5933ff6f4fd9bcfe12548105b064d4",
  "fingerprint": "39a86637391e1daea928c17f317e03898cc0869992fb0347386f4e4f6ca0108f",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-2-science",
  "question_id": "gk-2013-regular-national-2-science-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-e4f8542cdcec798eb72e918f651a993e7988b90e9eaa3b50cafa7b829ddf3edb",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0861

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 5源核验记录；SHA 6e1b230072a3dfc55f6533d9afa35851ea5933ff6f4fd9bcfe12548105b064d4",
  "fingerprint": "49583574cac63260c591074df97efaccc3a01d32ad47b4192100f1f214f2d7ec",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-2-science",
  "question_id": "gk-2013-regular-national-2-science-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-e4f8542cdcec798eb72e918f651a993e7988b90e9eaa3b50cafa7b829ddf3edb",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0862

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2013/2013新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 5源核验记录；SHA 6e1b230072a3dfc55f6533d9afa35851ea5933ff6f4fd9bcfe12548105b064d4",
  "fingerprint": "7b396ef52f31680324c334d144965ac7a10042cf28af75a3de860e11a19a8311",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2013-regular-national-2-science",
  "question_id": "gk-2013-regular-national-2-science-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-e4f8542cdcec798eb72e918f651a993e7988b90e9eaa3b50cafa7b829ddf3edb",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0863

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标1文(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 6源核验记录；SHA ea7f8f3172cf92b279fcadc4853d3b1942653182ba698cde59f42f45719aee6d",
  "fingerprint": "532b85fb564b247559c97cd217db7caf5154105503fe1e3a63780bda31a97e16",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-1-arts",
  "question_id": "gk-2014-regular-national-1-arts-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-4eef6d8d1598c2d404b03953d5739417310fabcdf5f543ab46bacef36a35ed4f",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0864

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标1文(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 6源核验记录；SHA ea7f8f3172cf92b279fcadc4853d3b1942653182ba698cde59f42f45719aee6d",
  "fingerprint": "aa9cf1708ba63ac9da86da6f6185dd8d0ce210c242d9f23e67b55f86ca16d2f0",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-1-arts",
  "question_id": "gk-2014-regular-national-1-arts-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-4eef6d8d1598c2d404b03953d5739417310fabcdf5f543ab46bacef36a35ed4f",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0865

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标1文(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 6源核验记录；SHA ea7f8f3172cf92b279fcadc4853d3b1942653182ba698cde59f42f45719aee6d",
  "fingerprint": "543896fcfbd24dfaad1a0f675fefc18081253d84c38254ed71415f7132b3f1f9",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-1-arts",
  "question_id": "gk-2014-regular-national-1-arts-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-4eef6d8d1598c2d404b03953d5739417310fabcdf5f543ab46bacef36a35ed4f",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0866

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标1理(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 7源核验记录；SHA 73a1b4f72e0d7cf3f90c4b82ff0802da49241fcbda76fdce4c2178b14a536c3b",
  "fingerprint": "e0073e240b78ab3c23b0b0c6eeb9f51589e1e4904e9d7cb68f543ce215e8c33c",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-1-science",
  "question_id": "gk-2014-regular-national-1-science-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-af40ea4e27633b30536919b9c6fa2ac65f153afdcfb06c749b36df5a9b4cd273",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0867

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标1理(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 7源核验记录；SHA 73a1b4f72e0d7cf3f90c4b82ff0802da49241fcbda76fdce4c2178b14a536c3b",
  "fingerprint": "2e362744fcc8df80d25b78feadfc3d90cf57ac6677cff069a38e144e7be94cd4",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-1-science",
  "question_id": "gk-2014-regular-national-1-science-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-af40ea4e27633b30536919b9c6fa2ac65f153afdcfb06c749b36df5a9b4cd273",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0868

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标1理(河南,河北,山西).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 7源核验记录；SHA 73a1b4f72e0d7cf3f90c4b82ff0802da49241fcbda76fdce4c2178b14a536c3b",
  "fingerprint": "37b97ce7aac97e6a109dccdf8bcd82a3a57f810b82d3aaf1eb747cde70579218",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-1-science",
  "question_id": "gk-2014-regular-national-1-science-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-af40ea4e27633b30536919b9c6fa2ac65f153afdcfb06c749b36df5a9b4cd273",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0869

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 8源核验记录；SHA b880ebb42bb2cf715ccb3ad1ebe5735d461c27ccc183edd157713a9bf0252755",
  "fingerprint": "5a0200f591016b9c44beb3a58d1c17110682d4220493658c10d84d1db17bc9d0",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-2-arts",
  "question_id": "gk-2014-regular-national-2-arts-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-6ba375c5a83f9e54600e3119a319860ec5959a6fe0116dd7e9adaf4bc4856e39",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0870

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 8源核验记录；SHA b880ebb42bb2cf715ccb3ad1ebe5735d461c27ccc183edd157713a9bf0252755",
  "fingerprint": "c27c0bd020ba081b76b89da9f753d2a613c429f0500b89cfaec3ceb33b56aacb",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-2-arts",
  "question_id": "gk-2014-regular-national-2-arts-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-6ba375c5a83f9e54600e3119a319860ec5959a6fe0116dd7e9adaf4bc4856e39",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0871

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 8源核验记录；SHA b880ebb42bb2cf715ccb3ad1ebe5735d461c27ccc183edd157713a9bf0252755",
  "fingerprint": "89076b7a90f2710bb22fdcefcc510f5ede05803b41ab30df96d67953870550a5",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-2-arts",
  "question_id": "gk-2014-regular-national-2-arts-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-6ba375c5a83f9e54600e3119a319860ec5959a6fe0116dd7e9adaf4bc4856e39",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0872

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 9源核验记录；SHA bf39cc10e8b3fe567565ba8f6a7d0330d13dac159683934e8c879897619aed57",
  "fingerprint": "61c28cab92e35b13cba84204c4766fbda050b59eb863880061d735c4b9df6857",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-2-science",
  "question_id": "gk-2014-regular-national-2-science-q22",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-0f812d4bb74d17dae79bf679938826223140fb59276e04a168ae98f256a60e2e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0873

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 9源核验记录；SHA bf39cc10e8b3fe567565ba8f6a7d0330d13dac159683934e8c879897619aed57",
  "fingerprint": "f7d27195bee54d647e3e4ab7106a8e30e2da878769f629821a1af2fa5592296f",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-2-science",
  "question_id": "gk-2014-regular-national-2-science-q23",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-0f812d4bb74d17dae79bf679938826223140fb59276e04a168ae98f256a60e2e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0874

```json
{
  "affected_paper_ids": [],
  "detail": "缺少作答规则，不影响本库已给的逐题独立解答，但阻断规则完整性验收。",
  "evidence": "固定源 普通高考/2014/2014新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf PDF 第2页，仅连续编号22–24，无选考标题或任选/必答规则；研究报告及Task 9源核验记录；SHA bf39cc10e8b3fe567565ba8f6a7d0330d13dac159683934e8c879897619aed57",
  "fingerprint": "c7caacb3b8bf227244c42487497073d83a75d3c4ffbf67dbd035d2475faf2162",
  "impact": "blocks_completion",
  "origin": "phase2-b02-source-rule",
  "paper_id": "gk-2014-regular-national-2-science",
  "question_id": "gk-2014-regular-national-2-science-q24",
  "resume_action": "取得可审计的原卷作答规则页，明确第22–24题作答属性后复核并结案；当前保留题面全部24题，不猜必答或选答。",
  "source_id": "src-0f812d4bb74d17dae79bf679938826223140fb59276e04a168ae98f256a60e2e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-0875

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "7f5095f38ae98fa2ec6a312e80f8151613843c111259f7e6b024771441478f2d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2014-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0876

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "5e87d224aa85bc33ea195bffc88b4d16fe8aa7c6e7b317e8094330c7b393be1a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2014-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0877

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "10bcfc98040a8a1ac720d8324a8fcbb7768fb2322d8a0f35c07782e1b8a84fd0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2014-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0878

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ef17d97ac08b8da666103d934c7dcdeb2abdedb6dd905ff3df19553e21461d63",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2014-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0879

```json
{
  "affected_paper_ids": [],
  "detail": "原题未限定公切线类型；文科单值答案与理科同型题既有多分支解析不一致，不猜答案。",
  "evidence": "Task10直接视觉核验固定源PDF第2页：直线同时与两圆相切，未限定内公切线；文科答案只给2sqrt3，理科既有解析另列18/7。",
  "fingerprint": "cc86600077917ae1100b6434d07654202be998cfce1a2d4493166fe3e8f04a9e",
  "impact": "blocks_completion",
  "origin": "phase2-b02-tangent-audit",
  "paper_id": "gk-2013-regular-national-1-arts",
  "question_id": "gk-2013-regular-national-1-arts-q21",
  "resume_action": "核对原卷切线类型及完整答案；未解决前不得声称唯一弦长。",
  "source_id": "src-47bd80f9a5d3b732a472e5fa228cf17ca1277abb11e832db0e9cded072589a92",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0880

```json
{
  "affected_paper_ids": [],
  "detail": "原题未限定公切线类型；文科单值答案与理科同型题既有多分支解析不一致，不猜答案。",
  "evidence": "Task10直接视觉核验固定源PDF第2页：直线同时与两圆相切，未限定内公切线；文科答案只给2sqrt3，理科既有解析另列18/7。",
  "fingerprint": "a43b2f7c324cd1d244e608f6bc4b2f082327f4594291f9b4ad5c5d3cd7ef2134",
  "impact": "blocks_completion",
  "origin": "phase2-b02-tangent-audit",
  "paper_id": "gk-2013-regular-national-1-science",
  "question_id": "gk-2013-regular-national-1-science-q20",
  "resume_action": "核对原卷切线类型及完整答案；未解决前不得声称唯一弦长。",
  "source_id": "src-993d110a9edd0c0bd5b892d64d897778e547bcce2efff6aab9f98668ef5ef2cb",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0881

```json
{
  "affected_paper_ids": [],
  "conflict_code": "pdf-header-national-i-vs-national-b-arts",
  "current_evidence": "固定上游 PDF 的内页标题逐字为“2021 普通高等学校招生考试（全国卷 I 文）”，而 manifest 固定上游路径文件名为“2021全国乙文(河南,山西,江西,安徽,陕西,甘肃,青海,内蒙古,黑龙江,吉林,.宁夏,新疆).pdf”；两者卷别标签冲突。",
  "fingerprint": "65ddec79486f0cb1ec812571693b6c80a72c562ecbe8363b9351f92279843fe3",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-b-arts",
  "resolved_evidence": "身份判定依据为固定上游路径及题目指纹，而非 PDF 内页标题。人民网转载的教育部考试中心 2021 命题评析将全国乙卷文、理第 16 题描述为开放性空间三视图，并称第 17 题考查芯片蚀刻速率统计；固定源乙文相应题目匹配。乙文第 9 题为奇函数变换，与同组乙理第 9 题《海岛算经》测量这一辨别指纹相异；因此乙文认定是固定路径与乙卷共享题目指纹结合后的判断，不声称评析单独识别了乙文第 9 题。评析来源：https://edu.people.com.cn/n1/2021/0608/c1006-32125641.html；官方评析索引：https://gaokao.neea.edu.cn/html1/category/21123/683-1.htm。内页标题冲突原因未知，不推测。",
  "resume_action": "无需后续动作；固定上游路径与题目指纹支持认定为 2021 全国乙文。PDF 内页眉照录；其与路径冲突的原因未能核实，不作推测。",
  "source_id": "src-626df595a17ee20bfaa1b298aee86d211ce914a9ae11ccf337ac9a30024d5e7a",
  "status": "resolved",
  "type": "identity-ambiguous"
}
```

## ISSUE-0882

```json
{
  "affected_paper_ids": [],
  "conflict_code": "pdf-header-national-ii-vs-national-a-science",
  "current_evidence": "固定上游 PDF 的内页标题逐字为“2021 普通高等学校招生考试（全国卷 II 理）”，而 manifest 固定上游路径文件名为“2021全国甲理(云南,广西,贵州,西藏,四川).pdf”；两者卷别标签冲突。",
  "fingerprint": "b9bd5af46f498a7c025195e7044a4820f6078ccf76c8aee680efec1bd12dc613",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-a-science",
  "resolved_evidence": "人民网转载的教育部考试中心 2021 命题评析指出，全国甲理第 8 题考查珠穆朗玛峰高度的三角测量，第 18 题为依据部分条件构造命题的立体几何问题；固定上游甲理 PDF 的对应题目指纹匹配。结合固定上游路径，认定其为 2021 全国甲理。来源：https://edu.people.com.cn/n1/2021/0608/c1006-32125641.html；官方评析索引：https://gaokao.neea.edu.cn/html1/category/21123/683-1.htm。内页标题冲突原因未知，不推测。",
  "resume_action": "无需后续动作；固定上游路径与题目指纹支持认定为 2021 全国甲理。PDF 内页眉照录；其与路径冲突的原因未能核实，不作推测。",
  "source_id": "src-97009310da2991644af50876d699aa0d2dc8399ed121340a0971157962419f1a",
  "status": "resolved",
  "type": "identity-ambiguous"
}
```

## ISSUE-0883

```json
{
  "affected_paper_ids": [],
  "conflict_code": "pdf-header-national-i-vs-national-b-science",
  "current_evidence": "固定上游 PDF 的内页标题逐字为“2021 普通高等学校招生考试（全国卷 I 理）”，而 manifest 固定上游路径文件名为“2021全国乙理(河南,山西,江西,安徽,陕西,甘肃,青海,内蒙古,黑龙江,吉林,.宁夏,新疆).pdf”；两者卷别标签冲突。",
  "fingerprint": "85c879810527f9740041e2e84abfa8baf16359b38beb8ec9462d02a1d61af83d",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-b-science",
  "resolved_evidence": "人民网转载的教育部考试中心 2021 命题评析将全国乙理第 9 题对应于刘徽《海岛算经》测量，并将全国乙卷文、理第 16 题对应于开放性空间三视图、第 17 题对应于芯片蚀刻速率统计；固定上游乙理 PDF 的相应题目指纹匹配。结合固定上游路径，认定其为 2021 全国乙理。来源：https://edu.people.com.cn/n1/2021/0608/c1006-32125641.html；官方评析索引：https://gaokao.neea.edu.cn/html1/category/21123/683-1.htm。内页标题冲突原因未知，不推测。",
  "resume_action": "无需后续动作；固定上游路径与题目指纹支持认定为 2021 全国乙理。PDF 内页眉照录；其与路径冲突的原因未能核实，不作推测。",
  "source_id": "src-07fbd034606d9e5fb0eb1763810e19e4b80175b24e53639b4cfe860c6b6fe067",
  "status": "resolved",
  "type": "identity-ambiguous"
}
```

## ISSUE-0884

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定上游 PDF 的第 23(2) 题原文为“若 f(x)>−a，求 a 的取值范围”，没有明示对 x 的全称或存在量词。若解释为对任意实数 x 恒成立，最小值条件给出 a>−3/2；若解释为存在实数 x 满足不等式，则因 f(x) 随 |x| 增大而无界，对任意实数 a 均可成立。两种解释的答案范围不同。",
  "fingerprint": "b8432b37a59ad71f497f4dd3128e3e1db9b88de7f57baa4ef389df5b73b8e0b7",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-b-arts",
  "question_id": "gk-2021-regular-national-b-arts-q23",
  "resume_action": "取得该版官方答案、勘误或其他权威同版文本，确认第 23(2) 题是否省略了“对任意 x 恒成立”等量词；在证据到位前保留题面原文，将 a>−3/2 明确标作全称解释下的条件答案，不宣称唯一结论。",
  "source_id": "src-626df595a17ee20bfaa1b298aee86d211ce914a9ae11ccf337ac9a30024d5e7a",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0885

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页第 11 题选项 B 与 D 均印为 √3/12；页面视觉复核确认该重复来自源卷。规范题面逐字照录两项。按题设 AC⊥BC、AC=BC=1 且 A、B、C 在单位球面，独立计算的体积为 √2/12，对应 A；重复选项不改变本题答案。",
  "fingerprint": "8b057fc85252de03d7903ac110e9b0727b102eb7304af6a6035b23fa8f020457",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-a-science",
  "question_id": "gk-2021-regular-national-a-science-q11",
  "resume_action": "取得同版官方勘误或其他权威同版文本，确认 B、D 重复是否为源卷印刷错误；在此之前保留选项原文与独立答案 A，不自行订正源卷。",
  "source_id": "src-97009310da2991644af50876d699aa0d2dc8399ed121340a0971157962419f1a",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0886

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定上游 PDF 第 2 页第 23(2) 题原文为“若 f(x)>−a，求 a 的取值范围”，没有说明对 x 的全称或存在量词。全称解释下，f(x)=|x−a|+|x+3| 的最小值为 |a+3|，条件给出 a>−3/2；存在解释下，f(x) 随 |x| 增大而无界，对任何实数 a 都可找到 x 满足不等式。两种解释的取值范围不同。",
  "fingerprint": "6f0bc608ed24e32ce4b169fe958d3a0552dafe423b75fedc25a39607675aadf2",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-b-science",
  "question_id": "gk-2021-regular-national-b-science-q23",
  "resume_action": "取得该版官方答案、勘误或其他权威同版文本，确认第 23(2) 题省略量词是否为源卷原貌；在证据到位前保留题面原文，并将 a>−3/2 仅标作全称解释下的条件答案，同时注明存在解释对应全体实数。",
  "source_id": "src-07fbd034606d9e5fb0eb1763810e19e4b80175b24e53639b4cfe860c6b6fe067",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0887

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "4312bd6ec61586b46d30822e692985499c84c184c5d599d3bf6b163cbf37ab4e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0888

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "7d4814b6183e3a1737a4b022ee4267457361a63a41c057d8734aaa5cd3eddbf1",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0889

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8783ac194e5bccc124a0573c1c74f7f25c26aa390907ed03b35cf974a46061be",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0890

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "e27b56310221364f78418b571f8ce045bbad386b20e1fad086f1cd5d582598ce",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0891

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "8a2506dc80936f4bac38b98bdc9728937a171f0c26990b5bcd99402328ab4a44",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0892

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "f6f3b4279bf25c96add14ae41f7967c6b0c19e7e2b43cae9d796f569631b31ca",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0893

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "9136a3a1c511d8754daf3581587d556ed96c1391e537750e4904e3f613e7437c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0894

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "63688e83fcba6f3b92a224e756541816e831304984c4a4c939434eabbd9e7b37",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0895

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页第 23(2) 题写作“若 f(x+a)≥g(x)，求 a 的取值范围”，未明示 x 的量词。对任意 x 恒成立时，必要且充分条件为 a≥11/2；若只要求存在 x，则任取 x≤−3/2 即有 g(x)=−4≤0≤f(x+a)，故所有实数 a 均可。两种解释结论不同。",
  "fingerprint": "1dfe0c044f3445e8a25ca311797d28a4400986eb80b939401aff61101e3a5240",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-regular-national-a-science",
  "question_id": "gk-2021-regular-national-a-science-q23",
  "resume_action": "取得官方答案、勘误或其他权威同版文本，确认第 23(2) 题是否省略“对任意 x 恒成立”等量词；在证据到位前保留题面原文，将 a≥11/2 标为全称解释下的条件答案，并列出存在解释为全体实数。",
  "source_id": "src-97009310da2991644af50876d699aa0d2dc8399ed121340a0971157962419f1a",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0896

```json
{
  "affected_paper_ids": [],
  "fingerprint": "0dca239d477bc4e3efca2f3011560af855f2d967f9c732ed7172a6bddfd8a306",
  "impact": "blocks_completion",
  "paper_id": "gk-2022-regular-national-a-science",
  "question_id": "gk-2022-regular-national-a-science-q08",
  "resolved_evidence": "固定源 PDF（SHA-256 f3083062446f8eaddb58875e435de933325a6bc1c6fcbf684eca86e1e555d9c9）第 1 页（纸面页码 1161）题干写明 C 是 AB 的中点、D 在弧 AB 上且 CD 垂直 AB；原图标签与题干一致。规范题面、解析和答案要点已按源文校正，原 TikZ 图稿正确并保留。phase2-b04 正式重编及视觉回执 FINALIZED；核验试题版第 3 页、解析版第 3/11 页、简答版第 3/6 页、印刷版第 2/7 页，四版共 49 页，页数 5/22/7/15，图文及答案 B 一致。",
  "resume_action": "无需后续动作；题面、解析和答案要点已同步，图稿与原文一致，四版本重编及视觉复核通过。",
  "source_id": "src-df2119c91f5a43a34e1716f4465359f6b64ba82e253d551e941126bc7e041831",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0897

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立核源（2026-11-09，.work/verify/2022-b-arts-q21.md）：水平线 y=-2 与椭圆 x²/3+y²/4=1 相切于 A(0,-2)，只有一个交点，被题干「交 E 于 M,N 两点」排除；H=N 需两交点纵坐标相同即 u=w，仅切线（k=0 或 k=2）时发生。故题设下恒有 H≠N，定点为 A(0,-2)。已改答案要点、解析正文、含解析三处并把 U/PENDING 降为定论。",
  "fingerprint": "920c377a901ddafb396c348f4b98b91817080dda4f54d4bbf4708f6f358d63b5",
  "impact": "blocks_completion",
  "paper_id": "gk-2022-regular-national-b-arts",
  "question_id": "gk-2022-regular-national-b-arts-q21",
  "resume_action": "已按独立复算给出唯一答案 A(0,-2)；如日后取得官方答案页可再比对。",
  "source_id": "src-e940ecc4f17429569b803de22ce16b6de7de5433e5e0c169584e3ed752288538",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-0898

```json
{
  "affected_paper_ids": [],
  "fingerprint": "35ffad13f27bcdf0fa51bf4305100571abcad74a5cf75126142e25984c21187f",
  "impact": "blocks_completion",
  "paper_id": "gk-2022-regular-national-b-science",
  "question_id": "gk-2022-regular-national-b-science-q11",
  "resume_action": "核实源题对 N 分支及 M、N 顺序的定义；补足条件后再确定选项。",
  "source_id": "src-b0b51a3f8309bc89c893fda343f481ab5a6011f2ca1b1dc21be11436bd938da2",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0899

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e98250f884eb097d4bd6cc1f2be7e407ecd85d338df6ecad9f6b1eb6d1344807",
  "impact": "blocks_completion",
  "paper_id": "gk-2022-regular-national-b-science",
  "question_id": "gk-2022-regular-national-b-science-q16",
  "resolution": "乙理第 16 题按源面 2a^x-e·x^2 重推：a>1 得 a<e，0<a<1 得 a>1/e，答案 (1/e,1)∪(1,e)，数值扫描边界 0.368/2.718 一致",
  "resume_action": "回查源 PDF 中指数项及“极大/极小”文字；确认原题或转录后重解。",
  "source_id": "src-b0b51a3f8309bc89c893fda343f481ab5a6011f2ca1b1dc21be11436bd938da2",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-0900

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "411c2503a0b158b870877dc7b737ec0dd55b1a7ec8ec7837dc38daea2eea441a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0901

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "8109dd014f55468aec4ce171e685d0dab4a2db86b9097d96bbc4f5774fc9f140",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0902

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "1abe9673322bdcf63e5a2615dd06d1d834dfdd1104e7e42092172e3f49ffb650",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0903

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "182e7792ec5fc93c11de377c8b6808bb408cc46ba92f3657bac7b61fc2a3f2c8",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0904

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "99dde062cca1008ebbba422a779c904e3aae028711fb2917fa1662bf0c04cfc4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0905

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "847297fd41cfa55d2d176455f3a6e006cff4677c6ee7d4f6e5555d533ee708a2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0906

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "7c07a33634206b6f2c6fe9db311d6432ddf0eb5c70023ed34f734425213b155b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0907

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "5430e991eb81a1012dc44749d1f08c9c5908a68737e10c8c78d09927b7ec6ee9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-a-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0908

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "bad8aa998e1be0a8a527327018ddf7aa7bb7e3c4ee755821bb3a586fe09b6e89",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0909

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "915439c346ee709b72ceed0f29627b7ddf6e0e9eed99cf293f54966f560df5be",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0910

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "ae07c179f3fae0d873dc5215772a1e898d3070595bdb7c6451607fcc089611c9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0911

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "afe872005e1e3842e82318cab4b767fa2db9100483ce80c59b31b569316dfd96",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0912

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "b23aa90125a90d482f17547a771f581ee2966fede45f5046820a3b9ba6ce04ce",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0913

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "b0f6bd81d5fcbf149ab30ef922823a0096777ab31cac007455edcb61d6dd9b24",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0914

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "5d8c17529399aea69cfafd14c25bba3f1a2bf620ba9c73d1b481b801ff40ae2e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0915

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "2815e9f960be57b2186d43fef6ee4cf4615150036dc9117a8b176016d7e8ebc6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2022-regular-national-b-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0916

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0c6feec3-9e12-41f8-b701-f8e2512a8d52",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "b175b8756b5081c48c4c32a27552a59623abaa0b670f3174687dd1166e1a96ec",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1977-regular-shanghai-science",
  "pdf_sha256": "d4ee341e79fadd6aa816b1b60cb62f1e1340442d6168a36a35d91ab5a53d196d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0917

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1ae872f1-f32d-4870-b097-4fe0521351e8",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "d849aa0d6d95ad74648698225b77dbdb282ad5cadd70d0f31b82a4df0f608ce2",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1977-regular-shanghai-science",
  "pdf_sha256": "6defac065a96779e3a0e44f287f7f26085f14d6d92a3b1c45842b2a85143a076",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0918

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0c6feec3-9e12-41f8-b701-f8e2512a8d52",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "ff1e71fd6c2629f63f4a99188310792d5eff50d4ce1f43f12856ca988d395139",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 9,
  "paper_id": "gk-1977-regular-shanghai-science",
  "pdf_sha256": "f3fecc50a012d2e64eefa3f432891aff1552532b2f90c8c352c48e4e9c8734eb",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0919

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1ae872f1-f32d-4870-b097-4fe0521351e8",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "14560cda23ba9587c85102653709e7bf17361b560ece563bba6a64b20069c8e2",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 9,
  "paper_id": "gk-1977-regular-shanghai-science",
  "pdf_sha256": "59a254ef121544e0104482d184de8a4ec00e668b2d85a1461c85724b90be924d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-0920

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "78651015-39fd-4d54-8014-698429f7adc3",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "8d034f6458d5e8c127e7f57175a688a77bb55d18d6e5e694c761628dedd6ed0c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 24,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "f93b7e838a1451b5acfd5973e88ab1de933c2dbb498ec9db09e3a3c9ad62f6ab",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0921

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "78651015-39fd-4d54-8014-698429f7adc3",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "928fbf410cd779396adad9a14639ddfaa17f2c6428360f4b6d59bbb30dc0df88",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "19c402a8e8a2bb6161ddc7d6b16a0a85ac83806932effc4756be1c584b75e4de",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0922

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "78651015-39fd-4d54-8014-698429f7adc3",
  "check_code": "pagination_whitespace",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "744e6e2f215aef4582aa2f52334705b0748327f7c52a727745530325c111edc4",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "803d7cbb5280eb7286f816d1ebc4d0309d81995ddf173320ec6db1ee43431474",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-0923

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f6a1bc8b-f5f7-4d86-8ea0-b532277cad21",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "8f80a43ebf39cc63cfd8421bfd770b8bd8f1e206091ad90cf9298b62b015d202",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 20,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "9c8493861296eef7f557aa90894ccef664122878e0549edddceb092e12f931e6",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0924

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f6a1bc8b-f5f7-4d86-8ea0-b532277cad21",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "26dbd18ad808250a02bbc6773d4fa726d1741bb4ad21375ef4fbfbfe88a48fb1",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 22,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "9c8493861296eef7f557aa90894ccef664122878e0549edddceb092e12f931e6",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0925

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f59a2fbd-f3c2-4464-8d61-2f6655926f04",
  "check_code": "heading_number",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "5ee20475a6fdfe5720bee0d46c67f8cde3a43374efd71d26c17c1a0ed5fe4879",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 23,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "b83b425198cd7e88c84adc5e91af6ef7aaf12be147993f2058fbb279bf6db7cc",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0926

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "689c7c0e-349b-4028-8571-29f713b76877",
  "check_code": "heading_number",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "e44ddf7927e3dbaaf2ad7fa27c1c9163b8bf6250184e1be7a7b4a7d3fb18b981",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "e279edebc810f2a77303d9d39a365ed240051e565818a88d321b85228999574e",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0927

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f6a1bc8b-f5f7-4d86-8ea0-b532277cad21",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "0b1bf905c639265833983b133ddd64a31cf6c433270ef9b9a8366fbd744454da",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 27,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "a16c24221e7554da1de5cf225788308dcf071f748d937566af7d2d9f0ed95059",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0928

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f6a1bc8b-f5f7-4d86-8ea0-b532277cad21",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "f463448e51a8b21e8944d747d880c0113bf84024390d41d2158f16b2dd680809",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 30,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "a16c24221e7554da1de5cf225788308dcf071f748d937566af7d2d9f0ed95059",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0929

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f59a2fbd-f3c2-4464-8d61-2f6655926f04",
  "check_code": "heading_number",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "2c37b7be7ea5923930e327ca297fd4acfae73819279b37f431bca5245a718bb1",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 32,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "af51bdc37bd90816a379b87711ded5990f69ca340625cd0092a04b25bf0924fd",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0930

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f59a2fbd-f3c2-4464-8d61-2f6655926f04",
  "check_code": "heading_number",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "164e83fccf2cf8413e9885d10fe9a273f1c34c9caec5ef30b16ca5912c290fc9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "5861a1abda69fe65624da5af31b7cd57dc9a29d3bb4e4d5b5338eb13ecbb424f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0931

```json
{
  "affected_paper_ids": [],
  "fingerprint": "6f4cc6140c48fdfe6417b651983404fe0668a85d775389b2a97b867aa40bb7f9",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-2-science",
  "question_id": "gk-2016-regular-national-2-science-q18",
  "resume_action": "核对原卷组题说明或考试机构勘误，明确“高出60%”表示恰好还是至少；未消歧前保留 U 并阻止该卷完成。",
  "source_id": "src-95b9fb9d77fbab0c74756443da599d2969dcd905991d5faf2c6cfbadae3328ae",
  "status": "investigating",
  "type": "answer-conflict"
}
```

## ISSUE-0932

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页与规范题面均只写 a>0，未要求 C1、C2 有非空交集。两圆圆心距为 √5、半径为 a 与 2；空交集时还存在 0<a<√5−2 或 a>√5+2。按全称命题字面读法条件空真；按考试常规预设公共点则答案 a=1。全国Ⅰ文、理源卷此题同文。",
  "fingerprint": "14403c9fdcf879138f22fc2d50a488b48fc6a030d313847c5965c118d3add8cb",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-1-arts",
  "question_id": "gk-2016-regular-national-1-arts-q23",
  "resume_action": "查找该题官方答案或命题说明，确认“公共点都在”是否预设非空交集；消歧前保留惯常解读 a=1 但标 U，并阻止该卷完成。",
  "source_id": "src-31bfc647b7ec677fe34d4e50a2fb23184952e0ecbc1c67cfcbc99ed302b81240",
  "status": "investigating",
  "type": "answer-conflict"
}
```

## ISSUE-0933

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页与规范题面均只写 a>0，未要求 C1、C2 有非空交集。两圆圆心距为 √5、半径为 a 与 2；空交集时还存在 0<a<√5−2 或 a>√5+2。按全称命题字面读法条件空真；按考试常规预设公共点则答案 a=1。全国Ⅰ文、理源卷此题同文。",
  "fingerprint": "f37261ece1a5c75dbe3c53514fe37b2323480eadd74a7d522da072bbb840b889",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-1-science",
  "question_id": "gk-2016-regular-national-1-science-q23",
  "resume_action": "查找该题官方答案或命题说明，确认“公共点都在”是否预设非空交集；消歧前保留惯常解读 a=1 但标 U，并阻止该卷完成。",
  "source_id": "src-22dfb5d209bc2df4fdd197e76b3e16e72bd49aa0d196debfeea5fa6c7e9d2e4b",
  "status": "investigating",
  "type": "answer-conflict"
}
```

## ISSUE-0934

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 与规范题面仅要求公共点均位于 C3，未明确两曲线有公共点；若交集为空，全称命题条件空真且 a 不唯一。当前惯常考试读法 a=1 尚无同版官方答案或命题说明确认，故答案等级 U。",
  "fingerprint": "00af778cc17dcc3bf82d237e28797be425339b0b7c56e5b0fcb6907950e9a7a9",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-1-arts",
  "question_id": "gk-2016-regular-national-1-arts-q23",
  "resume_action": "取得同版官方答案或命题说明，确认题目是否隐含两曲线有非空公共点；消歧前保留 U 并阻止完成。",
  "source_id": "src-31bfc647b7ec677fe34d4e50a2fb23184952e0ecbc1c67cfcbc99ed302b81240",
  "status": "investigating",
  "type": "answer-missing"
}
```

## ISSUE-0935

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 与规范题面仅要求公共点均位于 C3，未明确两曲线有公共点；若交集为空，全称命题条件空真且 a 不唯一。当前惯常考试读法 a=1 尚无同版官方答案或命题说明确认，故答案等级 U。",
  "fingerprint": "b1c33a183849622eb40770af3183118c5b34aae780c15708ee7e028b000085a4",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-1-science",
  "question_id": "gk-2016-regular-national-1-science-q23",
  "resume_action": "取得同版官方答案或命题说明，确认题目是否隐含两曲线有非空公共点；消歧前保留 U 并阻止完成。",
  "source_id": "src-22dfb5d209bc2df4fdd197e76b3e16e72bd49aa0d196debfeea5fa6c7e9d2e4b",
  "status": "investigating",
  "type": "answer-missing"
}
```

## ISSUE-0936

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源题面写“高出60%”但未明确恰好或至少；严格等式与阈值解释会得出不同答案。现有 3/11 仅由外部答案参考支持，原题本身不足以确认唯一解释，故答案等级 U。",
  "fingerprint": "a91c8234dd981b5f573e132cb6ad13e0f54c3162e37ef93ae47718af63d2c69a",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-2-science",
  "question_id": "gk-2016-regular-national-2-science-q18",
  "resume_action": "取得同版官方答案或命题说明，明确“高出60%”表示恰好还是至少；消歧前保留 U 并阻止完成。",
  "source_id": "src-95b9fb9d77fbab0c74756443da599d2969dcd905991d5faf2c6cfbadae3328ae",
  "status": "investigating",
  "type": "answer-missing"
}
```

## ISSUE-0937

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "618b5994cc1a8d7c67dca41a0d90224c373189f3127f8a71b12b39e4007cb2a4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0938

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "24d7f42b772180b1862a9de4a04943baddf5dd6ebf580f5730b2b52f0a26ba86",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-national-1-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0939

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "4c7586fdad57de3032554859719233854225ecd65d5cadfb643adee47f3e3017",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0940

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "42c0949466abefaf392b230677452a24694f683f7026baff1dd78f8659c2a791",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0941

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "cd3e5f09c8b51124c9282941b934c98b08090633a11a965a3d17792921f7f990",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "ae1e727de8658d1fb7d64d635373bcf754ff42543b7a02518244c2fdbd25fa37",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0942

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "4d7a6391e277ddecad49840651dda4d8c597f2410649f140420d0dbf5172728c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "ae1e727de8658d1fb7d64d635373bcf754ff42543b7a02518244c2fdbd25fa37",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0943

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "9647855a78a6f60b74ff6e1de857ca41625f9f0f160e94d83873fc5c9375f2d7",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "ae1e727de8658d1fb7d64d635373bcf754ff42543b7a02518244c2fdbd25fa37",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0944

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "94a457782cf9b182fd8177d2e88f3080bc5d272ba73ebd9582731c1768a7b4db",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 8,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "ae1e727de8658d1fb7d64d635373bcf754ff42543b7a02518244c2fdbd25fa37",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0945

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "964be83718c19c450843bcc22c04b0a7c49b59335fda7c4edd7e6faabea568c7",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "f35b7c6751d9304c9765ea8865960a237822996ba21ce9b7f7fde2d835cff8a6",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0946

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "3e14f98727953368de980149d5ec51e5a5d148528821050b492e8d043c2849f8",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "1667c560a82b2c6906aa08e0fea14de749fd9f077761a74e1525dce2655d10b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0947

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "7915fc7586433ef2e3282ec5d29b02c199daf6242ca535e76ab315be568b4acc",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "1667c560a82b2c6906aa08e0fea14de749fd9f077761a74e1525dce2655d10b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0948

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "32409fd9aea86b1e1fb99493a17b1dcacc24e3bae463cb8ab5b0f8a651c52673",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 8,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "1667c560a82b2c6906aa08e0fea14de749fd9f077761a74e1525dce2655d10b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0949

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "81f00297db5ecf90d30f4dde24399abe8924e9603bececa06d50101106a13b2a",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 9,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "1667c560a82b2c6906aa08e0fea14de749fd9f077761a74e1525dce2655d10b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0950

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "46ec6f153c8ea46b132bb475bb575763015a9fa52ffa63a5666fd961986a0091",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 10,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "1667c560a82b2c6906aa08e0fea14de749fd9f077761a74e1525dce2655d10b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0951

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "d7306ced-53f1-4f77-979b-d5564572705e",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "2ce640ad285061f18db74b46924168bd25371516ae648b59e41a15806e3a0b40",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-1964-regular-national",
  "pdf_sha256": "91cfdc165be31a51b3797dbf85ca2399bee0bf02183a1a1299824ddc814bea3c",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-0952

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 印刷页 1043 第17题仅给 a1=-1、b1=1、a2+b2=2、T3=21。令等差公差 d、等比公比 q，则 d+q=3 且 1+q+q^2=21，得到两个非零合法公比 q=4、q=-5；相应 S3=6-3q，分别为 -6、21。全国Ⅱ文科 solver 与独立 blind reviewer 均从题面独立得到这两支，未发现能排除任一支的印刷条件。",
  "fingerprint": "a406351b9a3dc21b74073f84f529008d9cb16a07581ff2114a46dde10da452bf",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-2-arts",
  "question_id": "gk-2017-regular-national-2-arts-q17",
  "resume_action": "取得可追溯的同版官方勘误或可靠说明，确认原卷是否遗漏用于选定公比的条件；若无勘误，继续保留所有满足原题的分支并标为 U。",
  "source_id": "src-0a282ae5bb0daabc25cea61ee4d965a48b2fc56a5877a5388d6795a178b22efa",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0953

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 印刷页 1046 第20题设抛物线 y²=2x，直线过 (2,0)，以两交点为直径的圆过 P(4,-2)，要求直线和圆方程。solver 与独立 blind reviewer 在隔离完成后均从题设推得两组有效解：k=1，l:y=x-2，圆 x²+y²-6x-2y=0；k=-2，l:y=-2x+4，圆 x²+y²-(9/2)x+y=0。两条直线各与抛物线有两个不同交点，所成直径圆均过 O 与 P；原题未给条件选定其中一组，故答案不唯一，应标 U。",
  "fingerprint": "8e7dc4c3d700bee120ef132252e50558c6b3217e080ed4b69f5f7f9aee344d7e",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-3-science",
  "question_id": "gk-2017-regular-national-3-science-q20",
  "resume_action": "取得同版可靠勘误或来源说明以确认原题遗漏的选解条件；若无勘误，保留两组满足原题的解并标 U，不补造条件。",
  "source_id": "src-63aac70d1ccb26b495575266a078b3eeebdfa0fbe6e7f05ff309c4a1a6d7775b",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0954

```json
{
  "affected_paper_ids": [],
  "fingerprint": "21b1d2e41f8792e8cf48fcc7e5cc40edb5807b67c5d4e0ef14e8dc70df166ec3",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-2-arts",
  "question_id": "gk-2017-regular-national-2-arts-q17",
  "resume_action": "取得同版可靠勘误，确认是否遗漏了用于唯一确定第17题答案的条件；在此之前保留全部合法分支并将单一答案证据标为 U。",
  "source_id": "src-0a282ae5bb0daabc25cea61ee4d965a48b2fc56a5877a5388d6795a178b22efa",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0955

```json
{
  "affected_paper_ids": [],
  "fingerprint": "c0cc38fb055b6805bacf42ba2d14cdf7a5180e531b8e88f88b44083ed9950b80",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-3-science",
  "question_id": "gk-2017-regular-national-3-science-q20",
  "resume_action": "取得同版可靠勘误，确认是否遗漏了用于唯一确定第20题直线/圆的条件；在此之前保留两组合法解并将单一答案证据标为 U。",
  "source_id": "src-63aac70d1ccb26b495575266a078b3eeebdfa0fbe6e7f05ff309c4a1a6d7775b",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0956

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "d8fc7eab08dacd59fac6e86c5d3b1f46ecb39d063db480fd6943422ad20fbf31",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0957

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "d15601a651897279191a43fa87f790ee9e5716ba99fd57a8a01833e835ef202e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0958

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "5713137b1752810749a57bb11e85fa45aa61824dce3c1eae29ab60f1e762dde2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-2-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0959

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "2606a09ebcec679c58a27e16d8af3674cd2b3ea0c211b51670e78a68f326b8c6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0960

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "6e31202dfb4fe49e33f83fa335a2a02a1c8c2d97415f6aa807d60ce27240d7d2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0961

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "66df70bde52ee9fdc1a5911d21b2d26dbd978d9cdceb6f955b3e79e0e80717b2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2017-regular-national-2-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-0962

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页印刷页 1056 第 17(3) 仅给出直线 NH 与直线 BE 所成角余弦为 √7/21。独立求解、与答案隔离的另一角色盲核及后续仅据固定源的独立复核均得到 AH=1/2 与 AH=8/5 两个棱 PA 上的合法值；未发现附加条件，保留 U。",
  "fingerprint": "fcad0135221dc49854b13263ed16b3ecf7188f31f5be9a8b6ce4eb45263a154a",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-tianjin-science",
  "question_id": "gk-2017-regular-tianjin-science-q17",
  "resume_action": "取得同版官方勘误或可靠来源说明确认是否漏印条件；在此之前保留两值并标 U。",
  "source_id": "src-59000d9a683992059d4ab4804d370738dd2efd09e37ecfa36d726310ff84cfec",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0963

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页印刷页 1056 第 17(3) 的标准非定向直线夹角条件对应两个合法长度 AH=1/2、8/5。不同角色的独立推导一致，来源未指定唯一答案。",
  "fingerprint": "711db9e05d606b2d1b4cd458d91b16f402959ba64aa9372f8dcce774b0ecadeb",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-tianjin-science",
  "question_id": "gk-2017-regular-tianjin-science-q17",
  "resume_action": "获取可追溯的同版答案或勘误；若无勘误，解析保留两解并明确说明原题条件不唯一。",
  "source_id": "src-59000d9a683992059d4ab4804d370738dd2efd09e37ecfa36d726310ff84cfec",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0964

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页印刷页 1056 第 19(2) 令 l 上 P、Q 关于 x 轴对称，但未指定 P、Q 谁在上方。独立盲核确认面积条件允许 AP 斜率 ±√6/2，两条镜像直线均满足题意；候选稿也同时列出，唯一符号无法确定。",
  "fingerprint": "c497db5366860394a14fdcd2a0dbcf4e346f23ad6fdbe8e888beef8466bb9c9c",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-tianjin-science",
  "question_id": "gk-2017-regular-tianjin-science-q19",
  "resume_action": "获取同版官方勘误或可靠来源说明确认是否漏印 P/Q 次序条件；在此之前保留两条镜像直线并标 U。",
  "source_id": "src-59000d9a683992059d4ab4804d370738dd2efd09e37ecfa36d726310ff84cfec",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0965

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页印刷页 1056 第 19(2) 的条件只规定 P、Q 关于 x 轴对称而未指定顺序；独立答案盲核得到 AP 两种镜像直线，无法支持唯一答案。",
  "fingerprint": "2d789b42bdce92dedffae72e2fec6a934eed5031c032e021bbcb4531e7de64f1",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-tianjin-science",
  "question_id": "gk-2017-regular-tianjin-science-q19",
  "resume_action": "获取可追溯的同版答案或勘误；若无勘误，解析列明两条合法直线并说明唯一性无法从原题推出。",
  "source_id": "src-59000d9a683992059d4ab4804d370738dd2efd09e37ecfa36d726310ff84cfec",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0966

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 8 题按棱的正交方向计数为 8；若“垂直”要求线段相交则为 4。固定题面未消歧。",
  "fingerprint": "2decdc6c8cf82d4910d6d8ebdfdce262341459e9d5a0b5654ffd9be86bd7e243",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-arts",
  "question_id": "gk-1985-regular-guangdong-arts-q08",
  "resume_action": "取得同版权威说明或勘误明确“垂直”的计数口径；之前保留两种读法并标 U。",
  "source_id": "src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0967

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 15 题选项 B 的对数底数字形无法由固定扫描可靠辨认；答案不能反推字形。",
  "fingerprint": "c8819d5cc4c98f4f3001e27be159978ef8c2a5813bccbc2c78fb4b2a0b98d73c",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-arts",
  "question_id": "gk-1985-regular-guangdong-arts-q15",
  "resume_action": "取得清晰同版页面或官方勘误确认底数；之前按疑字保留原稿并标 U。",
  "source_id": "src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0968

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 18 题“纯虚数”是否包含 0 会影响选项 D；A 可成立，但单选唯一性取决于术语口径。",
  "fingerprint": "d77250c598f741f2eda221bfcac1d1a81510c25503174ee9b5ebc04478ead628",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-arts",
  "question_id": "gk-1985-regular-guangdong-arts-q18",
  "resume_action": "取得同版术语约定或官方答案说明；之前保留术语歧义并标 U。",
  "source_id": "src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0969

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 21 题二项式指数上标在固定扫描中无法可靠辨认，唯一答案暂为 U/PENDING。",
  "fingerprint": "68f46b0ffd639ab0cb8173b55e89a29dcbb90c5f0ea492121d0c3f01d5d4e82a",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-arts",
  "question_id": "gk-1985-regular-guangdong-arts-q21",
  "resume_action": "取得清晰同版页面或官方勘误确认指数；之前不根据选项或答案推断。",
  "source_id": "src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0970

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 26 题恒等式题未明列正切及分式的共同定义域；解析仅在原式有定义处证明。",
  "fingerprint": "2032558e9d273d076734fcc67225ccf7262e849a71e657badd67ee3911962dea",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-arts",
  "question_id": "gk-1985-regular-guangdong-arts-q26",
  "resume_action": "取得同版可靠勘误/说明确认定义域条件；之前明确限制共同定义域并标 U。",
  "source_id": "src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0971

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 2 题给定 f(1/x) 不能确定 f(0)；规范答案已明确不补造该值。",
  "fingerprint": "a057b9db302ee574a2636c858c06c11507f8cbcf4c6d160851fd5992af5071d4",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-science",
  "question_id": "gk-1985-regular-guangdong-science-q02",
  "resume_action": "取得同版可靠勘误或条件说明；之前保留 f(0) 未定并标 U。",
  "source_id": "src-8dba39a5d57fc6a2b63128db5686a4c8145016f60fe7cde20ec7dc81363d4f08",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0972

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 15 题“纯虚数”是否包含 0 会影响选项 D 与单选唯一性。",
  "fingerprint": "d54b10edb87a9ae3110f1a74c9ec2c8214017c23ce2c207fe0ce725d12f71129",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-science",
  "question_id": "gk-1985-regular-guangdong-science-q15",
  "resume_action": "取得同版术语约定或官方答案说明；之前保留术语歧义并标 U。",
  "source_id": "src-8dba39a5d57fc6a2b63128db5686a4c8145016f60fe7cde20ec7dc81363d4f08",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0973

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第 30 题多个选项的字形疑似“棱柱/棱住”，固定扫描不能可靠确认；不以答案反推。",
  "fingerprint": "804396473b7ac33d031fdb0aa29bf3796fc39943fabe2670497797a7c44f24f3",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-science",
  "question_id": "gk-1985-regular-guangdong-science-q30",
  "resume_action": "取得清晰同版页面或官方勘误确认疑字；之前按原扫描逐字保留疑字并标 U。",
  "source_id": "src-8dba39a5d57fc6a2b63128db5686a4c8145016f60fe7cde20ec7dc81363d4f08",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0974

```json
{
  "affected_paper_ids": [],
  "conflict_code": "missing-answer-table-reference",
  "current_evidence": "固定来源 1985广东理.pdf 的题面说明要求将选项代号填入“下表”，但该 PDF 的题面页未见所指答题表；不从其他版本推补。",
  "fingerprint": "58ddd8e5f4dd3cf6c6bfca4b2335950a3997bdf69221622f15f637b0bf73fa50",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-science",
  "resume_action": "取得可追溯的同版完整原卷或官方说明，核对答题表是否缺页；在此之前保留原题提示并维持该卷未完成。",
  "source_id": "src-8dba39a5d57fc6a2b63128db5686a4c8145016f60fe7cde20ec7dc81363d4f08",
  "status": "open",
  "type": "source-mismatch"
}
```

## ISSUE-0975

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源扫描中的指数上标无法可靠辨认；当前答案稿明确 U/PENDING，未根据选项或原书答案反推指数。",
  "fingerprint": "86a0be2e206e9ff73f053359f02eff85a939cc579389ee799102586b2ed61685",
  "impact": "blocks_completion",
  "paper_id": "gk-1985-regular-guangdong-arts",
  "question_id": "gk-1985-regular-guangdong-arts-q21",
  "resume_action": "取得清晰同版页面或官方勘误确认二项式指数；指数未定前无法确定常数项，保留 U/PENDING。",
  "source_id": "src-282e302363febce2cf53ae86d8ad46dd6ce9786276c5722a3003b19afdcf8986",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0976

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原卷将 C_2 定义为圆，却要求三角形 C_2MN 的面积，未明确定义点 C_2。条件性地把 C_2 解释为圆心可算得面积 1/2，但不作为无条件答案。详见本批 gk-2015-regular-national-1-arts/answer-solve.md 与 issues.md。",
  "fingerprint": "92e6ad533f2449336e97d9f0e266694f3e0e4c622e2f83d8eddc05b2c8b7da21",
  "impact": "blocks_completion",
  "paper_id": "gk-2015-regular-national-1-arts",
  "question_id": "gk-2015-regular-national-1-arts-q23",
  "resume_action": "取得明确勘误或官方说明；此前保留原题记号并将该小问标 U。",
  "source_id": "src-fa40c5849cfb6f67c6864ed4c582abd83879630330c2dee93217e050e7c49d66",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-0977

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原卷将 C_2 定义为圆，却要求三角形 C_2MN 的面积，未明确定义点 C_2。条件性地把 C_2 解释为圆心可算得面积 1/2，但不作为无条件答案。详见本批 gk-2015-regular-national-1-science/answer-solve.md 与 issues.md。",
  "fingerprint": "adf2dcd09b29003fe7191ee7ee474d6a24f82cde14bdbae4ed1972f5e5752d81",
  "impact": "blocks_completion",
  "paper_id": "gk-2015-regular-national-1-science",
  "question_id": "gk-2015-regular-national-1-science-q23",
  "resume_action": "取得明确勘误或官方说明；此前保留原题记号并将该小问标 U。",
  "source_id": "src-cd9ee6484dcd625fc4e7aef0f4253bb8eacaebd8910335eee60f09456695c366",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0978

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f59a2fbd-f3c2-4464-8d61-2f6655926f04",
  "check_code": "heading_number",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "2212d1d86ff1ff0fa0549bb682d0b16fa03438d997d0d8dfc7161c8f9d60fa4c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "4f7e1272266d76dbd1765a51c678ae0b92648bafd49c25337db3befda5478db0",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0979

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f59a2fbd-f3c2-4464-8d61-2f6655926f04",
  "check_code": "heading_number",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "5354b1f095a360b6591013c98f0e6191d6f9388e930c05d2120bdf0874a49eea",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2020-regular-national-1-arts",
  "pdf_sha256": "af51bdc37bd90816a379b87711ded5990f69ca340625cd0092a04b25bf0924fd",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0980

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "cb1826db-41e3-496e-9fb6-8bfa93384f05",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "5c12eecdf96d6e844cfdd6b6eb11a4931b8467ef87523c9abbd9a905f17ff4d5",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 39,
  "paper_id": "gk-2023-regular-new-gaokao-1",
  "pdf_sha256": "b65ac507921be6e45792fd6005aae8195b7ef8014a14001bafee265fec8e73a1",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0981

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0ff60708-7da3-4fa9-84eb-099321b7f3ab",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "42cf49f967b03fbf81b970bbdada64c92daac04853069a1771db4f1abb453977",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 28,
  "paper_id": "gk-2024-regular-new-gaokao-2",
  "pdf_sha256": "d97c843065506fdc44be847e32ff46343157f60780e28221c50d2ed75fbcd035",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0982

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0ff60708-7da3-4fa9-84eb-099321b7f3ab",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "bc4a740a2a4d189b1b9c5c4977ede13818a3b1eca053513c21d3eddccaab7c35",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 29,
  "paper_id": "gk-2024-regular-new-gaokao-2",
  "pdf_sha256": "d97c843065506fdc44be847e32ff46343157f60780e28221c50d2ed75fbcd035",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0983

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "0ff60708-7da3-4fa9-84eb-099321b7f3ab",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "c3c6ae9eda669e129e4df2f42c2a679a16fd2aa6b9ae0bca98589ac893690ebb",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 40,
  "paper_id": "gk-2024-regular-new-gaokao-2",
  "pdf_sha256": "3869e2f91a4da0cd0cff72929718b5b519fbf63552ed7672c49fc3578647f1e9",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0984

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "7e5dc6f0-f4a8-4497-9ef2-d3dd563180b6",
  "check_code": "option_formula_alignment",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "94904600f9cfc02b1285ad9ee54810472963c56cd899561f19186ace04bdc784",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-2026-regular-national-1-recall",
  "pdf_sha256": "f7d7f0385319068e6ef27449aa8f883e314ccef1e11eccec91484f4e3c5bfc1d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0985

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "7e5dc6f0-f4a8-4497-9ef2-d3dd563180b6",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "dd5d60fbdc7417877960185db10f12fc49a79568ff10abc494907627623b0b00",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 39,
  "paper_id": "gk-2026-regular-national-1-recall",
  "pdf_sha256": "490c122a3dd3a972bec60bab5da33538ea44442e25f960c83ed68c82346a3358",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0986

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "7e5dc6f0-f4a8-4497-9ef2-d3dd563180b6",
  "check_code": "option_formula_alignment",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "320730b48cdd9f6d44f48dde590bf67fdb4ee1ee11633beb9a83f7453fb204cd",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-2026-regular-national-1-recall",
  "pdf_sha256": "e4c8269e0b6fe9987380581220dffcca95806336d14ef3cbd968d8bade4d5fa5",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0987

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1cd7e19b-c4fd-47fa-b476-68dd995e953a",
  "check_code": "heading_number",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "1f1a2ea8373cba68099ef2b700ad8095533d9cab6a1ae5e083abef7aa67e9fa3",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-2017-regular-national-2-arts",
  "pdf_sha256": "c1f0db9db13a894ab35a573832eff0e80b89ef4af819bd5d12894ae1cc597603",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0988

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1cd7e19b-c4fd-47fa-b476-68dd995e953a",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "08ca70e357deae3d74790d3afe7d0f091f63fae6a33df92d94e1c9e396c355b1",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 15,
  "paper_id": "gk-2017-regular-national-2-arts",
  "pdf_sha256": "03887093df148457218a28493dcef10dbbf0a2d4587be1bc19ad1c89eda5e279",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0989

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4da13d0b-2276-48d2-92bc-dcc0cb7242ba",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "d8f8ca33236036d7393a95f25f1e973b13a22414aebfc293fc915169661f6f0d",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 14,
  "paper_id": "gk-2017-regular-national-2-science",
  "pdf_sha256": "fd1f6bfd4939ac36fb8debbd40667314c755fbcd0e9c21c38aaaa17f729a0ea7",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0990

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2df0ba3e-7972-4900-aa16-ab40330c082e",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "9672355fe7f0e9667ac4291fa7b24eb94765b5b8e8c5e46354e724d7eaa35774",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 17,
  "paper_id": "gk-2017-regular-national-3-arts",
  "pdf_sha256": "91f1b0c1043bf6905f80f2f406be8ebfc6aef8dcdff50cdb63196a18a702873a",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0991

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "17baf347-1c04-4a6d-95ac-0cd61fdb0d1d",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "cceeba585808c5c7b7d230c3adfadcce27b2b663a50c10a8bf17e428ea0f42ea",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 16,
  "paper_id": "gk-2017-regular-national-3-science",
  "pdf_sha256": "3d303249bfc7ceea9dce66e1424dcea812d0ca55c157cefc6340b65ed561e028",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-0992

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "40885311-f768-42a7-b173-20967856b1f1",
  "check_code": "answer_leak",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "09673aed3a2953b98b59d83a95ad1cc0dfc1646d51a3811d8fbf029c9c0ccee5",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-2017-regular-tianjin-science",
  "pdf_sha256": "27d7529f003362dcc8c8582d81fd4f6399818bc0a9ea921dcec2f54a199886ae",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0993

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "10f3d56c-2972-4f82-a90f-1b3421e98811",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "3100e0f3dce484407bfc5006fc1b48b1f5c62dd63c6f084b511f24e660a55ae9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 12,
  "paper_id": "gk-2023-regular-national-a-science",
  "pdf_sha256": "d64c9bfa698472631f2c6c3150b3aefce94ed3de6ed0bc423a42f33cb4364cca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0994

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "10f3d56c-2972-4f82-a90f-1b3421e98811",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "a2e6b2c93d1ae89f9ea73b4dd5616c7d5380f76e24776c946888d1dc4609cfea",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 21,
  "paper_id": "gk-2023-regular-national-a-science",
  "pdf_sha256": "d64c9bfa698472631f2c6c3150b3aefce94ed3de6ed0bc423a42f33cb4364cca",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0995

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e495702f-7c73-4cae-9df9-98cc8b555ac6",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "fce9d21503dfbc450e1c44f4a510341c989f3ea78a17b3fe2cda420a78f3e958",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 15,
  "paper_id": "gk-2023-regular-national-b-arts",
  "pdf_sha256": "79f62f17eb7956c2d2150da645abab12d6eaaf233449c480d04ede45435b9869",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0996

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e495702f-7c73-4cae-9df9-98cc8b555ac6",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "835b542a99c835781eb4f2a2a6bbcd23b5ba10f06be740db07c2f375fc104bc1",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 16,
  "paper_id": "gk-2023-regular-national-b-arts",
  "pdf_sha256": "79f62f17eb7956c2d2150da645abab12d6eaaf233449c480d04ede45435b9869",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0997

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e495702f-7c73-4cae-9df9-98cc8b555ac6",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "0684ee72371048be0b5099d5755e4dfd6115f191b523c75611a851c2e87c4d82",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-2023-regular-national-b-arts",
  "pdf_sha256": "22987923bb0bc0807ab887e5577a5ff0c360c7ecdca008a1f74adda87bc013b9",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-0999

```json
{
  "affected_paper_ids": [],
  "fingerprint": "1801af7d7ff39133cc25ee791ebf658d44a0e3e45dd65fabc1ac5446678133f6",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-3-arts",
  "question_id": "gk-2016-regular-national-3-arts-q12",
  "resume_action": "原题允许 M=F、E=O，离心率任意；补充 E≠O 时才得到 e=1/3（选 A）。保留原题和 U；须取得来源勘误或明确的非退化约定后才可消除唯一性问题。",
  "source_id": "src-7b7f83ac42bfac1eb17a01ffcbd1dfe8b661bd4e91d6eaa50dbac5c98fe023d0",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-1000

```json
{
  "affected_paper_ids": [],
  "fingerprint": "adb6ce9e76e65abcbf6c036cc5ac25e078423b07ba51769f212c5792fb58c08a",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-national-3-science",
  "question_id": "gk-2016-regular-national-3-science-q11",
  "resume_action": "原题允许 M=F、E=O，离心率任意；补充 E≠O 时才得到 e=1/3（选 A）。保留原题和 U；须取得来源勘误或明确的非退化约定后才可消除唯一性问题。",
  "source_id": "src-556d9ea992950bcd4952763e72a15a168bfe8a1928e42bf5d71bd2ddbacd3fe1",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-0998

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e495702f-7c73-4cae-9df9-98cc8b555ac6",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "721d50b73d3a8218ee5cd2e267cfdd11623cfb0c54cf64620fd46ab8429066ce",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-2023-regular-national-b-arts",
  "pdf_sha256": "22987923bb0bc0807ab887e5577a5ff0c360c7ecdca008a1f74adda87bc013b9",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1001

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "69b6eb58760ada157e5cef34e95fe349a33d65cd00c29b28e9aedd9bb317528c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1002

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "a193d212c36fbaec6d0c188ec3e0482b8abbde07a978aac519ae2fa61e844c41",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1003

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8672d27d4a421f2ee1f101a198f38f46aa079dbc571daeec2e6992b276db2f8a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1004

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "fc4c8fe038a666763a1c9bb1fc24f1da8a8a0e30d6d18e34dc0a871994ee9431",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1005

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第8题题面未给跳绳决赛人数。反例 a=55,b=50，跳绳前7名为3、6、7、10、1、5、4号，与跳远前8名重合6人，而9号不入选。D仅在补充两项目决赛均8人的条件下成立。2026-11-02复查发现中国教育在线的2016试题页及答案页（https://gaokao.eol.cn/shiti/zhenti/201606/t20160607_1409236.shtml；https://gaokao.eol.cn/shiti/zhenti/201606/t20160607_1409440.shtml）仅作媒体分发线索；Google索引另可下载一份第三方托管的7页题目与答案PDF（https://download.s21i.co99.net/17094505/0/0/ABUIABA9GAAggrKh6QUoyrXD4wQ.pdf?f=YKT%EF%BC%88%E6%96%87%E6%95%B0%EF%BC%892016%E5%B9%B4%E5%8C%97%E4%BA%AC%E5%B8%82%E9%AB%98%E8%80%83%E6%96%87%E7%A7%91%E6%95%B0%E5%AD%A6%E8%AF%95%E9%A2%98%E5%8F%8A%E7%AD%94%E6%A1%88.pdf&v=1562925314），SHA-256 8b6b9cd176310db003814475d8aa5d98a127821087aa5d8e725afa4ca4c98580；PDF元数据作者为 ran.ping、Creator 为 WPS 文字、创建日期为2019-07-12。该副本答案键1—8为 C、A、B、D、C、B、C、B，第8题列B；其题面仍未写跳绳决赛人数，且无考试机构发布链或勘误说明，不能补足条件或认证为官方答案。该非官方答案与在“两项目各8人”假设下得到的D不一致，答案继续待核。 2026-11-02进一步核验北京教育考试院网站北京考试报高考版的两篇2016-06-15官方分析归档：《2016年高考数学北京卷试题解析》（原页面 https://www.bjeea.cn/html/ksb/gaozhaozhuanban/2016/0615/62330.html；可读存档 https://web.archive.org/web/20240625175311/https://www.bjeea.cn/html/ksb/gaozhaozhuanban/2016/0615/62330.html）只概括文科第8题以运动会成绩分析为背景；《对数学卷（文、理科）的初步分析》（原页面 https://www.bjeea.cn/html/ksb/gaozhaozhuanban/2016/0615/62329.html；可读存档 https://web.archive.org/web/20240625175319/https://www.bjeea.cn/html/ksb/gaozhaozhuanban/2016/0615/62329.html）将文科第8题描述为运动会成绩读表题。两篇均未补充跳绳决赛人数或列出该题答案，不能据此裁定 B/D；官方站内关键词检索“2016年北京高考数学文科”显示暂无内容。 2026-11-02 Chrome CDP 补充发现性查询：Google 对精确短语 site:bjeea.cn \"学生进入30 秒跳绳决赛\" 无结果，对 site:web.archive.org/web/ site:bjeea.cn 2016 北京 数学 文科 试题 组合亦未返回可用档案线索；普通精确题干查询仍只见第三方 PDF 与二手解析。搜索引擎无结果不证明材料不存在，且不作为官方证据；本轮未取得原卷或勘误，故 B/D 冲突、答案 U / needs-review 与本 issue blocker 状态不变。互联网档案馆 CDX 对北京考试院高考版 2016 年 6 月 URL 的目录查询（https://web.archive.org/cdx/search/cdx?url=www.bjeea.cn%2Fhtml%2Fksb%2Fgaozhaozhuanban%2F2016%2F06%2A&output=json&fl=original,timestamp,statuscode&filter=statuscode%3A200&collapse=urlkey）列出 2016-06-15 的 23 篇归档文章；逐篇查看标题与正文后，数学相关内容仅为已知的 62329、62330 两篇官方分析，无原卷、答案键或勘误。对 2016-06-22 的 27 篇归档文章定向匹配“跳绳、30秒、第8题、第八题、数学北京卷、勘误、试题答案”未命中。该范围检索未发现更正线索，不证明官方材料不存在；故 B/D 冲突、答案 U / needs-review 与 blocker 状态不变。",
  "fingerprint": "f4d63b3066e0ac6c09d9680121c3dc79afae777ca84ccb92058d15981337a0f3",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-beijing-arts",
  "question_id": "gk-2016-regular-beijing-arts-q08",
  "resume_action": "核验官方原卷或勘误中跳绳决赛名额；在此之前第8题答案按needs-review处理。",
  "source_id": "src-ecf09b64f30a39442d38dc7cc78ae41e3b5138c23a4ddb059f098ac5816543bf",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-1006

```json
{
  "affected_paper_ids": [],
  "current_evidence": "已按公开解析的古典概型解读并独立复算：每人从6种组合独立等可能选择，共36个有序结果、6个相同，概率1/6。百度题库的同题解析将其按古典概型处理（https://tiku.baidu.com/tikupc/chapterdetail/57bb913143323968011c9248-51-5-knowpoint），GaokaoHub题页给出1/6（https://gaokaohub.com/paper/2016-shanghai-wen-math.html）。原卷仍不附答案；两者均非考试院答案原件，故只确认通常模型/预期解，不标为官方答案。",
  "fingerprint": "6ac0d27b550ba3fcec06155060a390817b20be4255c8bcc3c34f8d2ce02f207c",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-shanghai-arts",
  "question_id": "gk-2016-regular-shanghai-arts-q11",
  "resume_action": "结案但保留非官方属性；若取得考试院参考答案，再补充官方来源，不改原卷题面。",
  "source_id": "src-ef0138abbecb25086fbdd068f074763b3b155e173f33462156d89059fbad582d",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-1007

```json
{
  "affected_paper_ids": [],
  "current_evidence": "已按公开解析的古典概型解读并独立精确复算：28个无序顶点对中有5对使P严格落在第一象限，概率5/28。GaokaoHub同题解析列出28个基本事件与5个有利事件（https://gaokaohub.com/q/item/36314608064002.html）；同题解析卷逐项列出5对（Scribd用户上传：https://www.scribd.com/document/926308400/2016%E5%B9%B4%E4%B8%8A%E6%B5%B7%E9%AB%98%E8%80%83%E7%90%86%E7%A7%91%E6%95%B0%E5%AD%A6%E7%9C%9F%E9%A2%98-%E8%A7%A3%E6%9E%90%E5%8D%B7）。原卷仍不附答案；这些均非考试院答案原件，只确认通常解读，不标为官方答案。",
  "fingerprint": "6cf5bfc3f13ac8a7a080a73d9f461829fb5e438edc9471dbca26cbadef54182a",
  "impact": "blocks_completion",
  "paper_id": "gk-2016-regular-shanghai-science",
  "question_id": "gk-2016-regular-shanghai-science-q14",
  "resume_action": "结案但保留非官方属性；若取得考试院参考答案，再补充官方来源，不改原卷题面。",
  "source_id": "src-c7e426f42297f5bf556e490676dabce8a95bff5bcdf56a106f471c95cdb591ae",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-1008

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "c4d65b1e0c35ab5b37660286aa4d352d865f80b8b03e57b6a91a9ddf40b3d988",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1009

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "1c568c4e7e2a674728eab5ea1785b3e30877b44b0507aff52a1e8bba96a22293",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1010

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8dc9b997484911db43b4391bce28de3675d92eed7a175fb9566d6200da6af674",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1011

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "93bfe2752db945e8497f9c893de8a1e1323d29216372cf3d4b6760950c12db5f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1012

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "c92ceefa0e61f650dfb487b54412b057b5534104f34f46adf34ca961deeaafb9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1013

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "f931486952f3f44eb95d5d3c4c4dfe3c9622284a49a36957026cf0a74ada39e9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1014

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "7ef181cfed45666aa5df8606826d94bd280d1972ccaab494ef4501e636c0874f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1015

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "c844d52c3561899ca5ac6c66bb545460e2b3b880588d7b2a3cde9e6f86457632",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2016-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1016

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "bd1af74b2a2d0933fc2072e24ce1a52e9becccb0afb97b9eeb0597bfe72e1169",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1017

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "2f3c6d9947d6f4c28ef4fcf0f05cfbaa1c44c5c56ae70cd49c4f7a365d1e6ea6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1018

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "c13113e3c7db2731920ec1abb60dfdd401b8ba9072d2b34a6fde364474e6eae6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1019

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "5f2698bc20277ee8c9682f3d07ad2852ceddc7d4d79eef8cecfc009d15e03dbc",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1020

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "af382c5b59ce9a5f096a40e03beb2635d1f176b5fe6ed46e627f074bcafbb548",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1021

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "d46dc84bfea87c1ec75eae3f8ef160cae661b089ddc966edf9a248e8cf9e61b4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1022

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8eb8a38e0d44517f0fbb910d858524f04b1dda29f884d16a500acf55b0e84501",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1023

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "80a5c5bcfe67dfa11e4c92fc3398c12893efd67d04d81d76fc299323affe0c51",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1024

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "762c5dc7ba169647f2490f22d12223abcc746fff964bd69bc7d338c38f397574",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1025

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "8b551e15a1ed674b65db6c15b93ab68a96488cc36776aee979eda138f24bcc1d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1026

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "893319d1b5f79a7e738af9d11456b444b1a508f0b3c3a2a6a7e7389b760ab2fb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1027

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "6ced2c3fa8d659b88c21d9add9bedc68d614ecb54a385a00ec1cb76b1140ca89",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1028

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "c4a26dcffcbe017e4d14c6c947d26bf4a01f2d6e39214220c4a4ab294880894b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1029

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "cec843fd4ece92b546d13a12c54b68c80ffc47f76a649fac903090fbebe18bd7",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1030

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "a8b1e91a7dab6ce6c91fcaa1cc390c6ae8d54b6a8775851219e76e383b2dbbed",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1031

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "455cc6a7c47b8e512db24cc929ebf6ba3ad93189581729bab04160f36e0281c8",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1032

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "1651f6bead92045e459bb5b4799cfddc913f59ddc03fa9474984d837795df014",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1033

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "4b292e4c056fcc05bb192e23248c4701dc403361b6c40f50f5d2aaf74c99aa64",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-sichuan-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1034

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "8a6c81bee83d1aeb84cdf83a8307edfedf5a77b32cd546cc3c052358d8ba9adc",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shandong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1035

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "302ed1c7bbcca4b028b7d1076d16ec1e0d344f3e9523927553eea9692fb9ab59",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shandong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1036

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "b4949e50aa995ed40b31a0f769acb7cfcdeeeb062842c7862fd4279d9f3b9a67",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shandong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1037

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "13356ee7c095e2db0cfd9999d3f325622cc6230334e4f9a30a236278170c90e3",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2015-regular-shandong-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1038

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 3 页第二大题第（8）小题答案为 7。旧解析分母写作 cosθ−sinθ，却按 sinθ−cosθ 代入并得 7；现已按余切差角恒等式改正，分母与代入一致且结果为 7。",
  "fingerprint": "682fa6fefff14b55e971528b27b9dec00fb1559a31e0639679244886add4b02e",
  "impact": "non_blocking",
  "paper_id": "gk-1986-regular-shanghai-science",
  "question_id": "gk-1986-regular-shanghai-science-q02",
  "resume_action": "已按固定源答案表及余切差角恒等式更正；未来改动时重新核对符号与代入。",
  "source_id": "src-194e8e0291756d4efe602fdad56cd93f41da514be669a940d5510dedcc6bc2f4",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-1039

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "c17334dd6465d2c3e761e17af461cbb7da6df72864e0f81dce6dd309cfc45cdc",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "aeb3ea362ba465dfbef4e42f9c7748f06ef43acec5169c751822e8af260e6fe0",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1040

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "50cbe5be3aa8136eb1c4f3bc8f65283e9393000e0d90e901750f7de995c8c3e3",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "aeb3ea362ba465dfbef4e42f9c7748f06ef43acec5169c751822e8af260e6fe0",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1041

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "3949a27e80f85124cba257c1c39ead6ff9f95470fb7b9d022bd4f39e45e0d332",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 10,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "aeb3ea362ba465dfbef4e42f9c7748f06ef43acec5169c751822e8af260e6fe0",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1042

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "0cbf0c1e135bc4a05f0a136c18ca4fe0543bea1630a5d0403c1591a21cf18164",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 15,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "aeb3ea362ba465dfbef4e42f9c7748f06ef43acec5169c751822e8af260e6fe0",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1043

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "4ad353cffa91d1a55a61251d682147a84f2671b8b2e43a721bd7e2af2df185df",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "576152ece96ad04842efd7965a3c9e3ba24dc03cc53c3e90ba9e54362a3e4285",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1044

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "glyph",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "a68d895064f70c20a3ba20eb29a8cb7a2e3b4a314ab89da7ae11da379b1d6ccc",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "576152ece96ad04842efd7965a3c9e3ba24dc03cc53c3e90ba9e54362a3e4285",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1045

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "7f0f08b1e8bf1f11a9ec0cee1fe383f108323e995659d0cc0045753f33cba36b",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "e6457a7ef9058ada306823c54ff1c52cdfda7014c2ad6ceaedcd64879d30d411",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1046

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "ef62af2ff0a6507adaa80b4fb1cb8ff0f9b268fccec0dae542863620cb256b03",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "e6457a7ef9058ada306823c54ff1c52cdfda7014c2ad6ceaedcd64879d30d411",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1047

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "afb6f0fad941fb22e81d44e127c07cc8823d4c24f76bed6e266bac088a142524",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 12,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "e6457a7ef9058ada306823c54ff1c52cdfda7014c2ad6ceaedcd64879d30d411",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1048

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "a96b37be2f15025b22bc23f248d23b913c3330dae42c12bb6dc031f7af026b9d",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 19,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "e6457a7ef9058ada306823c54ff1c52cdfda7014c2ad6ceaedcd64879d30d411",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1049

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "d746d0decda63ea2bf3997c1eaee9fd4c8607ae13519b211752904dcdece35f7",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "8bed6d20ae20fd6d6bdd70f79cb25624ab0ab5481c3f8761dae755aad1730826",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1050

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "adabd0f9-5ce7-4764-9373-6583a64ea098",
  "check_code": "glyph",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "6cd29832eb8cbad126b896fa962e6f35c3272a06e9fb1245646f5e1769e44e7c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "8bed6d20ae20fd6d6bdd70f79cb25624ab0ab5481c3f8761dae755aad1730826",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1051

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "82cfd59c-7c07-40ea-bb71-438a59b57801",
  "check_code": "answer_leak",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "ba07a1d35446713218f019541e42452f2b47430b5d6b86019feb92bc93d1117f",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-1986-regular-shanghai-arts",
  "pdf_sha256": "c8b77ff26bbd33c426b663bf2e917a9535596f45b1d58b3bc99381aac38480f1",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1052

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "dea4108d-f233-4641-8050-e2fac5986bb0",
  "check_code": "answer_leak",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "df018694875302c8005e0c1249bd5ce7db9c29338b92826854a064f3c836e393",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-1986-regular-shanghai-science",
  "pdf_sha256": "0ed683d124d852036fbb73af67f4757ceb3948e7074b7af90ec9ecdb92877204",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1053

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页第 1(8) 题五个选项中的运算连接符呈不可辨识方框，限页文本层为私用区字形 U+F067；从题意可独立算得选法数 2156，但不能据数学结构确认原印符号或唯一选项字母。若相关方框均为乘号，E 与结果相符。题面与答案均保留缺字，不补猜。",
  "fingerprint": "eb0204962f69f9af9bd7c28407f534eb4a242455768632e22cd3d53742ab1c50",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q01-(8)",
  "resume_action": "取得可辨识同版题面或权威勘误，确认选择式连接符；在此之前保留缺字方框、计数 2156 与条件式选项映射。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1054

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 2 页第 1(9) 题排列数表达式中的连接符呈不可辨识方框，限页文本层为私用区字形 U+F067；由节目排序条件可独立算得 5!P_5^3=7200，但不能据数学结构确认原印符号或唯一选项字母。若 C 中方框为乘号，C 与结果相符。题面与答案均保留缺字，不补猜。",
  "fingerprint": "aa9dbcf0ad0d731aa8232ca043035516795d173434b560fc50dc20191da27c62",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q01-(9)",
  "resume_action": "取得可辨识同版题面或权威勘误，确认排列数连接符；在此之前保留缺字方框、计数 7200 与条件式选项映射。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1055

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 3 页第 1(20) 题写作‘点 P 到三角形的三条边的距离相等’。若边指闭线段，独立论证支持投影为内心；若指三边所在直线，旁心反例使 E 不成立，且 A—D 也均非普遍成立。原题没有进一步限定，故不能在两种读法间擅自选择。",
  "fingerprint": "bec9042df73beddfe34833035cce5072a3e51ce08478960a2c8c076e2f43755c",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q01-(20)",
  "resume_action": "取得同版清晰题面、权威解答或勘误，确认‘三条边的距离’指线段还是所在直线；在此之前保留原题和两种读法的条件结论。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1056

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第一卷选择题组 q01 的独立复核确认：子题 8、9 的源连接符不可辨，子题 20 的‘三条边’存在会改变答案的几何语义分歧，子题 25 的图形选项缺失。故答案结论组仍有未解决冲突；具体证据分别见 ISSUE-1053、ISSUE-1054、ISSUE-1055、ISSUE-0778、ISSUE-0797。",
  "fingerprint": "89407570267f2e41219099fda6657e600a5fdb8320532f388b93623893900a51",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q01",
  "resume_action": "分别取得 q01(8)、q01(9) 的可辨识同版符号、q01(20) 的可靠语义说明，以及 q01(25) 的同版选项图；完成逐子题核验后再解除整题组冲突状态。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1057

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "cb0b202acf3b7b69341b3672526a5189228db847ec96a2ababfe876a2bf246fc",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "3e8c4ddfef6dcbb205cd3ca10dc3c8e93522210f930c575d3ff412fc3664e50a",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1058

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "6aacd9729ec12ca907855037301d99cfbde0583938243d61c04ed3aa6d66cc35",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "3e8c4ddfef6dcbb205cd3ca10dc3c8e93522210f930c575d3ff412fc3664e50a",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1059

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "glyph",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "9e25e900913a0bbd5c969a33d58fb68b638fd33defed381b6df436c5913a6906",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "b61e2b892efd5a6a3c9b06fb993c005910ee4d9e62c603aeea1ada9661c4046d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1060

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "824d0b3773ad808cd7ce4c35443f30068c9832482dcb80b3d7fd4833dbb8fe34",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "b61e2b892efd5a6a3c9b06fb993c005910ee4d9e62c603aeea1ada9661c4046d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1061

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "2c19c9f53916925c8d942120df3cc773549a3f9f459c3b2aacf854721ebf2116",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "57e78223c9d27d5535d6afbb90626bef7e6c5aa4c14193461ca8ed12a37d3406",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1062

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "f5b3f608ec36a10978cf2abd3026a9e97b71260b57d16b01d36e7ca819984150",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "57e78223c9d27d5535d6afbb90626bef7e6c5aa4c14193461ca8ed12a37d3406",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1063

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "glyph",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "3d43954d71c28418ca71e9fee681c8cce457a5c72628f0f7536aa5e0550f6003",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "30c259aa46a2d653cfb5231b6c3ba049c52e30030adbead9927ab3d042fb7a64",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1064

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4282128a-6c7e-4b68-ab5d-6ac670b3a70c",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "d2d4a5114002067d040aa7a09959cc3a17f65622c0ada9990acc14dbb8f637fa",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "30c259aa46a2d653cfb5231b6c3ba049c52e30030adbead9927ab3d042fb7a64",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1065

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立核源（2026-11-09，.work/verify/1987-national-science.md）：固定源仅题面；由下底周长 30、上底周长 12 得边长 10、4，三侧面梯形面积和 21l，两底面积差 √3/4·(10²−4²)=21√3，故 l=√3 cm；apothem 差恰为 √3 说明原题数据几何退化但解唯一。已把答案要点速查表与分题答案、含解析中的 3π 改为 √3 cm。",
  "fingerprint": "b4fe160c16c4b3919b84809194e242ef288686ccf18f13bc892458bbdf23a574",
  "impact": "blocks_completion",
  "paper_id": "gk-1987-regular-national-science",
  "question_id": "gk-1987-regular-national-science-q15",
  "resume_action": "已按独立复算订正答案要点、含解析与短答生成链；若日后取得官方答案页可再比对。",
  "source_id": "src-1027abd4ab36c6d3535d5370b4fa98af66ccd38c7dbd2cc91c43a06b1154cff0",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-1066

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e42f95a0-326c-4b2e-9241-82d16c23c3a9",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "11a5d524dc36f8fe2b6551871c53c626ffa1a0fcdee5c5fcb09117c5edaf610c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1987-regular-national-science",
  "pdf_sha256": "abc0306391322198e9887410281cf596c6dabf3840883a48fde1de133f246ced",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1067

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e42f95a0-326c-4b2e-9241-82d16c23c3a9",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "664118a63cfa0f130f8879f74d5edb037b876dae0273fa2d9c213f29637ae6d3",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1987-regular-national-science",
  "pdf_sha256": "30e7ce282687332532bbd22dfa0347e1afea03ba973eb264deba91b6bd3da9f4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1068

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e42f95a0-326c-4b2e-9241-82d16c23c3a9",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "3b532759f7c11fcde9865764b33dfb1e95b50cb5500f14f0b6cec85c544fcd28",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1987-regular-national-science",
  "pdf_sha256": "51fc501200e0b436a24996d6c08417d8715831c963ebfab0f02cddb6dc216a52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1069

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "e42f95a0-326c-4b2e-9241-82d16c23c3a9",
  "check_code": "pagination_whitespace",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "f04ae94447b3cf1aa6e3e9fbf77cf39f41a931b4eb9b4aa8cb45fc172e6925a2",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1987-regular-national-science",
  "pdf_sha256": "b24b7ea36d8d6b0a53ed35139ee582e73d57ace8d3729a09954f2763a551f117",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1070

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原卷PDF第2页第12题题干指向函数图象，但对应图位为空白；第5页答案表印B仅为来源记录，因题图缺失而不能独立核验。",
  "fingerprint": "cd14b529d21b4d7aaa9cabec5a3ecf10feebb0b452a371dfe1d21dc202636354",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-guangdong-science",
  "question_id": "gk-1990-regular-guangdong-science-q12",
  "resume_action": "取得可核验的同版完整题图或独立同版来源后复核题意与答案；不得凭模型记忆重建图形。",
  "source_id": "src-30b33e839ac3b04ec001587e1f600129eccb6a4b8ca3cc7a4c5ce79a5a205d5a",
  "status": "open",
  "type": "figure-missing"
}
```

## ISSUE-1071

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描件附载第25题分段定义域为t>0，第一支仅覆盖0<t<1/2，第二支写t≥2，区间[1/2,2)未被原印载分段覆盖。独立复核者仅获题面裁剪图、未见印载解答及主会话推导，独立得到项目分段面积与单调区间；项目答案已注明为非官方推导并保留印载原文。全26题逐题局部复核已完成，但来源差异仍在、出版者身份未认证，故本 issue 与整卷 blocker 保持开放；正式provenance、编译及视觉验收状态见项目回执。",
  "fingerprint": "49bf094c939ffb965fcc1d872220956a66c0b3a282c3f6a0f3d227cea7a79da4",
  "impact": "blocks_completion",
  "paper_id": "gk-1994-shanghai",
  "question_id": "gk-1994-shanghai-q25",
  "resume_action": "继续正式provenance、四版构建与视觉回执流程，不重复已完成的26题盲核。保留固定来源t≥2原文与[1/2,2)差异记录，不得把项目推导标成官方答案；来源身份与疑误未获可靠裁决前维持blocked。",
  "source_id": "src-175369213dde711e3bba990974dca1216e7e4ef6ed65cbc9e197dc39d81eba65",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1072

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源题面第23(3)两平面名之间缺少关系符号，原件不能判定待证关系。",
  "fingerprint": "18240ff5f5c8f4386b2d7cfc8be6c0c000ffcbb20e527ba438d1dc5c9794b735",
  "impact": "blocks_completion",
  "paper_id": "gk-1997-regular-national-science",
  "question_id": "gk-1997-regular-national-science-q23",
  "resume_action": "取得独立同版题面或权威勘误；此前保留缺符号并维持阻断。",
  "source_id": "src-930ed190601053d47a6c2d72d9d2185d4d734e0e92462e66ace578b294dbe9db",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1073

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面待证关系未知；既有垂直证明仅为条件推论，不足以核验原题答案。",
  "fingerprint": "9244ba108c2764eae3e1d3313161fb19b9087ebea2e09ab7209031afd10921a7",
  "impact": "blocks_completion",
  "paper_id": "gk-1997-regular-national-science",
  "question_id": "gk-1997-regular-national-science-q23",
  "resume_action": "确认第23(3)待证关系后重新求解并独立复核；不得把条件性垂直证明当作原题答案。",
  "source_id": "src-930ed190601053d47a6c2d72d9d2185d4d734e0e92462e66ace578b294dbe9db",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1074

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "a374ef25-7f08-4983-a2cc-b330cd6274ce",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "bbb456a41100a61fb7cdfddfc828cfc6ea4ff00c6f5365f3ca00cbdb231b9949",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1989-regular-national-arts",
  "pdf_sha256": "0372a7f7a816b205d8d877df49810c653d1685cf5059b76476e6158c3e7b59d4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1075

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "a374ef25-7f08-4983-a2cc-b330cd6274ce",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "102f1374ae5b76d43eb40f5a79b972912eab6df31e95d0913841f28aff0e15c7",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1989-regular-national-arts",
  "pdf_sha256": "0372a7f7a816b205d8d877df49810c653d1685cf5059b76476e6158c3e7b59d4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1076

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "a374ef25-7f08-4983-a2cc-b330cd6274ce",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "031c6ed6128a65064c0d301cc7385441e5c3172c79749e548cc5978bb5c46156",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1989-regular-national-arts",
  "pdf_sha256": "0372a7f7a816b205d8d877df49810c653d1685cf5059b76476e6158c3e7b59d4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1077

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "a374ef25-7f08-4983-a2cc-b330cd6274ce",
  "check_code": "pagination_whitespace",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "f6d74c07b5591e95640456bae82e4cabce10308233269238359877057ae6d82e",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1989-regular-national-arts",
  "pdf_sha256": "b32e714eee425cb6563d1725b3abc1fdf4f16108041c5c82fadb963b80715390",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1078

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定PDF第1页印作‘对称轴对x轴’，仅按‘对称轴为x轴’解释可推出选C；印载B型答案为C但canonical卷型映射未确认，尚无证据消除题干方位歧义。",
  "fingerprint": "cef50dbf1b6a78bedf7a53baf3cddce285f8d24ea823445c8ee2588c00b8b3d3",
  "impact": "blocks_completion",
  "paper_id": "gk-1989-regular-guangdong-science",
  "question_id": "gk-1989-regular-guangdong-science-q08",
  "resume_action": "取得固定来源版本对应说明、同版更清晰题面或权威勘误以确认原句意图；在证据到位前保留原文和条件性答案，不解除阻断。",
  "source_id": "src-db4a50c280ed27fa5f0f5542adec7d7fe605a216210ebbff7165fe4396b75256",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1079

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "81e1897a-a8d0-4a94-8a0f-51f514b86f3b",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "3be951e7d38648baf6c34b00e4f2de9ca2408b1347996adfca0cb7074e1e46d8",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 16,
  "paper_id": "gk-1989-regular-guangdong-science",
  "pdf_sha256": "76d45a603a977b77f44b22101e590ae73b216cda6cc914154b60c4b14563999a",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1080

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "81e1897a-a8d0-4a94-8a0f-51f514b86f3b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "7c35d895cb5a976b5c1157fff8f18d435ccdce08a60c2e3d33a6542514604225",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 24,
  "paper_id": "gk-1989-regular-guangdong-science",
  "pdf_sha256": "d86c90406bc66c703660f65f98fda512cca6c4752504ab36be7f93518e52412f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1081

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "f5ecf4f2-d049-4fca-bc0c-b11fa1e9eefd",
  "check_code": "answer_leak",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "6d9eed2959c9890725fb162f168b83cb19a11082114bc4df3d1b685ce77cb689",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-1986-regular-guangdong-arts",
  "pdf_sha256": "161963734eea4bfcb197df8277f9a4eb0e344b6a23658aa6852a86007e6effe2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1082

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 artifact SHA-256 为 ad1042cc4b8ed8ed08322a37f79995930df446d1c4827c85b96b019cb00cda24（上游路径 普通高考/1986/1986广东理.pdf）；本轮核对 PDF 第4页第2题（2）tgθ 与 secθ 之间、PDF 第5页第2题（9）两个三角函数之间均显示方框字形，扫描图不能确定原运算符。题面分别保留 □，不以答案解释代替源字形。",
  "fingerprint": "d76dfc85115cc1a59976e70c22f19345e5eb17c43f5f5f7eba2ef0fe68576456",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q02",
  "resume_action": "取得清晰同版试题或官方勘误，确认第2题（2）和（9）两处方框的原印运算符；确认前分别保留方框，不把答案页的解释冒充为题面字形。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1083

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 artifact SHA-256 为 ad1042cc4b8ed8ed08322a37f79995930df446d1c4827c85b96b019cb00cda24（上游路径 普通高考/1986/1986广东理.pdf）；本轮核对 PDF 第5页第2题（9），两个三角函数之间显示方框字形，扫描图不能确定原运算符。题面保留 □，不据解题推理还原题面字形。",
  "fingerprint": "4f603dff8adcc57972f4efef47ecfd7b6c7c673a4d23b09a1dfb46cd067f5b27",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q02-(9)",
  "resume_action": "取得清晰同版试题或官方勘误，确认第2题（9）方程中两个三角函数之间的原印运算符；确认前保留方框，不据解题推理还原题面字形。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1084

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 artifact SHA-256 为 ad1042cc4b8ed8ed08322a37f79995930df446d1c4827c85b96b019cb00cda24（上游路径 普通高考/1986/1986广东理.pdf）；本轮核对 PDF 第5页第5题（2），求和恒等式分子中的两个三角函数之间显示方框字形，扫描图不能确定原运算符。此前转录省略了该可见字形，现已补为 □ 并标待核；未据常见恒等式猜写为乘号。",
  "fingerprint": "d1abd2ac6198f4b3d2f443c477171841171cf4ac1df28af4777bfc1931302934",
  "impact": "blocks_completion",
  "paper_id": "gk-1986-regular-guangdong-science",
  "question_id": "gk-1986-regular-guangdong-science-q05",
  "resume_action": "取得清晰同版试题或官方勘误，确认第5题（2）求和恒等式分子中两个三角函数之间的原印运算符；确认前保留方框，不把相邻函数的常见乘积写法当作原字形。",
  "source_id": "src-2a7296b77ab3d2d8a4f48ac252e07d6a11c1aa1cbba19955a355b45fccae9e3e",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1085

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "72e21875-2bfb-401c-bf50-f553d1045486",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "cd9e832c7fbedc234cc70bf9059c6565f015280bc3fb91c05866da4bbe672b64",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "df6ff20ca20d95b60103555b6997cdb4d16c0ad9071215708e58928f76df99a4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1086

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "72e21875-2bfb-401c-bf50-f553d1045486",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "c9da949ff24ddeefb6b9f97c4a2961a3ad9c63fabf570cd8d0c8ae1c7b428639",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "ce31f5b41327c0e348c1d676ca3459979ea32fa12bba0c057c157c0211e9eb65",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1087

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "72e21875-2bfb-401c-bf50-f553d1045486",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "85666285309895f338491f348fcf85d3f41e4ccb0034d4e9308feb7b5f608c12",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "c4e021a487c93124d237c868ea042e427836d94243c1a69e770534a3b7c92595",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1088

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "72e21875-2bfb-401c-bf50-f553d1045486",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "dbf58492cbaa99ea506576fd7de8741e0942eaa99d735285b02557685f35cde9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1986-regular-guangdong-science",
  "pdf_sha256": "fd3940cbc35a356f061c683de23bfe6c99231445ae1b48dec7bc52f2065db790",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1089

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "80860921e587bd507a0b545cbd22733f27b798664ba36888807d7a57f73f3560",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "be6a861df5007dfbbd0c57412c03691601047caf53222bc3449facc5c2fe7561",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1090

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "58e0fd9c2b8624a093396336bf88a4f334a9724f3e16580112dbdb089e742532",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "be6a861df5007dfbbd0c57412c03691601047caf53222bc3449facc5c2fe7561",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1091

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "heading_number",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "29aae28418c09ca0a97b37be2a0297d003033408a3b9ff4c02e4206e78e5d9f7",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "be6a861df5007dfbbd0c57412c03691601047caf53222bc3449facc5c2fe7561",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1092

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "baf0a406a1a00f17b5e4533412e5192ae59400c6c2a8f3f7d5679d7c70669f0e",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "be6a861df5007dfbbd0c57412c03691601047caf53222bc3449facc5c2fe7561",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1093

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "12a9e818e53a47b6452917527bc2ab14cd40d736968bcdb0563fe5265b18c7b6",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 11,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "be6a861df5007dfbbd0c57412c03691601047caf53222bc3449facc5c2fe7561",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1094

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "56b8e410a8ffdd38200b66c6870057dab04b9674c93a893bb2a0950ce5aec8c9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "1387c998560128ae2f7f913b0bbcd6429e25da28045b163472721110e6da8894",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1095

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "eb6ec41188038767fa48c074c65de09950018ea8d161b13abb438cb40cd7907f",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "1387c998560128ae2f7f913b0bbcd6429e25da28045b163472721110e6da8894",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1096

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "heading_number",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "2fb58f0e5852e4c29a9d1d8dc41ec373360cfe845e3be9b0c4a7a4fac3a68baa",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "1387c998560128ae2f7f913b0bbcd6429e25da28045b163472721110e6da8894",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1097

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "f20045c79de2e2a9b5284a66d257df5c339eada697d18be0c168176780bfb5fc",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1098

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "3cb0321dcc962d1b2a59d55b2fa2731ee818ee2cfad86da9c943a831572a38c7",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1099

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "heading_number",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "0e1fe457ef29816276b97d8a676e39906bba912cd67b77b2aef988692f8109cc",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1100

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "fd533373bc5261192a62d3d8e1df59f932fed8cf882c3459f44b5f180fa057b9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 10,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1101

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "fc7718725b030084c0bfc30e647be3ef14715e261ab8185fc2dcb01fda66a437",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 16,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1102

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "heading_number",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "9ffe5189fdb4c7149638532cf789f055176053450d56cf68e9a1dbb2592746f8",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 17,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "a5890d6104e9ebbcd90a692f0cb6e719814acd9fa5b0b4c688ea63f0565c7633",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1103

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "3963dc0e6eaf58eaba191155d065ea5cd5edf1673908367f354a05e5744ac48c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "ccab37f4975d751ab09d5d71309c2c0a070662c771851d82b18ba3f7f6023d6b",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1104

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "7eef3e616ffa9de3ad654fdae6a83738c8271a3df0a0b52af1d158e1d1c16caa",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "ccab37f4975d751ab09d5d71309c2c0a070662c771851d82b18ba3f7f6023d6b",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1105

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "4713a95a-06b4-4399-9bab-c58f428d8b8c",
  "check_code": "heading_number",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "02b986429411c9b0f6ba846381834ea01769a658933bb5b8f7df38a68ad3df90",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1994-shanghai",
  "pdf_sha256": "ccab37f4975d751ab09d5d71309c2c0a070662c771851d82b18ba3f7f6023d6b",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1106

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源第955页明确题干为等比数列但未载入定义或答案页；条件化简得到 q(q-3)=0，两种定义约定会导致Q14答案不同，故暂保留分支。",
  "fingerprint": "f7b8c9ca9c0a90e308df3c3dc7ddb5f2e143764892f3f63ec204d49fe4f692e1",
  "impact": "blocks_completion",
  "paper_id": "gk-2015-regular-hunan-science",
  "question_id": "gk-2015-regular-hunan-science-q14",
  "resume_action": "取得适用于本卷的可追溯定义原页或授权答案后裁定定义约定，并独立复核Q14答案与解析。",
  "source_id": "src-b53d0d464f06084b1f8ca8e0bcc2927b503df76dc31ce0ba00095e9eacb1a4c8",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1107

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "27cc4355f0a3b3eb688204fd89e7773ad29719e1e10ecd91209c7c81c81ef118",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1108

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "015b1662c016336b9674d1578ba2adb0c4f721ab9cb0858c83cc5c442806951b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1109

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "300f7da1e5b76f595bd495b3dc68f366027aa0508e05d97a3ef693fd88f50174",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1110

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "0cd45e96aaf245708f58d98e004511113aecbcf1c4403599fa1095ed007aab32",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1111

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源原页第三个定义仍印 b，而选项使用 c；公开变体（https://ab1962.com/wp-content/uploads/2014/07/1%E3%80%81%E5%A4%A7%E7%BA%B2%E5%87%BD%E6%95%B0.pdf）写 c 但无原卷或勘误出处，不能据此修订题面。",
  "fingerprint": "52dc23ffb3b5d29537b1ab32802281b6cb81a005b388394a55f59d2f18c44ae7",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-shanghai",
  "question_id": "gk-1990-regular-shanghai-q18",
  "resume_action": "取得可回溯的同版书页或勘误，核定原变量及选项后更新转录/条件答案并复核。",
  "source_id": "src-bda5db939e3a48de23ec63fc5992d73c8e4a0e6a0ea39d36a5a81d4adf09a987",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1112

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源原页在点 P 后直接接直线 x=2，未见在；二手教学文章（https://doc.xuehai.net/b411428fbe76059dc788cd795.html）有同结构题并含在字，但无1990上海卷来源链。",
  "fingerprint": "353077e04fba922dd889cf8f25bf956d6c364324e85791ce97362f030d46c663",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-shanghai",
  "question_id": "gk-1990-regular-shanghai-q23",
  "resume_action": "取得带年份卷别或原版书页的直接证据；保留扫描原字直到有证据，之后复核条件性轨迹结论。",
  "source_id": "src-bda5db939e3a48de23ec63fc5992d73c8e4a0e6a0ea39d36a5a81d4adf09a987",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1113

```json
{
  "affected_paper_ids": [],
  "fingerprint": "7fb50c805157093fe162a3f091d46c605c35c7a3ece7fda14cc1cbbdae486d72",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-guangdong-science",
  "question_id": "gk-1990-regular-guangdong-science-q02",
  "resume_action": "核得单选选项仅在A唯一正确，或取得同版勘误/可靠原题说明；在解决前保留原文和印载答案A，不猜改选项。",
  "source_id": "src-30b33e839ac3b04ec001587e1f600129eccb6a4b8ca3cc7a4c5ce79a5a205d5a",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1114

```json
{
  "affected_paper_ids": [],
  "fingerprint": "e80c4f92aa0f94565283868ba9e20ac029dfa0f3f7bf48412ca7243c757e5aed",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-guangdong-science",
  "question_id": "gk-1990-regular-guangdong-science-q12",
  "resume_action": "取得可核验的同版完整题图或独立同版来源后，重新求解第12题；不可把来源表印载B直接当成已验证答案。",
  "source_id": "src-30b33e839ac3b04ec001587e1f600129eccb6a4b8ca3cc7a4c5ce79a5a205d5a",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1115

```json
{
  "affected_paper_ids": [],
  "current_evidence": "复用忽略目录中的第2页和答案表页图；既有进度回执将该缓存关联到此固定来源（SHA-256 c747bff56863a349aa9432b1616630a249cd7668ead997a5bbe1fefa2616f848），本阶段未重新物化原 PDF 或重算 SHA。题面页（印刷页115）第15题印有 A={x|x^2-5x-6>0}、B={x||x-5|<a}、a 为常数且 1∈B；答案及评分标准页第15题印载 D。由 1∈B 仅得 a>4：取 a=5 时 A–D 四项均不成立；取 a=7 时 A、D 两项同时成立。因此题面条件不能保证所印 D 为唯一正确项。",
  "fingerprint": "264f5ed68eae8a3e5bbea694ace76bc5e581fd5c06f6943ec53f05fd048aa2ea",
  "impact": "blocks_completion",
  "paper_id": null,
  "resolved_evidence": "固定来源保持不变：source_id=src-8c86b3e592e594953609fe09d0c182d5252c944006503dfb10e8efa1962aeca7，SHA-256=c747bff56863a349aa9432b1616630a249cd7668ead997a5bbe1fefa2616f848，原登记PDF检查通过。复核既有高分辨率缓存题面印刷页115，原字形明确为11∈B；此前记录为1∈B系漏读一位数字。按原题B=(5-a,5+a)，11∈B推出a>6，进而[-1,6]包含于B，D项唯一成立，与同一固定扫描件答案表D相符。已更正题面转录；未改变源文件、来源身份、paper_id或答案权威等级。",
  "resume_action": "无需动作；固定 blob 已重新验证并物化",
  "source_id": "src-8c86b3e592e594953609fe09d0c182d5252c944006503dfb10e8efa1962aeca7",
  "status": "resolved",
  "type": "source-mismatch"
}
```

## ISSUE-1116

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "3e257c84-5a32-46fb-9ae5-b05ee0ee2f69",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "956fdc7afaebd6a2c2e95c9a8edb997a93dcc101b09ddb96b7a954a11cb67554",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 39,
  "paper_id": "gk-2017-regular-national-1-arts",
  "pdf_sha256": "868ca2c5b9c5f58209bad619afbb76c9a3b43dcce3cd0e361b99d431051bd78a",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1117

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "94c34e71-8564-4ce5-b13d-162fc4cb53ce",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "cdfad2415e9f351ba55131a3d5df30b7aea85bb7b536ab959d3df518bc637e6b",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-2018-regular-national-1-arts",
  "pdf_sha256": "83f4e184a9da17ee47e3de735f00051ee1d9250ceed61acea2eff04ca49ddff8",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1118

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "94c34e71-8564-4ce5-b13d-162fc4cb53ce",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "61d574438efba6dab7c7a4d4fb30d868f75bf0ea5ba6c97d99548d155de38fd4",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-2018-regular-national-1-arts",
  "pdf_sha256": "477c0a02dd01edd16d0dcc72e11620984650d605558e28314a56ad78fcc65cf4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1119

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "94c34e71-8564-4ce5-b13d-162fc4cb53ce",
  "check_code": "pagination_whitespace",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "dd3ef773c160a06be16f7e5d651ceb0145e4b27018c2ef724d292ca8bba33fbb",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 6,
  "paper_id": "gk-2018-regular-national-1-arts",
  "pdf_sha256": "db974b0061f4ebaba2b34825cc412b6ad69128c38b44d6b25007705a4c20ef29",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1120

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "af65a573-ed7b-487d-bb36-e935249c2c30",
  "check_code": "glyph",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "d12e16ca472076b3f9197e93280f0edf937442cc9c86730488d36f1aeccfbe48",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-2015-regular-national-2-science",
  "pdf_sha256": "ba40932629169f12e8c13ca0be2af2c9d9b32f3579454693c13b27b640136322",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1121

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "af65a573-ed7b-487d-bb36-e935249c2c30",
  "check_code": "glyph",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "c9301bab6b2f698e0c042ba931cb629162492b3b73a7926cacf9ded75b35dd1c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2015-regular-national-2-science",
  "pdf_sha256": "c77df24f8e29449678eda2fb9c5de7138905f16d0c4c14b593769a0ab4b196af",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1122

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "af65a573-ed7b-487d-bb36-e935249c2c30",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "74166b985791600435a4d2dff904f62d404e053869cb2e08667871b4025ae29a",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 18,
  "paper_id": "gk-2015-regular-national-2-science",
  "pdf_sha256": "99743cd52563142f81704de26c43462dcc9fd4a329cb7cda2c734b8506a9bc5d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1123

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "af65a573-ed7b-487d-bb36-e935249c2c30",
  "check_code": "glyph",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "11e90e8e7c726a4cda1474c635a4252b6922acd075e290067377b4bda160de1f",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2015-regular-national-2-science",
  "pdf_sha256": "f901d96e238cff72b2e3c7a85a43b7163a95578f59d11f264950fbbb421def58",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1124

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 只有试题页，图中未标出哪部分是 V1 或 V2；几何复算只确定靠 A 一侧与另一侧的体积比为 7:5。答案要点和解析已明确保持待核。",
  "fingerprint": "20014849ae777195b4adc9b76eafb500cdab47d549f69ed0b5bd8b307bb13073",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-national-arts",
  "question_id": "gk-1990-regular-national-arts-q20",
  "resume_action": "取得能明确标示 V1/V2 与两侧对应关系的同版题页、权威答案或勘误；如始终无此证据，则继续保留无序比 7:5，并禁止给出唯一的 V1:V2。",
  "source_id": "src-4d319a8fc41be0c0fa7ce90615870abbabe5c3670150609e3cb0c37944091866",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1125

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定PDF第4页参考答案列(0,3-2√2)，而题面两不同根 r=3/2、s=7/4 给出 f(1)=3/8，超出该上界；独立推导范围为(0,1)。",
  "fingerprint": "7c536c4502d33ab1111445eba3ee06af8f36461dcd85e772f6375a22200615f6",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-spring-shanghai",
  "question_id": "gk-2017-spring-shanghai-q12",
  "resume_action": "查找官方勘误或独立同版原卷/答案以裁定差异；保持编者答案为非官方，不以模型推测改写。",
  "source_id": "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1126

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面 f(x)=(x-1)^2 的单调递增区间为[1,+∞)，应选B；固定PDF第4页参考答案列D（递减区间）。",
  "fingerprint": "b502b91998e2188e43fa3126581a529057d207dc8a2babd84ab3788a9605e0b8",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-spring-shanghai",
  "question_id": "gk-2017-spring-shanghai-q13",
  "resume_action": "取得官方勘误或独立同版答案资料后裁定；未有证据前并列保存题面推导与副本参考答案。",
  "source_id": "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1127

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题干按每米给圆形步道单价，按周长计价的最小总价为84π≈263.9千元；固定PDF第4页列42.0千元，恰未乘2π周长因子。",
  "fingerprint": "b66540305042fe26927ecdd5e713b8b9059a62d08d5b6d486a4291834827f348",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-spring-shanghai",
  "question_id": "gk-2017-spring-shanghai-q19",
  "resume_action": "核查官方勘误或独立同版资料的计价口径；在裁定前保留84π为编者推导、42.0为来源副本记载。",
  "source_id": "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1128

```json
{
  "affected_paper_ids": [],
  "current_evidence": "正八边形与向量 TikZ 草稿已建立并登记，四版本地编译成功；独立复核确认顶点次序和箭头，指出 P 的绘图参数 pos=0.45 必须仅作示意点理解。规范题面及来源图表清单明确该绘制位置不表示题设精确比例。phase4-b12 正式视觉回执（build attempt bc3315cf-facc-4c00-a4e1-c832b5d68e4a）四版本共41页通过；12个含图页的 figure_label 注释现已补录上述图稿语义并引用独立复核/图表清单。",
  "fingerprint": "da73b3e55764c3f6ff5717260d23db961409685d2ed7773a7da09b2d6592ba79",
  "impact": "non_blocking",
  "paper_id": "gk-2017-spring-shanghai",
  "question_id": "gk-2017-spring-shanghai-q16",
  "resume_action": "已关闭：来源图表清单、独立图稿复核及正式四版视觉回执已共同记录 P 仅为示意点；若图稿或来源变更，再重开并复核受影响页面。",
  "source_id": "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9",
  "status": "resolved",
  "type": "figure-missing"
}
```

## ISSUE-1129

```json
{
  "affected_paper_ids": [],
  "current_evidence": "长方体与辅助线 TikZ 草稿已建立并登记；独立复核确认顶点连接、实虚线及辅助线与固定来源相符。来源图表清单及正式 phase4-b12 四版视觉回执记录图形标签/线型清晰，且投影比例仅为示意、不增添几何条件；41页全审通过，回执 build attempt 为 bc3315cf-facc-4c00-a4e1-c832b5d68e4a。",
  "fingerprint": "8ec3c99bdf11741e1410acd5bbc38d99d3e1b40afcd9488d26ec6d248cb601ed",
  "impact": "non_blocking",
  "paper_id": "gk-2017-spring-shanghai",
  "question_id": "gk-2017-spring-shanghai-q17",
  "resume_action": "已关闭：固定来源拓扑、示意比例边界及正式四版视觉检查均已记录；若图稿或来源变更，再重开并复核受影响页面。",
  "source_id": "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9",
  "status": "resolved",
  "type": "figure-missing"
}
```

## ISSUE-1130

```json
{
  "affected_paper_ids": [],
  "current_evidence": "两圆切线 TikZ 草稿已建立并登记；独立复核指出源码中的54°参数易被误读，现已删除θ及三角函数角度参数，改用仅为示意的坐标布局。最终源码/图像独立复核确认无角度参数；来源图表清单与正式 phase4-b12 四版视觉回执均说明示意布局不表示题设未给的角度或半径比例。41页全审通过，build attempt 为 bc3315cf-facc-4c00-a4e1-c832b5d68e4a。",
  "fingerprint": "d9e79b9993d434d7e7c8b1dfe6e8a60d7c66425174b4f525c863720700d8f5db",
  "impact": "non_blocking",
  "paper_id": "gk-2017-spring-shanghai",
  "question_id": "gk-2017-spring-shanghai-q19",
  "resume_action": "已关闭：最终图稿源码复核、来源图表清单和正式四版视觉回执已记录示意坐标及角度不构成题设；若图稿或来源变更，再重开并复核受影响页面。",
  "source_id": "src-480836465b22d00a9a18f0d5cdfe26306df617cbe558553c86a162ef92ea16c9",
  "status": "resolved",
  "type": "figure-missing"
}
```

## ISSUE-1131

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面和图示只能确定靠A侧与其余区域的无序体积比为7:5，未说明V_1、V_2分别对应哪一侧，因此无法核定V_1:V_2的方向。",
  "fingerprint": "47c016d0bfd50b69decd174a3931fdb24bae5f77cc0f3433c88e849ef5ad4b9b",
  "impact": "blocks_completion",
  "paper_id": "gk-1990-regular-national-science",
  "question_id": "gk-1990-regular-national-science-q20",
  "resume_action": "取得同版权威答案、勘误或可核来源，确认V_1、V_2与两侧区域的对应关系后再登记有序比；未解决前保留无序比并维持阻塞。",
  "source_id": "src-9c2fc92cdbbeac0484bf7355db2d32805c316e1a7be74e3bf175a3891a167a49",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1132

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "2e1f8edcaec4d8bd910d0c158f5028bcdcfc74af839de23d02e354eb7bc8016c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1993-old-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1133

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "73fea208535a080cce3ba5f962a779964518222fad89032c02444c8390dcb0d2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1993-old-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1134

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "98d112fb01e7b6b6a265543ed4918cf0dbaad9d4cc26b6cc9f3afcbaaaee5cae",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1993-old-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1135

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "8e519b8b81addbed64de35bbdba4aa4bddefe8e3b34e22cac00c78fb6c62eca2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1993-old-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1136

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第2页Q15 A1写P在直线OA上且OP/PA=1/2，第5页只列B=(4,2)。通常无向距离解释t=1/3或-1，故B=(4,2)或(-12,-6)，缺乏排除外分点的题设。",
  "fingerprint": "7d921a8d5431af1ea7247cd51b5a51b247914942f8ad00c059207856c0165a06",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-shanghai-science",
  "question_id": "gk-1996-regular-shanghai-science-q15",
  "resume_action": "取得同版原始题页、可靠勘误或当年明确有向长度约定后裁定Q15 A1；此前保留源题、印载单解与完整推导两解，整卷保持blocked，不据答案补条件。",
  "source_id": "src-544d6951d540a551546ce474b93c3b9bc08e1863472ea0998f971dd4b619de21",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1137

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第2页写直线OA，OP/PA=1/2；第5页只印B=(4,2)。独立解题得B=(4,2)或(-12,-6)。原ISSUE-1136保留题源约定阻塞，本条明确记录印载答案与完整数学解集的未决冲突，以满足逐题answer-conflict门禁。",
  "fingerprint": "1b46e8099f014f308e909b89c11525436117c6fb22839e252f415ac410520f20",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-shanghai-science",
  "question_id": "gk-1996-regular-shanghai-science-q15",
  "resume_action": "取得同版题面勘误或明确有向距离约定后裁定Q15 A1；来源只列(4,2)，当前无向距离完整解含(-12,-6)，冲突未解决，保持U级与unresolved，不得标完成。",
  "source_id": "src-544d6951d540a551546ce474b93c3b9bc08e1863472ea0998f971dd4b619de21",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1138

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "cc6b426d010647ab2ab8abb5230eda7516376e9e2cb33c9599ed3507e88881bf",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1996-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1139

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "79d5c98108295b4c8b326883adb7b00316b121c763cf7e22abbca1e8c9033475",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1996-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1140

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "895cc26a73d70dea7f57adaf6b806ab5de1d732851ca7974325eff83206b2d3e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1996-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1141

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "94418c6f043a4ac4330f4665ec6c62d311cd5a12e6a3c293885c0183c9e01dd0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1996-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1142

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 2 页 Q15 A1 写 P 在直线 OA 上且 OP/PA=1/2，第 5 页只列 B=(4,2)。通常无向距离解释 t=1/3 或 -1，故 B=(4,2) 或 (-12,-6)，题设未排除外分点。",
  "fingerprint": "028570530cab8b825252454c2c34ed6151c64e798bcad2ca8047c9e3e4f5a82a",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-shanghai-arts",
  "question_id": "gk-1996-regular-shanghai-arts-q15",
  "resume_action": "取得同版原始题页、可靠勘误或当年明确有向长度约定后裁定 Q15 A1；此前保留源题「直线 OA」、印载单解 (4,2) 与完整推导两解，整卷保持 blocked。",
  "source_id": "src-2cd0e37e0e31e5698fdc0f84ba902576f04a18869a73ec0f15565f94f2c0bd35",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1143

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第 2 页写「直线 OA」，OP/PA=1/2；第 5 页只印 B=(4,2)。独立盲解与转录复核均得两解，印载答案与完整数学解集冲突，保持 U 级与 unresolved。",
  "fingerprint": "0c9fdfd08b8c8cd6be3deb17f3ae2875852d2862a149123611a3d182351d0fbe",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-shanghai-arts",
  "question_id": "gk-1996-regular-shanghai-arts-q15",
  "resume_action": "取得同版题面勘误或明确有向距离约定后裁定 Q15 A1；来源只列 (4,2)，当前无向距离完整解含 (-12,-6)，冲突未解决，不得标完成。",
  "source_id": "src-2cd0e37e0e31e5698fdc0f84ba902576f04a18869a73ec0f15565f94f2c0bd35",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1144

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "444e2aa05dac9d30907ee976ba31c68e55f56eea01ebc5aa15bd7736546b79c5",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1145

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "b8a2e58a525c5f355c630a7c7f6c6d896b293ffc952b35b9e0cc0f9106272871",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1146

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "52b4818e8c4349bb28990e14cf4056f494cb5b5d184d73b3a5e2d92710eb8e7b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1147

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "4c4f572a0e889adb39dc9710e92119c0f1be1a1de63bfe4911963d81bfa38991",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1148

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "e02178e7e08f7a5f943175dad982be3060a53af6e985c1357c3e32dbed99a936",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "ff7bd1e37ac3e711944007344e397d67a45dfb080ddc15022a2626ef7214fe44",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1149

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "figure_label",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "c64857aac7870c508be263c2b3164211d8f24b600cce007d73b0cb4467d45ac3",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "ff7bd1e37ac3e711944007344e397d67a45dfb080ddc15022a2626ef7214fe44",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1150

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "dec0b6900c00bb76fcd9ae9cc2012ff1087f1500d9ebb6cae97905bdfd2787b4",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "4e1069e4154a0d7d2b1bc0c368acad06d16513ff7cf130f78c219014632d2ef1",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1151

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "b39a4425c95aa18e319f4ff36d453fa1f96672c3ca3ff1a15d75e659e3a30d7a",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "4e1069e4154a0d7d2b1bc0c368acad06d16513ff7cf130f78c219014632d2ef1",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1152

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "option_formula_alignment",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "b3c6659334605269a1fdebecc5fa8debcb9fda8318da77d92da39bba605d6365",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1153

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "705d76034728fd05e03f217a5192e7262f170363a16d8ce3f6eb58133e36e34d",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1154

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "83e133e4a04dccef8cf8513a10995ed2196d637a37ab1d48c0240b971ab55108",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1155

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "03e17a946cbe6d3869834b940a9c9f8966e681112a326a7870b4fc33193dff91",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 7,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1156

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "a3cf1268eae4a909d7325419e001f127902c98e7cf156c52a68640dab1554196",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 8,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1157

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "5396f1795ab082dd455345a93a3f830e9c5655fff2ddb07079699ef851a114a9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 9,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1158

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "option_formula_alignment",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "ed61feb5afdef3f29d2031b675c51c2c0989bc04cd76df764f9fe1bb0193a817",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 11,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1159

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "5b965e921451f5b0f9946f44d115ae869864d802b9bcb5cfc5ce98cbd08b057f",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 11,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1160

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "721c094c7abfb8446895554b4bc66d493ab900a61a9b8486673829442fd7f7fe",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 12,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1161

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "heading_number",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "10ff42819b4d52eda637e27a49cd41daa8ce2666582b268d7d2d64646694c6a9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 15,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1162

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "3c1c00b846c98bd9061ab012e3db9e3da2140315e87ff0113e7af34b83c29fb8",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 18,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1163

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "heading_number",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "7ce76245d7676fbfd9bbec872afaa9d60183d91083aedc4d2cab73fa8c8e57eb",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 18,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "5c07130e4f9746fe449f2d1c1f0b15f150e440a0f21f298bf6b14808a759477f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1164

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "96ce7067-9f0c-4bdf-83d6-29809b6bf98b",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "e8b852a6c75c7ef886b1ca01e775a77567617bfb4ba908bbf720edc9a7ed4e4d",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1997-regular-shanghai-arts",
  "pdf_sha256": "a8fbd5d18d5ef888aef9486a47180adda488331f9b99924107c66e47df994ed2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1165

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "2db5e79a-9d7b-4bc5-baae-3cc4d7facdb1",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "7ab8e1ebe06bd90091595f34bc93365fd5d871ffc3c748d56e9b7623aa812d02",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 4,
  "paper_id": "gk-1997-regular-shanghai-science",
  "pdf_sha256": "4832a7067e994e83a1e14acb5c1c335269ccae816de941dd2be7abe26247f81d",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1166

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "a524e77b23bbc643542d34e653d99b62b25e997ca54f1434c1de9d6485e6fc02",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1999-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1167

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "bed46a8635b5303cb98f31706230b5ffec4b4eb95cfeb1630110f89a1e959253",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1999-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1168

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "answer_leak",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "7703464fd11f3d4bab2e8688774b19bc6f8fa1fc606743f5b6d4464881e54593",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "88e8e496ae89cd1213093955d8534020dede3a4d66776a198f9d9fd9e0e836fb",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1169

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "figure_label",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "f08c098785f5aa443d87170a300bbde601048a6ab6e534834c710f3b771e1c67",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "88e8e496ae89cd1213093955d8534020dede3a4d66776a198f9d9fd9e0e836fb",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1170

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "answer_leak",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "9f713105e6e5b9909972c213de32c476b1415137bf0330aff1dd24374530164e",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "f0ed0ec6760739b13ac9c3948a31ccf4acf94ac13e506fcdbae2a0e692618b52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1171

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "a6a89fabc55f7ef0e39934de5480d1a602f14579f1d7bd31a3e7c1789a65e97e",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "f0ed0ec6760739b13ac9c3948a31ccf4acf94ac13e506fcdbae2a0e692618b52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1172

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "glyph",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "da428168ec85fa8ee7498b8d6ac39f14fb36907d356dfb7a1225c825c6c2603c",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "f0ed0ec6760739b13ac9c3948a31ccf4acf94ac13e506fcdbae2a0e692618b52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1173

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "f83af72f0bcad7700866de01bdbe60b3ebbc78ecfac75b6643a7cf169150f257",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 10,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "f0ed0ec6760739b13ac9c3948a31ccf4acf94ac13e506fcdbae2a0e692618b52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1174

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "c9a6d82e2da161079bb1cb98c64a14dd7cce5ec550b7e8c650e23413f0f24e13",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 13,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "f0ed0ec6760739b13ac9c3948a31ccf4acf94ac13e506fcdbae2a0e692618b52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1175

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "figure_label",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "52cd95f86e6fc4da6c80feeab386565436e14d8899ed5a8faef7ccfd45077647",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 14,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "f0ed0ec6760739b13ac9c3948a31ccf4acf94ac13e506fcdbae2a0e692618b52",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1176

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "answer_leak",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "44034286245ac775cbc97ca17c21efe54a7ff6c2c04904bcf52a4440f435dbc9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "5ae8fe0ebed55e89cb92cae1a20991d0e5b05c7abcc79f8e468a31d4bc5382b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1177

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "95ae3e87-7159-4bd4-8d47-82b25a2c4c13",
  "check_code": "figure_label",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "961b6d6dc875107825d83b3d684dbf9046a8ae7f108cecf1e290b37931665bb6",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-1998-regular-shanghai-arts",
  "pdf_sha256": "5ae8fe0ebed55e89cb92cae1a20991d0e5b05c7abcc79f8e468a31d4bc5382b2",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1178

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面第 8 题为 (2x^2-1/x)^8：通项 x^{16-3k}，k=16/3 非整数，常数项不存在；卷内答案 60 = C(6,4)·2^2，对应指数 6。300 dpi 复核上标字形为 8（两个封闭孔），盲解独立复现“无常数项”。",
  "fingerprint": "63ebbe774ec627839476e6215a8db2a73fff1837d2b42657f83526bb2c722793",
  "impact": "blocks_completion",
  "paper_id": "gk-1991-regular-shanghai",
  "question_id": "gk-1991-regular-shanghai-q08",
  "resume_action": "取得同版原页或勘误确认上标应为 6（则答案 60）或确为 8（则应改为“无常数项”）；此前保留题面 8、卷内 60 与独立结论“无常数项”三说并列，整卷保持 blocked。",
  "source_id": "src-de45d6075f9038c7b46c233df86b014753be6f32fb2eb832653b00cbad96fcb9",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1179

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面给 l=β∩γ、l∥α、m⊂α、m⊥γ；可推出方向夹角为90°，但未保证 l 与 m 相交。按空间直线方向夹角解释选A；若“垂直”限于相交，题面条件不足。",
  "fingerprint": "d78eea92fa5411ad027c564445236129e6f05ce39ee3d2eeff1d3519f5a9f0c4",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-arts",
  "question_id": "gk-1996-regular-national-arts-q7",
  "resume_action": "编号更正：provenance 的规范题号为 q07；同一未决定义问题已按 q07 重新登记，继续由新编号阻断该卷完成。",
  "source_id": "src-14b5e41702770e8e042a2012628b4977636412e2adfb4e564c6ce6d4e72b063a",
  "status": "resolved",
  "type": "answer-convention-ambiguous"
}
```
## ISSUE-1180

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面未给 a1≠0。若 a1=0，零数列使任意实数公比 q 都满足；若 a1≠0，则 q=0 或 q=−1/∛2。",
  "fingerprint": "c5b495efa16f380b1a3ada741075d4c98fbf175b602524158a3f697475172078",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-arts",
  "question_id": "gk-1996-regular-national-arts-q21",
  "resume_action": "取得当年等比数列定义或可靠同版答案/勘误以裁定零首项是否纳入；此前保留两种条件分支。",
  "source_id": "src-14b5e41702770e8e042a2012628b4977636412e2adfb4e564c6ce6d4e72b063a",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1181

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面使用 log_a 但未另述底数范围；规范答案仅按合法底数 a>0 且 a≠1 分段给解，未补写题面条件。",
  "fingerprint": "1e94a65d1e7160014cf93993c5c08e87b8567323169f230895a8dfbc7898d236",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-science",
  "question_id": "gk-1996-regular-national-science-q20",
  "resume_action": "取得同版原始题页或可靠勘误以裁定底数范围；此前保留两种合法底数分支。",
  "source_id": "src-fb045a4a0667851f33004aec1c020d6220dfa5733a9ee28cc4eeb10d7f6b7aa6",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1182

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面未给 a1≠0。若 a1=0，任意实数 q 都满足；若 a1≠0，则 q=0 或 q=−1/∛2。",
  "fingerprint": "0041a8c7ea52dde17d72a7bfac937765680edbac000c3ec1911eae457451f56c",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-science",
  "question_id": "gk-1996-regular-national-science-q21",
  "resume_action": "取得当年等比数列定义或可靠同版答案/勘误以裁定零首项是否纳入；此前保留两种条件分支。",
  "source_id": "src-fb045a4a0667851f33004aec1c020d6220dfa5733a9ee28cc4eeb10d7f6b7aa6",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1183

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源可见原文为“侧面 AC1”，不足以唯一命名四边形侧面；答案与解析仅在它指 ACC1A1 时给出条件性解。",
  "fingerprint": "3dadc100f6bb94273830d04bb64f4a2d8ce13223953691730bf345b7f2d6a268",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-science",
  "question_id": "gk-1996-regular-national-science-q22",
  "resume_action": "取得更清晰同版原页或可靠勘误确认侧面全名；此前保持原文照录，并将 BE=EB1 与45°标为条件性结论。",
  "source_id": "src-fb045a4a0667851f33004aec1c020d6220dfa5733a9ee28cc4eeb10d7f6b7aa6",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1184

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源长度比条件后印有孤立 l1，之后又写“求 l1,l2 的方程”；规范答案保留该字符，当前推导以其不承载额外条件为前提。",
  "fingerprint": "faa7385db74ebdeea93b9c459ce42085a7cf932efb339ccc02b3acc7b7b7a180",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-science",
  "question_id": "gk-1996-regular-national-science-q24",
  "resume_action": "取得同版原页、勘误或独立版本确认孤立 l1 的含义；此前保留原文并将斜率/方程与弦长结论标为条件性。",
  "source_id": "src-fb045a4a0667851f33004aec1c020d6220dfa5733a9ee28cc4eeb10d7f6b7aa6",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1185

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面给 l=β∩γ、l∥α、m⊂α、m⊥γ；可推出方向夹角为90°，但未保证 l 与 m 相交。按空间直线方向夹角解释选A；若“垂直”限于相交，题面条件不足。",
  "fingerprint": "107e25411c44f77c886cb573d46b8ad1fa606785e7407b994bcd957cdb93ec05",
  "impact": "blocks_completion",
  "paper_id": "gk-1996-regular-national-arts",
  "question_id": "gk-1996-regular-national-arts-q07",
  "resume_action": "取得同版原始题页、可靠勘误或当年采用的空间异面直线垂直定义依据后裁定；此前保留转录及定义分支，不把选项结论称为无条件。",
  "source_id": "src-14b5e41702770e8e042a2012628b4977636412e2adfb4e564c6ce6d4e72b063a",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1186

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "3effd06bc52b51494ad2f317c8546b205125f6f7071f7ca1dbe7f16da823fbb3",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1996-regular-national-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1187

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "fadb08f5cc4aa7265985231bf4557d555d2b6a28065a29411b0ee738e8be062f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1996-regular-national-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1188

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描页3（印刷页136）题面直线逆时针旋转30度后为过圆心的水平线，独立计算得选A；同一PDF扫描页6（印刷页139）卷内答案表印C。两项均按固定源保留，尚无独立勘误或版次证据可裁定。",
  "fingerprint": "8bfbbaba7f733ff4f04a1edc9ab99e6c5d47e62bd3597510ea8a51998d70b693",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-shanghai-arts",
  "question_id": "gk-1999-regular-shanghai-arts-q13",
  "resume_action": "取得同版可追溯原刊、勘误或可靠的题面/答案分开来源后复核；在此之前保留题面推导A与卷内C并列，不将任一方定为官方答案。",
  "source_id": "src-f45a72cc4b6fca6b3bb48f421c9320f7c17aa8c04d746f7ae368c40ef4875742",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1189

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描页3（印刷页136）题面写4z+2̅z=3+√3+i；扫描页7（印刷页140）卷内解答代入式写4(a+bi)+2(a-bi)=3√3+i，所得z和|z-w|范围不同。未用推导改写任何一页。",
  "fingerprint": "2e677853d59a54b92cf461b0fb726d737fd47433e0891ffa4ed4d02e8042ae9e",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-shanghai-arts",
  "question_id": "gk-1999-regular-shanghai-arts-q19",
  "resume_action": "取得同版原刊、可核勘误或独立可信答案来源后逐字符复核并裁定；在此之前并列保留两种源读法，不登记单一答案。",
  "source_id": "src-f45a72cc4b6fca6b3bb48f421c9320f7c17aa8c04d746f7ae368c40ef4875742",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1190

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描页4（印刷页137）第21题（2）可见原句“如图所示形状的几何体积为柱体”，语句疑似漏字或排印异常；题面照录，卷内计算按柱体等截面解释，不能据现件确认缺失文字。",
  "fingerprint": "25a42b03f317848413fb319772b8c993c9ce492bedb997b32b9ac2682acf2737",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-shanghai-arts",
  "question_id": "gk-1999-regular-shanghai-arts-q21",
  "resume_action": "取得同版清晰原刊或可核勘误核对原句；在此之前保留源句并把体积结论标为等截面柱体条件下的解释。",
  "source_id": "src-f45a72cc4b6fca6b3bb48f421c9320f7c17aa8c04d746f7ae368c40ef4875742",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1191

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "edcc5c3cd38b8505e515751632707846e8831ace725b9b306a7e2ff1aee0ac97",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1999-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1192

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "6be9f202921525bdb474de99af1841453c4b8f458aef31d0876e9b71d35d6e68",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1999-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1193

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "6dbc87afa91505ee04bb8354eb7911600c5c07240df4df868d00855fb47dbe70",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1999-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1194

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ed86cb994a42a3de3cefeb7b6c3c34f5cf57fa4ebf3dc768aba6efd45d803c67",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1999-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1195

```json
{
  "paper_id": "gk-2000-regular-national-old-arts",
  "affected_paper_ids": [],
  "type": "answer-conflict",
  "status": "open",
  "impact": "blocks_completion",
  "question_id": "gk-2000-regular-national-old-arts-q12",
  "source_id": "src-a393ebd8958a2b13bc1971720c1c3e8703ed184cb9bc3e7db624e80ea591c461",
  "resume_action": "取得可追溯的同版勘误或可靠答案材料，确认题面是否漏字/图示是否另有解释；在此之前保留原题文字，将答案记为 U/PENDING，不选 A–D。",
  "fingerprint": "43533d728383cff2b37496d5a2c112d8448f7d408d5947436599fd0f667e2a3a",
  "issue_id": "ISSUE-1195",
  "current_evidence": "三个固定源PDF均无答案或解析页，题干与图示相同。按轴截面坐标设底面中心 O=(0,0)、顶点 V=(0,H)、底缘点 B=(R,0)，母线方程为 Hx+Rz=HR；垂足 A=(RH²/(R²+H²), HR²/(R²+H²))=(R cos²θ, H sin²θ)。旋转 OA 得到的内锥高为 H sin²θ、底半径为 R cos²θ，故内外体积比为 cos⁴θ sin²θ。令 u=cos²θ，则 u²(1-u) 的最大值为 4/27<1/2，按当前题面不可能平分体积。旧解析把内锥高度也写成整锥高度 h，漏掉 sin²θ 因子；此前答案 D 的推导不成立。"
}
```

## ISSUE-1196

```json
{
  "paper_id": "gk-2000-regular-national-old-science",
  "affected_paper_ids": [],
  "type": "answer-conflict",
  "status": "open",
  "impact": "blocks_completion",
  "question_id": "gk-2000-regular-national-old-science-q12",
  "source_id": "src-2df550ae82fa57dc70fc83d2c12364bf8a19f13cdc3e8cac49ad80fa8250d1fa",
  "resume_action": "取得可追溯的同版勘误或可靠答案材料，确认题面是否漏字/图示是否另有解释；在此之前保留原题文字，将答案记为 U/PENDING，不选 A–D。",
  "fingerprint": "0e5d2f166d140a09e0ff6fbca616ecf6d90e021790fd31027dd44cc21b62b80e",
  "issue_id": "ISSUE-1196",
  "current_evidence": "三个固定源PDF均无答案或解析页，题干与图示相同。按轴截面坐标设底面中心 O=(0,0)、顶点 V=(0,H)、底缘点 B=(R,0)，母线方程为 Hx+Rz=HR；垂足 A=(RH²/(R²+H²), HR²/(R²+H²))=(R cos²θ, H sin²θ)。旋转 OA 得到的内锥高为 H sin²θ、底半径为 R cos²θ，故内外体积比为 cos⁴θ sin²θ。令 u=cos²θ，则 u²(1-u) 的最大值为 4/27<1/2，按当前题面不可能平分体积。旧解析把内锥高度也写成整锥高度 h，漏掉 sin²θ 因子；此前答案 D 的推导不成立。"
}
```

## ISSUE-1197

```json
{
  "paper_id": "gk-2000-regular-national-new-science",
  "affected_paper_ids": [],
  "type": "answer-conflict",
  "status": "open",
  "impact": "blocks_completion",
  "question_id": "gk-2000-regular-national-new-science-q12",
  "source_id": "src-141d138f3d26910518b47759686b06eea4563ba9d9df53742fc363c6f69721b0",
  "resume_action": "取得可追溯的同版勘误或可靠答案材料，确认题面是否漏字/图示是否另有解释；在此之前保留原题文字，将答案记为 U/PENDING，不选 A–D。",
  "fingerprint": "2f1eae9bbb7ac0252ea5c6190394375136195a47b4a9635385d188680a7cc269",
  "issue_id": "ISSUE-1197",
  "current_evidence": "三个固定源PDF均无答案或解析页，题干与图示相同。按轴截面坐标设底面中心 O=(0,0)、顶点 V=(0,H)、底缘点 B=(R,0)，母线方程为 Hx+Rz=HR；垂足 A=(RH²/(R²+H²), HR²/(R²+H²))=(R cos²θ, H sin²θ)。旋转 OA 得到的内锥高为 H sin²θ、底半径为 R cos²θ，故内外体积比为 cos⁴θ sin²θ。令 u=cos²θ，则 u²(1-u) 的最大值为 4/27<1/2，按当前题面不可能平分体积。旧解析把内锥高度也写成整锥高度 h，漏掉 sin²θ 因子；此前答案 D 的推导不成立。"
}
```

## ISSUE-1198

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描题干与图示经逐页及300dpi局部复核一致，声称旋转OA所得曲面将圆锥分成等体积两部分。坐标计算所得内侧圆锥体积比为 cos^4(theta) sin^2(theta)，其最大值4/27<1/2，按当前题面不可能平分。扫描件不含答案页。",
  "fingerprint": "699349e9e1e3bee9a076dbb11fa2e7350d410493e8a60971ace5a9e479ef6bf1",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-guangdong-unspecified",
  "question_id": "gk-2000-regular-guangdong-unspecified-q12",
  "resume_action": "取得可追溯同版勘误或独立版本/可靠答案材料，确认题面或图示是否有缺漏；此前保留原文并将答案记为U/PENDING，不按选项猜填。",
  "source_id": "src-c603aac0b64fcc89e162bd2b5358ce3c9a5c1ce8e5949a7f787f906fa25393a6",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1199

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描原文仅写“点E分有向线段AC所成的比为lambda”，没有明确比值分子和分母；当前 e 范围只在 lambda=AE/EC 约定下推导。",
  "fingerprint": "cce89a643b7d9042be420cc49b40483097c287eac5153ae67f18c1e8c9e23e67",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-guangdong-unspecified",
  "question_id": "gk-2000-regular-guangdong-unspecified-q22",
  "resume_action": "寻找同版教材/勘误或可追溯权威定义确认有向分点比方向；此前保留U/PENDING，条件推导须显式标注定义。",
  "source_id": "src-c603aac0b64fcc89e162bd2b5358ce3c9a5c1ce8e5949a7f787f906fa25393a6",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1200

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源只有题面，没有答案页；现有几何推导证明等体积条件与题面冲突，不能据此选择选项。",
  "fingerprint": "929475dc310873e2fe90f5fcefc8ca97d3c59024e28285a997cc72c2f5125587",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-guangdong-unspecified",
  "question_id": "gk-2000-regular-guangdong-unspecified-q12",
  "resume_action": "取得可追溯同版勘误或独立可靠答案材料；此前将答案保持 U/PENDING。",
  "source_id": "src-c603aac0b64fcc89e162bd2b5358ce3c9a5c1ce8e5949a7f787f906fa25393a6",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1201

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定扫描第2页原字为“底面ABCD上菱形”；该句语义不通。本稿照录，不推定为“是菱形”。",
  "fingerprint": "a0c6b63a0fa297458d1b260266e5b1f8e0d5130630b099e815107d4379c5c381",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-guangdong-unspecified",
  "question_id": "gk-2000-regular-guangdong-unspecified-q19",
  "resume_action": "取得同版勘误、独立版本或更清晰且可追溯来源，确认原字是否讹误；此前保持原字并将依赖该释读的结论标为 U/PENDING。",
  "source_id": "src-c603aac0b64fcc89e162bd2b5358ce3c9a5c1ce8e5949a7f787f906fa25393a6",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1202

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源没有答案页；第(2)问的数值结论仅在将源文“上菱形”读作“是菱形”时成立，源文语义尚未核实。",
  "fingerprint": "20a2a9ba376af83051fd4789bdb611e8ffdef925bd5af96c8f6ee1c361de4d6f",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-guangdong-unspecified",
  "question_id": "gk-2000-regular-guangdong-unspecified-q19",
  "resume_action": "先确认题面释读并取得可追溯答案材料；此前最终答案保持 U/PENDING，条件推导须保留前提。",
  "source_id": "src-c603aac0b64fcc89e162bd2b5358ce3c9a5c1ce8e5949a7f787f906fa25393a6",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1203

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第2页 Q19 印作“其半轴长为2r，短半轴长为r”；图中 AB 水平尺寸标 2r，半椭圆高度标 2r。图示与“长半轴长为2r、短半轴长为r”的解释相符，但题干第一处未明确写“长”，故规范转录保留印刷原文，解答只按图示尺寸推导。",
  "fingerprint": "b47dc523542107f0dc722122cb2fdad826d8ddd3c559495b900ce7e7d425fb87",
  "impact": "blocks_completion",
  "paper_id": "gk-2007-regular-beijing-science",
  "question_id": "gk-2007-regular-beijing-science-q19",
  "resume_action": "找到可逐页比对的独立同期题面或清晰版本核实 Q19 术语；核实前保留“半轴长”原文，不静默改成“长半轴长”，并将依赖图示尺寸得到的公式明确标作编者推导。",
  "source_id": "src-3612a22ce3848ad6ebbec4d94861dd64b009980e14e8c7a83efefb2ea39bd367",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1204

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源PDF第2页原文仅写“已知 y=cos x”，后续两问使用 f(α) 与 f(x)，没有给出 f 的定义。题面已照录；在明确假设 f(x)=cos x 下的推导与源载答案相符，但该假设未由题面确定，规范答案保持U/PENDING。",
  "fingerprint": "3a2e1dda3639843155a90bb4c3800bfd5b7c93a9bde9440b9562d9dd7a3acf4f",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-spring-shanghai",
  "question_id": "gk-2018-spring-shanghai-q17",
  "resume_action": "寻找可追溯的独立同版题面或勘误，确认 y=cos x 是否对应未印出的 f(x) 定义；核实前保留原文及条件推导，答案保持U/PENDING。",
  "source_id": "src-b19b233abb266d1b051ded3c332a399c1722d8192d07ce1bf2234dda57bd25bc",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1205

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源PDF第3页定义双曲线Γ，随后原文仅写“若点(2,1)在上”，没有指明该点属于哪条曲线。题面已照录；仅在假设(2,1)∈Γ下可确定焦点，规范答案保持U/PENDING。",
  "fingerprint": "621b24c7d08ca47e17d1f93c053772764eacce0a7a9980a1ec94892231de241e",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-spring-shanghai",
  "question_id": "gk-2018-spring-shanghai-q18",
  "resume_action": "寻找可追溯的独立同版题面或勘误，确认点(2,1)所属曲线；核实前保留原文及条件推导，答案保持U/PENDING。",
  "source_id": "src-b19b233abb266d1b051ded3c332a399c1722d8192d07ce1bf2234dda57bd25bc",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1206

```json
{
  "affected_paper_ids": [],
  "evidence": "复查固定来源PDF第6页原图及文字层，Q21(3)明确印作“T_n 是 {c_n} 的前 n 项和”。此前题面转录漏掉“和”字，属于转录错误而非原卷定义缺项；已更正题面并据明示定义独立确认 a>0、q≥2，与第7页源载参考答案一致。该问题已解决。",
  "fingerprint": "7b75fe9f51494a3eea1f3650e04846cf2be6721875c0e3d3129bf876360b2a25",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-spring-shanghai",
  "question_id": "gk-2018-spring-shanghai-q21",
  "resume_action": "已复查固定来源第6页并更正漏字转录；无需寻找外部版本。",
  "source_id": "src-b19b233abb266d1b051ded3c332a399c1722d8192d07ce1bf2234dda57bd25bc",
  "status": "resolved",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1207

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "4e071b3c25dad54408dc5a739462d6bdd5bc22526e0eefe05a6daa1adf0ea907",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1208

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "d3e317929a39fbaf450c0a1ed1037b426530faced1047b8c7ad5368b632e9d09",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1209

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "8387e7215680a0b1057a8cbedb4b75bc577310497a333a870e2309ac349a9013",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1210

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "f77b308f5e46dbd77c91d571a754f591c7cbc22d28d53e1b910228593b753350",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1211

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 PDF 第1页 Q18 仅给出 b_1=1 与前 n 项和 B_n=(b_n+1)^2/4，未规定 b_n 的符号或取值范围。递推化简为 (b_n+b_{n-1})(b_n-b_{n-1}-2)=0，因此每步可有 b_n=-b_{n-1} 或 b_n=b_{n-1}+2；例如 b_n=(-1)^(n-1) 与 b_n=2n-1 均满足题面，通项不唯一。题面忠实保留源文，现有答案不强选唯一式。固定 PDF 不含答案页，不能用来源载答案解决此点。",
  "fingerprint": "ba606951d4705c7d429baba2b7307343077e1bae89b5d167fc1944986dc4c865",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-spring-anhui-arts",
  "question_id": "gk-2004-spring-anhui-arts-q18",
  "resume_action": "取得可追溯的同版勘误或独立同期题面/答案材料，核实是否漏印了对 b_n 的符号或取值范围限制；核实前保留原题与非唯一推导，将整卷 production_state 保持 blocked。",
  "source_id": "src-9c46c959fc97e9d53c91e510403e97f1810d192e5049962539d9d4b54331c35d",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1212

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "9581c673ea135e45f0bbd212588fc6e2e6e47e2b4b8e913dfe3d4842fc671338",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1213

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "d0b0a1f96c88bed3dc6952c90c8fd9d0e0f72f67d3ca7e9859129e3690598524",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1214

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "96cfa0de5f147a6703152277487dee19acb16ae6392a906cdc33f9cce72f0fa5",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1215

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "24d83b9540f16a7e55001f17260abd86664f61bcd9b17257b9b94beee86bd571",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-anhui-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1216

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第1页 Q2 印 1/x<1/2，解集为 (-∞,0)∪(2,+∞)，所列四个选项均不相等；固定副本未附答案。 新增 EOL 2006-06-10 安徽文科答案图将第（2）题标作 D；Quick Look 对照 6月9日 Word 试题件，确认该件 D 项同样印为 (-∞,2)∪(2,+∞)，其解答列出 x(2-x)<0 后仍选 D。同期 EOL 材料也存在选项/答案冲突，不能据字母 D 改写固定副本或确定原卷应有选项。详见 reports/2006-anhui-arts-eol-answer-recheck-2026-11-02.md。",
  "fingerprint": "2dcc9b93e3e35d167539aa68a13a22c69f338b477c32f6d6d3d96597b9732749",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-anhui-arts",
  "question_id": "gk-2006-regular-anhui-arts-q02",
  "resume_action": "取得可追溯的同版题页或可靠勘误核对 Q2 题干和选项，在此之前保留无匹配选项及阻断状态。",
  "source_id": "src-c8cc6985576733188a535d25ee781c6c6b1b8de19855999d38d24a0e053810a7",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1217

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第1页 Q5 椭圆式仅见 x²/6+y²/2，之后直接接右焦点，未见等号及右侧；两次源页核对一致。 新增 EOL 2006-06-09 文科 Word 试题件；Quick Look 视觉复核清楚显示其 Q5 椭圆式为 x²/6+y²/2=1，解答给出右焦点 (2,0)。这是 EOL 所载文科版本的直接证据；固定两页副本未见等号及右端，两者的同版/复制来源链未建立，故不能把 EOL 版本回写为固定副本原文。详见 reports/2006-anhui-arts-eol-answer-recheck-2026-11-02.md。",
  "fingerprint": "07a30ace92e8d26d373685a11dfc70b03d5794c3c314c4e0dd026dba40e038a3",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-anhui-arts",
  "question_id": "gk-2006-regular-anhui-arts-q05",
  "resume_action": "取得可追溯的同版题页或可靠勘误确认 Q5 椭圆方程，未核前不补写。",
  "source_id": "src-c8cc6985576733188a535d25ee781c6c6b1b8de19855999d38d24a0e053810a7",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1218

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本 Q5 椭圆式缺少可见等号及右侧，不能确定椭圆焦点或参数 p；固定副本未附答案。 新增 EOL 文科参考答案扫描图标记 Q5 为 D，配套 Word 文档视觉可读 Q5 方程 x²/6+y²/2=1，并解得 p=4；但文件出版/编者身份与固定候选源版本关系均未核。可支持 EOL 版本答案 D，不足以认证固定副本的答案来源，固定副本答案继续 U/PENDING。详见 reports/2006-anhui-arts-eol-answer-recheck-2026-11-02.md。",
  "fingerprint": "2ffc2d9a776c9f6d8cf78be2a2bbc132a79b4d08c2b90055f86ce5743e11eb53",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-anhui-arts",
  "question_id": "gk-2006-regular-anhui-arts-q05",
  "resume_action": "确认 Q5 完整题面后独立求解并复核；此前保留答案待核及阻断状态。",
  "source_id": "src-c8cc6985576733188a535d25ee781c6c6b1b8de19855999d38d24a0e053810a7",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1219

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本 Q3 只印出 x^2/6 + y^2/2，随后直接接“的右焦点”，未见等号和右侧。中国教育在线关联题面图及互联网档案馆保存的 2006 年四页文章快照对应 2006 安徽理科卷 Q1–Q22；EOL 图中 Q3 明确写 x^2/6 + y^2/2=1，独立复核据此推导 p=4（D）。Wayback 图片回放端点可读取 EOL 第1页的 2006-06-19 图像捕获（600×744，SHA-256 4b670066dbb0c0f0b4e7281147f6b6003925df9223d29b7baee5a88be3d8f895），故此前“CDX 未找到 JPG 历史字节快照”仅指此前 CDX 查询结果，不代表没有可回放捕获。此图仍是 EOL 四页版；与固定 A3 PDF 的版次/底本/扫描链未证实，EOL 也非考试机构原卷认证，因此不能证明固定副本漏印前的原文或官方答案。固定副本题面仍忠实照录，答案保持 U/PENDING，需取得可追溯同版完整题面或可靠勘误裁决。",
  "fingerprint": "5ffa2f8307ff0aa516cdbce8c8245ca876255336e9587e8a5283ff46401d3014",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-anhui-science",
  "question_id": "gk-2006-regular-anhui-science-q03",
  "resume_action": "取得可追溯的同版完整题面或可靠勘误，核明椭圆方程右侧后重新独立求解并更新答案及逐题来源记录。",
  "source_id": "src-3aed0bc3d5875c8ce734b5b97f95992307ff56fc580067083caea214e3028675",
  "status": "open",
  "type": "answer-missing"
}
```
## ISSUE-1220

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第1页 Q9 写明4人参加连续5天活动、甲连续参加2天、其他人各1天，但未说明每天是否必须有人参加；若每日都须覆盖则24种，若允许空日及同日多人则500种。固定副本所附答案为24种，但适用前提未写明。",
  "fingerprint": "908445ded075e7c1058dcce75f95765ee60e51b085ca27873c0c3727ecd52361",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-spring-shanghai",
  "question_id": "gk-2019-spring-shanghai-q09",
  "resume_action": "取得可追溯的同版题面或可靠勘误，确认五天是否必须每日有人参加；未确认前保留24与500两种条件分支及待核状态。",
  "source_id": "src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1221

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第1页 Q11 使用 F_1、F_2 记号，但题干未显式定义二者为椭圆焦点；现有夹角结论以该解释为条件。",
  "fingerprint": "b63d5185b560666e40ae189967e6d1b98acbff2909e94296573cca0ce3b415fa",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-spring-shanghai",
  "question_id": "gk-2019-spring-shanghai-q11",
  "resume_action": "取得可追溯的完整同版题面或原卷说明，确认 F_1、F_2 的定义；确认前保留条件性答案，不补写原题定义。",
  "source_id": "src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1222

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本所附答案选 A 并称轨迹为直线 x+y=2。按题面条件 y_i>0 且 y_i^2=1-2a_i，故 a_i<1/2；(1/a_1,1/a_2) 的严格轨迹还须满足 x<0 或 x>2，选项没有严格对应的两条开射线。两次独立推导均保留该差异。",
  "fingerprint": "36ff9784459d7f5bd803e08220e025dfed19455752e01591e866ad0ed52778ab",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-spring-shanghai",
  "question_id": "gk-2019-spring-shanghai-q16",
  "resume_action": "取得可追溯的同版原卷或可靠勘误，核对 Q16 轨迹与选项；此前并列保留源附答案 A 和严格推导范围，不强行唯一化。",
  "source_id": "src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1223

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第10–11页源附答案将 q=0 排除；现有解析指出，采用允许零公比的递推定义时需包含 q=0，而采用各项非零的等比数列定义时不包含。题面未给出定义约定。",
  "fingerprint": "b091893bb861fa16c98ae00945b41256f108d6c53819a533f76134c97dfd0c12",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-spring-shanghai",
  "question_id": "gk-2019-spring-shanghai-q18",
  "resume_action": "取得同版定义或可靠来源明确本卷采用的等比数列约定；此前保留 q=0 包含与排除两种条件结论。",
  "source_id": "src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1224

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第3页 Q19(3) 仅称 P_1、P_2、P_3 是抛物线准线上三点且 |P_1P_2|=|P_2P_3|，未说明三点互异；按互异条件可推出严格不等式，若 P_1=P_3 则结论不固定。",
  "fingerprint": "211a2670f469d1327e32ddcca1ebe0d4b9aac83d36c6a105f27d00bc3bb0ac0a",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-spring-shanghai",
  "question_id": "gk-2019-spring-shanghai-q19",
  "resume_action": "取得可追溯的同版完整题面或可靠勘误，确认 Q19(3) 是否要求三点互异；确认前保留两种条件下的结论并阻断唯一答案。",
  "source_id": "src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1225

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本第12页“点睛”称非退化三角形的中线满足 2AE>AB+AC；这与严格三角形不等式给出的 2AE<AB+AC 方向相反。源附最终答案虽然给出 >，但源解析中的该段文字存在可见冲突，须分开保留。",
  "fingerprint": "584d705f108a2702e3e62a9989ad1d3b450c7a79a9d4a975282fe36f385a52a2",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-spring-shanghai",
  "question_id": "gk-2019-spring-shanghai-q19",
  "resume_action": "取得可追溯同版勘误或可靠解析核实该源解析文字；未核前不静默改写源附内容，项目独立证明须单独标明来源与逻辑。",
  "source_id": "src-9bdb153dc0768790fc6e5af115cc9387a25f5f3dbdb3affdf6c74bc7058cd631",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1226

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第 1 页 Q17 四棱锥图已重绘为 TikZ 源并登记到 figure_files；规范题面和生成的含解析稿映射到该图，questions.tex 与 answers.tex 各引用一次。图稿对照源图保留 AD、DC、PD 虚线，PA、PB、PC、AB、BC 实线及 A/B/C/D/P 顶点标签，未增添角标。正式四版构建与排版视觉检查尚未执行。",
  "fingerprint": "10172ef6227c196b66200c007d224e99199258f3f9e2a20fad90c6bcda9ff712",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-spring-shanghai",
  "question_id": "gk-2020-spring-shanghai-q17",
  "resume_action": "图稿已按固定副本 Q17 源图重绘并登记，题面及确定性 TeX 映射已同步；此缺图问题结案。若正式构建中发现版面问题，另行登记具体修订事项。",
  "source_id": "src-aacbb6140d9e12bc5aca908afe4d613b6ae584f08da89de4fa537d174727f9c2",
  "status": "resolved",
  "type": "figure-missing"
}
```
## ISSUE-1227

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面称步行道 OA 长 120 米并定义 B(x,0)、ω2(t,0)，但未明列 x,t 范围；固定源所附解析按 B、ω2 均在线段 OA 上推导。",
  "fingerprint": "769aab6b7a42790d8eb7c499716993b4bf29f825b08354ad557f33f6d3241362",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-spring-shanghai",
  "question_id": "gk-2020-spring-shanghai-q19",
  "resume_action": "取得可追溯的同版题面/勘误或明确采用的命题约定；确认前保留答案 U 与线段解释下的条件结论，不把该范围补写进原题。",
  "source_id": "src-aacbb6140d9e12bc5aca908afe4d613b6ae584f08da89de4fa537d174727f9c2",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1228

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第 9 页第（3）问只写 m 为奇数；题面允许 m∈Z。项目按题面独立分类得到正奇数：m≤0 有 f(n)=-n 反例，正偶数有奇偶指示函数反例，正奇数由周期 2 与 m 且 gcd(2,m)=1 强制常值。",
  "fingerprint": "f0a9b473d8ea7752d82508f30c41d23d3bf0b91097ae2ae67a6bc6bb530e5264",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-spring-shanghai",
  "question_id": "gk-2020-spring-shanghai-q21",
  "resume_action": "取得同版勘误或可追溯答案材料后复核源附缺项；在此之前保留源附原结论、项目正奇数推导与 open/blocks_completion，不据源附答案单独裁定。",
  "source_id": "src-aacbb6140d9e12bc5aca908afe4d613b6ae584f08da89de4fa537d174727f9c2",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1229

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第1页（印刷页121）Q11 图中 E、B 之间的小点名无法从低清字形区分为 I 或 L；题干文字写 I。当前题面保留题干的 I，并在独立复核记录中明确图中字形未决，不能据图判定其确为 I。",
  "fingerprint": "8ca6d86e1a3f56a6218370141ea4f73a0346f7358542f3ebfe4eb4c4e630c1f0",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-spring-beijing-arts",
  "question_id": "gk-2003-spring-beijing-arts-q11",
  "resume_action": "取得可追溯的同版高清题页或可靠勘误，核定 Q11 图中字形；在此之前保留题干照录、图中文字形 uncertain 与完成阻断。",
  "source_id": "src-4ac986eba3d22fd3034252b57e1fed7e2b7b90eaaef7706499eb43fad52756e1",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1230

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "e17a09de045a8e3e3d40968c7c09686a3956484b17195f849d1c6e27bc668326",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1231

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "5a22f45ca355a94d02aa27b8f4075c3b247fffbafe7cee7f7556c86e0526223e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1232

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "0c16226e3e803075c93a797a6fb5c13c1ac026dbf244ed367e685ada0bccacc4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1233

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "7eda552d4fc84c2493d3b549b9e9015d12f5b595a4915dce5e61f3cd9ba39d3e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-spring-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1234

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "ec97e6aa594f213dfbe689022bd60461fd4034293311b2ab99d5512dcc4fb86b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1235

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "8c330015d2739387806d75c070419d31dafe534ed00ccc75670668871c903919",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1236

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "6d6d50aac23b5b61d4079f9a10368798554fb5d6c1c92be7a4c6653bb39c45ce",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1237

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "d335c5e24ef508dd0b45f4a639dcdcdffd085b88d0907a336b356c5c796615e8",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1238

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第2页（印刷页156）Q20尾问源文可辨为“计算公以及”。当前题面照录该短语并注记疑脱“式”字，但固定副本未提供勘误或可追溯的同版异本；依据上下文补成“计算公式”仍属推测，不能据此消除转录歧义。",
  "fingerprint": "cbde11e7d07568313e2b6f78923a54c121a35b431d7de416d55014d15c1c55c9",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-spring-beijing-arts",
  "question_id": "gk-2004-spring-beijing-arts-q20",
  "resume_action": "取得可追溯的同版高清题页、原始扫描或可靠勘误，核定 Q20 尾问是否脱“式”及其完整原文；核实前继续照录“计算公以及”，保留转录标记并保持整卷完成阻断。",
  "source_id": "src-417d865aa928e69f32b3fcbc80abe4fa227259b79ababcce8765ea981117119b",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1239

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第3页 Q16 印有“∠A₁AC =”但未见数值；第5–6页副本所载解答将 △AA₁C 称为直角三角形并据 AC=4 得体积48。现有题面可构造满足可见条件但体积分别为48与48√3的向量情形，因此48不能由现存题面唯一推出；答案材料官方身份未核。",
  "fingerprint": "ba65aae3dd9134245fac3eb616651c73a6ea44b46730d8def18827cfadb40c53",
  "impact": "blocks_completion",
  "paper_id": "gk-2009-spring-shanghai",
  "question_id": "gk-2009-spring-shanghai-q16",
  "resume_action": "取得可追溯的同版清晰题页或可靠正式勘误以核定 ∠A₁AC 条件，再重新求解并盲核；此前保留题面缺项、答案 U，并保持整卷完成阻断。",
  "source_id": "src-306adbf685e57e000a68f29eb9e85f4c3e0846f2c5b1f2b9e28d23d3635b629f",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1240

```json
{
  "affected_paper_ids": [],
  "current_evidence": "Q16 现存题面在 ∠A₁AC= 后缺值。独立数学复核确认两组满足其余可见条件的坐标构造分别给出体积48与48√3；因此没有可由当前题面唯一核定的数值答案，规范答案为 U。此条记录答案待补；既有 ISSUE-1239 单独记录印载48依赖未见直角条件的冲突。",
  "fingerprint": "82b193904bdc2732d95cd080f840b3654415583b34732826bfc620355ef40161",
  "impact": "blocks_completion",
  "paper_id": "gk-2009-spring-shanghai",
  "question_id": "gk-2009-spring-shanghai-q16",
  "resume_action": "取得可追溯的同版清晰题页或可靠正式勘误，核定缺失的 ∠A₁AC 条件后重新求解并独立复核；此前答案保持 U，并与 ISSUE-1239 的印载答案冲突共同阻断整卷完成。",
  "source_id": "src-306adbf685e57e000a68f29eb9e85f4c3e0846f2c5b1f2b9e28d23d3635b629f",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1241

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "d67803229691173f6ccc47202938b5f07173ad3667c0c8b54754436f3da86a2f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1242

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "8069ca83f2753184aba3aae98ae45f847432fe9a1c20795ce53597cae4cbe7f9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1243

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "f676733aeee51ce3e8e554ecc6d0db362d981d2e54ec90197430175d2f0dda89",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1244

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ce5f88d7a6979e7788578d4b9d9751f5a7130365eec6f899de8eccfdf4c6fbb2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1245

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面仅给出复数对应圆盘，未明确概率分布；圆盘均匀为项目建模假设。",
  "fingerprint": "56d41084b5b2b175075a12f510a2146dba703e8d8962f2162e3b30cfe0e0bc26",
  "impact": "blocks_completion",
  "paper_id": "gk-2015-regular-shaanxi-science",
  "question_id": "gk-2015-regular-shaanxi-science-q11",
  "resume_action": "寻找可追溯来源确认概率模型，或保留按均匀模型的条件结论。",
  "source_id": "src-35a90f08c9b32a20289a652cad7019dba5a69a734c5686fe11c7739b801c212b",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1246

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面要求最大流量比，截面积比例计算需流速等水力条件；源题未明示。",
  "fingerprint": "a3204fcc5cbfece5eeb5a8ad695865f0327a323c2be87f655fe4a4104186f82d",
  "impact": "blocks_completion",
  "paper_id": "gk-2015-regular-shaanxi-science",
  "question_id": "gk-2015-regular-shaanxi-science-q16",
  "resume_action": "核实原题和可追溯的流量模型，保留条件性结论。",
  "source_id": "src-35a90f08c9b32a20289a652cad7019dba5a69a734c5686fe11c7739b801c212b",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1247

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面给出单程样本频率，未明确去返程联合分布；相同边缘下可构造不同结果。",
  "fingerprint": "b5e5d092a77d23c2550166394660aa9263c0e951d026c500ddf99bd42ced4dbf",
  "impact": "blocks_completion",
  "paper_id": "gk-2015-regular-shaanxi-science",
  "question_id": "gk-2015-regular-shaanxi-science-q19",
  "resume_action": "寻找可核验的往返路况联合分布或原始题面；否则保留未定及条件分析。",
  "source_id": "src-35a90f08c9b32a20289a652cad7019dba5a69a734c5686fe11c7739b801c212b",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1248

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本题干称 I 为 BE 中点，图中相应标字为 L，存在图文标记不一致。",
  "fingerprint": "1e2be67d2b30b71d03d22b275374b22cbb3258e126cfacd1e033184e23b11e55",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-spring-beijing-science",
  "question_id": "gk-2003-spring-beijing-science-q08",
  "resolution": "第 8 题原图 BE 中点标作 L、题干作 I，600dpi 裁图逐点核对确认同一中点；答案 B 已定，题面保留原图字母并在图注说明",
  "resume_action": "寻找可核验独立来源核实图文标记；保留固定副本原貌。",
  "source_id": "src-64f42b96e9699618b024fcdb4364aa03d49d0a00a0242054e79536696e4999d8",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1249

```json
{
  "affected_paper_ids": [],
  "current_evidence": "按题干 I 为 BE 中点求得 B，但图文标记不一致，答案与图中标记关系待核。",
  "fingerprint": "9da32e12301818e713032a9d39f8d45f872cdee242319520842164490227de11",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-spring-beijing-science",
  "question_id": "gk-2003-spring-beijing-science-q08",
  "resolution": "300/600dpi 裁图逐格核对：展开图折成 D-E-F 正四面体，GH∥FD、IJ∥BD，夹角 60°，答案 B",
  "resume_action": "核实第8题原图及文字对应关系，再评定答案。",
  "source_id": "src-64f42b96e9699618b024fcdb4364aa03d49d0a00a0242054e79536696e4999d8",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-1250

```json
{
  "affected_paper_ids": [],
  "current_evidence": "表格仅列有限样本，140、85 是一种可能的规律，不能仅凭数列唯一确定缺失值。",
  "fingerprint": "372ca06d444474efa85ebe685967ba2d10ff4c355dd1e57026e541fabe29b965",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-spring-beijing-science",
  "question_id": "gk-2003-spring-beijing-science-q14",
  "resolution": "第 14 题表两空夹在已知值之间：收缩压 135→145 公差 5 得 140；舒张压 83→88 按 +2/+3 交替得 85，两空均唯一",
  "resume_action": "寻找可核验来源或题设规则，缺失时保留 U/PENDING。",
  "source_id": "src-64f42b96e9699618b024fcdb4364aa03d49d0a00a0242054e79536696e4999d8",
  "status": "resolved",
  "type": "answer-missing"
}
```

## ISSUE-1251

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源题面仅称无穷等比数列。允许q=0的递推定义下极限条件给a1=4且a2范围为(-4,4)；若约定q非零则去除0。当前没有本卷定义或命题约定证据可裁定。",
  "fingerprint": "3135b921ba6fd7c942e58e5df036f65fb194040fac2fd75dcdb34cebcae33303",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-spring-shanghai",
  "question_id": "gk-2021-spring-shanghai-q09",
  "resume_action": "核对本卷采用的等比数列定义或可追溯命题约定；取得证据前保留两种范围与U/PENDING。",
  "source_id": "src-7ae0174ccd32fd350e3842a1514ae63a3d1bf1bfb082340400feec85431fc1b1",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1252

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面原句为对任意n存在实数φ使cos(nθ+φ)<√3/2。任取θ>0可令φ=π−nθ，故没有最小正θ；固定副本参考答案印2π/5，无法由录题推出。",
  "fingerprint": "a11e63e085270b332b8f92860bf813d2bcf528688ffbc5b20a0b166bba5f3e5c",
  "impact": "blocks_completion",
  "paper_id": "gk-2021-spring-shanghai",
  "question_id": "gk-2021-spring-shanghai-q12",
  "resume_action": "寻找同版勘误或可追溯题源澄清量词；未澄清前保留题面照录与U/PENDING，不自行调换量词。",
  "source_id": "src-7ae0174ccd32fd350e3842a1514ae63a3d1bf1bfb082340400feec85431fc1b1",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1253

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "77b894cce1078c1abfb4f9bf0725890518c23e5ee58c719ddd1b0c2769ebc79d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1254

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ad5f20102781cf12a6dbf69be14b9f9b7148cf00b98695da2b295f72df0ecb9e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2021-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1255

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "ef920d97568bfe982cb44e559573c6c6a6b4667b6dbed605b571ed5a857dcc27",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-spring-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1256

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "16e4eef86cc419ea5b94742a3a459afd4964dfa05057abee8d61e8590a25842d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-spring-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1257

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "904fbb5fa775fd7b17cb51b2b847fcbe24443433d999f27454d755a5ad7005d8",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-spring-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1258

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "efc349761739f97f61dff7d0d2f96070f80c12d7a3e47871299a6de510eeb05c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-spring-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1259

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第3页（印刷页638）题面映射 (x,y)→(y−1,x+2)，像点 (3,−4) 的原象为 (−6,4)，对应选项 B；第8页（印刷页643）答案表清晰印 C。两处均照录，无法从同一扫描件裁定哪处代表正确答案。",
  "fingerprint": "987e168fe7509e271bc023896e177beb4431159946be136d01f432f812ec4798",
  "impact": "blocks_completion",
  "paper_id": "gk-1989-regular-guangdong-arts",
  "question_id": "gk-1989-regular-guangdong-arts-q09",
  "resume_action": "取得可追溯的同版勘误、独立版本或可靠出版资料以核对 Q9；在证据到位前保留题面推导 B 与扫描答案 C，并保持 U/PENDING 和完成阻断。",
  "source_id": "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1260

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第4页（印刷页639）Q16未说明“与两异面直线都垂直”是否要求相交；按方向夹角定义有无穷多条，若要求同时相交则为唯一公垂线。第8页答案表印 D，但不能据此补定题目采用的定义。",
  "fingerprint": "c425727c09f46c79e97f27881991efc98e09aff71b63d747042b2c30e2173ccf",
  "impact": "blocks_completion",
  "paper_id": "gk-1989-regular-guangdong-arts",
  "question_id": "gk-1989-regular-guangdong-arts-q16",
  "resume_action": "查得可靠教材语境、同版说明或勘误以确定本题“垂直”的约定；此前保留两种条件解释、答案 U/PENDING 与完成阻断。",
  "source_id": "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1261

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第5页（印刷页640）Q21选项 A 照录为 a≤3；按题设函数在 (−∞,4] 单调递减应有 a≤−3，四个选项均无完全匹配项。第8页答案表仍印 A，不能以推测漏印负号修复题面。",
  "fingerprint": "a902318a4fd18e349e2549b0551a025cdb793bd5d15f45d3dbc450c19e4bea74",
  "impact": "blocks_completion",
  "paper_id": "gk-1989-regular-guangdong-arts",
  "question_id": "gk-1989-regular-guangdong-arts-q21",
  "resume_action": "取得同版清晰扫描、可靠勘误或可追溯异本核定 Q21 源面缺项；在此之前照录 A 项 a≤3、保留数学范围 a≤−3、答案 U/PENDING 与完成阻断。",
  "source_id": "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1262

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第3页题面独立求得选项B，第8页答案表印C；固定源内部无法判定最终答案。ISSUE-1259仍记录印载答案冲突；答案最终裁定缺失，规范答案维持U。",
  "fingerprint": "53aa20335d8af8ceae19f1e92b1d9d9d643f94edfe10d066311ecee2eb67695b",
  "impact": "blocks_completion",
  "paper_id": "gk-1989-regular-guangdong-arts",
  "question_id": "gk-1989-regular-guangdong-arts-q09",
  "resume_action": "取得可追溯的同版勘误、独立版本或可靠出版资料核定Q9最终答案；在此之前保持U/PENDING，与ISSUE-1259的印载答案冲突共同阻断完成。",
  "source_id": "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1263

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第5页照录选项A为a≤3，按题设推得完整范围a≤−3；第8页答案表印A，但固定源内部无法裁定最终正确选项。ISSUE-1261仍记录题面选项与推导冲突；答案最终裁定缺失，规范答案维持U。",
  "fingerprint": "a7bd694f7ae25e783ab11d7f578416eccd261e9b879ca8da77c31475856a8356",
  "impact": "blocks_completion",
  "paper_id": "gk-1989-regular-guangdong-arts",
  "question_id": "gk-1989-regular-guangdong-arts-q21",
  "resume_action": "取得可追溯的同版勘误、独立版本或可靠出版资料核定Q21最终答案及源面选项；在此之前保持U/PENDING，与ISSUE-1261的题面冲突共同阻断完成。",
  "source_id": "src-ff04f7f2223009c3c15fc98a35cc99ba9f03d8be55457e6551b982fbb17f2766",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1264

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面印作 M⊆N，允许 M=N；真包含时为B，相等时为C，不能据当前题面唯一确定。",
  "fingerprint": "b826ffa9d2b4cfeaf9a187aa4dc20708e1081ce6e5d7b22c181d8fd1a9a140b0",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-spring-shanghai",
  "question_id": "gk-2004-spring-shanghai-q14",
  "resume_action": "取得可追溯同版原卷或明确勘误，核实包含条件；在此之前保留条件性答案和待核状态。",
  "source_id": "src-eda3090af4489c2848005279f9f1f65a561d4fa54daf91ccd574cfbff213be4f",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1265

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面称实数p满足不等式，但不等式使用变量x；现按印文保留并区分字面与条件性解释。",
  "fingerprint": "936605f92fcd5939988e9995c108c8b91a2edb31b1965830d35403107facc725",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-spring-shanghai",
  "question_id": "gk-2004-spring-shanghai-q18",
  "resume_action": "取得可追溯同版原卷或明确勘误，核对条件变量；在此之前保留原文与待核答案。",
  "source_id": "src-eda3090af4489c2848005279f9f1f65a561d4fa54daf91ccd574cfbff213be4f",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1266

```json
{
  "affected_paper_ids": [],
  "current_evidence": "独立盲解按对所有允许集合的全称判断选择 B，同时指出固定 M=N 时两命题等价为 C；现稿保留两种条件性结论。原题量词解释尚未核定。",
  "fingerprint": "196af8a3a6e34beadcf634f616731d037f811414e8eaa85a23e53d042f50a8e4",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-spring-shanghai",
  "question_id": "gk-2004-spring-shanghai-q14",
  "resume_action": "取得同版可靠答案、勘误或题意说明，核对全称判断与固定集合解释；在此之前保留两种条件结论及完成阻断。",
  "source_id": "src-eda3090af4489c2848005279f9f1f65a561d4fa54daf91ccd574cfbff213be4f",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1267

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "7b1cd129753dae051f5e2d16f84c962b6502f98e3cdc00c666a9a9b1bb1d4664",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1268

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "c1b50dc6b2983bcea8dd9a33b05b9593fed4ee773af5d400171f9c547198c36e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1269

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "c5ef58a399d89e9b04c30a7ec6eace971630caf2be22b7ab786abb34b203320d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1270

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "76843278f1dc39a27567895b18ddf40fcf48a2d8ad97ba9d6727896b7de314b3",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-spring-shanghai",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1271

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第1页第9题中向量 b 与 (-1,m) 之间未印等号；题面保留原样，解析仅在补入等号的假设下得到条件性结果，原题条件及答案待核。",
  "fingerprint": "550598e0dd05d7c17dbd9563493a19186cd65fd11050bd58d30c4d3aa56e35ac",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-regular-beijing-arts",
  "question_id": "gk-2018-regular-beijing-arts-q09",
  "resume_action": "取得可追溯的原卷或明确勘误，核对第9题向量条件后复核答案；核实前保留原貌和条件性结论。",
  "source_id": "src-7d1c1c70745a459a191b9d84445af35384cd41488151cdd836b110015b0091fa",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1272

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源第9题在向量 b 与坐标之间缺等号；若补入等号可推得 m=-1，但无官方答案或足以确认题意的原卷证据。",
  "fingerprint": "f416f9a743e8644bf47d60188b94229cbd59a3b270bb693ad9d1fde543f25b92",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-regular-beijing-arts",
  "question_id": "gk-2018-regular-beijing-arts-q09",
  "resume_action": "取得可追溯原卷或勘误，确认第9题向量条件后重新核算答案；确认前保持条件性结论。",
  "source_id": "src-7d1c1c70745a459a191b9d84445af35384cd41488151cdd836b110015b0091fa",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1273

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定PDF第1页第16题印“三棱锥 ABC-A1B1C1”，同时题干和配图标有六个顶点；现有证据不足以确认原题几何体名称。",
  "fingerprint": "d4af2ef692f39740a1992892f3c0ced4ad68ba47d83f74bf3713650993172640",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-regular-beijing-science",
  "question_id": "gk-2018-regular-beijing-science-q16",
  "resume_action": "取得可追溯的原卷或明确勘误，核对第16题几何体名称和结构后复核各问；核实前保留原文及条件性推导。",
  "source_id": "src-4396cf65cb605774e43cd50dea8acaa02c88603173808a5d3fa88e52bcf502d4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1274

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第16题解答仅在假设直三棱柱且侧棱长为2的条件下推导；固定源无答案页，原文名称与六顶点图冲突，无法确定无条件答案。",
  "fingerprint": "c913fc7a9b26f3c730540f8cd64254ee944596e810624797246b231ec9963218",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-regular-beijing-science",
  "question_id": "gk-2018-regular-beijing-science-q16",
  "resume_action": "取得可追溯的原卷或明确勘误，核对第16题几何体名称和结构后复核各问；核实前保留原文及条件性推导。",
  "source_id": "src-4396cf65cb605774e43cd50dea8acaa02c88603173808a5d3fa88e52bcf502d4",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1275

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "07d1b425d8c155e8ed71d75b65f0c18b315ffb7d510aa1a9a9643eb0fd792771",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-3-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1276

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "f751bb8fab71ca948c568480aafac13d1cbe3945d91d91b5927730bd66f335fb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-3-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1277

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "12569184d9168d8e5caf818c4dedb56a0f33a01aaf3fd7b9d09640ec98e3ea88",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-3-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1278

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ef31e219230fe485b90b69f4ae49edc2bf203ef10656e30b73f682b7498ccc96",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2018-regular-national-3-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1279

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "a9250be4e7ad79837eca43322e292d67e1938e325590cb386ddb6007e6d96563",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2019-regular-national-3-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1280

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "b424c9bce680ac50f6da53a4dc642e8b2960b11753c61216c03ce58eddf06e6a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2019-regular-national-3-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1281

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "e47f03eb93a782739f24388f6bdfdcef2f045c86a0541e7c6cfcc9b7b46ee28e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2019-regular-national-3-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1282

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "589b1a716194729aee1e46e1022d1f57c8ecd62f7230441c7f96f29ac5f2c73e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2019-regular-national-3-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1283

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定PDF第2页第19题印作矩形，未给定宽长比例；现有解析无来源地附加正方形条件。",
  "fingerprint": "1d726e6068cc17d37399de104aa90932611dc5b7d0439b44d342afc1ef68991d",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-regular-national-3-science",
  "question_id": "gk-2018-regular-national-3-science-q19",
  "resume_action": "取得可追溯原卷或勘误核对第19题矩形边长条件，再复核第（2）问；核实前保留依边长的表达式及待核状态。",
  "source_id": "src-d4cfa7d96fddac79dddeea4aadd9c96efa1cf1371d483b6acd3759eed3516767",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1284

```json
{
  "affected_paper_ids": [],
  "current_evidence": "第19题第（2）问的正弦值依赖矩形边长比；现有数值依赖固定源未给出的正方形假设，无法据此确定无条件数值。",
  "fingerprint": "728bd99f3aa166946f53365ce02501153d75d2f9e09a5166ae71fe220a278e3d",
  "impact": "blocks_completion",
  "paper_id": "gk-2018-regular-national-3-science",
  "question_id": "gk-2018-regular-national-3-science-q19",
  "resume_action": "取得可追溯原卷或勘误核对第19题矩形边长条件，再复核第（2）问；核实前保留依边长的表达式及待核状态。",
  "source_id": "src-d4cfa7d96fddac79dddeea4aadd9c96efa1cf1371d483b6acd3759eed3516767",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1285

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF SHA-256 11b8987221585bfaf21fe3c7785852470a3f50de6ebf91235bac71fecbd1dcfe 的第 1 页（印刷页 2-35）第 8 题题面明确写‘凹多面体’，按其展开图作向内凹入的方锥腔体积计算得到 1−√2/6；同一副本第 3 页参考答案印载 1+√2/6。Chrome 远程调试检索未找到可裁决的同版版本或勘误，且该扫描副本的出版者、版次、来源链及答案官方身份未认证。",
  "fingerprint": "cd0d7728793fe54baa3e5b6be1bc55270d77f9ea3fbf2a6a7bd7381b8b406e04",
  "impact": "blocks_completion",
  "paper_id": "gk-2008-spring-shanghai",
  "question_id": "gk-2008-spring-shanghai-q08",
  "resume_action": "取得可追溯同版原件或可靠正式勘误，核定‘凹多面体’题面与印载答案符号的冲突；此前保留答案 U 与两种证据并列，不改题面、不将副本答案称官方答案，并保持整卷完成阻断。",
  "source_id": "src-66d8e0b462eb08b09996bc94059c5e2083a6a84040cd7167072ede89b8e98a1e",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1286

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF SHA-256 11b8987221585bfaf21fe3c7785852470a3f50de6ebf91235bac71fecbd1dcfe 的第 1 页题面写“凹多面体”，按题面独立推导为 1−√2/6；第 3 页同一副本答案页印载 1+√2/6。未找到可裁决的同版版本或勘误，且答案发布归属与官方身份未核。正式答案保持 U。",
  "fingerprint": "bf0c3af089233a52377f26fe88b2681db4b14113b0a49955ffdb412ff219dde0",
  "impact": "blocks_completion",
  "paper_id": "gk-2008-spring-shanghai",
  "question_id": "gk-2008-spring-shanghai-q08",
  "resume_action": "取得可追溯同版原件或可靠正式勘误，裁定 Q8 的可接受答案；在此之前保持答案 U，不将副本印载值认证为官方答案并阻断整卷完成。",
  "source_id": "src-66d8e0b462eb08b09996bc94059c5e2083a6a84040cd7167072ede89b8e98a1e",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1287

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页印刷页338题14清晰写“若半径为1的圆分别与 y 轴的正半轴和射线 y=√3/3 x (x≥0) 相切，则这两个圆的方程为”。按一个圆同时与两条指定射线相切且切点位于射线上解释，当前只能确定一个候选圆方程；题干所称两个与条件不相符。固定 PDF 只有题面，无答案或勘误，无法确认原题文字是否有误。",
  "fingerprint": "024038cb8fec1e51a608afc97e42998d15c081cffe374d11e10f0c12e3252f04",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-tianjin-arts",
  "question_id": "gk-2006-regular-tianjin-arts-q14",
  "resume_action": "查找并核对同版可靠复本、正式勘误或可追溯的答案材料；未取得可核来源前，Q14答案继续记 U，不补造第二个方程，保留题面原文。",
  "source_id": "src-14a9fbe59a503a78a1e7f2d2cdf99e546574bda3fe11f37a5f17eaee39a4af70",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1288

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页印刷页336第2题写明双曲线焦点为 F1(-3,0)、F2(3,0)，并给出一条渐近线 y=√2x，问“两条渐近线间的距离”；该双曲线另一个渐近线为 y=-√2x，两条直线相交于原点，按直线间最小距离为0，选项却为6√3、4、2、1。固定 PDF 仅有题面，没有答案或勘误，无法确定预期问题或答案。",
  "fingerprint": "f35f501908305998ea7b439e837478987c42f21ba6c86d17eb1fc2decd538cd5",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-tianjin-science",
  "question_id": "gk-2006-regular-tianjin-science-q02",
  "resume_action": "查找并核对同版可靠复本、正式勘误或可追溯答案材料；未取得可核来源前，题面保持原样，Q2答案记 U，不选择不匹配选项。",
  "source_id": "src-634ea48d3fc77ee048d2cf8418a3afb0d6b18c347365c36d8a8e15b53796d307",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1289

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，没有答案或评分材料；Q2 题面与选项冲突，现有可追溯来源不能确认预期答案。答案源因此保留 U。该缺失答案问题与 ISSUE-1288 的题面/选项冲突是不同问题。",
  "fingerprint": "5d4f56e3f15ef2573d84cbfd675059b485fc0c63672dbdcca7296d736a721c3f",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-tianjin-science",
  "question_id": "gk-2006-regular-tianjin-science-q02",
  "resume_action": "取得同版可靠答案或正式勘误；在此之前答案继续记 U，并保留 ISSUE-1288 对题面/选项冲突的记录。",
  "source_id": "src-634ea48d3fc77ee048d2cf8418a3afb0d6b18c347365c36d8a8e15b53796d307",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1290

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "404a3830dde7d88bd8245faf6d6adeb80033aeb2590470403b57d0f3a034231a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-tianjin-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1291

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "e95d460bec70eddef341ab6cfaa43ebc67909881bcc2e4e45ed8c25362c69ee2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-tianjin-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1292

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "ee1755541f5418a3321a5c0fae544fb2fcdbccb360cd803343ee781fba63b5a0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-tianjin-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1293

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "34070094f04a790d59c452167b0df947ff2e8e6e389dd525956bd0db287f5ca4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-tianjin-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1294

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页（印刷页320）第5题给出 a=(1,-2)、b=(-2,4)、c=(-1,-2)，要求 4a、4b-2c、2(a-c)、d 首尾相接构成四边形。前三个向量之和为 (2,12)，故闭合要求 d=(-2,-12)，而四个选项为 (2,6)、(-2,6)、(2,-6)、(-2,-6)，均不符。固定 PDF 仅含题面，未见答案、勘误或可追溯裁决材料。 新增来源线索：EOL 2006-06-12 页面《2006年高考山东卷数学（理）试题答案》的第1页扫描图圈选 D=(-2,-6)（https://www.eol.cn/include/cer.net/gaokao/2006shiti/shandong/shandong_shuxuel_daan1.jpg）。扫描图带“天星 / tesoon.com”水印，但出版者、编者、版次及复制链未核，不能作为裁决；与固定题面推导仍冲突。详见 reports/2006-shandong-science-answer-source-recheck.md。",
  "fingerprint": "2dd203c2f8fdb009be3e781c6781c54a5825e8a0b26a523597ce9e1ee072b55f",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shandong-science",
  "question_id": "gk-2006-regular-shandong-science-q05",
  "resume_action": "取得可追溯的同版可靠复本、正式勘误或其他可裁决材料；此前保留固定题面原文及 U/PENDING，不猜题面或答案。",
  "source_id": "src-58e17c4f7678bc58e38a926d939e980fac0868d781ca9da87efeeed6bf6c6947",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1295

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 仅含试题，未见答案、解析、评分材料或正式勘误；Q5 按固定题面推导与全部选项冲突，现有材料无法确认可用答案。答案层据此保留 U/PENDING。 新增 EOL 历史答案页面及扫描件线索（页面：https://gaokao.eol.cn/huodong/2006zt/200606/t20060612_183252.shtml；扫描图带“天星 / tesoon.com”水印），但无可追溯出版链或官方身份，尚不满足可信答案来源门槛。固定题面 PDF 本身仍不含答案、解析、评分材料或正式勘误；答案保持 U/PENDING。详见 reports/2006-shandong-science-answer-source-recheck.md。",
  "fingerprint": "b38cf6a9cd9edbeabb695251e56acfbfd41f74cbe14075c04afcf2e2706f9cf6",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shandong-science",
  "question_id": "gk-2006-regular-shandong-science-q05",
  "resume_action": "取得具有可信来源链的答案或正式勘误；此前答案继续为 U/PENDING，不推定官方答案。",
  "source_id": "src-58e17c4f7678bc58e38a926d939e980fac0868d781ca9da87efeeed6bf6c6947",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1296

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页（印刷页320）第10题印作 (x^3-i/sqrt(x))^n，第三、第五项系数之比为 -3/14，i^2=-1，并问常数项。由系数比得 n=10；通项 x 指数为 3n-7k/2，常数项要求 k=60/7 非整数。因此固定题面所述展开式不存在常数项，与选项冲突。固定 PDF 仅含题面，未见答案或勘误。 新增来源线索：EOL 2006-06-12 页面《2006年高考山东卷数学（理）试题答案》的第2页扫描图圈选 B=45i（https://www.eol.cn/include/cer.net/gaokao/2006shiti/shandong/shandong_shuxuel_daan2.jpg）。扫描图带“天星 / tesoon.com”水印，但出版者、编者、版次及复制链未核，不能作为裁决；与固定题面推导仍冲突。详见 reports/2006-shandong-science-answer-source-recheck.md。",
  "fingerprint": "30ba5f77c0821e5e70422dcf397044ecbe3bb2abb6bf6c953fc1494b4f41e55a",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shandong-science",
  "question_id": "gk-2006-regular-shandong-science-q10",
  "resume_action": "取得可追溯的同版可靠复本、正式勘误或其他可裁决材料；此前保留固定题面原文及 U/PENDING，不猜题面或答案。",
  "source_id": "src-58e17c4f7678bc58e38a926d939e980fac0868d781ca9da87efeeed6bf6c6947",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1297

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 仅含试题，未见答案、解析、评分材料或正式勘误；Q10 按固定题面推导不存在题目所称的常数项，现有材料无法确认预期题意或可用答案。答案层据此保留 U/PENDING。 新增 EOL 历史答案页面及扫描件线索（页面：https://gaokao.eol.cn/huodong/2006zt/200606/t20060612_183252.shtml；扫描图带“天星 / tesoon.com”水印），但无可追溯出版链或官方身份，尚不满足可信答案来源门槛。固定题面 PDF 本身仍不含答案、解析、评分材料或正式勘误；答案保持 U/PENDING。详见 reports/2006-shandong-science-answer-source-recheck.md。",
  "fingerprint": "fda5cbdaa2116c458e2bff4514278fa55f1d66b099a4303b51530bcd231ff172",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shandong-science",
  "question_id": "gk-2006-regular-shandong-science-q10",
  "resume_action": "取得具有可信来源链的答案或正式勘误；此前答案继续为 U/PENDING，不推定官方答案。",
  "source_id": "src-58e17c4f7678bc58e38a926d939e980fac0868d781ca9da87efeeed6bf6c6947",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1298

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页 Q6 的题干缺少对象名称，规范题面忠实保留该缺失。现有文字不足以确定所谈对象，答案层因此标为 U/PENDING；不能补猜对象或答案。",
  "fingerprint": "1cb9d195295a5b9f14e8488c9586b050157026b5ebf811e288014a3096f31ecf",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q06",
  "resume_action": "取得可追溯的同版完整题面、正式勘误或其他可裁决材料；核明对象后再独立求解并更新题面、答案和逐题 provenance。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1299

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页 Q16 给出边缘概率，但未定义随机变量 ξ，也未给出联合模型；(1)仅在另加独立性假设时可算为0.04，(2)(3)无从确定。题面照录，三问保留 U/PENDING。",
  "fingerprint": "5ea876a56b25253482a97fac81b1410022a9b5c6994359f210ff7397bac99b50",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q16",
  "resume_action": "取得可追溯的同版完整题面、正式勘误或可裁决的变量/联合分布条件；此前不增添独立性假设或填造答案。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1300

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页 Q19 同时要求正项等比数列全体和为9、偶数项子列和为81/5；正公比下偶数项和严格小于全体和，两个条件互相矛盾，依赖该数列的各问无法成立。题面照录，答案保留 U/PENDING。",
  "fingerprint": "63dc2745b7b1b82a0c2ae25b039cd7a2d76e154ddd797c890cbacf27db6d9d32",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q19",
  "resume_action": "取得可追溯的同版可靠复本或正式勘误，核明矛盾条件；在此之前不改题面、不选择任何猜测性答案。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1301

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页 Q20(1)按题面把 x∈[2,4] 代入定义域为[2,4]的 φ(2x)，自变量超出定义域；规范题面照录，答案标 U/PENDING。",
  "fingerprint": "4ea538deedd0d82fd446f4d28f77a114d3577c024095d96db9ff66074808eb0b",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q20",
  "resume_action": "取得可追溯的同版完整题面或正式勘误，核明区间或函数自变量；未核前不改写。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1302

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页 Q20(3)按字面要求从任意给定初值反向求收缩迭代的原像，但题设不保证该原像存在。若无限迭代确实存在，有界性可推出其为不动点；不能据此证明任意初值均可逆推，结论仍为 U/PENDING。",
  "fingerprint": "fa2b8a393c3bc7ffad28c3e6be742446826ab1a1610e6dded3d4eebb24103c1f",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q20",
  "resume_action": "取得可追溯的同版可靠复本或正式勘误，确认迭代方向/存在性条件；未核前保留原文及 U/PENDING。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1303

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页 Q4 按当前转录，四组选项中 A 两命题互不蕴含，B 等价，C 与 D 均为充分不必要；题问所需的必要不充分关系没有对应选项。题面照录，无法判断原卷题干或选项是否有误，答案保留 U/PENDING。",
  "fingerprint": "50bca6a2010f41483437d7322e443044e540e4c03c946e4c66ca04b9fa74bc72",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-jiangxi-arts",
  "question_id": "gk-2006-regular-jiangxi-arts-q04",
  "resume_action": "取得可追溯的同版可靠复本、正式勘误或可裁决答案材料；在此之前不推定应改题干、选项或逻辑方向。",
  "source_id": "src-6eedba8c015f6631959cccdffc0f2b5e63fbc71b424490f1ea554ea6ed7b3be2",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1304

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页 Q8 的比例分层配额应为红4、蓝3、白2、黄1，现有四个选项均不对应该配置。题面照录，无法确定预期答案，答案保留 U/PENDING。",
  "fingerprint": "9b42fd1219dee7cc4fdc0e393530919c97f1953560b8323284614277e8a209e6",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-jiangxi-arts",
  "question_id": "gk-2006-regular-jiangxi-arts-q08",
  "resume_action": "取得可追溯的同版可靠复本或正式勘误以核对选项；未获得前不改写选项或猜选答案。",
  "source_id": "src-6eedba8c015f6631959cccdffc0f2b5e63fbc71b424490f1ea554ea6ed7b3be2",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1305

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，未见答案、解析、评分材料或勘误；Q6 对象名称缺失导致现有条件不足以形成可核答案，答案层保持 U/PENDING。",
  "fingerprint": "e0c987360b950ab4c7763c9b19b97e13a0e67470b8a50dfcc48fcd20b49073c3",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q06",
  "resume_action": "取得可追溯的同版完整题面、正式勘误或可靠答案材料；核明对象并独立求解后再更新。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1306

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，未见答案、解析或评分材料；Q16 未定义随机变量 ξ 且缺联合模型，(2)(3) 无法确定，答案层保持 U/PENDING。",
  "fingerprint": "f4ebf90d3358dea4729dcdd2fafd7a88f8f672c7b09151889abff92a30e9bf7b",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q16",
  "resume_action": "取得可追溯的变量定义、联合分布条件或可靠勘误/答案材料；此前不补加独立性假设。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1307

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，未见答案、解析、评分材料或勘误；Q19 给定正项等比数列总和与偶数项和互相矛盾，依赖该数列的答案均无法成立，答案层保持 U/PENDING。",
  "fingerprint": "a22ad660bac227c3fe42221c3e53b202569970e712531365ad743f49f1f71088",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q19",
  "resume_action": "取得可追溯的同版可靠复本或正式勘误后核明题意，再重算并更新答案。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1308

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，未见答案、解析、评分材料或勘误；Q20(1) 自变量超出所定义域，(3) 未保证任意初值可逆推，未决小问答案保持 U/PENDING。",
  "fingerprint": "e7724168844dc11330260b5b25e9798579432ebbd9425762df7acccbdec53e89",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-guangdong",
  "question_id": "gk-2006-regular-guangdong-q20",
  "resume_action": "取得可追溯的同版可靠复本、正式勘误或可裁决答案材料，核明定义域与迭代存在性条件；此前不猜答案。",
  "source_id": "src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1309

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，未见答案、解析、评分材料或勘误；Q4 按现有选项无符合题问的逻辑关系，答案无法确认并保持 U/PENDING。",
  "fingerprint": "baad0df9895dc583d529b9efdc3094f1e9dc0660a8c0bbba9f07501e3943eb80",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-jiangxi-arts",
  "question_id": "gk-2006-regular-jiangxi-arts-q04",
  "resume_action": "取得可追溯的同版可靠复本、正式勘误或可靠答案材料；未核前不改题干、选项或关系方向。",
  "source_id": "src-6eedba8c015f6631959cccdffc0f2b5e63fbc71b424490f1ea554ea6ed7b3be2",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1310

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 只含题面，未见答案、解析、评分材料或勘误；Q8 四选项均不含按比例分层抽样对应的红4、蓝3、白2、黄1配置，答案无法确认并保持 U/PENDING。",
  "fingerprint": "74ae7155a8b63d3864defb3f2f9ffabee973509991e5fb8da308b6cfc0f6eb3a",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-jiangxi-arts",
  "question_id": "gk-2006-regular-jiangxi-arts-q08",
  "resume_action": "取得可追溯的同版可靠复本或正式勘误核对选项；未获得前不猜选答案。",
  "source_id": "src-6eedba8c015f6631959cccdffc0f2b5e63fbc71b424490f1ea554ea6ed7b3be2",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1311

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "f6a75115d99ffb0f594868b9ef5c9830eb187ff57a40db02535f9d5caa3cf87a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-jiangsu",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1312

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "2cbe6d7ed912273ac62b4e1c679bb13422c286a1ab5fac8531fb226eff55394b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-jiangsu",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1313

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "422efd28-f04f-480b-aaa2-32a211acd5fe",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "9e667a1d7ab4249bc7510dd35aad51a14b813d49cb58f254bf6914f1dd4d8407",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-2006-regular-jiangsu",
  "pdf_sha256": "22677c17c09af0ca8cedf3b4c5dd4335854bea267dc347b501bb7a26c8e213b5",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1314

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1fdf62f6-244a-4261-8c4b-e9900a14e7ce",
  "check_code": "pagination_whitespace",
  "edition": "简答版",
  "figure_id": "visual-review",
  "fingerprint": "0570d0d01aa10c4ea47398484c1fc5d762db4cf1f5d21d6eff9f181947a99335",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2006-regular-jiangsu",
  "pdf_sha256": "bbdefc82a428f4ee1e00d4a6e5071af19715cf524777b14a4ba3dacd0955a247",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1315

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "422efd28-f04f-480b-aaa2-32a211acd5fe",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "c1527c1cdac2312e4524e57ad0e5e9db8b7736941e3edb2589b749455160fbc1",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-2006-regular-jiangsu",
  "pdf_sha256": "93c54492c98bb27c1be75bb81f5ca4f112a48db0428cd39fd248a3e5540a4c9f",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1316

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1fdf62f6-244a-4261-8c4b-e9900a14e7ce",
  "check_code": "pagination_whitespace",
  "edition": "解析版",
  "figure_id": "visual-review",
  "fingerprint": "7f95d8f94231cae76b5d24eff1c5ba806f60799f8e1a4c441da9e4b327810d73",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2006-regular-jiangsu",
  "pdf_sha256": "bb9cfba80a0ec50d7c915a8b5561dabf3449da9534e272e7c6a36bda028493e4",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1317

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "422efd28-f04f-480b-aaa2-32a211acd5fe",
  "check_code": "pagination_whitespace",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "c9381c202486fe89eaabfcff4a3220d2e46afe5d6d4d28478ea21f6f935655de",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 3,
  "paper_id": "gk-2006-regular-jiangsu",
  "pdf_sha256": "c476bdc47c7e2f2a7c901e319ffa901a6c305a2b629a93f97259723ce0cb1523",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1318

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "1fdf62f6-244a-4261-8c4b-e9900a14e7ce",
  "check_code": "pagination_whitespace",
  "edition": "试题版",
  "figure_id": "visual-review",
  "fingerprint": "a12868931f6a7a229cb6be4c2350fea5796bddf7428fe4fe5b8b60604df010ae",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 5,
  "paper_id": "gk-2006-regular-jiangsu",
  "pdf_sha256": "5b9100b5e06e1a4c70af0ca72d02da6ec78e5d6c921dcd26722675aa64947f03",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1319

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选题面 Q17（2）给出 a₁=1、a₂=7，故 T₁=m/7；题设要求对所有 n∈N 有 Tₙ<m/20，取 n=1 即对任意正整数 m 均有 m/7>m/20，与题设矛盾。固定 PDF 仅含题面，未见正式勘误或可追溯裁决材料。",
  "fingerprint": "b1b8564c5da6b701ecd6b72a51cdf356d17a2ad964f034629613888cc824692d",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-hubei-science",
  "question_id": "gk-2006-regular-hubei-science-q17",
  "resume_action": "取得可追溯的同版可靠复本、正式勘误或其他可裁决材料；此前保留固定题面原文及 U/PENDING，不猜题面或答案。",
  "source_id": "src-3e4d37728fe026360081acff678b849c40c747cd67ac478230a0040ead794c42",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1320

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 仅含题面，未见答案、解析、评分材料或正式勘误；Q17（2）按题面推出的 T₁=m/7 与约束 T₁<m/20 矛盾，现有材料无法确认该问的预期题意或答案。答案层据此保留 U/PENDING，official_answer 为空。",
  "fingerprint": "4bb1ae1c7fed2ccf533eb0a8c124cd845204a8ffef0539019ed4f4f9ea6d5a25",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-hubei-science",
  "question_id": "gk-2006-regular-hubei-science-q17",
  "resume_action": "取得具有可信来源链的答案或正式勘误；此前答案继续为 U/PENDING，不推定官方答案。",
  "source_id": "src-3e4d37728fe026360081acff678b849c40c747cd67ac478230a0040ead794c42",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1321

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第1页（印刷页55）第23题（3）印作‘证明：面 AED 面 A1FD1’，两平面名之间未印关系符号。独立题面复核确认这是固定副本原件缺项，不是转录漏字；不依据可证出的垂直关系补猜原题。",
  "fingerprint": "b479ae57e23ac3a2f7c7fb44693f4ca4430c9bba2153f2c252e72a8b812798fb",
  "impact": "blocks_completion",
  "paper_id": "gk-1997-regular-national-arts",
  "question_id": "gk-1997-regular-national-arts-q23",
  "resume_action": "取得可追溯的同版完整题面或可信勘误；此前保留【原卷缺关系符号】占位及原题其他文字，不补猜关系。",
  "source_id": "src-c2f96b8723b85758e1407771ee05f1bb5c457c71a0bc567c01f84ea8c3fadbd9",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1322

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q23（3）缺少待证关系符号，现有独立解析只能提供条件推论，不能给出该小问的无条件答案；答案要点明确标为未决，official_answer=null。",
  "fingerprint": "540f6c05a1c91809fc80ebde8b47b3c8e2a434b589f35c8b585621d4d46ae68a",
  "impact": "blocks_completion",
  "paper_id": "gk-1997-regular-national-arts",
  "question_id": "gk-1997-regular-national-arts-q23",
  "resume_action": "取得可裁决题面关系符号的同版来源或可信勘误后再求解并复核；此前 Q23（3）答案保持 U/PENDING。",
  "source_id": "src-c2f96b8723b85758e1407771ee05f1bb5c457c71a0bc567c01f84ea8c3fadbd9",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1323

```json
{
  "affected_paper_ids": [],
  "current_evidence": "Q10 原题按固定扫描字面为“EF 与面 AC 的距离”，无法据文字确定“面 AC”对应的完整平面；图稿不补猜关系。",
  "fingerprint": "b951127a666830d77741262fb3e8015a9ba5ff4b09f7d88eca0a6859aee9bcb7",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-guangdong",
  "question_id": "gk-1999-regular-guangdong-q10",
  "resume_action": "取得可核验的同版完整题面、勘误或更清晰原页，确认该距离所指平面；此前题面保留字面，答案维持 U。",
  "source_id": "src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1324

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定副本 A 型答案栏印 Q10 为 D，但题面几何条件指称不全，无法独立推导或确认体积答案。",
  "fingerprint": "82574256c208a68cfc0267a193cecbc400d614743056a905532fbcb7a7ee7dfe",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-guangdong",
  "question_id": "gk-1999-regular-guangdong-q10",
  "resume_action": "取得可以消除 Q10 几何歧义的同版完整题面或可靠勘误，再独立复算答案；此前不把源内 D 作为已验证答案。",
  "source_id": "src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1325

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面定义右焦点为 F1，却随后写“经过 F”，并在句尾重复“的距离，则椭圆的离心率是”；扫描字形可辨但原意未明。",
  "fingerprint": "3b55183be1a454cc492739c132aa9c9d47427b10ec8c27e0c6e11e50af357068",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-guangdong",
  "question_id": "gk-1999-regular-guangdong-q13",
  "resume_action": "取得可追溯的同版题面或勘误，确认 F 与 F1 及重复句的原文；此前照录并保留标疑。",
  "source_id": "src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1326

```json
{
  "affected_paper_ids": [],
  "current_evidence": "e=1/2 只在将题面的 F 解释成 F1 时成立；固定 A 型答案栏的 1/2 不能消除题面文字歧义。",
  "fingerprint": "512a85502942be27dcb8aeeda57e7eb03e7df6e4e1ac703a62a5845f9ba4cc75",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-guangdong",
  "question_id": "gk-1999-regular-guangdong-q13",
  "resume_action": "取得可靠来源确认题意后再将条件推导判为最终答案；此前答案保持条件性。",
  "source_id": "src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1327

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面字面为 x(x_n)=n，小问（Ⅰ）为“x1、x2x 和 xn”；两处均可辨但原意未明。",
  "fingerprint": "5939f9ec6766cc1b89e7fe23ca5e2fb613182ee9581425999fafe6efd897553c",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-guangdong",
  "question_id": "gk-1999-regular-guangdong-q21",
  "resume_action": "取得可追溯的同版题面或勘误确认函数记号与小问列式；此前保留原字样和待核标记。",
  "source_id": "src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1328

```json
{
  "affected_paper_ids": [],
  "current_evidence": "数列及函数答案依赖将原文条件性复原为 f(x_n)=n，不能据此认定为原题无条件答案。",
  "fingerprint": "7c0313ab8b334625afa7fbcf08ed7b6546a0a5a7314e4e67a82e2758984b7ca4",
  "impact": "blocks_completion",
  "paper_id": "gk-1999-regular-guangdong",
  "question_id": "gk-1999-regular-guangdong-q21",
  "resume_action": "取得可靠来源确认定义和小问内容后再复核数列、极限、分段式及定义域；此前仅保留条件答案。",
  "source_id": "src-3ad60523830b820fe8f81c5fdba2bda567b74a0b40597731f417050de3b7c019",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1329

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "73bf412ac2b0f4d21a3e5472f50ea4a857dc6297b8415109cd0de0d0fc970c58",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1330

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "77dd71244c4ab2a0cd9332f2adb38414bb18694e0f8155e6f80dec3e3f625c06",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1331

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "e342ba5b087b92e164e4c2bb676d9d17cac5d1e3719c5d23c2098ec9e7be1528",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1332

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "905aedf5476c5a039b335793a972584747339e071467dc5929bbf02048bf08d9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-1997-regular-national-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1333

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第1页 Q12 只给每人出现发热反应的边缘概率0.80和人数5，未声明个体反应相互独立或给出联合模型。完全同动且边缘概率均为0.80时，至少3人发热的概率为0.80；独立模型下为0.94208，精确到0.01为0.94。故边缘概率不足以唯一确定题目所求，答案保持U/PENDING；0.94仅为独立假设下条件值。",
  "fingerprint": "5e5047efe733503125a26a82ccd7f8ac4a2eb67cd18607bcdab7e14fa3546026",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-hubei-arts",
  "question_id": "gk-2006-regular-hubei-arts-q12",
  "resume_action": "取得可追溯的明确独立性条件、正式答案/勘误或其他可裁定材料；此前保持Q12为U/PENDING，不把二项独立假设当作原题条件。",
  "source_id": "src-af4cc84c7c2f6c2c1ed0bef598d5a51f57d65a1b25926d7a02631cc6c5387d75",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1334

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "63ce19bcc0b9417e2ab80791b7d07396c15d8b12d78d14732ba78c1a0a5f3e02",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-hubei-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1335

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "30b67046ca56b3530fa0b1f44d5599e103fd77441e62723baaa3331b7e259955",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-hubei-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1336

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "28f933fc086ed1b886cdd5bc1f5ed16d04917a076fec75417a7494279955672f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-hubei-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1337

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "5c2c5e475c8f65cc4ecb9c7d0e969d8dbaa401b668a1e6377992cc8c3df3d45b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-hubei-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1338

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面第17题只说明“每家煤矿安检是否合格是相互独立的”，但未明确不同煤矿整改复查结果的联合独立关系。至少关闭一家煤矿的概率不能仅由单家复查边缘概率推出；0.41 仅在把独立性扩展到初检及复查结果时成立，规范答案保留 U/PENDING。",
  "fingerprint": "121d2b229e6d2bc6044cc74cff00af213e572151728143081c94df284bbbd4b3",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-hunan-arts",
  "question_id": "gk-2006-regular-hunan-arts-q17",
  "resume_action": "取得可追溯的明确跨矿复查独立性条件、正式答案/勘误或其他可裁定同版材料；此前保持第17题（3）为 U/PENDING，不把 0.41 写成无条件答案。",
  "source_id": "src-6387f1664484c2d0ee3ea1a27f673d6624df685f465bfd701fb8e95c0a8b856d",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1339

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第 1 页 Q17 给出整改前合格概率 0.5、整改后复查合格概率 0.8，并称每家煤矿安检是否合格相互独立；题干未明确该独立性是否覆盖不同煤矿整改复查结果及其与初检结果的联合关系。至少关闭一家只有在关闭事件独立时才能由 1-0.9^5 算为 0.41。",
  "fingerprint": "af0e2c3aa8587fa8c0414de09fdc38670c9206e6f74cb9827079d89d082392bc",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-hunan-science",
  "question_id": "gk-2006-regular-hunan-science-q17",
  "resume_action": "取得同版权威答案、勘误或明确适用于整改复查阶段的跨矿联合独立性材料后裁定；此前保留 Q17（3）为 U/PENDING，不把 0.41 写成无条件答案。",
  "source_id": "src-74bd6a8b302120c812e3aa287309cf3d3a0cf6217761cc4637696bf4d12817cb",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1340

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源 PDF 第2页 Q21(2) 印作“四边形 APCD”，但此前定义的点只有 A、B、C、D，未说明 P；当前只确认固定副本字面，无法判定 P 是否为排印错误。",
  "fingerprint": "37828a86e1df7bda6ad37e632e9ed187eb01f2a8f2e329e11cc79587c4396aa7",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-liaoning-arts",
  "question_id": "gk-2006-regular-liaoning-arts-q21",
  "resume_action": "取得可追溯的同版完整复本、正式勘误或其他能说明 P 定义的可靠材料后再裁定；此前保留 APCD 原字样和 U/PENDING，不推测改为 ABCD，也不据此求 a,d。",
  "source_id": "src-b784613ebc50375b17eb4a91083b447879ebb9ed75bb6a76227bb74345cfbfd3",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1341

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选源 src-5abd831561d7d4fa968c5bf0deb634e0d666376fd8cc90967cf30d301e77a351（SHA-256 211d79b8676187c7e4a98c71d7eae5eadd28b2e5aaf9237fefd55a791241faa3，上游 commit 34c13a6cf632c0b69c95f89b9b923bbc4a08924d）第2页 Q20(1) 印作 b²>4(a−1)。中国教育在线 2006-06-09 题面分页影像（https://gaokao.eol.cn/huodong/2006zt/200606/t20060609_182836.shtml；第5页图 https://www.eol.cn/include/cer.net/gaokao/2006shiti/chongqing/chongqing_shuxue5.jpg）同题印作 b²>4(c−1)。该转载影像不能确认官方性、版次或与固定源的版本关系；固定题面照录 a，答案与解析保留 U/PENDING。",
  "fingerprint": "3c2a52e3a97e95482ac046a78a9752396fc546d07e15a3b76aa372c87195284a",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-chongqing-science",
  "question_id": "gk-2006-regular-chongqing-science-q20",
  "resume_action": "取得可追溯的同版勘误或独立题面版本，确认 Q20(1) 条件中的字母；在证据出现前保留原印 a 与 U/PENDING，不推测改为 c，也不据此补解。",
  "source_id": "src-5abd831561d7d4fa968c5bf0deb634e0d666376fd8cc90967cf30d301e77a351",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```
## ISSUE-1342

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面只给等差数列 a₁+a₈=8 并询问 S₉。满足条件的正项数列 (a₁,d)=(4,0) 与 (1/2,1) 分别给出 S₉=36 与 81/2，条件不足；答案与解析保留 U/PENDING。",
  "fingerprint": "953546783cd2d8b9111445674e7bec8c886d0d7686cd3e497da7e27420ab41e2",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shaanxi-arts",
  "question_id": "gk-2006-regular-shaanxi-arts-q03",
  "resume_action": "取得可追溯的同版题面、勘误或能确认遗漏条件的独立材料；此前保留 U/PENDING，不从选项反推条件或选择唯一答案。",
  "source_id": "src-d3bb569fc2c589e075c748b1494aaadeaae67bbe0e3926306e123e08de2a5fec",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```
## ISSUE-1343

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原页可见字样“甲和乙不同去”，转录已按原字保留；这句话的选派语义不能唯一确定，可能对应不同计数条件，答案与解析保留 U/PENDING。",
  "fingerprint": "8cd9625c739725aa257773f956e227e3545e9a8512bb17e8004e2c4148ef61f3",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shaanxi-arts",
  "question_id": "gk-2006-regular-shaanxi-arts-q15",
  "resume_action": "取得可追溯的独立题面或明确勘误，消除“甲和乙不同去”的语义歧义；此前不按猜测确定选派关系或方案数。",
  "source_id": "src-d3bb569fc2c589e075c748b1494aaadeaae67bbe0e3926306e123e08de2a5fec",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```
## ISSUE-1344

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面原句为“甲和乙不同去”，文字可辨但语义存在歧义；答案与解析保留 U/PENDING，不据猜测给方案数。",
  "fingerprint": "2d55adf0d59ada3a4429215043c9dc0e4cf839656911972f32f8a3aecf76ca3b",
  "impact": "blocks_completion",
  "paper_id": "gk-2006-regular-shaanxi-science",
  "question_id": "gk-2006-regular-shaanxi-science-q16",
  "resume_action": "取得可追溯的独立题面或明确勘误，消除“甲和乙不同去”的语义歧义；此前保留原字，不推断选派关系或给唯一方案数。",
  "source_id": "src-6914e1c400640e0c3ef3785cb187876891213e18557a04ba0e97c2f4dae5a999",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1345

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "cd51753fcbe21682f7ba36bddd5e3dcd22f5308042540fb8f31f35a8d430aa6e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1346

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "b22f5ab7f7ee8529e4cf074b80b0259c2a7dc83a335459f442da12559003fb14",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1347

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "264c64ca5f7fedd9d6f4774d2896e29df4cb7cf7ca78492c899afce91c19bd53",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-chongqing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1348

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "271329074a0bde6d20255433bf8db8e65c55b6c1ce6e566e6b7a5ed6de0db034",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-chongqing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1349

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "8fdf13aa11cb544b8f0c1e3ad7b2f4d6f75dd2eed204a906ec5ca0dcdc03ad2e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-chongqing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1350

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "dd593622199707c9b912b631eefa583414c82f68a663c9e11a05fb5942d72ce6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-shaanxi-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1351

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "991832fbe92a52714083872dc454fec6435c3135170eea7c3864ec89b4ea51c4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-shaanxi-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1352

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "ada84511dbbda508767c402cc3b461cd69642a8de1e7e12e6d44259ca0c79488",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-shaanxi-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1353

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "fb09d8d58be1c0df5f9e680d0629fe41b0ad21ddc5cd03e3e9cb01f28f409187",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-shaanxi-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1354

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "c9500666c313b51fc89b836e1bd484869cfa098cb4933fb9da0f282a3db08bbe",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2006-regular-shaanxi-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1355

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定来源 PDF 第2页 Q18 说明沿线11站包括起点站、6位乘客在起点站之外各站下车等可能；未说明六位乘客的选择联合独立。相同的均匀边缘分布既可对应独立模型，也可对应所有乘客共用一个均匀站点的完全相关模型，两个所求事件概率因此不唯一。189/1250 与 729/50000 仅在额外的乘客间相互独立假设下成立；规范答案两问均为 U/PENDING。",
  "fingerprint": "e4ea458412933cd6bdebaa9c760d9e92bb1b7bd84c73b27d534d6b17fc94184b",
  "impact": "blocks_completion",
  "paper_id": "gk-2007-regular-beijing-arts",
  "question_id": "gk-2007-regular-beijing-arts-q18",
  "resume_action": "取得可追溯的同版材料，明确六位乘客下车选择之间的联合独立性，或取得可裁定的正式答案/勘误；此前保持 Q18 两问为 U/PENDING，不将独立模型条件值写作无条件答案。",
  "source_id": "src-71817304e261efb7deaf51c2a5f400421a95ac91a90313d8f558bee701a624f9",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1356

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "ef275e3b36743cedae97feb6a6234dc067fa1ceea9094f49460249731de966b9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1357

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "b8dc9050e33f4484b7be4723bb2488d3b9d340fefcabac7360e5a648aaf8291f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1358

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "6c88f6b3a788dda349fe7105084498ef5ce1f300b75fb98bb710cce8dd6b9dfe",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1359

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ad4fad8905bed95f54cc2bbf45cece7809505801fab52747df9604566de7cf86",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1360

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面原式为 x^2+y^2-2x-2y+8=0，配方得 (x-1)^2+(y-1)^2=-6，实数范围内无圆上点；题目所称圆、切点及面积因而无法定义。固定 PDF 不附答案页或同版勘误。题面逐字保留，答案 U/PENDING，未推测或改写系数。",
  "fingerprint": "1bb8735af0506b236f6ecae5d4d2d0aafdb78f7a86ffc3b71f1b30cbe9dfdaf7",
  "impact": "blocks_completion",
  "paper_id": "gk-2002-regular-beijing-science",
  "question_id": "gk-2002-regular-beijing-science-q16",
  "resume_action": "取得可追溯的同版勘误或更强来源后，核定原题意并重算；在此之前保持题面原式、U/PENDING 与 blocker。",
  "source_id": "src-6b6e5d61614e04d9b61330de2c085ab84c2f6fddfca9e6f357695a7ba074e690",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1361

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 的 Q19 开头及第（3）问称数列为 {a_n}，递推式、前两问和所求极限均使用 x_n；独立转录复核确认这组符号差异确为原件印文。按原文保留，未将 {a_n} 改写为 {x_n}；依据递推可证明 x_n 的极限为 √a，但无法确认题面预期符号。",
  "fingerprint": "9a8b808b35f1ee16fa5f0f34380627b0e4b7c05c42fce190970a91208a8c444f",
  "impact": "blocks_completion",
  "paper_id": "gk-2002-regular-beijing-science",
  "question_id": "gk-2002-regular-beijing-science-q19",
  "resume_action": "取得可追溯同版勘误或权威同版材料核明数列符号；未核前保留原印文与针对递推数列 x_n 的条件性结论，并保持问题未决。",
  "source_id": "src-6b6e5d61614e04d9b61330de2c085ab84c2f6fddfca9e6f357695a7ba074e690",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-1362

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题首将满足 a^2=b^2+c^2、a>0、b>c>0 的一般曲线定义为果圆；第（1）问另加等边焦点条件，而第（3）问仅称 P 为果圆上任意一点，没有明确是否承接该特例。一般参数读法下，令 t=c/a：0<t<=1/2 时最小横坐标为 -c 与 a；1/2<t<1/sqrt(2) 时为 a^2(a-c)/(2c^2)。若承接（1）的参数，则横坐标为 7(sqrt(7)-sqrt(3))/12。固定 PDF 仅有题面，无答案、解析或勘误页可裁定本问参数作用域；规范答案和解析均保留 U/PENDING。",
  "fingerprint": "bcd8d5c1e1843d0a680cd2a8dcab57c9c5a169a7e6527ca23ce1a237884c5a0f",
  "impact": "blocks_completion",
  "paper_id": "gk-2007-regular-shanghai-arts",
  "question_id": "gk-2007-regular-shanghai-arts-q21",
  "resume_action": "取得可追溯的同版答案、解析或勘误以明确 Q21(3) 是否承接（1）的等边焦点条件；在此之前保留两种条件结果和 U/PENDING，不把特例写成一般答案。",
  "source_id": "src-51aa9840dc7a866be37ded966d4a337c999cacd912ce0118e07b3e6c768c5789",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1363

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第 2 页（印刷页 73）Q21 印作 y=2000(a/10)^2，不含 x；按常值函数字面解释与“函数图象”及（3）问存在最大项数的设问冲突。新浪 2000-07-11 同期答案/评分副本按指数 x 推导，但页面未证明发布链、官方身份或与固定 PDF 同版。题面照录，Q21 答案保留 U/PENDING。",
  "fingerprint": "ca7878be3e1caaa7f4548f2522cae934e19f95cd88c4e0cd31369a2fe7d3c893",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-shanghai-arts",
  "question_id": "gk-2000-regular-shanghai-arts-q21",
  "resume_action": "取得可追溯且能与本卷版本绑定的原始出版页、正式答案或勘误；核实指数后再更新题面/答案与三角色 provenance。未取得前保持固定印式照录、U/PENDING 和 blocks_completion，不将同期副本当作官方裁定。",
  "source_id": "src-8d14b1f9f511665ea10dbda45959a3b445a17806415be6b034f816bec663d7f5",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1364

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 PDF 第 2 页（印刷页 73）将函数写为 y=2000(a/10)^2，未出现 x；按字面为常值函数，而同期未认证、未证同版副本按 x 指数解释，现有证据无法判定原题所需变量与答案约定。固定答案层 Q21(1)–(3) 保留 U/PENDING。",
  "fingerprint": "5b012906b10a75e4b9036b0d67887f9469e96a555ff2211b8857ef949580377b",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-shanghai-arts",
  "question_id": "gk-2000-regular-shanghai-arts-q21",
  "resume_action": "取得可追溯且能与本卷版本绑定的原始出版页、正式答案或勘误，确认 Q21 指数变量；在此之前保留题面字面式与各问 U/PENDING，不用未经绑定的同期副本裁定。",
  "source_id": "src-8d14b1f9f511665ea10dbda45959a3b445a17806415be6b034f816bec663d7f5",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1365

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "e4f59b15f3c22a784cf78b64b9baab2e3fd5b2c562dc3ca036cef4966df0a66f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1366

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "dc3f1367ecbde5ca017a0ec037b0d1103b528d2ce20bb0154a871deb8dcbaa2d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1367

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "baa54ff3ee08efecaf35699fbe7f82ee5200431f3d129f969703bd8f0af82556",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1368

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "f702d245c1700d2da082f72546908d660b073ca0cea9eb06400f2aa2896e4480",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1369

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页 Q12 在300 dpi原页及局部放大均读作“等此数列”，未发现答案或勘误页。“等此数列”无法确定数列类型；若条件性假设为等比数列可以推出乘积恒等式，但这不能证明源字或本题原意。",
  "fingerprint": "8fbecaaadd8614cf771e6e8aaa4bc9c9359fd0634876cc14ddbdae6fea9039b0",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-shanghai-science",
  "question_id": "gk-2000-regular-shanghai-science-q12",
  "resume_action": "取得可追溯的同版清晰副本、勘误或可靠同期材料，核定 Q12 原字及数列类型；此前按固定 PDF 保留“等此数列”，答案维持 U/PENDING，不按惯用表述替换。",
  "source_id": "src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1370

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页 Q21 函数排印指数清楚为数字2。按字面，等腰条件给 a_n=n+1/2、b_n=20a^2；Q21（2）允许全部 0<a<10，最小整数 a=1 时 B_n=20^n 严格递增，没有最大项，与（3）设问不相容。固定 PDF 未附答案、解析或勘误页。",
  "fingerprint": "05ee88924d958a85ff7db0bcf5f720bdc891c568c5f8e57e8c5910bb44fe17ae",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-shanghai-science",
  "question_id": "gk-2000-regular-shanghai-science-q21",
  "resume_action": "取得可追溯的同版答案、解析、勘误或可靠同版副本，确认 Q21 是否存在原卷印刷或版本差异；此前保留指数2并按字面说明无最大项，整题答案保持 U/PENDING，不推测替换成 n。",
  "source_id": "src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1371

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第1页 Q12 在原页及局部放大均读作“等此数列”，固定副本没有答案、解析或勘误页。转录按字面通过，但无法据此确定 b_n 的数列类型和确定答案；“若为等比数列”的乘积式仅属条件性推导，不作为答案。",
  "fingerprint": "eac81cb1071c79f3385d531f1ad7763b7973531daca8cb6824439c2a4022ee70",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-shanghai-science",
  "question_id": "gk-2000-regular-shanghai-science-q12",
  "resume_action": "取得可追溯的同版清晰副本、答案、勘误或可靠同期材料，核定 Q12“等此数列”对应的数列类型；此前按原页字面保留题面，答案维持 U/PENDING，不以常见术语补字。",
  "source_id": "src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1372

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页 Q21 的函数指数清楚印为2；按字面推导后（3）不存在最大项。固定 PDF 没有同版答案、解析或勘误，无法核定原卷版本是否存在排印差异或预期指数约定。题面照录2，确定答案暂缺。",
  "fingerprint": "d7ce4a294bc7e8c9ab36c9b1efa7204479109793845b97ecb993caf36cd9a086",
  "impact": "blocks_completion",
  "paper_id": "gk-2000-regular-shanghai-science",
  "question_id": "gk-2000-regular-shanghai-science-q21",
  "resume_action": "取得可追溯的同版答案、勘误或可靠同版副本，核定 Q21 指数2是否为本版预期题意；此前按固定原页保留指数2，整题答案维持 U/PENDING，不推测改为 n。",
  "source_id": "src-b46bf909434f6686413681f206c6f1c3566760d6e574f4799dc8b1e0658f9ee8",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1373

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "f2da91f802ab20134b4426d405498fc644a0d07da07375f056686d803b45f425",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1374

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "03fea737a6865780bf54af06b6f1bdfaffe322bf1afface27ab37bd9822d6ae0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1375

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "f33e8c90f0649a186c083e41f93729441047d0f42a0ea6086975d6eb05af8107",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1376

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "eeed23c933dedc0252b976a8163a04cb458c0c15d66c5a7fc5c207e14797bde4",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2000-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1377

```json
{
  "affected_paper_ids": [],
  "current_evidence": "Q12表面积计算表明四棱柱严格小于三棱柱时0<a<sqrt(5/3)，a=sqrt(5/3)时两者并列最小；固定题面只写“四棱柱全面积最小”，未说明是否允许并列或要求唯一最小，端点结论不能无依据裁定。",
  "fingerprint": "b6c9e5411e2bb5dc2805bb668938734589defc7579fd34765eb178c702a5faeb",
  "impact": "blocks_completion",
  "paper_id": "gk-2005-regular-shanghai-arts",
  "question_id": "gk-2005-regular-shanghai-arts-q12",
  "resume_action": "取得可追溯同版答案、解析或勘误以确认“最小”是否允许并列；在此之前保留U/PENDING，不替来源补充唯一性条件。",
  "source_id": "src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1378

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原页Q20(1)清楚印作“中低价层”，与题目前文及第(2)问的“中低价房”冲突。题面照录来源；仅按“房”解释时条件计算为2013年底，不能据上下文静默改字并冒充确定答案。",
  "fingerprint": "7809e71ee548c3038ed5b21f5d4046e6d2e1561ecdfb622cf7dc133450cbd632",
  "impact": "blocks_completion",
  "paper_id": "gk-2005-regular-shanghai-arts",
  "question_id": "gk-2005-regular-shanghai-arts-q20",
  "resolved_evidence": "固定 PDF 原页清楚印作“中低价层”，规范题面已忠实照录；字形转录本身无歧义。答案能否按上下文解释为“中低价房”属于解释/答案约定未决，另由 ISSUE-1379 阻断。",
  "resume_action": "核对可靠同版印本、勘误或可追溯官方说明，确认“层”是否为原字或误植；在此之前保留原文及U/PENDING，条件结果不得写成确定答案。",
  "source_id": "src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846",
  "status": "resolved",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1379

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原页 Q20(1) 清楚印作“中低价层”，与前文及第(2)问“中低价房”冲突。题面忠实照录；仅在按“房”解释时条件计算为2013年底，现有证据不能裁定原题意。",
  "fingerprint": "e1e23364a33286802a5685b59675ec7483c567bc6552e869be78f4e2db8e6569",
  "impact": "blocks_completion",
  "paper_id": "gk-2005-regular-shanghai-arts",
  "question_id": "gk-2005-regular-shanghai-arts-q20",
  "resume_action": "取得可追溯同版答案、勘误或可靠说明以确认“中低价层”是否应按“中低价房”解释；在此之前将 Q20(1) 保留 U/PENDING，条件性年份不写为确定答案。",
  "source_id": "src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1380

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q11 给出两种相同直三棱柱，高为 2/a，底边为 3a、4a、5a，并称“全面积最小的是一个四棱柱”。按表面积比较，最佳四棱柱与三棱柱面积差为 12a^2-20；a=sqrt(5/3) 时两类并列最小，题面未说明是否要求唯一最小。",
  "fingerprint": "b51e2e4671dc178fbeedd3f9bbb74e044e3f7eec5b4283dce5b05b4f4fbf04bd",
  "impact": "blocks_completion",
  "paper_id": "gk-2005-regular-shanghai-science",
  "question_id": "gk-2005-regular-shanghai-science-q11",
  "resume_action": "取得可追溯同版答案、解析或勘误以确认“最小的是一个四棱柱”是否要求唯一最小；在此之前保留 U/PENDING，不替来源补充唯一性条件。",
  "source_id": "src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1381

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q20(1) 清楚印作“中低价层”，与前文及第(2)问“中低价房”不一致。只有按“房”解释时累计面积的条件计算结果才是 2013 年底，现有证据不能确定原题意。",
  "fingerprint": "8316b7dbaea5b4ffcaa77cc1bf273396dd462f1e12fd8158ace966eff550a17f",
  "impact": "blocks_completion",
  "paper_id": "gk-2005-regular-shanghai-science",
  "question_id": "gk-2005-regular-shanghai-science-q20",
  "resume_action": "取得可追溯同版答案、勘误或可靠说明以确认“中低价层”是否应按“中低价房”解释；在此之前将 Q20(1) 保留 U/PENDING，条件性年份不写为确定答案。",
  "source_id": "src-22a421a422f050bc84accae7bf41feb6903c62df04bd83f34d8267d28f49ee2e",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1382

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "ea75375550d0ee904d8020d68935e90df84e9b62777f411f95fa72a87ab9f6ee",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1383

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "1392581c067b583d4707f59e2bf3ea11a0db97eb278d6e9bbc0b8bc93320efa0",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1384

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q17 给出复数条件 (1+i)z1 = -1+5i 与 z2 = a-2-i，并要求 |z1 - z2| < |z1|。代数化简得 (a-4)^2 < -3，在实数范围内无解。部分外部版本作 |z1/z2| < |z1|（对应 a != 2）。因固定原卷字面确为减号，原题条件在实数范围内无解。",
  "fingerprint": "9a9a56a5131e2b62e70a6be070afb1e5862f95158628e2862612c9adaa8b4f99",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-regular-shanghai-arts",
  "question_id": "gk-2004-regular-shanghai-arts-q17",
  "resume_action": "取得可追溯官方权威答案、评分标准或同期勘误以确认原题是否为除法或确系无解试题；在此之前将 Q17 保留 U/PENDING，不擅自修改题面符号。",
  "source_id": "src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1385

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q19 题干定义函数 g(x) 的定义域为 D，但在第 (2) 问提问中印作“若 B ⊆ A，求实数 a 的取值范围”，题面通篇未定义集合 B。若按常理将 B 视为 g(x) 的定义域 D 则可解得 a <= -2 或 1/2 <= a < 1。",
  "fingerprint": "cdad28bd43a5bd39e94c9d52274bf003dbf10622c22b01762a9a401e1cc02529",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-regular-shanghai-arts",
  "question_id": "gk-2004-regular-shanghai-arts-q19",
  "resume_action": "取得可追溯官方试题、同版答案或勘误确认原题第 (2) 问集合符号；在此之前将 Q19(2) 保留 U/PENDING，条件性解集不写为确定结论。",
  "source_id": "src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```


## ISSUE-1386

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q19 题干定义函数 g(x) 的定义域为 D，但在第 (2) 问提问中印作“若 B ⊆ A，求实数 a 的取值范围”，题面通篇未定义集合 B。若按常理将 B 视为 g(x) 的定义域 D 则可解得 a <= -2 或 1/2 <= a < 1。",
  "fingerprint": "c6d0171ae9dc54b482b7016de640062becff58c1b7bb29340667338e8930dbf8",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-regular-shanghai-science",
  "question_id": "gk-2004-regular-shanghai-science-q19",
  "resume_action": "取得可追溯官方试题、同版答案或勘误确认原题第 (2) 问集合符号；在此之前将 Q19(2) 保留 U/PENDING，条件性解集不写为确定结论。",
  "source_id": "src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```
## ISSUE-1387

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面 Q22(1) 印载点 P1(3, 0)，代入椭圆方程 x^2/100 + y^2/25 = 1 得 9/100 != 1，点 P1 不在椭圆上。若依字面 a1 = 9 与 S3 = 255 推算得 a3 = 161，超出椭圆上点到原点距离平方的最大值 100，在实数范围内无对应曲线上的点 P3。",
  "fingerprint": "492d9f8ef3d71a97ee1330849f61d61a392e5ec65ec61664a062b28d0d3add47",
  "impact": "blocks_completion",
  "paper_id": "gk-2004-regular-shanghai-science",
  "question_id": "gk-2004-regular-shanghai-science-q22",
  "resume_action": "取得可追溯官方权威真题、答案或勘误以确认 Q22(1) 椭圆方程或点 P1/S3 之字面；在此之前将 Q22(1) 保留 U/PENDING，不擅自修改题面数值。",
  "source_id": "src-f8969b851ca75536af43f98ea865a04b66de9068f24bdec2c3790cd1351bed0a",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1388

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面在Q14列出四个判断条件，但没有声明平面 α 与 β 互异。严格将面面平行定义为两平面无交点时，选项 D 只能推出两平面方向相同，仍允许 α=β；其余选项不足以推出平行。固定 PDF 仅含题面，无可追溯答案、勘误或评分页据以裁决，因此题面下的答案仍为 U/PENDING；若另行假定两平面互异，预期选项 D。",
  "fingerprint": "03104f7445d4f00aa81826249d7fd6ff926cd39db26b0f6f16b3e0e525505e60",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-shanghai-arts",
  "question_id": "gk-2003-regular-shanghai-arts-q14",
  "resume_action": "取得可追溯的同版答案、勘误或考试编写约定，确认“平面平行”是否包含重合或是否默认 α≠β；据新证据重新判断 Q14。在此之前保持 U/PENDING，不把预期选项 D 写成确定答案或官方答案。",
  "source_id": "src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1389

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面在Q14列出四个判断条件，但没有声明平面 α 与 β 互异。严格将面面平行定义为两平面无交点时，选项 D 只能推出两平面方向相同，仍允许 α=β；其余选项不足以推出平行。固定 PDF 仅含题面，无可追溯答案、勘误或评分页据以裁决，因此题面下的答案仍为 U/PENDING；若另行假定两平面互异，预期选项 D。",
  "fingerprint": "c1d30cac22494ed065227e8fdb45850cafe8e39f1d7f81ceb0a5638524da4cbc",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-shanghai-science",
  "question_id": "gk-2003-regular-shanghai-science-q14",
  "resume_action": "取得可追溯的同版答案、勘误或考试编写约定，确认“平面平行”是否包含重合或是否默认 α≠β；据新证据重新判断 Q14。在此之前保持 U/PENDING，不把预期选项 D 写成确定答案或官方答案。",
  "source_id": "src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1390

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "50bdada5f48e3b05db05f268035eaf0f354421eb74db7f4107d7e02a27dfd10f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1391

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "e3df0b5f824f990ba9df9fb9c186615ccd4d8afcad415a1f37d515d69263ca02",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1392

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "74ad4c4fb46fd05a5b9f9f1a5bf080b9e33b11bbc3d0a479b48eb3ed099ab5d3",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1393

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "346247947e78bbd71cebb84d774af562add1ec3b0808e1b0b140a68dea31112c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1394

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "55e69214bbee65b79f40426d81b78da15ea1931a7c599350aabad32ffa56884f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1395

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "69f534c60d009a0c18c5758aac8d8ef218630fa996dfb14739532accbb5736d6",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1396

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "ae7314483a6654d588fd7234318e5b7886a8ee7edf0f701deb3368c617dd1d29",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1397

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "0a85c1239833607d88162cd0c89c3fddba89363d59192fb5bb3fead4309aa57d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-shanghai-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1398

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第2页（印刷页127）Q18 首句称顶点为 A1、A2，后文使用 OA、A1P、AP1；原图标左端 A1(-5,0)、右端 A(5,0)，没有 A2。300 dpi 原页复看与独立题面复核确认该差异确在原件。新查到新浪教育 2003-06-09 北京文科试题扫描（page 45210，扫描页17）右端标 A2(5,0)，同期答案扫描（page 45213，扫描页20）也以 A2 推导；页图 SHA-256 分别为 a544751f475d112fe87850cc81aefc6bff795206f7a2e9d2b220c724e031226f 与 9c91358e1c72e74e57ff7737defa6ba8cf09843bbf1ac3c299a508090c1c6150。该材料来自精华听课网经新浪教育发布，带有新浪“仅供参考、以权威部门为准”声明；其独立分页、未认证的发布链不能证明与固定 PDF SHA 7fc0fd289fc486a0ae1c16a9ab5b4f0561830897df6e8897c50666f03d511913 为同一版，也不是官方勘误。详情见 reports/2003-beijing-contemporaneous-source-corroboration-20261104.md。",
  "fingerprint": "dabbd97eba1b6861c574e702cb84bfc8b59aae40df98f2be8657ca01762d5bc2",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-beijing-arts",
  "question_id": "gk-2003-regular-beijing-arts-q18",
  "resume_action": "取得可追溯的同版勘误、答案材料或独立同版原件，确认 Q18 顶点记号的原卷意图；在此之前继续照录原文和图示，不静默统一字母。",
  "source_id": "src-dcc6a2c21c7b8e7b8f23f5188f34d7f542f94e40f4219b54cfb85a0d7004bc0f",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1399

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定题面字面同时出现 A1、A2 和后文的 A，仍无法从该固定副本本身唯一确定构造所用右顶点。新浪教育 2003-06-09 的同期北京文科答案扫描（page 45213）用 A2(5,0) 并据此给出椭圆与准线结果，提供非官方同期答案材料支持；但其不能认证固定 PDF 的精确版本或官方答案。答案要点与解析继续标 U/PENDING；按 A2 的推导只作为条件性结果，不能当作官方答案。详见 reports/2003-beijing-contemporaneous-source-corroboration-20261104.md。",
  "fingerprint": "f59e73479110d23cd9a8bb289a60af044c17a6a8d531f95c194da2bfaaf0e126",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-beijing-arts",
  "question_id": "gk-2003-regular-beijing-arts-q18",
  "resume_action": "取得可追溯的同版答案、勘误或可靠同期材料以确认题目构造所指顶点，并据新证据重审 Q18；此前保持 U/PENDING，条件性推导与确定答案分开。",
  "source_id": "src-dcc6a2c21c7b8e7b8f23f5188f34d7f542f94e40f4219b54cfb85a0d7004bc0f",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1400

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF 第2页（印刷页125）Q17 可见原文为“底面边长的 3”，其后紧接逗号和“侧棱”，3 后没有可见“为”；300 dpi 源页复看和独立题面复核均确认如此。新浪教育 2003-06-09 北京理科试题同期扫描（page 45222，扫描页42）同题写“底面边长为3”，页图 SHA-256 a000900a4b021a3a275c3d80006648009cc4a8257f816f8dc41f7f80b8312199；同期答案扫描（page 45226，扫描页45）以 BD=BC=AB、BE=1/2 AC=3/2 求解，页图 SHA-256 c5669185cdd2049d89f225b6257d2e4254391ffa1447aa5e93bc4c6568fdfdab。材料由精华听课网经新浪教育发布，新浪注明仅供参考；分页不同且来源链未认证，不能证明与固定 PDF SHA d0081500bd56d03199ddcf232fe8e870f2ecd7e9c41ba849417af9af79fbb702 同版，也不是官方勘误。详情见 reports/2003-beijing-contemporaneous-source-corroboration-20261104.md。",
  "fingerprint": "9ed886cb05969987b28f6b8b1112e6c3a14220530fac1eb184ce5b777767d954",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-beijing-science",
  "question_id": "gk-2003-regular-beijing-science-q17",
  "resume_action": "取得可追溯的同版勘误、答案材料或独立同版原件以确认 Q17 边长原文；在此之前保留“底面边长的 3”的字面，不增补缺字。",
  "source_id": "src-120ea104f8cb373f5731039fa9d36469df457869849f27420831962ef1ad2306",
  "status": "open",
  "type": "transcription-ambiguous"
}
```
## ISSUE-1401

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定原页仍不能确定正三棱柱底面边长是否应为3。新浪教育 2003-06-09 的同期北京理科试题扫描写“底面边长为3”，对应答案扫描支持 s=3 的后续计算；这是一条非官方同期材料，未认证为固定 PDF 的精确版本或官方答案。Q17(1) 可独立证明；Q17(2)(3) 继续标 U/PENDING，并只在显式假设边长为3时列条件性结果。详情见 reports/2003-beijing-contemporaneous-source-corroboration-20261104.md。",
  "fingerprint": "051248b1687d9bd5477e0eb99bf16ff9d6ce3ef76bf8beb1038f69a19fc6745f",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-beijing-science",
  "question_id": "gk-2003-regular-beijing-science-q17",
  "resume_action": "取得可追溯的同版答案、勘误或可靠同期材料以确认 Q17 底面边长；此前保持整题 U/PENDING，不将 s=3 条件性结果升级为确定答案。",
  "source_id": "src-120ea104f8cb373f5731039fa9d36469df457869849f27420831962ef1ad2306",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1402

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "dd4f8a8539acc8fd08f12d437f7e0fbf89bcfd5ab6d47f5d620071d4685ba606",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1403

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "c1b71a71d3d6a9080343624250ac279033580fb870a2e1a666e16e4530667822",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-beijing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1404

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "dbf00fe1bfe6f2d7d542abcb7f336ca72fc909695451b4f55d4adcf85ba7fe20",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1405

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "623915af9172f47c0d2b3d2ba42b183ab7d3a619be7efafce7df970933aa76a3",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1406

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "4f3cb69bc61d0fbf411a62c11660b9288cb92dc949da637e87d389f4af6f63d1",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1407

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "b703bcc67be1f3c72b50b1714d326e0f0151738a59dd4a1a702be96978b2a20e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2003-regular-beijing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1408

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选回忆版 PDF（SHA-256 7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9）Q10 的四个选项分别为 [5/16,53/80]、[5/16,73/80]、[5/12,53/80]、[5/12,73/80]。第三方六页 PDF（SHA-256 3949ba57c1be0eb4fd4f9ff78dbad3bd65ab401599061659595d0fa6d6e15a5f）给出不同端点/区间，来源链未认证；候选版计算的数值区间不能确定正式卷选项字母。",
  "fingerprint": "9726b290fac64d91c34bde0f712c3a2efe0d16b1acba8e4929d3cb1c386ad5a4",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q10",
  "resume_action": "取得可追溯至考试机构的完整同版正式卷或勘误，逐项裁定 Q10 选项；之前保留固定来源字面、条件性区间和 U/PENDING，不选定版本。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1409

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选回忆版 PDF 第2页上限印为 y≤3lg2，第三方六页 PDF 作 y<3lg2；两份副本均未能认证为正式题面，端点不同会改变 f=4900 是否包含。",
  "fingerprint": "f3664f5b851c316e50e02143d89e8b7f9aa6a09b7dac5e9e1367ac923f07d6b3",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q13",
  "resume_action": "取得可验证的同版正式卷或勘误裁定上限端点；在此之前保留候选版与第三方版两种条件结果，并将最终端点答案标为 U/PENDING。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1410

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选回忆版 PDF 第2页把 c=1 陈述列为②、c=0 陈述列为③；第三方六页 PDF 将这两条陈述序号互换。现有证据不足以认证正式卷的陈述编号。",
  "fingerprint": "b7a4cc5d392aa0282cd4a3b63d377a7a17b835dac7f3ccb0bb2ed4f2e5c98cdf",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q15",
  "resume_action": "取得来源链可验证的完整正式卷或勘误，确认②③原文次序；保留固定候选版本并标出异文，不静默改题。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1411

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页的四杆闭合结构及以 A 为视觉中心的完整圆已按 reports/2026-beijing-recall-figure-source-review.md 重绘为 2026_北京卷_回忆版/figures/f2026_beijing_recall_q10_fourbar_linkage.tex；图稿头绑定 source_id src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee、PDF SHA-256 7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9、第2页和 Q10。规范题面有独立 Markdown 链接，确定性 _含解析.md 已刷新，manifest figure_files 登记 expected_occurrences=2，生成的 questions.tex 与 answers.tex 均引用图稿；三页 XeLaTeX 局部预览已逐图对照固定原页检查。圆未标成可达轨迹，投影比例仍仅作示意。",
  "fingerprint": "93a530d35aef8eafb13f201aad34382d2c4f787dde291c5c7c4ad07c2e02a699",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q10",
  "resume_action": "已完成 TikZ 重绘、固定原页目视复核、规范题面图链、确定性生成映射与 figure_files 登记；本图缺失问题已解决。正式试卷排版若发现具体图形问题，应另行登记，不从示意比例推断数学条件。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "resolved",
  "type": "figure-missing"
}
```

## ISSUE-1412

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第2页三棱锥 A-BCD 已按 reports/2026-beijing-recall-figure-source-review.md 重绘为 2026_北京卷_回忆版/figures/f2026_beijing_recall_q14_tetrahedron.tex；图稿头绑定 source_id src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee、PDF SHA-256 7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9、第2页和 Q14。仅 DC 画为虚线，规范题面有独立 Markdown 链接，确定性 _含解析.md 已刷新，manifest figure_files 登记 expected_occurrences=2，生成的 questions.tex 与 answers.tex 均引用图稿；三页 XeLaTeX 局部预览已逐图对照固定原页检查。未添加垂直、长度或中点标记。",
  "fingerprint": "c70f602216b2fd2d2bf2597f5caa3361c9afd640d80b1e753db1f4fc62ce3140",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q14",
  "resume_action": "已完成 TikZ 重绘、固定原页目视复核、规范题面图链、确定性生成映射与 figure_files 登记；本图缺失问题已解决。正式试卷排版若发现具体图形问题，应另行登记。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "resolved",
  "type": "figure-missing"
}
```

## ISSUE-1413

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定候选 PDF 第3页三棱柱及辅助线已按 reports/2026-beijing-recall-figure-source-review.md 重绘为 2026_北京卷_回忆版/figures/f2026_beijing_recall_q18_triangular_prism.tex；图稿头绑定 source_id src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee、PDF SHA-256 7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9、第3页和 Q18。实虚侧棱、底棱及 EP/ED/PD 线型按固定原页重绘；D、E 为题干给定中点，P 的位置仍为示意。规范题面有独立 Markdown 链接，确定性 _含解析.md 已刷新，manifest figure_files 登记 expected_occurrences=2，生成的 questions.tex 与 answers.tex 均引用图稿；三页 XeLaTeX 局部预览已逐图对照固定原页检查。",
  "fingerprint": "65cea86524ae4cfc2051a8977a68bec8dd3d7f4de7cab4b47c20a50892c41ff5",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q18",
  "resume_action": "已完成 TikZ 重绘、固定原页目视复核、规范题面图链、确定性生成映射与 figure_files 登记；本图缺失问题已解决。正式试卷排版若发现具体图形问题，应另行登记；P 的比例位置不作为题设。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "resolved",
  "type": "figure-missing"
}
```

## ISSUE-1414

```json
{
  "affected_paper_ids": [],
  "current_evidence": "在 EP∥B1C1 参数化 P=(1−t,t,√2) 下，独立推导显示条件③ BB1∥平面 PDE 对所有 t≠0 均成立；t=0 时 P=E，三点不确定平面。因此条件③不能唯一确定 P，条件①/②各给出 t=1/2。固定回忆版题面未说明该设计问题的勘误。",
  "fingerprint": "80d53339b38fa74bfe3d4da0dd70a831358c9c3f284eab10e7e55f57b57eb236",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q18",
  "resume_action": "取得可追溯的同版勘误或权威解释确认条件③是否漏限；在此之前仅保留条件①/②的条件性结果，Q18(2) 标为 U/PENDING。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1415

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定回忆版候选 PDF 第2页的选项 B 对应独立推导范围 [5/16,73/80]；来源冲突报告记录第三方未认证副本把同一区间列为选项 A，且其余选项也不同。来源链与正式卷身份均未核，最终选择字母保留 U/PENDING。",
  "fingerprint": "295222f754496d5493eca85a5d2f5cf8542a0f519d40b6784b3f3ee8d31278c1",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q10",
  "resume_action": "取得可追溯至考试机构的同版正式卷或勘误，裁定 Q10 的选项字母；在此之前保留条件性数值范围和 U/PENDING，不按副本身份择版。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1416

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定回忆版候选 PDF 第2页给出 lg2≤y≤3lg2，对应 f∈[700,4900]；第三方未认证副本将上界写为严格小于，对应 f∈[700,4900)。来源链与正式卷身份均未核，最终端点保留 U/PENDING。",
  "fingerprint": "abdf24d689e0fafddc888154084213bbc34ca49a616e5761b671d79c75871589",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-beijing-recall",
  "question_id": "gk-2026-regular-beijing-recall-q13",
  "resume_action": "取得可追溯至考试机构的同版正式卷或勘误，裁定 Q13 上界是否含等号；在此之前并列保留两种条件结果并维持 U/PENDING。",
  "source_id": "src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1417

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF（SHA-256 4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91）第 2 页第 18 题只称 {b_n} 为等比数列，未说明公比非零；该 PDF 无答案或评分页，不能由同版答案材料核定零公比约定。依题面条件可得 q^2=0 或 1/2；答案要点与解析保留 q=0、q=±1/√2 的条件结果，标 U/PENDING。",
  "fingerprint": "7654a62e41d55dabc9224fb6225963966645b8ec2a7804800886d6644dcfb0a9",
  "impact": "blocks_completion",
  "paper_id": "gk-2002-regular-suyuyuegui",
  "question_id": "gk-2002-regular-suyuyuegui-q18",
  "resume_action": "取得可绑定到同一版次或同一固定 PDF 的答案、勘误或可追溯定义材料，核定零公比约定；核定前保留 U/PENDING 与条件分支，不把该卷标记为完成。",
  "source_id": "src-0daae2fa54742835e68d7f3b2cb647b26cee7c4d302f16958e53100e71e4bab4",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1418

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "a9ad31745f544d10d6a3943941977f16480e94c7d1745b87f257b65d45d90a32",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-suyuyuegui",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1419

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "c0d45cebb11be4447bf0cbb35c7f425f9848a56c011a98aa2529dba5abcdd9ee",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-suyuyuegui",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1420

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "9d1eed8c6be4e59554f0ccac2762543034e4fa19bb2b9c8bc1f880d2bcd8812b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-suyuyuegui",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1421

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "8c153c9428239fe9698d9c9a092208e39aaf6a086119c94fb77dbabfc8d2ac28",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2002-regular-suyuyuegui",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1422

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "03cafc86-5ceb-425c-b048-2d309875a9f2",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "cf7a222a8a497279ba34905b9ab0c289f838ec5d38c4bc4f687b3f5940da4b3a",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-2017-regular-beijing-arts",
  "pdf_sha256": "8d1e2924ea03b984b593fa870b428527db4a35f606bbb1c49357408b1645719c",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1423

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "03cafc86-5ceb-425c-b048-2d309875a9f2",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "9f2a483784ce9719c38f2f301930981bec23761133e659153852d7d75d49a525",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-2017-regular-beijing-arts",
  "pdf_sha256": "8d1e2924ea03b984b593fa870b428527db4a35f606bbb1c49357408b1645719c",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1424

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "7265f2c2-1337-45b2-a177-6d2a42b37264",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "2cc0445c18b29671e81546a01484a3a8ab0d6c32509f2eb2670b0d85611dedb9",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 1,
  "paper_id": "gk-2017-regular-tianjin-science",
  "pdf_sha256": "ab1e3030992dc0b617c3946a868deff863716fedd89e2dcc0f47369d28dc0de3",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```
## ISSUE-1425

```json
{
  "affected_paper_ids": [],
  "build_attempt_id": "7265f2c2-1337-45b2-a177-6d2a42b37264",
  "check_code": "pagination_whitespace",
  "edition": "印刷版",
  "figure_id": "visual-review",
  "fingerprint": "50c50080ffc81c79fc86ba3c5300015c259e8349d64000823acb5c68636f9e4d",
  "impact": "non_blocking",
  "origin": "visual-review",
  "page": 2,
  "paper_id": "gk-2017-regular-tianjin-science",
  "pdf_sha256": "ab1e3030992dc0b617c3946a868deff863716fedd89e2dcc0f47369d28dc0de3",
  "resume_action": "已在新一次全页视觉审查中通过，无需动作",
  "status": "resolved",
  "type": "layout-warning"
}
```

## ISSUE-1426

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF（SHA-256 dbf7bd3f4e11621d7d31e38ed304f3617f20ecb070e96ac0ec0fbc5a17b9748b）第 1 页第 12 题设问为求点 M 的纵坐标，但所列选项印为“7倍/5倍/4倍/3倍”（实为理科第 12 题倍数选项），计算所得纵坐标 ±√3/4 落在第 13 题选项 A 中。原卷选项错位互换，答案标 U/PENDING。",
  "fingerprint": "381fad38da14b45dda524868b98c4c317d80ed39671b465ba88e9b84df437548",
  "impact": "blocks_completion",
  "paper_id": "gk-1998-regular-national-arts",
  "question_id": "gk-1998-regular-national-arts-q12",
  "resume_action": "取得可绑定到同一版次或官方勘误材料，核定原卷更正说明；核定前保留 U/PENDING，不把该卷标记为完成。",
  "source_id": "src-19546ffe511fd8607988e9153f3b24ef24704bd592b19f95cfcde2844ab83cc5",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1427

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF（SHA-256 dbf7bd3f4e11621d7d31e38ed304f3617f20ecb070e96ac0ec0fbc5a17b9748b）第 1 页第 13 题设问为求球半径，但所列选项印为“±√3/4、±√2/2、±√3/2、±3/4”，带有正负号（实为第 12 题纵坐标选项）。依题意计算球半径为 2√3，选项中无对应值。答案标 U/PENDING。",
  "fingerprint": "85f2bdc243cd587b4e22cf4081b4f9d457f975cb17acec2794f78d13adc9acda",
  "impact": "blocks_completion",
  "paper_id": "gk-1998-regular-national-arts",
  "question_id": "gk-1998-regular-national-arts-q13",
  "resume_action": "取得可绑定到同一版次或官方勘误材料，核定原卷更正说明；核定前保留 U/PENDING，不把该卷标记为完成。",
  "source_id": "src-19546ffe511fd8607988e9153f3b24ef24704bd592b19f95cfcde2844ab83cc5",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1428

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF（SHA-256 dbf7bd3f4e11621d7d31e38ed304f3617f20ecb070e96ac0ec0fbc5a17b9748b）第 1 页第 25 题第 (2) 问通项印为 lg(1+1/b_n)，同句却残留理科条件‘其中 a>0, 且 a≠1’；且比较对象印为 1/2 lg b_n + 1，字形上 +1 未入下标。答案要点与解析正文对命题意图与字面含义均作完整讨论，答案标 U/PENDING。",
  "fingerprint": "3e8dd29966db59ef78173e935ffeea949c48c5d4faf44ae21031ff49fdf6a2cb",
  "impact": "blocks_completion",
  "paper_id": "gk-1998-regular-national-arts",
  "question_id": "gk-1998-regular-national-arts-q25",
  "resume_action": "取得可绑定到同一版次的官方答案或编写约定，核定第 25 题第 (2) 问官方评卷口径；核定前保留两套分支说明，不把该卷标记为完成。",
  "source_id": "src-19546ffe511fd8607988e9153f3b24ef24704bd592b19f95cfcde2844ab83cc5",
  "status": "open",
  "type": "answer-convention-ambiguous"
}
```

## ISSUE-1429

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定 PDF（SHA-256 8fa242a22c63304be81479064cbba81281dba644d554c1a2b37b0f5840363575）第 1 页第 10 题设问求 f(x)=sin x, x∈[π/2, 3π/2] 的反函数，严密推导反函数表达式为 f^{-1}(x) = π - arcsin x, x∈[-1, 1]（对照 2003 全国理科第 10 题选项 D 为 π - arcsin x）。但在本卷排版印刷中，选项 (D) 误印为 -π - arcsin x，与选项 (B) 字面完全重复，且四个选项中无一与正确反函数表达式匹配。答案标 U/PENDING。",
  "fingerprint": "e20959f567f11b4595814cb546c651e2af65629ac55eb4219d1e4d37c125c493",
  "impact": "blocks_completion",
  "paper_id": "gk-2003-regular-yuegui",
  "question_id": "gk-2003-regular-yuegui-q10",
  "resume_action": "取得可绑定到同一版次或官方勘误材料，核定原卷选项勘误说明；核定前保留 U/PENDING，不把该卷标记为完成。",
  "source_id": "src-b832b045aa19322b4da5d7657c59eb6e57247c15149902598f68b5af3c8c59ff",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1430

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "d987ac10a1be338fc0c11cebc4ad049e2260bcf04ac9fd4340486ee87747074d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-tianjin-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1431

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "e5f744f6747c190f970a830ae73ee50d52a7c915edc20f54feddce13d72cea3e",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-tianjin-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1432

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "7695fbaa8afd5ac1144bfe11658ed2fdc33eef3b7a03a528ed38156022c2940b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-hubei-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1433

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "c5dd321783a5ee659ca062ab207c078da362bbb5209705ea05ec545872a6d8cb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-hubei-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1434

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "204931a39571b59bf10e25cdef20723f23291e58a61078c1d5e7f43a4bcacaf2",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1435

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "1be5122ad99aeb0f883fb5ed7b911fb76ec8cfb221d12653a4ab4693f18e3b2b",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2004-regular-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1436

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "02fb8b355dfe48c3b171729f50b145040300080af523a42cb95b6021689dd3b9",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1437

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "9fda80f2eaa23ae98b19294f53bc249a97c721c2049d798ae530f1549964d661",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1438

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "c6b4f8e1ea96f546c33feae9f3556e3e466d1855dd76360696bc58b783676135",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-fujian-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1439

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "2fcb2b832eb6b416f538cd44609c7c511fa6b3518014c5fd6496b335acba6f02",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-fujian-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1440

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "12478efc025abddf0b24c9cfc58a200a65c9be787536f185a25c632222221678",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-liaoning",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1441

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "222d85c43b5ffc65e7c92cd0911b47b30558b38d0317e8e7205b83f244a6802a",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-liaoning",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1442

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "a2ef6b75f8b17c52a9394e0359f681fd89e083a8092cdb6c38c1c49105bc708f",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-liaoning",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1443

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "04824083da9c772ae33f13460e949a087cde4babe45e9304202d40e11f15491c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2005-regular-liaoning",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1444

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 文本层第 20 题印作「$a_2$ 是 $a_1$ 与 $a_4$ 的等差中项」并同时给出 $d\\neq0$；由 $2a_2=a_1+a_4$ 得 $2(a_1+d)=a_1+(a_1+3d)$ 即 $d=0$，与题设自相矛盾。文科、理科两卷此处字面相同。题库保留源面字面并在题下注记，解析按「等比中项」处理（此时 $a_1,a_3,a_{k}\\dots$ 成等比给出 $k_n=3^{n+1}$）。",
  "fingerprint": "c89cf9e146384f483ce254ac8474a15377d37abe94f416511b7d4664ef8128e1",
  "impact": "non_blocking",
  "paper_id": "gk-2005-regular-national-3-arts",
  "question_id": "gk-2005-regular-national-3-arts-q20",
  "resume_action": "取得同版勘误或官方标准答案以确认原词为「等比」；未取得前题面保留字面、解析注明误植判断，不代改题面。",
  "source_id": "src-de5ca92375a2c3f24affb84420f1c29a58928c8b50e638e46513944adb80431a",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1445

```json
{
  "affected_paper_ids": [],
  "current_evidence": "同 ISSUE-1444：固定源 PDF 文本层第 20 题印作「等差中项」又给 $d\\neq0$，字面自相矛盾；理科卷另有第 21(2) 端点问题已按开区间处理。题库保留字面并注记，解析按等比处理。",
  "fingerprint": "52d2a4c1251f28114788bf7d433b6266c5eec50b16305fcaad652f1be89be270",
  "impact": "non_blocking",
  "paper_id": "gk-2005-regular-national-3-science",
  "question_id": "gk-2005-regular-national-3-science-q20",
  "resume_action": "同 ISSUE-1444：待同版勘误或官方答案确认用词。",
  "source_id": "src-d83681afc201b87c3dbfcabe7dff39f6f9c3067b1e28f234307b994784eda1bc",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1446

```json
{
  "affected_paper_ids": [],
  "current_evidence": "2026-11-09 审计发现本库第一版解析把 $(A\\cap B)\\cup C=\\{1,2\\}\\cup\\{2,3,4\\}$ 误写成 $\\{2,3,4\\}$ 而答案写 D，等式与选项自相矛盾。已改正为 $\\{1,2,3,4\\}$（= D）并重跑生成、编译与审查，四层 Markdown 与四版 PDF 现一致。",
  "fingerprint": "943cf9056c4b30b6847bfd47318e493d42f8faf84828b1f23aa84158ab7d7a6a",
  "impact": "non_blocking",
  "paper_id": "gk-2005-regular-jiangsu",
  "question_id": "gk-2005-regular-jiangsu-q1",
  "resume_action": "已修复：无需动作，保留记录供后续抽查同类并集运算。",
  "source_id": "src-935f381a6fe96aa7c90e29bd5d55871232018e04915422713605b6843b981999",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-1447

```json
{
  "affected_paper_ids": [],
  "current_evidence": "2026-11-09 审计发现 Q12 折叠角误答 $45^\\circ$（误按平面中位线处理）。用坐标法复核：$E(0,0,0)$、$B(b,0,0)$、$D(0,d,0)$、$C(b,d,0)$、$A(b,0,b)$，$M(b/2,d/2,b/2)$、$N(b,d/2,0)$，$\\overrightarrow{MN}\\cdot\\overrightarrow{EA}=0$，故为 $90^\\circ$。已改正四层 Markdown 并重建。",
  "fingerprint": "f7bc8fa9dea06dd80b4a6e083338ffe7033057d680a44ad3139690b51630bdae",
  "impact": "non_blocking",
  "paper_id": "gk-2005-regular-zhejiang-arts",
  "question_id": "gk-2005-regular-zhejiang-arts-q12",
  "resume_action": "已修复：无需动作。",
  "source_id": "src-471caa672d0669c285806b64c504cc9694bcd51dd60b0a0b2a7a45178fb560cb",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-1448

```json
{
  "affected_paper_ids": [],
  "current_evidence": "同 ISSUE-1447：理科卷 Q12 同题同误，已由 $45^\\circ$ 订正为 $90^\\circ$（坐标法 $\\overrightarrow{MN}\\cdot\\overrightarrow{EA}=0$）并重建四版。",
  "fingerprint": "2b5e00c1d8f93c01a8dc32115c1d1c9b37a70f9ca0ebb060c9bb3ddfe07446dd",
  "impact": "non_blocking",
  "paper_id": "gk-2005-regular-zhejiang-science",
  "question_id": "gk-2005-regular-zhejiang-science-q12",
  "resume_action": "已修复：无需动作。",
  "source_id": "src-216c3b98cde76aa00ef9438e3d25ba93e13bfc6f605279dcf1399de98457ac48",
  "status": "resolved",
  "type": "answer-conflict"
}
```

## ISSUE-1449

```json
{
  "affected_paper_ids": [],
  "conflict_code": "duplicate-option-bd",
  "current_evidence": "固定源 PDF（SHA-256 6f3287a6…1395cc2d，印刷页 409）第 1 题选项 (B) 与 (D) 均印作 1，300 dpi 与 300% 局部放大两次核对均为同一字符，非渲染伪影。(1+i)/(1−i)+i³=0，答案取 (A)，两项重复不影响判分，但原页确实自相重复。",
  "fingerprint": "5304f73fe9856343a7faec2fac18e3953c0c24853688b7cb1133c47e547ed127",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-sichuan-science",
  "question_id": "gk-2007-regular-sichuan-science-q01",
  "resume_action": "取得同版答案、勘误或更清晰的同期印刷件确认 (B)、(D) 中哪一项为原意干扰项；在此之前按原页照录两项同为 1，不擅自改选项，答案仍取 (A)。",
  "source_id": "src-7f0853b7bdbe811e775df7c347bf09950fb6409f271efff9afb08e8360cd9049",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1450

```json
{
  "affected_paper_ids": [],
  "conflict_code": "no-valid-option",
  "current_evidence": "固定源 PDF（印刷页 409）第 11 题四个选项按印面为 2√3≈3.464、4√6/3≈3.266、(3−√7)/4≈0.089、(2−√21)/3≈−0.861；按 l1–l2 距离 1、l2–l3 距离 2 且正三角形三顶点分居三线，独立推导（代数解与投影恒等式两条路径）得边长 2√21/3≈3.055，四个印刷选项无一吻合；(D) 与正解同分子 √21、同分母 3，仅差根号，疑为误印。",
  "fingerprint": "676c4034ba9b1f4518fc43b4ddd2477cfde58db21dbbd9fe1b045df4bf5f0509",
  "impact": "blocks_completion",
  "paper_id": "gk-2007-regular-sichuan-science",
  "question_id": "gk-2007-regular-sichuan-science-q11",
  "resume_action": "取得同版答案、解析或勘误确认 (D) 是否应为 2√21/3；在此之前保留原页四个选项与独立推导结论，不擅自把 (D) 改成正解，也不把该题标作已完成。",
  "source_id": "src-7f0853b7bdbe811e775df7c347bf09950fb6409f271efff9afb08e8360cd9049",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-1451

```json
{
  "affected_paper_ids": [],
  "conflict_code": "unreduced-option-d",
  "current_evidence": "固定源 PDF（印刷页 409）第 12 题选项 (A) 1/12、(B) 7/60、(C) 6/25、(D) 5/25；300 dpi 局部放大两次核对 (D) 的分子确为 5、分母确为 25（未约分）。独立推导正解为 7/60，即 (B)，(D) 是否原意如此不影响答案。",
  "fingerprint": "f880eceb79f28e8f31f307c837aaa64e26feeda116576deca14d12305d3989d9",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-sichuan-science",
  "question_id": "gk-2007-regular-sichuan-science-q12",
  "resume_action": "取得同版材料确认 (D) 是否本应印作 5/25；在此之前按印面照录，不代为约分，也不改选项。",
  "source_id": "src-7f0853b7bdbe811e775df7c347bf09950fb6409f271efff9afb08e8360cd9049",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1452

```json
{
  "affected_paper_ids": [],
  "conflict_code": "hyperbola-y2-printed-r2",
  "current_evidence": "固定源 PDF（印刷页 347）第 9 题双曲线方程第二项的分子印作 $r^2$，即 $\\frac{x^2}{a^2}-\\frac{r^2}{b^2}=1$；全题再无 $r$ 出现，按双曲线标准形式与题设（$a>0$，$b>0$，焦点在 $x$ 轴）只可能是 $y^2$。300% 局部放大两次核读，字形为无下伸笔画的 $r$，不是 $y$ 的字体变体。独立推导按 $y^2$ 计算得离心率 $1+\\sqrt3$，落在选项 (D)。",
  "fingerprint": "58f8852437527ed9d36afad7352c96acb49b7658629b32e0fa1a5ae6a341f6e4",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-anhui-science",
  "question_id": "gk-2007-regular-anhui-science-q09",
  "resume_action": "取得同版答案或勘误确认该处是否为 $y^2$；在此之前按原页字形照录题面，解答按 $y^2$ 计算并在解析内标注源疑点，不改题面。",
  "source_id": "src-3d9060a0d561c198ee84aa2f9257aac76855602149b18224d4302cae3ea426a4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1453

```json
{
  "affected_paper_ids": [],
  "conflict_code": "vector-ab-printed-instead-of-oa",
  "current_evidence": "固定源 PDF（印刷页 347）第 13 题首项印作 $\\overrightarrow{AB}=\\boldsymbol a$，而后两项 $\\overrightarrow{OB}=\\boldsymbol b$、$\\overrightarrow{OC}=\\boldsymbol c$ 均以 $O$ 为起点，所求为 $\\overrightarrow{OE}$；常见版本多作 $\\overrightarrow{OA}=\\boldsymbol a$。300% 局部放大确认字母为 $AB$ 而非 $OA$。按 $\\overrightarrow{AB}$ 推导得 $\\overrightarrow{OE}=-\\frac12\\boldsymbol a+\\frac34\\boldsymbol b+\\frac14\\boldsymbol c$；若按 $\\overrightarrow{OA}$ 读法则为 $\\frac12\\boldsymbol a+\\frac14\\boldsymbol b+\\frac14\\boldsymbol c$。",
  "fingerprint": "3e7fb2e45c8d3b793335afcdd4713170fb4770d77b25ff01bba3a0fbaded28e5",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-anhui-science",
  "question_id": "gk-2007-regular-anhui-science-q13",
  "resume_action": "取得同版答案或勘误确认首项是 $\\overrightarrow{AB}$ 还是 $\\overrightarrow{OA}$；在此之前按原页 $\\overrightarrow{AB}$ 作答并在解析内标注两种读法的差异。",
  "source_id": "src-3d9060a0d561c198ee84aa2f9257aac76855602149b18224d4302cae3ea426a4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1454

```json
{
  "affected_paper_ids": [],
  "conflict_code": "latin-a-vs-greek-alpha",
  "current_evidence": "固定源 PDF（印刷页 347）第 16 题题头「$0<a<\\frac{\\pi}{4}$」与 $\\tan\\left(a+\\frac{\\beta}{4}\\right)$ 使用拉丁斜体 $a$，而同题 $\\boldsymbol b=(\\cos\\alpha,2)$ 与所求分式使用希腊 $\\alpha$，且向量 $\\boldsymbol a$ 与标量 $a$ 仅靠字重区分。300% 局部放大确认两处字形不同，非同一字符的排版变体。解答按「两处为同一角」处理，得 $2m+4$；若视为两个独立角，题设条件不足以确定原式的值。",
  "fingerprint": "34e65b372b77cd4510f92fa80d1b962c75b80a83a1f2f8f74d8c9957a5344bf8",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-anhui-science",
  "question_id": "gk-2007-regular-anhui-science-q16",
  "resume_action": "取得同版材料确认题头与 $\\tan$ 内的角是否应为 $\\alpha$；在此之前按原页字形照录，解答以「同一角」为工作假设并写明另一读法下条件不足。",
  "source_id": "src-3d9060a0d561c198ee84aa2f9257aac76855602149b18224d4302cae3ea426a4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1455

```json
{
  "affected_paper_ids": [],
  "conflict_code": "储备金-printed-储务金",
  "current_evidence": "固定源 PDF（印刷页 348）第 21 题「历年所交纳的储务金数目」中「储务金」的「务」应为「备」，全题其余三处均作「储备金」。300% 局部放大确认印面为「务」字。不影响任何计算。",
  "fingerprint": "4fb2d87c71c42ef19bde2da4a27586b2aee5dcf21f8660534cdc2054cd98d711",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-anhui-science",
  "question_id": "gk-2007-regular-anhui-science-q21",
  "resume_action": "取得同版材料确认该处是否为「储备金」；在此之前按原页字形照录题面，解答按「储备金」理解。",
  "source_id": "src-3d9060a0d561c198ee84aa2f9257aac76855602149b18224d4302cae3ea426a4",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1456

```json
{
  "affected_paper_ids": [],
  "conflict_code": "vector-ab-printed-instead-of-oa",
  "current_evidence": "固定源 PDF（印刷页 349）第 13 题首项印作 $\\overrightarrow{AB}=\\boldsymbol a$，而后两项 $\\overrightarrow{OB}=\\boldsymbol b$、$\\overrightarrow{OC}=\\boldsymbol c$ 均以 $O$ 为起点，所求为 $\\overrightarrow{OE}$；常见版本多作 $\\overrightarrow{OA}=\\boldsymbol a$。300% 局部放大确认字母为 $AB$ 而非 $OA$。按 $\\overrightarrow{AB}$ 推导得 $\\overrightarrow{OE}=-\\frac12\\boldsymbol a+\\frac34\\boldsymbol b+\\frac14\\boldsymbol c$；若按 $\\overrightarrow{OA}$ 读法则为 $\\frac12\\boldsymbol a+\\frac14\\boldsymbol b+\\frac14\\boldsymbol c$。",
  "fingerprint": "e876ae36946289cf92b80a816bfcdf3a11e3dc1f233742beed2cc2da38d5c6bb",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-anhui-arts",
  "question_id": "gk-2007-regular-anhui-arts-q13",
  "resume_action": "取得同版答案或勘误确认首项是 $\\overrightarrow{AB}$ 还是 $\\overrightarrow{OA}$；在此之前按原页 $\\overrightarrow{AB}$ 作答并在解析内标注两种读法的差异。",
  "source_id": "src-3efb292c80b2029e9720e241726d066b603d10688f3a3f9c090ecf1bad6ff04b",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1457

```json
{
  "affected_paper_ids": [],
  "conflict_code": "储备金-printed-储务金",
  "current_evidence": "固定源 PDF（印刷页 350）第 21 题「历年所交纳的储务金数目」中「储务金」的「务」应为「备」，全题其余三处均作「储备金」。300% 局部放大确认印面为「务」字。不影响任何计算。",
  "fingerprint": "9e482b03ffad1c747c223efc83b0ec2664e10d717b9c136e38a5c83807e16ffe",
  "impact": "non_blocking",
  "paper_id": "gk-2007-regular-anhui-arts",
  "question_id": "gk-2007-regular-anhui-arts-q21",
  "resume_action": "取得同版材料确认该处是否为「储备金」；在此之前按原页字形照录题面，解答按「储备金」理解。",
  "source_id": "src-3efb292c80b2029e9720e241726d066b603d10688f3a3f9c090ecf1bad6ff04b",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-1458

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "813d893202dd38f796712c6d27159baa587ccfeb045c4103fe7bb50ebf4230ec",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-chongqing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1459

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "b28475b340682620b7aeb5aff80117c0f77a7b8a7a2537f15fc63007e2f2da45",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2007-chongqing-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1460

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "f3951834b88e37b5d8d885ac57a547a9f25e642bf87821aaa59e988d0db17c6d",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1461

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "4ffb9ae682b4155ee795bb67c0d9401d2c77085657c9957c8fa14fb1d4db6469",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1462

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "91f3e6f52f7481b34050ec53460cd4302bf81c9db8cc31743b6dd8e48b46f377",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1463

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "cec180e3d947ff0cd12cd6e6b8e9c2df7ec2fadb7ba5651e3f539b943810f8bb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-shanghai-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1464

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "试题版",
  "figure_id": "formal-build",
  "fingerprint": "69b4bb20ba005b32853a29613e8eaec5bb915574dd48c75ec31dacf6bcf170fc",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1465

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "82613f2ccb824bd783c0b885969dce169cd52d0db529857dde2954f6390e57eb",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1466

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "简答版",
  "figure_id": "formal-build",
  "fingerprint": "7c913993af446d80b9837f60ed8d39bba17034d4d89de3db9aaafca0d0a4eeb5",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1467

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "ca2bc47c9ec2d71ccfd52802fef58e766c3b3803939210f2721739ace63876f7",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-chongqing-arts",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1468

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "解析版",
  "figure_id": "formal-build",
  "fingerprint": "30899d6b47affbfb499f4ee0693d6576b0edf50375e0a9b5d50d0ef195babb5c",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-nceq-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```
## ISSUE-1469

```json
{
  "affected_paper_ids": [],
  "check_code": "formal-build",
  "edition": "印刷版",
  "figure_id": "formal-build",
  "fingerprint": "0a05e4d169f26fcf7fe602657b36366bb003e3104c7da060f33a4d31caa11234",
  "impact": "non_blocking",
  "origin": "formal-build",
  "page": 1,
  "paper_id": "gk-2008-nceq-science",
  "resume_action": "已在新一次正式构建中通过，无需动作",
  "status": "resolved",
  "type": "compile-error"
}
```

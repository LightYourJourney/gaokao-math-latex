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
  "current_evidence": "b01 题面核对：题干文字忠实，但配图 images/2017理-t7-三视图.png（560x630）底部俯视图的等腰直角三角形只剩上半，直角顶点与底边切在画布外；题干明写「俯视图为等腰直角三角形」，属实质内容损失。",
  "fingerprint": "42aeaff5fe35ed88f5e4960e7c46d0f935b4c91442b8bfdf040f2fb02ed0c0cd",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-1-science",
  "question_id": "gk-2017-regular-national-1-science-q07",
  "resume_action": "从上游 PDF 第 1 页重新导出 images/2017理-t7-三视图.png（当前俯视图的等腰直角三角形被画布下边缘截断），补全后重跑题面核对",
  "source_id": "src-51eb5c18a0e4ad056c80a78acd915bc5d94193d7bb4506dd2fd2d078157b8d40",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0004

```json
{
  "affected_paper_ids": [],
  "current_evidence": "b01 题面核对：配图 images/2017文-t8-四图.png 底边被截断，下方两幅图象的下降分支切在画布外，PDF 中标在其下方的选项标签 (C)、(D) 整体缺失，图中只剩 (A)、(B)，无法据图对应选项。",
  "fingerprint": "78c8e8465c7357d3f9e820e8944ff1aea9509fd28092c4eb4bef7fc400f05f83",
  "impact": "blocks_completion",
  "paper_id": "gk-2017-regular-national-1-arts",
  "question_id": "gk-2017-regular-national-1-arts-q08",
  "resume_action": "从上游 PDF 第 1 页重新导出 images/2017文-t8-四图.png（当前底边被截断、选项标签 (C)(D) 整体缺失），补全四个标签后重跑题面核对",
  "source_id": "src-f4cc1ec8f7a5385f215c3ccec22f7942eadf5c1caa6a30fa88862df589f91c55",
  "status": "open",
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
  "current_evidence": "ISSUE-0002 收口时逐卷核验：2017 年山东有独立卷（与全国 1 卷第 1 题内容互异实证），上游文件名 `2017全国1理/文(河南,河北,山西,江西,湖北,湖南,广东,安徽,福建).pdf` 正确、不含山东，而两卷 frontmatter 的适用省份多列了「山东」（2018 上游文件名才含山东）。",
  "fingerprint": "f5d0925b92f2e0cf2b1741332467f6b80726c8b958a6326a9d728369a880d802",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "修正 2017 理/文两卷 `_试题.md` frontmatter 的「适用省份」（以及理科卷正文卷种提示处的同一串）——应为 河南、河北、山西、江西、湖北、湖南、广东、安徽、福建，**不含山东**；改动涉规范源基线登记，须走基线更新流程",
  "status": "open",
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
  "current_evidence": "b01 答案独立求解角色在 A 级判定的比对说明中记录了这三处要点论证缺口（结论一致、过程跳步）。",
  "fingerprint": "48c04c30c3aea79e39d6c78bc09fdcd7dfa0f0e82ae4ae5068361602e6fa53b4",
  "impact": "non_blocking",
  "paper_id": null,
  "resume_action": "补齐三处论证：2017 理 Q12 要点中「只能 k+3=2^m」未给证明；2018 理 Q22(2) 只由相切距离方程解出 k=-4/3，缺 k>0 / -4/3<k<0 / k<-4/3 的分类讨论；2018 理 Q19(2) 设 l:y=k(x-1)，未覆盖斜率不存在（垂直）情形。三处结论均已由独立求解角色复核为正确，缺的是论证。",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0009

```json
{
  "affected_paper_ids": [],
  "current_evidence": "题面缺句 + 配图整幅缺失：规范源删去「爻分为阳爻“——”和阴爻“— —”，如图就是一重卦」的符号说明与整句；PDF 该处印有六爻重卦示意图，而 2019/images/ 下不存在任何 2019理-t6-* 文件、正文亦无图片引用。选项与答案不受影响。",
  "fingerprint": "e52460575976f006ce1b6600a8b8753f6a3aab17c097b90444a55a0315cd4710",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-regular-national-1-science",
  "question_id": "gk-2019-regular-national-1-science-q06",
  "resume_action": "补回被删去的两句（阴爻/阳爻符号说明与「如图就是一重卦」），并转录 PDF p1 选项上方的六爻重卦示意图到 2019/images/ 后重跑题面核对",
  "source_id": "src-7052c2bd0093946c481076d7dfc16a8eaaec17214ab251fa4f0d43660f94e002",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0010

```json
{
  "affected_paper_ids": [],
  "current_evidence": "配图左缘被切（内容包围盒 x 起自 0）：待填空白框左边框被切除、「k=k+1」被切成「= k + 1」、循环回边不完整；下缘越界混入第 9、10 题正文与被切成残片的选项行（(A) 项不可读）。同一框图在文卷的转录件 2019文-t9-程序框图.png 无此问题。",
  "fingerprint": "ef53e85a85a78cede3c8d180b1ad96eb90af09ab1861111996a2c8341c271128",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-regular-national-1-science",
  "question_id": "gk-2019-regular-national-1-science-q08",
  "resume_action": "重新导出 images/2019理-t8-程序框图.png：左缘需完整含待填「空白框」左边框与 k=k+1 框，下缘不得越界混入第 9/10 题正文与残缺选项行",
  "source_id": "src-7052c2bd0093946c481076d7dfc16a8eaaec17214ab251fa4f0d43660f94e002",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0011

```json
{
  "affected_paper_ids": [],
  "current_evidence": "配图实质裁切：仅保留纵轴 100%/80%/60%/40% 与「率 20%」的上半截，横轴刻度与「温度 / °C」标签、散点云下部整块被切除；图内另混入题干末两行文字。",
  "fingerprint": "aac74a79333bf972f0dad1ff2038fbe915c52199d42398f3593db1d5ede09833",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q05",
  "resume_action": "重新导出 images/2020理-t5-散点图.png，必须完整保留横轴刻度 0/10/20/30/40 与「温度 / °C」标签及散点云下部（本题设问依赖 10 °C–40 °C 区间读图）",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0012

```json
{
  "affected_paper_ids": [],
  "current_evidence": "配图在 x 轴稍下方即被切断，左右两个波谷的下半部分被整块切除，仅剩波峰与轴线附近，曲线主体不完整。",
  "fingerprint": "1d16e3a6bed0798f589bc86973f74165eff09da0fa926445e3f9d4a1f47d990f",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q07",
  "resume_action": "重新导出 images/2020理-t7-图象.png，需完整含 [−π,π] 上左右两个波谷的下半部分与横轴标注 −π、−4π/9、O、π",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0013

```json
{
  "affected_paper_ids": [],
  "current_evidence": "图片资产错位：250×350 的文件内没有任何平面展开图，只有从相邻栏误裁出的零散文字碎片（「AB ⊥ AC, AB ⊥」及「匀/x/最/)」等），墨迹占比 0.63%。该展开图是本题唯一的几何信息来源，缺图后本题不可解（求解角色系仅凭题干文字完成求解）。",
  "fingerprint": "d13a5e11a755fd220001718a56bc6fc9132c5bdb253ccda80cd6dc38a6a79984",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q16",
  "resume_action": "重做 images/2020理-t16-展开图.png：现文件内容完全错位，需替换为 PDF 原图（标注 D(P)、A、B、C、E(P)、F(P) 的三棱锥平面展开图）",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0014

```json
{
  "affected_paper_ids": [],
  "current_evidence": "①题面缺句：规范源删去「由实验数据 (xᵢ,yᵢ) (i=1,2,…,20)」（同年理科卷第 5 题为同题且完整保留该句，卷首亦自称与理科卷第 5 题重合，可交叉印证）；②配图实质裁切：复用的 images/2020理-t5-散点图.png 横轴刻度与「温度 / °C」标签被整块切除。",
  "fingerprint": "53d1a4270c45205732fc2720759b8238bf72ac67fa6831fa6665bdf7ac9644dc",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-arts",
  "question_id": "gk-2020-regular-national-1-arts-q05",
  "resume_action": "补回被删去的「由实验数据 (xᵢ,yᵢ) (i=1,2,…,20)」一句，并随理科卷第 5 题一并修复散点图横轴（本卷复用 images/2020理-t5-散点图.png）",
  "source_id": "src-922b361942c8607abdfaba4bb5d504e18b644f5cfb744d7ae848a477192919bf",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0015

```json
{
  "affected_paper_ids": [],
  "current_evidence": "配图实质裁切：复用的 images/2020理-t7-图象.png 在 x 轴稍下方被切断，PDF 原波形左右两个波谷的下半部分被整块切除，曲线主体不完整。",
  "fingerprint": "eed5d5c350a48802bdb98c890787a6803fdb0b6590cc0b689d7ecbe108fc38bb",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-arts",
  "question_id": "gk-2020-regular-national-1-arts-q07",
  "resume_action": "随理科卷第 7 题一并修复图象（本卷复用 images/2020理-t7-图象.png，需含两个波谷的完整下半部分）",
  "source_id": "src-922b361942c8607abdfaba4bb5d504e18b644f5cfb744d7ae848a477192919bf",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0016

```json
{
  "affected_paper_ids": [],
  "current_evidence": "求解角色判 U 级：库内答案要点第 18(2) 题给 -2√5/5，四种独立方法（棱上垂直分量两取点、三面角球面余弦定理、同定向法向量叉积）一致给出 +2√5/5≈0.894427；要点的取负理由「B 与 E 在棱 PC 两侧」不成立——轴截面符号检验显示 B 与 E 同侧、A 才在另一侧，且 E 恒为不含 A 的弧 BC 中点，二面角必为锐角。在答案未更正前，本题答案证据不能定为 A。",
  "fingerprint": "c953859e9024b1898ccd56fd010e5aa7df3a34a7c1c7cccca541a93328bd79bb",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q18",
  "resume_action": "更正 2020 理科卷 `_答案要点.md` 第 18(2) 题：二面角 B-PC-E 的余弦值应为 +2√5/5（现值 -2√5/5 系定号错误）；更正后本题答案证据方可由 U 升级",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0017

```json
{
  "affected_paper_ids": [],
  "current_evidence": "盲核冲突未解决：独立求解与库内答案要点在第 18(2) 题符号上分歧（+2√5/5 对 -2√5/5），数值部分 |cos|=2/√5 双方一致，分歧只在定号。旁证：同构形下二面角 A-PC-B=90°、A-PC-E≈116.565°，两者之差 26.565° 与 B-PC-E 自洽。**这是本库首个被双盲核实的答案错误，冲突须待内容更正后才能了结。**",
  "fingerprint": "87894b0360c60bb0b5ad40ea7e7c43b2dab282e881847d4ce6d3e9c8f5abcdfd",
  "impact": "blocks_completion",
  "paper_id": "gk-2020-regular-national-1-science",
  "question_id": "gk-2020-regular-national-1-science-q18",
  "resume_action": "以求解角色的四法互证为据更正库内答案要点第 18(2) 题符号（-2√5/5 → +2√5/5），更正后重跑盲核以了结冲突",
  "source_id": "src-fdd4c494b504524d50a2032f2ba74f41552b8c41e0dc1407eccb0344d8848668",
  "status": "open",
  "type": "answer-conflict"
}
```

## ISSUE-0018

```json
{
  "affected_paper_ids": [],
  "current_evidence": "盲核冲突未解决：答案 D 正确，但库内答案要点的排除依据张冠李戴——其写「奇函数排除 B、C；f(π/2)>1 排除 A」，而放大原图核对显示 B、C 两图都是奇对称的、非奇的恰是 A，且 A 的峰值本就超过 1、用 f(π/2)>1 排不掉 A。同年理科卷同题要点列的四条判据无此问题。",
  "fingerprint": "e72c14acf6c00916b001b22d329162d9dc7b01e2fdcf91b404ff3bff52648fe7",
  "impact": "blocks_completion",
  "paper_id": "gk-2019-regular-national-1-arts",
  "question_id": "gk-2019-regular-national-1-arts-q05",
  "resume_action": "更正 2019 文科卷 `_答案要点.md` 第 5 题的排除依据（答案 D 本身正确）：应为「奇偶性排除 A、f(π/2)>1（峰高）排除 B、(0,π) 上符号为正排除 C」，更正后重跑盲核",
  "source_id": "src-67200538ccc7c8c92b28b4ee9180beac26c60144b9fc409ccf93ce5db5ebc37c",
  "status": "open",
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
  "current_evidence": "题面核对判 passed（200 dpi 渲染复核）：4 门体育类 + 4 门艺术类共 8 门、选修 2 门或 3 门、每类至少 1 门、「(用数字作答)」均一致，唯末尾漏一「课」字，不改题意与答案。本题无配图。",
  "fingerprint": "91a1212be76d82c368ff795020cee10c2a1a48e38d2c170342806d8457fc4f66",
  "impact": "non_blocking",
  "paper_id": "gk-2023-regular-new-gaokao-1",
  "question_id": "gk-2023-regular-new-gaokao-1-q13",
  "resume_action": "补回漏字：PDF 作「学生需从这 8 门课中选修 2 门或 3 门课」，规范源作「选修 2 门或 3 门」，末尾漏一「课」字；纯转录漏字，可直接补",
  "source_id": "src-7fdec764fe31e143cd6daf81734e2df4d142dc09b0a3ad696d522aacbefa7f63",
  "status": "open",
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
  "current_evidence": "盲核角色判 conflict_status=resolved，本条为该状态的承接指针（沿 b04 ISSUE-0033 口径：resolved 也要留一条可追溯条目，否则「这里曾有分歧、结论是什么」在 provenance 里只剩一个状态词）。盲核指出库内要点佐证两处硬伤：一是见证值 k=10 与其自述阈值自相矛盾（实测 z>y>x 而非 y>z>x），正确见证为 k=8；二是阈值 ≈9.32 应为 ≈9.3013。答案 B 经解析阈值与逐点扫描双重确认正确。求解角色的落盘证据可为阈值一项作旁证：其独立算得三条临界 x=y 于 k≈4.709、x=z 于 k≈7.270、y=z 于 k≈9.302——9.302 与盲核的 9.3013 相符，而与要点的 9.32 不符。",
  "fingerprint": "3ba8cd72d53c8b630da71b4aa1eed378f729e2b9ee02641b4ad3344dcbd65a5c",
  "impact": "non_blocking",
  "paper_id": "gk-2025-regular-national-1",
  "question_id": "gk-2025-regular-national-1-q08",
  "resume_action": "更正 2025 全国 1 卷 `_答案要点.md` 第 8 题的佐证：其见证值 k=10 与自述阈值自相矛盾（k=10 实测为 z>y>x，而非要点所称的 y>z>x），正确见证应取 k=8；所给阈值 ≈9.32 应为 ≈9.3013。答案 B 本身正确，只需改佐证",
  "source_id": "src-52c0a1ccacd7d0f6a8ba555e22474325194ac4aba7daa75012cc39626bc32ac3",
  "status": "open",
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
  "current_evidence": "题面核对判 passed（与 b04 ISSUE-0040 的辅助虚实线差异同级，不阻断），但其 evidence 原写「虚实线归属一致」系正面假断言，经三路互证证伪：一、上游源 PDF 第 2 页 1200 dpi 渲染视读——C 与 B 之间有一条清晰的虚线段（与实线 A′B 近乎平行、在其下方，于 B 点交汇），即源图 C—B 为虚线；二、仓库件 images/2025-2-t17-翻折四边形.png（718×363）裁剪区 (430,150)-(700,320) 做 7 倍最近邻放大——C 到 B 是一条连续实线、全程无断口，而同图的 E—F—C 与 F—D′ 仍显示为虚线，可排除「虚线在缩放中被糊成实线」的解释；三、TikZ 源 f2025g2_t17_fold.tex 第 19 行为 \\draw (C) -- (B);，是实线指令，与第 21/22/24 行的 \\draw[dashed] 形成对照——虚实翻转在图形源头即已存在。影响：C—B 是被遮挡棱，画成实线会误导遮挡关系的读取；但八个标注 A/B/C/D/E/F/A′/D′ 全在、其余虚实归属正确、四边无墨迹触边、无裁切，两小问的作答不依赖该棱的虚实，故维持 passed。孤例核验：本批其余三张含图 PNG（2024-t11、2024-t17、2024-Ⅱ-t17、2025-t17）未见同类翻转。",
  "fingerprint": "4b1782752dd28caa4cc8c219a32b2f94a82f051b3811a6b7667961fce19fe84b",
  "impact": "non_blocking",
  "paper_id": "gk-2025-regular-national-2",
  "question_id": "gk-2025-regular-national-2-q17",
  "resume_action": "重绘 images/2025-2-t17-翻折四边形.png：把 C—B 段由实线改回虚线。TikZ 源 math-gaokao-latex/2025_全国2卷/figures/f2025g2_t17_fold.tex 第 19 行现为 \\draw (C) -- (B);（实线指令），应改为 \\draw[dashed] (C) -- (B);——同文件第 21、22、24 行已用 \\draw[dashed]，改法与之一致；共享副本 math-gaokao-2017-2026/figures/f2025g2_t17_fold.tex 与本文件逐字节相同，须同步改",
  "source_id": "src-63d8cf8aeded86d1dc644b80483c817de4f9ba7d312f117942a408b916bcc94d",
  "status": "open",
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
  "current_evidence": "固定源 PDF 第 1 页高分辨率复核：题干印作“过 D 作 BC 的平分线交 AC 于 E”，而图中 D-E 线段与 BC 同向平行；按字面构造与图示构造不一致。",
  "fingerprint": "38050afbb46610362059f5e3637d8955596a041b9d53d371b29ec2725dcb2f3d",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanghai-arts",
  "question_id": "gk-1977-regular-shanghai-arts-q02",
  "resume_action": "取得同一固定源的清晰排印件或独立权威答案，确认题干“BC 的平分线”是否为原卷笔误；在确认前保留题面原文并按图示关系单独标注，不能将其当作无条件平行线题。",
  "source_id": "src-21ede2f4d2feea45ce0c013e43c589d4c6268b39e22ee860d9939b045f6a197c",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0126

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页高分辨率复核：题干印作“过 D 作 BC 的平分线交 AC 于 E”，而图中 D-E 线段与 BC 同向平行；按字面构造与图示构造不一致。",
  "fingerprint": "002076828588d3eec0048a3aa120fdb89846810732603f2fedfe41163b2729e4",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-shanghai-arts",
  "question_id": "gk-1977-regular-shanghai-arts-q02",
  "resume_action": "先解决第 2 题题干“BC 的平分线”与图示 DE∥BC 的冲突；确认构造后重跑独立答案、盲核与 provenance，方可解除 U 级答案证据。",
  "source_id": "src-21ede2f4d2feea45ce0c013e43c589d4c6268b39e22ee860d9939b045f6a197c",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0127

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页高分辨率复核：第 1(1) 行印作“在什么条件下，y/(2x)”后立即列出“是正数、是负数、等于零、没有意义”四项，未见可判定的条件或完整设问。",
  "fingerprint": "bf1c895f6d8c21e4bbba57cd71d93051b4418f34ebabe521bef76dc5afa88ffb",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tianjin",
  "question_id": "gk-1977-regular-tianjin-q01",
  "resume_action": "取得更清晰排印件或独立权威版本，确认第 1(1) 缺失的条件/设问；在确认前保留源页可见文字，不能补写。",
  "source_id": "src-fe8066472767be7a1d3a8466092df82bc08c125c6b5317f8d5334c617119ff24",
  "status": "open",
  "type": "transcription-ambiguous"
}
```

## ISSUE-0128

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页高分辨率复核：第 1(1) 行印作“在什么条件下，y/(2x)”后立即列出“是正数、是负数、等于零、没有意义”四项，未见可判定的条件或完整设问。",
  "fingerprint": "e009d5c9f80a8158077909d5e32eb705b8fc4e8c54f5edbc9c9dbe5ad1de9393",
  "impact": "blocks_completion",
  "paper_id": "gk-1977-regular-tianjin",
  "question_id": "gk-1977-regular-tianjin-q01",
  "resume_action": "先确认第 1(1) 的完整设问，再重做该小问答案、盲核与 provenance；其余小问不受该缺口影响。",
  "source_id": "src-fe8066472767be7a1d3a8466092df82bc08c125c6b5317f8d5334c617119ff24",
  "status": "open",
  "type": "answer-missing"
}
```

## ISSUE-0129

```json
{
  "affected_paper_ids": [],
  "current_evidence": "固定源 PDF 第 1 页高清局部复核确认第 1(3) 根式印作 sqrt((-1/16)^(-1/2))；第 2 页源解答却将同一处按 sqrt((1/16)^(-1/2)) 计算并给出 -72。严格按实数题面原式没有实数意义，源解答与题面不一致。",
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
  "current_evidence": "固定源 PDF《1977 江苏卷》单页高清复核确认第 1(1) 末项印作 (-27/8)^(-1/2)。负数的负半次幂在实数范围内无定义，而该题设问为计算题；在没有答案页或权威勘误前，无法确认这是原题意还是排印误写。",
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
  "current_evidence": "固定源 PDF《1977 江苏卷》单页高清复核确认附加题 7 写作 lim(n→∞) sqrt(x)(sqrt(x+1)-sqrt(x))，表达式只含 x 且未定义 x 与 n 的关系。按常见误写将 x 改为 n 可得 1/2，但这不是当前源页的字面内容。",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-d6811b4ee90fcb4c689f1ce1098e95218c259c8936d940e787689bf447f5775f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-7e099eb7b1f60b597d4fb6531a8f7e95702a5bdb36ed891ce68ecaa09794a718",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-4b137443f3517a495249741d7865a35219b34a43df024edffed5e5d2a599a93f",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-2ba72d23bef8bd52e9577b33ef8e8041dc5e4480414c42048c5e4ca4d2d4c979",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-9942a25450991741b525f62ca05393e08c7ba6534955f56776532adf87aa3687",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-565ee99d2452268215c074d90a9c421a328d5a3b72399fb539edefd863c6bc39",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-5454c05cffc2574b95187a0c039a157459a59c77dc5a20534f9e9a03cd7be644",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "open",
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
  "resume_action": "批级视觉审查时逐页对照固定源扫描件复核题面文字、公式与小问，确认后升级 passed 并 resolve 本问题。",
  "source_id": "src-6227c6ae2acbc473c193ea0d0b1322cfe349c985e795b71f851f5c870db030e4",
  "status": "open",
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

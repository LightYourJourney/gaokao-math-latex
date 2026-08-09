# 高考数学 LaTeX 缺失与问题总账

每个问题块使用稳定编号和可重算 fingerprint；已解决问题保留记录。

## ISSUE-0001

```json
{
  "affected_paper_ids": [],
  "conflict_code": "recall-vs-official",
  "fingerprint": "838b91797a3403c21eee95a996aa19fccfa8bf0d9e78955f16c9ba97811b9f20",
  "impact": "blocks_completion",
  "paper_id": "gk-2026-regular-national-1-recall",
  "resume_action": "正式卷公开后人工核验身份；回忆版不得自动绑定正式卷",
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

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
  "current_evidence": "题面核对判 passed，其证据末段记录：PDF 原文第 (2) 问作「当 c∈[95,105], 求 f(c) 的解析式」，「[95,105]」之后缺一「时」字；规范源 2023/2023_数学真题_新高考Ⅱ_试题.md 第 133 行照录为「当 $c\\in[95,105]$，求 $f(c)$ 的解析式，并求 $f(c)$ 在区间 $[95,105]$ 的最小值。」，同样无「时」字，已由导入方直接核对规范源确认（对照同题第 (1) 问第 131 行「当漏诊率 $p(c)=0.5\\%$ 时，求…」，「时」字在该处是有的，可见缺字仅在第 (2) 问）。本处与 ISSUE-0041 的三处方向相反：0041 是「源错、规范源按正确版改对」，本处是「源错、规范源照录不改」，两类的后续处置不同，故分条登记。",
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

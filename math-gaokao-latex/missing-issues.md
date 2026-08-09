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

# 真缺源清单（missing-source）

## 判定口径与 schema 冲突说明

目标要求把缺源套在 manifest 标为 `blocked_from=missing-source`。实测 `schemas/source-manifest.schema.json` 的 `blocked_from` 是 oneOf 闭枚举，合法值只有 `null / compiled / complete / legacy_unverified / planned / transcription_draft`；`missing-source` 只作为 `tools/manifest_csv.py:79` 的 CSV 派生列存在（`source_state != ready` 时输出）。写入 manifest 会被 `source_manifest.py validate` 直接拒绝。

因此本组采用**语义等价、schema 合法**的落法：`production_state=blocked` + `blocked_from=legacy_unverified`（该卷从未与任何 source 绑定）+ 显式 ISSUE + 本报披露；CSV 与报告中该卷仍显示未完成。

## 缺源套

| 试卷 | 缺什么 | 已尝试的核查 | 当前处置 |
|---|---|---|---|
| `gk-2026-regular-national-1-recall` | 教育部考试院 2026 全国 1 卷**官方正式卷**；现有上游件页眉自陈「回忆版」 | ① 上游 PDF 头部与页眉核对：明确标注回忆版；对照件 sha256 `f6f8ed7cdab86bedd7b3d261b7066c97a9fe24e3ad71538d1d01e6ce03f3fcb1`；② manifest 绑定通道关闭，`source_ids=[]`；③ 不以「与回忆版逐题一致」推断与正式卷一致 | 保持 `blocked`，ISSUE-0001（identity-ambiguous，open）；取得官方正式卷前不得绑定任何上游 source |

## 结论

除上述 1 套外，1952–2026 其余 469 套均有固定上游文件或既有固定副本，不存在第二套「零来源」试卷。

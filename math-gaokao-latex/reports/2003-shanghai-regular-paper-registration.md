# 2003 上海普通卷文理科：规范事实源与内部卷登记

- 日期：2026-11-04。
- 文科固定候选 source `src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4`，PDF SHA-256 `ffd59c395a0c675118f6da576e48842549c4afa031d923448f26f33087bc7e85`；题面为 PDF 第 1–2 页、原印刷页 140–141。
- 理科固定候选 source `src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0`，PDF SHA-256 `88b72fea05d331215504bb89257e375d07c18ba21e830cf9e6288461e88ccf8d`；题面为 PDF 第 1–2 页、原印刷页 138–139。
- 两份 PDF 均只有题面；发布者、版次、复制/扫描链与官方身份未核。与内部卷绑定只用于固定本库转录来源，不代表官方身份认证；`official_answer=null`。

## 规范源与指纹

两套卷均有 `_试题.md`、`_答案要点.md`、`_解析正文.md` 三份事实源；`_含解析.md` 由 `solution_sources.py` 确定性生成。题面从已复核转录稿规范化为可识别题号格式，Q16/Q18/Q20 链接到本批六张 TikZ 源码。答案和解析仍标为本库独立推导（非官方），Q14 明示 U/PENDING。

| 文件 | SHA-256 |
|---|---|
| 文科 `_试题.md` | `17f12653604a7c0b3ffe56bedd88ef4757d93e200de768b04eff61841f00addc` |
| 文科 `_答案要点.md` | `29367733c0a7a8120e36c38945facc17763fccd3d4dc4ce04a8c5813536298c0` |
| 文科 `_解析正文.md` | `3a7c8c5338d525fc98a5dd67b2e984c8d0d0eeaa3faa6e1058226b8eb3d17d9c` |
| 文科 `_含解析.md` | `7cad3e1bb0e63d856fe4c5fcf116470c89a60e83b1356e8894827d43930d3dc5` |
| 理科 `_试题.md` | `63fded52d5e9bf75635b3fc48545e1f09391d719e430aee9b9b56a489972856b` |
| 理科 `_答案要点.md` | `e7c687b40baed9fbca10c240aa5ab47cb3b9597464d0aa4c643d820b566a181a` |
| 理科 `_解析正文.md` | `dd4aa1f779390d052aec64ecdba989e2c97e76a3c4391068f7cf608924d2c74f` |
| 理科 `_含解析.md` | `a852b99fddd77bd9dc5486017e1617043b31e143bb5344f5a3426ee7663fcd35` |

## 登记与待核项

- 通过 `source_manifest.py register-papers --write` 新建 batch `phase4-b47` 和 paper `gk-2003-regular-shanghai-arts`、`gk-2003-regular-shanghai-science`。登记时 manifest revision `6132→6133`；随后以 `sync-figure-registry --write` 登记每卷 3 个图文件及每图 2 次引用，revision `6133→6135`。
- 文科 Q14 创建阻塞项 `ISSUE-1388`，理科 Q14 创建阻塞项 `ISSUE-1389`，类型均为 `answer-convention-ambiguous`。若平面平行要求无交点，D 仍允许两平面重合；题面没有给出互异条件，且固定来源没有答案或勘误页可裁决。按证据边界保留 U/PENDING；默认两平面互异时 D 仅为条件性预期答案。
- 两卷 `production_state=blocked`，batch 状态 `planned`。source 与纸面题签/字节绑定已核，不等于发布者、版次、来源链或官方身份核验。

## 流程校验与下一步

- `solution_sources.extract-batch --write` 后 `check-batch` 通过，两卷均为 22 题，题面、答案锚点和解析小问集合对齐；六个图引用均同步为 `expected_occurrences=2`。
- `source_manifest.py validate`、`issues.py validate` 通过；`manifest_csv.py --write` 后 `--check` 通过，投影 775 行。
- 本阶段未运行测试套件、OCR、联网或模型。尚未建立逐题 provenance、项目生成/正式 PDF、视觉回执或批次关闭回执。下一步创建并核对 provenance，再按项目规范生成 TeX/PDF，处理构建及逐页视觉审查；Q14 阻塞保持打开。

本登记不表示官方答案已核、来源已认证或整卷验收完成。

# 2003 上海普通卷文理科：规范事实源与内部卷登记

- 日期：2026-11-04。
- 文科固定候选 source `src-a2453dc34b5026e77f4d0739bc0db2e578931f651c2edf799310ddb5ccc483c4`，PDF SHA-256 `ffd59c395a0c675118f6da576e48842549c4afa031d923448f26f33087bc7e85`；题面为 PDF 第 1–2 页、原印刷页 140–141。
- 理科固定候选 source `src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0`，PDF SHA-256 `88b72fea05d331215504bb89257e375d07c18ba21e830cf9e6288461e88ccf8d`；题面为 PDF 第 1–2 页、原印刷页 138–139。
- 两份 PDF 均只有题面；发布者、版次、复制/扫描链与官方身份未核。与内部卷绑定只用于固定本库转录来源，不代表官方身份认证；`official_answer=null`。

## 规范源与指纹

两套卷均有 `_试题.md`、`_答案要点.md`、`_解析正文.md` 三份事实源；`_含解析.md` 由 `solution_sources.py` 确定性生成。题面从已复核转录稿规范化为可识别题号格式，Q16/Q18/Q20 链接到本批六张 TikZ 源码。答案和解析仍标为本库独立推导（非官方），Q14 明示 U/PENDING。

| 文件 | SHA-256 |
|---|---|
| 文科 `_试题.md` | `eea8c115e1cc7683635553ad16aa7a0128c36ab4e78c58518f40c4b3d26adbed` |
| 文科 `_答案要点.md` | `f46bad5efc183343fc54166a47f5b382f673624d669d43c26f99364fd720433c` |
| 文科 `_解析正文.md` | `21dcc3f4f636d37ac233a025ea340d8db5cc492fcd92a620c1d6e1872192c15d` |
| 文科 `_含解析.md` | `c6326585b1b28247988606c3ea862464b4205d3dd2507fa5add055dec6a945ca` |
| 理科 `_试题.md` | `847c4ee72d6a441843c03c8e1a22f5b1ad64b0cc8b1a96625869adbc9eefe851` |
| 理科 `_答案要点.md` | `76e19ab93418d2a22516d82a43278a617ef2a61f19d250ab35dd75c42b8c7804` |
| 理科 `_解析正文.md` | `991219818f01e1f534e58a65ea8a1c03dba3e9ddb8445a1984d1c549d4118794` |
| 理科 `_含解析.md` | `86495c304451b11f27e84734f906476b81e37f21a580aa2fd78b4cf99cbd0b2a` |

## 登记与待核项

- 通过 `source_manifest.py register-papers --write` 新建 batch `phase4-b47` 和 paper `gk-2003-regular-shanghai-arts`、`gk-2003-regular-shanghai-science`。登记时 manifest revision `6132→6133`；随后以 `sync-figure-registry --write` 登记每卷 3 个图文件及每图 2 次引用，revision `6133→6135`。
- 文科 Q14 创建阻塞项 `ISSUE-1388`，理科 Q14 创建阻塞项 `ISSUE-1389`，类型均为 `answer-convention-ambiguous`。若平面平行要求无交点，D 仍允许两平面重合；题面没有给出互异条件，且固定来源没有答案或勘误页可裁决。按证据边界保留 U/PENDING；默认两平面互异时 D 仅为条件性预期答案。
- 两卷 `production_state=blocked`，batch 状态 `planned`。source 与纸面题签/字节绑定已核，不等于发布者、版次、来源链或官方身份核验。

## 流程校验与下一步

- `solution_sources.extract-batch --write` 后 `check-batch` 通过，两卷均为 22 题，题面、答案锚点和解析小问集合对齐；六个图引用均同步为 `expected_occurrences=2`。
- `source_manifest.py validate`、`issues.py validate` 通过；`manifest_csv.py --write` 后 `--check` 通过，投影 775 行。
- 本阶段未运行测试套件、OCR、联网或模型。尚未建立逐题 provenance、项目生成/正式 PDF、视觉回执或批次关闭回执。下一步创建并核对 provenance，再按项目规范生成 TeX/PDF，处理构建及逐页视觉审查；Q14 阻塞保持打开。

本登记不表示官方答案已核、来源已认证或整卷验收完成。

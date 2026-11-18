# 2005 年封年：phase4-b94 … b99 批次清单冻结

- 冻结时间：2026-11-09
- 分支 / 工作树：工作分支（`仓库根`）
- 基线提交：`a0fae969e`（docs: 更新项目交接与进度记录至 phase4-b93）
- manifest revision：6683（775 sources / 464 papers / 310 batches）

## 1. live 状态核对（task-1 证据）

| 项目 | 实测值 |
| --- | --- |
| `git status --short --branch` | `* 工作分支...origin/工作分支` + 仅 `?? scratch/`（会话开始前既有，非本次创建） |
| `PROGRESS.md` 末尾回执 | phase4-b80（天津理科）；顶部回执与 `reports/phase4-b93.md` 一致（福建理科，63 页，四版 succeeded，0 问题） |
| 2005 已登记卷 | 26 套：`complete` 23，`blocked` 3 |
| 2005 未分配来源 | **6 个**（下表） |
| README 统计 | 464 卷 / 775 源；blocked 111、compiled 3、complete 350；1856/1856 版本已编译 |

### 1.1 阻塞卷（不在本清单增量内，需来源侧证据）

| 试卷 | 阻塞原因 | 续做动作 |
| --- | --- | --- |
| `gk-2005-regular-national-1-science` | 第 4 题选项 C 需清晰勘误或同版源确认 | 取得勘误/同版源后解阻 |
| `gk-2005-regular-shanghai-arts` | "最小"是否允许并列 | 取得可追溯同版答案/解析/勘误 |
| `gk-2005-regular-shanghai-science` | "最小的一个四棱柱"唯一性 | 同上 |

## 2. 冻结的批次（6 套新卷，严格按 b94 → b99 顺序执行）

| 批次 | paper_id | 上游来源 | SHA-256 | 字节 | 页 |
| --- | --- | --- | --- | --- | --- |
| phase4-b94 | `gk-2005-regular-liaoning` | `普通高考/2005/2005辽宁.pdf` | `08a3f76c37665b93b985abe546c5a5b709d5445e6d00bc8340b743e87581a28a` | 535787 | 2 |
| phase4-b95 | `gk-2005-regular-jiangsu` | `普通高考/2005/2005江苏.pdf` | `29ccab1b5b7d579a0e8e4124fa5f2f732ebb2436d570b7529e6dbce988cd4dde` | 508805 | 2 |
| phase4-b96 | `gk-2005-regular-national-3-arts` | `普通高考/2005/2005全国3文(四川,云南,贵州,甘肃,陕西,青海,西藏).pdf` | `0ccbff13e3d195ac7420ec7ccd0ee34064aef285217cfae4228d45fd051863e9` | 500254 | 2 |
| phase4-b97 | `gk-2005-regular-national-3-science` | `普通高考/2005/2005全国3理(四川,云南,贵州,甘肃,陕西,青海,西藏).pdf` | `a5c45d0c0d338915e398faf55e9662a294e21e02f22f97e0eb16da2ed2d7bb11` | 507137 | 2 |
| phase4-b98 | `gk-2005-regular-zhejiang-arts` | `普通高考/2005/2005浙江文.pdf` | `a61b752378b1a6670c3328d1e9b1aa19507cc51fd4fba66895f1976b779cdd6f` | 505812 | 2 |
| phase4-b99 | `gk-2005-regular-zhejiang-science` | `普通高考/2005/2005浙江理.pdf` | `d552fffa21812b159fe5fd81fb5ee4376e6ad1992f364c2df121b84e40f5b884` | 513209 | 2 |

上游固定 commit：`34c13a6cf632c0b69c95f89b9b923bbc4a08924d`（`https://github.com/deekur/gaokaomath`）。
上游文件读取自 `gaokaomath-src/`（只读；该目录被 main 的 `.gitignore` 忽略）。

manifest 的 source 记录只有 `artifact`（含 `sha256`/`page_count`/`size_bytes`）与 `source_state`，没有独立的物化路径字段；本计划立项时这 6 个 source 均未登记 `artifact`，需在各自批次里先实测回填，不得手填未经实测的值。

## 3. 每套卷的固定流水线（沿用 phase4-b78…b93）

1. 物化 + 源认证：PDF 落 `.work/ocr-local/sources/`，`pdfinfo` 取页数，回填 SHA/字节/印刷页码与题签；写 `reports/2005-<region>-source-intake.md`。
2. 题面转录：逐页渲染 → 四层 Markdown（`_试题.md`/`_答案要点.md`/`_解析正文.md`/`_含解析.md`）。
3. 图形：示意图/函数图象/立体图全部 TikZ 矢量重绘，存 `figures/f<year>_<region>_q<NN>_<kind>.tex`；原始扫描图只在无可回避时进附录。
4. 独立推导：解析一律标"非官方·独立推导"，脚本复算或第二代理盲核；证据等级 A/B/C/D/U 逐题记录。
5. 投影：`questions.tex`/`answers.tex`/`answers_short.tex`/`provenance.json` + 四个版本壳。
6. 构建：`build_projects.py` 四版，回执哈希一致，0 error / 0 missing char / 0 overfull（或带豁免）/ 0 undefined ref。
7. 视觉审查：逐页 8 类检查，`review_receipts.py prepare-batch` → `finalize-batch`。
8. 封账：`reports/phase4-bNN.md`、`report.py render --all` + `check --all`、`manifest_csv.py`，更新 `PROGRESS.md` 与交接文档。

## 4. 所有权（并行纪律）

- 内容代理只写 `.work/phase4-bNN/<paper>/`，不得碰 `source-manifest.json`、`index.json`、`PROGRESS.md`、`missing-issues.md`、`tests/`、`2005/*.md`。
- 共享文件（manifest / index / PROGRESS / 交接 / reports 汇总）与全部提交由主代理独占。
- 同一时刻至多 4 个内容代理；禁止嵌套派发；提交前 `git status` 核对未夹带他人改动。

## 5. 验收口径（每批）

- `tests/test_2005_<region>_solutions.py` 通过；
- 四版 `receipts/build.json` 全 `succeeded`；
- `receipts/review.json` 逐页通过，无未豁免视觉问题；
- `review_receipts.py check-batch` 通过，批次 `closed`、卷 `eligible_complete`；
- `report.py check --all` 与 `manifest_csv.py` 全量一致；
- 不改动 3 套既有 blocked 卷的状态与 issue。

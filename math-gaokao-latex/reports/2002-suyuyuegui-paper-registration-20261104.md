# 2002 苏豫粤桂卷：规范事实源与内部卷登记

- 日期：2026-11-04；工作树 `仓库根`；工作分支。
- 本报告记录固定题面来源下的规范事实源、内部 paper/batch 登记和题图引用登记，不认证来源发布者、版次、复制链或官方身份。

## 固定来源与规范事实源

- source `src-0daae2fa54742835e68d7f3b2cb647b26cee7c4d302f16958e53100e71e4bab4`：PDF SHA-256 `4dd869fb3bc24cda6947ab2c2069ed3f470b70f775c5679064f8c5a95f43bc91`，Git blob `24ff45c0af6a8707358e31392c08cb4e2c96a32f`，固定两页 A3，原件印刷页 113–114，无答案或评分页。
- 已形成 Q1–Q22 三层规范源：题面、答案要点和解析正文。`official_answer=null`；答案和解析是本库独立推导。source 保持 `track=null`、`regions=[]`，paper `track=none` 仅表达本库没有文理分类。
- 四份规范/派生文件 SHA-256：

| 文件 | SHA-256 |
|---|---|
| `_试题.md` | `1ac12c75343cfd427138b7f296f79c3320519c1036f3fafd111a0e4226e2722a` |
| `_答案要点.md` | `f2f557206074d4dedd203cd90cc663f41b4643ff4d2e511f3a64dd6b28a43b3e` |
| `_解析正文.md` | `d7a330f789fc79f1828233ece647bb0c713201dbe3e9351d18f49fce28118820` |
| `_含解析.md` | `dc07b73b5836d1334238e44aa70c4fdff0ab3992539fa72c97d6ea30a6607379` |

Q18 题面只写“等比数列”，没有说明公比是否非零。答案与解析保留 `q=0` 和 `q=±1/√2` 条件分支，并标记 `U/PENDING`。

## 登记与题图

- `register-papers --write` 登记 `gk-2002-regular-suyuyuegui` 与 `phase4-b50`，并将 source 以 `canonical` 关系绑定。manifest revision `6178→6179`；随后 `sync-figure-registry --write` 把 revision 推进至 `6180`。
- Q18 建立 `ISSUE-1417`（`answer-convention-ambiguous`，`open / blocks_completion`）。paper 状态为 `blocked`、`blocked_from=planned`，batch 状态为 `planned`。
- 登记四张图：Q10 选项图、Q19 四棱锥图、Q21 原题三角形图、Q21 答案剪线图。按题面与当前确定性 `_含解析.md` 中的实际引用，`expected_occurrences` 依次为 `2、2、2、1`。

## 验证与剩余工作

- `solution_sources.render_combined` 对三层源成功；`extract-batch --write` 提交两个目标，`check-batch` 显示 22 题通过。
- `source_manifest.py validate` 与 `issues.py validate` 均通过。`manifest_csv.py --check` 输出“manifest.csv 当前且 775 行”；`report.py check --all` 输出“报告输出与全量 manifest 当前一致；未完成状态已在报告中保留”。当前全量快照报 266 个 `INVALID_OR_STALE`、1 个历史 `VISUAL_FAILED`；新卷项目生成尚未刷新共享 `index.json`，须在后续生成后重新运行回执验证与全量报告检查，不能把此过渡快照当最终批次门禁结论。
- 本阶段没有调用 OCR、没有导入逐题 provenance、没有生成项目 TeX/简答/四版入口，也没有正式构建、PDF 视觉回执或批次关闭。OCR 调用为 0；模型 token / 费用不可见，记未知。
- 下一阶段按最终事实源导入 Q1–Q22 的题面复核、盲解和答案复核 provenance，重点保留 Q18 blocker；之后再生成 TeX 与四版入口并做确定性核对。

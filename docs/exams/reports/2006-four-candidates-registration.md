# 2006 广东、江苏、江西文、浙江文：paper/source 登记与问题入账

日期：2026-11-02。

## 登记范围

批次 `phase1-b69` 登记以下四套 2006 候选卷；注册事务将 manifest revision 从 `5791` 推进至 `5792`，随后更正浙江文科登记注记的印刷页码为 PDF intake 所载 342–343，revision 到 `5793`：

| Paper ID | 固定 Source ID | 题数 | 登记状态 |
|---|---|---:|---|
| `gk-2006-regular-guangdong` | `src-e0c5020a85c6b155cb454ed921b44ba51adb3067a3998d7ee6020674ed5b4e24` | 20 | `blocked` |
| `gk-2006-regular-jiangsu` | `src-25169d2a434a7b2533aeaf510aa9ee6406808e72e43f9bc75d95c2737c09de13` | 21 | `planned` |
| `gk-2006-regular-jiangxi-arts` | `src-6eedba8c015f6631959cccdffc0f2b5e63fbc71b424490f1ea554ea6ed7b3be2` | 22 | `blocked` |
| `gk-2006-regular-zhejiang-arts` | `src-59546e1a9f2fb01cc7a4ae820d82001a86aa1ee61cc2eb5320aab728375c8e1b` | 20 | `planned` |

各 source 已通过 manifest 内固定字节校验并以 `canonical` 关系绑定到对应 paper；这仅用于本库引用固定候选文件，不认证发布者、出版版次、来源链或官方原件身份。四份固定 PDF 均未见答案材料，四卷 `official_answer` 继续为 null。江苏原题题签未标科类，其 paper/index variant 显式登记为未知，不推定文理卷。

## 阻断问题

- 广东卷：`ISSUE-1298`（Q6 对象名缺失，`transcription-ambiguous`）、`ISSUE-1299`（Q16 未定义随机变量/联合模型，`transcription-ambiguous`）、`ISSUE-1300`（Q19 条件矛盾，`answer-conflict`）、`ISSUE-1301`（Q20(1) 定义域冲突，`transcription-ambiguous`）、`ISSUE-1302`（Q20(3) 任意初值下逆像存在性不足，`answer-conflict`）。均为 open / `blocks_completion`；原题与 U/PENDING 不作猜测性改写。
- 江西文科：`ISSUE-1303`（Q4 选项逻辑关系与题问不匹配）及 `ISSUE-1304`（Q8 选项不含比例分层配置），均为 open / `blocks_completion`，答案保持 U/PENDING。
- 江苏、浙江文科本次无已知逐题 blocker；此状态只代表当前题面与非官方推导草稿没有发现未决答案冲突，不证明来源身份，也不表示正式验收。

为满足逐题 provenance 对 U 答案必须关联 `answer-missing` blocker 的门禁，后续状态事务另增 `ISSUE-1305`–`ISSUE-1310`：广东 Q6/Q16/Q19/Q20 分别一条、江西文科 Q4/Q8 各一条。它们与既有题面/答案冲突 issue 配对，不替代、不关闭原 issue；追加后 manifest revision 为 `5794`，provenance 导入再推进至 `5795`。完整逐题记录见 `reports/2006-four-candidates-provenance.md`。

## 规范源绑定与验证

将 paper_id 写入四卷规范题面、答案要点和解析正文。依 `solution_sources` 确定性生成四份 `_含解析.md` 和四份 `_解析正文.md` 投影。登记字段由固定源指纹、原页可见结构与逐题复核证据组成，并经 `register-papers` dry-run 校验后写入。

验证结果：`source_manifest.py validate` 成功；`issues.py validate --file missing-issues.md` 成功；`solution_sources.py check-batch --manifest source-manifest.json --batch phase1-b69` 返回四卷全部通过；`git diff --check` 成功。登记前 `register-papers` dry-run 校验规格通过；随后事务写入成功，新增四 paper、一 batch 和七条逐题问题。

## 后续边界

尚未建立逐题 question-review / answer-solve / answer-review provenance，未制作和登记题图，未生成项目 TeX 与简答版，未做正式 PDF 构建、全页视觉审阅或批次收口。两套 blocked 卷必须先解决相应 open blocker；planned 卷也仍需完成来源/答案 provenance 和后续项目门禁。本阶段不表示任一卷已闭环，更不表示 1952–2026 长期语料完成。

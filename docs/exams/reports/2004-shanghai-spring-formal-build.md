# 2004 上海春季卷：四版正式构建

日期：2026-10-31

- 批次 `phase1-b62`，卷件 `gk-2004-spring-shanghai`。当时 attempt `3074e568-0549-4cbf-9306-9a77af09df4c`，已被下述回流构建取代，构建输入 manifest revision 5528，完成后 revision 5529；2026-10-31 13:15:49—13:16:07（本地时区）。正式回执位于 `2004_春季上海卷/receipts/build.json`。
- 试题、解析、简答、印刷版分别为 4、19、6、15 页，共44页；四版均 succeeded，日志中的 error、missing character、undefined reference、Overfull 与 Underfull 均为0。PDF SHA-256 依次为 `bc63e1cedbcb6cdd0c19cd9290e6f94ead5b17d15a42c35e6fbc2176e4ae4bd8`、`173eec92a1b1f117da5bc672e48790879bf4f56def3251627031c93dba089cef`、`bf55e275a97eb965f47c3aa871dd57b05c4325a3f5abdf43e65f4809f227ddc7`、`6011a08f15346bdc1e5a337dde8fec28d904cf3663296a1c7450536b9b316bff`。
- 首次 attempt `4129af29-a997-44bc-afc5-3558dbfc05ac` 四版失败：生成题面来源说明中的裸下划线 `paper_id` 在 `questions.tex:8` 触发 `Missing $ inserted`。规范题面改为中文“卷件标识”，生成 TeX 后重编；四条非阻断编译 issue `ISSUE-1267`—`ISSUE-1270` 随成功构建解决。中间成功 attempt `6b20d821-5d68-43be-8a54-0c8ca9f3950b` 后，卷目注记更新为构建完成、视觉待验；最终 attempt 随后重建以绑定该注记。
- 该阶段 build receipt 为 `compiled_pending_review`，当时四版44页待逐页视觉检查；paper 因 `ISSUE-1264`、`ISSUE-1265`、`ISSUE-1266` 保持 blocked。固定来源出版者、版次、来源链及官方身份未核，答案为本库非官方推导。构建成功不表示本卷或长期题库完成。

## 视觉初检回流与新构建（2026-10-31）

- 对 attempt `3074e568-0549-4cbf-9306-9a77af09df4c` 做视觉初检：试题、简答及解析版中 Q13（D）标签与公式分行，Q14（D）文字拆行；解析版末页仅余 Q22（3）答案框；首页图表说明留有“暂不作为正式 LaTeX 构建输入”的过时状态。初检还提示印刷版第7页 Q7 行距较紧，须在新构建中复核。本次初检不是旧 attempt 的全页视觉通过结论。
- Q13/Q14 仅添加选项换行；删除过时状态句。Q22（3）解析把重复显示公式改写为逐区间距离的文字及行内表达式，完整分段函数继续保留在答案要点和生成答案框；数学结论未改。Q13/Q14 当前题面哈希已重导入 provenance，既有来源核对的时间边界仍记录。
- 新 attempt `7de1258f-7b9c-4b52-9416-e295824edbc2` 输入 manifest revision 5531，完成后 revision 5532；四版依次 4/18/6/15 页，共43页，均 succeeded，error、missing character、undefined reference、Overfull 与 Underfull 为0。PDF SHA-256 依次为 `74ad932993dd143ae2a22cf480afe308bcd207e569cd47880aeebdbe6f515e41`、`3b82e24feedf5294c19990b55be149fd1432f36e7300e4addf47ce4f510b8455`、`bfe7a957e3765206a602543a8867fc0e5ebc73524b6d393920d0e53486274`、`9d3ed1d3f0f2f36f428bbd6c44fc8d0fc3ad391e16a2df19cda7c28bbb3db6c0`。
- 主流程目视新试题版第1、3页及解析版第18页：过时说明已去除，Q13/Q14 选项完整换行，Q22 三个答案框同页且分段函数完整。其余页面及四版完整八项检查仍待完成；build receipt 当前、review pending，`ISSUE-1264`—`ISSUE-1266` 保持开放阻断。

## 最终回执更新

卷目注记改为引用正式回执，避免视觉完成后仍写“待完成”；最终 attempt `3c1f0efa-edf1-4344-8272-2cfda8606be9` 以 revision 5535 构建，四版仍为 4/18/6/15 页。其43页90 dpi PNG 与已实际审查的 attempt `7de1258f` 逐页字节相同，最终 review 绑定新 attempt 并继承实际视觉结论；`phase1-b62` 在 revision 5537 收口为 `closed_with_blockers`。详见 `reports/2004-shanghai-spring-formal-review.md` 与机器可读回执。

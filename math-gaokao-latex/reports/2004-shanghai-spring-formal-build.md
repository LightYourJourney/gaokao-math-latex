# 2004 上海春季卷：四版正式构建

日期：2026-10-31

- 批次 `phase1-b62`，卷件 `gk-2004-spring-shanghai`。最终 attempt `3074e568-0549-4cbf-9306-9a77af09df4c`，构建输入 manifest revision 5528，完成后 revision 5529；2026-10-31 13:15:49—13:16:07（本地时区）。正式回执位于 `2004_春季上海卷/receipts/build.json`。
- 试题、解析、简答、印刷版分别为 4、19、6、15 页，共44页；四版均 succeeded，日志中的 error、missing character、undefined reference、Overfull 与 Underfull 均为0。PDF SHA-256 依次为 `bc63e1cedbcb6cdd0c19cd9290e6f94ead5b17d15a42c35e6fbc2176e4ae4bd8`、`173eec92a1b1f117da5bc672e48790879bf4f56def3251627031c93dba089cef`、`bf55e275a97eb965f47c3aa871dd57b05c4325a3f5abdf43e65f4809f227ddc7`、`6011a08f15346bdc1e5a337dde8fec28d904cf3663296a1c7450536b9b316bff`。
- 首次 attempt `4129af29-a997-44bc-afc5-3558dbfc05ac` 四版失败：生成题面来源说明中的裸下划线 `paper_id` 在 `questions.tex:8` 触发 `Missing $ inserted`。规范题面改为中文“卷件标识”，生成 TeX 后重编；四条非阻断编译 issue `ISSUE-1267`—`ISSUE-1270` 随成功构建解决。中间成功 attempt `6b20d821-5d68-43be-8a54-0c8ca9f3950b` 后，卷目注记更新为构建完成、视觉待验；最终 attempt 随后重建以绑定该注记。
- 当前 build receipt 为 `compiled_pending_review`，四版所有44页尚待逐页视觉检查；paper 因 `ISSUE-1264`、`ISSUE-1265`、`ISSUE-1266` 保持 blocked。固定来源出版者、版次、来源链及官方身份未核，答案为本库非官方推导。构建成功不表示本卷或长期题库完成。

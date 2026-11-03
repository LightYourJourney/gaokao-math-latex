# 2007 上海文科候选卷：四版正式构建（Q21 分页修正后）

- 日期：2026-11-03。
- Paper：`gk-2007-regular-shanghai-arts`；batch：`phase1-b83`。
- Build attempt：`f8997e0e-2c2d-4a29-a7fc-c35519b32d9a`；输入 manifest revision `6058`；构建完成后 revision `6059`，事务 `b9048be7-c32a-4789-ae33-df976d226469`。
- 上一 attempt `9a6f2b2e-45da-4851-a97e-beef2fc9f00b` 因 Q21(3) 解析源的分页回流而失效。现印刷版 15 页，原先只剩两条答案框的第 16 页已消失。
- Toolchain：TeX Live 2026；XeTeX `3.141592653-2.6-0.999998`；Poppler 26.10.0。完整工具指纹与输入树哈希保存在 `2007_上海卷_文科/receipts/build.json`。

## 输出

四版均单次 XeLaTeX 编译成功；日志均无 TeX 错误、缺字、Overfull 或未定义引用。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 4 | `9da51332e9d0bc99ffcb4c06c91042b38b6eca66cebee9517106d6b5f3610567` |
| 解析版 | 17 | `25f8588f19047c63d118e360cb7bec1251ef9b34eba2049c2946331336f29452` |
| 简答版 | 6 | `cac2135d37f39c585cd8f80c4ac8ac8e6b88ef2ee5ef0a5389853c8bb0fc8379` |
| 印刷版 | 15 | `203ca7edd496b12d261d9682d9ec48ec14f8fe5939203d14a92752d4fd64ccd6` |

PDF 位于忽略目录 `2007_上海卷_文科/build/`，构建回执位于 `2007_上海卷_文科/receipts/build.json`。`build_projects.py validate-receipts --manifest source-manifest.json --batch phase1-b83 --require-current-inputs --json` 返回 `code=OK`、0 failed、0 invalid、0 missing、0 stale；批次有 1 卷 pending，等待正式视觉回执聚合。

## 阶段边界

新四版共 42 页渲染：40 页 PNG 与修正前 attempt 的直接目检图像 SHA-256 完全一致，沿用原八项目检结论；解析版第 17 页、印刷版第 15 页重新以 110/300 dpi 检查。印刷版 16 页的新末页问题已消除，所有答案框与 Q21 完整解答同页。逐页回执已填写，尚待批次聚合提交。

Q21(3) 仍为 U/PENDING / ISSUE-1362，paper `blocked`，`official_answer=null`，固定来源出版身份未核。本阶段只完成重建与页面检查，不表示本卷闭环或长期语料完成。

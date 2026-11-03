# 2007 上海文科候选卷：四版正式构建

- 日期：2026-11-03。
- Paper：`gk-2007-regular-shanghai-arts`；batch：`phase1-b83`。
- Build attempt：`9a6f2b2e-45da-4851-a97e-beef2fc9f00b`。
- 构建输入 manifest revision：`6055`；完成 receipt 后当前 revision：`6056`，事务 `d79981ee-69da-4ad8-b6c9-8b1880c0bebb`。
- Toolchain：TeX Live 2026；XeTeX `3.141592653-2.6-0.999998`；Poppler 26.10.0。完整工具指纹与输入树哈希保存在 `2007_上海卷_文科/receipts/build.json`。

## 输出

四版均单次 XeLaTeX 编译成功；日志均无 TeX 错误、缺字、Overfull 或未定义引用。

| 版本 | 页数 | PDF SHA-256 |
|---|---:|---|
| 试题版 | 4 | `769456ed96f447393f389f600158c2b22a6520fbeeec3f3af926c6f58486b586` |
| 解析版 | 17 | `488426717759e5073b07701695dd273d10c1134e9bb7b73dbe850cde2c6bac83` |
| 简答版 | 6 | `be62f17a4a77889aeb543af7ea9dbe28ca5b208bc14a517af699f1e2954cd1ae` |
| 印刷版 | 16 | `c968373a965c6d58c6f7165cae88b3ed5392eed28c325ef10049404aad5f3167` |

PDF 位于忽略目录 `2007_上海卷_文科/build/`，构建回执位于 `2007_上海卷_文科/receipts/build.json`。`build_projects.py validate-receipts --manifest source-manifest.json --batch phase1-b83 --json` 返回 `code=OK`、0 failed、0 invalid、0 missing、0 stale；批次仍有 1 卷 pending，等待视觉审查。

## 阶段边界

四份 PDF 尚未逐页渲染和视觉裁决，当前 build 状态为 `compiled_pending_review`；不得把无 TeX 警告当作页面视觉合格。Q21(3) 仍为 U/PENDING / ISSUE-1362，paper `blocked`，`official_answer=null`，固定来源出版身份未核。下一阶段对 43 页逐页检查并写入与本 attempt、manifest、PDF SHA 和工具链绑定的视觉回执；本阶段不表示本卷闭环或长期语料完成。

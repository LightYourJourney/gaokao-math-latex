# 2026 北京高考数学回忆版候选卷：固定来源接收与文字层路由

- 日期：2026-11-04；canonical worktree：`仓库根`；分支：`feat/gaokao-phase0`；source manifest revision：6159。
- 固定候选 source：`src-96ac0e772a0483bbf7cf803b94b1a1d8d8e1d2ae16b936b196e6abc05d1251ee`，manifest 相对路径 `普通高考/2026/2026北京.pdf`。manifest 状态为 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`；本阶段未改 manifest，也未建立 paper/batch 绑定。
- 只读来源 checkout：`gaokaomath-src`，HEAD `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`，工作区干净。PDF 大小 365,585 bytes；现场 SHA-256 `7e840dc5c259cf05138337178794a58b6593dc7f2bf0d693826489856da416e9`，Git blob `cf49aa3671ff4143e5c665c7bc53b5f08ab38fca`，与 manifest 相符。
- PDF 共 5 页，A4 纵向（595.44 × 842.04 pt）。首页题签可见“2026 年北京高考数学真题（回忆版）”；此题签只记录副本自称，不认证发布者、出版者、版次、来源链或官方身份。

## 页面结构与文字层路由

| PDF 页 | 可见范围 |
| --- | --- |
| 1 | Q1–Q10 开始；Q10 选项续至第2页 |
| 2 | Q10 选项续页；Q11–Q16 |
| 3 | Q17–Q18 |
| 4 | Q19–Q20 |
| 5 | Q21，含两个数阵表 |

- 每页都有文字层；`analyze_pdf.py --no-cache --include-text` 将文档标为 `text_with_raster_content_candidate`，五页均为 `text_candidate`。非空白字符数依次为 814、558、415、254、280；机器检测的可疑字符均为 0。第1页含一个 2×2 占位图像对象，第2页含摇杆与三棱锥图，第3页含三棱柱图，第4–5页没有图像对象。文字提取只作为定位候选，不证明公式或图形标记忠实。
- 五页以 Poppler 26.10.0、120 DPI 渲染并逐页查看。页图和 `analyze_pdf.py` 原始输出保存在忽略目录 `.work/ocr-local/sources/2026-beijing/`。本 PDF 有可用文字层，无 raster-only 页面；依 `docs/OCR_WORKFLOW.md` 不启动 OCR，`ocr_calls=0`、`model_calls=0`。题面中的公式、数阵和图形仍须在转录时逐题对原页核对。
- 未见答案页或解析页；来源候选只覆盖题面 Q1–Q21。

## 边界与下一步

本阶段核对了固定 PDF 的 SHA、Git blob、大小、页数、版面方向、首页题签、题号范围和文字层路由。首页明确自称“回忆版”，来源发布者、出版者、版次、原始发布渠道、复制链和官方身份均未核实。该候选尚未绑定到独立 paper，不能与 2026 全国 I 回忆版混同，也不能据题签推定与任何正式卷一致。下一阶段应先为这份回忆版建立独立跟踪范围，再开展题面转录与隔离复核；所有疑点保留原字并标记，不补造缺失条件或答案。本报告不表示题面或整卷完成。

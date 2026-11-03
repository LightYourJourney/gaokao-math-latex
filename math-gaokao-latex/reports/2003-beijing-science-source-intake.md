# 2003 北京理科候选卷：固定来源接收与文字层路由

- 日期：2026-11-04；canonical worktree：`仓库根`；分支：`feat/gaokao-phase0`；source manifest revision：6146。
- 固定候选 source：`src-120ea104f8cb373f5731039fa9d36469df457869849f27420831962ef1ad2306`，manifest 相对路径 `普通高考/2003/2003北京理.pdf`。manifest 状态为 `ready`，`paper_id=null`、`paper_relation=null`、`track=null`；本阶段未修改 manifest 或建立 paper/batch 绑定。
- 固定来源 checkout：`gaokaomath-src`，HEAD `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`，工作区干净。PDF 大小 507,308 bytes；现场 SHA-256 `d0081500bd56d03199ddcf232fe8e870f2ecd7e9c41ba849417af9af79fbb702`，Git blob `1f3cde756f4b417da80d0bb4b7cf2501e1ffad37`，均与 manifest 相符。
- PDF 为 2 页 A3 横向（1190.55 × 841.89 pt），未加密。页内题签可见“2003 普通高等学校招生考试（北京卷理）”，印刷页码 124–125；该题签只作为页面可见文字记录，不认证出版者、版次、来源链或官方身份。

## 页面结构与文字层路由

| PDF 页 | 印刷页码 | 可见范围 |
| --- | ---: | --- |
| 1 | 124 | Q1–Q17；选择题 Q1–Q10、填空题 Q11–Q14、解答题 Q15–Q17 |
| 2 | 125 | Q18–Q20 |

- `analyze_pdf.py --no-cache --include-text` 的文档级结果为 `text_layer_candidate`，文档完整；第 1、2 页分别有 1,527、727 个非空白字符，各检测到 7 个可疑字符，两页页级分类均为 `review`。页面有文字层且无图像对象；文字抽取的跨栏阅读顺序、公式和字形风险须由原页图复核。
- 两页以 Poppler 26.10.0 的 `pdftoppm` 渲染并逐页查看；页面图和原始分析 JSON 保存在忽略目录 `.work/phase4-b48/intake/main/`。完整可见题号范围为 Q1–Q20；本阶段未发现答案页或解析页。
- 按 `docs/OCR_WORKFLOW.md`，已有文字层保留为候选；本阶段 `ocr_calls=0`、`model_calls=0`，未调用 Xiaomi-OCR-0、PaddleOCR-VL-1.6、MinerU 或外部来源。可疑抽取字符通过直接查看整页原图处理，没有以 OCR 输出替代源页。

## 边界

本阶段固定并复核了候选文件字节、PDF 页数/尺寸、题签、印刷页码、题号范围和文字层路由。发布者、出版者、版次、原始发布渠道、复制/扫描链和官方身份均未核实；来源仍是未绑定候选。题面草稿与独立复核已在忽略工作区完成；原页可见 Q17“底面边长的 3”存在句意异常，转录照录并列为待核，未据语义补字。下一阶段将把题面和复核记录纳入跟踪目录。本报告不认证来源，也不表示题面或整卷已完成。

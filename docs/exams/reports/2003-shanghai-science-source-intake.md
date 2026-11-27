# 2003 上海理科普通卷：固定来源接收

- 日期：2026-11-04；canonical worktree `仓库根`，工作分支。
- 候选来源 `src-1c1b7702523f8dab3f1fb274ae6d8c631a291090d33ddb6e3d9f3d8de897a1d0`，manifest revision 6132 中为 `ready`、`paper_id=null`、`paper_relation=null`、`track=null`。上游相对路径 `普通高考/2003/2003上海理.pdf`。
- 固定上游 checkout `gaokaomath-src`，HEAD `34c13a6cf632c0b69c95f89b9b923bbc4a08924d`。现场文件 SHA-256 `88b72fea05d331215504bb89257e375d07c18ba21e830cf9e6288461e88ccf8d`、Git blob `d8679fb9dee874be062e92b436dbabbbcb41eb85`、大小 594899 bytes，与 manifest 一致；`pdfinfo` 页数为2，A3横向，页面尺寸1190.55 × 841.89 pt。

## 原页结构与内容路由

- 两页题签为“2003 普通高等学校招生考试（上海卷理）”，印刷页码138–139，题面共22题：填空Q1–Q12、选择Q13–Q16、解答Q17–Q22。第1页含Q1–Q19，第2页含Q20–Q22；原页有三个图位：Q16函数图、Q18平行六面体图、Q20隧道拱线图。未见答案、解析或评分页。
- `python3 tools/analyze_pdf.py --no-cache --include-text` 判为 `text_layer_candidate`：第1页 `text_candidate`、1583个非空白字符、0个可疑字符；第2页 `text_candidate`、530个非空白字符、0个可疑字符；两页 `image_objects=0`，内容证据为 `text_layer`。`pdfimages -list` 未列出嵌入位图。
- 已将两页分别渲染为150 DPI和300 DPI PNG并直接目视检查。题签、页码、题号范围、题面主体、Q16/Q18/Q20图位均可辨；文字层仅作定位，后续逐题转录须继续以原页图核对，不能将机器抽取文字直接视作规范题稿。
- 转录核对时发现一处重要抽取差异：固定 PDF 第2页 300 DPI 原图的 Q22 是函数集合 (M) 题；同页文字层却在 Q22 位置抽取出等比数列组合和题，而该题实际印在第1页 Q19。此为文字层与可见页内容的明显不一致，Q22 必须按渲染原图转录，不能采用该处抽取文本。此前只确认文字层存在，未验证此项内容对应关系；本补记修正该限制。
- 本阶段未调用OCR或生成式模型：`model_calls=0`、`ocr_calls=0`。无外部API调用。

## 边界与下一阶段

本报告只记录固定候选来源、文件指纹、页序结构和文字层路由；未创建规范题面、答案、解析、卷目录或paper/batch登记，也未改 manifest/issues。发布者、出版者、版次、复制/扫描链和官方身份均未核实，`official_answer` 未认证。下一阶段逐题转录Q1–Q22并记录来源内疑点，随后由独立复核对照固定原页。本报告不表示来源身份认证、题面转录完成、答案验证或整卷验收。

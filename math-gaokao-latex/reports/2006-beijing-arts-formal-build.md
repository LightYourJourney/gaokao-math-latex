# 2006 北京文科候选卷：四版正式构建

日期：2026-10-30

## 构建结果

- 批次 `phase1-b60`，试卷 `gk-2006-regular-beijing-arts`；正式构建 attempt `d3bf6424-8f6d-45c0-92e7-5be594f3a9bc`，结束于 `2026-10-30T09:53:53+08:00`。构建输入 manifest revision `5488`，完成后当前 revision `5489`。此 attempt 取代先前绑定旧目录注记的 `47d7ac49-05f4-4dfc-a156-83e9b488bf1e`。
- 四版试题/解析/简答/印刷共45页；工具链为 XeTeX / TeX Live 2026、latexmk 4.88、Poppler 26.10.0。完整工具指纹、输入树、每版日志与 PDF SHA-256 由 `2006_北京卷_文科/receipts/build.json` 绑定记录。

- 试题版：5 页，SHA-256 `1e9f0bae66e3ee00d587f2b62379e63b374c7721479a040a2065a87ee383b77f`。
- 解析版：19 页，SHA-256 `971bb91f706d8ee0f01dc35fd2203d0d981024411823123da5ad7f27184d1590`。
- 简答版：7 页，SHA-256 `2ac26862bf9ea6ed344d43a631561504c7dd14c905dc68136caec029f7419df8`。
- 印刷版：14 页，SHA-256 `14745b63a88ecd9b0212d461192ac0644f270813d2de5041bc7cf81708c53943`。

- 四版均编译成功；错误、缺字、未解析引用和 Overfull 均为 0。`source_manifest.py validate` 与三种生成器 `--check` 均通过。`build_projects.py validate-receipts --batch phase1-b60 --require-current-inputs --json` 返回 `OK`，missing/invalid/stale 均为 0，仍有 1 个 review pending。`manifest.csv` 投影为 775 行并已刷新。
- 构建 wall time 约 11.8 秒。未运行测试套件。

## 阶段边界

- 此记录只确认四版正式构建成功。45 页视觉审查尚未完成；下一阶段必须对本 attempt 的四份 PDF 逐页检查并生成 review receipt。
- 固定候选 PDF 只作本库内部 canonical 固定字节绑定；发布者、版次、来源链及官方身份未认证。PDF 无答案页，答案为本库独立推导、非官方，`official_answer=null`。三幅新图稿尚待视觉校样。本卷不因此视为完成，也不表示长期语料库完成。

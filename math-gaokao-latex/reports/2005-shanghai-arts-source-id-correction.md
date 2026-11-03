# 2005 上海文科普通卷：source ID 更正记录

- 日期：2026-11-03。
- 固定来源文件 SHA-256：`952989a262e3f7b34a425ccb6e2132af7e88408a387edae50f59a9505ebe46a1`。
- Git blob：`d3849e9bf2f21c95b4823be90b24669b74ee1685`；大小512658 bytes；2页。

## 更正内容

在转录、答案与复核材料整理时，source ID 曾被人工抄写为错误值：

```text
错误：src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d028e2d0bdb1638bb8d17846
正确：src-88b71f0fa7eccf6a3db8fdf7ce80e432fa2c3d5d0288e2d0bdb1638bb8d17846
```

以 manifest 中与上述 PDF SHA-256、Git blob、文件大小和页数一致的来源记录为准，已更正题面、答案要点、解析正文、含解析稿、PROGRESS 及四份题面/答案阶段报告中的引用。旧值已从事实源、既有转录/答案报告和 manifest 中移除；本更正记录仅为审计目的保留旧值。来源 PDF 和其字节、上游路径、SHA-256、Git blob、页数均未改动；本次只修正引用身份，不重选来源，也不据此认证官方性。

该问题来自手工复制，不是 manifest 或来源文件变更。后续来源引用应从 manifest 读取并用文件 SHA-256 与 Git blob 交叉核对。

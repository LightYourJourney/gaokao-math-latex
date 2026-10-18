# 批次 phase2-b23 视觉审查诊断

- 当前结论：`VISUAL_FAILED`
- 批次闭环：未完成；本诊断不得作为 `closed` 或 `closed_with_blockers` 报告
- 试卷数：2
- 审查页数：53
- 失败检查数：2

## gk-1977-regular-shanghai-arts

- 标题：1977 年·上海卷·文科
- 项目目录：`1977_上海卷_文科`
- 构建状态：`compiled_pending_review`；attempt `321afeec-4d93-43c9-9793-50a071f39e2b`
- 复核状态：`passed`；时间 2026-10-18T23:37:09+08:00
- 试题版：2 页；PDF SHA-256 `1d98b7739e2d6e3dc11763e288034ac7b0c4b1b2d6f537142d46965f93a13e83`
- 解析版：9 页；PDF SHA-256 `0a2902009661b531881de4b223229e476b2d64f2947a506762712e732357b237`
- 简答版：3 页；PDF SHA-256 `e8e32b221d4ae677d2f80b7e0b51d43b708344a9e45390b75d871b66b505dfec`
- 印刷版：8 页；PDF SHA-256 `21171d6ff9c5000849487a8bceee48a2369c5d8e4135a5fff9a7fe93c68f1424`

## gk-1977-regular-shanghai-science

- 标题：1977 年·上海卷·理科
- 项目目录：`1977_上海卷_理科`
- 构建状态：`compiled_pending_review`；attempt `0c6feec3-9e12-41f8-b701-f8e2512a8d52`
- 复核状态：`failed`；时间 2026-10-18T23:37:09+08:00
- 试题版：3 页；PDF SHA-256 `eb6810610249a0774461d92f39ff866a5d3ab9133ec6355f0541d25c41c28a5f`
- 解析版：14 页；PDF SHA-256 `f3fecc50a012d2e64eefa3f432891aff1552532b2f90c8c352c48e4e9c8734eb`
- 简答版：4 页；PDF SHA-256 `2fb23067db387ac54a06d73653f7c487dad9e448ad76bdf046872be9ef210326`
- 印刷版：10 页；PDF SHA-256 `d4ee341e79fadd6aa816b1b60cb62f1e1340442d6168a36a35d91ab5a53d196d`

## 失败检查

- gk-1977-regular-shanghai-science｜解析版 第 9 页｜`figure_label`｜attempt `0c6feec3-9e12-41f8-b701-f8e2512a8d52`｜本轮主会话实际目视当前PDF的150dpi页图：Q5数轴的-4、-2、3、4标号挤在图形左侧，未与四个端点对应；空心圆存在但标签/端点关系不清。旧结论漏检，在新旧像素相同的情况下仍覆盖为失败。根因：规范解析用~~~包裹ASCII数轴，生成LaTeX未置入等宽保空格环境，数字行空格被折叠。需要只改该题为带坐标标签的TikZ矢量数轴，保持[-4,-2)∪(3,4]不变。
- gk-1977-regular-shanghai-science｜印刷版 第 6 页｜`figure_label`｜attempt `0c6feec3-9e12-41f8-b701-f8e2512a8d52`｜本轮主会话实际目视当前PDF的150dpi页图：Q5数轴的-4、-2、3、4标号挤在图形左侧，未与四个端点对应；空心圆存在但标签/端点关系不清。旧结论漏检，在新旧像素相同的情况下仍覆盖为失败。根因：规范解析用~~~包裹ASCII数轴，生成LaTeX未置入等宽保空格环境，数字行空格被折叠。需要只改该题为带坐标标签的TikZ矢量数轴，保持[-4,-2)∪(3,4]不变。

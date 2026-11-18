# 本地 OCR 工作流部署验收（2026-11-03）

本机 Apple M3 / 16 GB 已完成三引擎部署、权重下载、统一候选入口及真实来源接入验收。执行规范：[OCR_WORKFLOW.md](../docs/OCR_WORKFLOW.md)。固定资产：[模型与环境配置](../tools/ocr-local-models.json)、[逐文件模型指纹](../benchmarks/ocr-local-assets.json)、[同裁片试跑](../benchmarks/ocr-local-smoke.json)、[端到端回执](../benchmarks/ocr-local-acceptance.json)。这些是候选生成验收，不是准确率或试卷验收。

| 路径 | 运行资产 | 实际结果 |
| --- | --- | --- |
| Xiaomi 首选 | 原始 Xiaomi-OCR-0 固定 HF revision，Python 3.13.18 / Transformers 5.17.0 / Torch 2.14.0 / MPS | 真实公式裁片、原始扫描 PDF 第1页识别成功，页级候选绑定通过；整页最终 worker 全耗时175.87秒，含冷启动 |
| Paddle 交叉 | PaddleOCR-VL-1.6 与 PP-DocLayoutV3 固定 revision，Python 3.11.18 / PaddleOCR 3.7.0 / PaddlePaddle 3.2.1 / CPU | 同一裁片和同一扫描页分别识别成功；整页 worker 全耗时304.66秒，包含初始化，停止/截断原因未知 |
| MinerU 批处理 | MinerU 4.1.4 / Basic ONNX CPU / 固定13文件模型包 | 1977 新疆理科扫描 PDF 显式第2页生成候选；2006 福建理科 PDF 两页按原生文字路由，不重复 OCR；两任务均成功 |

权重内容合计4,687,646,107字节，不含环境和缓存。`doctor`、`deploy_local_ocr.py --verify-only` 均通过；实际重新执行三引擎重建入口也完成，依赖锁一致，权重内容相同所以复用下载。模型版本、Python 完整版本、全部固定依赖、worker 和输入指纹参与候选缓存身份。

真实扫描源来自 manifest 的固定上游 commit；1977 新疆理科 SHA 为 `d6b42603b7f2ed9a8557d9d93ef9e5f08ae147f3d349145473229fabb183cb4e`。首次同页交叉输出不一致，分别保留，不自动裁决。第二次交叉命中两个引擎缓存，`model_calls_this_run=0`；耗时字段明确标记为所存 worker 执行时间，不把历史推理时间误记为缓存调用的新推理成本。

源页人工检查确认 OCR 仍存在底数/指数/根号范围错误，尤其源页第1小题的外层底数和第4小题的六次根式；不能直接采用输出作为规范题面。Paddle 接口未暴露 finish reason，回执保留 unknown；本次仅人工核对该页包含四个小题及输出尾部，不声称通用截断检测已实现。Gold 仍待人工批准，没有 CER 或准确率。

验证：43 项 OCR 相关测试、4 项既有公式识别测试、3 项报告契约测试通过。针对新入口的13项测试覆盖缓存、篡改、来源、页路由、跨引擎一致仍待核、部分批处理失败、超时和 Ctrl-C 进程组清理、输入保护及 Python 漂移。完整报告测试启动后在全库事实收集阶段中断，未记为通过；六份正式报告另由 `report.py render --all` 完成单事务写入和回读校验。本轮未运行全语料测试、重编四版或更新已有试卷回执。

六份报告同步了此前 phase1-b76 已提交但尚未反映的福建文科收口：397卷、249批；既有42个无效/过期门禁与1个视觉失败均保留，ownership 从历史 `validated` 同步为已提交状态。并在生成模板和项目 README 中登记工作规范入口。

部署阶段的当时计划是接收2006福建理科固定来源；该卷随后已完成（当前 manifest 中 `gk-2006-regular-fujian-science` 为 `complete`，分支已有 finalize 提交 `4f24b156`），不再作为待办。当前下一项应按现行 manifest、`PROGRESS.md` 和上游来源核查重新选择。本报告保留为部署阶段记录，不代表长期语料库完成。

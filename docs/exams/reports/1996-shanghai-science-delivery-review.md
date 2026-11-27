# 1996上海理科phase4-b21交付阶段复核

## 验收边界

24题、150分，保留全部A1/B1、A2/B2选做分支。来源/数学/规范登记阶段已提交e16f759。此阶段完成四版构建和视觉校样；不裁定Q15 A1来源单解与通常无向距离两解之冲突。ISSUE-1136/1137均保留开放阻断，逐题U/unresolved，整卷blocked。

最终正式attempt：75a8a3fe-beda-4e63-bf17-3872c808876d；四版7/28/9/23页，共67页、536项视觉检查；finalize-batch返回FINALIZED，批次closed_with_blockers，revision4752。

## 三轮自审与独立终审

1. 来源与变更边界：复读实际MD/图稿diff、来源校对哈希及独立来源终审；Q8/Q17源条件正确，选做和计分未丢失，解析补充明确归属，固定源官方性未认证。
2. 数学与数据状态：复核24题独立数学结论、规范题/答案hash、provenance及issue；Q15例外未掩盖，两个阻断保持open，其余结论与独立数学记录一致。
3. 实际输出与回执：主代理实看试题7页和简答9页，独立复核解析28页与印刷23页；迭代修复图注碰撞和章节边界后，以新旧全部页面一对一比较及所有变化页实看验证最终版本。每版PDF SHA绑定当前build/review，生成源未手改派生物。

独立最终终审见`1996-shanghai-science-delivery-final-review.md`。真实逐页证据见main-visual-final、solution-visual-initial/final/accepted、print-visual-initial/accepted；每份标明对应attempt，旧attempt的通过不得当作新版本验收，最新accepted报告才对应最终回执。

## 验证记录

- 最后两图标签调整后来源专项8/8通过。
- 全量 `python3 -B -m unittest discover -s tests -q`：1757项，0失败，13跳过，用时1012.138秒，命令exit 0。最后图稿标签改动另以8项专项复验通过。
- 六个全量报告已以单事务刷新并回读校验，CSV已更新775行；最终回执校验OK，missing/stale/invalid/failed均为0，provenance和全部生成一致性检查通过。报告check当前命令待结束后补录。
- 清理器仅删除本卷24个非PDF编译中间文件，四份PDF保留。
- 四版正式构建errors/missing_characters/overfull/undefined_references均为空。
- 原PDF固定字节身份可复现，出版者/版次、官方参考答案身份仍未认证。无新增OCR或网络/付费API；模型Token与费用不可见。

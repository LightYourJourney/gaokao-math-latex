# 2007 上海理科、四川文科转录接续

状态：pending。尚未导入 manifest；禁止据候选题面认定完成。

## 固定来源
- `src-4aa615d46874256833ba863103cadbfe1ef4fd9a84f779e648264b31b5b6f129`：`普通高考/2007/2007上海理.pdf`；当前 paper_id=None。
- `src-9aca159335308217b48f6d305942d30328d9bb142e4b623c35058b7c489e3821`：`普通高考/2007/2007四川文.pdf`；当前 paper_id=None。

## 接续门禁

1. 接收 `.work/intake-2007-shanghai-science/` 与 `.work/intake-2007-sichuan-arts/` 的原页转录，主代理逐题核对。
2. 独立求解并交叉复算；源歧义保持 U，登记 issue，不借邻卷补题。
3. 为原页图形绘制 TikZ，登记 figure_files、题面引用与 provenance。
4. 主代理统一登记 source/paper/batch；不复用已占用批次号。
5. 生成共享 TeX 与四版入口，构建、逐页视觉审查、回执当前性验证、报告与 CSV 对账后才封账。

既有 2007 上海文科为另一独立卷，Q21(3) 有 ISSUE-1362；本次不得更改其阻塞结论。

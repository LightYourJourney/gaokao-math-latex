# phase1-b55：登记、规范源与正式题图集成复核

日期：2026-10-28。复核者：`review_2007_spring_source`。只读检查 canonical worktree `仓库根`；未编辑仓库、未改manifest或图稿。

## 当前发现

当前正式输入未发现尚未修复的题文、登记映射、漏题或题图语义问题。

复核期间发现并向主会话报告了一个真实编译问题：首轮 `questions.tex` 来源说明中的普通正文 `official_answer保持null` 含未转义下划线。四版日志均在该文件第6行报 `Missing $ inserted`。主会话随后把说明改为中文“官方答案字段保持空值”，重生成并正式构建。当前四版PDF及回执已属于修复后attempt `4325af60-e0a2-453c-b61e-cd1f9afa87d5`，首轮失败不再是当前未解决问题；本报告不把失败历史抹去，也不把旧日志误算为当前失败。

## 实际检查范围及绑定证据

- 阅读实际 `git diff`：新增phase1-b55及单卷、来源反向绑定、index条目、CSV及四条正式构建issue变动；阅读新增规范源、六个正式TikZ、provenance及四个入口。`git diff --check`返回0。
- source ID `src-f34e9ac131532163db0030e99318a02d0e1d74cd393e842c738bdba8a0fc4646` 与paper `gk-2007-spring-shanghai` 双向一致；canonical仅绑定固定字节，题面/答案来源、页范围和未认证身份边界未丢失。
- 当前规范题面除来源说明中上述中文替换外，与本复核者已核私有规范稿完全相同；21题题文本身未改。Q1–5页1、Q6页1–2、Q7–16页2、Q17页2–3、Q18–21页3，与provenance逐题映射一致。
- `questions.tex`及`answers.tex`的题号分别完整为1–21，各输入6个图文件。`answers_short.tex`含Q1–11、Q16–21，Q12–15在单独速查表，代号A/B/B/D完整；不是漏掉四道选择题。Q18–21答案子问与题面对应；Q20(3)第三边公式及适用符号条件未被简答提取丢失，Q21(3)只作答①。
- 四入口共用questions；解析版/印刷版共用answers；简答版共用answers_short；没有重复维护题目。
- manifest的6条`figure_files`、index图列表、题面6个链接、图表清单与正式文件一一对应；每条expected_occurrences=2，对应questions/answers各一次。Q19一个文件包含源图两幅，Q21使用原生表格，不列成图文件。
- 21条provenance题序连续，source SHA相同且匹配固定副本，全部为D级独立推导、conflict_status=none，三个角色分开。`provenance.py check-batch --batch phase1-b55`实际两次返回`OK：1 卷`（含修复后当前状态复查）。
- 当前build回执读取为`compiled_pending_review`；回执manifest_revision=5332，主会话构建完成事务后当前manifest revision5333、production_state=compiled。四版为7/25/9/19页。以SHA重新核对四个PDF，均匹配回执；dependency_tree与generation_input_tree中所有文件当前哈希匹配，没有发现变更输入后沿用旧PDF。

## 图形独立源检查

本复核者未撰写图稿。阅读全部六个正式TikZ，对照此前实际核过的固定PDF2–3题图；随后将当前正式试题版全部7页以125 dpi渲染至`/private/tmp/2007-integration-question-1.png`至`-7.png`并逐页实际查看。该试题版PDF SHA-256为`8559eeaf4d2277d2fdb24ce52d7bda5a01073b837eca4120d84630e892ddfff7`。本轮未把旧wrapper图当作正式版面证据。

- Q13：两直线无箭头，P1左向、P2右上，I/II/III/IV位置与源图相同；正式PDF第3页标签可辨，未见错误区域或遮挡。
- Q14：无刻度与方程标签，正域可见先降后升曲线、轴箭头和O完整；当前对数横参数采样保留靠近y轴的上升段，正式PDF第4页未见新增数学条件。
- Q16：E/F分别为上、下前边中点，A'F实线，EC及AD/DC/DD'虚线，其他框架关系与源图一致；正式第5页线型与全部顶点标签可读。
- Q18：半长轴2.7、半短轴1.9092、焦点横坐标±1.9092满足椭圆焦距关系至坐标舍入精度（a²−b²−c²≈−0.00008928），M=(1.9092,1.35)在椭圆上；其统一比例对应题面M=(√2,1)。l过右焦点，未加B/N或所求三角形；正式第5页M落在l与上半椭圆交点附近，标签可辨，没有把焦点画成任意非焦位置。
- Q19：单砖浅灰ABE、黑CFE、白AEFD顺序正确；四个旋转副本共享中心，E/F/G/H分别在中央四边形左/上/右/下，公共接点重合；外框、接缝、各块浅灰旋转方向保持源图关系。正式第6页两幅图及标签可辨；图未标出示意坐标数值，不能用示意比例替代题文的铺设约束。
- Q20：A30°、B240°、C300°在同圆，只画BA/BC和圆心点O；AB两端相差150°，确非直径。正式第6页O不在AB上，未增加AC、半径或45°角标。
- Q21：正式第7页原生6×6表的表头、预填1/q/q²/…/q^(n−1)和待填空格可读，与源表相符。

## 本复核未覆盖的门禁

1. 本轮只实际查看当前试题版全部7页；未逐页视觉检查解析版25页、简答版9页、印刷版19页，不能据本报告填满四版视觉回执。
2. `generate_projects --check`与`make_short_answers --check`在默认沙箱尝试时因为共享`.git/gaokao-latex.lock`写权限被拒绝，没有完成；未升级抢锁。主会话须顺序运行其正式确定性检查，并包括make_editions、solution_sources及manifest/CSV/report当前性验证。
3. 未运行本轮全测试套件；未执行finalize、最终receipt验证或Git提交。构建通过仍处于待视觉验收状态；后续主会话须根据实际结果关闭issue/刷新CSV、形成正式视觉证据并提交。
4. 本报告不认证印载答案为官方标准，不替代来源链核验，也不代表长期全集完成。

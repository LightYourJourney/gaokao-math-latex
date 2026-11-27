# 三角色建议的缺项与边界

不得直接导入。question-review 与 answer-solve 由同一实际代理完成，不可仅改名称冒充两个独立身份；provenance.py 要求三角色两两不同。

- 需要独立主体对正式题面逐题读图复核，填 question-review.result；本代理只转录与自查，保留 null。
- 所有正式题块/答案哈希留空，未读取并绑定最新正式源，不拿候选哈希冒充规范源哈希。
- answer-review 引用主体为主代理；Q1–18有明确一致确认，Q19有主代理独立记录。Q20需确认奇/偶峰形选择与各自和式；Q21(3)现存主代理记录不足，保留 null。
- 本目录 suggested JSON 不满足直接导入要求，未运行 import、未修改正式 provenance。
- source_ref 仅提供 source_id 建议；正式结构需主代理依schema核定，未声称此局部建议已通过完整校验。

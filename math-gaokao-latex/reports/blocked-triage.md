# blocked 卷逐条复核与分流（机械生成）

本文件由 `.work/gen_triage.py` 从 manifest、各卷 `receipts/build.json`、`receipts/review.json`、
`provenance.json`、`missing-issues.md` 与上游 PDF 磁盘存在性机械生成，不手写判据。

## 分类规则（互斥，按序判定）

1. **缺源**：`source_ids` 为空。
2. **保留 U**：`provenance.json` 中存在 `answer_evidence.grade == "U"` 的题（源文不足以唯一判定）。
3. **保留 U（源缺陷/歧义）**：无 U，但仍有 `status != resolved` 的 issue。
4. **可收口**：无 U、无未结 issue。

机制约束：`tools/provenance.py` 把任一题 `grade == "U"` 记为 `provenance_unknown`，
`tools/status.py` 据此派生 `eligible_blocked`；构建本身可成功（回执 `succeeded`），但派生状态落为 blocked、不予封账——含 U 的卷只能按「保留 U 并登记 ISSUE」交付。

## 与 objective 三分法的对应

| objective 要求 | 本表分类 | 含义 |
|---|---|---|
| 补源后完成 | 保留 U（源缺陷/歧义） | 固定源在盘但印面有缺字/歧义，需外部勘误或独立扫描页重证；修好后可走完 build→review→finalize |
| 保留 U 并登记 ISSUE | 保留 U | 源文不足以唯一判定，按 U 政策不写确定答案，逐题 ISSUE 已登记 |
| 确认 missing-source | 缺源 | `source_ids` 为空，无任何固定上游（2026 回忆版） |

## 口径对账（111 套从哪来）

目标里的 111 套 blocked 是立项时（2026-11-09）的口径注记，**无法从当前仓库机械复算**；本轮已封账 5 套（`gk-1986-regular-guangdong-arts`、
`gk-1987-regular-national-science`、`gk-2003-spring-beijing-science`、`gk-2020-regular-national-1-arts`、
`gk-2022-regular-national-b-arts`；封账提交分别为 dceb1fde1 / fc0740f8d / 51ba8346a / 7ea5e8efb），
另有 3 套原为 `compiled` 的已封账（`gk-2019-regular-national-1-{arts,science}`、`gk-2020-regular-national-1-science`，提交 51ba8346a）。
因此 111 = 本表 106 套 + 已封账 5 套。

## 计数

- 复核总数：**106** 套（`production_state != complete`）
- 可收口：**0** 套
- 保留 U：**71** 套
- 保留 U（源缺陷/歧义）：**34** 套
- 缺源：**1** 套

## 逐卷

| 年 | 试卷 | blocked_from | build | review | U 题号 | 未结 ISSUE | ISSUE 类型 | 上游 PDF 在盘 | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| 2025 | gk-2025-regular-national-1 | legacy_unverified | succeeded | passed | — | ISSUE-0048,ISSUE-0050,ISSUE-0056,ISSUE-0057,ISSUE-0058,ISSUE-0059 | source-mismatch,source-unavailable,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2026 | gk-2026-regular-national-1-recall | legacy_unverified | succeeded | passed | — | ISSUE-0001,ISSUE-0060,ISSUE-0061,ISSUE-0062,ISSUE-0064,ISSUE-0065,ISSUE-0066,ISSUE-0067,ISSUE-0068,ISSUE-0069 | answer-conflict,answer-missing,identity-ambiguous,source-mismatch,source-unavailable,transcription-ambiguous | — | 缺源 |
| 1977 | gk-1977-regular-inner-mongolia-arts | planned | succeeded | passed | — | ISSUE-0129,ISSUE-0130 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |
| 1977 | gk-1977-regular-jiangsu | planned | succeeded | passed | — | ISSUE-0131,ISSUE-0132 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1977 | gk-1977-regular-fujian-arts | planned | succeeded | passed | — | ISSUE-0133,ISSUE-0134,ISSUE-0135,ISSUE-0136 | answer-missing,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1977 | gk-1977-regular-fujian-science | planned | succeeded | passed | — | ISSUE-0137,ISSUE-0138,ISSUE-0139 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1986 | gk-1986-regular-guangdong-science | planned | succeeded | passed | — | ISSUE-0778,ISSUE-0797,ISSUE-1053,ISSUE-1054,ISSUE-1055,ISSUE-1056,ISSUE-1082,ISSUE-1083,ISSUE-1084 | answer-conflict,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1987 | gk-1987-regular-guangdong-science | planned | succeeded | passed | — | ISSUE-0781,ISSUE-0782,ISSUE-0783,ISSUE-0784,ISSUE-0791,ISSUE-0792 | answer-conflict,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1988 | gk-1988-regular-guangdong-science | planned | succeeded | passed | — | ISSUE-0785 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1997 | gk-1997-regular-national-science | complete | succeeded | passed | 23 | ISSUE-1072,ISSUE-1073 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2000 | gk-2000-regular-national-old-science | complete | succeeded | passed | 12 | ISSUE-1196 | answer-conflict | 是 | 保留 U |
| 2000 | gk-2000-regular-national-old-arts | complete | succeeded | passed | 12 | ISSUE-1195 | answer-conflict | 是 | 保留 U |
| 2000 | gk-2000-regular-national-new-science | complete | succeeded | passed | 12 | ISSUE-1197 | answer-conflict | 是 | 保留 U |
| 2005 | gk-2005-regular-national-1-science | planned | succeeded | passed | 4 | ISSUE-0834 | answer-missing | 是 | 保留 U |
| 2008 | gk-2008-regular-national-2-arts | planned | succeeded | passed | — | ISSUE-0839 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |
| 2009 | gk-2009-regular-national-1-arts | planned | succeeded | passed | — | ISSUE-0840 | source-mismatch | 是 | 保留 U（源缺陷/歧义） |
| 2013 | gk-2013-regular-national-1-arts | planned | succeeded | passed | — | ISSUE-0851,ISSUE-0852,ISSUE-0853,ISSUE-0879 | answer-conflict,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2013 | gk-2013-regular-national-1-science | planned | succeeded | passed | — | ISSUE-0854,ISSUE-0855,ISSUE-0856,ISSUE-0880 | answer-conflict,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2013 | gk-2013-regular-national-2-arts | planned | succeeded | passed | — | ISSUE-0857,ISSUE-0858,ISSUE-0859 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2013 | gk-2013-regular-national-2-science | planned | succeeded | passed | — | ISSUE-0860,ISSUE-0861,ISSUE-0862 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2014 | gk-2014-regular-national-1-arts | planned | succeeded | passed | — | ISSUE-0863,ISSUE-0864,ISSUE-0865 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2014 | gk-2014-regular-national-1-science | planned | succeeded | passed | — | ISSUE-0866,ISSUE-0867,ISSUE-0868 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2014 | gk-2014-regular-national-2-arts | planned | succeeded | passed | — | ISSUE-0869,ISSUE-0870,ISSUE-0871 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2014 | gk-2014-regular-national-2-science | planned | succeeded | passed | — | ISSUE-0872,ISSUE-0873,ISSUE-0874 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2021 | gk-2021-regular-national-b-arts | planned | succeeded | passed | — | ISSUE-0884 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2021 | gk-2021-regular-national-a-science | planned | succeeded | passed | — | ISSUE-0885,ISSUE-0895 | source-mismatch,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2021 | gk-2021-regular-national-b-science | planned | succeeded | passed | — | ISSUE-0886 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2022 | gk-2022-regular-national-b-science | planned | succeeded | passed | 11 | ISSUE-0898 | answer-missing | 是 | 保留 U |
| 2016 | gk-2016-regular-national-1-arts | planned | succeeded | passed | 23 | ISSUE-0932,ISSUE-0934 | answer-conflict,answer-missing | 是 | 保留 U |
| 2016 | gk-2016-regular-national-1-science | planned | succeeded | passed | 23 | ISSUE-0933,ISSUE-0935 | answer-conflict,answer-missing | 是 | 保留 U |
| 2016 | gk-2016-regular-national-2-science | planned | succeeded | passed | 18 | ISSUE-0931,ISSUE-0936 | answer-conflict,answer-missing | 是 | 保留 U |
| 2017 | gk-2017-regular-national-2-arts | planned | succeeded | passed | 17 | ISSUE-0952,ISSUE-0954 | answer-conflict,answer-missing | 是 | 保留 U |
| 2017 | gk-2017-regular-national-3-science | planned | succeeded | passed | 20 | ISSUE-0953,ISSUE-0955 | answer-conflict,answer-missing | 是 | 保留 U |
| 2017 | gk-2017-regular-tianjin-science | planned | succeeded | passed | 17,19 | ISSUE-0962,ISSUE-0963,ISSUE-0964,ISSUE-0965 | answer-conflict,answer-missing | 是 | 保留 U |
| 1985 | gk-1985-regular-guangdong-arts | planned | succeeded | passed | 11 | ISSUE-0966,ISSUE-0967,ISSUE-0968,ISSUE-0969,ISSUE-0970,ISSUE-0975 | answer-conflict,answer-missing,transcription-ambiguous | 是 | 保留 U |
| 1985 | gk-1985-regular-guangdong-science | planned | succeeded | passed | 2 | ISSUE-0971,ISSUE-0972,ISSUE-0973,ISSUE-0974 | answer-conflict,answer-missing,source-mismatch,transcription-ambiguous | 是 | 保留 U |
| 2015 | gk-2015-regular-national-1-arts | planned | succeeded | passed | 23 | ISSUE-0976 | answer-missing | 是 | 保留 U |
| 2015 | gk-2015-regular-national-1-science | planned | succeeded | passed | 23 | ISSUE-0977 | answer-missing | 是 | 保留 U |
| 2016 | gk-2016-regular-national-3-arts | planned | succeeded | passed | 12 | ISSUE-0999 | answer-missing | 是 | 保留 U |
| 2016 | gk-2016-regular-national-3-science | planned | succeeded | passed | 11 | ISSUE-1000 | answer-missing | 是 | 保留 U |
| 2016 | gk-2016-regular-beijing-arts | complete | succeeded | passed | 8 | ISSUE-1005 | answer-missing | 是 | 保留 U |
| 1989 | gk-1989-regular-guangdong-science | planned | succeeded | passed | — | ISSUE-1078 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |
| 1990 | gk-1990-regular-guangdong-science | planned | succeeded | passed | 12 | ISSUE-1070,ISSUE-1113,ISSUE-1114 | answer-conflict,answer-missing,figure-missing | 是 | 保留 U |
| 1994 | gk-1994-shanghai | planned | succeeded | passed | — | ISSUE-1071 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |
| 2015 | gk-2015-regular-hunan-science | planned | succeeded | passed | — | ISSUE-1106 | answer-convention-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1990 | gk-1990-regular-shanghai | planned | succeeded | passed | — | ISSUE-1111,ISSUE-1112 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1990 | gk-1990-regular-national-arts | planned | succeeded | passed | 20 | ISSUE-1124 | answer-convention-ambiguous | 是 | 保留 U |
| 2017 | gk-2017-spring-shanghai | planned | succeeded | passed | — | ISSUE-1125,ISSUE-1126,ISSUE-1127 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |
| 1990 | gk-1990-regular-national-science | planned | succeeded | passed | 20 | ISSUE-1131 | answer-convention-ambiguous | 是 | 保留 U |
| 1996 | gk-1996-regular-shanghai-science | planned | succeeded | passed | 15 | ISSUE-1136,ISSUE-1137 | answer-conflict,answer-convention-ambiguous | 是 | 保留 U |
| 1996 | gk-1996-regular-shanghai-arts | compiled | succeeded | passed | — | ISSUE-1142,ISSUE-1143 | answer-conflict,answer-convention-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1991 | gk-1991-regular-shanghai | compiled | succeeded | passed | — | ISSUE-1178 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |
| 1996 | gk-1996-regular-national-arts | planned | succeeded | passed | 7 | ISSUE-1180,ISSUE-1185 | answer-convention-ambiguous | 是 | 保留 U |
| 1996 | gk-1996-regular-national-science | planned | succeeded | passed | — | ISSUE-1181,ISSUE-1182,ISSUE-1183,ISSUE-1184 | answer-convention-ambiguous,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 1999 | gk-1999-regular-shanghai-arts | planned | succeeded | passed | — | ISSUE-1188,ISSUE-1189,ISSUE-1190 | answer-conflict,transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2000 | gk-2000-regular-guangdong-unspecified | planned | succeeded | passed | 12,19,22 | ISSUE-1198,ISSUE-1199,ISSUE-1200,ISSUE-1201,ISSUE-1202 | answer-conflict,answer-convention-ambiguous,answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2007 | gk-2007-regular-beijing-science | transcription_draft | succeeded | passed | — | ISSUE-1203 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2018 | gk-2018-spring-shanghai | planned | succeeded | passed | 17,18 | ISSUE-1204,ISSUE-1205 | answer-convention-ambiguous | 是 | 保留 U |
| 2004 | gk-2004-spring-anhui-arts | planned | succeeded | passed | 18 | ISSUE-1211 | answer-missing | 是 | 保留 U |
| 2006 | gk-2006-regular-anhui-arts | planned | succeeded | passed | 2,5 | ISSUE-1216,ISSUE-1217,ISSUE-1218 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-anhui-science | planned | succeeded | passed | 3 | ISSUE-1219 | answer-missing | 是 | 保留 U |
| 2019 | gk-2019-spring-shanghai | planned | succeeded | passed | 18 | ISSUE-1220,ISSUE-1221,ISSUE-1222,ISSUE-1223,ISSUE-1224,ISSUE-1225 | answer-conflict,answer-convention-ambiguous,transcription-ambiguous | 是 | 保留 U |
| 2020 | gk-2020-spring-shanghai | planned | succeeded | passed | 19 | ISSUE-1227,ISSUE-1228 | answer-conflict,answer-convention-ambiguous | 是 | 保留 U |
| 2003 | gk-2003-spring-beijing-arts | planned | succeeded | passed | — | ISSUE-1229 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2004 | gk-2004-spring-beijing-arts | planned | succeeded | passed | — | ISSUE-1238 | transcription-ambiguous | 是 | 保留 U（源缺陷/歧义） |
| 2009 | gk-2009-spring-shanghai | planned | succeeded | passed | 16 | ISSUE-1239,ISSUE-1240 | answer-conflict,answer-missing | 是 | 保留 U |
| 2015 | gk-2015-regular-shaanxi-science | planned | succeeded | passed | 11,16,19 | ISSUE-1245,ISSUE-1246,ISSUE-1247 | answer-convention-ambiguous,answer-missing | 是 | 保留 U |
| 2021 | gk-2021-spring-shanghai | planned | succeeded | passed | 9 | ISSUE-1251,ISSUE-1252 | answer-conflict,answer-convention-ambiguous | 是 | 保留 U |
| 1989 | gk-1989-regular-guangdong-arts | planned | succeeded | passed | 9,16,21 | ISSUE-1259,ISSUE-1260,ISSUE-1261,ISSUE-1262,ISSUE-1263 | answer-conflict,answer-convention-ambiguous,answer-missing | 是 | 保留 U |
| 2004 | gk-2004-spring-shanghai | planned | succeeded | passed | 14,18 | ISSUE-1264,ISSUE-1265,ISSUE-1266 | answer-conflict,answer-convention-ambiguous,answer-missing | 是 | 保留 U |
| 2018 | gk-2018-regular-beijing-arts | planned | succeeded | passed | 9 | ISSUE-1271,ISSUE-1272 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2018 | gk-2018-regular-beijing-science | planned | succeeded | passed | 16 | ISSUE-1273,ISSUE-1274 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2018 | gk-2018-regular-national-3-science | complete | succeeded | passed | 19 | ISSUE-1283,ISSUE-1284 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2008 | gk-2008-spring-shanghai | planned | succeeded | passed | 8 | ISSUE-1285,ISSUE-1286 | answer-conflict,answer-missing | 是 | 保留 U |
| 2006 | gk-2006-regular-tianjin-arts | planned | succeeded | passed | 14 | ISSUE-1287 | answer-convention-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-tianjin-science | planned | succeeded | passed | 2 | ISSUE-1288,ISSUE-1289 | answer-conflict,answer-missing | 是 | 保留 U |
| 2006 | gk-2006-regular-shandong-science | planned | succeeded | passed | 5,10 | ISSUE-1294,ISSUE-1295,ISSUE-1296,ISSUE-1297 | answer-conflict,answer-missing | 是 | 保留 U |
| 2006 | gk-2006-regular-guangdong | planned | succeeded | passed | 6,16,19,20 | ISSUE-1298,ISSUE-1299,ISSUE-1300,ISSUE-1301,ISSUE-1302,ISSUE-1305,ISSUE-1306,ISSUE-1307,ISSUE-1308 | answer-conflict,answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-jiangxi-arts | planned | succeeded | passed | 4,8 | ISSUE-1303,ISSUE-1304,ISSUE-1309,ISSUE-1310 | answer-conflict,answer-missing | 是 | 保留 U |
| 2006 | gk-2006-regular-hubei-science | planned | succeeded | passed | 17 | ISSUE-1319,ISSUE-1320 | answer-conflict,answer-missing | 是 | 保留 U |
| 1997 | gk-1997-regular-national-arts | planned | succeeded | passed | 23 | ISSUE-1321,ISSUE-1322 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 1999 | gk-1999-regular-guangdong | planned | succeeded | passed | 10,13,21 | ISSUE-1323,ISSUE-1324,ISSUE-1325,ISSUE-1326,ISSUE-1327,ISSUE-1328 | answer-missing,transcription-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-hubei-arts | planned | succeeded | passed | 12 | ISSUE-1333 | answer-missing | 是 | 保留 U |
| 2006 | gk-2006-regular-hunan-arts | planned | succeeded | passed | 17 | ISSUE-1338 | answer-convention-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-hunan-science | planned | succeeded | passed | 17 | ISSUE-1339 | answer-convention-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-liaoning-arts | planned | succeeded | passed | 21 | ISSUE-1340 | answer-convention-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-chongqing-science | planned | succeeded | passed | 20 | ISSUE-1341 | answer-convention-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-shaanxi-arts | planned | succeeded | passed | 3,15 | ISSUE-1342,ISSUE-1343 | answer-convention-ambiguous | 是 | 保留 U |
| 2006 | gk-2006-regular-shaanxi-science | planned | succeeded | passed | 16 | ISSUE-1344 | answer-convention-ambiguous | 是 | 保留 U |
| 2007 | gk-2007-regular-beijing-arts | planned | succeeded | passed | 18 | ISSUE-1355 | answer-convention-ambiguous | 是 | 保留 U |
| 2002 | gk-2002-regular-beijing-science | planned | succeeded | passed | 16 | ISSUE-1360,ISSUE-1361 | answer-missing | 是 | 保留 U |
| 2007 | gk-2007-regular-shanghai-arts | planned | succeeded | passed | 21 | ISSUE-1362 | answer-convention-ambiguous | 是 | 保留 U |
| 2000 | gk-2000-regular-shanghai-arts | planned | succeeded | passed | 21 | ISSUE-1363,ISSUE-1364 | answer-conflict,answer-convention-ambiguous | 是 | 保留 U |
| 2000 | gk-2000-regular-shanghai-science | planned | succeeded | passed | 12,21 | ISSUE-1369,ISSUE-1370,ISSUE-1371,ISSUE-1372 | answer-conflict,answer-convention-ambiguous,transcription-ambiguous | 是 | 保留 U |
| 2005 | gk-2005-regular-shanghai-arts | planned | succeeded | passed | 12,20 | ISSUE-1377,ISSUE-1379 | answer-convention-ambiguous | 是 | 保留 U |
| 2005 | gk-2005-regular-shanghai-science | planned | succeeded | passed | 11,20 | ISSUE-1380,ISSUE-1381 | answer-convention-ambiguous | 是 | 保留 U |
| 2004 | gk-2004-regular-shanghai-arts | planned | succeeded | passed | 17,19 | ISSUE-1384,ISSUE-1385 | answer-convention-ambiguous | 是 | 保留 U |
| 2004 | gk-2004-regular-shanghai-science | planned | succeeded | passed | 19,22 | ISSUE-1386,ISSUE-1387 | answer-convention-ambiguous | 是 | 保留 U |
| 2003 | gk-2003-regular-shanghai-arts | planned | succeeded | passed | 14 | ISSUE-1388 | answer-convention-ambiguous | 是 | 保留 U |
| 2003 | gk-2003-regular-shanghai-science | planned | succeeded | passed | 14 | ISSUE-1389 | answer-convention-ambiguous | 是 | 保留 U |
| 2003 | gk-2003-regular-beijing-arts | planned | succeeded | passed | 18 | ISSUE-1398,ISSUE-1399 | answer-convention-ambiguous,transcription-ambiguous | 是 | 保留 U |
| 2003 | gk-2003-regular-beijing-science | planned | succeeded | passed | 17 | ISSUE-1400,ISSUE-1401 | answer-convention-ambiguous,transcription-ambiguous | 是 | 保留 U |
| 2026 | gk-2026-regular-beijing-recall | planned | succeeded | passed | 18 | ISSUE-1408,ISSUE-1409,ISSUE-1410,ISSUE-1414,ISSUE-1415,ISSUE-1416 | answer-conflict,answer-convention-ambiguous,transcription-ambiguous | 是 | 保留 U |
| 2002 | gk-2002-regular-suyuyuegui | planned | succeeded | passed | 18 | ISSUE-1417 | answer-convention-ambiguous | 是 | 保留 U |
| 1998 | gk-1998-regular-national-arts | planned | succeeded | passed | 25 | ISSUE-1426,ISSUE-1427,ISSUE-1428 | answer-conflict,answer-convention-ambiguous | 是 | 保留 U |
| 2003 | gk-2003-regular-yuegui | planned | succeeded | passed | — | ISSUE-1429 | answer-conflict | 是 | 保留 U（源缺陷/歧义） |

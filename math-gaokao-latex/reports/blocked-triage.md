# Blocked 卷复核清单（逐卷解除条件）

- 生成方式：由 `source-manifest.json` 与 `missing-issues.md` 只读导出，不修改任何状态。
- 口径：`blocked_from` + 问题类型 + 解除条件；「本地源」列给出上游 PDF 是否存在、页数、前两页文字层字符数（0 表示扫描件）。
- 处置建议分四档：可重建/可独立推导（本轮可尝试解除）、需裁决证据、需更清晰源、缺源不可解除。

## 汇总

| 阻断来源 | 卷数 |
| --- | ---: |
| `transcription-ambiguous` | 112 |
| `compile-error` | 111 |
| `answer-conflict` | 63 |
| `answer-missing` | 53 |
| `answer-convention-ambiguous` | 52 |
| `layout-warning` | 40 |
| `figure-missing` | 8 |
| `source-mismatch` | 6 |
| `source-unavailable` | 4 |
| `identity-ambiguous` | 4 |

## 逐卷明细

| 卷 | 年份 | blocked_from | 问题类型 | 解除条件 | 本地源（存在/页数/文字层） |
| --- | ---: | --- | --- | --- | --- |
| `gk-1977-regular-fujian-arts` | 1977 | `planned` | answer-missing、transcription-ambiguous | 可独立推导（等级 D）；需更清晰源或权威勘误 | 普通高考/1977/1977福建文.pdf：有/1页/1138字 |
| `gk-1977-regular-fujian-science` | 1977 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/1977/1977福建理.pdf：有/1页/1504字 |
| `gk-1977-regular-inner-mongolia-arts` | 1977 | `planned` | answer-conflict | 需裁决证据 | 普通高考/1977/1977内蒙古文.pdf：有/4页/0字 |
| `gk-1977-regular-jiangsu` | 1977 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/1977/1977江苏.pdf：有/1页/1039字 |
| `gk-1985-regular-guangdong-arts` | 1985 | `planned` | answer-conflict、answer-missing、transcription-ambiguous | 需裁决证据；需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/1985/1985广东文.pdf：有/16页/0字 |
| `gk-1985-regular-guangdong-science` | 1985 | `planned` | answer-conflict、answer-missing、source-mismatch、transcription-ambiguous | 可独立推导（等级 D）；需裁决证据；需更清晰源或权威勘误；需核对源身份 | 普通高考/1985/1985广东理.pdf：有/11页/2067字 |
| `gk-1986-regular-guangdong-science` | 1986 | `planned` | answer-conflict、layout-warning、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/1986/1986广东理.pdf：有/11页/2301字 |
| `gk-1987-regular-guangdong-science` | 1987 | `planned` | answer-conflict、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/1987/1987广东理.pdf：有/10页/2289字 |
| `gk-1988-regular-guangdong-science` | 1988 | `planned` | compile-error、transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/1988/1988广东理.pdf：有/9页/2408字 |
| `gk-1989-regular-guangdong-arts` | 1989 | `planned` | answer-conflict、answer-convention-ambiguous、answer-missing | 需裁决证据；可独立推导（等级 D） | 普通高考/1989/1989广东文.pdf：有/9页/0字 |
| `gk-1989-regular-guangdong-science` | 1989 | `planned` | answer-conflict、layout-warning | 需裁决证据 | 普通高考/1989/1989广东理.pdf：有/9页/2257字 |
| `gk-1990-regular-guangdong-science` | 1990 | `planned` | answer-conflict、answer-missing、figure-missing | 可依原页重绘；需裁决证据；可独立推导（等级 D） | 普通高考/1990/1990广东理.pdf：有/8页/2198字 |
| `gk-1990-regular-national-arts` | 1990 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/1990/1990全国文.pdf：有/1页/2729字 |
| `gk-1990-regular-national-science` | 1990 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/1990/1990全国理.pdf：有/1页/2907字 |
| `gk-1990-regular-shanghai` | 1990 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/1990/1990上海.pdf：有/1页/2583字 |
| `gk-1991-regular-shanghai` | 1991 | `compiled` | answer-conflict | 需裁决证据 | 普通高考/1991/1991上海.pdf：有/7页/0字 |
| `gk-1994-shanghai` | 1994 | `planned` | answer-conflict、layout-warning | 需裁决证据 | 普通高考/1994/1994上海.pdf：有/5页/0字 |
| `gk-1996-regular-national-arts` | 1996 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/1996/1996全国文.pdf：有/1页/2833字 |
| `gk-1996-regular-national-science` | 1996 | `planned` | answer-convention-ambiguous、compile-error、transcription-ambiguous | 需裁决证据；需更清晰源或权威勘误 | 普通高考/1996/1996全国理.pdf：有/1页/3149字 |
| `gk-1996-regular-shanghai-arts` | 1996 | `compiled` | answer-conflict、answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/1996/1996上海文.pdf：有/8页/0字 |
| `gk-1996-regular-shanghai-science` | 1996 | `planned` | answer-conflict、answer-convention-ambiguous | 需裁决证据 | 普通高考/1996/1996上海理.pdf：有/9页/0字 |
| `gk-1997-regular-national-arts` | 1997 | `planned` | answer-missing、compile-error、transcription-ambiguous | 需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/1997/1997全国文.pdf：有/1页/3265字 |
| `gk-1997-regular-national-science` | 1997 | `complete` | answer-missing、compile-error、transcription-ambiguous | 需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/1997/1997全国理.pdf：有/1页/3440字 |
| `gk-1998-regular-national-arts` | 1998 | `planned` | answer-conflict、answer-convention-ambiguous | 需裁决证据 | 普通高考/1998/1998全国文.pdf：有/1页/3212字 |
| `gk-1999-regular-guangdong` | 1999 | `planned` | answer-missing、transcription-ambiguous | 需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/1999/1999广东.pdf：有/13页/0字 |
| `gk-1999-regular-shanghai-arts` | 1999 | `planned` | answer-conflict、compile-error、transcription-ambiguous | 需裁决证据；需更清晰源或权威勘误 | 普通高考/1999/1999上海文.pdf：有/10页/0字 |
| `gk-2000-regular-guangdong-unspecified` | 2000 | `planned` | answer-conflict、answer-convention-ambiguous、answer-missing、transcription-ambiguous | 需裁决证据；可独立推导（等级 D）；需更清晰源或权威勘误 | 普通高考/2000/2000广东.pdf：有/2页/3044字 |
| `gk-2000-regular-national-new-science` | 2000 | `complete` | answer-conflict | 需裁决证据 | 普通高考/2000/2000全国新课程理(江西,山西,天津).pdf：有/2页/3098字 |
| `gk-2000-regular-national-old-arts` | 2000 | `complete` | answer-conflict | 需裁决证据 | 普通高考/2000/2000全国旧课程文.pdf：有/2页/3125字 |
| `gk-2000-regular-national-old-science` | 2000 | `complete` | answer-conflict | 需裁决证据 | 普通高考/2000/2000全国旧课程理.pdf：有/2页/3215字 |
| `gk-2000-regular-shanghai-arts` | 2000 | `planned` | answer-conflict、answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2000/2000上海文.pdf：有/2页/3138字 |
| `gk-2000-regular-shanghai-science` | 2000 | `planned` | answer-conflict、answer-convention-ambiguous、compile-error、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2000/2000上海理.pdf：有/2页/3224字 |
| `gk-2002-regular-beijing-science` | 2002 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2002/2002北京理.pdf：有/2页/3844字 |
| `gk-2002-regular-suyuyuegui` | 2002 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2002/2002广东,河南,江苏,广西.pdf：有/2页/2638字 |
| `gk-2003-regular-beijing-arts` | 2003 | `planned` | answer-convention-ambiguous、compile-error、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2003/2003北京文.pdf：有/2页/2965字 |
| `gk-2003-regular-beijing-science` | 2003 | `planned` | answer-convention-ambiguous、compile-error、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2003/2003北京理.pdf：有/2页/3320字 |
| `gk-2003-regular-shanghai-arts` | 2003 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2003/2003上海文.pdf：有/2页/2867字 |
| `gk-2003-regular-shanghai-science` | 2003 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2003/2003上海理.pdf：有/2页/3035字 |
| `gk-2003-regular-yuegui` | 2003 | `planned` | answer-conflict | 需裁决证据 | 普通高考/2003/2003广东,广西.pdf：有/2页/2821字 |
| `gk-2003-spring-beijing-arts` | 2003 | `planned` | compile-error、transcription-ambiguous | 需更清晰源或权威勘误 | 春季高考/2003/2003春季北京文.pdf：有/2页/2754字 |
| `gk-2004-regular-shanghai-arts` | 2004 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2004/2004上海文.pdf：有/2页/3103字 |
| `gk-2004-regular-shanghai-science` | 2004 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2004/2004上海理.pdf：有/2页/3112字 |
| `gk-2004-spring-anhui-arts` | 2004 | `planned` | answer-missing、compile-error | 可独立推导（等级 D） | 春季高考/2004/2004春季安徽文.pdf：有/2页/2629字 |
| `gk-2004-spring-beijing-arts` | 2004 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 春季高考/2004/2004春季北京文.pdf：有/2页/2772字 |
| `gk-2004-spring-shanghai` | 2004 | `planned` | answer-conflict、answer-convention-ambiguous、answer-missing、compile-error | 需裁决证据；可独立推导（等级 D） | 春季高考/2004/2004春季上海.pdf：有/2页/2735字 |
| `gk-2005-regular-national-1-science` | 2005 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2005/2005全国1理(河北.河南,安徽,山西,海南).pdf：有/2页/3031字 |
| `gk-2005-regular-shanghai-arts` | 2005 | `planned` | answer-convention-ambiguous、transcription-ambiguous | 需裁决证据 | 普通高考/2005/2005上海文.pdf：有/2页/2934字 |
| `gk-2005-regular-shanghai-science` | 2005 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2005/2005上海理.pdf：有/2页/3217字 |
| `gk-2006-regular-anhui-arts` | 2006 | `planned` | answer-missing、transcription-ambiguous | 可独立推导（等级 D）；需更清晰源或权威勘误 | 普通高考/2006/2006安徽文.pdf：有/2页/2961字 |
| `gk-2006-regular-anhui-science` | 2006 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2006/2006安徽理.pdf：有/2页/3378字 |
| `gk-2006-regular-chongqing-science` | 2006 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2006/2006重庆理.pdf：有/2页/3091字 |
| `gk-2006-regular-guangdong` | 2006 | `planned` | answer-conflict、answer-missing、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据；可独立推导（等级 D） | 普通高考/2006/2006广东.pdf：有/2页/3223字 |
| `gk-2006-regular-hubei-arts` | 2006 | `planned` | answer-missing、compile-error | 可独立推导（等级 D） | 普通高考/2006/2006湖北文.pdf：有/2页/3104字 |
| `gk-2006-regular-hubei-science` | 2006 | `planned` | answer-conflict、answer-missing | 需裁决证据；可独立推导（等级 D） | 普通高考/2006/2006湖北理.pdf：有/2页/4145字 |
| `gk-2006-regular-hunan-arts` | 2006 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2006/2006湖南文.pdf：有/2页/2800字 |
| `gk-2006-regular-hunan-science` | 2006 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2006/2006湖南理.pdf：有/2页/3023字 |
| `gk-2006-regular-jiangxi-arts` | 2006 | `planned` | answer-conflict、answer-missing | 需裁决证据；可独立推导（等级 D） | 普通高考/2006/2006江西文.pdf：有/2页/3547字 |
| `gk-2006-regular-liaoning-arts` | 2006 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2006/2006辽宁文.pdf：有/2页/3138字 |
| `gk-2006-regular-shaanxi-arts` | 2006 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2006/2006陕西文.pdf：有/2页/2733字 |
| `gk-2006-regular-shaanxi-science` | 2006 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2006/2006陕西理.pdf：有/2页/2916字 |
| `gk-2006-regular-shandong-science` | 2006 | `planned` | answer-conflict、answer-missing | 需裁决证据；可独立推导（等级 D） | 普通高考/2006/2006山东理.pdf：有/2页/3367字 |
| `gk-2006-regular-tianjin-arts` | 2006 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2006/2006天津文.pdf：有/2页/3105字 |
| `gk-2006-regular-tianjin-science` | 2006 | `planned` | answer-conflict、answer-missing、compile-error | 需裁决证据；可独立推导（等级 D） | 普通高考/2006/2006天津理.pdf：有/2页/3425字 |
| `gk-2007-regular-beijing-arts` | 2007 | `planned` | answer-convention-ambiguous、compile-error | 需裁决证据 | 普通高考/2007/2007北京文.pdf：有/2页/2729字 |
| `gk-2007-regular-beijing-science` | 2007 | `transcription_draft` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2007/2007北京理.pdf：有/2页/3223字 |
| `gk-2007-regular-shanghai-arts` | 2007 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2007/2007上海文.pdf：有/2页/3311字 |
| `gk-2007-regular-sichuan-arts` | 2007 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2007/2007四川文.pdf：有/2页/3530字 |
| `gk-2007-regular-sichuan-science` | 2007 | `planned` | answer-conflict、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2007/2007四川理.pdf：有/2页/3528字 |
| `gk-2008-beijing-arts` | 2008 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2008/2008北京文.pdf：有/2页/2588字 |
| `gk-2008-regular-national-2-arts` | 2008 | `planned` | answer-conflict | 需裁决证据 | 普通高考/2008/2008大纲2文(黑龙江,吉林,贵州,新疆,内蒙古,青海,云南,西藏,甘肃).pdf：有/2页/2336字 |
| `gk-2008-spring-shanghai` | 2008 | `planned` | answer-conflict、answer-missing | 需裁决证据；可独立推导（等级 D） | 春季高考/2008/2008春季上海.pdf：有/4页/0字 |
| `gk-2009-beijing-arts` | 2009 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2009/2009北京文.pdf：有/2页/2594字 |
| `gk-2009-jiangsu` | 2009 | `planned` | answer-convention-ambiguous、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2009/2009江苏.pdf：有/2页/3791字 |
| `gk-2009-liaoning-arts` | 2009 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2009/2009辽宁文.pdf：有/2页/3575字 |
| `gk-2009-nceq-science` | 2009 | `complete` | answer-conflict、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2009/2009新课标理(海南,宁夏).pdf：有/2页/4545字 |
| `gk-2009-regular-national-1-arts` | 2009 | `planned` | source-mismatch | 需核对源身份 | 普通高考/2009/2009大纲1文(河北,河南,山西,广西).pdf：有/2页/2709字 |
| `gk-2009-shandong-arts` | 2009 | `planned` | answer-convention-ambiguous、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2009/2009山东文.pdf：有/2页/3487字 |
| `gk-2009-shandong-science` | 2009 | `complete` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2009/2009山东理.pdf：有/2页/3683字 |
| `gk-2009-shanghai-arts` | 2009 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2009/2009上海文.pdf：有/2页/3026字 |
| `gk-2009-shanghai-science` | 2009 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2009/2009上海理.pdf：有/2页/3202字 |
| `gk-2009-sichuan-science` | 2009 | `planned` | answer-convention-ambiguous、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2009/2009四川理.pdf：有/2页/3786字 |
| `gk-2009-spring-shanghai` | 2009 | `planned` | answer-conflict、answer-missing | 需裁决证据；可独立推导（等级 D） | 春季高考/2009/2009春季上海.pdf：有/9页/1719字 |
| `gk-2013-regular-national-1-arts` | 2013 | `planned` | answer-conflict、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2013/2013新课标1文(河南,河北,山西).pdf：有/2页/3349字 |
| `gk-2013-regular-national-1-science` | 2013 | `planned` | answer-conflict、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2013/2013新课标1理(河南,河北,山西).pdf：有/2页/3654字 |
| `gk-2013-regular-national-2-arts` | 2013 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2013/2013新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf：有/2页/3410字 |
| `gk-2013-regular-national-2-science` | 2013 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2013/2013新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf：有/2页/3658字 |
| `gk-2014-regular-national-1-arts` | 2014 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2014/2014新课标1文(河南,河北,山西).pdf：有/2页/3316字 |
| `gk-2014-regular-national-1-science` | 2014 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2014/2014新课标1理(河南,河北,山西).pdf：有/2页/3697字 |
| `gk-2014-regular-national-2-arts` | 2014 | `planned` | transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2014/2014新课标2文(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf：有/2页/3173字 |
| `gk-2014-regular-national-2-science` | 2014 | `planned` | compile-error、transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2014/2014新课标2理(贵州,甘肃,青海,西藏,黑龙江,吉林,海南,宁夏,内蒙古,新疆,云南).pdf：有/2页/3296字 |
| `gk-2015-regular-hunan-science` | 2015 | `planned` | answer-convention-ambiguous | 需裁决证据 | 普通高考/2015/2015湖南理.pdf：有/2页/3514字 |
| `gk-2015-regular-national-1-arts` | 2015 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2015/2015全国1文(河南,河北,山西,江西).pdf：有/2页/3920字 |
| `gk-2015-regular-national-1-science` | 2015 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2015/2015全国1理(河南,河北,山西,江西).pdf：有/2页/4087字 |
| `gk-2015-regular-shaanxi-science` | 2015 | `planned` | answer-convention-ambiguous、answer-missing | 需裁决证据；可独立推导（等级 D） | 普通高考/2015/2015陕西理.pdf：有/2页/3425字 |
| `gk-2016-regular-beijing-arts` | 2016 | `complete` | answer-missing、compile-error | 可独立推导（等级 D） | 普通高考/2016/2016北京文.pdf：有/2页/2677字 |
| `gk-2016-regular-national-1-arts` | 2016 | `planned` | answer-conflict、answer-missing、compile-error | 需裁决证据；可独立推导（等级 D） | 普通高考/2016/2016全国1文(河南,河北,山西,江西,湖北,湖南,广东,安徽,福建).pdf：有/2页/3642字 |
| `gk-2016-regular-national-1-science` | 2016 | `planned` | answer-conflict、answer-missing | 需裁决证据；可独立推导（等级 D） | 普通高考/2016/2016全国1理(河南,河北,山西,江西,湖北,湖南,广东,安徽,福建).pdf：有/2页/3659字 |
| `gk-2016-regular-national-2-science` | 2016 | `planned` | answer-conflict、answer-missing、compile-error | 需裁决证据；可独立推导（等级 D） | 普通高考/2016/2016全国2理(甘肃,青海,内蒙古,黑龙江,吉林,辽宁,海南,宁夏,新疆,西藏,陕西,重庆).pdf：有/2页/3756字 |
| `gk-2016-regular-national-3-arts` | 2016 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2016/2016全国3文(云南,广西,贵州).pdf：有/2页/3864字 |
| `gk-2016-regular-national-3-science` | 2016 | `planned` | answer-missing | 可独立推导（等级 D） | 普通高考/2016/2016全国3理(云南,广西,贵州).pdf：有/2页/3925字 |
| `gk-2017-regular-national-2-arts` | 2017 | `planned` | answer-conflict、answer-missing、compile-error、layout-warning | 需裁决证据；可独立推导（等级 D） | 普通高考/2017/2017全国2文(甘肃,青海,内蒙古,黑龙江,吉林,辽宁,海南,宁夏,新疆,陕西,重庆).pdf：有/2页/3156字 |
| `gk-2017-regular-national-3-science` | 2017 | `planned` | answer-conflict、answer-missing、layout-warning | 需裁决证据；可独立推导（等级 D） | 普通高考/2017/2017全国3理(云南,广西,贵州,四川,西藏).pdf：有/2页/3705字 |
| `gk-2017-regular-tianjin-science` | 2017 | `planned` | answer-conflict、answer-missing、layout-warning | 需裁决证据；可独立推导（等级 D） | 普通高考/2017/2017天津理.pdf：有/2页/3109字 |
| `gk-2017-spring-shanghai` | 2017 | `planned` | answer-conflict、figure-missing | 需裁决证据 | 春季高考/2017/2017春季上海.pdf：有/4页/1096字 |
| `gk-2018-regular-beijing-arts` | 2018 | `planned` | answer-missing、transcription-ambiguous | 需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/2018/2018北京文.pdf：有/2页/2760字 |
| `gk-2018-regular-beijing-science` | 2018 | `planned` | answer-missing、transcription-ambiguous | 需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/2018/2018北京理.pdf：有/2页/3267字 |
| `gk-2018-regular-national-3-science` | 2018 | `complete` | answer-missing、transcription-ambiguous | 需更清晰源或权威勘误；可独立推导（等级 D） | 普通高考/2018/2018全国3理(云南,广西,贵州,西藏,四川).pdf：有/2页/3210字 |
| `gk-2018-spring-shanghai` | 2018 | `planned` | answer-convention-ambiguous | 需裁决证据 | 春季高考/2018/2018春季上海.pdf：有/7页/1656字 |
| `gk-2019-spring-shanghai` | 2019 | `planned` | answer-conflict、answer-convention-ambiguous、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 春季高考/2019/2019春季上海.pdf：有/15页/1732字 |
| `gk-2020-spring-shanghai` | 2020 | `planned` | answer-conflict、answer-convention-ambiguous、figure-missing | 需裁决证据 | 春季高考/2020/2020春季上海.pdf：有/9页/2537字 |
| `gk-2021-regular-national-a-science` | 2021 | `planned` | compile-error、identity-ambiguous、source-mismatch、transcription-ambiguous | 需核对源身份；需更清晰源或权威勘误 | 普通高考/2021/2021全国甲理(云南,广西,贵州,西藏,四川).pdf：有/2页/3779字 |
| `gk-2021-regular-national-b-arts` | 2021 | `planned` | identity-ambiguous、transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2021/2021全国乙文(河南,山西,江西,安徽,陕西,甘肃,青海,内蒙古,黑龙江,吉林,.宁夏,新疆).pdf：有/2页/2807字 |
| `gk-2021-regular-national-b-science` | 2021 | `planned` | compile-error、identity-ambiguous、transcription-ambiguous | 需更清晰源或权威勘误 | 普通高考/2021/2021全国乙理(河南,山西,江西,安徽,陕西,甘肃,青海,内蒙古,黑龙江,吉林,.宁夏,新疆).pdf：有/2页/3220字 |
| `gk-2021-spring-shanghai` | 2021 | `planned` | answer-conflict、answer-convention-ambiguous、compile-error | 需裁决证据 | 春季高考/2021/2021春季上海.pdf：有/12页/2269字 |
| `gk-2022-regular-national-b-science` | 2022 | `planned` | answer-missing、compile-error | 可独立推导（等级 D） | 普通高考/2022/2022全国乙理(河南,山西,江西,安徽,陕西,甘肃,青海,内蒙古,黑龙江,吉林,.宁夏,新疆).pdf：有/2页/3740字 |
| `gk-2025-regular-national-1` | 2025 | `legacy_unverified` | answer-conflict、source-mismatch、source-unavailable、transcription-ambiguous | 需更清晰源或权威勘误；缺源，无法解除；需核对源身份 | 普通高考/2025/2025全国1(山东,广东,湖南,湖北,河北,江苏,福建,浙江,河南,江西,安徽).pdf：有/2页/3018字 |
| `gk-2026-regular-beijing-recall` | 2026 | `planned` | answer-conflict、answer-convention-ambiguous、figure-missing、transcription-ambiguous | 需更清晰源或权威勘误；需裁决证据 | 普通高考/2026/2026北京.pdf：有/5页/1769字 |
| `gk-2026-regular-national-1-recall` | 2026 | `legacy_unverified` | answer-conflict、answer-missing、identity-ambiguous、layout-warning、source-mismatch、source-unavailable、transcription-ambiguous | 需核对源身份；需裁决证据；需更清晰源或权威勘误；缺源，无法解除；可独立推导（等级 D） | 无绑定源 |


# 2004 上海文科普通卷：项目 TeX 生成、简答与四版入口

- 日期：2026-11-03。
- 批次/试卷：`phase4-b45` / `gk-2004-regular-shanghai-arts`。
- 固定候选来源：`src-cb0092e0533abc5b37a4e6843ba9688dfd851d0597a8dd9d44a827bd35e58290`，PDF SHA-256 `4ffc26d1ee893834e7cdf6a1b6ab3385fb97dd791d838d2630538461026ca7ad`。

## 项目生成结果

按 `phase4-b45` 逐卷生成：

| 文件 | SHA-256 |
|---|---|
| `2004_上海卷_文科/questions.tex` | `cb91772698d6e676495d8a278d23b2c6e8da2aa0addcaa376d481b1d95c6bf7e` |
| `2004_上海卷_文科/answers.tex` | `ebb71baa6f1e5963a28fd780a774a548f7c2965be64ba9e5be12d620a68829c0` |
| `2004_上海卷_文科/answers_short.tex` | `35e63d0b1ce16818691e191ccca20f8cd06f92e0b71f05d1a37c51fac0221b0b` |
| `2004_上海卷_文科/试题版.tex` | `b2bbb39d6fa22f2380b2ae8bdc2d9623217ab389bdc39517ac23b6c2e4891e6e` |
| `2004_上海卷_文科/解析版.tex` | `15e4ee96034a06fc7507f167f660c4f4e9c0000645244097d72203f1da6d571b` |
| `2004_上海卷_文科/简答版.tex` | `48c9606bcc6e17f7bf24985a52806bffe6a877ceede7bf3c5b98af59e116c5b2` |
| `2004_上海卷_文科/印刷版.tex` | `ba6cec724573d08cec5ff4dd5b5476895b2644ba60f32094e52e18037b15c6c4` |
| `index.json` | `f4dc3390826097746226f121e2ee06ae1e737bd48ead0ab4806c2b5f66fb5ab2` |

索引条目登记22题、Q5/Q18/Q20/Q21四张图和候选来源说明。生成的 `questions.tex`、`answers.tex` 均包含四张图的 `\input`；简答稿继续保留 Q17、Q19 的 U/PENDING。

## 验证与边界

- 串行执行 `generate_projects.py --check`、`make_short_answers.py --check`、`make_editions.py --check`；三项均与生成结果一致。
- `solution_sources.py check-batch`（22题）、`provenance.py check-batch`（22题）、`source_manifest.py validate`、`issues.py validate` 均通过。Q17 `ISSUE-1384` 与 Q19 `ISSUE-1385` 继续 open / blocks_completion。
- 本阶段生成项目 TeX、简答与四版入口；尚未编译正式 PDF、写 build/review receipt 或进行整卷逐页视觉验收。固定 PDF 无答案页，`official_answer=null`，paper 仍 blocked。本报告不表示来源认证、整卷完成或长期语料库完成。

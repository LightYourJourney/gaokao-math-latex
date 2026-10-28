# 2000 上海春季卷：固定来源内部登记、图稿归档与确定性生成

日期：2026-10-28

## 来源裁定

固定来源为 `src-2980f0ba5ee7c2ceec0fb5ea733769661ddc2a0012bd727f326ad93cd15a2bc0`，上游路径 `春季高考/2000/2000春季上海.pdf`，SHA-256 `f58f3b980fef4e1b74955a9e37bbbf751056d4d3c9a2215d77b489fd14e5a954`，Git blob `1d638c2ac9e78cd2bfcb9a31cd8ec31d9b7e5bb9`，9页、1,716,042字节。source manifest 原记录为 `ready` 且未绑定 paper。

2026-10-19 的来源核查未证明该扫描件与题头“高中数学能力型问题研究”的具体出版物相对应，因此出版社、版次、书目关系及扫描来源链仍未核。本次依照当前分支较新的登记口径（2003春季北京文科、2006安徽理科、2017上海普通卷、2019/2020春季卷）：区分“本库选用哪份固定输入”和“输入是否为官方原件/能否定位到出版物”。本库将题签自称“2000年上海市普通高等学校春季招生考试 / 数学试卷”的固定副本登记为内部 `canonical` 输入，以便继续处理本卷；该绑定不认证发布者、出版物、版次、复制来源链或官方身份。旧进度中“取得书目证据前不得绑定”的限制仅在“内部输入绑定”这一层由当前分支实践取代，外部来源认证状态不变。

固定 PDF 的第5–9页含“答案要点”和解答文字，但附录归属及官方性未核；答案与解析仍为项目独立推导，`official_answer=null`。

## 登记结果

- `source_manifest.py register-papers` dry-run 通过，随后以一个状态事务登记 `gk-2000-spring-shanghai` / `phase1-b51`，manifest revision `5289 → 5290`，事务 ID `dfbbf3c5-871c-46ff-8b0d-bc1a955520b6`。
- 纸卷22题，`track=none`；题面位于 PDF 第1–4页，附录位于第5–9页（印刷页182–190）。题型结构为填空1–12、选择13–16、解答17–22。paper 与 batch 均为 `planned`，无逐题阻断项；这只是工作流登记，不是四版验收或来源认证。
- 将三幅已完成的 TikZ 图稿从 `2000/figures/` 移入 `2000_春季上海卷/figures/`，题面与含解析稿链接改为项目内路径。三图 `expected_occurrences=2`，源文件 SHA-256 分别为：
  - Q8：`0ae4270069d998e83fcbfb37604d096772ce7d6a3a2d858c30c89152f6f0cfd8`
  - Q17：`d6fe979d1e66bedb9f4d14cc8babee94df078d3a3e557ee0a45ebd24ace0df24`
  - Q22：`afd04df54b5239ece5ea8af50cdc63d778ff187c4de272d706e7645bf2f45bc6`
- 题面、答案要点、解析正文均标注 `paper_id`；含解析稿由官方 `solution_sources.py extract-batch` 内容事务重生成。当前题面 SHA-256 `f5f1a09f57911cbac524ed21521c7b3a1735ea26a079609477b178c069eafe20`，答案要点 `cf490a2594407b7b1f007bde51e2d852f0ece6f6ac790ad33c46ecf4f4db8c6a`，解析正文 `bfab824c8c97912a4cdbe4b4905faea0d236141d8965b1984005f43368deeb0c`，含解析稿 `4894944a50178d3d63f81481ea097a2056249d7364915a9328ac5162051711a5`。

## 确定性生成与共享索引

- `generate_projects.py --paper gk-2000-spring-shanghai --write` 写入本卷 `questions.tex`、`answers.tex` 与全库 `index.json`；对应 `--check` 通过。登记新增全库索引项后，旧卷会暂时因共享索引不一致而被判生成物 stale；索引更新后 `phase1-b50` 与 `phase0-b01` 的 `review_receipts.py check-batch` 均返回 `FINALIZED`，没有改写旧批次 build/review 回执。
- 为 `make_short_answers.py` 的第三路核对，从同一份本库答案要点中重复列出 Q13–Q16（B、D、A、A）速查行；没有新增答案判断，也未引用扫描附录作为权威。随后简答稿写入并通过 `--check`。
- `make_editions.py --paper ... --write` 写入试题、解析、简答、印刷四版入口壳；对应 `--check` 通过。答案表结构调整后再次调用 `solution_sources.py extract-batch`，工具确认含解析稿已是当前派生结果、未开启写事务。

## 验证及阶段边界

`source_manifest.py validate`、`issues.py validate --file missing-issues.md`、`solution_sources.py check-batch`（22题）、本卷项目 TeX/简答稿/四版入口的三个 `--check`、`report.py render --all` / `check --all` 与 `manifest_csv.py --check` 均通过。全量门禁为 196 个 `FINALIZED`、3 个既有 `VISUAL_FAILED`、1 个 `INVALID_OR_STALE`（本卷尚无 build/review 回执）。未运行测试套件，未导入逐题 provenance，未正式构建 PDF 或逐页视觉审查。

登记规格首次把 `pages_q/pages_s` 写成逐页数组时，CLI 按 schema 要求“起止页对”拒绝；改为 `[1,4]` 与 `[5,9]` 后 dry-run 通过。问题校验器要求 `--file`；首次错误参数调用在解析阶段退出、未写入，随后正确调用通过。

下一阶段复用已完成的题面、答案、解析、三图及确定性派生物，导入逐题 provenance；随后正式构建及逐页审查。不得重做已完成的转录或把附录答案称为官方答案。该卷登记不代表1952–2026语料库完成。

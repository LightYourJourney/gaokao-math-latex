# PDF → LaTeX 流程审计与 Token 成本基线

审计日期：2026-10-13

范围：当前工作树中 `math-gaokao-latex/` 的来源管理、转录存储、LaTeX 生成、构建、复核和测试代码。未扫描构建目录、缓存内容、用户会话日志或外部服务账单。

## 结论

当前仓库已是一套成熟的来源可追溯、确定性 LaTeX 生成与质量门系统，不是尚待重建的 PDF/OCR 应用。manifest 有 775 个来源、272 套试卷、138 个批次；题目转录和答案/解析主要以分卷 Markdown 为规范源，模板和 Python 生成器产生四种 TeX 版本。XeLaTeX/latexmk 构建回执、输入依赖指纹、逐页视觉复核回执、来源 provenance 和状态投影均已有严格验证。

发现的主要缺口是**入库 PDF 到规范题目 Markdown 的前置识别过程并未被本仓库工具化**：没有集成 OCR、逐页文字层/扫描页分析、题目级结构化中间表示，也没有模型任务路由或题目识别缓存。因而无法从仓库代码证实 Claude Code / Codex 会话中发生过多少模型调用，也无法确认某一题是否重复发送给模型。

## 现状证据

| 环节 | 观察 | 证据/限制 |
|---|---|---|
| 语言与依赖 | 转换工具为 Python；工具与测试未发现项目级 requirements/pyproject 声明，处理逻辑主要使用 Python 标准库及外部命令。 | `tools/` 18 个 Python 文件；`tests/` 18 个 `test_*.py` 文件。 |
| PDF 来源 | 775 条来源记录固定上游路径、Git blob OID 与内容哈希；来源获取器按 blob OID 缓存并校验 PDF 文件与页数。缓存位于 Git 元数据目录而非题库版本目录。 | `tools/source_manifest.py`；本工作树对应的来源 PDF 缓存目录当前不存在/为空，因此缓存命中率未知，不能声称已有节省。 |
| PDF 提取/OCR | 构建和视觉复核使用 Poppler 的 `pdfinfo`、`pdftotext`、`pdftoppm`；没有调用这些工具来生成题目转录。项目代码/测试中未找到 Tesseract、PaddleOCR、MinerU、pix2tex、Mathpix 或模型 API 集成。 | 当前主机有 Poppler 26.10.0、Tesseract 5.5.3（语言 `chi_sim`、`eng`、`osd`、`snum`）；未发现 `paddleocr`、`mineru`、`pix2tex`、PyMuPDF、pdfplumber、pytesseract Python 模块。工具“已安装”不等于已评测。 |
| 题目与答案存储 | Markdown 是规范转录源；问题、解答和答案要点按卷组织；provenance 逐题关联来源页/证据哈希和问题项。没有统一的逐题 OCR JSON/坐标框数据层。 | `generate_projects.py`、`solution_sources.py`、`provenance.py`、`source-manifest.json`。 |
| LaTeX 生成 | 从规范 Markdown 和共享模板/宏确定性生成试题、解析、简答、印刷四版；可按卷检查/写入。数学图稿可用已登记的 TeX/TikZ 源。 | `tools/generate_projects.py`、`make_editions.py`、`templates/`、`common/`。 |
| 构建与缓存 | latexmk 驱动 XeLaTeX；回执绑定输入树、`.fls` 依赖闭包、工具链版本和二进制哈希。正式构建有意强制重建以确保正确性；不是利用 latexmk 旧产物跳过正式验证。PDF 来源有内容缓存，但没有 OCR/渲染/题目级持久缓存。 | `tools/build_projects.py`、`tests/test_build_projects.py`。忽略的 `.work` 可存批次复核数据，但不构成通用内容缓存。 |
| 自动质量门 | 来源清单、schema、provenance、生成器一致性、构建/警告、逐页 review 和报告均有 CLI 与测试；视觉 review 强制全页覆盖八项检查，候选页只用于提高重点复看效率。 | `tools/`、`tests/`；review 的文本/图像候选分数不声称理解数学内容。 |
| LLM/Token 成本 | 可检查的仓库源代码没有模型 API 调用、Token 计量或费用台账。Claude Code/Codex 的会话级用量与账单数据未提供给本审计。 | 输入/输出 Token、缓存 Token、模型/图像调用数、费用、Agent 推理耗时：**未知，未估算**。不得据此宣称现流程的 Token 基线或节省百分比。 |

本机已核验的构建/提取工具版本：Poppler `pdfinfo/pdftotext/pdftoppm 26.10.0`、XeTeX `TeX Live 2026`、latexmk `4.88`。这些版本是本次工作树主机观察值，不代表所有协作者环境。

## 主要瓶颈与优先级

1. **P0 — 缺少 PDF 页面级预分析。** 现有系统尚未判断原生文字层可用性、扫描/混合页面、空白/乱码或需局部 OCR 区域；故无法可靠决定哪些页根本不需要模型/OCR。
2. **P1 — OCR/转录过程缺少可复现缓存与成本日志。** 来源 PDF 可按 blob 缓存，但页文字、OCR、裁剪、结构化结果没有按输入哈希和引擎版本缓存；会话模型调用也没有项目内可核对记录。
3. **P2 — 缺少题目级结构化 IR。** Markdown 当前足以驱动排版和题目 provenance，但缺少机器可读的 bbox、逐题识别状态/置信度、答案来源类别等识别中间数据；应避免破坏现有规范源和既有溯源门禁。
4. **P3 — OCR 与数学语义评测不足。** 当前没有基于人工核对扫描样本的中文/数学符号/公式结构/题号/图形评测集。单看普通字符 CER 不足以替代数学忠实度。
5. **P4 — 质量与排版后段已有较强基础。** 四版生成、稳定构建、warning 复核、逐页回执和来源验证已存在；新流程应复用这些门禁，不重复造一套。

## 最小升级路径建议

### 首个增量（建议先做）

新增一个只依赖现有 Poppler CLI 的确定性 PDF 预分析命令：按 PDF SHA-256、分析器版本和 Poppler 版本缓存机器可读的页级记录；每页提取字符数、空白/替换字符信号并分类为“可提取文本 / 近空白待 OCR / 混合卷中待人工确认”。先用已提交的生成型 PDF 验证文本路径，用小型人工构造的图像型与混合型 PDF fixture 验证分类边界。该命令不猜数学内容、不覆盖源文件、不调用模型，也不把启发式分类伪装成 OCR 准确率。输入必须是显式 PDF 路径；缓存置于忽略的 `.work/pdf-analysis-cache/`，可关闭缓存并支持 JSON 输出。

该增量能将后续 OCR/模型工作从“整卷默认处理”转成“只看明确低文字层/混合页”，但**现阶段没有实测基线，不能量化节省了多少 Token 或费用**。真实扫描样本仍需在下一阶段选取并测量。

### 后续阶段

1. 用少量分层真实 PDF（文字型、扫描型、混合型，覆盖选择/填空/解答及复杂公式/图形）验证页分析，不重复处理已验收题目。
2. 建立人工核对的短评测集，再只对需要 OCR 的区域比较少量候选引擎；先比较本地方案，不预装 MinerU/PaddleOCR/pix2tex 全家桶，不将 pix2tex 当整页解析器，Mathpix 仅在本地识别确实不足且成本可核算时评估。
3. 引入版本化页/题缓存与题目级 IR，逐步将规范 Markdown 与机器数据的职责拆开；官方答案与模型推导/解析必须分字段、分状态。
4. 增加任务路由和用量接口：Level 0 确定性工具、Level 1 本地 OCR、Level 2 低成本局部修复、Level 3 疑难数学/视觉复核；仅在实际调用层拿到用量时记录 Token/费用，缺值明确为 unknown。
5. 选一张真实试卷端到端通过既有四版生成、数学/来源门禁、编译和逐页视觉验收后，再扩大批量范围。

## 本阶段边界

本报告是 Phase 0 的仓库证据审计，不是 OCR 引擎效果报告；未安装新依赖、未下载外部试卷、未修改任何试卷转录/题源/构建产物，也未改变既有门禁。首项代码增量已实现下面的页级确定性预分析；来源 manifest 接入、OCR 和题目 IR 属于后续阶段。

## 首项已实现改进及运行方法

新增 `math-gaokao-latex/tools/analyze_pdf.py`，依赖现有 Poppler 的 `pdfinfo`、`pdftotext` 和 `pdfimages`，无需新 Python 包。在仓库根目录运行：

```bash
python3 math-gaokao-latex/tools/analyze_pdf.py path/to/source.pdf
python3 math-gaokao-latex/tools/analyze_pdf.py path/to/source.pdf --page 2 --page 5
python3 math-gaokao-latex/tools/analyze_pdf.py path/to/source.pdf --page 2 --include-text --no-cache
python3 -m unittest discover -s math-gaokao-latex/tests -p test_analyze_pdf.py
```

默认 JSON 只输出页级指标，避免把全文重复带入 Agent 上下文；`--include-text` 可显式读取所选页文字。缓存保留提取文字用于下游复用，位于已忽略的 `.work/pdf-analysis-cache/`；`--cache-dir` 可设置位置，`--no-cache` 跳过读写。每页成功后以临时文件和原子替换保存 checkpoint；中断或后续页失败后，恢复时仅补提取缺页。缓存键绑定 PDF SHA-256、分析器版本、文字阈值、提取设置，以及工具的路径、版本和二进制哈希。输入变化、配置变化或版本变化自动使用新缓存；损坏缓存重算。外部命令超时/退出失败会返回非零退出码及 JSON 错误，不自动重试。

文字层分类含义：`text_candidate` 表示文字量达到阈值且未发现已定义的异常字符；`review` 表示字数偏少或含替换字符、私用区等信号；`needs_ocr_or_blank` 表示未提取到文字。卷级 `mixed_candidates` 仅反映文字层类别差异。Schema v2 另通过 `pdfimages -list` 提供页级 `content_evidence`（文字层、栅格对象、两者兼有或两者皆无）及图像对象数/最大像素尺寸；新增 `document_content_classification` 可区分文字+栅格页候选与真正出现“有文字页/仅栅格页”的混合候选。该字段仅依据所选页汇总，必须同时查看 `complete_document` 判断是否覆盖全卷。它们仍是结构证据：栅格对象可能是插图，不代表整页扫描；没有对象也不证明页面空白。所有页仍须复核。工具不判断图形语义、倾斜、模糊、裁切、题号或数学正确性，不能自动放行。

### 本次可复现验证

- 6 项定向测试通过：页分类、缓存补算、输入/配置/分析器版本失效、损坏缓存、失败后 checkpoint 恢复、关闭缓存、非法页码、命令超时/非零退出；含实际 Poppler 读取的三页 PDF（原生文字、图像、空白）。
- 真实题库的既有生成型 PDF `2024_新高考Ⅰ卷/build/试题版.pdf` 共 4 页、SHA-256 `21884234072f98643e277f79c594ff623e69594e251f9e6d4d8aa4d6b43d52d3`：首次 0 命中/4 页提取，耗时 0.358007 秒；第二次 4 命中/0 页提取，耗时 0.064376 秒，提取非空白字符总量均为 2479。这是单机单次观察，含工具指纹检查，不是通用性能结论。
- 该 PDF 的部分数学字体字符落入私用区，触发 `review`；这些标记是人工核对入口，不是自动断言原卷存在错误。`--page 1` 只输出该页且命中缓存，`complete_document=false`。
- 默认缓存路径经 `git check-ignore` 确认不会入库；`git diff --check` 通过。没有调用 OCR 或聊天模型；API Token/费用和原 Agent 流程基线仍未知，因此未计算 Token 或费用节省率。

本次真实样本是题库生成型 PDF，并非上游扫描原件；扫描页的识别准确性、真实混合卷判定与 OCR 引擎比较仍待后续用固定来源原件和人工标注样本验证。当前新增模块不在既有 LaTeX 生成器依赖链中，因此无需全库重建或刷新已验收回执。

## 后续实测：固定来源原件与基础 OCR 对照

已找到主检出既有的 `gaokaomath-src/` 原件目录，优先复用，无需网络取件。机器可读记录见 `exams/math-gaokao-latex/benchmarks/pdf-ocr-pilot.json`，以 source_id、上游 commit 和文件 SHA-256 定位，不依赖本机绝对路径。

| 固定来源 | 页数 | 文字层分析 | 首次耗时/再次耗时（秒） |
|---|---:|---|---|
| 1952 全国卷 | 2 | 两页有文字，仍需内容复核 | 0.323531 / 0.086591 |
| 1977 上海理科 | 1 | 有文字，6 个异常字符信号 | 0.198695 / 0.076389 |
| 2024 新高考Ⅰ卷 | 2 | 两页有文字，仍需内容复核 | 0.380024 / 0.130869 |
| 2025 全国Ⅰ卷 | 2 | 两页有文字，仍需内容复核 | 0.279642 / 0.141997 |
| 1977 新疆理科 | 4 | 四页无文字；pdfimages 列出逐页栅格图像，已视读第1页扫描内容 | 0.417531 / 0.109355 |

共 5 份原件、11 页，首次提取11页，再次全部命中缓存、未重提取；每份原件 SHA-256、Git blob OID、页数均核对来源清单。以上计时是一次运行观察，不是统计基准。该轮筛查时尚未找到真实混合型原件；后续2008混合卷实测见本报告末尾，合成fixture仍不替代真实试卷验证。

对 1977 新疆理科第1页开展了两个本地 Tesseract 5.5.3 对照：150dpi 整页（`chi_sim+eng`、PSM 3）耗时3.788693秒；150dpi局部单行（PSM 7）耗时0.882757秒。人工视读核对的题面方程是 `x^2-2x+\operatorname{Lg}a=0`，整页识别丢失上标/等号，局部识别还把系数2识为a、Lg识为Le；两次均标记数学忠实度失败。局部图像、bbox、来源页、输出片段和错误项已关联；图像保存在忽略目录，未入库。两种模式设置不同，不能把计时差异全部归因于裁剪。

这个小试验确认了需要保留扫描识别和公式复核入口；不能据一个题目给出 Tesseract 总体准确率，也不能据此宣称其他 OCR 引擎更优。人工视读仍由 Agent 完成，相关 Token 与成本不可获取；仅记录实际运行的2次本地OCR调用。下一阶段应扩充独立核对样本，再比较 MinerU/PaddleOCR 的数学表现；目前二者尚未安装或测试。

## 专业公式识别：PaddleOCR 隔离环境与局部推理

继续核查的 PyPI 元数据版本为 MinerU 4.0.12、PaddleOCR 3.7.0、PaddlePaddle 3.3.1。MinerU 官方4.x文档支持 Python >=3.10,<3.15，Apple Silicon 基础安装还会引入 Torch；当前主机为 arm64/16GB，默认 Python3.15不在其支持范围。Paddle 官方提供 Apple Silicon 的虚拟环境路线，PyPI 有Python3.11/arm64框架wheel。本次选择已有Python3.11，仅安装PaddleOCR、PaddleX的OCR依赖与框架，未安装MinerU或完整OCR集合。[MinerU安装文档](https://github.com/opendatalab/MinerU/blob/master/docs/en/quick_start/index.md)、[Paddle Apple Silicon指南](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/PaddleOCR-VL-Apple-Silicon.en.md)、[PaddleOCR 3.7.0](https://pypi.org/project/paddleocr/3.7.0/)。

新增 `tools/recognize_formula.py` 和可选的 `tools/requirements-ocr.txt`。主工具使用标准库，调用指定虚拟环境中的CPU worker；模型必须由调用者显式准备并指定目录。缓存绑定裁剪内容SHA、权重目录树SHA、分析器版本、Python/框架版本及CPU配置；成功结果保留 `recognized_unverified` / `needs-review`，失败和空结果不缓存。worker有超时，失败无自动重试。模型仅识别局部公式，不承担整卷文档解析。[官方 FormulaRecognition API](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/module_usage/formula_recognition.en.md)。

在仓库根目录设置环境后运行：

```bash
uv venv --python /opt/homebrew/bin/python3.11 math-gaokao-latex/.work/ocr-env
uv pip install --python math-gaokao-latex/.work/ocr-env/bin/python -r math-gaokao-latex/tools/requirements-ocr.txt
python3 math-gaokao-latex/tools/recognize_formula.py path/to/formula.png --engine-python math-gaokao-latex/.work/ocr-env/bin/python --model-dir path/to/PP-FormulaNet_plus-S_infer
```

模型来源为[官方PP-FormulaNet_plus-S归档](https://paddle-model-ecology.bj.bcebos.com/paddlex/official_inference_model/paddle3.0.0/PP-FormulaNet_plus-S_infer.tar)。本机模型/虚拟环境分别位于 `.work/ocr-models/` 与 `.work/ocr-env/`，依赖安装96个包；磁盘观察分别为516160 KiB（含模型归档及解压文件）和1031840 KiB。项目核心校验不依赖这个可选环境。

同一1977新疆理科方程的公式裁剪实际推理记录：

- 首次裁剪残留前一个汉字笔画，预测额外的 `\frac{1}{2}`，标为失败；记录保留以说明裁剪边界会影响数学条件。
- 人工检查后收紧边界至150dpi全页像素bbox `[441,875,179,40]`，得到 `x^{2}-2x+L g a=0`；上标、系数、等号与源图一致，Lg仍需算子格式规范化，因此仍为needs-review，未修改题源。
- 该次加载模型7.023472秒、推理0.530120秒、worker峰值RSS941670400字节；调用端总耗时14.865541秒（含进程启动/依赖导入/指纹计算）。同输入再次运行缓存命中，总耗时0.297260秒，实际OCR调用0。
- 新增4项测试通过，覆盖缓存/权重变化/损坏结果、空结果/失败不入缓存、超时/无效worker协议和环境错误；连同页分析6项，相关10项测试通过。

两次Paddle推理使pilot记录累计实际本地OCR调用达到4次。Tesseract使用整页/中文行，Paddle使用公式局部图，输入任务不同；上述结果不能直接用于引擎准确率排名。MinerU整页解析、PaddleOCR正文/布局识别、独立分层gold与完整端到端流程仍待验证。原来的Tesseract结果、失败裁剪与成功提取均已持久记录，不重复执行。

### 评分输入来源一致性门禁（2026-10-13）

复核发现评分器此前只校验 gold 对应的来源身份，没有将 OCR 运行记录的 `metadata` 和 gold 样本做关联检查；因此同一 `case_id` 下误附其他来源/页的识别输出有机会被评分。现要求每个运行记录携带来源元数据，并核对其中存在的 `source_id`、SHA-256、页码、像素 bbox 与任务类型；来源 SHA、页码和任务为必需字段，区域 gold 的 bbox 也必须出现在运行元数据中。已有2008整页pilot记录包含并通过 SHA、页码及 task 校验；gold 仍 pending，不产生分数。

验证：新增负例先按预期失败（错误源 SHA 未被拒绝），实现后 OCR scorer 测试7/7通过；对现存 `ocr-gold.json`、`ocr-runs.jsonl` 和 manifest 的 CLI 校验成功，仍为2个待审、0个计分。全套测试885项：869通过、13跳过、3失败，失败仍为两项既有摘要哈希漂移和52卷缓存派生状态不符；本次未修改历史基线。此增量不调用OCR或模型，不引入成本变化；它减少的是错配运行污染评测的风险，不能换算成Token节省。

### OCR Phase 1：来源绑定评分接口（初始样本仍待人工复核）

`tools/score_ocr.py` 对人工确认的OCR片段提供可复算评分，输入为：

```bash
python3 tools/score_ocr.py benchmarks/ocr-gold.json path/to/ocr-runs.jsonl \
  --manifest source-manifest.json
```

Gold记录用 `source_id + source_sha256 + source_page` 定位固定原件；区域样本可额外给定正数宽高的像素bbox、渲染DPI和 `review_status`。评分前核对source manifest中的来源ID、SHA和页数。`human_verified` 必须带非空参考文本、复核人及ISO日期；`pending_human_review` 可暂存候选区域但永不进入分数。运行记录每行提供case ID、引擎及版本、输出字符串。

正文按移除空白后的Unicode NFC字符计算CER；公式和结构字段在移除空白、NFC后逐字符精确匹配，任何正负号、运算符或符号差异都不会被折叠。报告保留逐项结果并按引擎/版本/任务给出微平均；它不是题目来源真实性、数学正确性或构建验收门禁。

初始 `benchmarks/ocr-gold.json` 含2个待复核候选：1977新疆理科局部公式，以及2008延考区文第5页的扫描版立体几何解答页。后者已由整页栅格对象和可视内容确认属于真实的原生文本页/扫描页混合PDF。**目前没有已批准的人工gold样本，因此该阶段不产生OCR准确率或引擎排名**；需完成独立人工核对并加入同任务OCR运行记录后，评分结果才有解释意义。

2008延考区文扫描页已用隔离环境中的PaddleOCR3.7.0/PaddlePaddle3.3.1做真实整页CPU试跑，显式选择`PP-OCRv5_mobile_det`与`PP-OCRv5_mobile_rec`，禁用方向、去畸变等额外子模型。官方API支持配置检测/识别模型路径；此次模型缓存在忽略目录`.work/ocr-model-cache/official_models/`，两模型磁盘合计约20.8MB。输入页图SHA绑定到`benchmarks/ocr-runs.jsonl`，144dpi、1190×1685；冷初始化23.905秒（含首次模型下载）+页推理19.614秒，热缓存进程初始化3.037秒+页推理20.598秒，峰值RSS为1,522,876,416 bytes（macOS `ru_maxrss`）。第二次OCR仅因首轮工具输出被截断而采集可持久化的完整文本，不代表独立重复样本；无聊天/API调用。

视觉抽查显示整页OCR能检出题文区域，但公式符号、下标、几何标签有明显错识、碎片化；全文未人工核对，所以不能报CER/准确率，也不能作为题目转录。冷启动新下载约20.8MB，热缓存后的页推理约20.6秒、进程级峰值RSS约1.42GiB；没有批量成本、缓存命中节省或Token/API账单数据。MinerU 4.x官方资料要求Python `>=3.10,<3.15`，支持模型档位与本地模型配置；本机未安装或评测，现阶段不为单页强行引入Torch运行时。

### OCR Phase 1：真实混合页结构证据增量（2026-10-13）

页分析器升级到 schema/version 2，在已有页文字抽取之外调用同一 Poppler 工具链的 `pdfimages -list`，解析每页可见图像/模板对象和辅助 mask 数量，并将结果与文字层一并缓存。缓存键包含版本及 `pdfimages` 路径、版本、二进制 SHA；首次扫描建立全卷图像页映射，后续只补未提取的页面文字，复用全部栅格元数据。保留原有 `classification` 与 `document_classification` 兼容字段，新增证据字段不会把视觉证据升级成内容验收。

固定来源 2008 延考区文原件（SHA-256 `fdfb4e9e88d4405f8a99380d6f2197f3269e061ef9b2c4f7ed7066a56a1e88c2`，7 页）实测：第 1、2、6、7 页仅检出文字层；第 3、4 页同时有文字层与栅格插图；第 5 页文字为 0 但有 1 个 1190×1685 栅格对象。全卷分类为 `mixed_text_and_raster_candidates`，不再把此具体页仅留在“扫描或空白”二选一里。顺序复跑，全页缓存命中 7/7、未重提取，0 OCR/模型调用。全卷首轮在第 5 页已有缓存时为 1 hit/6 misses，0.151179 秒；重复运行 0.035072 秒。这是单机单样本观察；另有两次并发单页烟测都报告 miss，属于缓存尚未写入时的竞争，不用于缓存节省量统计。

`test_analyze_pdf.py` 7/7、直接依赖分析器公共方法的 `test_recognize_formula.py` 4/4 通过，覆盖图像与辅助 mask 计数、真实 Poppler 三页文字/图像/空白 fixture、页缓存与损坏缓存恢复。完整套件 886 项运行293.345秒：870通过、13跳过、3失败。失败仍为已记录的历史漂移：task28/task29的来源摘要哈希不匹配，以及52卷缓存派生状态不符；未修改这些基线。真实扫描页的OCR准确率、页面倾斜/清晰度判断、人工gold和聊天模型Token/费用仍未知；不宣称OCR或Token节省率。

### OCR Phase 1：缓存式按页文字 OCR 闭环（2026-10-13）

新增 `tools/ocr_pdf.py`，串接既有 `analyze_pdf.py`、Poppler `pdftoppm` 与系统 Tesseract，不新增 Python 依赖。默认完整扫描页级文字/栅格证据，只自动识别“无原生文字且有栅格对象”的页；原生文字页、混合内容页、疑似空白页不自动重复 OCR。`--page` 可显式覆盖选择，但会在结果里标记 `explicit_page_override`。Tesseract 文档支持 `-l` 多语言、`--psm` 页面分割模式及 `--dpi` 输入分辨率；本机 5.5.3 的这些参数已在实际 1989 来源页调用中验证。[Tesseract CLI 文档](https://github.com/tesseract-ocr/tessdoc/blob/main/Command-Line-Usage.md)

两级缓存位于忽略目录 `.work/ocr-page-cache/`：渲染缓存键绑定 PDF SHA、页码、DPI、Poppler 可执行文件路径/版本/SHA，并用原子 sidecar 校验 PNG 内容哈希和尺寸；OCR 结果键绑定页面图像 SHA、Tesseract 可执行文件与版本、请求语言、对应 `.traineddata` 模型 SHA、PSM/DPI 和工具链配置。成功但空白的识别结果也会缓存为 `empty_unverified`；工具失败、超时不重试且不缓存。`--no-cache` 同时关闭页分析、渲染及识别缓存。默认 stdout 只给摘要，`--include-text` 才输出识别全文。

使用示例：

```bash
python3 math-gaokao-latex/tools/ocr_pdf.py path/to/source.pdf --source-id src-...
python3 math-gaokao-latex/tools/ocr_pdf.py path/to/source.pdf --page 3 --dpi 180 --include-text
python3 math-gaokao-latex/tools/ocr_pdf.py path/to/source.pdf --languages chi_sim+eng --psm 3 --no-cache
```

每页结果携带来源 SHA、source_id（若提供）、原页码、渲染 bbox/DPI、图像 SHA、引擎及模型指纹、缓存状态。所有结果固定为 `recognized_unverified` 或 `empty_unverified`、`needs-review`、`not_verified`；不修改规范题目、答案、解析或 OCR gold。`page_text` 目前是整页识别，不处理图文混合页的局部区域，也不支持独立图片输入；页面分析不能判断图像语义，因此显式页 OCR 仍可能重复识别页内已有文本。

真实烟测复用固定来源 1989 上海卷第1页（source_id `src-9085cdc9a4c6fd6f3c77225cda02cf3491cd5d8ebf2e1ae671df38a8156e10dd`，PDF SHA-256 `79f26e889678621a022423dc04afc47c799f0f3013056c61737ccc3ef84ff766`），180dpi 得到1253×1757图像。Tesseract 5.5.3 首次OCR约2.513秒，实际识别1次；同页复跑识别缓存命中，`ocr_calls=0`（此前单次观察0.100秒）；加入渲染 sidecar 校验后再跑，页面/识别两级缓存都命中，`ocr_calls=0`、0.112秒。只作为单页执行与恢复验证，不是通用性能基准。输出标题大致可读，但题目中的公式、上下标、字符有明显错误；按设计保留为待人工核对候选，**没有得到可报告的CER或数学准确率**。没有调用聊天/API模型，真实Token及费用仍未知。

新增 `test_ocr_pdf.py` 10项；与页分析、局部公式 OCR、评分器相关测试合计28项全部通过。代码审查发现并用回归测试修复了“校验和正确但 JSON cache body 类型错误”会逸出 `AttributeError` 的边界。全量测试未在本小阶段重跑；当前历史全量基线仍记录三项无关漂移（task28/task29来源摘要SHA、52卷派生缓存状态）。下一步先形成少量人工核对 gold，再在相同页/区域比较 OCR；MinerU、完整 Paddle 正文/布局识别、图片输入、题目级 IR/路由、三版 LaTeX 和八项端到端验收仍未完成。该增量只证明可选择性调用和续用本地缓存，不声称已经降低了可观测聊天 Token 或整体OCR成本。

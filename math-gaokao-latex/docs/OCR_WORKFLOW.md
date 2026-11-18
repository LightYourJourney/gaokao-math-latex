# 高考数学本地 OCR 与转录工作规范

版本：2026-11-03。适用于本项目全部新转录及 OCR 重跑。用户已授权本机部署与模型下载，并指定 Xiaomi-OCR-0 首选、PaddleOCR-VL-1.6 交叉验证、MinerU 批量 PDF。实施记录见 [部署计划](OCR_DEPLOYMENT_PLAN.md)；固定部署参数、版本及权重指纹以 `tools/ocr-local-models.json` 为准。

## 1. 开工与路径

1. 确认工作目录为本仓库根，分支为 `main`。
2. 查看 `git status --short --branch`、最近 Git 历史和 `PROGRESS.md`。先跳过已有题稿、OCR、图稿或有效回执已完成的步骤，不按旧会话推断进度。
3. 模型、环境、下载缓存、原始图像、PDF、原始识别输出和运行日志统一放在本项目忽略目录 `.work/ocr-local/`；规范题稿、指纹清单、工具和阶段报告按项目既有目录提交。
4. 不覆盖他人未提交修改。各完成阶段精确暂存、检查实际暂存 diff 与 `git diff --cached --check` 后提交，不推送。

下文命令均在 `math-gaokao-latex/` 执行。部署前需要 `uv`、Python 3.11/3.13 以及 Poppler（`pdfinfo`、`pdftotext`、`pdfimages`、`pdftoppm`）。依赖锁仅针对已验证的 macOS arm64 路径；迁移机器必须重做部署验收。

## 2. 模型与职责

| 引擎 | 任务 | 本机路径与边界 |
| --- | --- | --- |
| Xiaomi-OCR-0 | 扫描页或文字/公式裁片的首选识别 | 原始 Hugging Face 权重，Transformers + PyTorch，M3 的 MPS；显式失败不静默换引擎 |
| PaddleOCR-VL-1.6 | 复杂版面或公式的第二份候选 | 单独环境、独立输出；保留完成/截断可见性，不能把未暴露停止原因写成完整输出 |
| MinerU | 批量 PDF 的逐页结构解析 | Basic ONNX CPU；页码必须映射回原 PDF；文字层自动复用，不代表来源文字可靠 |

两个引擎一致只表示输出相同，不能代替原图校对。差异不得自动投票裁决。正文、公式、表格、题图是不同识别对象，图形占位符不能当矢量重绘成果。

## 3. 部署、下载与验收

按固定清单重建本机环境和模型：

```bash
python3 tools/deploy_local_ocr.py                    # 安装三个环境并下载固定权重
python3 tools/deploy_local_ocr.py --engine xiaomi    # 只重建一个引擎
python3 tools/deploy_local_ocr.py --verify-only      # 不下载，只核对已有资产
python3 tools/local_ocr.py doctor
```

1. 用固定版本依赖锁建立各引擎独立环境；下载固定 revision 的权重。模型指纹覆盖实际推理使用的全部文件（包括版面检测模型），不能只记录未使用的 HF 权重。
2. 下载完成后核验上游文件大小/哈希与本地模型树哈希；不得把 `.incomplete` 或只有配置的目录当已下载。模型或依赖变化须重新记录、测试和提交。
3. `python3 tools/local_ocr.py doctor` 校验本机目录、权重和关键依赖与部署锁一致。该命令证明运行资产一致性；真实推理成功必须另有执行记录。
4. 依次跑：固定源公式裁片、同图第二引擎、登记 PDF 显式选页、含多个 PDF 任务的批处理、再次调用的缓存复用。保存命令、输入/输出 SHA、模型指纹、耗时、停止/截断状态和原始日志。
5. 检查来源绑定、页码、输出非空、截断以及典型数学字符。无人工核定 gold 时不得发布 CER/准确率/模型排名。冒烟试跑成功只证明该输入和配置的可执行性。
6. 部署报告中逐项区分环境已安装、权重完整、推理成功、真实来源候选导出成功；四者均完成后才恢复下一批转录。

模型串行推理，统一入口提供进程锁。16 GB M3 不同时加载多个大模型；超时终止整组 worker 子进程，保留失败日志。已有用户服务不应被关闭或改配置。

## 4. 来源锁定与页路由

1. 从当前 manifest 的 `ready` 来源中选取尚未处理的试卷，检查年份/地区/文理/考试类型和卷内题签；重复或同卷来源先判关系。
2. 从固定上游 commit 获取只读 PDF，现场重算 SHA-256，并核对来源 ID、页数、大小和 Git blob。出版者、版次、官方身份缺证时继续标未核实。
3. 先用 `analyze_pdf.py` 检查每页文字层和图像证据；已有文字层保留为候选，不自动重跑 OCR。
4. 默认只对 `raster_only` 页启动 OCR。文字过短、编码可疑或混合页面进入人工路由清单；查看原图后用 `--page` 明确选页。空白页原图确认后记录跳过，不强行获得非空文本。
5. 渲染缓存绑定原 PDF SHA、原页码、DPI 和 Poppler 指纹。公式需裁片时另记原页坐标、裁片 SHA、缩放参数；不能混淆裁片像素坐标与原始渲染坐标。

## 5. 统一执行入口

```bash
# 单图/裁片：只生成独立的待核 run，不猜 source ID 或题号
python3 tools/local_ocr.py image .work/ocr-local/sources/formula.png \
  --task formula --output .work/ocr-local/formula-xiaomi.json

python3 tools/local_ocr.py image .work/ocr-local/sources/formula.png \
  --engine paddle --task formula --output .work/ocr-local/formula-paddle.json

# 已登记 PDF：source ID 必须换成该 PDF 的清单 ID；--page 可重复
python3 tools/local_ocr.py pdf /absolute/path/to/source.pdf \
  --source-id SOURCE_ID --page 1 --cross-check \
  --output .work/ocr-local/page-1-candidates.json

# 批处理：jobs.json 中的 pdf 路径相对 jobs 文件所在目录
python3 tools/local_ocr.py batch .work/ocr-local/jobs.json \
  --output .work/ocr-local/batch-candidates.json
```

批处理任务文件为非空数组：`[{"pdf":"sources/a.pdf","source_id":"...","pages":[1,3]}]`。省略 `pages` 时逐页自动路由。批处理默认 MinerU，逐份执行、保存已完成项；任何任务失败都使最终退出码非零。重启时复用已验证缓存，不能把部分成功当整批完成。

输出同时保留独立引擎 run 与 `ocr-page-candidate`，后者通过既有 `ocr_candidate_ir.convert_run` 校验来源。`question_id=null`，状态固定为 `recognized_unverified`、`needs-review`、`not_verified`。交叉验证结果分别保存，`exact_match` 只比较输出字节，不等同数学正确性。

## 6. 缓存和异常

- 缓存键包含输入内容、模型树指纹、revision、依赖、worker 代码、任务、页选择和输出预算。命中前检查内容哈希；缓存损坏重算，不能复用篡改内容。
- 输入 PDF、源图或模型变化会使旧结果不适用。正式候选导出前再次核对源 PDF，防止推理过程中源件变化。
- 缺模型、依赖漂移、来源不符、错误页码、空输出或已知截断直接失败。不静默切到另一模型，也不将错误 JSON 当正文。
- 若引擎 API 不暴露 token 停止原因，记录为未知并强制人工检查输出尾部与源页覆盖；不把此限制改写为“未截断”。
- 失败和超时保留 `.work/ocr-local/logs/` 原始记录。只修复运行配置，不据乱码或模型推测补写题面。可明确调整预算或裁片后再运行，参数变化另建缓存。

## 7. 从候选进入规范转录

1. 按原 PDF 逐页逐题检查题号、分值、选做分支、正文、选项、指数/下标、正负号、根号范围、括号、向量/集合符号与题图标注。逐题人工切分并修正候选，不直接批量覆盖规范题稿。
2. 三个事实源层分别为 `_试题.md`、`_答案要点.md`、`_解析正文.md`；`_含解析.md` 仅由规范源确定性生成。来源附答案、编者推导和官方答案身份分别记证，不混同。
3. 题目生成与独立复核分离。独立逐题核题、盲解和答案复核使用非重叠任务；按用户偏好使用 Luna/high 子代理。代理自述不作为验收证据，主代理核查实际文件、原图和差异。
4. 缺源或存疑保留 U/PENDING、来源冲突和 blocker；OCR 一致不能解除 blocker。来源无充分证据时 `official_answer=null`。
5. 题图按来源矢量重绘，登记 generator、`figure_files`、Markdown 映射与 provenance。将图稿 `.tex` 链接独立成段写入规范 `_试题.md` 后，先运行 `solution_sources.py extract-batch --write` 刷新确定性 `_含解析.md`，再运行 `source_manifest.py sync-figure-registry --write` 生成引用次数；该计数覆盖 `_试题.md` 与当前 `_含解析.md`，不得手工填写或在合并稿刷新前同步。题面、图稿或答案要点定稿后再导入 provenance，使现场题面/答案摘要与最终事实源一致。OCR 图片块不是已完成图稿。
6. 使用既有来源/答案/provenance 验证工具和事务登记；生成 TeX、简答、四版入口。正式构建与逐页视觉检查继续走既有回执流程，OCR 成功不替代构建或视觉验收。
7. 批次报告列出已完成内容、尚未核实内容、测试、当前回执和剩余步骤；每阶段提交，结尾核实工作区干净。单卷/一批完成不表示长期语料库完成。

来源与批次登记之后按实际阶段执行既有门禁（`BATCH_ID` / `PAPER_ID` 替换为当前登记值）：

```bash
python3 tools/source_manifest.py validate --manifest source-manifest.json
python3 tools/issues.py validate --file missing-issues.md
python3 tools/solution_sources.py check-batch --manifest source-manifest.json --batch BATCH_ID
python3 tools/provenance.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch BATCH_ID
python3 tools/build_projects.py validate-receipts --manifest source-manifest.json \
  --paper PAPER_ID --require-final --require-current-inputs
python3 tools/review_receipts.py check-batch --manifest source-manifest.json --issues missing-issues.md --batch BATCH_ID
python3 tools/report.py check --all --manifest source-manifest.json --issues missing-issues.md
```

构建/视觉回执未完成时不得以门禁失败为由伪造回执或提前宣称 complete。具体写入、构建、prepare/finalize 命令按对应工具 `--help` 和本批已有记录选择，不能盲目重建已完成批次。

## 8. 修改本规范

运行时遇到规范未覆盖情况时，先补充可复查的具体规则和失败证据，再按修订规则重跑对应验收。选型、路由默认值或候选状态变化必须更新本文件、工具与针对性回归；不在临时会话里另立相互冲突的默认流程。

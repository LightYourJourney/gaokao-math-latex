#!/bin/bash
# ============================================================
# compile.sh —— tools/build_projects.py 的薄包装（Bash 3.2 兼容）
#
# 这里**只做转交**：编译策略、退出码契约、回执与事务全在 Python 侧。
# 上一版在 Bash 里判编译成败（日志里找 "^!" + PDF 存在性），那套判据既漏掉 pdfinfo
# 失败与缺页，也没有任何可提交的证据——「编过了」只能靠人复述。
#
# 用法（原样透传给 Python）：
#   ./compile.sh build <项目目录> [版本]     smoke：只写 ignored build/ 与诊断
#   ./compile.sh build --formal --all …      正式构建：两阶段事务写回执与状态
#   ./compile.sh validate-receipts …         只读核对
#   ./compile.sh check-tools                 工具链指纹
# 退出码：0 通过 / 2 usage / 3 仅待视觉审查 / 4 invalid 或门禁未过 / 5 构建失败。
# ============================================================
# **绝不 cd**：调用方一律从仓库根传相对路径（`--manifest .../source-manifest.json`），
# 先 cd 到脚本目录会把它解析成 `.../...`。旧版 compile.sh 需要 cd
# 是因为它自己调 xelatex；现在编译发生在 Python 侧、cwd 由它按项目目录显式指定。
set -eu
exec python3 "$(dirname "$0")/tools/build_projects.py" "$@"

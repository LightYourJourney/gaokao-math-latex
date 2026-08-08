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
set -eu
cd "$(dirname "$0")"
exec python3 tools/build_projects.py "$@"

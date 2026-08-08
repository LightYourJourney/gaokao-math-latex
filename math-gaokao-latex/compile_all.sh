#!/bin/bash
# ============================================================
# compile_all.sh —— 全量正式构建的稳定入口（Bash 3.2 兼容）
#
# 固定 `build --formal --all`，其余参数原样透传（`--manifest` / `--issues` / `--json`）。
# 之所以单独存在：全量构建是主流程唯一会写 84 份 PDF 与 21 份回执的动作，把它钉成一个
# 无参数即正确的入口，比让每个调用方各自拼 `--formal --all` 更难拼错。
# 退出码沿用 compile.sh（0 通过 / 5 构建失败，诊断状态已保存）。
# ============================================================
# 同 compile.sh：不 cd，好让调用方传的相对 --manifest/--issues 按调用方 cwd 解析。
set -eu
exec "$(dirname "$0")/compile.sh" build --formal --all "$@"

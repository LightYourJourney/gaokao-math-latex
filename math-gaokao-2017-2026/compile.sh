#!/usr/bin/env bash
# 一键编译：xelatex 两遍（第一遍生成目录/交叉引用，第二遍回填）
# 用法：./compile.sh          正常两遍编译
#       ./compile.sh quick    只编译一遍（迭代排错用）
set -u
cd "$(dirname "$0")"

run() {
  xelatex -interaction=nonstopmode -file-line-error main.tex >/dev/null
  return $?
}

echo "== pass 1 =="
run
if grep -qE '^!|^./.*:[0-9]+: ' main.log; then
  echo "!! 编译有错误，摘录："
  grep -E '^!|^./.*:[0-9]+: ' main.log | head -20
  exit 1
fi

if [ "${1:-}" != "quick" ]; then
  echo "== pass 2 =="
  run
fi

echo "== 检查警告 =="
grep -E 'Overfull \\hbox \([0-9]{2,}' main.log | head -10 || true
echo "OK: $(grep -c 'Overfull' main.log 2>/dev/null || echo 0) 处 overfull；输出 main.pdf（$(pdfinfo main.pdf 2>/dev/null | awk '/Pages/{print $2}') 页）"

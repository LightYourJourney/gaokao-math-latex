#!/bin/bash
# ============================================================
# compile.sh —— 编译拆分版试卷项目
# 用法：
#   ./compile.sh                    全部 14 套 × 4 版本
#   ./compile.sh <试卷目录名>       该套的 4 个版本
#   ./compile.sh <试卷目录名> <版本名>   单个（如 ./compile.sh 2017_全国Ⅰ卷_理科 解析版）
# 每个目标 xelatex 跑两遍（解析头的"题目见第 X 页"回链需要第二遍）。
# 退出码：任一目标编译失败则非零。
# ============================================================
set -u
cd "$(dirname "$0")"

EDITIONS=(试题版 解析版 简答版 印刷版)
FAIL=0

build_one() {
    local dir="$1" ed="$2"
    ( cd "$dir" || exit 1
      for pass in 1 2; do
          xelatex -interaction=nonstopmode "${ed}.tex" > /dev/null 2>&1
      done
      # 以 log 中的 Error 与 PDF 存在性双判
      if [[ ! -f "${ed}.pdf" ]] || grep -q "^!" "${ed}.log"; then
          exit 1
      fi )
    if [[ $? -ne 0 ]]; then
        echo "✗ ${dir}/${ed}"
        FAIL=1
    else
        local pages
        pages=$(grep -oE "Output written.*\(([0-9]+) page" "${dir}/${ed}.log" | grep -oE "[0-9]+" | tail -1)
        echo "✓ ${dir}/${ed}  ${pages} 页"
    fi
}

if [[ $# -ge 2 ]]; then
    build_one "$1" "$2"
elif [[ $# -eq 1 ]]; then
    for ed in "${EDITIONS[@]}"; do build_one "$1" "$ed"; done
else
    for dir in [0-9]*/; do
        dir="${dir%/}"
        for ed in "${EDITIONS[@]}"; do build_one "$dir" "$ed"; done
    done
fi
exit $FAIL

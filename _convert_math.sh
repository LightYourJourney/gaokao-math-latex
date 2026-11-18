#!/bin/bash
# 把 <年份>/<年份>_数学真题_*.md 批量转换为 PDF 与 Word
# 用法：bash _convert_math.sh [年份]   不给年份则转换全部
#
# 本脚本处理手工转写的数学真题 Markdown。
set -uo pipefail
cd "$(dirname "$0")" || exit 1
ROOT="$(pwd)"
YEAR="${1:-}"

FONT="Songti SC"; SANS="PingFang SC"; MONO="Menlo"

convert_one() {
  local md="$1" dir base tmp
  dir="$(dirname "$md")"; base="$(basename "$md" .md)"
  tmp="$(mktemp /tmp/mathconv.XXXXXX.md)"
  # 剥掉在 PDF/Word 中显示为方框的 emoji，其余内容原样保留
  LC_ALL=C sed -E 's/⚠️|⚠|✓|✗|📘//g' "$md" > "$tmp"

  pandoc "$tmp" -o "$dir/$base.pdf" --pdf-engine=xelatex \
    --resource-path="$dir:$dir/images" \
    -V CJKmainfont="$FONT" -V CJKsansfont="$SANS" -V CJKmonofont="$MONO" \
    -V mainfont="$FONT" -V geometry:margin=2.2cm -V linkcolor=blue \
    --toc --toc-depth=2 2>/dev/null \
    && echo "  PDF  ok  $base.pdf" || echo "  PDF  FAIL $base"

  pandoc "$tmp" -o "$dir/$base.docx" --resource-path="$dir:$dir/images" \
    --toc --toc-depth=2 2>/dev/null \
    && echo "  DOCX ok  $base.docx" || echo "  DOCX FAIL $base"
  rm -f "$tmp"
}

if [ -n "$YEAR" ]; then dirs="$ROOT/$YEAR"; else dirs=$(find "$ROOT" -maxdepth 1 -type d -name "20*" | sort); fi

for d in $dirs; do
  [ -d "$d" ] || continue
  # 只转换对外三件套。`_解析正文.md` 是内部唯一规范源（详细推导），由
  # tools/solution_sources.py 生成与消费，不面向读者，显式排除以免多出一份 PDF/Word。
  found=$(find "$d" -maxdepth 1 \
    \( -name "*_数学真题*_试题.md" \
    -o -name "*_数学真题*_答案要点.md" \
    -o -name "*_数学真题*_含解析.md" \) \
    ! -name "*_解析正文.md" | sort)
  [ -z "$found" ] && continue
  echo "== $(basename "$d") =="
  echo "$found" | while read -r f; do convert_one "$f"; done
done
echo "完成。"

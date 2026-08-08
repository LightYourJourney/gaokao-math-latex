#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""split_project.py —— 只读兼容 CLI，已降级为 generate_projects.py 的一层壳。

历史上它从合并书 `papers/`、`answers/` 拆出各卷 `questions.tex`/`answers.tex`，
并往项目 `figures/` 复制图。阶段 0 把生成链改成来源总账驱动之后：

- 唯一写入口是 `generate_projects.py`（先全批校验、再一个 `content` 事务落盘）；
- 项目 `figures/` **只读**，不再从合并书复制副本；
- 本文件**不得再拥有独立写实现**——两处写实现意味着两套切分边界，而边界一旦分叉，
  谁也说不清在库的 TeX 是哪一套规则产出的。

保留它只为兼容既有调用习惯：`split_project.py (--all|--paper) --check`。
`--check` 是必选项，因为这里根本没有写模式可选。
"""
import argparse
import sys
from pathlib import Path

from generate_projects import DEFAULT_MANIFEST
from generate_projects import main as generate_main


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="只读核对各卷共享 LaTeX 与 index.json（写入请用 generate_projects.py）"
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--all", action="store_true", help="全部试卷")
    selector.add_argument("--paper", metavar="PAPER_ID", help="按 manifest paper_id")
    # 只读入口没有第二种模式：必须显式写出 --check，免得有人以为默认会写。
    parser.add_argument("--check", action="store_true", required=True, help="只读比对")
    return parser


def main(argv=None, figure_map=None, index_metadata=None) -> int:
    """退出码与 generate_projects.py --check 一致：0 全过、1 有差异、2 用法错。"""
    arguments = _parser().parse_args(argv)
    forwarded = ["--manifest", str(Path(arguments.manifest)), "--check"]
    forwarded += ["--all"] if arguments.all else ["--paper", arguments.paper]
    return generate_main(forwarded, figure_map=figure_map, index_metadata=index_metadata)


if __name__ == "__main__":
    sys.exit(main())

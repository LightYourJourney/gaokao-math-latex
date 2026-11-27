#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""五件工具链的可编程替身（含 latexmk 编排 XeLaTeX）。

**夹具的形状决定你能发现什么**：真实 XeLaTeX 只会给出「这台机器此刻的那一种」行为，
于是所有分支——第二遍才失败、PDF 没写出来、pdfinfo 挂掉、log 里带 Missing character、
`.fls` 两遍内容不同、版本串认不出来——统统测不到。这个替身把这些形态全部变成可点选项。

用法：测试写一份 JSON spec，再在临时 bin 目录里放五个 shim（见 `write_shims()`），
把该目录传给 `resolve_toolchain(search_path=...)`。spec 的形状：

```json
{
  "xelatex": {
    "version_output": "XeTeX 3.14 (TeX Live 2026)\\n",
    "version_exit": 0,
    "passes": [{"exit_code": 0}, {"exit_code": 1}],
    "log": "…",  "log_by_pass": ["第一遍", "第二遍"],
    "fls": ["INPUT questions.tex"], "fls_by_pass": [[...], [...]],
    "write_pdf": true, "pdf_content": "%PDF-1.4 …"
  },
  "pdfinfo":   {"version_output": "pdfinfo version 26.08.0", "exit_code": 0, "pages": 3},
  "pdftotext": {"version_output": "pdftotext version 26.08.0"},
  "pdftoppm":  {"version_output": "pdftoppm version 26.08.0"}
}
```

`passes/log_by_pass/fls_by_pass` 按**每个目标各自的调用序**取值（第 1/2 遍），序号越界时
沿用最后一项。调用计数存在 spec 同目录的 `<spec>.state.json`，按 `工具:工作目录:job` 计。
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

TOOLS = ("xelatex", "latexmk", "pdfinfo", "pdftotext", "pdftoppm")
SPEC_ENV = "FAKE_TOOLCHAIN_SPEC"


# ---------------------------------------------------------------- 夹具搭建


def write_shims(bin_dir, spec_path, tools=TOOLS, marker=""):
    """在 `bin_dir` 放四个可执行 shim，指向本脚本。

    `marker` 会写进 shim 正文——测试改一下它就能模拟「同名同版本但二进制指纹变了」。
    """
    bin_dir = Path(bin_dir)
    bin_dir.mkdir(parents=True, exist_ok=True)
    for name in tools:
        script = bin_dir / name
        script.write_text(
            "#!/bin/sh\n"
            "# fake %s %s\n"
            'FAKE_TOOLCHAIN_SPEC="%s" exec "%s" "%s" --fake-tool %s "$@"\n'
            % (name, marker, spec_path, sys.executable, Path(__file__).resolve(), name),
            encoding="utf-8",
        )
        script.chmod(0o755)
    return bin_dir


DEFAULT_SPEC = {
    "xelatex": {
        "version_output": "XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026)\n",
        "version_exit": 0,
        "passes": [{"exit_code": 0}, {"exit_code": 0}],
        "log": "This is XeTeX\nOutput written on build/x.pdf (2 pages).\n",
        # 真实的两遍 `-recorder` 一定有 INPUT；默认给一条，好让「依赖闭包为空」保持
        # 为一种需要显式点选的异常形态，而不是所有用例的隐性常态。
        "fls": ["INPUT questions.tex"],
        "write_pdf": True,
        "pdf_content": "%PDF-1.4 fake\n",
    },
    "latexmk": {
        "version_output": "Latexmk, John Collins, 9 March 2026. Version 4.88\n",
        "version_exit": 0,
        "xelatex_runs": 2,
        "exit_code": None,
    },
    "pdfinfo": {
        "version_output": "pdfinfo version 26.08.0\n",
        "exit_code": 0,
        "pages": 2,
    },
    "pdftotext": {"version_output": "pdftotext version 26.08.0\n"},
    "pdftoppm": {"version_output": "pdftoppm version 26.08.0\n"},
}


def write_spec(path, overrides=None):
    """写一份 spec：默认全绿，`overrides` 按工具逐字段覆盖。"""
    spec = {name: dict(value) for name, value in DEFAULT_SPEC.items()}
    for name, values in (overrides or {}).items():
        spec.setdefault(name, {})
        spec[name].update(values)
    Path(path).write_text(
        json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return Path(path)


# ---------------------------------------------------------------- 运行时


def _load_spec():
    raw = os.environ.get(SPEC_ENV)
    if not raw:
        return {}
    try:
        return json.loads(Path(raw).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _bump(spec_path, key):
    state_path = Path(str(spec_path) + ".state.json")
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    count = int(state.get(key, 0)) + 1
    state[key] = count
    state_path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    return count


def _pick(values, index, default=None):
    if not values:
        return default
    return values[min(index, len(values) - 1)]


def _is_version_request(argv):
    return any(item in {"--version", "-v", "-version"} for item in argv)


def _emit_version(config, stream_is_stderr):
    text = config.get("version_output", "")
    stream = sys.stderr if stream_is_stderr else sys.stdout
    stream.write(text)
    stream.flush()
    return int(config.get("version_exit", 0))


def _run_xelatex(config, argv, spec_path):
    output_dir = Path(".")
    job = None
    for item in argv:
        if item.startswith("-output-directory="):
            output_dir = Path(item.split("=", 1)[1])
        elif not item.startswith("-"):
            job = Path(item).stem
    if job is None:
        sys.stderr.write("fake xelatex: 没有给出 .tex 目标\n")
        return 2

    index = _bump(spec_path, "xelatex:%s:%s" % (Path.cwd(), job)) - 1
    output_dir.mkdir(parents=True, exist_ok=True)

    log_text = _pick(
        config.get("log_by_pass") or [], index, config.get("log", "")
    )
    (output_dir / (job + ".log")).write_text(log_text, encoding="utf-8")

    if "-recorder" in argv:
        lines = _pick(config.get("fls_by_pass") or [], index, config.get("fls") or [])
        body = "PWD %s\n" % Path.cwd()
        body += "".join(str(item) + "\n" for item in lines)
        (output_dir / (job + ".fls")).write_text(body, encoding="utf-8")

    record = _pick(config.get("passes") or [], index, {"exit_code": 0}) or {}
    if config.get("write_pdf", True) and not record.get("skip_pdf"):
        content = config.get("pdf_content", "%PDF-1.4 fake\n")
        (output_dir / (job + ".pdf")).write_text(
            content if isinstance(content, str) else str(content), encoding="utf-8"
        )
    elif record.get("remove_pdf") or not config.get("write_pdf", True):
        target = output_dir / (job + ".pdf")
        if target.exists():
            target.unlink()
    return int(record.get("exit_code", 0))


def _run_latexmk(config, xelatex_config, argv, spec_path):
    """用最终一遍 XeLaTeX 的 log/fls 模拟 latexmk 的稳定构建结果。"""
    output_dir = Path("build")
    source = None
    for item in argv:
        if item.startswith(("-outdir=", "-output-directory=")):
            output_dir = Path(item.split("=", 1)[1])
        elif item.endswith(".tex"):
            source = Path(item)
    if source is None:
        sys.stderr.write("fake latexmk: 没有给出 .tex 目标\n")
        return 2

    # 可选地模拟 latexmk 的增量路径：有数据库和全部输出时，默认可能跳过 TeX。
    # 回归测试通过 -gt 强制 XeLaTeX 运行，避免把缓存 PDF 误登记为当前工具链产物。
    job = source.stem
    cached_outputs = (
        output_dir / (job + ".fdb_latexmk"),
        output_dir / (job + ".pdf"),
        output_dir / (job + ".log"),
        output_dir / (job + ".fls"),
    )
    if (
        config.get("skip_when_cached")
        and "-gt" not in argv
        and all(path.is_file() for path in cached_outputs)
    ):
        return int(config.get("cached_exit_code", 0))

    xelatex_argv = [
        "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
        "-no-shell-escape", "-recorder",
        "-output-directory=%s" % output_dir, source.name,
    ]
    exit_code = 0
    for _ in range(int(config.get("xelatex_runs", 2))):
        exit_code = _run_xelatex(xelatex_config, xelatex_argv, spec_path)
        if exit_code != 0:
            return exit_code
    configured_exit = config.get("exit_code")
    return exit_code if configured_exit is None else int(configured_exit)


def _run_pdfinfo(config, argv):
    exit_code = int(config.get("exit_code", 0))
    if exit_code != 0:
        sys.stderr.write(config.get("stderr", "fake pdfinfo: 打不开文件\n"))
        return exit_code
    pages = config.get("pages", 2)
    body = "Title:          fake\nProducer:       fake\n"
    if pages is not None:
        body += "Pages:          %s\n" % pages
    body += "Page size:      595 x 842 pts (A4)\n"
    sys.stdout.write(config.get("stdout", body))
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    tool = Path(sys.argv[0]).name
    if argv[:1] == ["--fake-tool"]:
        tool = argv[1]
        argv = argv[2:]
    if tool not in TOOLS:
        sys.stderr.write("fake: 未知工具 %s\n" % tool)
        return 2

    spec_path = os.environ.get(SPEC_ENV, "")
    config = _load_spec().get(tool, {})
    if _is_version_request(argv):
        # poppler 三件套把版本写 stderr，xelatex 写 stdout——形状不同才测得出解析器。
        return _emit_version(config, stream_is_stderr=tool != "xelatex")
    if tool == "xelatex":
        return _run_xelatex(config, argv, spec_path)
    if tool == "latexmk":
        return _run_latexmk(config, _load_spec().get("xelatex", {}), argv, spec_path)
    if tool == "pdfinfo":
        return _run_pdfinfo(config, argv)
    sys.stdout.write("")
    return int(config.get("exit_code", 0))


if __name__ == "__main__":
    raise SystemExit(main())

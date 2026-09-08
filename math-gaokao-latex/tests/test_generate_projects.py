# -*- coding: utf-8 -*-
"""Task 13：manifest 驱动的共享 LaTeX、图形检查与 index 投影。

三条主线：
1. `md2tex` 的纯转换接口——警告与被引用 figure 全由返回值携带，模块内无全局状态；
2. 生成器的三道门禁（题号 / 答案 / figure 复用计数）与**失败零覆盖**；
3. 全批单事务提交、崩溃两端可恢复、index 投影与 manifest 身份一致。
"""
import dataclasses
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT.parent / "math-gaokao-2017-2026" / "tools"))

import md2tex
from manifest import atomic_write_json, canonical_json, file_sha256, load_manifest
from source_manifest import project_legacy_index
from transaction import TRANSACTIONS_RELATIVE, recover_transactions

import generate_projects
import split_project
from generate_projects import (
    CONVERTER_SOURCE_TARGET,
    GENERATOR_SOURCE_TARGET,
    INDEX_TARGET,
    MANIFEST_TARGET,
    RENDERER_SOURCE_TARGET,
    GenerationError,
    build_legacy_index,
    commit_project_result,
    generate_project,
    paper_sources,
    run,
    validate_project_result,
    wrap,
)


class SimulatedCrash(RuntimeError):
    pass


# ------------------------------------------------------------------ 夹具试卷（虚构 2099 卷）

QUESTIONS = """---
title: 2099 年数学真题（试题）
---

# 2099 年测试卷

## 一、选择题

**1．** 已知集合 $A=\\{x\\mid x<1\\}$，则（　　）

  A．$1$　　B．$2$

**2．** 如图，求阴影部分面积（　　）

![示意图](images/t2.png)

  A．$\\dfrac14$　　B．$\\dfrac\\pi8$

---

## 二、解答题

**3．（12 分）** 已知函数 $f(x)$。

  (1) 求 $f(1)$；

  (2) 证明 $f$ 在 $\\mathbf R$ 上单调递增。
"""

ANSWER_KEY = """---
title: 2099 年数学真题（答案要点）
---

# 2099 年测试卷 · 答案要点

## 一、选择题

**1．** 集合运算

> **答案：A**
>
> 由定义直接可得。

**2．** 几何概型

> **答案：B（$\\dfrac\\pi8$）**
>
> 由对称性可得。

## 二、解答题

**3．** 函数性质

> **(1) 答案：$f(1)=2$**
>
> 代入即可。
>
> **(2) 答案：$f$ 在 $\\mathbf R$ 上单调递增**
"""

SOLUTION_BODY = """---
title: 2099 年数学真题（解析正文）
---

# 2099 年测试卷 · 逐题解析

## 一、选择题

### 第 1 题（集合运算）

**解析**

由定义可得 $x<0$。

---

### 第 2 题（几何概型）

**解析**

由对称性直接得面积比，辅助线如下图：

![辅助线](images/t2-aux.png)

$$S=\\frac\\pi8$$

---

## 二、解答题

### 第 3 题（12 分，函数性质）

**解析**

#### (1) 求 $f(1)$

代入得

$$f(1)=2$$

#### (2) 证明单调递增

求导即可。
"""

PAPER_ID = "gk-2099-regular-national-1"
LEGACY_ID = "legacy2099"
PROJECT_DIR = "2099_全国1卷"
PAPER_ROOT = "2099"
QUESTIONS_PATH = PAPER_ROOT + "/2099_数学真题_试题.md"
ANSWER_KEY_PATH = PAPER_ROOT + "/2099_数学真题_答案要点.md"
SOLUTION_PATH = PAPER_ROOT + "/2099_数学真题_解析正文.md"
COMBINED_PATH = PAPER_ROOT + "/2099_数学真题_含解析.md"
PROJECT_RELATIVE = "math-gaokao-latex"
QUESTIONS_TEX = PROJECT_RELATIVE + "/" + PROJECT_DIR + "/questions.tex"
ANSWERS_TEX = PROJECT_RELATIVE + "/" + PROJECT_DIR + "/answers.tex"
FIGURE_MAIN = PROJECT_DIR + "/figures/f2099_t2.tex"
FIGURE_AUX = PROJECT_DIR + "/figures/f2099_aux.tex"

# 夹具自带的配图映射：生产映射表 FIGMAP 里当然没有虚构卷的图。
FIGURE_MAP = {"t2": "f2099_t2", "t2-aux": "f2099_aux"}
# 夹具自带的 index 静态元数据（manifest 不携带 base/structure/pdf_pages 等旧字段）。
INDEX_METADATA = {
    PROJECT_DIR: {
        "id": LEGACY_ID,
        "base": "2099_g1",
        "paper": "全国 1 卷",
        "track": None,
        "variant": None,
        "structure": {"选择题": [1, 2], "解答题": [3, 3]},
        "pages_q": None,
        "pages_s": None,
        "note": None,
    }
}


def paper_entry(figure_files=None, question_count=3):
    return {
        "blocked_from": None,
        "figure_files": figure_files if figure_files is not None else [
            {"path": FIGURE_AUX, "expected_occurrences": 1},
            {"path": FIGURE_MAIN, "expected_occurrences": 2},
        ],
        "issue_ids": [],
        "last_verified_hash": None,
        "legacy_ids": [LEGACY_ID],
        "legacy_source_files": [],
        "paper_id": PAPER_ID,
        "production_state": "legacy_unverified",
        "project_dir": PROJECT_DIR,
        "question_count": question_count,
        "resume_action": None,
        "source_files": {
            "answer_key": ANSWER_KEY_PATH,
            "combined_rendered": COMBINED_PATH,
            "questions": QUESTIONS_PATH,
            "solution_body": SOLUTION_PATH,
        },
        "source_ids": [],
        "title": "2099 年·全国 1 卷",
        "track": "none",
        "year": 2099,
    }


def manifest_document(papers, batches=None, revision=1):
    if batches is None:
        batches = [{
            "batch_id": "phase0-b01",
            "issues": [],
            "paper_ids": [paper["paper_id"] for paper in papers],
            "status": "planned",
        }]
    return {
        "$schema": "schemas/source-manifest.schema.json",
        "batches": batches,
        "inventory": {"root_counts": {}, "total_sources": 0},
        "last_transaction_id": None,
        "papers": papers,
        "revision": revision,
        "schema_version": 1,
        "sources": [],
        "upstream": {
            "commit": "0" * 40,
            "scoped_roots": ["普通高考"],
            "url": "https://example.invalid/gaokaomath",
        },
    }


class RepositoryFixture:
    """自带 schema、manifest、工具副本、夹具试卷与只读 figures/ 的临时 git 仓库。"""

    def __init__(self, papers=None, questions=QUESTIONS, answer_key=ANSWER_KEY,
                 solution_body=SOLUTION_BODY, figures=(FIGURE_MAIN, FIGURE_AUX)):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for key, value in (("user.email", "t13@example.invalid"), ("user.name", "Task 13")):
            subprocess.run(["git", "-C", str(self.root), "config", key, value], check=True)

        project = self.root / PROJECT_RELATIVE
        (project / "schemas").mkdir(parents=True)
        (project / "tools").mkdir(parents=True)
        shutil.copy2(
            ROOT / "schemas" / "source-manifest.schema.json",
            project / "schemas" / "source-manifest.schema.json",
        )
        # 三份源码要以规范路径存在：它们是事务的只读输入，缺一就 CAS 不上。
        for relative in (GENERATOR_SOURCE_TARGET, RENDERER_SOURCE_TARGET, CONVERTER_SOURCE_TARGET):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.repository_source(relative), target)

        papers = papers if papers is not None else [paper_entry()]
        self.manifest_path = self.root / MANIFEST_TARGET
        atomic_write_json(self.manifest_path, manifest_document(papers))
        self.write(QUESTIONS_PATH, questions)
        self.write(ANSWER_KEY_PATH, answer_key)
        self.write(SOLUTION_PATH, solution_body)
        for relative in figures:
            self.write(
                PROJECT_RELATIVE + "/" + relative,
                "%% 夹具图 %s\n\\begin{tikzpicture}\\end{tikzpicture}\n" % relative,
            )

    @staticmethod
    def repository_source(relative):
        """仓库里那份真源码的位置（夹具只是复制一份到相同的仓库相对路径）。"""
        return ROOT.parent.parent.parent / relative

    def cleanup(self):
        self.temporary.cleanup()

    def path(self, relative):
        return self.root / relative

    def write(self, relative, text):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def read(self, relative):
        return (self.root / relative).read_text(encoding="utf-8")

    def snapshot(self):
        """记录仓库内全部普通文件的字节哈希，用于「失败零覆盖」断言。"""
        recorded = {}
        for path in sorted(self.root.rglob("*")):
            if ".git" in path.parts or not path.is_file():
                continue
            recorded[path.relative_to(self.root).as_posix()] = file_sha256(path)
        return recorded

    def pending_transactions(self):
        directory = self.root / TRANSACTIONS_RELATIVE
        return sorted(item.name for item in directory.iterdir()) if directory.is_dir() else []

    def run(self, selector, value=None, write=False, event_hook=None):
        return run(
            self.manifest_path,
            selector,
            value,
            write=write,
            figure_map=FIGURE_MAP,
            index_metadata=INDEX_METADATA,
            event_hook=event_hook,
        )


# ------------------------------------------------------------------ md2tex 纯接口


class AnswerBoxXeLaTeXRegressionTests(unittest.TestCase):
    def test_a_long_mixed_answer_wraps_without_overfull_and_remains_readable(self):
        xelatex = shutil.which("xelatex")
        pdftotext = shutil.which("pdftotext")
        if not (xelatex and pdftotext):
            self.skipTest("xelatex/pdftotext 不齐，无法运行真实答案框回归")

        macros = (ROOT / "common" / "macros.tex").as_posix()
        long_answer = (
            "起始标记：答案（1）中英文 mixed English and 中文数字 2017 交错，"
            "$f'(x)=\\dfrac{x^2-ax+1}{x^2}$；当 $a\\le2$ 时函数在区间 "
            "$(0,+\\infty)$ 上单调递减；when parameter $a>2$, the function "
            "decreases, increases, and then decreases across three intervals；"
            "继续补充中英文 mixed English and 中文数字 2018 以确保答案超过一行，结束标记。"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "answer-box.tex"
            source.write_text(
                "\\documentclass[zihao=-4,a4paper,fontset=fandol]{ctexart}\n"
                "\\usepackage[margin=2.2cm]{geometry}\n"
                "\\usepackage{amsmath,amssymb,mathtools}\n"
                "\\usepackage[most]{tcolorbox}\n"
                "\\usepackage{hyperref}\n"
                f"\\input{{{macros}}}\n"
                "\\begin{document}\n"
                f"\\gkanswer{{{long_answer}}}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [xelatex, "-interaction=nonstopmode", "-halt-on-error", source.name],
                cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True,
            )
            log = (root / "answer-box.log").read_text(encoding="utf-8", errors="replace")
            extracted = subprocess.run(
                [pdftotext, "-layout", "answer-box.pdf", "-"], cwd=root, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            ).stdout

        self.assertNotIn("Overfull \\hbox", log, completed.stdout)
        self.assertIn("起始标记", extracted)
        self.assertIn("结束标记", extracted)


class ImageQuestionXeLaTeXRegressionTests(unittest.TestCase):
    def compile_question(self, question, fill="9.2cm"):
        xelatex = shutil.which("xelatex")
        pdftotext = shutil.which("pdftotext")
        if not (xelatex and pdftotext):
            self.skipTest("xelatex/pdftotext 不齐，无法运行真实题图分页回归")
        converted = md2tex.convert_markdown(
            question, md2tex.ConversionContext(figure_map={"a": "fa"})
        ).text
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "figures").mkdir()
            (root / "figures" / "fa.tex").write_text(
                "\\rule{4cm}{2.2cm}\\par FIGUREMARK\n", encoding="utf-8"
            )
            (root / "pagination.tex").write_text(
                "\\documentclass[zihao=-4,fontset=fandol]{ctexart}\n"
                "\\usepackage[paperwidth=18cm,paperheight=16cm,margin=1cm]{geometry}\n"
                "\\usepackage{tasks,needspace}\n"
                "\\NewTasksEnvironment[style=itemize]{gkopts}[\\task](4)\n"
                "\\newcommand{\\gkti}[1]{\\par\\medskip\\noindent\\textbf{#1．}}\n"
                "\\pagestyle{empty}\n"
                "\\begin{document}\n"
                f"FILLER\\par\\vspace*{{{fill}}}\n"
                + converted
                + "\\end{document}\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [xelatex, "-interaction=nonstopmode", "-halt-on-error", "pagination.tex"],
                cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            log = (root / "pagination.log").read_text(encoding="utf-8", errors="replace")
            text = subprocess.run(
                [pdftotext, "-layout", "pagination.pdf", "-"], cwd=root, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            ).stdout
        self.assertNotIn("Overfull \\hbox", log)
        return text.split("\f")

    def test_image_question_stem_figure_and_options_stay_on_one_page_near_page_end(self):
        pages = self.compile_question(
            "**7．** STEMMARK 某多面体的三视图如图所示，求梯形面积之和（　　）\n\n"
            "![三视图](images/a.png)\n\n"
            "  A．OPTIONMARK 10　　B．12　　C．14　　D．16\n"
        )
        joined = [page for page in pages if "STEMMARK" in page]
        self.assertEqual(len(joined), 1)
        self.assertIn("FIGUREMARK", joined[0])
        self.assertIn("OPTIONMARK", joined[0])

    def test_sufficient_remaining_space_does_not_force_an_extra_page(self):
        pages = self.compile_question(
            "**9．** STEMMARK 如图所示，求阴影部分面积（　　）\n\n"
            "![示意图](images/a.png)\n\n"
            "  A．OPTIONMARK 1　　B．2　　C．3　　D．4\n",
            fill="7.8cm",
        )
        filler_page = next(page for page in pages if "FILLER" in page)
        self.assertIn("STEMMARK", filler_page)
        self.assertIn("FIGUREMARK", filler_page)
        self.assertIn("OPTIONMARK", filler_page)

    def test_soft_reservation_does_not_box_a_long_image_question(self):
        long_body = "很长的题干内容。" * 180
        pages = self.compile_question(
            "**10．** STEMMARK " + long_body + "\n\n"
            "![程序框图](images/a.png)\n\n"
            "  A．OPTIONMARK 甲　　B．乙　　C．丙　　D．丁\n",
            fill="0cm",
        )
        used = [page for page in pages if any(
            marker in page for marker in ("STEMMARK", "FIGUREMARK", "OPTIONMARK")
        )]
        self.assertGreater(len(used), 1)
        self.assertTrue(any("OPTIONMARK" in page for page in used))

    def test_short_question_near_page_bottom_stays_with_previous_content(self):
        pages = self.compile_question(
            "**8．** STEMMARK 一道只有两行的短题（　　）\n\n"
            "  A．OPTIONMARK 1　　B．2　　C．3　　D．4\n",
            fill="11.8cm",
        )
        filler_page = next(page for page in pages if "FILLER" in page)
        self.assertIn("STEMMARK", filler_page)
        self.assertIn("OPTIONMARK", filler_page)


class ProductionPreambleNeedspaceTests(unittest.TestCase):
    def test_production_preamble_compiles_generated_needspace(self):
        xelatex = shutil.which("xelatex")
        if not xelatex:
            self.skipTest("xelatex 不存在，无法运行生产 preamble 集成回归")
        preamble = (ROOT / "common" / "preamble.tex").as_posix()
        generated = md2tex.convert_markdown(
            "**7．** 见图（　　）\n\n![图](images/a.png)\n\n  A．1　　B．2\n",
            md2tex.ConversionContext(figure_map={"a": "fa"}),
        ).text
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "figures").mkdir()
            (root / "figures" / "fa.tex").write_text(
                "\\rule{2cm}{1cm}\n", encoding="utf-8"
            )
            (root / "preamble-integration.tex").write_text(
                "\\documentclass[zihao=-4,a4paper,fontset=fandol]{ctexart}\n"
                f"\\input{{{preamble}}}\n"
                "\\newcommand{\\gkti}[1]{\\par\\noindent\\textbf{#1．}}\n"
                "\\begin{document}\n" + generated + "\\end{document}\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [xelatex, "-interaction=nonstopmode", "-halt-on-error",
                 "preamble-integration.tex"],
                cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertNotIn("Undefined control sequence", completed.stdout)


class ConversionInterfaceTests(unittest.TestCase):
    def test_the_module_keeps_no_global_warning_state(self):
        # 全局 warning 会让批量生成里「哪一卷出的问题」不可判定，必须彻底消失。
        self.assertFalse(hasattr(md2tex, "warnings"))

    def test_returns_text_warnings_and_referenced_figures(self):
        source = "**1．** 见图。\n\n![甲](images/a.png)\n"
        result = md2tex.convert_markdown(
            source, md2tex.ConversionContext(figure_map={"a": "fa"})
        )
        self.assertIn("\\input{figures/fa}", result.text)
        self.assertEqual(result.warnings, ())
        self.assertEqual(result.referenced_figures, ("fa",))

    def test_records_every_occurrence_of_a_reused_figure(self):
        source = "![甲](images/a.png)\n\n![甲](images/a.png)\n\n![乙](images/b.png)\n"
        result = md2tex.convert_markdown(
            source, md2tex.ConversionContext(figure_map={"a": "fa", "b": "fb"})
        )
        # 复用计数靠它，去重就等于把「同一张图被引两次」抹平成一次。
        self.assertEqual(result.referenced_figures, ("fa", "fa", "fb"))

    def test_an_image_keeps_both_adjacent_page_break_guards_without_changing_content(self):
        source = (
            "**7．** 题干末句。\n\n"
            "![三视图](images/a.png)\n\n"
            "  A．$1$　　B．$2$　　C．$3$　　D．$4$\n"
        )
        result = md2tex.convert_markdown(
            source, md2tex.ConversionContext(figure_map={"a": "fa"})
        )
        figure = r"\begin{center}\input{figures/fa}\end{center}"
        protected = "题干末句。\n\\nopagebreak[4]\n%s\n\\nopagebreak[4]\n\\begin{gkopts}" % figure

        self.assertIn(protected, result.text)
        self.assertEqual(result.text.count(r"\nopagebreak[4]"), 2)
        self.assertIn(r"\Needspace{0.4\textheight}", result.text)
        self.assertEqual(result.text.count(figure), 1)
        self.assertEqual(result.text.count(r"\gkti{7}"), 1)
        self.assertEqual(result.text.count(r"\task "), 4)
        self.assertEqual(result.referenced_figures, ("fa",))
        # 变异牙齿：删掉图片前或图片后的任一保护，`protected` 与数量断言都会变红。

    def test_display_math_keeps_the_introducing_line_with_the_formula(self):
        result = md2tex.convert_markdown(
            "所以\n\n$$\nx=1.\n$$\n",
            md2tex.ConversionContext(figure_map={}),
        )

        self.assertIn("所以\n\n\\nopagebreak[4]\n\\[", result.text)
        self.assertEqual(result.text.count(r"\nopagebreak[4]"), 1)

    def test_choice_answer_parentheses_do_not_split_across_lines(self):
        result = md2tex.convert_markdown(
            "**1．** 结果为（　　）\n\n  A．1　　B．2\n",
            md2tex.ConversionContext(figure_map={}),
        )

        self.assertIn(r"结果为\mbox{（　　）}", result.text)

    def test_plain_cjk_option_of_seven_chars_uses_two_columns(self):
        # 纯文本选项每个 CJK 字满字宽，「A．甲与丙相互独立」在 4 栏里会把「立」
        # 折到下一行悬挂（2021 新高考Ⅰ 第 8 题实测）。7 字纯文本选项必须落到 2 栏。
        result = md2tex.convert_markdown(
            "**8．** 则（　　）\n\n"
            "  A．甲与丙相互独立　　B．甲与丁相互独立　　C．乙与丙相互独立　　D．丙与丁相互独立\n",
            md2tex.ConversionContext(figure_map={}),
        )
        self.assertIn(r"\begin{gkopts}(2)", result.text)

    def test_math_option_of_similar_source_length_stays_four_columns(self):
        # 数学段 0.55 折算后仍可能到 9–10 单元，但分数实际渲染很窄，不该被降为 2 栏。
        result = md2tex.convert_markdown(
            "**1．** 则（　　）\n\n"
            "  A．$\\dfrac{10\\pi}9$　　B．$\\dfrac{8\\pi}9$　　C．$\\dfrac{7\\pi}9$　　D．$\\dfrac{5\\pi}9$\n",
            md2tex.ConversionContext(figure_map={}),
        )
        self.assertIn(r"\begin{gkopts}(4)", result.text)

    def test_solution_heading_stays_with_its_first_paragraph(self):
        result = md2tex.convert_markdown(
            "**解析**\n\n第一步。\n",
            md2tex.ConversionContext(figure_map={}),
        )

        self.assertIn(
            "\\Needspace{4\\baselineskip}\n\\textbf{解析}\n\n第一步。",
            result.text,
        )
        ordinary = md2tex.convert_markdown(
            "**解析方法**\n", md2tex.ConversionContext(figure_map={})
        )
        self.assertNotIn(r"\Needspace", ordinary.text)

    def test_statistical_appendix_stays_with_its_following_table(self):
        source = (
            "附：$K^2=1$，\n\n"
            "| $P$ | $0.05$ |\n"
            "|:---:|:---:|\n"
            "| $k$ | $3.841$ |\n"
        )
        result = md2tex.convert_markdown(
            source, md2tex.ConversionContext(figure_map={})
        )

        self.assertIn(r"\Needspace{10\baselineskip}", result.text)
        ordinary = md2tex.convert_markdown(
            "附：普通说明。\n", md2tex.ConversionContext(figure_map={})
        )
        self.assertNotIn(r"\Needspace", ordinary.text)

    def test_strict_mode_fails_on_any_warning(self):
        with self.assertRaises(md2tex.ConversionError) as caught:
            md2tex.convert_markdown(
                "![甲](images/a.png)\n", md2tex.ConversionContext(figure_map={})
            )
        self.assertEqual(len(caught.exception.warnings), 1)
        self.assertIn("图片无映射", caught.exception.warnings[0])

    def test_lenient_mode_carries_the_warning_in_the_result(self):
        result = md2tex.convert_markdown(
            "![甲](images/a.png)\n",
            md2tex.ConversionContext(figure_map={}, strict=False),
        )
        self.assertEqual(len(result.warnings), 1)
        self.assertEqual(result.referenced_figures, ())

    def test_unpaired_dollar_is_reported_as_a_warning(self):
        with self.assertRaises(md2tex.ConversionError) as caught:
            md2tex.convert_markdown(
                "这里 $x+1 少了一个美元号。\n", md2tex.ConversionContext(figure_map={})
            )
        self.assertIn("未配对的 $", caught.exception.warnings[0])

    def test_a_failed_conversion_does_not_leak_into_the_next_one(self):
        context = md2tex.ConversionContext(figure_map={}, strict=False)
        first = md2tex.convert_markdown("$x\n", context)
        second = md2tex.convert_markdown("普通一行。\n", context)
        self.assertEqual(len(first.warnings), 1)
        self.assertEqual(second.warnings, ())

    def test_inline_conversion_shares_the_same_result_shape(self):
        result = md2tex.convert_inline(
            "**答案：$1$**", md2tex.ConversionContext(figure_map={})
        )
        self.assertEqual(result.text, "\\textbf{答案：$1$}")
        self.assertEqual(result.warnings, ())

    def test_the_figure_map_comes_from_the_context_not_a_global(self):
        result = md2tex.convert_markdown(
            "![太极](images/2017理-t2-太极图.png)\n",
            md2tex.ConversionContext(figure_map={"2017理-t2-太极图": "覆盖名"}),
        )
        self.assertIn("figures/覆盖名", result.text)

    def test_1956_source_figures_have_explicit_production_mappings(self):
        expected = {
            "1956-t3-圆": "f1956_t3_circle",
            "1956-t4-棱柱": "f1956_t4_prism",
            "1956-t4-证明": "f1956_t4_proof_prism",
        }
        self.assertEqual(
            {name: md2tex.FIGMAP[name] for name in expected},
            expected,
        )

    def test_1957_source_figures_have_explicit_production_mappings(self):
        expected = {
            "1957-t4-四面体": "f1957_t4_tetra",
            "1957-t5-平行平面": "f1957_t5_parallel",
            "1957-t7-内切圆": "f1957_t7_incircle",
            "1957-t8-圆": "f1957_t8_circle",
        }
        self.assertEqual(
            {name: md2tex.FIGMAP[name] for name in expected},
            expected,
        )

    def test_1959_source_figures_have_explicit_production_mappings(self):
        expected = {
            "1959-t6-体积": "f1959_t6_volume",
            "1959-t8-三角形": "f1959_t8_triangle",
            "1959-t10-圆": "f1959_t10_circle",
        }
        self.assertEqual(
            {name: md2tex.FIGMAP[name] for name in expected},
            expected,
        )

    def test_1960_source_figures_have_explicit_production_mappings(self):
        expected = {
            "1960-t3-航行": "f1960_t3_navigation",
            "1960-t4-抛物线": "f1960_t4_parabola",
            "1960-t5-钢珠": "f1960_t5_ball",
            "1960-t6-四棱锥": "f1960_t6_pyramid",
        }
        self.assertEqual(
            {name: md2tex.FIGMAP[name] for name in expected},
            expected,
        )

    def test_1961_source_figures_have_explicit_production_mappings(self):
        expected = {
            "1961-t3-圆环": "f1961_t3_annulus",
            "1961-t4-测高": "f1961_t4_mountain",
            "1961-t5-排水管": "f1961_t5_segment",
            "1961-t6-二面角": "f1961_t6_dihedral",
        }
        self.assertEqual(
            {name: md2tex.FIGMAP[name] for name in expected},
            expected,
        )

    def test_1962_source_figures_have_explicit_production_mappings(self):
        expected = {
            "1962-t5-内接矩形": "f1962_t5_rectangle",
            "1962-t5-外切菱形": "f1962_t5_tangent_rhombus",
            "1962-t7-正方形": "f1962_t7_square",
            "1962-t8-三角形": "f1962_t8_triangle",
            "1962-t9-正方体": "f1962_t9_cube",
        }
        self.assertEqual(
            {name: md2tex.FIGMAP[name] for name in expected},
            expected,
        )

    def test_1961_live_answers_keep_cjk_punctuation_outside_math(self):
        manifest = load_manifest(ROOT / "source-manifest.json")
        paper = next(
            item for item in manifest["papers"]
            if item["paper_id"] == "gk-1961-regular-national"
        )
        result = generate_project(ROOT.parent.parent.parent, paper_sources(paper))
        answers = result.targets[
            PROJECT_RELATIVE + "/1961_全国卷/answers.tex"
        ].decode("utf-8")
        math_blocks = re.findall(r"\\\[(.*?)\\\]", answers, flags=re.DOTALL)
        self.assertTrue(math_blocks)
        self.assertFalse(any(re.search(r"[。且]", block) for block in math_blocks))


# ------------------------------------------------------------------ 环境边界：包裹规则


class WrapBoundaryTests(unittest.TestCase):
    def test_a_question_subpart_heading_closes_the_previous_question(self):
        text = "\\gkti{1}第一题\n正文\n\\gksubpart{（一）必考题}\n\\gkti{2}第二题\n"
        wrapped, numbers = wrap(text, "questions")
        self.assertEqual(numbers, [1, 2])
        # 节级标题必须落在 question 环境之外，否则它会被排进上一题的题干里。
        self.assertIn("\\end{question}\n\\gksubpart{（一）必考题}\n\\begin{question}", wrapped)

    def test_a_solution_subpart_heading_stays_inside_the_answer(self):
        text = "\\gksolhead{1}{集合}\n\\gksubpart{(1)}\n推导\n\\gksolhead{2}{几何}\n"
        wrapped, numbers = wrap(text, "answers")
        self.assertEqual(numbers, [1, 2])
        # 解析里的 gksubpart 是题内小问标题，被当成边界会把一道题劈成两半。
        self.assertNotIn("\\end{answer}\n\\gksubpart{(1)}", wrapped)
        self.assertIn("\\gksubpart{(1)}", wrapped)

    def test_a_part_heading_closes_the_block_in_both_modes(self):
        for mode, head in (("questions", "\\gkti{1}题"), ("answers", "\\gksolhead{1}{题}")):
            wrapped, _ = wrap(head + "\n\\gkpart{二、填空题}\n", mode)
            self.assertIn("\\gkpart{二、填空题}", wrapped)
            self.assertNotIn("\\gkpart{二、填空题}\n\\end{", wrapped)


# ------------------------------------------------------------------ 生成与门禁


class GenerateProjectTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.manifest = load_manifest(self.fixture.manifest_path)
        self.sources = paper_sources(self.manifest["papers"][0])

    def build(self):
        return generate_project(self.fixture.root, self.sources, figure_map=FIGURE_MAP)

    def test_generates_exactly_the_two_shared_latex_targets(self):
        result = self.build()
        self.assertEqual(sorted(result.targets), sorted([QUESTIONS_TEX, ANSWERS_TEX]))

    def test_the_generated_header_is_a_single_percent_tex_comment(self):
        # `.format()` 不认 `%%` 转义，写错就会在 TeX 里留下一串字面 `%%`。
        for relative, opening in (
            (QUESTIONS_TEX, "% questions.tex ——"), (ANSWERS_TEX, "% answers.tex ——"),
        ):
            head = self.build().targets[relative].decode("utf-8").split("\n")[:2]
            self.assertTrue(head[0].startswith(opening), head[0])
            self.assertFalse(head[0].startswith("%%"), head[0])
            self.assertTrue(head[1].startswith("% 由 tools/generate_projects.py"), head[1])

    def test_questions_come_from_the_questions_markdown_only(self):
        text = self.build().targets[QUESTIONS_TEX].decode("utf-8")
        self.assertIn("\\gkti{1}", text)
        self.assertIn("已知集合", text)
        # 题目版绝不能带答案。
        self.assertNotIn("\\gkanswer{", text)

    def test_answers_carry_the_question_stem_the_derivation_and_the_final_answer(self):
        text = self.build().targets[ANSWERS_TEX].decode("utf-8")
        self.assertIn("\\gksolhead{1}", text)
        self.assertIn("由定义可得", text)                       # 来自解析正文
        self.assertIn("\\textbf{题目}", text)                   # 来自试题
        self.assertIn("\\gkanswer{答案：A}", text)              # 来自答案要点
        self.assertIn("$\\dfrac\\pi8$", text)

    def test_every_question_is_wrapped_in_its_own_environment(self):
        result = self.build()
        self.assertEqual(result.question_numbers["questions"], (1, 2, 3))
        self.assertEqual(result.question_numbers["answers"], (1, 2, 3))
        answers = result.targets[ANSWERS_TEX].decode("utf-8")
        self.assertEqual(answers.count("\\begin{answer}"), 3)
        self.assertEqual(answers.count("\\end{answer}"), 3)

    def test_a_multi_subpart_question_gets_one_answer_block_per_subpart(self):
        result = self.build()
        self.assertEqual(result.expected_answer_counts, {1: 1, 2: 1, 3: 2})
        self.assertEqual(result.answer_counts, {1: 1, 2: 1, 3: 2})

    def test_figure_occurrences_are_counted_from_the_generated_content(self):
        result = self.build()
        # 主图题面与解析各一次、辅助图只在解析里一次——与 manifest 登记逐条相等。
        self.assertEqual(
            result.figure_occurrences, {FIGURE_MAIN: 2, FIGURE_AUX: 1}
        )
        self.assertEqual(validate_project_result(self.sources, result), ())

    def test_the_project_figures_directory_is_never_written(self):
        before = self.fixture.snapshot()
        self.fixture.run("all", write=True)
        after = self.fixture.snapshot()
        for relative in (PROJECT_RELATIVE + "/" + FIGURE_MAIN, PROJECT_RELATIVE + "/" + FIGURE_AUX):
            self.assertEqual(before[relative], after[relative])

    def test_a_figure_count_mismatch_is_reported(self):
        sources = dataclasses.replace(
            self.sources, figures=((FIGURE_MAIN, 1), (FIGURE_AUX, 1))
        )
        problems = validate_project_result(sources, self.build())
        self.assertTrue(any("figure" in problem for problem in problems), problems)

    def test_an_unregistered_figure_is_reported(self):
        sources = dataclasses.replace(self.sources, figures=((FIGURE_MAIN, 2),))
        problems = validate_project_result(sources, self.build())
        self.assertTrue(any(FIGURE_AUX in problem for problem in problems), problems)

    def test_a_question_count_mismatch_is_reported(self):
        sources = dataclasses.replace(self.sources, question_count=4)
        problems = validate_project_result(sources, self.build())
        self.assertTrue(any("题号" in problem for problem in problems), problems)


# ------------------------------------------------------------------ 失败零覆盖


class FailureLeavesEveryFileUntouchedTests(unittest.TestCase):
    """任何一种失败都不得落下半份生成物——现有文件必须逐字节不变。"""

    def assert_zero_coverage(self, **fixture_arguments):
        fixture = RepositoryFixture(**fixture_arguments)
        self.addCleanup(fixture.cleanup)
        before = fixture.snapshot()
        with self.assertRaises(GenerationError):
            fixture.run("all", write=True)
        self.assertEqual(fixture.snapshot(), before)
        self.assertEqual(fixture.pending_transactions(), [])
        return fixture

    def test_a_missing_question_writes_nothing(self):
        self.assert_zero_coverage(
            questions=QUESTIONS.replace("**3．（12 分）** 已知函数 $f(x)$。", "")
        )

    def test_a_duplicated_question_number_writes_nothing(self):
        self.assert_zero_coverage(questions=QUESTIONS.replace("**2．**", "**1．**"))

    def test_an_unmapped_figure_writes_nothing(self):
        self.assert_zero_coverage(
            questions=QUESTIONS.replace("images/t2.png", "images/t9-未登记.png")
        )

    def test_a_missing_figure_file_writes_nothing(self):
        self.assert_zero_coverage(figures=(FIGURE_MAIN,))

    def test_an_unpaired_formula_writes_nothing(self):
        self.assert_zero_coverage(
            solution_body=SOLUTION_BODY.replace("由定义可得 $x<0$。", "由定义可得 $x<0。")
        )

    def test_a_figure_reuse_count_drift_writes_nothing(self):
        papers = [paper_entry(figure_files=[
            {"path": FIGURE_AUX, "expected_occurrences": 1},
            {"path": FIGURE_MAIN, "expected_occurrences": 3},
        ])]
        self.assert_zero_coverage(papers=papers)

    def test_check_mode_never_writes_even_when_everything_is_valid(self):
        fixture = RepositoryFixture()
        self.addCleanup(fixture.cleanup)
        before = fixture.snapshot()
        report = fixture.run("all", write=False)
        self.assertEqual(fixture.snapshot(), before)
        # 目标尚不存在，--check 必须如实报出差异而不是悄悄放行。
        self.assertTrue(report["problems"])


class FailureLeavesPreExistingTargetsUntouchedTests(unittest.TestCase):
    """**目标已经存在**时的失败零覆盖——这才是 brief 说的「现有文件逐字节不变」。

    上一个测试类每例都从空仓起步，快照时三个目标根本不存在，它证明的只是「干净仓
    保持干净」：哪怕实现改成「先截断目标再生成」，那些用例照样全绿。这里先真实写一轮
    让三个目标落盘，再破坏来源重跑，断言旧内容逐字节复原。
    """

    def assert_previous_targets_survive(self, damage):
        fixture = RepositoryFixture()
        self.addCleanup(fixture.cleanup)
        self.assertTrue(fixture.run("all", write=True)["written"])
        targets = (QUESTIONS_TEX, ANSWERS_TEX, INDEX_TARGET)
        for relative in targets:
            self.assertTrue(fixture.path(relative).is_file(), relative)
        written = {relative: fixture.path(relative).read_bytes() for relative in targets}

        damage(fixture)                 # 先破坏来源，再取基准快照
        before = fixture.snapshot()
        with self.assertRaises(GenerationError):
            fixture.run("all", write=True)

        self.assertEqual(fixture.snapshot(), before)
        for relative, value in written.items():
            self.assertEqual(fixture.path(relative).read_bytes(), value, relative)
        # 连事务都不该开始：门禁全过之前不碰 journal。
        self.assertEqual(fixture.pending_transactions(), [])

    def test_an_unmapped_figure_leaves_the_previous_targets_intact(self):
        self.assert_previous_targets_survive(
            lambda fixture: fixture.write(
                QUESTIONS_PATH, QUESTIONS.replace("images/t2.png", "images/t9-未登记.png")
            )
        )

    def test_a_deleted_figure_file_leaves_the_previous_targets_intact(self):
        self.assert_previous_targets_survive(
            lambda fixture: fixture.path(PROJECT_RELATIVE + "/" + FIGURE_AUX).unlink()
        )

    def test_a_missing_question_leaves_the_previous_targets_intact(self):
        self.assert_previous_targets_survive(
            lambda fixture: fixture.write(
                QUESTIONS_PATH,
                QUESTIONS.replace("**3．（12 分）** 已知函数 $f(x)$。", ""),
            )
        )

    def test_an_unpaired_formula_leaves_the_previous_targets_intact(self):
        self.assert_previous_targets_survive(
            lambda fixture: fixture.write(
                SOLUTION_PATH,
                SOLUTION_BODY.replace("由定义可得 $x<0$。", "由定义可得 $x<0。"),
            )
        )


# ------------------------------------------------------------------ 原子提交与恢复


class CommitTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_writes_all_targets_in_one_transaction(self):
        seen = {}

        def hook(event, path):
            if event == "journal_prepared":
                seen.update(json.loads(path.read_text(encoding="utf-8")))

        report = self.fixture.run("all", write=True, event_hook=hook)
        self.assertTrue(report["written"])
        self.assertEqual(seen["mode"], "content")
        self.assertEqual(
            sorted(record["path"] for record in seen["targets"]),
            sorted([QUESTIONS_TEX, ANSWERS_TEX, INDEX_TARGET]),
        )

    def test_transaction_inputs_pin_manifest_sources_figures_and_tools(self):
        seen = {}

        def hook(event, path):
            if event == "journal_prepared":
                seen.update(json.loads(path.read_text(encoding="utf-8")))

        self.fixture.run("all", write=True, event_hook=hook)
        expected = sorted([
            MANIFEST_TARGET,
            QUESTIONS_PATH, ANSWER_KEY_PATH, SOLUTION_PATH,
            PROJECT_RELATIVE + "/" + FIGURE_MAIN,
            PROJECT_RELATIVE + "/" + FIGURE_AUX,
            CONVERTER_SOURCE_TARGET, RENDERER_SOURCE_TARGET, GENERATOR_SOURCE_TARGET,
        ])
        self.assertEqual(sorted(seen["inputs"]), expected)
        self.assertEqual(
            seen["inputs"][MANIFEST_TARGET], file_sha256(self.fixture.manifest_path)
        )
        # 被重写的目标绝不能同时充当只读输入。
        for target in (QUESTIONS_TEX, ANSWERS_TEX, INDEX_TARGET):
            self.assertNotIn(target, seen["inputs"])

    def test_a_second_run_is_a_no_op(self):
        self.fixture.run("all", write=True)
        report = self.fixture.run("all", write=True)
        self.assertFalse(report["written"])
        self.assertEqual(self.fixture.pending_transactions(), [])

    def test_check_passes_after_a_write(self):
        self.fixture.run("all", write=True)
        report = self.fixture.run("all", write=False)
        self.assertEqual(report["problems"], [])

    def crash_after_target(self, ordinal):
        state = {"count": 0}

        def hook(event, path):
            if event != "target_replaced":
                return
            state["count"] += 1
            if state["count"] == ordinal:
                raise SimulatedCrash("模拟崩溃")

        with self.assertRaises(SimulatedCrash):
            self.fixture.run("all", write=True, event_hook=hook)
        self.assertEqual(len(self.fixture.pending_transactions()), 1)

    def assert_recovered(self):
        recovered = recover_transactions(self.fixture.root)
        self.assertEqual(len(recovered), 1)
        self.assertEqual(self.fixture.pending_transactions(), [])
        report = self.fixture.run("all", write=False)
        self.assertEqual(report["problems"], [])

    def test_recovers_from_a_crash_after_the_first_target(self):
        self.crash_after_target(1)
        self.assert_recovered()

    def test_recovers_from_a_crash_after_the_last_target(self):
        self.crash_after_target(3)
        self.assert_recovered()

    def test_a_later_run_recovers_the_pending_transaction_by_itself(self):
        self.crash_after_target(1)
        report = self.fixture.run("all", write=True)
        self.assertFalse(report["written"])
        self.assertEqual(self.fixture.pending_transactions(), [])


# ------------------------------------------------------------------ index 投影


class IndexProjectionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.manifest = load_manifest(self.fixture.manifest_path)

    def test_the_index_is_the_manifest_identity_projected_on_the_legacy_shape(self):
        legacy = build_legacy_index(self.manifest, INDEX_METADATA)
        expected = canonical_json(project_legacy_index(self.manifest, legacy))
        self.fixture.run("all", write=True)
        self.assertEqual(self.fixture.read(INDEX_TARGET), expected)

    def test_the_index_figures_come_from_the_manifest_registration(self):
        legacy = build_legacy_index(self.manifest, INDEX_METADATA)
        self.assertEqual(
            legacy["papers"][0]["figures"], ["f2099_aux.tex", "f2099_t2.tex"]
        )

    def test_missing_static_metadata_is_a_hard_error(self):
        with self.assertRaises(GenerationError):
            build_legacy_index(self.manifest, {})

    def test_a_structure_that_does_not_cover_every_question_is_a_hard_error(self):
        broken = {PROJECT_DIR: dict(INDEX_METADATA[PROJECT_DIR], structure={"选择题": [1, 2]})}
        with self.assertRaises(GenerationError):
            build_legacy_index(self.manifest, broken)


class IndexProjectionExcludesRuntimeStateTests(unittest.TestCase):
    """T16 控制器授权的拆雷：index 投影里不得有任何运行态。

    index.json 落在 build 回执的 `generation_input_tree` 内。运行态一旦被投影进来，
    推进一次批次状态就会改动它的字节——于是要么 `--check` 当场失配，要么 21 份回执
    连锁 stale。「推进状态」与「保持已编译产物当前」不能是互斥的两件事。
    """

    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.assertTrue(self.fixture.run("all", write=True)["written"])

    def advance(self):
        """把批次与试卷状态推进一格（真实 state 事务写进 manifest 的正是这些字段）。"""
        document = json.loads(
            self.fixture.manifest_path.read_text(encoding="utf-8")
        )
        document["batches"][0]["status"] = "provenance_verified"
        document["batches"][0]["issues"] = ["ISSUE-0007"]
        document["papers"][0]["production_state"] = "answers_verified"
        document["papers"][0]["issue_ids"] = ["ISSUE-0007"]
        document["revision"] = int(document["revision"]) + 1
        document["last_transaction_id"] = "11111111-2222-4333-8444-555555555555"
        atomic_json = self.fixture.path(MANIFEST_TARGET)
        atomic_json.write_text(canonical_json(document), encoding="utf-8")
        return document

    def test_the_index_has_no_batches_section(self):
        index = json.loads(self.fixture.read(INDEX_TARGET))
        self.assertNotIn("batches", index)
        self.assertEqual(index["generated_by"], "tools/generate_projects.py")

    def test_advancing_batch_state_leaves_the_index_bytes_untouched(self):
        before = self.fixture.path(INDEX_TARGET).read_bytes()
        document = self.advance()
        self.assertEqual(
            generate_projects.project_index_bytes(document, INDEX_METADATA), before
        )

    def test_check_still_passes_after_the_state_advanced(self):
        self.advance()
        report = self.fixture.run("all")
        self.assertEqual(report["problems"], [])
        self.assertIn(INDEX_TARGET, report["targets"])


class LiveIndexIsUnchangedTests(unittest.TestCase):
    """真库自检：manifest 驱动重建出的 index.json 必须与在库的那份逐字节相同。"""

    def test_the_repository_index_is_reproducible_from_the_manifest(self):
        manifest = load_manifest(ROOT / "source-manifest.json")
        legacy = build_legacy_index(manifest, generate_projects.INDEX_METADATA)
        expected = canonical_json(project_legacy_index(manifest, legacy))
        self.assertEqual((ROOT / "index.json").read_text(encoding="utf-8"), expected)


# ------------------------------------------------------------------ CLI 契约


class GeneratorCliTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def invoke(self, *arguments):
        return generate_projects.main(
            ["--manifest", str(self.fixture.manifest_path)] + list(arguments),
            figure_map=FIGURE_MAP,
            index_metadata=INDEX_METADATA,
        )

    def test_check_on_a_fresh_repository_exits_nonzero(self):
        self.assertEqual(self.invoke("--all", "--check"), 1)

    def test_write_then_check_exits_zero(self):
        self.assertEqual(self.invoke("--all", "--write"), 0)
        self.assertEqual(self.invoke("--all", "--check"), 0)

    def test_a_selector_is_required(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--check")
        self.assertEqual(caught.exception.code, 2)

    def test_selectors_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--all", "--paper", PAPER_ID, "--check")
        self.assertEqual(caught.exception.code, 2)

    def test_a_mode_is_required(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--all")
        self.assertEqual(caught.exception.code, 2)

    def test_write_and_check_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--all", "--write", "--check")
        self.assertEqual(caught.exception.code, 2)

    def test_batch_and_paper_selectors_work(self):
        self.assertEqual(self.invoke("--batch", "phase0-b01", "--write"), 0)
        self.assertEqual(self.invoke("--paper", PAPER_ID, "--check"), 0)

    def test_an_unknown_paper_exits_nonzero(self):
        self.assertEqual(self.invoke("--paper", "gk-不存在", "--check"), 1)


class SplitProjectCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def invoke(self, *arguments):
        return split_project.main(
            ["--manifest", str(self.fixture.manifest_path)] + list(arguments),
            figure_map=FIGURE_MAP,
            index_metadata=INDEX_METADATA,
        )

    def test_it_has_no_write_implementation_of_its_own(self):
        source = (ROOT / "tools" / "split_project.py").read_text(encoding="utf-8")
        for forbidden in ("write_text", "shutil.copy", "Transaction("):
            self.assertNotIn(forbidden, source)

    def test_check_reports_the_same_verdict_as_the_generator(self):
        self.assertEqual(self.invoke("--all", "--check"), 1)
        generate_projects.main(
            ["--manifest", str(self.fixture.manifest_path), "--all", "--write"],
            figure_map=FIGURE_MAP,
            index_metadata=INDEX_METADATA,
        )
        self.assertEqual(self.invoke("--all", "--check"), 0)
        self.assertEqual(self.invoke("--paper", PAPER_ID, "--check"), 0)

    def test_check_is_required(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--all")
        self.assertEqual(caught.exception.code, 2)

    def test_it_offers_no_write_switch(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--all", "--write")
        self.assertEqual(caught.exception.code, 2)

    def test_selectors_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as caught:
            self.invoke("--all", "--paper", PAPER_ID, "--check")
        self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()

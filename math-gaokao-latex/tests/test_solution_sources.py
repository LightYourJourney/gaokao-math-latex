import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from manifest import atomic_write_json, file_sha256
from transaction import TRANSACTIONS_RELATIVE, recover_transactions
import solution_sources
from solution_sources import (
    REPORT_TARGET,
    TOOL_SOURCE_TARGET,
    SolutionSourceError,
    check_paper,
    check_staged,
    extract_batch,
    extract_solution_blocks,
    main,
    parse_answer_points,
    parse_question_blocks,
    render_combined,
    render_migration_report,
    validate_solution_body,
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

**2．** 如图，求阴影部分面积。

![太极图](images/t2.png)

## 二、解答题

**3．（12 分）** 已知函数 $f(x)$。

  (1) 求 $f(1)$；

  (2) 证明 $f$ 在 $\\mathbf R$ 上单调递增。
"""

ANSWERS = """---
title: 2099 年数学真题（答案要点）
---

# 2099 年测试卷 · 答案要点

**答案速查表**

| 题号 | 1 | 2 |
|:---:|:---:|:---:|
| 答案 | A | B |

## 一、选择题

**1．** 集合运算

> **答案：A**
>
> 由定义直接可得。

**2．** 几何概型

> **答案：B（$\\dfrac\\pi8$）**（同[理科卷第 2 题](2099_数学真题_含解析.md)）

## 二、解答题

**3．** 函数性质

> **(1) 答案：$f(1)=2$**
>
> 代入即可。
>
> **(2) 证明要点**：求导后判号，$f'(x)>0$ 恒成立。
"""

COMBINED = """---
title: 2099 年数学真题（逐题解析）
---

# 2099 年测试卷 · 逐题解析

> **⚠️ 解析归属声明**：本文解析由本库编写者独立推导。

---

## 一、选择题

### 第 1 题（集合运算）

**题目**：已知集合 $A=\\{x\\mid x<1\\}$。

**解析**

由定义可得 $x<0$。

**答案：A**

---

### 第 2 题（几何概型）

**题目**：求阴影部分面积。

![太极图](images/t2.png)

**解析**

由对称性直接得面积比。辅助线如下图：

![辅助线](images/t2-aux.png)

$$S=\\frac\\pi8$$

**答案：B**

---

## 二、解答题

### 第 3 题（12 分，函数性质）

**题目**：已知函数 $f(x)$。

#### (1) 求 $f(1)$

代入得

$$f(1)=2$$

#### (2) 证明单调递增

这一步要说明**必须包含在答案里**的等号情形，正文里的"答案"二字不是答案块。

求导即可。

**答案（1）：$f(1)=2$**

**答案（2）：$f$ 在 $\\mathbf R$ 上单调递增**
"""

PAPER_DIR = "2099"
QUESTIONS_PATH = PAPER_DIR + "/2099_数学真题_试题.md"
ANSWERS_PATH = PAPER_DIR + "/2099_数学真题_答案要点.md"
SOLUTION_PATH = PAPER_DIR + "/2099_数学真题_解析正文.md"
COMBINED_PATH = PAPER_DIR + "/2099_数学真题_含解析.md"
MANIFEST_RELATIVE = "math-gaokao-latex/source-manifest.json"


def paper_entry(paper_id, year, directory, stem, question_count=3):
    base = "{0}/{1}".format(year, stem)
    return {
        "blocked_from": None,
        "figure_files": [],
        "issue_ids": [],
        "last_verified_hash": None,
        "legacy_ids": [paper_id.replace("gk-", "legacy")],
        "legacy_source_files": [],
        "paper_id": paper_id,
        "production_state": "legacy_unverified",
        "project_dir": directory,
        "question_count": question_count,
        "resume_action": None,
        "source_files": {
            "answer_key": base + "_答案要点.md",
            "combined_rendered": base + "_含解析.md",
            "questions": base + "_试题.md",
            "solution_body": base + "_解析正文.md",
        },
        "source_ids": [],
        "title": "测试卷 " + paper_id,
        "track": "none",
        "year": year,
    }


def manifest_document(papers, batches, revision=1):
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
    """一个自带 schema、manifest、工具副本和夹具试卷的临时 git 仓库。"""

    def __init__(self, papers=None, batches=None):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for key, value in (("user.email", "task6@example.invalid"), ("user.name", "Task 6")):
            subprocess.run(["git", "-C", str(self.root), "config", key, value], check=True)

        project = self.root / "docs" / "exams" / "math-gaokao-latex"
        (project / "schemas").mkdir(parents=True)
        (project / "tools").mkdir(parents=True)
        shutil.copy2(
            ROOT / "schemas" / "source-manifest.schema.json",
            project / "schemas" / "source-manifest.schema.json",
        )
        shutil.copy2(ROOT / "tools" / "solution_sources.py", self.root / TOOL_SOURCE_TARGET)

        papers = papers if papers is not None else [
            paper_entry("gk-2099-regular-national-1", 2099, "2099_全国1卷", "2099_数学真题")
        ]
        batches = batches if batches is not None else [{
            "batch_id": "phase0-b01",
            "issues": [],
            "paper_ids": [paper["paper_id"] for paper in papers],
            "status": "planned",
        }]
        self.manifest_path = self.root / MANIFEST_RELATIVE
        atomic_write_json(self.manifest_path, manifest_document(papers, batches))
        for paper in papers:
            files = paper["source_files"]
            self.write(files["questions"], QUESTIONS)
            self.write(files["answer_key"], ANSWERS)
            self.write(files["combined_rendered"], COMBINED)

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

    def git(self, *arguments):
        return subprocess.run(
            ["git", "-C", str(self.root)] + list(arguments),
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        ).stdout

    def commit_all(self, message="initial"):
        self.git("add", "-A")
        self.git("commit", "-qm", message)

    def pending_transactions(self):
        directory = self.root / TRANSACTIONS_RELATIVE
        return sorted(item.name for item in directory.iterdir()) if directory.is_dir() else []


# ------------------------------------------------------------------ 提取规则


class ExtractSolutionBlocksTests(unittest.TestCase):
    def test_extracts_only_reasoning(self):
        combined = """### 第 1 题（集合）\n\n**题目** 已知集合 $A$。\n\n**解析**\n由定义可得。\n\n**答案：A**\n"""
        body = extract_solution_blocks(combined)
        self.assertIn("### 第 1 题（集合）", body)
        self.assertIn("**解析**", body)
        self.assertIn("由定义可得", body)
        self.assertNotIn("**题目**", body)
        self.assertNotIn("已知集合", body)
        self.assertNotIn("**答案：A**", body)

    def test_keeps_subquestion_headings_and_their_bodies(self):
        body = extract_solution_blocks(COMBINED)
        self.assertIn("#### (1) 求 $f(1)$", body)
        self.assertIn("#### (2) 证明单调递增", body)
        self.assertIn("$$f(1)=2$$", body)
        self.assertIn("求导即可。", body)

    def test_keeps_ordinary_answer_wording_inside_a_proof(self):
        body = extract_solution_blocks(COMBINED)
        self.assertIn("必须包含在答案里", body)
        self.assertNotIn("**答案（1）：", body)
        self.assertNotIn("**答案（2）：", body)

    def test_drops_answer_block_that_carries_a_trailing_note(self):
        combined = (
            "### 第 1 题（填空）\n\n**题目**：求值。\n\n**解析**\n\n计算得结果。\n\n"
            "**答案：$\\dfrac{61}{25}$**（$=2.44$）\n"
        )
        body = extract_solution_blocks(combined)
        self.assertIn("计算得结果。", body)
        self.assertNotIn("61", body)
        self.assertNotIn("2.44", body)

    def test_keeps_multiline_paragraph_whose_first_line_looks_like_an_answer(self):
        combined = (
            "### 第 1 题（讨论）\n\n**题目**：讨论。\n\n**解析**\n\n"
            "**答案：A**\n还要说明为什么排除 B。\n"
        )
        body = extract_solution_blocks(combined)
        self.assertIn("还要说明为什么排除 B", body)

    def test_drops_the_question_figure_but_keeps_the_solution_figure(self):
        body = extract_solution_blocks(COMBINED)
        self.assertNotIn("images/t2.png", body)
        self.assertIn("images/t2-aux.png", body)

    def test_preserves_preamble_and_section_headings(self):
        body = extract_solution_blocks(COMBINED)
        self.assertTrue(body.startswith("---\ntitle: 2099 年数学真题（逐题解析）\n---"))
        self.assertIn("## 一、选择题", body)
        self.assertIn("## 二、解答题", body)

    def test_prepends_the_canonical_marker_when_the_source_has_none(self):
        combined = (
            "### 第 1 题（解答）\n\n**题目**：求解。\n\n#### (1) 第一问\n\n推导。\n\n"
            "#### (2) 第二问\n\n再推导。\n"
        )
        body = extract_solution_blocks(combined)
        self.assertEqual(
            body,
            "### 第 1 题（解答）\n\n**解析**\n\n#### (1) 第一问\n\n推导。\n\n"
            "#### (2) 第二问\n\n再推导。\n",
        )

    def test_extraction_is_idempotent(self):
        once = extract_solution_blocks(COMBINED)
        self.assertEqual(extract_solution_blocks(once), once)

    def test_rejects_a_document_without_question_blocks(self):
        with self.assertRaises(SolutionSourceError):
            extract_solution_blocks("---\ntitle: 空文档\n---\n\n没有题目。\n")


class ParseQuestionBlocksTests(unittest.TestCase):
    def test_reads_inline_numbering_with_its_score_marker(self):
        blocks = parse_question_blocks(QUESTIONS)
        self.assertEqual([block.number for block in blocks], [1, 2, 3])
        self.assertEqual(blocks[2].title, "（12 分）")
        self.assertEqual(blocks[2].subparts, (1, 2))
        self.assertEqual(blocks[0].subparts, ())
        self.assertIn("A．$1$", blocks[0].body)
        # 章节标题不得被吞进上一题。
        self.assertNotIn("## 二、解答题", blocks[1].body)
        self.assertEqual(blocks[2].lead, "## 二、解答题")

    def test_reads_heading_numbering_with_subpart_headings(self):
        blocks = parse_question_blocks(COMBINED)
        self.assertEqual([block.number for block in blocks], [1, 2, 3])
        self.assertEqual(blocks[2].title, "（12 分，函数性质）")
        self.assertEqual(blocks[2].subparts, (1, 2))
        self.assertIn("#### (1) 求 $f(1)$", blocks[2].body)

    def test_heading_style_wins_when_both_markers_are_present(self):
        text = "### 第 1 题（甲）\n\n**解析**\n\n正文里提到 **2．** 这种写法。\n"
        blocks = parse_question_blocks(text)
        self.assertEqual([block.number for block in blocks], [1])

    def test_rejects_duplicate_question_numbers(self):
        text = COMBINED.replace("### 第 3 题（12 分，函数性质）", "### 第 2 题（重题）")
        with self.assertRaises(SolutionSourceError) as caught:
            parse_question_blocks(text)
        self.assertIn("重复题号", str(caught.exception))

    def test_rejects_out_of_order_question_numbers(self):
        text = (
            "### 第 2 题（乙）\n\n**解析**\n\n甲。\n\n"
            "### 第 1 题（甲）\n\n**解析**\n\n乙。\n"
        )
        with self.assertRaises(SolutionSourceError) as caught:
            parse_question_blocks(text)
        self.assertIn("题号乱序", str(caught.exception))

    def test_accepts_a_subpart_split_across_several_headings(self):
        text = (
            "### 第 1 题（统计）\n\n**解析**\n\n#### (1) 求概率\n\n甲。\n\n"
            "#### (2) ① 合理性\n\n乙。\n\n#### (2) ② 重新估计\n\n丙。\n"
        )
        self.assertEqual(parse_question_blocks(text)[0].subparts, (1, 2))

    def test_rejects_subparts_that_do_not_start_at_one(self):
        text = "### 第 1 题（甲）\n\n**解析**\n\n#### (2) 第二问\n\n甲。\n"
        with self.assertRaises(SolutionSourceError) as caught:
            parse_question_blocks(text)
        self.assertIn("从 1 开始", str(caught.exception))

    def test_rejects_an_unknown_style(self):
        with self.assertRaises(SolutionSourceError):
            parse_question_blocks(COMBINED, style="setext")

    def test_heading_style_accepts_a_bold_subpart_anchor(self):
        # 真题里解答题常写成 `**(1) 解**` 而不是 `#### (1) …`，两者都是小问锚点。
        text = (
            "### 第 17 题（解三角形）\n\n**解析**\n\n**(1) 解**\n\n由正弦定理。\n\n"
            "**(2) 解**\n\n由余弦定理。\n"
        )
        self.assertEqual(parse_question_blocks(text)[0].subparts, (1, 2))

    def test_an_unnumbered_subheading_is_content_not_structure(self):
        # `#### 先算清折叠前后的所有长度` 属当前作用域的内容，不改变小问集合。
        text = (
            "### 第 18 题（立体几何）\n\n**解析**\n\n#### (1) 证明垂直\n\n甲。\n\n"
            "#### 先算清折叠前后的所有长度\n\n乙。\n\n#### (2) 求二面角\n\n丙。\n"
        )
        block = parse_question_blocks(text)[0]
        self.assertEqual(block.subparts, (1, 2))
        self.assertIn("#### 先算清折叠前后的所有长度", block.body)

    def test_reads_a_title_that_is_not_wrapped_in_parentheses(self):
        text = "### 第 22 题　〔坐标系与参数方程〕\n\n**解析**\n\n消参。\n"
        block = parse_question_blocks(text)[0]
        self.assertEqual(block.number, 22)
        self.assertEqual(block.title, "　〔坐标系与参数方程〕")
        self.assertEqual(
            extract_solution_blocks(text), "### 第 22 题　〔坐标系与参数方程〕\n\n**解析**\n\n消参。\n"
        )

    def test_rejects_content_left_over_after_the_last_question(self):
        text = (
            "### 第 1 题（甲）\n\n**解析**\n\n推导。\n\n"
            "## 四、选考题\n\n### 第 22 题 〔无法识别的写法〕\n\n还有一整章。\n"
        ).replace("### 第 22 题 〔无法识别的写法〕", "第 22 题 〔无法识别的写法〕")
        with self.assertRaises(SolutionSourceError) as caught:
            parse_question_blocks(text)
        self.assertIn("最后一题之后还有未归属的内容", str(caught.exception))


class ParseAnswerPointsTests(unittest.TestCase):
    def test_reads_whole_question_and_per_subpart_answers(self):
        points = {point.number: point for point in parse_answer_points(ANSWERS)}
        self.assertEqual(sorted(points), [1, 2, 3])
        self.assertEqual(points[1].answers, ((None, "A"),))
        self.assertEqual(points[2].answers, ((None, "B（$\\dfrac\\pi8$）"),))
        self.assertEqual(points[3].subparts, (1, 2))
        self.assertEqual(points[3].answers[0], (1, "$f(1)=2$"))

    def test_a_bold_anchor_without_an_answer_still_counts_as_a_subpart(self):
        # 证明类小问写作 `**(2) 证明要点**：…`，没有最终答案块，但小问确实存在。
        point = {item.number: item for item in parse_answer_points(ANSWERS)}[3]
        self.assertEqual(point.subparts, (1, 2))
        self.assertEqual([key for key, _ in point.answers], [1])

    def test_recognises_the_whole_anchor_family(self):
        original = "> **(2) 证明要点**：求导后判号，$f'(x)>0$ 恒成立。"
        for anchor in (
            "**(2) 答案：$x>0$**", "**(2) 证明**：略。", "**(2) 证明要点**：略。",
            "**(2) 解**", "**(2)** 直接计算。", "**（2）思路**：略。",
        ):
            point = {
                item.number: item
                for item in parse_answer_points(ANSWERS.replace(original, "> " + anchor))
            }[3]
            self.assertEqual(point.subparts, (1, 2), anchor)

    def test_ignores_the_lookup_table_in_the_preamble(self):
        self.assertEqual(len(parse_answer_points(ANSWERS)), 3)

    def test_rejects_a_question_without_any_answer_block(self):
        text = ANSWERS.replace("> **答案：A**", "> 只有一句话，没有答案块。")
        with self.assertRaises(SolutionSourceError) as caught:
            parse_answer_points(text)
        self.assertIn("没有可识别的加粗答案块", str(caught.exception))

    def test_rejects_mixing_whole_question_and_subpart_answers(self):
        text = ANSWERS.replace(
            "> **(1) 答案：$f(1)=2$**", "> **答案：整题**\n>\n> **(1) 答案：$f(1)=2$**"
        )
        with self.assertRaises(SolutionSourceError) as caught:
            parse_answer_points(text)
        self.assertIn("无法唯一识别答案块", str(caught.exception))

    def test_rejects_subparts_that_skip_the_first_subpart(self):
        text = ANSWERS.replace("> **(1) 答案：$f(1)=2$**\n>\n> 代入即可。\n>\n", "")
        with self.assertRaises(SolutionSourceError) as caught:
            parse_answer_points(text)
        self.assertIn("从 1 开始", str(caught.exception))

    def test_rejects_two_answer_blocks_for_one_subpart(self):
        text = ANSWERS.replace(
            "> **(2) 证明要点**：求导后判号，$f'(x)>0$ 恒成立。",
            "> **(1) 答案：$f(1)=3$**\n>\n> **(2) 答案：单调递增**",
        )
        with self.assertRaises(SolutionSourceError) as caught:
            parse_answer_points(text)
        self.assertIn("无法唯一识别答案块", str(caught.exception))

    def test_rejects_two_subpart_numbers_on_one_answer_block(self):
        text = ANSWERS.replace("> **(1) 答案：$f(1)=2$**", "> **(1) 答案（2）：$f(1)=2$**")
        with self.assertRaises(SolutionSourceError) as caught:
            parse_answer_points(text)
        self.assertIn("两处小问号", str(caught.exception))

    def test_reads_a_final_answer_whose_colon_sits_outside_the_bold_span(self):
        # 仓库既有惯例本就成对处理两种冒号位形（make_short_answers.py 的 ANS_IN/ANS_OUT、
        # SUB_IN/SUB_OUT）。冒号在加粗外的写法承载着真实答案，不得被占位符顶掉。
        for written, expected in (
            ("**(1) 答案**：$f'(x)=2x$。", "$f'(x)=2x$。"),
            ("**(1) 答案（$a=1$）**：$f'(x)=\\mathrm e^{x}-1$", "$f'(x)=\\mathrm e^{x}-1$"),
        ):
            text = ANSWERS.replace("> **(1) 答案：$f(1)=2$**", "> " + written)
            point = {item.number: item for item in parse_answer_points(text)}[3]
            self.assertEqual(point.answer_for(1), expected, written)

    def test_reads_a_whole_question_answer_whose_colon_sits_outside_the_bold_span(self):
        text = ANSWERS.replace("> **答案：A**", "> **答案**：A")
        point = {item.number: item for item in parse_answer_points(text)}[1]
        self.assertEqual(point.answers, ((None, "A"),))

    def test_rejects_an_anchor_that_says_answer_but_yields_no_value(self):
        # 占位符只许用于真正没有最终答案块的证明/表格类小问；写了「答案」却解析不出值
        # 必须报错，否则真实答案会被 `见解析版` 静默顶掉。
        for written in (
            "**(2) ① 答案：需要检查**",          # (k) 与「答案」之间夹了 ① 等次级序号
            "**(2)(i) 答案：$\\hat p=0.15$**",   # 同上，(i) 形态
            "**(2) 答案（分布列）**：",            # 冒号在外但值为空（答案其实是下面的表格）
        ):
            text = ANSWERS.replace(
                "> **(2) 证明要点**：求导后判号，$f'(x)>0$ 恒成立。", "> " + written
            )
            with self.assertRaises(SolutionSourceError) as caught:
                parse_answer_points(text)
            self.assertIn("解析不出最终答案", str(caught.exception), written)

    def test_still_placeholders_only_anchors_that_never_mention_an_answer(self):
        for written in ("**(2) 证明**：略。", "**(2) 思路**：略。", "**(2) 解**"):
            text = ANSWERS.replace(
                "> **(2) 证明要点**：求导后判号，$f'(x)>0$ 恒成立。", "> " + written
            )
            point = {item.number: item for item in parse_answer_points(text)}[3]
            self.assertEqual(point.subparts, (1, 2), written)
            self.assertIsNone(point.answer_for(2), written)


class ValidateSolutionBodyTests(unittest.TestCase):
    def test_rejects_a_copied_question_statement(self):
        body = extract_solution_blocks(COMBINED)
        polluted = body.replace("**解析**\n\n由定义", "**题目**：已知集合。\n\n**解析**\n\n由定义")
        with self.assertRaises(SolutionSourceError) as caught:
            validate_solution_body(polluted)
        self.assertIn("复制了题面", str(caught.exception))

    def test_rejects_a_copied_final_answer(self):
        body = extract_solution_blocks(COMBINED) + "\n**答案：A**\n"
        with self.assertRaises(SolutionSourceError) as caught:
            validate_solution_body(body)
        self.assertIn("独立加粗答案块", str(caught.exception))


class RenderCombinedTests(unittest.TestCase):
    def setUp(self):
        self.solution = extract_solution_blocks(COMBINED)

    def test_orders_question_then_solution_then_generated_answer(self):
        rendered = render_combined(QUESTIONS, self.solution, ANSWERS)
        block = rendered.split("### 第 1 题（集合运算）")[1].split("### 第 2 题")[0]
        self.assertLess(block.index("**题目**"), block.index("**解析**"))
        self.assertLess(block.index("**解析**"), block.index("**答案：A**"))

    def test_keeps_the_inter_question_separator_between_questions(self):
        # 真题式样（2017 理 第 1 题）：`**答案：A**` 在题末，`---` 在它之后隔开下一题。
        # 分隔线曾被算进上一题正文并渲染到答案之前——题间分隔线消失、题中多出一条 <hr>，
        # 而且 `_convert_math.sh` 会把它印进 PDF/DOCX。
        rendered = render_combined(QUESTIONS, self.solution, ANSWERS)
        self.assertIn("**答案：A**\n\n---\n\n### 第 2 题（几何概型）", rendered)
        self.assertNotIn("---\n\n**答案：A**", rendered)

    def test_the_separator_survives_the_extraction_round_trip(self):
        block = self.solution.split("### 第 1 题（集合运算）")[1].split("### 第 2 题")[0]
        self.assertTrue(block.rstrip().endswith("---"), block)
        rendered = render_combined(QUESTIONS, self.solution, ANSWERS)
        self.assertEqual(extract_solution_blocks(rendered), self.solution)

    def test_a_proof_subpart_gets_the_repo_placeholder_not_a_fabricated_answer(self):
        rendered = render_combined(QUESTIONS, self.solution, ANSWERS)
        self.assertIn("**答案（1）：$f(1)=2$**", rendered)
        self.assertIn("**答案（2）：见解析版**", rendered)
        # 证明要点的原文属于答案要点，不得被搬进展示文档冒充最终答案。
        self.assertNotIn("求导后判号，$f'(x)>0$ 恒成立。", rendered)

    def test_final_answers_come_only_from_the_answer_key(self):
        answers = ANSWERS.replace("> **答案：A**", "> **答案：D**")
        rendered = render_combined(QUESTIONS, self.solution, answers)
        self.assertIn("**答案：D**", rendered)
        self.assertNotIn("**答案：A**", rendered)

    def test_question_body_and_score_marker_come_from_the_questions_file(self):
        rendered = render_combined(QUESTIONS, self.solution, ANSWERS)
        self.assertIn("**题目**（12 分）：", rendered)
        self.assertIn("  (1) 求 $f(1)$；", rendered)
        self.assertIn("![太极图](images/t2.png)", rendered)

    def test_round_trips_through_extraction(self):
        rendered = render_combined(QUESTIONS, self.solution, ANSWERS)
        self.assertEqual(extract_solution_blocks(rendered), self.solution)

    def test_is_deterministic(self):
        first = render_combined(QUESTIONS, self.solution, ANSWERS)
        second = render_combined(QUESTIONS, self.solution, ANSWERS)
        self.assertEqual(first, second)

    def test_rejects_a_question_missing_from_the_solution_body(self):
        trimmed = self.solution.split("## 二、解答题")[0].rstrip() + "\n"
        with self.assertRaises(SolutionSourceError) as caught:
            render_combined(QUESTIONS, trimmed, ANSWERS)
        self.assertIn("解析正文题号集合与试题不一致", str(caught.exception))

    def test_rejects_a_question_missing_from_the_answer_key(self):
        trimmed = ANSWERS.split("## 二、解答题")[0]
        with self.assertRaises(SolutionSourceError) as caught:
            render_combined(QUESTIONS, self.solution, trimmed)
        self.assertIn("答案要点题号集合与试题不一致", str(caught.exception))

    def test_rejects_a_solution_whose_subparts_differ_from_the_questions(self):
        dropped = self.solution.replace("#### (2) 证明单调递增", "#### 证明单调递增")
        with self.assertRaises(SolutionSourceError) as caught:
            render_combined(QUESTIONS, dropped, ANSWERS)
        self.assertIn("小问集合与试题不一致", str(caught.exception))

    def test_rejects_an_answer_key_whose_subparts_differ_from_the_questions(self):
        answers = ANSWERS.replace(
            "> **(1) 答案：$f(1)=2$**\n>\n> 代入即可。\n>\n"
            "> **(2) 证明要点**：求导后判号，$f'(x)>0$ 恒成立。",
            "> **答案：见推导**",
        )
        with self.assertRaises(SolutionSourceError) as caught:
            render_combined(QUESTIONS, self.solution, answers)
        self.assertIn("答案要点小问集合与试题不一致", str(caught.exception))


# ------------------------------------------------------------------ 批次提取（content 事务）


class ExtractBatchTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.fixture.commit_all()
        self.addCleanup(self.fixture.cleanup)

    def run_extract(self, event_hook=None):
        return extract_batch(self.fixture.manifest_path, "phase0-b01", event_hook=event_hook)

    def test_writes_both_derived_files_in_one_transaction(self):
        before = self.fixture.read(COMBINED_PATH)
        result = self.run_extract()
        self.assertTrue(result["written"])
        self.assertEqual(result["targets"], sorted([SOLUTION_PATH, COMBINED_PATH]))
        solution = self.fixture.read(SOLUTION_PATH)
        self.assertEqual(solution, extract_solution_blocks(before))
        self.assertEqual(
            self.fixture.read(COMBINED_PATH),
            render_combined(QUESTIONS, solution, ANSWERS),
        )
        self.assertEqual(self.fixture.pending_transactions(), [])

    def test_second_run_is_a_no_op_without_opening_a_transaction(self):
        self.run_extract()
        stamp = file_sha256(self.fixture.path(COMBINED_PATH))
        result = self.run_extract()
        self.assertFalse(result["written"])
        self.assertEqual(file_sha256(self.fixture.path(COMBINED_PATH)), stamp)

    def test_solution_body_becomes_the_source_of_truth_after_migration(self):
        self.run_extract()
        # 迁移后直接改展示文档：下一次提取从解析正文重建，改动被覆盖回去。
        self.fixture.write(COMBINED_PATH, self.fixture.read(COMBINED_PATH) + "\n手工乱改。\n")
        self.run_extract()
        self.assertNotIn("手工乱改", self.fixture.read(COMBINED_PATH))

    def test_a_single_broken_paper_leaves_the_whole_batch_untouched(self):
        papers = [
            paper_entry("gk-2099-regular-national-1", 2099, "2099_全国1卷", "2099_数学真题"),
            paper_entry("gk-2098-regular-national-1", 2098, "2098_全国1卷", "2098_数学真题"),
        ]
        broken = RepositoryFixture(papers=papers)
        self.addCleanup(broken.cleanup)
        broken.write(
            "2098/2098_数学真题_答案要点.md",
            ANSWERS.replace("> **答案：A**", "> 这题忘了写答案块。"),
        )
        broken.commit_all()
        with self.assertRaises(SolutionSourceError) as caught:
            extract_batch(broken.manifest_path, "phase0-b01")
        self.assertIn("gk-2098-regular-national-1", str(caught.exception))
        self.assertFalse(broken.path(SOLUTION_PATH).exists())
        self.assertFalse(broken.path("2098/2098_数学真题_解析正文.md").exists())
        self.assertEqual(broken.read(COMBINED_PATH), COMBINED)
        self.assertEqual(broken.pending_transactions(), [])

    def test_readonly_inputs_are_pinned_to_manifest_sources_and_tool(self):
        seen = {}
        original = solution_sources.Transaction

        class Recording(original):
            def prepare(self, mode, targets, inputs, expected_revision=None):
                seen["mode"] = mode
                seen["inputs"] = dict(inputs)
                seen["targets"] = sorted(targets)
                return original.prepare(self, mode, targets, inputs, expected_revision)

        solution_sources.Transaction = Recording
        self.addCleanup(setattr, solution_sources, "Transaction", original)
        self.run_extract()
        self.assertEqual(seen["mode"], "content")
        self.assertEqual(
            sorted(seen["inputs"]),
            sorted([MANIFEST_RELATIVE, TOOL_SOURCE_TARGET, QUESTIONS_PATH, ANSWERS_PATH]),
        )
        self.assertEqual(
            seen["inputs"][MANIFEST_RELATIVE], file_sha256(self.fixture.manifest_path)
        )
        self.assertEqual(seen["targets"], sorted([SOLUTION_PATH, COMBINED_PATH]))
        # 被重写的展示文档不得混进只读输入。
        self.assertNotIn(COMBINED_PATH, seen["inputs"])

    def test_manifest_drift_during_the_run_aborts_and_asks_for_a_fresh_snapshot(self):
        manifest_path = self.fixture.manifest_path

        def drift(event, path):
            if event == "journal_prepared":
                document = json.loads(manifest_path.read_text(encoding="utf-8"))
                document["revision"] += 1
                atomic_write_json(manifest_path, document)

        with self.assertRaises(SolutionSourceError) as caught:
            self.run_extract(event_hook=drift)
        self.assertIn("从新的 manifest 快照重跑", str(caught.exception))
        self.assertFalse(self.fixture.path(SOLUTION_PATH).exists())

    def crash_after_target(self, ordinal):
        state = {"count": 0}

        def hook(event, path):
            if event != "target_replaced":
                return
            state["count"] += 1
            if state["count"] == ordinal:
                raise SimulatedCrash("模拟崩溃")

        with self.assertRaises(SimulatedCrash):
            self.run_extract(event_hook=hook)
        self.assertEqual(len(self.fixture.pending_transactions()), 1)

    def assert_recovered(self):
        recovered = recover_transactions(self.fixture.root)
        self.assertEqual(len(recovered), 1)
        self.assertEqual(self.fixture.pending_transactions(), [])
        solution = self.fixture.read(SOLUTION_PATH)
        self.assertEqual(solution, extract_solution_blocks(COMBINED))
        self.assertEqual(
            self.fixture.read(COMBINED_PATH), render_combined(QUESTIONS, solution, ANSWERS)
        )

    def test_recovers_from_a_crash_after_the_first_target(self):
        self.crash_after_target(1)
        self.assert_recovered()

    def test_recovers_from_a_crash_after_the_last_target(self):
        self.crash_after_target(2)
        self.assert_recovered()

    def test_a_later_run_recovers_the_pending_transaction_by_itself(self):
        self.crash_after_target(1)
        result = self.run_extract()
        self.assertFalse(result["written"])
        self.assertEqual(self.fixture.pending_transactions(), [])
        self.assertEqual(self.fixture.read(SOLUTION_PATH), extract_solution_blocks(COMBINED))

    def test_rejects_an_unknown_batch(self):
        with self.assertRaises(SolutionSourceError) as caught:
            extract_batch(self.fixture.manifest_path, "phase0-b99")
        self.assertIn("未知批次", str(caught.exception))


# ------------------------------------------------------------------ 只读检查与报告


class CheckPaperTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.fixture.commit_all()
        self.addCleanup(self.fixture.cleanup)
        self.sources = solution_sources.batch_papers(
            json.loads(self.fixture.manifest_path.read_text(encoding="utf-8")), "phase0-b01"
        )[0]

    def test_reports_only_the_missing_solution_body_before_migration(self):
        record = check_paper(self.fixture.root, self.sources)
        self.assertFalse(record["ok"])
        self.assertEqual(record["problems"], ["解析正文缺失：" + SOLUTION_PATH])
        self.assertEqual(record["question_numbers"], [1, 2, 3])

    def test_passes_after_migration(self):
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        record = check_paper(self.fixture.root, self.sources)
        self.assertEqual(record["problems"], [])
        self.assertTrue(record["ok"])
        self.assertEqual(
            record["files"]["solution_body"]["sha256"],
            record["files"]["solution_body"]["expected_sha256"],
        )

    def test_detects_a_hand_edited_display_document(self):
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        self.fixture.write(COMBINED_PATH, self.fixture.read(COMBINED_PATH) + "\n手工乱改。\n")
        record = check_paper(self.fixture.root, self.sources)
        self.assertIn(COMBINED_PATH + " 与确定性生成结果不一致", record["problems"])

    def test_detects_a_question_count_that_disagrees_with_the_manifest(self):
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        document = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        document["papers"][0]["question_count"] = 4
        atomic_write_json(self.fixture.manifest_path, document)
        sources = solution_sources.all_papers(document)[0]
        record = check_paper(self.fixture.root, sources)
        self.assertTrue(any("题目数与 manifest 不一致" in item for item in record["problems"]))

    def test_detects_an_answer_leaked_back_into_the_solution_body(self):
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        self.fixture.write(
            SOLUTION_PATH, self.fixture.read(SOLUTION_PATH).replace(
                "由定义可得 $x<0$。", "由定义可得 $x<0$。\n\n**答案：A**"
            )
        )
        record = check_paper(self.fixture.root, self.sources)
        self.assertIn(SOLUTION_PATH + " 与确定性生成结果不一致", record["problems"])


class MigrationReportTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.fixture.commit_all()
        self.addCleanup(self.fixture.cleanup)

    def test_records_question_numbers_old_and_new_hashes_and_results(self):
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        document = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        report = render_migration_report(document, self.fixture.root, self.fixture.manifest_path)
        self.assertEqual(report["summary"], {"paper_count": 1, "ok_count": 1, "problem_count": 0})
        paper = report["papers"][0]
        self.assertEqual(paper["question_numbers"], [1, 2, 3])
        self.assertEqual(
            paper["files"]["combined_rendered"]["sha256"],
            paper["files"]["combined_rendered"]["expected_sha256"],
        )
        self.assertEqual(paper["files"]["questions"]["path"], QUESTIONS_PATH)
        self.assertEqual(
            report["inputs"]["manifest_sha256"], file_sha256(self.fixture.manifest_path)
        )

    def test_is_reproducible_for_an_unchanged_tree(self):
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        document = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        first = render_migration_report(document, self.fixture.root, self.fixture.manifest_path)
        second = render_migration_report(document, self.fixture.root, self.fixture.manifest_path)
        self.assertEqual(first, second)


# ------------------------------------------------------------------ 暂存区范围核对


class CheckStagedTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.fixture.commit_all()
        self.addCleanup(self.fixture.cleanup)
        extract_batch(self.fixture.manifest_path, "phase0-b01")
        self.scope = [SOLUTION_PATH, COMBINED_PATH]

    def stage(self, *relatives):
        self.fixture.git("add", "--", *relatives)

    def test_passes_when_the_scope_is_exactly_staged(self):
        self.stage(*self.scope)
        self.assertEqual(check_staged(self.fixture.root, self.scope), [])

    def test_does_not_require_a_byte_identical_target_in_the_staged_diff(self):
        # 含解析被重建成与 HEAD 逐字节相同：它不会出现在 staged diff 里，也不该报错。
        self.fixture.write(COMBINED_PATH, COMBINED)
        self.stage(*self.scope)
        self.assertEqual(check_staged(self.fixture.root, self.scope), [])

    def test_rejects_staged_changes_outside_the_scope(self):
        self.fixture.write(QUESTIONS_PATH, QUESTIONS + "\n**4．** 多出来的题。\n")
        self.stage(*self.scope, QUESTIONS_PATH)
        problems = check_staged(self.fixture.root, self.scope)
        self.assertTrue(any("范围外存在 staged 变更" in item for item in problems))

    def test_rejects_an_unstaged_residue_inside_the_scope(self):
        self.stage(*self.scope)
        self.fixture.write(COMBINED_PATH, self.fixture.read(COMBINED_PATH) + "\n又改了。\n")
        problems = check_staged(self.fixture.root, self.scope)
        self.assertTrue(any("范围内存在 unstaged 残留" in item for item in problems))

    def test_rejects_a_new_file_inside_the_scope_that_was_never_staged(self):
        self.stage(COMBINED_PATH)
        problems = check_staged(self.fixture.root, self.scope)
        self.assertTrue(any("未全部 staged" in item for item in problems))
        self.assertTrue(any("unstaged 残留" in item for item in problems))

    def test_rejects_an_unstaged_deletion_inside_the_scope(self):
        self.stage(*self.scope)
        self.fixture.git("commit", "-qm", "batch")
        os.unlink(str(self.fixture.path(SOLUTION_PATH)))
        problems = check_staged(self.fixture.root, self.scope)
        self.assertTrue(any("未全部 staged" in item for item in problems))


# ------------------------------------------------------------------ CLI 契约


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.fixture.commit_all()
        self.addCleanup(self.fixture.cleanup)
        self.manifest = str(self.fixture.manifest_path)
        self.previous = Path.cwd()
        os.chdir(str(self.fixture.root))
        self.addCleanup(os.chdir, str(self.previous))
        _silence_standard_streams(self)

    def test_check_batch_fails_before_migration_and_passes_after(self):
        self.assertEqual(main(["check-batch", "--manifest", self.manifest, "--batch", "phase0-b01"]), 1)
        self.assertEqual(
            main(["extract-batch", "--manifest", self.manifest, "--batch", "phase0-b01", "--write"]), 0
        )
        self.assertEqual(main(["check-batch", "--manifest", self.manifest, "--batch", "phase0-b01"]), 0)
        self.assertEqual(main(["check-all", "--manifest", self.manifest]), 0)

    def test_extract_batch_requires_the_write_flag(self):
        with self.assertRaises(SystemExit) as caught:
            main(["extract-batch", "--manifest", self.manifest, "--batch", "phase0-b01"])
        self.assertEqual(caught.exception.code, 2)

    def test_每个子命令的必需参数都被冻结(self):
        for argv in (
            ["check-batch", "--manifest", self.manifest],
            ["check-all"],
            ["report", "--manifest", self.manifest],
            ["output-paths", "--manifest", self.manifest, "--batch", "phase0-b01"],
            ["check-staged", "--pathspec-file", "x"],
            [],
        ):
            with self.assertRaises(SystemExit) as caught:
                main(argv)
            self.assertEqual(caught.exception.code, 2, argv)

    def test_output_paths_emits_nul_terminated_ownership_scope(self):
        buffer = _captured_stdout(
            lambda: main([
                "output-paths", "--manifest", self.manifest,
                "--batch", "phase0-b01", "--nul",
            ])
        )
        self.assertEqual(
            buffer, (SOLUTION_PATH + "\0" + COMBINED_PATH + "\0").encode("utf-8")
        )

    def test_output_paths_can_append_the_shared_report(self):
        buffer = _captured_stdout(
            lambda: main([
                "output-paths", "--manifest", self.manifest, "--batch", "phase0-b01",
                "--include-report", REPORT_TARGET, "--nul",
            ])
        )
        self.assertTrue(buffer.endswith((REPORT_TARGET + "\0").encode("utf-8")))

    def test_output_paths_pins_the_report_to_its_canonical_location(self):
        with self.assertRaises(SolutionSourceError):
            main([
                "output-paths", "--manifest", self.manifest, "--batch", "phase0-b01",
                "--include-report", "math-gaokao-latex/reports/other.json", "--nul",
            ])

    def test_output_paths_feeds_git_add_pathspec_from_file(self):
        main(["extract-batch", "--manifest", self.manifest, "--batch", "phase0-b01", "--write"])
        spec = self.fixture.path("math-gaokao-latex/.work/phase0-b01-paths")
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_bytes(_captured_stdout(
            lambda: main([
                "output-paths", "--manifest", self.manifest,
                "--batch", "phase0-b01", "--nul",
            ])
        ))
        self.fixture.git(
            "add", "--pathspec-from-file=" + str(spec), "--pathspec-file-nul"
        )
        self.assertEqual(
            main(["check-staged", "--pathspec-file", str(spec), "--nul"]), 0
        )

    def test_report_writes_the_canonical_file_and_refuses_other_paths(self):
        main(["extract-batch", "--manifest", self.manifest, "--batch", "phase0-b01", "--write"])
        self.assertEqual(
            main(["report", "--manifest", self.manifest, "--output", REPORT_TARGET]), 0
        )
        document = json.loads(self.fixture.read(REPORT_TARGET))
        self.assertEqual(document["summary"]["ok_count"], 1)
        with self.assertRaises(SolutionSourceError):
            main([
                "report", "--manifest", self.manifest,
                "--output", "math-gaokao-latex/reports/other.json",
            ])

    def test_report_exits_nonzero_when_a_paper_still_fails(self):
        self.assertEqual(
            main(["report", "--manifest", self.manifest, "--output", REPORT_TARGET]), 1
        )


def _silence_standard_streams(case):
    """把 CLI 的正常输出与 argparse 用法信息挡在测试报告之外。"""
    sys.stdout.flush()
    sys.stderr.flush()
    sink = open(os.devnull, "wb")
    saved = [(fileno, os.dup(fileno)) for fileno in (1, 2)]

    def restore():
        sys.stdout.flush()
        sys.stderr.flush()
        for fileno, duplicate in saved:
            os.dup2(duplicate, fileno)
            os.close(duplicate)
        sink.close()

    case.addCleanup(restore)
    for fileno, _ in saved:
        os.dup2(sink.fileno(), fileno)


def _captured_stdout(action):
    """按文件描述符捕获 stdout 原始字节。

    重定向**之前**必须先 flush：Python 文本层里残留的旧内容会在重定向期间被冲进
    捕获文件，混进 NUL 分隔的 pathspec 里（真让 `git add --pathspec-from-file` 报
    过 128）。
    """
    sys.stdout.flush()
    handle = tempfile.TemporaryFile()
    duplicate = os.dup(1)
    try:
        os.dup2(handle.fileno(), 1)
        action()
        sys.stdout.flush()
    finally:
        os.dup2(duplicate, 1)
        os.close(duplicate)
    handle.seek(0)
    try:
        return handle.read()
    finally:
        handle.close()


if __name__ == "__main__":
    unittest.main()

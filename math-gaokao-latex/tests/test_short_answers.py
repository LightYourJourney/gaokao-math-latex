# -*- coding: utf-8 -*-
"""Task 14：结构化简答（answers_short.tex）。

三条主线：
1. 答案值从**生成的 answers.tex** 逐题提取，再与唯一事实源 `_答案要点.md` 做结构化
   比较——两侧的题号、小问号、值三者全等才允许写文件，冲突一律写前失败；
2. 版块顺序按 structure 的**题号语义顺序**，绝不依赖 JSON 键序（T4 的 `sort_keys`
   曾把「单选/多选/填空/解答」打乱成字典序，简答版随之错位）；
3. 全批 21 份一次 `content` 事务提交，失败零覆盖、崩溃两端可恢复。
"""
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

from manifest import atomic_write_json, file_sha256, load_manifest
from transaction import TRANSACTIONS_RELATIVE, recover_transactions

import make_short_answers
from make_short_answers import (
    CONVERTER_SOURCE_TARGET,
    MANIFEST_TARGET,
    RENDERER_SOURCE_TARGET,
    STRUCTURE_SOURCE_TARGET,
    TOOL_SOURCE_TARGET,
    AnswerRecord,
    ShortAnswerError,
    compare_generated_answers,
    cross_check_quick_table,
    expected_answer_records,
    generate_short_answers,
    merge_answer_records,
    paper_sources,
    parse_quick_table,
    parse_answer_points,
    parse_generated_answers_tex,
    render_short_answers,
    run,
)


class SimulatedCrash(RuntimeError):
    pass


PROJECT_RELATIVE = "math-gaokao-latex"
PAPER_ID = "gk-2099-regular-national-1"
LEGACY_ID = "legacy2099"
PROJECT_DIR = "2099_全国1卷"
TITLE = "2099 年·全国 1 卷"
PAPER_ROOT = "2099"
ANSWER_KEY_PATH = PAPER_ROOT + "/2099_数学真题_答案要点.md"
QUESTIONS_PATH = PAPER_ROOT + "/2099_数学真题_试题.md"
ANSWERS_TEX = "%s/%s/answers.tex" % (PROJECT_RELATIVE, PROJECT_DIR)
SHORT_TEX = "%s/%s/answers_short.tex" % (PROJECT_RELATIVE, PROJECT_DIR)

# 夹具的 structure：键序刻意写成 index.json 那种字典序（填空题排在单选题之前），
# 用来证明渲染只认题号语义顺序。
INDEX_METADATA = {
    PROJECT_DIR: {"structure": {"解答题": [3, 3], "选择题": [1, 2]}}
}

ANSWER_KEY = """---
title: 2099 年数学真题（答案要点）
---

# 2099 年测试卷 · 答案要点

## 答案速查表

| 题号 | 1 | 2 |
| --- | --- | --- |
| 答案 | A | B |

## 一、选择题

**1．** 集合运算

> **答案：A**
>
> 由定义直接可得。

**2．** 几何概型

> **答案：B（$\\dfrac\\pi8$）**

## 二、解答题

**3．** 函数性质

> **(1) 答案：$x=1$**
>
> 代入即可。
>
> **(2) 证明要点**：由导数符号可得。
"""

QUESTIONS = """---
title: 2099 年数学真题（试题）
---

# 2099 年测试卷

**1．** 集合运算

**2．** 几何概型

**3．（12 分）** 函数性质
"""

ANSWERS_TEX_TEXT = """% answers.tex —— 2099 年·全国 1 卷 · 参考答案与详细解析片段
\\gkpart{一、选择题}
\\begin{answer}
\\gksolhead{1}{集合运算}
\\textbf{题目}：已知集合。
由定义可得。
\\gkanswer{答案：A}
\\end{answer}
\\begin{answer}
\\gksolhead{2}{几何概型}
\\textbf{题目}：求阴影面积。
\\gkanswer{答案：B（$\\dfrac\\pi8$）}
\\end{answer}
\\gkpart{二、解答题}
\\begin{answer}
\\gksolhead{3}{12 分}
\\gksubpart{(1)}
代入得。
\\gkanswer{答案（1）：$x=1$}
\\gkanswer{答案（2）：见解析版}
\\end{answer}
"""

EXPECTED_RECORDS = (
    AnswerRecord(number=1, subpart=None, value="A"),
    AnswerRecord(number=2, subpart=None, value="B（$\\dfrac\\pi8$）"),
    AnswerRecord(number=3, subpart=1, value="$x=1$"),
    AnswerRecord(number=3, subpart=2, value="见解析版"),
)


def paper_entry(question_count=3):
    return {
        "blocked_from": None,
        "figure_files": [],
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
            "combined_rendered": PAPER_ROOT + "/2099_数学真题_含解析.md",
            "questions": PAPER_ROOT + "/2099_数学真题_试题.md",
            "solution_body": PAPER_ROOT + "/2099_数学真题_解析正文.md",
        },
        "source_ids": [],
        "title": TITLE,
        "track": "none",
        "year": 2099,
    }


def manifest_document(papers):
    return {
        "$schema": "schemas/source-manifest.schema.json",
        "batches": [{
            "batch_id": "phase0-b01",
            "issues": [],
            "paper_ids": [paper["paper_id"] for paper in papers],
            "status": "planned",
        }],
        "inventory": {"root_counts": {}, "total_sources": 0},
        "last_transaction_id": None,
        "papers": papers,
        "revision": 1,
        "schema_version": 1,
        "sources": [],
        "upstream": {
            "commit": "0" * 40,
            "scoped_roots": ["普通高考"],
            "url": "https://example.invalid/gaokaomath",
        },
    }


class RepositoryFixture:
    """自带 schema、manifest、工具副本、答案要点与生成 answers.tex 的临时 git 仓库。"""

    def __init__(self, papers=None, answer_key=ANSWER_KEY, answers_tex=ANSWERS_TEX_TEXT):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for key, value in (("user.email", "t14@example.invalid"), ("user.name", "Task 14")):
            subprocess.run(["git", "-C", str(self.root), "config", key, value], check=True)

        project = self.root / PROJECT_RELATIVE
        (project / "schemas").mkdir(parents=True)
        shutil.copy2(
            ROOT / "schemas" / "source-manifest.schema.json",
            project / "schemas" / "source-manifest.schema.json",
        )
        for relative in (
            TOOL_SOURCE_TARGET, RENDERER_SOURCE_TARGET,
            CONVERTER_SOURCE_TARGET, STRUCTURE_SOURCE_TARGET,
        ):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT.parent.parent.parent / relative, target)

        papers = papers if papers is not None else [paper_entry()]
        self.manifest_path = self.root / MANIFEST_TARGET
        atomic_write_json(self.manifest_path, manifest_document(papers))
        self.write(QUESTIONS_PATH, QUESTIONS)
        self.write(ANSWER_KEY_PATH, answer_key)
        self.write(ANSWERS_TEX, answers_tex)

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
        recorded = {}
        for path in sorted(self.root.rglob("*")):
            if ".git" in path.parts or not path.is_file():
                continue
            recorded[path.relative_to(self.root).as_posix()] = file_sha256(path)
        return recorded

    def pending_transactions(self):
        directory = self.root / TRANSACTIONS_RELATIVE
        return sorted(item.name for item in directory.iterdir()) if directory.is_dir() else []

    def run(self, selector="all", value=None, write=False, event_hook=None):
        return run(
            self.manifest_path, selector, value, write=write,
            index_metadata=INDEX_METADATA, event_hook=event_hook,
        )


# ------------------------------------------------------------------ 答案格式


class AnswerFormatTests(unittest.TestCase):
    def test_reads_every_answer_shape_out_of_the_generated_tex(self):
        self.assertEqual(parse_generated_answers_tex(ANSWERS_TEX_TEXT), EXPECTED_RECORDS)

    def test_a_bold_fallback_answer_is_read_too(self):
        # 值里含 `*` 时转换器的 ANSLINE 认不出，退化成 \textbf——那也是落地的答案。
        text = (
            "\\gksolhead{1}{}\n"
            "\\textbf{答案：$\\mathbf N^{*}$}\n"
        )
        self.assertEqual(
            parse_generated_answers_tex(text),
            (AnswerRecord(number=1, subpart=None, value="$\\mathbf N^{*}$"),),
        )

    def test_an_answer_before_any_question_head_is_a_hard_error(self):
        with self.assertRaises(ShortAnswerError):
            parse_generated_answers_tex("\\gkanswer{答案：A}\n")

    def test_the_answer_key_yields_the_same_records(self):
        self.assertEqual(expected_answer_records(ANSWER_KEY), EXPECTED_RECORDS)

    def test_a_proof_subpart_keeps_the_honest_placeholder(self):
        # 证明类小问「有锚点、无最终答案」是合法状态，绝不编造答案。
        points = {point.number: point for point in parse_answer_points(ANSWER_KEY)}
        self.assertEqual(points[3].subparts, (1, 2))
        self.assertIsNone(points[3].answer_for(2))
        self.assertEqual(EXPECTED_RECORDS[-1].value, "见解析版")

    def test_two_consistent_sources_report_no_conflict(self):
        self.assertEqual(compare_generated_answers(ANSWERS_TEX_TEXT, ANSWER_KEY), ())

    def test_a_value_conflict_is_reported(self):
        damaged = ANSWERS_TEX_TEXT.replace("答案（1）：$x=1$", "答案（1）：$x=2$")
        problems = compare_generated_answers(damaged, ANSWER_KEY)
        self.assertEqual(len(problems), 1)
        self.assertIn("第 3 题", problems[0])

    def test_a_missing_answer_block_is_reported(self):
        damaged = ANSWERS_TEX_TEXT.replace("\\gkanswer{答案（2）：见解析版}\n", "")
        self.assertTrue(compare_generated_answers(damaged, ANSWER_KEY))

    def test_an_extra_answer_block_is_reported(self):
        damaged = ANSWERS_TEX_TEXT.replace(
            "\\gkanswer{答案：A}", "\\gkanswer{答案：A}\n\\gkanswer{答案：D}"
        )
        self.assertTrue(compare_generated_answers(damaged, ANSWER_KEY))

    def test_question_oriented_quick_table_reports_pending_choice_status(self):
        quick_table = """| 题号 | 答案 | 证据 |
|:---:|:---|:---:|
| 1 | A | D |
| 2 | A、C 均可构造，无法唯一判定 | U |
| 3 | D | D |
"""
        self.assertEqual(parse_quick_table(quick_table, 3), ("A", "U", "D"))

    def test_pending_choice_answer_matches_independent_u_evidence(self):
        quick_table = """| 题号 | 答案 | 证据 |
|---|---|---|
| 1 | A | D |
| 2 | A、C 均可构造，无法唯一判定 | U |
"""
        self.assertEqual(
            cross_check_quick_table(
                quick_table,
                (("选择题", 1, 2),),
                {1: "A", 2: "U/PENDING；题面条件不能唯一确定"},
            ),
            (),
        )


# ------------------------------------------------------------------ 渲染


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.answers = merge_answer_records(EXPECTED_RECORDS)

    def test_a_targeted_override_replaces_only_one_subpart(self):
        records = (
            AnswerRecord(number=19, subpart=1, value="完整解析"),
            AnswerRecord(number=19, subpart=2, value="第二问原值"),
            AnswerRecord(number=20, subpart=None, value="未命中原值"),
        )
        self.assertEqual(
            merge_answer_records(records, {(19, 1): "见解析版"}),
            {19: "(1) 见解析版；(2) 第二问原值", 20: "未命中原值"},
        )

    def test_no_overrides_preserves_existing_merge_behavior(self):
        self.assertEqual(
            merge_answer_records(EXPECTED_RECORDS, None),
            merge_answer_records(EXPECTED_RECORDS),
        )

    def render(self, structure=None):
        return render_short_answers(
            TITLE,
            ANSWER_KEY_PATH,
            INDEX_METADATA[PROJECT_DIR]["structure"] if structure is None else structure,
            self.answers,
        )

    def test_subparts_are_joined_in_question_order(self):
        self.assertEqual(self.answers[3], "(1) $x=1$；(2) 见解析版")
        self.assertEqual(self.answers[1], "A")

    def test_sections_follow_the_question_numbers_not_the_json_key_order(self):
        text = self.render()
        self.assertLess(text.index("\\gkpart{选择题}"), text.index("\\gkpart{解答题}"))

    def test_a_realistic_four_group_paper_keeps_the_exam_order(self):
        # index.json 经 sort_keys 后的键序恰好是「单选/填空/多选/解答」，照抄即错位。
        structure = {"单选题": [1, 2], "填空题": [5, 5], "多选题": [3, 4], "解答题": [6, 6]}
        answers = {1: "A", 2: "B", 3: "AC", 4: "BD", 5: "$1$", 6: "$2$"}
        text = render_short_answers(TITLE, ANSWER_KEY_PATH, structure, answers)
        order = [text.index("\\gkpart{%s}" % name)
                 for name in ("单选题", "多选题", "填空题", "解答题")]
        self.assertEqual(order, sorted(order))

    def test_choice_groups_render_as_a_booktabs_table(self):
        text = self.render()
        self.assertIn("题号 & 1 & 2 \\\\", text)
        self.assertIn("答案 & A & B \\\\", text)

    def test_pending_choice_is_shown_as_u_with_an_explicit_legend(self):
        text = render_short_answers(
            TITLE,
            ANSWER_KEY_PATH,
            {"选择题": [1, 2], "解答题": [3, 3]},
            {1: "U/PENDING；源题面条件不唯一", 2: "A", 3: "$1$"},
        )
        self.assertIn("答案 & U & A", text)
        self.assertIn("U 表示待核", text)

    def test_other_groups_render_as_an_itemized_list(self):
        self.assertIn("\\item[\\textbf{3.}] (1) $x=1$；(2) 见解析版", self.render())

    def test_repeated_source_labels_render_without_exposing_internal_order(self):
        text = render_short_answers(
            TITLE,
            ANSWER_KEY_PATH,
            {"选择题": [11, 12], "解答题": [31, 31]},
            {11: "A", 12: "B", 31: "$1$"},
            printed_labels={11: "1", 12: "2", 31: "1"},
        )
        self.assertIn("题号 & 1 & 2", text)
        self.assertIn("\\item[\\textbf{1.}] $1$", text)
        self.assertNotIn("\\textbf{31.}", text)

    def test_generated_head_with_source_label_still_parses_internal_answer_identity(self):
        records = parse_generated_answers_tex(
            "\\gksolheadwithlabel{11}{1}{}\n\\gkanswer{答案：A}\n"
        )
        self.assertEqual(records, (AnswerRecord(11, None, "A"),))

    def test_the_header_names_the_two_compared_sources(self):
        head = self.render().split("\n")[:3]
        self.assertIn("answers_short.tex", head[0])
        self.assertIn(TITLE, head[0])
        self.assertIn("answers.tex", "\n".join(head))
        self.assertIn(ANSWER_KEY_PATH, "\n".join(head))

    def test_custom_usage_notice_can_preserve_paper_specific_provenance(self):
        notice = "来源解答整理，未经盲核；第25题待核。"
        text = render_short_answers(
            TITLE,
            ANSWER_KEY_PATH,
            INDEX_METADATA[PROJECT_DIR]["structure"],
            self.answers,
            usage_notice=notice,
        )
        self.assertIn(notice, text)
        self.assertNotIn("答案为编写者独立推导", text)

    def test_1994_source_answer_threshold_is_rendered_as_math_not_unicode_text(self):
        text = render_short_answers(
            TITLE,
            ANSWER_KEY_PATH,
            INDEX_METADATA[PROJECT_DIR]["structure"],
            self.answers,
            usage_notice=make_short_answers.SHORT_ANSWER_NOTICE_OVERRIDES[
                "gk-1994-shanghai"
            ],
        )
        self.assertIn("$t\\ge2$", text)
        self.assertNotIn("≥", text)

    def test_a_choice_answer_that_is_not_a_letter_is_a_hard_error(self):
        answers = dict(self.answers)
        answers[1] = "$1$"
        with self.assertRaises(ShortAnswerError):
            render_short_answers(
                TITLE, ANSWER_KEY_PATH, INDEX_METADATA[PROJECT_DIR]["structure"], answers
            )

    def test_a_question_missing_from_the_structure_is_a_hard_error(self):
        with self.assertRaises(ShortAnswerError):
            self.render(structure={"选择题": [1, 2]})


# ------------------------------------------------------------------ 冲突写前失败


class ConflictFailsBeforeWritingTests(unittest.TestCase):
    def assert_zero_coverage(self, **fixture_arguments):
        fixture = RepositoryFixture(**fixture_arguments)
        self.addCleanup(fixture.cleanup)
        before = fixture.snapshot()
        with self.assertRaises(ShortAnswerError):
            fixture.run(write=True)
        self.assertEqual(fixture.snapshot(), before)
        self.assertEqual(fixture.pending_transactions(), [])

    def test_a_value_conflict_writes_nothing(self):
        self.assert_zero_coverage(
            answers_tex=ANSWERS_TEX_TEXT.replace("答案（1）：$x=1$", "答案（1）：$x=9$")
        )

    def test_a_quick_table_conflict_writes_nothing(self):
        self.assert_zero_coverage(answer_key=ANSWER_KEY.replace("| 答案 | A | B |",
                                                               "| 答案 | C | B |"))

    def test_a_missing_quick_table_writes_nothing(self):
        self.assert_zero_coverage(
            answer_key=ANSWER_KEY.replace("| 答案 | A | B |", "")
        )

    def test_a_question_count_mismatch_writes_nothing(self):
        self.assert_zero_coverage(papers=[paper_entry(question_count=4)])

    def test_an_existing_short_answer_file_survives_a_later_conflict(self):
        fixture = RepositoryFixture()
        self.addCleanup(fixture.cleanup)
        self.assertTrue(fixture.run(write=True)["written"])
        written = fixture.path(SHORT_TEX).read_bytes()
        fixture.write(ANSWERS_TEX, ANSWERS_TEX_TEXT.replace("答案：A", "答案：D"))
        with self.assertRaises(ShortAnswerError):
            fixture.run(write=True)
        self.assertEqual(fixture.path(SHORT_TEX).read_bytes(), written)
        self.assertEqual(fixture.pending_transactions(), [])


# ------------------------------------------------------------------ 事务与恢复


class CommitTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def journal(self):
        seen = {}

        def hook(event, path):
            if event == "journal_prepared":
                seen.update(json.loads(path.read_text(encoding="utf-8")))

        self.fixture.run(write=True, event_hook=hook)
        return seen

    def test_all_short_answers_land_in_one_content_transaction(self):
        seen = self.journal()
        self.assertEqual(seen["mode"], "content")
        self.assertEqual([record["path"] for record in seen["targets"]], [SHORT_TEX])

    def test_inputs_pin_the_manifest_the_sources_and_the_tools(self):
        seen = self.journal()
        self.assertEqual(sorted(seen["inputs"]), sorted([
            MANIFEST_TARGET, QUESTIONS_PATH, ANSWER_KEY_PATH, ANSWERS_TEX,
            TOOL_SOURCE_TARGET, RENDERER_SOURCE_TARGET,
            CONVERTER_SOURCE_TARGET, STRUCTURE_SOURCE_TARGET,
        ]))
        self.assertEqual(
            seen["inputs"][MANIFEST_TARGET], file_sha256(self.fixture.manifest_path)
        )
        self.assertNotIn(SHORT_TEX, seen["inputs"])

    def test_a_second_run_is_a_no_op(self):
        self.fixture.run(write=True)
        self.assertFalse(self.fixture.run(write=True)["written"])
        self.assertEqual(self.fixture.pending_transactions(), [])

    def test_check_fails_before_the_first_write_and_passes_after(self):
        self.assertTrue(self.fixture.run(write=False)["problems"])
        self.fixture.run(write=True)
        self.assertEqual(self.fixture.run(write=False)["problems"], [])

    def test_check_never_writes(self):
        before = self.fixture.snapshot()
        self.fixture.run(write=False)
        self.assertEqual(self.fixture.snapshot(), before)

    def test_recovers_from_a_crash_during_commit(self):
        def hook(event, path):
            if event == "target_replaced":
                raise SimulatedCrash("模拟崩溃")

        with self.assertRaises(SimulatedCrash):
            self.fixture.run(write=True, event_hook=hook)
        self.assertEqual(len(self.fixture.pending_transactions()), 1)
        self.assertEqual(len(recover_transactions(self.fixture.root)), 1)
        self.assertEqual(self.fixture.pending_transactions(), [])
        self.assertEqual(self.fixture.run(write=False)["problems"], [])


# ------------------------------------------------------------------ 真库自检


class LiveRepositoryTests(unittest.TestCase):
    def test_generation_uses_source_labels_and_keeps_internal_answer_identity(self):
        fixture = RepositoryFixture()
        self.addCleanup(fixture.cleanup)
        questions = fixture.path(QUESTIONS_PATH)
        questions.write_text(
            questions.read_text(encoding="utf-8").replace(
                "**2．**", "**2．**<!-- printed-label: 一 -->", 1
            ),
            encoding="utf-8",
        )
        answers = fixture.path(ANSWERS_TEX)
        answers.write_text(
            answers.read_text(encoding="utf-8").replace(
                r"\gksolhead{2}{几何概型}",
                r"\gksolheadwithlabel{2}{一}{几何概型}",
                1,
            ),
            encoding="utf-8",
        )
        paper = paper_entry()
        sources = paper_sources(paper, INDEX_METADATA)

        result, problems = generate_short_answers(fixture.root, sources)

        self.assertEqual(problems, ())
        output = result.targets[SHORT_TEX].decode("utf-8")
        self.assertIn("题号 & 1 & 一", output)
        self.assertIn(r"\item[\textbf{3.}]", output)
        self.assertNotIn(r"\item[\textbf{2.}]", output)

    def test_2023_new_gaokao_1_short_answer_19_1_is_not_a_solution_leak(self):
        manifest = load_manifest(ROOT / "source-manifest.json")
        paper = next(
            paper for paper in manifest["papers"]
            if paper["paper_id"] == "gk-2023-regular-new-gaokao-1"
        )
        sources = paper_sources(paper, make_short_answers.INDEX_METADATA)
        result, problems = generate_short_answers(ROOT.parent.parent.parent, sources)
        self.assertEqual(problems, ())
        short_answers = result.targets[
            f"{PROJECT_RELATIVE}/{paper['project_dir']}/answers_short.tex"
        ].decode("utf-8")
        match = re.search(
            r"\\item\[\\textbf\{19\.\}\] (.*)", short_answers
        )
        self.assertIsNotNone(match)
        item = match.group(1)
        self.assertRegex(item, r"\(1\) (?:最终结论|见解析版)")
        self.assertNotRegex(item, r"导数|零点|分类讨论|分类讨论.*单调|递减|递增")

    def test_every_paper_agrees_between_answers_tex_and_the_answer_key(self):
        repo = ROOT.parent.parent.parent
        manifest = load_manifest(ROOT / "source-manifest.json")
        for paper in manifest["papers"]:
            problems = compare_generated_answers(
                (ROOT / paper["project_dir"] / "answers.tex").read_text(encoding="utf-8"),
                (repo / paper["source_files"]["answer_key"]).read_text(encoding="utf-8"),
            )
            self.assertEqual(problems, (), paper["paper_id"])


    def test_2022_b_science_pending_choice_generates_an_explicit_short_answer(self):
        repo = ROOT.parent.parent.parent
        manifest = load_manifest(ROOT / "source-manifest.json")
        paper = next(
            paper for paper in manifest["papers"]
            if paper["paper_id"] == "gk-2022-regular-national-b-science"
        )
        sources = paper_sources(paper, make_short_answers.INDEX_METADATA)
        result, problems = generate_short_answers(repo, sources)
        self.assertEqual(problems, ())
        short_answers = result.targets[
            f"{PROJECT_RELATIVE}/{paper['project_dir']}/answers_short.tex"
        ].decode("utf-8")
        self.assertIn("U 表示待核", short_answers)
        self.assertIn("答案 & A & A & C", short_answers)

    def test_all_2022_national_papers_have_a_valid_short_answer_source(self):
        repo = ROOT.parent.parent.parent
        manifest = load_manifest(ROOT / "source-manifest.json")
        paper_ids = (
            "gk-2022-regular-national-a-arts",
            "gk-2022-regular-national-a-science",
            "gk-2022-regular-national-b-arts",
            "gk-2022-regular-national-b-science",
        )
        for paper_id in paper_ids:
            paper = next(item for item in manifest["papers"] if item["paper_id"] == paper_id)
            sources = paper_sources(paper, make_short_answers.INDEX_METADATA)
            _, problems = generate_short_answers(repo, sources)
            self.assertEqual(problems, (), paper_id)


# ------------------------------------------------------------------ CLI 契约


class ShortAnswerCliTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def invoke(self, *arguments):
        return make_short_answers.main(
            ["--manifest", str(self.fixture.manifest_path)] + list(arguments),
            index_metadata=INDEX_METADATA,
        )

    def test_check_on_a_fresh_repository_exits_nonzero(self):
        self.assertEqual(self.invoke("--all", "--check"), 1)

    def test_write_then_check_exits_zero(self):
        self.assertEqual(self.invoke("--all", "--write"), 0)
        self.assertEqual(self.invoke("--all", "--check"), 0)

    def test_batch_and_paper_selectors_work(self):
        self.assertEqual(self.invoke("--batch", "phase0-b01", "--write"), 0)
        self.assertEqual(self.invoke("--paper", PAPER_ID, "--check"), 0)

    def test_an_unknown_paper_exits_nonzero(self):
        self.assertEqual(self.invoke("--paper", "gk-不存在", "--check"), 1)

    def test_a_conflict_exits_nonzero_instead_of_raising(self):
        self.fixture.write(ANSWERS_TEX, ANSWERS_TEX_TEXT.replace("答案：A", "答案：D"))
        self.assertEqual(self.invoke("--all", "--write"), 1)

    def test_selector_failures_raise_this_tool_s_error_type(self):
        # 骨架收敛进 cli_common 后异常类型是**参数化**出来的：退化成基类 ValueError
        # 会让直接调 run() 的调用方分不清失败来自哪个工具。
        for selector, value in (("batch", "不存在的批次"), ("paper", "gk-不存在")):
            with self.subTest(selector=selector):
                with self.assertRaises(ShortAnswerError):
                    self.fixture.run(selector, value)

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


if __name__ == "__main__":
    unittest.main()

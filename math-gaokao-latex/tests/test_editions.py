# -*- coding: utf-8 -*-
"""Task 14：四版本壳的模板化生成。

三条主线：
1. 模板只认五个固定占位符，未知占位符与缺失占位符都是硬错误；
2. 四版本的**输入矩阵**被冻结（试题版 questions；解析版 questions+answers；
   简答版 questions+answers_short；印刷版 questions+answers），且渲染出的
   `\\input` 集合必须与矩阵逐项相等——矩阵与模板分家就是壳指错文件的开始；
3. 全批 84 个壳一次 `content` 事务提交，失败零覆盖、崩溃两端可恢复。
"""
import json
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

import make_editions
from make_editions import (
    CLASS_OPTIONS,
    EDITION_INPUTS,
    EDITIONS,
    MANIFEST_TARGET,
    PLACEHOLDERS,
    TOOL_SOURCE_TARGET,
    EditionError,
    build_shells,
    load_templates,
    paper_shell,
    render_body,
    render_edition,
    run,
    template_target,
)


class SimulatedCrash(RuntimeError):
    pass


PROJECT_RELATIVE = "math-gaokao-latex"
PAPER_ID = "gk-2099-regular-national-1"
LEGACY_ID = "legacy2099"
PROJECT_DIR = "2099_全国1卷"
TITLE = "2099 年·全国 1 卷"
PAPER_ROOT = "2099"


def paper_entry(legacy_ids=None):
    return {
        "blocked_from": None,
        "figure_files": [],
        "issue_ids": [],
        "last_verified_hash": None,
        "legacy_ids": [LEGACY_ID] if legacy_ids is None else legacy_ids,
        "legacy_source_files": [],
        "paper_id": PAPER_ID,
        "production_state": "legacy_unverified",
        "project_dir": PROJECT_DIR,
        "question_count": 3,
        "resume_action": None,
        "source_files": {
            "answer_key": PAPER_ROOT + "/2099_数学真题_答案要点.md",
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
    """自带 schema、manifest、四模板、工具副本与三份共享 TeX 的临时 git 仓库。"""

    def __init__(self, papers=None, contents=("questions", "answers", "answers_short")):
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
        # 工具源码与四模板都是事务的只读输入，须以规范仓库相对路径存在。
        for relative in [TOOL_SOURCE_TARGET] + [
            template_target(edition) for edition in EDITIONS
        ]:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT.parent.parent.parent / relative, target)

        papers = papers if papers is not None else [paper_entry()]
        self.manifest_path = self.root / MANIFEST_TARGET
        atomic_write_json(self.manifest_path, manifest_document(papers))
        for name in contents:
            self.write(
                "%s/%s/%s.tex" % (PROJECT_RELATIVE, PROJECT_DIR, name),
                "%% 夹具 %s\n" % name,
            )

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
        return run(self.manifest_path, selector, value, write=write, event_hook=event_hook)

    def shell(self, edition):
        return "%s/%s/%s.tex" % (PROJECT_RELATIVE, PROJECT_DIR, edition)


# ------------------------------------------------------------------ 占位符契约


class PlaceholderTests(unittest.TestCase):
    def setUp(self):
        self.values = {
            "@@CLASS_OPTIONS@@": "zihao=-4, a4paper",
            "@@PAPER_ID@@": LEGACY_ID,
            "@@TITLE@@": TITLE,
            "@@EDITION@@": "试题版",
            "@@BODY@@": "\\input{questions}\n",
        }

    def test_the_placeholder_set_is_frozen(self):
        self.assertEqual(
            PLACEHOLDERS,
            ("@@CLASS_OPTIONS@@", "@@PAPER_ID@@", "@@TITLE@@", "@@EDITION@@", "@@BODY@@"),
        )

    def test_every_placeholder_is_substituted(self):
        template = (
            "\\documentclass[@@CLASS_OPTIONS@@]{ctexart}\n"
            "\\renewcommand{\\gkpaperid}{@@PAPER_ID@@}\n"
            "@@TITLE@@ · @@EDITION@@\n"
            "@@BODY@@\\end{document}\n"
        )
        rendered = render_edition(template, self.values)
        self.assertNotIn("@@", rendered)
        self.assertIn("zihao=-4, a4paper", rendered)
        self.assertIn(TITLE + " · 试题版", rendered)

    def test_an_unknown_placeholder_is_rejected(self):
        template = (
            "@@CLASS_OPTIONS@@@@PAPER_ID@@@@TITLE@@@@EDITION@@@@BODY@@@@ZIHAO@@"
        )
        with self.assertRaises(EditionError) as caught:
            render_edition(template, self.values)
        self.assertIn("@@ZIHAO@@", str(caught.exception))

    def test_a_missing_placeholder_is_rejected(self):
        # 少一个占位符意味着壳里少了一段身份信息（如 \gkpaperid），必须当场失败。
        template = "@@CLASS_OPTIONS@@@@TITLE@@@@EDITION@@@@BODY@@"
        with self.assertRaises(EditionError) as caught:
            render_edition(template, self.values)
        self.assertIn("@@PAPER_ID@@", str(caught.exception))

    def test_values_must_cover_exactly_the_placeholder_set(self):
        template = "@@CLASS_OPTIONS@@@@PAPER_ID@@@@TITLE@@@@EDITION@@@@BODY@@"
        incomplete = dict(self.values)
        incomplete.pop("@@BODY@@")
        with self.assertRaises(EditionError):
            render_edition(template, incomplete)

    def test_a_substituted_value_is_never_rescanned(self):
        # 值里若含 `@@…@@` 字样也只当普通文本，绝不做第二轮替换。
        values = dict(self.values, **{"@@TITLE@@": "@@PAPER_ID@@"})
        template = "@@CLASS_OPTIONS@@@@PAPER_ID@@[@@TITLE@@]@@EDITION@@@@BODY@@"
        self.assertIn("[@@PAPER_ID@@]", render_edition(template, values))


# ------------------------------------------------------------------ 输入矩阵


class InputMatrixTests(unittest.TestCase):
    def test_the_matrix_is_frozen(self):
        self.assertEqual(EDITIONS, ("试题版", "解析版", "简答版", "印刷版"))
        self.assertEqual(EDITION_INPUTS, {
            "试题版": ("questions",),
            "解析版": ("questions", "answers"),
            "简答版": ("questions", "answers_short"),
            "印刷版": ("questions", "answers"),
        })

    def test_the_rendered_body_inputs_exactly_the_matrix(self):
        for edition, expected in EDITION_INPUTS.items():
            body = render_body(edition)
            found = tuple(make_editions.body_inputs(body))
            self.assertEqual(found, expected, edition)

    def test_only_the_print_edition_uses_the_compact_class_option(self):
        self.assertEqual(CLASS_OPTIONS["印刷版"], "zihao=5, a4paper")
        for edition in ("试题版", "解析版", "简答版"):
            self.assertEqual(CLASS_OPTIONS[edition], "zihao=-4, a4paper")

    def test_the_short_edition_never_inputs_the_full_solutions(self):
        # 简答版一旦 \input{answers} 就变成了解析版，速查的意义全失。
        self.assertNotIn("answers", EDITION_INPUTS["简答版"])
        self.assertIn("answers_short", EDITION_INPUTS["简答版"])

    def test_an_unknown_edition_is_rejected(self):
        with self.assertRaises(EditionError):
            render_body("草稿版")


# ------------------------------------------------------------------ 壳生成


class ShellGenerationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.manifest = load_manifest(self.fixture.manifest_path)
        self.templates = load_templates(self.fixture.root)
        self.shell = paper_shell(self.manifest["papers"][0])

    def test_generates_four_shells_per_paper(self):
        targets = build_shells(self.templates, self.shell)
        self.assertEqual(
            sorted(targets),
            sorted(self.fixture.shell(edition) for edition in EDITIONS),
        )

    def test_the_paper_identity_reaches_every_shell(self):
        targets = build_shells(self.templates, self.shell)
        for edition in EDITIONS:
            text = targets[self.fixture.shell(edition)].decode("utf-8")
            self.assertIn("\\renewcommand{\\gkpaperid}{%s}" % LEGACY_ID, text)
            self.assertIn("\\renewcommand{\\gkheadR}{%s}" % edition, text)
            self.assertIn("{\\Large\\bfseries %s}" % TITLE, text)

    def test_a_paper_without_exactly_one_legacy_id_is_rejected(self):
        for legacy_ids in ([], ["a", "b"]):
            with self.assertRaises(EditionError):
                paper_shell(paper_entry(legacy_ids=legacy_ids))

    def test_a_missing_matrix_input_fails_before_writing(self):
        fixture = RepositoryFixture(contents=("questions", "answers"))
        self.addCleanup(fixture.cleanup)
        before = fixture.snapshot()
        with self.assertRaises(EditionError):
            fixture.run(write=True)
        self.assertEqual(fixture.snapshot(), before)
        self.assertEqual(fixture.pending_transactions(), [])

    def test_a_template_with_an_unknown_placeholder_fails_before_writing(self):
        fixture = RepositoryFixture()
        self.addCleanup(fixture.cleanup)
        relative = template_target("试题版")
        fixture.write(relative, fixture.read(relative) + "@@ZIHAO@@\n")
        before = fixture.snapshot()
        with self.assertRaises(EditionError):
            fixture.run(write=True)
        self.assertEqual(fixture.snapshot(), before)
        self.assertEqual(fixture.pending_transactions(), [])

    def test_a_missing_template_is_a_hard_error(self):
        fixture = RepositoryFixture()
        self.addCleanup(fixture.cleanup)
        fixture.path(template_target("印刷版")).unlink()
        with self.assertRaises(EditionError):
            fixture.run(write=True)


class LiveShellsAreByteIdenticalTests(unittest.TestCase):
    """真库自检：模板渲染出的 84 个壳必须与在库的那 84 个逐字节相同。

    模板化是**重构**，不是改版：任何一个字节的变化都会在黄金基线里显形为壳漂移，
    而壳漂移没有任何预授权登记可用。
    """

    def test_every_repository_shell_is_reproducible_from_the_templates(self):
        repo = ROOT.parent.parent.parent
        manifest = load_manifest(ROOT / "source-manifest.json")
        templates = load_templates(repo)
        for paper in manifest["papers"]:
            targets = build_shells(templates, paper_shell(paper))
            self.assertEqual(len(targets), 4)
            for relative, value in targets.items():
                self.assertEqual((repo / relative).read_bytes(), value, relative)


# ------------------------------------------------------------------ 事务与恢复


class CommitTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def journal(self, **arguments):
        seen = {}

        def hook(event, path):
            if event == "journal_prepared":
                seen.update(json.loads(path.read_text(encoding="utf-8")))

        self.fixture.run(write=True, event_hook=hook, **arguments)
        return seen

    def test_all_shells_land_in_one_content_transaction(self):
        seen = self.journal()
        self.assertEqual(seen["mode"], "content")
        self.assertEqual(
            sorted(record["path"] for record in seen["targets"]),
            sorted(self.fixture.shell(edition) for edition in EDITIONS),
        )

    def test_inputs_pin_the_manifest_the_templates_the_tool_and_the_matrix(self):
        seen = self.journal()
        expected = sorted(
            [MANIFEST_TARGET, TOOL_SOURCE_TARGET]
            + [template_target(edition) for edition in EDITIONS]
            + [
                "%s/%s/%s.tex" % (PROJECT_RELATIVE, PROJECT_DIR, name)
                for name in ("questions", "answers", "answers_short")
            ]
        )
        self.assertEqual(sorted(seen["inputs"]), expected)
        self.assertEqual(
            seen["inputs"][MANIFEST_TARGET], file_sha256(self.fixture.manifest_path)
        )
        for edition in EDITIONS:
            self.assertNotIn(self.fixture.shell(edition), seen["inputs"])

    def test_a_second_run_is_a_no_op(self):
        self.fixture.run(write=True)
        report = self.fixture.run(write=True)
        self.assertFalse(report["written"])
        self.assertEqual(self.fixture.pending_transactions(), [])

    def test_check_fails_before_the_first_write_and_passes_after(self):
        self.assertTrue(self.fixture.run(write=False)["problems"])
        self.fixture.run(write=True)
        self.assertEqual(self.fixture.run(write=False)["problems"], [])

    def test_check_never_writes(self):
        before = self.fixture.snapshot()
        self.fixture.run(write=False)
        self.assertEqual(self.fixture.snapshot(), before)

    def crash_after_target(self, ordinal):
        state = {"count": 0}

        def hook(event, path):
            if event != "target_replaced":
                return
            state["count"] += 1
            if state["count"] == ordinal:
                raise SimulatedCrash("模拟崩溃")

        with self.assertRaises(SimulatedCrash):
            self.fixture.run(write=True, event_hook=hook)
        self.assertEqual(len(self.fixture.pending_transactions()), 1)

    def test_a_crash_midway_leaves_no_half_set_of_shells(self):
        self.crash_after_target(2)
        # 崩溃点之后的壳尚未落盘：半套壳正是本任务要杜绝的状态。
        landed = [
            edition for edition in EDITIONS
            if self.fixture.path(self.fixture.shell(edition)).is_file()
        ]
        self.assertLess(len(landed), 4)
        self.assertEqual(len(recover_transactions(self.fixture.root)), 1)
        self.assertEqual(self.fixture.pending_transactions(), [])
        self.assertEqual(self.fixture.run(write=False)["problems"], [])

    def test_a_later_run_recovers_the_pending_transaction_by_itself(self):
        self.crash_after_target(1)
        report = self.fixture.run(write=True)
        self.assertFalse(report["written"])
        self.assertEqual(self.fixture.pending_transactions(), [])


# ------------------------------------------------------------------ CLI 契约


class EditionCliTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def invoke(self, *arguments):
        return make_editions.main(
            ["--manifest", str(self.fixture.manifest_path)] + list(arguments)
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

    def test_selector_failures_raise_this_tool_s_error_type(self):
        # 骨架收敛进 cli_common 后异常类型是**参数化**出来的：退化成基类 ValueError
        # 会让直接调 run() 的调用方分不清失败来自哪个工具。
        for selector, value in (("batch", "不存在的批次"), ("paper", "gk-不存在")):
            with self.subTest(selector=selector):
                with self.assertRaises(EditionError):
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

# -*- coding: utf-8 -*-
"""Task 15：严格 XeLaTeX 构建、实际依赖闭包、两阶段回执与安全清理。

这套测试守的是一件事——**不能假绿**。一份 build 回执要么能逐项证明「这个 PDF 是由
这些字节、这条工具链、此刻的 manifest 投影产出的」，要么就是 stale；证明链上任何一环
断了都必须降级，而不是沿用上一次的结论。仓库里那 21 个过期的「简答版.pdf」就是反面
教材：文件在、内容老、没有任何回执为它背书，任何机制都不得让它算数。

四条主线：

1. **依赖闭包**——两遍 `.fls` 的仓库内 INPUT 并集 + `generation_input_tree`
   （规范 Markdown / figure / index / 模板 / 四壳 / 全部生成器源码）+ 该卷 manifest
   投影 + 工具链指纹，任一变化即 stale；manifest 的运行态字段变化则**不得**使其 stale；
2. **两阶段回执**——formal build 先事务写 `running`，构建后第二事务写结果；中断留在
   `running` 的回执永远不能被当作 final；
3. **状态机**——`running → failed` / `running → compiled_pending_review → succeeded`，
   0.4588pt 的 Overfull 也只能候选 `compiled_pending_review`；
4. **清理门禁**——symlink、越界、tracked 内容、未被 ignore 任一命中即零删除。
"""
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent / "fixtures"))

import fake_xelatex
import build_projects
import status
from build_projects import (
    BUILD_DIR_NAME,
    EDITIONS,
    EXIT_BUILD_FAILED,
    EXIT_INVALID,
    EXIT_OK,
    EXIT_PENDING_REVIEW,
    EXIT_USAGE,
    GENERATOR_SOURCES,
    ISSUES_TARGET,
    MANIFEST_TARGET,
    PROJECTION_FIELDS,
    STATUS_TRANSITIONS,
    BuildError,
    assert_transition,
    build_manifest_projection,
    build_paper_result,
    cleanup_legacy,
    clean_build,
    dependency_tree,
    finalize_receipt,
    parse_fls,
    projection_digest,
    receipt_currency,
    resolve_toolchain,
    scan_log,
    validate_receipt,
)
from manifest import atomic_write_json, canonical_json, file_sha256, load_manifest

PROJECT_RELATIVE = "math-gaokao-latex"
PAPER_ID = "gk-2099-regular-national-1"
OTHER_ID = "gk-2099-regular-national-2"
PROJECT_DIR = "2099_全国1卷"
OTHER_DIR = "2099_全国2卷"
BATCH_ID = "phase0-b01"
PAPER_ROOT = "2099"


def paper_entry(paper_id=PAPER_ID, project_dir=PROJECT_DIR, legacy="legacy2099"):
    prefix = "%s/%s" % (PAPER_ROOT, legacy)
    return {
        "blocked_from": None,
        "figure_files": [
            {"expected_occurrences": 2, "path": "%s/figures/f1.tex" % project_dir}
        ],
        "issue_ids": [],
        "last_verified_hash": None,
        "legacy_ids": [legacy],
        "legacy_source_files": [],
        "paper_id": paper_id,
        "production_state": "legacy_unverified",
        "project_dir": project_dir,
        "question_count": 3,
        "resume_action": None,
        "source_files": {
            "answer_key": prefix + "_答案要点.md",
            "combined_rendered": prefix + "_含解析.md",
            "questions": prefix + "_试题.md",
            "solution_body": prefix + "_解析正文.md",
        },
        "source_ids": [],
        "title": "2099 年·全国 %s 卷" % paper_id[-1],
        "track": "none",
        "year": 2099,
    }


def manifest_document(papers):
    return {
        "$schema": "schemas/source-manifest.schema.json",
        "batches": [{
            "batch_id": BATCH_ID,
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


def loaded_facts(**overrides):
    """facts_loader 的返回形状：除 build/build_currency 外的全部维度。"""
    values = {
        "provenance": "current",
        "provenance_unknown": False,
        "provenance_conflicts": False,
        "artifacts": "current",
        "review": "missing",
        "review_currency": "stale",
        "issues": (),
        "batch_report_valid": False,
    }
    values.update(overrides)
    return values


def make_loader(default=None, per_paper=None):
    default = default if default is not None else loaded_facts()

    def loader(root, manifest, paper_ids):
        result = {}
        for paper_id in paper_ids:
            values = dict(default)
            values.update((per_paper or {}).get(paper_id, {}))
            result[paper_id] = values
        return result

    return loader


class RepositoryFixture:
    """自带 schema、manifest、模板、生成器源码、四壳与共享 TeX 的临时 git 仓库。

    `.gitignore` 直接复制真实文件——清理门禁的 `git check-ignore` 因此会真的去问
    Step 5 写下的那几行；忘了加 `*/build/` 时本套件必红。
    """

    def __init__(self, papers=None, commit=True):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for key, value in (
            ("user.email", "t15@example.invalid"), ("user.name", "Task 15")
        ):
            subprocess.run(
                ["git", "-C", str(self.root), "config", key, value], check=True
            )

        for name in ("source-manifest.schema.json", "build-receipt.schema.json"):
            self.copy_real("%s/schemas/%s" % (PROJECT_RELATIVE, name))
        self.copy_real("%s/.gitignore" % PROJECT_RELATIVE)
        for relative in GENERATOR_SOURCES:
            self.write(relative, "# 生成器源码替身 %s\n" % relative)
        for edition in EDITIONS:
            self.write(
                "%s/templates/%s.tex.tpl" % (PROJECT_RELATIVE, edition),
                "%% 模板 %s\n" % edition,
            )
        self.write("%s/index.json" % PROJECT_RELATIVE, "{}\n")
        self.write(
            ISSUES_TARGET,
            "# 高考数学 LaTeX 缺失与问题总账\n\n"
            "每个问题块使用稳定编号和可重算 fingerprint；已解决问题保留记录。\n\n",
        )

        self.papers = papers if papers is not None else [paper_entry()]
        for paper in self.papers:
            directory = paper["project_dir"]
            for edition in EDITIONS:
                self.write(
                    "%s/%s/%s.tex" % (PROJECT_RELATIVE, directory, edition),
                    "%% 壳 %s\n\\input{questions}\n" % edition,
                )
            for name in ("questions", "answers", "answers_short"):
                self.write(
                    "%s/%s/%s.tex" % (PROJECT_RELATIVE, directory, name),
                    "%% 内容 %s\n" % name,
                )
            for item in paper["figure_files"]:
                self.write("%s/%s" % (PROJECT_RELATIVE, item["path"]), "%% 图\n")
            for relative in paper["source_files"].values():
                self.write(relative, "# 规范源 %s\n" % relative)
        self.write("%s/common/preamble.tex" % PROJECT_RELATIVE, "%% 导言\n")

        self.manifest_path = self.root / MANIFEST_TARGET
        atomic_write_json(self.manifest_path, manifest_document(self.papers))
        self.issues_path = self.root / ISSUES_TARGET

        self.bin_dir = self.root / ".fake-bin"
        self.spec_path = self.root / ".fake-spec.json"
        fake_xelatex.write_spec(self.spec_path)
        fake_xelatex.write_shims(self.bin_dir, self.spec_path)
        if commit:
            self.commit_all("初始提交")

    # ------------------------------------------------------------ 基础操作

    def cleanup(self):
        self.temporary.cleanup()

    def copy_real(self, relative):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT.parent.parent.parent / relative, target)

    def write(self, relative, text):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def read(self, relative):
        return (self.root / relative).read_text(encoding="utf-8")

    def path(self, relative):
        return self.root / relative

    def git(self, *arguments):
        subprocess.run(["git", "-C", str(self.root)] + list(arguments), check=True)

    def commit_all(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def snapshot(self):
        """工作树快照。`.git` 与 `.fake-*`（替身工具的 spec / 调用计数）不算被测产物。"""
        recorded = {}
        for path in sorted(self.root.rglob("*")):
            relative = path.relative_to(self.root).as_posix()
            if ".git" in path.parts or not path.is_file():
                continue
            if relative.startswith(".fake"):
                continue
            recorded[relative] = file_sha256(path)
        return recorded

    # ------------------------------------------------------------ 工具链

    def spec(self, overrides):
        fake_xelatex.write_spec(self.spec_path, overrides)

    def toolchain(self, marker=""):
        if marker:
            fake_xelatex.write_shims(self.bin_dir, self.spec_path, marker=marker)
        return resolve_toolchain(search_path=str(self.bin_dir))

    def manifest(self):
        return load_manifest(self.manifest_path)

    def receipt_relative(self, project_dir=PROJECT_DIR):
        return "%s/%s/receipts/build.json" % (PROJECT_RELATIVE, project_dir)

    def receipt(self, project_dir=PROJECT_DIR):
        return json.loads(self.read(self.receipt_relative(project_dir)))

    def build(self, paper_id=PAPER_ID, **kwargs):
        return build_paper_result(
            self.root, self.manifest(), paper_id, self.toolchain(), **kwargs
        )

    def formal(self, selector="all", value=None, loader=None, **kwargs):
        return build_projects.run_formal(
            self.manifest_path, self.issues_path, selector, value,
            facts_loader=loader or make_loader(),
            toolchain=self.toolchain(), **kwargs
        )

    def cli(self, argv, loader=None):
        return build_projects.main(argv, facts_loader=loader)


# ================================================================ manifest 投影


class ProjectionTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.document = manifest_document([paper_entry()])

    def test_the_projected_field_set_is_frozen(self):
        self.assertEqual(
            PROJECTION_FIELDS,
            (
                "figure_files", "legacy_ids", "paper_id", "project_dir",
                "question_count", "source_files", "title", "track", "year",
            ),
        )
        projection = build_manifest_projection(self.document, PAPER_ID)
        self.assertEqual(tuple(sorted(projection)), PROJECTION_FIELDS)

    def test_runtime_fields_never_enter_the_projection(self):
        for field in (
            "production_state", "issue_ids", "blocked_from", "resume_action",
            "last_verified_hash", "source_ids", "legacy_source_files",
        ):
            self.assertNotIn(field, build_manifest_projection(self.document, PAPER_ID))

    def test_runtime_drift_does_not_change_the_digest(self):
        # 计划逐字点名的五类运行态：改了它们仍必须复用旧回执，否则每次状态推进都要重编 84 个目标。
        before = projection_digest(self.document, PAPER_ID)
        drifted = json.loads(json.dumps(self.document))
        drifted["revision"] = 99
        drifted["last_transaction_id"] = "11111111-2222-4333-8444-555555555555"
        drifted["batches"][0]["status"] = "compiled_pending_review"
        drifted["batches"][0]["issues"] = ["ISSUE-0007"]
        drifted["papers"][0]["production_state"] = "blocked"
        drifted["papers"][0]["issue_ids"] = ["ISSUE-0007"]
        drifted["papers"][0]["blocked_from"] = "compiled"
        drifted["papers"][0]["resume_action"] = "修源后重编"
        drifted["papers"][0]["last_verified_hash"] = "a" * 64
        self.assertEqual(projection_digest(drifted, PAPER_ID), before)

    def test_static_assembly_drift_changes_the_digest(self):
        before = projection_digest(self.document, PAPER_ID)
        for mutate in (
            lambda paper: paper.update(question_count=4),
            lambda paper: paper.update(title="改了标题"),
            lambda paper: paper.update(year=2100),
            lambda paper: paper.update(track="science"),
            lambda paper: paper.update(legacy_ids=["other"]),
            lambda paper: paper.update(project_dir="别的目录"),
            lambda paper: paper["source_files"].update(questions="x.md"),
            lambda paper: paper["figure_files"].append(
                {"expected_occurrences": 1, "path": "x/figures/f2.tex"}
            ),
        ):
            drifted = json.loads(json.dumps(self.document))
            mutate(drifted["papers"][0])
            self.assertNotEqual(projection_digest(drifted, PAPER_ID), before)

    def test_an_unknown_paper_fails_closed(self):
        with self.assertRaises(BuildError):
            build_manifest_projection(self.document, "gk-1900-regular-x")

    def test_the_digest_is_the_canonical_json_sha256(self):
        import hashlib

        projection = build_manifest_projection(self.document, PAPER_ID)
        self.assertEqual(
            projection_digest(self.document, PAPER_ID),
            hashlib.sha256(canonical_json(projection).encode("utf-8")).hexdigest(),
        )


# ================================================================ .fls 与日志


class FlsParserTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.project = self.fixture.root / PROJECT_RELATIVE / PROJECT_DIR

    def fls(self, *lines):
        return "PWD %s\n" % self.project + "".join(item + "\n" for item in lines)

    def test_relative_inputs_resolve_against_pwd(self):
        text = self.fls("INPUT questions.tex", "INPUT ../common/preamble.tex")
        self.assertEqual(
            parse_fls(text, self.fixture.root),
            (
                "%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR),
                "%s/common/preamble.tex" % PROJECT_RELATIVE,
            ),
        )

    def test_outputs_and_out_of_repo_inputs_are_dropped(self):
        text = self.fls(
            "INPUT /usr/local/texlive/tex/latex/base/article.cls",
            "OUTPUT build/解析版.pdf",
            "INPUT questions.tex",
        )
        self.assertEqual(
            parse_fls(text, self.fixture.root),
            ("%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR),),
        )

    def test_git_build_and_work_are_excluded(self):
        text = self.fls(
            "INPUT build/解析版.aux",
            "INPUT ../../../../.git/config",
            "INPUT ../.work/scratch.tex",
            "INPUT questions.tex",
        )
        self.assertEqual(
            parse_fls(text, self.fixture.root),
            ("%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR),),
        )

    def test_duplicates_collapse_and_order_is_stable(self):
        text = self.fls(
            "INPUT questions.tex", "INPUT answers.tex", "INPUT questions.tex",
            "INPUT ./questions.tex",
        )
        parsed = parse_fls(text, self.fixture.root)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(list(parsed), sorted(parsed))

    def test_a_missing_pwd_line_fails_closed(self):
        with self.assertRaises(BuildError):
            parse_fls("INPUT questions.tex\n", self.fixture.root)

    def test_the_dependency_tree_hashes_every_recorded_file(self):
        relative = "%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR)
        tree = dependency_tree(self.fixture.root, [relative])
        self.assertEqual(
            tree["files"],
            [{"path": relative, "sha256": file_sha256(self.fixture.path(relative))}],
        )
        self.fixture.write(relative, "%% 改了\n")
        self.assertNotEqual(
            dependency_tree(self.fixture.root, [relative])["tree_sha256"],
            tree["tree_sha256"],
        )

    def test_a_missing_dependency_fails_closed(self):
        with self.assertRaises(BuildError):
            dependency_tree(self.fixture.root, ["不存在.tex"])


class LogScannerTests(unittest.TestCase):
    def test_missing_characters_are_collected(self):
        text = (
            "Missing character: There is no 〇 (U+3007) in font [lmroman10-regular]!\n"
            "Missing character: There is no ㎡ (U+33A1) in font [lmroman10-regular]!\n"
        )
        found = scan_log(text)
        self.assertEqual(len(found["missing_characters"]), 2)
        self.assertIn("U+3007", found["missing_characters"][0]["text"])

    def test_undefined_references_are_collected(self):
        text = (
            "LaTeX Warning: Reference `q17' on page 3 undefined on input line 88.\n"
            "LaTeX Warning: There were undefined references.\n"
        )
        found = scan_log(text)
        self.assertEqual(len(found["undefined_references"]), 2)

    def test_a_hairline_overfull_is_still_recorded(self):
        # 0.4588pt 是本库真实存在的那一条：再小也只能候选 compiled_pending_review。
        text = (
            "Overfull \\hbox (0.4588pt too wide) in paragraph at lines 120--121\n"
            "Underfull \\vbox (badness 10000) has occurred while \\output is active\n"
        )
        found = scan_log(text)
        self.assertEqual(len(found["overfull"]), 2)
        first = found["overfull"][0]
        self.assertEqual(first["kind"], "Overfull")
        self.assertEqual(first["box"], "hbox")
        self.assertEqual(first["width_pt"], "0.4588")
        self.assertEqual(first["lines"], "120--121")
        self.assertEqual(found["overfull"][1]["width_pt"], None)

    def test_errors_are_collected_from_both_shapes(self):
        text = (
            "! Undefined control sequence.\n"
            "./解析版.tex:12: LaTeX Error: File `nope.sty' not found.\n"
        )
        found = scan_log(text)
        self.assertEqual(len(found["errors"]), 2)

    def test_a_clean_log_yields_four_empty_buckets(self):
        found = scan_log("This is XeTeX\nOutput written on x.pdf (2 pages).\n")
        self.assertEqual(
            sorted(found), ["errors", "missing_characters", "overfull", "undefined_references"]
        )
        self.assertEqual([item for bucket in found.values() for item in bucket], [])


# ================================================================ 工具链指纹


class ToolchainTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_all_four_tools_are_fingerprinted(self):
        fingerprint = self.fixture.toolchain()
        self.assertEqual(
            [item["name"] for item in fingerprint["tools"]],
            ["pdfinfo", "pdftoppm", "pdftotext", "xelatex"],
        )
        self.assertEqual(fingerprint["texlive_revision"], "TeX Live 2026")
        for item in fingerprint["tools"]:
            self.assertTrue(item["path"].startswith("/"))
            self.assertEqual(len(item["sha256"]), 64)

    def test_a_missing_tool_fails_closed(self):
        (self.fixture.bin_dir / "pdftoppm").unlink()
        with self.assertRaises(BuildError) as caught:
            self.fixture.toolchain()
        self.assertIn("pdftoppm", str(caught.exception))

    def test_an_unrecognisable_version_fails_closed(self):
        self.fixture.spec({"pdftotext": {"version_output": "\n"}})
        with self.assertRaises(BuildError):
            self.fixture.toolchain()

    def test_an_unrecognisable_texlive_revision_fails_closed(self):
        self.fixture.spec({"xelatex": {"version_output": "XeTeX unknown build\n"}})
        with self.assertRaises(BuildError):
            self.fixture.toolchain()

    def test_a_nonzero_version_exit_fails_closed(self):
        self.fixture.spec({"xelatex": {"version_exit": 3}})
        with self.assertRaises(BuildError):
            self.fixture.toolchain()

    def test_the_fingerprint_moves_with_version_path_and_bytes(self):
        base = self.fixture.toolchain()
        self.fixture.spec(
            {"pdfinfo": {"version_output": "pdfinfo version 99.99.99\n"}}
        )
        self.assertNotEqual(self.fixture.toolchain(), base)
        self.fixture.spec({"pdfinfo": {"version_output": "pdfinfo version 26.08.0\n"}})
        self.assertEqual(self.fixture.toolchain(), base)
        self.assertNotEqual(self.fixture.toolchain(marker="二进制变了"), base)

    def test_a_relocated_toolchain_changes_the_fingerprint(self):
        base = self.fixture.toolchain()
        moved = self.fixture.root / ".fake-bin-2"
        fake_xelatex.write_shims(moved, self.fixture.spec_path)
        self.assertNotEqual(resolve_toolchain(search_path=str(moved)), base)


# ================================================================ 单目标构建


class BuildTargetTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_a_clean_build_is_pending_review_not_succeeded(self):
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "compiled_pending_review")
        self.assertEqual(len(receipt["editions"]), 4)
        self.assertEqual(
            [item["edition"] for item in receipt["editions"]], list(EDITIONS)
        )
        for item in receipt["editions"]:
            self.assertEqual(item["result"], "succeeded")
            self.assertEqual([pass_["pass"] for pass_ in item["passes"]], [1, 2])
            self.assertEqual(item["pdf"]["page_count"], 2)
        validate_receipt(receipt)

    def test_the_frozen_argv_is_used_verbatim(self):
        recorded = []

        def spy(argv, **kwargs):
            recorded.append(argv)
            return subprocess.run(argv, **kwargs)

        self.fixture.build(runner=spy)
        first = recorded[0]
        self.assertTrue(first[0].endswith("xelatex"))
        self.assertEqual(first[1:], [
            "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
            "-no-shell-escape", "-recorder", "-output-directory=build",
            "试题版.tex",
        ])
        # 每个目标两遍，四版本共八次调用；pdfinfo 不走 xelatex 这条记录。
        self.assertEqual(len([item for item in recorded if item[-1].endswith(".tex")]), 8)

    def test_a_first_pass_failure_fails_the_paper(self):
        self.fixture.spec({"xelatex": {"passes": [{"exit_code": 1}, {"exit_code": 0}]}})
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "failed")
        self.assertEqual(receipt["editions"][0]["result"], "failed")
        self.assertEqual(receipt["editions"][0]["passes"][0]["exit_code"], 1)

    def test_a_second_pass_failure_fails_the_paper(self):
        self.fixture.spec({"xelatex": {"passes": [{"exit_code": 0}, {"exit_code": 1}]}})
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "failed")
        self.assertEqual(
            [item["exit_code"] for item in receipt["editions"][0]["passes"]], [0, 1]
        )

    def test_a_missing_pdf_fails_the_paper(self):
        self.fixture.spec({"xelatex": {"write_pdf": False}})
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "failed")
        self.assertIsNone(receipt["editions"][0]["pdf"])
        self.assertTrue(receipt["editions"][0]["problems"])

    def test_a_failing_pdfinfo_fails_the_paper(self):
        self.fixture.spec({"pdfinfo": {"exit_code": 1}})
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "failed")
        self.assertIsNone(receipt["editions"][0]["pdf"])

    def test_pdfinfo_without_a_page_count_fails_the_paper(self):
        self.fixture.spec({"pdfinfo": {"pages": None}})
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "failed")

    def test_warnings_are_recorded_but_do_not_fail_the_build(self):
        self.fixture.spec({"xelatex": {"log": (
            "Missing character: There is no 〇 (U+3007) in font [x]!\n"
            "LaTeX Warning: Reference `q3' on page 1 undefined on input line 9.\n"
            "Overfull \\hbox (0.4588pt too wide) in paragraph at lines 12--13\n"
        )}})
        receipt = self.fixture.build()
        self.assertEqual(receipt["status"], "compiled_pending_review")
        found = receipt["editions"][0]["log"]
        self.assertEqual(len(found["missing_characters"]), 1)
        self.assertEqual(len(found["undefined_references"]), 1)
        self.assertEqual(len(found["overfull"]), 1)

    def test_both_passes_contribute_to_the_dependency_union(self):
        self.fixture.spec({"xelatex": {"fls_by_pass": [
            ["INPUT questions.tex"],
            ["INPUT answers.tex", "INPUT ../common/preamble.tex"],
        ]}})
        receipt = self.fixture.build()
        recorded = [item["path"] for item in receipt["dependency_tree"]["files"]]
        for relative in (
            "%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR),
            "%s/%s/answers.tex" % (PROJECT_RELATIVE, PROJECT_DIR),
            "%s/common/preamble.tex" % PROJECT_RELATIVE,
        ):
            self.assertIn(relative, recorded)

    def test_the_generation_input_tree_covers_the_whole_chain(self):
        receipt = self.fixture.build()
        recorded = {item["path"] for item in receipt["generation_input_tree"]["files"]}
        expected = set(GENERATOR_SOURCES)
        expected.add("%s/index.json" % PROJECT_RELATIVE)
        expected.update(
            "%s/templates/%s.tex.tpl" % (PROJECT_RELATIVE, edition)
            for edition in EDITIONS
        )
        expected.update(
            "%s/%s/%s.tex" % (PROJECT_RELATIVE, PROJECT_DIR, edition)
            for edition in EDITIONS
        )
        expected.add("%s/%s/figures/f1.tex" % (PROJECT_RELATIVE, PROJECT_DIR))
        paper = paper_entry()
        for key in ("questions", "solution_body", "answer_key"):
            expected.add(paper["source_files"][key])
        self.assertEqual(recorded, expected)

    def test_the_build_directory_is_the_only_write_target(self):
        before = self.fixture.snapshot()
        self.fixture.build()
        after = self.fixture.snapshot()
        created = sorted(set(after) - set(before))
        self.assertTrue(created)
        for relative in created:
            self.assertIn("/%s/" % BUILD_DIR_NAME, relative)
        self.assertEqual(
            {key: before[key] for key in before},
            {key: after[key] for key in before},
        )


# ================================================================ 回执当前性


class ReceiptCurrencyTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.receipt = self.fixture.build()

    def currency(self, manifest=None, toolchain=None, receipt=None):
        return receipt_currency(
            self.fixture.root, manifest or self.fixture.manifest(),
            receipt or self.receipt, toolchain=toolchain,
        )

    def test_a_fresh_receipt_is_current(self):
        current, reasons = self.currency()
        self.assertTrue(current, reasons)
        self.assertEqual(reasons, [])

    def test_a_stale_pdf_is_not_green(self):
        # 「旧 PDF 不能假绿」：PDF 被换掉后回执立刻失效，哪怕文件还在原地。
        target = self.receipt["editions"][0]["pdf"]["path"]
        self.fixture.write(target, "%PDF-1.4 别的东西\n")
        current, reasons = self.currency()
        self.assertFalse(current)
        self.assertTrue(any("PDF" in item for item in reasons))

    def test_a_deleted_pdf_is_not_green(self):
        self.fixture.path(self.receipt["editions"][0]["pdf"]["path"]).unlink()
        self.assertFalse(self.currency()[0])

    def test_a_changed_dependency_makes_it_stale(self):
        self.fixture.write(
            "%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR), "%% 改了题面\n"
        )
        self.assertFalse(self.currency()[0])

    def test_a_changed_canonical_source_makes_it_stale(self):
        # 规范源已改但 TeX 尚未重跑——generation_input_tree 就是为这一格存在的。
        self.fixture.write(paper_entry()["source_files"]["questions"], "# 改了\n")
        self.assertFalse(self.currency()[0])

    def test_a_changed_generator_makes_it_stale(self):
        for relative in GENERATOR_SOURCES:
            with self.subTest(relative=relative):
                original = self.fixture.read(relative)
                self.fixture.write(relative, original + "# 改了\n")
                self.assertFalse(self.currency()[0])
                self.fixture.write(relative, original)
                self.assertTrue(self.currency()[0])

    def test_a_changed_projection_makes_it_stale(self):
        document = json.loads(json.dumps(manifest_document([paper_entry()])))
        document["papers"][0]["question_count"] = 4
        self.assertFalse(self.currency(manifest=document)[0])

    def test_manifest_runtime_drift_keeps_it_current(self):
        document = json.loads(json.dumps(manifest_document([paper_entry()])))
        document["revision"] = 42
        document["last_transaction_id"] = "11111111-2222-4333-8444-555555555555"
        document["batches"][0]["status"] = "compiled_pending_review"
        document["papers"][0]["production_state"] = "compiled"
        document["papers"][0]["issue_ids"] = ["ISSUE-0003"]
        current, reasons = self.currency(manifest=document)
        self.assertTrue(current, reasons)

    def test_every_tool_dimension_invalidates_the_receipt(self):
        base = self.fixture.toolchain()
        self.assertTrue(self.currency(toolchain=base)[0])
        for mutate in (
            lambda: self.fixture.spec(
                {"pdfinfo": {"version_output": "pdfinfo version 99.0.0\n"}}
            ),
            lambda: fake_xelatex.write_shims(
                self.fixture.bin_dir, self.fixture.spec_path, marker="换了二进制"
            ),
        ):
            mutate()
            current, reasons = self.currency(toolchain=self.fixture.toolchain())
            self.assertFalse(current)
            self.assertTrue(any("工具链" in item for item in reasons))
        moved = self.fixture.root / ".fake-bin-3"
        fake_xelatex.write_shims(moved, self.fixture.spec_path)
        self.assertFalse(
            self.currency(toolchain=resolve_toolchain(search_path=str(moved)))[0]
        )

    def test_a_running_receipt_can_never_be_current(self):
        running = build_projects.running_receipt(
            self.fixture.root, self.fixture.manifest(), PAPER_ID,
            self.fixture.toolchain(),
        )
        current, reasons = self.currency(receipt=running)
        self.assertFalse(current)
        self.assertTrue(any("running" in item for item in reasons))


# ================================================================ 状态机


class StateMachineTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_the_transition_table_matches_the_frozen_schema(self):
        schema = json.loads(
            (ROOT / "schemas" / "build-receipt.schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [list(item) for item in STATUS_TRANSITIONS],
            schema["$defs"]["status_transitions"]["const"],
        )
        self.assertEqual(
            STATUS_TRANSITIONS,
            (
                ("running", "failed"),
                ("running", "compiled_pending_review"),
                ("compiled_pending_review", "succeeded"),
            ),
        )

    def test_a_new_attempt_may_always_restart_at_running(self):
        old = build_projects.running_receipt(
            self.fixture.root, self.fixture.manifest(), PAPER_ID,
            self.fixture.toolchain(),
        )
        fresh = dict(old, attempt_id="11111111-2222-4333-8444-555555555555")
        assert_transition(old, fresh)

    def test_illegal_transitions_are_refused(self):
        old = build_projects.running_receipt(
            self.fixture.root, self.fixture.manifest(), PAPER_ID,
            self.fixture.toolchain(),
        )
        for target in ("succeeded", "running"):
            with self.assertRaises(BuildError):
                assert_transition(old, dict(old, status=target))
        failed = dict(old, status="failed")
        for target in ("succeeded", "compiled_pending_review"):
            with self.assertRaises(BuildError):
                assert_transition(failed, dict(failed, status=target))


class FinalizeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.fixture.spec({"xelatex": {"log": (
            "Overfull \\hbox (0.4588pt too wide) in paragraph at lines 12--13\n"
        )}})
        self.build = self.fixture.build()

    def review(self, **overrides):
        record = {
            "paper_id": self.build["paper_id"],
            "status": "passed",
            "build_attempt_id": self.build["attempt_id"],
            "input_projection": self.build["input_projection"],
            "generation_input_tree_sha256":
                self.build["generation_input_tree"]["tree_sha256"],
            "dependency_tree_sha256": self.build["dependency_tree"]["tree_sha256"],
            "toolchain_fingerprint": self.build["toolchain_fingerprint"],
            "editions": [
                {
                    "edition": item["edition"],
                    "pdf_sha256": item["pdf"]["sha256"],
                    "page_count": item["pdf"]["page_count"],
                }
                for item in self.build["editions"]
            ],
            "warning_exemptions": [
                {
                    "edition": item["edition"],
                    "kind": warning["kind"],
                    "box": warning["box"],
                    "width_pt": warning["width_pt"],
                    "lines": warning["lines"],
                    "reason": "版心内可接受",
                }
                for item in self.build["editions"]
                for warning in item["log"]["overfull"]
            ],
        }
        record.update(overrides)
        return record

    def test_a_matching_review_promotes_the_receipt(self):
        finalized = finalize_receipt(self.build, self.review())
        self.assertEqual(finalized["status"], "succeeded")
        self.assertEqual(finalized["attempt_id"], self.build["attempt_id"])
        self.assertEqual(self.build["status"], "compiled_pending_review")
        validate_receipt(finalized)

    def test_finalize_writes_nothing(self):
        before = self.fixture.snapshot()
        finalize_receipt(self.build, self.review())
        self.assertEqual(self.fixture.snapshot(), before)

    def test_a_running_receipt_can_never_be_finalized(self):
        running = build_projects.running_receipt(
            self.fixture.root, self.fixture.manifest(), PAPER_ID,
            self.fixture.toolchain(),
        )
        with self.assertRaises(BuildError):
            finalize_receipt(running, self.review())

    def test_a_failed_review_is_not_a_failed_build(self):
        with self.assertRaises(BuildError):
            finalize_receipt(self.build, self.review(status="failed"))
        self.assertEqual(self.build["status"], "compiled_pending_review")

    def test_every_binding_is_checked_item_by_item(self):
        for field, value in (
            ("build_attempt_id", "11111111-2222-4333-8444-555555555555"),
            ("input_projection", "b" * 64),
            ("generation_input_tree_sha256", "c" * 64),
            ("dependency_tree_sha256", "d" * 64),
            ("paper_id", OTHER_ID),
        ):
            with self.subTest(field=field):
                with self.assertRaises(BuildError):
                    finalize_receipt(self.build, self.review(**{field: value}))

    def test_a_mismatched_pdf_hash_refuses_promotion(self):
        review = self.review()
        review["editions"][0]["pdf_sha256"] = "e" * 64
        with self.assertRaises(BuildError):
            finalize_receipt(self.build, review)

    def test_a_missing_edition_refuses_promotion(self):
        review = self.review()
        del review["editions"][0]
        with self.assertRaises(BuildError):
            finalize_receipt(self.build, review)

    def test_warning_exemptions_must_match_the_warning_set_item_by_item(self):
        with self.assertRaises(BuildError):
            finalize_receipt(self.build, self.review(warning_exemptions=[]))
        extra = self.review()
        extra["warning_exemptions"].append(
            dict(extra["warning_exemptions"][0], width_pt="9.9")
        )
        with self.assertRaises(BuildError):
            finalize_receipt(self.build, extra)

    def test_a_changed_toolchain_refuses_promotion(self):
        other = json.loads(json.dumps(self.build["toolchain_fingerprint"]))
        other["tools"][0]["sha256"] = "f" * 64
        with self.assertRaises(BuildError):
            finalize_receipt(self.build, self.review(toolchain_fingerprint=other))


# ================================================================ formal 两阶段


class FormalBuildTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture(
            papers=[paper_entry(), paper_entry(OTHER_ID, OTHER_DIR, "legacy2099b")]
        )
        self.addCleanup(self.fixture.cleanup)

    def test_the_running_transaction_lands_before_any_compilation(self):
        seen = {}

        def builder(*arguments, **keywords):
            seen["receipt"] = self.fixture.receipt()
            seen["revision"] = self.fixture.manifest()["revision"]
            return build_paper_result(*arguments, **keywords)

        report = self.fixture.formal(builder=builder)
        self.assertEqual(seen["receipt"]["status"], "running")
        self.assertIsNone(seen["receipt"]["dependency_tree"])
        self.assertEqual(seen["receipt"]["editions"], [])
        self.assertEqual(seen["revision"], 2)
        self.assertEqual(report["code"], "COMPILED_PENDING_REVIEW")
        self.assertEqual(self.fixture.manifest()["revision"], 3)

    def test_an_interrupted_build_stays_running_and_is_never_final(self):
        def explode(*arguments, **keywords):
            raise KeyboardInterrupt("模拟中断")

        with self.assertRaises(KeyboardInterrupt):
            self.fixture.formal(builder=explode)
        receipt = self.fixture.receipt()
        self.assertEqual(receipt["status"], "running")
        self.assertEqual(self.fixture.manifest()["revision"], 2)
        report = build_projects.validate_receipts(
            self.fixture.manifest_path, "all", None, require_final=True
        )
        self.assertEqual(report["code"], "INVALID")
        self.assertEqual(report["running"], 2)

    def test_a_rerun_with_identical_inputs_reuses_the_attempt(self):
        def explode(*arguments, **keywords):
            raise KeyboardInterrupt("模拟中断")

        with self.assertRaises(KeyboardInterrupt):
            self.fixture.formal(builder=explode)
        interrupted = self.fixture.receipt()["attempt_id"]
        self.fixture.formal()
        resumed = self.fixture.receipt()
        self.assertEqual(resumed["attempt_id"], interrupted)
        self.assertIsNone(resumed["previous_attempt_id"])
        self.assertEqual(resumed["status"], "compiled_pending_review")

    def test_a_rerun_with_changed_inputs_replaces_the_attempt(self):
        def explode(*arguments, **keywords):
            raise KeyboardInterrupt("模拟中断")

        with self.assertRaises(KeyboardInterrupt):
            self.fixture.formal(builder=explode)
        interrupted = self.fixture.receipt()["attempt_id"]
        self.fixture.write(paper_entry()["source_files"]["questions"], "# 改了源\n")
        self.fixture.formal()
        resumed = self.fixture.receipt()
        self.assertNotEqual(resumed["attempt_id"], interrupted)
        self.assertEqual(resumed["previous_attempt_id"], interrupted)

    def test_a_successful_run_reconciles_papers_and_batches(self):
        report = self.fixture.formal()
        self.assertEqual(report["pending"], 2)
        self.assertEqual(report["failed"], 0)
        manifest = self.fixture.manifest()
        for paper in manifest["papers"]:
            self.assertEqual(paper["production_state"], "compiled")
        self.assertEqual(manifest["batches"][0]["status"], "compiled_pending_review")
        for directory in (PROJECT_DIR, OTHER_DIR):
            self.assertEqual(
                self.fixture.receipt(directory)["status"], "compiled_pending_review"
            )

    def test_stale_provenance_refuses_to_start(self):
        loader = make_loader(loaded_facts(provenance="stale"))
        before = self.fixture.snapshot()
        with self.assertRaises(BuildError):
            self.fixture.formal(loader=loader)
        self.assertEqual(self.fixture.snapshot(), before)

    def test_a_loader_that_supplies_build_facts_is_refused(self):
        loader = make_loader(loaded_facts(build="succeeded"))
        with self.assertRaises(BuildError):
            self.fixture.formal(loader=loader)

    def test_a_failed_target_upserts_a_formal_build_issue_and_blocks_the_paper(self):
        self.fixture.spec({"xelatex": {"passes": [{"exit_code": 1}, {"exit_code": 0}]}})
        report = self.fixture.formal(selector="paper", value=PAPER_ID)
        self.assertEqual(report["code"], "BUILD_FAILED")
        self.assertEqual(report["failed"], 1)

        import issues as issues_module

        recorded = issues_module.load_issues(self.fixture.issues_path)
        compile_errors = [
            item for item in recorded
            if item["type"] == "compile-error" and item.get("origin") == "formal-build"
        ]
        self.assertEqual(len(compile_errors), 4)
        self.assertEqual({item["status"] for item in compile_errors}, {"open"})
        self.assertEqual(
            {item["edition"] for item in compile_errors}, set(EDITIONS)
        )

        paper = self.fixture.manifest()["papers"][0]
        self.assertEqual(paper["production_state"], "blocked")
        self.assertTrue(paper["issue_ids"])
        self.assertTrue(paper["resume_action"])
        # running 事务已经把它推到 editions_generated，失败正是从那一格被 block 的。
        self.assertEqual(paper["blocked_from"], "editions_generated")
        self.assertEqual(
            self.fixture.manifest()["batches"][0]["status"], "provenance_verified"
        )

    def test_a_later_success_resolves_the_old_attempt_issues(self):
        self.fixture.spec({"xelatex": {"passes": [{"exit_code": 1}, {"exit_code": 0}]}})
        self.fixture.formal(selector="paper", value=PAPER_ID)
        self.fixture.spec({"xelatex": {"passes": [{"exit_code": 0}, {"exit_code": 0}]}})
        report = self.fixture.formal(selector="paper", value=PAPER_ID)
        self.assertEqual(report["code"], "COMPILED_PENDING_REVIEW")

        import issues as issues_module

        recorded = issues_module.load_issues(self.fixture.issues_path)
        compile_errors = [
            item for item in recorded
            if item["type"] == "compile-error" and item.get("origin") == "formal-build"
        ]
        self.assertEqual(len(compile_errors), 4)
        self.assertEqual({item["status"] for item in compile_errors}, {"resolved"})
        self.assertEqual(
            self.fixture.manifest()["papers"][0]["production_state"], "compiled"
        )

    def test_a_partial_failure_still_builds_the_rest(self):
        original = build_projects.build_paper_result

        def builder(root, manifest, paper_id, toolchain, **keywords):
            receipt = original(root, manifest, paper_id, toolchain, **keywords)
            if paper_id == PAPER_ID:
                receipt["status"] = "failed"
                receipt["editions"][0]["result"] = "failed"
                receipt["editions"][0]["problems"] = ["注入的失败"]
            return receipt

        report = self.fixture.formal(builder=builder)
        self.assertEqual(report["code"], "BUILD_FAILED")
        self.assertEqual(report["failed"], 1)
        self.assertEqual(report["pending"], 1)
        self.assertEqual(self.fixture.receipt(PROJECT_DIR)["status"], "failed")
        self.assertEqual(
            self.fixture.receipt(OTHER_DIR)["status"], "compiled_pending_review"
        )
        self.assertEqual(
            self.fixture.manifest()["batches"][0]["status"], "provenance_verified"
        )

    def test_the_result_transaction_is_atomic_across_receipts_and_manifest(self):
        pending = self.fixture.root / PROJECT_RELATIVE / ".work" / "transactions"
        self.fixture.formal()
        self.assertEqual(
            sorted(item.name for item in pending.iterdir()) if pending.is_dir() else [],
            [],
        )
        self.assertEqual(
            self.fixture.manifest()["last_transaction_id"] is not None, True
        )


# ================================================================ 位置参数 smoke


class SmokeModeTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_positional_mode_writes_no_formal_receipt(self):
        before_manifest = self.fixture.read(MANIFEST_TARGET)
        code = build_projects.main(
            ["build", PROJECT_DIR, "解析版", "--manifest", str(self.fixture.manifest_path)],
            search_path=str(self.fixture.bin_dir),
        )
        self.assertEqual(code, EXIT_OK)
        self.assertFalse(
            self.fixture.path("%s/%s/receipts" % (PROJECT_RELATIVE, PROJECT_DIR)).exists()
        )
        self.assertEqual(self.fixture.read(MANIFEST_TARGET), before_manifest)
        diagnostics = self.fixture.path(
            "%s/%s/%s/解析版.diagnostics.json" % (PROJECT_RELATIVE, PROJECT_DIR, BUILD_DIR_NAME)
        )
        self.assertTrue(diagnostics.is_file())
        payload = json.loads(diagnostics.read_text(encoding="utf-8"))
        self.assertEqual(payload["edition"], "解析版")
        self.assertEqual(payload["result"], "succeeded")

    def test_positional_mode_without_an_edition_builds_all_four(self):
        code = build_projects.main(
            ["build", PROJECT_DIR, "--manifest", str(self.fixture.manifest_path)],
            search_path=str(self.fixture.bin_dir),
        )
        self.assertEqual(code, EXIT_OK)
        for edition in EDITIONS:
            self.assertTrue(self.fixture.path(
                "%s/%s/%s/%s.pdf" % (PROJECT_RELATIVE, PROJECT_DIR, BUILD_DIR_NAME, edition)
            ).is_file())

    def test_a_failing_smoke_returns_the_build_failed_code(self):
        self.fixture.spec({"xelatex": {"write_pdf": False}})
        code = build_projects.main(
            ["build", PROJECT_DIR, "解析版", "--manifest", str(self.fixture.manifest_path)],
            search_path=str(self.fixture.bin_dir),
        )
        self.assertEqual(code, EXIT_BUILD_FAILED)

    def test_an_unknown_project_directory_is_usage(self):
        code = build_projects.main(
            ["build", "不存在的目录", "--manifest", str(self.fixture.manifest_path)],
            search_path=str(self.fixture.bin_dir),
        )
        self.assertEqual(code, EXIT_USAGE)


# ================================================================ 清理门禁


class CleanBuildTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        self.fixture.build()
        self.build_dir = self.fixture.path(
            "%s/%s/%s" % (PROJECT_RELATIVE, PROJECT_DIR, BUILD_DIR_NAME)
        )

    def plan(self, execute=False):
        return clean_build(
            self.fixture.root, self.fixture.manifest(), [PAPER_ID], execute=execute
        )

    def test_dry_run_and_execute_enumerate_the_same_targets(self):
        dry = self.plan()
        self.assertEqual(dry["targets"], [
            "%s/%s/%s" % (PROJECT_RELATIVE, PROJECT_DIR, BUILD_DIR_NAME)
        ])
        self.assertTrue(self.build_dir.is_dir())
        run = self.plan(execute=True)
        self.assertEqual(run["targets"], dry["targets"])
        self.assertFalse(self.build_dir.exists())

    def test_a_symlinked_build_directory_deletes_nothing(self):
        shutil.rmtree(self.build_dir)
        outside = self.fixture.root / "outside"
        outside.mkdir()
        self.build_dir.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(BuildError):
            self.plan(execute=True)
        self.assertTrue(self.build_dir.is_symlink())
        self.assertTrue(outside.is_dir())

    def test_tracked_content_inside_build_deletes_nothing(self):
        self.fixture.write(
            "%s/%s/%s/keep.txt" % (PROJECT_RELATIVE, PROJECT_DIR, BUILD_DIR_NAME), "x\n"
        )
        self.fixture.git("add", "-f",
                         "%s/%s/%s/keep.txt" % (PROJECT_RELATIVE, PROJECT_DIR, BUILD_DIR_NAME))
        self.fixture.git("commit", "-q", "-m", "误入库")
        with self.assertRaises(BuildError) as caught:
            self.plan(execute=True)
        self.assertIn("tracked", str(caught.exception))
        self.assertTrue(self.build_dir.is_dir())

    def test_an_unignored_build_directory_deletes_nothing(self):
        self.fixture.write("%s/.gitignore" % PROJECT_RELATIVE, "# 什么都不忽略\n")
        with self.assertRaises(BuildError):
            self.plan(execute=True)
        self.assertTrue(self.build_dir.is_dir())

    def test_a_project_directory_escaping_the_repo_deletes_nothing(self):
        document = json.loads(json.dumps(manifest_document([paper_entry()])))
        document["papers"][0]["project_dir"] = ".."
        with self.assertRaises(BuildError):
            clean_build(self.fixture.root, document, [PAPER_ID], execute=True)
        self.assertTrue(self.build_dir.is_dir())

    def test_a_missing_build_directory_is_not_an_error(self):
        shutil.rmtree(self.build_dir)
        report = self.plan(execute=True)
        self.assertEqual(report["removed"], [])
        self.assertEqual(report["targets"], [])


class CleanupLegacyTests(unittest.TestCase):
    LEGACY_SUFFIXES = (
        ".pdf", ".log", ".aux", ".out", ".toc", ".fls", ".xdv", ".synctex.gz"
    )

    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)
        for edition in EDITIONS:
            for suffix in self.LEGACY_SUFFIXES:
                self.fixture.write(
                    "%s/%s/%s%s" % (PROJECT_RELATIVE, PROJECT_DIR, edition, suffix),
                    "旧产物\n",
                )

    def prepare(self, build_status="succeeded", review="passed", provenance=True):
        receipt = self.fixture.build()
        if build_status == "succeeded":
            receipt = dict(receipt, status="succeeded")
        elif build_status != "compiled_pending_review":
            receipt = dict(receipt, status=build_status)
        atomic_write_json(
            self.fixture.path(self.fixture.receipt_relative()), receipt
        )
        # 逐档准备时必须**删掉**不该存在的那一份：同一夹具跑多个 subTest，留下上一档
        # 写的文件会让「缺 provenance」这一档静默变成「什么都不缺」。
        review_path = self.fixture.path(
            "%s/%s/receipts/review.json" % (PROJECT_RELATIVE, PROJECT_DIR)
        )
        provenance_path = self.fixture.path(
            "%s/%s/provenance.json" % (PROJECT_RELATIVE, PROJECT_DIR)
        )
        if review is not None:
            atomic_write_json(review_path, {"paper_id": PAPER_ID, "status": review})
        elif review_path.exists():
            review_path.unlink()
        if provenance:
            atomic_write_json(provenance_path, {"paper_id": PAPER_ID})
        elif provenance_path.exists():
            provenance_path.unlink()
        return receipt

    def legacy_paths(self):
        return [
            "%s/%s/%s%s" % (PROJECT_RELATIVE, PROJECT_DIR, edition, suffix)
            for edition in EDITIONS for suffix in self.LEGACY_SUFFIXES
        ]

    def test_a_complete_evidence_chain_removes_exactly_the_legacy_artifacts(self):
        self.prepare()
        before = self.fixture.snapshot()
        report = cleanup_legacy(self.fixture.root, self.fixture.manifest(), execute=True)
        self.assertEqual(sorted(report["removed"]), sorted(self.legacy_paths()))
        after = self.fixture.snapshot()
        self.assertEqual(sorted(set(before) - set(after)), sorted(self.legacy_paths()))

    def test_a_missing_receipt_removes_nothing(self):
        before = self.fixture.snapshot()
        with self.assertRaises(BuildError):
            cleanup_legacy(self.fixture.root, self.fixture.manifest(), execute=True)
        self.assertEqual(self.fixture.snapshot(), before)

    def test_a_failed_running_or_pending_receipt_removes_nothing(self):
        for build_status in ("failed", "running", "compiled_pending_review"):
            with self.subTest(build_status=build_status):
                self.prepare(build_status=build_status)
                before = self.fixture.snapshot()
                with self.assertRaises(BuildError):
                    cleanup_legacy(
                        self.fixture.root, self.fixture.manifest(), execute=True
                    )
                self.assertEqual(self.fixture.snapshot(), before)

    def test_a_stale_receipt_removes_nothing(self):
        self.prepare()
        self.fixture.write(
            "%s/%s/questions.tex" % (PROJECT_RELATIVE, PROJECT_DIR), "%% 改了\n"
        )
        before = self.fixture.snapshot()
        with self.assertRaises(BuildError):
            cleanup_legacy(self.fixture.root, self.fixture.manifest(), execute=True)
        self.assertEqual(self.fixture.snapshot(), before)

    def test_a_missing_review_or_provenance_removes_nothing(self):
        for keywords in ({"review": None}, {"provenance": False}, {"review": "pending"}):
            with self.subTest(keywords=keywords):
                self.prepare(**keywords)
                before = self.fixture.snapshot()
                with self.assertRaises(BuildError):
                    cleanup_legacy(
                        self.fixture.root, self.fixture.manifest(), execute=True
                    )
                self.assertEqual(self.fixture.snapshot(), before)

    def test_dry_run_never_touches_the_disk(self):
        self.prepare()
        before = self.fixture.snapshot()
        report = cleanup_legacy(self.fixture.root, self.fixture.manifest())
        self.assertEqual(sorted(report["targets"]), sorted(self.legacy_paths()))
        self.assertEqual(report["removed"], [])
        self.assertEqual(self.fixture.snapshot(), before)

    def test_a_symlinked_legacy_artifact_removes_nothing(self):
        self.prepare()
        target = self.fixture.path(
            "%s/%s/解析版.pdf" % (PROJECT_RELATIVE, PROJECT_DIR)
        )
        target.unlink()
        target.symlink_to(self.fixture.path("%s/index.json" % PROJECT_RELATIVE))
        before = self.fixture.snapshot()
        with self.assertRaises(BuildError):
            cleanup_legacy(self.fixture.root, self.fixture.manifest(), execute=True)
        self.assertEqual(self.fixture.snapshot(), before)

    def test_a_tracked_legacy_artifact_removes_nothing(self):
        self.prepare()
        self.fixture.git(
            "add", "-f", "%s/%s/解析版.pdf" % (PROJECT_RELATIVE, PROJECT_DIR)
        )
        self.fixture.git("commit", "-q", "-m", "误入库的旧 PDF")
        before = self.fixture.snapshot()
        with self.assertRaises(BuildError):
            cleanup_legacy(self.fixture.root, self.fixture.manifest(), execute=True)
        self.assertEqual(self.fixture.snapshot(), before)


# ================================================================ CLI 面


class CommandLineTests(unittest.TestCase):
    def setUp(self):
        self.fixture = RepositoryFixture()
        self.addCleanup(self.fixture.cleanup)

    def cli(self, *arguments, **keywords):
        keywords.setdefault("search_path", str(self.fixture.bin_dir))
        return build_projects.main(list(arguments), **keywords)

    def capture(self, *arguments, **keywords):
        import io
        import contextlib

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = self.cli(*arguments, **keywords)
        return code, buffer.getvalue()

    def test_check_tools_reports_all_four(self):
        code, output = self.capture("check-tools", "--json")
        self.assertEqual(code, EXIT_OK)
        payload = json.loads(output)
        self.assertEqual(payload["code"], "OK")
        self.assertEqual(len(payload["toolchain"]["tools"]), 4)

    def test_check_tools_fails_closed_when_a_tool_is_missing(self):
        (self.fixture.bin_dir / "pdfinfo").unlink()
        code, output = self.capture("check-tools", "--json")
        self.assertEqual(code, EXIT_INVALID)
        self.assertEqual(json.loads(output)["code"], "INVALID")

    def test_selectors_are_mutually_exclusive(self):
        for arguments in (
            ("validate-receipts", "--manifest", "m", "--all", "--paper", PAPER_ID),
            ("validate-receipts", "--manifest", "m", "--batch", BATCH_ID, "--all"),
            ("clean-build", "--manifest", "m", "--all", "--dry-run", "--execute"),
            ("cleanup-legacy", "--manifest", "m"),
            ("validate-receipts", "--manifest", "m"),
            ("clean-build", "--manifest", "m", "--all"),
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaises(SystemExit) as caught:
                    build_projects.main(list(arguments))
                self.assertEqual(caught.exception.code, EXIT_USAGE)

    def test_formal_and_positional_modes_are_mutually_exclusive(self):
        with self.assertRaises(SystemExit) as caught:
            build_projects.main(
                ["build", PROJECT_DIR, "--formal", "--all", "--manifest", "m"]
            )
        self.assertEqual(caught.exception.code, EXIT_USAGE)

    def test_validate_receipts_pending_review_uses_its_own_exit_code(self):
        build_projects.run_formal(
            self.fixture.manifest_path, self.fixture.issues_path, "all", None,
            facts_loader=make_loader(), toolchain=self.fixture.toolchain(),
        )
        code, output = self.capture(
            "validate-receipts", "--manifest", str(self.fixture.manifest_path),
            "--all", "--require-final", "--json",
        )
        self.assertEqual(code, EXIT_PENDING_REVIEW)
        payload = json.loads(output)
        self.assertEqual(payload["code"], "PENDING_REVIEW")
        self.assertEqual(payload["pending"], 1)
        self.assertEqual(payload["failed"], 0)
        self.assertEqual(payload["stale"], 0)
        self.assertEqual(payload["running"], 0)

        code, output = self.capture(
            "validate-receipts", "--manifest", str(self.fixture.manifest_path),
            "--all", "--json",
        )
        self.assertEqual(code, EXIT_OK)
        self.assertEqual(json.loads(output)["code"], "OK")

    def test_validate_receipts_separates_failure_from_pending(self):
        self.fixture.spec({"xelatex": {"write_pdf": False}})
        try:
            build_projects.run_formal(
                self.fixture.manifest_path, self.fixture.issues_path, "all", None,
                facts_loader=make_loader(), toolchain=self.fixture.toolchain(),
            )
        except BuildError:
            pass
        code, output = self.capture(
            "validate-receipts", "--manifest", str(self.fixture.manifest_path),
            "--all", "--require-final", "--json",
        )
        self.assertEqual(code, EXIT_INVALID)
        payload = json.loads(output)
        self.assertEqual(payload["code"], "INVALID")
        self.assertEqual(payload["failed"], 1)
        self.assertEqual(payload["pending"], 0)

    def test_a_missing_receipt_is_invalid_not_pending(self):
        code, output = self.capture(
            "validate-receipts", "--manifest", str(self.fixture.manifest_path),
            "--all", "--json",
        )
        self.assertEqual(code, EXIT_INVALID)
        self.assertEqual(json.loads(output)["missing"], 1)

    def test_stale_inputs_require_the_opt_in_toolchain_check(self):
        build_projects.run_formal(
            self.fixture.manifest_path, self.fixture.issues_path, "all", None,
            facts_loader=make_loader(), toolchain=self.fixture.toolchain(),
        )
        fake_xelatex.write_shims(
            self.fixture.bin_dir, self.fixture.spec_path, marker="新二进制"
        )
        code, _ = self.capture(
            "validate-receipts", "--manifest", str(self.fixture.manifest_path),
            "--all", "--json",
        )
        self.assertEqual(code, EXIT_OK)
        code, output = self.capture(
            "validate-receipts", "--manifest", str(self.fixture.manifest_path),
            "--all", "--require-current-inputs", "--json",
        )
        self.assertEqual(code, EXIT_INVALID)
        self.assertEqual(json.loads(output)["stale"], 1)

    def test_output_paths_emits_nul_separated_ownership(self):
        import io
        import contextlib

        buffer = io.BytesIO()

        class Wrapper:
            def __init__(self, target):
                self.buffer = target

            def write(self, text):
                self.buffer.write(text.encode("utf-8"))

            def flush(self):
                pass

        wrapper = Wrapper(buffer)
        with contextlib.redirect_stdout(wrapper):
            code = self.cli(
                "output-paths", "--manifest", str(self.fixture.manifest_path),
                "--issues", str(self.fixture.issues_path), "--all",
                "--include-state", "--nul",
            )
        self.assertEqual(code, EXIT_OK)
        entries = [item for item in buffer.getvalue().split(b"\0") if item]
        self.assertEqual(
            [item.decode("utf-8") for item in entries],
            [
                "%s/%s/receipts/build.json" % (PROJECT_RELATIVE, PROJECT_DIR),
                MANIFEST_TARGET,
                ISSUES_TARGET,
            ],
        )

    def test_output_paths_without_include_state_lists_receipts_only(self):
        import io
        import contextlib

        buffer = io.BytesIO()

        class Wrapper:
            def __init__(self, target):
                self.buffer = target

            def write(self, text):
                self.buffer.write(text.encode("utf-8"))

            def flush(self):
                pass

        with contextlib.redirect_stdout(Wrapper(buffer)):
            self.cli(
                "output-paths", "--manifest", str(self.fixture.manifest_path),
                "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID, "--nul",
            )
        entries = [item for item in buffer.getvalue().split(b"\0") if item]
        self.assertEqual(len(entries), 1)

    def test_check_staged_accepts_exactly_the_ownership_range(self):
        # check-staged 没有 --manifest，仓库根按 cwd 解析（与 solution_sources 同语义）。
        origin = os.getcwd()
        os.chdir(str(self.fixture.root))
        self.addCleanup(os.chdir, origin)
        build_projects.run_formal(
            self.fixture.manifest_path, self.fixture.issues_path, "all", None,
            facts_loader=make_loader(), toolchain=self.fixture.toolchain(),
        )
        pathspec = self.fixture.root / "paths.nul"
        paths = [
            "%s/%s/receipts/build.json" % (PROJECT_RELATIVE, PROJECT_DIR),
            MANIFEST_TARGET,
            ISSUES_TARGET,
        ]
        pathspec.write_bytes(b"".join(item.encode("utf-8") + b"\0" for item in paths))
        self.fixture.git("add", "--", *paths)
        self.assertEqual(
            self.cli("check-staged", "--pathspec-file", str(pathspec), "--nul"),
            EXIT_OK,
        )
        self.fixture.write("%s/index.json" % PROJECT_RELATIVE, '{"夹带": true}\n')
        self.fixture.git("add", "%s/index.json" % PROJECT_RELATIVE)
        self.assertEqual(
            self.cli("check-staged", "--pathspec-file", str(pathspec), "--nul"),
            EXIT_INVALID,
        )


# ================================================================ Bash 包装


class ShellWrapperTests(unittest.TestCase):
    def setUp(self):
        self.compile_sh = ROOT / "compile.sh"
        self.compile_all = ROOT / "compile_all.sh"

    def test_both_wrappers_are_executable(self):
        for script in (self.compile_sh, self.compile_all):
            self.assertTrue(script.is_file(), script)
            self.assertTrue(os.access(str(script), os.X_OK), script)
            self.assertTrue(
                stat.S_IMODE(script.stat().st_mode) & stat.S_IXUSR, script
            )

    def test_both_wrappers_parse_under_bash(self):
        for script in (self.compile_sh, self.compile_all):
            result = subprocess.run(
                ["/bin/bash", "-n", str(script)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_compile_sh_only_delegates(self):
        text = self.compile_sh.read_text(encoding="utf-8")
        self.assertIn("tools/build_projects.py", text)
        self.assertIn("exec", text)
        for forbidden in ("xelatex", "grep -q", "EDITIONS="):
            self.assertNotIn(forbidden, text)

    def test_compile_all_delegates_to_the_formal_all_mode(self):
        text = self.compile_all.read_text(encoding="utf-8")
        self.assertIn("compile.sh", text)
        self.assertIn("--formal", text)
        self.assertIn("--all", text)
        self.assertIn('"$@"', text)

    def test_the_ignore_rules_cover_build_products_but_not_receipts(self):
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        for rule in (".work/", "*/build/", "*.fls", "*.xdv"):
            self.assertIn(rule, text.split("\n"), rule)
        self.assertNotIn("receipts/", text)


if __name__ == "__main__":
    unittest.main()

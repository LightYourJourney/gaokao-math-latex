#!/usr/bin/env python3
"""Task 24 第一原子段：视觉回执基础契约。"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

PROJECT = Path(__file__).resolve().parents[1]
TOOLS = PROJECT / "tools"
TESTS = PROJECT / "tests"
for directory in (TOOLS, TESTS):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import review_receipts as subject
import test_build_projects as build_tests
from manifest import atomic_write_json, canonical_json, file_sha256, load_manifest
from transaction import Transaction, recover_transactions


SHA_A = "a" * 64
SHA_B = "b" * 64
ATTEMPT = "12345678-1234-4123-8123-123456789abc"


def tool(name: str) -> dict:
    return {
        "name": name,
        "path": f"/usr/bin/{name}",
        "real_path": f"/usr/bin/{name}",
        "sha256": SHA_A,
        "version": f"{name} 1.0",
    }


def toolchain() -> dict:
    return {
        "texlive_revision": "2026",
        "tools": [tool(name) for name in ("xelatex", "pdfinfo", "pdftotext", "pdftoppm")],
    }


def visual() -> dict:
    tools = {item["name"]: item for item in toolchain()["tools"]}
    return {"tools": [copy.deepcopy(tools[name]) for name in subject.VISUAL_TOOL_NAMES]}


def checks(*, not_applicable: str | None = None) -> list[dict]:
    records = []
    for code in subject.CHECK_CODES:
        result = "not_applicable" if code == not_applicable else "pass"
        records.append({
            "check": code,
            "result": result,
            "note": "本页无图形" if result == "not_applicable" else "",
        })
    return records


def page(number: int, *, not_applicable: str | None = None) -> dict:
    return {"page": number, "result": "pass", "checks": checks(not_applicable=not_applicable)}


def warning(kind: str, width: str | None, lines: str | None = "12--13") -> dict:
    return {"kind": kind, "box": "hbox", "width_pt": width, "lines": lines}


def exemption(edition: str, item: dict) -> dict:
    return {
        "edition": edition,
        **copy.deepcopy(item),
        "source_file": "contents/answers.tex",
        "pdf_page": 1,
        "visual_result": "pass",
        "reason": "已逐页确认未越出版心",
    }


def build_receipt(warnings: list[dict] | None = None) -> dict:
    mixed = warnings if warnings is not None else []
    return {
        "paper_id": "gk-2026-test",
        "attempt_id": ATTEMPT,
        "input_projection": SHA_A,
        "generation_input_tree": {"tree_sha256": SHA_A},
        "dependency_tree": {"tree_sha256": SHA_B},
        "toolchain_fingerprint": toolchain(),
        "editions": [
            {
                "edition": edition,
                "pdf": {"path": f"build/{edition}.pdf", "sha256": SHA_A, "page_count": 2},
                "log": {"overfull": copy.deepcopy(mixed)},
            }
            for edition in subject.EDITIONS
        ],
    }


def review_receipt(warnings: list[dict] | None = None) -> dict:
    mixed = warnings if warnings is not None else []
    return {
        "schema_version": 1,
        "paper_id": "gk-2026-test",
        "project_dir": "2026-test",
        "batch_id": "batch-1",
        "status": "passed",
        "reviewed_at": "2026-08-11T12:00:00+08:00",
        "build_attempt_id": ATTEMPT,
        "input_projection": SHA_A,
        "generation_input_tree_sha256": SHA_A,
        "dependency_tree_sha256": SHA_B,
        "toolchain_fingerprint": toolchain(),
        "visual_tool_fingerprint": visual(),
        "editions": [
            {
                "edition": edition,
                "pdf_sha256": SHA_A,
                "page_count": 2,
                "result": "pass",
                "candidate_pages": [2],
                "candidate_override": None,
                "pages": [page(1, not_applicable="figure_label"), page(2)],
            }
            for edition in subject.EDITIONS
        ],
        "warning_exemptions": [
            exemption(edition, item)
            for edition in subject.EDITIONS
            for item in mixed
        ],
    }


def manifest() -> dict:
    return {
        "papers": [{
            "paper_id": "gk-2026-test",
            "project_dir": "2026-test",
            "title": "测试卷",
        }],
        "batches": [{"batch_id": "batch-1", "paper_ids": ["gk-2026-test"]}],
    }


class ReviewSchemaContractTests(unittest.TestCase):
    def test_schema_accepts_complete_four_edition_review(self) -> None:
        subject.validate_review(review_receipt())

    def test_schema_rejects_missing_required_binding(self) -> None:
        receipt = review_receipt()
        del receipt["input_projection"]
        with self.assertRaisesRegex(subject.ReviewError, "Schema"):
            subject.validate_review(receipt)

    def test_pages_must_cover_exactly_one_through_n(self) -> None:
        duplicate = page(1)
        duplicate["checks"][0]["note"] = "重复页的不同记录"
        for pages, message in (([page(1)], "缺页"),
                               ([page(1), duplicate], "重页"),
                               ([page(1), page(3)], "越界页")):
            with self.subTest(message=message):
                receipt = review_receipt()
                receipt["editions"][0]["pages"] = pages
                with self.assertRaisesRegex(subject.ReviewError, message):
                    subject.validate_review(receipt)

    def test_not_applicable_and_fail_checks_require_reason(self) -> None:
        for result in ("not_applicable", "fail"):
            with self.subTest(result=result):
                receipt = review_receipt()
                check = receipt["editions"][0]["pages"][0]["checks"][0]
                check.update(result=result, note="")
                if result == "fail":
                    receipt["editions"][0]["pages"][0]["result"] = "fail"
                    receipt["editions"][0]["result"] = "fail"
                    receipt["status"] = "failed"
                with self.assertRaisesRegex(subject.ReviewError, "必须写明理由"):
                    subject.validate_review(receipt)

    def test_candidate_pages_do_not_replace_full_page_review(self) -> None:
        receipt = review_receipt()
        receipt["editions"][0]["candidate_pages"] = [2]
        subject.validate_review(receipt)
        self.assertEqual([1, 2], [item["page"] for item in receipt["editions"][0]["pages"]])


class PublicInterfaceAndCandidateTests(unittest.TestCase):
    def test_six_public_interfaces_exist(self) -> None:
        for name in (
            "candidate_pages", "new_review_work_item", "aggregate_batch_in_memory",
            "render_batch_report", "finalize_batch", "is_stale",
        ):
            with self.subTest(name=name):
                self.assertTrue(callable(getattr(subject, name)))

    def test_candidate_pages_uses_equal_weight_min_max_and_only_highest(self) -> None:
        result = subject.candidate_pages([
            {"page": 1, "text_chars": 0, "math_glyph_proxy": 0, "ink_ratio": 0.0},
            {"page": 2, "text_chars": 10, "math_glyph_proxy": 5, "ink_ratio": 0.5},
            {"page": 3, "text_chars": 5, "math_glyph_proxy": 0, "ink_ratio": 0.0},
        ])
        self.assertEqual([2], result["pages"])
        self.assertEqual([2], result["dense_pages"])
        self.assertEqual([0.0, 1.0, 1.0 / 6.0], [item["score"] for item in result["scores"]])

    def test_default_page_metrics_runs_real_poppler_when_available(self) -> None:
        pdftotext = shutil.which("pdftotext")
        pdftoppm = shutil.which("pdftoppm")
        xelatex = shutil.which("xelatex")
        if not (pdftotext and pdftoppm and xelatex):
            self.skipTest("pdftotext/pdftoppm/xelatex 不齐，无法真实生成并读取 PDF")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "metrics.tex"
            source.write_text(
                r"\documentclass{article}\begin{document}Plain text\newpage $x+y=2$\end{document}",
                encoding="utf-8",
            )
            subprocess.run(
                [xelatex, "-interaction=nonstopmode", "-halt-on-error", source.name],
                cwd=root, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            tools = []
            for name, path in (("pdftotext", pdftotext), ("pdftoppm", pdftoppm)):
                resolved = str(Path(path).resolve())
                tools.append({"name": name, "path": resolved, "real_path": resolved,
                              "sha256": hashlib.sha256(Path(resolved).read_bytes()).hexdigest(),
                              "version": "integration"})
            metrics = subject.default_page_metrics(
                root, "metrics.pdf", 2, {"tools": tools}
            )
        self.assertEqual([1, 2], [item["page"] for item in metrics])
        self.assertGreater(metrics[0]["text_chars"], 0)
        self.assertGreaterEqual(metrics[1]["math_glyph_proxy"], 2)
        self.assertTrue(all(0.0 < item["ink_ratio"] < 1.0 for item in metrics))

    def test_candidate_override_cannot_hide_original_candidate_tampering(self) -> None:
        build = build_receipt()
        item = subject.new_review_work_item(
            manifest(), "batch-1", "gk-2026-test", subject.EDITIONS[0],
            build, visual(), [2],
        )
        item["candidate_pages"] = [1]
        with self.assertRaisesRegex(subject.ReviewError, "原候选"):
            subject._validate_work_binding(item, build, subject.EDITIONS[0], visual())

        item = subject.new_review_work_item(
            manifest(), "batch-1", "gk-2026-test", subject.EDITIONS[0],
            build, visual(), [2],
        )
        item["candidate_override"] = {
            "original_pages": [1], "chosen_pages": [1], "reason": "人工改选"
        }
        item["candidate_pages"] = [1]
        with self.assertRaisesRegex(subject.ReviewError, "original_pages"):
            subject._validate_work_binding(item, build, subject.EDITIONS[0], visual())

    def test_new_work_item_contains_every_page_and_all_checks(self) -> None:
        item = subject.new_review_work_item(
            manifest(), "batch-1", "gk-2026-test", subject.EDITIONS[0],
            build_receipt(), visual(), [2],
        )
        self.assertEqual([1, 2], [record["page"] for record in item["pages"]])
        self.assertEqual(set(subject.CHECK_CODES), {record["check"] for record in item["pages"][0]["checks"]})
        self.assertEqual([2], item["candidate_pages"])
        self.assertEqual([2], item["original_candidate_pages"])

    def test_aggregate_batch_in_memory_builds_a_passed_review(self) -> None:
        build = build_receipt()
        with tempfile.TemporaryDirectory() as temporary:
            work = Path(temporary)
            for edition in subject.EDITIONS:
                item = subject.new_review_work_item(
                    manifest(), "batch-1", "gk-2026-test", edition, build, visual(), [2]
                )
                item["result"] = "pass"
                item["pages"] = [page(1), page(2)]
                target = subject.work_item_path(work, "batch-1", edition, "gk-2026-test")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps(item), encoding="utf-8")
            result = subject.aggregate_batch_in_memory(
                PROJECT, manifest(), "batch-1", {"gk-2026-test": build}, work, visual(),
                reviewed_at="2026-08-11T12:00:00+08:00",
            )
        self.assertEqual("passed", result["reviews"]["gk-2026-test"]["status"])
        self.assertEqual([], result["fails"])

    def test_render_batch_report_has_stable_basic_fields(self) -> None:
        report = subject.render_batch_report({
            "batch_id": "batch-1", "batch_outcome": "closed", "paper_count": 0,
            "edition_count": 0, "page_total": 0, "papers": [],
        })
        self.assertIn("# 批次 batch-1 视觉审查报告", report)
        self.assertIn("- 批次结论：`closed`", report)


class CurrencyAndWarningTests(unittest.TestCase):
    def test_current_and_stale_build_projection_toolchain_pdf_sha(self) -> None:
        build = build_receipt()
        review = review_receipt()
        self.assertEqual((False, []), subject.is_stale(build, review, visual()))
        mutations = (
            ("projection", lambda item: item.__setitem__("input_projection", SHA_B), "manifest 投影变化"),
            ("toolchain", lambda item: item["toolchain_fingerprint"].__setitem__("texlive_revision", "changed"), "构建工具链"),
            ("pdf", lambda item: item["editions"][0].__setitem__("pdf_sha256", SHA_B), "PDF 已变化"),
        )
        for name, mutate, reason in mutations:
            with self.subTest(name=name):
                changed = review_receipt()
                mutate(changed)
                stale, reasons = subject.is_stale(build, changed, visual())
                self.assertTrue(stale)
                self.assertTrue(any(reason in item for item in reasons), reasons)

    def test_real_mixed_warning_shape_matches_without_string_sorting(self) -> None:
        mixed = [
            warning("Overfull", "86.97256", "20--21"),
            warning("Overfull", "506.01268", "10--11"),
            warning("Underfull", None, None),
        ]
        review = review_receipt(mixed)
        subject.validate_review(review)
        self.assertEqual((False, []), subject.is_stale(build_receipt(mixed), review, visual()))
        ordered = sorted(
            [subject._warning_key(subject.EDITIONS[0], item) for item in mixed],
            key=subject._warning_sort_key,
        )
        self.assertEqual(["86.97256", "506.01268", None], [item[3] for item in ordered])

    def test_warning_line_or_width_change_invalidates_exemption(self) -> None:
        original = warning("Overfull", "86.97256", "20--21")
        for changed in (
            warning("Overfull", "86.97256", "21--22"),
            warning("Overfull", "86.97257", "20--21"),
        ):
            with self.subTest(changed=changed):
                stale, reasons = subject.is_stale(
                    build_receipt([changed]), review_receipt([original]), visual()
                )
                self.assertTrue(stale)
                self.assertTrue(any("警告集合" in item for item in reasons))

    def test_warning_sort_checks_kind_before_float_width(self) -> None:
        with self.assertRaisesRegex(subject.ReviewError, "Underfull.*null"):
            subject._warning_sort_key((subject.EDITIONS[0], "Underfull", "hbox", "bad", None))
        with self.assertRaisesRegex(subject.ReviewError, "Overfull.*null"):
            subject._warning_sort_key((subject.EDITIONS[0], "Overfull", "hbox", None, None))

    def test_warning_change_makes_review_stale(self) -> None:
        mixed = [warning("Overfull", "86.97256")]
        changed = [warning("Overfull", "506.01268")]
        stale, reasons = subject.is_stale(build_receipt(changed), review_receipt(mixed), visual())
        self.assertTrue(stale)
        self.assertTrue(any("警告集合" in item for item in reasons))


class CliContractTests(unittest.TestCase):
    def test_parser_contains_all_brief_commands_and_no_legacy_writers(self) -> None:
        parser = subject._parser()
        choices = next(action for action in parser._actions if action.dest == "command").choices
        self.assertEqual({
            "prepare-batch", "finalize-batch", "finalize-batch-checked",
            "check-batch", "check-all", "output-paths", "check-staged",
        }, set(choices))
        self.assertTrue({"aggregate", "finalize", "close", "report"}.isdisjoint(choices))

    def test_exit_code_constants(self) -> None:
        self.assertEqual((0, 2, 4, 6), (
            subject.EXIT_FINALIZED, subject.EXIT_USAGE,
            subject.EXIT_VISUAL_FAILED, subject.EXIT_INVALID,
        ))

    def test_prepare_batch_requires_two_to_four_papers(self) -> None:
        for count in (1, 5):
            with self.subTest(count=count):
                document = manifest()
                document["batches"][0]["paper_ids"] = [
                    "gk-2026-test-%d" % index for index in range(count)
                ]
                with self.assertRaisesRegex(subject.ReviewError, "2–4"):
                    subject._validate_batch_size(document, "batch-1")

    def test_work_and_report_containment_reject_escaping_paths(self) -> None:
        root = PROJECT.parents[3]
        with self.assertRaises(subject.UsageError):
            subject._validated_work_dir(root, root / "outside-work")
        with self.assertRaises(subject.UsageError):
            subject._require_report_path(root, root / "wrong.md", "batch-1")
        self.assertEqual(
            subject.report_target("batch-1"),
            subject._require_report_path(root, root / subject.report_target("batch-1"), "batch-1"),
        )


class BatchIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        papers = [
            build_tests.paper_entry(),
            build_tests.paper_entry(
                paper_id=build_tests.OTHER_ID,
                project_dir=build_tests.OTHER_DIR,
                legacy="legacy-other",
            ),
        ]
        self.fixture = build_tests.RepositoryFixture(papers=papers)
        self.addCleanup(self.fixture.cleanup)
        self.chain = self.fixture.toolchain()
        self.loader = build_tests.make_loader()
        result = self.fixture.formal(loader=self.loader)
        self.assertEqual("COMPILED_PENDING_REVIEW", result["code"])
        self.fixture.commit_all("待视觉审查基线")
        self.manifest = self.fixture.manifest()
        self.batch_id = build_tests.BATCH_ID
        self.report_path = self.fixture.root / subject.report_target(self.batch_id)

    @staticmethod
    def probe(root, pdf_relative, page_count, toolchain):
        return [
            {"page": number, "text_chars": number, "math_glyph_proxy": number,
             "ink_ratio": number / 10.0}
            for number in range(1, page_count + 1)
        ]

    def prepare(self) -> dict:
        return subject.prepare_batch(
            self.fixture.manifest_path, self.batch_id, toolchain=self.chain,
            metrics_probe=self.probe,
        )

    def complete_work(self, failures=()) -> None:
        failure_set = set(failures)
        work = self.fixture.root / subject.WORK_RELATIVE
        for paper_id in (build_tests.PAPER_ID, build_tests.OTHER_ID):
            for edition in subject.EDITIONS:
                path = subject.work_item_path(work, self.batch_id, edition, paper_id)
                item = json.loads(path.read_text(encoding="utf-8"))
                item["result"] = "pass"
                for record in item["pages"]:
                    record["result"] = "pass"
                    for check in record["checks"]:
                        check["result"] = "pass"
                    key = (paper_id, edition, record["page"])
                    if key in failure_set:
                        record["result"] = "fail"
                        record["checks"][0].update(result="fail", note="图形跨页断裂")
                        item["result"] = "fail"
                path.write_text(json.dumps(item), encoding="utf-8")

    def finalize(self, **kwargs) -> dict:
        kwargs.setdefault("metrics_probe", self.probe)
        return subject.finalize_batch(
            self.fixture.manifest_path, self.fixture.issues_path, self.batch_id,
            self.report_path, facts_loader=self.loader, toolchain=self.chain,
            **kwargs,
        )

    def mutate_first_work(self, mutate) -> None:
        path = subject.work_item_path(
            self.fixture.root / subject.WORK_RELATIVE, self.batch_id,
            subject.EDITIONS[0], build_tests.PAPER_ID,
        )
        item = json.loads(path.read_text(encoding="utf-8"))
        mutate(item)
        path.write_text(json.dumps(item), encoding="utf-8")

    def test_finalize_recomputes_candidate_when_original_and_candidate_both_tampered(self) -> None:
        self.prepare()
        self.complete_work()
        self.mutate_first_work(lambda item: item.update(
            original_candidate_pages=[], candidate_pages=[]
        ))
        with self.assertRaisesRegex(subject.ReviewError, "重算原候选"):
            self.finalize(metrics_probe=self.probe)

    def test_finalize_recomputes_candidate_when_both_candidate_fields_deleted(self) -> None:
        self.prepare()
        self.complete_work()
        self.mutate_first_work(lambda item: (
            item.pop("original_candidate_pages"), item.pop("candidate_pages")
        ))
        with self.assertRaisesRegex(subject.ReviewError, "重算原候选"):
            self.finalize(metrics_probe=self.probe)

    def test_finalize_recomputes_candidate_for_forged_override_original(self) -> None:
        self.prepare()
        self.complete_work()
        self.mutate_first_work(lambda item: item.update(
            original_candidate_pages=[], candidate_pages=[],
            candidate_override={
                "original_pages": [], "chosen_pages": [], "reason": "伪造原候选"
            },
        ))
        with self.assertRaisesRegex(subject.ReviewError, "重算原候选"):
            self.finalize(metrics_probe=self.probe)

    def test_finalize_accepts_recomputed_normal_and_legal_override(self) -> None:
        self.prepare()
        self.complete_work()
        self.mutate_first_work(lambda item: item.update(candidate_override={
            "original_pages": list(item["original_candidate_pages"]),
            "chosen_pages": list(item["candidate_pages"]),
            "reason": "人工复核后维持原候选",
        }))
        result = self.finalize(metrics_probe=self.probe)
        self.assertEqual("FINALIZED", result["code"])

    def tracked_state(self) -> dict:
        result = {}
        for path in sorted(self.fixture.root.rglob("*")):
            if not path.is_file() or ".git" in path.parts or ".work" in path.parts:
                continue
            relative = path.relative_to(self.fixture.root).as_posix()
            if relative.startswith(".fake"):
                continue
            result[relative] = file_sha256(path)
        return result

    def test_state_transaction_interruption_recovers_all_finalize_targets(self) -> None:
        self.prepare()
        self.complete_work()
        original = subject.build_projects.commit_state
        captured = {}

        def interrupted(root, manifest, receipts, extra, build_manifest):
            transaction = Transaction(root, event_hook=lambda event, path: (
                (_ for _ in ()).throw(RuntimeError("simulated interruption"))
                if event == "target_replaced" else None
            ))
            document = build_manifest(transaction.transaction_id)
            targets = {}
            for relative in sorted(receipts):
                targets[relative] = receipts[relative]
            for relative in sorted(extra):
                targets[relative] = extra[relative]
            targets[subject.MANIFEST_TARGET] = canonical_json(document).encode("utf-8")
            transaction.prepare("state", targets, {}, expected_revision=manifest["revision"])
            captured["targets"] = targets
            transaction.commit()

        with mock.patch.object(subject.build_projects, "commit_state", side_effect=interrupted):
            with self.assertRaisesRegex(RuntimeError, "simulated interruption"):
                self.finalize()
        recover_transactions(self.fixture.root)
        for relative, expected in captured["targets"].items():
            self.assertEqual(expected, (self.fixture.root / relative).read_bytes())
        transactions = self.fixture.root / subject.WORK_RELATIVE / "transactions"
        self.assertEqual([], list(transactions.iterdir()) if transactions.exists() else [])

    def test_blocked_provenance_is_not_overwritten_by_build_review(self) -> None:
        blocker = subject.issues_module.question_issue(
            build_tests.PAPER_ID, "1", "source-a", "transcription", "人工核实来源"
        )
        issue_id = subject.issues_module.upsert_issue(self.fixture.issues_path, blocker)
        document = self.fixture.manifest()
        paper = next(item for item in document["papers"] if item["paper_id"] == build_tests.PAPER_ID)
        paper.update(production_state="blocked", blocked_from="answers_verified",
                     resume_action="人工核实来源", issue_ids=[issue_id])
        atomic_write_json(self.fixture.manifest_path, document)
        self.prepare()
        self.complete_work()
        result = self.finalize()
        self.assertEqual("closed_with_blockers", result["batch_status"])
        paper = next(item for item in self.fixture.manifest()["papers"]
                     if item["paper_id"] == build_tests.PAPER_ID)
        self.assertEqual("blocked", paper["production_state"])
        self.assertEqual("answers_verified", paper["blocked_from"])
        self.assertEqual("人工核实来源", paper["resume_action"])

    def test_finalize_success_commits_one_state_and_closes(self) -> None:
        self.prepare()
        self.complete_work()
        before_revision = self.fixture.manifest()["revision"]
        calls = []
        original = subject.build_projects.commit_state

        def counted(*args, **kwargs):
            calls.append(True)
            return original(*args, **kwargs)

        with mock.patch.object(subject.build_projects, "commit_state", side_effect=counted):
            result = self.finalize(reviewed_at="2026-08-12T12:00:00+08:00")
        self.assertEqual("FINALIZED", result["code"])
        self.assertEqual("closed", result["batch_status"])
        self.assertEqual([True], calls)
        self.assertEqual(before_revision + 1, self.fixture.manifest()["revision"])
        self.assertTrue(self.report_path.is_file())
        for paper in self.fixture.manifest()["papers"]:
            self.assertEqual("complete", paper["production_state"])
            self.assertEqual("succeeded", self.fixture.receipt(paper["project_dir"])["status"])
            review = json.loads((self.fixture.root / subject.review_receipt_path(paper)).read_text())
            self.assertEqual("passed", review["status"])
            self.assertEqual(subject.EDITIONS, tuple(item["edition"] for item in review["editions"]))

    def test_visual_fail_is_valid_diagnostic_without_build_or_report(self) -> None:
        self.prepare()
        failure = (build_tests.PAPER_ID, subject.EDITIONS[1], 1)
        self.complete_work([failure])
        report_sentinel = b"old report\n"
        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        self.report_path.write_bytes(report_sentinel)
        builds_before = {
            paper["paper_id"]: (self.fixture.root / subject.build_receipt_path(paper)).read_bytes()
            for paper in self.fixture.manifest()["papers"]
        }
        result = self.finalize(reviewed_at="2026-08-12T12:00:00+08:00")
        self.assertEqual("VISUAL_FAILED", result["code"])
        self.assertEqual("compiled_pending_review", result["batch_status"])
        self.assertFalse(result["report_written"])
        self.assertEqual(report_sentinel, self.report_path.read_bytes())
        for paper in self.fixture.manifest()["papers"]:
            self.assertEqual(
                builds_before[paper["paper_id"]],
                (self.fixture.root / subject.build_receipt_path(paper)).read_bytes(),
            )
        failed = next(
            paper for paper in self.fixture.manifest()["papers"]
            if paper["paper_id"] == build_tests.PAPER_ID
        )
        self.assertEqual("blocked", failed["production_state"])
        issues = subject.issues_module.load_issues(self.fixture.issues_path)
        visual = [item for item in issues if item.get("origin") == subject.ISSUE_ORIGIN]
        self.assertEqual(1, len(visual))
        self.assertEqual((subject.EDITIONS[1], 1, "glyph"),
                         (visual[0]["edition"], visual[0]["page"], visual[0]["check_code"]))

    def test_incomplete_currency_cas_and_report_failures_change_no_formal_state(self) -> None:
        self.prepare()
        self.complete_work()
        work = self.fixture.root / subject.WORK_RELATIVE
        missing = subject.work_item_path(
            work, self.batch_id, subject.EDITIONS[-1], build_tests.OTHER_ID
        )
        missing.unlink()
        before = self.tracked_state()
        with self.assertRaises(subject.ReviewError):
            self.finalize()
        self.assertEqual(before, self.tracked_state())

        self.prepare_after_removing_work()
        self.complete_work()
        first_path = subject.work_item_path(
            self.fixture.root / subject.WORK_RELATIVE, self.batch_id,
            subject.EDITIONS[0], build_tests.PAPER_ID,
        )
        item = json.loads(first_path.read_text())
        item["pdf"]["sha256"] = SHA_B
        first_path.write_text(json.dumps(item), encoding="utf-8")
        before = self.tracked_state()
        with self.assertRaisesRegex(subject.ReviewError, "不匹配"):
            self.finalize()
        self.assertEqual(before, self.tracked_state())

        shutil.rmtree(self.fixture.root / subject.WORK_RELATIVE / self.batch_id)
        self.prepare()
        self.complete_work()
        before = self.tracked_state()
        with self.assertRaises(subject.ReviewError):
            self.finalize(renderer=lambda payload: "破损报告\n")
        self.assertEqual(before, self.tracked_state())

        before = self.tracked_state()
        with mock.patch.object(
            subject.build_projects, "commit_state", side_effect=RuntimeError("revision CAS")
        ):
            with self.assertRaisesRegex(RuntimeError, "CAS"):
                self.finalize()
        self.assertEqual(before, self.tracked_state())

    def prepare_after_removing_work(self) -> None:
        directory = self.fixture.root / subject.WORK_RELATIVE / self.batch_id
        if directory.exists():
            shutil.rmtree(directory)
        self.prepare()

    def test_check_batch_rejects_report_after_blocker_changes_without_reconcile(self) -> None:
        blocker = subject.issues_module.question_issue(
            build_tests.PAPER_ID, "1", "source-a", "transcription", "人工核实来源"
        )
        subject.issues_module.upsert_issue(self.fixture.issues_path, blocker)
        self.prepare()
        self.complete_work()
        self.assertEqual("closed_with_blockers", self.finalize()["batch_status"])
        current = next(
            item for item in subject.issues_module.load_issues(self.fixture.issues_path)
            if item.get("origin") != subject.ISSUE_ORIGIN
        )
        current.update(status="resolved", impact="non_blocking")
        subject.issues_module.upsert_issue(self.fixture.issues_path, current)
        before = self.tracked_state()
        result = subject.check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, self.batch_id,
            toolchain=self.chain, facts_loader=self.loader,
        )
        self.assertEqual("INVALID_OR_STALE", result["code"])
        self.assertTrue(any("报告" in item or "状态" in item for item in result["problems"]))
        self.assertEqual(before, self.tracked_state())

    def test_report_only_reconciliation_closes_after_blocker_resolves(self) -> None:
        blocker = subject.issues_module.question_issue(
            build_tests.PAPER_ID, "1", "source-a", "transcription", "人工核实来源"
        )
        subject.issues_module.upsert_issue(self.fixture.issues_path, blocker)
        self.prepare()
        self.complete_work()
        result = self.finalize()
        self.assertEqual("closed_with_blockers", result["batch_status"])
        shutil.rmtree(self.fixture.root / subject.WORK_RELATIVE / self.batch_id)
        records = subject.issues_module.load_issues(self.fixture.issues_path)
        current = next(item for item in records if item.get("origin") != subject.ISSUE_ORIGIN)
        current["status"] = "resolved"
        current["impact"] = "non_blocking"
        subject.issues_module.upsert_issue(self.fixture.issues_path, current)
        result = self.finalize()
        self.assertEqual("report-only", result["mode"])
        self.assertEqual("closed", result["batch_status"])

    def test_prepare_batch_uses_current_receipts_and_only_writes_ignored_work(self) -> None:
        before = self.tracked_state()
        result = self.prepare()
        self.assertEqual(8, len(result["created"]))
        self.assertEqual(before, self.tracked_state())
        self.assertEqual([], subject._tracked_tree_is_clean(self.fixture.root))
        for relative in result["created"]:
            self.assertTrue(relative.startswith(subject.WORK_RELATIVE + "/"))
            ignored = subprocess.run(
                ["git", "-C", str(self.fixture.root), "check-ignore", "-q", "--", relative]
            )
            self.assertEqual(0, ignored.returncode)

    def test_prepare_rejects_non_pending_and_stale_build_without_work(self) -> None:
        first = build_tests.PAPER_ID
        receipt_path = self.fixture.root / subject.build_receipt_path(
            next(item for item in self.manifest["papers"] if item["paper_id"] == first)
        )
        original = receipt_path.read_bytes()
        receipt = json.loads(original)
        receipt["status"] = "succeeded"
        receipt_path.write_bytes(canonical_json(receipt).encode("utf-8"))
        with self.assertRaisesRegex(subject.ReviewError, "compiled_pending_review"):
            self.prepare()
        self.assertFalse((self.fixture.root / subject.WORK_RELATIVE / self.batch_id).exists())
        receipt_path.write_bytes(original)
        self.fixture.write(
            "%s/%s/questions.tex" % (subject.PROJECT_RELATIVE, build_tests.PROJECT_DIR),
            "漂移\n",
        )
        with self.assertRaisesRegex(subject.ReviewError, "失效"):
            self.prepare()
        self.assertFalse((self.fixture.root / subject.WORK_RELATIVE / self.batch_id).exists())


class OwnershipAndCliIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "task24@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Task 24"], check=True)
        self.scope = ["owned-mod.txt", "owned-new.txt", "owned-delete.txt", "issues.md"]
        for name in ("owned-mod.txt", "owned-delete.txt", "issues.md", "outside.txt"):
            (self.root / name).write_text("old\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "base"], check=True)

    def git(self, *args) -> None:
        subprocess.run(["git", "-C", str(self.root), *args], check=True)

    def test_check_staged_covers_modify_add_delete_and_unchanged_issues(self) -> None:
        (self.root / "owned-mod.txt").write_text("new\n", encoding="utf-8")
        (self.root / "owned-new.txt").write_text("new\n", encoding="utf-8")
        (self.root / "owned-delete.txt").unlink()
        self.git("add", "--", "owned-mod.txt", "owned-new.txt", "owned-delete.txt")
        self.assertEqual([], subject.check_staged(self.root, self.scope))

    def test_check_staged_accepts_issues_add_or_resolve_and_rejects_outside(self) -> None:
        for text in ("new issue\n", "resolved issue\n"):
            with self.subTest(text=text):
                self.git("reset", "--hard", "-q", "HEAD")
                (self.root / "issues.md").write_text(text, encoding="utf-8")
                self.git("add", "issues.md")
                self.assertEqual([], subject.check_staged(self.root, self.scope))
        (self.root / "outside.txt").write_text("staged outside\n", encoding="utf-8")
        self.git("add", "outside.txt")
        self.assertTrue(any("范围外" in item for item in subject.check_staged(self.root, self.scope)))

    def test_output_paths_include_state_report_and_nul(self) -> None:
        document = manifest()
        document["papers"].append({
            "paper_id": "gk-2026-test-2", "project_dir": "2026-test-2", "title": "测试卷2"
        })
        document["batches"][0]["paper_ids"].append("gk-2026-test-2")
        with mock.patch.object(subject, "load_manifest", return_value=document), \
                mock.patch.object(subject.cli_common, "repository_root", return_value=self.root), \
                mock.patch.object(subject, "_require_canonical", return_value=self.root / subject.MANIFEST_TARGET), \
                mock.patch.object(subject, "_require_report_path", return_value=subject.report_target("batch-1")), \
                mock.patch.object(sys, "stdout") as stdout:
            stdout.buffer = mock.Mock()
            code = subject._output_paths_command(argparse_namespace(
                manifest=str(self.root / subject.MANIFEST_TARGET), batch="batch-1",
                include_state=True, report=str(self.root / subject.report_target("batch-1")), nul=True,
            ))
            payload = b"".join(call.args[0] for call in stdout.buffer.write.call_args_list)
        self.assertEqual(0, code)
        paths = [item.decode() for item in payload.split(b"\0") if item]
        self.assertIn(subject.MANIFEST_TARGET, paths)
        self.assertIn(subject.ISSUES_TARGET, paths)
        self.assertIn(subject.report_target("batch-1"), paths)
        self.assertEqual(7, len(paths))

    def test_argparse_usage_is_json_for_real_invalid_argv(self) -> None:
        cases = (
            ["finalize-batch", "--json"],
            ["unknown-command", "--json"],
            ["check-batch", "--json", "--illegal"],
        )
        for argv in cases:
            with self.subTest(argv=argv):
                output = StringIO()
                with redirect_stdout(output), redirect_stderr(StringIO()):
                    code = subject.main(argv)
                self.assertEqual(2, code)
                self.assertEqual("USAGE", json.loads(output.getvalue())["code"])

    def test_json_code_exit_matrix_and_usage(self) -> None:
        common = ["--manifest", "m", "--issues", "i", "--batch", "b"]
        commands = (
            ("finalize-batch", {"code": "FINALIZED", "batch_id": "b"}, 0),
            ("finalize-batch", {"code": "VISUAL_FAILED", "batch_id": "b", "problems": []}, 4),
            ("check-batch", {"code": "INVALID_OR_STALE", "batch_id": "b", "papers": [], "problems": []}, 6),
        )
        for command, report, expected in commands:
            argv = [command, *common]
            patch_name = "finalize_batch" if command == "finalize-batch" else "check_batch"
            if command == "finalize-batch":
                argv += ["--output-report", "r"]
            argv += ["--json"]
            output = StringIO()
            with mock.patch.object(subject, patch_name, return_value=report), redirect_stdout(output):
                code = subject.main(argv)
            self.assertEqual(expected, code)
            self.assertEqual(report["code"], json.loads(output.getvalue())["code"])
        output = StringIO()
        with mock.patch.object(subject, "finalize_batch", side_effect=subject.UsageError("bad")), \
                redirect_stdout(output), redirect_stderr(StringIO()):
            code = subject.main(["finalize-batch", *common, "--output-report", "r", "--json"])
        self.assertEqual(2, code)
        self.assertEqual("USAGE", json.loads(output.getvalue())["code"])


def argparse_namespace(**kwargs):
    return type("Arguments", (), kwargs)()


class VisualIssueReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = Path(self.temporary.name) / "issues.md"

    def fail(self, page_number, attempt=ATTEMPT, pdf=SHA_A, check="figure_label"):
        return {
            "paper_id": "gk-2026-test", "edition": subject.EDITIONS[0],
            "page": page_number, "check_code": check, "note": "图形跨页",
            "build_attempt_id": attempt, "pdf_sha256": pdf,
        }

    def test_current_fails_upsert_and_deleted_or_moved_pages_resolve(self) -> None:
        payload, _, first = subject.reconcile_visual_issues(
            self.path, ["gk-2026-test"], [self.fail(1)]
        )
        self.path.write_bytes(payload)
        self.assertEqual("open", first[0]["status"])
        payload, _, second = subject.reconcile_visual_issues(
            self.path, ["gk-2026-test"], [self.fail(2, pdf=SHA_B)]
        )
        self.path.write_bytes(payload)
        by_page = {item["page"]: item for item in second}
        self.assertEqual("resolved", by_page[1]["status"])
        self.assertEqual("open", by_page[2]["status"])
        self.assertEqual(SHA_B, by_page[2]["pdf_sha256"])

    def test_old_attempt_pdf_disappearing_resolves_but_manual_issue_never_does(self) -> None:
        payload, _, _ = subject.reconcile_visual_issues(
            self.path, ["gk-2026-test"], [self.fail(1)]
        )
        self.path.write_bytes(payload)
        manual = subject.issues_module.question_issue(
            "gk-2026-test", "1", "source-a", "transcription", "人工核对来源"
        )
        subject.issues_module.upsert_issue(self.path, manual)
        payload, _, records = subject.reconcile_visual_issues(
            self.path, ["gk-2026-test"], []
        )
        visual = next(item for item in records if item.get("origin") == subject.ISSUE_ORIGIN)
        human = next(item for item in records if item.get("origin") != subject.ISSUE_ORIGIN)
        self.assertEqual("resolved", visual["status"])
        self.assertEqual("open", human["status"])

    def test_graphic_cross_page_failures_keep_both_pages(self) -> None:
        payload, _, records = subject.reconcile_visual_issues(
            self.path, ["gk-2026-test"], [self.fail(1), self.fail(2)]
        )
        self.assertTrue(payload)
        self.assertEqual([1, 2], sorted(item["page"] for item in records))


class CheckedWrapperTests(BatchIntegrationTests):
    def test_checked_stage_failures_reset_exact_scope_and_allow_retry(self) -> None:
        for failure in ("check-staged", "diff-check", "commit"):
            with self.subTest(failure=failure):
                self.tearDown()
                self.setUp()
                self.prepare()
                self.complete_work([(build_tests.PAPER_ID, subject.EDITIONS[0], 1)])
                original_git = subject._git
                original_check = subject.check_staged
                state = {"failed": False}

                def failing_git(root, arguments):
                    if not state["failed"] and (
                        (failure == "diff-check" and arguments[:3] == ["diff", "--cached", "--check"])
                        or (failure == "commit" and arguments[0] == "commit")
                    ):
                        state["failed"] = True
                        raise subprocess.CalledProcessError(1, arguments)
                    return original_git(root, arguments)

                def failing_check(root, scope):
                    if failure == "check-staged" and not state["failed"]:
                        state["failed"] = True
                        return ["injected"]
                    return original_check(root, scope)

                with mock.patch.object(subject, "_git", side_effect=failing_git), \
                        mock.patch.object(subject, "check_staged", side_effect=failing_check):
                    with self.assertRaises((subject.ReviewError, subprocess.CalledProcessError)):
                        subject.finalize_batch_checked(
                            self.fixture.manifest_path, self.fixture.issues_path, self.batch_id,
                            self.report_path, facts_loader=self.loader, toolchain=self.chain, metrics_probe=self.probe,
                        )
                staged = subprocess.check_output(
                    ["git", "-C", str(self.fixture.root), "diff", "--cached", "--name-only"],
                    text=True,
                )
                self.assertEqual("", staged)
                self.fixture.commit_all("保存诊断状态供重试")
                shutil.rmtree(self.fixture.root / subject.WORK_RELATIVE / self.batch_id)
                self.chain = self.fixture.toolchain()
                self.loader = build_tests.make_loader()
                self.fixture.formal(loader=self.loader)
                self.fixture.commit_all("重编基线")
                self.prepare()
                self.complete_work([(build_tests.PAPER_ID, subject.EDITIONS[0], 1)])
                retried = subject.finalize_batch_checked(
                    self.fixture.manifest_path, self.fixture.issues_path, self.batch_id,
                    self.report_path, facts_loader=self.loader, toolchain=self.chain, metrics_probe=self.probe,
                )
                self.assertTrue(retried["committed"])

    def test_checked_visual_fail_commits_exact_diagnostic_scope_without_report(self) -> None:
        self.prepare()
        self.complete_work([(build_tests.PAPER_ID, subject.EDITIONS[0], 1)])
        result = subject.finalize_batch_checked(
            self.fixture.manifest_path, self.fixture.issues_path, self.batch_id,
            self.report_path, facts_loader=self.loader, toolchain=self.chain, metrics_probe=self.probe,
        )
        self.assertEqual("VISUAL_FAILED", result["code"])
        self.assertTrue(result["committed"])
        self.assertNotIn(subject.report_target(self.batch_id), result["committed_paths"])
        message = subprocess.check_output(
            ["git", "-C", str(self.fixture.root), "log", "-1", "--format=%s"], text=True
        ).strip()
        self.assertEqual(subject.DIAGNOSTIC_MESSAGE_TEMPLATE % self.batch_id, message)
        self.assertEqual([], subject._tracked_tree_is_clean(self.fixture.root))

    def test_checked_finalized_does_not_stage_or_commit(self) -> None:
        self.prepare()
        self.complete_work()
        before = subprocess.check_output(
            ["git", "-C", str(self.fixture.root), "rev-parse", "HEAD"], text=True
        ).strip()
        result = subject.finalize_batch_checked(
            self.fixture.manifest_path, self.fixture.issues_path, self.batch_id,
            self.report_path, facts_loader=self.loader, toolchain=self.chain, metrics_probe=self.probe,
        )
        self.assertEqual("FINALIZED", result["code"])
        self.assertFalse(result["committed"])
        self.assertEqual(before, subprocess.check_output(
            ["git", "-C", str(self.fixture.root), "rev-parse", "HEAD"], text=True
        ).strip())
        staged = subprocess.check_output(
            ["git", "-C", str(self.fixture.root), "diff", "--cached", "--name-only"], text=True
        )
        self.assertEqual("", staged)

    def test_checked_rejects_dirty_entry_and_non_visual_results_without_git(self) -> None:
        self.fixture.write("tracked.txt", "untracked does not count\n")
        self.fixture.write(subject.MANIFEST_TARGET, self.fixture.read(subject.MANIFEST_TARGET) + " ")
        before = subprocess.check_output(
            ["git", "-C", str(self.fixture.root), "rev-parse", "HEAD"], text=True
        ).strip()
        result = subject.finalize_batch_checked(
            self.fixture.manifest_path, self.fixture.issues_path, self.batch_id, self.report_path
        )
        self.assertEqual("INVALID_OR_STALE", result["code"])
        self.assertFalse(result["committed"])
        self.assertEqual(before, subprocess.check_output(
            ["git", "-C", str(self.fixture.root), "rev-parse", "HEAD"], text=True
        ).strip())

        subprocess.run(["git", "-C", str(self.fixture.root), "checkout", "--", subject.MANIFEST_TARGET], check=True)
        for code in ("USAGE", "INVALID_OR_STALE", "CAS_FAILED", "OTHER"):
            with self.subTest(code=code), \
                    mock.patch.object(subject, "finalize_batch", return_value={"code": code}), \
                    mock.patch.object(subject, "_git") as git:
                result = subject.finalize_batch_checked(
                    self.fixture.manifest_path, self.fixture.issues_path,
                    self.batch_id, self.report_path,
                )
                self.assertFalse(result["committed"])
                git.assert_not_called()

    def test_git_helpers_use_argument_arrays_and_never_shell_true(self) -> None:
        with mock.patch.object(subject.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, stdout=b"", stderr=b"")
            subject._git(self.fixture.root, ["status", "--short"])
        args, kwargs = run.call_args
        self.assertIsInstance(args[0], list)
        self.assertNotIn("shell", kwargs)


if __name__ == "__main__":
    unittest.main()

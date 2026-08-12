#!/usr/bin/env python3
"""Task 24 第一原子段：视觉回执基础契约。"""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
TOOLS = PROJECT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import review_receipts as subject


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

    def test_new_work_item_contains_every_page_and_all_checks(self) -> None:
        item = subject.new_review_work_item(
            manifest(), "batch-1", "gk-2026-test", subject.EDITIONS[0],
            build_receipt(), visual(), [2],
        )
        self.assertEqual([1, 2], [record["page"] for record in item["pages"]])
        self.assertEqual(set(subject.CHECK_CODES), {record["check"] for record in item["pages"][0]["checks"]})
        self.assertEqual([2], item["candidate_pages"])

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


if __name__ == "__main__":
    unittest.main()

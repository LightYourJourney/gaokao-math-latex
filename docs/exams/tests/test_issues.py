import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from issues import (
    blocks_completion,
    issue_fingerprint,
    load_issues,
    main,
    question_issue,
    upsert_issue,
)


def issue(**updates):
    value = {
        "paper_id": "gk-2026-regular-national-1-recall",
        "affected_paper_ids": [],
        "type": "identity-ambiguous",
        "status": "open",
        "impact": "blocks_completion",
        "resume_action": "人工核验正式卷与回忆版身份",
        "conflict_code": "recall-vs-official",
    }
    value.update(updates)
    return value


def block(issue_id, value):
    payload = copy.deepcopy(value)
    if "fingerprint" not in payload:
        payload["fingerprint"] = issue_fingerprint(payload)
    return (
        f"## {issue_id}\n\n"
        "```json\n"
        + json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n```\n"
    )


class IssueLedgerTests(unittest.TestCase):
    def test_answer_convention_issue_is_question_scoped_and_blocks_completion(self):
        value = question_issue(
            paper_id="gk-2015-regular-hunan-science",
            question_id="gk-2015-regular-hunan-science-q14",
            source_id="src-hunan-2015",
            kind="convention",
            resume_action="取得适用定义或可核答案后裁定并重核Q14",
        )
        self.assertEqual(value["type"], "answer-convention-ambiguous")
        self.assertTrue(blocks_completion(value, "gk-2015-regular-hunan-science"))
        self.assertEqual(len(value["fingerprint"]), 64)

    def test_fingerprint_is_stable_and_ignores_mutable_workflow_fields(self):
        base = issue()
        changed = issue(
            status="investigating",
            impact="non_blocking",
            resume_action="下一步已更新",
            current_evidence="新增证据",
        )
        self.assertEqual(issue_fingerprint(base), issue_fingerprint(changed))
        self.assertEqual(len(issue_fingerprint(base)), 64)

    def test_fingerprint_distinguishes_question_and_visual_dimensions(self):
        question = issue(
            type="transcription-ambiguous",
            question_id="q-11",
            source_id="src-a",
        )
        question_other = dict(question, question_id="q-12")
        self.assertNotEqual(
            issue_fingerprint(question), issue_fingerprint(question_other)
        )

        visual = issue(
            type="figure-missing", edition="试题版", page=3,
            check_code="figure-not-rendered", figure_id="fig-1",
        )
        variants = [
            dict(visual, edition="解析版"),
            dict(visual, page=4),
            dict(visual, check_code="figure-clipped"),
            dict(visual, figure_id="fig-2"),
        ]
        for variant in variants:
            self.assertNotEqual(issue_fingerprint(visual), issue_fingerprint(variant))

        warning = issue(
            type="layout-warning", edition="印刷版", page=9,
            check_code="overfull-hbox",
            warning={"source_file": " questions.tex ", "line": 12, "width": "0.4588pt"},
        )
        normalized = dict(
            warning,
            warning={"source_file": "questions.tex", "line": "12", "width": "0.4588 pt"},
        )
        self.assertEqual(issue_fingerprint(warning), issue_fingerprint(normalized))
        self.assertNotEqual(
            issue_fingerprint(warning),
            issue_fingerprint(dict(warning, warning={
                "source_file": "questions.tex", "line": 13, "width": "0.4588pt"
            })),
        )

    def test_cross_paper_fingerprint_sorts_targets_and_uses_conflict_code(self):
        cross = issue(
            paper_id=None,
            affected_paper_ids=["paper-b", "paper-a"],
            conflict_code="region-path-conflict",
        )
        sorted_targets = dict(cross, affected_paper_ids=["paper-a", "paper-b"])
        other_conflict = dict(cross, conflict_code="other")
        self.assertEqual(issue_fingerprint(cross), issue_fingerprint(sorted_targets))
        self.assertNotEqual(
            issue_fingerprint(cross), issue_fingerprint(other_conflict)
        )

    def test_source_fingerprint_uses_type_and_source_id(self):
        source = issue(
            paper_id=None,
            type="source-unavailable",
            source_id="src-a",
        )
        source.pop("conflict_code")
        self.assertNotEqual(
            issue_fingerprint(source),
            issue_fingerprint(dict(source, source_id="src-b")),
        )
        self.assertNotEqual(
            issue_fingerprint(source),
            issue_fingerprint(dict(source, type="source-unreadable")),
        )

    def test_blocks_completion_uses_target_impact_and_all_unresolved_statuses(self):
        for status in ("open", "investigating", "deferred"):
            value = issue(status=status)
            self.assertTrue(
                blocks_completion(value, "gk-2026-regular-national-1-recall")
            )
            self.assertFalse(blocks_completion(value, "other-paper"))
        self.assertFalse(blocks_completion(
            issue(status="resolved"), "gk-2026-regular-national-1-recall"
        ))
        self.assertFalse(blocks_completion(
            issue(impact="non_blocking"), "gk-2026-regular-national-1-recall"
        ))
        cross = issue(
            paper_id=None,
            affected_paper_ids=["paper-a", "paper-b"],
        )
        self.assertTrue(blocks_completion(cross, "paper-a"))
        self.assertFalse(blocks_completion(cross, "paper-c"))

    def test_upsert_reuses_stable_number_is_idempotent_and_keeps_other_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing-issues.md"
            first = issue()
            second = issue(
                paper_id=None,
                affected_paper_ids=["paper-a", "paper-b"],
                conflict_code="region-path-conflict",
            )
            first_id = upsert_issue(path, first)
            second_id = upsert_issue(path, second)
            self.assertEqual((first_id, second_id), ("ISSUE-0001", "ISSUE-0002"))
            before = path.read_bytes()
            self.assertEqual(upsert_issue(path, second), "ISSUE-0002")
            self.assertEqual(path.read_bytes(), before)

            updated = dict(first, status="investigating", resume_action="核验中")
            self.assertEqual(upsert_issue(path, updated), "ISSUE-0001")
            loaded = load_issues(path)
            self.assertEqual([item["issue_id"] for item in loaded], [
                "ISSUE-0001", "ISSUE-0002"
            ])
            self.assertEqual(loaded[0]["status"], "investigating")
            self.assertEqual(loaded[1]["conflict_code"], "region-path-conflict")

    def test_same_paper_and_type_with_different_visual_identity_get_new_numbers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing-issues.md"
            base = issue(
                type="layout-warning", edition="印刷版", page=1,
                check_code="overfull-hbox", figure_id=None,
                warning={"source_file": "questions.tex", "line": 10, "width": "1pt"},
            )
            identifiers = [upsert_issue(path, base)]
            for updates in (
                {"edition": "解析版"},
                {"page": 2},
                {"warning": {"source_file": "questions.tex", "line": 11, "width": "1pt"}},
                {"figure_id": "fig-1"},
            ):
                identifiers.append(upsert_issue(path, dict(base, **updates)))
            self.assertEqual(identifiers, [
                "ISSUE-0001", "ISSUE-0002", "ISSUE-0003",
                "ISSUE-0004", "ISSUE-0005",
            ])
            self.assertEqual(len(load_issues(path)), 5)

    def test_load_rejects_missing_fields_unknown_enums_bad_targets_and_duplicates(self):
        valid = issue()
        cases = {}
        missing = dict(valid)
        missing.pop("resume_action")
        cases["resume_action"] = "# 问题总账\n\n" + block("ISSUE-0001", missing)
        cases["未知 status"] = "# 问题总账\n\n" + block(
            "ISSUE-0001", dict(valid, status="closed")
        )
        cases["未知 impact"] = "# 问题总账\n\n" + block(
            "ISSUE-0001", dict(valid, impact="fatal")
        )
        no_target = dict(valid, paper_id=None, affected_paper_ids=[])
        no_target["fingerprint"] = "0" * 64
        cases["目标"] = "# 问题总账\n\n" + block("ISSUE-0001", no_target)
        cases["affected_paper_ids"] = "# 问题总账\n\n" + block(
            "ISSUE-0001", dict(
                valid, paper_id=None, affected_paper_ids=["paper-b", "paper-a"]
            )
        )
        duplicate_id = "# 问题总账\n\n" + block("ISSUE-0001", valid)
        duplicate_id += "\n" + block("ISSUE-0001", dict(valid, conflict_code="other"))
        cases["重复问题编号"] = duplicate_id
        duplicate_fp = "# 问题总账\n\n" + block("ISSUE-0001", valid)
        duplicate_fp += "\n" + block("ISSUE-0002", valid)
        cases["重复 fingerprint"] = duplicate_fp
        stale = dict(valid, fingerprint="0" * 64)
        cases["fingerprint"] = "# 问题总账\n\n" + block("ISSUE-0001", stale)
        cases["问题编号格式"] = (
            "# 问题总账\n\n"
            + block("ISSUE-1", valid)
        )
        duplicate_json_key = block("ISSUE-0001", valid).replace(
            '  "status": "open",',
            '  "status": "open",\n  "status": "resolved",',
        )
        cases["重复 JSON 字段"] = "# 问题总账\n\n" + duplicate_json_key
        cases["问题编号格式错误"] = (
            "# 问题总账\n\n"
            + block("ISSUE-0001", valid)
            + "\n## ISSUE-bad\n\n```json\n{}\n```\n"
        )
        blank_target = dict(valid, paper_id=" ")
        blank_target["fingerprint"] = "0" * 64
        cases["paper_id"] = "# 问题总账\n\n" + block(
            "ISSUE-0001", blank_target
        )
        blank_affected = dict(
            valid, paper_id=None, affected_paper_ids=["paper-a", " "]
        )
        blank_affected["fingerprint"] = "0" * 64
        cases["affected_paper_ids"] = "# 问题总账\n\n" + block(
            "ISSUE-0001", blank_affected
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "issues.md"
            for expected, raw in cases.items():
                with self.subTest(expected=expected):
                    path.write_text(raw, encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, expected):
                        load_issues(path)

    def test_phase0_seed_cli_writes_stable_forward_references_and_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing-issues.md"
            self.assertEqual(main([
                "init", "--phase0-seed", "--output", str(path)
            ]), 0)
            before = path.read_bytes()
            self.assertEqual(main([
                "init", "--phase0-seed", "--output", str(path)
            ]), 0)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(main(["validate", "--file", str(path)]), 0)
            loaded = load_issues(path)
            self.assertEqual([item["issue_id"] for item in loaded], [
                "ISSUE-0001", "ISSUE-0002"
            ])
            self.assertEqual(loaded[0]["type"], "identity-ambiguous")
            self.assertEqual(
                loaded[0]["paper_id"],
                "gk-2026-regular-national-1-recall",
            )
            self.assertEqual(loaded[0]["affected_paper_ids"], [])
            self.assertIsNone(loaded[1]["paper_id"])
            self.assertEqual(loaded[1]["affected_paper_ids"], [
                "gk-2017-regular-national-1-arts",
                "gk-2017-regular-national-1-science",
            ])
            self.assertEqual(
                [item["status"] for item in loaded], ["open", "open"]
            )
            self.assertEqual(
                [item["impact"] for item in loaded],
                ["blocks_completion", "blocks_completion"],
            )

            path.write_text("# unrelated ledger\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "不同"):
                main(["init", "--phase0-seed", "--output", str(path)])
            self.assertEqual(path.read_text(encoding="utf-8"), "# unrelated ledger\n")

    def test_cli_required_arguments_are_enforced(self):
        for args in (["init", "--output", "x"], ["validate"]):
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    main(args)
                self.assertEqual(raised.exception.code, 2)

    def test_cli_process_exit_codes_are_zero_one_and_two(self):
        script = ROOT / "tools" / "issues.py"
        valid = ROOT / "missing-issues.md"
        passed = subprocess.run(
            [sys.executable, str(script), "validate", "--file", str(valid)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(passed.returncode, 0, passed.stderr)
        runtime_error = subprocess.run(
            [sys.executable, str(script), "validate", "--file", str(valid) + ".missing"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(runtime_error.returncode, 1)
        usage_error = subprocess.run(
            [sys.executable, str(script), "validate"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(usage_error.returncode, 2)


if __name__ == "__main__":
    unittest.main()

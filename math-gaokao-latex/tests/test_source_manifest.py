import copy
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from manifest import canonical_json
from source_manifest import (
    build_inventory,
    git_tree,
    main,
    merge_inventory,
    parse_ls_tree,
    source_id,
)

ENTRIES = [{
    "mode": "100644",
    "oid": "a" * 40,
    "path": "普通高考/2021/2021新高考1(山东).pdf",
}]


class SourceManifestTests(unittest.TestCase):
    def test_parse_nul_ls_tree_preserves_spaces_and_rejects_malformed_records(self):
        raw = (
            b"100644 blob " + b"a" * 40
            + b"\t\xe6\x99\xae\xe9\x80\x9a\xe9\xab\x98\xe8\x80\x83/2021/a b.pdf\0"
        )
        self.assertEqual(parse_ls_tree(raw), [{
            "mode": "100644",
            "oid": "a" * 40,
            "path": "普通高考/2021/a b.pdf",
        }])
        for malformed in (
            b"100644 blob " + b"a" * 40 + b"\tmissing-nul",
            b"100644 tree " + b"a" * 40 + b"\tx\0",
            b"100644 blob not-an-oid\tx\0",
            b"100644 blob " + b"a" * 40 + b"\tbad\xff\0",
        ):
            with self.subTest(raw=malformed):
                with self.assertRaises(ValueError):
                    parse_ls_tree(malformed)

    def test_git_tree_uses_nul_full_tree_without_long_or_lazy_fetch(self):
        completed = subprocess.CompletedProcess(
            args=[], returncode=0,
            stdout=b"100644 blob " + b"a" * 40 + b"\tordinary.pdf\0",
            stderr=b"",
        )
        with mock.patch("source_manifest.subprocess.run", return_value=completed) as run:
            entries = git_tree(Path("/repo"), "c" * 40)
        self.assertEqual(entries[0]["path"], "ordinary.pdf")
        args = run.call_args.args[0]
        self.assertEqual(
            args,
            ["git", "-C", "/repo", "ls-tree", "-r", "-z", "--full-tree", "c" * 40],
        )
        self.assertNotIn("--long", args)
        self.assertEqual(run.call_args.kwargs["env"]["GIT_NO_LAZY_FETCH"], "1")
        self.assertTrue(run.call_args.kwargs["check"])

    def test_source_id_is_stable_and_includes_url_commit_and_path(self):
        value = source_id("https://example.invalid/r", "c" * 40, ENTRIES[0]["path"])
        self.assertEqual(value, source_id(
            "https://example.invalid/r", "c" * 40, ENTRIES[0]["path"]
        ))
        self.assertTrue(value.startswith("src-"))
        self.assertNotEqual(value, source_id("other", "c" * 40, ENTRIES[0]["path"]))
        self.assertNotEqual(value, source_id(
            "https://example.invalid/r", "d" * 40, ENTRIES[0]["path"]
        ))
        self.assertNotEqual(value, source_id(
            "https://example.invalid/r", "c" * 40, "普通高考/2021/other.pdf"
        ))

    def test_build_inventory_uses_only_pdf_roots_and_does_not_guess_identity(self):
        entries = ENTRIES + [
            {"mode": "100644", "oid": "b" * 40,
             "path": "春季高考/2000/2000春季上海.pdf"},
            {"mode": "100644", "oid": "c" * 40,
             "path": "普通高考/2004/北京和全国3卷为旧课程.txt"},
            {"mode": "100644", "oid": "d" * 40, "path": "README.md"},
        ]
        manifest = build_inventory(entries, "u", "c")
        self.assertEqual(manifest["inventory"], {
            "total_sources": 2,
            "root_counts": {"regular": 1, "spring": 1},
        })
        self.assertEqual(manifest["upstream"]["scoped_roots"], ["普通高考", "春季高考"])
        regular = next(
            source for source in manifest["sources"]
            if source["exam_type"] == "regular"
        )
        self.assertEqual(regular["year"], 2021)
        self.assertEqual(regular["raw_paper_name"], "2021新高考1(山东).pdf")
        self.assertIsNone(regular["track"])
        self.assertEqual(regular["regions"], [])
        self.assertEqual(regular["source_state"], "not_started")
        self.assertIsNone(regular["paper_relation"])
        self.assertIsNone(regular["paper_id"])
        self.assertIsNone(regular["artifact"])
        self.assertEqual(regular["issue_ids"], [])

    def test_merge_preserves_human_runtime_and_unknown_top_level_state(self):
        old = build_inventory(ENTRIES, "u", "c")
        old["sources"][0].update({
            "track": "none", "regions": ["山东"], "source_state": "ready",
            "paper_relation": "canonical", "paper_id": "p",
            "artifact": {"sha256": "b" * 64}, "issue_ids": ["ISSUE-9"],
            "future_source_state": {"reviewed": True},
        })
        old["papers"] = [{"paper_id": "p"}]
        old["batches"] = [{"batch_id": "phase0-b01"}]
        old["future_top_level"] = {"owned_by": "task-99"}
        fresh = build_inventory(ENTRIES, "u", "c")
        merged = merge_inventory(old, fresh)
        self.assertEqual(merged["sources"][0]["regions"], ["山东"])
        self.assertEqual(merged["sources"][0]["artifact"]["sha256"], "b" * 64)
        self.assertEqual(merged["sources"][0]["future_source_state"], {"reviewed": True})
        self.assertEqual(merged["papers"], old["papers"])
        self.assertEqual(merged["batches"], old["batches"])
        self.assertEqual(merged["future_top_level"], old["future_top_level"])
        self.assertIsNot(merged, old)
        self.assertIsNot(merged["sources"][0], old["sources"][0])

    def test_merge_refreshes_only_owned_fields_and_counts(self):
        old = build_inventory(ENTRIES, "u", "c")
        old["inventory"] = {"total_sources": 9, "root_counts": {"regular": 9}}
        fresh_entries = copy.deepcopy(ENTRIES)
        fresh_entries[0]["mode"] = "100755"
        fresh = build_inventory(fresh_entries, "u", "c")
        merged = merge_inventory(old, fresh)
        self.assertEqual(merged["inventory"], fresh["inventory"])
        for field in (
            "source_id", "upstream_path", "git_blob_oid", "year",
            "exam_type", "raw_paper_name",
        ):
            self.assertEqual(merged["sources"][0][field], fresh["sources"][0][field])

    def test_merge_rejects_source_set_path_oid_and_upstream_drift(self):
        old = build_inventory(ENTRIES, "u", "c")
        mutations = []
        extra = build_inventory(ENTRIES + [{
            "mode": "100644", "oid": "b" * 40,
            "path": "普通高考/2022/other.pdf",
        }], "u", "c")
        mutations.append(extra)
        changed_path = build_inventory([{**ENTRIES[0], "path": "普通高考/2021/other.pdf"}], "u", "c")
        mutations.append(changed_path)
        changed_oid = build_inventory([{**ENTRIES[0], "oid": "b" * 40}], "u", "c")
        mutations.append(changed_oid)
        mutations.append(build_inventory(ENTRIES, "other", "c"))
        mutations.append(build_inventory(ENTRIES, "u", "d"))
        for fresh in mutations:
            with self.subTest(fresh=fresh["upstream"]):
                with self.assertRaises(ValueError):
                    merge_inventory(old, fresh)

    def test_inventory_cli_output_merge_check_and_expectations(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "upstream"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            (repo / "普通高考" / "2021").mkdir(parents=True)
            (repo / "春季高考" / "2000").mkdir(parents=True)
            (repo / "普通高考" / "2021" / "a.pdf").write_bytes(b"pdf-a")
            (repo / "春季高考" / "2000" / "b.pdf").write_bytes(b"pdf-b")
            (repo / "普通高考" / "2004").mkdir()
            (repo / "普通高考" / "2004" / "北京和全国3卷为旧课程.txt").write_text("x")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "seed"], check=True)
            commit = subprocess.check_output(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
            ).strip()
            subprocess.run(
                ["git", "-C", str(repo), "remote", "add", "origin", "https://example.invalid/upstream"],
                check=True,
            )
            output = Path(tmp) / "source-manifest.json"
            args = [
                "inventory", "--repo", str(repo), "--commit", commit,
                "--output", str(output), "--expect-total", "2",
                "--expect-root", "regular=1", "--expect-root", "spring=1",
            ]
            self.assertEqual(main(args), 0)
            original = output.read_bytes()
            data = json.loads(original.decode("utf-8"))
            data["sources"][0]["regions"] = ["保留"]
            data["future_top_level"] = {"keep": True}
            output.write_text(canonical_json(data), encoding="utf-8")
            self.assertEqual(main(args), 0)
            merged = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(merged["sources"][0]["regions"], ["保留"])
            self.assertEqual(merged["future_top_level"], {"keep": True})

            check_args = [
                "inventory", "--repo", str(repo), "--commit", commit,
                "--check", str(output), "--expect-total", "2",
                "--expect-root", "regular=1", "--expect-root", "spring=1",
            ]
            before = output.read_bytes()
            self.assertEqual(main(check_args), 0)
            self.assertEqual(output.read_bytes(), before)
            output.write_bytes(before + b"\n")
            with self.assertRaisesRegex(ValueError, "字节"):
                main(check_args)
            output.write_bytes(before)
            wrong_total = list(check_args)
            wrong_total[wrong_total.index("--expect-total") + 1] = "3"
            with self.assertRaisesRegex(ValueError, "总数"):
                main(wrong_total)

            script = ROOT / "tools" / "source_manifest.py"
            passed = subprocess.run(
                [sys.executable, str(script), *check_args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(passed.returncode, 0, passed.stderr)
            runtime_args = list(check_args)
            runtime_args[runtime_args.index("--repo") + 1] = str(
                Path(tmp) / "missing-repo"
            )
            runtime_error = subprocess.run(
                [sys.executable, str(script), *runtime_args],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(runtime_error.returncode, 1)
            usage_error = subprocess.run(
                [sys.executable, str(script), "inventory"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(usage_error.returncode, 2)

    def test_cli_requires_exactly_one_destination_and_unique_root_expectations(self):
        stderr = io.StringIO()
        cases = [
            ["inventory", "--repo", "/r", "--commit", "c" * 40,
             "--expect-total", "1", "--expect-root", "regular=1"],
            ["inventory", "--repo", "/r", "--commit", "c" * 40,
             "--output", "a", "--check", "b", "--expect-total", "1",
             "--expect-root", "regular=1"],
            ["inventory", "--repo", "/r", "--commit", "c" * 40,
             "--output", "a", "--expect-total", "1",
             "--expect-root", "regular=1", "--expect-root", "regular=1"],
        ]
        for args in cases:
            with self.subTest(args=args), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    main(args)
                self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()

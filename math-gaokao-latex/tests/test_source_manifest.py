import copy
import http.server
import io
import json
import os
import hashlib
import signal
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import zipfile
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from issues import load_issues
from manifest import canonical_json, load_manifest
from schema_validate import SchemaError, validate
from transaction import Transaction as RealTransaction
import source_manifest as source_manifest_module
from source_manifest import (
    FetchContext,
    _download_http_to,
    _ensure_codeload_zip,
    _materialize_command,
    build_inventory,
    cache_directory,
    fetch_blob,
    git_tree,
    inspect_existing,
    inspect_pdf,
    main,
    materialize_source,
    materialization_status,
    merge_inventory,
    parse_ls_tree,
    probe_transports,
    safe_zip_member_bytes,
    source_id,
    state_source_result,
    validate_source_manifest,
    verify_fetched_bytes,
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

    def test_merge_preserves_unknown_nested_upstream_metadata(self):
        old = build_inventory(ENTRIES, "u", "c")
        old["upstream"]["future_metadata"] = {
            "mirrors": [{"url": "https://mirror.invalid/upstream"}],
        }
        merged = merge_inventory(old, build_inventory(ENTRIES, "u", "c"))
        self.assertEqual(
            merged["upstream"]["future_metadata"],
            old["upstream"]["future_metadata"],
        )
        self.assertIsNot(
            merged["upstream"]["future_metadata"],
            old["upstream"]["future_metadata"],
        )

    def test_merge_preserves_unknown_nested_inventory_metadata(self):
        old = build_inventory(ENTRIES, "u", "c")
        old["inventory"]["future_metadata"] = {
            "last_scan": {"worker": "inventory-v2"},
        }
        fresh = build_inventory(ENTRIES, "u", "c")
        merged = merge_inventory(old, fresh)
        self.assertEqual(
            merged["inventory"]["future_metadata"],
            old["inventory"]["future_metadata"],
        )
        self.assertIsNot(
            merged["inventory"]["future_metadata"],
            old["inventory"]["future_metadata"],
        )
        self.assertEqual(merged["inventory"]["total_sources"], 1)
        self.assertEqual(
            merged["inventory"]["root_counts"], fresh["inventory"]["root_counts"]
        )

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

    def test_inventory_check_rejects_canonical_manifest_with_invalid_relationship(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "upstream"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "t@example.invalid"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Test"],
                check=True,
            )
            (repo / "普通高考" / "2021").mkdir(parents=True)
            (repo / "普通高考" / "2021" / "a.pdf").write_bytes(b"pdf-a")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "seed"], check=True)
            commit = subprocess.check_output(
                ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
            ).strip()
            subprocess.run(
                [
                    "git", "-C", str(repo), "remote", "add", "origin",
                    "https://example.invalid/upstream",
                ],
                check=True,
            )

            output = Path(tmp) / "source-manifest.json"
            script = ROOT / "tools" / "source_manifest.py"
            common = [
                "inventory", "--repo", str(repo), "--commit", commit,
                "--expect-total", "1", "--expect-root", "regular=1",
                "--expect-root", "spring=0",
            ]
            created = subprocess.run(
                [sys.executable, str(script), *common, "--output", str(output)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(created.returncode, 0, created.stderr)

            manifest = json.loads(output.read_text(encoding="utf-8"))
            source = manifest["sources"][0]
            source.update({
                "source_state": "non_paper",
                "paper_relation": "canonical",
                "paper_id": "paper-1",
            })
            manifest["papers"] = [{
                "paper_id": "paper-1",
                "source_ids": [source["source_id"]],
            }]
            output.write_text(canonical_json(manifest), encoding="utf-8")

            checked = subprocess.run(
                [sys.executable, str(script), *common, "--check", str(output)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertNotEqual(
                checked.returncode, 0, "invalid canonical manifest was accepted"
            )
            self.assertIn("non_paper", checked.stderr)

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


def git_blob_oid(value):
    header = ("blob %d\0" % len(value)).encode("ascii")
    return hashlib.sha1(header + value).hexdigest()


def source_fixture(value=b"%PDF-task-3\n", **updates):
    source = {
        "source_id": "src-" + "1" * 64,
        "upstream_path": "普通高考/2021/a b.pdf",
        "git_blob_oid": git_blob_oid(value),
        "year": 2021,
        "exam_type": "regular",
        "track": None,
        "regions": [],
        "raw_paper_name": "a b.pdf",
        "source_state": "not_started",
        "paper_relation": None,
        "paper_id": None,
        "artifact": None,
        "issue_ids": [],
    }
    source.update(updates)
    return source


def write_pdfinfo(
    directory, *, pages=2, version="24.01", exit_code=0, version_exit_code=0
):
    path = Path(directory) / ("pdfinfo-fake-" + next(tempfile._get_candidate_names()))
    path.write_text(
        "#!/bin/sh\n"
        "if [ \"$1\" = \"-v\" ]; then\n"
        "  echo \"pdfinfo version %s\" >&2\n"
        "  exit %s\n"
        "fi\n"
        "echo \"Pages: %s\"\n"
        "exit %s\n" % (version, version_exit_code, pages, exit_code),
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path.resolve()


def artifact_fixture(value=b"%PDF-task-3\n"):
    return {
        "size_bytes": len(value),
        "sha256": hashlib.sha256(value).hexdigest(),
        "page_count": 2,
        "media_type": "application/pdf",
        "header_is_pdf": True,
        "git_oid_verified": True,
        "pdf_check": "passed",
        "pdfinfo_version": "24.01",
    }


def init_state_repository(directory, source):
    repo = Path(directory) / "project-repo"
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    project = repo / "docs" / "exams" / "math-gaokao-latex"
    (project / "schemas").mkdir(parents=True)
    schema_path = ROOT / "schemas" / "source-manifest.schema.json"
    (project / "schemas" / schema_path.name).write_bytes(schema_path.read_bytes())
    manifest = build_inventory([], "https://example.invalid/upstream", "c" * 40)
    manifest["sources"] = [copy.deepcopy(source)]
    manifest["inventory"] = {
        "total_sources": 1,
        "root_counts": {"regular": 1, "spring": 0},
    }
    manifest_path = project / "source-manifest.json"
    manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
    issues_path = project / "missing-issues.md"
    issues_path.write_text("# issues\n", encoding="utf-8")
    return repo, manifest_path, issues_path


class FakeHttpResponse:
    def __init__(self, chunks, headers=None, on_enter=None, on_read=None):
        self._chunks = list(chunks)
        self.headers = headers or {}
        self.on_enter = on_enter
        self.on_read = on_read
        self.read_timeout = None
        socket = self
        self.fp = type("Fp", (), {})()
        self.fp.raw = type("Raw", (), {})()
        self.fp.raw._sock = socket

    def __enter__(self):
        if self.on_enter is not None:
            self.on_enter()
        return self

    def __exit__(self, *unused):
        return False

    def read(self, unused_size):
        if self.on_read is not None:
            self.on_read()
        return self._chunks.pop(0) if self._chunks else b""

    def settimeout(self, seconds):
        self.read_timeout = seconds


class InjectedTransactionFailure(RuntimeError):
    pass


class MaterializationTests(unittest.TestCase):
    def test_artifact_schema_requires_all_verification_fields(self):
        schema = json.loads(
            (ROOT / "schemas" / "source-manifest.schema.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = build_inventory(
            ENTRIES, "https://example.invalid/upstream", "c" * 40
        )
        artifact = {
            "size_bytes": 12,
            "sha256": "b" * 64,
            "page_count": 2,
            "media_type": "application/pdf",
            "header_is_pdf": True,
            "git_oid_verified": True,
            "pdf_check": "passed",
            "pdfinfo_version": "24.01",
        }
        manifest["sources"][0]["artifact"] = artifact
        validate(manifest, schema)
        for field in tuple(artifact):
            with self.subTest(field=field):
                invalid = copy.deepcopy(manifest)
                del invalid["sources"][0]["artifact"][field]
                with self.assertRaises(SchemaError):
                    validate(invalid, schema)

    def test_source_state_semantics_bind_ready_to_complete_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "schemas").mkdir()
            schema_path = ROOT / "schemas" / "source-manifest.schema.json"
            (project / "schemas" / schema_path.name).write_bytes(schema_path.read_bytes())
            value = b"%PDF-semantic\n"
            cases = [
                ("ready", None),
                ("blocked", artifact_fixture(value)),
                ("not_started", artifact_fixture(value)),
                ("non_paper", artifact_fixture(value)),
            ]
            for state, artifact in cases:
                manifest = build_inventory(
                    ENTRIES, "https://example.invalid/upstream", "c" * 40
                )
                manifest["sources"][0]["source_state"] = state
                manifest["sources"][0]["artifact"] = artifact
                path = project / (state + ".json")
                path.write_text(canonical_json(manifest), encoding="utf-8")
                with self.subTest(state=state), self.assertRaisesRegex(
                    ValueError, "artifact|ready"
                ):
                    validate_source_manifest(path)

            manifest["sources"][0]["source_state"] = "ready"
            manifest["sources"][0]["artifact"] = artifact_fixture(value)
            valid_path = project / "valid.json"
            valid_path.write_text(canonical_json(manifest), encoding="utf-8")
            self.assertEqual(validate_source_manifest(valid_path, 1), 1)

    def test_ready_failure_clears_artifact_and_all_resume_converges(self):
        value = b"%PDF-resume\n"
        source = source_fixture(
            value, source_state="ready", artifact=artifact_fixture(value)
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            subprocess.run(
                ["git", "-C", str(upstream), "hash-object", "-w", "--stdin"],
                input=value,
                check=True,
                stdout=subprocess.PIPE,
            )
            target = upstream / source["upstream_path"]
            target.parent.mkdir(parents=True)
            target.write_bytes(b"different")
            pdfinfo = write_pdfinfo(tmp)
            common = [
                "materialize", "--repo", str(upstream),
                "--manifest", str(manifest_path), "--issues", str(issues_path),
                "--jobs", "1", "--deadline-seconds", "30",
                "--pdfinfo", str(pdfinfo),
            ]
            with mock.patch("source_manifest.probe_transports", return_value={"ok": True}):
                self.assertEqual(main(common + ["--source", source["source_id"]]), 1)
            failed = load_manifest(manifest_path)
            failed_source = failed["sources"][0]
            self.assertEqual(failed_source["source_state"], "blocked")
            self.assertIsNone(failed_source["artifact"])
            issue_id = failed_source["issue_ids"][0]
            self.assertEqual(load_issues(issues_path)[0]["status"], "open")

            target.unlink()
            with mock.patch("source_manifest.probe_transports", return_value={"ok": True}):
                self.assertEqual(main(common + ["--all"]), 0)
            completed = load_manifest(manifest_path)
            completed_source = completed["sources"][0]
            self.assertEqual(completed_source["source_state"], "ready")
            self.assertEqual(completed_source["artifact"], artifact_fixture(value))
            self.assertNotIn(issue_id, completed_source["issue_ids"])
            issues = load_issues(issues_path)
            self.assertEqual(len(issues), 1)
            self.assertEqual(issues[0]["issue_id"], issue_id)
            self.assertEqual(issues[0]["status"], "resolved")

    def test_existing_mismatch_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "x.pdf"
            target.write_bytes(b"local")
            source = source_fixture()
            with self.assertRaisesRegex(RuntimeError, "已有文件与固定 blob 不一致"):
                materialize_source(
                    source, target=target,
                    fetcher=lambda _: b"%PDF-never-used",
                    pdfinfo=write_pdfinfo(tmp),
                )
            self.assertEqual(target.read_bytes(), b"local")

    def test_fallback_bytes_must_match_git_oid_and_pdf_header(self):
        with self.assertRaisesRegex(RuntimeError, "blob OID"):
            verify_fetched_bytes(
                source_fixture(oid="a" * 40), b"%PDF-wrong"
            )
        plain = b"not-a-pdf"
        with self.assertRaisesRegex(RuntimeError, "%PDF-"):
            verify_fetched_bytes(source_fixture(plain), plain)

    def test_pdfinfo_is_required_to_succeed_with_positive_page_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "x.pdf"
            pdf.write_bytes(b"%PDF-test")
            inspected = inspect_pdf(pdf, write_pdfinfo(tmp))
            self.assertEqual(inspected, {
                "page_count": 2,
                "pdf_check": "passed",
                "pdfinfo_version": "24.01",
            })
            with self.assertRaisesRegex(RuntimeError, "pdfinfo"):
                inspect_pdf(pdf, write_pdfinfo(tmp, exit_code=7))
            with self.assertRaisesRegex(RuntimeError, "Pages"):
                inspect_pdf(pdf, write_pdfinfo(tmp, pages=0))
            with self.assertRaisesRegex(ValueError, "绝对路径"):
                inspect_pdf(pdf, Path("pdfinfo"))

    def test_pdfinfo_global_preflight_rejects_tool_failures_without_writes(self):
        value = b"%PDF-tool\n"
        source = source_fixture(value)
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            before_manifest = manifest_path.read_bytes()
            before_issues = issues_path.read_bytes()

            nonexistent = Path(tmp) / "missing-pdfinfo"
            non_executable = Path(tmp) / "non-executable"
            non_executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            broken = Path(tmp) / "broken"
            broken.mkdir()
            bad_exit = write_pdfinfo(tmp, version_exit_code=7)
            bad_version = write_pdfinfo(tmp, version="")
            valid = write_pdfinfo(tmp, version="24.02")
            cases = [nonexistent, non_executable, broken, bad_exit, bad_version]
            for tool in cases:
                with self.subTest(tool=tool), mock.patch(
                    "source_manifest.probe_transports"
                ) as probe, self.assertRaisesRegex(
                    (ValueError, RuntimeError), "pdfinfo"
                ):
                    main([
                        "materialize", "--repo", str(upstream),
                        "--manifest", str(manifest_path),
                        "--issues", str(issues_path), "--all", "--jobs", "1",
                        "--deadline-seconds", "10", "--pdfinfo", str(tool),
                    ])
                probe.assert_not_called()
                self.assertEqual(manifest_path.read_bytes(), before_manifest)
                self.assertEqual(issues_path.read_bytes(), before_issues)
            self.assertEqual(
                source_manifest_module.validate_pdfinfo_tool(valid), "24.02"
            )

    def test_materialize_atomically_creates_target_and_returns_full_artifact(self):
        value = b"%PDF-created\n"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "source.pdf"
            artifact = materialize_source(
                source_fixture(value), target=target,
                fetcher=lambda _: value, pdfinfo=write_pdfinfo(tmp),
            )
            self.assertEqual(target.read_bytes(), value)
            self.assertEqual(artifact["sha256"], hashlib.sha256(value).hexdigest())
            self.assertEqual(artifact["size_bytes"], len(value))
            self.assertEqual(artifact["page_count"], 2)
            self.assertTrue(artifact["header_is_pdf"])
            self.assertTrue(artifact["git_oid_verified"])

    def test_cache_uses_resolved_git_dir_rejects_corruption_and_reuses_verified_blob(self):
        value = b"%PDF-cache\n"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "upstream"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            oid = subprocess.check_output(
                ["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                input=value,
            ).decode("ascii").strip()
            source = source_fixture(value, git_blob_oid=oid)
            cache = cache_directory(repo)
            self.assertEqual(cache, (repo / ".git" / "gaokao-pdf-cache").resolve())
            cache.mkdir(parents=True)
            cached = cache / (oid + ".pdf")
            cached.write_bytes(b"%PDF-corrupt")
            context = FetchContext(
                commit="c" * 40, pdfinfo=write_pdfinfo(tmp),
                sleep=lambda _: None,
            )
            self.assertEqual(fetch_blob(repo, source, cache, context).read_bytes(), value)
            with mock.patch("source_manifest._git_cat_file", side_effect=AssertionError):
                self.assertEqual(
                    fetch_blob(repo, source, cache, context).read_bytes(), value
                )

    def test_linked_worktree_cache_resolves_gitfile_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "main"
            linked = Path(tmp) / "linked"
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@x"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "T"], check=True)
            (repo / "x").write_text("x", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "x"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "seed"], check=True)
            subprocess.run([
                "git", "-C", str(repo), "worktree", "add", "-q", "-b", "linked",
                str(linked),
            ], check=True)
            expected = subprocess.check_output(
                ["git", "-C", str(linked), "rev-parse", "--git-dir"], text=True
            ).strip()
            expected_path = Path(expected)
            if not expected_path.is_absolute():
                expected_path = linked / expected_path
            self.assertEqual(
                cache_directory(linked),
                expected_path.resolve() / "gaokao-pdf-cache",
            )

    def test_lazy_git_blob_fetch_removes_inherited_no_lazy_fetch(self):
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=b"blob", stderr=b""
        )
        with mock.patch.dict(os.environ, {"GIT_NO_LAZY_FETCH": "1"}), mock.patch(
            "source_manifest.subprocess.run", return_value=completed
        ) as run:
            self.assertEqual(
                source_manifest_module._git_cat_file(Path("/repo"), "a" * 40),
                b"blob",
            )
        environment = run.call_args.kwargs["env"]
        self.assertNotIn("GIT_NO_LAZY_FETCH", environment)

    def test_fetch_retries_git_with_fixed_backoff_then_raw_encoded_path(self):
        value = b"%PDF-fallback\n"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            source = source_fixture(value)
            sleeps = []
            context = FetchContext(
                commit="d" * 40, pdfinfo=write_pdfinfo(tmp), sleeps=sleeps,
                sleep=sleeps.append,
            )

            def raw_download(url, destination, limit, _context):
                self.assertIn("a%20b.pdf", url)
                self.assertEqual(limit, 100 * 1024 * 1024)
                destination.write_bytes(value)

            with mock.patch("source_manifest._git_cat_file", side_effect=RuntimeError("git")) as cat, \
                    mock.patch("source_manifest._download_http_to", side_effect=raw_download) as download, \
                    mock.patch("source_manifest._zip_member_to_cache") as zip_fallback:
                result = fetch_blob(repo, source, cache_directory(repo), context)
            self.assertEqual(result.read_bytes(), value)
            self.assertEqual(cat.call_count, 3)
            self.assertEqual(sleeps, [2, 5, 10])
            self.assertEqual(download.call_count, 1)
            zip_fallback.assert_not_called()

    def test_wrong_raw_oid_falls_back_to_zip_and_zip_downloads_once_per_context(self):
        first = b"%PDF-first\n"
        second = b"%PDF-second\n"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            context = FetchContext(
                commit="e" * 40, pdfinfo=write_pdfinfo(tmp), sleep=lambda _: None,
            )

            sources = [
                source_fixture(first, raw_paper_name="first.pdf", upstream_path="普通高考/2021/first.pdf"),
                source_fixture(second, raw_paper_name="second.pdf", upstream_path="普通高考/2021/second.pdf"),
            ]
            def download(url, destination, limit, _context):
                if "raw.githubusercontent" in url:
                    destination.write_bytes(b"%PDF-wrong")
                    return
                self.assertIn("codeload.github.com", url)
                self.assertEqual(limit, 1024 * 1024 * 1024)
                with zipfile.ZipFile(str(destination), "w") as archive:
                    for source, value in zip(sources, (first, second)):
                        archive.writestr(
                            "gaokaomath-%s/%s" % (
                                context.commit, source["upstream_path"]
                            ),
                            value,
                        )

            with mock.patch("source_manifest._git_cat_file", side_effect=RuntimeError("git")), \
                    mock.patch("source_manifest._download_http_to", side_effect=download) as downloaded:
                for source in sources:
                    self.assertEqual(
                        fetch_blob(repo, source, cache_directory(repo), context).read_bytes(),
                        first if source is sources[0] else second,
                    )
            self.assertEqual(downloaded.call_count, 3)
            self.assertEqual(context.zip_download_count, 1)

    def test_total_deadline_stops_before_new_transport(self):
        value = b"%PDF-deadline\n"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            context = FetchContext(
                commit="f" * 40, pdfinfo=write_pdfinfo(tmp),
                deadline=1.0, monotonic=lambda: 2.0, sleep=lambda _: None,
            )
            with mock.patch("source_manifest._git_cat_file") as cat:
                with self.assertRaisesRegex(RuntimeError, "deadline"):
                    fetch_blob(repo, source_fixture(value), cache_directory(repo), context)
            cat.assert_not_called()

    def test_http_content_length_stream_limits_deadlines_and_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "download.tmp"
            clock = {"now": 0.0}
            context = FetchContext(
                commit="a" * 40,
                pdfinfo=write_pdfinfo(tmp),
                deadline=30.0,
                monotonic=lambda: clock["now"],
                read_deadline_seconds=5,
                raw_limit=5,
            )

            cases = [
                (
                    FakeHttpResponse([], {"Content-Length": "6"}),
                    "超过限制",
                ),
                (
                    FakeHttpResponse([b"abc", b"def"]),
                    "超过限制",
                ),
                (
                    FakeHttpResponse([b"abc"], {"Content-Length": "4"}),
                    "长度不符",
                ),
            ]
            for response, expected in cases:
                destination.unlink(missing_ok=True)
                with self.subTest(expected=expected), mock.patch(
                    "source_manifest.urllib.request.urlopen", return_value=response
                ), self.assertRaisesRegex(RuntimeError, expected):
                    _download_http_to("https://example.invalid/a", destination, 5, context)
                self.assertFalse(destination.exists())

            def slow_connect():
                clock["now"] = 31.0

            slow_connect_response = FakeHttpResponse([], on_enter=slow_connect)
            with mock.patch(
                "source_manifest.urllib.request.urlopen",
                return_value=slow_connect_response,
            ), self.assertRaisesRegex(RuntimeError, "deadline"):
                _download_http_to("https://example.invalid/connect", destination, 5, context)
            self.assertFalse(destination.exists())

            clock["now"] = 0.0
            reads = {"count": 0}

            def slow_read():
                reads["count"] += 1
                clock["now"] = 6.0 if reads["count"] > 1 else 1.0

            slow_read_response = FakeHttpResponse(
                [b"a", b"b"], on_read=slow_read
            )
            with mock.patch(
                "source_manifest.urllib.request.urlopen",
                return_value=slow_read_response,
            ), self.assertRaisesRegex(RuntimeError, "读取 deadline"):
                _download_http_to("https://example.invalid/read", destination, 5, context)
            self.assertFalse(destination.exists())
            self.assertGreater(slow_read_response.read_timeout, 0)
            self.assertLessEqual(slow_read_response.read_timeout, 5.0)

    def test_http_production_path_streams_limits_times_out_and_cleans_up(self):
        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, unused_format, *unused_args):
                pass

            def do_GET(self):
                if self.path == "/declared-too-large":
                    self.send_response(200)
                    self.send_header("Content-Length", "6")
                    self.end_headers()
                    return
                if self.path == "/stream-too-large":
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"abc")
                    self.wfile.flush()
                    self.wfile.write(b"def")
                    return
                if self.path == "/short":
                    self.send_response(200)
                    self.send_header("Content-Length", "4")
                    self.end_headers()
                    self.wfile.write(b"abc")
                    return
                if self.path == "/slow":
                    self.send_response(200)
                    self.send_header("Content-Length", "1")
                    self.end_headers()
                    self.wfile.flush()
                    time.sleep(0.2)
                    try:
                        self.wfile.write(b"x")
                    except BrokenPipeError:
                        pass
                    return
                self.send_response(200)
                self.send_header("Content-Length", "3")
                self.end_headers()
                self.wfile.write(b"abc")

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = "http://127.0.0.1:%d" % server.server_address[1]
            with tempfile.TemporaryDirectory() as tmp:
                destination = Path(tmp) / "download.tmp"

                def context(read_deadline=2.0):
                    return FetchContext(
                        commit="a" * 40,
                        pdfinfo=write_pdfinfo(tmp),
                        deadline=time.monotonic() + 5.0,
                        http_timeout=1,
                        read_deadline_seconds=read_deadline,
                    )

                for endpoint, expected in (
                    ("/declared-too-large", "超过限制"),
                    ("/stream-too-large", "超过限制"),
                    ("/short", "长度不符"),
                ):
                    with self.subTest(endpoint=endpoint), self.assertRaisesRegex(
                        RuntimeError, expected
                    ):
                        _download_http_to(
                            base + endpoint, destination, 5, context()
                        )
                    self.assertFalse(destination.exists())

                with self.assertRaisesRegex(RuntimeError, "读取 deadline"):
                    _download_http_to(
                        base + "/slow", destination, 5, context(0.05)
                    )
                self.assertFalse(destination.exists())

                _download_http_to(base + "/ok", destination, 5, context())
                self.assertEqual(destination.read_bytes(), b"abc")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_preflight_git_subprocesses_are_bounded_by_total_remaining(self):
        context = FetchContext(
            commit="a" * 40,
            pdfinfo=Path("/absolute/pdfinfo"),
            deadline=10.0,
            monotonic=lambda: 4.0,
        )
        tree_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=b"", stderr=b""
        )
        with mock.patch(
            "source_manifest.subprocess.run", return_value=tree_result
        ) as run:
            self.assertEqual(
                git_tree(Path("/repo"), "a" * 40, context=context), []
            )
        self.assertEqual(run.call_args.kwargs["timeout"], 6.0)
        self.assertEqual(
            run.call_args.kwargs["env"]["GIT_NO_LAZY_FETCH"], "1"
        )

        exists_result = subprocess.CompletedProcess(
            args=[], returncode=1, stdout=b"", stderr=b""
        )
        with mock.patch(
            "source_manifest.subprocess.run", return_value=exists_result
        ) as run:
            self.assertFalse(
                source_manifest_module._git_has_blob(
                    Path("/repo"), "b" * 40, context=context
                )
            )
        self.assertEqual(run.call_args.kwargs["timeout"], 6.0)
        self.assertEqual(
            run.call_args.kwargs["env"]["GIT_NO_LAZY_FETCH"], "1"
        )

        git_dir_result = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=".git\n", stderr=""
        )
        with mock.patch(
            "source_manifest.subprocess.run", return_value=git_dir_result
        ) as run:
            self.assertEqual(
                cache_directory(Path("/repo"), context=context),
                Path("/repo/.git/gaokao-pdf-cache"),
            )
        self.assertEqual(run.call_args.kwargs["timeout"], 6.0)

    def test_total_deadline_includes_transport_preflight(self):
        value = b"%PDF-preflight-deadline\n"
        source = source_fixture(value)
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            before = (manifest_path.read_bytes(), issues_path.read_bytes())
            clock = {"now": 100.0}

            def preflight(unused_repo, unused_commit, unused_pdfinfo, context=None):
                self.assertIsNotNone(context)
                clock["now"] = 111.0
                context.check_deadline()

            arguments = source_manifest_module._parser().parse_args([
                "materialize", "--repo", str(upstream),
                "--manifest", str(manifest_path), "--issues", str(issues_path),
                "--all", "--jobs", "1", "--deadline-seconds", "10",
                "--pdfinfo", str(write_pdfinfo(tmp)),
            ])
            with mock.patch("source_manifest.time.monotonic", side_effect=lambda: clock["now"]), \
                    mock.patch("source_manifest.probe_transports", side_effect=preflight):
                with self.assertRaisesRegex(RuntimeError, "deadline"):
                    _materialize_command(arguments)
            self.assertEqual((manifest_path.read_bytes(), issues_path.read_bytes()), before)

    def test_safe_zip_rejects_traversal_absolute_symlink_and_requires_exact_member(self):
        wanted = "gaokaomath-%s/普通高考/2021/a.pdf" % ("a" * 40)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            valid = tmp_path / "valid.zip"
            with zipfile.ZipFile(str(valid), "w") as archive:
                archive.writestr(wanted, b"%PDF-safe")
            self.assertEqual(safe_zip_member_bytes(valid, wanted), b"%PDF-safe")

            cases = {
                "traversal.zip": ("../escape", None),
                "absolute.zip": ("/absolute", None),
                "symlink.zip": ("link", (stat.S_IFLNK | 0o777) << 16),
            }
            for name, (member, attributes) in cases.items():
                archive_path = tmp_path / name
                with zipfile.ZipFile(str(archive_path), "w") as archive:
                    info = zipfile.ZipInfo(member)
                    if attributes is not None:
                        info.create_system = 3
                        info.external_attr = attributes
                    archive.writestr(info, b"x")
                    archive.writestr(wanted, b"%PDF-safe")
                with self.subTest(name=name), self.assertRaisesRegex(RuntimeError, "ZIP"):
                    safe_zip_member_bytes(archive_path, wanted)
            with self.assertRaisesRegex(RuntimeError, "精确成员"):
                safe_zip_member_bytes(valid, wanted + ".other")

    def test_zip_is_validated_once_per_context_and_revalidated_next_command(self):
        first = b"%PDF-zip-first\n"
        second = b"%PDF-zip-second\n"
        commit = "b" * 40
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp) / "cache"
            cache.mkdir()
            zip_path = cache / (commit + ".zip")
            members = [
                "gaokaomath-%s/普通高考/2021/%s.pdf" % (commit, name)
                for name in ("first", "second")
            ]
            with zipfile.ZipFile(str(zip_path), "w") as archive:
                archive.writestr(members[0], first)
                archive.writestr(members[1], second)
            context = FetchContext(commit=commit, pdfinfo=write_pdfinfo(tmp))
            with mock.patch(
                "source_manifest._validated_zip_infos",
                wraps=source_manifest_module._validated_zip_infos,
            ) as validated:
                self.assertEqual(_ensure_codeload_zip(cache, context), zip_path)
                self.assertEqual(
                    safe_zip_member_bytes(
                        zip_path, members[0], context=context
                    ),
                    first,
                )
                self.assertEqual(
                    safe_zip_member_bytes(
                        zip_path, members[1], context=context
                    ),
                    second,
                )
                self.assertEqual(validated.call_count, 1)

            next_context = FetchContext(commit=commit, pdfinfo=write_pdfinfo(tmp))
            with mock.patch(
                "source_manifest._validated_zip_infos",
                wraps=source_manifest_module._validated_zip_infos,
            ) as validated:
                self.assertEqual(_ensure_codeload_zip(cache, next_context), zip_path)
                self.assertEqual(validated.call_count, 1)

            corrupt = cache / ("c" * 40 + ".zip")
            corrupt.write_bytes(b"not-a-zip")
            corrupt_context = FetchContext(
                commit="c" * 40, pdfinfo=write_pdfinfo(tmp)
            )
            with mock.patch(
                "source_manifest._download_http_to",
                side_effect=RuntimeError("offline"),
            ), self.assertRaisesRegex(RuntimeError, "offline"):
                _ensure_codeload_zip(cache, corrupt_context)
            self.assertFalse(corrupt.exists())
            self.assertFalse((cache / (corrupt.name + ".tmp")).exists())

            new_context = FetchContext(commit="d" * 40, pdfinfo=write_pdfinfo(tmp))

            def corrupt_download(unused_url, destination, unused_limit, unused_context):
                destination.write_bytes(b"broken new zip")

            with mock.patch(
                "source_manifest._download_http_to", side_effect=corrupt_download
            ), self.assertRaisesRegex(RuntimeError, "ZIP"):
                _ensure_codeload_zip(cache, new_context)
            self.assertFalse((cache / ("d" * 40 + ".zip")).exists())
            self.assertFalse((cache / ("d" * 40 + ".zip.tmp")).exists())

    def test_sigkill_orphan_target_temp_is_cleaned_on_rerun(self):
        value = b"%PDF-interrupted\n"
        source = source_fixture(value)
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            target = directory / "source.pdf"
            marker = directory / "temp-created"
            slow_pdfinfo = directory / "pdfinfo-slow"
            slow_pdfinfo.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = \"-v\" ]; then echo 'pdfinfo version 24.01' >&2; exit 0; fi\n"
                "case \"$1\" in\n"
                "  *.tmp) touch %s; sleep 60 ;;\n"
                "esac\n"
                "echo 'Pages: 2'\n" % str(marker),
                encoding="utf-8",
            )
            slow_pdfinfo.chmod(0o700)
            code = (
                "import json,sys; from pathlib import Path; "
                "sys.path.insert(0,sys.argv[1]); "
                "from source_manifest import materialize_source; "
                "s=json.loads(sys.argv[2]); v=bytes.fromhex(sys.argv[3]); "
                "materialize_source(s,target=Path(sys.argv[4]),"
                "fetcher=lambda unused:v,pdfinfo=Path(sys.argv[5]))"
            )
            process = subprocess.Popen([
                sys.executable, "-c", code, str(ROOT / "tools"),
                json.dumps(source), value.hex(), str(target), str(slow_pdfinfo),
            ])
            try:
                for _ in range(200):
                    if marker.exists():
                        break
                    if process.poll() is not None:
                        self.fail("materialization child exited before creating target temp")
                    time.sleep(0.01)
                self.assertTrue(marker.exists(), "target temp creation marker missing")
                process.kill()
                process.wait(timeout=10)
                self.assertEqual(process.returncode, -signal.SIGKILL)
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait(timeout=10)
            orphans = list(directory.glob(".source.pdf.gaokao-materialize-*.tmp"))
            self.assertEqual(len(orphans), 1)
            unrelated = directory / ".source.pdf.unrelated.tmp"
            unrelated.write_bytes(b"keep")

            artifact = materialize_source(
                source,
                target=target,
                fetcher=lambda unused: value,
                pdfinfo=write_pdfinfo(tmp),
            )
            self.assertEqual(target.read_bytes(), value)
            self.assertEqual(artifact, artifact_fixture(value))
            self.assertEqual(
                list(directory.glob(".source.pdf.gaokao-materialize-*.tmp")), []
            )
            self.assertEqual(unrelated.read_bytes(), b"keep")

    def test_materialization_status_is_read_only_and_counts_match_mismatch_missing(self):
        values = [b"%PDF-match", b"%PDF-other", b"%PDF-missing"]
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            sources = []
            for index, value in enumerate(values):
                source = source_fixture(
                    value, source_id="src-%064d" % index,
                    upstream_path="普通高考/2021/%d.pdf" % index,
                    raw_paper_name="%d.pdf" % index,
                )
                sources.append(source)
            (repo / "普通高考" / "2021").mkdir(parents=True)
            (repo / sources[0]["upstream_path"]).write_bytes(values[0])
            (repo / sources[1]["upstream_path"]).write_bytes(b"different")
            manifest = build_inventory(
                [], "https://example.invalid/upstream", "c" * 40
            )
            manifest["sources"] = sources
            manifest["inventory"] = {"total_sources": 3, "root_counts": {"regular": 3, "spring": 0}}
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
            before = manifest_path.read_bytes()
            status_result = materialization_status(repo, manifest_path)
            self.assertEqual(status_result, {
                "total": 3, "matching": 1, "mismatched": 1,
                "missing": 1, "artifacts": 0,
            })
            self.assertEqual(manifest_path.read_bytes(), before)

    def test_probe_all_local_is_zero_network_and_failed_preflight_writes_no_state(self):
        value = b"%PDF-probe"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "upstream"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            oid = subprocess.check_output(
                ["git", "-C", str(repo), "hash-object", "-w", "--stdin"],
                input=value,
            ).decode().strip()
            entry = ENTRIES[0].copy()
            entry["oid"] = oid
            entry["path"] = "普通高考/2021/a.pdf"
            with mock.patch("source_manifest.git_tree", return_value=[entry]), \
                    mock.patch("source_manifest._download_http_to") as network:
                result = probe_transports(repo, "c" * 40)
            self.assertEqual(result["channel"], "local")
            network.assert_not_called()

            project = Path(tmp) / "project"
            project.mkdir()
            manifest = project / "source-manifest.json"
            issues = project / "missing-issues.md"
            state = build_inventory(
                [], "https://example.invalid/upstream", "c" * 40
            )
            manifest.write_text(canonical_json(state), encoding="utf-8")
            issues.write_bytes(b"issues-before")
            manifest_before = manifest.read_bytes()
            with mock.patch("source_manifest.probe_transports", side_effect=RuntimeError("all failed")):
                with self.assertRaisesRegex(RuntimeError, "all failed"):
                    main([
                        "materialize", "--repo", str(repo),
                        "--manifest", str(manifest), "--issues", str(issues),
                        "--all", "--jobs", "1", "--deadline-seconds", "10",
                        "--pdfinfo", str(write_pdfinfo(tmp)),
                    ])
            self.assertEqual(manifest.read_bytes(), manifest_before)
            self.assertEqual(issues.read_bytes(), b"issues-before")

    def test_each_source_result_is_one_state_transaction_and_success_resolves_issue(self):
        value = b"%PDF-state"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            project = repo / "docs" / "exams" / "math-gaokao-latex"
            (project / "schemas").mkdir(parents=True)
            schema_path = ROOT / "schemas" / "source-manifest.schema.json"
            (project / "schemas" / schema_path.name).write_bytes(schema_path.read_bytes())
            source = source_fixture(value)
            manifest = build_inventory(
                [], "https://example.invalid/upstream", "c" * 40
            )
            manifest["sources"] = [source]
            manifest["inventory"] = {"total_sources": 1, "root_counts": {"regular": 1, "spring": 0}}
            manifest_path = project / "source-manifest.json"
            manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
            issues_path = project / "missing-issues.md"
            issues_path.write_text("# issues\n", encoding="utf-8")

            with mock.patch("source_manifest.Transaction") as transaction_type:
                transaction = transaction_type.return_value
                transaction.transaction_id = "11111111-1111-4111-8111-111111111111"
                state_source_result(
                    repo, manifest_path, issues_path, source["source_id"],
                    artifact=None, issue_type="source-unavailable", evidence="offline",
                )
                transaction.prepare.assert_called_once()
                self.assertEqual(transaction.prepare.call_args.args[0], "state")
                transaction.commit.assert_called_once_with()

            # Run real state transactions to verify stable issue resolution and blocker removal.
            state_source_result(
                repo, manifest_path, issues_path, source["source_id"],
                artifact=None, issue_type="source-unavailable", evidence="offline",
            )
            failed_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            issue_id = failed_manifest["sources"][0]["issue_ids"][0]
            self.assertEqual(failed_manifest["revision"], 1)
            self.assertEqual(load_issues(issues_path)[0]["status"], "open")
            artifact = {
                "size_bytes": len(value), "sha256": hashlib.sha256(value).hexdigest(),
                "page_count": 2, "media_type": "application/pdf",
                "header_is_pdf": True, "git_oid_verified": True,
                "pdf_check": "passed", "pdfinfo_version": "24.01",
            }
            state_source_result(
                repo, manifest_path, issues_path, source["source_id"], artifact=artifact,
            )
            completed = load_manifest(manifest_path)
            completed_source = completed["sources"][0]
            self.assertEqual(completed["revision"], 2)
            self.assertEqual(completed_source["source_state"], "ready")
            self.assertEqual(completed_source["artifact"], artifact)
            self.assertNotIn(issue_id, completed_source["issue_ids"])
            resolved = load_issues(issues_path)[0]
            self.assertEqual(resolved["issue_id"], issue_id)
            self.assertEqual(resolved["status"], "resolved")
            self.assertIn("resolved_evidence", resolved)

    def test_state_prepare_failure_does_not_accept_already_equal_artifact(self):
        value = b"%PDF-prior-equal\n"
        artifact = artifact_fixture(value)
        source = source_fixture(value, source_state="ready", artifact=artifact)
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            subprocess.run(
                ["git", "-C", str(upstream), "hash-object", "-w", "--stdin"],
                input=value,
                check=True,
                stdout=subprocess.PIPE,
            )
            target = upstream / source["upstream_path"]
            pdfinfo = write_pdfinfo(tmp)
            attempted = []

            def factory(root):
                def hook(event, unused_path):
                    if event == "staged_durable":
                        raise InjectedTransactionFailure("prepare injected")
                transaction = RealTransaction(root, event_hook=hook)
                attempted.append(transaction.transaction_id)
                return transaction

            with mock.patch("source_manifest.Transaction", side_effect=factory), \
                    mock.patch("source_manifest.probe_transports", return_value={"ok": True}), \
                    self.assertRaisesRegex(InjectedTransactionFailure, "prepare injected") as raised:
                main([
                    "materialize", "--repo", str(upstream),
                    "--manifest", str(manifest_path), "--issues", str(issues_path),
                    "--source", source["source_id"], "--jobs", "1",
                    "--deadline-seconds", "30", "--pdfinfo", str(pdfinfo),
                ])
            self.assertEqual(raised.exception.transaction_id, attempted[0])
            self.assertFalse(target.exists())
            unchanged = load_manifest(manifest_path)
            self.assertEqual(unchanged["revision"], 0)
            self.assertNotEqual(unchanged["last_transaction_id"], attempted[0])
            self.assertEqual(unchanged["sources"][0]["artifact"], artifact)
            self.assertEqual(load_issues(issues_path), [])

    def test_state_failure_does_not_delete_later_equal_target(self):
        value = b"%PDF-later-equal\n"
        source = source_fixture(
            value, source_state="ready", artifact=artifact_fixture(value)
        )
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            subprocess.run(
                ["git", "-C", str(upstream), "hash-object", "-w", "--stdin"],
                input=value,
                check=True,
                stdout=subprocess.PIPE,
            )
            target = upstream / source["upstream_path"]
            replacement_identity = []

            def factory(root):
                def hook(event, unused_path):
                    if event == "staged_durable" and not replacement_identity:
                        target.unlink()
                        target.write_bytes(value)
                        status = target.stat()
                        replacement_identity.append((status.st_dev, status.st_ino))
                        raise InjectedTransactionFailure("later writer")
                return RealTransaction(root, event_hook=hook)

            with mock.patch("source_manifest.Transaction", side_effect=factory), \
                    mock.patch("source_manifest.probe_transports", return_value={"ok": True}), \
                    self.assertRaisesRegex(InjectedTransactionFailure, "later writer"):
                main([
                    "materialize", "--repo", str(upstream),
                    "--manifest", str(manifest_path), "--issues", str(issues_path),
                    "--source", source["source_id"], "--jobs", "1",
                    "--deadline-seconds", "30",
                    "--pdfinfo", str(write_pdfinfo(tmp)),
                ])
            self.assertTrue(target.is_file())
            status = target.stat()
            self.assertEqual((status.st_dev, status.st_ino), replacement_identity[0])
            self.assertEqual(target.read_bytes(), value)

    def test_state_cas_failure_restores_new_target_and_propagates(self):
        value = b"%PDF-cas\n"
        artifact = artifact_fixture(value)
        source = source_fixture(value, source_state="ready", artifact=artifact)
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            subprocess.run(
                ["git", "-C", str(upstream), "hash-object", "-w", "--stdin"],
                input=value,
                check=True,
                stdout=subprocess.PIPE,
            )
            target = upstream / source["upstream_path"]
            changed = {"done": False}

            def factory(root):
                def hook(event, unused_path):
                    if event == "journal_prepared" and not changed["done"]:
                        external = json.loads(manifest_path.read_text(encoding="utf-8"))
                        external["revision"] = 7
                        manifest_path.write_text(canonical_json(external), encoding="utf-8")
                        changed["done"] = True
                return RealTransaction(root, event_hook=hook)

            with mock.patch("source_manifest.Transaction", side_effect=factory), \
                    mock.patch("source_manifest.probe_transports", return_value={"ok": True}), \
                    self.assertRaisesRegex(RuntimeError, "CAS"):
                main([
                    "materialize", "--repo", str(upstream),
                    "--manifest", str(manifest_path), "--issues", str(issues_path),
                    "--source", source["source_id"], "--jobs", "1",
                    "--deadline-seconds", "30",
                    "--pdfinfo", str(write_pdfinfo(tmp)),
                ])
            self.assertFalse(target.exists())
            self.assertEqual(load_manifest(manifest_path)["revision"], 7)
            self.assertEqual(load_issues(issues_path), [])

    def test_partial_commit_recovery_requires_exact_attempted_transaction(self):
        value = b"%PDF-partial\n"
        artifact = artifact_fixture(value)
        source = source_fixture(value, source_state="ready", artifact=artifact)
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, issues_path = init_state_repository(tmp, source)
            upstream = Path(tmp) / "upstream"
            subprocess.run(["git", "init", "-q", str(upstream)], check=True)
            subprocess.run(
                ["git", "-C", str(upstream), "hash-object", "-w", "--stdin"],
                input=value,
                check=True,
                stdout=subprocess.PIPE,
            )
            crashes = {"remaining": 1}
            attempted = []

            def factory(root):
                def hook(event, unused_path):
                    if event == "target_replaced" and crashes["remaining"]:
                        crashes["remaining"] -= 1
                        raise InjectedTransactionFailure("partial commit")
                transaction = RealTransaction(root, event_hook=hook)
                attempted.append(transaction.transaction_id)
                return transaction

            with mock.patch("source_manifest.Transaction", side_effect=factory), \
                    mock.patch("source_manifest.probe_transports", return_value={"ok": True}):
                result = main([
                    "materialize", "--repo", str(upstream),
                    "--manifest", str(manifest_path), "--issues", str(issues_path),
                    "--source", source["source_id"], "--jobs", "1",
                    "--deadline-seconds", "30",
                    "--pdfinfo", str(write_pdfinfo(tmp)),
                ])
            self.assertEqual(result, 0)
            completed = load_manifest(manifest_path)
            self.assertEqual(completed["revision"], 1)
            self.assertEqual(completed["last_transaction_id"], attempted[0])
            self.assertEqual(completed["sources"][0]["source_state"], "ready")
            self.assertEqual(completed["sources"][0]["artifact"], artifact)
            self.assertEqual(load_issues(issues_path), [])

    def test_validate_requires_exact_artifact_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "schemas").mkdir()
            schema_path = ROOT / "schemas" / "source-manifest.schema.json"
            (project / "schemas" / schema_path.name).write_bytes(schema_path.read_bytes())
            manifest = build_inventory(
                ENTRIES, "https://example.invalid/upstream", "c" * 40
            )
            manifest_path = project / "source-manifest.json"
            manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
            self.assertEqual(validate_source_manifest(manifest_path), 0)
            with self.assertRaisesRegex(ValueError, "artifact.*1"):
                validate_source_manifest(manifest_path, require_artifacts=1)

    def test_materialize_cli_parser_boundaries_and_exit_codes(self):
        common = [
            "materialize", "--repo", "/repo", "--manifest", "/manifest",
            "--issues", "/issues", "--jobs", "1", "--deadline-seconds", "1",
            "--pdfinfo", "/pdfinfo",
        ]
        invalid = [
            common,
            common + ["--all", "--source", "src-x"],
            common[:-7] + ["--jobs", "0", "--deadline-seconds", "1", "--pdfinfo", "/p", "--all"],
            common[:-5] + ["--deadline-seconds", "0", "--pdfinfo", "/p", "--all"],
            common[:-3] + ["--pdfinfo", "relative", "--all"],
        ]
        for args in invalid:
            with self.subTest(args=args), redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    main(args)
                self.assertEqual(raised.exception.code, 2)


class RegisterPapersTests(unittest.TestCase):
    """阶段 1 新增：把「未绑定来源 → paper 记录 + batch 记录」纳入 state 事务。

    阶段 0 的 21 套由 `migrate_legacy_index()` 从冻结常量一次性种入，且显式拒绝覆盖；
    在此之前没有任何入口能新增试卷，一套新卷都做不出来。
    """

    PREFIX = "2021/2021_数学真题_全国甲文"

    def _repo(self, tmp):
        repo = Path(tmp) / "repo"
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        project = repo / "docs" / "exams" / "math-gaokao-latex"
        (project / "schemas").mkdir(parents=True)
        schema_path = ROOT / "schemas" / "source-manifest.schema.json"
        (project / "schemas" / schema_path.name).write_bytes(schema_path.read_bytes())

        source = source_fixture(paper_relation=None, source_state="ready", artifact={
            "size_bytes": 11, "sha256": "d" * 64, "page_count": 2,
            "media_type": "application/pdf", "header_is_pdf": True,
            "git_oid_verified": True, "pdf_check": "passed",
            "pdfinfo_version": "26.08.0",
        })
        manifest = build_inventory([], "https://example.invalid/upstream", "c" * 40)
        manifest["sources"] = [source]
        manifest["papers"] = []
        manifest["batches"] = []
        manifest["inventory"] = {
            "total_sources": 1, "root_counts": {"regular": 1, "spring": 0},
        }
        manifest_path = project / "source-manifest.json"
        manifest_path.write_text(canonical_json(manifest), encoding="utf-8")

        # 注册是对已存在产物的事实登记：三个必需规范 Markdown 必须先在盘上。
        for suffix in ("_试题.md", "_答案要点.md", "_含解析.md"):
            target = repo / (self.PREFIX + suffix)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("# 占位\n", encoding="utf-8")
        return repo, manifest_path, source["source_id"]

    def _spec(self, source_id_value, **updates):
        paper = {
            "paper_id": "gk-2021-regular-national-a-arts",
            "project_dir": "2021_全国甲卷_文科",
            "title": "2021 年·全国甲卷·文科",
            "year": 2021,
            "track": "arts",
            "question_count": 23,
            "markdown_prefix": self.PREFIX,
            "source_ids": [source_id_value],
            "figure_files": [],
            "index_metadata": {
                "id": "gk-2021-regular-national-a-arts",
                "base": "2021_gaokao_a_arts",
                "paper": "全国甲卷",
                "track": "文科",
                "variant": "全国甲文",
                "structure": {"选择题": [1, 12], "填空题": [13, 16], "解答题": [17, 21], "选做题": [22, 23]},
                "pages_q": None,
                "pages_s": None,
                "note": None,
            },
        }
        paper.update(updates)
        return {"batch_id": "phase1-b07", "papers": [paper]}

    def test_dry_run_reports_plan_without_touching_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            before = manifest_path.read_bytes()
            report = source_manifest_module.register_papers(
                repo, manifest_path, self._spec(source_id_value)
            )
            self.assertEqual(report["code"], "OK")
            self.assertFalse(report["written"])
            self.assertEqual(report["paper_ids"], ["gk-2021-regular-national-a-arts"])
            self.assertEqual(manifest_path.read_bytes(), before)

    def test_write_binds_source_and_batch_in_one_state_transaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            before = load_manifest(manifest_path)
            source_manifest_module.register_papers(
                repo, manifest_path, self._spec(source_id_value), write=True
            )
            after = load_manifest(manifest_path)
            self.assertEqual(after["revision"], before["revision"] + 1)

            paper = after["papers"][0]
            self.assertEqual(paper["paper_id"], "gk-2021-regular-national-a-arts")
            self.assertEqual(paper["production_state"], "planned")
            self.assertEqual(paper["legacy_ids"], [])
            self.assertEqual(paper["source_ids"], [source_id_value])
            self.assertEqual(paper["source_files"], {
                "questions": self.PREFIX + "_试题.md",
                "answer_key": self.PREFIX + "_答案要点.md",
                "solution_body": self.PREFIX + "_解析正文.md",
                "combined_rendered": self.PREFIX + "_含解析.md",
            })
            # 双向关系必须在同一事务内闭合，否则 validate_manifest_semantics 当场拒绝。
            bound = after["sources"][0]
            self.assertEqual(bound["paper_id"], "gk-2021-regular-national-a-arts")
            self.assertEqual(bound["paper_relation"], "canonical")
            self.assertEqual(after["batches"], [{
                "batch_id": "phase1-b07",
                "paper_ids": ["gk-2021-regular-national-a-arts"],
                "status": "planned",
                "issues": [],
            }])

    def test_registers_question_blocker_with_paper_in_one_state_transaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            issues_path = repo / "math-gaokao-latex/missing-issues.md"
            issues_path.write_text("# Missing issues\n\n", encoding="utf-8")
            paper_id = "gk-2021-regular-national-a-arts"
            resume_action = "取得可核原图后补录；不得凭模型记忆重建图形"
            spec = self._spec(source_id_value)
            spec["papers"][0]["question_issues"] = [{
                "kind": "figure",
                "question_id": paper_id + "-q12",
                "source_id": source_id_value,
                "current_evidence": "固定扫描页题干指向下图，但对应图位为空白。",
                "resume_action": resume_action,
            }]

            manifest_before = manifest_path.read_bytes()
            issues_before = issues_path.read_bytes()
            dry_run = source_manifest_module.register_papers(
                repo, manifest_path, spec
            )
            self.assertFalse(dry_run["written"])
            self.assertIn("issue_ids", dry_run)
            self.assertEqual(dry_run["issue_ids"], {paper_id: ["ISSUE-0001"]})
            self.assertEqual(manifest_path.read_bytes(), manifest_before)
            self.assertEqual(issues_path.read_bytes(), issues_before)

            transaction = RealTransaction(repo)
            with mock.patch("source_manifest.Transaction", return_value=transaction):
                with mock.patch.object(
                    transaction, "prepare", wraps=transaction.prepare
                ) as prepare:
                    source_manifest_module.register_papers(
                        repo, manifest_path, spec, write=True
                    )
                    prepare.assert_called_once()
                    self.assertEqual(prepare.call_args.args[0], "state")
                    self.assertEqual(
                        set(prepare.call_args.args[1]),
                        {
                            "math-gaokao-latex/missing-issues.md",
                            "math-gaokao-latex/source-manifest.json",
                        },
                    )
            manifest = load_manifest(manifest_path)
            paper = manifest["papers"][0]
            self.assertEqual(paper["production_state"], "blocked")
            self.assertEqual(paper["blocked_from"], "planned")
            self.assertEqual(paper["issue_ids"], ["ISSUE-0001"])
            self.assertEqual(paper["resume_action"], resume_action)
            self.assertEqual(manifest["sources"][0]["paper_id"], paper_id)
            issue, = load_issues(issues_path)
            self.assertEqual(issue["issue_id"], "ISSUE-0001")
            self.assertEqual(issue["type"], "figure-missing")
            self.assertEqual(issue["question_id"], paper_id + "-q12")
            self.assertEqual(issue["source_id"], source_id_value)
            self.assertEqual(issue["current_evidence"], "固定扫描页题干指向下图，但对应图位为空白。")

    def test_question_issue_source_must_be_bound_to_new_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            issues_path = repo / "math-gaokao-latex/missing-issues.md"
            issues_path.write_text("# Missing issues\n\n", encoding="utf-8")
            spec = self._spec(source_id_value)
            spec["papers"][0]["question_issues"] = [{
                "kind": "figure",
                "question_id": "gk-2021-regular-national-a-arts-q12",
                "source_id": "src-not-bound-to-this-paper",
                "current_evidence": "原卷对应图位为空白。",
                "resume_action": "取得可核图源后复核。",
            }]
            manifest_before = manifest_path.read_bytes()
            issues_before = issues_path.read_bytes()

            with self.assertRaisesRegex(ValueError, "问题来源未绑定到该卷"):
                source_manifest_module.register_papers(
                    repo, manifest_path, spec, write=True
                )

            self.assertEqual(manifest_path.read_bytes(), manifest_before)
            self.assertEqual(issues_path.read_bytes(), issues_before)

    def test_rejects_rebinding_a_source_already_owned_by_another_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            source_manifest_module.register_papers(
                repo, manifest_path, self._spec(source_id_value), write=True
            )
            second = self._spec(
                source_id_value,
                paper_id="gk-2021-regular-national-a-science",
                project_dir="2021_全国甲卷_理科",
            )
            second["papers"][0]["index_metadata"]["id"] = (
                "gk-2021-regular-national-a-science"
            )
            second["batch_id"] = "phase1-b08"
            with self.assertRaisesRegex(ValueError, "已绑定"):
                source_manifest_module.register_papers(
                    repo, manifest_path, second, write=True
                )

    def test_rejects_unknown_source_duplicate_identity_and_bad_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            cases = {
                "来源不存在": self._spec("src-" + "9" * 64),
                "question_count": self._spec(source_id_value, question_count=0),
                "paper_id": self._spec(source_id_value, paper_id="not-a-paper-id"),
            }
            for label, spec in cases.items():
                with self.subTest(label=label):
                    with self.assertRaises(ValueError):
                        source_manifest_module.register_papers(
                            repo, manifest_path, spec, write=True
                        )
            # 全部拒绝后 manifest 必须仍是初始状态：失败不得留半份注册。
            self.assertEqual(load_manifest(manifest_path)["papers"], [])

    def test_rejects_reusing_an_existing_batch_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            source_manifest_module.register_papers(
                repo, manifest_path, self._spec(source_id_value), write=True
            )
            manifest = load_manifest(manifest_path)
            manifest["sources"][0]["paper_id"] = None
            manifest["sources"][0]["paper_relation"] = None
            manifest["papers"] = []
            manifest["batches"] = [{
                "batch_id": "phase1-b07", "paper_ids": [], "status": "planned",
                "issues": [],
            }]
            manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "batch_id"):
                source_manifest_module.register_papers(
                    repo, manifest_path, self._spec(source_id_value), write=True
                )

    def test_persisted_manifest_rejects_malformed_index_metadata_on_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            source_manifest_module.register_papers(
                repo, manifest_path, self._spec(source_id_value), write=True
            )
            valid = json.loads(manifest_path.read_text(encoding="utf-8"))
            cases = {
                "pages_q": [1],
                "structure": {"全部": [1]},
            }
            for field, malformed in cases.items():
                with self.subTest(field=field):
                    manifest = copy.deepcopy(valid)
                    manifest["papers"][0]["index_metadata"][field] = malformed
                    manifest_path.write_text(canonical_json(manifest), encoding="utf-8")
                    with self.assertRaises((SchemaError, ValueError)):
                        load_manifest(manifest_path)

    def test_requires_canonical_markdown_to_exist_before_registration(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            (repo / (self.PREFIX + "_答案要点.md")).unlink()
            with self.assertRaisesRegex(ValueError, "答案要点"):
                source_manifest_module.register_papers(
                    repo, manifest_path, self._spec(source_id_value), write=True
                )

    def test_rejects_index_metadata_that_cannot_identify_or_partition_the_paper(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path, source_id_value = self._repo(tmp)
            cases = {}
            wrong_id = self._spec(source_id_value)
            wrong_id["papers"][0]["index_metadata"]["id"] = "gk-2021-wrong"
            cases["必须与 paper_id 一致"] = wrong_id
            overlap = self._spec(source_id_value)
            overlap["papers"][0]["index_metadata"]["structure"] = {
                "前段": [1, 12], "后段": [12, 23],
            }
            cases["范围重叠"] = overlap
            bad_pages = self._spec(source_id_value)
            bad_pages["papers"][0]["index_metadata"]["pages_q"] = [3, 1]
            cases["pages_q"] = bad_pages
            for message, spec in cases.items():
                with self.subTest(message=message):
                    with self.assertRaisesRegex(ValueError, message):
                        source_manifest_module.register_papers(
                            repo, manifest_path, spec, write=True
                        )
            self.assertEqual(load_manifest(manifest_path)["papers"], [])

    def test_project_legacy_index_supports_canonical_new_ids_but_rejects_unknown_ids(self):
        manifest = load_manifest(ROOT / "source-manifest.json")
        paper_id = "gk-2021-regular-national-a-arts"
        projected = source_manifest_module.project_legacy_index(
            manifest, {"papers": [{"id": paper_id}]}
        )
        self.assertEqual(projected["papers"][0]["paper_id"], paper_id)
        self.assertEqual(projected["papers"][0]["legacy_ids"], [])
        with self.assertRaisesRegex(ValueError, "未覆盖 index ID"):
            source_manifest_module.project_legacy_index(
                manifest, {"papers": [{"id": "gk-2099-unknown"}]}
            )

    def test_migrated_papers_keep_frozen_legacy_ids(self):
        """schema 放开 minItems 后，迁移卷的身份改由定向机检守住。"""
        manifest = copy.deepcopy(dict(load_manifest(ROOT / "source-manifest.json")))
        target = next(
            paper for paper in manifest["papers"]
            if paper["paper_id"] == "gk-2018-regular-national-1-science"
        )
        target["legacy_ids"] = []
        with self.assertRaisesRegex(ValueError, "legacy_ids"):
            source_manifest_module._validate_paper_semantics(manifest)


if __name__ == "__main__":
    unittest.main()

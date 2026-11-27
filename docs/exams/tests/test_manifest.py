import fcntl
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from manifest import (
    atomic_write_json,
    canonical_json,
    durable_fsync,
    load_manifest,
    project_index,
    validate_manifest_semantics,
)
from schema_validate import SchemaError, validate


class ManifestTests(unittest.TestCase):
    def test_relation_requires_paper_id(self):
        manifest = {
            "sources": [{
                "source_id": "src-1", "upstream_path": "普通高考/2021/a.pdf",
                "source_state": "ready", "paper_relation": "canonical",
                "paper_id": None,
            }],
            "papers": [], "batches": [],
        }
        with self.assertRaisesRegex(ValueError, "paper_id"):
            validate_manifest_semantics(manifest)

    def test_atomic_json_is_stable(self):
        value = {"z": 1, "a": [2, 1]}
        self.assertEqual(canonical_json(value), '{\n  "a": [\n    2,\n    1\n  ],\n  "z": 1\n}\n')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "new" / "x.json"
            atomic_write_json(path, value)
            self.assertEqual(path.read_text(encoding="utf-8"), canonical_json(value))
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")), value)

    def test_semantics_reject_duplicates_missing_papers_and_reverse_drift(self):
        base = {
            "sources": [{
                "source_id": "src-1", "source_state": "ready",
                "paper_relation": "canonical", "paper_id": "paper-1",
            }],
            "papers": [{"paper_id": "paper-1", "source_ids": ["src-1"]}],
            "batches": [],
        }
        validate_manifest_semantics(base)
        self.assertEqual(project_index(base), {"paper-1": base["papers"][0]})

        duplicate_source = json.loads(json.dumps(base))
        duplicate_source["sources"].append(duplicate_source["sources"][0])
        with self.assertRaisesRegex(ValueError, "source_id"):
            validate_manifest_semantics(duplicate_source)

        duplicate_paper = json.loads(json.dumps(base))
        duplicate_paper["papers"].append(duplicate_paper["papers"][0])
        with self.assertRaisesRegex(ValueError, "paper_id"):
            validate_manifest_semantics(duplicate_paper)

        missing_paper = json.loads(json.dumps(base))
        missing_paper["sources"][0]["paper_id"] = "paper-missing"
        with self.assertRaisesRegex(ValueError, "paper_id 不存在"):
            validate_manifest_semantics(missing_paper)

        reverse_drift = json.loads(json.dumps(base))
        reverse_drift["papers"][0]["source_ids"] = []
        with self.assertRaisesRegex(ValueError, "双向关系"):
            validate_manifest_semantics(reverse_drift)

    def test_non_paper_cannot_bind_a_paper(self):
        manifest = {
            "sources": [{
                "source_id": "src-1", "source_state": "non_paper",
                "paper_relation": None, "paper_id": "paper-1",
            }],
            "papers": [{"paper_id": "paper-1", "source_ids": []}],
            "batches": [],
        }
        with self.assertRaisesRegex(ValueError, "non_paper"):
            validate_manifest_semantics(manifest)

    def test_task_one_does_not_define_batch_id_semantics(self):
        manifest = {
            "sources": [],
            "papers": [],
            "batches": [
                {"batch_id": "future-batch"},
                {"batch_id": "future-batch"},
                {"future_shape": True},
            ],
        }
        validate_manifest_semantics(manifest)

    def test_durable_fsync_prefers_fullfsync_when_supported(self):
        with mock.patch.object(fcntl, "F_FULLFSYNC", 123, create=True), \
                mock.patch.object(fcntl, "fcntl") as full_sync, \
                mock.patch.object(os, "fsync") as fallback:
            self.assertEqual(durable_fsync(9), "fullfsync")
        full_sync.assert_called_once_with(9, 123)
        fallback.assert_not_called()

    def test_durable_fsync_falls_back_when_fullfsync_is_unsupported(self):
        with mock.patch.object(fcntl, "F_FULLFSYNC", 123, create=True), \
                mock.patch.object(fcntl, "fcntl", side_effect=OSError("unsupported")) as full_sync, \
                mock.patch.object(os, "fsync") as fallback:
            self.assertEqual(durable_fsync(9), "fsync")
        full_sync.assert_called_once_with(9, 123)
        fallback.assert_called_once_with(9)

    def test_minimal_source_manifest_schema_and_load(self):
        schema_path = ROOT / "schemas" / "source-manifest.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        manifest = {
            "$schema": "schemas/source-manifest.schema.json",
            "schema_version": 1,
            "revision": 0,
            "last_transaction_id": None,
            "upstream": {
                "url": "https://example.invalid/upstream.git",
                "commit": "a" * 40,
                "scoped_roots": ["普通高考"],
            },
            "inventory": {
                "total_sources": 1,
                "root_counts": {"regular": 1},
            },
            "sources": [{
                "source_id": "src-1",
                "upstream_path": "普通高考/2021/a.pdf",
                "git_blob_oid": "b" * 40,
                "year": 2021,
                "exam_type": "regular",
                "track": None,
                "regions": [],
                "raw_paper_name": "a.pdf",
                "source_state": "not_started",
                "paper_relation": None,
                "paper_id": None,
                "artifact": None,
                "issue_ids": [],
            }],
            "papers": [],
            "batches": [],
        }
        validate(manifest, schema)

        unknown_cases = (
            ("top", lambda value: value.__setitem__("invented", True), r"\$\.invented"),
            ("upstream", lambda value: value["upstream"].__setitem__("invented", True), r"\$\.upstream\.invented"),
            ("inventory", lambda value: value["inventory"].__setitem__("invented", True), r"\$\.inventory\.invented"),
            ("source", lambda value: value["sources"][0].__setitem__("invented", True), r"\$\.sources\[0\]\.invented"),
        )
        for label, mutate, expected_path in unknown_cases:
            with self.subTest(additional_properties=label):
                unknown = json.loads(json.dumps(manifest))
                mutate(unknown)
                with self.assertRaisesRegex(SchemaError, expected_path):
                    validate(unknown, schema)

        required_cases = (
            ("schema_version", lambda value: value.pop("schema_version"), r"\$\.schema_version"),
            ("upstream.commit", lambda value: value["upstream"].pop("commit"), r"\$\.upstream\.commit"),
            ("inventory.total_sources", lambda value: value["inventory"].pop("total_sources"), r"\$\.inventory\.total_sources"),
            ("source.git_blob_oid", lambda value: value["sources"][0].pop("git_blob_oid"), r"\$\.sources\[0\]\.git_blob_oid"),
        )
        for label, mutate, expected_path in required_cases:
            with self.subTest(required=label):
                missing = json.loads(json.dumps(manifest))
                mutate(missing)
                with self.assertRaisesRegex(SchemaError, expected_path):
                    validate(missing, schema)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "schemas").mkdir()
            (root / "schemas" / schema_path.name).write_bytes(schema_path.read_bytes())
            path = root / "source-manifest.json"
            atomic_write_json(path, manifest)
            self.assertEqual(load_manifest(path), manifest)

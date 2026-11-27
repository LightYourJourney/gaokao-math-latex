import csv
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from manifest_csv import CSV_FIELDS, render_manifest_csv


class ManifestCsvTests(unittest.TestCase):
    def test_render_is_stable_and_exposes_unregistered_sources_as_pending(self):
        manifest = {
            "sources": [
                {
                    "source_id": "src-b",
                    "year": 1958,
                    "upstream_path": "普通高考/1958/b.pdf",
                    "source_state": "ready",
                    "paper_relation": None,
                    "paper_id": None,
                    "artifact": {"sha256": "b" * 64},
                    "issue_ids": [],
                },
                {
                    "source_id": "src-a",
                    "year": 1957,
                    "upstream_path": "普通高考/1957/a.pdf",
                    "source_state": "ready",
                    "paper_relation": "canonical",
                    "paper_id": "gk-1957-regular-national",
                    "artifact": {"sha256": "a" * 64},
                    "issue_ids": [],
                },
            ],
            "papers": [
                {
                    "paper_id": "gk-1957-regular-national",
                    "project_dir": "1957_全国卷",
                    "title": "1957 年·全国卷",
                    "production_state": "complete",
                    "question_count": 9,
                    "issue_ids": [],
                }
            ],
            "batches": [
                {"batch_id": "phase1-b14", "paper_ids": ["gk-1957-regular-national"]}
            ],
        }

        first = render_manifest_csv(manifest)
        second = render_manifest_csv(manifest)
        self.assertEqual(first, second)

        rows = list(csv.DictReader(io.StringIO(first)))
        self.assertEqual(first.splitlines()[0].split(","), CSV_FIELDS)
        self.assertEqual([row["source_id"] for row in rows], ["src-a", "src-b"])
        self.assertEqual(rows[0]["production_state"], "complete")
        self.assertEqual(rows[0]["batch_ids"], "phase1-b14")
        self.assertEqual(rows[1]["production_state"], "pending")
        self.assertEqual(rows[1]["status_note"], "未注册独立题面")

    def test_csv_escapes_commas_and_newlines_with_standard_csv_rules(self):
        manifest = {
            "sources": [
                {
                    "source_id": "src-1",
                    "year": 1959,
                    "upstream_path": "普通高考/1959/1959.pdf",
                    "source_state": "ready",
                    "paper_relation": "canonical",
                    "paper_id": "gk-1959-regular-national",
                    "artifact": {"sha256": "c" * 64},
                    "issue_ids": ["ISSUE-0111"],
                }
            ],
            "papers": [
                {
                    "paper_id": "gk-1959-regular-national",
                    "project_dir": "1959_全国卷",
                    "title": "1959 年·全国卷,不分文理",
                    "production_state": "blocked",
                    "question_count": 10,
                    "issue_ids": ["ISSUE-0112"],
                }
            ],
            "batches": [],
        }
        rows = list(csv.DictReader(io.StringIO(render_manifest_csv(manifest))))
        self.assertEqual(rows[0]["title"], "1959 年·全国卷,不分文理")
        self.assertEqual(rows[0]["issue_ids"], "ISSUE-0111;ISSUE-0112")


if __name__ == "__main__":
    unittest.main()

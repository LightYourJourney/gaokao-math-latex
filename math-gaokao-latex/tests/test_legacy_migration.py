import copy
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from issues import load_issues
from manifest import canonical_json, file_sha256, load_manifest, project_index
from schema_validate import SchemaError, validate
from transaction import MANIFEST_TARGET
from source_manifest import (
    BATCH_STATUSES,
    LEGACY_PAPERS,
    MARKDOWN_GROUPS,
    PHASE0_BATCHES,
    PRODUCTION_STATES,
    SOURCE_FILE_KEYS,
    main,
    migrate_legacy_index,
    project_legacy_index,
    validate_source_state,
)

# 计划 Task 4 Step 2 的 21 条映射逐字重抄，测试与实现各持一份，任一侧漂移都会红。
EXPECTED_PAPER_IDS = {
    "2017li": "gk-2017-regular-national-1-science",
    "2017wen": "gk-2017-regular-national-1-arts",
    "2018li": "gk-2018-regular-national-1-science",
    "2018wen": "gk-2018-regular-national-1-arts",
    "2019li": "gk-2019-regular-national-1-science",
    "2019wen": "gk-2019-regular-national-1-arts",
    "2020li": "gk-2020-regular-national-1-science",
    "2020wen": "gk-2020-regular-national-1-arts",
    "2020x2": "gk-2020-regular-new-gaokao-2",
    "2021": "gk-2021-regular-new-gaokao-1",
    "2021x2": "gk-2021-regular-new-gaokao-2",
    "2022": "gk-2022-regular-new-gaokao-1",
    "2022x2": "gk-2022-regular-new-gaokao-2",
    "2023": "gk-2023-regular-new-gaokao-1",
    "2023x2": "gk-2023-regular-new-gaokao-2",
    "2024": "gk-2024-regular-new-gaokao-1",
    "2024x2": "gk-2024-regular-new-gaokao-2",
    "2025": "gk-2025-regular-national-1",
    "2025g2": "gk-2025-regular-national-2",
    "2026": "gk-2026-regular-national-1-recall",
    "2026g2": "gk-2026-regular-national-2",
}

# 计划 Task 4 Step 3 的六个不可变子批次逐字重抄。
EXPECTED_BATCHES = (
    ("phase0-b01", ("2017li", "2017wen", "2018li", "2018wen")),
    ("phase0-b02", ("2019li", "2019wen", "2020li", "2020wen")),
    ("phase0-b03", ("2020x2", "2021", "2021x2")),
    ("phase0-b04", ("2022", "2022x2", "2023", "2023x2")),
    ("phase0-b05", ("2024", "2024x2", "2025", "2025g2")),
    ("phase0-b06", ("2026", "2026g2")),
)

EDITIONS = ("试题版", "解析版", "简答版", "印刷版")
_PAPER_ID_RE = re.compile(r"\\renewcommand\{\\gkpaperid\}\{([^{}]+)\}")
_FIGURE_INPUT_RE = re.compile(r"\\input\{figures/([^{}/]+)\}")
_MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def counted(texts, pattern):
    counts = {}
    for text in texts:
        for match in pattern.finditer(text):
            key = match.group(1)
            counts[key] = counts.get(key, 0) + 1
    return counts


def legacy_index_view(index):
    """去掉投影新增的三个键，还原迁移前的兼容 index 形状。"""
    view = copy.deepcopy(index)
    view.pop("batches", None)
    for paper in view["papers"]:
        paper.pop("paper_id", None)
        paper.pop("legacy_ids", None)
    return view


def minimal_paper():
    return {
        "paper_id": "gk-2017-regular-national-1-science",
        "legacy_ids": ["2017li"],
        "project_dir": "2017_全国Ⅰ卷_理科",
        "title": "2017 年·全国Ⅰ卷·理科",
        "year": 2017,
        "track": "science",
        "question_count": 23,
        "source_files": {
            "questions": "2017/2017_数学真题_理_试题.md",
            "answer_key": "2017/2017_数学真题_理_答案要点.md",
            "solution_body": "2017/2017_数学真题_理_解析正文.md",
            "combined_rendered": "2017/2017_数学真题_理_含解析.md",
        },
        "figure_files": [
            {
                "path": "2017_全国Ⅰ卷_理科/figures/f2017_taiji.tex",
                "expected_occurrences": 2,
            },
        ],
        "legacy_source_files": [],
        "source_ids": [],
        "production_state": "legacy_unverified",
        "issue_ids": [],
        "blocked_from": None,
        "last_verified_hash": None,
        "resume_action": None,
    }


def minimal_manifest():
    return {
        "$schema": "schemas/source-manifest.schema.json",
        "schema_version": 1,
        "revision": 0,
        "last_transaction_id": None,
        "upstream": {
            "url": "https://example.invalid/upstream",
            "commit": "c" * 40,
            "scoped_roots": ["普通高考"],
        },
        "inventory": {"total_sources": 0, "root_counts": {}},
        "sources": [],
        "papers": [minimal_paper()],
        "batches": [{
            "batch_id": "phase0-b01",
            "paper_ids": ["gk-2017-regular-national-1-science"],
            "status": "planned",
            "issues": [],
        }],
    }


def fixture_repository(directory):
    """建一个只含迁移所需 tracked 文件的临时仓库；manifest 回到迁移前状态。"""
    repo = Path(directory) / "repo"
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    project = repo / "docs" / "exams" / "math-gaokao-latex"
    (project / "schemas").mkdir(parents=True)
    shutil.copy2(
        ROOT / "schemas" / "source-manifest.schema.json",
        project / "schemas" / "source-manifest.schema.json",
    )
    shutil.copy2(ROOT / "index.json", project / "index.json")
    shutil.copy2(ROOT / "missing-issues.md", project / "missing-issues.md")
    manifest = json.loads(read_text(ROOT / "source-manifest.json"))
    manifest["papers"] = []
    manifest["batches"] = []
    (project / "source-manifest.json").write_text(
        canonical_json(manifest), encoding="utf-8"
    )

    legacy = json.loads(read_text(ROOT / "index.json"))
    for paper in legacy["papers"]:
        target = project / paper["dir"]
        (target / "figures").mkdir(parents=True)
        for name in ("questions.tex", "answers.tex"):
            shutil.copy2(ROOT / paper["dir"] / name, target / name)
        for figure in paper["figures"]:
            shutil.copy2(
                ROOT / paper["dir"] / "figures" / figure,
                target / "figures" / figure,
            )
    for entry in LEGACY_PAPERS:
        for suffix in ("_试题.md", "_答案要点.md", "_含解析.md"):
            relative = entry.markdown_prefix + suffix
            destination = repo / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / relative, destination)
    return repo, project


def migrate_arguments(project):
    return [
        "migrate-legacy-index",
        "--manifest", str(project / "source-manifest.json"),
        "--legacy-index", str(project / "index.json"),
        "--issues", str(project / "missing-issues.md"),
        "--output-manifest", str(project / "source-manifest.json"),
        "--output-index", str(project / "index.json"),
    ]


class IdentityTableTests(unittest.TestCase):
    def test_constant_table_maps_21_legacy_ids_verbatim(self):
        table = {entry.legacy_id: entry.paper_id for entry in LEGACY_PAPERS}
        self.assertEqual(len(LEGACY_PAPERS), 21)
        self.assertEqual(table, EXPECTED_PAPER_IDS)
        self.assertEqual(len(set(table.values())), 21)

    def test_markdown_prefixes_are_explicit_and_fall_in_four_fixed_groups(self):
        prefixes = [entry.markdown_prefix for entry in LEGACY_PAPERS]
        self.assertEqual(len(set(prefixes)), 21)
        self.assertEqual(
            set(entry.markdown_group for entry in LEGACY_PAPERS),
            set(MARKDOWN_GROUPS),
        )
        self.assertEqual(len(MARKDOWN_GROUPS), 4)
        for entry in LEGACY_PAPERS:
            with self.subTest(legacy_id=entry.legacy_id):
                self.assertTrue(
                    entry.markdown_prefix.startswith(""),
                    entry.markdown_prefix,
                )
                for suffix in ("_试题.md", "_答案要点.md", "_含解析.md"):
                    self.assertTrue(
                        (REPO / (entry.markdown_prefix + suffix)).is_file(),
                        entry.markdown_prefix + suffix,
                    )

    def test_six_batches_partition_all_21_papers_in_declared_order(self):
        expected = tuple(
            (batch_id, tuple(EXPECTED_PAPER_IDS[legacy] for legacy in members))
            for batch_id, members in EXPECTED_BATCHES
        )
        self.assertEqual(PHASE0_BATCHES, expected)
        self.assertEqual([len(members) for _, members in PHASE0_BATCHES],
                         [4, 4, 3, 4, 4, 2])
        members = [
            paper_id for _, paper_ids in PHASE0_BATCHES for paper_id in paper_ids
        ]
        self.assertEqual(len(members), 21)
        self.assertEqual(set(members), set(EXPECTED_PAPER_IDS.values()))


class MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.legacy = json.loads(read_text(ROOT / "index.json"))
        cls.manifest = json.loads(read_text(ROOT / "source-manifest.json"))
        cls.issues = load_issues(ROOT / "missing-issues.md")
        cls.migrated = migrate_legacy_index(
            cls.manifest, cls.legacy, repo_root=REPO, issues=cls.issues
        )
        cls.papers = {paper["paper_id"]: paper for paper in cls.migrated["papers"]}
        cls.by_legacy = {paper["id"]: paper for paper in cls.legacy["papers"]}

    def test_migration_produces_21_papers_and_6_planned_batches(self):
        self.assertEqual(len(self.migrated["papers"]), 21)
        self.assertEqual(
            [paper["paper_id"] for paper in self.migrated["papers"]],
            [entry.paper_id for entry in LEGACY_PAPERS],
        )
        self.assertEqual(
            sorted(project_index(self.migrated)),
            sorted(EXPECTED_PAPER_IDS.values()),
        )
        for paper in self.migrated["papers"]:
            with self.subTest(paper_id=paper["paper_id"]):
                self.assertEqual(paper["production_state"], "legacy_unverified")
                self.assertEqual(paper["source_ids"], [])
                # blocked 摘要由 Task 15 填写，迁移后必须仍是空的。
                self.assertIsNone(paper["blocked_from"])
                self.assertIsNone(paper["last_verified_hash"])
                self.assertIsNone(paper["resume_action"])
        self.assertEqual(
            [batch["batch_id"] for batch in self.migrated["batches"]],
            [batch_id for batch_id, _ in PHASE0_BATCHES],
        )
        for batch in self.migrated["batches"]:
            with self.subTest(batch_id=batch["batch_id"]):
                self.assertEqual(batch["status"], "planned")
                self.assertEqual(batch["issues"], [])
        self.assertEqual(
            [batch["paper_ids"] for batch in self.migrated["batches"]],
            [list(paper_ids) for _, paper_ids in PHASE0_BATCHES],
        )

    def test_migration_is_idempotent_and_preserves_revision_fields(self):
        again = migrate_legacy_index(
            self.migrated, self.legacy, repo_root=REPO, issues=self.issues
        )
        self.assertEqual(again, self.migrated)
        self.assertEqual(again["revision"], self.manifest["revision"])
        self.assertEqual(
            again["last_transaction_id"], self.manifest["last_transaction_id"]
        )
        self.assertEqual(again["sources"], self.manifest["sources"])

    def test_migration_refuses_to_overwrite_drifted_papers(self):
        drifted = copy.deepcopy(self.migrated)
        drifted["papers"][0]["production_state"] = "complete"
        with self.assertRaisesRegex(ValueError, "papers"):
            migrate_legacy_index(
                drifted, self.legacy, repo_root=REPO, issues=self.issues
            )

    def test_legacy_ids_and_gkpaperid_are_unchanged(self):
        for entry in LEGACY_PAPERS:
            paper = self.papers[entry.paper_id]
            legacy = self.by_legacy[entry.legacy_id]
            with self.subTest(legacy_id=entry.legacy_id):
                self.assertEqual(paper["legacy_ids"], [entry.legacy_id])
                self.assertEqual(paper["project_dir"], legacy["dir"])
                self.assertEqual(paper["question_count"], legacy["questions"])
                self.assertEqual(paper["title"], legacy["title"])
                self.assertEqual(paper["year"], legacy["year"])
                for edition in EDITIONS:
                    shell = ROOT / legacy["dir"] / (edition + ".tex")
                    self.assertEqual(
                        _PAPER_ID_RE.findall(read_text(shell)), [entry.legacy_id]
                    )

    def test_track_is_mapped_to_the_frozen_enum(self):
        expected = {"理科": "science", "文科": "arts", None: "none"}
        for entry in LEGACY_PAPERS:
            with self.subTest(legacy_id=entry.legacy_id):
                self.assertEqual(
                    self.papers[entry.paper_id]["track"],
                    expected[self.by_legacy[entry.legacy_id]["track"]],
                )
                self.assertEqual(self.papers[entry.paper_id]["track"], entry.track)

    def test_source_files_are_closed_four_keys_with_unique_explicit_paths(self):
        for entry in LEGACY_PAPERS:
            source_files = self.papers[entry.paper_id]["source_files"]
            with self.subTest(legacy_id=entry.legacy_id):
                self.assertEqual(set(source_files), set(SOURCE_FILE_KEYS))
                self.assertEqual(len(set(source_files.values())), 4)
                self.assertEqual(
                    source_files["questions"], entry.markdown_prefix + "_试题.md"
                )
                self.assertEqual(
                    source_files["answer_key"], entry.markdown_prefix + "_答案要点.md"
                )
                self.assertEqual(
                    source_files["solution_body"],
                    entry.markdown_prefix + "_解析正文.md",
                )
                self.assertEqual(
                    source_files["combined_rendered"],
                    entry.markdown_prefix + "_含解析.md",
                )
                # 解析正文由 Task 6–12 生成，此刻必须允许缺失。
                for key in ("questions", "answer_key", "combined_rendered"):
                    self.assertTrue((REPO / source_files[key]).is_file(), key)

    def test_only_the_2026_recall_paper_registers_a_legacy_source_file(self):
        recall = self.papers["gk-2026-regular-national-1-recall"]
        self.assertEqual(recall["source_ids"], [])
        relative = "2026/2026_数学真题_试题.md"
        self.assertEqual(
            recall["legacy_source_files"],
            [{"path": relative, "sha256": file_sha256(REPO / relative)}],
        )
        for paper_id, paper in self.papers.items():
            if paper_id == "gk-2026-regular-national-1-recall":
                continue
            with self.subTest(paper_id=paper_id):
                self.assertEqual(paper["legacy_source_files"], [])

    def test_figure_files_are_sorted_unique_and_match_reference_counts(self):
        baseline = json.loads(read_text(ROOT / "reports" / "legacy-baseline.json"))
        frozen = {
            paper["legacy_id"]: [figure["path"] for figure in paper["figures"]]
            for paper in baseline["papers"]
        }
        total = 0
        for entry in LEGACY_PAPERS:
            paper = self.papers[entry.paper_id]
            legacy = self.by_legacy[entry.legacy_id]
            figures = paper["figure_files"]
            paths = [figure["path"] for figure in figures]
            with self.subTest(legacy_id=entry.legacy_id):
                self.assertEqual(paths, sorted(paths))
                self.assertEqual(len(set(paths)), len(paths))
                self.assertEqual(paths, frozen[entry.legacy_id])
                self.assertEqual(
                    paths,
                    [
                        "%s/figures/%s" % (legacy["dir"], name)
                        for name in legacy["figures"]
                    ],
                )
                # 引用次数用旧 TeX 定位到具体图，用规范 Markdown 定位到数量。
                tex_counts = counted(
                    [
                        read_text(ROOT / legacy["dir"] / name)
                        for name in ("questions.tex", "answers.tex")
                    ],
                    _FIGURE_INPUT_RE,
                )
                markdown_counts = counted(
                    [
                        read_text(REPO / paper["source_files"][key])
                        for key in ("questions", "combined_rendered")
                    ],
                    _MARKDOWN_IMAGE_RE,
                )
                occurrences = [figure["expected_occurrences"] for figure in figures]
                self.assertTrue(all(count > 0 for count in occurrences))
                self.assertEqual(
                    sorted(occurrences), sorted(markdown_counts.values())
                )
                self.assertEqual(sum(occurrences), sum(markdown_counts.values()))
                for figure in figures:
                    stem = Path(figure["path"]).stem
                    self.assertEqual(
                        figure["expected_occurrences"], tex_counts[stem], stem
                    )
                total += len(figures)
        self.assertEqual(total, 59)

    def test_seed_issue_ids_are_reverse_linked_to_their_papers(self):
        self.assertEqual(
            self.papers["gk-2026-regular-national-1-recall"]["issue_ids"],
            ["ISSUE-0001"],
        )
        for paper_id in (
            "gk-2017-regular-national-1-arts", "gk-2017-regular-national-1-science"
        ):
            with self.subTest(paper_id=paper_id):
                self.assertEqual(self.papers[paper_id]["issue_ids"], ["ISSUE-0002"])
        linked = {"gk-2026-regular-national-1-recall",
                  "gk-2017-regular-national-1-arts",
                  "gk-2017-regular-national-1-science"}
        for paper_id, paper in self.papers.items():
            if paper_id in linked:
                continue
            with self.subTest(paper_id=paper_id):
                self.assertEqual(paper["issue_ids"], [])

    def test_seed_issues_stay_open_blocking_and_shaped_as_designed(self):
        by_id = {issue["issue_id"]: issue for issue in self.issues}
        self.assertIn("ISSUE-0001", by_id)
        self.assertIn("ISSUE-0002", by_id)
        for issue_id in ("ISSUE-0001", "ISSUE-0002"):
            issue = by_id[issue_id]
            with self.subTest(issue_id=issue_id):
                self.assertEqual(issue["type"], "identity-ambiguous")
                self.assertEqual(issue["status"], "open")
                self.assertEqual(issue["impact"], "blocks_completion")
        self.assertEqual(
            by_id["ISSUE-0001"]["paper_id"], "gk-2026-regular-national-1-recall"
        )
        self.assertEqual(by_id["ISSUE-0001"]["affected_paper_ids"], [])
        self.assertIsNone(by_id["ISSUE-0002"]["paper_id"])
        self.assertEqual(
            by_id["ISSUE-0002"]["affected_paper_ids"],
            sorted([
                "gk-2017-regular-national-1-arts",
                "gk-2017-regular-national-1-science",
            ]),
        )

    def test_missing_or_drifted_seed_issue_blocks_the_whole_migration(self):
        for mutation in ("missing", "resolved", "retargeted"):
            issues = copy.deepcopy(self.issues)
            if mutation == "missing":
                issues = [item for item in issues if item["issue_id"] != "ISSUE-0001"]
            elif mutation == "resolved":
                issues[0]["status"] = "resolved"
            else:
                issues[1]["affected_paper_ids"] = ["gk-2018-regular-national-1-arts"]
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError):
                    migrate_legacy_index(
                        self.manifest, self.legacy, repo_root=REPO, issues=issues
                    )

    def test_migration_rejects_legacy_index_with_unknown_or_missing_ids(self):
        dropped = copy.deepcopy(self.legacy)
        dropped["papers"] = dropped["papers"][:-1]
        with self.assertRaisesRegex(ValueError, "旧 ID"):
            migrate_legacy_index(
                self.manifest, dropped, repo_root=REPO, issues=self.issues
            )
        renamed = copy.deepcopy(self.legacy)
        renamed["papers"][0]["id"] = "2017li-new"
        with self.assertRaisesRegex(ValueError, "旧 ID"):
            migrate_legacy_index(
                self.manifest, renamed, repo_root=REPO, issues=self.issues
            )

    def test_migrated_manifest_passes_schema_and_semantics(self):
        schema = json.loads(read_text(ROOT / "schemas" / "source-manifest.schema.json"))
        validate(self.migrated, schema)


class IndexProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = json.loads(read_text(ROOT / "index.json"))
        cls.legacy = legacy_index_view(cls.current)
        cls.manifest = json.loads(read_text(ROOT / "source-manifest.json"))
        cls.migrated = migrate_legacy_index(
            cls.manifest,
            cls.legacy,
            repo_root=REPO,
            issues=load_issues(ROOT / "missing-issues.md"),
        )
        cls.projected = project_legacy_index(cls.migrated, cls.legacy)

    def test_projection_is_idempotent_over_an_already_projected_index(self):
        self.assertEqual(
            project_legacy_index(self.migrated, self.current), self.projected
        )

    def test_projection_only_adds_paper_id_legacy_ids_and_batches(self):
        self.assertEqual(
            set(self.projected) - set(self.legacy), {"batches"}
        )
        self.assertEqual(set(self.legacy) - set(self.projected), set())
        for key in set(self.legacy) - {"papers"}:
            with self.subTest(key=key):
                self.assertEqual(self.projected[key], self.legacy[key])
        for projected, legacy in zip(self.projected["papers"], self.legacy["papers"]):
            with self.subTest(legacy_id=legacy["id"]):
                self.assertEqual(
                    set(projected) - set(legacy), {"paper_id", "legacy_ids"}
                )
                for key in legacy:
                    self.assertEqual(projected[key], legacy[key], key)
                self.assertEqual(projected["paper_id"], EXPECTED_PAPER_IDS[legacy["id"]])
                self.assertEqual(projected["legacy_ids"], [legacy["id"]])

    def test_projection_carries_the_six_batches(self):
        self.assertEqual(self.projected["batches"], self.migrated["batches"])

    def test_projection_rejects_a_legacy_index_the_manifest_does_not_cover(self):
        foreign = copy.deepcopy(self.legacy)
        foreign["papers"][0]["id"] = "2017li-new"
        with self.assertRaises(ValueError):
            project_legacy_index(self.migrated, foreign)


class SourceStateTests(unittest.TestCase):
    def source(self, **updates):
        source = {
            "source_id": "src-1",
            "source_state": "not_started",
            "paper_relation": None,
            "paper_id": None,
            "artifact": None,
        }
        source.update(updates)
        return source

    def test_ready_requires_a_verified_artifact(self):
        known = {"gk-2017-regular-national-1-science"}
        with self.assertRaisesRegex(ValueError, "artifact|ready"):
            validate_source_state(self.source(source_state="ready"), known)
        validate_source_state(
            self.source(source_state="ready", artifact={"sha256": "a" * 64}), known
        )

    def test_non_ready_states_must_not_carry_an_artifact(self):
        known = set()
        for state in ("not_started", "blocked", "non_paper"):
            with self.subTest(state=state):
                with self.assertRaisesRegex(ValueError, "artifact|ready"):
                    validate_source_state(
                        self.source(source_state=state, artifact={"sha256": "a" * 64}),
                        known,
                    )

    def test_confirmed_relation_requires_ready_and_an_existing_paper(self):
        known = {"gk-2017-regular-national-1-science"}
        validate_source_state(
            self.source(
                source_state="ready",
                artifact={"sha256": "a" * 64},
                paper_relation="canonical",
                paper_id="gk-2017-regular-national-1-science",
            ),
            known,
        )
        with self.assertRaisesRegex(ValueError, "paper_id"):
            validate_source_state(
                self.source(
                    source_state="ready",
                    artifact={"sha256": "a" * 64},
                    paper_relation="canonical",
                ),
                known,
            )
        with self.assertRaisesRegex(ValueError, "paper_id"):
            validate_source_state(
                self.source(
                    source_state="ready",
                    artifact={"sha256": "a" * 64},
                    paper_relation="canonical",
                    paper_id="gk-9999-regular-national-1",
                ),
                known,
            )

    def test_not_started_blocked_and_non_paper_reject_confirmed_relations(self):
        known = {"gk-2017-regular-national-1-science"}
        for state in ("not_started", "blocked", "non_paper"):
            with self.subTest(state=state):
                with self.assertRaisesRegex(ValueError, "确认关系"):
                    validate_source_state(
                        self.source(
                            source_state=state,
                            paper_relation="canonical",
                            paper_id="gk-2017-regular-national-1-science",
                        ),
                        known,
                    )
        with self.assertRaisesRegex(ValueError, "non_paper"):
            validate_source_state(
                self.source(
                    source_state="non_paper",
                    paper_id="gk-2017-regular-national-1-science",
                ),
                known,
            )

    def test_unknown_state_and_relation_values_are_rejected(self):
        known = {"gk-2017-regular-national-1-science"}
        with self.assertRaisesRegex(ValueError, "source_state"):
            validate_source_state(self.source(source_state="done"), known)
        with self.assertRaisesRegex(ValueError, "paper_relation"):
            validate_source_state(
                self.source(
                    source_state="ready",
                    artifact={"sha256": "a" * 64},
                    paper_relation="probably",
                    paper_id="gk-2017-regular-national-1-science",
                ),
                known,
            )


class SchemaFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            read_text(ROOT / "schemas" / "source-manifest.schema.json")
        )

    def test_minimal_paper_and_batch_pass(self):
        validate(minimal_manifest(), self.schema)

    def test_paper_and_batch_shapes_are_closed(self):
        cases = {
            "unknown_paper_field": ("papers", 0, {"reviewed": True}),
            "unknown_batch_field": ("batches", 0, {"owner": "task-99"}),
        }
        for name, (section, index, update) in cases.items():
            manifest = minimal_manifest()
            manifest[section][index].update(update)
            with self.subTest(case=name), self.assertRaises(SchemaError):
                validate(manifest, self.schema)

    def test_frozen_enums_and_bounds_are_enforced(self):
        mutations = {
            "production_state": lambda m: m["papers"][0].update(
                {"production_state": "almost_done"}
            ),
            "batch_status": lambda m: m["batches"][0].update({"status": "done"}),
            "track": lambda m: m["papers"][0].update({"track": "理科"}),
            "zero_occurrences": lambda m: m["papers"][0]["figure_files"][0].update(
                {"expected_occurrences": 0}
            ),
            "missing_source_file_key": lambda m: m["papers"][0]["source_files"].pop(
                "solution_body"
            ),
            "extra_source_file_key": lambda m: m["papers"][0]["source_files"].update(
                {"printable": "2017/x.md"}
            ),
            "empty_legacy_ids": lambda m: m["papers"][0].update({"legacy_ids": []}),
            "bad_legacy_source_sha": lambda m: m["papers"][0].update(
                {"legacy_source_files": [{"path": "2026/a.md",
                                          "sha256": "z" * 64}]}
            ),
            "bad_paper_id": lambda m: m["papers"][0].update({"paper_id": "2017li"}),
            "bad_batch_id": lambda m: m["batches"][0].update({"batch_id": "b1"}),
            "bad_blocked_from": lambda m: m["papers"][0].update(
                {"blocked_from": "almost_done"}
            ),
            "bad_last_verified_hash": lambda m: m["papers"][0].update(
                {"last_verified_hash": "not-a-hash"}
            ),
            "empty_resume_action": lambda m: m["papers"][0].update(
                {"resume_action": ""}
            ),
        }
        for name, mutate in mutations.items():
            manifest = minimal_manifest()
            mutate(manifest)
            with self.subTest(case=name), self.assertRaises(SchemaError):
                validate(manifest, self.schema)

    def test_state_enums_match_the_approved_design(self):
        self.assertEqual(
            list(PRODUCTION_STATES),
            [
                "legacy_unverified", "planned", "source_ready",
                "transcription_draft", "questions_verified", "answers_draft",
                "answers_verified", "shared_frozen", "editions_generated",
                "compiled", "complete", "blocked",
            ],
        )
        self.assertEqual(
            list(BATCH_STATUSES),
            [
                "planned", "provenance_verified", "compiled_pending_review",
                "closed", "closed_with_blockers",
            ],
        )


class MigrateCommandTests(unittest.TestCase):
    def test_command_writes_index_issues_and_manifest_in_one_state_transaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            revision = json.loads(
                read_text(project / "source-manifest.json")
            )["revision"]
            before = (project / "source-manifest.json").read_bytes()
            with mock.patch("source_manifest.Transaction") as transaction_type:
                transaction = transaction_type.return_value
                transaction.transaction_id = "11111111-1111-4111-8111-111111111111"
                self.assertEqual(main(migrate_arguments(project)), 0)
            transaction.prepare.assert_called_once()
            transaction.commit.assert_called_once_with()
            arguments = transaction.prepare.call_args
            self.assertEqual(arguments.args[0], "state")
            self.assertEqual(
                list(arguments.args[1]),
                [
                    "math-gaokao-latex/index.json",
                    "math-gaokao-latex/missing-issues.md",
                    MANIFEST_TARGET,
                ],
            )
            self.assertEqual(arguments.kwargs["inputs"], {})
            self.assertEqual(arguments.kwargs["expected_revision"], revision)
            staged = json.loads(arguments.args[1][MANIFEST_TARGET].decode("utf-8"))
            self.assertEqual(staged["revision"], revision + 1)
            self.assertEqual(
                staged["last_transaction_id"], transaction.transaction_id
            )
            self.assertEqual(len(staged["papers"]), 21)
            # 被 mock 的事务不落盘，工作树必须原样。
            self.assertEqual((project / "source-manifest.json").read_bytes(), before)

    def test_command_migrates_in_place_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            manifest_path = project / "source-manifest.json"
            index_path = project / "index.json"
            issues_path = project / "missing-issues.md"
            revision = json.loads(read_text(manifest_path))["revision"]
            issues_before = issues_path.read_bytes()

            self.assertEqual(main(migrate_arguments(project)), 0)
            manifest = load_manifest(manifest_path)
            self.assertEqual(len(manifest["papers"]), 21)
            self.assertEqual(len(manifest["batches"]), 6)
            self.assertEqual(manifest["revision"], revision + 1)
            self.assertIsNotNone(manifest["last_transaction_id"])
            index = json.loads(read_text(index_path))
            self.assertEqual(len(index["batches"]), 6)
            self.assertEqual(issues_path.read_bytes(), issues_before)
            self.assertEqual(
                [issue["issue_id"] for issue in load_issues(issues_path)],
                ["ISSUE-0001", "ISSUE-0002"],
            )

            manifest_bytes = manifest_path.read_bytes()
            index_bytes = index_path.read_bytes()
            self.assertEqual(main(migrate_arguments(project)), 0)
            self.assertEqual(manifest_path.read_bytes(), manifest_bytes)
            self.assertEqual(index_path.read_bytes(), index_bytes)
            self.assertEqual(issues_path.read_bytes(), issues_before)

    def test_command_writes_nothing_when_a_seed_issue_drifted(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            issues_path = project / "missing-issues.md"
            issues_path.write_text(
                read_text(issues_path).replace('"status": "open"', '"status": "deferred"'),
                encoding="utf-8",
            )
            manifest_before = (project / "source-manifest.json").read_bytes()
            index_before = (project / "index.json").read_bytes()
            issues_before = issues_path.read_bytes()
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaises(ValueError):
                    main(migrate_arguments(project))
            self.assertEqual(
                (project / "source-manifest.json").read_bytes(), manifest_before
            )
            self.assertEqual((project / "index.json").read_bytes(), index_before)
            self.assertEqual(issues_path.read_bytes(), issues_before)

    def test_command_requires_the_canonical_manifest_output_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            arguments = migrate_arguments(project)
            arguments[arguments.index("--output-manifest") + 1] = str(
                project / "copy-manifest.json"
            )
            with self.assertRaisesRegex(ValueError, MANIFEST_TARGET):
                main(arguments)

    def test_parser_requires_all_five_paths(self):
        stderr = io.StringIO()
        complete = [
            "migrate-legacy-index",
            "--manifest", "m", "--legacy-index", "i", "--issues", "s",
            "--output-manifest", "om", "--output-index", "oi",
        ]
        for index in range(1, len(complete), 2):
            partial = complete[:index] + complete[index + 2:]
            with self.subTest(dropped=complete[index]), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    main(partial)
                self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()

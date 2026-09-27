import copy
import io
import json
import posixpath
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
from issues import main as issues_main
from manifest import canonical_json, file_sha256, load_manifest, project_index
from schema_validate import SchemaError, validate
from transaction import MANIFEST_TARGET
import source_manifest as source_manifest_module
from source_manifest import (
    BATCH_STATUSES,
    LEGACY_PAPERS,
    MARKDOWN_GROUPS,
    PHASE0_BATCHES,
    PHASE0_ISSUE_SEEDS,
    PRODUCTION_STATES,
    SOURCE_FILE_KEYS,
    main,
    migrate_legacy_index,
    project_legacy_index,
    state_figure_occurrences,
    validate_figure_occurrences,
    validate_source_state,
    verify_phase0_issue_seeds,
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


def ordered_counted(texts, pattern):
    """按首次出现顺序统计，返回 (顺序列表, 计数字典)——与工具侧配对口径一致。"""
    order, counts = [], {}
    for text in texts:
        for match in pattern.finditer(text):
            key = match.group(1)
            if key not in counts:
                order.append(key)
                counts[key] = 0
            counts[key] += 1
    return order, counts


def migration_anchor():
    """legacy 基线钉死的迁移前 HEAD，同 baseline.recover_legacy_index 的锚点手法。"""
    baseline = json.loads(read_text(ROOT / "reports" / "legacy-baseline.json"))
    head = baseline["repository"]["head"]
    if not isinstance(head, str) or not head:
        raise ValueError("legacy 基线缺少 repository.head 锚点")
    return head


def read_text_at(head, relative):
    """从 git 锚点取回文件文本；取不到一律报错，不得静默跳过。"""
    return subprocess.check_output(
        ["git", "-C", str(REPO), "show", "%s:%s" % (head, relative)],
        stderr=subprocess.DEVNULL,
    ).decode("utf-8")


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


def seed_issue_ledger(path):
    """写一份 phase0 种子问题总账（两条身份问题，皆 open）并返回解析结果。

    **迁移测试一律用它，不用 live 的 `missing-issues.md`**：迁移是一次性历史动作，它
    当时看到的世界就是这两条种子。live 总账会随业务推进（T17 逐卷核验后 ISSUE-0002
    收口成 resolved、逐题问题陆续登记），拿它当迁移输入等于把「仓库停在迁移完成那一
    瞬间」当作不变量——那不是不变量，那是当时的快照。
    """
    issues_main(["init", "--phase0-seed", "--output", str(path)])
    return load_issues(path)


def legacy_index():
    """live index 中只取冻结的 21 个 legacy 条目，重建一次性迁移输入。"""
    document = json.loads(read_text(ROOT / "index.json"))
    legacy_ids = {entry.legacy_id for entry in LEGACY_PAPERS}
    document["papers"] = [
        paper for paper in document["papers"] if paper.get("id") in legacy_ids
    ]
    return document


def premigration_manifest():
    """迁移前的 manifest：papers / batches 尚未写入。

    live manifest 的 papers 已随批次推进（`production_state` / `issue_ids` 都动过），
    拿它喂 `migrate_legacy_index()` 会撞上「拒绝覆盖已推进状态」的护栏——**那条护栏是
    对的**，错的是把 live 状态当成迁移输入。

    source 的绑定也要一并解除：T4 的迁移**刻意不建立任何 source↔paper 绑定**，绑定是
    T17 用 `confirm-source` 建的。只清 papers 不清绑定，会留下「source 指着一个
    `source_ids` 为空的 paper」的半截世界，双向关系当场校验不过。
    """
    manifest = json.loads(read_text(ROOT / "source-manifest.json"))
    manifest["papers"] = []
    manifest["batches"] = []
    for source in manifest["sources"]:
        source["paper_id"] = None
        source["paper_relation"] = None
    return manifest


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
    (project / "index.json").write_text(
        json.dumps(legacy_index(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    # 问题总账同样回到迁移前：manifest 回退了、总账不回退，那就不是「迁移前状态」。
    seed_issue_ledger(project / "missing-issues.md")
    (project / "source-manifest.json").write_text(
        canonical_json(premigration_manifest()), encoding="utf-8"
    )

    legacy = legacy_index()
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
    """迁移语义：在**迁移前的世界**上跑，与 live 仓库当前推进到哪一批解耦。"""

    @classmethod
    def setUpClass(cls):
        cls.legacy = legacy_index()
        cls.manifest = premigration_manifest()
        cls.temporary = tempfile.TemporaryDirectory()
        cls.issues = seed_issue_ledger(
            Path(cls.temporary.name) / "missing-issues.md"
        )
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
                expected_frozen = list(frozen[entry.legacy_id])
                if entry.legacy_id == "2019li":
                    # 178b4c31：迁移后补回、已独立核验的六爻矢量图；冻结迁移
                    # 基线本身不应被改写，但 live figure tree 必须纳入它。
                    expected_frozen.append(
                        "2019_全国Ⅰ卷_理科/figures/f2019_t6_hexagram.tex"
                    )
                self.assertEqual(paths, expected_frozen)
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
                # 逐图对位：figure 由 legacy TeX 的引用顺序定位，次数取自**规范 Markdown**。
                # 内容迁移后规范 Markdown 才是图引用的唯一事实源，legacy TeX 是滞后
                # 派生物（T13 重生成 editions 时追平），故此处**不再**与 tex_counts 比数；
                # 「Markdown == legacy TeX」只对冻结迁移态成立，已移到下面的锚点测试。
                self.assertEqual(len(tex_counts), len(markdown_counts))
                tex_order, _ = ordered_counted(
                    [
                        read_text(ROOT / legacy["dir"] / name)
                        for name in ("questions.tex", "answers.tex")
                    ],
                    _FIGURE_INPUT_RE,
                )
                image_order, image_counts = ordered_counted(
                    [
                        read_text(REPO / paper["source_files"][key])
                        for key in ("questions", "combined_rendered")
                    ],
                    _MARKDOWN_IMAGE_RE,
                )
                by_stem = {
                    stem: image_counts[image]
                    for stem, image in zip(tex_order, image_order)
                }
                for figure in figures:
                    stem = Path(figure["path"]).stem
                    self.assertEqual(
                        figure["expected_occurrences"], by_stem[stem], stem
                    )
                total += len(figures)
        self.assertEqual(total, 60)

    def test_frozen_migration_state_markdown_matched_legacy_tex(self):
        """「Markdown 计数 == legacy TeX 计数」这条等式只对**冻结迁移态**成立。

        它此前被当成 live 树不变式，而它在 f2018wen_t19_grid 上恰好成立于
        「旧 _含解析.md 用占位符丢了那张图」这个 bug 之上——内容迁移修掉 bug 后
        等式即破。这里把它钉到 legacy 基线的 git 锚点（迁移前的树），
        断言本身一字不改，只是绑到它真正成立的那棵树上。
        """
        head = migration_anchor()
        total = 0
        for entry in LEGACY_PAPERS:
            paper = self.papers[entry.paper_id]
            legacy = self.by_legacy[entry.legacy_id]
            with self.subTest(legacy_id=entry.legacy_id):
                tex_order, tex_counts = ordered_counted(
                    [
                        read_text_at(
                            head,
                            "math-gaokao-latex/%s/%s" % (legacy["dir"], name),
                        )
                        for name in ("questions.tex", "answers.tex")
                    ],
                    _FIGURE_INPUT_RE,
                )
                image_order, image_counts = ordered_counted(
                    [
                        read_text_at(head, paper["source_files"][key])
                        for key in ("questions", "combined_rendered")
                    ],
                    _MARKDOWN_IMAGE_RE,
                )
                self.assertEqual(len(image_order), len(tex_order))
                for stem, image in zip(tex_order, image_order):
                    self.assertEqual(image_counts[image], tex_counts[stem], stem)
                total += len(tex_order)
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

    def test_the_seed_ledger_is_shaped_as_designed(self):
        """这一条描述的是**种子总账**（迁移当时的世界），不是 live 总账的现状。

        live 侧的不变量在 `LiveSeedIssueInvariantTests`：身份不变、状态可推进。
        """
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
        """**身份**漂移一律拦下；生命周期推进不算漂移（见下一条）。"""
        for mutation in ("missing", "retargeted", "retyped", "recoded", "downgraded"):
            issues = copy.deepcopy(self.issues)
            if mutation == "missing":
                issues = [item for item in issues if item["issue_id"] != "ISSUE-0001"]
            elif mutation == "retargeted":
                issues[1]["affected_paper_ids"] = ["gk-2018-regular-national-1-arts"]
            elif mutation == "retyped":
                issues[0]["type"] = "source-mismatch"
            elif mutation == "recoded":
                issues[0]["conflict_code"] = "换了一个码"
            else:
                # 未了结却降级成 non_blocking：在不解决它的前提下解除封锁，是绕过不是推进。
                issues[0]["impact"] = "non_blocking"
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError):
                    migrate_legacy_index(
                        self.manifest, self.legacy, repo_root=REPO, issues=issues
                    )

    def test_a_resolved_seed_issue_is_lifecycle_not_drift(self):
        """T17 逐卷核验后把 ISSUE-0002 收口成 resolved——守卫必须放行。

        把状态钉死在 open 会让「这条种子问题被解决了」与「这条种子问题被人换掉了」在
        报错上不可区分，而守卫要拦的只有后者。resolved 之后它不再反链进迁移产出的
        `issue_ids`（`_issue_ids_by_paper` 跳过 resolved），这正是 live 仓库现在的形状。
        """
        issues = copy.deepcopy(self.issues)
        for item in issues:
            if item["issue_id"] == "ISSUE-0002":
                item["status"] = "resolved"
        migrated = migrate_legacy_index(
            self.manifest, self.legacy, repo_root=REPO, issues=issues
        )
        papers = {paper["paper_id"]: paper for paper in migrated["papers"]}
        for paper_id in (
            "gk-2017-regular-national-1-arts", "gk-2017-regular-national-1-science"
        ):
            with self.subTest(paper_id=paper_id):
                self.assertEqual(papers[paper_id]["issue_ids"], [])
        self.assertEqual(
            papers["gk-2026-regular-national-1-recall"]["issue_ids"], ["ISSUE-0001"]
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


class LiveSeedIssueInvariantTests(unittest.TestCase):
    """live 问题总账：种子问题的**身份**必须不变，状态允许推进。

    与 `MigrationTests` 分工明确——那边测「迁移这个动作」（跑在迁移前的世界上），这边
    测「live 仓库此刻仍满足的不变量」。把两者混在一起，就会写出「21 卷仍停在迁移完成
    瞬间」这种会随每一批导入而失效的假不变量。
    """

    @classmethod
    def setUpClass(cls):
        cls.issues = load_issues(ROOT / "missing-issues.md")
        cls.by_id = {issue["issue_id"]: issue for issue in cls.issues}
        cls.papers = project_index(load_manifest(ROOT / "source-manifest.json"))

    def test_the_live_ledger_still_passes_the_seed_identity_guard(self):
        verify_phase0_issue_seeds(self.issues)

    def test_the_live_seed_identities_match_the_frozen_seeds(self):
        for seed in PHASE0_ISSUE_SEEDS:
            issue = self.by_id.get(seed["issue_id"])
            with self.subTest(issue_id=seed["issue_id"]):
                self.assertIsNotNone(issue)
                for field in (
                    "type", "paper_id", "affected_paper_ids", "conflict_code"
                ):
                    self.assertEqual(issue.get(field), seed[field], field)

    def test_an_unresolved_seed_issue_still_blocks(self):
        for issue in self.by_id.values():
            if issue["issue_id"] in {"ISSUE-0001", "ISSUE-0002"}:
                with self.subTest(issue_id=issue["issue_id"]):
                    if issue["status"] != "resolved":
                        self.assertEqual(issue["impact"], "blocks_completion")

    def test_the_2017_pair_keeps_referencing_issue_0002(self):
        """收口不等于抹掉档案：两卷的 `issue_ids` 仍**包含** ISSUE-0002。

        断言用「包含」而不是「等于」——逐题问题会随批次导入不断追加，写死等号就等于
        要求每导一批就来改一次测试。
        """
        for paper_id in (
            "gk-2017-regular-national-1-arts", "gk-2017-regular-national-1-science"
        ):
            with self.subTest(paper_id=paper_id):
                self.assertIn("ISSUE-0002", self.papers[paper_id]["issue_ids"])


class IndexProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = legacy_index()
        cls.legacy = legacy_index_view(cls.current)
        cls.manifest = premigration_manifest()
        cls.temporary = tempfile.TemporaryDirectory()
        cls.migrated = migrate_legacy_index(
            cls.manifest,
            cls.legacy,
            repo_root=REPO,
            issues=seed_issue_ledger(
                Path(cls.temporary.name) / "missing-issues.md"
            ),
        )
        cls.projected = project_legacy_index(cls.migrated, cls.legacy)

    def test_projection_is_idempotent_over_an_already_projected_index(self):
        self.assertEqual(
            project_legacy_index(self.migrated, self.current), self.projected
        )

    def test_projection_only_adds_paper_id_and_legacy_ids(self):
        self.assertEqual(set(self.projected) - set(self.legacy), set())
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

    def test_projection_carries_no_runtime_state(self):
        """投影只带静态身份：批次段与任何运行态字段都不得出现在 index 里。

        index.json 落在 build 回执的 `generation_input_tree` 内——一旦批次状态被投影
        进来，推进一次批次状态就会让 21 份回执连锁 stale，「推进状态」与「保持产物当前」
        就变成互斥的两件事。运行态的唯一住处是 manifest。
        """
        self.assertNotIn("batches", self.projected)
        for paper in self.projected["papers"]:
            for runtime in (
                "production_state", "issue_ids", "blocked_from", "resume_action",
                "last_verified_hash", "source_ids", "legacy_source_files",
            ):
                self.assertNotIn(runtime, paper)

    def test_projection_drops_a_smuggled_batches_section(self):
        smuggled = copy.deepcopy(self.legacy)
        smuggled["batches"] = [{"batch_id": "phase0-b01"}]
        self.assertNotIn("batches", project_legacy_index(self.migrated, smuggled))

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

    def test_empty_legacy_ids_pass_schema_for_newly_transcribed_papers(self):
        """阶段 1 起新转录的卷没有旧 ID，编一个即伪造历史身份。

        约束没有取消，只是从 schema 的 `minItems` 移到了更准的位置：
        `source_manifest._validate_paper_semantics()` 定向核对**迁移卷**的 legacy_ids
        必须与冻结常量表逐字相等（见 test_source_manifest.RegisterPapersTests）。
        """
        manifest = minimal_manifest()
        manifest["papers"][0]["legacy_ids"] = []
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


class FigureOccurrenceGuardTests(unittest.TestCase):
    """live 树主守卫：规范 Markdown 引用数 == manifest expected_occurrences。

    内容迁移后规范 Markdown 是唯一事实源，所以「防丢图」不能再靠 legacy TeX 对账，
    必须靠 manifest 登记值对账。任何未经 manifest 登记的漂移（丢图或多图）都得硬错。
    """

    def _replace_images_with_registered_links(self, repo, project, paper):
        tex_order, _ = ordered_counted(
            [
                read_text(project / paper["project_dir"] / "questions.tex"),
                read_text(project / paper["project_dir"] / "answers.tex"),
            ],
            _FIGURE_INPUT_RE,
        )
        image_order, _ = ordered_counted(
            [
                read_text(repo / paper["source_files"][key])
                for key in ("questions", "combined_rendered")
            ],
            _MARKDOWN_IMAGE_RE,
        )
        self.assertEqual(len(image_order), len(tex_order))
        figure_by_image = dict(zip(image_order, tex_order))
        rewritten_count = 0
        for key in ("questions", "combined_rendered"):
            source = repo / paper["source_files"][key]
            text = source.read_text(encoding="utf-8")

            def to_registered_link(match):
                figure_path = "%s/%s/figures/%s.tex" % (
                    "math-gaokao-latex",
                    paper["project_dir"],
                    figure_by_image[match.group(1)],
                )
                target = posixpath.relpath(
                    figure_path,
                    posixpath.dirname(paper["source_files"][key]),
                )
                return "[题图](%s)" % target

            linked, count = _MARKDOWN_IMAGE_RE.subn(to_registered_link, text)
            rewritten_count += count
            source.write_text(linked, encoding="utf-8")
        return rewritten_count

    def test_real_repository_matches_the_registered_occurrences(self):
        manifest = json.loads(read_text(ROOT / "source-manifest.json"))
        # 不抛异常即通过；真实仓库必须始终与登记值一致。
        self.assertEqual(
            validate_figure_occurrences(manifest, REPO),
            sum(len(paper["figure_files"]) for paper in manifest["papers"]),
        )

    def test_a_dropped_figure_reference_is_a_hard_error(self):
        # 反事实：假如生成器再丢一张图，套件必须红。这是本守卫存在的唯一理由。
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            migrated = migrate_legacy_index(
                json.loads(read_text(project / "source-manifest.json")),
                json.loads(read_text(project / "index.json")),
                repo_root=repo,
                issues=load_issues(project / "missing-issues.md"),
            )
            self.assertEqual(validate_figure_occurrences(migrated, repo), 60)

            paper = {item["paper_id"]: item for item in migrated["papers"]}[
                "gk-2018-regular-national-1-arts"
            ]
            combined = repo / paper["source_files"]["combined_rendered"]
            text = combined.read_text(encoding="utf-8")
            dropped = _MARKDOWN_IMAGE_RE.sub("", text, count=1)
            self.assertNotEqual(dropped, text)
            combined.write_text(dropped, encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                validate_figure_occurrences(migrated, repo)
            self.assertIn("引用次数与 manifest 登记不一致", str(caught.exception))

    def test_an_extra_figure_reference_is_also_a_hard_error(self):
        # 漂移的**两个方向**都必须硬错，否则守卫只挡一半。
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            migrated = migrate_legacy_index(
                json.loads(read_text(project / "source-manifest.json")),
                json.loads(read_text(project / "index.json")),
                repo_root=repo,
                issues=load_issues(project / "missing-issues.md"),
            )
            paper = {item["paper_id"]: item for item in migrated["papers"]}[
                "gk-2018-regular-national-1-arts"
            ]
            combined = repo / paper["source_files"]["combined_rendered"]
            text = combined.read_text(encoding="utf-8")
            first = _MARKDOWN_IMAGE_RE.search(text)
            combined.write_text(text + "\n\n" + first.group(0) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError) as caught:
                validate_figure_occurrences(migrated, repo)
            self.assertIn("引用次数与 manifest 登记不一致", str(caught.exception))

    def test_registered_local_tex_links_are_counted_as_figure_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            migrated = migrate_legacy_index(
                json.loads(read_text(project / "source-manifest.json")),
                json.loads(read_text(project / "index.json")),
                repo_root=repo,
                issues=load_issues(project / "missing-issues.md"),
            )
            paper = next(
                item for item in migrated["papers"]
                if item["paper_id"] == "gk-2017-regular-national-1-science"
            )
            rewritten_count = self._replace_images_with_registered_links(
                repo, project, paper
            )

            self.assertEqual(
                rewritten_count,
                sum(figure["expected_occurrences"] for figure in paper["figure_files"]),
            )
            (project / paper["project_dir"] / "questions.tex").unlink()
            (project / paper["project_dir"] / "answers.tex").unlink()
            self.assertEqual(validate_figure_occurrences(migrated, repo), 60)

    def test_a_tex_link_to_an_unregistered_figure_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            migrated = migrate_legacy_index(
                json.loads(read_text(project / "source-manifest.json")),
                json.loads(read_text(project / "index.json")),
                repo_root=repo,
                issues=load_issues(project / "missing-issues.md"),
            )
            paper = next(
                item for item in migrated["papers"]
                if item["paper_id"] == "gk-2017-regular-national-1-science"
            )
            self._replace_images_with_registered_links(repo, project, paper)
            combined = repo / paper["source_files"]["combined_rendered"]
            text = combined.read_text(encoding="utf-8")
            invalid = "../math-gaokao-latex/%s/figures/not-registered.tex" % paper[
                "project_dir"
            ]
            linked, count = re.subn(
                r"(?m)^\[题图\]\([^)]+\)$",
                "[题图](%s)" % invalid,
                text,
                count=1,
            )
            self.assertEqual(count, 1)
            combined.write_text(linked, encoding="utf-8")

            with self.assertRaises(ValueError) as caught:
                validate_figure_occurrences(migrated, repo)
            self.assertIn("图稿链接", str(caught.exception))


class SyncFigureOccurrencesTests(unittest.TestCase):
    """窄入口：唯一允许改写 expected_occurrences 的正规路径。"""

    def _migrated_fixture(self, tmp):
        repo, project = fixture_repository(tmp)
        self.assertEqual(main(migrate_arguments(project)), 0)
        return repo, project / "source-manifest.json"

    def test_advances_the_registered_count_in_a_state_transaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path = self._migrated_fixture(tmp)
            manifest = json.loads(read_text(manifest_path))
            before = manifest["revision"]
            # 人为把一个登记值改错，模拟「内容迁移合法改变了图引用数」
            manifest["papers"][3]["figure_files"][0]["expected_occurrences"] += 3
            manifest_path.write_text(canonical_json(manifest), encoding="utf-8")

            transaction_id = state_figure_occurrences(repo, manifest_path)
            self.assertIsNotNone(transaction_id)
            after = json.loads(read_text(manifest_path))
            self.assertEqual(after["revision"], before + 1)
            self.assertEqual(after["last_transaction_id"], transaction_id)
            # 登记值被拉回规范 Markdown 的实际值，守卫随之转绿
            self.assertEqual(validate_figure_occurrences(after, repo), 60)
            # 除 expected_occurrences / revision / last_transaction_id 外一字未改
            for key in ("revision", "last_transaction_id"):
                manifest[key] = after[key]
            manifest["papers"][3]["figure_files"][0]["expected_occurrences"] = (
                after["papers"][3]["figure_files"][0]["expected_occurrences"]
            )
            self.assertEqual(manifest, after)

    def test_is_a_no_op_when_already_aligned(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, manifest_path = self._migrated_fixture(tmp)
            before = manifest_path.read_bytes()
            self.assertIsNone(state_figure_occurrences(repo, manifest_path))
            self.assertEqual(manifest_path.read_bytes(), before)


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
            # 六个批次只住在 manifest 里：index 投影自 T16 起不带任何运行态。
            self.assertNotIn("batches", index)
            self.assertEqual(len(index["papers"]), 21)
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
        """漂移用「未了结却降级成 non_blocking」构造。

        原先用 `open → deferred` 构造漂移，但那是**合法的生命周期推进**（守卫收窄后
        deferred 仍算未了结、仍要求 blocks_completion，所以照样通过）。`impact` 不进
        fingerprint 身份，改它不会先被 `load_issues` 的 fingerprint 校验拦掉，正好落在
        本守卫的判据上。
        """
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            issues_path = project / "missing-issues.md"
            issues_path.write_text(
                read_text(issues_path).replace(
                    '"impact": "blocks_completion"', '"impact": "non_blocking"'
                ),
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

    def test_transaction_target_paths_are_pinned_and_pairwise_distinct(self):
        pinned = [
            MANIFEST_TARGET,
            source_manifest_module.INDEX_TARGET,
            source_manifest_module.ISSUES_TARGET,
        ]
        self.assertEqual(pinned[1], "math-gaokao-latex/index.json")
        self.assertEqual(
            pinned[2], "math-gaokao-latex/missing-issues.md"
        )
        self.assertEqual(len(set(pinned)), 3)

    def test_command_requires_the_three_canonical_target_paths(self):
        cases = {
            "--output-manifest": (MANIFEST_TARGET, "copy-manifest.json"),
            "--output-index": (
                "math-gaokao-latex/index.json", "copy-index.json"
            ),
            "--issues": (
                "math-gaokao-latex/missing-issues.md", "copy-issues.md",
            ),
        }
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            before = {
                name: (project / name).read_bytes()
                for name in ("source-manifest.json", "index.json", "missing-issues.md")
            }
            for option, (expected, replacement) in cases.items():
                arguments = migrate_arguments(project)
                decoy = project / replacement
                decoy.write_bytes((project / "missing-issues.md").read_bytes())
                arguments[arguments.index(option) + 1] = str(decoy)
                with self.subTest(option=option):
                    with self.assertRaisesRegex(ValueError, re.escape(expected)):
                        main(arguments)
                    for name, value in before.items():
                        self.assertEqual((project / name).read_bytes(), value, name)
                    self.assertEqual(
                        decoy.read_bytes(),
                        (project / "missing-issues.md").read_bytes(),
                    )

    def test_command_rejects_colliding_transaction_targets(self):
        # 三个目标钉死后 CLI 已无法制造碰撞，这里压常量验证最后一道拦截：
        # 没有它时 targets 字典会因键重复静默丢掉一次写入，而 transaction.py
        # 的 manifest 唯一性检查永远看不到被字典去重掉的那一个。
        with tempfile.TemporaryDirectory() as tmp:
            repo, project = fixture_repository(tmp)
            before = {
                name: (project / name).read_bytes()
                for name in ("source-manifest.json", "index.json", "missing-issues.md")
            }
            arguments = migrate_arguments(project)
            arguments[arguments.index("--output-index") + 1] = str(
                project / "source-manifest.json"
            )
            with mock.patch.object(
                source_manifest_module, "INDEX_TARGET", MANIFEST_TARGET
            ):
                with self.assertRaisesRegex(ValueError, "两两不同"):
                    main(arguments)
            for name, value in before.items():
                self.assertEqual((project / name).read_bytes(), value, name)

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

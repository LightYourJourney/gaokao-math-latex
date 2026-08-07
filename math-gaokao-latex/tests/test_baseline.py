import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from baseline import (
    _tracked_build_inputs,
    collect_current_baseline,
    collect_legacy_baseline,
    compare_baselines,
    legacy_index_projection,
    main,
)
from manifest import file_sha256, load_manifest

FROZEN_LEGACY = ROOT / "reports" / "legacy-baseline.json"
MANIFEST = ROOT / "source-manifest.json"


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def quiet_main(argv):
    """跑 CLI 但不把它的正常输出混进测试报告。"""
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        return main(argv)


class LegacyBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = collect_legacy_baseline(ROOT)
        cls.index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))

    def test_records_index_hash_and_all_legacy_ids(self):
        expected_ids = [paper["id"] for paper in self.index["papers"]]
        self.assertEqual(self.baseline["index"]["path"], "index.json")
        self.assertEqual(
            self.baseline["index"]["sha256"], file_sha256(ROOT / "index.json")
        )
        self.assertEqual(self.baseline["index"]["paper_count"], 21)
        self.assertEqual(self.baseline["index"]["legacy_ids"], expected_ids)
        self.assertEqual(
            [paper["legacy_id"] for paper in self.baseline["papers"]], expected_ids
        )

    def test_records_84_shells_and_their_legacy_paper_ids(self):
        indexed = {paper["dir"]: paper["id"] for paper in self.index["papers"]}
        shells = [
            shell for paper in self.baseline["papers"] for shell in paper["shells"]
        ]
        self.assertEqual(len(shells), 84)
        self.assertEqual(
            {shell["edition"] for shell in shells},
            {"试题版", "解析版", "简答版", "印刷版"},
        )
        for paper in self.baseline["papers"]:
            self.assertEqual(len(paper["shells"]), 4)
            for shell in paper["shells"]:
                self.assertEqual(shell["paper_id"], indexed[paper["project_dir"]])
                self.assertEqual(len(shell["sha256"]), 64)

    def test_records_21_shared_content_hash_groups_and_figure_tree(self):
        expected_figures = sorted(
            path.relative_to(ROOT).as_posix()
            for path in ROOT.glob("[0-9]*/figures/*")
            if path.is_file()
        )
        recorded_figures = sorted(
            figure["path"]
            for paper in self.baseline["papers"]
            for figure in paper["figures"]
        )
        self.assertEqual(len(self.baseline["papers"]), 21)
        self.assertEqual(recorded_figures, expected_figures)
        for paper in self.baseline["papers"]:
            self.assertEqual(
                set(paper["content_sha256"]),
                {"questions.tex", "answers.tex", "answers_short.tex"},
            )
            self.assertTrue(
                all(len(value) == 64 for value in paper["content_sha256"].values())
            )
            self.assertEqual(
                [item["path"] for item in paper["figures"]],
                sorted(item["path"] for item in paper["figures"]),
            )

    def test_records_all_pdf_pages_and_log_warning_summary(self):
        targets = [
            target
            for paper in self.baseline["papers"]
            for target in paper["targets"]
        ]
        self.assertEqual(len(targets), 84)
        self.assertEqual(sum(target["pages"] for target in targets), 1336)
        self.assertEqual(
            sum(target["warnings"]["hard_errors"] for target in targets), 0
        )
        self.assertEqual(
            sum(target["warnings"]["missing_characters"] for target in targets), 0
        )
        self.assertEqual(
            sum(target["warnings"]["undefined_references"] for target in targets), 0
        )
        overfull = [
            (target["path"], warning)
            for target in targets
            for warning in target["warnings"]["overfull"]
        ]
        self.assertEqual(len(overfull), 1)
        self.assertEqual(overfull[0][0], "2025_全国2卷/印刷版.pdf")
        self.assertEqual(overfull[0][1]["width_pt"], "0.4588")
        self.assertEqual(self.baseline["summary"]["paper_count"], 21)
        self.assertEqual(self.baseline["summary"]["target_count"], 84)
        self.assertEqual(self.baseline["summary"]["total_pages"], 1336)

    def test_records_repository_and_tracked_build_input_identity(self):
        repo = Path(
            subprocess.check_output(
                ["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"],
                text=True,
            ).strip()
        )
        expected_head = subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip()
        self.assertEqual(self.baseline["repository"]["head"], expected_head)
        self.assertEqual(
            self.baseline["repository"]["compile_sha256"],
            file_sha256(ROOT / "compile.sh"),
        )
        plan = repo / self.baseline["repository"]["plan_path"]
        self.assertTrue(plan.is_file())
        self.assertEqual(
            self.baseline["repository"]["plan_sha256"], file_sha256(plan)
        )
        inputs = self.baseline["build_inputs"]
        self.assertEqual(
            [item["path"] for item in inputs["files"]],
            sorted(item["path"] for item in inputs["files"]),
        )
        self.assertTrue(inputs["files"])
        self.assertTrue(
            all(Path(item["path"]).suffix in {".tex", ".md", ".py", ".sh"}
                for item in inputs["files"])
        )
        self.assertEqual(len(inputs["tree_sha256"]), 64)

    def test_tracked_build_inputs_are_read_from_head_not_the_staging_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run([
                "git", "-C", str(repo), "config", "user.email", "t@example.invalid"
            ], check=True)
            subprocess.run([
                "git", "-C", str(repo), "config", "user.name", "Test"
            ], check=True)
            project = repo / "project"
            project.mkdir()
            tracked = project / "tracked.tex"
            staged_only = project / "staged.py"
            tracked.write_text("tracked", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run([
                "git", "-C", str(repo), "commit", "-qm", "tracked"
            ], check=True)
            staged_only.write_text("staged", encoding="utf-8")
            subprocess.run([
                "git", "-C", str(repo), "add", staged_only.relative_to(repo)
            ], check=True)
            inputs = _tracked_build_inputs(repo, project)
            self.assertEqual(
                [item["path"] for item in inputs["files"]],
                ["project/tracked.tex"],
            )
            tracked.write_text("modified", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "HEAD"):
                _tracked_build_inputs(repo, project)

    def test_write_and_check_cli_are_single_file_and_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "legacy.json"
            self.assertEqual(
                main([
                    "write-legacy",
                    "--project-root", str(ROOT),
                    "--output", str(output),
                ]),
                0,
            )
            before = output.read_bytes()
            self.assertEqual(main(["check-legacy", "--baseline", str(output)]), 0)
            self.assertEqual(output.read_bytes(), before)

            data = json.loads(before.decode("utf-8"))
            data["summary"]["target_count"] = 83
            output.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "84"):
                main(["check-legacy", "--baseline", str(output)])

            data = json.loads(before.decode("utf-8"))
            data["papers"][0]["shells"].pop()
            output.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "壳"):
                main(["check-legacy", "--baseline", str(output)])

            data = json.loads(before.decode("utf-8"))
            data["papers"][0]["content_sha256"]["questions.tex"] = "0" * 63
            output.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "共享内容"):
                main(["check-legacy", "--baseline", str(output)])

            data = json.loads(before.decode("utf-8"))
            data["papers"][0]["figures"][0]["sha256"] = "0" * 63
            output.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "figure tree"):
                main(["check-legacy", "--baseline", str(output)])

            data = json.loads(before.decode("utf-8"))
            data["build_inputs"]["tree_sha256"] = "0" * 64
            output.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "build input tree"):
                main(["check-legacy", "--baseline", str(output)])

            data = json.loads(before.decode("utf-8"))
            data["papers"][0]["targets"][0]["warnings"]["hard_errors"] = 1
            output.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "warning summary"):
                main(["check-legacy", "--baseline", str(output)])

    def test_cli_process_exit_codes_are_zero_one_and_two(self):
        script = ROOT / "tools" / "baseline.py"
        valid = ROOT / "reports" / "legacy-baseline.json"
        passed = subprocess.run(
            [sys.executable, str(script), "check-legacy", "--baseline", str(valid)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(passed.returncode, 0, passed.stderr)
        runtime_error = subprocess.run(
            [sys.executable, str(script), "check-legacy", "--baseline", str(valid) + ".missing"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(runtime_error.returncode, 1)
        usage_error = subprocess.run(
            [sys.executable, str(script), "check-legacy"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(usage_error.returncode, 2)


class PreMigrationIndexTests(unittest.TestCase):
    """迁移前的 index.json 由 legacy 基线的 head + SHA-256 钉死，从 git 取回逐字段核对。

    身份迁移整体重写了 index.json（键序与缩进都变了），字节比较已无意义；能证明"旧字段
    未变"的唯一锚点就是 legacy 基线里冻结的那个哈希，配 git 取回原始 blob。
    """

    @classmethod
    def setUpClass(cls):
        frozen = read_json(FROZEN_LEGACY)
        prefix = PurePosixPath(frozen["repository"]["compile_path"]).parent
        cls.frozen = frozen
        cls.blob = subprocess.check_output([
            "git", "-C", str(ROOT), "show",
            "{0}:{1}".format(
                frozen["repository"]["head"], prefix / frozen["index"]["path"]
            ),
        ])
        cls.pre = json.loads(cls.blob.decode("utf-8"))
        cls.current = read_json(ROOT / "index.json")

    def test_recovered_index_matches_the_hash_frozen_in_the_legacy_baseline(self):
        self.assertEqual(
            hashlib.sha256(self.blob).hexdigest(), self.frozen["index"]["sha256"]
        )

    def test_migration_added_only_paper_id_legacy_ids_and_batches(self):
        self.assertEqual(set(self.current) - set(self.pre), {"batches"})
        self.assertEqual(set(self.pre) - set(self.current), set())
        self.assertEqual(len(self.current["papers"]), len(self.pre["papers"]))
        for current, pre in zip(self.current["papers"], self.pre["papers"]):
            with self.subTest(legacy_id=pre["id"]):
                self.assertEqual(set(current) - set(pre), {"paper_id", "legacy_ids"})
                self.assertEqual(set(pre) - set(current), set())

    def test_every_pre_migration_index_field_value_is_unchanged(self):
        self.assertEqual(legacy_index_projection(self.current), self.pre)

    def test_any_change_to_a_compatible_field_is_detected(self):
        for mutate in (
            lambda index: index["papers"][0].update(questions=99),
            lambda index: index["papers"][0]["structure"].pop("选择题"),
            lambda index: index["papers"][0].pop("note"),
            lambda index: index.update(source_pdf="../other/main.pdf"),
            lambda index: index["papers"][0].update(smuggled=True),
        ):
            with self.subTest(mutate=mutate):
                mutated = copy.deepcopy(self.current)
                mutate(mutated)
                self.assertNotEqual(legacy_index_projection(mutated), self.pre)


class CurrentBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest(MANIFEST)
        cls.current = collect_current_baseline(ROOT, cls.manifest)

    def test_records_the_same_shape_as_the_legacy_baseline_plus_paper_id(self):
        expected = {paper["id"] for paper in read_json(ROOT / "index.json")["papers"]}
        self.assertEqual(self.current["kind"], "current")
        self.assertEqual(len(self.current["papers"]), 21)
        self.assertEqual(
            {paper["legacy_id"] for paper in self.current["papers"]}, expected
        )
        by_legacy = {
            legacy_id: paper["paper_id"]
            for paper in self.manifest["papers"]
            for legacy_id in paper["legacy_ids"]
        }
        for paper in self.current["papers"]:
            with self.subTest(legacy_id=paper["legacy_id"]):
                self.assertEqual(paper["paper_id"], by_legacy[paper["legacy_id"]])
                self.assertEqual(len(paper["shells"]), 4)
                self.assertEqual(len(paper["targets"]), 4)

    def test_summary_still_reports_84_targets_1336_pages_and_one_overfull(self):
        self.assertEqual(self.current["summary"]["paper_count"], 21)
        self.assertEqual(self.current["summary"]["target_count"], 84)
        self.assertEqual(self.current["summary"]["total_pages"], 1336)
        self.assertEqual(self.current["summary"]["overfull_count"], 1)
        self.assertEqual(self.current["summary"]["hard_errors"], 0)

    def test_rejects_an_index_that_is_not_the_manifest_identity_projection(self):
        manifest = copy.deepcopy(dict(self.manifest))
        manifest["papers"][0]["paper_id"] = "gk-0000-not-migrated"
        with self.assertRaisesRegex(ValueError, "投影"):
            collect_current_baseline(ROOT, manifest)

    def test_sources_only_collection_skips_pdf_and_log(self):
        sources = collect_current_baseline(ROOT, self.manifest, include_targets=False)
        self.assertEqual(sources["summary"]["target_count"], None)
        self.assertEqual(sources["summary"]["total_pages"], None)
        for paper in sources["papers"]:
            with self.subTest(legacy_id=paper["legacy_id"]):
                self.assertNotIn("targets", paper)
                self.assertEqual(len(paper["shells"]), 4)


class BaselineComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.legacy = read_json(FROZEN_LEGACY)
        cls.manifest = load_manifest(MANIFEST)
        cls.current = collect_current_baseline(ROOT, cls.manifest)

    def drift(self, mutate=None, **options):
        current = copy.deepcopy(self.current)
        if mutate is not None:
            mutate(current)
        return compare_baselines(self.legacy, current, **options)["drift"]

    def test_identity_migration_produces_no_unreviewed_drift(self):
        report = compare_baselines(self.legacy, self.current)
        self.assertEqual(report["drift"], [])
        self.assertEqual(report["summary"]["target_count"], 84)
        self.assertEqual(report["summary"]["total_pages"], 1336)
        self.assertEqual(report["summary"]["overfull_count"], 1)

    def test_non_reproducible_fields_are_reviewed_instead_of_drift(self):
        reviewed = {item["field"] for item in compare_baselines(
            self.legacy, self.current
        )["reviewed"]}
        self.assertEqual(
            reviewed,
            {
                "repository.head",
                "build_inputs",
                "index.sha256",
                "papers[].targets[].pdf_sha256",
                "papers[].targets[].log_sha256",
                "papers[].targets[].warnings[].log_line",
            },
        )
        # 这三项在迁移后确实不同，但不得计为漂移。
        self.assertNotEqual(
            self.current["repository"]["head"], self.legacy["repository"]["head"]
        )
        self.assertNotEqual(
            self.current["index"]["sha256"], self.legacy["index"]["sha256"]
        )
        self.assertEqual(self.drift(), [])

    def test_changed_legacy_id_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["index"].update(
                legacy_ids=["x"] + current["index"]["legacy_ids"][1:]
            )
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][0].update(legacy_id="x")
        ))

    def test_changed_index_compatible_projection_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["index"].update(paper_count=20)
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][3].update(project_dir="别的目录")
        ))

    def test_changed_or_missing_shell_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["papers"][0]["shells"][2].update(sha256="0" * 64)
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][0]["shells"][1].update(paper_id="2017x")
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][5]["shells"].pop()
        ))

    def test_changed_shared_content_hash_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["papers"][7]["content_sha256"].update(
                **{"answers.tex": "0" * 64}
            )
        ))

    def test_changed_question_sequence_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["papers"][2]["question_ids"].pop()
        ))

    def test_changed_figure_tree_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["papers"][0]["figures"][0].update(sha256="0" * 64)
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][0]["figures"].append(
                {"path": "2017_全国Ⅰ卷_理科/figures/新增.tex", "sha256": "0" * 64}
            )
        ))

    def overfull_position(self):
        for paper, record in enumerate(self.current["papers"]):
            for target, item in enumerate(record["targets"]):
                if item["warnings"]["overfull"]:
                    return paper, target
        raise AssertionError("迁移后基线里没有 Overfull，无法验证该维度")

    def test_changed_pages_or_overfull_is_drift(self):
        paper, target = self.overfull_position()
        self.assertEqual(
            self.current["papers"][paper]["targets"][target]["path"],
            "2025_全国2卷/印刷版.pdf",
        )
        self.assertTrue(self.drift(
            lambda current: current["papers"][0]["targets"][0].update(pages=99)
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][paper]["targets"][target]["warnings"][
                "overfull"
            ].clear()
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][paper]["targets"][target]["warnings"][
                "overfull"
            ][0].update(width_pt="9.9999")
        ))

    def test_sources_only_skips_pdf_and_log_but_keeps_the_six_source_dimensions(self):
        self.assertEqual(
            self.drift(
                lambda current: current["papers"][0]["targets"][0].update(pages=99),
                sources_only=True,
            ),
            [],
        )
        for mutate in (
            lambda current: current["index"].update(legacy_ids=["x"] * 21),
            lambda current: current["papers"][0].update(project_dir="别的目录"),
            lambda current: current["papers"][0]["shells"][0].update(sha256="0" * 64),
            lambda current: current["papers"][0]["content_sha256"].update(
                **{"questions.tex": "0" * 64}
            ),
            lambda current: current["papers"][0]["question_ids"].pop(),
            lambda current: current["papers"][0]["figures"][0].update(sha256="0" * 64),
        ):
            with self.subTest(mutate=mutate):
                self.assertTrue(self.drift(mutate, sources_only=True))

    def test_a_baseline_without_targets_cannot_be_compared_in_full_mode(self):
        sources = collect_current_baseline(ROOT, self.manifest, include_targets=False)
        self.assertEqual(compare_baselines(self.legacy, sources, sources_only=True)["drift"], [])
        with self.assertRaisesRegex(ValueError, "sources-only"):
            compare_baselines(self.legacy, sources)


class CurrentBaselineCliTests(unittest.TestCase):
    def test_write_current_writes_one_file_and_compare_touches_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "current.json"
            legacy_before = FROZEN_LEGACY.read_bytes()
            index_before = (ROOT / "index.json").read_bytes()
            self.assertEqual(
                quiet_main([
                    "write-current",
                    "--manifest", str(MANIFEST),
                    "--output", str(output),
                ]),
                0,
            )
            self.assertEqual([item.name for item in Path(tmp).iterdir()], ["current.json"])
            before = output.read_bytes()
            self.assertEqual(
                quiet_main([
                    "compare",
                    "--legacy", str(FROZEN_LEGACY),
                    "--current", str(output),
                ]),
                0,
            )
            self.assertEqual(output.read_bytes(), before)
            self.assertEqual(FROZEN_LEGACY.read_bytes(), legacy_before)
            self.assertEqual((ROOT / "index.json").read_bytes(), index_before)

    def test_compare_honours_project_root_and_exits_one_on_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "current.json"
            self.assertEqual(
                quiet_main([
                    "write-current",
                    "--manifest", str(MANIFEST),
                    "--output", str(output),
                    "--project-root", str(ROOT),
                ]),
                0,
            )
            drifted = read_json(output)
            drifted["papers"][0]["content_sha256"]["questions.tex"] = "0" * 64
            output.write_text(json.dumps(drifted), encoding="utf-8")
            self.assertEqual(
                quiet_main([
                    "compare",
                    "--legacy", str(FROZEN_LEGACY),
                    "--current", str(output),
                ]),
                1,
            )

    def test_compare_working_collects_the_live_worktree(self):
        for extra in ([], ["--sources-only"]):
            with self.subTest(extra=extra):
                self.assertEqual(
                    quiet_main([
                        "compare-working",
                        "--legacy", str(FROZEN_LEGACY),
                        "--project-root", str(ROOT),
                        "--manifest", str(MANIFEST),
                    ] + extra),
                    0,
                )

    def test_parsers_require_every_path_and_scope_sources_only(self):
        for argv in (
            ["write-current", "--manifest", "m"],
            ["write-current", "--output", "o"],
            ["compare", "--legacy", "l"],
            ["compare", "--current", "c"],
            ["compare-working", "--legacy", "l", "--project-root", "p"],
            ["compare-working", "--legacy", "l", "--manifest", "m"],
            ["compare-working", "--project-root", "p", "--manifest", "m"],
            ["write-current", "--manifest", "m", "--output", "o", "--sources-only"],
            ["check-legacy", "--baseline", "b", "--sources-only"],
        ):
            with self.subTest(argv=argv):
                with redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit) as raised:
                        main(argv)
                self.assertEqual(raised.exception.code, 2)

    def test_compare_process_exit_codes_are_zero_one_and_two(self):
        script = ROOT / "tools" / "baseline.py"
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "current.json"
            self.assertEqual(
                quiet_main([
                    "write-current",
                    "--manifest", str(MANIFEST),
                    "--output", str(output),
                ]),
                0,
            )
            passed = subprocess.run(
                [
                    sys.executable, str(script), "compare",
                    "--legacy", str(FROZEN_LEGACY), "--current", str(output),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            self.assertEqual(passed.returncode, 0, passed.stderr)
            drifted = read_json(output)
            drifted["papers"][0]["question_ids"].pop()
            output.write_text(json.dumps(drifted), encoding="utf-8")
            drift = subprocess.run(
                [
                    sys.executable, str(script), "compare",
                    "--legacy", str(FROZEN_LEGACY), "--current", str(output),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            self.assertEqual(drift.returncode, 1)
            self.assertIn("question_ids", drift.stderr)
            usage = subprocess.run(
                [sys.executable, str(script), "compare", "--legacy", str(FROZEN_LEGACY)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            self.assertEqual(usage.returncode, 2)


if __name__ == "__main__":
    unittest.main()

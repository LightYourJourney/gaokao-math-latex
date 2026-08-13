import copy
import difflib
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
    _ABSENT,
    _LEVEL_PATHS,
    _REVIEWED_FIELDS,
    _REWRITTEN_FIELDS,
    ADJUDICATED_DRIFTS_PATH,
    DRIFT_CLASSES,
    LEDGER_VERSION,
    _comparable,
    _tracked_build_inputs,
    collect_current_baseline,
    collect_legacy_baseline,
    compare_baselines,
    legacy_index_projection,
    load_adjudicated_drifts,
    main,
    recover_legacy_index,
    with_legacy_compat,
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

    def test_migration_added_only_paper_id_and_legacy_ids(self):
        # T16 起 index 投影不再携带 `batches`（运行态只住在 manifest 里），于是顶层键集
        # 与迁移前完全一致；逐条新增只剩 paper 级的静态身份两键。
        self.assertEqual(set(self.current) - set(self.pre), set())
        self.assertEqual(set(self.pre) - set(self.current), set())
        self.assertEqual(len(self.current["papers"]), len(self.pre["papers"]))
        for current, pre in zip(self.current["papers"], self.pre["papers"]):
            with self.subTest(legacy_id=pre["id"]):
                self.assertEqual(set(current) - set(pre), {"paper_id", "legacy_ids"})
                self.assertEqual(set(pre) - set(current), set())

    def test_every_pre_migration_index_field_value_is_unchanged(self):
        projected = legacy_index_projection(self.current)
        # `generated_by` 是登记在案的正当改写（baseline._REWRITTEN_FIELDS）：写实现自
        # T13 起就在 generate_projects.py，T16 剔除运行态投影时一并落实。除它之外，
        # 迁移前的每一个字段值仍必须逐字未变。
        self.assertEqual(projected.pop("generated_by"), "tools/generate_projects.py")
        self.assertEqual(self.pre["generated_by"], "tools/split_project.py")
        self.assertEqual(
            projected,
            {key: value for key, value in self.pre.items() if key != "generated_by"},
        )

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
        cls.legacy_index = recover_legacy_index(cls.legacy, ROOT)
        cls.adjudicated = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)

    def drift(self, mutate=None, **options):
        current = copy.deepcopy(self.current)
        if mutate is not None:
            mutate(current)
        options.setdefault("legacy_index", self.legacy_index)
        options.setdefault("adjudicated", self.adjudicated)
        return compare_baselines(self.legacy, current, **options)["drift"]

    def report(self, **options):
        options.setdefault("legacy_index", self.legacy_index)
        options.setdefault("adjudicated", self.adjudicated)
        return compare_baselines(self.legacy, self.current, **options)

    def test_identity_migration_leaves_no_unadjudicated_drift(self):
        """口径是「零**未裁定**漂移」：共享 TeX 的 63 条已由登记表逐条放行。

        T13 把 questions/answers 改成来源总账驱动（42 条），T14 又把 answers_short
        改成自 answers.tex 提取（21 条）；计划从未承诺共享 TeX 字节不变。这里守的是
        「除已裁定的那 63 条之外，一个字节都没动」——84 个版本壳就在这条守卫之内，
        T13/T14 的 63 个唯一键仍保持不增不减；T25 只更新其中 b01 的 8 个既有键，
        把裁定来源和类别改为窄定义的视觉排版修复，并钉住新的 current hash。
        """
        report = self.report()
        self.assertEqual(report["drift"], [])
        self.assertEqual(len(report["adjudicated"]), 63)
        self.assertEqual(report["summary"]["target_count"], 84)
        self.assertEqual(report["summary"]["total_pages"], 1336)
        self.assertEqual(report["summary"]["overfull_count"], 1)

    def test_every_adjudicated_entry_is_a_shared_tex_content_hash(self):
        adjudicated = self.report()["adjudicated"]
        self.assertEqual(
            {item["artifact"] for item in adjudicated},
            {"questions.tex", "answers.tex", "answers_short.tex"},
        )
        counts = {}
        for item in adjudicated:
            counts[item["class"]] = counts.get(item["class"], 0) + 1
        # class 是逐条可审计的字段，不是散文注释的复述：T14 的 21 卷里只有 15 卷动了
        # 答案值，另 6 卷逐 hunk 核对只有生成头注一处变化，按本表自己的 class 定义
        # 就该记 header——否则后人按 class 筛选拿不到 15/6 的区分。
        self.assertEqual(counts, {
            "migration": 2, "header": 7, "stale-artifact": 1,
            "short-answers-regeneration": 14, "short-answer-safety-repair": 1,
            "visual-layout-repair": 8, "layout-regeneration": 30,
        })
        by_task = {
            "task-13-review", "task-14-review", "task-25-visual-review",
            "task-26-regeneration", "task-27-regeneration",
            "task-28-regeneration", "task-28-answer-leak-repair",
            "task-29-regeneration",
        }
        for item in adjudicated:
            self.assertRegex(item["field"], r"^papers\[\d+\]\.content_sha256\.")
            self.assertIn(item["adjudicated_by"], by_task)
        # 每一条都必须指名裁定它的那一轮：T14 只挂 answers_short，T25 恰为
        # phase0-b01 四卷的 questions/answers 八个既有唯一键。
        self.assertEqual(
            {item["artifact"] for item in adjudicated
             if item["adjudicated_by"] == "task-14-review"},
            {"answers_short.tex"},
        )
        self.assertEqual(
            len([item for item in adjudicated
                 if item["adjudicated_by"] == "task-25-visual-review"]),
            8,
        )
        self.assertEqual(
            len([item for item in adjudicated
                 if item["adjudicated_by"] == "task-26-regeneration"]),
            8,
        )
        self.assertEqual(
            len([item for item in adjudicated
                 if item["adjudicated_by"] == "task-27-regeneration"]),
            6,
        )
        self.assertEqual(
            len([item for item in adjudicated
                 if item["adjudicated_by"] == "task-28-regeneration"]),
            8,
        )
        self.assertEqual(
            len([item for item in adjudicated
                 if item["adjudicated_by"] == "task-29-regeneration"]),
            8,
        )

    def test_without_the_ledger_every_content_drift_is_reported(self):
        """缺登记表 = 现状：63 条全部未裁定。登记表绝不能是「默认放行」。"""
        report = compare_baselines(
            self.legacy, self.current, legacy_index=self.legacy_index
        )
        self.assertEqual(len(report["drift"]), 63)
        self.assertEqual(report["adjudicated"], [])

    def test_a_further_change_to_current_is_reported_again(self):
        """裁定钉的是**那一个**字节结果；再动一次必须重新报警。"""
        drift = self.drift(
            lambda current: current["papers"][0]["content_sha256"].update(
                {"answers.tex": "0" * 64}
            )
        )
        self.assertEqual(len(drift), 1)
        self.assertEqual(drift[0]["field"], "papers[0].content_sha256.answers.tex")
        self.assertEqual(drift[0]["current"], "0" * 64)

    def test_a_legacy_side_mismatch_is_reported(self):
        legacy = copy.deepcopy(self.legacy)
        legacy["papers"][0]["content_sha256"]["answers.tex"] = "1" * 64
        drift = compare_baselines(
            legacy, self.current,
            legacy_index=self.legacy_index, adjudicated=self.adjudicated,
        )["drift"]
        self.assertEqual(len(drift), 1)
        self.assertEqual(drift[0]["legacy"], "1" * 64)

    def test_an_unregistered_artifact_is_never_adjudicated(self):
        partial = {
            key: value for key, value in self.adjudicated.items()
            if key[1] != "questions.tex"
        }
        drift = self.drift(adjudicated=partial)
        self.assertEqual(len(drift), 21)
        for item in drift:
            self.assertTrue(item["field"].endswith(".questions.tex"), item["field"])

    def test_only_content_hashes_can_be_adjudicated(self):
        """登记表是窄入口：非 content_sha256 的漂移永远进不来。"""
        drift = self.drift(
            lambda current: current["papers"][0]["figures"].append("凭空多出.tex")
        )
        self.assertEqual([item["field"] for item in drift], ["papers[0].figures[5]"])

    # ---- 正当改写表：豁免的是「路径 + 取值对」，不是路径

    def test_the_rewritten_table_registers_both_sides_of_every_pair(self):
        """表项必须是四元组：只登记路径就等于给那条路径开永久免检。"""
        self.assertTrue(_REWRITTEN_FIELDS)
        for entry in _REWRITTEN_FIELDS:
            self.assertEqual(len(entry), 4)
            field, legacy_value, current_value, reason = entry
            self.assertTrue(field and reason)
            self.assertNotEqual(legacy_value, current_value)

    def test_the_registered_pair_matches_the_live_baselines(self):
        """登记的两个取值必须就是实测的那一对，否则这条豁免根本不该命中。"""
        registered = {
            field: (legacy_value, current_value)
            for field, legacy_value, current_value, _ in _REWRITTEN_FIELDS
        }
        self.assertEqual(
            registered["index.legacy_compat.generated_by"],
            ("tools/split_project.py", "tools/generate_projects.py"),
        )
        self.assertEqual(self.report()["drift"], [])

    def test_a_third_value_on_the_current_side_is_drift_again(self):
        drift = self.drift(
            lambda current: current["index"]["legacy_compat"].update(
                generated_by="tools/别的东西.py"
            )
        )
        self.assertEqual(
            [item["field"] for item in drift],
            ["index.legacy_compat.generated_by"],
        )
        self.assertEqual(drift[0]["current"], "tools/别的东西.py")

    def test_deleting_a_rewritten_key_is_drift_not_a_free_pass(self):
        """整键删除经 `left.get(key, _ABSENT)` 汇入同一条标量比较——必须照样报警。"""
        drift = self.drift(
            lambda current: current["index"]["legacy_compat"].pop("generated_by")
        )
        self.assertEqual(
            [item["field"] for item in drift],
            ["index.legacy_compat.generated_by"],
        )
        self.assertEqual(drift[0]["current"], repr(_ABSENT))

    def test_a_legacy_side_change_to_a_rewritten_field_is_drift(self):
        """legacy 侧对不上说明冻结锚点被换过；与双哈希口径一致地重新报警。"""
        tampered = copy.deepcopy(self.legacy_index)
        tampered["generated_by"] = "tools/换过的旧值.py"
        drift = compare_baselines(
            self.legacy, self.current,
            legacy_index=tampered, adjudicated=self.adjudicated,
        )["drift"]
        self.assertEqual(
            [item["field"] for item in drift],
            ["index.legacy_compat.generated_by"],
        )
        self.assertEqual(drift[0]["legacy"], "tools/换过的旧值.py")

    def test_non_reproducible_fields_are_reviewed_instead_of_drift(self):
        reviewed = {item["field"] for item in self.report()["reviewed"]}
        self.assertEqual(
            reviewed,
            {
                "kind",
                "build_inputs",
                "repository.head",
                "repository.compile_sha256",
                "index.sha256",
                # 路径精确的正当改写：粒度是 legacy_compat 深处的一个叶子，
                # 整个 legacy_compat 仍逐字段受保护。
                "index.legacy_compat.generated_by",
                "papers[].paper_id",
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
        self.assertNotEqual(self.current["kind"], self.legacy["kind"])
        self.assertEqual(self.drift(), [])

    def test_compare_fails_closed_without_the_pre_migration_index(self):
        # 冻结的 legacy 基线没有记录兼容投影；拿不到 git 锚点就必须报错，不得静默跳过。
        self.assertNotIn("legacy_compat", self.legacy["index"])
        with self.assertRaisesRegex(ValueError, "兼容投影"):
            compare_baselines(self.legacy, self.current)
        with self.assertRaisesRegex(ValueError, "兼容投影"):
            compare_baselines(self.legacy, self.current, True)

    def test_current_baseline_without_the_compat_projection_is_drift(self):
        self.assertTrue(self.drift(
            lambda current: current["index"].pop("legacy_compat")
        ))

    def test_index_deep_field_drift_is_caught_in_both_modes(self):
        for mutate in (
            lambda current: current["index"]["legacy_compat"]["papers"][0][
                "structure"
            ].update(选择题=[1, 99]),
            lambda current: current["index"]["legacy_compat"]["papers"][0].update(
                pdf_pages=None
            ),
            lambda current: current["index"]["legacy_compat"]["papers"][3].update(
                title="改过的标题"
            ),
            lambda current: current["index"]["legacy_compat"]["papers"][5].update(
                year=1999, track="改过", variant="改过", base="改过"
            ),
            lambda current: current["index"]["legacy_compat"]["papers"][2].pop("note"),
            lambda current: current["index"]["legacy_compat"].update(
                source_pdf="../别处/main.pdf"
            ),
            lambda current: current["index"]["legacy_compat"]["papers"][0][
                "figures"
            ].append("夹带.tex"),
        ):
            for sources_only in (False, True):
                with self.subTest(mutate=mutate, sources_only=sources_only):
                    self.assertTrue(self.drift(mutate, sources_only=sources_only))

    def test_a_migrated_index_smuggled_back_into_the_projection_is_drift(self):
        # 兼容投影里混进迁移新增的三个键，同样必须报漂移。
        self.assertTrue(self.drift(
            lambda current: current["index"]["legacy_compat"].update(batches=[])
        ))
        self.assertTrue(self.drift(
            lambda current: current["index"]["legacy_compat"]["papers"][0].update(
                paper_id="gk-2017-regular-national-1-science"
            )
        ))

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

    def test_every_remaining_compared_field_has_a_mutation_that_drifts(self):
        """审查指出的无变异覆盖的字段：每个都必须能被检出。"""
        for mutate in (
            lambda current: current["repository"].update(plan_sha256="0" * 64),
            # compile_sha256 自 Task 15 起是 reviewed 字段（compile.sh 由本任务改写），
            # 故不再列在这里；compile_path 仍守着「不得改名搬家」。
            lambda current: current["repository"].update(plan_path="别的/计划.md"),
            lambda current: current["repository"].update(compile_path="别的/compile.sh"),
            lambda current: current["index"].update(path="别的index.json"),
            lambda current: current.update(baseline_version=2),
            lambda current: current["summary"].update(paper_count=20),
            lambda current: current["papers"][0]["targets"][0].update(edition="改过"),
            lambda current: current["papers"][0]["targets"][0].update(
                log_path="别的.log"
            ),
            lambda current: current["papers"][0]["targets"][0].update(path="别的.pdf"),
            lambda current: current["papers"][0]["targets"][0]["warnings"].update(
                hard_errors=1
            ),
            lambda current: current["papers"][0]["targets"][0]["warnings"].update(
                missing_characters=1
            ),
            lambda current: current["papers"][0]["targets"][0]["warnings"].update(
                undefined_references=1
            ),
            lambda current: current["papers"][0]["targets"][0]["warnings"][
                "latex_warnings"
            ].append({"log_line": 1, "message": "LaTeX Warning: 夹带"}),
            lambda current: current["papers"][1]["targets"][1]["warnings"][
                "underfull"
            ].clear(),
            lambda current: current["summary"].update(total_pages=1335),
            lambda current: current["summary"].update(overfull_count=0),
        ):
            with self.subTest(mutate=mutate):
                self.assertTrue(self.drift(mutate))

    def test_underfull_details_are_compared_but_log_line_is_not(self):
        underfull = None
        for paper, record in enumerate(self.current["papers"]):
            for target, item in enumerate(record["targets"]):
                if item["warnings"]["underfull"]:
                    underfull = (paper, target)
                    break
            if underfull:
                break
        self.assertIsNotNone(underfull, "迁移后基线里没有 Underfull，无法验证该维度")
        paper, target = underfull
        self.assertTrue(self.drift(
            lambda current: current["papers"][paper]["targets"][target]["warnings"][
                "underfull"
            ][0].update(badness=1)
        ))
        self.assertTrue(self.drift(
            lambda current: current["papers"][paper]["targets"][target]["warnings"][
                "underfull"
            ][0].update(context="in paragraph at lines 1--2")
        ))
        # log_line 是日志内位置，属 reviewed，不计漂移。
        self.assertEqual(self.drift(
            lambda current: current["papers"][paper]["targets"][target]["warnings"][
                "underfull"
            ][0].update(log_line=999999)
        ), [])

    def test_a_baseline_without_targets_cannot_be_compared_in_full_mode(self):
        sources = collect_current_baseline(ROOT, self.manifest, include_targets=False)
        self.assertEqual(
            compare_baselines(
                self.legacy, sources, True,
                legacy_index=self.legacy_index, adjudicated=self.adjudicated,
            )["drift"],
            [],
        )
        with self.assertRaisesRegex(ValueError, "sources-only"):
            compare_baselines(self.legacy, sources, legacy_index=self.legacy_index)


class AdjudicatedDriftLedgerTests(unittest.TestCase):
    """登记表的读入契约：缺文件退化成现状，读不懂一律报错。"""

    def write(self, document):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "adjudicated-drifts.json"
        path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
        return path

    def valid_record(self, **overrides):
        record = {
            "adjudicated_by": "task-13-review",
            "artifact": "answers.tex",
            "class": "migration",
            "current_sha256": "b" * 64,
            "legacy_sha256": "a" * 64,
            "paper_id": "gk-2099-regular-national-1",
        }
        record.update(overrides)
        return record

    def test_a_missing_ledger_means_nothing_is_adjudicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_adjudicated_drifts(Path(tmp) / "缺席.json"), {})

    def test_a_valid_ledger_is_keyed_by_paper_and_artifact(self):
        path = self.write({
            "ledger_version": LEDGER_VERSION, "drifts": [self.valid_record()]
        })
        ledger = load_adjudicated_drifts(path)
        self.assertEqual(
            list(ledger), [("gk-2099-regular-national-1", "answers.tex")]
        )

    def test_visual_layout_repair_has_one_narrow_adjudication_source(self):
        record = self.valid_record(**{
            "adjudicated_by": "task-25-visual-review",
            "class": "visual-layout-repair",
        })
        ledger = load_adjudicated_drifts(self.write({
            "ledger_version": LEDGER_VERSION, "drifts": [record]
        }))
        self.assertEqual(
            ledger[("gk-2099-regular-national-1", "answers.tex")], record
        )

        record["adjudicated_by"] = "随便一个来源"
        with self.assertRaises(ValueError):
            load_adjudicated_drifts(self.write({
                "ledger_version": LEDGER_VERSION, "drifts": [record]
            }))

    def test_layout_regeneration_has_batch_scoped_adjudication_sources(self):
        for source in (
            "task-26-regeneration", "task-27-regeneration", "task-28-regeneration",
            "task-29-regeneration",
        ):
            with self.subTest(source=source):
                record = self.valid_record(**{
                    "adjudicated_by": source,
                    "class": "layout-regeneration",
                })
                ledger = load_adjudicated_drifts(self.write({
                    "ledger_version": LEDGER_VERSION, "drifts": [record]
                }))
                self.assertEqual(
                    ledger[("gk-2099-regular-national-1", "answers.tex")], record
                )

        record = self.valid_record(**{
            "adjudicated_by": "task-28-regeneration",
            "class": "layout-regeneration",
        })
        for field, value in (
            ("adjudicated_by", "随便一个来源"),
            ("class", "随便一个类别"),
        ):
            invalid = dict(record)
            invalid[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                load_adjudicated_drifts(self.write({
                    "ledger_version": LEDGER_VERSION, "drifts": [invalid]
                }))

    def test_a_malformed_ledger_fails_closed(self):
        cases = {
            "版本": {"ledger_version": 99, "drifts": []},
            "drifts": {"ledger_version": LEDGER_VERSION, "drifts": {}},
            "条目类型": {"ledger_version": LEDGER_VERSION, "drifts": ["x"]},
            "缺字段": {
                "ledger_version": LEDGER_VERSION,
                "drifts": [{"paper_id": "p", "artifact": "answers.tex"}],
            },
            "类别": {
                "ledger_version": LEDGER_VERSION,
                "drifts": [self.valid_record(**{"class": "随便放行"})],
            },
            "产物": {
                "ledger_version": LEDGER_VERSION,
                "drifts": [self.valid_record(artifact="main.pdf")],
            },
            "哈希": {
                "ledger_version": LEDGER_VERSION,
                "drifts": [self.valid_record(current_sha256="不是哈希")],
            },
            "重复": {
                "ledger_version": LEDGER_VERSION,
                "drifts": [self.valid_record(), self.valid_record()],
            },
        }
        for name, document in cases.items():
            with self.subTest(case=name):
                with self.assertRaises(ValueError):
                    load_adjudicated_drifts(self.write(document))

    def test_task28_answer_leak_repair_updates_exactly_one_existing_key(self):
        key = ("gk-2023-regular-new-gaokao-1", "answers_short.tex")
        relative = (
            "math-gaokao-latex/2023_新高考Ⅰ卷/answers_short.tex"
        )
        repo = ROOT.parent.parent.parent
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        record = ledger[key]
        before = subprocess.check_output([
            "git", "-C", str(repo), "show", "a8bdf08^:" + relative,
        ]).decode("utf-8")
        after = (repo / relative).read_text(encoding="utf-8")

        self.assertEqual(record["adjudicated_by"], "task-28-answer-leak-repair")
        self.assertEqual(record["class"], "short-answer-safety-repair")
        self.assertEqual(
            record["legacy_sha256"],
            "b250d729f0d72814ba1bf340572c34465dba4815d58a58fc84ed8709ead33fcd",
        )
        self.assertEqual(record["current_sha256"], file_sha256(repo / relative))
        leaked = r"  \item[\textbf{19.}] (1) $f'(x)=a\mathrm e^x-1$。$a\le0$：$a\mathrm e^x\le0$，故 $f'(x)<0$，$f$ 在 $\mathbf R$ 上单调递减；$a>0$：由 $f'(x)=0$ 得 $x=-\ln a$，$f$ 在 $(-\infty,-\ln a)$ 递减、在 $(-\ln a,+\infty)$ 递增；(2) 见解析版"
        safe = r"  \item[\textbf{19.}] (1) 见解析版；(2) 见解析版"
        self.assertEqual(before.count(leaked), 1)
        self.assertNotIn(safe, before)
        self.assertEqual(after, before.replace(leaked, safe))
        selected = {
            ledger_key for ledger_key, item in ledger.items()
            if item["adjudicated_by"] == "task-28-answer-leak-repair"
        }
        self.assertEqual(selected, {key})

        for field, value in (
            ("adjudicated_by", "未知来源"),
            ("class", "未知类别"),
        ):
            invalid = dict(record)
            invalid[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                load_adjudicated_drifts(self.write({
                    "ledger_version": LEDGER_VERSION, "drifts": [invalid]
                }))

        for field, value in (
            ("paper_id", "gk-2023-regular-new-gaokao-2"),
            ("artifact", "answers.tex"),
            ("adjudicated_by", "task-28-regeneration"),
            ("class", "layout-regeneration"),
        ):
            invalid = dict(record)
            invalid[field] = value
            with self.subTest(scope=field), self.assertRaises(ValueError):
                load_adjudicated_drifts(self.write({
                    "ledger_version": LEDGER_VERSION, "drifts": [invalid]
                }))

    def test_task29_updates_exactly_eight_existing_b05_keys_with_layout_only_diffs(self):
        projects = {
            "gk-2024-regular-new-gaokao-1": "2024_新高考Ⅰ卷",
            "gk-2024-regular-new-gaokao-2": "2024_新高考Ⅱ卷",
            "gk-2025-regular-national-1": "2025_全国1卷",
            "gk-2025-regular-national-2": "2025_全国2卷",
        }
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        ledger_relative = ADJUDICATED_DRIFTS_PATH.relative_to(
            ROOT.parent.parent.parent
        ).as_posix()
        previous_document = json.loads(subprocess.check_output([
            "git", "-C", str(ROOT.parent.parent.parent), "show",
            "36ca6b2:" + ledger_relative,
        ]).decode("utf-8"))
        previous = {
            (record["paper_id"], record["artifact"]): record
            for record in previous_document["drifts"]
        }
        self.assertEqual(len(ledger), len(previous))
        selected = {
            key: record for key, record in ledger.items()
            if record["adjudicated_by"] == "task-29-regeneration"
        }
        expected_keys = {
            (paper_id, artifact)
            for paper_id in projects
            for artifact in ("questions.tex", "answers.tex")
        }
        self.assertEqual(set(selected), expected_keys)

        for (paper_id, artifact), record in selected.items():
            relative = "math-gaokao-latex/{}/{}".format(
                projects[paper_id], artifact
            )
            current = ROOT.parent.parent.parent / relative
            head = subprocess.check_output([
                "git", "-C", str(ROOT.parent.parent.parent), "show",
                "36ca6b2:" + relative,
            ]).decode("utf-8")
            now = current.read_text(encoding="utf-8")
            self.assertEqual(record["class"], "layout-regeneration")
            self.assertEqual(
                record["legacy_sha256"],
                previous[(paper_id, artifact)]["legacy_sha256"],
            )
            self.assertEqual(record["current_sha256"], file_sha256(current))

            removed = []
            added = []
            for line in difflib.ndiff(head.splitlines(), now.splitlines()):
                if line.startswith("- "):
                    removed.append(line[2:])
                elif line.startswith("+ "):
                    added.append(line[2:])
            self.assertTrue(added)
            self.assertTrue(all(line in {
                r"\nopagebreak[4]", r"\Needspace{0.4\textheight}"
            } for line in added))
            self.assertTrue(all(line == "" for line in removed))
            for token in (r"\gkti{", r"\task ", r"\input{figures/", "$", r"\["):
                self.assertEqual(head.count(token), now.count(token), (relative, token))

    def test_task28_updates_exactly_eight_existing_b04_keys_with_layout_only_diffs(self):
        projects = {
            "gk-2022-regular-new-gaokao-1": "2022_新高考Ⅰ卷",
            "gk-2022-regular-new-gaokao-2": "2022_新高考Ⅱ卷",
            "gk-2023-regular-new-gaokao-1": "2023_新高考Ⅰ卷",
            "gk-2023-regular-new-gaokao-2": "2023_新高考Ⅱ卷",
        }
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        ledger_relative = ADJUDICATED_DRIFTS_PATH.relative_to(
            ROOT.parent.parent.parent
        ).as_posix()
        previous_document = json.loads(subprocess.check_output([
            "git", "-C", str(ROOT.parent.parent.parent), "show",
            "1c7b418:" + ledger_relative,
        ]).decode("utf-8"))
        previous = {
            (record["paper_id"], record["artifact"]): record
            for record in previous_document["drifts"]
        }
        self.assertEqual(len(ledger), len(previous))
        selected = {
            key: record for key, record in ledger.items()
            if record["adjudicated_by"] == "task-28-regeneration"
        }
        expected_keys = {
            (paper_id, artifact)
            for paper_id in projects
            for artifact in ("questions.tex", "answers.tex")
        }
        self.assertEqual(set(selected), expected_keys)

        for (paper_id, artifact), record in selected.items():
            relative = "math-gaokao-latex/{}/{}".format(
                projects[paper_id], artifact
            )
            current = ROOT.parent.parent.parent / relative
            head = subprocess.check_output([
                "git", "-C", str(ROOT.parent.parent.parent), "show",
                "1c7b418:" + relative,
            ]).decode("utf-8")
            now = current.read_text(encoding="utf-8")
            self.assertEqual(record["class"], "layout-regeneration")
            self.assertEqual(
                record["legacy_sha256"],
                previous[(paper_id, artifact)]["legacy_sha256"],
            )
            self.assertEqual(record["current_sha256"], file_sha256(current))

            removed = []
            added = []
            for line in difflib.ndiff(head.splitlines(), now.splitlines()):
                if line.startswith("- "):
                    removed.append(line[2:])
                elif line.startswith("+ "):
                    added.append(line[2:])
            self.assertTrue(added)
            self.assertTrue(all(line in {
                r"\nopagebreak[4]", r"\Needspace{0.4\textheight}"
            } for line in added))
            self.assertTrue(all(line == "" for line in removed))
            for token in (r"\gkti{", r"\task ", r"\input{figures/", "$", r"\["):
                self.assertEqual(head.count(token), now.count(token), (relative, token))

    def test_task27_updates_exactly_six_existing_b03_keys_with_layout_only_diffs(self):
        projects = {
            "gk-2020-regular-new-gaokao-2": "2020_新高考Ⅱ卷",
            "gk-2021-regular-new-gaokao-1": "2021_新高考Ⅰ卷",
            "gk-2021-regular-new-gaokao-2": "2021_新高考Ⅱ卷",
        }
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        ledger_relative = ADJUDICATED_DRIFTS_PATH.relative_to(
            ROOT.parent.parent.parent
        ).as_posix()
        previous_document = json.loads(subprocess.check_output([
            "git", "-C", str(ROOT.parent.parent.parent), "show",
            "075ed1c:" + ledger_relative,
        ]).decode("utf-8"))
        previous = {
            (record["paper_id"], record["artifact"]): record
            for record in previous_document["drifts"]
        }
        self.assertEqual(len(ledger), len(previous))
        selected = {
            key: record for key, record in ledger.items()
            if record["adjudicated_by"] == "task-27-regeneration"
        }
        expected_keys = {
            (paper_id, artifact)
            for paper_id in projects
            for artifact in ("questions.tex", "answers.tex")
        }
        self.assertEqual(set(selected), expected_keys)

        for (paper_id, artifact), record in selected.items():
            relative = "math-gaokao-latex/{}/{}".format(
                projects[paper_id], artifact
            )
            current = ROOT.parent.parent.parent / relative
            head = subprocess.check_output([
                "git", "-C", str(ROOT.parent.parent.parent), "show",
                "075ed1c:" + relative,
            ]).decode("utf-8")
            now = current.read_text(encoding="utf-8")
            self.assertEqual(record["class"], "layout-regeneration")
            self.assertEqual(
                record["legacy_sha256"],
                previous[(paper_id, artifact)]["legacy_sha256"],
            )
            self.assertEqual(record["current_sha256"], file_sha256(current))

            removed = []
            added = []
            for line in difflib.ndiff(head.splitlines(), now.splitlines()):
                if line.startswith("- "):
                    removed.append(line[2:])
                elif line.startswith("+ "):
                    added.append(line[2:])
            self.assertTrue(added)
            self.assertTrue(all(line in {
                r"\nopagebreak[4]", r"\Needspace{0.4\textheight}"
            } for line in added))
            self.assertTrue(all(line == "" for line in removed))
            for token in (r"\gkti{", r"\task ", r"\input{figures/", "$", r"\["):
                self.assertEqual(head.count(token), now.count(token), (relative, token))

    def test_task26_updates_exactly_eight_existing_b02_keys_with_layout_only_diffs(self):
        projects = {
            "gk-2019-regular-national-1-arts": "2019_全国Ⅰ卷_文科",
            "gk-2019-regular-national-1-science": "2019_全国Ⅰ卷_理科",
            "gk-2020-regular-national-1-arts": "2020_全国Ⅰ卷_文科",
            "gk-2020-regular-national-1-science": "2020_全国Ⅰ卷_理科",
        }
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        selected = {
            key: record for key, record in ledger.items()
            if record["adjudicated_by"] == "task-26-regeneration"
        }
        expected_keys = {
            (paper_id, artifact)
            for paper_id in projects
            for artifact in ("questions.tex", "answers.tex")
        }
        self.assertEqual(set(selected), expected_keys)

        for (paper_id, artifact), record in selected.items():
            relative = "math-gaokao-latex/{}/{}".format(
                projects[paper_id], artifact
            )
            current = ROOT.parent.parent.parent / relative
            head = subprocess.check_output([
                "git", "-C", str(ROOT.parent.parent.parent), "show",
                "eccf7f0:" + relative,
            ]).decode("utf-8")
            now = current.read_text(encoding="utf-8")
            self.assertEqual(record["class"], "layout-regeneration")
            self.assertEqual(record["current_sha256"], file_sha256(current))

            removed = []
            added = []
            for line in difflib.ndiff(head.splitlines(), now.splitlines()):
                if line.startswith("- "):
                    removed.append(line[2:])
                elif line.startswith("+ "):
                    added.append(line[2:])
            self.assertTrue(added)
            self.assertTrue(all(line in {
                r"\nopagebreak[4]", r"\Needspace{0.4\textheight}"
            } for line in added))
            self.assertTrue(all(line == "" for line in removed))
            for token in (r"\gkti{", r"\task ", r"\input{figures/", "$", r"\["):
                self.assertEqual(head.count(token), now.count(token), (relative, token))

    def test_task25_updates_exactly_eight_existing_keys_with_layout_only_diffs(self):
        projects = {
            "gk-2017-regular-national-1-arts": "2017_全国Ⅰ卷_文科",
            "gk-2017-regular-national-1-science": "2017_全国Ⅰ卷_理科",
            "gk-2018-regular-national-1-arts": "2018_全国Ⅰ卷_文科",
            "gk-2018-regular-national-1-science": "2018_全国Ⅰ卷_理科",
        }
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        selected = {
            key: record for key, record in ledger.items()
            if record["adjudicated_by"] == "task-25-visual-review"
            and key[0] in projects
        }
        expected_keys = {
            (paper_id, artifact)
            for paper_id in projects
            for artifact in ("questions.tex", "answers.tex")
        }
        self.assertEqual(set(selected), expected_keys)
        self.assertEqual(len(selected), 8)

        for (paper_id, artifact), record in selected.items():
            relative = "math-gaokao-latex/{}/{}".format(
                projects[paper_id], artifact
            )
            current = ROOT.parent.parent.parent / relative
            head = subprocess.check_output([
                "git", "-C", str(ROOT.parent.parent.parent), "show",
                "e8f2ff5:" + relative,
            ]).decode("utf-8")
            now = current.read_text(encoding="utf-8")
            self.assertEqual(record["class"], "visual-layout-repair")
            self.assertEqual(record["current_sha256"], file_sha256(current))
            self.assertNotEqual(hashlib.sha256(head.encode()).hexdigest(), record["current_sha256"])

            removed = []
            added = []
            for line in difflib.ndiff(head.splitlines(), now.splitlines()):
                if line.startswith("- "):
                    removed.append(line[2:])
                elif line.startswith("+ "):
                    added.append(line[2:])
            self.assertTrue(added)
            self.assertTrue(all(line in {
                r"\nopagebreak[4]", r"\Needspace{0.4\textheight}"
            } for line in added))
            self.assertTrue(all(line == "" for line in removed))
            for token in (r"\gkti{", r"\task ", r"\input{figures/", "$", r"\["):
                self.assertEqual(head.count(token), now.count(token), (relative, token))

    def test_the_repository_ledger_registers_the_63_shared_tex_drifts(self):
        ledger = load_adjudicated_drifts(ADJUDICATED_DRIFTS_PATH)
        self.assertEqual(len(ledger), 63)
        self.assertEqual(
            {key[1] for key in ledger},
            {"questions.tex", "answers.tex", "answers_short.tex"},
        )
        self.assertTrue(
            all(record["class"] in DRIFT_CLASSES for record in ledger.values())
        )
        # 依据链必须留在文件里：没有它，后人只看得到一张「豁免名单」。
        document = read_json(ADJUDICATED_DRIFTS_PATH)
        self.assertTrue(any("依据链" in line for line in document["$comment"]))


class LegacyIndexRecoveryTests(unittest.TestCase):
    """git 锚点恢复必须 fail-closed：拿不到 blob 或哈希不符一律报错。"""

    @classmethod
    def setUpClass(cls):
        cls.legacy = read_json(FROZEN_LEGACY)

    def test_recovers_the_blob_pinned_by_head_and_sha256(self):
        recovered = recover_legacy_index(self.legacy, ROOT)
        prefix = PurePosixPath(self.legacy["repository"]["compile_path"]).parent
        blob = subprocess.check_output([
            "git", "-C", str(ROOT), "show",
            "{0}:{1}".format(
                self.legacy["repository"]["head"],
                prefix / self.legacy["index"]["path"],
            ),
        ])
        self.assertEqual(
            hashlib.sha256(blob).hexdigest(), self.legacy["index"]["sha256"]
        )
        self.assertEqual(recovered, json.loads(blob.decode("utf-8")))
        self.assertNotIn("batches", recovered)

    def test_a_hash_that_does_not_match_the_blob_fails_closed(self):
        tampered = copy.deepcopy(self.legacy)
        tampered["index"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "SHA-256"):
            recover_legacy_index(tampered, ROOT)

    def test_an_unreachable_commit_or_path_fails_closed(self):
        for mutate in (
            lambda legacy: legacy["repository"].update(head="0" * 40),
            lambda legacy: legacy["index"].update(path="不存在.json"),
        ):
            with self.subTest(mutate=mutate):
                tampered = copy.deepcopy(self.legacy)
                mutate(tampered)
                with self.assertRaisesRegex(ValueError, "取回"):
                    recover_legacy_index(tampered, ROOT)

    def test_malformed_anchor_fields_fail_closed(self):
        for mutate in (
            lambda legacy: legacy["repository"].pop("head"),
            lambda legacy: legacy["index"].update(sha256="不是哈希"),
            lambda legacy: legacy["repository"].pop("compile_path"),
        ):
            with self.subTest(mutate=mutate):
                tampered = copy.deepcopy(self.legacy)
                mutate(tampered)
                with self.assertRaisesRegex(ValueError, "锚点"):
                    recover_legacy_index(tampered, ROOT)


class ComparedFieldCoverageTests(unittest.TestCase):
    """比较闸门自检：采集器吐出的每个键，要么被比较，要么在 reviewed 名单里。

    `_picked` 对两侧都缺失的字段名会静默相等，所以拼错或写旧的字段名会让一个维度悄悄
    停止比较而测试全绿。这个类把"字段名清单与采集器输出同步"变成断言。
    """

    @classmethod
    def setUpClass(cls):
        raw = collect_legacy_baseline(ROOT)
        # 比较的是 compare_baselines 实际 diff 的那两个视图，故 legacy 侧同样补上
        # 由 git 锚点取回的兼容投影。
        cls.legacy = with_legacy_compat(raw, recover_legacy_index(raw, ROOT))
        cls.current = collect_current_baseline(ROOT, load_manifest(MANIFEST))

    def collector_keys(self):
        levels = {level: set() for level in _LEVEL_PATHS}
        for baseline in (self.legacy, self.current):
            levels["baseline"] |= set(baseline)
            levels["repository"] |= set(baseline["repository"])
            levels["index"] |= set(baseline["index"])
            for paper in baseline["papers"]:
                levels["paper"] |= set(paper)
                for target in paper["targets"]:
                    levels["target"] |= set(target)
                    levels["warnings"] |= set(target["warnings"])
                    for name in ("overfull", "underfull", "latex_warnings"):
                        for entry in target["warnings"][name]:
                            levels["warning"] |= set(entry)
        return levels

    def compared_keys(self):
        legacy = _comparable(self.legacy, False)
        current = _comparable(self.current, False)
        levels = {level: set() for level in _LEVEL_PATHS}
        for view in (legacy, current):
            levels["baseline"] |= set(view)
            levels["repository"] |= set(view["repository"])
            levels["index"] |= set(view["index"])
            for paper in view["papers"]:
                levels["paper"] |= set(paper)
                for target in paper["targets"]:
                    levels["target"] |= set(target)
                    levels["warnings"] |= set(target["warnings"])
                    for name in ("overfull", "underfull", "latex_warnings"):
                        for entry in target["warnings"][name]:
                            levels["warning"] |= set(entry)
        return levels

    def test_every_collected_key_is_either_compared_or_reviewed(self):
        collected = self.collector_keys()
        compared = self.compared_keys()
        reviewed = {level: set() for level in _LEVEL_PATHS}
        for level, field, _ in _REVIEWED_FIELDS:
            reviewed[level].add(field)
        for level in _LEVEL_PATHS:
            with self.subTest(level=level):
                self.assertTrue(collected[level], f"{level} 层没有采集到任何键")
                self.assertEqual(compared[level] | reviewed[level], collected[level])

    def test_no_compared_field_is_stale_or_mistyped(self):
        """比较视图里不得残留 _ABSENT——那正是字段名写错时的表现。"""
        def walk(field, value):
            if isinstance(value, dict):
                for key in sorted(value):
                    walk(f"{field}.{key}" if field else str(key), value[key])
                return
            if isinstance(value, list):
                for position, item in enumerate(value):
                    walk(f"{field}[{position}]", item)
                return
            self.assertIsNot(value, _ABSENT, f"{field} 在两侧都缺失，该维度已静默失效")

        for sources_only in (False, True):
            for name, baseline in (
                ("legacy", self.legacy), ("current", self.current),
            ):
                with self.subTest(baseline=name, sources_only=sources_only):
                    walk("", _comparable(baseline, sources_only))

    def test_summary_target_fields_are_only_compared_in_full_mode(self):
        full = _comparable(self.current, False)["summary"]
        sources = _comparable(self.current, True)["summary"]
        self.assertEqual(set(sources), {"paper_count"})
        self.assertIn("total_pages", full)
        self.assertNotIn("targets", _comparable(self.current, True)["papers"][0])


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

    def compare_working(self, *extra):
        stream = io.StringIO()
        with redirect_stdout(stream), redirect_stderr(io.StringIO()):
            code = main([
                "compare-working",
                "--legacy", str(FROZEN_LEGACY),
                "--project-root", str(ROOT),
                "--manifest", str(MANIFEST),
                "--sources-only",
            ] + list(extra))
        return code, stream.getvalue()

    def test_compare_working_reports_the_adjudicated_count_instead_of_zero_drift(self):
        code, output = self.compare_working()
        self.assertEqual(code, 0)
        self.assertIn("已裁定漂移 63 条", output)
        self.assertIn("零未裁定漂移", output)

    def test_pointing_the_ledger_elsewhere_restores_the_alarm(self):
        """登记表不是「默认放行」：拿不到它就必须重新报出全部 63 条。"""
        with tempfile.TemporaryDirectory() as tmp:
            code, output = self.compare_working(
                "--adjudicated", str(Path(tmp) / "不存在.json")
            )
        self.assertEqual(code, 1)
        self.assertNotIn("零未裁定漂移", output)

    def test_a_malformed_ledger_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "adjudicated-drifts.json"
            broken.write_text('{"ledger_version": 99, "drifts": []}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "版本"):
                self.compare_working("--adjudicated", str(broken))

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

    def test_compare_fails_closed_when_the_git_anchor_does_not_verify(self):
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
            tampered = Path(tmp) / "legacy.json"
            data = read_json(FROZEN_LEGACY)
            data["index"]["sha256"] = "0" * 64
            tampered.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable, str(script), "compare",
                    "--legacy", str(tampered), "--current", str(output),
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("SHA-256", result.stderr)
            self.assertNotIn("零未裁定漂移", result.stdout)

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

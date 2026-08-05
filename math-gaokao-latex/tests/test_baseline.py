import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from baseline import _tracked_build_inputs, collect_legacy_baseline, main
from manifest import file_sha256


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


if __name__ == "__main__":
    unittest.main()

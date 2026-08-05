from collections.abc import Mapping
import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from manifest import atomic_write_json, canonical_json, file_sha256
import transaction
from transaction import RepoLock, Transaction, recover_transactions


class SimulatedCrash(RuntimeError):
    pass


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.external = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        self.outside = Path(self.external.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.project = self.repo / "docs" / "exams" / "math-gaokao-latex"
        self.project.mkdir(parents=True)
        self.manifest_path = self.project / "source-manifest.json"
        atomic_write_json(self.manifest_path, self.manifest(0, None))

    def tearDown(self):
        self.temporary.cleanup()
        self.external.cleanup()

    @staticmethod
    def manifest(revision, transaction_id):
        return {
            "revision": revision,
            "last_transaction_id": transaction_id,
            "sources": [],
            "papers": [],
            "batches": [],
        }

    def repo_path(self, relative):
        return self.repo / relative

    def transaction_targets(self, transaction, ordinary):
        targets = dict(ordinary)
        targets["math-gaokao-latex/source-manifest.json"] = canonical_json(
            self.manifest(1, transaction.transaction_id)
        ).encode("utf-8")
        return targets

    def test_second_process_cannot_take_repo_lock(self):
        tools = str(ROOT / "tools")
        script = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[2])
from transaction import RepoLock
try:
    with RepoLock(Path(sys.argv[1])):
        pass
except BlockingIOError:
    raise SystemExit(0)
raise SystemExit(3)
"""
        with RepoLock(self.repo):
            result = subprocess.run(
                [sys.executable, "-c", script, str(self.repo), tools],
                check=False,
                timeout=5,
            )
        self.assertEqual(result.returncode, 0)
        common_dir = subprocess.check_output(
            ["git", "-C", str(self.repo), "rev-parse", "--git-common-dir"],
            text=True,
        ).strip()
        lock_path = Path(common_dir)
        if not lock_path.is_absolute():
            lock_path = self.repo / lock_path
        self.assertTrue((lock_path / "gaokao-latex.lock").exists())

    def test_linked_worktree_uses_the_common_git_directory_lock(self):
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.email", "task1@example.invalid"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.repo), "config", "user.name", "Task 1"],
            check=True,
        )
        (self.repo / "tracked.txt").write_text("tracked", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.repo), "add", "tracked.txt"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "initial"], check=True)
        worktree = self.outside / "linked-worktree"
        subprocess.run(
            ["git", "-C", str(self.repo), "worktree", "add", "-q", "-b", "linked", str(worktree)],
            check=True,
        )
        tools = str(ROOT / "tools")
        script = """
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[2])
from transaction import RepoLock
try:
    with RepoLock(Path(sys.argv[1]), recover=False):
        pass
except BlockingIOError:
    raise SystemExit(0)
raise SystemExit(3)
"""
        try:
            with RepoLock(self.repo, recover=False) as main_lock:
                result = subprocess.run(
                    [sys.executable, "-c", script, str(worktree), tools],
                    check=False,
                    timeout=5,
                )
                common = subprocess.check_output(
                    ["git", "-C", str(worktree), "rev-parse", "--git-common-dir"],
                    text=True,
                ).strip()
                common_path = Path(common)
                if not common_path.is_absolute():
                    common_path = worktree / common_path
                self.assertEqual(main_lock.lock_path, common_path.resolve() / "gaokao-latex.lock")
            self.assertEqual(result.returncode, 0)
        finally:
            subprocess.run(
                ["git", "-C", str(self.repo), "worktree", "remove", "--force", str(worktree)],
                check=True,
            )

    def test_repo_lock_recovers_before_entering_write_section(self):
        target = self.repo / "recover-on-lock.txt"
        target.write_bytes(b"old")
        tx = Transaction(self.repo, event_hook=self._crash_after_replacement(1))
        tx.prepare(
            "content", {"recover-on-lock.txt": b"new"},
            inputs={"source.txt": None},
        )
        with self.assertRaises(SimulatedCrash):
            tx.commit()
        with RepoLock(self.repo):
            self.assertEqual(target.read_bytes(), b"new")
            self.assertFalse(tx.transaction_dir.exists())

    def test_prepared_journal_records_durability_capability(self):
        tx = Transaction(self.repo)
        tx.prepare("content", {"result.txt": b"new"}, inputs={})
        journal = json.loads(tx.journal_path.read_text(encoding="utf-8"))
        self.assertEqual(journal["durability"]["directory_sync"], "fsync")
        self.assertTrue(journal["durability"]["file_sync"])
        self.assertTrue(
            set(journal["durability"]["file_sync"]).issubset({"fsync", "fullfsync"})
        )

    def test_state_revision_cas_failure_writes_no_target(self):
        output = self.repo / "result.txt"
        output.write_bytes(b"old")
        tx = Transaction(self.repo)
        tx.prepare(
            "state",
            self.transaction_targets(tx, {"result.txt": b"new"}),
            inputs={},
            expected_revision=0,
        )
        atomic_write_json(self.manifest_path, self.manifest(2, "someone-else"))
        with self.assertRaisesRegex(RuntimeError, "revision"):
            tx.commit()
        self.assertEqual(output.read_bytes(), b"old")
        self.assertEqual(json.loads(self.manifest_path.read_text())["revision"], 2)

    def test_content_input_cas_failure_writes_no_target(self):
        source = self.repo / "source.txt"
        first = self.repo / "first.txt"
        second = self.repo / "second.txt"
        source.write_bytes(b"input")
        first.write_bytes(b"old-first")
        second.write_bytes(b"old-second")
        tx = Transaction(self.repo)
        tx.prepare(
            "content",
            {"first.txt": b"new-first", "second.txt": b"new-second"},
            inputs={"source.txt": file_sha256(source)},
        )
        source.write_bytes(b"drift")
        with self.assertRaisesRegex(RuntimeError, "输入.*漂移"):
            tx.commit()
        self.assertEqual(first.read_bytes(), b"old-first")
        self.assertEqual(second.read_bytes(), b"old-second")

    def test_prepare_rejects_invalid_mode_contracts(self):
        tx = Transaction(self.repo)
        with self.assertRaisesRegex(ValueError, "相交"):
            tx.prepare(
                "content", {"same.txt": b"x"},
                inputs={"same.txt": None},
            )
        with self.assertRaisesRegex(ValueError, "sha256"):
            Transaction(self.repo).prepare(
                "content", {"x.txt": b"x"}, inputs={"source.txt": "not-a-hash"}
            )
        with self.assertRaisesRegex(ValueError, "manifest.*最后"):
            Transaction(self.repo).prepare(
                "state",
                {"math-gaokao-latex/source-manifest.json": b"{}", "x": b"x"},
                inputs={}, expected_revision=0,
            )
        with self.assertRaisesRegex(ValueError, "revision"):
            Transaction(self.repo).prepare(
                "state", {"x": b"x"}, inputs={}, expected_revision=None,
            )

    def test_prepare_rejects_root_aliases_before_transaction_creation(self):
        aliases = (".", "./", "./.", "././", ".//./")
        sentinel = self.repo / "root-alias-sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        manifest_before = self.manifest_path.read_bytes()
        for alias in aliases:
            for kind in ("target", "input"):
                with self.subTest(path=alias, kind=kind):
                    tx = Transaction(self.repo)
                    targets = {alias: b"new"} if kind == "target" else {"safe.txt": b"new"}
                    inputs = {alias: None} if kind == "input" else {}
                    with self.assertRaisesRegex(ValueError, "非法仓库相对路径"):
                        tx.prepare("content", targets, inputs=inputs)
                    self.assertFalse(tx.transaction_dir.exists())
                    self.assertFalse(tx.journal_path.exists())
                    self.assertFalse((self.repo / "safe.txt").exists())
                    self.assertEqual(sentinel.read_bytes(), b"unchanged")
                    self.assertEqual(self.manifest_path.read_bytes(), manifest_before)

    def test_state_manifest_cannot_use_a_root_alias(self):
        for alias in (".", "./", "./."):
            with self.subTest(path=alias):
                tx = Transaction(self.repo)
                staged = canonical_json(
                    self.manifest(1, tx.transaction_id)
                ).encode("utf-8")
                with self.assertRaisesRegex(ValueError, "非法仓库相对路径"):
                    tx.prepare(
                        "state",
                        {alias: staged},
                        inputs={},
                        expected_revision=0,
                    )
                self.assertFalse(tx.transaction_dir.exists())
                self.assertEqual(
                    json.loads(self.manifest_path.read_text(encoding="utf-8"))["revision"],
                    0,
                )

    def test_target_count_boundary_and_prepare_rejection(self):
        maximum = 10000
        self.assertTrue(hasattr(transaction, "_validate_target_count"))
        self.assertEqual(transaction.MAX_TARGET_COUNT, maximum)
        transaction._validate_target_count(maximum, ValueError)
        with self.assertRaisesRegex(ValueError, "目标数量.*10000"):
            transaction._validate_target_count(maximum + 1, ValueError)
        with self.assertRaisesRegex(RuntimeError, "目标数量.*10000"):
            transaction._validate_target_count(maximum + 1, RuntimeError)

        class OversizedTargets(Mapping):
            def __len__(self):
                return maximum + 1

            def __iter__(self):
                raise AssertionError("数量越界时不应遍历 targets")

            def __getitem__(self, key):
                raise AssertionError("数量越界时不应读取 targets")

        sentinel = self.repo / "count-sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        tx = Transaction(self.repo)
        with self.assertRaisesRegex(ValueError, "目标数量.*10000"):
            tx.prepare("content", OversizedTargets(), inputs={})
        self.assertFalse(tx.transaction_dir.exists())
        self.assertFalse(tx.journal_path.exists())
        self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def test_prepare_rejects_casefold_and_unicode_aliases_before_journal(self):
        cases = (
            ({"Result.txt": b"first", "result.txt": b"second"}, {}, "重复目标"),
            (
                {"safe.txt": b"new"},
                {"Source.txt": None, "source.txt": None},
                "重复输入",
            ),
            (
                {"safe.txt": b"new"},
                {"caf\u00e9.txt": None, "cafe\u0301.txt": None},
                "重复输入",
            ),
            ({"Result.txt": b"new"}, {"result.txt": None}, "相交"),
            (
                {"caf\u00e9.txt": b"first", "cafe\u0301.txt": b"second"},
                {},
                "重复目标",
            ),
            ({"caf\u00e9.txt": b"new"}, {"cafe\u0301.txt": None}, "相交"),
        )
        for targets, inputs, message in cases:
            with self.subTest(targets=tuple(targets), inputs=tuple(inputs)):
                tx = Transaction(self.repo)
                with self.assertRaisesRegex(ValueError, message):
                    tx.prepare("content", targets, inputs=inputs)
                self.assertFalse(tx.transaction_dir.exists())
                self.assertFalse(tx.journal_path.exists())

    def test_prepare_rejects_casefolded_reserved_paths_before_journal(self):
        cases = (
            ".Git/config",
            "DOCS/EXAMS/MATH-GAOKAO-LATEX/.WORK/TRANSACTIONS/payload.bin",
        )
        for reserved in cases:
            for kind in ("target", "input"):
                with self.subTest(path=reserved, kind=kind):
                    tx = Transaction(self.repo)
                    targets = {reserved: b"new"} if kind == "target" else {"safe.txt": b"new"}
                    inputs = {reserved: None} if kind == "input" else {}
                    with self.assertRaisesRegex(ValueError, "保留路径"):
                        tx.prepare("content", targets, inputs=inputs)
                    self.assertFalse(tx.transaction_dir.exists())
                    self.assertFalse(tx.journal_path.exists())

    def test_state_manifest_revision_requires_exact_int(self):
        for revision in (True, False, 0.0, 1.0):
            with self.subTest(staged_revision=revision):
                tx = Transaction(self.repo)
                staged = canonical_json(
                    self.manifest(revision, tx.transaction_id)
                ).encode("utf-8")
                with self.assertRaisesRegex(ValueError, "revision.*整数"):
                    tx.prepare(
                        "state",
                        {"math-gaokao-latex/source-manifest.json": staged},
                        inputs={},
                        expected_revision=0,
                    )
                self.assertFalse(tx.journal_path.exists())

        for revision in (True, False, 0.0, 1.0):
            with self.subTest(installed_revision=revision):
                atomic_write_json(self.manifest_path, self.manifest(0, None))
                target = self.repo / "revision-output.txt"
                target.write_bytes(b"old")
                tx = Transaction(self.repo)
                tx.prepare(
                    "state",
                    self.transaction_targets(tx, {target.name: b"new"}),
                    inputs={},
                    expected_revision=0,
                )
                transaction_id = tx.transaction_id if revision in (True, 1.0) else None
                atomic_write_json(
                    self.manifest_path,
                    self.manifest(revision, transaction_id),
                )
                with self.assertRaisesRegex(RuntimeError, "revision.*整数"):
                    tx.commit()
                self.assertEqual(target.read_bytes(), b"old")
                self.assertTrue(tx.journal_path.exists())
                shutil.rmtree(str(tx.transaction_dir))
                target.unlink()

    def test_prepare_rejects_symlink_components_without_publishing_journal(self):
        outside = self.outside / "outside-targets"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        (self.repo / "linked-parent").symlink_to(outside, target_is_directory=True)
        (self.repo / "linked-target.txt").symlink_to(sentinel)
        (self.repo / "linked-input.txt").symlink_to(sentinel)

        cases = (
            ({"linked-parent/new.txt": b"new"}, {}, "目标父目录"),
            ({"linked-target.txt": b"new"}, {}, "目标文件"),
            ({"result.txt": b"new"}, {"linked-input.txt": file_sha256(sentinel)}, "输入文件"),
        )
        for targets, inputs, label in cases:
            with self.subTest(path_kind=label):
                tx = Transaction(self.repo)
                with self.assertRaisesRegex(ValueError, "符号链接"):
                    tx.prepare("content", targets, inputs=inputs)
                self.assertFalse(tx.transaction_dir.exists())
                self.assertEqual(sentinel.read_bytes(), b"unchanged")
                self.assertFalse((outside / "new.txt").exists())

    def test_prepare_rejects_symlinked_transactions_parent(self):
        outside = self.outside / "outside-transactions"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        work = self.project / ".work"
        work.mkdir()
        (work / "transactions").symlink_to(outside, target_is_directory=True)

        tx = Transaction(self.repo)
        with self.assertRaisesRegex(ValueError, "符号链接"):
            tx.prepare("content", {"result.txt": b"new"}, inputs={})
        self.assertEqual(sorted(path.name for path in outside.iterdir()), ["sentinel.txt"])
        self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def test_recovery_revalidates_target_parent_before_hash_or_replace(self):
        real_parent = self.repo / "switch-parent"
        real_parent.mkdir()
        target = real_parent / "result.txt"
        target.write_bytes(b"old")
        outside = self.outside / "outside-switch"
        outside.mkdir()
        outside_target = outside / "result.txt"
        outside_target.write_bytes(b"outside")
        tx = Transaction(self.repo)
        tx.prepare("content", {"switch-parent/result.txt": b"new"}, inputs={})

        target.unlink()
        real_parent.rmdir()
        real_parent.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(RuntimeError, "符号链接"):
            recover_transactions(self.repo)
        self.assertEqual(outside_target.read_bytes(), b"outside")
        self.assertTrue(tx.journal_path.exists())

    def test_prepare_rejects_protocol_and_git_admin_paths_before_journal(self):
        other_id = "11111111-1111-4111-8111-111111111111"
        cases = (
            "math-gaokao-latex/.work/transactions",
            "math-gaokao-latex/.work/transactions/{own}/journal.json",
            "math-gaokao-latex/.work/transactions/{own}/target-0000.bin",
            "math-gaokao-latex/.work/transactions/%s/payload.bin" % other_id,
            ".git/index.lock",
            ".git/config",
        )
        for template in cases:
            for kind in ("target", "input"):
                with self.subTest(path=template, kind=kind):
                    tx = Transaction(self.repo)
                    path = template.format(own=tx.transaction_id)
                    targets = {path: b"new"} if kind == "target" else {"safe.txt": b"new"}
                    inputs = {path: None} if kind == "input" else {}
                    with self.assertRaisesRegex(ValueError, "保留路径"):
                        tx.prepare("content", targets, inputs=inputs)
                    self.assertFalse(tx.journal_path.exists())

    def test_recovery_rejects_reserved_paths_from_journal(self):
        cases = (
            ".git/index.lock",
            ".Git/config",
            "math-gaokao-latex/.work/transactions/11111111-1111-4111-8111-111111111111/payload.bin",
            "DOCS/EXAMS/MATH-GAOKAO-LATEX/.WORK/TRANSACTIONS/payload.bin",
        )
        for reserved in cases:
            for kind in ("target", "input"):
                with self.subTest(path=reserved, kind=kind):
                    tx = Transaction(self.repo)
                    tx.prepare("content", {"safe.txt": b"new"}, inputs={})
                    journal = json.loads(tx.journal_path.read_text(encoding="utf-8"))
                    if kind == "target":
                        journal["targets"][0]["path"] = reserved
                    else:
                        journal["inputs"] = {reserved: None}
                    atomic_write_json(tx.journal_path, journal)
                    reserved_path = self.repo / reserved
                    before = reserved_path.read_bytes() if reserved_path.is_file() else None
                    with self.assertRaisesRegex(RuntimeError, "保留路径"):
                        recover_transactions(self.repo)
                    self.assertTrue(tx.journal_path.exists())
                    if before is None:
                        self.assertFalse(reserved_path.exists())
                    else:
                        self.assertEqual(reserved_path.read_bytes(), before)
                    shutil.rmtree(str(tx.transaction_dir))

    def test_recovery_rejects_root_aliases_and_preserves_journal(self):
        aliases = (".", "./", "./.", "././", ".//./")
        sentinel = self.repo / "recovery-root-sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        manifest_before = self.manifest_path.read_bytes()
        for alias in aliases:
            for kind in ("target", "input"):
                with self.subTest(path=alias, kind=kind):
                    tx = Transaction(self.repo)
                    tx.prepare("content", {"safe.txt": b"new"}, inputs={})
                    journal = json.loads(tx.journal_path.read_text(encoding="utf-8"))
                    if kind == "target":
                        journal["targets"][0]["path"] = alias
                    else:
                        journal["inputs"] = {alias: None}
                    atomic_write_json(tx.journal_path, journal)
                    with self.assertRaisesRegex(RuntimeError, "非法仓库相对路径"):
                        recover_transactions(self.repo)
                    self.assertTrue(tx.journal_path.exists())
                    self.assertFalse((self.repo / "safe.txt").exists())
                    self.assertEqual(sentinel.read_bytes(), b"unchanged")
                    self.assertEqual(self.manifest_path.read_bytes(), manifest_before)
                    shutil.rmtree(str(tx.transaction_dir))

    def test_recovery_rejects_root_alias_for_state_manifest(self):
        for alias in (".", "./", "./."):
            with self.subTest(path=alias):
                tx = Transaction(self.repo)
                tx.prepare(
                    "state",
                    self.transaction_targets(tx, {"state-safe.txt": b"new"}),
                    inputs={},
                    expected_revision=0,
                )
                journal = json.loads(tx.journal_path.read_text(encoding="utf-8"))
                journal["targets"][-1]["path"] = alias
                atomic_write_json(tx.journal_path, journal)
                with self.assertRaisesRegex(RuntimeError, "非法仓库相对路径"):
                    recover_transactions(self.repo)
                self.assertTrue(tx.journal_path.exists())
                self.assertFalse((self.repo / "state-safe.txt").exists())
                self.assertEqual(
                    json.loads(self.manifest_path.read_text(encoding="utf-8"))["revision"],
                    0,
                )
                shutil.rmtree(str(tx.transaction_dir))

    def test_recovery_rejects_target_count_above_staging_limit(self):
        sentinel = self.repo / "recovery-count-sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        tx = Transaction(self.repo)
        tx.prepare("content", {"safe.txt": b"new"}, inputs={})
        journal = json.loads(tx.journal_path.read_text(encoding="utf-8"))
        journal["targets"] = journal["targets"] * 10001
        atomic_write_json(tx.journal_path, journal)
        with self.assertRaisesRegex(RuntimeError, "目标数量.*10000"):
            recover_transactions(self.repo)
        self.assertTrue(tx.journal_path.exists())
        self.assertFalse((self.repo / "safe.txt").exists())
        self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def test_recovery_rejects_casefold_aliases_in_journal(self):
        def duplicate_targets(journal):
            journal["targets"][1]["path"] = "SAFE.TXT"

        def duplicate_unicode_targets(journal):
            journal["targets"][1]["path"] = "cafe\u0301.txt"

        def duplicate_inputs(journal):
            journal["inputs"] = {"Source.txt": None, "source.txt": None}

        def duplicate_unicode_inputs(journal):
            journal["inputs"] = {"caf\u00e9.txt": None, "cafe\u0301.txt": None}

        def input_target_overlap(journal):
            journal["inputs"] = {"SAFE.TXT": None}

        def unicode_input_target_overlap(journal):
            journal["inputs"] = {"cafe\u0301.txt": None}

        cases = (
            (
                {"safe.txt": b"new", "other.txt": b"other"},
                duplicate_targets,
                "target 重复",
            ),
            (
                {"caf\u00e9.txt": b"new", "other.txt": b"other"},
                duplicate_unicode_targets,
                "target 重复",
            ),
            ({"safe.txt": b"new"}, duplicate_inputs, "输入重复"),
            ({"safe.txt": b"new"}, duplicate_unicode_inputs, "输入重复"),
            ({"safe.txt": b"new"}, input_target_overlap, "相交"),
            ({"caf\u00e9.txt": b"new"}, unicode_input_target_overlap, "相交"),
        )
        for targets, mutate, message in cases:
            with self.subTest(message=message):
                tx = Transaction(self.repo)
                tx.prepare("content", targets, inputs={})
                journal = json.loads(tx.journal_path.read_text(encoding="utf-8"))
                mutate(journal)
                atomic_write_json(tx.journal_path, journal)
                with self.assertRaisesRegex(RuntimeError, message):
                    recover_transactions(self.repo)
                self.assertTrue(tx.journal_path.exists())
                shutil.rmtree(str(tx.transaction_dir))

    def test_prepare_rejects_its_uuid_named_symlink(self):
        transactions = self.project / ".work" / "transactions"
        transactions.mkdir(parents=True)
        outside = self.outside / "outside-prepare-uuid"
        outside.mkdir()
        sentinel = outside / "sentinel.txt"
        sentinel.write_bytes(b"unchanged")
        transaction_id = "33333333-3333-4333-8333-333333333333"
        linked = transactions / transaction_id
        linked.symlink_to(outside, target_is_directory=True)

        tx = Transaction(self.repo, transaction_id=transaction_id)
        with self.assertRaisesRegex(ValueError, "符号链接"):
            tx.prepare("content", {"result.txt": b"new"}, inputs={})
        self.assertTrue(linked.is_symlink())
        self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def test_recovery_rejects_uuid_named_symlink_and_leaves_outside_unchanged(self):
        transactions = self.project / ".work" / "transactions"
        transactions.mkdir(parents=True)
        outside = self.outside / "outside-recovery"
        outside.mkdir()
        sentinel = outside / "journal.json"
        sentinel.write_bytes(b"unchanged")
        linked = transactions / "22222222-2222-4222-8222-222222222222"
        linked.symlink_to(outside, target_is_directory=True)

        with self.assertRaisesRegex(RuntimeError, "符号链接"):
            recover_transactions(self.repo)
        self.assertTrue(linked.is_symlink())
        self.assertEqual(sentinel.read_bytes(), b"unchanged")

    def _crash_after_replacement(self, number):
        count = {"value": 0}

        def hook(event, path):
            if event == "target_replaced":
                count["value"] += 1
                if count["value"] == number:
                    raise SimulatedCrash(str(path))

        return hook

    def test_content_recovery_after_first_and_nth_replacement(self):
        for crash_at in (1, 2):
            with self.subTest(crash_at=crash_at):
                first = self.repo / "first.txt"
                second = self.repo / "second.txt"
                first.write_bytes(b"old-first")
                second.write_bytes(b"old-second")
                tx = Transaction(self.repo, event_hook=self._crash_after_replacement(crash_at))
                tx.prepare(
                    "content",
                    {"first.txt": b"new-first", "second.txt": b"new-second"},
                    inputs={"source.txt": None},
                )
                with self.assertRaises(SimulatedCrash):
                    tx.commit()
                recover_transactions(self.repo)
                self.assertEqual(first.read_bytes(), b"new-first")
                self.assertEqual(second.read_bytes(), b"new-second")
                self.assertFalse(tx.transaction_dir.exists())
                first.unlink()
                second.unlink()

    def test_state_recovery_after_first_and_manifest_replacement(self):
        for crash_at in (1, 2):
            with self.subTest(crash_at=crash_at):
                atomic_write_json(self.manifest_path, self.manifest(0, None))
                output = self.repo / "state-output.txt"
                output.write_bytes(b"old")
                tx = Transaction(self.repo, event_hook=self._crash_after_replacement(crash_at))
                tx.prepare(
                    "state",
                    self.transaction_targets(tx, {"state-output.txt": b"new"}),
                    inputs={}, expected_revision=0,
                )
                with self.assertRaises(SimulatedCrash):
                    tx.commit()
                recover_transactions(self.repo)
                self.assertEqual(output.read_bytes(), b"new")
                manifest = json.loads(self.manifest_path.read_text())
                self.assertEqual(manifest["revision"], 1)
                self.assertEqual(manifest["last_transaction_id"], tx.transaction_id)
                self.assertFalse(tx.transaction_dir.exists())
                output.unlink()

    def test_recovery_discards_unprepared_transaction_directory(self):
        transactions = self.project / ".work" / "transactions"
        orphan = transactions / "00000000-0000-4000-8000-000000000000"
        orphan.mkdir(parents=True)
        (orphan / "target-0000.bin").write_bytes(b"never prepared")
        orphan_real = orphan.resolve()
        transactions_real = transactions.resolve()
        events = []
        recover_transactions(
            self.repo,
            event_hook=lambda event, path: events.append((event, Path(path))),
        )
        self.assertFalse(orphan.exists())
        self.assertIn(("transaction_removed", orphan_real), events)
        self.assertEqual(events[-1], ("transactions_parent_fsynced", transactions_real))

    def test_recovery_revalidates_inputs_after_partial_commit(self):
        source = self.repo / "source.txt"
        target = self.repo / "target.txt"
        source.write_bytes(b"input")
        target.write_bytes(b"old")
        tx = Transaction(self.repo, event_hook=self._crash_after_replacement(1))
        tx.prepare(
            "content", {"target.txt": b"new"},
            inputs={"source.txt": file_sha256(source)},
        )
        with self.assertRaises(SimulatedCrash):
            tx.commit()
        source.write_bytes(b"drift")
        with self.assertRaisesRegex(RuntimeError, "输入.*漂移"):
            recover_transactions(self.repo)
        self.assertTrue((tx.transaction_dir / "journal.json").exists())

    def test_recovery_refuses_third_target_hash_and_preserves_journal(self):
        target = self.repo / "target.txt"
        target.write_bytes(b"old")
        tx = Transaction(self.repo, event_hook=self._crash_after_replacement(1))
        tx.prepare(
            "content", {"target.txt": b"new"},
            inputs={"source.txt": None},
        )
        with self.assertRaises(SimulatedCrash):
            tx.commit()
        target.write_bytes(b"third-party")
        with self.assertRaisesRegex(RuntimeError, "第三种哈希"):
            recover_transactions(self.repo)
        self.assertTrue((tx.transaction_dir / "journal.json").exists())
        self.assertEqual(target.read_bytes(), b"third-party")

    def test_recovery_finishes_partially_deleted_committed_transaction(self):
        target = self.repo / "target.txt"
        target.write_bytes(b"old")

        def hook(event, path):
            if event == "journal_committed":
                raise SimulatedCrash(str(path))

        tx = Transaction(self.repo, event_hook=hook)
        tx.prepare(
            "content", {"target.txt": b"new"},
            inputs={"source.txt": None},
        )
        with self.assertRaises(SimulatedCrash):
            tx.commit()
        for staged in tx.transaction_dir.glob("target-*.bin"):
            staged.unlink()
        recover_transactions(self.repo)
        self.assertEqual(target.read_bytes(), b"new")
        self.assertFalse(tx.transaction_dir.exists())

    def test_recovery_idempotently_finishes_after_all_targets_applied(self):
        for mode in ("content", "state"):
            with self.subTest(mode=mode):
                atomic_write_json(self.manifest_path, self.manifest(0, None))
                target = self.repo / (mode + ".txt")
                target.write_bytes(b"old")

                def hook(event, path):
                    if event == "before_mark_committed":
                        raise SimulatedCrash(str(path))

                tx = Transaction(self.repo, event_hook=hook)
                if mode == "content":
                    targets = {target.name: b"new"}
                    kwargs = {"inputs": {"source.txt": None}}
                else:
                    targets = self.transaction_targets(tx, {target.name: b"new"})
                    kwargs = {"inputs": {}, "expected_revision": 0}
                tx.prepare(mode, targets, **kwargs)
                with self.assertRaises(SimulatedCrash):
                    tx.commit()
                recover_transactions(self.repo)
                recover_transactions(self.repo)
                self.assertEqual(target.read_bytes(), b"new")
                self.assertFalse(tx.transaction_dir.exists())
                target.unlink()

    def test_fsync_order_and_new_directory_entries_survive_simulated_crash(self):
        events = []
        replacements = {"count": 0}

        def hook(event, path):
            events.append((event, Path(path)))
            if event == "target_replaced":
                replacements["count"] += 1
                if replacements["count"] == 1:
                    raise SimulatedCrash(str(path))

        target_relative = "math-gaokao-latex/new/project/receipts/build.json"
        tx = Transaction(self.repo, event_hook=hook)
        tx.prepare(
            "content", {target_relative: b"receipt"},
            inputs={"source.txt": None},
        )
        with self.assertRaises(SimulatedCrash):
            tx.commit()

        first_replace = next(i for i, event in enumerate(events) if event[0] == "target_replaced")
        created = [(i, path) for i, (event, path) in enumerate(events) if event == "directory_created"]
        for created_at, directory in created:
            parent_fsyncs = [
                i for i, (event, path) in enumerate(events)
                if event == "directory_fsynced" and path == directory.parent
            ]
            self.assertTrue(
                any(created_at < i < first_replace for i in parent_fsyncs),
                "new directory entry was not made durable before first target replacement: %s" % directory,
            )

        # 模拟丢失崩溃前未通过父目录 fsync 持久化的所有新目录项。
        for created_at, directory in reversed(created):
            durable = any(
                created_at < i < first_replace
                for i, (event, path) in enumerate(events)
                if event == "directory_fsynced" and path == directory.parent
            )
            if not durable and directory.exists():
                shutil.rmtree(str(directory))
        target = self.repo_path(target_relative)
        target.unlink()  # 替换后尚未执行父目录 fsync 即发生崩溃。

        recover_transactions(self.repo)
        self.assertEqual(target.read_bytes(), b"receipt")

        # 成功事务中每次替换后都要执行父目录 fsync，且完成这些 fsync 后才能记录 committed。
        ordered = []
        tx2 = Transaction(self.repo, event_hook=lambda event, path: ordered.append((event, Path(path))))
        tx2.prepare(
            "content", {"a/out.txt": b"a", "b/out.txt": b"b"},
            inputs={"source.txt": None},
        ).commit()
        committed_at = next(i for i, item in enumerate(ordered) if item[0] == "journal_committed")
        for i, (event, path) in enumerate(ordered):
            if event == "target_replaced":
                self.assertIn(
                    ("target_directory_fsynced", path.parent),
                    ordered[i + 1:committed_at],
                )
        self.assertEqual(ordered[-2][0], "transaction_removed")
        self.assertEqual(ordered[-1], ("transactions_parent_fsynced", tx2.transactions_parent))

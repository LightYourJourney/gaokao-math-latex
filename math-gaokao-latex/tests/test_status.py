# -*- coding: utf-8 -*-
"""Task 15：纯 facts 状态核心 `status.py`。

三条主线：

1. **穷举**——`derive_status()` 对 provenance/build/review/issues/report 的合法状态
   笛卡尔积逐点核对。状态机的价值全在「混合状态下唯一且 fail-closed」，抽样测不出来；
2. **report 门禁**——`derive_content_outcome()` 在报告验证前只能给出 `eligible_*`
   候选，任何路径都不得产出可持久化的 `complete`；批次同理不得 `closed`；
3. **git 派生**——`derive_git_state()` 只认「相对 HEAD 有变化 = validated」与
   「已入 HEAD 且零 diff 且能定位提交 = committed」，其余一律失败而非猜测。

前三条主线一律不 import provenance/build/review：status 核心的全部输入都是闭合 facts。
末尾的 `RealAdapterIntegrationTests` 是**唯一的例外**，Task 16 补入：纯口径测得再全，也
证明不了真实 adapter 递进来的那份 facts 与本核心的字段契约对得上——两侧各自自洽而彼此
错位，正是纯单元测试看不见的那一格。它只做「adapter → 核心」的贯通验证，不引入任何新
的状态规则。
"""
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import status
from status import (
    ARTIFACT_STATES,
    BATCH_STATES,
    BUILD_STATES,
    CONTENT_OUTCOMES,
    CURRENCY_STATES,
    PRODUCTION_STATES,
    PROVENANCE_STATES,
    REVIEW_STATES,
    StatusError,
    batch_ownership_paths,
    derive_content_outcome,
    derive_git_state,
    derive_status,
    facts_without_report,
    paper_facts,
    paper_ownership_paths,
    reconcile_batch_status,
)

PAPER_ID = "gk-2099-regular-national-1"
OTHER_ID = "gk-2099-regular-national-2"


def blocking_issue(paper_id=PAPER_ID):
    return {
        "issue_id": "ISSUE-0009",
        "paper_id": paper_id,
        "affected_paper_ids": [],
        "type": "compile-error",
        "status": "open",
        "impact": "blocks_completion",
        "resume_action": "修源后重编",
    }


def resolved_issue(paper_id=PAPER_ID):
    return dict(blocking_issue(paper_id), status="resolved")


# ------------------------------------------------------------------ 独立口径

# 下面这份优先级表按计划散文逐条誊写，**不是**实现的复制：实现走一串 if，这里是数据。
# 两份口径在 3 万余点笛卡尔积上必须逐点一致，任何一侧写错都会被对方揪出来。


def effective_build(facts):
    if facts["build"] in {"missing", "running"}:
        return facts["build"]
    if facts["build"] == "failed":
        return "failed"
    if facts["build_currency"] == "stale":
        return "stale"
    return facts["build"]


def effective_review(facts):
    if facts["review"] in {"missing", "pending", "failed"}:
        return facts["review"]
    if facts["review_currency"] == "stale":
        return "stale"
    return facts["review"]


def oracle_content_outcome(facts):
    """计划 780 行散文的独立誊写（不含 report 一步）。"""
    if facts["provenance"] != "current":
        if facts["is_legacy"]:
            return "legacy_unverified"
        if facts["provenance"] == "missing":
            return "planned"
        return "eligible_blocked"
    if facts["provenance_unknown"] or facts["provenance_conflicts"]:
        return "eligible_blocked"
    if facts["build"] == "failed" or facts["review"] == "failed":
        return "eligible_blocked"
    if any(
        item.get("impact") == "blocks_completion" and item.get("status") != "resolved"
        for item in facts["issues"]
    ):
        return "eligible_blocked"
    if facts["artifacts"] != "current":
        return "answers_verified"
    if effective_build(facts) in {"missing", "running", "stale"}:
        return "editions_generated"
    if effective_build(facts) != "succeeded" or effective_review(facts) != "passed":
        return "compiled"
    return "eligible_complete"


def oracle_status(facts):
    outcome = oracle_content_outcome(facts)
    if outcome == "eligible_blocked":
        return "blocked"
    if outcome == "eligible_complete":
        return "complete" if facts["batch_report_valid"] else "compiled"
    return outcome


def oracle_batch(facts_by_paper):
    values = list(facts_by_paper.values())
    if any(item["provenance"] != "current" for item in values):
        return "planned"
    # 生成物一行是计划表的缺口（散文列了「生成物」、表里没有），按 fail-closed 补。
    if any(
        item["artifacts"] != "current"
        or effective_build(item) in {"missing", "running", "failed", "stale"}
        for item in values
    ):
        return "provenance_verified"
    if any(effective_build(item) == "compiled_pending_review" for item in values):
        return "compiled_pending_review"
    if any(
        effective_build(item) == "succeeded" and effective_review(item) != "passed"
        for item in values
    ):
        return "compiled_pending_review"
    if any(not item["batch_report_valid"] for item in values):
        return "compiled_pending_review"
    derived = [oracle_status(item) for item in values]
    if all(item == "complete" for item in derived):
        return "closed"
    if all(item in {"complete", "blocked"} for item in derived) and any(
        item == "blocked" for item in derived
    ):
        return "closed_with_blockers"
    raise AssertionError("独立口径未命中任何分支")


def all_axes(paper_id=PAPER_ID):
    """合法 facts 的完整笛卡尔积（issues 取空/未解决阻断/已解决三档）。"""
    issue_axis = ((), (blocking_issue(paper_id),), (resolved_issue(paper_id),))
    for combo in itertools.product(
        (False, True), PROVENANCE_STATES, (False, True), (False, True), ARTIFACT_STATES,
        BUILD_STATES, CURRENCY_STATES, REVIEW_STATES, CURRENCY_STATES,
        issue_axis, (False, True),
    ):
        yield paper_facts(
            paper_id,
            is_legacy=combo[0],
            provenance=combo[1],
            provenance_unknown=combo[2],
            provenance_conflicts=combo[3],
            artifacts=combo[4],
            build=combo[5],
            build_currency=combo[6],
            review=combo[7],
            review_currency=combo[8],
            issues=combo[9],
            batch_report_valid=combo[10],
        )


# ------------------------------------------------------------------ facts 契约


class FactsContractTests(unittest.TestCase):
    def test_the_state_vocabularies_are_frozen(self):
        self.assertEqual(
            PROVENANCE_STATES, ("missing", "invalid", "stale", "current")
        )
        self.assertEqual(
            BUILD_STATES,
            ("missing", "running", "failed", "compiled_pending_review", "succeeded"),
        )
        self.assertEqual(REVIEW_STATES, ("missing", "pending", "failed", "passed"))
        self.assertEqual(ARTIFACT_STATES, ("missing", "stale", "current"))
        self.assertEqual(CURRENCY_STATES, ("current", "stale"))
        self.assertEqual(
            PRODUCTION_STATES,
            (
                "legacy_unverified", "planned", "source_ready", "transcription_draft",
                "questions_verified", "answers_draft", "answers_verified",
                "shared_frozen", "editions_generated", "compiled", "complete",
                "blocked",
            ),
        )
        self.assertEqual(
            BATCH_STATES,
            (
                "planned", "provenance_verified", "compiled_pending_review",
                "closed", "closed_with_blockers",
            ),
        )
        self.assertEqual(
            CONTENT_OUTCOMES,
            (
                "legacy_unverified", "planned", "answers_verified",
                "editions_generated", "compiled", "eligible_blocked",
                "eligible_complete",
            ),
        )

    def test_an_unknown_fact_value_is_rejected(self):
        with self.assertRaises(StatusError):
            paper_facts(PAPER_ID, build="compiled")

    def test_an_unknown_fact_key_is_rejected(self):
        facts = paper_facts(PAPER_ID)
        facts["reviewed_by"] = "人工"
        with self.assertRaises(StatusError):
            derive_status(facts)

    def test_a_missing_fact_key_is_rejected(self):
        facts = paper_facts(PAPER_ID)
        del facts["review_currency"]
        with self.assertRaises(StatusError):
            derive_status(facts)

    def test_content_outcome_refuses_facts_that_carry_the_report(self):
        # 带着 report 事实调用内容候选 = 把最终裁决混进候选阶段，必须当场拒绝。
        with self.assertRaises(StatusError):
            derive_content_outcome(paper_facts(PAPER_ID))

    def test_facts_without_report_drops_exactly_one_key(self):
        facts = paper_facts(PAPER_ID)
        trimmed = facts_without_report(facts)
        self.assertEqual(set(facts) - set(trimmed), {"batch_report_valid"})
        self.assertNotIn("batch_report_valid", trimmed)


# ------------------------------------------------------------------ 笛卡尔积


class ExhaustiveStatusTests(unittest.TestCase):
    def test_every_legal_combination_matches_the_independent_oracle(self):
        checked = 0
        for facts in all_axes():
            with self.subTest(facts=json.dumps(
                {k: v for k, v in facts.items() if k != "issues"}, sort_keys=True
            ), issues=len(facts["issues"])):
                self.assertEqual(derive_status(facts), oracle_status(facts))
                self.assertEqual(
                    derive_content_outcome(facts_without_report(facts)),
                    oracle_content_outcome(facts),
                )
            checked += 1
        self.assertEqual(checked, 2 * 4 * 2 * 2 * 3 * 5 * 2 * 4 * 2 * 3 * 2)

    def test_every_derived_status_is_in_the_frozen_enum(self):
        for facts in all_axes():
            self.assertIn(derive_status(facts), PRODUCTION_STATES)

    def test_content_outcome_never_produces_a_persistable_final_state(self):
        for facts in all_axes():
            outcome = derive_content_outcome(facts_without_report(facts))
            self.assertIn(outcome, CONTENT_OUTCOMES)
            self.assertNotIn(outcome, {"complete", "closed", "blocked"})

    def test_complete_requires_the_whole_evidence_chain(self):
        for facts in all_axes():
            if derive_status(facts) != "complete":
                continue
            self.assertEqual(facts["provenance"], "current")
            self.assertFalse(facts["provenance_unknown"])
            self.assertFalse(facts["provenance_conflicts"])
            self.assertEqual(facts["artifacts"], "current")
            self.assertEqual(facts["build"], "succeeded")
            self.assertEqual(facts["build_currency"], "current")
            self.assertEqual(facts["review"], "passed")
            self.assertEqual(facts["review_currency"], "current")
            self.assertTrue(facts["batch_report_valid"])
            self.assertEqual([], [
                item for item in facts["issues"]
                if item["impact"] == "blocks_completion" and item["status"] != "resolved"
            ])

    def test_noncurrent_provenance_respects_legacy_identity(self):
        expected = {
            (True, "missing"): "legacy_unverified",
            (True, "invalid"): "legacy_unverified",
            (True, "stale"): "legacy_unverified",
            (False, "missing"): "planned",
            (False, "invalid"): "blocked",
            (False, "stale"): "blocked",
        }
        for (is_legacy, provenance), status in expected.items():
            with self.subTest(is_legacy=is_legacy, provenance=provenance):
                facts = paper_facts(
                    PAPER_ID, is_legacy=is_legacy, provenance=provenance
                )
                self.assertEqual(derive_status(facts), status)

    def test_blocked_is_exactly_the_blocker_predicate(self):
        for facts in all_axes():
            expected = (
                not facts["is_legacy"]
                and facts["provenance"] in {"invalid", "stale"}
            ) or facts["provenance"] == "current" and (
                    facts["provenance_unknown"]
                    or facts["provenance_conflicts"]
                    or facts["build"] == "failed"
                    or facts["review"] == "failed"
                    or any(
                        item["impact"] == "blocks_completion"
                        and item["status"] != "resolved"
                        for item in facts["issues"]
                    )
                )
            self.assertEqual(derive_status(facts) == "blocked", expected)


# ------------------------------------------------------------------ 具名场景


class NamedScenarioTests(unittest.TestCase):
    def base(self, **overrides):
        values = dict(
            provenance="current", artifacts="current", build="succeeded",
            build_currency="current", review="passed", review_currency="current",
            batch_report_valid=True,
        )
        values.update(overrides)
        return paper_facts(PAPER_ID, **values)

    def test_running_build_ignores_any_stale_review_verdict(self):
        # 计划：build running 时无论旧 review 状态为何都不得越过 editions_generated。
        for review, currency in (
            ("passed", "current"), ("passed", "stale"), ("missing", "stale"),
            ("pending", "current"),
        ):
            facts = self.base(build="running", review=review, review_currency=currency)
            self.assertEqual(derive_status(facts), "editions_generated")
            self.assertEqual(
                reconcile_batch_status({PAPER_ID: facts}), "provenance_verified"
            )

    def test_succeeded_build_with_passed_review_but_no_report_is_not_complete(self):
        facts = self.base(batch_report_valid=False)
        self.assertEqual(derive_status(facts), "compiled")
        self.assertEqual(
            derive_content_outcome(facts_without_report(facts)), "eligible_complete"
        )
        self.assertEqual(
            reconcile_batch_status({PAPER_ID: facts}), "compiled_pending_review"
        )

    def test_a_stale_receipt_demotes_both_paper_and_batch(self):
        facts = self.base(build_currency="stale")
        self.assertEqual(derive_status(facts), "editions_generated")
        self.assertEqual(
            reconcile_batch_status({PAPER_ID: facts}), "provenance_verified"
        )
        facts = self.base(review_currency="stale")
        self.assertEqual(derive_status(facts), "compiled")
        self.assertEqual(
            reconcile_batch_status({PAPER_ID: facts}), "compiled_pending_review"
        )

    def test_an_overfull_only_build_is_pending_review_not_failed(self):
        facts = self.base(build="compiled_pending_review", review="pending")
        self.assertEqual(derive_status(facts), "compiled")
        self.assertEqual(
            reconcile_batch_status({PAPER_ID: facts}), "compiled_pending_review"
        )

    def test_a_failed_review_never_demotes_the_build_to_failed(self):
        facts = self.base(review="failed")
        self.assertEqual(derive_status(facts), "blocked")
        self.assertEqual(
            reconcile_batch_status({PAPER_ID: facts}), "compiled_pending_review"
        )

    def test_a_resolved_issue_no_longer_blocks(self):
        self.assertEqual(
            derive_status(self.base(issues=(resolved_issue(),))), "complete"
        )
        self.assertEqual(
            derive_status(self.base(issues=(blocking_issue(),))), "blocked"
        )

    def test_an_issue_targeting_another_paper_does_not_block(self):
        facts = self.base(issues=(blocking_issue(OTHER_ID),))
        self.assertEqual(derive_status(facts), "complete")

    def test_a_shared_issue_blocks_every_affected_paper(self):
        shared = {
            "issue_id": "ISSUE-0002",
            "paper_id": None,
            "affected_paper_ids": [OTHER_ID, PAPER_ID],
            "type": "identity-ambiguous",
            "status": "open",
            "impact": "blocks_completion",
            "resume_action": "逐卷核验",
        }
        self.assertEqual(derive_status(self.base(issues=(shared,))), "blocked")

    def test_a_non_blocking_issue_does_not_block(self):
        soft = dict(blocking_issue(), impact="non_blocking")
        self.assertEqual(derive_status(self.base(issues=(soft,))), "complete")


# ------------------------------------------------------------------ 批次聚合


class BatchReconcilerTests(unittest.TestCase):
    def facts(self, **overrides):
        values = dict(
            provenance="current", artifacts="current", build="succeeded",
            build_currency="current", review="passed", review_currency="current",
            batch_report_valid=True,
        )
        values.update(overrides)
        return values

    def batch(self, *papers):
        return {
            "gk-2099-regular-national-%d" % index: paper_facts(
                "gk-2099-regular-national-%d" % index, **values
            )
            for index, values in enumerate(papers, start=1)
        }

    def test_an_empty_batch_is_a_state_machine_defect(self):
        with self.assertRaises(StatusError):
            reconcile_batch_status({})

    def test_one_invalid_provenance_pulls_the_whole_batch_to_planned(self):
        mixed = self.batch(self.facts(), self.facts(provenance="missing"))
        self.assertEqual(reconcile_batch_status(mixed), "planned")

    def test_one_failed_build_keeps_the_batch_at_provenance_verified(self):
        mixed = self.batch(self.facts(), self.facts(build="failed"))
        self.assertEqual(reconcile_batch_status(mixed), "provenance_verified")

    def test_a_fully_reviewed_batch_closes(self):
        self.assertEqual(
            reconcile_batch_status(self.batch(self.facts(), self.facts())), "closed"
        )

    def test_a_blocked_paper_closes_the_batch_with_blockers(self):
        mixed = self.batch(self.facts(), self.facts(issues=(blocking_issue(
            "gk-2099-regular-national-2"
        ),)))
        self.assertEqual(reconcile_batch_status(mixed), "closed_with_blockers")

    def test_every_mixed_batch_matches_the_independent_oracle(self):
        interesting = [
            self.facts(),
            self.facts(provenance="stale"),
            self.facts(build="running"),
            self.facts(build="failed"),
            self.facts(build="compiled_pending_review", review="pending"),
            self.facts(build_currency="stale"),
            self.facts(review="missing"),
            self.facts(review_currency="stale"),
            self.facts(batch_report_valid=False),
            self.facts(artifacts="stale"),
            self.facts(provenance_unknown=True),
        ]
        for left, right in itertools.product(interesting, repeat=2):
            mixed = self.batch(left, right)
            with self.subTest(left=left, right=right):
                self.assertEqual(reconcile_batch_status(mixed), oracle_batch(mixed))

    def test_a_batch_never_closes_before_the_report_is_valid(self):
        for left, right in itertools.product(
            (True, False), repeat=2
        ):
            mixed = self.batch(
                self.facts(batch_report_valid=left),
                self.facts(batch_report_valid=right),
            )
            if not (left and right):
                self.assertEqual(
                    reconcile_batch_status(mixed), "compiled_pending_review"
                )


# ------------------------------------------------------------------ 所有权路径


def manifest_document(papers, batches):
    return {
        "papers": papers,
        "batches": batches,
        "revision": 3,
        "last_transaction_id": None,
    }


class OwnershipPathTests(unittest.TestCase):
    def setUp(self):
        self.manifest = manifest_document(
            [
                {"paper_id": PAPER_ID, "project_dir": "2099_全国1卷"},
                {"paper_id": OTHER_ID, "project_dir": "2099_全国2卷"},
            ],
            [{"batch_id": "phase0-b01", "paper_ids": [OTHER_ID, PAPER_ID]}],
        )

    def test_batch_paths_are_the_exact_build_receipts_sorted(self):
        self.assertEqual(
            batch_ownership_paths(self.manifest, "phase0-b01"),
            (
                "math-gaokao-latex/2099_全国1卷/receipts/build.json",
                "math-gaokao-latex/2099_全国2卷/receipts/build.json",
            ),
        )

    def test_an_unknown_batch_fails_closed(self):
        with self.assertRaises(StatusError):
            batch_ownership_paths(self.manifest, "phase0-b99")

    def test_an_unknown_paper_fails_closed(self):
        with self.assertRaises(StatusError):
            paper_ownership_paths(self.manifest, ["gk-2099-regular-national-9"])

    def test_paper_paths_never_include_state_files(self):
        for path in paper_ownership_paths(self.manifest, [PAPER_ID]):
            self.assertTrue(path.endswith("/receipts/build.json"))


# ------------------------------------------------------------------ git 派生


class GitFixture:
    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for key, value in (
            ("user.email", "t15@example.invalid"), ("user.name", "Task 15")
        ):
            subprocess.run(
                ["git", "-C", str(self.root), "config", key, value], check=True
            )

    def cleanup(self):
        self.temporary.cleanup()

    def write(self, relative, text):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def git(self, *arguments):
        subprocess.run(["git", "-C", str(self.root)] + list(arguments), check=True)

    def commit(self, message="c"):
        self.git("commit", "-q", "-m", message)


class GitStateTests(unittest.TestCase):
    def setUp(self):
        self.fixture = GitFixture()
        self.addCleanup(self.fixture.cleanup)
        self.paths = ["a/receipts/build.json", "b/receipts/build.json"]
        for relative in self.paths:
            self.fixture.write(relative, "{}\n")
        self.fixture.write("README.md", "x\n")
        self.fixture.git("add", "README.md")
        self.fixture.commit("初始提交")

    def test_untracked_ownership_paths_are_validated(self):
        self.assertEqual(derive_git_state(self.fixture.root, self.paths), "validated")

    def test_staged_ownership_paths_are_validated(self):
        self.fixture.git("add", *self.paths)
        self.assertEqual(derive_git_state(self.fixture.root, self.paths), "validated")

    def test_unstaged_modification_after_commit_is_validated(self):
        self.fixture.git("add", *self.paths)
        self.fixture.commit("回执")
        self.fixture.write(self.paths[0], '{"changed": true}\n')
        self.assertEqual(derive_git_state(self.fixture.root, self.paths), "validated")

    def test_committed_ownership_paths_are_committed(self):
        self.fixture.git("add", *self.paths)
        self.fixture.commit("回执")
        self.assertEqual(derive_git_state(self.fixture.root, self.paths), "committed")

    def test_a_path_missing_from_head_fails(self):
        self.fixture.git("add", self.paths[0])
        self.fixture.commit("只提交一个")
        (self.fixture.root / self.paths[1]).unlink()
        with self.assertRaises(StatusError):
            derive_git_state(self.fixture.root, self.paths)

    def test_an_empty_path_set_fails(self):
        with self.assertRaises(StatusError):
            derive_git_state(self.fixture.root, [])

    def test_an_absolute_or_escaping_path_fails(self):
        for bad in ("/etc/passwd", "../outside.json", "a/../../x.json"):
            with self.assertRaises(StatusError):
                derive_git_state(self.fixture.root, [bad])


# ------------------------------------------------------------------ 真实 adapter


class RealAdapterIntegrationTests(unittest.TestCase):
    """Task 16：真实 provenance adapter 递进来的 facts 必须直接喂得进本核心。

    夹具借用 `test_provenance.ProvenanceFixture`（三卷：两卷上游源、一卷回忆版带
    identity blocker），本类只断言「adapter 出来的东西正好是核心要的东西」。
    """

    @classmethod
    def setUpClass(cls):
        import test_provenance
        cls.support = test_provenance

    def setUp(self):
        self.fixture = self.support.ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)
        for paper in self.fixture.papers:
            self.fixture.install(paper["paper_id"])

    def loaded(self, **overrides):
        return self.fixture.loader(**overrides)(
            self.fixture.root, self.fixture.manifest(),
            [paper["paper_id"] for paper in self.fixture.papers],
        )

    def full(self, **overrides):
        return {
            paper_id: paper_facts(
                paper_id, build="succeeded", build_currency="current", **values
            )
            for paper_id, values in self.loaded(**overrides).items()
        }

    def test_the_adapter_output_is_accepted_by_paper_facts_verbatim(self):
        for paper_id, values in self.loaded().items():
            with self.subTest(paper_id=paper_id):
                # 多一个键、少一个键都会被 validate_facts 当场拒绝。
                facts = paper_facts(
                    paper_id, build="missing", build_currency="stale", **values
                )
                self.assertIn(derive_status(facts), PRODUCTION_STATES)

    def test_a_verified_batch_without_builds_stays_at_provenance_verified(self):
        facts = {
            paper_id: paper_facts(
                paper_id, build="missing", build_currency="stale", **values
            )
            for paper_id, values in self.loaded().items()
        }
        self.assertEqual(reconcile_batch_status(facts), "provenance_verified")

    def test_a_full_evidence_chain_closes_the_batch_with_the_recall_blocker(self):
        facts = self.full(
            review="passed", review_currency="current", batch_report_valid=True
        )
        derived = {key: derive_status(value) for key, value in facts.items()}
        self.assertEqual(derived[self.support.PAPER_ONE], "complete")
        self.assertEqual(derived[self.support.PAPER_TWO], "complete")
        self.assertEqual(derived[self.support.PAPER_RECALL], "blocked")
        self.assertEqual(reconcile_batch_status(facts), "closed_with_blockers")

    def test_a_missing_provenance_pulls_the_whole_batch_back_to_planned(self):
        (self.fixture.root / self.fixture.provenance_relative(
            self.support.PAPER_TWO
        )).unlink()
        facts = self.full(
            review="passed", review_currency="current", batch_report_valid=True
        )
        self.assertEqual(reconcile_batch_status(facts), "planned")


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Task 16：逐题 provenance、结构化问题联动与完成状态验证器。

四条主线：

1. **哈希口径冻结**——`question_text_sha256` 是题面块「去行尾空白 + 统一 LF」后的
   UTF-8 SHA-256；`answer_sha256` 绝不对自由文本直接取哈希，而是把
   `parse_answer_points()` 折出的 `AnswerRecord` 排序后构造规范 JSON 再取哈希。
   两者任一变化即让核验失效；
2. **假绿反例**——「引用另一卷的有效 source」「source 非 ready」「页码越界」
   「本地路径不属于本卷」四条必须逐条被拒。有效 ≠ 属于本卷；
3. **完成判定**——failed/uncertain 题面核对、U 级答案、unresolved 冲突、角色重复、
   review pending/failed、open/investigating/deferred 的 blocker，任一存在都不得
   `complete`。状态规则本身仍只属于 Task 15 的 `status.py`，本模块只产 facts；
4. **三角色 .work 与单事务导入**——三条独占路径、work-dir 必须落在 ignored `.work`
   内、三组 paper 集合恰好等于批次、题号一致，最后一个 `state` 事务提交 provenance /
   issues / manifest。
"""
import copy
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
sys.path.insert(0, str(ROOT.parent / "math-gaokao-2017-2026" / "tools"))

import issues as issues_module
import provenance
import source_manifest
import status as status_core
from manifest import atomic_write_json, canonical_json, file_sha256, load_manifest
from make_short_answers import expected_answer_records
from provenance import (
    ANSWER_GRADES,
    CONFLICT_STATES,
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    STAGES,
    TRANSCRIPTION_RESULTS,
    ProvenanceError,
    answer_digests,
    check_batch,
    import_batch,
    init_batch,
    load_provenance_facts,
    new_provenance,
    question_id,
    question_text_digests,
    validate_provenance,
)
from solution_sources import parse_question_blocks
from status import derive_status, reconcile_batch_status
from transaction import TRANSACTIONS_RELATIVE, recover_transactions

PROJECT_RELATIVE = "math-gaokao-latex"
MANIFEST_TARGET = PROJECT_RELATIVE + "/source-manifest.json"
ISSUES_TARGET = PROJECT_RELATIVE + "/missing-issues.md"
WORK_RELATIVE = PROJECT_RELATIVE + "/.work"
BATCH_ID = "phase0-b01"

PAPER_ONE = "gk-2099-regular-national-1"
PAPER_TWO = "gk-2099-regular-national-2"
PAPER_RECALL = "gk-2099-regular-national-3-recall"
DIR_ONE = "2099_全国1卷"
DIR_TWO = "2099_全国2卷"
DIR_RECALL = "2099_全国3卷_回忆版"
SOURCE_ONE = "src-" + "1" * 64
SOURCE_TWO = "src-" + "2" * 64

ROLE_QUESTION = "核对员甲"
ROLE_SOLVER = "求解员乙"
ROLE_REVIEWER = "盲核员丙"

QUESTIONS_MD = """---
title: 2099 年数学真题（试题）
---

# 2099 年测试卷

**1．** 已知集合 $A=\\{x\\mid x<1\\}$，则（　　）

  A．$1$　　B．$2$

**2．** 求 $1+1$ 的值。

**3．（12 分）** 已知函数 $f(x)$。

  (1) 求 $f(1)$；

  (2) 求 $f(2)$。
"""

# 真库 21 份 `_试题.md` 一律以这个形状收尾（实测：thematic break 之后恰好一行引用块，
# 三种文案 `原卷影印件`/`试题来源` 皆然）。它落在**最后一题**的正文里，因为后面没有
# 下一题来接管——这正是 2017 理/文两卷 q23 题面逐字相同却算出两个摘要的原因。
FOOTER_TEMPLATE = "\n---\n\n> **原卷影印件**：[`../_raw/2099_数学_%s.pdf`](../_raw/)\n"

ANSWER_KEY_MD = """---
title: 2099 年数学真题（答案要点）
---

# 2099 年测试卷 · 答案要点

**1．** 集合运算

> **答案：A**
>
> 由定义直接可得。

**2．** 直接计算

> **答案：$2$**

**3．** 函数性质

> **(1) 答案：$f(1)=1$**
>
> **(2) 答案：$f(2)=2$**
"""


def paper_entry(paper_id, project_dir, legacy_id, source_ids, legacy_source_files):
    prefix = "2099/%s" % legacy_id
    return {
        "blocked_from": None,
        "figure_files": [],
        "issue_ids": [],
        "last_verified_hash": None,
        "legacy_ids": [legacy_id],
        "legacy_source_files": list(legacy_source_files),
        "paper_id": paper_id,
        "production_state": "legacy_unverified",
        "project_dir": project_dir,
        "question_count": 3,
        "resume_action": None,
        "source_files": {
            "answer_key": prefix + "_答案要点.md",
            "combined_rendered": prefix + "_含解析.md",
            "questions": prefix + "_试题.md",
            "solution_body": prefix + "_解析正文.md",
        },
        "source_ids": list(source_ids),
        "title": "2099 年·%s" % project_dir,
        "track": "none",
        "year": 2099,
    }


def source_entry(source_id, paper_id, page_count=4, source_state="ready"):
    return {
        "artifact": {
            "git_oid_verified": True,
            "header_is_pdf": True,
            "media_type": "application/pdf",
            "page_count": page_count,
            "pdf_check": "passed",
            "pdfinfo_version": "26.08.0",
            "sha256": hashlib.sha256(source_id.encode("utf-8")).hexdigest(),
            "size_bytes": 1024,
        },
        "exam_type": "regular",
        "git_blob_oid": "a" * 40,
        "issue_ids": [],
        "paper_id": paper_id,
        "paper_relation": "canonical" if paper_id is not None else None,
        "raw_paper_name": "%s.pdf" % source_id,
        "regions": [],
        "source_id": source_id,
        "source_state": source_state,
        "track": None,
        "upstream_path": "普通高考/2099/%s.pdf" % source_id,
        "year": 2099,
    }


class ProvenanceFixture:
    """自带 schema、三卷规范源、问题总账与 ignored `.work` 的临时 git 仓库。

    第三卷是「回忆版」镜像：没有确认上游 source，只有登记在案的 `legacy_source_files`，
    并带一条 open 的 identity-ambiguous blocker——它必须永远拿不到 `complete`。
    """

    def __init__(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for key, value in (
            ("user.email", "t16@example.invalid"), ("user.name", "Task 16")
        ):
            subprocess.run(
                ["git", "-C", str(self.root), "config", key, value], check=True
            )
        for name in ("source-manifest.schema.json", "provenance.schema.json"):
            self.copy_real("%s/schemas/%s" % (PROJECT_RELATIVE, name))
        self.copy_real("%s/.gitignore" % PROJECT_RELATIVE)

        self.papers = [
            paper_entry(PAPER_ONE, DIR_ONE, "legacy2099a", [SOURCE_ONE], []),
            paper_entry(PAPER_TWO, DIR_TWO, "legacy2099b", [SOURCE_TWO], []),
            paper_entry(PAPER_RECALL, DIR_RECALL, "legacy2099c", [], []),
        ]
        for paper in self.papers:
            for key in ("questions", "answer_key"):
                self.write(
                    paper["source_files"][key],
                    QUESTIONS_MD if key == "questions" else ANSWER_KEY_MD,
                )
        recall = self.papers[2]
        recall["legacy_source_files"] = [{
            "path": recall["source_files"]["questions"],
            "sha256": file_sha256(self.root / recall["source_files"]["questions"]),
        }]

        self.manifest_path = self.root / MANIFEST_TARGET
        atomic_write_json(self.manifest_path, self.document())
        self.issues_path = self.root / ISSUES_TARGET
        issues_module.main([
            "init", "--phase0-seed", "--output", str(self.issues_path)
        ])
        self.seed_recall_blocker()
        self.work_dir = self.root / WORK_RELATIVE
        self.commit_all("初始提交")

    # ------------------------------------------------------------ 基础操作

    def document(self, revision=1):
        return {
            "$schema": "schemas/source-manifest.schema.json",
            "batches": [{
                "batch_id": BATCH_ID,
                "issues": [],
                "paper_ids": [paper["paper_id"] for paper in self.papers],
                "status": "planned",
            }],
            "inventory": {"root_counts": {}, "total_sources": 0},
            "last_transaction_id": None,
            "papers": copy.deepcopy(self.papers),
            "revision": revision,
            "schema_version": 1,
            "sources": [
                source_entry(SOURCE_ONE, PAPER_ONE),
                source_entry(SOURCE_TWO, PAPER_TWO),
            ],
            "upstream": {
                "commit": "0" * 40,
                "scoped_roots": ["普通高考"],
                "url": "https://example.invalid/gaokaomath",
            },
        }

    def seed_recall_blocker(self):
        """回忆版身份问题：与生产 seed 同形，只换 paper_id。"""
        issues_module.upsert_issue(self.issues_path, {
            "paper_id": PAPER_RECALL,
            "affected_paper_ids": [],
            "type": "identity-ambiguous",
            "status": "open",
            "impact": "blocks_completion",
            "resume_action": "正式卷公开后人工核验身份；回忆版不得自动绑定正式卷",
            "conflict_code": "recall-vs-official",
        })

    def cleanup(self):
        self.temporary.cleanup()

    def copy_real(self, relative):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT.parent.parent.parent / relative, target)

    def write(self, relative, text):
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def read_bytes(self, relative):
        return (self.root / relative).read_bytes()

    def git(self, *arguments):
        subprocess.run(["git", "-C", str(self.root)] + list(arguments), check=True)

    def commit_all(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def manifest(self):
        return load_manifest(self.manifest_path)

    def provenance_relative(self, paper_id):
        return status_core.provenance_path(
            next(item for item in self.manifest()["papers"]
                 if item["paper_id"] == paper_id)
        )

    def snapshot(self):
        recorded = {}
        for path in sorted(self.root.rglob("*")):
            if ".git" in path.parts or not path.is_file():
                continue
            recorded[path.relative_to(self.root).as_posix()] = file_sha256(path)
        return recorded

    def rewrite_manifest(self, mutate):
        """就地改写 manifest（绕过事务，供只读判定与前置条件构造使用）。"""
        document = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        mutate(document)
        atomic_write_json(self.manifest_path, document)
        return document

    def unbind(self, *source_ids):
        """把若干 source 还原成「ready 但未绑定」——T17 面对的真实起点。"""
        def mutate(document):
            targets = set(source_ids)
            released = set()
            for source in document["sources"]:
                if source["source_id"] not in targets:
                    continue
                released.add(source["paper_id"])
                source["paper_id"] = None
                source["paper_relation"] = None
            for paper in document["papers"]:
                if paper["paper_id"] in released:
                    paper["source_ids"] = [
                        item for item in paper["source_ids"] if item not in targets
                    ]
        return self.rewrite_manifest(mutate)

    # ------------------------------------------------------------ 真值构造

    def truth(self, paper_id):
        """本卷三种哈希的现场真值（题面 / 答案 / 来源）。"""
        paper = next(
            item for item in self.papers if item["paper_id"] == paper_id
        )
        questions = (self.root / paper["source_files"]["questions"]).read_text(
            encoding="utf-8"
        )
        answers = (self.root / paper["source_files"]["answer_key"]).read_text(
            encoding="utf-8"
        )
        return {
            "texts": question_text_digests(questions),
            "answers": answer_digests(paper_id, answers),
        }

    def source_reference(self, paper_id):
        if paper_id == PAPER_RECALL:
            path = self.papers[2]["legacy_source_files"][0]["path"]
            return {"path": path}, file_sha256(self.root / path), []
        source_id = SOURCE_ONE if paper_id == PAPER_ONE else SOURCE_TWO
        digest = hashlib.sha256(source_id.encode("utf-8")).hexdigest()
        return {"source_id": source_id}, digest, [1, 2]

    def questions(self, paper_id, overrides=None):
        truth = self.truth(paper_id)
        source_ref, source_sha256, pages = self.source_reference(paper_id)
        records = []
        for number in sorted(truth["texts"]):
            record = {
                "question_id": question_id(paper_id, number),
                "printed_number": number,
                "source_ref": copy.deepcopy(source_ref),
                "source_sha256": source_sha256,
                "source_pages": list(pages),
                "question_text_sha256": truth["texts"][number],
                "answer_sha256": truth["answers"][number],
                "transcription_review": {
                    "role": ROLE_QUESTION, "result": "passed", "evidence": "逐字对读",
                },
                "answer_evidence": {"grade": "A", "evidence": "独立求解一致"},
                "solver_role": ROLE_SOLVER,
                "reviewer_role": ROLE_REVIEWER,
                "conflict_status": "none",
                "issue_ids": [],
            }
            record.update(copy.deepcopy((overrides or {}).get(number, {})))
            records.append(record)
        return records

    def document_for(self, paper_id, overrides=None):
        return new_provenance(paper_id, BATCH_ID, self.questions(paper_id, overrides))

    def install(self, paper_id, document=None):
        """把一份 provenance 直接落到工作树（绕过事务，供只读判定测试使用）。"""
        document = self.document_for(paper_id) if document is None else document
        relative = self.provenance_relative(paper_id)
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(canonical_json(document).encode("utf-8"))
        return relative

    # ------------------------------------------------------------ 角色文件

    def role_documents(self, paper_id, overrides=None):
        records = self.questions(paper_id, overrides)
        by_stage = {}
        by_stage["question-review"] = {
            "stage": "question-review",
            "role": ROLE_QUESTION,
            "batch_id": BATCH_ID,
            "paper_id": paper_id,
            "questions": [{
                "question_id": item["question_id"],
                "printed_number": item["printed_number"],
                "source_ref": item["source_ref"],
                "source_sha256": item["source_sha256"],
                "source_pages": item["source_pages"],
                "question_text_sha256": item["question_text_sha256"],
                "result": item["transcription_review"]["result"],
                "evidence": item["transcription_review"]["evidence"],
                "issue_ids": item["issue_ids"],
            } for item in records],
        }
        by_stage["answer-solve"] = {
            "stage": "answer-solve",
            "role": ROLE_SOLVER,
            "batch_id": BATCH_ID,
            "paper_id": paper_id,
            "questions": [{
                "question_id": item["question_id"],
                "printed_number": item["printed_number"],
                "answer_sha256": item["answer_sha256"],
                "grade": item["answer_evidence"]["grade"],
                "evidence": item["answer_evidence"]["evidence"],
                "issue_ids": item["issue_ids"],
            } for item in records],
        }
        by_stage["answer-review"] = {
            "stage": "answer-review",
            "role": ROLE_REVIEWER,
            "batch_id": BATCH_ID,
            "paper_id": paper_id,
            "questions": [{
                "question_id": item["question_id"],
                "printed_number": item["printed_number"],
                "answer_sha256": item["answer_sha256"],
                "conflict_status": item["conflict_status"],
                "issue_ids": item["issue_ids"],
            } for item in records],
        }
        return by_stage

    def fill_work(self, per_paper=None):
        """写满三角色 `.work` 文件；`per_paper[paper_id]` 是逐题覆盖表。"""
        if (self.work_dir / BATCH_ID).exists():
            shutil.rmtree(str(self.work_dir / BATCH_ID))
        init_batch(self.manifest_path, BATCH_ID, self.work_dir)
        for paper in self.papers:
            paper_id = paper["paper_id"]
            documents = self.role_documents(
                paper_id, (per_paper or {}).get(paper_id, {})
            )
            for stage, document in documents.items():
                path = provenance.work_paths(
                    self.work_dir, BATCH_ID, paper_id
                )[stage]
                path.write_bytes(canonical_json(document).encode("utf-8"))

    # ------------------------------------------------------------ 调用入口

    def loader(self, **overrides):
        return provenance.facts_loader(
            artifacts_state=lambda root, manifest, paper_id: overrides.get(
                "artifacts", "current"
            ),
            review_state=lambda root, manifest, paper_id: (
                overrides.get("review", "missing"),
                overrides.get("review_currency", "stale"),
            ),
            batch_report_valid=lambda root, manifest, paper_id: overrides.get(
                "batch_report_valid", False
            ),
        )

    def facts(self, paper_id, **overrides):
        loaded = self.loader(**overrides)(
            self.root, self.manifest(), [paper_id]
        )[paper_id]
        return status_core.paper_facts(
            paper_id,
            build=overrides.get("build", "succeeded"),
            build_currency=overrides.get("build_currency", "current"),
            **loaded
        )

    def cli(self, *argv):
        return provenance.main(list(argv), artifacts_state=lambda *_: "current")


# ================================================================ 哈希口径


class HashContractTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_question_text_digest_is_the_normalized_block_hash(self):
        blocks = parse_question_blocks(QUESTIONS_MD)
        digests = question_text_digests(QUESTIONS_MD)
        self.assertEqual(sorted(digests), [1, 2, 3])
        for block in blocks:
            expected = hashlib.sha256(
                provenance.question_block_text(block).encode("utf-8")
            ).hexdigest()
            self.assertEqual(digests[block.number], expected)

    def test_trailing_whitespace_and_crlf_do_not_change_the_question_digest(self):
        noisy = QUESTIONS_MD.replace("\n", "   \n").replace("\n", "\r\n")
        self.assertEqual(
            question_text_digests(noisy), question_text_digests(QUESTIONS_MD)
        )

    def test_editing_a_question_changes_only_that_digest(self):
        before = question_text_digests(QUESTIONS_MD)
        after = question_text_digests(QUESTIONS_MD.replace("求 $1+1$", "求 $2+2$"))
        self.assertEqual(before[1], after[1])
        self.assertNotEqual(before[2], after[2])
        self.assertEqual(before[3], after[3])

    def test_answer_digest_is_the_canonical_record_json_not_the_free_text(self):
        digests = answer_digests(PAPER_ONE, ANSWER_KEY_MD)
        records = [
            item for item in expected_answer_records(ANSWER_KEY_MD) if item.number == 3
        ]
        payload = {
            "question_id": question_id(PAPER_ONE, 3),
            "parts": sorted(
                ({"part": str(item.subpart), "answer": item.value} for item in records),
                key=lambda item: item["part"],
            ),
        }
        self.assertEqual(
            digests[3],
            hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest(),
        )
        # 自由文本直接取哈希是被明文禁止的口径，两者必须不同。
        self.assertNotEqual(
            digests[3], hashlib.sha256(ANSWER_KEY_MD.encode("utf-8")).hexdigest()
        )

    def test_a_whole_question_answer_uses_the_empty_part_key(self):
        digests = answer_digests(PAPER_ONE, ANSWER_KEY_MD)
        payload = {
            "question_id": question_id(PAPER_ONE, 1),
            "parts": [{"part": "", "answer": "A"}],
        }
        self.assertEqual(
            digests[1],
            hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest(),
        )

    def test_the_answer_digest_is_bound_to_the_paper(self):
        self.assertNotEqual(
            answer_digests(PAPER_ONE, ANSWER_KEY_MD)[1],
            answer_digests(PAPER_TWO, ANSWER_KEY_MD)[1],
        )

    def test_question_ids_are_derived_from_the_paper_and_printed_number(self):
        self.assertEqual(question_id(PAPER_ONE, 7), PAPER_ONE + "-q07")
        self.assertEqual(question_id(PAPER_ONE, 23), PAPER_ONE + "-q23")

    # ---- 文末页脚：末题摘要必须是题面的纯函数

    def test_the_last_question_digest_excludes_the_file_footer(self):
        """两份文件末题逐字相同、只有文末页脚不同 → 摘要必须相同。

        页脚（`---` + `> **原卷影印件**：…`）落在最后一题块的正文里，因为它后面没有
        下一题来接管。不剥掉它，末题的声明哈希就不是题面的纯函数——改一次页脚里的
        PDF 路径，整卷核验静默失效。
        """
        science = QUESTIONS_MD + FOOTER_TEMPLATE % "理"
        arts = QUESTIONS_MD + FOOTER_TEMPLATE % "文"
        self.assertNotEqual(science, arts)
        self.assertEqual(
            question_text_digests(science), question_text_digests(arts)
        )

    def test_stripping_the_footer_does_not_change_the_footerless_digest(self):
        """有页脚与无页脚必须同值——剥掉的是页脚，不是把末题换了个口径。"""
        self.assertEqual(
            question_text_digests(QUESTIONS_MD + FOOTER_TEMPLATE % "理"),
            question_text_digests(QUESTIONS_MD),
        )

    def test_an_edit_to_the_last_question_still_changes_its_digest(self):
        with_footer = QUESTIONS_MD + FOOTER_TEMPLATE % "理"
        edited = with_footer.replace("求 $f(2)$", "求 $f(3)$")
        self.assertNotEqual(
            question_text_digests(with_footer)[3], question_text_digests(edited)[3]
        )

    def test_a_thematic_break_followed_by_prose_is_not_a_footer(self):
        """页脚判据是「break 之后只剩引用块」；后面接正文的 `---` 一律不剥。"""
        base = QUESTIONS_MD + "\n---\n\n附注：本卷选做题二选一。\n"
        edited = base.replace("二选一", "三选一")
        self.assertNotEqual(
            question_text_digests(base)[3], question_text_digests(edited)[3]
        )

    def test_a_mid_document_thematic_break_is_never_stripped(self):
        """只有**最后一题**才可能带文末页脚；题间的 break + 引用块属于题面正文。"""
        base = QUESTIONS_MD.replace(
            "**2．** 求 $1+1$ 的值。",
            "---\n\n> 注：以下为第二部分。\n\n**2．** 求 $1+1$ 的值。",
        )
        edited = base.replace("第二部分", "第贰部分")
        self.assertNotEqual(
            question_text_digests(base)[1], question_text_digests(edited)[1]
        )


# ================================================================ 枚举与 Schema


class SchemaContractTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_the_enumerations_are_frozen(self):
        self.assertEqual(TRANSCRIPTION_RESULTS, ("passed", "failed", "uncertain"))
        self.assertEqual(ANSWER_GRADES, ("A", "B", "C", "D", "U"))
        self.assertEqual(CONFLICT_STATES, ("none", "resolved", "unresolved"))
        self.assertEqual(
            STAGES, ("question-review", "answer-solve", "answer-review")
        )

    def test_the_required_question_fields_are_frozen(self):
        document = self.fixture.document_for(PAPER_ONE)
        self.assertEqual(sorted(document["questions"][0]), sorted([
            "question_id", "printed_number", "source_ref", "source_sha256",
            "source_pages", "question_text_sha256", "answer_sha256",
            "transcription_review", "answer_evidence", "solver_role",
            "reviewer_role", "conflict_status", "issue_ids",
        ]))

    def test_a_value_outside_a_frozen_enum_is_rejected(self):
        for field, value in (
            ("transcription_review", {"role": ROLE_QUESTION, "result": "ok",
                                      "evidence": "x"}),
            ("answer_evidence", {"grade": "E", "evidence": "x"}),
            ("conflict_status", "pending"),
        ):
            with self.subTest(field=field):
                document = self.fixture.document_for(PAPER_ONE, {1: {field: value}})
                with self.assertRaises(ProvenanceError):
                    validate_provenance(
                        document, self.fixture.manifest(), self.fixture.root
                    )

    def test_an_unknown_question_field_is_rejected(self):
        document = self.fixture.document_for(PAPER_ONE)
        document["questions"][0]["reviewed_by"] = "某人"
        with self.assertRaises(ProvenanceError):
            validate_provenance(document, self.fixture.manifest(), self.fixture.root)

    def test_a_source_ref_may_not_mix_both_forms(self):
        document = self.fixture.document_for(PAPER_ONE)
        document["questions"][0]["source_ref"] = {
            "source_id": SOURCE_ONE, "path": "2099/x.md",
        }
        with self.assertRaises(ProvenanceError):
            validate_provenance(document, self.fixture.manifest(), self.fixture.root)

    def test_a_valid_document_passes(self):
        for paper_id in (PAPER_ONE, PAPER_TWO, PAPER_RECALL):
            with self.subTest(paper_id=paper_id):
                validate_provenance(
                    self.fixture.document_for(paper_id),
                    self.fixture.manifest(), self.fixture.root,
                )


# ================================================================ 四个假绿反例


class FalseGreenTests(unittest.TestCase):
    """有效 ≠ 属于本卷。四条反例逐条冻结，任何一条放行都是「看起来有来源」。"""

    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def reject(self, document, manifest=None):
        with self.assertRaises(ProvenanceError):
            validate_provenance(
                document, manifest or self.fixture.manifest(), self.fixture.root
            )

    def test_a_valid_source_belonging_to_another_paper_is_rejected(self):
        # SOURCE_TWO 本身 ready、artifact 当前、双向关系成立——但它是第二卷的。
        digest = hashlib.sha256(SOURCE_TWO.encode("utf-8")).hexdigest()
        self.reject(self.fixture.document_for(PAPER_ONE, {1: {
            "source_ref": {"source_id": SOURCE_TWO}, "source_sha256": digest,
        }}))

    def test_a_source_that_is_not_ready_is_rejected(self):
        document = self.fixture.document()
        for source in document["sources"]:
            if source["source_id"] == SOURCE_ONE:
                source["source_state"] = "blocked"
        atomic_write_json(self.fixture.manifest_path, document)
        self.reject(
            self.fixture.document_for(PAPER_ONE), self.fixture.manifest()
        )

    def test_page_numbers_outside_the_artifact_are_rejected(self):
        self.reject(self.fixture.document_for(PAPER_ONE, {1: {
            "source_pages": [1, 5],
        }}))

    def test_a_local_path_that_is_not_registered_for_this_paper_is_rejected(self):
        other = self.fixture.papers[0]["source_files"]["questions"]
        digest = file_sha256(self.fixture.root / other)
        self.reject(self.fixture.document_for(PAPER_RECALL, {1: {
            "source_ref": {"path": other}, "source_sha256": digest,
        }}))

    # ---- 同族的其余门禁

    def test_unsorted_or_duplicated_pages_are_rejected(self):
        for pages in ([2, 1], [1, 1], [0, 1]):
            with self.subTest(pages=pages):
                self.reject(self.fixture.document_for(
                    PAPER_ONE, {1: {"source_pages": pages}}
                ))

    def test_an_upstream_reference_needs_at_least_one_page(self):
        self.reject(self.fixture.document_for(PAPER_ONE, {1: {"source_pages": []}}))

    def test_a_local_path_is_refused_once_the_paper_has_an_upstream_source(self):
        path = self.fixture.papers[0]["source_files"]["questions"]
        digest = file_sha256(self.fixture.root / path)
        document = self.fixture.document()
        document["papers"][0]["legacy_source_files"] = [
            {"path": path, "sha256": digest}
        ]
        atomic_write_json(self.fixture.manifest_path, document)
        self.reject(
            self.fixture.document_for(PAPER_ONE, {1: {
                "source_ref": {"path": path}, "source_sha256": digest,
            }}),
            self.fixture.manifest(),
        )

    def test_a_recomputed_source_hash_mismatch_is_rejected(self):
        self.reject(self.fixture.document_for(PAPER_ONE, {1: {
            "source_sha256": "0" * 64,
        }}))

    def test_a_question_text_or_answer_hash_mismatch_is_rejected(self):
        for field in ("question_text_sha256", "answer_sha256"):
            with self.subTest(field=field):
                self.reject(self.fixture.document_for(
                    PAPER_ONE, {2: {field: "0" * 64}}
                ))

    def test_a_missing_or_extra_printed_number_is_rejected(self):
        document = self.fixture.document_for(PAPER_ONE)
        document["questions"] = document["questions"][:2]
        self.reject(document)
        document = self.fixture.document_for(PAPER_ONE)
        extra = copy.deepcopy(document["questions"][2])
        extra["printed_number"] = 4
        extra["question_id"] = question_id(PAPER_ONE, 4)
        document["questions"].append(extra)
        self.reject(document)

    def test_a_question_id_that_does_not_match_the_printed_number_is_rejected(self):
        self.reject(self.fixture.document_for(PAPER_ONE, {1: {
            "question_id": question_id(PAPER_ONE, 9),
        }}))

    def test_repeated_printed_number_uses_distinct_internal_question_order(self):
        paper = next(item for item in self.fixture.papers
                     if item["paper_id"] == PAPER_ONE)
        path = self.fixture.root / paper["source_files"]["questions"]
        text = path.read_text(encoding="utf-8").replace(
            "**2．**", "**2．**<!-- printed-label: 1 -->", 1
        )
        path.write_text(text, encoding="utf-8")
        document = self.fixture.document_for(PAPER_ONE)
        for record in document["questions"]:
            order = record["printed_number"]
            record["question_order"] = order
            record["printed_label"] = "1" if order == 2 else str(order)
            if order == 2:
                record["printed_number"] = 1
        validate_provenance(document, self.fixture.manifest(), self.fixture.root)

    def test_a_document_bound_to_the_wrong_batch_is_rejected(self):
        document = self.fixture.document_for(PAPER_ONE)
        document["batch_id"] = "phase0-b09"
        self.reject(document)


# ================================================================ 完成判定


class CompletionGateTests(unittest.TestCase):
    """真实 adapter 产出的 facts 喂进 Task 15 的状态核心，逐条守住 `complete`。"""

    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)
        self.fixture.install(PAPER_ONE)

    def test_a_complete_evidence_chain_reaches_complete(self):
        facts = self.fixture.facts(
            PAPER_ONE, review="passed", review_currency="current",
            batch_report_valid=True,
        )
        self.assertEqual(derive_status(facts), "complete")

    def test_a_failed_or_uncertain_transcription_never_completes(self):
        for result in ("failed", "uncertain"):
            with self.subTest(result=result):
                document = self.fixture.document_for(PAPER_ONE, {1: {
                    "transcription_review": {
                        "role": ROLE_QUESTION, "result": result, "evidence": "存疑",
                    },
                }})
                self.fixture.install(PAPER_ONE, document)
                facts = self.fixture.facts(
                    PAPER_ONE, review="passed", review_currency="current",
                    batch_report_valid=True,
                )
                self.assertTrue(facts["provenance_unknown"])
                self.assertNotEqual(derive_status(facts), "complete")

    def test_a_u_grade_never_completes(self):
        self.fixture.install(PAPER_ONE, self.fixture.document_for(PAPER_ONE, {2: {
            "answer_evidence": {"grade": "U", "evidence": "无法定级"},
        }}))
        facts = self.fixture.facts(
            PAPER_ONE, review="passed", review_currency="current",
            batch_report_valid=True,
        )
        self.assertTrue(facts["provenance_unknown"])
        self.assertNotEqual(derive_status(facts), "complete")

    def test_an_unresolved_conflict_never_completes(self):
        self.fixture.install(PAPER_ONE, self.fixture.document_for(PAPER_ONE, {3: {
            "conflict_status": "unresolved",
        }}))
        facts = self.fixture.facts(
            PAPER_ONE, review="passed", review_currency="current",
            batch_report_valid=True,
        )
        self.assertTrue(facts["provenance_conflicts"])
        self.assertNotEqual(derive_status(facts), "complete")

    def test_a_resolved_conflict_still_completes(self):
        self.fixture.install(PAPER_ONE, self.fixture.document_for(PAPER_ONE, {3: {
            "conflict_status": "resolved",
        }}))
        facts = self.fixture.facts(
            PAPER_ONE, review="passed", review_currency="current",
            batch_report_valid=True,
        )
        self.assertEqual(derive_status(facts), "complete")

    def test_two_identical_roles_make_the_provenance_invalid(self):
        for override in (
            {"solver_role": ROLE_REVIEWER},
            {"reviewer_role": ROLE_QUESTION},
            {"transcription_review": {
                "role": ROLE_SOLVER, "result": "passed", "evidence": "逐字对读",
            }},
        ):
            with self.subTest(override=sorted(override)):
                document = self.fixture.document_for(PAPER_ONE, {1: override})
                with self.assertRaises(ProvenanceError):
                    validate_provenance(
                        document, self.fixture.manifest(), self.fixture.root
                    )
                self.fixture.install(PAPER_ONE, document)
                facts = self.fixture.facts(
                    PAPER_ONE, review="passed", review_currency="current",
                    batch_report_valid=True,
                )
                self.assertEqual(facts["provenance"], "invalid")
                self.assertEqual(derive_status(facts), "legacy_unverified")

    def test_a_pending_or_failed_review_never_completes(self):
        for review in ("missing", "pending", "failed"):
            with self.subTest(review=review):
                facts = self.fixture.facts(
                    PAPER_ONE, review=review, review_currency="current",
                    batch_report_valid=True,
                )
                self.assertNotEqual(derive_status(facts), "complete")

    def test_an_unfinished_issue_never_completes(self):
        for state in ("open", "investigating", "deferred"):
            with self.subTest(state=state):
                issues_module.upsert_issue(self.fixture.issues_path, {
                    "paper_id": PAPER_ONE,
                    "affected_paper_ids": [],
                    "type": "transcription-ambiguous",
                    "status": state,
                    "impact": "blocks_completion",
                    "question_id": question_id(PAPER_ONE, 1),
                    "source_id": SOURCE_ONE,
                    "resume_action": "回到原卷复核第 1 题",
                })
                facts = self.fixture.facts(
                    PAPER_ONE, review="passed", review_currency="current",
                    batch_report_valid=True,
                )
                self.assertEqual(derive_status(facts), "blocked")

    def test_the_recall_identity_blocker_keeps_blocking_complete(self):
        self.fixture.install(PAPER_RECALL)
        facts = self.fixture.facts(
            PAPER_RECALL, review="passed", review_currency="current",
            batch_report_valid=True,
        )
        self.assertEqual(derive_status(facts), "blocked")

    def test_a_missing_provenance_stays_legacy_unverified(self):
        facts = self.fixture.facts(
            PAPER_TWO, review="passed", review_currency="current",
            batch_report_valid=True,
        )
        self.assertEqual(facts["provenance"], "missing")
        self.assertEqual(derive_status(facts), "legacy_unverified")

    def test_a_new_paper_without_provenance_stays_planned(self):
        manifest = self.fixture.manifest()
        paper = next(
            item for item in manifest["papers"] if item["paper_id"] == PAPER_TWO
        )
        paper["legacy_ids"] = []

        loaded = provenance.load_provenance_facts(
            self.fixture.root, manifest, [PAPER_TWO]
        )
        facts = status_core.paper_facts(PAPER_TWO, **loaded[PAPER_TWO])

        self.assertEqual(facts["provenance"], "missing")
        self.assertEqual(derive_status(facts), "planned")

    def test_editing_the_canonical_source_makes_the_provenance_stale(self):
        paper = self.fixture.papers[0]
        self.fixture.write(
            paper["source_files"]["questions"],
            QUESTIONS_MD.replace("求 $1+1$", "求 $3+3$"),
        )
        facts = self.fixture.facts(PAPER_ONE)
        self.assertEqual(facts["provenance"], "stale")
        self.assertEqual(derive_status(facts), "legacy_unverified")

    def test_the_loader_returns_exactly_the_fields_the_status_core_expects(self):
        loaded = self.fixture.loader()(
            self.fixture.root, self.fixture.manifest(), [PAPER_ONE]
        )
        self.assertEqual(sorted(loaded[PAPER_ONE]), sorted([
            "is_legacy", "provenance", "provenance_unknown", "provenance_conflicts",
            "artifacts", "review", "review_currency", "issues", "batch_report_valid",
        ]))

    def test_the_loader_never_reports_a_valid_batch_report_on_its_own(self):
        loaded = load_provenance_facts(
            self.fixture.root, self.fixture.manifest(), [PAPER_ONE]
        )
        self.assertFalse(loaded[PAPER_ONE]["batch_report_valid"])

    def test_the_adapter_does_not_own_any_status_rule(self):
        source = (ROOT / "tools" / "provenance.py").read_text(encoding="utf-8")
        for forbidden in ("def derive_status", "def reconcile_batch_status"):
            self.assertNotIn(forbidden, source)


# ================================================================ init-batch


class InitBatchTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_it_creates_three_exclusive_paths_per_paper(self):
        report = init_batch(
            self.fixture.manifest_path, BATCH_ID, self.fixture.work_dir
        )
        created = sorted(report["created"])
        expected = sorted(
            "%s/%s/provenance/%s/%s.json" % (
                WORK_RELATIVE, BATCH_ID, stage, paper["paper_id"]
            )
            for paper in self.fixture.papers for stage in STAGES
        )
        self.assertEqual(created, expected)
        self.assertEqual(len(set(created)), 9)
        for relative in created:
            self.assertTrue((self.fixture.root / relative).is_file())

    def test_it_seeds_the_original_label_separately_from_internal_order(self):
        paper = next(item for item in self.fixture.papers
                     if item["paper_id"] == PAPER_ONE)
        questions_path = self.fixture.root / paper["source_files"]["questions"]
        text = questions_path.read_text(encoding="utf-8").replace(
            "**2．**", "**2．**<!-- printed-label: 一 -->", 1
        )
        questions_path.write_text(text, encoding="utf-8")

        init_batch(self.fixture.manifest_path, BATCH_ID, self.fixture.work_dir)
        for stage in STAGES:
            role_path = provenance.work_paths(
                self.fixture.work_dir, BATCH_ID, PAPER_ONE
            )[stage]
            document = json.loads(role_path.read_text(encoding="utf-8"))
            second = document["questions"][1]
            self.assertEqual(second["question_order"], 2)
            self.assertEqual(second["printed_label"], "一")
            self.assertEqual(second["printed_number"], "一")

    def test_it_writes_nothing_tracked(self):
        before = self.fixture.snapshot()
        init_batch(self.fixture.manifest_path, BATCH_ID, self.fixture.work_dir)
        after = self.fixture.snapshot()
        added = sorted(set(after) - set(before))
        self.assertTrue(added)
        for relative in added:
            self.assertTrue(relative.startswith(WORK_RELATIVE + "/"), relative)
        self.assertEqual(
            {key: before[key] for key in before},
            {key: after[key] for key in before},
        )

    def test_the_answer_review_skeleton_carries_no_answer_from_the_solver(self):
        init_batch(self.fixture.manifest_path, BATCH_ID, self.fixture.work_dir)
        paths = provenance.work_paths(self.fixture.work_dir, BATCH_ID, PAPER_ONE)
        blind = json.loads(paths["answer-review"].read_text(encoding="utf-8"))
        for record in blind["questions"]:
            self.assertIsNone(record["answer_sha256"])
            self.assertIsNone(record["conflict_status"])

    def test_a_work_dir_outside_the_ignored_work_tree_is_refused(self):
        for candidate in (
            self.fixture.root / PROJECT_RELATIVE / "reports",
            self.fixture.root / "elsewhere",
            self.fixture.root / WORK_RELATIVE / ".." / "2099_全国1卷",
        ):
            with self.subTest(candidate=str(candidate)):
                with self.assertRaises(ProvenanceError):
                    init_batch(self.fixture.manifest_path, BATCH_ID, candidate)

    def test_it_refuses_to_clobber_an_existing_role_file(self):
        init_batch(self.fixture.manifest_path, BATCH_ID, self.fixture.work_dir)
        paths = provenance.work_paths(self.fixture.work_dir, BATCH_ID, PAPER_ONE)
        paths["answer-solve"].write_text("{}", encoding="utf-8")
        with self.assertRaises(ProvenanceError):
            init_batch(self.fixture.manifest_path, BATCH_ID, self.fixture.work_dir)

    def test_an_unknown_batch_fails_closed(self):
        with self.assertRaises(ProvenanceError):
            init_batch(self.fixture.manifest_path, "phase0-b99", self.fixture.work_dir)


# ================================================================ import-batch


class ImportBatchTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def do_import(self, write=True, **kwargs):
        return import_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            self.fixture.work_dir, write=write,
            artifacts_state=lambda *_: "current", **kwargs
        )

    def test_a_clean_batch_imports_in_one_state_transaction(self):
        self.fixture.fill_work()
        before = self.fixture.manifest()["revision"]
        report = self.do_import()
        self.assertEqual(report["code"], "OK")
        manifest = self.fixture.manifest()
        self.assertEqual(manifest["revision"], before + 1)
        for paper in self.fixture.papers:
            relative = self.fixture.provenance_relative(paper["paper_id"])
            self.assertTrue((self.fixture.root / relative).is_file())
        batch = next(
            item for item in manifest["batches"] if item["batch_id"] == BATCH_ID
        )
        self.assertEqual(batch["status"], "provenance_verified")
        self.assertEqual(
            batch["status"],
            reconcile_batch_status({
                paper["paper_id"]: self.fixture.facts(
                    paper["paper_id"], build="missing", build_currency="stale"
                )
                for paper in self.fixture.papers
            }),
        )

    def test_a_dry_run_writes_nothing(self):
        self.fixture.fill_work()
        before = self.fixture.snapshot()
        self.do_import(write=False)
        self.assertEqual(self.fixture.snapshot(), before)

    def test_the_transaction_leaves_no_journal_behind(self):
        self.fixture.fill_work()
        self.do_import()
        journals = list(
            (self.fixture.root / TRANSACTIONS_RELATIVE).glob("*/journal.json")
        )
        self.assertEqual(journals, [])

    def test_a_missing_role_file_aborts_the_whole_batch(self):
        self.fixture.fill_work()
        provenance.work_paths(
            self.fixture.work_dir, BATCH_ID, PAPER_TWO
        )["answer-review"].unlink()
        before = self.fixture.snapshot()
        with self.assertRaises(ProvenanceError):
            self.do_import()
        self.assertEqual(self.fixture.snapshot(), before)

    def test_an_extra_paper_in_the_work_tree_aborts(self):
        self.fixture.fill_work()
        stray = self.fixture.work_dir / BATCH_ID / "provenance" / "answer-solve" / (
            "gk-2099-regular-national-9.json"
        )
        stray.write_text("{}", encoding="utf-8")
        with self.assertRaises(ProvenanceError):
            self.do_import()

    def test_question_numbers_must_agree_across_the_three_roles(self):
        self.fixture.fill_work()
        path = provenance.work_paths(
            self.fixture.work_dir, BATCH_ID, PAPER_ONE
        )["answer-solve"]
        document = json.loads(path.read_text(encoding="utf-8"))
        document["questions"] = document["questions"][:2]
        path.write_bytes(canonical_json(document).encode("utf-8"))
        with self.assertRaises(ProvenanceError):
            self.do_import()

    def test_two_roles_may_not_share_an_identity(self):
        self.fixture.fill_work()
        path = provenance.work_paths(
            self.fixture.work_dir, BATCH_ID, PAPER_ONE
        )["answer-review"]
        document = json.loads(path.read_text(encoding="utf-8"))
        document["role"] = ROLE_SOLVER
        path.write_bytes(canonical_json(document).encode("utf-8"))
        with self.assertRaises(ProvenanceError):
            self.do_import()

    def test_a_declared_hash_that_disagrees_with_the_tracked_source_aborts(self):
        self.fixture.fill_work()
        path = provenance.work_paths(
            self.fixture.work_dir, BATCH_ID, PAPER_ONE
        )["question-review"]
        document = json.loads(path.read_text(encoding="utf-8"))
        document["questions"][0]["question_text_sha256"] = "0" * 64
        path.write_bytes(canonical_json(document).encode("utf-8"))
        with self.assertRaises(ProvenanceError):
            self.do_import()

    def test_an_unknown_defect_without_a_current_issue_is_refused(self):
        for override in (
            {"transcription_review": {
                "role": ROLE_QUESTION, "result": "uncertain", "evidence": "字迹不清",
            }},
            {"answer_evidence": {"grade": "U", "evidence": "无法定级"}},
            {"conflict_status": "unresolved"},
        ):
            with self.subTest(override=sorted(override)):
                self.fixture.fill_work({PAPER_ONE: {1: override}})
                with self.assertRaises(ProvenanceError):
                    self.do_import()
                shutil.rmtree(str(self.fixture.work_dir))

    def test_a_declared_defect_with_a_matching_blocker_imports(self):
        issue_id = issues_module.upsert_issue(self.fixture.issues_path, {
            "paper_id": PAPER_ONE,
            "affected_paper_ids": [],
            "type": "answer-conflict",
            "status": "open",
            "impact": "blocks_completion",
            "question_id": question_id(PAPER_ONE, 1),
            "source_id": SOURCE_ONE,
            "resume_action": "回到原卷仲裁第 1 题的两份答案",
        })
        self.fixture.fill_work({PAPER_ONE: {1: {
            "conflict_status": "unresolved", "issue_ids": [issue_id],
        }}})
        report = self.do_import()
        self.assertEqual(report["code"], "OK")
        document = json.loads(
            (self.fixture.root / self.fixture.provenance_relative(PAPER_ONE))
            .read_text(encoding="utf-8")
        )
        self.assertEqual(document["questions"][0]["issue_ids"], [issue_id])
        facts = self.fixture.facts(PAPER_ONE)
        self.assertTrue(facts["provenance_conflicts"])
        self.assertEqual(derive_status(facts), "blocked")

    def test_an_issue_of_the_wrong_kind_does_not_satisfy_the_linkage(self):
        issue_id = issues_module.upsert_issue(self.fixture.issues_path, {
            "paper_id": PAPER_ONE,
            "affected_paper_ids": [],
            "type": "transcription-ambiguous",
            "status": "open",
            "impact": "blocks_completion",
            "question_id": question_id(PAPER_ONE, 1),
            "source_id": SOURCE_ONE,
            "resume_action": "回到原卷复核第 1 题",
        })
        self.fixture.fill_work({PAPER_ONE: {1: {
            "conflict_status": "unresolved", "issue_ids": [issue_id],
        }}})
        with self.assertRaises(ProvenanceError):
            self.do_import()

    def test_a_resolved_issue_does_not_satisfy_the_linkage(self):
        issue = {
            "paper_id": PAPER_ONE,
            "affected_paper_ids": [],
            "type": "answer-conflict",
            "status": "resolved",
            "impact": "blocks_completion",
            "question_id": question_id(PAPER_ONE, 1),
            "source_id": SOURCE_ONE,
            "resume_action": "已仲裁",
        }
        issue_id = issues_module.upsert_issue(self.fixture.issues_path, issue)
        self.fixture.fill_work({PAPER_ONE: {1: {
            "conflict_status": "unresolved", "issue_ids": [issue_id],
        }}})
        with self.assertRaises(ProvenanceError):
            self.do_import()

    def test_importing_twice_is_idempotent_on_the_provenance_bytes(self):
        self.fixture.fill_work()
        self.do_import()
        first = self.fixture.read_bytes(self.fixture.provenance_relative(PAPER_ONE))
        self.do_import()
        self.assertEqual(
            self.fixture.read_bytes(self.fixture.provenance_relative(PAPER_ONE)),
            first,
        )


# ================================================================ confirm-source


class SimulatedCrash(RuntimeError):
    pass


class ConfirmSourceTests(unittest.TestCase):
    """建立 source↔paper 绑定。**每条 fail-closed 守卫一个测试。**

    起点就是 T17 遇到的真实形状：卷的 `source_ids` 空、source 未绑定，两条 source_ref
    通道都还不通。绑定属批次导入期产出，故守卫必须全部前置——绑错一次没有 unbind
    可退（错误绑定是升级事项，不造无人要求的能力）。
    """

    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)
        self.fixture.unbind(SOURCE_ONE)

    def confirm(self, paper_id=PAPER_ONE, source_id=SOURCE_ONE, write=False, **kw):
        return provenance.confirm_source(
            self.fixture.manifest_path, self.fixture.issues_path,
            paper_id, source_id, write=write, **kw
        )

    def source(self, source_id=SOURCE_ONE, manifest=None):
        manifest = manifest or self.fixture.manifest()
        return next(
            item for item in manifest["sources"] if item["source_id"] == source_id
        )

    def paper(self, paper_id=PAPER_ONE, manifest=None):
        manifest = manifest or self.fixture.manifest()
        return next(
            item for item in manifest["papers"] if item["paper_id"] == paper_id
        )

    def refuse(self, **kw):
        before = self.fixture.snapshot()
        with self.assertRaises(ProvenanceError) as caught:
            self.confirm(write=True, **kw)
        self.assertEqual(self.fixture.snapshot(), before)
        return caught.exception

    # ---- 正路

    def test_a_dry_run_reports_the_binding_and_writes_nothing(self):
        before = self.fixture.snapshot()
        report = self.confirm()
        self.assertEqual(report["code"], "OK")
        self.assertFalse(report["written"])
        self.assertEqual(report["paper_id"], PAPER_ONE)
        self.assertEqual(report["source_id"], SOURCE_ONE)
        self.assertEqual(report["paper_relation"], "canonical")
        self.assertEqual(report["source_ids"], [SOURCE_ONE])
        self.assertEqual(self.fixture.snapshot(), before)

    def test_write_binds_both_directions_in_one_state_transaction(self):
        revision = self.fixture.manifest()["revision"]
        report = self.confirm(write=True)
        self.assertTrue(report["written"])
        manifest = self.fixture.manifest()
        self.assertEqual(manifest["revision"], revision + 1)
        self.assertEqual(report["revision"], revision + 1)
        self.assertEqual(self.source(manifest=manifest)["paper_id"], PAPER_ONE)
        self.assertEqual(
            self.source(manifest=manifest)["paper_relation"], "canonical"
        )
        self.assertEqual(self.paper(manifest=manifest)["source_ids"], [SOURCE_ONE])
        self.assertEqual(
            list((self.fixture.root / TRANSACTIONS_RELATIVE).glob("*/journal.json")),
            [],
        )

    def test_the_bound_manifest_passes_full_validation(self):
        self.confirm(write=True)
        # load_manifest 只跑 Schema + manifest 语义；来源/试卷两层语义要另外过一遍。
        source_manifest.validate_manifest_document(
            self.fixture.manifest_path, self.fixture.manifest()
        )

    def test_source_ids_stay_sorted(self):
        self.fixture.unbind(SOURCE_TWO)
        self.confirm(source_id=SOURCE_TWO, write=True)
        self.confirm(source_id=SOURCE_ONE, write=True)
        self.assertEqual(
            self.paper()["source_ids"], sorted([SOURCE_ONE, SOURCE_TWO])
        )

    def test_binding_does_not_move_any_cached_state(self):
        self.confirm(write=True)
        report = check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, None,
            artifacts_state=lambda *_: "current",
        )
        self.assertEqual(report["problems"], [])
        self.assertEqual(self.paper()["production_state"], "legacy_unverified")

    # ---- 守卫 ①：source 必须存在且 ready

    def test_an_unknown_source_is_refused(self):
        self.refuse(source_id="src-" + "9" * 64)

    def test_a_source_that_is_not_ready_is_refused(self):
        self.fixture.rewrite_manifest(lambda document: [
            source.update(source_state="blocked")
            for source in document["sources"]
            if source["source_id"] == SOURCE_ONE
        ])
        self.refuse()

    # ---- 守卫 ②：source 必须未绑定（含绑到本卷）

    def test_an_already_bound_source_is_refused(self):
        self.refuse(source_id=SOURCE_TWO)

    def test_rebinding_a_source_to_its_own_paper_is_refused_not_idempotent(self):
        """已绑定就是已绑定：静默幂等会把「绑错了」伪装成「本来就这样」。"""
        self.refuse(paper_id=PAPER_TWO, source_id=SOURCE_TWO)

    def test_a_half_bound_source_is_refused(self):
        """只有 paper_id、没有 paper_relation：manifest 载得进来，必须由守卫②拦下。"""
        self.fixture.rewrite_manifest(lambda document: [
            source.update(paper_id=PAPER_ONE)
            for source in document["sources"]
            if source["source_id"] == SOURCE_ONE
        ])
        self.refuse()

    def test_the_other_half_bound_shape_never_loads_at_all(self):
        """只有 paper_relation、没有 paper_id：manifest 语义层更早一步就拒收。

        守卫②在这一格是第二道防线而不是唯一防线——记下来是为了让后人知道，改动
        `validate_manifest_semantics` 并不会把这一格放出去。
        """
        before = self.fixture.snapshot()
        self.fixture.rewrite_manifest(lambda document: [
            source.update(paper_relation="canonical")
            for source in document["sources"]
            if source["source_id"] == SOURCE_ONE
        ])
        with self.assertRaisesRegex(ValueError, "paper_relation 存在但 paper_id 为空"):
            self.confirm(write=True)
        self.assertEqual(
            {key: value for key, value in self.fixture.snapshot().items()
             if key != MANIFEST_TARGET},
            {key: value for key, value in before.items() if key != MANIFEST_TARGET},
        )

    # ---- 守卫 ③：paper 必须存在

    def test_an_unknown_paper_is_refused(self):
        self.refuse(paper_id="gk-2099-regular-national-9")

    # ---- 守卫 ④：identity-ambiguous blocker 一律拒绝绑定

    def test_an_open_identity_issue_refuses_the_binding(self):
        """ISSUE-0001 那条纪律在此变成机器强制：回忆版不得自动绑定正式卷。"""
        self.fixture.unbind(SOURCE_ONE)
        self.refuse(paper_id=PAPER_RECALL)

    def test_the_unfinished_states_are_the_complement_of_resolved(self):
        """判据是**取反**而不是白名单：issues 的状态全集将来加一个新值，这条一票否决
        的守卫必须默认拒绝，而不是默认放行。"""
        self.assertEqual(
            set(provenance.UNFINISHED_ISSUE_STATES),
            issues_module.STATUSES - {"resolved"},
        )

    def test_a_status_outside_todays_enum_still_blocks(self):
        """直接喂一个当前枚举里没有的状态：白名单实现会放行，取反实现会拒绝。"""
        record = {
            "issue_id": "ISSUE-9001",
            "paper_id": PAPER_ONE,
            "affected_paper_ids": [],
            "type": "identity-ambiguous",
            "status": "wontfix",
            "impact": "non_blocking",
            "resume_action": "占位",
        }
        self.assertEqual(
            provenance._identity_blockers([record], PAPER_ONE), ["ISSUE-9001"]
        )
        record["status"] = "resolved"
        self.assertEqual(provenance._identity_blockers([record], PAPER_ONE), [])

    def test_every_unfinished_identity_issue_state_refuses_the_binding(self):
        for state in sorted(issues_module.STATUSES - {"resolved"}):
            with self.subTest(state=state):
                issues_module.upsert_issue(self.fixture.issues_path, {
                    "paper_id": PAPER_ONE,
                    "affected_paper_ids": [],
                    "type": "identity-ambiguous",
                    "status": state,
                    "impact": "blocks_completion",
                    "resume_action": "逐卷核验规范源地区与固定上游路径",
                    "conflict_code": "regions-vs-upstream-path",
                })
                self.refuse()

    def test_a_shared_identity_issue_blocks_through_affected_paper_ids(self):
        issues_module.upsert_issue(self.fixture.issues_path, {
            "paper_id": None,
            "affected_paper_ids": sorted([PAPER_ONE, PAPER_TWO]),
            "type": "identity-ambiguous",
            "status": "open",
            "impact": "blocks_completion",
            "resume_action": "两卷同源，须先分清哪一卷对应哪条上游路径",
            "conflict_code": "regions-vs-upstream-path",
        })
        self.refuse()

    def test_a_resolved_identity_issue_no_longer_refuses(self):
        issue = {
            "paper_id": PAPER_ONE,
            "affected_paper_ids": [],
            "type": "identity-ambiguous",
            "status": "resolved",
            "impact": "blocks_completion",
            "resume_action": "已人工核验身份",
            "conflict_code": "regions-vs-upstream-path",
        }
        issues_module.upsert_issue(self.fixture.issues_path, issue)
        self.assertTrue(self.confirm(write=True)["written"])

    def test_a_non_identity_issue_does_not_refuse(self):
        issues_module.upsert_issue(self.fixture.issues_path, {
            "paper_id": PAPER_ONE,
            "affected_paper_ids": [],
            "type": "transcription-ambiguous",
            "status": "open",
            "impact": "blocks_completion",
            "question_id": question_id(PAPER_ONE, 1),
            "source_id": SOURCE_ONE,
            "resume_action": "回到原卷复核第 1 题",
        })
        self.assertTrue(self.confirm(write=True)["written"])

    # ---- 守卫 ⑤：绑定后的来源语义必须自洽

    def test_a_binding_that_would_break_source_semantics_is_refused(self):
        """ready 但 artifact 为空：Schema 与 manifest 语义都放行，只有 ⑤ 拦得住。"""
        self.fixture.rewrite_manifest(lambda document: [
            source.update(artifact=None)
            for source in document["sources"]
            if source["source_id"] == SOURCE_ONE
        ])
        self.refuse()

    # ---- 崩溃恢复

    def test_a_crash_after_the_journal_is_prepared_leaves_no_half_commit(self):
        def hook(event, path):
            if event == "journal_prepared":
                raise SimulatedCrash("模拟崩溃")

        before = self.fixture.read_bytes(MANIFEST_TARGET)
        with self.assertRaises(SimulatedCrash):
            self.confirm(write=True, event_hook=hook)
        self.assertEqual(self.fixture.read_bytes(MANIFEST_TARGET), before)
        pending = sorted(
            (self.fixture.root / TRANSACTIONS_RELATIVE).glob("*/journal.json")
        )
        self.assertEqual(len(pending), 1)

        self.assertEqual(len(recover_transactions(self.fixture.root)), 1)
        self.assertEqual(self.source()["paper_id"], PAPER_ONE)
        self.assertEqual(self.paper()["source_ids"], [SOURCE_ONE])

    # ---- CLI

    def test_the_cli_round_trips(self):
        arguments = [
            "confirm-source", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path),
            "--paper", PAPER_ONE, "--source", SOURCE_ONE,
        ]
        self.assertEqual(self.fixture.cli(*arguments), EXIT_OK)
        self.assertIsNone(self.source()["paper_id"])
        self.assertEqual(self.fixture.cli(*(arguments + ["--write"])), EXIT_OK)
        self.assertEqual(self.source()["paper_id"], PAPER_ONE)
        # 再来一次：已绑定，退出码 4 而不是静默成功。
        self.assertEqual(self.fixture.cli(*(arguments + ["--write"])), EXIT_INVALID)

    def test_all_four_options_are_required(self):
        full = {
            "--manifest": str(self.fixture.manifest_path),
            "--issues": str(self.fixture.issues_path),
            "--paper": PAPER_ONE,
            "--source": SOURCE_ONE,
        }
        for dropped in ("--issues", "--paper", "--source"):
            with self.subTest(dropped=dropped):
                argv = ["confirm-source"]
                for key, value in full.items():
                    if key != dropped:
                        argv += [key, value]
                with self.assertRaises(SystemExit) as caught:
                    self.fixture.cli(*argv)
                self.assertEqual(caught.exception.code, EXIT_USAGE)

    def test_there_is_no_unbind_subcommand(self):
        """错误绑定属升级事项；不造无人要求的能力。"""
        with self.assertRaises(SystemExit) as caught:
            self.fixture.cli(
                "unbind-source", "--manifest", str(self.fixture.manifest_path),
                "--paper", PAPER_ONE, "--source", SOURCE_ONE,
            )
        self.assertEqual(caught.exception.code, EXIT_USAGE)


# ================================================================ 只读核对


class ReadOnlyCheckTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_check_batch_passes_right_after_import(self):
        self.fixture.fill_work()
        import_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            self.fixture.work_dir, write=True, artifacts_state=lambda *_: "current",
        )
        report = check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            artifacts_state=lambda *_: "current",
        )
        self.assertEqual(report["problems"], [])
        self.assertEqual(report["code"], "OK")

    def test_check_batch_rejects_a_cached_state_that_drifted(self):
        self.fixture.fill_work()
        import_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            self.fixture.work_dir, write=True, artifacts_state=lambda *_: "current",
        )
        document = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        document["papers"][0]["production_state"] = "complete"
        atomic_write_json(self.fixture.manifest_path, document)
        report = check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            artifacts_state=lambda *_: "current",
        )
        self.assertEqual(report["code"], "INVALID")
        self.assertTrue(report["problems"])

    def test_check_batch_rejects_an_edited_canonical_source(self):
        self.fixture.fill_work()
        import_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            self.fixture.work_dir, write=True, artifacts_state=lambda *_: "current",
        )
        paper = self.fixture.papers[0]
        self.fixture.write(
            paper["source_files"]["answer_key"],
            ANSWER_KEY_MD.replace("**答案：A**", "**答案：B**"),
        )
        report = check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            artifacts_state=lambda *_: "current",
        )
        self.assertEqual(report["code"], "INVALID")

    def test_check_all_on_a_fresh_repository_is_consistent(self):
        report = check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, None,
            artifacts_state=lambda *_: "current",
        )
        self.assertEqual(report["problems"], [])
        self.assertEqual(report["papers"], 3)

    def test_check_writes_nothing(self):
        self.fixture.fill_work()
        import_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            self.fixture.work_dir, write=True, artifacts_state=lambda *_: "current",
        )
        before = self.fixture.snapshot()
        check_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            artifacts_state=lambda *_: "current",
        )
        self.assertEqual(self.fixture.snapshot(), before)


# ================================================================ CLI 契约


class CliTests(unittest.TestCase):
    def setUp(self):
        self.fixture = ProvenanceFixture()
        self.addCleanup(self.fixture.cleanup)

    def test_init_batch_and_import_batch_round_trip(self):
        self.assertEqual(self.fixture.cli(
            "init-batch", "--manifest", str(self.fixture.manifest_path),
            "--batch", BATCH_ID, "--work-dir", str(self.fixture.work_dir),
        ), EXIT_OK)
        for paper in self.fixture.papers:
            documents = self.fixture.role_documents(paper["paper_id"])
            for stage, document in documents.items():
                provenance.work_paths(
                    self.fixture.work_dir, BATCH_ID, paper["paper_id"]
                )[stage].write_bytes(canonical_json(document).encode("utf-8"))
        self.assertEqual(self.fixture.cli(
            "import-batch", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
            "--work-dir", str(self.fixture.work_dir), "--write",
        ), EXIT_OK)
        self.assertEqual(self.fixture.cli(
            "check-batch", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
        ), EXIT_OK)
        self.assertEqual(self.fixture.cli(
            "check-all", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path),
        ), EXIT_OK)

    def test_check_batch_exits_invalid_when_the_cache_drifted(self):
        document = json.loads(self.fixture.manifest_path.read_text(encoding="utf-8"))
        document["papers"][0]["production_state"] = "complete"
        atomic_write_json(self.fixture.manifest_path, document)
        self.assertEqual(self.fixture.cli(
            "check-all", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path),
        ), EXIT_INVALID)

    def test_only_import_accepts_write(self):
        for command, extra in (
            ("init-batch", ["--batch", BATCH_ID,
                            "--work-dir", str(self.fixture.work_dir)]),
            ("check-batch", ["--issues", str(self.fixture.issues_path),
                             "--batch", BATCH_ID]),
            ("check-all", ["--issues", str(self.fixture.issues_path)]),
            ("status", ["--issues", str(self.fixture.issues_path)]),
        ):
            with self.subTest(command=command):
                with self.assertRaises(SystemExit) as caught:
                    self.fixture.cli(
                        command, "--manifest", str(self.fixture.manifest_path),
                        *(extra + ["--write"])
                    )
                self.assertEqual(caught.exception.code, EXIT_USAGE)

    def test_only_batch_scoped_commands_accept_a_selector(self):
        with self.assertRaises(SystemExit) as caught:
            self.fixture.cli(
                "check-all", "--manifest", str(self.fixture.manifest_path),
                "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
            )
        self.assertEqual(caught.exception.code, EXIT_USAGE)

    def test_status_reports_the_derived_state(self):
        self.assertEqual(self.fixture.cli(
            "status", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
        ), EXIT_OK)

    def test_status_can_require_a_git_state(self):
        self.assertEqual(self.fixture.cli(
            "status", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
            "--require-git-state", "committed",
        ), EXIT_INVALID)
        self.fixture.fill_work()
        import_batch(
            self.fixture.manifest_path, self.fixture.issues_path, BATCH_ID,
            self.fixture.work_dir, write=True, artifacts_state=lambda *_: "current",
        )
        self.assertEqual(self.fixture.cli(
            "status", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
            "--require-git-state", "validated",
        ), EXIT_OK)
        self.fixture.commit_all("provenance")
        self.assertEqual(self.fixture.cli(
            "status", "--manifest", str(self.fixture.manifest_path),
            "--issues", str(self.fixture.issues_path), "--batch", BATCH_ID,
            "--require-git-state", "committed",
        ), EXIT_OK)

    def test_a_manifest_outside_the_canonical_path_is_refused(self):
        stray = self.fixture.root / PROJECT_RELATIVE / "reports" / "copy.json"
        stray.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.fixture.manifest_path, stray)
        self.assertEqual(self.fixture.cli(
            "check-all", "--manifest", str(stray),
            "--issues", str(self.fixture.issues_path),
        ), EXIT_INVALID)


# ================================================================ 真库自检


class LiveRepositoryTests(unittest.TestCase):
    """真库自检：只断言**随批次推进自动成立**的不变量，不记账。

    这里曾写着「21 套仍是 legacy_unverified、六个批次仍是 planned」——那不是不变量，
    是批次导入开始前的一张快照，b01 一落地就红。凡「每导一批就得来改一次」的断言都是
    账目而非不变量；下面两条都由 manifest 自身派生，b02–b06 落地时无需任何改动。
    """

    @classmethod
    def setUpClass(cls):
        cls.root = ROOT.parent.parent.parent
        cls.manifest = load_manifest(ROOT / "source-manifest.json")

    def provenance_papers(self):
        return {
            paper["paper_id"] for paper in self.manifest["papers"]
            if (self.root / status_core.provenance_path(paper)).is_file()
        }

    def test_batch_report_validity_is_checked_once_per_batch(self):
        selected_batches = [
            batch for batch in self.manifest["batches"]
            if len(batch["paper_ids"]) > 1
        ][:2]
        paper_ids = [
            paper_id for batch in selected_batches for paper_id in batch["paper_ids"]
        ]
        report_probe_calls = []

        loaded = load_provenance_facts(
            self.root,
            self.manifest,
            paper_ids,
            artifacts_state=lambda *_: "current",
            review_state=lambda *_: ("passed", "current"),
            batch_report_valid=lambda _root, _manifest, paper_id: (
                report_probe_calls.append(paper_id) or True
            ),
        )

        self.assertEqual(set(loaded), set(paper_ids))
        self.assertEqual(len(report_probe_calls), len(selected_batches))

    def test_provenance_files_exactly_cover_the_non_planned_batches(self):
        """有 provenance 的卷 == 已离开 `planned` 的批次里的卷。

        `import_batch()` 整批写 provenance 并把批次推出 `planned`，两侧因此恒等；
        任一侧单独漂移都说明有人绕过了导入事务。
        """
        expected = {
            paper_id for batch in self.manifest["batches"]
            if batch["status"] != "planned" for paper_id in batch["paper_ids"]
        }
        self.assertEqual(self.provenance_papers(), expected)

    def test_no_paper_advances_beyond_planning_without_provenance(self):
        """状态不得先于证据：离开初始/计划态的卷必有 provenance 文件。

        新转录卷注册时先进入 `planned`，随后才由三角色工作流建立 provenance；把
        `planned` 也视为已推进会让合法注册事务在证据尚未导入时立即自相矛盾。
        """
        advanced = {
            paper["paper_id"] for paper in self.manifest["papers"]
            if paper["production_state"] not in ("legacy_unverified", "planned")
        }
        self.assertLessEqual(advanced, self.provenance_papers())

    def test_the_generated_artifacts_are_current(self):
        for paper in self.manifest["papers"][:2]:
            with self.subTest(paper_id=paper["paper_id"]):
                self.assertEqual(
                    provenance.default_artifacts_state(
                        self.root, self.manifest, paper["paper_id"]
                    ),
                    "current",
                )

    def test_the_2017_pair_agrees_on_every_shared_question_text(self):
        """真库实证：2017 理/文的 q23 题面逐字相同，摘要必须相同。

        q22 在修复前就已同值（题间的 `---` 两卷一样），它是对照组——证明「其余题号本来
        就正常」，问题只出在末题吸收了文末页脚。
        """
        digests = {}
        for suffix in ("science", "arts"):
            paper = next(
                item for item in self.manifest["papers"]
                if item["paper_id"] == "gk-2017-regular-national-1-" + suffix
            )
            digests[suffix] = question_text_digests(
                (self.root / paper["source_files"]["questions"]).read_text(
                    encoding="utf-8"
                )
            )
        self.assertEqual(digests["science"][22], digests["arts"][22])
        self.assertEqual(digests["science"][23], digests["arts"][23])
        # 两卷的其余题面确实不同——修复不得把所有题号都抹平成同值。
        self.assertNotEqual(digests["science"][1], digests["arts"][1])

    def test_every_paper_last_question_digest_drops_its_footer(self):
        """逐卷核对：末题摘要等于显式剥除合法文末引用块后的题面摘要。"""
        for paper in self.manifest["papers"]:
            with self.subTest(paper_id=paper["paper_id"]):
                text = (self.root / paper["source_files"]["questions"]).read_text(
                    encoding="utf-8"
                )
                blocks = parse_question_blocks(text)
                last = blocks[-1]
                expected = hashlib.sha256(
                    provenance.question_block_text(last, strip_footer=True).encode("utf-8")
                ).hexdigest()
                self.assertEqual(question_text_digests(text)[last.number], expected)

    def test_the_cached_states_match_the_recomputed_ones(self):
        report = check_batch(
            ROOT / "source-manifest.json", ROOT / "missing-issues.md", None,
        )
        manifest = load_manifest(ROOT / "source-manifest.json")
        self.assertEqual(report["problems"], [])
        self.assertEqual(report["papers"], len(manifest["papers"]))


if __name__ == "__main__":
    unittest.main()

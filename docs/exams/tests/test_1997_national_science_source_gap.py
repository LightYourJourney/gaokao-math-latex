"""1997 全国理科 Q23(3) 的原卷缺符号必须阻止误报来源与答案已核。"""

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAPER_ID = "gk-1997-regular-national-science"
QUESTIONS = ROOT.parent / "1997" / "1997_数学真题_全国理_试题.md"
ANSWER_KEY = ROOT.parent / "1997" / "1997_数学真题_全国理_答案要点.md"
PROJECT = ROOT / "1997_全国卷_理科"
ISSUES = ROOT / "missing-issues.md"

sys.path.insert(0, str(ROOT / "tools"))
import issues
import provenance
import solution_sources
import status


class NationalScience1997SourceGapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        cls.question_text = QUESTIONS.read_text(encoding="utf-8")
        cls.answer_text = ANSWER_KEY.read_text(encoding="utf-8")
        cls.questions = solution_sources.parse_question_blocks(cls.question_text)
        cls.question = next(item for item in cls.questions if item.number == 23)
        cls.provenance_doc = json.loads((PROJECT / "provenance.json").read_text(encoding="utf-8"))
        cls.provenance_question = next(
            item for item in cls.provenance_doc["questions"]
            if item["printed_number"] == 23
        )

    def test_q23_part3_preserves_the_missing_source_relation(self):
        part3 = self.question.body.split("（3）", 1)[1].split("（4）", 1)[0]
        part1 = self.question.body.split("（1）", 1)[1].split("（2）", 1)[0]
        self.assertIn("【原卷缺关系符号】", part3)
        self.assertNotIn(r"\perp", part3)
        self.assertIn(r"\perp", part1)

    def test_q23_transcription_and_answer_blockers_match_current_provenance(self):
        linked_issues = [
            item for item in issues.load_issues(ISSUES)
            if item.get("paper_id") == PAPER_ID
            and item.get("question_id") == f"{PAPER_ID}-q23"
        ]
        by_type = {item["type"]: item for item in linked_issues}
        self.assertEqual(set(by_type), {"transcription-ambiguous", "answer-missing"})
        self.assertTrue(all(item["status"] == "open" for item in by_type.values()))
        self.assertTrue(all(item["impact"] == "blocks_completion" for item in by_type.values()))
        self.assertEqual(
            set(self.provenance_question["issue_ids"]),
            {item["issue_id"] for item in by_type.values()},
        )
        self.assertEqual(self.provenance_question["transcription_review"]["result"], "failed")
        self.assertEqual(self.provenance_question["answer_evidence"]["grade"], "U")
        self.assertEqual(
            self.provenance_question["question_text_sha256"],
            provenance.question_text_digests(self.question_text)[23],
        )
        self.assertEqual(
            self.provenance_question["answer_sha256"],
            provenance.answer_digests(PAPER_ID, self.answer_text)[23],
        )

    def test_manifest_and_consumers_keep_the_paper_blocked(self):
        paper = next(item for item in self.manifest["papers"] if item["paper_id"] == PAPER_ID)
        self.assertEqual(paper["production_state"], "blocked")
        loaded = provenance.load_provenance_facts(
            ROOT, self.manifest, [PAPER_ID], issues_path=ISSUES
        )[PAPER_ID]
        derived = status.derive_status(status.paper_facts(
            PAPER_ID, build="succeeded", build_currency="current", **loaded
        ))
        self.assertEqual(derived, "blocked")
        question_tex = (PROJECT / "questions.tex").read_text(encoding="utf-8")
        short_tex = (PROJECT / "answers_short.tex").read_text(encoding="utf-8")
        self.assertIn("原卷缺关系符号", question_tex)
        self.assertIn("待核", short_tex)
        index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        paper_index = next(item for item in index["papers"] if item["id"] == PAPER_ID)
        self.assertIn("第 23 题（3）", paper_index["note"])
        self.assertIn("待核", paper_index["note"])


if __name__ == "__main__":
    unittest.main()

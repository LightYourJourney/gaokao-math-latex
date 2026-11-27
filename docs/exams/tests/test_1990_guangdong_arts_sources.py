"""1990 广东文史类来源与规范稿绑定检查（canonical 阶段，C 级卷内答案）。"""

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1990_广东卷_文科"
QUESTIONS = ROOT.parent / "1990/1990_广东_试题.md"
ANSWERS = ROOT.parent / "1990/1990_广东_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class GuangdongArts1990SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))
        cls.questions = solution_sources.parse_question_blocks(
            QUESTIONS.read_text(encoding="utf-8")
        )
        cls.answers = solution_sources.parse_answer_points(
            ANSWERS.read_text(encoding="utf-8")
        )

    def test_source_identity_is_bound_to_the_fixed_scan(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(
            s for s in manifest["sources"] if s["source_id"] == self.record["source_id"]
        )
        self.assertEqual(source["upstream_path"], "普通高考/1990/1990广东文.pdf")
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["artifact"]["page_count"], 7)
        self.assertEqual(source["paper_id"], "gk-1990-regular-guangdong-arts")

    def test_all_30_slots_align(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 31)))
        self.assertEqual([a.number for a in self.answers], list(range(1, 31)))
        self.assertEqual(
            [q.subparts for q in self.questions],
            [a.subparts for a in self.answers],
        )

    def test_choice_key_and_partial_answer_provenance(self):
        letters = [a.answer_for(None).strip("$。") for a in self.answers[:25]]
        self.assertEqual(
            letters,
            list("ADADBBAABCCCDBDCDBCBACBCD"),
        )
        self.assertEqual(
            [item["question_number"] for item in self.record["source_issues"]],
            [11, 28, 29, 30],
        )
        self.assertEqual(self.record["answer_provenance"], "source-provided-partial")
        self.assertIsNone(self.record["official_answer"])

    def test_q26_coefficient_is_minus_ten(self):
        text = self.answer_for(26, 2)
        self.assertIn("-10", text)

    def test_two_figures_are_registered(self):
        figures = self.record["figure_files"]
        self.assertEqual(len(figures), 2)
        for figure in figures:
            file = PROJECT / figure["path"]
            self.assertTrue(file.is_file(), str(file))
            self.assertEqual(
                hashlib.sha256(file.read_bytes()).hexdigest(), figure["sha256"]
            )

    def test_canonical_hashes(self):
        self.assertEqual(
            self.record["canonical_question_sha256"],
            hashlib.sha256(QUESTIONS.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            self.record["canonical_answer_sha256"],
            hashlib.sha256(ANSWERS.read_bytes()).hexdigest(),
        )

    def answer_for(self, number, subpart):
        record = self.answers[number - 1]
        return record.answer_for(subpart)


if __name__ == "__main__":
    unittest.main()

"""1995 全国理科来源与规范稿绑定检查（canonical 阶段，D 级答案）。"""

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1995_全国卷_理科"
QUESTIONS = ROOT.parent / "1995/1995_数学真题_全国理_试题.md"
ANSWERS = ROOT.parent / "1995/1995_数学真题_全国理_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class NationalScience1995SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))
        cls.questions = solution_sources.parse_question_blocks(
            QUESTIONS.read_text(encoding="utf-8")
        )
        cls.answers = solution_sources.parse_answer_points(
            ANSWERS.read_text(encoding="utf-8")
        )

    def test_source_identity_and_answer_grade(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(
            s for s in manifest["sources"] if s["source_id"] == self.record["source_id"]
        )
        self.assertEqual(source["upstream_path"], "普通高考/1995/1995全国理.pdf")
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["artifact"]["page_count"], 1)
        self.assertFalse(self.record["source_has_answers"])
        self.assertEqual(
            self.record["answer_provenance"], "project-derived-double-solved"
        )
        self.assertEqual(source["paper_id"], "gk-1995-regular-national-1-science")

    def test_all_26_slots_align(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 27)))
        self.assertEqual([a.number for a in self.answers], list(range(1, 27)))

    def test_choice_key_and_source_issues(self):
        letters = [a.answer_for(None).strip("$。") for a in self.answers[:15]]
        self.assertEqual(letters, list("CBCBDDBCADBCADA"))
        self.assertEqual(
            [item["question_number"] for item in self.record["source_issues"]],
            [14, 23],
        )

    def test_four_figures_are_registered(self):
        figures = self.record["figure_files"]
        self.assertEqual(len(figures), 4)
        for figure in figures:
            file = PROJECT / figure["path"]
            self.assertTrue(file.is_file(), str(file))
            self.assertEqual(
                hashlib.sha256(file.read_bytes()).hexdigest(), figure["sha256"]
            )
            text = file.read_text(encoding="utf-8")
            for command in (r"\includegraphics", r"\input", r"\write18"):
                self.assertNotIn(command, text)

    def test_canonical_hashes(self):
        self.assertEqual(
            self.record["canonical_question_sha256"],
            hashlib.sha256(QUESTIONS.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            self.record["canonical_answer_sha256"],
            hashlib.sha256(ANSWERS.read_bytes()).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()

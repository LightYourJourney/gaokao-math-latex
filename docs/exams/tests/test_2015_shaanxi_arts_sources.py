"""2015 陕西文史类来源与规范稿绑定检查（D 级双解答案）。"""

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "2015_陕西卷_文科"
QUESTIONS = ROOT.parent / "2015/2015_数学真题_陕西文_试题.md"
ANSWERS = ROOT.parent / "2015/2015_数学真题_陕西文_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class ShaanxiArts2015SourceTests(unittest.TestCase):
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
        self.assertEqual(source["upstream_path"], "普通高考/2015/2015陕西文.pdf")
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["artifact"]["page_count"], 2)
        self.assertFalse(self.record["source_has_answers"])
        self.assertEqual(self.record["answer_provenance"], "project-derived-double-solved")

    def test_all_24_slots_align(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 25)))
        self.assertEqual([a.number for a in self.answers], list(range(1, 25)))

    def test_choice_key_and_two_corrections(self):
        letters = [a.answer_for(None).strip("$。") for a in self.answers[:12]]
        self.assertEqual(letters, list("ACBCDADBB CDC".replace(" ", "")))
        self.assertIn(r"\dfrac{7}{8}", self.answers[18].answer_for(2))
        self.assertIn("b=1", self.answers[23].answer_for(1).replace(" ", ""))
        self.assertIn("4", self.answers[23].answer_for(2))

    def test_seven_figures_are_registered(self):
        figures = self.record["figure_files"]
        self.assertEqual(len(figures), 7)
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


if __name__ == "__main__":
    unittest.main()

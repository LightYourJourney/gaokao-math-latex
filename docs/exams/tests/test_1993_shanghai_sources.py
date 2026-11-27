"""1993 上海卷来源与规范稿绑定检查（canonical 阶段）。"""

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1993_上海卷"
QUESTIONS = ROOT.parent / "1993/1993_上海_试题.md"
ANSWERS = ROOT.parent / "1993/1993_上海_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Shanghai1993SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((PROJECT / "来源校对.json").read_text(encoding="utf-8"))
        cls.questions = solution_sources.parse_question_blocks(
            QUESTIONS.read_text(encoding="utf-8")
        )
        cls.answers = solution_sources.parse_answer_points(
            ANSWERS.read_text(encoding="utf-8")
        )

    def test_source_identity_is_bound_and_warnings_are_recorded(self):
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        source = next(
            s for s in manifest["sources"] if s["source_id"] == self.record["source_id"]
        )
        self.assertEqual(source["upstream_path"], "普通高考/1993/1993上海.pdf")
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["artifact"]["page_count"], 7)
        self.assertEqual(source["paper_id"], "gk-1993-regular-shanghai")
        self.assertEqual(self.record["review_status"], "reviewed")
        self.assertEqual(
            [item["question_number"] for item in self.record["source_issues"]],
            [24, 26],
        )

    def test_all_26_slots_align(self):
        self.assertEqual([q.number for q in self.questions], list(range(1, 27)))
        self.assertEqual([a.number for a in self.answers], list(range(1, 27)))
        self.assertEqual(
            [q.subparts for q in self.questions],
            [a.subparts for a in self.answers],
        )

    def test_choice_key_and_no_leaked_notes(self):
        letters = [a.answer_for(None).strip("$。") for a in self.answers[10:20]]
        self.assertEqual(letters, list("CB DCDBACBC".replace(" ", "")))
        text = QUESTIONS.read_text(encoding="utf-8")
        self.assertNotIn("得 $CR=a-AR$", text)
        self.assertNotIn("x_0^2=a^2(1-y_0^2)", text)

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

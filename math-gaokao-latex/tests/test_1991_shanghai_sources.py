"""1991 上海卷来源与规范稿绑定检查（canonical 阶段）。"""

import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "1991_上海卷"
QUESTIONS = ROOT.parent / "1991/1991_上海_试题.md"
ANSWERS = ROOT.parent / "1991/1991_上海_答案要点.md"
sys.path.insert(0, str(ROOT / "tools"))
import solution_sources


class Shanghai1991SourceTests(unittest.TestCase):
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
        self.assertEqual(source["upstream_path"], "普通高考/1991/1991上海.pdf")
        self.assertEqual(source["artifact"]["sha256"], self.record["pdf_sha256"])
        self.assertEqual(source["git_blob_oid"], self.record["git_blob_oid"])
        self.assertEqual(source["artifact"]["page_count"], 7)
        self.assertEqual(source["paper_id"], "gk-1991-regular-shanghai")
        self.assertEqual(source["paper_relation"], "canonical")

    def test_all_27_question_and_answer_slots_align(self):
        expected = list(range(1, 28))
        self.assertEqual([q.number for q in self.questions], expected)
        self.assertEqual([a.number for a in self.answers], expected)
        self.assertEqual(
            [q.subparts for q in self.questions],
            [a.subparts for a in self.answers],
        )

    def test_q8_source_conflict_is_recorded_not_smoothed(self):
        self.assertEqual(self.record["paper_id"], "gk-1991-regular-shanghai")
        self.assertEqual(self.record["review_status"], "reviewed")
        self.assertTrue(self.record["canonical_question_source_ready"])
        self.assertIn("ISSUE-1178", self.record["issue_ids"])
        answer = self.answers[7].answer_for(None)
        self.assertIn("无常数项", answer)
        self.assertIn("60", answer)
        manifest = json.loads((ROOT / "source-manifest.json").read_text(encoding="utf-8"))
        paper = next(
            p for p in manifest["papers"] if p["paper_id"] == "gk-1991-regular-shanghai"
        )
        self.assertEqual(paper["production_state"], "blocked")
        self.assertIn("ISSUE-1178", paper["issue_ids"])

    def test_four_vector_sources_exist_without_raster_or_external_dependencies(self):
        figures = self.record["figure_files"]
        self.assertEqual(len(figures), 4)
        for figure in figures:
            file = PROJECT / figure["path"]
            self.assertTrue(file.is_file(), str(file))
            self.assertEqual(
                hashlib.sha256(file.read_bytes()).hexdigest(), figure["sha256"]
            )
            text = file.read_text(encoding="utf-8")
            self.assertEqual(text.count(r"\begin{tikzpicture}"), 1)
            self.assertEqual(text.count(r"\end{tikzpicture}"), 1)
            for command in (
                r"\includegraphics",
                r"\input",
                r"\write18",
                r"\documentclass",
            ):
                self.assertNotIn(command, text)
        self.assertEqual(
            [Path(f["path"]).name for f in figures],
            [
                "f1991_shanghai_q14_choices.tex",
                "f1991_shanghai_q24_tetrahedron.tex",
                "f1991_shanghai_q26_parabola.tex",
                "f1991_shanghai_q27_triangle.tex",
            ],
        )

    def test_canonical_hashes_are_current(self):
        for key, path in (
            ("canonical_question_sha256", QUESTIONS),
            ("canonical_answer_sha256", ANSWERS),
        ):
            self.assertEqual(
                self.record.get(key), hashlib.sha256(path.read_bytes()).hexdigest()
            )


if __name__ == "__main__":
    unittest.main()

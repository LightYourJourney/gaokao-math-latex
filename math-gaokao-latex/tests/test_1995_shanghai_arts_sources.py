"""Source-bound completeness checks for the 1995 Shanghai arts paper."""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_ID = "gk-1995-regular-shanghai-arts"
SOURCE_ID = "src-ef7576922eed4ed30b369569c10911cf87356d83988aa0d9bdaf82927061e059"
PDF_SHA256 = "7a54c35368fb8de8e0842c2da263affa0115f5d1d9afa9798322e3c389a023c0"
PAPER = ROOT / "1995_上海卷_文史类"
QUESTIONS = ROOT.parent / "1995" / "1995_数学真题_上海文_试题.md"
ANSWERS = ROOT.parent / "1995" / "1995_数学真题_上海文_答案要点.md"
SOLUTIONS = ROOT.parent / "1995" / "1995_数学真题_上海文_解析正文.md"
RECORD = PAPER / "来源校对.json"
MANIFEST = ROOT / "source-manifest.json"


class ShanghaiArts1995SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.source = next(
            (s for s in cls.manifest["sources"] if s.get("source_id") == SOURCE_ID), None
        )
        cls.record = json.loads(RECORD.read_text(encoding="utf-8")) if RECORD.is_file() else {}
        cls.questions = QUESTIONS.read_text(encoding="utf-8") if QUESTIONS.is_file() else ""
        cls.answers = ANSWERS.read_text(encoding="utf-8") if ANSWERS.is_file() else ""
        cls.solutions = SOLUTIONS.read_text(encoding="utf-8") if SOLUTIONS.is_file() else ""

    def test_source_identity_and_canonical_bidirectional_binding(self):
        self.assertIsNotNone(self.source)
        self.assertTrue(RECORD.is_file())
        self.assertEqual(self.source["source_state"], "ready")
        self.assertEqual(self.source["paper_id"], PAPER_ID)
        self.assertEqual(self.source["paper_relation"], "canonical")
        self.assertEqual(self.source["artifact"]["sha256"], PDF_SHA256)
        self.assertEqual(self.source["artifact"]["page_count"], 7)
        self.assertEqual(self.record["source_id"], SOURCE_ID)
        self.assertEqual(self.record["paper_id"], PAPER_ID)
        self.assertEqual(self.record["pdf_sha256"], PDF_SHA256)
        self.assertEqual(self.record["pdf_sha256"], self.source["artifact"]["sha256"])
        self.assertEqual(self.record["git_blob_oid"], self.source["git_blob_oid"])
        self.assertEqual(self.record["question_draft_sha256"], hashlib.sha256(QUESTIONS.read_bytes()).hexdigest())
        self.assertEqual(self.record["answers_draft_sha256"], hashlib.sha256(ANSWERS.read_bytes()).hexdigest())
        self.assertEqual(self.record["solutions_draft_sha256"], hashlib.sha256(SOLUTIONS.read_bytes()).hexdigest())

    def test_question_and_variant_coverage_matches_printed_structure(self):
        self.assertTrue(self.questions)
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.questions, re.MULTILINE)]
        self.assertEqual(numbers, list(range(1, 26)))
        self.assertEqual(self.record["question_count"], 25)
        self.assertEqual(self.record["prompt_variant_count"], 30)
        self.assertEqual(len(self.record["question_sources"]), 25)
        self.assertEqual(
            [q["question_number"] for q in self.record["question_sources"]], list(range(1, 26))
        )
        for track in ("A₁", "B₁", "A₂", "B₂"):
            self.assertIn(track, self.questions)
        self.assertIn("附卷内「数学试卷答案及评分标准」", self.questions)
        self.assertIn("出版者、版次及答案是否为官方版本未核实", self.questions)

    def test_arts_specific_stems_and_source_answers_are_preserved(self):
        required = (
            "上海数学试卷（文史类）",
            r"y=3x^2+1",
            r"y=\lg\sqrt{10^x-2}",
            r"y=\sin\dfrac x2+\cos\dfrac x2",
            r"z_1+z_2=i",
            r"f(x)g(x)+mx+n=x^3",
            r"(x-mq^k)^2+(y-nq^k)^2=r_k^2",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.questions)
        self.assertEqual([int(n) for n in re.findall(r"^\*\*(\d+)．\*\*", self.answers, re.MULTILINE)], list(range(1, 26)))
        self.assertEqual([int(n) for n in re.findall(r"^### 第 (\d+) 题", self.solutions, re.MULTILINE)], list(range(1, 26)))
        self.assertIn("固定扫描件中所载答案", self.answers)
        self.assertIn("出版者、版次和答案的官方身份尚未核", self.answers)
        self.assertIn("-\\dfrac{\\sqrt3}{2}+\\dfrac12i", self.answers)

    def test_question_source_pages_and_figure_bindings_are_complete(self):
        self.assertEqual(self.record["question_type_ranges"], [
            {"type": "single-choice", "first": 1, "last": 8},
            {"type": "fill-in", "first": 9, "last": 20},
            {"type": "solution", "first": 21, "last": 25},
        ])
        figures = self.record["figure_files"]
        self.assertEqual({f["question_number"] for f in figures}, {6, 21, 23})
        self.assertEqual(len(figures), 4)
        for figure in figures:
            path = PAPER / figure["path"]
            linked = self.solutions if figure["role"] == "solution-construction" else self.questions
            self.assertTrue(path.is_file(), figure["path"])
            self.assertEqual(path.suffix, ".tex")
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), figure["sha256"])
            self.assertIn(f"](../math-gaokao-latex/{PAPER.name}/{figure['path']})", linked)
        self.assertEqual(self.record["source_has_answers"], True)
        self.assertIsNone(self.record["official_answer"])
        self.assertEqual(self.record["answer_provenance"], "source-provided-unverified")


if __name__ == "__main__":
    unittest.main()

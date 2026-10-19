import csv
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2015/2015_数学真题_湖南理_试题.md"
FIGURES = ROOT / "2015/2015_数学真题_湖南理_图形清单.md"
REVIEW = ROOT / "2015/2015_湖南理科_来源校对.json"
MANIFEST = ROOT / "math-gaokao-latex/manifest.csv"


class HunanScienceTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.figures = FIGURES.read_text(encoding="utf-8")
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))

    def test_manifest_source_is_ready_unbound_and_hash_matches_transcript_record(self):
        source_id = self.review["source"]["source_id"]
        with MANIFEST.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        source = next(row for row in rows if row["source_id"] == source_id)

        self.assertEqual(source["source_state"], "ready")
        self.assertEqual(source["paper_id"], "")
        self.assertEqual(source["source_sha256"], self.review["source"]["sha256"])
        self.assertEqual(self.review["source"]["pdf_pages"], 2)
        self.assertEqual(self.review["source"]["printed_pages"], [955, 956])

    def test_all_21_questions_are_present_in_three_source_sections(self):
        numbers = [int(n) for n in re.findall(r"^### 第 (\d+) 题", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 22)))
        self.assertEqual(self.review["question_transcript"]["question_numbers"], numbers)
        self.assertEqual(self.review["question_transcript"]["question_types"], {
            "single_choice": list(range(1, 11)),
            "fill_in": list(range(11, 16)),
            "written_response": list(range(16, 22)),
        })

    def test_high_risk_source_expressions_and_unresolved_answer_boundary_are_recorded(self):
        for expression in (
            r"2x-y\leqslant 1",
            r"x^{\frac32}",
            r"\overrightarrow{PA}+\overrightarrow{PB}+\overrightarrow{PC}",
            r"3S_1,2S_2,S_3",
            r"\overrightarrow{AC}\) 与 \(\overrightarrow{BD}",
            r"\dfrac{1}{\sqrt{e^2-1}}",
        ):
            self.assertIn(expression, self.transcript)
        self.assertIsNone(self.review["official_answer"]["value"])
        self.assertEqual(self.review["official_answer"]["status"], "not-present-in-fixed-source")
        self.assertEqual(self.review["generated_solution"]["status"], "not-started")

    def test_every_original_figure_is_in_inventory_and_not_committed_as_raster(self):
        self.assertIn("| 3 | 955 |", self.figures)
        for q in (7, 10, 12, "16A", 19):
            self.assertIn(f"| {q} |", self.figures)
        self.assertFalse(self.review["figures"]["source_raster_committed"])
        self.assertEqual(self.review["figures"]["vector_reconstruction_status"], "pending")


if __name__ == "__main__":
    unittest.main()

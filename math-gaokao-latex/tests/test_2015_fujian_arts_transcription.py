import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TRANSCRIPT = ROOT / "2015/2015_数学真题_福建文_试题.md"
REVIEW = ROOT / "2015/2015_福建文科_来源校对.json"
FIGURES = ROOT / "2015/2015_数学真题_福建文_图表清单.md"


class FujianArtsTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.transcript = TRANSCRIPT.read_text(encoding="utf-8")
        cls.review = json.loads(REVIEW.read_text(encoding="utf-8"))
        cls.figures = FIGURES.read_text(encoding="utf-8")

    def test_source_identity_and_transcription_hash(self):
        self.assertEqual(
            self.review["source"]["sha256"],
            "4ca0fbac9967c9a73bdb0bc00eceb3d0181c57285ee72fc260a02c9c24172383",
        )
        self.assertEqual(self.review["source"]["page_count"], 2)
        self.assertEqual(self.review["source"]["printed_pages"], [945, 946])
        self.assertIsNone(self.review["paper_id"])
        self.assertIsNone(self.review["official_answer"])
        self.assertEqual(
            hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
            self.review["transcription"]["sha256"],
        )

    def test_all_questions_are_present_in_their_source_order(self):
        numbers = [int(n) for n in re.findall(r"^\*\*(\d+)．", self.transcript, re.M)]
        self.assertEqual(numbers, list(range(1, 23)))
        self.assertEqual(self.review["transcription"]["question_count"], 22)
        self.assertEqual(self.review["transcription"]["question_types"], {
            "single_choice": list(range(1, 11)),
            "fill_in": list(range(11, 17)),
            "written_response": list(range(17, 23)),
        })

    def test_high_risk_formula_and_condition_strings_are_preserved(self):
        for expression in (
            r"\sin\alpha=-\dfrac{5}{13}",
            r"x-2y+2\geqslant0",
            r"\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1",
            r"k\sin x\cos x<x",
            r"b_n=2^{a_n-2}+n",
            r"10\sqrt3\sin\dfrac{x}{2}\cos\dfrac{x}{2}",
            r"f(x)=\ln x-\dfrac{(x-1)^2}{2}",
        ):
            self.assertIn(expression, self.transcript)

    def test_diagrams_and_table_are_accounted_for_without_raster_assets(self):
        self.assertEqual(
            self.review["figures_and_tables"]["items"],
            ["q4-flowchart", "q8-shaded-region", "q9-three-views", "q18-frequency-table", "q19-parabola-geometry", "q20-solid-geometry"],
        )
        self.assertIn("待重建为 TikZ", self.figures)
        self.assertFalse(self.review["figures_and_tables"]["raster_source_committed"])

    def test_inline_math_delimiters_are_balanced_in_transcript_and_inventory(self):
        for text in (self.transcript, self.figures):
            self.assertEqual(text.count(r"\("), text.count(r"\)"))
            self.assertGreater(text.count(r"\("), 0)


if __name__ == "__main__":
    unittest.main()

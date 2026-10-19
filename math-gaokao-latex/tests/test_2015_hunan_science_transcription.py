import csv
import hashlib
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
        self.assertEqual(
            hashlib.sha256(TRANSCRIPT.read_bytes()).hexdigest(),
            self.review["question_transcript"]["sha256"],
        )

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
        self.assertEqual(
            self.review["generated_solution"]["status"],
            "main-session-draft-awaiting-blind-review",
        )

    def test_stem_leaf_data_is_transcribed_without_omissions_or_reordering(self):
        body = re.search(
            r"\\begin\{array\}\{c\|l\}\s*(.*?)\\end\{array\}",
            self.transcript,
            re.S,
        ).group(1)
        rows = {}
        for line in body.splitlines():
            if "&" in line:
                stem, leaves = line.split("&", 1)
                rows[stem.strip()] = re.findall(r"\d+", leaves)
        self.assertEqual(rows, {
            "13": ["0", "0", "3", "4", "5", "6", "6", "8", "8", "8", "9"],
            "14": ["1", "1", "1", "2", "2", "2", "3", "3", "4", "4", "5", "5", "5", "6", "6", "7", "8"],
            "15": ["0", "1", "2", "2", "3", "3", "3"],
        })
        self.assertEqual(sum(map(len, rows.values())), 35)

    def test_every_original_figure_is_in_inventory_and_not_committed_as_raster(self):
        self.assertIn("| 3 | 955 |", self.figures)
        for q in (7, 10, 12, "16A", 19):
            self.assertIn(f"| {q} |", self.figures)
        self.assertNotIn("| 待制作 |", self.figures)
        self.assertEqual(self.figures.count("草稿已建、smoke编译；待逐项对照原图复核"), 5)
        self.assertIn("题面已录入35叶；待独立逐叶复核", self.figures)
        self.assertFalse(self.review["figures"]["source_raster_committed"])
        self.assertEqual(
            self.review["figures"]["vector_reconstruction_status"],
            "draft-smoke-compiled-awaiting-page-review",
        )
        vector_dir = ROOT / self.review["figures"]["vector_source_directory"]
        vector_files = sorted(vector_dir.glob("*.tex"))
        self.assertEqual(len(vector_files), 5)
        self.assertFalse(list(vector_dir.glob("*.png")))
        self.assertFalse(list(vector_dir.glob("*.jpg")))
        self.assertFalse(list(vector_dir.glob("*.jpeg")))
        for name, expected_sha in self.review["figures"]["vector_sources"].items():
            path = next(p for p in vector_files if f"_{name.lower()}_" in p.name)
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected_sha)


if __name__ == "__main__":
    unittest.main()
